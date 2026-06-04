from __future__ import annotations

from test_stage5de_common import ensure_stage5de_built, load_yaml


def test_stage5de_respects_governance_scope_control() -> None:
    ensure_stage5de_built()
    governance = load_yaml("data/project-state/stage5de-governance-scope-control.yaml")

    assert governance["governance_overbuild_risk_acknowledged"] is True
    assert governance["stage5dc_is_narrow_operator_choice_stage"] is True
    assert governance["stage5de_is_narrow_operator_approval_preparation_stage"] is True
    assert governance["additional_generic_preflight_layers_allowed_without_concrete_defect"] is False
    assert governance["stage5de_creates_generic_preflight_layer"] is False
    assert governance["stage5de_creates_broad_new_negative_fixture_layer"] is False
    assert governance["stage5de_creates_real_operator_approval_record"] is False
    assert governance["stage5de_authorizes_activation"] is False
