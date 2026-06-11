from __future__ import annotations

from copy import deepcopy

from jsonschema import Draft202012Validator

from libreprimus.token_block.stage5eb import DATA_PATHS, SCHEMA_BY_DATA_KEY, SCHEMA_PATHS
from test_stage5eb_common import ensure_stage5eb_built, load_yaml


def test_stage5eb_schemas_validate_records() -> None:
    ensure_stage5eb_built()

    for key, path in DATA_PATHS.items():
        payload = load_yaml(path)
        schema_key = SCHEMA_BY_DATA_KEY.get(key, "generic_preservation")
        schema = load_yaml(SCHEMA_PATHS[schema_key])
        errors = list(Draft202012Validator(schema).iter_errors(payload))
        assert errors == []


def test_stage5eb_summary_schema_rejects_execution_flags() -> None:
    ensure_stage5eb_built()

    schema = load_yaml(SCHEMA_PATHS["summary"])
    payload = load_yaml(DATA_PATHS["summary"])
    for key in (
        "solve_claim",
        "source_lock_entry_batch_review_performed_now",
        "number_fact_review_batch_3_performed_now",
        "new_number_fact_overlays_added_now",
        "byte_stream_generation_authorized_now",
        "execution_performed",
        "cuda_execution_performed",
    ):
        mutated = deepcopy(payload)
        mutated[key] = True
        assert list(Draft202012Validator(schema).iter_errors(mutated))
