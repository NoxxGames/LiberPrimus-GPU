from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from libreprimus.approval_readiness.packet_generator import build_approval_readiness_packet
from libreprimus.approval_readiness.validation import validate_record

REPO = Path(__file__).resolve().parents[2]
PROPOSAL = REPO / "experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml"
APPROVAL = REPO / "experiments/proposals/stage2i/approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml"


def _packet(tmp_path: Path):
    return build_approval_readiness_packet(PROPOSAL, approval_path=APPROVAL, out_dir=tmp_path)


def test_valid_readiness_packet_validates(tmp_path: Path) -> None:
    validate_record(_packet(tmp_path))


@pytest.mark.parametrize(
    "field",
    [
        "approved_for_execution",
        "execution_enabled",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
    ],
)
def test_true_false_field_fails(tmp_path: Path, field: str) -> None:
    packet = replace(_packet(tmp_path), **{field: True})

    with pytest.raises(Exception):
        validate_record(packet)


def test_real_unsolved_with_approved_status_fails(tmp_path: Path) -> None:
    packet = replace(_packet(tmp_path), approval_status="approved")

    with pytest.raises(Exception):
        validate_record(packet)
