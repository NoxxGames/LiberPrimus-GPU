"""Validation helpers for minimal triage score records."""

from __future__ import annotations

import json
from typing import Any

from jsonschema import ValidationError, validate

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable

SCHEMA_PATH = repo_root() / "schemas/scoring/minimal-triage-score-v0.schema.json"


def validate_minimal_triage_score(score: Any) -> dict[str, Any]:
    payload = to_jsonable(score)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        validate(instance=payload, schema=schema)
    except ValidationError as exc:
        location = ".".join(str(item) for item in exc.absolute_path)
        prefix = f"{location}: " if location else ""
        raise ValueError(f"{prefix}{exc.message}") from exc
    return payload
