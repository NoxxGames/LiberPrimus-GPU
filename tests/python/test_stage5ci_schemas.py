import json

import jsonschema

from test_stage5ci_common import ROOT, STAGE5CI_RECORDS, load_yaml


def test_stage5ci_records_validate_against_schemas() -> None:
    for path in STAGE5CI_RECORDS:
        payload = load_yaml(path)
        schema = json.loads((ROOT / payload["schema"]).read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(payload)


def test_stage5ci_schema_rejects_solve_cuda_and_approval_satisfaction() -> None:
    payload = load_yaml("data/project-state/stage5ci-summary.yaml")
    schema = json.loads((ROOT / payload["schema"]).read_text(encoding="utf-8"))
    bad = dict(payload)
    bad["solve_claim"] = True
    bad["execution_allowed"] = True
    bad["approval_gate_satisfied_now"] = True
    bad["activation_authorized_now"] = True
    bad["cuda_execution_performed"] = True
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(bad))
    assert len(errors) >= 5


def test_stage5ci_required_schemas_exist() -> None:
    for path in STAGE5CI_RECORDS:
        payload = load_yaml(path)
        assert (ROOT / payload["schema"]).is_file()
