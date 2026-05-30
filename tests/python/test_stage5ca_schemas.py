import jsonschema

from test_stage5ca_common import STAGE5CA_RECORDS, ROOT, load_json, load_yaml


def test_stage5ca_records_validate_against_schemas() -> None:
    for path in STAGE5CA_RECORDS:
        payload = load_yaml(path)
        schema = load_json(payload["schema"])
        jsonschema.Draft202012Validator(schema).validate(payload)


def test_stage5ca_schema_rejects_solve_execution_and_active_ingestion() -> None:
    payload = load_yaml("data/project-state/stage5ca-summary.yaml")
    schema = load_json(payload["schema"])
    bad = dict(payload)
    bad["solve_claim"] = True
    bad["execution_allowed"] = True
    bad["string4_active_input_allowed"] = True
    validator = jsonschema.Draft202012Validator(schema)
    errors = list(validator.iter_errors(bad))
    assert len(errors) >= 3


def test_stage5ca_required_schemas_exist() -> None:
    for path in STAGE5CA_RECORDS:
        payload = load_yaml(path)
        assert (ROOT / payload["schema"]).is_file()
