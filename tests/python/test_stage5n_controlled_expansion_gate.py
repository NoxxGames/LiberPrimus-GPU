from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_solved_fixture_cuda_reporting.summary import load_summary


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def test_stage5n_controlled_expansion_gate_blocks_broad_and_unsolved_cuda() -> None:
    records = {record["gate_id"]: record for record in _records("data/cuda/stage5n-gematria-controlled-expansion-gate.yaml")}
    assert records["broad_solved_fixture_cuda_gate"]["gate_status"] == "blocked_broad_scope"
    assert records["unsolved_page_cuda_gate"]["gate_status"] == "blocked_unsolved"
    assert records["unsolved_page_cuda_gate"]["execution_permission_granted"] is False


def test_stage5n_next_stage_decision_is_deterministic_from_gate_statuses() -> None:
    summary = load_summary(Path("data/cuda/stage5n-solved-fixture-cuda-reporting-summary.yaml"))
    assert summary["controlled_expansion_gate_status_counts"] == {
        "approved_for_exact_repeat_only": 1,
        "blocked_broad_scope": 1,
        "blocked_unsolved": 1,
        "needs_candidate_selection": 1,
        "needs_result_store_preflight": 1,
    }
    assert summary["selected_next_stage"] == "Stage 5O - solved-fixture-safe Gematria CUDA repeat verification and result-store preflight"
