"""Import Stage 2A solved-baseline outputs into result-store records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root
from libreprimus.result_store.export import write_result_store_outputs
from libreprimus.result_store.models import (
    ExperimentArtifactRecord,
    ExperimentEventRecord,
    ExperimentRunRecord,
    ExperimentRunSummary,
    ResultStoreManifest,
)
from libreprimus.result_store.provenance import (
    git_branch,
    git_commit,
    host_metadata,
    profile_metadata,
    sha256_file,
    tool_versions,
    utc_now,
)
from libreprimus.result_store.schema_validation import (
    load_yaml_payload,
    validate_result_store_manifest_payload,
)
from libreprimus.result_store.sqlite_sink import write_sqlite_store


def _resolve(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else repo_root() / candidate


def _display_path(path: Path) -> str:
    return str(path.relative_to(repo_root())).replace("\\", "/") if path.is_relative_to(repo_root()) else str(path)


def load_result_store_manifest(path: Path) -> ResultStoreManifest:
    manifest_path = _resolve(path)
    payload = load_yaml_payload(manifest_path)
    validate_result_store_manifest_payload(payload)
    return ResultStoreManifest(
        record_type=str(payload["record_type"]),
        manifest_id=str(payload["manifest_id"]),
        manifest_version=str(payload["manifest_version"]),
        description=str(payload["description"]),
        input_manifest_path=str(payload["input_manifest_path"]),
        input_manifest_sha256=str(payload["input_manifest_sha256"]),
        output_dir=str(payload["output_dir"]),
        jsonl_output_path=str(payload["jsonl_output_path"]),
        sqlite_output_path=str(payload["sqlite_output_path"]),
        import_sources=[str(item) for item in payload["import_sources"]],
        canonical_corpus_active=bool(payload["canonical_corpus_active"]),
        page_boundaries_final=bool(payload["page_boundaries_final"]),
        search_enabled=bool(payload["search_enabled"]),
        scoring_enabled=bool(payload["scoring_enabled"]),
        cuda_enabled=bool(payload["cuda_enabled"]),
        expected_run_kind=str(payload["expected_run_kind"]),
        notes=[str(item) for item in payload.get("notes", [])],
    )


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _artifact(run_id: str, path: Path, kind: str) -> ExperimentArtifactRecord:
    return ExperimentArtifactRecord(
        record_type="experiment_artifact_record",
        run_id=run_id,
        artifact_id=f"{kind}-{path.stem}",
        artifact_kind=kind,
        path=_display_path(path),
        sha256=sha256_file(path),
        size_bytes=path.stat().st_size,
        committed=False,
        ignored_by_git=True,
        notes=["Generated artifact imported into Stage 2B result store."],
        trusted_as_canonical=False,
    )


def build_solved_baseline_import_records(
    manifest: ResultStoreManifest,
    *,
    solved_baseline_results: Path,
    out_dir: Path,
) -> tuple[list[ExperimentRunRecord], list[ExperimentEventRecord], list[ExperimentArtifactRecord], ExperimentRunSummary]:
    results_dir = _resolve(solved_baseline_results)
    output_dir = _resolve(out_dir)
    summary_path = results_dir / "summary.json"
    records_path = results_dir / "manifest_run_records.jsonl"
    warnings_path = results_dir / "warnings.jsonl"
    if not summary_path.is_file() or not records_path.is_file():
        raise FileNotFoundError(f"Stage 2A solved-baseline outputs are missing in {results_dir}.")

    solved_summary = json.loads(summary_path.read_text(encoding="utf-8"))
    manifest_payload = load_yaml_payload(_resolve(manifest.input_manifest_path))
    run_id = f"{manifest.manifest_id}-{solved_summary['manifest_id']}-{solved_summary['manifest_sha256'][:12]}"
    now = utc_now()
    imported_records = _read_jsonl(records_path)
    imported_warnings = _read_jsonl(warnings_path)
    warning_messages = [str(item.get("warning", item)) for item in imported_warnings]
    fail_count = int(solved_summary.get("fail_count", 0))
    pending_count = int(solved_summary.get("pending_count", 0))
    skipped_count = int(solved_summary.get("skipped_count", 0))
    run_status = "pass" if fail_count == 0 and pending_count == 0 and skipped_count == 0 else "partial"
    transform_counts = {
        "direct_translation_pass_count": int(solved_summary.get("direct_translation_pass_count", 0)),
        "atbash_family_pass_count": int(solved_summary.get("atbash_family_pass_count", 0)),
        "vigenere_pass_count": int(solved_summary.get("vigenere_pass_count", 0)),
        "prime_stream_pass_count": int(solved_summary.get("prime_stream_pass_count", 0)),
    }
    artifacts = [
        _artifact(run_id, summary_path, "solved_baseline_summary"),
        _artifact(run_id, records_path, "solved_baseline_records"),
    ]
    if warnings_path.is_file():
        artifacts.append(_artifact(run_id, warnings_path, "solved_baseline_warnings"))

    run_record = ExperimentRunRecord(
        record_type="experiment_run_record",
        run_id=run_id,
        run_kind="solved_baseline",
        run_status=run_status,
        manifest_id=str(solved_summary["manifest_id"]),
        manifest_sha256=str(solved_summary["manifest_sha256"]),
        registry_id=str(solved_summary["registry_id"]),
        registry_sha256=str(solved_summary["registry_sha256"]),
        git_commit=git_commit(),
        branch=git_branch(),
        created_at_utc=now,
        completed_at_utc=now,
        elapsed_ms=float(solved_summary.get("elapsed_ms", 0.0)),
        host=host_metadata(),
        tool_versions=tool_versions(),
        input_sources=[
            {
                "source_id": str(solved_summary["manifest_id"]),
                "source_kind": "solved_baseline_manifest_run",
                "sha256": solved_summary.get("manifest_sha256"),
            },
            {
                "source_id": manifest.input_manifest_path,
                "source_kind": "solved_baseline_manifest",
                "sha256": manifest.input_manifest_sha256,
            },
            *[
                {
                    "source_id": source_path,
                    "source_kind": "generated_import_source",
                    "sha256": sha256_file(_resolve(source_path)) if _resolve(source_path).is_file() else None,
                }
                for source_path in manifest.import_sources
            ],
        ],
        profiles=profile_metadata(),
        corpus_candidate_id=str(manifest_payload.get("corpus_candidate_id", "rtkd-master-v0-candidate")),
        canonical_corpus_active=False,
        page_boundaries_final=False,
        search_performed=bool(solved_summary.get("search_performed_any", False)),
        scoring_used=bool(solved_summary.get("scoring_used_any", False)),
        cuda_used=bool(solved_summary.get("cuda_used_any", False)),
        gpu_required=False,
        random_seed=None,
        fixture_counts={
            "total": int(solved_summary.get("fixture_count", len(imported_records))),
            "pass": int(solved_summary.get("pass_count", 0)),
            "fail": fail_count,
            "pending": pending_count,
            "skipped": skipped_count,
        },
        transform_counts=transform_counts,
        output_artifacts=[artifact.artifact_id for artifact in artifacts],
        warnings=warning_messages,
        trusted_as_canonical=False,
        notes=[
            "Imported Stage 2A solved-baseline manifest-run output.",
            "Regression evidence only; not an unsolved-page experiment.",
        ],
        validation_status="pass",
    )
    events = [
        ExperimentEventRecord(
            record_type="experiment_event_record",
            run_id=run_id,
            event_index=0,
            timestamp_utc=now,
            level="info",
            event_type="import_started",
            message="Started solved-baseline result import.",
            data={"source_dir": str(results_dir)},
            trusted_as_canonical=False,
        ),
        ExperimentEventRecord(
            record_type="experiment_event_record",
            run_id=run_id,
            event_index=1,
            timestamp_utc=now,
            level="info",
            event_type="solved_baseline_summary",
            message="Imported solved-baseline summary counts.",
            data={
                "pass_count": run_record.fixture_counts["pass"],
                "fail_count": run_record.fixture_counts["fail"],
                "pending_count": run_record.fixture_counts["pending"],
                "skipped_count": run_record.fixture_counts["skipped"],
            },
            trusted_as_canonical=False,
        ),
    ]
    for index, warning in enumerate(warning_messages, start=2):
        events.append(
            ExperimentEventRecord(
                record_type="experiment_event_record",
                run_id=run_id,
                event_index=index,
                timestamp_utc=now,
                level="warning",
                event_type="import_warning",
                message=warning,
                data={},
                trusted_as_canonical=False,
            )
        )
    summary = ExperimentRunSummary(
        record_type="experiment_run_summary",
        summary_id=f"{manifest.manifest_id}-summary",
        generated_at_utc=now,
        run_count=1,
        pass_count=1 if run_status == "pass" else 0,
        fail_count=1 if run_status == "fail" else 0,
        partial_count=1 if run_status == "partial" else 0,
        pending_count=0,
        skipped_count=0,
        error_count=0,
        run_kinds=["solved_baseline"],
        canonical_corpus_active_any=False,
        search_performed_any=run_record.search_performed,
        scoring_used_any=run_record.scoring_used,
        cuda_used_any=run_record.cuda_used,
        generated_artifact_count=len(artifacts),
        sqlite_database_path=_display_path(output_dir / "results.sqlite3"),
        jsonl_path=_display_path(output_dir / "run_records.jsonl"),
        warnings=warning_messages,
        trusted_as_canonical=False,
    )
    return [run_record], events, artifacts, summary


def import_solved_baseline(
    manifest_path: Path,
    *,
    solved_baseline_results: Path,
    out_dir: Path,
    replace: bool = False,
) -> dict[str, Any]:
    manifest = load_result_store_manifest(manifest_path)
    output_dir = _resolve(out_dir)
    runs, events, artifacts, summary = build_solved_baseline_import_records(
        manifest,
        solved_baseline_results=solved_baseline_results,
        out_dir=output_dir,
    )
    output_paths = write_result_store_outputs(
        output_dir,
        run_records=runs,
        event_records=events,
        artifact_records=artifacts,
        summary=summary,
    )
    sqlite_path = output_dir / "results.sqlite3"
    write_sqlite_store(
        sqlite_path,
        run_records=runs,
        event_records=events,
        artifact_records=artifacts,
        summaries=[summary],
        replace=replace,
    )
    output_paths["sqlite"] = sqlite_path
    return {
        "manifest": manifest,
        "run_records": runs,
        "event_records": events,
        "artifact_records": artifacts,
        "summary": summary,
        "paths": output_paths,
    }
