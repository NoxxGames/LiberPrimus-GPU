from __future__ import annotations

from jsonschema import Draft202012Validator, ValidationError

from libreprimus.token_block import stage5ei
from test_stage5ei_common import load_yaml, stage5ei_data


def test_stage5ei_schemas_validate_all_payloads() -> None:
    for key, data_path in stage5ei.DATA_PATHS.items():
        schema = load_yaml(stage5ei.SCHEMA_PATHS[key])
        payload = load_yaml(data_path)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(payload)


def test_stage5ei_summary_schema_rejects_solve_claim_true() -> None:
    schema = load_yaml(stage5ei.SCHEMA_PATHS["summary"])
    payload = stage5ei_data("summary")
    payload["solve_claim"] = True

    try:
        Draft202012Validator(schema).validate(payload)
    except ValidationError:
        return
    raise AssertionError("Stage 5EI summary schema accepted solve_claim=true")


def test_stage5ei_summary_schema_rejects_cuda_execution_true() -> None:
    schema = load_yaml(stage5ei.SCHEMA_PATHS["summary"])
    payload = stage5ei_data("summary")
    payload["cuda_execution_performed"] = True

    try:
        Draft202012Validator(schema).validate(payload)
    except ValidationError:
        return
    raise AssertionError("Stage 5EI summary schema accepted cuda_execution_performed=true")


def test_stage5ei_summary_schema_rejects_route_stream_true() -> None:
    schema = load_yaml(stage5ei.SCHEMA_PATHS["summary"])
    payload = stage5ei_data("summary")
    payload["route_stream_generated_now"] = True

    try:
        Draft202012Validator(schema).validate(payload)
    except ValidationError:
        return
    raise AssertionError("Stage 5EI summary schema accepted route_stream_generated_now=true")

