from __future__ import annotations

from jsonschema import Draft202012Validator, ValidationError

from libreprimus.token_block import stage6
from test_stage6_common import load_yaml, stage6_data


def test_stage6_schemas_validate_all_payloads() -> None:
    for key, data_path in stage6.DATA_PATHS.items():
        schema = load_yaml(stage6.SCHEMA_PATHS[key])
        payload = load_yaml(data_path)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(payload)


def test_stage6_summary_schema_rejects_execution_flags() -> None:
    schema = load_yaml(stage6.SCHEMA_PATHS["summary"])
    payload = stage6_data("summary")
    payload["solve_claim"] = True
    try:
        Draft202012Validator(schema).validate(payload)
    except ValidationError:
        return
    raise AssertionError("Stage 6 summary schema accepted solve_claim=true")


def test_stage6_summary_schema_rejects_cuda_true() -> None:
    schema = load_yaml(stage6.SCHEMA_PATHS["summary"])
    payload = stage6_data("summary")
    payload["cuda_execution_performed"] = True
    try:
        Draft202012Validator(schema).validate(payload)
    except ValidationError:
        return
    raise AssertionError("Stage 6 summary schema accepted cuda_execution_performed=true")
