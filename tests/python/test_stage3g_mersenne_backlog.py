from __future__ import annotations

from pathlib import Path

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.method_backlog.counts import validate_candidate_count
from libreprimus.method_backlog.loader import load_method_backlog
from libreprimus.method_backlog.support import classify_executor_support
from libreprimus.method_backlog.validation import validate_method_backlog_item, validate_stage3e_queue_item

REPO = Path(__file__).resolve().parents[2]
BACKLOG = REPO / "experiments/queues/stage3e-method-backlog.yaml"
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"


def test_mersenne_backlog_item_is_bounded_probe_promoted_for_stage3j() -> None:
    backlog = load_method_backlog(BACKLOG)
    item = next(item for item in backlog.items if item["experiment_id"] == "stage3i_mersenne_prime_stream_tiny_v1")
    validated = validate_method_backlog_item(item)

    assert validated["candidate_count_estimate"] == 192
    assert validated["implementation_status"] == "runnable_now"
    assert validated["evidence_level"] == "weak_to_moderate"
    assert validated["cuda_enabled"] is False
    assert validated["no_solve_claim"] is True


def test_mersenne_queue_item_is_runnable_after_stage3j_executor() -> None:
    queue = load_bounded_queue(QUEUE)
    item = next(item for item in queue.items if item["item_id"] == "stage3i_mersenne_prime_stream_tiny_v1")
    validated = validate_stage3e_queue_item(item)

    assert validate_candidate_count(validated) == 192
    assert validated["implementation_status"] == "runnable_now"
    assert validated["dry_run_only"] is False
    assert validated["output_policy"]["execution_enabled"] is True
    assert classify_executor_support(validated) == ("runnable_now", "stage3j_mersenne_stream_probe_executor")
