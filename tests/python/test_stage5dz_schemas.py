from __future__ import annotations

from copy import deepcopy

from jsonschema import Draft202012Validator

from libreprimus.token_block.stage5dz import DATA_PATHS, SCHEMA_BY_DATA_KEY, SCHEMA_PATHS
from test_stage5dz_common import ensure_stage5dz_built, load_yaml


def test_stage5dz_schemas_validate_records() -> None:
    ensure_stage5dz_built()

    for key, path in DATA_PATHS.items():
        payload = load_yaml(path)
        schema = load_yaml(SCHEMA_PATHS[SCHEMA_BY_DATA_KEY[key]])
        errors = list(Draft202012Validator(schema).iter_errors(payload))
        assert errors == []


def test_stage5dz_summary_schema_fails_closed_on_guardrails() -> None:
    ensure_stage5dz_built()

    schema = load_yaml(SCHEMA_PATHS["summary"])
    payload = load_yaml(DATA_PATHS["summary"])
    for key in (
        "solve_claim",
        "route_extraction_performed_now",
        "triangle_route_extraction_performed_now",
        "page32_route_extraction_performed_now",
        "target_priority_decision_created_now",
        "pivot_target_selected_now",
        "byte_stream_generation_authorized_now",
        "execution_performed",
        "raw_source_files_committed",
    ):
        mutated = deepcopy(payload)
        mutated[key] = True
        assert list(Draft202012Validator(schema).iter_errors(mutated))
