from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from libreprimus.approval_readiness.readiness_analyzer import analyze_approval_readiness

REPO = Path(__file__).resolve().parents[2]
PROPOSAL = REPO / "experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml"
APPROVAL = REPO / "experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml"


def test_valid_stage2i_proposal_returns_review_ready() -> None:
    analysis = analyze_approval_readiness(PROPOSAL, approval_path=APPROVAL)

    assert analysis.readiness_status in {"ready_for_human_review", "blocked_pending_approval"}
    assert analysis.real_unsolved_material_touched is True


def test_pending_approval_keeps_proposal_blocked() -> None:
    analysis = analyze_approval_readiness(PROPOSAL, approval_path=APPROVAL)

    assert analysis.approval_status == "pending"
    assert "explicit_approved_approval_record_required_before_execution" in analysis.blocking_conditions


def test_missing_approval_keeps_proposal_blocked() -> None:
    analysis = analyze_approval_readiness(PROPOSAL)

    assert analysis.approval_status == "missing"
    assert "approval_record_missing" in analysis.blocking_conditions


def test_raw_dump_like_text_fails(tmp_path: Path) -> None:
    payload = yaml.safe_load(PROPOSAL.read_text(encoding="utf-8"))
    payload["notes"].append("BEGIN RAW")
    bad = tmp_path / "bad.yaml"
    bad.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    with pytest.raises(ValueError, match="raw corpus"):
        analyze_approval_readiness(bad, approval_path=APPROVAL)


def test_candidate_estimate_841_detected() -> None:
    analysis = analyze_approval_readiness(PROPOSAL, approval_path=APPROVAL)

    assert analysis.candidate_count_estimate == 841
    assert analysis.candidate_count_upper_bound == 841


def test_missing_review_checklist_fails(tmp_path: Path) -> None:
    payload = yaml.safe_load(PROPOSAL.read_text(encoding="utf-8"))
    del payload["review_checklist"]
    bad = tmp_path / "missing-checklist.yaml"
    bad.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    with pytest.raises(Exception):
        analyze_approval_readiness(bad, approval_path=APPROVAL)
