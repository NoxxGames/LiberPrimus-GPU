import json

import jsonschema

from test_stage5ck_common import ROOT, STAGE5CK_RECORDS, load_yaml


def test_stage5ck_records_validate_against_schemas() -> None:
    for path in STAGE5CK_RECORDS:
        payload = load_yaml(path)
        schema = json.loads((ROOT / payload["schema"]).read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(payload)


def test_stage5ck_schema_rejects_solve_execution_and_activation() -> None:
    payload = load_yaml("data/project-state/stage5ck-summary.yaml")
    schema = json.loads((ROOT / payload["schema"]).read_text(encoding="utf-8"))
    bad = dict(payload)
    bad["solve_claim"] = True
    bad["execution_allowed"] = True
    bad["activation_authorized_now"] = True
    bad["active_planning_input_selected_now"] = True
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(bad))
    assert len(errors) >= 4


def test_stage5ck_required_schemas_exist() -> None:
    for path in STAGE5CK_RECORDS:
        payload = load_yaml(path)
        assert (ROOT / payload["schema"]).is_file()
