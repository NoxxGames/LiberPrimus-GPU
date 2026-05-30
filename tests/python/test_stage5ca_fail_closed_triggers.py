from pathlib import Path

import yaml

from libreprimus.token_block.stage5ca import (
    REQUIRED_FAIL_CLOSED_TRIGGERS,
    validate_stage5ca_fail_closed_triggers,
)
from test_stage5ca_common import load_yaml


def test_stage5ca_fail_closed_trigger_contract_includes_required_triggers() -> None:
    payload = load_yaml("data/token-block/stage5ca-fail-closed-trigger-contract.yaml")
    assert payload["required_fail_closed_triggers"] == REQUIRED_FAIL_CLOSED_TRIGGERS
    assert "codex_output_used" in payload["required_fail_closed_triggers"]
    assert payload["future_runner_must_fail_closed"] is True


def test_stage5ca_fail_closed_trigger_validator_rejects_missing_trigger(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ca-fail-closed-trigger-contract.yaml")
    payload["required_fail_closed_triggers"] = payload["required_fail_closed_triggers"][:-1]
    candidate = tmp_path / "triggers.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ca_fail_closed_triggers(trigger_contract=candidate)
    assert counts["stage5ca_fail_closed_triggers_valid"] is False
    assert any(error.startswith("missing_required_fail_closed_trigger=") for error in errors)
