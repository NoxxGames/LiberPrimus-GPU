"""Validation helpers for minimal triage score records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import ValidationError, validate

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable

SCHEMA_PATH = repo_root() / "schemas/scoring/minimal-triage-score-v0.schema.json"
CONTROL_SCHEMA_PATH = repo_root() / "schemas/scoring/scoring-control-record-v0.schema.json"
CALIBRATION_SUMMARY_SCHEMA_PATH = repo_root() / "schemas/scoring/scoring-calibration-summary-v0.schema.json"
CRIB_SCHEMA_PATH = repo_root() / "schemas/scoring/crib-check-result-v0.schema.json"


def validate_minimal_triage_score(score: Any) -> dict[str, Any]:
    return _validate_payload(score, SCHEMA_PATH)


def validate_scoring_control_record(record: Any) -> dict[str, Any]:
    return _validate_payload(record, CONTROL_SCHEMA_PATH)


def validate_scoring_calibration_summary(summary: Any) -> dict[str, Any]:
    return _validate_payload(summary, CALIBRATION_SUMMARY_SCHEMA_PATH)


def validate_crib_check_result(result: Any) -> dict[str, Any]:
    return _validate_payload(result, CRIB_SCHEMA_PATH)


def _validate_payload(payload_like: Any, schema_path: Path) -> dict[str, Any]:
    payload = to_jsonable(payload_like)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        validate(instance=payload, schema=schema)
    except ValidationError as exc:
        location = ".".join(str(item) for item in exc.absolute_path)
        prefix = f"{location}: " if location else ""
        raise ValueError(f"{prefix}{exc.message}") from exc
    return payload
