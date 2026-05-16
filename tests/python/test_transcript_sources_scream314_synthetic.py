from pathlib import Path

from libreprimus.transcript_sources.scream314_reference import parse_scream314_reference


def test_scream314_parser_extracts_page_count_and_labels(tmp_path: Path) -> None:
    path = tmp_path / "liber_primus.md"
    path.write_text(
        "LP2 is 58 pages long (0-57).\n"
        "## Liber Primus - 57.jpg\n"
        "**Key:** Vigenere prime method note.\n",
        encoding="utf-8",
    )

    records, summary = parse_scream314_reference(path)

    assert summary.lp2_page_count_statement == "LP2 is 58 pages long (0-57)."
    assert summary.page_label_count == 1
    assert any(record.page_label == "57.jpg" for record in records)
    assert any("vigenere" in record.method_keywords for record in records)
    assert all(record.trusted_as_canonical is False for record in records)
    assert summary.canonical_corpus_active is False
