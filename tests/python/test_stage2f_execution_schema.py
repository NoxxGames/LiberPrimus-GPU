from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from libreprimus.experiment_execution.manifest_loader import (
    validate_cpu_execution_manifest_payload,
)

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml"


def _payload() -> dict:
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


def test_valid_synthetic_execution_manifest_validates() -> None:
    validate_cpu_execution_manifest_payload(_payload())


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
def test_true_unsafe_flags_fail(field: str) -> None:
    payload = _payload()
    payload[field] = True

    with pytest.raises(Exception):
        validate_cpu_execution_manifest_payload(payload)


def test_future_unsolved_page_candidate_fails() -> None:
    payload = _payload()
    payload["corpus_slice"] = {
        "slice_id": "blocked",
        "slice_kind": "future_unsolved_page_candidate",
        "review_required": True,
    }

    with pytest.raises(ValueError, match="future_unsolved_page_candidate"):
        validate_cpu_execution_manifest_payload(payload)


def test_page_candidate_without_solved_fixture_flag_fails() -> None:
    payload = deepcopy(_payload())
    payload["corpus_slice"] = {
        "slice_id": "blocked-page",
        "slice_kind": "page_candidate",
        "solved_fixture_only": False,
    }

    with pytest.raises(ValueError, match="page_candidate"):
        validate_cpu_execution_manifest_payload(payload)

