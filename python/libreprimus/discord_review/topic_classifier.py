"""Keyword/domain topic classification for Stage 3Q review leads."""

from __future__ import annotations

from urllib.parse import urlparse

from libreprimus.discord_review.models import TOPICS


def classify_topic(
    *,
    text: str = "",
    method_keywords: list[str] | None = None,
    numeric_values: list[int] | None = None,
    public_links: list[str] | None = None,
    source_channel: str = "",
) -> str:
    haystack = " ".join(
        [
            text.lower(),
            " ".join(keyword.lower() for keyword in method_keywords or []),
            " ".join(str(number) for number in numeric_values or []),
            " ".join(public_links or []).lower(),
            source_channel.lower(),
        ]
    )
    domains = {urlparse(link).netloc.lower() for link in public_links or []}
    if _has(haystack, "false positive", "debunk", "bogus", "wrong", "failed", "no result", "hallucination"):
        return "claimed-decodes-false-positives-debunks"
    if domains & {"github.com", "raw.githubusercontent.com"} or _has(haystack, "tool", "repository", "repo", "code"):
        return "tools-code-and-repositories"
    if domains or _has(haystack, "archive", "dataset", "fandom", "wiki", "pastebin", "transcript", "source"):
        return "source-links-and-datasets"
    if _has(haystack, "cuneiform", "base60", "base 60", "babylonian"):
        return "cuneiform-base60-and-babylonian"
    if _has(haystack, "dot", "dots", "binary", "braille", "star", "stars", "page-art-dots"):
        return "page-art-dots-binary-braille-stars"
    if _has(haystack, "number square", "number squares", "onion7", "onion 7", "4x4", "table"):
        return "number-squares-and-onion7"
    if _has(haystack, "hash", "cookie", "the-deep-web-hash", "761", "167"):
        return "deep-web-hash-and-cookies"
    if _has(haystack, "prime", "totient", "phi", "mersenne", "fibonacci", "stream"):
        return "prime-streams-totients-and-number-theory"
    if _has(haystack, "vigenere", "key", "literature", "book", "poem"):
        return "vigenere-keys-and-literature"
    if _has(haystack, "gematria", "gp sum", "rune count", "runes"):
        return "gematria-gp-sums-and-rune-counts"
    if _has(haystack, "image", "artwork", "symbol", "tree", "mayfly", "spiral", "mobius", "visual"):
        return "image-artwork-symbols-and-visual-clues"
    if _has(haystack, "outguess", "stego", "spectrogram", "audio", "mp3"):
        return "outguess-stego-audio-spectrograms"
    if _has(haystack, "solved", "known solved", "method history", "decrypt", "decode"):
        return "solved-pages-and-method-history"
    if _has(haystack, "open question", "strong lead", "unknown", "maybe"):
        return "open-questions-and-strong-leads"
    if any(str(number) in haystack for number in (3301, 1033, 761, 167, 509, 503, 563, 569, 3722101)):
        return "open-questions-and-strong-leads"
    return TOPICS[-1]


def _has(text: str, *needles: str) -> bool:
    return any(needle in text for needle in needles)
