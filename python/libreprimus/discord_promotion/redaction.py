"""Redaction helpers for promoted Stage 3O public records."""

from __future__ import annotations

from urllib.parse import urlparse, urlunparse

from libreprimus.discord_promotion.models import DISCORD_DOMAINS

PRIVATE_QUERY_KEYS = {"token", "ex", "is", "hm", "signature", "auth", "key", "expires"}


def safe_public_url(url: str) -> str | None:
    """Return a public-safe URL or None when the URL should not be promoted."""
    try:
        parsed = urlparse(url.strip())
    except ValueError:
        return None
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    domain = parsed.netloc.lower()
    if is_discord_domain(domain):
        return None
    if any(marker in parsed.query.lower() for marker in PRIVATE_QUERY_KEYS):
        return None
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))


def is_discord_domain(domain: str) -> bool:
    return any(domain == item or domain.endswith(f".{item}") for item in DISCORD_DOMAINS)
