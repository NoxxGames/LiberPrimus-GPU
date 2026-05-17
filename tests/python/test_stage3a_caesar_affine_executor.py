from __future__ import annotations

from libreprimus.bounded_execution.caesar_affine import affine_outputs, caesar_outputs
from libreprimus.bounded_execution.input_slice_loader import load_input_slice
from libreprimus.bounded_execution.runner import AFFINE_COUNT, CAESAR_COUNT, TOTAL_COUNT


def test_caesar_generates_29_candidates() -> None:
    outputs = caesar_outputs([0, 1, 28])

    assert len(outputs) == CAESAR_COUNT
    assert all(0 <= value <= 28 for _, values in outputs for value in values)


def test_affine_generates_812_candidates() -> None:
    outputs = affine_outputs([0, 1, 28])

    assert len(outputs) == AFFINE_COUNT
    assert all(0 <= value <= 28 for _, values in outputs for value in values)


def test_caesar_and_affine_total_is_841() -> None:
    assert len(caesar_outputs([4, 8, 15])) + len(affine_outputs([4, 8, 15])) == TOTAL_COUNT


def test_inline_input_slice_loader_validates_index_range() -> None:
    item = {
        "corpus_slice": {
            "slice_id": "synthetic-stage3a-test",
            "corpus_candidate_id": "synthetic-inline",
            "selector": {"selector_kind": "inline_index29_values", "index29_values": [0, 1, 28]},
        }
    }

    input_slice = load_input_slice(item)

    assert input_slice.index29_values == [0, 1, 28]
    assert input_slice.input_length == 3
    assert "synthetic_inline_index_stream" in input_slice.warnings
