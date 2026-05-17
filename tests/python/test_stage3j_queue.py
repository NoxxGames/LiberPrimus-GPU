from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from libreprimus.bounded_experiments.policy_checker import check_item
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_experiments.runner import run_all
from libreprimus.method_backlog.counts import validate_candidate_count
from libreprimus.method_backlog.support import classify_executor_support
from libreprimus.method_backlog.validation import validate_stage3e_queue_item

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3j-bounded-cpu-queue.yaml"


def test_stage3j_queue_item_count_and_policy() -> None:
    item = load_bounded_queue(QUEUE).items[0]
    validated = validate_stage3e_queue_item(item)

    assert validated["item_id"] == "stage3j_mersenne_prime_stream_tiny_v1"
    assert validate_candidate_count(validated) == 192
    assert classify_executor_support(validated) == ("runnable_now", "stage3j_mersenne_stream_probe_executor")
    assert validated["cuda_enabled"] is False
    assert validated["no_solve_claim"] is True


def test_stage3j_policy_blocks_if_offsets_expand_without_count_update() -> None:
    policy = load_operator_policy(POLICY)
    item = deepcopy(load_bounded_queue(QUEUE).items[0])
    item["transform_plan"]["parameters"]["offsets"]["stop_inclusive"] = 16

    result = check_item(policy, item)

    assert "declared_exact_count_mismatch" in result.blocking_reasons


def test_stage3j_bounded_experiment_run_all_uses_mersenne_executor(tmp_path: Path) -> None:
    queue = load_bounded_queue(QUEUE).payload
    payload = dict(queue)
    item = deepcopy(payload["items"][0])
    selector = dict(item["corpus_slice"]["selector"])
    selector["index29_values"] = [0, 1, 2, 3]
    selector["token_records"] = [
        {"token_kind": "rune", "index29": 0, "token_index_global": 0, "line_index": 0},
        {"token_kind": "rune", "index29": 1, "token_index_global": 1, "line_index": 0},
        {"token_kind": "rune", "index29": 2, "token_index_global": 2, "line_index": 1},
        {"token_kind": "rune", "index29": 3, "token_index_global": 3, "line_index": 1},
    ]
    item["corpus_slice"]["selector"] = selector
    payload["items"] = [item]
    queue_path = tmp_path / "queue.yaml"
    queue_path.write_text(json.dumps(payload), encoding="utf-8")

    _checks, results, summary_path = run_all(POLICY, queue_path, tmp_path / "out", allow_warnings=True)

    assert len(results) == 1
    assert results[0].execution_performed is True
    assert results[0].summary["stage3j_run_id"]
    assert results[0].summary["mersenne_candidate_count"] == 192
    assert results[0].solve_claim_made is False
    assert json.loads(summary_path.read_text(encoding="utf-8"))["executed_count"] == 1
