from __future__ import annotations

from libreprimus.bounded_execution.mersenne_stream_probe import (
    EXPECTED_EXPONENT_SEQUENCE,
    cyclic_exponent_at,
    mersenne_minus_one_mod29,
    mersenne_mod29,
    perfect_number_mod29,
)


def test_stage3j_exponent_sequence_is_fixed() -> None:
    assert EXPECTED_EXPONENT_SEQUENCE == [2, 3, 5, 7, 13, 17, 19, 31]


def test_stage3j_mersenne_mod29_values_are_deterministic() -> None:
    assert [mersenne_mod29(exponent) for exponent in EXPECTED_EXPONENT_SEQUENCE[:4]] == [3, 7, 2, 11]


def test_stage3j_mersenne_minus_one_mod29_values_are_deterministic() -> None:
    assert [mersenne_minus_one_mod29(exponent) for exponent in EXPECTED_EXPONENT_SEQUENCE[:4]] == [2, 6, 1, 10]


def test_stage3j_perfect_number_mod29_values_are_deterministic() -> None:
    assert [perfect_number_mod29(exponent) for exponent in EXPECTED_EXPONENT_SEQUENCE[:4]] == [6, 28, 3, 8]


def test_stage3j_cyclic_exponent_indexing_is_explicit() -> None:
    sequence = EXPECTED_EXPONENT_SEQUENCE
    assert cyclic_exponent_at(sequence, offset=8, token_position=0, segment_length=4, direction="forward") == 2
    assert cyclic_exponent_at(sequence, offset=3, token_position=2, segment_length=4, direction="forward") == 17
    assert cyclic_exponent_at(sequence, offset=0, token_position=0, segment_length=4, direction="reverse") == 7
    assert cyclic_exponent_at(sequence, offset=0, token_position=3, segment_length=4, direction="reverse") == 2
