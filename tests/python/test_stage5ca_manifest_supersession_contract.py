from pathlib import Path

import yaml

from libreprimus.token_block.stage5ca import (
    REQUIRED_SUPERSESSION_REQUIREMENTS,
    validate_stage5ca_manifest_supersession_contract,
)
from test_stage5ca_common import load_yaml


def test_stage5ca_manifest_supersession_contract_is_preflight_only() -> None:
    payload = load_yaml("data/token-block/stage5ca-manifest-supersession-preflight-contract.yaml")
    assert payload["future_supersession_would_require"] == REQUIRED_SUPERSESSION_REQUIREMENTS
    assert payload["manifest_supersession_performed"] is False
    assert payload["explicit_target_manifest_list_required"] is True
    assert payload["before_after_digest_comparison_required"] is True


def test_stage5ca_supersession_validator_rejects_performed_supersession(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ca-manifest-supersession-preflight-contract.yaml")
    payload["manifest_supersession_performed"] = True
    candidate = tmp_path / "supersession.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ca_manifest_supersession_contract(
        supersession_contract=candidate
    )
    assert counts["stage5ca_manifest_supersession_contract_valid"] is False
    assert "manifest supersession must not be performed" in errors
