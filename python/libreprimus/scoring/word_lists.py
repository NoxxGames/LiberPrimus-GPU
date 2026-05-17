"""Tiny committed word-list loader for deterministic local triage."""

from __future__ import annotations

from pathlib import Path

from libreprimus.paths import repo_root

DEFAULT_TINY_WORD_LIST = Path("data/scoring/english-common-words-tiny-v0.txt")
DEFAULT_TINY_IMPOSSIBLE_BIGRAMS = Path("data/scoring/english-impossible-bigrams-tiny-v0.txt")


def load_tiny_common_words(path: Path | None = None) -> list[str]:
    resolved = repo_root() / (path or DEFAULT_TINY_WORD_LIST)
    words = []
    for line in resolved.read_text(encoding="utf-8").splitlines():
        stripped = line.strip().upper()
        if stripped and not stripped.startswith("#"):
            words.append(stripped)
    return words


def load_tiny_impossible_bigrams(path: Path | None = None) -> list[str]:
    resolved = repo_root() / (path or DEFAULT_TINY_IMPOSSIBLE_BIGRAMS)
    if not resolved.is_file():
        return []
    bigrams = []
    for line in resolved.read_text(encoding="utf-8").splitlines():
        stripped = line.strip().upper()
        if stripped and not stripped.startswith("#"):
            bigrams.append(stripped)
    return bigrams
