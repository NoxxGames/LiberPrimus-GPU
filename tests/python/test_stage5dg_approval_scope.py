from __future__ import annotations

from libreprimus.token_block.stage5dg import validate_stage5dg_operator_approval_scope

from test_stage5dg_common import ensure_stage5dg_built, load_yaml


def test_stage5dg_approval_scope_is_narrow() -> None:
    ensure_stage5dg_built()
    counts, errors = validate_stage5dg_operator_approval_scope()

    assert errors == []
    assert counts["allowed_action_count"] == 3

    payload = load_yaml("data/token-block/stage5dg-operator-approval-scope.yaml")
    assert "create_stage5dg_real_operator_approval_record" in payload["approval_scope_allowed_actions"]
    assert "authorize_execution" in payload["approval_scope_disallowed_actions"]
    assert "perform_tor_or_network_access" in payload["approval_scope_disallowed_actions"]
