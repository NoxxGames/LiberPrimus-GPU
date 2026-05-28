from jsonschema import Draft202012Validator

from test_stage5bm_common import STAGE5BM_RECORDS, load_json, load_yaml


def test_stage5bm_yaml_records_validate_against_schemas() -> None:
    for data_path in STAGE5BM_RECORDS:
        payload = load_yaml(data_path)
        Draft202012Validator(load_json(payload["schema"])).validate(payload)


def test_stage5bm_branch_schema_rejects_solve_claim() -> None:
    payload = load_yaml("data/token-block/stage5bm-string4-stage5aw-branch-membership.yaml")
    schema = load_json(payload["schema"])
    payload["solve_claim"] = True

    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors
