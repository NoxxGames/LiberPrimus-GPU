"""Solved-fixture-safe input stream helpers for Stage 4O CPU batches."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
from typing import Any

from libreprimus.bounded_execution.caesar_affine import labels_by_index
from libreprimus.cpu_batch.input_streams import stable_json_sha256
from libreprimus.cpu_batch.manifest_loader import load_manifest
from libreprimus.history.source_records import resolve_repo_path
from libreprimus.solved_fixtures.fixture_loader import load_fixture_payload

RUNE_LABELS_BY_INDEX = labels_by_index()
INDEX_BY_RUNE_LABEL = {label: index for index, label in RUNE_LABELS_BY_INDEX.items()}
_TOKEN_LABELS = sorted(INDEX_BY_RUNE_LABEL, key=len, reverse=True)


def solved_fixture_stream_records_from_manifest(manifest_path: Path) -> list[dict[str, Any]]:
    """Return metadata records for solved-fixture input streams in one manifest."""

    manifest = load_manifest(manifest_path)
    return [
        solved_fixture_stream_record(stream)
        for stream in manifest.input_streams
        if stream.get("source_kind") == "solved_fixture"
    ]


def solved_fixture_stream_record(stream: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic stream record for committed fixture-safe parity."""

    tokens = [dict(item) for item in stream.get("tokens", [])]
    line_indexes = {
        int(token["logical_line_index"])
        for token in tokens
        if isinstance(token.get("logical_line_index"), int)
    }
    return {
        "record_type": "cpu_batch_solved_fixture_stream",
        "input_stream_id": str(stream["input_stream_id"]),
        "fixture_id": str(stream.get("fixture_id", "synthetic-fixture-safe")),
        "source_type": "committed_solved_fixture",
        "token_count": len(tokens),
        "transformable_token_count": sum(1 for token in tokens if token.get("token_kind") == "rune"),
        "separator_count": sum(1 for token in tokens if str(token.get("token_kind", "")).endswith("separator")),
        "line_count": len(line_indexes) if line_indexes else 1 if tokens else 0,
        "input_token_stream_hash": stable_json_sha256(tokens),
        "cpu_only": True,
        "cuda_used": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
    }


def skipped_missing_fixture_stream_record(fixture_path: Path, *, stream_id: str) -> dict[str, Any]:
    """Return an explicit skipped fixture-stream record for unavailable fixture material."""

    resolved = resolve_repo_path(fixture_path)
    return {
        "record_type": "cpu_batch_solved_fixture_stream",
        "input_stream_id": stream_id,
        "fixture_id": resolved.stem,
        "source_type": "skipped_missing_fixture",
        "token_count": 0,
        "transformable_token_count": 0,
        "separator_count": 0,
        "line_count": 0,
        "input_token_stream_hash": hashlib.sha256(str(resolved).encode("utf-8")).hexdigest(),
        "skip_reason": "fixture file unavailable or raw-dependent; no stream was generated",
        "cpu_only": True,
        "cuda_used": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
    }


def tokens_from_fixture_expected_plaintext(fixture_path: Path) -> list[dict[str, Any]]:
    """Build a deterministic token stream from a committed fixture's expected plaintext."""

    payload = load_fixture_payload(resolve_repo_path(fixture_path))
    plaintext = str(payload.get("expected_normalized_plaintext") or "")
    if not plaintext:
        raise ValueError(f"fixture has no expected_normalized_plaintext: {fixture_path}")
    return tokens_from_normalized_plaintext(plaintext)


def tokens_from_normalized_plaintext(plaintext: str) -> list[dict[str, Any]]:
    """Tokenise expected fixture plaintext into Gematria labels without reading raw corpus data."""

    tokens: list[dict[str, Any]] = []
    logical_line = 0
    cursor = 0
    text = plaintext.upper()
    while cursor < len(text):
        char = text[cursor]
        if char.isspace():
            _append_separator(tokens, "word_separator", " ", logical_line)
            cursor += 1
            continue
        if char in ".!?":
            _append_separator(tokens, "clause_separator", char, logical_line)
            cursor += 1
            continue
        if not re.match(r"[A-Z]", char):
            cursor += 1
            continue
        for label in _TOKEN_LABELS:
            if text.startswith(label, cursor):
                tokens.append(
                    {
                        "token_kind": "rune",
                        "index29": INDEX_BY_RUNE_LABEL[label],
                        "latin_label": label,
                        "token_index_global": len(tokens),
                        "logical_line_index": logical_line,
                    }
                )
                cursor += len(label)
                break
        else:
            tokens.append(
                {
                    "token_kind": "unknown_symbol",
                    "raw_text": char,
                    "token_index_global": len(tokens),
                    "logical_line_index": logical_line,
                }
            )
            cursor += 1
    return tokens


def encode_expected_plaintext_tokens(tokens: list[dict[str, Any]], *, transform_id: str, parameters: dict[str, Any]) -> list[dict[str, Any]]:
    """Encode plaintext-like tokens into cipher-side input tokens for parity fixtures."""

    encoded: list[dict[str, Any]] = []
    rune_position = 0
    key_indices = _key_indices(parameters.get("key_text")) if transform_id == "vigenere_explicit_key" else []
    prime_stream = [1, 2, 4, 6, 10, 12, 16, 18, 22, 28, 0, 2, 4, 12, 18, 28]
    for token in tokens:
        item = dict(token)
        if item.get("token_kind") == "rune":
            plain_index = int(item["index29"])
            if transform_id == "direct_translation":
                cipher_index = plain_index
            elif transform_id == "reverse_gematria":
                cipher_index = 28 - plain_index
            elif transform_id == "rotated_reverse_gematria":
                cipher_index = (28 + int(parameters["rotation"]) - plain_index) % 29
            elif transform_id == "vigenere_explicit_key":
                cipher_index = (plain_index + key_indices[rune_position % len(key_indices)]) % 29
            elif transform_id in {"prime_minus_one_stream", "phi_prime_stream"}:
                cipher_index = (plain_index + prime_stream[rune_position % len(prime_stream)]) % 29
            else:
                raise ValueError(f"unsupported fixture encoder: {transform_id}")
            item["index29"] = cipher_index
            item["latin_label"] = RUNE_LABELS_BY_INDEX[cipher_index]
            rune_position += 1
        encoded.append(item)
    return encoded


def _append_separator(tokens: list[dict[str, Any]], kind: str, raw_text: str, logical_line: int) -> None:
    if tokens and tokens[-1].get("token_kind") == kind:
        return
    tokens.append(
        {
            "token_kind": kind,
            "raw_text": raw_text,
            "token_index_global": len(tokens),
            "logical_line_index": logical_line,
        }
    )


def _key_indices(key_text: Any) -> list[int]:
    key = str(key_text or "").upper()
    tokens = [token for token in tokens_from_normalized_plaintext(key) if token.get("token_kind") == "rune"]
    if not tokens:
        raise ValueError("vigenere fixture encoder requires a non-empty key_text")
    return [int(token["index29"]) for token in tokens]
