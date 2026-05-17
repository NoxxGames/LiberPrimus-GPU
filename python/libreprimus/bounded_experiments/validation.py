"""Schema and policy validation for Stage 2J bounded experiments."""

from __future__ import annotations

import json
from typing import Any

from jsonschema import ValidationError, validate

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable

SCHEMA_DIR = repo_root() / "schemas/experiments"

SCHEMA_BY_NAME = {
    "operator_policy": "operator-policy-v0.schema.json",
    "bounded_experiment_queue": "bounded-experiment-queue-v0.schema.json",
    "bounded_experiment_item": "bounded-experiment-item-v0.schema.json",
    "policy_check_result": "policy-check-result-v0.schema.json",
    "bounded_auto_run_result": "bounded-auto-run-result-v0.schema.json",
}


def load_schema(schema_name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))


def validate_payload(payload: Any, schema_name: str) -> None:
    try:
        validate(instance=to_jsonable(payload), schema=load_schema(schema_name))
    except ValidationError as exc:
        location = ".".join(str(item) for item in exc.absolute_path)
        prefix = f"{location}: " if location else ""
        raise ValueError(f"{prefix}{exc.message}") from exc


def validate_operator_policy_payload(payload: dict[str, Any]) -> None:
    validate_payload(payload, SCHEMA_BY_NAME["operator_policy"])
    limits = payload["limits"]
    if limits["max_candidate_count"] > 100000:
        raise ValueError("Operator policy max_candidate_count must be <= 100000.")
    if limits["max_estimated_runtime_seconds"] > 600:
        raise ValueError("Operator policy max_estimated_runtime_seconds must be <= 600.")
    if limits["max_generated_output_mb"] > 250:
        raise ValueError("Operator policy max_generated_output_mb must be <= 250.")
    allowed = payload["allowed_execution"]
    if allowed.get("cpu_only") is not True:
        raise ValueError("Operator policy requires cpu_only=true.")
    for field in ["cuda_enabled", "cloud_execution", "paid_services"]:
        if allowed.get(field) is not False:
            raise ValueError(f"Operator policy requires {field}=false.")


def validate_bounded_item_payload(payload: dict[str, Any]) -> None:
    validate_payload(payload, SCHEMA_BY_NAME["bounded_experiment_item"])
    if payload.get("cuda_enabled") is not False:
        raise ValueError("Bounded items require cuda_enabled=false.")
    if payload.get("no_solve_claim") is not True:
        raise ValueError("Bounded items require no_solve_claim=true.")


def validate_queue_payload(payload: dict[str, Any]) -> None:
    validate_payload(payload, SCHEMA_BY_NAME["bounded_experiment_queue"])
    for field in ["canonical_corpus_active", "page_boundaries_final", "trusted_as_canonical"]:
        if payload.get(field) is not False:
            raise ValueError(f"Bounded queues require {field}=false.")
    for item in payload.get("items", []):
        validate_bounded_item_payload(dict(item))


def validate_policy_check_result(record: Any) -> dict[str, Any]:
    payload = to_jsonable(record)
    validate_payload(payload, SCHEMA_BY_NAME["policy_check_result"])
    return payload


def validate_bounded_auto_run_result(record: Any) -> dict[str, Any]:
    payload = to_jsonable(record)
    validate_payload(payload, SCHEMA_BY_NAME["bounded_auto_run_result"])
    text = json.dumps(payload, sort_keys=True)
    if "candidate_plaintext" in text or "candidate_plaintexts" in text:
        raise ValueError("Bounded auto-run results must not contain candidate plaintext fields.")
    for field in [
        "cuda_used",
        "solve_claim_made",
        "canonical_corpus_active",
        "page_boundaries_final",
        "trusted_as_canonical",
    ]:
        if payload.get(field) is not False:
            raise ValueError(f"Bounded auto-run results require {field}=false.")
    return payload
