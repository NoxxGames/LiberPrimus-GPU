from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from libreprimus.experiments.manifest_loader import validate_exploratory_manifest_payload

REPO = Path(__file__).resolve().parents[2]
VALID_MANIFEST = REPO / "experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml"


def _payload() -> dict[str, Any]:
    return yaml.safe_load(VALID_MANIFEST.read_text(encoding="utf-8"))


def _assert_invalid(payload: dict[str, Any]) -> None:
    with pytest.raises(Exception):
        validate_exploratory_manifest_payload(payload)


def test_valid_exploratory_manifest_validates() -> None:
    validate_exploratory_manifest_payload(_payload())


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
def test_true_safety_flags_fail(field: str) -> None:
    payload = _payload()
    payload[field] = True

    _assert_invalid(payload)


def test_missing_candidate_upper_bound_fails() -> None:
    payload = _payload()
    del payload["expected_candidate_count_upper_bound"]

    _assert_invalid(payload)


def test_future_unsolved_slice_without_review_fails() -> None:
    payload = _payload()
    payload["corpus_slice"]["review_required"] = False

    _assert_invalid(payload)
