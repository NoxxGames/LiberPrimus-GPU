from libreprimus.token_block.stage5cs import (
    validate_stage5cs_actual_record_rejection,
    validate_stage5cs_options_nonselection,
)

from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_options_nonselection_proof_is_closed() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-operator-options-nonselection-proof.yaml")
    assert payload["operator_options_nonselection_proof_created"] is True
    assert payload["operator_decision_option_selected_now"] is False
    assert payload["selected_option_id"] is None
    counts, errors = validate_stage5cs_options_nonselection()
    assert not errors
    assert counts["stage5cs_options_nonselection_valid"] is True


def test_stage5cs_rejects_selected_option_id() -> None:
    assert validate_stage5cs_actual_record_rejection({"selected_option_id": "keep_blocked_no_action"})
