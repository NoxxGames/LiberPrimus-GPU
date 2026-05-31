from libreprimus.token_block.stage5cg import (
    validate_stage5cg_active_planning_input_decision_scaffold,
)
from test_stage5cg_common import load_yaml, write_yaml


def test_stage5cg_active_planning_input_decision_does_not_authorize(tmp_path) -> None:
    counts, errors = validate_stage5cg_active_planning_input_decision_scaffold()
    assert not errors
    assert counts["active_planning_input_authorized_now"] is False
    assert counts["active_planning_input_selected_now"] is False

    payload = load_yaml(
        "data/token-block/stage5cg-active-planning-input-decision-record-scaffold.yaml"
    )
    payload["active_planning_input_selected_now"] = True
    bad = tmp_path / "active-planning.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5cg_active_planning_input_decision_scaffold(
        active_planning_decision=bad
    )
    assert bad_errors
