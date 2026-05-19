"""Shared constants for Stage 4A Discord full-review bundles."""

from __future__ import annotations

from pathlib import Path

DEFAULT_DISCORD_DIR = Path("third_party/LiberPrimusDiscordChats")
DEFAULT_LP_PAGES_DIR = Path("third_party/LiberPrimusPages")
DEFAULT_OUTPUT_DIR = Path("experiments/results/discord-full-review/stage4a")
DEFAULT_PRIVACY_MODE = "redacted_public"

HTML_SUFFIXES = {".html", ".htm"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

TOPIC_DEFINITIONS: dict[str, tuple[str, ...]] = {
    "cuneiform-base60": ("cuneiform", "base60", "base 60", "babylonian", "sexagesimal"),
    "page-art-dots-binary-braille-stars": (
        "dot",
        "dots",
        "binary",
        "braille",
        "star",
        "stars",
        "page art",
        "constellation",
    ),
    "onion7-number-squares": ("onion7", "onion 7", "number square", "number squares", "4x4", "table"),
    "deep-web-hash-cookies": ("deep web hash", "cookie", "hash", "sha-256", "sha256", "761", "167"),
    "outguess-stego-audio": ("outguess", "stego", "steganography", "spectrogram", "audio", "mp3"),
    "gp-sums-rune-counts": ("gp sum", "gematria", "rune count", "rune counts", "mod29", "mod 29"),
    "solved-method-history": ("solved", "known solved", "method history", "atbash", "vigenere"),
    "debunks-false-positives": ("debunk", "false positive", "wrong", "bogus", "failed", "no result"),
    "source-links-tools-datasets": ("github", "tool", "dataset", "archive", "source", "wiki", "transcript"),
    "literature-keys": ("literature", "book", "poem", "key phrase", "william blake", "holy"),
    "geometry-symmetry": ("geometry", "symmetry", "spiral", "mobius", "moebius", "rotation"),
    "open-questions-strong-leads": ("open question", "strong lead", "maybe", "unknown", "hypothesis"),
}

METHOD_KEYWORDS = {
    "affine",
    "atbash",
    "caesar",
    "vigenere",
    "prime",
    "totient",
    "phi",
    "mersenne",
    "outguess",
    "stego",
    "hash",
    "sha256",
    "sha-256",
    "gematria",
    "gp",
    "rune",
    "onion7",
    "base60",
}

VISUAL_KEYWORDS = {
    "image",
    "jpg",
    "jpeg",
    "png",
    "art",
    "visual",
    "dot",
    "dots",
    "binary",
    "braille",
    "star",
    "cuneiform",
    "glyph",
}

DEBUNK_KEYWORDS = {"debunk", "false positive", "wrong", "bogus", "failed", "no result", "hallucination"}

SHARD_TARGET_MESSAGES = 400
SHARD_TARGET_MARKDOWN_BYTES = 180_000
