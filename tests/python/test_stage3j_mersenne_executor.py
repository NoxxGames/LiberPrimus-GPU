from __future__ import annotations

from pathlib import Path

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_execution.mersenne_stream_probe import (
    EXPECTED_EXPONENT_SEQUENCE,
    load_declared_mersenne_probe,
    render_mersenne_candidate,
    run_mersenne_stream_probe_item,
    stream_signature_sha256,
)

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3j-bounded-cpu-queue.yaml"


def _item() -> dict:
    return load_bounded_queue(QUEUE).items[0]


def _synthetic_item() -> dict:
    item = dict(_item())
    corpus_slice = dict(item["corpus_slice"])
    selector = dict(corpus_slice["selector"])
    selector["index29_values"] = [0, 1, 2, 3, 4, 5]
    selector["token_records"] = [
        {"token_kind": "rune", "index29": 0, "token_index_global": 0, "line_index": 0},
        {"token_kind": "rune", "index29": 1, "token_index_global": 1, "line_index": 0},
        {"token_kind": "word_separator", "token_index_global": 2},
        {"token_kind": "rune", "index29": 2, "token_index_global": 3, "line_index": 1},
        {"token_kind": "rune", "index29": 3, "token_index_global": 4, "line_index": 1},
        {"token_kind": "rune", "index29": 4, "token_index_global": 5, "line_index": 1},
        {"token_kind": "rune", "index29": 5, "token_index_global": 6, "line_index": 1},
    ]
    corpus_slice["selector"] = selector
    item["corpus_slice"] = corpus_slice
    return item


def test_stage3j_declared_probe_counts() -> None:
    probe = load_declared_mersenne_probe(_item())

    assert len(probe.exponent_sequence) == 8
    assert len(probe.stream_variants) == 3
    assert len(probe.offsets) == 16
    assert len(probe.directions) == 2
    assert len(probe.reset_modes) == 2
    assert probe.expected_candidate_count == 192


def test_stage3j_forward_and_reverse_rendering() -> None:
    tokens = [{"token_kind": "rune", "index29": value, "line_index": 0} for value in [0, 1, 2, 3]]
    labels = {index: chr(65 + index) for index in range(29)}

    forward_text, forward_indices, _forward_exponents, _forward_values = render_mersenne_candidate(
        tokens,
        exponent_sequence=EXPECTED_EXPONENT_SEQUENCE,
        stream_variant="mersenne_mod29",
        offset=0,
        direction="forward",
        reset_mode="none",
        labels=labels,
    )
    reverse_text, reverse_indices, _reverse_exponents, _reverse_values = render_mersenne_candidate(
        tokens,
        exponent_sequence=EXPECTED_EXPONENT_SEQUENCE,
        stream_variant="mersenne_mod29",
        offset=0,
        direction="reverse",
        reset_mode="none",
        labels=labels,
    )

    assert forward_indices != reverse_indices
    assert forward_text
    assert reverse_text


def test_stage3j_duplicate_stream_signatures_are_detectable() -> None:
    tokens = [{"token_kind": "rune", "index29": value, "line_index": 0} for value in [0, 1, 2, 3]]
    signature_0 = stream_signature_sha256(
        tokens,
        exponent_sequence=EXPECTED_EXPONENT_SEQUENCE,
        stream_variant="mersenne_mod29",
        offset=0,
        direction="forward",
        reset_mode="none",
    )
    signature_8 = stream_signature_sha256(
        tokens,
        exponent_sequence=EXPECTED_EXPONENT_SEQUENCE,
        stream_variant="mersenne_mod29",
        offset=8,
        direction="forward",
        reset_mode="none",
    )

    assert signature_0 == signature_8


def test_stage3j_executor_writes_summary_with_duplicate_counts(tmp_path: Path) -> None:
    summary = run_mersenne_stream_probe_item(_synthetic_item(), out_dir=tmp_path, top_k=5)

    assert summary.expected_candidate_count == 192
    assert summary.executed_candidate_count == 192
    assert summary.deferred_candidate_count == 0
    assert summary.unique_stream_signature_count is not None
    assert summary.duplicate_stream_signature_count is not None
    assert summary.duplicate_stream_signature_count > 0
