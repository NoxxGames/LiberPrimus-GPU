from __future__ import annotations

from pathlib import Path

from libreprimus.bounded_experiments.policy_checker import check_queue
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.method_backlog.counts import validate_candidate_count

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"


def test_stage3e_queue_validates_and_counts_match() -> None:
    queue = load_bounded_queue(QUEUE)
    counts = {str(item["item_id"]): validate_candidate_count(item) for item in queue.items}

    assert counts == {
        "stage3e_vig_lp_evidence_pack_v1": 48,
        "stage3e_prime_minus_one_offsets_v1": 256,
        "stage3e_vig_history_key_pack_v1": 56,
        "stage3e_negative_control_extension_v1": 100,
        "stage3e_reset_advance_ablation_v1": 64,
        "stage3e_prime_mod_gap_pack_v1": 256,
    }


def test_stage3e_queue_items_are_under_operator_policy() -> None:
    policy = load_operator_policy(POLICY)
    queue = load_bounded_queue(QUEUE)
    checks = check_queue(policy, queue)

    assert all(not check.blocking_reasons for check in checks)
    assert all(check.item_id.startswith("stage3e_") for check in checks)
