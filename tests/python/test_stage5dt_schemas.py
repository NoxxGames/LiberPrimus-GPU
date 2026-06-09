from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from libreprimus.token_block.stage5dt import DATA_PATHS, SCHEMA_PATHS
from test_stage5dt_common import ensure_stage5dt_built, load_yaml


def test_stage5dt_schema_files_exist_and_validate_core_records() -> None:
    ensure_stage5dt_built()
    pairs = [
        ("summary", "summary"),
        ("next_stage_decision", "next_stage_decision"),
        ("fact_card_gui_summary", "fact_card_gui_summary"),
        ("number_fact_reviewability_audit", "number_fact_reviewability_audit"),
        ("review_batch_plan_summary", "review_batch_plan_summary"),
        ("scope_control", "scope_control"),
        ("example_overlay", "number_fact_overlay"),
        ("batch_plan", "number_fact_review_batch"),
        ("number_fact_review_states", "number_fact_review_state"),
    ]
    for record_key, schema_key in pairs:
        record_path = DATA_PATHS[record_key]
        schema_path = SCHEMA_PATHS[schema_key]
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(load_yaml(record_path))
