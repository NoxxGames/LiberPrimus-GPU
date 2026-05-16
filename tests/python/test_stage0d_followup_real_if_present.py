from pathlib import Path

import pytest

from libreprimus.alignment.pastebin_to_transcript import align_pastebin_to_transcript_followup
from libreprimus.paths import repo_root


def _real_sources() -> tuple[Path, Path]:
    root = repo_root()
    return (
        root / "data/raw/legacy-pastebins/58-Pages-In-Runes-With-Prime-Values-Pastebin.txt",
        root / "data/raw/transcripts/rtkd/liber-primus__transcription--master.txt",
    )


def test_real_stage0d_followup_smoke_if_present() -> None:
    pastebin, transcript = _real_sources()
    if not pastebin.is_file() or not transcript.is_file():
        pytest.skip("real Stage 0D-followup sources absent")

    result = align_pastebin_to_transcript_followup(pastebin, transcript)

    assert len(result["alignments"]) == 185
    assert result["gap_summary"].record_type == "alignment_gap_summary"
    assert result["boundary_audit_summary"].record_type == "page_boundary_audit"
    assert all(not alignment.trusted_as_canonical for alignment in result["alignments"])
    assert all(not boundary.canonical_page_boundary for boundary in result["boundary_candidates"])
    assert result["summary"].canonical_corpus_active is False
    assert result["summary"].page_boundary_status != "canonical"
    assert result["summary"].none_count <= 153
    assert result["boundary_audit_summary"].canonical_page_boundary_all_false is True


def test_real_glyph_variant_observation_preserves_raw_if_present() -> None:
    pastebin, transcript = _real_sources()
    if not pastebin.is_file() or not transcript.is_file():
        pytest.skip("real Stage 0D-followup sources absent")

    result = align_pastebin_to_transcript_followup(pastebin, transcript)
    observations = result["glyph_variant_observations"]

    assert observations
    assert observations[0].observed_glyph == "\u16c2"
    assert observations[0].observed_prime_value == 37
    assert observations[0].trusted_as_canonical is False
