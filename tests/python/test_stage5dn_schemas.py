from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5dn_common import ROOT, STAGE5DN_RECORDS, STAGE5DN_SCHEMAS, ensure_stage5dn_built, load_yaml


def test_stage5dn_schemas_validate_records() -> None:
    ensure_stage5dn_built()

    for schema_path, record_path in zip(STAGE5DN_SCHEMAS, STAGE5DN_RECORDS, strict=True):
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record = load_yaml(record_path)
        assert list(Draft202012Validator(schema).iter_errors(record)) == []


def test_stage5dn_summary_schema_rejects_forbidden_flags() -> None:
    ensure_stage5dn_built()
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5dn-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    for forbidden in [
        "solve_claim",
        "execution_authorized_now",
        "generated_outputs_committed",
        "pivot_target_selected_now",
        "alberti_cipher_execution_performed_now",
        "html_tool_executed_now",
        "ocr_performed",
    ]:
        record = load_yaml("data/project-state/stage5dn-summary.yaml")
        record[forbidden] = True
        assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage5dn_schema_and_record_lists_are_populated() -> None:
    ensure_stage5dn_built()

    assert len(STAGE5DN_RECORDS) == 31
    assert len(STAGE5DN_SCHEMAS) == 31
