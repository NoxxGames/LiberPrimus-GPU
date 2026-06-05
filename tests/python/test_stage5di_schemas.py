from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5di_common import (
    ROOT,
    STAGE5DI_RECORDS,
    STAGE5DI_SCHEMAS,
    ensure_stage5di_built,
    load_yaml,
)


def test_stage5di_schemas_validate_records() -> None:
    ensure_stage5di_built()

    for schema_path in STAGE5DI_SCHEMAS:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record_path = schema_path.replace("schemas/", "data/").replace("-v0.schema.json", ".yaml")
        record = load_yaml(record_path)
        errors = list(Draft202012Validator(schema).iter_errors(record))
        assert errors == []


def test_stage5di_schema_rejects_solve_cuda_execution_and_pivot_selection() -> None:
    ensure_stage5di_built()
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5di-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )

    for field in [
        "solve_claim",
        "cuda_execution_performed",
        "execution_authorized_now",
        "pivot_target_selected_now",
        "byte_stream_generation_authorized_now",
    ]:
        record = load_yaml("data/project-state/stage5di-summary.yaml")
        record[field] = True
        assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage5di_record_and_schema_lists_are_populated() -> None:
    ensure_stage5di_built()

    assert len(STAGE5DI_RECORDS) == 35
    assert len(STAGE5DI_SCHEMAS) == len(STAGE5DI_RECORDS)
