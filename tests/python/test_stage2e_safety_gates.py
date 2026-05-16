from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.experiments.candidate_estimator import estimate_candidate_count
from libreprimus.experiments.safety_gates import evaluate_safety_gates

REPO = Path(__file__).resolve().parents[2]
VALID_MANIFEST = REPO / "experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml"


def _payload() -> dict:
    return yaml.safe_load(VALID_MANIFEST.read_text(encoding="utf-8"))


def _gates(payload: dict, out_dir: Path | None = None):
    return evaluate_safety_gates(
        payload,
        estimate_candidate_count(payload),
        out_dir=out_dir or REPO / "experiments/results/exploratory-dry-runs/stage2e",
    )


def test_all_false_flags_pass() -> None:
    assert not [gate for gate in _gates(_payload()) if gate.is_failure]


def test_execution_true_fails() -> None:
    payload = _payload()
    payload["execution_enabled"] = True

    assert any(gate.gate_id == "execution_enabled" and gate.is_failure for gate in _gates(payload))


def test_estimated_count_greater_than_upper_bound_fails() -> None:
    payload = _payload()
    payload["expected_candidate_count_upper_bound"] = 1

    assert any(gate.gate_id == "candidate_count_within_bound" and gate.is_failure for gate in _gates(payload))


def test_output_path_outside_ignored_repo_directory_fails() -> None:
    payload = _payload()

    assert any(
        gate.gate_id == "output_path_policy" and gate.is_failure
        for gate in _gates(payload, out_dir=REPO / "not-ignored-stage2e-output")
    )


def test_future_unsolved_slice_without_review_fails() -> None:
    payload = _payload()
    payload["corpus_slice"]["review_required"] = False

    assert any(
        gate.gate_id == "future_unsolved_slice_review_required" and gate.is_failure
        for gate in _gates(payload)
    )
