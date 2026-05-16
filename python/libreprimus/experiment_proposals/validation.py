"""Schema validation helpers for Stage 2G proposal records."""

from __future__ import annotations

import json
from typing import Any

from jsonschema import validate

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable

SCHEMA_DIR = repo_root() / "schemas/experiments"

SCHEMA_BY_RECORD_TYPE = {
    "experiment_proposal": "experiment-proposal-v0.schema.json",
    "experiment_review_checklist": "experiment-review-checklist-v0.schema.json",
    "experiment_approval_record": "experiment-approval-record-v0.schema.json",
    "experiment_review_packet": "experiment-review-packet-v0.schema.json",
}


def load_schema(schema_name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))


def validate_payload(payload: Any, schema_name: str) -> None:
    validate(instance=to_jsonable(payload), schema=load_schema(schema_name))


def validate_record(record: Any) -> dict[str, Any]:
    payload = to_jsonable(record)
    record_type = payload.get("record_type")
    if record_type not in SCHEMA_BY_RECORD_TYPE:
        raise ValueError(f"Unsupported proposal record_type: {record_type}")
    validate_payload(payload, SCHEMA_BY_RECORD_TYPE[str(record_type)])
    return payload

