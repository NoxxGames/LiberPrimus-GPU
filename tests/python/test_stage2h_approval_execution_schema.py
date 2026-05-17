from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from libreprimus.approval_execution.request_loader import validate_approval_execution_request_payload

REPO = Path(__file__).resolve().parents[2]
REQUEST = REPO / "experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml"


def _payload() -> dict:
    return yaml.safe_load(REQUEST.read_text(encoding="utf-8"))


def test_valid_request_validates() -> None:
    validate_approval_execution_request_payload(_payload())


@pytest.mark.parametrize(
    "field",
    [
        "unsolved_execution_allowed",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
    ],
)
def test_true_safety_flag_fails(field: str) -> None:
    payload = _payload()
    payload[field] = True

    with pytest.raises(Exception):
        validate_approval_execution_request_payload(payload)


def test_unsupported_scope_fails() -> None:
    payload = _payload()
    payload["execution_scope"] = "future_unsolved_page_candidate"

    with pytest.raises(Exception):
        validate_approval_execution_request_payload(payload)


def test_raw_dump_like_request_fails() -> None:
    payload = _payload()
    source_text = yaml.safe_dump(deepcopy(payload)) + "\nBEGIN RAW\n" + ("X" * 100)

    with pytest.raises(ValueError, match="raw corpus"):
        validate_approval_execution_request_payload(payload, source_text=source_text)

