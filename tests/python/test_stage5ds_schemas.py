from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5ds_common import ROOT, STAGE5DS_SCHEMAS, ensure_stage5ds_built, load_yaml
from libreprimus.token_block.stage5ds import DATA_PATHS


def test_stage5ds_schemas_validate_records() -> None:
    ensure_stage5ds_built()
    for schema_path in STAGE5DS_SCHEMAS:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    for record_path in DATA_PATHS.values():
        record = load_yaml(record_path)
        schema_path = record.get("schema")
        if not schema_path:
            continue
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(record))
        assert not errors, f"{record_path}: {errors}"


def test_stage5ds_schema_rejects_execution_flags() -> None:
    ensure_stage5ds_built()
    record = load_yaml("data/project-state/stage5ds-summary.yaml")
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5ds-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    record["solve_claim"] = True
    errors = list(Draft202012Validator(schema).iter_errors(record))
    assert errors
