from __future__ import annotations

from libreprimus.token_block.stage5dg import (
    APPROVAL_RECORD_ID,
    validate_stage5dg_real_operator_approval_record,
)

from test_stage5dg_common import ensure_stage5dg_built, load_yaml


def test_stage5dg_creates_real_operator_approval_record_only() -> None:
    ensure_stage5dg_built()
    counts, errors = validate_stage5dg_real_operator_approval_record()

    assert errors == []
    assert counts["real_operator_approval_record_created_now"] is True
    assert counts["operator_approval_component_satisfied_now"] is True

    payload = load_yaml("data/token-block/stage5dg-real-operator-approval-record.yaml")
    assert payload["approval_record_id"] == APPROVAL_RECORD_ID
    assert payload["approval_record_status"] == "valid_real_operator_approval_record"
    assert payload["operator_identity_or_role"] == "project_operator_explicit_chat_operator"
    assert payload["operator_approval_alone_satisfies_combined_gate"] is False
