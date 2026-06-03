from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from test_stage5da_common import STAGE5DA_RECORDS, STAGE5DA_SCHEMAS, ensure_stage5da_built, load_yaml


def test_stage5da_schemas_validate_all_records() -> None:
    ensure_stage5da_built()
    for schema_path, record_path in zip(STAGE5DA_SCHEMAS, STAGE5DA_RECORDS, strict=True):
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(load_yaml(record_path))


@pytest.mark.parametrize(
    "field_name",
    [
        "solve_claim",
        "cuda_execution_performed",
        "generated_outputs_committed",
        "operator_decision_option_selected_now",
        "explicit_pause_selected_now",
        "operator_choice_or_pause_record_created_now",
    ],
)
def test_stage5da_summary_schema_rejects_prohibited_true_flags(field_name: str) -> None:
    ensure_stage5da_built()
    payload = load_yaml("data/project-state/stage5da-summary.yaml")
    schema = json.loads(
        Path("schemas/project-state/stage5da-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    payload[field_name] = True
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors


def test_stage5da_summary_schema_rejects_selected_option_id() -> None:
    ensure_stage5da_built()
    payload = load_yaml("data/project-state/stage5da-summary.yaml")
    schema = json.loads(
        Path("schemas/project-state/stage5da-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    payload["selected_option_id"] = "defer_for_more_review"
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors
