"""Validation for Stage 4I scoring consolidation records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import ValidationError, validate

from libreprimus.paths import repo_root
from libreprimus.scoring_consolidation.models import (
    CALIBRATION_PROFILE_PATH,
    CALIBRATION_PROFILE_SCHEMA,
    CALIBRATION_REPORT_PATH,
    CALIBRATION_REPORT_SCHEMA,
    COMPATIBILITY_MAP_PATH,
    COMPATIBILITY_MAP_SCHEMA,
    CONFIDENCE_LABELS,
    CONFIDENCE_LABELS_PATH,
    CONFIDENCE_LABEL_SCHEMA,
    DEFAULT_DATA_DIR,
    SCORER_RECORDS_PATH,
    SCORER_SCHEMA,
    SCORE_SUMMARY_SCHEMA,
)

REQUIRED_FILES = {
    SCORER_RECORDS_PATH: SCORER_SCHEMA,
    CONFIDENCE_LABELS_PATH: CONFIDENCE_LABEL_SCHEMA,
    COMPATIBILITY_MAP_PATH: COMPATIBILITY_MAP_SCHEMA,
    CALIBRATION_PROFILE_PATH: CALIBRATION_PROFILE_SCHEMA,
    CALIBRATION_REPORT_PATH: CALIBRATION_REPORT_SCHEMA,
}


def validate_data_dir(data_dir: Path = DEFAULT_DATA_DIR) -> tuple[dict[str, int], list[str]]:
    """Validate committed scoring records."""

    resolved = data_dir if data_dir.is_absolute() else repo_root() / data_dir
    counts: dict[str, int] = {}
    errors: list[str] = []
    for relative, schema_path in REQUIRED_FILES.items():
        path = resolved / relative
        if not path.is_file():
            errors.append(f"missing required scoring data file: {relative}")
            counts[_count_key(relative)] = 0
            continue
        records = _records(path)
        counts[_count_key(relative)] = len(records)
        schema = _schema(schema_path)
        for index, record in enumerate(records):
            try:
                validate(instance=record, schema=schema)
            except ValidationError as exc:
                location = ".".join(str(item) for item in exc.absolute_path)
                prefix = f"{relative}#{index}.{location}: " if location else f"{relative}#{index}: "
                errors.append(prefix + exc.message)
            _policy_errors(record, f"{relative}#{index}", errors)
    label_records = _records(resolved / CONFIDENCE_LABELS_PATH) if (resolved / CONFIDENCE_LABELS_PATH).is_file() else []
    labels = {str(record.get("label")) for record in label_records}
    if labels != set(CONFIDENCE_LABELS):
        errors.append("confidence label records must exactly match the Stage 4I finite label set")
    return counts, errors


def validate_score_summary(record: dict[str, Any]) -> dict[str, Any]:
    """Validate one Stage 4I score-summary record."""

    try:
        validate(instance=record, schema=_schema(SCORE_SUMMARY_SCHEMA))
    except ValidationError as exc:
        location = ".".join(str(item) for item in exc.absolute_path)
        prefix = f"{location}: " if location else ""
        raise ValueError(prefix + exc.message) from exc
    errors: list[str] = []
    _policy_errors(record, "score_summary", errors)
    if errors:
        raise ValueError("; ".join(errors))
    return record


def _records(path: Path) -> list[dict[str, Any]]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise ValueError(f"{path}: expected record set with records list")
    return [dict(item) for item in payload["records"] if isinstance(item, dict)]


def _schema(path: Path) -> dict[str, Any]:
    resolved = path if path.is_absolute() else repo_root() / path
    return json.loads(resolved.read_text(encoding="utf-8"))


def _policy_errors(record: dict[str, Any], prefix: str, errors: list[str]) -> None:
    if record.get("solve_claim") is not False and record.get("record_type") != "confidence_label_record":
        errors.append(f"{prefix}: solve_claim must be false")
    if record.get("trusted_as_canonical") is not False and record.get("record_type") != "confidence_label_record":
        errors.append(f"{prefix}: trusted_as_canonical must be false")
    if record.get("cuda_used") is not False:
        errors.append(f"{prefix}: cuda_used must be false")
    label = str(record.get("label", record.get("confidence_label", ""))).lower()
    if label in {"solved", "plaintext_verified"}:
        errors.append(f"{prefix}: scoring labels cannot imply solved/plaintext_verified")
    if record.get("solve_claim_allowed") is True:
        errors.append(f"{prefix}: solve_claim_allowed must be false")


def _count_key(path: Path) -> str:
    return path.stem.replace("-", "_")
