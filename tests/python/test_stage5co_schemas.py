import json

from jsonschema import Draft202012Validator

from test_stage5co_common import ROOT, STAGE5CO_RECORDS, STAGE5CO_SCHEMAS, load_yaml


def test_stage5co_schemas_validate_records() -> None:
    for schema_path in STAGE5CO_SCHEMAS:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)

    for record_path in STAGE5CO_RECORDS:
        schema_path = (
            record_path.replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
        )
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(load_yaml(record_path)))
        assert errors == []


def test_stage5co_schema_rejects_solve_claim() -> None:
    payload = load_yaml("data/project-state/stage5co-summary.yaml")
    payload["solve_claim"] = True
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5co-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert list(Draft202012Validator(schema).iter_errors(payload))
