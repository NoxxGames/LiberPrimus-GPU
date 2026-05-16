from libreprimus.legacy_pastebin.parser import build_line_pairs
from libreprimus.legacy_pastebin.summary import summarize


def test_mismatched_word_count_warns() -> None:
    line_pairs, warnings, _, _ = build_line_pairs("{ᛋ,ᚻ}\n{{53}}\n", "abc123")

    assert len(line_pairs) == 1
    assert not line_pairs[0].word_count_match
    assert any("Word count mismatch" in warning.message for warning in warnings)


def test_mismatched_rune_prime_length_warns() -> None:
    line_pairs, warnings, _, _ = build_line_pairs("{ᛋᚻ}\n{{53}}\n", "abc123")

    assert len(line_pairs) == 1
    assert not line_pairs[0].per_word_length_match
    assert any("Rune/prime length mismatch" in warning.message for warning in warnings)


def test_unknown_prime_value_warns() -> None:
    line_pairs, warnings, _, _ = build_line_pairs("{ᛋ}\n{{999}}\n", "abc123")

    assert len(line_pairs) == 1
    assert line_pairs[0].decimal_index_words == [[None]]
    assert not line_pairs[0].validated_prime_mapping
    assert any("Unknown Gematria prime value" in warning.message for warning in warnings)


def test_unknown_glyph_alias_warning_not_silent() -> None:
    line_pairs, warnings, _, _ = build_line_pairs("{ᛂ}\n{{37}}\n", "abc123")

    assert len(line_pairs) == 1
    assert line_pairs[0].decimal_index_words == [[11]]
    assert line_pairs[0].glyph_alias_inferred is True
    assert line_pairs[0].validated_prime_mapping is True
    assert any("Unknown glyph" in warning.message for warning in warnings)


def test_prime_values_are_not_decimal_indices() -> None:
    line_pairs, _, _, _ = build_line_pairs("{ᛋ}\n{{53}}\n", "abc123")

    assert line_pairs[0].prime_words == [[53]]
    assert line_pairs[0].decimal_index_words == [[15]]
    assert line_pairs[0].prime_words != line_pairs[0].decimal_index_words


def test_summary_noncanonical_and_page_boundaries_not_finalized() -> None:
    line_pairs, warnings, rune_rows, prime_rows = build_line_pairs("{ᛋ}\n{{53}}\n", "abc123")
    summary = summarize(
        source_sha256="abc123",
        line_pairs=line_pairs,
        warnings=warnings,
        rune_row_count=rune_rows,
        prime_value_row_count=prime_rows,
    )

    assert summary.canonical_corpus_allowed is False
    assert summary.page_boundary_status == "not_finalized"
    assert summary.all_records_trusted_as_canonical is False
