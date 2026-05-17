from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.bounded_experiments.runner import run_all
from libreprimus.bounded_experiments.summary import load_summary

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage2j-bounded-cpu-queue.yaml"


def test_run_all_does_not_run_blocked_item(tmp_path: Path) -> None:
    checks, results, summary_path = run_all(POLICY, QUEUE, tmp_path, allow_warnings=True)
    by_item = {result.item_id: result for result in results}

    assert summary_path.is_file()
    assert len(checks) == 3
    assert by_item["stage2j-caesar-affine-first-reviewable-slice"].execution_status in {"pass", "deferred"}
    if by_item["stage2j-caesar-affine-first-reviewable-slice"].execution_status == "pass":
        assert by_item["stage2j-caesar-affine-first-reviewable-slice"].search_performed is True
        assert by_item["stage2j-caesar-affine-first-reviewable-slice"].scoring_used is True
    else:
        assert by_item["stage2j-caesar-affine-first-reviewable-slice"].deferred_reason == "missing_reviewable_slice_input"
    assert by_item["stage2j-solved-baseline-regression-control"].execution_status == "pass"
    assert by_item["stage2j-solved-baseline-regression-control"].execution_performed is True
    assert by_item["stage2j-blocked-overbudget-example"].execution_status == "blocked"
    assert by_item["stage2j-blocked-overbudget-example"].execution_performed is False
    assert all(result.cuda_used is False for result in results)


def test_run_all_writes_ignored_outputs() -> None:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", "experiments/results/bounded-auto-runs/stage2j/summary.json"],
        cwd=REPO,
        check=False,
    )

    assert result.returncode == 0


def test_run_all_summary_counts(tmp_path: Path) -> None:
    run_all(POLICY, QUEUE, tmp_path, allow_warnings=True)
    summary = load_summary(tmp_path)

    assert summary["policy_pass_count"] == 2
    assert summary["policy_blocked_count"] == 1
    assert summary["executed_count"] in {1, 2}
    assert summary["deferred_count"] in {0, 1}
    assert summary["blocked_count"] == 1
