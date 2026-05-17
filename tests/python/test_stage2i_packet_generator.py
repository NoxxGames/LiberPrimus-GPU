from __future__ import annotations

import json
from pathlib import Path

from libreprimus.approval_readiness.export import write_approval_readiness_outputs
from libreprimus.approval_readiness.packet_generator import build_approval_readiness_packet

REPO = Path(__file__).resolve().parents[2]
PROPOSAL = REPO / "experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml"
APPROVAL = REPO / "experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml"


def test_packet_generated(tmp_path: Path) -> None:
    packet = build_approval_readiness_packet(PROPOSAL, approval_path=APPROVAL, out_dir=tmp_path)

    assert packet.record_type == "approval_readiness_packet"
    assert packet.proposal_id == "stage2i-first-bounded-caesar-affine-review"


def test_packet_false_flags_and_candidate_count(tmp_path: Path) -> None:
    packet = build_approval_readiness_packet(PROPOSAL, approval_path=APPROVAL, out_dir=tmp_path)

    assert packet.execution_enabled is False
    assert packet.approved_for_execution is False
    assert packet.candidate_count_estimate == 841
    assert packet.candidate_count_upper_bound == 841


def test_packet_has_blocking_conditions(tmp_path: Path) -> None:
    packet = build_approval_readiness_packet(PROPOSAL, approval_path=APPROVAL, out_dir=tmp_path)

    assert packet.blocking_conditions
    assert "separate_human_decision_required" in packet.blocking_conditions


def test_packet_contains_no_candidate_plaintexts_or_raw_text(tmp_path: Path) -> None:
    packet = build_approval_readiness_packet(PROPOSAL, approval_path=APPROVAL, out_dir=tmp_path)
    paths = write_approval_readiness_outputs(tmp_path, packet)
    text = paths["packet_json"].read_text(encoding="utf-8")

    assert "candidate_plaintext" not in text
    assert "BEGIN RAW" not in text
    assert "data/raw/" not in text
    assert json.loads(text)["real_unsolved_material_touched"] is True
