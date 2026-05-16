from pathlib import Path

from libreprimus.alignment.pastebin_to_transcript import align_pastebin_to_transcript


PARABLE = "ᛈᚪᚱᚪᛒᛚᛖ"


def test_explicit_marker_and_parable_emit_noncanonical_boundaries(tmp_path: Path) -> None:
    pastebin = tmp_path / "pastebin.txt"
    pastebin.write_text(f"{{ᛋ}}\n{{{{53}}}}\n{{{PARABLE}}}\n{{{{43,97,11,97,61,73,67}}}}\n", encoding="utf-8")
    transcript = tmp_path / "rtkd.txt"
    transcript.write_text(f"%\nᛋ/\n{PARABLE}/\n", encoding="utf-8")

    result = align_pastebin_to_transcript(pastebin, transcript)
    boundaries = result["boundary_candidates"]

    assert any("explicit rtkd percent page marker" in boundary.evidence for boundary in boundaries)
    assert any(boundary.candidate_page_label == "57.jpg" for boundary in boundaries)
    assert all(boundary.canonical_page_boundary is False for boundary in boundaries)
    assert result["summary"].parable_boundary_candidate_present is True


def test_empty_pairs_do_not_create_canonical_boundaries(tmp_path: Path) -> None:
    pastebin = tmp_path / "pastebin.txt"
    pastebin.write_text("{}\n{}\n", encoding="utf-8")
    transcript = tmp_path / "rtkd.txt"
    transcript.write_text("ᛋ/\n", encoding="utf-8")

    result = align_pastebin_to_transcript(pastebin, transcript)

    assert result["alignments"][0].best_match is None
    assert all(boundary.canonical_page_boundary is False for boundary in result["boundary_candidates"])
    assert result["summary"].page_boundary_status == "tentative_not_finalized"
