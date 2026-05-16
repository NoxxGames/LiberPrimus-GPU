"""Validation for solved-page fixture manifests and generated results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import validate

from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import compute_sha256
from libreprimus.solved_fixtures.fixture_loader import load_fixture_payload, load_fixtures
from libreprimus.solved_fixtures.direct_translation import sha256_text


DEFAULT_PROFILE_PATHS = {
    "gematria_profile_sha256": Path("data/profiles/gematria/gematria-primus-v0.json"),
    "separator_grammar_sha256": Path("data/profiles/separators/rtkd-separator-grammar-v0.json"),
    "glyph_variant_profile_sha256": Path("data/profiles/glyph-variants/glyph-variants-v0.json"),
    "source_transcript_sha256": Path("data/raw/transcripts/rtkd/liber-primus__transcription--master.txt"),
    "solved_reference_sha256": Path("data/raw/transcripts/scream314/liber_primus.md"),
}


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


def _schema_path(name: str) -> Path:
    return repo_root() / "schemas/corpus" / name


def _transform_params(payload: dict[str, Any], method_family: str, transform_name: str | None = None) -> dict[str, Any]:
    expected_name = transform_name or method_family
    for item in payload.get("transform_chain", []):
        if isinstance(item, dict) and item.get("name") == expected_name:
            params = item.get("params", {})
            return dict(params) if isinstance(params, dict) else {}
        if isinstance(item, str) and item == expected_name:
            return {}
    return {}


def validate_fixture_file(path: Path) -> list[str]:
    errors: list[str] = []
    payload = load_fixture_payload(path)
    validate(instance=payload, schema=load_json(_schema_path("solved-page-fixture-v0.schema.json")))
    if payload.get("trusted_as_canonical") is not False:
        errors.append(f"{path.name}: trusted_as_canonical must be false.")
    if payload.get("canonical_corpus_active") is not False:
        errors.append(f"{path.name}: canonical_corpus_active must be false.")
    if payload.get("page_boundaries_final") is not False:
        errors.append(f"{path.name}: page_boundaries_final must be false.")
    for field, relative in DEFAULT_PROFILE_PATHS.items():
        expected_path = repo_root() / relative
        if expected_path.is_file() and payload.get(field) != compute_sha256(expected_path):
            errors.append(f"{path.name}: {field} does not match local file SHA-256.")
    expected = payload.get("expected_normalized_plaintext")
    expected_hash = payload.get("expected_normalized_plaintext_sha256")
    method_family = payload.get("method_family")
    method_status = str(payload.get("method_status", ""))
    if method_family == "rotated_reverse_gematria" and payload.get("in_scope_for_stage"):
        rotation = _transform_params(payload, "rotated_reverse_gematria").get("rotation")
        if not isinstance(rotation, int):
            errors.append(f"{path.name}: rotated_reverse_gematria fixture requires integer params.rotation.")
    if method_family == "reverse_gematria" and payload.get("in_scope_for_stage"):
        if payload.get("direct_translation_expected") is not False:
            errors.append(f"{path.name}: reverse Gematria fixture must not be marked direct_translation_expected.")
    if method_family == "vigenere" and payload.get("in_scope_for_stage"):
        params = _transform_params(payload, "vigenere", "vigenere_explicit_key")
        if not isinstance(params.get("key_text"), str) or not params.get("key_text"):
            errors.append(f"{path.name}: vigenere fixture requires params.key_text.")
        if params.get("direction") != "decrypt_subtract":
            errors.append(f"{path.name}: vigenere fixture requires direction=decrypt_subtract.")
        if not payload.get("method_reference_source_id") or not payload.get("method_reference_sha256"):
            errors.append(f"{path.name}: vigenere fixture requires method-reference provenance.")
    if method_family in {"prime_minus_one_stream", "phi_prime_stream"} and payload.get("in_scope_for_stage"):
        params = _transform_params(payload, "prime_minus_one_stream")
        if not params:
            params = _transform_params(payload, "phi_prime_stream")
        if not isinstance(params.get("prime_start_index"), int):
            errors.append(f"{path.name}: prime stream fixture requires integer params.prime_start_index.")
        if params.get("direction") != "forward":
            errors.append(f"{path.name}: prime stream fixture requires direction=forward.")
        if params.get("stream_value") != "prime_minus_one_mod29":
            errors.append(f"{path.name}: prime stream fixture requires stream_value=prime_minus_one_mod29.")
        if not payload.get("method_reference_source_id") or not payload.get("method_reference_sha256"):
            errors.append(f"{path.name}: prime stream fixture requires method-reference provenance.")
        for check in payload.get("payload_checks", []):
            if not isinstance(check, dict):
                errors.append(f"{path.name}: payload_checks entries must be objects.")
                continue
            expected_payload = check.get("expected_payload_text")
            expected_payload_sha = check.get("expected_payload_sha256")
            if isinstance(expected_payload, str) and expected_payload_sha != sha256_text(expected_payload):
                errors.append(f"{path.name}: payload check {check.get('payload_id')} SHA-256 mismatch.")
    if method_status.startswith("pending"):
        if expected is not None or expected_hash is not None:
            errors.append(f"{path.name}: pending fixture must not contain expected plaintext/hash.")
        if not payload.get("notes"):
            errors.append(f"{path.name}: pending fixture must include notes.")
    elif payload.get("in_scope_for_stage"):
        if not isinstance(expected, str) or not expected:
            errors.append(f"{path.name}: passing-intended fixture requires expected plaintext.")
        if expected_hash != (sha256_text(expected) if isinstance(expected, str) else None):
            errors.append(f"{path.name}: expected plaintext SHA-256 mismatch.")
    return errors


def validate_fixture_dir(fixture_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(fixture_dir.glob("*.fixture.json")):
        errors.extend(validate_fixture_file(path))
    if not load_fixtures(fixture_dir):
        errors.append(f"No fixture files found in {fixture_dir}.")
    return errors


def validate_reproduction_results(results_dir: Path, *, allow_warnings: bool = False) -> list[str]:
    errors: list[str] = []
    summary_path = results_dir / "summary.json"
    records_path = results_dir / "reproduction_records.jsonl"
    if not summary_path.is_file():
        return [f"Missing reproduction summary: {summary_path}"]
    if not records_path.is_file():
        return [f"Missing reproduction records: {records_path}"]
    summary = load_json(summary_path)
    validate(instance=summary, schema=load_json(_schema_path("solved-page-reproduction-summary-v0.schema.json")))
    if summary.get("canonical_corpus_active") is not False:
        errors.append("Reproduction summary canonical_corpus_active must be false.")
    if summary.get("page_boundaries_final") is not False:
        errors.append("Reproduction summary page_boundaries_final must be false.")
    for record in _read_jsonl(records_path):
        validate(instance=record, schema=load_json(_schema_path("solved-page-reproduction-record-v0.schema.json")))
        if record.get("trusted_as_canonical") is not False:
            errors.append(f"{record.get('fixture_id')}: trusted_as_canonical must be false.")
        if record.get("canonical_corpus_active") is not False:
            errors.append(f"{record.get('fixture_id')}: canonical_corpus_active must be false.")
        if record.get("page_boundaries_final") is not False:
            errors.append(f"{record.get('fixture_id')}: page_boundaries_final must be false.")
    if summary.get("warnings") and not allow_warnings:
        errors.append("Reproduction summary has warnings.")
    return errors
