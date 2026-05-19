"""Validation for Stage 4D bounded numeric generated outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.bounded_numeric.loaders import read_json, read_jsonl
from libreprimus.bounded_numeric.models import SCHEMA_PATHS
from libreprimus.bounded_numeric.no_fudge_policy import validate_no_fudge_record
from libreprimus.paths import repo_root


def validate_bounded_numeric_results(results_dir: Path) -> tuple[dict[str, Any], list[str]]:
    """Validate generated Stage 4D bounded numeric outputs."""

    errors: list[str] = []
    required = {
        "summary": results_dir / "summary.json",
        "result_records": results_dir / "result_records.jsonl",
        "manifest_status_records": results_dir / "manifest_status_records.jsonl",
        "negative_control_records": results_dir / "negative_control_records.jsonl",
        "warnings": results_dir / "warnings.jsonl",
    }
    for label, path in required.items():
        if not path.is_file():
            errors.append(f"{label}:missing:{path}")

    summary: dict[str, Any] = {}
    if required["summary"].is_file():
        summary = read_json(required["summary"])
        _validate_summary(summary, errors)

    result_records = read_jsonl(required["result_records"])
    negative_records = read_jsonl(required["negative_control_records"])
    delimiter_records = [record for record in result_records if record.get("record_type") == "delimiter_handedness_audit_record"]
    bounded_records = [record for record in result_records if record.get("record_type") == "bounded_numeric_result_record"]

    _validate_records(bounded_records, repo_root() / SCHEMA_PATHS["result"], "result_records", errors)
    _validate_records(delimiter_records, repo_root() / SCHEMA_PATHS["delimiter"], "delimiter_records", errors)
    _validate_records(negative_records, repo_root() / SCHEMA_PATHS["negative"], "negative_control_records", errors)

    for record in result_records + negative_records:
        errors.extend(validate_no_fudge_record(record))
        cap = int(record.get("cap") or record.get("candidate_count_upper_bound") or 0)
        count = int(record.get("candidate_count") or 0)
        if count > cap:
            errors.append(f"{record.get('result_id')}:candidate_count_exceeds_cap")

    if summary:
        if summary.get("cuneiform_deferred") is not True:
            errors.append("summary:cuneiform_deferred_must_be_true")
        if summary.get("cookie_pack_deferred") is not True:
            errors.append("summary:cookie_pack_deferred_must_be_true")
        if summary.get("no_fudge_policy") is not True:
            errors.append("summary:no_fudge_policy_must_be_true")
        if summary.get("solve_claim") is not False:
            errors.append("summary:solve_claim_must_be_false")
        if summary.get("cuda_used") is not False:
            errors.append("summary:cuda_used_must_be_false")

    return summary, errors


def _validate_summary(summary: dict[str, Any], errors: list[str]) -> None:
    for field in (
        "manifests_discovered",
        "manifests_executed",
        "manifests_deferred",
        "result_records_count",
        "negative_control_records_count",
    ):
        if not isinstance(summary.get(field), int):
            errors.append(f"summary:{field}_missing_or_not_integer")


def _validate_records(
    records: list[dict[str, Any]], schema_path: Path, label: str, errors: list[str]
) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    seen: set[str] = set()
    for index, record in enumerate(records):
        identifier = str(record.get("result_id") or record.get("negative_control_id") or index)
        if identifier in seen:
            errors.append(f"{label}:duplicate:{identifier}")
        seen.add(identifier)
        for validation_error in validator.iter_errors(record):
            path = ".".join(str(part) for part in validation_error.path)
            errors.append(f"{label}[{index}] {path}: {validation_error.message}")
