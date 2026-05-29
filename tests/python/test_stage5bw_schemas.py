from jsonschema import Draft202012Validator

from test_stage5bw_common import STAGE5BW_RECORDS, ROOT, load_json, load_yaml


def test_stage5bw_records_validate_against_schemas() -> None:
    for record_path in STAGE5BW_RECORDS:
        payload = load_yaml(record_path)
        schema = load_json(payload["schema"])
        Draft202012Validator(schema).validate(payload)


def test_stage5bw_schema_rejects_solve_claim() -> None:
    payload = load_yaml("data/project-state/stage5bw-summary.yaml")
    schema = load_json(payload["schema"])
    payload["solve_claim"] = True
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors


def test_stage5bw_required_schemas_exist() -> None:
    for record_path in STAGE5BW_RECORDS:
        payload = load_yaml(record_path)
        assert (ROOT / payload["schema"]).is_file()
