from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5dp_common import ROOT, STAGE5DP_RECORDS, STAGE5DP_SCHEMAS, ensure_stage5dp_built, load_yaml


def test_stage5dp_schemas_validate_records() -> None:
    ensure_stage5dp_built()

    assert len(STAGE5DP_RECORDS) == len(STAGE5DP_SCHEMAS)
    for record_path, schema_path in zip(STAGE5DP_RECORDS, STAGE5DP_SCHEMAS, strict=True):
        record = load_yaml(record_path)
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(record))
        assert errors == []


def test_stage5dp_schema_rejects_execution_flags() -> None:
    ensure_stage5dp_built()
    record = load_yaml("data/project-state/stage5dp-summary.yaml")
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5dp-summary-v0.schema.json").read_text(encoding="utf-8")
    )
    record["solve_claim"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))

    record["solve_claim"] = False
    record["route_extraction_performed_now"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))
