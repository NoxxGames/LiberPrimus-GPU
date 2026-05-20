"""Join unified results to method-family and retirement status."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.input_streams import stable_json_sha256
from libreprimus.result_store.stage4p_export import read_jsonl, read_yaml, resolve_repo_path, write_json
from libreprimus.result_store.unified_models import (
    METHOD_STATUS_JOIN_JSON,
    STAGE4P_OUTPUT_DIR,
    UNIFIED_RESULT_JSONL,
)

METHOD_STATUS_PATH = Path("data/research/method-family-status-records-v0.yaml")
METHOD_RETIREMENT_PATH = Path("data/research/method-retirement-records-v0.yaml")


def build_method_status_join(*, out_dir: Path = STAGE4P_OUTPUT_DIR) -> list[dict[str, Any]]:
    """Write method status join records for unified result records."""

    resolved_out = resolve_repo_path(out_dir)
    results = read_jsonl(resolved_out / UNIFIED_RESULT_JSONL)
    method_status = _records_by_method(read_yaml(METHOD_STATUS_PATH).get("records", []))
    retirements = _records_by_method(read_yaml(METHOD_RETIREMENT_PATH).get("records", []))
    joins = [
        _join_record(result, method_status.get(str(result.get("method_family"))), retirements.get(str(result.get("method_family"))))
        for result in results
    ]
    joins = sorted(joins, key=lambda item: str(item["join_id"]))
    write_json(resolved_out / METHOD_STATUS_JOIN_JSON, {"records": joins})
    return joins


def _records_by_method(records: Iterable[Any]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for record in records:
        if isinstance(record, dict):
            indexed[str(record.get("method_family_id"))] = dict(record)
    return indexed


def _join_record(
    result: dict[str, Any],
    method: dict[str, Any] | None,
    retirement: dict[str, Any] | None,
) -> dict[str, Any]:
    method_family = str(result.get("method_family", "unknown"))
    method_status = str(method.get("status")) if method else str(result.get("method_status", "unknown"))
    retirement_status = str(retirement.get("retired_status")) if retirement else str(result.get("retirement_status", "unknown"))
    join_status = "joined" if method else ("not_applicable" if method_family == "unknown" else "missing_method_status")
    join_id = "stage4p-join-" + stable_json_sha256([result.get("unified_result_id"), method_family])[:20]
    warnings: list[str] = []
    if join_status == "missing_method_status":
        warnings.append("Unified result has no matching method-family status record.")
    return {
        "record_type": "result_method_status_join_record",
        "join_id": join_id,
        "unified_result_id": result.get("unified_result_id"),
        "method_family": method_family,
        "method_status": _normalize_status(method_status),
        "retirement_status": retirement_status,
        "join_status": join_status,
        "score_interpretation": "triage_only",
        "no_solve_claim": True,
        "solve_claim": False,
        "cuda_used": False,
        "warnings": warnings,
    }


def _normalize_status(status: str) -> str:
    if status in {
        "active",
        "infrastructure",
        "infrastructure_only",
        "noisy",
        "inconclusive",
        "negative",
        "retired",
        "deferred",
        "blocked",
    }:
        return status
    return "unknown"
