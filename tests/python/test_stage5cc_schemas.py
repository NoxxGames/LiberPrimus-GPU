import jsonschema

from test_stage5cc_common import ROOT, STAGE5CC_RECORDS, load_json, load_yaml


def test_stage5cc_records_validate_against_schemas() -> None:
    for path in STAGE5CC_RECORDS:
        payload = load_yaml(path)
        schema = load_json(payload["schema"])
        jsonschema.Draft202012Validator(schema).validate(payload)


def test_stage5cc_schema_rejects_solve_execution_and_outputs() -> None:
    payload = load_yaml("data/project-state/stage5cc-summary.yaml")
    schema = load_json(payload["schema"])
    bad = dict(payload)
    bad["solve_claim"] = True
    bad["execution_allowed"] = True
    bad["generated_outputs_committed"] = True
    validator = jsonschema.Draft202012Validator(schema)
    errors = list(validator.iter_errors(bad))
    assert len(errors) >= 3


def test_stage5cc_required_schemas_exist() -> None:
    for path in STAGE5CC_RECORDS:
        payload = load_yaml(path)
        assert (ROOT / payload["schema"]).is_file()
