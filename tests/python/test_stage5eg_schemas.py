from __future__ import annotations

from jsonschema import Draft202012Validator, ValidationError

from libreprimus.token_block import stage5eg
from test_stage5eg_common import ensure_stage5eg_built, load_yaml


def test_stage5eg_schemas_validate_all_payloads() -> None:
    ensure_stage5eg_built()

    for key, data_path in stage5eg.DATA_PATHS.items():
        schema = load_yaml(stage5eg.SCHEMA_PATHS[key])
        payload = load_yaml(data_path)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(payload)


def test_stage5eg_summary_schema_rejects_solve_claim_true() -> None:
    ensure_stage5eg_built()

    schema = load_yaml(stage5eg.SCHEMA_PATHS["summary"])
    payload = load_yaml(stage5eg.DATA_PATHS["summary"])
    payload["solve_claim"] = True

    try:
        Draft202012Validator(schema).validate(payload)
    except ValidationError:
        return
    raise AssertionError("Stage 5EG summary schema accepted solve_claim=true")


def test_stage5eg_summary_schema_rejects_execution_true() -> None:
    ensure_stage5eg_built()

    schema = load_yaml(stage5eg.SCHEMA_PATHS["summary"])
    payload = load_yaml(stage5eg.DATA_PATHS["summary"])
    payload["execution_performed"] = True

    try:
        Draft202012Validator(schema).validate(payload)
    except ValidationError:
        return
    raise AssertionError("Stage 5EG summary schema accepted execution_performed=true")
