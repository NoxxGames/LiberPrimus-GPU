from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_execution.caesar_affine import labels_by_index
from libreprimus.bounded_execution.prime_offset_sweep import (
    load_declared_prime_offset_sweep,
    prime_minus_one_stream_value,
    prime_stream_index,
    render_prime_offset_candidate,
    run_prime_offset_sweep_item,
)
from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.prime_stream import first_n_primes

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"


def _target_item() -> dict:
    queue = load_bounded_queue(QUEUE)
    for item in queue.items:
        if item["item_id"] == "stage3e_prime_minus_one_offsets_v1":
            return deepcopy(item)
    raise AssertionError("Stage 3G target item missing")


def _synthetic_item(*, with_line_metadata: bool = True) -> dict:
    item = _target_item()
    token_records = [
        {"token_kind": "rune", "index29": 20, "token_index_global": 0, "logical_line_index": 1},
        {"token_kind": "word_separator", "token_index_global": 1, "logical_line_index": 1},
        {"token_kind": "rune", "index29": 10, "token_index_global": 2, "logical_line_index": 1},
        {"token_kind": "physical_newline", "token_index_global": 3, "logical_line_index": 1},
        {"token_kind": "rune", "index29": 17, "token_index_global": 4, "logical_line_index": 2},
        {"token_kind": "rune", "index29": 18, "token_index_global": 5, "logical_line_index": 2},
    ]
    if not with_line_metadata:
        for token in token_records:
            token.pop("logical_line_index", None)
    item["corpus_slice"]["slice_id"] = "stage3g-synthetic-slice"
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3g-synthetic",
        "index29_values": [20, 10, 17, 18],
        "token_records": token_records,
        "raw_unsolved_text_included": False,
    }
    item["corpus_slice"]["metadata_paths"] = []
    return item


def test_prime_generator_and_prime_minus_one_values() -> None:
    assert first_n_primes(10) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert [prime_minus_one_stream_value(index) for index in range(5)] == [1, 2, 4, 6, 10]


def test_prime_offset_sweep_declared_counts() -> None:
    sweep = load_declared_prime_offset_sweep(_target_item())

    assert len(sweep.offsets) == 64
    assert len(sweep.directions) == 2
    assert len(sweep.reset_modes) == 2
    assert sweep.expected_candidate_count == 256


def test_forward_and_reverse_stream_indexing() -> None:
    assert [prime_stream_index(3, pos, 4, "forward") for pos in range(4)] == [3, 4, 5, 6]
    assert [prime_stream_index(3, pos, 4, "reverse") for pos in range(4)] == [6, 5, 4, 3]


def test_reset_none_and_line_execute_with_line_metadata(tmp_path: Path) -> None:
    summary = run_prime_offset_sweep_item(_synthetic_item(with_line_metadata=True), out_dir=tmp_path, top_k=5)

    assert summary.expected_candidate_count == 256
    assert summary.executed_candidate_count == 256
    assert summary.deferred_candidate_count == 0
    assert summary.prime_candidate_count == 256
    assert summary.solve_claim is False


def test_line_reset_defers_without_line_metadata(tmp_path: Path) -> None:
    summary = run_prime_offset_sweep_item(_synthetic_item(with_line_metadata=False), out_dir=tmp_path, top_k=5)

    assert summary.expected_candidate_count == 256
    assert summary.executed_candidate_count == 128
    assert summary.deferred_candidate_count == 128
    assert any("line_reset_metadata_missing" in warning for warning in summary.warnings)


def test_prime_offset_formula_uses_subtract_convention() -> None:
    labels = labels_by_index(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")
    text, output_indices, prime_indices, stream_values = render_prime_offset_candidate(
        [{"token_kind": "rune", "index29": 5}, {"token_kind": "rune", "index29": 1}],
        offset=0,
        direction="forward",
        reset_mode="none",
        labels=labels,
    )

    assert prime_indices == [0, 1]
    assert stream_values == [1, 2]
    assert output_indices == [4, 28]
    assert text
