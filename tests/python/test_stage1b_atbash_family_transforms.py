import pytest

from libreprimus.solved_fixtures.atbash_family import (
    decode_atbash_family,
    reverse_gematria_index,
    rotated_reverse_gematria_index,
)


def test_reverse_gematria_index_formula() -> None:
    assert reverse_gematria_index(0) == 28
    assert reverse_gematria_index(28) == 0
    assert reverse_gematria_index(14) == 14


def test_rotated_reverse_gematria_index_formula() -> None:
    assert rotated_reverse_gematria_index(0, rotation=3) == 2
    assert rotated_reverse_gematria_index(28, rotation=3) == 3
    assert rotated_reverse_gematria_index(2, rotation=3) == 0


def test_rotated_reverse_requires_explicit_rotation() -> None:
    with pytest.raises(ValueError, match="rotation"):
        decode_atbash_family(
            [{"token_kind": "rune", "index29": 0, "token_index_global": 0}],
            method_family="rotated_reverse_gematria",
            transform_chain=[{"name": "rotated_reverse_gematria", "params": {}}],
        )


def test_invalid_index_fails_clearly() -> None:
    with pytest.raises(ValueError, match="Z_29"):
        reverse_gematria_index(29)


def test_atbash_family_preserves_separators_and_numbers_without_search() -> None:
    result = decode_atbash_family(
        [
            {"token_kind": "rune", "index29": 0, "token_index_global": 0},
            {"token_kind": "word_separator", "raw_text": "-", "token_index_global": 1},
            {"token_kind": "numeric_literal", "raw_text": "123", "token_index_global": 2},
            {"token_kind": "clause_separator", "raw_text": ".", "token_index_global": 3},
            {"token_kind": "rune", "index29": 28, "token_index_global": 4},
        ],
        method_family="reverse_gematria",
        transform_chain=[{"name": "reverse_gematria", "params": {}}],
    )

    assert result["decoded_normalized_plaintext"] == "EA 123. F"
    assert "vigenere" not in result["decoded_index_formula"].lower()
    assert "prime" not in result["decoded_index_formula"].lower()
