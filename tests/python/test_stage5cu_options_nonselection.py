from libreprimus.token_block.stage5cu import (
    validate_stage5cu_actual_record_rejection,
    validate_stage5cu_options_nonselection,
)

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_options_nonselection_proof_keeps_all_options_unselected() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/token-block/stage5cu-operator-options-nonselection-proof.yaml")
    assert payload["all_options_unselected"] is True
    assert payload["selected_option_id"] is None
    assert all(option["selected_now"] is False for option in payload["options"])
    counts, errors = validate_stage5cu_options_nonselection()
    assert not errors
    assert counts["stage5cu_options_nonselection_valid"] is True


def test_stage5cu_rejects_selected_option_id() -> None:
    assert validate_stage5cu_actual_record_rejection({"selected_option_id": "keep_blocked_no_action"})
