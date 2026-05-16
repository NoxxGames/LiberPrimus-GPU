import json
from pathlib import Path

import pytest

from libreprimus.corpus_candidate.export import write_corpus_candidate_outputs
from libreprimus.corpus_candidate.generator import build_rtkd_corpus_candidate
from libreprimus.corpus_candidate.validation import validate_corpus_candidate
from libreprimus.paths import repo_root


def _profile_paths() -> tuple[Path, Path, Path]:
    root = repo_root()
    return (
        root / "data/profiles/gematria/gematria-primus-v0.json",
        root / "data/profiles/glyph-variants/glyph-variants-v0.json",
        root / "data/profiles/separators/rtkd-separator-grammar-v0.json",
    )


def test_synthetic_corpus_candidate_generation_is_deterministic(tmp_path: Path) -> None:
    transcript = tmp_path / "rtkd.txt"
    transcript.write_text("%\n\u16a0-\u16c2/\n", encoding="utf-8")
    gematria, variants, separators = _profile_paths()

    result1 = build_rtkd_corpus_candidate(
        transcript_path=transcript,
        gematria_path=gematria,
        glyph_variants_path=variants,
        separators_path=separators,
        alignment_dir=tmp_path / "missing-alignment",
    )
    result2 = build_rtkd_corpus_candidate(
        transcript_path=transcript,
        gematria_path=gematria,
        glyph_variants_path=variants,
        separators_path=separators,
        alignment_dir=tmp_path / "missing-alignment",
    )

    assert [token.raw_text for token in result1["tokens"]] == [token.raw_text for token in result2["tokens"]]
    assert result1["summary"].token_count == result2["summary"].token_count
    assert result1["summary"].variant_mapped_token_count == 1
    assert result1["summary"].canonical_corpus_active is False
    assert result1["warnings"]


def test_generated_candidate_outputs_validate(tmp_path: Path) -> None:
    transcript = tmp_path / "rtkd.txt"
    transcript.write_text("\u16a0/\n", encoding="utf-8")
    gematria, variants, separators = _profile_paths()
    result = build_rtkd_corpus_candidate(
        transcript_path=transcript,
        gematria_path=gematria,
        glyph_variants_path=variants,
        separators_path=separators,
        alignment_dir=tmp_path / "missing-alignment",
    )
    out_dir = tmp_path / "candidate"
    write_corpus_candidate_outputs(out_dir, result)

    assert validate_corpus_candidate(out_dir, allow_warnings=True) == []


def test_candidate_generation_refuses_invalid_profile(tmp_path: Path) -> None:
    transcript = tmp_path / "rtkd.txt"
    transcript.write_text("\u16a0/\n", encoding="utf-8")
    gematria, variants, separators = _profile_paths()
    invalid = tmp_path / "invalid-gematria.json"
    payload = json.loads(gematria.read_text(encoding="utf-8"))
    payload["entries"] = payload["entries"][:-1]
    invalid.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        build_rtkd_corpus_candidate(
            transcript_path=transcript,
            gematria_path=invalid,
            glyph_variants_path=variants,
            separators_path=separators,
            alignment_dir=tmp_path / "missing-alignment",
        )
