from __future__ import annotations

from jsonschema import Draft202012Validator, ValidationError

from libreprimus.token_block import stage5eh
from test_stage5eh_common import load_yaml, stage5eh_data


def test_stage5eh_schemas_validate_all_payloads() -> None:
    for key, data_path in stage5eh.DATA_PATHS.items():
        schema = load_yaml(stage5eh.SCHEMA_PATHS[key])
        payload = load_yaml(data_path)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(payload)


def test_stage5eh_summary_schema_rejects_solve_claim_true() -> None:
    schema = load_yaml(stage5eh.SCHEMA_PATHS["summary"])
    payload = stage5eh_data("summary")
    payload["solve_claim"] = True

    try:
        Draft202012Validator(schema).validate(payload)
    except ValidationError:
        return
    raise AssertionError("Stage 5EH summary schema accepted solve_claim=true")


def test_stage5eh_summary_schema_rejects_execution_true() -> None:
    schema = load_yaml(stage5eh.SCHEMA_PATHS["summary"])
    payload = stage5eh_data("summary")
    payload["execution_performed"] = True

    try:
        Draft202012Validator(schema).validate(payload)
    except ValidationError:
        return
    raise AssertionError("Stage 5EH summary schema accepted execution_performed=true")


def test_stage5eh_summary_schema_rejects_stegdetect_execution_true() -> None:
    schema = load_yaml(stage5eh.SCHEMA_PATHS["summary"])
    payload = stage5eh_data("summary")
    payload["stegdetect_execution_performed_now"] = True

    try:
        Draft202012Validator(schema).validate(payload)
    except ValidationError:
        return
    raise AssertionError("Stage 5EH summary schema accepted stegdetect_execution_performed_now=true")
