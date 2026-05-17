from __future__ import annotations

import pytest

from libreprimus.bounded_execution.reset_advance import (
    apply_stateful_transform,
    build_tokens,
    unsupported_reset_reason,
)

LABELS = {index: chr(ord("A") + index) for index in range(29)}


def _tokens(with_word: bool = True, with_clause: bool = True, with_line: bool = True):
    records = [
        {"token_kind": "rune", "index29": 5, "token_index_global": 0, "logical_line_index": 1},
        {"token_kind": "word_separator", "token_index_global": 1, "logical_line_index": 1},
        {"token_kind": "rune", "index29": 6, "token_index_global": 2, "logical_line_index": 1},
        {"token_kind": "clause_separator", "token_index_global": 3, "logical_line_index": 1},
        {"token_kind": "rune", "index29": 7, "token_index_global": 4, "logical_line_index": 2},
    ]
    if not with_word:
        records[1]["token_kind"] = "unknown_symbol"
    if not with_clause:
        records[3]["token_kind"] = "unknown_symbol"
    if not with_line:
        for record in records:
            record.pop("logical_line_index", None)
    return build_tokens(records)


def test_reset_none_segments_whole_sequence() -> None:
    rendered = apply_stateful_transform(
        _tokens(),
        LABELS,
        reset_mode="none",
        advance_mode="runes_only",
        transform_step=lambda _cipher, position: (position, {}),
    )

    assert rendered.output_indices == [0, 1, 2]


def test_reset_line_segments_by_line_metadata() -> None:
    rendered = apply_stateful_transform(
        _tokens(),
        LABELS,
        reset_mode="line",
        advance_mode="runes_only",
        transform_step=lambda _cipher, position: (position, {}),
    )

    assert rendered.output_indices == [0, 1, 0]


def test_word_and_clause_reset_require_metadata() -> None:
    assert unsupported_reset_reason(_tokens(with_word=False), "word") == "word_reset_metadata_missing"
    assert unsupported_reset_reason(_tokens(with_clause=False), "clause") == "clause_reset_metadata_missing"


def test_missing_line_metadata_defers_instead_of_faking() -> None:
    assert unsupported_reset_reason(_tokens(with_line=False), "line") == "line_reset_metadata_missing"
    with pytest.raises(ValueError, match="line_reset_metadata_missing"):
        apply_stateful_transform(
            _tokens(with_line=False),
            LABELS,
            reset_mode="line",
            advance_mode="runes_only",
            transform_step=lambda cipher, _position: (cipher, {}),
        )


def test_runes_only_advances_only_transformable_tokens() -> None:
    rendered = apply_stateful_transform(
        _tokens(),
        LABELS,
        reset_mode="none",
        advance_mode="runes_only",
        transform_step=lambda _cipher, position: (position, {}),
    )

    assert rendered.output_indices == [0, 1, 2]
    assert " " not in rendered.output_text


def test_token_break_preserving_preserves_separators() -> None:
    rendered = apply_stateful_transform(
        _tokens(),
        LABELS,
        reset_mode="none",
        advance_mode="token_break_preserving",
        transform_step=lambda _cipher, position: (position, {}),
    )

    assert " " in rendered.output_text
    assert "." in rendered.output_text
