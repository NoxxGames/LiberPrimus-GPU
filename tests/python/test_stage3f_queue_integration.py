from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from libreprimus.bounded_experiments.policy_checker import check_item
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.method_backlog.counts import validate_candidate_count
from libreprimus.method_backlog.support import classify_executor_support

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"


def _target_item() -> dict:
    queue = load_bounded_queue(QUEUE)
    for item in queue.items:
        if item["item_id"] == "stage3e_vig_lp_evidence_pack_v1":
            return deepcopy(item)
    raise AssertionError("Stage 3F target item missing")


def test_stage3f_queue_item_count_matches_key_reset_advance_product() -> None:
    item = _target_item()

    assert validate_candidate_count(item) == 48
    assert classify_executor_support(item) == ("runnable_now", "stage3f_evidence_key_pack_executor")
    assert item["implementation_status"] == "runnable_now"
    assert item["required_executor"] == "stage3f_evidence_key_pack_executor"


def test_stage3f_queue_item_passes_operator_policy() -> None:
    policy = load_operator_policy(POLICY)
    item = _target_item()
    check = check_item(policy, item)

    assert check.status == "pass"
    assert not check.blocking_reasons


def test_stage3f_policy_blocks_key_expansion_without_count_update() -> None:
    policy = load_operator_policy(POLICY)
    item = _target_item()
    item["transform_plan"]["parameters"]["keys"].append("EXTRA")
    check = check_item(policy, item)

    assert "declared_vigenere_key_pack_count_mismatch" in check.blocking_reasons


def test_stage3f_historical_key_pack_is_no_longer_deferred_after_stage3i() -> None:
    queue = load_bounded_queue(QUEUE)
    item = next(item for item in queue.items if item["item_id"] == "stage3e_vig_history_key_pack_v1")

    assert classify_executor_support(item) == ("runnable_now", "stage3i_historical_key_pack_executor")
