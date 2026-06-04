from __future__ import annotations

from libreprimus.token_block.stage5dg import (
    validate_stage5dg_activation_nonauthorization,
    validate_stage5dg_operator_approval_nonactivation,
)

from test_stage5dg_common import ensure_stage5dg_built, load_yaml


def test_stage5dg_operator_approval_does_not_activate_anything() -> None:
    ensure_stage5dg_built()
    nonactivation_counts, nonactivation_errors = validate_stage5dg_operator_approval_nonactivation()
    activation_counts, activation_errors = validate_stage5dg_activation_nonauthorization()

    assert nonactivation_errors == []
    assert activation_errors == []
    assert nonactivation_counts["operator_approval_component_satisfied_now"] is True
    assert nonactivation_counts["combined_approval_gate_satisfied_now"] is False
    assert activation_counts["activation_authorized_now"] is False

    payload = load_yaml("data/token-block/stage5dg-operator-approval-nonactivation-proof.yaml")
    assert payload["active_planning_input_selected_now"] is False
    assert payload["byte_stream_generation_authorized_now"] is False
    assert payload["execution_authorized_now"] is False
