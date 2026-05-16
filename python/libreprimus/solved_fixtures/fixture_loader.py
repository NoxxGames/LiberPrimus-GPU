"""Load solved-page fixture manifests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.solved_fixtures.models import SolvedPageFixture, SpanSelector


def load_fixture(path: Path) -> SolvedPageFixture:
    payload = json.loads(path.read_text(encoding="utf-8"))
    selector_payload = payload["span_selector"]
    selector = SpanSelector(
        selector_kind=str(selector_payload["selector_kind"]),
        source=str(selector_payload["source"]),
        start_logical_line_index=selector_payload.get("start_logical_line_index"),
        end_logical_line_index=selector_payload.get("end_logical_line_index"),
        start_token_index=selector_payload.get("start_token_index"),
        end_token_index=selector_payload.get("end_token_index"),
        page_candidate_ids=[str(item) for item in selector_payload.get("page_candidate_ids", [])],
        notes=str(selector_payload.get("notes", "")),
    )
    return SolvedPageFixture(
        record_type=str(payload["record_type"]),
        fixture_id=str(payload["fixture_id"]),
        fixture_version=str(payload["fixture_version"]),
        solved_section_title=str(payload["solved_section_title"]),
        solved_section_aliases=[str(item) for item in payload.get("solved_section_aliases", [])],
        method_family=str(payload["method_family"]),
        method_status=str(payload["method_status"]),
        transform_chain=list(payload.get("transform_chain", [])),
        direct_translation_expected=bool(payload["direct_translation_expected"]),
        in_scope_for_stage=bool(payload["in_scope_for_stage"]),
        source_transcript_id=str(payload["source_transcript_id"]),
        source_transcript_sha256=str(payload["source_transcript_sha256"]),
        solved_reference_source_id=str(payload["solved_reference_source_id"]),
        solved_reference_sha256=str(payload["solved_reference_sha256"]),
        gematria_profile_id=str(payload["gematria_profile_id"]),
        gematria_profile_sha256=str(payload["gematria_profile_sha256"]),
        separator_grammar_id=str(payload["separator_grammar_id"]),
        separator_grammar_sha256=str(payload["separator_grammar_sha256"]),
        glyph_variant_profile_id=str(payload["glyph_variant_profile_id"]),
        glyph_variant_profile_sha256=str(payload["glyph_variant_profile_sha256"]),
        corpus_candidate_id=str(payload["corpus_candidate_id"]),
        corpus_candidate_status=str(payload["corpus_candidate_status"]),
        span_selector=selector,
        span_status=str(payload["span_status"]),
        expected_normalized_plaintext=payload.get("expected_normalized_plaintext"),
        expected_normalized_plaintext_sha256=payload.get("expected_normalized_plaintext_sha256"),
        expected_rune_count=payload.get("expected_rune_count"),
        expected_numeric_literal_count=payload.get("expected_numeric_literal_count"),
        expected_separator_policy=str(payload["expected_separator_policy"]),
        expected_known_caveats=[str(item) for item in payload.get("expected_known_caveats", [])],
        payload_checks=[dict(item) for item in payload.get("payload_checks", []) if isinstance(item, dict)],
        trusted_as_canonical=bool(payload["trusted_as_canonical"]),
        canonical_corpus_active=bool(payload["canonical_corpus_active"]),
        page_boundaries_final=bool(payload["page_boundaries_final"]),
        notes=[str(item) for item in payload.get("notes", [])],
    )


def load_fixture_payload(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_fixtures(fixture_dir: Path) -> list[SolvedPageFixture]:
    return [load_fixture(path) for path in sorted(fixture_dir.glob("*.fixture.json"))]
