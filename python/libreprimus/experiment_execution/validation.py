"""Schema validation helpers for Stage 2F execution records."""

from __future__ import annotations

import json
from typing import Any

from jsonschema import validate

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable

SCHEMA_DIR = repo_root() / "schemas/experiments"

SCHEMA_BY_RECORD_TYPE = {
    "cpu_execution_manifest": "cpu-execution-manifest-v0.schema.json",
    "cpu_execution_plan": "cpu-execution-plan-v0.schema.json",
    "cpu_execution_result": "cpu-execution-result-v0.schema.json",
    "synthetic_corpus_record": "synthetic-corpus-record-v0.schema.json",
}


def load_schema(schema_name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))


def validate_payload(payload: Any, schema_name: str) -> None:
    validate(instance=to_jsonable(payload), schema=load_schema(schema_name))


def validate_record(record: Any) -> dict[str, Any]:
    payload = to_jsonable(record)
    record_type = payload.get("record_type")
    if record_type not in SCHEMA_BY_RECORD_TYPE:
        raise ValueError(f"Unsupported CPU execution record_type: {record_type}")
    validate_payload(payload, SCHEMA_BY_RECORD_TYPE[str(record_type)])
    return payload

