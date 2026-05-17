from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
STAGE2H = REPO / "experiments/proposals/stage2h"
APPROVAL_DIR = STAGE2H / "approval-records"


def test_no_approved_unsolved_approval_records_are_committed() -> None:
    proposals = {
        path.stem: yaml.safe_load(path.read_text(encoding="utf-8"))
        for path in STAGE2H.glob("*.yaml")
        if not path.name.endswith("-request.yaml")
    }
    by_id = {payload["proposal_id"]: payload for payload in proposals.values()}
    for approval_path in APPROVAL_DIR.glob("*.yaml"):
        if approval_path.name == "README.md":
            continue
        approval = yaml.safe_load(approval_path.read_text(encoding="utf-8"))
        if approval.get("approval_status") != "approved":
            continue
        proposal = by_id[approval["proposal_id"]]
        assert proposal["corpus_slice"]["slice_kind"] != "future_unsolved_page_candidate"
        assert approval["approval_scope"]["execution_scope"] in {"synthetic_only", "solved_fixture_only"}


def test_no_stage2h_request_permits_unsolved_execution() -> None:
    for request_path in STAGE2H.glob("*-request.yaml"):
        request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
        assert request["unsolved_execution_allowed"] is False
        assert request["search_execution_enabled"] is False
        assert request["candidate_generation_enabled"] is False
        assert request["scoring_enabled"] is False
        assert request["cuda_enabled"] is False


def test_no_stage2h_proposal_includes_raw_unsolved_text() -> None:
    for proposal_path in STAGE2H.glob("*.yaml"):
        text = proposal_path.read_text(encoding="utf-8")
        assert "BEGIN RAW" not in text
        assert "data/raw/" not in text
        assert len(text) < 30000


def test_noop_real_request_uses_pending_approval() -> None:
    approval = yaml.safe_load((APPROVAL_DIR / "stage2h-noop-real-pending-approval.yaml").read_text(encoding="utf-8"))

    assert approval["approval_status"] == "pending"
    assert approval["approved_for_execution"] is False

