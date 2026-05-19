"""Stage 4F stego/audio fixture source-lock orchestration."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any
import json

from libreprimus.stego_fixtures.disabled_manifests import write_disabled_manifests
from libreprimus.stego_fixtures.fixture_classifier import build_audio_fixture_records, build_outguess_fixture_records
from libreprimus.stego_fixtures.loaders import load_yaml_records, stage4e_candidates, write_yaml_records
from libreprimus.stego_fixtures.source_health import build_source_health_records
from libreprimus.stego_fixtures.toolchain_requirements import build_toolchain_requirements


def build_stego_fixture_records(
    *,
    stage4e_source_delta: Path,
    stage4e_source_health: Path,
    stage4b_sources: Path,
    out_dir: Path,
    outguess_fixtures_out: Path,
    audio_fixtures_out: Path,
    source_health_out: Path,
    toolchain_out: Path,
    manifest_out_dir: Path,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Build Stage 4F fixture source-lock metadata records."""

    del allow_warnings
    out_dir.mkdir(parents=True, exist_ok=True)
    candidates = stage4e_candidates(stage4e_source_delta)
    stage4b = load_yaml_records(stage4b_sources)
    stage4e_health = load_yaml_records(stage4e_source_health)
    outguess_records = build_outguess_fixture_records(candidates, stage4b)
    audio_records = build_audio_fixture_records(stage4b)
    all_fixture_records = [*outguess_records, *audio_records]
    health_records = build_source_health_records(all_fixture_records)
    toolchain_records = build_toolchain_requirements()
    manifest_paths = write_disabled_manifests(manifest_out_dir)

    write_yaml_records(
        outguess_fixtures_out,
        record_set_id="stage4f-outguess-fixture-source-records",
        schema="schemas/stego/stego-fixture-source-record-v0.schema.json",
        records=outguess_records,
    )
    write_yaml_records(
        audio_fixtures_out,
        record_set_id="stage4f-audio-fixture-source-records",
        schema="schemas/stego/audio-fixture-source-record-v0.schema.json",
        records=audio_records,
    )
    write_yaml_records(
        source_health_out,
        record_set_id="stage4f-stego-fixture-source-health",
        schema="schemas/stego/fixture-source-health-record-v0.schema.json",
        records=health_records,
    )
    write_yaml_records(
        toolchain_out,
        record_set_id="stage4f-toolchain-requirements",
        schema="schemas/stego/toolchain-requirement-record-v0.schema.json",
        records=toolchain_records,
    )

    availability_counts = Counter(str(record.get("local_availability", "unknown")) for record in all_fixture_records)
    gaps = [
        {
            "fixture_id": record.get("fixture_id"),
            "local_availability": record.get("local_availability"),
            "recommended_action": "future source-lock/download stage required",
        }
        for record in all_fixture_records
        if record.get("local_availability") != "present_ignored_cache"
    ]
    warnings = []
    if not candidates:
        warnings.append({"warning": "stage4e_source_delta_candidates_missing"})
    if not stage4e_health:
        warnings.append({"warning": "stage4e_source_health_missing"})
    _write_jsonl(out_dir / "source_gap_records.jsonl", gaps)
    _write_jsonl(out_dir / "warnings.jsonl", warnings)

    summary = {
        "run_id": "stage4f-stego-fixture-source-lock",
        "outguess_fixture_source_records_count": len(outguess_records),
        "audio_fixture_source_records_count": len(audio_records),
        "source_health_records_count": len(health_records),
        "toolchain_requirement_records_count": len(toolchain_records),
        "disabled_manifest_count": len([path for path in manifest_paths if path.name != "README.md"]),
        "local_availability_counts": dict(sorted(availability_counts.items())),
        "raw_file_committed": False,
        "binary_committed": False,
        "audio_committed": False,
        "image_committed": False,
        "extracted_payload_committed": False,
        "font_committed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
        "cuda_used": False,
        "output_paths": {
            "fixture_candidate_report": (out_dir / "fixture_candidate_report.json").as_posix(),
            "source_gap_records": (out_dir / "source_gap_records.jsonl").as_posix(),
            "warnings": (out_dir / "warnings.jsonl").as_posix(),
        },
    }
    (out_dir / "fixture_candidate_report.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
