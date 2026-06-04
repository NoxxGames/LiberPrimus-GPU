from __future__ import annotations

from libreprimus.token_block.stage5dg import validate_stage5dg_governance_scope

from test_stage5dg_common import ensure_stage5dg_built, load_yaml


def test_stage5dg_governance_scope_prevents_overbuild() -> None:
    ensure_stage5dg_built()
    counts, errors = validate_stage5dg_governance_scope()

    assert errors == []
    assert counts["stage5dg_is_narrow_real_operator_approval_record_stage"] is True
    assert counts["stage5dg_creates_generic_preflight_layer"] is False

    payload = load_yaml("data/project-state/stage5dg-governance-scope-control.yaml")
    assert payload["stage5dg_authorizes_deep_research_acceptance"] is False
    assert payload["stage5dg_authorizes_activation"] is False
    assert payload["stage5dg_authorizes_execution"] is False
