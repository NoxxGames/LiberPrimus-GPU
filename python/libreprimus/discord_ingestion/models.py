"""Shared constants for Stage 3N Discord ingestion."""

from __future__ import annotations

ARCHIVE_ID = "admin-provided-discord-html-stage3n"
SOURCE_STATUS = "admin_provided_export"

URL_KINDS = {
    "github",
    "fandom",
    "reddit",
    "pastebin",
    "google_docs",
    "internet_archive",
    "discord_attachment",
    "image",
    "audio",
    "pdf",
    "html",
    "unknown",
}

METHOD_KEYWORDS = {
    "vigenere",
    "affine",
    "caesar",
    "atbash",
    "prime",
    "totient",
    "phi",
    "fibonacci",
    "mersenne",
    "cuneiform",
    "base60",
    "base 60",
    "binary",
    "outguess",
    "spectrogram",
    "cookie",
    "hash",
    "rune count",
    "gp sum",
    "gematria",
    "onion",
    "page 56",
    "page 57",
    "p56",
    "p57",
}

FAILURE_KEYWORDS = {
    "false positive",
    "tried",
    "failed",
    "debunked",
    "wrong",
    "bogus",
    "no result",
    "noise",
    "hallucination",
}

SOURCE_KEYWORDS = {
    "github",
    "pastebin",
    "archive",
    "fandom",
    "transcript",
    "rtkd",
    "scream314",
}

KNOWN_NUMBERS = {3301, 1033, 761, 167, 509, 503, 563, 569, 29, 31, 13, 3722101}
