from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.bounded_experiments.policy_checker import check_queue
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3b-bounded-cpu-queue.yaml"


def test_stage3b_queue_candidate_count_under_policy() -> None:
    policy = load_operator_policy(POLICY)
    queue = load_bounded_queue(QUEUE)
    checks = {check.item_id: check for check in check_queue(policy, queue)}

    assert checks["stage3b-caesar-affine-reverse-direction"].status == "pass"
    assert checks["stage3b-stage3a-rerank-control"].status == "pass"
    assert checks["stage3b-blocked-overbudget-control"].status == "fail"


def test_stage3b_generated_outputs_are_ignored() -> None:
    for path in [
        "experiments/results/bounded-auto-runs/stage3b/reranked_top_candidates.jsonl",
        "experiments/results/bounded-auto-runs/stage3b/reverse_direction/candidate_records.jsonl",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=REPO, check=False)
        assert result.returncode == 0, path


def test_stage3b_queue_has_no_solve_claims() -> None:
    queue = load_bounded_queue(QUEUE)

    assert all(item["no_solve_claim"] is True for item in queue.items)
    assert all(item.get("cuda_enabled") is False for item in queue.items)
