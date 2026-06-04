from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5dc_common import (
    ROOT,
    STAGE5DC_RECORDS,
    STAGE5DC_SCHEMAS,
    ensure_stage5dc_built,
    load_yaml,
)


def test_stage5dc_schemas_validate_records() -> None:
    ensure_stage5dc_built()

    for schema_path in STAGE5DC_SCHEMAS:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record_path = schema_path.replace("schemas/", "data/").replace("-v0.schema.json", ".yaml")
        record = load_yaml(record_path)
        errors = list(Draft202012Validator(schema).iter_errors(record))
        assert errors == []


def test_stage5dc_schema_rejects_solve_claim_and_execution() -> None:
    ensure_stage5dc_built()
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5dc-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    record = load_yaml("data/project-state/stage5dc-summary.yaml")

    record["solve_claim"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))

    record = load_yaml("data/project-state/stage5dc-summary.yaml")
    record["execution_authorized_now"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage5dc_record_and_schema_lists_are_populated() -> None:
    ensure_stage5dc_built()

    assert len(STAGE5DC_RECORDS) >= 18
    assert len(STAGE5DC_SCHEMAS) == len(STAGE5DC_RECORDS)
