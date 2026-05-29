from copy import deepcopy

from jsonschema import Draft202012Validator

from test_stage5bs_common import STAGE5BS_RECORDS, load_json, load_yaml


def test_stage5bs_yaml_records_validate_against_schemas() -> None:
    for data_path in STAGE5BS_RECORDS:
        payload = load_yaml(data_path)
        Draft202012Validator(load_json(payload["schema"])).validate(payload)


def test_stage5bs_schema_rejects_solve_claim_and_execution() -> None:
    payload = load_yaml("data/token-block/stage5bs-string4-planning-ingestion-gate.yaml")
    schema = load_json(payload["schema"])
    bad = deepcopy(payload)
    bad["solve_claim"] = True
    bad["execution_allowed"] = True

    assert list(Draft202012Validator(schema).iter_errors(bad))


def test_stage5bs_guardrail_schema_rejects_forbidden_true_flags() -> None:
    payload = load_yaml("data/historical-route/stage5bs-guardrail.yaml")
    schema = load_json(payload["schema"])
    bad = deepcopy(payload)
    bad["cuda_execution_performed"] = True
    bad["generated_outputs_committed"] = True
    bad["string4_active_input_allowed"] = True
    bad["variant_materialisation_performed"] = True

    assert list(Draft202012Validator(schema).iter_errors(bad))
