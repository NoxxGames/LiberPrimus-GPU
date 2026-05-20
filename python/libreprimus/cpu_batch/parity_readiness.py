"""Stage 4O scoring compatibility and parity-readiness summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.cpu_batch.input_streams import stable_json_sha256
from libreprimus.cpu_batch.parity_expectations import write_parity_expectations
from libreprimus.cpu_batch.solved_fixture_streams import solved_fixture_stream_records_from_manifest
from libreprimus.history.source_records import resolve_repo_path
from libreprimus.scoring_consolidation.cpu_batch_integration import score_summary_from_cpu_batch_result


def build_scoring_compatibility(records: list[dict[str, Any]], *, out_dir: Path) -> dict[str, Any]:
    """Write Stage 4O scoring compatibility records for expanded CPU batch output."""

    shape_hashes: list[str] = []
    compatible = 0
    unavailable = 0
    for record in records:
        score_view = score_summary_from_cpu_batch_result(record)
        shape_hashes.append(stable_json_sha256(sorted(score_view.keys())))
        if score_view.get("score_status") == "scored":
            compatible += 1
        else:
            unavailable += 1
    payload = {
        "record_type": "cpu_batch_scoring_compatibility",
        "compatible": True,
        "record_count": len(records),
        "scoring_compatible_count": compatible,
        "scoring_unavailable_count": unavailable,
        "score_summary_shape_hashes": sorted(set(shape_hashes)),
        "cpu_only": True,
        "cuda_used": False,
        "cuda_required": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
    }
    resolved_out = resolve_repo_path(out_dir)
    resolved_out.mkdir(parents=True, exist_ok=True)
    (resolved_out / "scoring_compatibility.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def write_stage4o_readiness(
    *,
    manifest: Path,
    results_dir: Path,
    summary_out: Path,
) -> dict[str, Any]:
    """Build parity expectations, scoring compatibility, and committed Stage 4O summary."""

    resolved_results = resolve_repo_path(results_dir)
    records = _read_jsonl(resolved_results / "result_records.jsonl")
    adapter_coverage = _read_json(resolved_results / "adapter_coverage.json")
    parity = write_parity_expectations(records=records, out_dir=resolved_results)
    scoring = build_scoring_compatibility(records, out_dir=resolved_results)
    fixture_streams = solved_fixture_stream_records_from_manifest(manifest)
    executed_stream_ids = {
        str(record["input_stream_id"])
        for record in records
        if record.get("execution_status") == "executed"
    }
    summary = {
        "record_type": "stage4o_cpu_batch_adapter_expansion_summary",
        "schema": "schemas/experiments/cpu-batch-adapter-expansion-summary-v0.schema.json",
        "stage_id": "stage-4o",
        "status": "complete",
        "solved_fixture_streams_discovered": len(fixture_streams),
        "solved_fixture_streams_executed": sum(1 for stream in fixture_streams if stream["input_stream_id"] in executed_stream_ids),
        "skipped_fixture_streams": 0,
        "transform_adapters_supported": int(adapter_coverage.get("supported_adapter_count", 0)),
        "transform_adapters_missing_or_deferred": int(adapter_coverage.get("missing_or_deferred_adapter_count", 0)),
        "candidates_executed": sum(1 for record in records if record.get("execution_status") == "executed"),
        "result_records": len(records),
        "parity_expectations_written": len(parity),
        "scoring_compatible_count": int(scoring["scoring_compatible_count"]),
        "scoring_unavailable_count": int(scoring["scoring_unavailable_count"]),
        "cpu_only": True,
        "cuda_used": False,
        "cuda_required": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
        "notes": [
            "Stage 4O expands CPU batch parity records for future CUDA reference checks.",
            "Generated Stage 4O result records remain ignored under experiments/results/cpu-batch/stage4o/.",
        ],
    }
    resolved_summary = resolve_repo_path(summary_out)
    resolved_summary.parent.mkdir(parents=True, exist_ok=True)
    resolved_summary.write_text(yaml.safe_dump(summary, sort_keys=False, allow_unicode=False), encoding="utf-8")
    (resolved_results / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON file must contain a mapping: {path}")
    return payload


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"JSONL record must be a mapping: {path}")
        records.append(payload)
    return records
