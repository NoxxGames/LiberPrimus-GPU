"""Schema validation helpers for exploratory experiment records."""

from __future__ import annotations

import json
from typing import Any

from jsonschema import validate

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable

SCHEMA_DIR = repo_root() / "schemas/experiments"

SCHEMA_BY_RECORD_TYPE = {
    "exploratory_experiment_manifest": "exploratory-experiment-manifest-v0.schema.json",
    "exploratory_dry_run_plan": "exploratory-dry-run-plan-v0.schema.json",
}


def load_schema(schema_name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))


def validate_payload(payload: Any, schema_name: str) -> None:
    validate(instance=to_jsonable(payload), schema=load_schema(schema_name))


def validate_record(record: Any) -> dict[str, Any]:
    payload = to_jsonable(record)
    record_type = payload.get("record_type")
    if record_type not in SCHEMA_BY_RECORD_TYPE:
        raise ValueError(f"Unsupported exploratory experiment record_type: {record_type}")
    validate_payload(payload, SCHEMA_BY_RECORD_TYPE[str(record_type)])
    return payload
