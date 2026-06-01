import json

import pytest
from jsonschema import Draft202012Validator, ValidationError

from test_stage5cs_common import (
    ROOT,
    STAGE5CS_RECORDS,
    STAGE5CS_SCHEMAS,
    ensure_stage5cs_built,
    load_yaml,
)


def test_stage5cs_schemas_validate_records() -> None:
    ensure_stage5cs_built()
    assert len(STAGE5CS_RECORDS) == len(STAGE5CS_SCHEMAS)
    for record_path in STAGE5CS_RECORDS:
        payload = load_yaml(record_path)
        schema = json.loads((ROOT / payload["schema"]).read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(payload)


def test_stage5cs_schema_rejects_solve_claim() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/project-state/stage5cs-summary.yaml")
    payload["solve_claim"] = True
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5cs-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(payload)


def test_stage5cs_schema_rejects_execution_flag() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-no-execution-transition-gate.yaml")
    payload["execution_authorized_now"] = True
    schema = json.loads((ROOT / payload["schema"]).read_text(encoding="utf-8"))
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(payload)
