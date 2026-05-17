from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

from libreprimus.approval_execution.approval_gate import evaluate_approval_execution_gate
from libreprimus.approval_execution.request_loader import load_approval_execution_request
from libreprimus.experiment_proposals.proposal_loader import load_experiment_proposal

REPO = Path(__file__).resolve().parents[2]
STAGE2H = REPO / "experiments/proposals/stage2h"


def test_stage2h_proposals_validate() -> None:
    proposal_paths = [path for path in STAGE2H.glob("*.yaml") if not path.name.endswith("-request.yaml")]

    assert {path.name for path in proposal_paths} == {
        "stage2h-approved-synthetic-direct-proposal.yaml",
        "stage2h-approved-solved-fixture-replay-proposal.yaml",
        "stage2h-noop-real-proposal.yaml",
    }
    for proposal_path in proposal_paths:
        proposal = load_experiment_proposal(proposal_path)
        assert proposal.payload["approved_for_execution"] is False
        assert proposal.payload["execution_enabled"] is False


def test_stage2h_requests_validate_and_gate_expected_status() -> None:
    statuses = {}
    for request_path in STAGE2H.glob("*-request.yaml"):
        request = load_approval_execution_request(request_path)
        statuses[request.request_id] = evaluate_approval_execution_gate(request).approval_gate_status

    assert statuses["stage2h-approved-synthetic-direct-request"] == "pass"
    assert statuses["stage2h-approved-solved-fixture-replay-request"] == "pass"
    assert statuses["stage2h-noop-real-request"] == "blocked"


def test_stage2h_approved_records_are_safe_scoped() -> None:
    for path in (STAGE2H / "approval-records").glob("*.yaml"):
        if path.name == "README.md":
            continue
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if payload["approval_status"] == "approved":
            assert payload["approval_scope"]["execution_scope"] in {"synthetic_only", "solved_fixture_only"}
            assert payload["approved_for_execution"] is True
        else:
            assert payload["approved_for_execution"] is False


def test_generated_approval_execution_outputs_are_ignored() -> None:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", "experiments/results/approval-gated-execution/stage2h/summary.json"],
        cwd=REPO,
        check=False,
    )

    assert result.returncode == 0

