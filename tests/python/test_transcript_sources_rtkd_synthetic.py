from pathlib import Path

from libreprimus.transcript_sources.rtkd_master import parse_rtkd_master


def test_rtkd_parser_preserves_raw_text_and_line_numbers(tmp_path: Path) -> None:
    path = tmp_path / "rtkd.txt"
    path.write_text("Delimiters\nPage     : %\n%\nᛋ-ᚻ.ᛖ/\n", encoding="utf-8")

    records, summary = parse_rtkd_master(path)

    assert records[3].physical_line_number == 4
    assert records[3].raw_text == "ᛋ-ᚻ.ᛖ/"
    assert records[3].rune_glyphs == ["ᛋ", "ᚻ", "ᛖ"]
    assert records[3].separator_counts["word"] == 1
    assert records[3].separator_counts["clause"] == 1
    assert records[3].separator_counts["line"] == 1
    assert records[2].has_page_marker is True
    assert records[3].trusted_as_canonical is False
    assert summary.canonical_corpus_active is False


def test_rtkd_parser_warns_on_unknown_symbols_in_rune_lines(tmp_path: Path) -> None:
    path = tmp_path / "rtkd.txt"
    path.write_text("ᛋ@ᚻ/\n", encoding="utf-8")

    records, summary = parse_rtkd_master(path)

    assert records[0].rune_count == 2
    assert records[0].separator_counts["unknown_non_rune_symbol"] == 1
    assert records[0].parse_warnings
    assert summary.parse_warning_count == 1
