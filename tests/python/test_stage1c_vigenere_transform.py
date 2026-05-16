from pathlib import Path

import pytest

from libreprimus.solved_fixtures.vigenere import decode_vigenere_explicit_key, key_text_to_indices
from libreprimus.profiles.gematria_profile import load_gematria_profile


def _profile():
    return load_gematria_profile(Path("data/profiles/gematria/gematria-primus-v0.json"))


def test_key_text_converts_to_gematria_indices() -> None:
    assert key_text_to_indices("DIVINITY", _profile()) == [23, 10, 1, 10, 9, 10, 16, 26]


def test_decrypt_subtract_formula_advances_on_runes_only() -> None:
    result = decode_vigenere_explicit_key(
        [
            {"token_kind": "rune", "index29": 1, "token_index_global": 0},
            {"token_kind": "word_separator", "raw_text": "-", "token_index_global": 1},
            {"token_kind": "numeric_literal", "raw_text": "7", "token_index_global": 2},
            {"token_kind": "rune", "index29": 2, "token_index_global": 3},
        ],
        transform_chain=[{"name": "vigenere_explicit_key", "params": {"key_text": "U", "direction": "decrypt_subtract"}}],
    )

    assert result["decoded_normalized_plaintext"] == "F 7U"
    assert result["key_indices"] == [1]


def test_cleartext_f_skip_is_fixture_declared_and_does_not_advance_key() -> None:
    result = decode_vigenere_explicit_key(
        [
            {"token_kind": "rune", "index29": 0, "token_index_global": 10},
            {"token_kind": "word_separator", "raw_text": "-", "token_index_global": 11},
            {"token_kind": "rune", "index29": 1, "token_index_global": 12},
        ],
        transform_chain=[
            {
                "name": "vigenere_explicit_key",
                "params": {
                    "key_text": "U",
                    "direction": "decrypt_subtract",
                    "skip_rule": {
                        "name": "cleartext_f_pass_through",
                        "cleartext_pass_through_rune_indices": [0],
                        "advance_key_on_skip": False,
                    },
                },
            }
        ],
    )

    assert result["decoded_normalized_plaintext"] == "F F"
    assert result["skip_rule_applied_count"] == 1


def test_skip_rule_not_applied_unless_declared() -> None:
    result = decode_vigenere_explicit_key(
        [{"token_kind": "rune", "index29": 0, "token_index_global": 0}],
        transform_chain=[{"name": "vigenere_explicit_key", "params": {"key_text": "U", "direction": "decrypt_subtract"}}],
    )

    assert result["decoded_normalized_plaintext"] == "EA"
    assert result["skip_rule_applied_count"] == 0


def test_invalid_key_and_direction_fail_clearly() -> None:
    with pytest.raises(ValueError, match="key"):
        decode_vigenere_explicit_key(
            [],
            transform_chain=[{"name": "vigenere_explicit_key", "params": {"key_text": "?", "direction": "decrypt_subtract"}}],
        )
    with pytest.raises(ValueError, match="direction"):
        decode_vigenere_explicit_key(
            [],
            transform_chain=[{"name": "vigenere_explicit_key", "params": {"key_text": "F", "direction": "encrypt"}}],
        )
