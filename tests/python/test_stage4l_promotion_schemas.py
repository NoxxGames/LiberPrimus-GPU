from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/observations/reviewed-observation-promotion-ledger-v0.schema.json",
    "schemas/observations/observation-promotion-readiness-record-v0.schema.json",
    "schemas/observations/observation-promotion-blocker-record-v0.schema.json",
    "schemas/experiments/manifest-readiness-record-v0.schema.json",
    "schemas/experiments/manifest-readiness-summary-v0.schema.json",
]


def test_stage4l_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4l_schema_rejects_solve_claim() -> None:
    schema = json.loads(
        Path("schemas/observations/reviewed-observation-promotion-ledger-v0.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    record = _ledger_record()
    record["solve_claim"] = True
    assert list(validator.iter_errors(record))


def _ledger_record() -> dict:
    return {
        "record_type": "reviewed_observation_promotion_ledger_record",
        "ledger_record_id": "stage4l-ledger-test",
        "review_decision_id": "decision-test",
        "observation_id": "observation-test",
        "promotion_category": "ready_as_control_only",
        "blocker_ids": [],
        "source_lock_status": "source_locked",
        "execution_enabled": False,
        "solve_claim": False,
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
    }
