"""Validation helpers for generated corpus candidates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import validate

from libreprimus.paths import repo_root


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def validate_with_schema(record: dict[str, Any], schema_path: Path) -> None:
    validate(instance=record, schema=load_json(schema_path))


def validate_corpus_candidate(candidate_dir: Path, *, allow_warnings: bool = False) -> list[str]:
    errors: list[str] = []
    root = repo_root()
    manifest_path = candidate_dir / "corpus_candidate_manifest.json"
    tokens_path = candidate_dir / "tokens.jsonl"
    lines_path = candidate_dir / "lines.jsonl"
    pages_path = candidate_dir / "page_candidates.jsonl"
    warnings_path = candidate_dir / "warnings.jsonl"
    required = [manifest_path, tokens_path, lines_path, pages_path, warnings_path, candidate_dir / "summary.json"]
    for path in required:
        if not path.is_file():
            errors.append(f"Missing candidate output: {path}")
    if errors:
        return errors
    manifest = load_json(manifest_path)
    schemas = root / "schemas/corpus"
    validate_with_schema(manifest, schemas / "corpus-candidate-manifest-v0.schema.json")
    if manifest.get("canonical_corpus_active") is not False:
        errors.append("Manifest must have canonical_corpus_active=false.")
    if manifest.get("page_boundaries_final") is not False:
        errors.append("Manifest must have page_boundaries_final=false.")
    if manifest.get("trusted_as_canonical") is not False:
        errors.append("Manifest must have trusted_as_canonical=false.")
    for record in _read_jsonl(tokens_path)[:50]:
        validate_with_schema(record, schemas / "corpus-token-record-v0.schema.json")
        if record.get("trusted_as_canonical") is not False:
            errors.append("Token record trusted_as_canonical must be false.")
    for record in _read_jsonl(lines_path)[:50]:
        validate_with_schema(record, schemas / "corpus-line-record-v0.schema.json")
    for record in _read_jsonl(pages_path):
        validate_with_schema(record, schemas / "corpus-page-candidate-record-v0.schema.json")
        if record.get("canonical_page_boundary") is not False:
            errors.append("Page candidate canonical_page_boundary must be false.")
        if record.get("page_boundaries_final") is not False:
            errors.append("Page candidate page_boundaries_final must be false.")
    warning_records = _read_jsonl(warnings_path)
    for record in warning_records[:50]:
        validate_with_schema(record, schemas / "corpus-generation-warning-v0.schema.json")
    if warning_records and not allow_warnings:
        errors.append("Corpus candidate has warnings.")
    return errors
