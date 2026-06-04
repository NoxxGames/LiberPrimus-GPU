from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5dg_common import (
    ROOT,
    STAGE5DG_RECORDS,
    STAGE5DG_SCHEMAS,
    ensure_stage5dg_built,
    load_yaml,
)


def test_stage5dg_schemas_validate_records() -> None:
    ensure_stage5dg_built()

    for schema_path in STAGE5DG_SCHEMAS:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record_path = schema_path.replace("schemas/", "data/").replace("-v0.schema.json", ".yaml")
        record = load_yaml(record_path)
        errors = list(Draft202012Validator(schema).iter_errors(record))
        assert errors == []


def test_stage5dg_schema_rejects_solve_cuda_generated_and_approval_downgrade() -> None:
    ensure_stage5dg_built()
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5dg-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    record = load_yaml("data/project-state/stage5dg-summary.yaml")

    record["solve_claim"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))

    record = load_yaml("data/project-state/stage5dg-summary.yaml")
    record["cuda_execution_performed"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))

    record = load_yaml("data/project-state/stage5dg-summary.yaml")
    record["generated_outputs_committed"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))

    record = load_yaml("data/project-state/stage5dg-summary.yaml")
    record["real_operator_approval_record_created_now"] = False
    assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage5dg_record_and_schema_lists_are_populated() -> None:
    ensure_stage5dg_built()

    assert len(STAGE5DG_RECORDS) == 25
    assert len(STAGE5DG_SCHEMAS) == len(STAGE5DG_RECORDS)
