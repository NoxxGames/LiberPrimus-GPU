from copy import deepcopy

from jsonschema import Draft202012Validator

from test_stage5bq_common import STAGE5BQ_RECORDS, load_json, load_yaml


def test_stage5bq_yaml_records_validate_against_schemas() -> None:
    for data_path in STAGE5BQ_RECORDS:
        payload = load_yaml(data_path)
        Draft202012Validator(load_json(payload["schema"])).validate(payload)


def test_stage5bq_schema_rejects_solve_claim_and_execution() -> None:
    payload = load_yaml("data/token-block/stage5bq-string4-inactive-branch-planning-context.yaml")
    schema = load_json(payload["schema"])
    bad = deepcopy(payload)
    bad["solve_claim"] = True
    bad["execution_allowed"] = True

    assert list(Draft202012Validator(schema).iter_errors(bad))


def test_stage5bq_guardrail_schema_rejects_forbidden_true_flags() -> None:
    payload = load_yaml("data/historical-route/stage5bq-guardrail.yaml")
    schema = load_json(payload["schema"])
    bad = deepcopy(payload)
    bad["cuda_execution_performed"] = True
    bad["generated_outputs_committed"] = True
    bad["string4_active_input_allowed"] = True

    assert list(Draft202012Validator(schema).iter_errors(bad))
