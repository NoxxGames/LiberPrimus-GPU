"""Load Stage 5P input records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml
from libreprimus.gematria_cuda_result_store.export import read_record_set
from libreprimus.gematria_cuda_result_store.models import (
    METHOD_STATUS_RECORDS,
    STAGE4I_CONFIDENCE_LABELS,
    STAGE4P_SUMMARY,
    STAGE5O_EXPANSION_DECISION,
    STAGE5O_REPEAT_PARITY,
    STAGE5O_RESULT_STORE_PREFLIGHT,
    STAGE5O_SCORE_SUMMARY_PREFLIGHT,
    STAGE5O_SUMMARY,
)


def load_stage5o_repeat_parity(path: Path = STAGE5O_REPEAT_PARITY) -> list[dict[str, Any]]:
    return read_record_set(path)


def load_stage5o_result_store_preflight(path: Path = STAGE5O_RESULT_STORE_PREFLIGHT) -> list[dict[str, Any]]:
    return read_record_set(path)


def load_stage5o_score_summary_preflight(path: Path = STAGE5O_SCORE_SUMMARY_PREFLIGHT) -> list[dict[str, Any]]:
    return read_record_set(path)


def load_stage5o_expansion_decision(path: Path = STAGE5O_EXPANSION_DECISION) -> list[dict[str, Any]]:
    return read_record_set(path)


def load_stage5o_summary(path: Path = STAGE5O_SUMMARY) -> dict[str, Any]:
    return read_yaml(path)


def load_stage4p_summary(path: Path = STAGE4P_SUMMARY) -> dict[str, Any]:
    return read_yaml(path)


def load_stage4i_confidence_labels(path: Path = STAGE4I_CONFIDENCE_LABELS) -> set[str]:
    return {str(record["label"]) for record in read_yaml(path).get("records", [])}


def load_method_status_records(path: Path = METHOD_STATUS_RECORDS) -> list[dict[str, Any]]:
    return [dict(record) for record in read_yaml(path).get("records", [])]
