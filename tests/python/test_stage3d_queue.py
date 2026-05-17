from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from libreprimus.bounded_experiments.policy_checker import check_item
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3c-bounded-cpu-queue.yaml"


def test_stage3d_queue_item_candidate_count_matches_key_count() -> None:
    item = load_bounded_queue(QUEUE).items[0]
    keys = item["transform_plan"]["families"][0]["parameters"]["keys"]

    assert item["item_id"] == "stage3c-small-vigenere-known-motif-key-list"
    assert len(keys) == 4
    assert item["candidate_count_upper_bound"] == len(keys)
    assert item["cuda_enabled"] is False
    assert item["no_solve_claim"] is True


def test_stage3d_policy_blocks_key_count_above_candidate_bound() -> None:
    policy = load_operator_policy(POLICY)
    item = deepcopy(load_bounded_queue(QUEUE).items[0])
    item["candidate_count_upper_bound"] = 3

    check = check_item(policy, item)

    assert check.status == "fail"
    assert "declared_key_count_exceeds_candidate_bound" in check.blocking_reasons
