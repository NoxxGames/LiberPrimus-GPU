"""JSON schema validation for result-store records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import validate

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable

SCHEMA_DIR = repo_root() / "schemas/results"

SCHEMA_BY_RECORD_TYPE = {
    "experiment_run_record": "experiment-run-record-v0.schema.json",
    "experiment_run_summary": "experiment-run-summary-v0.schema.json",
    "experiment_event_record": "experiment-event-record-v0.schema.json",
    "experiment_artifact_record": "experiment-artifact-record-v0.schema.json",
    "experiment_result_store_manifest": "experiment-result-store-manifest-v0.schema.json",
    "sqlite_result_store_schema": "sqlite-result-store-v0.schema.json",
}


def load_schema(schema_name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))


def validate_payload(payload: Any, schema_name: str) -> None:
    validate(instance=to_jsonable(payload), schema=load_schema(schema_name))


def validate_record(record: Any) -> dict[str, Any]:
    payload = to_jsonable(record)
    record_type = payload.get("record_type")
    if record_type not in SCHEMA_BY_RECORD_TYPE:
        raise ValueError(f"Unsupported result-store record_type: {record_type}")
    validate_payload(payload, SCHEMA_BY_RECORD_TYPE[str(record_type)])
    return payload


def load_yaml_payload(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"YAML payload must be a mapping: {path}")
    return payload


def validate_result_store_manifest_payload(payload: dict[str, Any]) -> None:
    validate_payload(payload, "experiment-result-store-manifest-v0.schema.json")
