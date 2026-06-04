from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5de_common import (
    ROOT,
    STAGE5DE_RECORDS,
    STAGE5DE_SCHEMAS,
    ensure_stage5de_built,
    load_yaml,
)


def test_stage5de_schemas_validate_records() -> None:
    ensure_stage5de_built()

    for schema_path in STAGE5DE_SCHEMAS:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record_path = schema_path.replace("schemas/", "data/").replace("-v0.schema.json", ".yaml")
        record = load_yaml(record_path)
        errors = list(Draft202012Validator(schema).iter_errors(record))
        assert errors == []


def test_stage5de_schema_rejects_solve_claim_execution_and_approval() -> None:
    ensure_stage5de_built()
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5de-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    record = load_yaml("data/project-state/stage5de-summary.yaml")

    record["solve_claim"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))

    record = load_yaml("data/project-state/stage5de-summary.yaml")
    record["execution_authorized_now"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))

    record = load_yaml("data/project-state/stage5de-summary.yaml")
    record["real_operator_approval_record_created_now"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage5de_record_and_schema_lists_are_populated() -> None:
    ensure_stage5de_built()

    assert len(STAGE5DE_RECORDS) == 23
    assert len(STAGE5DE_SCHEMAS) == len(STAGE5DE_RECORDS)
