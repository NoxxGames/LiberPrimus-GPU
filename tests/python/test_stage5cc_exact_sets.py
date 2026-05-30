from pathlib import Path

import yaml

from libreprimus.token_block.stage5cc import (
    REQUIRED_ACTIVATION_PRECONDITIONS,
    REQUIRED_FAIL_CLOSED_TRIGGERS,
    validate_stage5cc_activation_preconditions,
    validate_stage5cc_fail_closed_triggers,
)
from test_stage5cc_common import load_yaml


def test_stage5cc_fail_closed_trigger_exact_set_passes() -> None:
    payload = load_yaml("data/token-block/stage5cc-fail-closed-trigger-exact-set-contract.yaml")
    assert payload["required_fail_closed_triggers"] == REQUIRED_FAIL_CLOSED_TRIGGERS
    assert payload["fail_closed_trigger_validation_mode"] == "exact_set"
    assert payload["missing_trigger_fails_closed"] is True
    assert payload["extra_trigger_fails_closed"] is True


def test_stage5cc_fail_closed_trigger_missing_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-fail-closed-trigger-exact-set-contract.yaml")
    payload["required_fail_closed_triggers"] = payload["required_fail_closed_triggers"][:-1]
    candidate = tmp_path / "triggers.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_fail_closed_triggers(trigger_contract=candidate)
    assert counts["stage5cc_fail_closed_triggers_valid"] is False
    assert any(error.startswith("missing_required_fail_closed_trigger=") for error in errors)


def test_stage5cc_fail_closed_trigger_extra_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-fail-closed-trigger-exact-set-contract.yaml")
    payload["required_fail_closed_triggers"] = [
        *payload["required_fail_closed_triggers"],
        "unclassified_future_trigger",
    ]
    candidate = tmp_path / "triggers.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_fail_closed_triggers(trigger_contract=candidate)
    assert counts["stage5cc_fail_closed_triggers_valid"] is False
    assert "extra_fail_closed_trigger=unclassified_future_trigger" in errors


def test_stage5cc_activation_precondition_exact_set_passes() -> None:
    payload = load_yaml("data/token-block/stage5cc-activation-precondition-exact-set-contract.yaml")
    assert payload["required_activation_preconditions"] == REQUIRED_ACTIVATION_PRECONDITIONS
    assert payload["activation_precondition_validation_mode"] == "exact_set"
    assert payload["activation_preconditions_satisfied_now"] is False


def test_stage5cc_activation_precondition_missing_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-activation-precondition-exact-set-contract.yaml")
    payload["required_activation_preconditions"] = payload["required_activation_preconditions"][:-1]
    candidate = tmp_path / "activation.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_activation_preconditions(activation_contract=candidate)
    assert counts["stage5cc_activation_preconditions_valid"] is False
    assert any(error.startswith("missing_required_activation_precondition=") for error in errors)


def test_stage5cc_activation_precondition_extra_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-activation-precondition-exact-set-contract.yaml")
    payload["required_activation_preconditions"] = [
        *payload["required_activation_preconditions"],
        "unclassified_future_precondition",
    ]
    candidate = tmp_path / "activation.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_activation_preconditions(activation_contract=candidate)
    assert counts["stage5cc_activation_preconditions_valid"] is False
    assert "extra_activation_precondition=unclassified_future_precondition" in errors
