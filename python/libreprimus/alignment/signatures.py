"""Deterministic line signatures for Stage 0D alignment."""

from __future__ import annotations

import hashlib
import json

from libreprimus.legacy_pastebin.gematria_validation import RUNE_TO_ENTRY
from libreprimus.legacy_pastebin.models import LegacyPastebinLinePair
from libreprimus.transcript_sources.models import TranscriptLineRecord
from libreprimus.alignment.models import LineSignature

DOCUMENTED_VARIANT_MAP = {"ᛂ": "ᛄ"}


def normalize_glyph_sequence(glyphs: list[str] | str) -> str:
    """Return a normalized-view sequence while preserving raw records elsewhere."""
    return "".join(DOCUMENTED_VARIANT_MAP.get(glyph, glyph) for glyph in glyphs)


def decimal_indices_for_glyphs(glyphs: list[str] | str) -> list[int]:
    """Map transcript glyphs to decimal indices using documented normalized view."""
    indices: list[int] = []
    for glyph in glyphs:
        normalized = DOCUMENTED_VARIANT_MAP.get(glyph, glyph)
        entry = RUNE_TO_ENTRY.get(normalized)
        if entry is not None:
            indices.append(entry.decimal_index)
    return indices


def _signature_hash(payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def pastebin_signature(line_pair: LegacyPastebinLinePair) -> LineSignature:
    """Build a deterministic signature for one legacy Pastebin line pair."""
    raw_sequence = "".join(line_pair.rune_words)
    decimal_index_sequence = [
        index
        for word in line_pair.decimal_index_words
        for index in word
        if index is not None
    ]
    payload = {
        "kind": "pastebin_line_pair",
        "pair_index": line_pair.pair_index,
        "raw_rune_sequence": raw_sequence,
        "normalized_rune_sequence": normalize_glyph_sequence(raw_sequence),
        "decimal_index_sequence": decimal_index_sequence,
        "word_length_sequence": [len(word) for word in line_pair.rune_words],
        "rune_count": len(raw_sequence),
        "empty_pair": line_pair.empty_pair,
    }
    return LineSignature(
        signature_kind="pastebin_line_pair",
        source_index=line_pair.pair_index,
        raw_rune_sequence=str(payload["raw_rune_sequence"]),
        normalized_rune_sequence=str(payload["normalized_rune_sequence"]),
        decimal_index_sequence=decimal_index_sequence,
        word_length_sequence=list(payload["word_length_sequence"]),
        rune_count=int(payload["rune_count"]),
        empty_pair=bool(payload["empty_pair"]),
        signature_sha256=_signature_hash(payload),
    )


def transcript_signature(record: TranscriptLineRecord) -> LineSignature:
    """Build a deterministic signature for one transcript line."""
    raw_sequence = "".join(record.rune_glyphs)
    word_lengths = [
        len(part)
        for part in record.raw_text.replace(".", "-").replace("/", "-").split("-")
        if any("\u16A0" <= char <= "\u16FF" for char in part)
    ]
    payload = {
        "kind": "transcript_line",
        "physical_line_number": record.physical_line_number,
        "raw_rune_sequence": raw_sequence,
        "normalized_rune_sequence": normalize_glyph_sequence(raw_sequence),
        "decimal_index_sequence": decimal_indices_for_glyphs(raw_sequence),
        "word_length_sequence": word_lengths,
        "rune_count": len(raw_sequence),
        "empty_pair": len(raw_sequence) == 0,
        "separator_profile": record.separator_counts,
    }
    return LineSignature(
        signature_kind="transcript_line",
        source_index=record.physical_line_number,
        raw_rune_sequence=str(payload["raw_rune_sequence"]),
        normalized_rune_sequence=str(payload["normalized_rune_sequence"]),
        decimal_index_sequence=list(payload["decimal_index_sequence"]),
        word_length_sequence=word_lengths,
        rune_count=int(payload["rune_count"]),
        empty_pair=bool(payload["empty_pair"]),
        signature_sha256=_signature_hash(payload),
    )


def build_signature_index(signatures: list[LineSignature], attr: str) -> dict[object, list[LineSignature]]:
    """Index signatures by a chosen signature attribute."""
    index: dict[object, list[LineSignature]] = {}
    for signature in signatures:
        key = getattr(signature, attr)
        if isinstance(key, list):
            key = tuple(key)
        if key in {"", ()}:
            continue
        index.setdefault(key, []).append(signature)
    return index
