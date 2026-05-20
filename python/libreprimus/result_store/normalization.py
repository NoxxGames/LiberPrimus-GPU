"""Normalize result surfaces into Stage 4P unified result records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.input_streams import stable_json_sha256
from libreprimus.result_store.source_inventory import build_source_inventory_from_manifest
from libreprimus.result_store.stage4p_export import read_json, read_jsonl, read_yaml, resolve_repo_path, write_jsonl
from libreprimus.result_store.unified_models import (
    STAGE4P_OUTPUT_DIR,
    UNIFIED_RESULT_JSONL,
)
from libreprimus.scoring_consolidation.confidence_labels import map_legacy_label


def build_unified_result_records(
    manifest_path: Path,
    *,
    out_dir: Path = STAGE4P_OUTPUT_DIR,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Build source inventory and unified result records."""

    inventory, warnings = build_source_inventory_from_manifest(manifest_path, out_dir=out_dir)
    records: list[dict[str, Any]] = []
    for source in inventory:
        records.extend(_records_for_source(source))
    records = sorted(records, key=_result_sort_key)
    write_jsonl(resolve_repo_path(out_dir) / UNIFIED_RESULT_JSONL, records)
    return inventory, records, warnings


def _records_for_source(source: dict[str, Any]) -> list[dict[str, Any]]:
    status = str(source["source_presence_status"])
    if status in {"optional_generated_missing", "skipped_raw_required", "skipped_schema_unknown"}:
        return [_base_record(source, result_count=0, warning=status)]
    path = resolve_repo_path(Path(str(source["source_path"])))
    if path.suffix == ".jsonl":
        payloads = read_jsonl(path)
        return [_record_from_payload(source, payload, index) for index, payload in enumerate(payloads)]
    payload = read_json(path) if path.suffix == ".json" else read_yaml(path)
    if isinstance(payload.get("records"), list):
        return [
            _record_from_payload(source, dict(payload_item), index)
            for index, payload_item in enumerate(payload["records"])
            if isinstance(payload_item, dict)
        ]
    return [_record_from_payload(source, payload, 0)]


def _record_from_payload(source: dict[str, Any], payload: dict[str, Any], index: int) -> dict[str, Any]:
    base = _base_record(
        source,
        result_count=_result_count(payload),
        candidate_count=_candidate_count(payload),
    )
    source_kind = str(source["result_source_kind"])
    source_record_type = str(payload.get("record_type", source.get("source_record_type", "summary")))
    base["source_record_type"] = source_record_type
    base["source_payload_index"] = index
    base["candidate_id"] = str(payload.get("candidate_id", base["unified_result_id"]))
    base["transform_family"] = str(payload.get("transform_family", "unknown"))
    base["output_text_hash"] = payload.get("output_text_hash")
    base["output_token_hash"] = payload.get("output_token_hash")
    if source_kind == "cpu_batch_result" and source_record_type == "cpu_batch_result_record":
        score_summary = dict(payload.get("score_summary") or {})
        label = map_legacy_label(str(score_summary.get("confidence_label", "scoring_not_available")))
        base["confidence_label"] = label
        base["score_summary_available"] = bool(score_summary)
        base["method_family"] = "cpu_batch_transform_api"
    elif source_kind == "cpu_batch_parity_expectation":
        base["parity_expectation_id"] = str(
            payload.get("parity_expectation_id", payload.get("candidate_id", base["unified_result_id"]))
        )
        base["records_with_parity_expectation"] = True
        base["method_family"] = "cpu_batch_transform_api"
    elif source_kind == "method_family_status":
        base["method_family"] = str(payload.get("method_family_id", source.get("method_family", "unknown")))
        base["method_status"] = _normalize_method_status(str(payload.get("status", "unknown")))
    elif source_kind == "method_retirement":
        base["method_family"] = str(payload.get("method_family_id", source.get("method_family", "unknown")))
        base["retirement_status"] = str(payload.get("retired_status", "unknown"))
    return {key: value for key, value in base.items() if value is not None}


def _base_record(
    source: dict[str, Any],
    *,
    result_count: int,
    candidate_count: int | None = None,
    warning: str | None = None,
) -> dict[str, Any]:
    source_id = str(source["source_id"])
    result_id = "stage4p-" + stable_json_sha256(
        [source_id, source["source_path"], result_count, candidate_count, warning]
    )[:20]
    warnings = list(source.get("warnings", []))
    if warning:
        warnings.append(warning)
    record = {
        "record_type": "unified_result_record",
        "unified_result_id": result_id,
        "source_id": source_id,
        "source_stage_id": str(source["source_stage_id"]),
        "source_record_type": str(source.get("source_record_type", "summary")),
        "result_source_kind": str(source["result_source_kind"]),
        "source_path": str(source["source_path"]),
        "source_presence_status": str(source["source_presence_status"]),
        "method_family": str(source.get("method_family", "unknown")),
        "transform_family": "unknown",
        "candidate_count": candidate_count,
        "result_count": result_count,
        "score_summary_available": False,
        "confidence_label": "scoring_not_available",
        "method_status": "unknown",
        "retirement_status": "unknown",
        "no_solve_claim": True,
        "solve_claim": False,
        "cuda_used": False,
        "cuda_required": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
        "raw_data_processed": False,
        "new_experiment_executed": False,
        "new_scorer_added": False,
        "score_interpretation": "triage_only",
        "warnings": warnings,
    }
    return {key: value for key, value in record.items() if value is not None}


def _result_count(payload: dict[str, Any]) -> int:
    for key in ("result_records", "result_record_count", "run_count", "record_count", "records"):
        value = payload.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, list):
            return len(value)
    return 1


def _candidate_count(payload: dict[str, Any]) -> int | None:
    for key in ("candidate_count", "candidates_executed", "executed_candidate_count"):
        value = payload.get(key)
        if isinstance(value, int):
            return value
    fixture_counts = payload.get("fixture_counts")
    if isinstance(fixture_counts, dict) and isinstance(fixture_counts.get("total"), int):
        return int(fixture_counts["total"])
    return None


def _normalize_method_status(status: str) -> str:
    if status == "infrastructure_only":
        return "infrastructure_only"
    if status in {"active", "noisy", "inconclusive", "negative", "retired", "deferred", "blocked"}:
        return status
    return "unknown"


def _result_sort_key(record: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        str(record.get("source_stage_id", "")),
        str(record.get("result_source_kind", "")),
        str(record.get("method_family", "")),
        str(record.get("source_path", "")),
        str(record.get("candidate_id", "")),
    )
