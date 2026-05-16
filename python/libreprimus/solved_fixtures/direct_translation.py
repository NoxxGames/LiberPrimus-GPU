"""Direct Gematria-profile transliteration for solved fixtures."""

from __future__ import annotations

import hashlib
import re
from typing import Any


def normalize_plaintext(parts: list[str]) -> str:
    text = "".join(parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\. *", ". ", text)
    return text.strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def decode_direct_translation(tokens: list[dict[str, Any]]) -> dict[str, Any]:
    parts: list[str] = []
    warnings: list[str] = []
    rune_count = 0
    numeric_literal_count = 0
    separator_count = 0
    for token in tokens:
        kind = str(token.get("token_kind"))
        if kind == "rune":
            label = token.get("latin_label")
            if label is None:
                warnings.append(f"Rune token without Latin label at token {token.get('token_index_global')}.")
                raw = token.get("raw_glyph") or token.get("raw_text") or ""
                parts.append(str(raw))
            else:
                parts.append(str(label).upper())
            rune_count += 1
            continue
        if kind == "word_separator":
            parts.append(" ")
            separator_count += 1
            continue
        if kind == "clause_separator":
            parts.append(". ")
            separator_count += 1
            continue
        if kind in {"line_separator", "physical_newline"}:
            separator_count += 1
            continue
        if kind in {"paragraph_separator", "segment_separator", "chapter_separator", "page_separator_or_marker", "whitespace"}:
            parts.append(" ")
            separator_count += 1
            continue
        if kind == "numeric_literal":
            parts.append(str(token.get("raw_text", "")))
            numeric_literal_count += 1
            continue
        if kind == "unknown_symbol":
            raw = str(token.get("raw_text", ""))
            parts.append(raw)
            warnings.append(f"Unknown symbol preserved in direct translation: {raw!r}.")
            continue
    plaintext = normalize_plaintext(parts)
    return {
        "decoded_normalized_plaintext": plaintext,
        "decoded_normalized_plaintext_sha256": sha256_text(plaintext),
        "rune_count": rune_count,
        "numeric_literal_count": numeric_literal_count,
        "separator_count": separator_count,
        "warnings": warnings,
    }
