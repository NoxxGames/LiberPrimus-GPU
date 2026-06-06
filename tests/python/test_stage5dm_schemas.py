from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5dm_common import ROOT, STAGE5DM_RECORDS, STAGE5DM_SCHEMAS, ensure_stage5dm_built, load_yaml


def test_stage5dm_schemas_validate_records() -> None:
    ensure_stage5dm_built()

    for schema_path, record_path in zip(STAGE5DM_SCHEMAS, STAGE5DM_RECORDS, strict=True):
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record = load_yaml(record_path)
        assert list(Draft202012Validator(schema).iter_errors(record)) == []


def test_stage5dm_summary_schema_rejects_forbidden_flags() -> None:
    ensure_stage5dm_built()
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5dm-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    for forbidden in [
        "solve_claim",
        "execution_authorized_now",
        "generated_outputs_committed",
        "pivot_target_selected_now",
        "stage5dm_builds_evidence_atlas_tool_now",
    ]:
        record = load_yaml("data/project-state/stage5dm-summary.yaml")
        record[forbidden] = True
        assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage5dm_schema_and_record_lists_are_populated() -> None:
    ensure_stage5dm_built()

    assert len(STAGE5DM_RECORDS) == 19
    assert len(STAGE5DM_SCHEMAS) == 19
