from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5dl_common import ROOT, STAGE5DL_RECORDS, STAGE5DL_SCHEMAS, ensure_stage5dl_built, load_yaml


def test_stage5dl_schemas_validate_records() -> None:
    ensure_stage5dl_built()

    for schema_path, record_path in zip(STAGE5DL_SCHEMAS, STAGE5DL_RECORDS, strict=True):
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record = load_yaml(record_path)
        errors = list(Draft202012Validator(schema).iter_errors(record))
        assert errors == []


def test_stage5dl_summary_schema_rejects_solve_execution_and_generated_output() -> None:
    ensure_stage5dl_built()
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5dl-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    for forbidden in [
        "solve_claim",
        "execution_authorized_now",
        "generated_outputs_committed",
        "pivot_target_selected_now",
    ]:
        record = load_yaml("data/project-state/stage5dl-summary.yaml")
        record[forbidden] = True
        assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage5dl_schema_and_record_lists_are_populated() -> None:
    ensure_stage5dl_built()

    assert len(STAGE5DL_RECORDS) == 29
    assert len(STAGE5DL_SCHEMAS) == 29
