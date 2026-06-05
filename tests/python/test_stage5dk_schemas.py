from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5dk_common import (
    ROOT,
    STAGE5DK_RECORDS,
    STAGE5DK_SCHEMAS,
    ensure_stage5dk_built,
    load_yaml,
)


def test_stage5dk_schemas_validate_records() -> None:
    ensure_stage5dk_built()

    for schema_path in STAGE5DK_SCHEMAS:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record_path = schema_path.replace("schemas/", "data/").replace(
            "-v0.schema.json",
            ".yaml",
        )
        record = load_yaml(record_path)
        assert list(Draft202012Validator(schema).iter_errors(record)) == []


def test_stage5dk_summary_schema_rejects_activation_execution_and_raw_bodies() -> None:
    ensure_stage5dk_built()
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5dk-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )

    for field in [
        "activation_authorized",
        "execution_authorized",
        "combined_gate_satisfied",
        "generated_outputs_committed",
        "raw_webpage_bodies_committed",
        "stage5dk_selects_target_priority_now",
        "worker_cap_16_allowed",
    ]:
        record = load_yaml("data/project-state/stage5dk-summary.yaml")
        record[field] = True
        assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage5dk_page56_schema_rejects_hash_algorithm_and_preimage_claims() -> None:
    ensure_stage5dk_built()
    schema = json.loads(
        (
            ROOT
            / "schemas/project-state/stage5dk-page56-hash-contract-refinement-v0.schema.json"
        ).read_text(encoding="utf-8")
    )

    for field in [
        "page56_hash_algorithm_known",
        "page56_hash_algorithm_selected_now",
        "page56_hash_preimage_known",
        "page56_hash_preimage_candidate_tested_now",
        "hash_preimage_search_performed",
        "target_class_validation_implemented",
    ]:
        record = load_yaml("data/project-state/stage5dk-page56-hash-contract-refinement.yaml")
        record[field] = True
        assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage5dk_record_and_schema_lists_are_populated() -> None:
    ensure_stage5dk_built()

    assert len(STAGE5DK_RECORDS) == 27
    assert len(STAGE5DK_SCHEMAS) == len(STAGE5DK_RECORDS)
