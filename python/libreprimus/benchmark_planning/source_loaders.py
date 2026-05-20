"""Read-only source loaders for Stage 4Q planning records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_json, read_jsonl, read_yaml, resolve_repo_path
from libreprimus.benchmark_planning.models import (
    FALLBACK_ADAPTER_COVERAGE,
    STAGE4O_ADAPTER_COVERAGE_PATH,
    STAGE4O_PARITY_EXPECTATIONS_PATH,
    STAGE4O_RESULT_RECORDS_PATH,
    STAGE4O_SUMMARY_PATH,
    STAGE4P_SUMMARY_PATH,
)


def load_stage4o_summary(path: Path = STAGE4O_SUMMARY_PATH) -> dict[str, Any]:
    return read_yaml(path)


def load_stage4p_summary(path: Path = STAGE4P_SUMMARY_PATH) -> dict[str, Any]:
    return read_yaml(path)


def load_stage4o_adapter_records(path: Path = STAGE4O_ADAPTER_COVERAGE_PATH) -> tuple[list[dict[str, Any]], bool]:
    """Load Stage 4O adapter coverage, falling back to committed summary-compatible constants."""

    resolved = resolve_repo_path(path)
    if resolved.is_file():
        payload = read_json(path)
        records = payload.get("records", [])
        if isinstance(records, list):
            return [record for record in records if isinstance(record, dict)], True
    fallback = [
        {
            "transform_id": transform_id,
            "canonical_transform_id": transform_id,
            "transform_family": transform_family,
            "adapter_status": status,
            "supports_gpu": False,
            "reason": "Fallback Stage 4Q coverage from committed Stage 4O summary constants.",
        }
        for transform_id, transform_family, status in FALLBACK_ADAPTER_COVERAGE
    ]
    return fallback, False


def load_stage4o_parity_expectations(path: Path = STAGE4O_PARITY_EXPECTATIONS_PATH) -> list[dict[str, Any]]:
    return read_jsonl(path)


def load_stage4o_result_records(path: Path = STAGE4O_RESULT_RECORDS_PATH) -> list[dict[str, Any]]:
    return read_jsonl(path)
