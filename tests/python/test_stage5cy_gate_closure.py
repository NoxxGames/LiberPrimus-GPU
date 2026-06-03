from test_stage5cy_common import ensure_stage5cy_built, load_yaml


def test_stage5cy_real_records_combined_gate_and_activation_remain_blocked() -> None:
    ensure_stage5cy_built()
    blocker = load_yaml("data/token-block/stage5cy-real-record-creation-blocker.yaml")
    combined = load_yaml("data/token-block/stage5cy-combined-gate-non-satisfaction-proof.yaml")
    activation = load_yaml("data/token-block/stage5cy-activation-decision-nonauthorization-proof.yaml")

    assert blocker["real_record_class_count"] == 10
    assert all(record["created_now"] is False for record in blocker["blocked_real_record_classes"])
    assert combined["combined_approval_gate_satisfied_now"] is False
    assert combined["real_combined_gate_validation_record_created_now"] is False
    assert activation["activation_decision_valid_now"] is False
    assert activation["activation_authorized_now"] is False
    assert activation["active_planning_input_authorized_now"] is False
    assert activation["active_planning_input_selected_now"] is False


def test_stage5cy_no_active_no_byte_no_execution_gates_closed() -> None:
    ensure_stage5cy_built()
    no_active = load_yaml("data/token-block/stage5cy-no-active-ingestion-proof.yaml")
    no_byte = load_yaml("data/token-block/stage5cy-no-byte-stream-transition-gate.yaml")
    no_execution = load_yaml("data/token-block/stage5cy-no-execution-transition-gate.yaml")

    assert no_active["no_active_ingestion_status"] == "closed"
    assert no_active["string4_sidecar_status"] == "scaffolded_inactive"
    assert no_active["active_planning_input_authorized_now"] is False
    assert no_byte["no_byte_stream_transition_gate_status"] == "closed"
    assert no_byte["byte_stream_generation_authorized_now"] is False
    assert no_byte["operator_facing_option_selection_preflight_authorizes_bytes"] is False
    assert no_execution["no_execution_transition_gate_status"] == "closed"
    assert no_execution["execution_authorized_now"] is False
    assert no_execution["operator_facing_option_selection_preflight_authorizes_execution"] is False
