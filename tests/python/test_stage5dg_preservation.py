from __future__ import annotations

from libreprimus.token_block.stage5dg import (
    SELECTED_OPTION_ID,
    validate_stage5dg_active_lineage_preservation,
    validate_stage5dg_selected_option_preservation,
    validate_stage5dg_stage5bd_preservation,
    validate_stage5dg_stage5dc_preservation,
    validate_stage5dg_stage5de_preservation,
    validate_stage5dg_unselected_options_preservation,
)

from test_stage5dg_common import ensure_stage5dg_built, load_yaml


def test_stage5dg_preserves_stage5de_and_stage5dc_choice_layers() -> None:
    ensure_stage5dg_built()
    for validator in [
        validate_stage5dg_stage5de_preservation,
        validate_stage5dg_stage5dc_preservation,
        validate_stage5dg_selected_option_preservation,
        validate_stage5dg_unselected_options_preservation,
    ]:
        _, errors = validator()
        assert errors == []

    payload = load_yaml("data/token-block/stage5dg-selected-option-preservation.yaml")
    assert payload["stage5dc_selected_option_record_option_id"] == SELECTED_OPTION_ID
    assert payload["stage5de_review_makes_stage5dg_record_creation_in_scope"] is True


def test_stage5dg_preserves_stage5bd_and_active_lineage() -> None:
    ensure_stage5dg_built()
    stage5bd_counts, stage5bd_errors = validate_stage5dg_stage5bd_preservation()
    lineage_counts, lineage_errors = validate_stage5dg_active_lineage_preservation()

    assert stage5bd_errors == []
    assert lineage_errors == []
    assert stage5bd_counts["stage5bd_run_plan_id_count"] == 10
    assert lineage_counts["active_lineage_record_count"] == 8
