from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

from libreprimus.experiment_proposals.proposal_loader import load_experiment_proposal

REPO = Path(__file__).resolve().parents[2]
STAGE2I = REPO / "experiments/proposals/stage2i"
PROPOSAL = STAGE2I / "stage2i-first-bounded-caesar-affine-review.yaml"
APPROVAL = STAGE2I / "approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml"


def test_stage2i_proposal_and_pending_approval_exist() -> None:
    assert PROPOSAL.is_file()
    assert APPROVAL.is_file()


def test_no_approved_stage2i_approval_records_committed() -> None:
    for path in (STAGE2I / "approval-records").glob("*.yaml"):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert payload["approval_status"] != "approved"
        assert payload["approved_for_execution"] is False


def test_proposal_references_future_unsolved_metadata_without_raw_text() -> None:
    payload = yaml.safe_load(PROPOSAL.read_text(encoding="utf-8"))

    assert payload["corpus_slice"]["slice_kind"] == "future_unsolved_page_candidate"
    assert payload["corpus_slice"]["review_required"] is True
    assert "BEGIN RAW" not in PROPOSAL.read_text(encoding="utf-8")
    assert "data/raw/" not in PROPOSAL.read_text(encoding="utf-8")


def test_proposal_flags_false_and_candidate_bound() -> None:
    proposal = load_experiment_proposal(PROPOSAL)
    payload = proposal.payload

    for field in [
        "approved_for_execution",
        "execution_enabled",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
        "trusted_as_canonical",
    ]:
        assert payload[field] is False
    assert payload["candidate_count_estimate"] == 841
    assert payload["candidate_count_upper_bound"] == 841


def test_generated_approval_readiness_outputs_are_ignored() -> None:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", "experiments/results/approval-readiness/stage2i/summary.json"],
        cwd=REPO,
        check=False,
    )

    assert result.returncode == 0
