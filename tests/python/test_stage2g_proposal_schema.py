from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from libreprimus.experiment_proposals.proposal_loader import validate_experiment_proposal_payload

REPO = Path(__file__).resolve().parents[2]
PROPOSAL = REPO / "experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml"


def _payload() -> dict:
    return yaml.safe_load(PROPOSAL.read_text(encoding="utf-8"))


def test_valid_proposal_validates() -> None:
    validate_experiment_proposal_payload(_payload())


@pytest.mark.parametrize(
    "field",
    [
        "execution_enabled",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
    ],
)
def test_true_unsafe_flags_fail(field: str) -> None:
    payload = _payload()
    payload[field] = True

    with pytest.raises(Exception):
        validate_experiment_proposal_payload(payload)


def test_missing_review_checklist_fails() -> None:
    payload = _payload()
    del payload["review_checklist"]

    with pytest.raises(Exception):
        validate_experiment_proposal_payload(payload)


def test_raw_dump_like_huge_text_fails() -> None:
    payload = deepcopy(_payload())

    with pytest.raises(ValueError, match="raw corpus"):
        validate_experiment_proposal_payload(payload, source_text="A" * 30001)

