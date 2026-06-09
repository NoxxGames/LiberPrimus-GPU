from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from libreprimus.token_block.stage5du import DATA_PATHS, SCHEMA_PATHS
from test_stage5du_common import ensure_stage5du_built, load_yaml


def test_stage5du_schema_files_exist_and_validate_core_records() -> None:
    ensure_stage5du_built()
    pairs = [
        ("summary", "summary"),
        ("next_stage_decision", "next_stage_decision"),
        ("scope_control", "scope_control"),
        ("community_thread_source_lock_register", "community_thread_source_lock_register"),
        ("community_thread_file_inventory", "community_thread_file_inventory"),
        ("thread_messages_source_locks", "thread_messages_source_locks"),
        ("thread_attachment_order_index", "thread_attachment_order_index"),
        ("canonical_lp_page_image_root_crosslink", "canonical_lp_page_image_root_crosslink"),
        ("red_runes_gateless_gate_koan20_title_candidate", "red_heading_candidate"),
        ("lp_negative_space_visual_layer_candidate_family", "negative_space_candidate"),
        ("star_artifacts_exact254_mask_method", "star_artifact_candidate"),
        ("mobius_totient_zero_class_gp_alphabet_candidate", "mobius_totient_candidate"),
        ("no_token_block_execution_proof", "no_token_block_execution_proof"),
    ]
    for record_key, schema_key in pairs:
        schema = json.loads(SCHEMA_PATHS[schema_key].read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(load_yaml(DATA_PATHS[record_key]))


def test_stage5du_summary_rejects_execution_flags() -> None:
    ensure_stage5du_built()
    schema = json.loads(SCHEMA_PATHS["summary"].read_text(encoding="utf-8"))
    record = load_yaml(DATA_PATHS["summary"])
    record["solve_claim"] = True
    errors = list(Draft202012Validator(schema).iter_errors(record))
    assert errors
