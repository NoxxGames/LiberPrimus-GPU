"""Observed separator inventory generation."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from libreprimus.profiles.separator_grammar import SeparatorGrammar


def _is_rune(char: str) -> bool:
    return "\u16a0" <= char <= "\u16ff"


def observed_separator_inventory(transcript_path: Path, grammar: SeparatorGrammar) -> dict[str, object]:
    text = transcript_path.read_text(encoding="utf-8-sig")
    known = grammar.by_glyph
    observed = Counter()
    unknown = Counter()
    for char in text:
        if _is_rune(char):
            continue
        if char == "\n" or char == "\r":
            observed["physical_newline"] += 1
        elif char in known:
            observed[known[char].token_kind] += 1
        elif char.isdigit():
            observed["numeric_literal"] += 1
        elif char.isspace():
            observed["whitespace"] += 1
        else:
            unknown[char] += 1
    return {
        "record_type": "observed_separator_inventory",
        "source_path": str(transcript_path.as_posix()),
        "known_token_counts": dict(sorted(observed.items())),
        "unknown_symbols": dict(sorted(unknown.items())),
        "unknown_observed_separator_count": sum(unknown.values()),
        "canonical_corpus_active": False,
    }
