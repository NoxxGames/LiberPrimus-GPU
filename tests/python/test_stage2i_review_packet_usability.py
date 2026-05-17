from __future__ import annotations

import json
from pathlib import Path

from libreprimus.approval_readiness.export import write_approval_readiness_outputs
from libreprimus.approval_readiness.packet_generator import build_approval_readiness_packet

REPO = Path(__file__).resolve().parents[2]
PROPOSAL = REPO / "experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml"
APPROVAL = REPO / "experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml"


def test_json_packet_includes_review_paths_and_corpus_metadata(tmp_path: Path) -> None:
    packet = build_approval_readiness_packet(PROPOSAL, approval_path=APPROVAL, out_dir=tmp_path)
    payload = json.loads(write_approval_readiness_outputs(tmp_path, packet)["packet_json"].read_text(encoding="utf-8"))

    assert payload["proposal_path"] == str(PROPOSAL)
    assert payload["approval_path"] == str(APPROVAL)
    assert payload["corpus_slice"]["slice_id"] == "stage2i-lp2-reviewable-page-candidate-placeholder"
    assert payload["corpus_slice"]["slice_kind"] == "future_unsolved_page_candidate"
    assert payload["corpus_slice"]["raw_unsolved_text_included"] is False
    assert payload["corpus_slice"]["metadata_paths"]


def test_json_packet_includes_machine_checks_decisions_and_commands(tmp_path: Path) -> None:
    packet = build_approval_readiness_packet(PROPOSAL, approval_path=APPROVAL, out_dir=tmp_path)
    payload = json.loads(write_approval_readiness_outputs(tmp_path, packet)["packet_json"].read_text(encoding="utf-8"))

    assert payload["machine_check_results"]
    assert {item["check"] for item in payload["machine_check_results"]} >= {
        "raw unsolved text included",
        "candidate bound present",
        "execution disabled",
        "generated outputs ignored",
    }
    assert {item["decision"] for item in payload["decision_options"]} == {
        "approve later execution",
        "revise proposal",
        "deny/defer",
    }
    assert set(payload["next_commands"]) == {"approve_later_execution", "revise_proposal", "deny_or_defer"}


def test_markdown_review_packet_is_human_readable(tmp_path: Path) -> None:
    packet = build_approval_readiness_packet(PROPOSAL, approval_path=APPROVAL, out_dir=tmp_path)
    paths = write_approval_readiness_outputs(tmp_path, packet)
    text = paths["review_markdown"].read_text(encoding="utf-8")

    assert paths["review_markdown"].name == "stage2i-first-bounded-caesar-affine-review.review.md"
    for heading in [
        "## Decision needed",
        "## Files to inspect",
        "## Machine checks",
        "## Candidate bounds",
        "## Decision options",
    ]:
        assert heading in text
    assert "BEGIN RAW" not in text
    assert "candidate_plaintext" not in text
    assert "Has the reviewable corpus slice metadata been reviewed by a human?" not in text


def test_missing_standalone_metadata_path_is_clear_revision_warning(tmp_path: Path) -> None:
    packet = build_approval_readiness_packet(PROPOSAL, approval_path=APPROVAL, out_dir=tmp_path)
    paths = write_approval_readiness_outputs(tmp_path, packet)
    payload = json.loads(paths["packet_json"].read_text(encoding="utf-8"))
    markdown = paths["review_markdown"].read_text(encoding="utf-8")

    assert payload["corpus_slice"]["metadata_path_status"] == "no_standalone_metadata_path_referenced"
    assert "No standalone corpus metadata file is currently referenced" in markdown
    assert "revise_or_defer_until_metadata_path_is_explicit" in markdown
