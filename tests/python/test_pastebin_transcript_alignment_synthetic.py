from pathlib import Path

from libreprimus.alignment.pastebin_to_transcript import align_pastebin_to_transcript


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_exact_raw_rune_sequence_match(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", "{ᛋᚻᛖ}\n{{53,23,67}}\n")
    transcript = _write(tmp_path / "rtkd.txt", "ᛋ-ᚻᛖ/\n")

    result = align_pastebin_to_transcript(pastebin, transcript)
    alignment = result["alignments"][0]

    assert alignment.best_match is not None
    assert alignment.best_match.confidence in {"exact", "high"}
    assert alignment.best_match.match_pass == "exact_raw_rune_sequence"
    assert alignment.trusted_as_canonical is False


def test_variant_normalized_match_is_documented(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", "{ᛂ}\n{{37}}\n")
    transcript = _write(tmp_path / "rtkd.txt", "ᛄ/\n")

    result = align_pastebin_to_transcript(pastebin, transcript)
    alignment = result["alignments"][0]

    assert alignment.best_match is not None
    assert alignment.best_match.confidence == "high"
    assert alignment.best_match.variant_mapping_applied is True


def test_word_length_only_does_not_create_high_confidence(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", "{ᛋᛋᛋ}\n{{53,53,53}}\n")
    transcript = _write(tmp_path / "rtkd.txt", "ᚠᚠᚠ/\n")

    result = align_pastebin_to_transcript(pastebin, transcript)
    alignment = result["alignments"][0]

    assert alignment.best_match is None
    assert result["summary"].no_match_count == 1


def test_timing_metadata_exists(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", "{ᛋ}\n{{53}}\n")
    transcript = _write(tmp_path / "rtkd.txt", "ᛋ/\n")

    result = align_pastebin_to_transcript(pastebin, transcript)

    assert "pastebin_parse" in result["summary"].elapsed_milliseconds
    assert "matching" in result["summary"].elapsed_milliseconds
