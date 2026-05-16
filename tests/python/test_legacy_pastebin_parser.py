from libreprimus.legacy_pastebin.parser import build_line_pairs, parse_prime_row, parse_rune_row

FIRST_PAIR = """{ᛋᚻᛖᚩᚷᛗᛡᚠ,ᛋᚣᛖᛝᚳ}
{{53,23,67,7,17,71,107,2},{53,103,67,79,13}}
"""


def test_parse_first_known_pair() -> None:
    line_pairs, warnings, rune_rows, prime_rows = build_line_pairs(FIRST_PAIR, "abc123")

    assert rune_rows == 1
    assert prime_rows == 1
    assert warnings == []
    assert len(line_pairs) == 1
    record = line_pairs[0]
    assert record.rune_words == ["ᛋᚻᛖᚩᚷᛗᛡᚠ", "ᛋᚣᛖᛝᚳ"]
    assert record.prime_words == [[53, 23, 67, 7, 17, 71, 107, 2], [53, 103, 67, 79, 13]]
    assert record.decimal_index_words == [[15, 8, 18, 3, 6, 19, 27, 0], [15, 26, 18, 21, 5]]
    assert record.trusted_as_canonical is False
    assert record.validated_prime_mapping is True


def test_empty_pair_preserved() -> None:
    line_pairs, warnings, _, _ = build_line_pairs("{}\n{}\n", "abc123")

    assert warnings == []
    assert len(line_pairs) == 1
    assert line_pairs[0].empty_pair is True
    assert line_pairs[0].rune_words == []
    assert line_pairs[0].prime_words == []
    assert line_pairs[0].page_boundary_confidence == "not_inferred"


def test_parse_row_helpers() -> None:
    assert parse_rune_row("{ᛋᚻ,ᛖ}") == ["ᛋᚻ", "ᛖ"]
    assert parse_rune_row("{}") == []
    assert parse_prime_row("{{53,23},{67}}") == [[53, 23], [67]]
    assert parse_prime_row("{}") == []
