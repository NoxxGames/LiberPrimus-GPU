from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.method_backlog.validation import validate_stage3e_queue_item

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"


def test_stage3e_queue_disables_cuda_and_solve_claims() -> None:
    queue = load_bounded_queue(QUEUE)

    for item in queue.items:
        assert item["cuda_enabled"] is False
        assert item["no_solve_claim"] is True
        assert item["canonical_corpus_active"] is False
        assert item["page_boundaries_final"] is False


def test_stage3e_queue_has_no_broad_dictionary_or_skip_mask_search() -> None:
    queue = load_bounded_queue(QUEUE)

    for item in queue.items:
        validate_stage3e_queue_item(item)
        assert not _nested_true(item, "dictionary_search_enabled")
        assert not _nested_true(item, "key_search_enabled")
        assert not _nested_true(item, "unconstrained_skip_masks")


def _nested_true(payload: Any, key: str) -> bool:
    if isinstance(payload, dict):
        return payload.get(key) is True or any(_nested_true(value, key) for value in payload.values())
    if isinstance(payload, list):
        return any(_nested_true(value, key) for value in payload)
    return False
