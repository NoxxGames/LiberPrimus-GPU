"""Validation for Stage 4C visual annotation records."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from jsonschema import ValidationError, validate

from libreprimus.paths import repo_root
from libreprimus.visual_annotation.loaders import load_yaml_payload, load_yaml_records
from libreprimus.visual_annotation.models import SCHEMA_PATHS


def validate_visual_annotation_records(
    *,
    task: Path,
    cuneiform: Path,
    dot: Path,
    delimiter: Path,
    negative: Path,
    summary: Path,
) -> tuple[dict[str, int], list[str]]:
    """Validate all committed Stage 4C visual annotation records."""

    errors: list[str] = []
    counts: dict[str, int] = {}

    record_sets = {
        "tasks": (task, "tasks"),
        "cuneiform": (cuneiform, "cuneiform"),
        "dot": (dot, "dot"),
        "delimiter": (delimiter, "delimiter"),
        "negative": (negative, "negative"),
    }
    loaded: dict[str, list[dict[str, Any]]] = {}
    for label, (path, schema_key) in record_sets.items():
        if not path.is_file():
            errors.append(f"{label}: missing {path}")
            counts[label] = 0
            loaded[label] = []
            continue
        records = load_yaml_records(path)
        loaded[label] = records
        counts[label] = len(records)
        _validate_records(records, repo_root() / SCHEMA_PATHS[schema_key], label, errors)

    if not summary.is_file():
        errors.append(f"summary: missing {summary}")
        summary_payload: dict[str, Any] = {}
    else:
        summary_payload = load_yaml_payload(summary)
        _validate_one(summary_payload, repo_root() / SCHEMA_PATHS["summary"], "summary", errors)

    counts["summary"] = 1 if summary_payload else 0
    _cross_checks(loaded=loaded, summary=summary_payload, errors=errors)
    return counts, errors


def _cross_checks(
    *,
    loaded: dict[str, list[dict[str, Any]]],
    summary: dict[str, Any],
    errors: list[str],
) -> None:
    task_ids = {str(record.get("task_id")) for record in loaded.get("tasks", [])}
    if "stage4c-task-cuneiform-17-13-55-1" not in task_ids:
        errors.append("tasks: missing stage4c-task-cuneiform-17-13-55-1")
    if "stage4c-task-dot-binary-13-31-ambiguity" not in task_ids:
        errors.append("tasks: missing stage4c-task-dot-binary-13-31-ambiguity")

    for record in loaded.get("cuneiform", []):
        if record.get("usable_as_experiment_seed") is not False:
            errors.append(f"{record.get('candidate_id')}: usable_as_experiment_seed must be false")
        if record.get("annotation_status") == "annotated":
            errors.append(f"{record.get('candidate_id')}: cuneiform candidate must not be verified")
        if record.get("coordinate_system") != "unknown_pending_annotation":
            errors.append(f"{record.get('candidate_id')}: coordinates must not be invented")

    for record in loaded.get("dot", []):
        if record.get("review_status") == "verified":
            errors.append(f"{record.get('task_id')}: dot task must not be verified")
        claimed = {str(value) for value in record.get("claimed_readings", [])}
        if not {"13", "31"} <= claimed:
            errors.append(f"{record.get('task_id')}: expected ambiguous 13/31 claimed readings")
        if record.get("usable_as_experiment_seed") is not False:
            errors.append(f"{record.get('task_id')}: usable_as_experiment_seed must be false")

    for record in loaded.get("delimiter", []):
        if record.get("reset_boundary_hypothesis") is not False:
            errors.append(f"{record.get('task_id')}: reset_boundary_hypothesis must be false")

    negative_classes = {str(record.get("false_positive_class")) for record in loaded.get("negative", [])}
    for required in ("braille_dot_readings", "constellation_dot_readings", "forced_13_31_dot_values"):
        if required not in negative_classes:
            errors.append(f"negative: missing {required}")

    for key in ("tasks", "cuneiform", "dot", "delimiter", "negative"):
        for record in loaded.get(key, []):
            if record.get("solve_claim") is not False:
                errors.append(f"{key}:{record.get('task_id', record.get('candidate_id'))} solve_claim must be false")
            if record.get("trusted_as_canonical") is not False:
                errors.append(f"{key}:{record.get('task_id', record.get('candidate_id'))} trusted_as_canonical must be false")
            if record.get("usable_as_experiment_seed") is not False:
                errors.append(f"{key}:{record.get('task_id', record.get('candidate_id'))} usable_as_experiment_seed must be false")

    if summary:
        expected = {
            "task_count": len(loaded.get("tasks", [])),
            "cuneiform_task_count": len(loaded.get("cuneiform", [])),
            "dot_task_count": len(loaded.get("dot", [])),
            "delimiter_task_count": len(loaded.get("delimiter", [])),
            "negative_control_task_count": len(loaded.get("negative", [])),
        }
        for key, value in expected.items():
            if summary.get(key) != value:
                errors.append(f"summary: {key} expected {value}, found {summary.get(key)}")


def _validate_records(
    records: list[dict[str, Any]], schema_path: Path, label: str, errors: list[str]
) -> None:
    seen: set[str] = set()
    for record in records:
        _validate_one(record, schema_path, label, errors)
        identifier = str(record.get("task_id", record.get("candidate_id", "")))
        if identifier in seen:
            errors.append(f"{label}: duplicate id {identifier}")
        seen.add(identifier)


def _validate_one(
    payload: dict[str, Any], schema_path: Path, label: str, errors: list[str]
) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        validate(payload, schema)
    except ValidationError as error:
        path = ".".join(str(part) for part in error.path)
        errors.append(f"{label}: {path}: {error.message}")
