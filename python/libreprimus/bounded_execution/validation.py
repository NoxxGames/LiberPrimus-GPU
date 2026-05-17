"""Validation helpers for Stage 3A bounded candidate outputs."""

from __future__ import annotations

import json
from typing import Any

from jsonschema import ValidationError, validate

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable

SCHEMA_DIR = repo_root() / "schemas"


def _load_schema(path: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / path).read_text(encoding="utf-8"))


def _validate(payload: Any, schema_path: str) -> dict[str, Any]:
    jsonable = to_jsonable(payload)
    try:
        validate(instance=jsonable, schema=_load_schema(schema_path))
    except ValidationError as exc:
        location = ".".join(str(item) for item in exc.absolute_path)
        prefix = f"{location}: " if location else ""
        raise ValueError(f"{prefix}{exc.message}") from exc
    return jsonable


def validate_candidate_record(record: Any) -> dict[str, Any]:
    payload = _validate(record, "experiments/bounded-candidate-record-v0.schema.json")
    if payload.get("solve_claim") is not False:
        raise ValueError("Candidate record must keep solve_claim=false.")
    return payload


def validate_run_summary(summary: Any) -> dict[str, Any]:
    payload = _validate(summary, "experiments/bounded-experiment-run-summary-v0.schema.json")
    if payload.get("generated_outputs_ignored") is not True:
        raise ValueError("Run summary must record generated_outputs_ignored=true.")
    return payload
