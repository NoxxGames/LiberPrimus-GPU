"""Input stream helpers for CPU batch transforms."""

from __future__ import annotations

import hashlib
import json
from typing import Any

TRANSFORMABLE_TOKEN_KIND = "rune"


def normalize_input_stream(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a normalized stream with deterministic token indexes and counts."""

    stream = dict(payload)
    tokens = [dict(item) for item in stream.get("tokens", [])]
    for index, token in enumerate(tokens):
        token.setdefault("token_index_global", index)
    stream["tokens"] = tokens
    stream["token_count"] = len(tokens)
    stream["transformable_token_count"] = sum(1 for token in tokens if token.get("token_kind") == TRANSFORMABLE_TOKEN_KIND)
    stream.setdefault("canonical_corpus_active", False)
    stream.setdefault("page_boundaries_final", False)
    return stream


def stream_index(streams: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Index streams by ID and reject duplicates."""

    indexed: dict[str, dict[str, Any]] = {}
    for stream in streams:
        normalized = normalize_input_stream(stream)
        stream_id = str(normalized["input_stream_id"])
        if stream_id in indexed:
            raise ValueError(f"duplicate input_stream_id: {stream_id}")
        indexed[stream_id] = normalized
    return indexed


def stable_json_sha256(payload: Any) -> str:
    """Hash JSON data with deterministic key ordering and compact separators."""

    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()
