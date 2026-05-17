from __future__ import annotations

from pathlib import Path

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage2j-bounded-cpu-queue.yaml"


def test_queue_validates() -> None:
    queue = load_bounded_queue(QUEUE)

    assert queue.queue_id == "stage2j-bounded-cpu-queue"
    assert len(queue.items) == 3


def test_first_item_has_841_candidate_bound() -> None:
    queue = load_bounded_queue(QUEUE)
    first = next(item for item in queue.items if item["item_id"] == "stage2j-caesar-affine-first-reviewable-slice")

    assert first["candidate_count_upper_bound"] == 841
    assert first["cpu_only"] is True
    assert first["cuda_enabled"] is False


def test_overbudget_example_is_present() -> None:
    queue = load_bounded_queue(QUEUE)
    blocked = next(item for item in queue.items if item["item_id"] == "stage2j-blocked-overbudget-example")

    assert blocked["candidate_count_upper_bound"] == 100001
    assert blocked["expected_policy_status"] == "fail"
