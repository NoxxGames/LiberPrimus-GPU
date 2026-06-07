from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from test_stage5dq_common import ROOT, STAGE5DQ_RECORDS, STAGE5DQ_SCHEMAS, ensure_stage5dq_built, load_yaml

OPERATOR_CONSOLE_SCHEMA_RECORDS = [
    ("data/operator-console/source-browser/path-aliases/default.yaml", "schemas/operator-console/source-browser-path-aliases-v0.schema.json"),
    (
        "data/operator-console/source-browser/column-profiles/default.yaml",
        "schemas/operator-console/source-browser-column-profile-v0.schema.json",
    ),
]


def test_stage5dq_schemas_validate_records() -> None:
    ensure_stage5dq_built()

    assert len(STAGE5DQ_RECORDS) == len(STAGE5DQ_SCHEMAS)
    for record_path, schema_path in zip(STAGE5DQ_RECORDS, STAGE5DQ_SCHEMAS, strict=True):
        record = load_yaml(record_path)
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(record))
        assert errors == []


def test_operator_console_config_schemas_validate() -> None:
    for record_path, schema_path in OPERATOR_CONSOLE_SCHEMA_RECORDS:
        record = yaml.safe_load(Path(record_path).read_text(encoding="utf-8"))
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        assert list(Draft202012Validator(schema).iter_errors(record)) == []


def test_stage5dq_schema_rejects_execution_flags() -> None:
    ensure_stage5dq_built()
    record = load_yaml("data/project-state/stage5dq-summary.yaml")
    schema = json.loads((ROOT / "schemas/project-state/stage5dq-summary-v0.schema.json").read_text(encoding="utf-8"))

    record["solve_claim"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))

    record["solve_claim"] = False
    record["source_browser_runs_ocr"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))
