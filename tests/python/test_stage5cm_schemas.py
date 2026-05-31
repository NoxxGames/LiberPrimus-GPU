import json

from jsonschema import Draft202012Validator

from test_stage5cm_common import ROOT, STAGE5CM_RECORDS, STAGE5CM_SCHEMAS, load_yaml


def test_stage5cm_schemas_validate_records() -> None:
    for schema_path in STAGE5CM_SCHEMAS:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)

    for record_path in STAGE5CM_RECORDS:
        schema_path = (
            record_path.replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
        )
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(load_yaml(record_path)))
        assert errors == []


def test_stage5cm_schema_rejects_solve_claim() -> None:
    record_path = "data/project-state/stage5cm-summary.yaml"
    schema_path = "schemas/project-state/stage5cm-summary-v0.schema.json"
    payload = load_yaml(record_path)
    payload["solve_claim"] = True
    schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors
