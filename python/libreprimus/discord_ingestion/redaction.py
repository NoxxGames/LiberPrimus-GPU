"""Redaction helpers for Discord archive ingestion."""

from __future__ import annotations

import html
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

DISCORD_ATTACHMENT_DOMAINS = {
    "cdn.discordapp.com",
    "media.discordapp.net",
    "cdn.discordapp.net",
    "discord.com",
    "discordapp.com",
    "discord.gg",
}

TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def normalize_url(url: str) -> str:
    """Normalize a URL while redacting private Discord attachment query strings."""
    cleaned = html.unescape(url.strip().strip("\"'<>),.;"))
    try:
        parsed = urlparse(cleaned)
    except ValueError:
        return cleaned
    if not parsed.scheme and parsed.netloc:
        parsed = parsed._replace(scheme="https")
    if parsed.scheme not in {"http", "https"}:
        return cleaned
    domain = parsed.netloc.lower()
    if _is_discord_attachment_domain(domain):
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
    query_pairs = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in TRACKING_KEYS
    ]
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", urlencode(query_pairs), ""))


def redacted_url_for_record(url: str) -> str:
    """Return a URL safe for generated review records."""
    normalized = normalize_url(url)
    try:
        parsed = urlparse(normalized)
    except ValueError:
        return normalized
    if _is_discord_attachment_domain(parsed.netloc.lower()):
        return normalized
    return normalized


def redacted_summary(keywords: list[str], *, prefix: str) -> str:
    """Build a summary that contains only keyword classes, not message text."""
    return f"{prefix}: {', '.join(sorted(set(keywords))) if keywords else 'unknown'}"


def _is_discord_attachment_domain(domain: str) -> bool:
    return any(domain == item or domain.endswith(f".{item}") for item in DISCORD_ATTACHMENT_DOMAINS)
