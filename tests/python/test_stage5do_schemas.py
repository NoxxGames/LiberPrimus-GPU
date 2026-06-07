from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5do_common import ROOT, STAGE5DO_RECORDS, STAGE5DO_SCHEMAS, ensure_stage5do_built, load_yaml


def test_stage5do_schemas_validate_records() -> None:
    ensure_stage5do_built()

    for schema_path, record_path in zip(STAGE5DO_SCHEMAS, STAGE5DO_RECORDS, strict=True):
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record = load_yaml(record_path)
        assert list(Draft202012Validator(schema).iter_errors(record)) == []


def test_stage5do_summary_schema_rejects_forbidden_flags() -> None:
    ensure_stage5do_built()
    schema = json.loads((ROOT / "schemas/project-state/stage5do-summary-v0.schema.json").read_text())
    for forbidden in [
        "solve_claim",
        "execution_authorized_now",
        "generated_outputs_committed",
        "pivot_target_selected_now",
        "source_browser_gui_implemented_now",
        "ocr_performed",
        "image_forensics_performed",
        "cuda_execution_performed",
    ]:
        record = load_yaml("data/project-state/stage5do-summary.yaml")
        record[forbidden] = True
        assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage5do_schema_and_record_lists_are_populated() -> None:
    ensure_stage5do_built()

    assert len(STAGE5DO_RECORDS) == 31
    assert len(STAGE5DO_SCHEMAS) == 31
