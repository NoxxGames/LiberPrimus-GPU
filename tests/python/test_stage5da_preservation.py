from __future__ import annotations

from test_stage5da_common import ensure_stage5da_built, load_yaml


def test_stage5da_real_record_blocker_blocks_all_relevant_classes() -> None:
    ensure_stage5da_built()
    blocker = load_yaml("data/token-block/stage5da-real-record-creation-blocker.yaml")

    assert blocker["real_record_class_count"] == 11
    assert all(record["created_now"] is False for record in blocker["blocked_real_record_classes"])
    assert all(record["present_now"] is False for record in blocker["blocked_real_record_classes"])
    assert all(record["valid_now"] is False for record in blocker["blocked_real_record_classes"])
    assert blocker["blocked_real_record_classes"][0]["record_class"] == (
        "real_operator_choice_pause_record"
    )


def test_stage5da_preserves_stage5cy_stage5bd_and_active_lineage() -> None:
    ensure_stage5da_built()
    stage5cy = load_yaml("data/token-block/stage5da-stage5cy-preservation.yaml")
    stage5bd = load_yaml("data/token-block/stage5da-stage5bd-plan-preservation.yaml")
    lineage = load_yaml("data/token-block/stage5da-active-lineage-preservation.yaml")

    assert stage5cy["stage5cy_option_selection_preflight_preserved"] is True
    assert stage5cy["stage5cy_validation_count_reconciliation_preserved"] is True
    assert stage5bd["stage5bd_run_plan_id_count"] == 10
    assert stage5bd["stage5bd_run_plan_ids_changed"] is False
    assert stage5bd["string4_added_to_stage5bd_run_plan_ids"] is False
    assert lineage["active_lineage_record_count"] == 8
    assert lineage["correct_stage5aw_path_included"] is True
    assert lineage["deprecated_stage5aw_path_absent"] is True
    assert lineage["all_lineage_paths_resolve"] is True


def test_stage5da_no_active_no_byte_no_execution_gates_closed() -> None:
    ensure_stage5da_built()
    no_active = load_yaml("data/token-block/stage5da-no-active-ingestion-proof.yaml")
    no_byte = load_yaml("data/token-block/stage5da-no-byte-stream-transition-gate.yaml")
    no_execution = load_yaml("data/token-block/stage5da-no-execution-transition-gate.yaml")

    assert no_active["no_active_ingestion_status"] == "closed"
    assert no_active["string4_sidecar_status"] == "scaffolded_inactive"
    assert no_active["string4_active_input_allowed"] is False
    assert no_byte["no_byte_stream_transition_gate_status"] == "closed"
    assert no_byte["real_byte_stream_generated"] is False
    assert no_execution["no_execution_transition_gate_status"] == "closed"
    assert no_execution["dwh_hash_search_performed"] is False
    assert no_execution["scoring_performed"] is False
    assert no_execution["cuda_execution_performed"] is False


def test_stage5da_governance_scope_blocks_generic_layer_expansion() -> None:
    ensure_stage5da_built()
    governance = load_yaml("data/project-state/stage5da-governance-scope-control.yaml")
    next_stage = load_yaml("data/project-state/stage5da-next-stage-decision.yaml")

    assert governance["governance_overbuild_risk_acknowledged"] is True
    assert governance["stage5cz_review_integrated"] is True
    assert governance["stage5da_selects_operator_choice"] is False
    assert governance["stage5da_selects_explicit_pause"] is False
    assert governance["stage5da_creates_generic_preflight_layer"] is False
    assert governance["stage5da_creates_broad_new_negative_fixture_layer"] is False
    assert governance["additional_generic_preflight_layers_allowed_without_concrete_defect"] is False
    assert next_stage["selected_next_stage_id"] == "stage-5db"
    assert next_stage["selected_next_prompt_type"] == "deep_research_review"
    assert next_stage["selected_next_stage_authorizes_execution"] is False
