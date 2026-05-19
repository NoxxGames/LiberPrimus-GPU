"""Build and export Stage 4N stego/audio positive-control readiness records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root
from libreprimus.stego_positive_controls.cache_policy import build_cache_record
from libreprimus.stego_positive_controls.expected_outputs import build_expected_output_record
from libreprimus.stego_positive_controls.fixture_classifier import classify_audio_fixture, classify_outguess_fixture
from libreprimus.stego_positive_controls.loaders import (
    load_yaml_records,
    write_json,
    write_yaml_document,
    write_yaml_records,
)
from libreprimus.stego_positive_controls.models import (
    DEFAULT_AUDIO_READINESS_OUT,
    DEFAULT_AUDIO_SOURCES,
    DEFAULT_CACHE_DIR,
    DEFAULT_EXPECTED_OUTPUT_OUT,
    DEFAULT_FIXTURE_CACHE_OUT,
    DEFAULT_MANIFEST_READINESS,
    DEFAULT_OUT_DIR,
    DEFAULT_OUTGUESS_ARTIFACTS,
    DEFAULT_OUTGUESS_READINESS_OUT,
    DEFAULT_OUTGUESS_SOURCES,
    DEFAULT_SOURCE_FETCHES,
    DEFAULT_SOURCE_HEALTH,
    DEFAULT_SOURCE_LOCKS,
    DEFAULT_SOURCE_LOCK_SUMMARY,
    DEFAULT_SUMMARY_OUT,
    DEFAULT_TOOLCHAIN_OUT,
    DEFAULT_TOOLCHAIN_REQUIREMENTS,
)
from libreprimus.stego_positive_controls.readiness import build_readiness_record
from libreprimus.stego_positive_controls.summary import summarize_positive_controls
from libreprimus.stego_positive_controls.synthetic_controls import synthetic_outguess_controls
from libreprimus.stego_positive_controls.toolchain_detection import detect_toolchains


def build_stego_positive_controls(
    *,
    out_dir: Path = repo_root() / DEFAULT_OUT_DIR,
    cache_dir: Path = repo_root() / DEFAULT_CACHE_DIR,
    outguess_sources: Path = repo_root() / DEFAULT_OUTGUESS_SOURCES,
    audio_sources: Path = repo_root() / DEFAULT_AUDIO_SOURCES,
    source_health: Path = repo_root() / DEFAULT_SOURCE_HEALTH,
    toolchain_requirements: Path = repo_root() / DEFAULT_TOOLCHAIN_REQUIREMENTS,
    source_locks: Path = repo_root() / DEFAULT_SOURCE_LOCKS,
    source_fetches: Path = repo_root() / DEFAULT_SOURCE_FETCHES,
    source_lock_summary: Path = repo_root() / DEFAULT_SOURCE_LOCK_SUMMARY,
    outguess_artifacts: Path = repo_root() / DEFAULT_OUTGUESS_ARTIFACTS,
    manifest_readiness: Path = repo_root() / DEFAULT_MANIFEST_READINESS,
    outguess_readiness_out: Path = repo_root() / DEFAULT_OUTGUESS_READINESS_OUT,
    audio_readiness_out: Path = repo_root() / DEFAULT_AUDIO_READINESS_OUT,
    fixture_cache_out: Path = repo_root() / DEFAULT_FIXTURE_CACHE_OUT,
    expected_output_out: Path = repo_root() / DEFAULT_EXPECTED_OUTPUT_OUT,
    toolchain_out: Path = repo_root() / DEFAULT_TOOLCHAIN_OUT,
    summary_out: Path = repo_root() / DEFAULT_SUMMARY_OUT,
    allow_network: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Build committed Stage 4N readiness records and ignored generated reports."""

    del allow_network, allow_warnings, source_fetches, source_lock_summary
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    source_lock_records = load_yaml_records(source_locks)
    source_health_records = load_yaml_records(source_health)
    toolchain_requirement_records = load_yaml_records(toolchain_requirements)
    manifest_readiness_records = load_yaml_records(manifest_readiness)
    toolchain_records = detect_toolchains()

    outguess_records = load_yaml_records(outguess_sources)
    stage3v_records = [
        record for record in load_yaml_records(outguess_artifacts) if record.get("source_class") != "synthetic_control"
    ]
    synthetic_records = synthetic_outguess_controls()
    all_outguess_records = outguess_records + stage3v_records + synthetic_records
    audio_records = load_yaml_records(audio_sources)

    outguess_readiness: list[dict[str, Any]] = []
    audio_readiness: list[dict[str, Any]] = []
    cache_records: list[dict[str, Any]] = []
    expected_output_records: list[dict[str, Any]] = []

    for record in all_outguess_records:
        category = classify_outguess_fixture(record)
        synthetic = category.startswith("synthetic_")
        cache_record = build_cache_record(record, category=category, cache_dir=cache_dir, source_kind="outguess")
        expected_record = build_expected_output_record(record, category=category, synthetic=synthetic)
        readiness_record = build_readiness_record(
            _with_source_lock(record, source_lock_records),
            category=category,
            cache_record=cache_record,
            expected_record=expected_record,
            toolchain_records=toolchain_records,
            record_type="stego_positive_control_readiness",
        )
        outguess_readiness.append(readiness_record)
        cache_records.append(cache_record)
        expected_output_records.append(expected_record)

    for record in audio_records:
        category = classify_audio_fixture(record)
        cache_record = build_cache_record(record, category=category, cache_dir=cache_dir, source_kind="audio")
        expected_record = build_expected_output_record(record, category=category, synthetic=False)
        readiness_record = build_readiness_record(
            _with_source_lock(record, source_lock_records),
            category=category,
            cache_record=cache_record,
            expected_record=expected_record,
            toolchain_records=toolchain_records,
            record_type="audio_positive_control_readiness",
        )
        audio_readiness.append(readiness_record)
        cache_records.append(cache_record)
        expected_output_records.append(expected_record)

    summary = summarize_positive_controls(
        outguess_readiness=outguess_readiness,
        audio_readiness=audio_readiness,
        fixture_cache=cache_records,
        expected_outputs=expected_output_records,
        toolchain=toolchain_records,
    )
    summary["source_health_records_loaded"] = len(source_health_records)
    summary["toolchain_requirement_records_loaded"] = len(toolchain_requirement_records)
    summary["source_lock_records_loaded"] = len(source_lock_records)
    summary["manifest_readiness_records_loaded"] = len(manifest_readiness_records)

    write_yaml_records(
        outguess_readiness_out,
        record_set_id="stage4n-outguess-positive-control-readiness",
        schema="schemas/stego/stego-positive-control-readiness-v0.schema.json",
        records=outguess_readiness,
    )
    write_yaml_records(
        audio_readiness_out,
        record_set_id="stage4n-audio-positive-control-readiness",
        schema="schemas/stego/audio-positive-control-readiness-v0.schema.json",
        records=audio_readiness,
    )
    write_yaml_records(
        fixture_cache_out,
        record_set_id="stage4n-fixture-cache-records",
        schema="schemas/stego/stego-fixture-cache-record-v0.schema.json",
        records=cache_records,
    )
    write_yaml_records(
        expected_output_out,
        record_set_id="stage4n-expected-output-records",
        schema="schemas/stego/stego-expected-output-record-v0.schema.json",
        records=expected_output_records,
    )
    write_yaml_records(
        toolchain_out,
        record_set_id="stage4n-toolchain-readiness",
        schema="schemas/stego/stego-toolchain-readiness-v0.schema.json",
        records=toolchain_records,
    )
    write_yaml_document(summary_out, summary)

    write_json(out_dir / "readiness_report.json", outguess_readiness + audio_readiness)
    write_json(out_dir / "cache_report.json", cache_records)
    write_json(out_dir / "toolchain_report.json", toolchain_records)
    (out_dir / "warnings.jsonl").write_text("", encoding="utf-8")
    return summary


def _with_source_lock(record: dict[str, Any], source_lock_records: list[dict[str, Any]]) -> dict[str, Any]:
    enriched = dict(record)
    source_url = str(record.get("source_url") or "")
    source_path = str(record.get("source_path") or "")
    match = _match_source_lock(source_url, source_path, source_lock_records)
    enriched["source_lock_status"] = match.get("lock_status") if match else "not_locked"
    enriched["source_lock_record_id"] = match.get("snapshot_record_id") if match else None
    enriched["canonical_url"] = match.get("canonical_url") if match else None
    return enriched


def _match_source_lock(source_url: str, source_path: str, source_lock_records: list[dict[str, Any]]) -> dict[str, Any] | None:
    for lock in source_lock_records:
        if source_url and source_url == str(lock.get("source_url") or ""):
            return lock
    for lock in source_lock_records:
        lock_url = str(lock.get("source_url") or "")
        lock_path = str(lock.get("source_path") or "")
        if source_path and source_path.rstrip("/") == lock_path.rstrip("/"):
            return lock
        if source_url.startswith("https://github.com/cicada-solvers/iddqd") and lock_url == "https://github.com/cicada-solvers/iddqd":
            return lock
    return None
