from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.bounded_experiments.policy_checker import check_queue
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3c-bounded-cpu-queue.yaml"


def test_stage3c_next_queue_candidate_count_under_policy() -> None:
    policy = load_operator_policy(POLICY)
    queue = load_bounded_queue(QUEUE)
    checks = {check.item_id: check for check in check_queue(policy, queue)}

    assert checks["stage3c-small-vigenere-known-motif-key-list"].status == "pass"
    assert checks["stage3c-blocked-overbudget-control"].status == "fail"
    item = next(item for item in queue.items if item["item_id"] == "stage3c-small-vigenere-known-motif-key-list")
    assert item["candidate_count_upper_bound"] == 4
    assert item["cuda_enabled"] is False
    assert item["no_solve_claim"] is True


def test_stage3c_generated_outputs_are_ignored() -> None:
    for path in [
        "experiments/results/scoring-calibration/stage3c/calibration_summary.json",
        "experiments/results/scoring-calibration/stage3c/null_control_scores.jsonl",
        "experiments/results/scoring-calibration/stage3c/stage3_candidates_calibrated.jsonl",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=REPO, check=False)
        assert result.returncode == 0, path
