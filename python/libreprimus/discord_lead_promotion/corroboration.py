"""Corroboration helpers for Stage 3R lead promotion."""

from __future__ import annotations

from urllib.parse import urlparse, urlunparse

PRIVATE_DOMAINS = {
    "cdn.discordapp.com",
    "media.discordapp.net",
    "discord.com",
    "discordapp.com",
}


def normalized_public_url(url: str) -> str | None:
    """Return a public-safe normalized URL or ``None`` for private/unsafe links."""
    stripped = url.strip()
    if not stripped:
        return None
    parsed = urlparse(stripped)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    domain = parsed.netloc.lower()
    if any(domain == private or domain.endswith(f".{private}") for private in PRIVATE_DOMAINS):
        return None
    query = ""
    if domain.endswith("github.com") or domain.endswith("raw.githubusercontent.com"):
        query = parsed.query
    path = parsed.path.rstrip("/") or parsed.path
    return urlunparse((parsed.scheme.lower(), domain, path, "", query, ""))


def is_private_or_unsafe_url(url: str) -> bool:
    return normalized_public_url(url) is None


def classify_lead(*, url: str | None, has_public_source: bool, speculative: bool = False) -> str:
    """Classify a Discord-derived lead under the Stage 3R promotion policy."""
    if url and is_private_or_unsafe_url(url):
        return "unsafe_or_private"
    if speculative and not has_public_source:
        return "too_speculative"
    if has_public_source:
        return "source_to_lock"
    return "ignore_for_now"
