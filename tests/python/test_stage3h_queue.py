from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.bounded_experiments.policy_checker import check_queue
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.method_backlog.counts import validate_candidate_count

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3h-bounded-cpu-queue.yaml"


def test_stage3h_queue_validates_and_counts_match() -> None:
    queue = load_bounded_queue(QUEUE)
    counts = {str(item["item_id"]): validate_candidate_count(item) for item in queue.items}

    assert counts["stage3h_reset_advance_ablation_v1"] == 64
    assert counts["stage3h_family_specific_negative_controls_v1"] == 100


def test_stage3h_queue_items_are_under_operator_policy() -> None:
    policy = load_operator_policy(POLICY)
    queue = load_bounded_queue(QUEUE)
    checks = check_queue(policy, queue)

    assert all(not check.blocking_reasons for check in checks)
    assert all(check.status == "pass" for check in checks)


def test_stage3h_generated_outputs_are_ignored() -> None:
    paths = [
        "experiments/results/bounded-auto-runs/stage3h/candidate_records.jsonl",
        "experiments/results/bounded-auto-runs/stage3h/top_candidates.jsonl",
        "experiments/results/bounded-auto-runs/stage3h/negative_control_records.jsonl",
        "experiments/results/bounded-auto-runs/stage3h/summary.json",
    ]

    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=REPO, check=False)
        assert result.returncode == 0
