from copy import deepcopy

import pytest
from jsonschema import Draft202012Validator, ValidationError

from test_stage5bu_common import STAGE5BU_RECORDS, load_json, load_yaml


def test_stage5bu_yaml_records_validate_against_schemas() -> None:
    for record_path in STAGE5BU_RECORDS:
        payload = load_yaml(record_path)
        schema = load_json(payload["schema"])
        Draft202012Validator(schema).validate(payload)


def test_stage5bu_schema_rejects_solve_claim_and_execution() -> None:
    payload = load_yaml("data/project-state/stage5bu-summary.yaml")
    schema = load_json(payload["schema"])
    bad = deepcopy(payload)
    bad["solve_claim"] = True
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(bad)
    bad = deepcopy(payload)
    bad["execution_allowed"] = True
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(bad)
