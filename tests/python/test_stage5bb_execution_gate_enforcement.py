from pathlib import Path

import yaml


def test_stage5bb_execution_gate_enforcement_fails_closed() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-execution-gate-enforcement-policy.yaml").read_text())

    assert payload["execution_authorised_now"] is False
    assert payload["all_gates_required_before_execution"] is True
    assert payload["gate_enforcer_fails_closed"] is True
    assert payload["real_execution_blocked"] is True
    assert payload["token_experiments_executed"] is False
