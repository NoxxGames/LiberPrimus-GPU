"""Schema validation helpers for Stage 2I approval-readiness records."""

from __future__ import annotations

import json
from typing import Any

from jsonschema import validate

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable

SCHEMA_DIR = repo_root() / "schemas/experiments"

SCHEMA_BY_RECORD_TYPE = {
    "approval_readiness_packet": "approval-readiness-packet-v0.schema.json",
}


def load_schema(schema_name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))


def validate_payload(payload: Any, schema_name: str) -> None:
    validate(instance=to_jsonable(payload), schema=load_schema(schema_name))


def validate_record(record: Any) -> dict[str, Any]:
    payload = to_jsonable(record)
    record_type = payload.get("record_type")
    if record_type not in SCHEMA_BY_RECORD_TYPE:
        raise ValueError(f"Unsupported approval-readiness record_type: {record_type}")
    validate_payload(payload, SCHEMA_BY_RECORD_TYPE[str(record_type)])
    validate_approval_readiness_payload(payload)
    return payload


def validate_approval_readiness_payload(payload: dict[str, Any]) -> None:
    for field in [
        "approved_for_execution",
        "execution_enabled",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
        "trusted_as_canonical",
    ]:
        if payload.get(field) is not False:
            raise ValueError(f"Approval-readiness packets require {field}=false.")
    if payload.get("real_unsolved_material_touched") is True and payload.get("approval_status") == "approved":
        raise ValueError("Stage 2I real exploratory packets must not be approved.")
    if not payload.get("blocking_conditions"):
        raise ValueError("Approval-readiness packets require blocking_conditions.")
    if payload.get("human_decision_required") is not True:
        raise ValueError("Approval-readiness packets require human_decision_required=true.")
    if not payload.get("machine_check_results"):
        raise ValueError("Approval-readiness packets require machine_check_results.")
    if not payload.get("decision_options"):
        raise ValueError("Approval-readiness packets require decision_options.")
    if not payload.get("next_commands"):
        raise ValueError("Approval-readiness packets require next_commands.")
    text = json.dumps(to_jsonable(payload), sort_keys=True)
    if "candidate_plaintext" in text or "candidate_plaintexts" in text:
        raise ValueError("Approval-readiness packets must not contain candidate plaintext fields.")
    if "BEGIN RAW" in text or "data/raw/" in text:
        raise ValueError("Approval-readiness packets must not contain raw unsolved text.")
