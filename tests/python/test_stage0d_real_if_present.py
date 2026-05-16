from pathlib import Path

import pytest

from libreprimus.alignment.pastebin_to_transcript import align_pastebin_to_transcript
from libreprimus.legacy_pastebin.export import extract_legacy_pastebin
from libreprimus.transcript_sources.rtkd_master import parse_rtkd_master

PASTEBIN = Path("data/raw/legacy-pastebins/58-Pages-In-Runes-With-Prime-Values-Pastebin.txt")
RTKD = Path("data/raw/transcripts/rtkd/liber-primus__transcription--master.txt")


def test_real_stage0d_sources_if_present() -> None:
    if not (PASTEBIN.is_file() and RTKD.is_file()):
        pytest.skip("real Stage 0D sources absent")

    transcript_records, transcript_summary = parse_rtkd_master(RTKD)
    pastebin_extraction = extract_legacy_pastebin(PASTEBIN)
    result = align_pastebin_to_transcript(PASTEBIN, RTKD)

    assert transcript_summary.physical_line_count > 100
    assert len(transcript_records) == transcript_summary.physical_line_count
    assert pastebin_extraction.summary.line_pair_count == 185
    assert len(result["alignments"]) == 185
    assert result["summary"].exact_confidence_match_count + result["summary"].high_confidence_match_count >= 1
    assert any(anchor.page_label_candidate == "57.jpg" for anchor in pastebin_extraction.anchors)
    assert result["boundary_candidates"]
    assert all(alignment.trusted_as_canonical is False for alignment in result["alignments"])
    assert all(boundary.canonical_page_boundary is False for boundary in result["boundary_candidates"])
    assert result["summary"].canonical_corpus_active is False
    if any("ᛂ" in "".join(line_pair.rune_words) for line_pair in pastebin_extraction.line_pairs):
        assert result["glyph_variant_observations"]
