from __future__ import annotations

import json
from pathlib import Path

from libreprimus.experiment_proposals.export import write_review_packet_outputs
from libreprimus.experiment_proposals.proposal_loader import load_experiment_proposal
from libreprimus.experiment_proposals.review_packet import build_review_packet

REPO = Path(__file__).resolve().parents[2]
PROPOSAL = REPO / "experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml"


def test_review_packet_generated(tmp_path: Path) -> None:
    proposal = load_experiment_proposal(PROPOSAL)
    packet = build_review_packet(proposal, out_dir=tmp_path)

    assert packet.record_type == "experiment_review_packet"
    assert packet.execution_blocked is True
    assert packet.approved_for_execution is False


def test_review_packet_includes_safety_gates_and_candidate_count(tmp_path: Path) -> None:
    proposal = load_experiment_proposal(PROPOSAL)
    packet = build_review_packet(proposal, out_dir=tmp_path)

    assert packet.safety_gate_summary["human_approval_required"] is True
    assert packet.proposal_summary["candidate_count_estimate"] == 29


def test_review_packet_contains_no_candidate_plaintexts(tmp_path: Path) -> None:
    proposal = load_experiment_proposal(PROPOSAL)
    packet = build_review_packet(proposal, out_dir=tmp_path)
    paths = write_review_packet_outputs(tmp_path, packet)
    text = json.dumps(json.loads(paths["review_packet_json"].read_text(encoding="utf-8")))

    assert '"candidate_plaintexts":' not in text
    assert "No candidate plaintexts" in paths["review_packet_markdown"].read_text(encoding="utf-8")
