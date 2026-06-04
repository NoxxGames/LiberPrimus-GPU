from __future__ import annotations

from test_stage5dc_common import ensure_stage5dc_built, load_yaml


def test_stage5dc_preserves_governance_scope_control() -> None:
    ensure_stage5dc_built()
    governance = load_yaml("data/project-state/stage5dc-governance-scope-control.yaml")

    assert governance["stage5db_review_integrated"] is True
    assert governance["stage5dc_is_narrow_operator_choice_stage"] is True
    assert governance["additional_generic_preflight_layers_allowed_without_concrete_defect"] is False
    assert governance["stage5dc_creates_generic_preflight_layer"] is False
    assert governance["stage5dc_creates_broad_new_negative_fixture_layer"] is False
    assert governance["old_16_worker_default_reintroduced"] is False
