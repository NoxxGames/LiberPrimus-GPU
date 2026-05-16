from pathlib import Path

from libreprimus.corpus_candidate.validation import load_json, validate_with_schema
from libreprimus.paths import repo_root


def test_corpus_schema_files_exist_and_enforce_false_flags() -> None:
    schema_dir = repo_root() / "schemas/corpus"
    schemas = list(schema_dir.glob("*.schema.json"))

    assert len(schemas) >= 8
    manifest_schema = load_json(schema_dir / "corpus-candidate-manifest-v0.schema.json")
    token_schema = load_json(schema_dir / "corpus-token-record-v0.schema.json")
    page_schema = load_json(schema_dir / "corpus-page-candidate-record-v0.schema.json")

    assert manifest_schema["properties"]["canonical_corpus_active"]["const"] is False
    assert token_schema["properties"]["trusted_as_canonical"]["const"] is False
    assert page_schema["properties"]["page_boundaries_final"]["const"] is False


def test_sample_manifest_validates_against_schema(tmp_path: Path) -> None:
    schema = repo_root() / "schemas/corpus/corpus-candidate-manifest-v0.schema.json"
    record = {
        "record_type": "corpus_candidate_manifest",
        "corpus_candidate_id": "sample",
        "source_transcript_id": "source",
        "source_transcript_sha256": "sha",
        "source_transcript_local_path": "path",
        "gematria_profile_id": "gematria",
        "gematria_profile_sha256": "sha",
        "separator_grammar_id": "separators",
        "separator_grammar_sha256": "sha",
        "glyph_variant_profile_id": "variants",
        "glyph_variant_profile_sha256": "sha",
        "generated_at_utc": "2026-05-16T00:00:00Z",
        "git_commit": "commit",
        "generator_version": "test",
        "canonical_corpus_candidate": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "trusted_as_canonical": False,
        "line_count": 1,
        "token_count": 1,
        "rune_token_count": 1,
        "separator_token_count": 0,
        "unknown_symbol_count": 0,
        "warning_count": 0,
        "page_candidate_count": 0,
        "notes": [],
    }

    validate_with_schema(record, schema)
