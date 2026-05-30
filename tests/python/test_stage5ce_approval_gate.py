from pathlib import Path

import yaml

from libreprimus.token_block.stage5ce import validate_stage5ce_approval_gate
from test_stage5ce_common import load_yaml


def test_stage5ce_approval_gate_requires_operator_and_deep_research() -> None:
    payload = load_yaml("data/token-block/stage5ce-operator-deep-research-combined-gate-contract.yaml")
    assert payload["operator_approval_required_before_activation"] is True
    assert payload["deep_research_review_required_before_activation"] is True
    assert payload["approval_gate_satisfied_now"] is False
    assert payload["approval_gate_authorizes_activation_now"] is False


def test_stage5ce_approval_gate_satisfied_true_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-operator-deep-research-combined-gate-contract.yaml")
    payload["approval_gate_satisfied_now"] = True
    candidate = tmp_path / "gate.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_approval_gate(combined_gate=candidate)
    assert counts["stage5ce_approval_gate_valid"] is False
    assert "approval_gate_satisfied_now must be false" in errors


def test_stage5ce_approval_gate_activation_true_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-operator-deep-research-combined-gate-contract.yaml")
    payload["approval_gate_authorizes_activation_now"] = True
    candidate = tmp_path / "gate.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_approval_gate(combined_gate=candidate)
    assert counts["stage5ce_approval_gate_valid"] is False
    assert "approval_gate_authorizes_activation_now must be false" in errors
