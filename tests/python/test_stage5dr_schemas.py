from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5dr_common import ROOT, STAGE5DR_SCHEMAS, ensure_stage5dr_built, load_yaml


def test_stage5dr_schemas_validate_records() -> None:
    ensure_stage5dr_built()

    schema_pairs = [
        ("data/project-state/stage5dr-summary.yaml", "schemas/project-state/stage5dr-summary-v0.schema.json"),
        (
            "data/project-state/stage5dr-gui-refinement-summary.yaml",
            "schemas/project-state/stage5dr-gui-refinement-summary-v0.schema.json",
        ),
        (
            "data/project-state/stage5dr-operator-console-scope-control.yaml",
            "schemas/project-state/stage5dr-operator-console-scope-control-v0.schema.json",
        ),
    ]
    assert len(STAGE5DR_SCHEMAS) == 3
    for record_path, schema_path in schema_pairs:
        record = load_yaml(record_path)
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        assert list(Draft202012Validator(schema).iter_errors(record)) == []


def test_stage5dr_schema_rejects_execution_flags() -> None:
    ensure_stage5dr_built()
    record = load_yaml("data/project-state/stage5dr-summary.yaml")
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5dr-summary-v0.schema.json").read_text(encoding="utf-8")
    )

    record["solve_claim"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))

    record["solve_claim"] = False
    record["ocr_performed"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))
