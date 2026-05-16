from libreprimus.solved_fixtures.direct_translation import decode_direct_translation, sha256_text


def test_direct_translation_decodes_profile_labels_and_separators() -> None:
    tokens = [
        {"token_kind": "rune", "latin_label": "F", "token_index_global": 0},
        {"token_kind": "word_separator", "raw_text": "-", "token_index_global": 1},
        {"token_kind": "rune", "latin_label": "A", "token_index_global": 2},
        {"token_kind": "clause_separator", "raw_text": ".", "token_index_global": 3},
        {"token_kind": "numeric_literal", "raw_text": "123", "token_index_global": 4},
    ]

    result = decode_direct_translation(tokens)

    assert result["decoded_normalized_plaintext"] == "F A. 123"
    assert result["decoded_normalized_plaintext_sha256"] == sha256_text("F A. 123")
    assert result["rune_count"] == 2
    assert result["numeric_literal_count"] == 1


def test_direct_translation_preserves_unknown_symbol_with_warning() -> None:
    result = decode_direct_translation([{"token_kind": "unknown_symbol", "raw_text": "?", "token_index_global": 0}])

    assert result["decoded_normalized_plaintext"] == "?"
    assert result["warnings"]


def test_direct_translation_does_not_apply_non_direct_methods() -> None:
    tokens = [
        {
            "token_kind": "rune",
            "latin_label": "F",
            "raw_glyph": "\u16a0",
            "normalized_glyph": "\u16a0",
            "variant_mapping_applied": False,
            "token_index_global": 0,
        }
    ]

    assert decode_direct_translation(tokens)["decoded_normalized_plaintext"] == "F"


def test_direct_translation_variant_uses_recorded_normalized_view_only() -> None:
    tokens = [
        {
            "token_kind": "rune",
            "latin_label": "J",
            "raw_glyph": "\u16c2",
            "normalized_glyph": "\u16c4",
            "variant_mapping_applied": True,
            "token_index_global": 0,
        }
    ]

    result = decode_direct_translation(tokens)

    assert result["decoded_normalized_plaintext"] == "J"
    assert tokens[0]["raw_glyph"] == "\u16c2"
