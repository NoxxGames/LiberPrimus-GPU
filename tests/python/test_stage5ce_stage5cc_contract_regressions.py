from pathlib import Path

import yaml

from libreprimus.token_block.stage5cc import (
    validate_stage5cc_activation_preconditions,
    validate_stage5cc_fail_closed_triggers,
)
from test_stage5ce_common import load_yaml


def test_stage5ce_regresses_missing_fail_closed_trigger() -> None:
    payload = load_yaml("data/token-block/stage5cc-fail-closed-trigger-exact-set-contract.yaml")
    assert payload["required_fail_closed_triggers"]


def test_stage5ce_missing_fail_closed_trigger_still_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-fail-closed-trigger-exact-set-contract.yaml")
    payload["required_fail_closed_triggers"] = payload["required_fail_closed_triggers"][:-1]
    candidate = tmp_path / "triggers.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_fail_closed_triggers(trigger_contract=candidate)
    assert counts["stage5cc_fail_closed_triggers_valid"] is False
    assert any(error.startswith("missing_required_fail_closed_trigger=") for error in errors)


def test_stage5ce_extra_fail_closed_trigger_still_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-fail-closed-trigger-exact-set-contract.yaml")
    payload["required_fail_closed_triggers"] = [
        *payload["required_fail_closed_triggers"],
        "stage5ce_unclassified_trigger",
    ]
    candidate = tmp_path / "triggers.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_fail_closed_triggers(trigger_contract=candidate)
    assert counts["stage5cc_fail_closed_triggers_valid"] is False
    assert "extra_fail_closed_trigger=stage5ce_unclassified_trigger" in errors


def test_stage5ce_missing_activation_precondition_still_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-activation-precondition-exact-set-contract.yaml")
    payload["required_activation_preconditions"] = payload["required_activation_preconditions"][:-1]
    candidate = tmp_path / "activation.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_activation_preconditions(activation_contract=candidate)
    assert counts["stage5cc_activation_preconditions_valid"] is False
    assert any(error.startswith("missing_required_activation_precondition=") for error in errors)


def test_stage5ce_extra_activation_precondition_still_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5cc-activation-precondition-exact-set-contract.yaml")
    payload["required_activation_preconditions"] = [
        *payload["required_activation_preconditions"],
        "stage5ce_unclassified_precondition",
    ]
    candidate = tmp_path / "activation.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5cc_activation_preconditions(activation_contract=candidate)
    assert counts["stage5cc_activation_preconditions_valid"] is False
    assert "extra_activation_precondition=stage5ce_unclassified_precondition" in errors
