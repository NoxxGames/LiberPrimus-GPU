from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/observations/observation-review-state-v0.schema.json",
    "schemas/observations/observation-review-decision-v0.schema.json",
    "schemas/observations/observation-promotion-record-v0.schema.json",
    "schemas/observations/observation-quarantine-record-v0.schema.json",
    "schemas/observations/observation-review-summary-v0.schema.json",
    "schemas/observations/observation-review-policy-v0.schema.json",
]


def test_stage4j_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4j_decision_schema_rejects_seed_and_solve_claim() -> None:
    schema = json.loads(Path("schemas/observations/observation-review-decision-v0.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    record = _decision()
    record["usable_as_experiment_seed"] = True
    assert list(validator.iter_errors(record))
    record = _decision()
    record["solve_claim"] = True
    assert list(validator.iter_errors(record))


def _decision() -> dict:
    return {
        "record_type": "observation_review_decision",
        "review_decision_id": "decision-1",
        "observation_id": "obs-1",
        "observation_type": "negative_control",
        "review_state": "negative_control",
        "reviewed_by": "automated_policy_check",
        "source_locked": True,
        "solve_claim": False,
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
    }
