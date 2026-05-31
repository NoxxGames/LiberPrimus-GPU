import json

import jsonschema

from test_stage5cg_common import ROOT, STAGE5CG_RECORDS, load_yaml


def test_stage5cg_records_validate_against_schemas() -> None:
    for path in STAGE5CG_RECORDS:
        payload = load_yaml(path)
        schema = json.loads((ROOT / payload["schema"]).read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(payload)


def test_stage5cg_schema_rejects_solve_execution_and_gate_satisfaction() -> None:
    payload = load_yaml("data/project-state/stage5cg-summary.yaml")
    schema = json.loads((ROOT / payload["schema"]).read_text(encoding="utf-8"))
    bad = dict(payload)
    bad["solve_claim"] = True
    bad["execution_allowed"] = True
    bad["approval_gate_satisfied_now"] = True
    bad["activation_authorized_now"] = True
    validator = jsonschema.Draft202012Validator(schema)
    errors = list(validator.iter_errors(bad))
    assert len(errors) >= 4


def test_stage5cg_required_schemas_exist() -> None:
    for path in STAGE5CG_RECORDS:
        payload = load_yaml(path)
        assert (ROOT / payload["schema"]).is_file()
