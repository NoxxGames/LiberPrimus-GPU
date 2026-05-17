"""Schema and safety validation for Stage 3E backlog records."""

from __future__ import annotations

import json
from typing import Any

from jsonschema import ValidationError, validate

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable

SCHEMA_DIR = repo_root() / "schemas/experiments"


def _load_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def _validate(payload: Any, schema_name: str) -> dict[str, Any]:
    jsonable = to_jsonable(payload)
    try:
        validate(instance=jsonable, schema=_load_schema(schema_name))
    except ValidationError as exc:
        location = ".".join(str(item) for item in exc.absolute_path)
        prefix = f"{location}: " if location else ""
        raise ValueError(f"{prefix}{exc.message}") from exc
    return jsonable


def validate_method_backlog(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate(payload, "method-backlog-v0.schema.json")
    for item in validated.get("items", []):
        validate_method_backlog_item(dict(item))
    return validated


def validate_method_backlog_item(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate(payload, "method-backlog-item-v0.schema.json")
    _validate_false_flags(validated)
    return validated


def validate_stage3e_queue_item(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate(payload, "stage3e-queue-item-v0.schema.json")
    _validate_false_flags(validated)
    if any(_nested_true(validated, key) for key in {"dictionary_search_enabled", "key_search_enabled", "unconstrained_skip_masks"}):
        raise ValueError("Stage 3E queue item enables broad search or unconstrained skip masks.")
    return validated


def _validate_false_flags(payload: dict[str, Any]) -> None:
    if payload.get("cuda_enabled") is not False:
        raise ValueError("Stage 3E records require cuda_enabled=false.")
    if payload.get("no_solve_claim") is not True:
        raise ValueError("Stage 3E records require no_solve_claim=true.")
    if payload.get("canonical_corpus_active") is not False:
        raise ValueError("Stage 3E records require canonical_corpus_active=false.")
    if payload.get("page_boundaries_final") is not False:
        raise ValueError("Stage 3E records require page_boundaries_final=false.")


def _nested_true(payload: Any, key: str) -> bool:
    if isinstance(payload, dict):
        return payload.get(key) is True or any(_nested_true(value, key) for value in payload.values())
    if isinstance(payload, list):
        return any(_nested_true(value, key) for value in payload)
    return False
