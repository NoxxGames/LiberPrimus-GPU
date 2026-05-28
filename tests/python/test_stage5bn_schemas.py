from copy import deepcopy

from jsonschema import Draft202012Validator

from test_stage5bn_common import STAGE5BN_RECORDS, load_json, load_yaml


def test_stage5bn_yaml_records_validate_against_schemas() -> None:
    for data_path in STAGE5BN_RECORDS:
        payload = load_yaml(data_path)
        Draft202012Validator(load_json(payload["schema"])).validate(payload)


def test_stage5bn_schema_rejects_solve_claim() -> None:
    payload = load_yaml("data/token-block/stage5bn-string4-unsupported-position-target.yaml")
    schema = load_json(payload["schema"])
    bad = deepcopy(payload)
    bad["solve_claim"] = True

    assert list(Draft202012Validator(schema).iter_errors(bad))


def test_stage5bn_schema_rejects_cuda_and_generated_output_publication() -> None:
    payload = load_yaml("data/historical-route/stage5bn-guardrail.yaml")
    schema = load_json(payload["schema"])
    bad = deepcopy(payload)
    bad["cuda_execution_performed"] = True
    bad["generated_outputs_committed"] = True

    assert list(Draft202012Validator(schema).iter_errors(bad))
