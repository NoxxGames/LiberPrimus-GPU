"""Synthetic Stage 2F input helpers."""

from __future__ import annotations

from typing import Any


def synthetic_tokens(record: dict[str, Any]) -> list[dict[str, Any]]:
    if record.get("record_type") != "synthetic_corpus_record":
        raise ValueError("Synthetic execution requires a synthetic_corpus_record.")
    if record.get("safe_for_execution") is not True:
        raise ValueError("Synthetic record is not marked safe_for_execution=true.")
    if record.get("contains_liber_primus_unsolved_text") is not False:
        raise ValueError("Synthetic record contains unsolved Liber Primus text.")
    tokens = record.get("token_records", [])
    if not isinstance(tokens, list) or not tokens:
        raise ValueError("Synthetic record requires token_records.")
    return [dict(token) for token in tokens if isinstance(token, dict)]


def expected_plaintext_sha256(record: dict[str, Any]) -> str | None:
    value = record.get("expected_plaintext_sha256")
    return str(value) if isinstance(value, str) and value else None

