from test_stage5bk_common import load_yaml


def test_stage5bk_token_block_constraint_update_keeps_execution_blocked() -> None:
    payload = load_yaml("data/token-block/stage5bk-token-block-historical-constraint-update.yaml")
    assert payload["historical_constraints_integrated"] is True
    assert payload["future_token_block_execution_remains_blocked"] is True
    assert payload["active_token_block_manifest_changed"] is False
    assert payload["token_experiment_executed"] is False
