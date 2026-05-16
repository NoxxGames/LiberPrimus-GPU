from pathlib import Path

from libreprimus.alignment.pastebin_to_transcript import align_pastebin_to_transcript_followup

F = "\u16a0"
U = "\u16a2"
J = "\u16c4"
J_VARIANT = "\u16c2"
S = "\u16cb"
H = "\u16bb"


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def _best_pass(result: dict) -> str:
    return result["alignments"][0].best_match.match_pass


def test_followup_matches_physical_line_exactly(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", f"{{{S}{H}}}\n{{{{53,23}}}}\n")
    transcript = _write(tmp_path / "rtkd.txt", f"{S}{H}\n")

    result = align_pastebin_to_transcript_followup(pastebin, transcript)

    assert _best_pass(result) == "physical_line_exact_raw"
    assert result["alignments"][0].trusted_as_canonical is False


def test_followup_matches_logical_line_inside_physical_line(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", f"{{{S}{H}}}\n{{{{53,23}}}}\n")
    transcript = _write(tmp_path / "rtkd.txt", f"{F}{U}/{S}{H}/\n")

    result = align_pastebin_to_transcript_followup(pastebin, transcript)

    assert _best_pass(result) == "logical_line_exact_raw"
    assert result["summary"].logical_line_match_count == 1


def test_followup_matches_across_physical_line_segmentation(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", f"{{{S}{H}}}\n{{{{53,23}}}}\n")
    transcript = _write(tmp_path / "rtkd.txt", f"{F}\n{S}\n{H}\n{U}\n")

    result = align_pastebin_to_transcript_followup(pastebin, transcript)

    assert result["alignments"][0].best_match.match_pass == "stream_subsequence_exact"
    assert result["summary"].stream_subsequence_match_count == 1


def test_variant_normalized_match_preserves_raw_glyph(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", f"{{{J_VARIANT}}}\n{{{{37}}}}\n")
    transcript = _write(tmp_path / "rtkd.txt", f"{J}/\n")

    result = align_pastebin_to_transcript_followup(pastebin, transcript)

    best = result["alignments"][0].best_match
    assert best.variant_mapping_applied is True
    assert "variant" in best.match_pass
    assert result["pastebin_extraction"].line_pairs[0].rune_words == [J_VARIANT]


def test_decimal_index_subsequence_match_when_glyphs_differ(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", f"{{{J_VARIANT}{S}}}\n{{{{37,53}}}}\n")
    transcript = _write(tmp_path / "rtkd.txt", f"{F}\n{J}\n{S}\n{U}\n")

    result = align_pastebin_to_transcript_followup(pastebin, transcript)

    best = result["alignments"][0].best_match
    assert best.match_pass in {"stream_subsequence_documented_variant_normalized", "stream_subsequence_decimal_index"}
    assert best.confidence in {"high", "medium", "exact"}
