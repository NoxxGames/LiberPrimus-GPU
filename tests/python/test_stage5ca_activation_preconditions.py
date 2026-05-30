from pathlib import Path

import yaml

from libreprimus.token_block.stage5ca import (
    REQUIRED_ACTIVATION_PRECONDITIONS,
    validate_stage5ca_activation_preconditions,
)
from test_stage5ca_common import load_yaml


def test_stage5ca_activation_preconditions_require_future_stage_and_review() -> None:
    payload = load_yaml("data/token-block/stage5ca-activation-precondition-contract.yaml")
    preconditions = payload["required_activation_preconditions"]
    assert preconditions == REQUIRED_ACTIVATION_PRECONDITIONS
    assert "explicit_future_stage_authorization" in preconditions
    assert "deep_research_or_operator_review_if_selected" in preconditions
    assert payload["activation_preconditions_satisfied_now"] is False
    assert payload["current_stage_authorizes_activation"] is False


def test_stage5ca_activation_validator_rejects_current_authorization(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ca-activation-precondition-contract.yaml")
    payload["current_stage_authorizes_activation"] = True
    candidate = tmp_path / "activation.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ca_activation_preconditions(activation_contract=candidate)
    assert counts["stage5ca_activation_preconditions_valid"] is False
    assert "current_stage_authorizes_activation must be false" in errors
