import json

import pytest
from jsonschema import Draft202012Validator, ValidationError

from test_stage5cu_common import (
    ROOT,
    STAGE5CU_RECORDS,
    STAGE5CU_SCHEMAS,
    ensure_stage5cu_built,
    load_yaml,
)


def test_stage5cu_schemas_validate_records() -> None:
    ensure_stage5cu_built()
    assert len(STAGE5CU_RECORDS) == len(STAGE5CU_SCHEMAS)
    for record_path in STAGE5CU_RECORDS:
        payload = load_yaml(record_path)
        schema = json.loads((ROOT / payload["schema"]).read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(payload)


def test_stage5cu_schema_rejects_solve_claim() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/project-state/stage5cu-summary.yaml")
    payload["solve_claim"] = True
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5cu-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(payload)


def test_stage5cu_schema_rejects_selected_option() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/token-block/stage5cu-operator-options-nonselection-proof.yaml")
    payload["operator_decision_option_selected_now"] = True
    schema = json.loads((ROOT / payload["schema"]).read_text(encoding="utf-8"))
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(payload)
