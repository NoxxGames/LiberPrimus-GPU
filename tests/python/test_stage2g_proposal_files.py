from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

from libreprimus.experiment_proposals.proposal_loader import load_experiment_proposal

REPO = Path(__file__).resolve().parents[2]
PROPOSAL_DIR = REPO / "experiments/proposals/stage2g"
APPROVAL_DIR = PROPOSAL_DIR / "approval-records"


def test_all_stage2g_proposals_validate() -> None:
    for path in PROPOSAL_DIR.glob("*.yaml"):
        proposal = load_experiment_proposal(path)
        assert proposal.payload["approved_for_execution"] is False
        assert proposal.payload["execution_enabled"] is False


def test_future_unsolved_proposals_require_human_approval() -> None:
    for path in PROPOSAL_DIR.glob("*.yaml"):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if payload["corpus_slice"]["slice_kind"] == "future_unsolved_page_candidate":
            assert payload["human_approval_required"] is True
            assert payload["corpus_slice"]["review_required"] is True


def test_no_approved_approval_record_is_committed() -> None:
    for path in APPROVAL_DIR.glob("*.yaml"):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert payload["approval_status"] != "approved"
        assert payload["approved_for_execution"] is False


def test_generated_review_packet_paths_are_ignored() -> None:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", "experiments/results/proposal-reviews/stage2g/summary.json"],
        cwd=REPO,
        check=False,
    )

    assert result.returncode == 0

