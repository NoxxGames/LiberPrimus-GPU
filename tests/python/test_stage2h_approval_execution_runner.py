from __future__ import annotations

from pathlib import Path

from libreprimus.approval_execution.execution_bridge import run_approval_execution_request

REPO = Path(__file__).resolve().parents[2]
STAGE2H = REPO / "experiments/proposals/stage2h"
SYNTHETIC_REQUEST = STAGE2H / "stage2h-approved-synthetic-direct-request.yaml"
SOLVED_REQUEST = STAGE2H / "stage2h-approved-solved-fixture-replay-request.yaml"
NOOP_REQUEST = STAGE2H / "stage2h-noop-real-request.yaml"


def test_approved_synthetic_direct_executes(tmp_path: Path) -> None:
    plan, result = run_approval_execution_request(SYNTHETIC_REQUEST, out_dir=tmp_path)

    assert plan.approval_gate_status == "pass"
    assert result.execution_status == "pass"
    assert result.execution_performed is True
    assert result.search_performed is False
    assert result.candidate_generation_performed is False
    assert result.scoring_used is False
    assert result.cuda_used is False
    assert result.unsolved_execution_allowed is False
    assert "candidate_plaintexts" not in result.summary


def test_approved_solved_replay_executes_or_delegates(tmp_path: Path) -> None:
    plan, result = run_approval_execution_request(SOLVED_REQUEST, out_dir=tmp_path)

    assert plan.approval_gate_status == "pass"
    assert result.execution_status == "pass"
    assert result.execution_performed is True
    assert result.summary["underlying_pass_count"] == 1


def test_noop_real_proposal_blocks_without_execution(tmp_path: Path) -> None:
    plan, result = run_approval_execution_request(NOOP_REQUEST, out_dir=tmp_path)

    assert plan.approval_gate_status == "blocked"
    assert result.execution_status in {"blocked", "skipped"}
    assert result.execution_performed is False
    assert result.underlying_execution_result_ids == []

