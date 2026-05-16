from pathlib import Path

import pytest

from libreprimus.corpus_candidate.export import write_corpus_candidate_outputs
from libreprimus.corpus_candidate.generator import build_rtkd_corpus_candidate
from libreprimus.paths import repo_root


def test_stage0e_real_candidate_if_present(tmp_path: Path) -> None:
    root = repo_root()
    transcript = root / "data/raw/transcripts/rtkd/liber-primus__transcription--master.txt"
    gematria = root / "data/profiles/gematria/gematria-primus-v0.json"
    separators = root / "data/profiles/separators/rtkd-separator-grammar-v0.json"
    variants = root / "data/profiles/glyph-variants/glyph-variants-v0.json"
    if not all(path.is_file() for path in [transcript, gematria, separators, variants]):
        pytest.skip("real Stage 0E sources or profiles absent")

    result = build_rtkd_corpus_candidate(
        transcript_path=transcript,
        gematria_path=gematria,
        glyph_variants_path=variants,
        separators_path=separators,
        alignment_dir=root / "data/normalized/alignment",
    )
    out_dir = tmp_path / "candidate"
    write_corpus_candidate_outputs(out_dir, result)

    manifest = result["manifest"]
    assert manifest.canonical_corpus_candidate is True
    assert manifest.canonical_corpus_active is False
    assert manifest.page_boundaries_final is False
    assert manifest.trusted_as_canonical is False
    assert result["summary"].token_count > 0
    assert result["summary"].rune_token_count > 0
    assert result["summary"].separator_token_count > 0
    assert all(not page.canonical_page_boundary for page in result["page_candidates"])
    assert result["manifest"].gematria_profile_sha256
    assert result["manifest"].separator_grammar_sha256
