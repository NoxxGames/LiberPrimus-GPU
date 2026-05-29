from copy import deepcopy

from jsonschema import Draft202012Validator

from test_stage5by_common import STAGE5BY_RECORDS, ROOT, load_json, load_yaml


def test_stage5by_records_validate_against_schemas() -> None:
    for record_path in STAGE5BY_RECORDS:
        payload = load_yaml(record_path)
        schema = load_json(payload["schema"])
        Draft202012Validator(schema).validate(payload)


def test_stage5by_schema_rejects_solve_execution_and_active_ingestion() -> None:
    payload = load_yaml("data/project-state/stage5by-summary.yaml")
    schema = load_json(payload["schema"])
    for field in ["solve_claim", "execution_allowed", "string4_active_input_allowed"]:
        mutated = deepcopy(payload)
        mutated[field] = True
        assert list(Draft202012Validator(schema).iter_errors(mutated))


def test_stage5by_required_schemas_exist() -> None:
    for record_path in STAGE5BY_RECORDS:
        payload = load_yaml(record_path)
        assert (ROOT / payload["schema"]).is_file()
