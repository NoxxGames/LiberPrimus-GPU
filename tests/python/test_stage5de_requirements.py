from __future__ import annotations

from test_stage5de_common import ensure_stage5de_built, load_yaml


def test_stage5de_future_operator_approval_requirements_are_complete() -> None:
    ensure_stage5de_built()
    requirements = load_yaml(
        "data/token-block/stage5de-future-operator-approval-record-requirements.yaml"
    )

    assert requirements["future_operator_approval_required_input_count"] == 34
    assert requirements["future_operator_approval_record_created_now"] is False
    assert requirements["future_operator_approval_record_valid_now"] is False
    ids = [item["requirement_id"] for item in requirements["future_operator_approval_requirements"]]
    assert "future_operator_identity_or_operator_role" in ids
    assert "explicit_operator_approval_alone_does_not_authorize_activation_statement" in ids
    assert "explicit_no_generic_preflight_layer_statement" in ids
