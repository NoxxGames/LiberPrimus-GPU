from pathlib import Path

import yaml


def test_stage5az_execution_gates_add_integrity_gate_without_execution() -> None:
    payload = yaml.safe_load(
        Path("data/token-block/stage5az-repaired-execution-gates.yaml").read_text(encoding="utf-8")
    )
    gate_ids = [gate["gate_id"] for gate in payload["gates"]]

    assert "manifest_integrity_gate" in gate_ids
    assert payload["manifest_integrity_gate_status"] == "design_satisfied_execution_still_blocked"
    assert payload["execution_authorised_now"] is False
    assert payload["token_experiments_executed"] is False
