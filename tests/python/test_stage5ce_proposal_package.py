from pathlib import Path

import yaml

from libreprimus.token_block.stage5ce import validate_stage5ce_proposal_package
from test_stage5ce_common import load_yaml


def test_stage5ce_proposal_package_is_review_only() -> None:
    payload = load_yaml("data/token-block/stage5ce-active-planning-input-proposal-package.yaml")
    assert payload["active_planning_input_proposal_package_status"] == "review_package_only"
    assert payload["active_planning_input_proposal_performed"] is False
    assert payload["active_planning_input_authorized_now"] is False
    assert payload["active_planning_input_selected_now"] is False
    assert payload["new_active_planning_input_created"] is False


def test_stage5ce_active_planning_authorization_true_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-active-planning-input-proposal-package.yaml")
    payload["active_planning_input_authorized_now"] = True
    candidate = tmp_path / "proposal.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_proposal_package(proposal_package=candidate)
    assert counts["stage5ce_proposal_package_valid"] is False
    assert "active_planning_input_authorized_now must be false" in errors


def test_stage5ce_new_active_input_true_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-active-planning-input-proposal-package.yaml")
    payload["new_active_planning_input_created"] = True
    candidate = tmp_path / "proposal.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_proposal_package(proposal_package=candidate)
    assert counts["stage5ce_proposal_package_valid"] is False
    assert "new_active_planning_input_created must be false" in errors
