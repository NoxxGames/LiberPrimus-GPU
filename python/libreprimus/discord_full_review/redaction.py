"""Privacy-preserving redaction helpers for Stage 4A."""

from __future__ import annotations

from pathlib import Path
import re
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

URL_RE = re.compile(r"https?://[^\s<>'\")\]]+", re.IGNORECASE)
DISCORD_URL_RE = re.compile(
    r"https?://(?:[^/\s<>'\")\]]*\.)?discord(?:app)?\.(?:com|net)/[^\s<>'\")\]]+",
    re.IGNORECASE,
)
MENTION_RE = re.compile(r"<@!?\d+>|@\w[\w.\-]{1,40}")
SNOWFLAKE_RE = re.compile(r"\b\d{17,20}\b")
SAFE_QUERY_KEYS = {"id", "page", "q", "v"}


def redact_text(text: str) -> str:
    """Redact identities and private Discord URLs while preserving research text."""

    redacted = DISCORD_URL_RE.sub(lambda match: redacted_discord_url(match.group(0)), text)
    redacted = MENTION_RE.sub("[redacted-user]", redacted)
    redacted = SNOWFLAKE_RE.sub("[redacted-id]", redacted)
    redacted = re.sub(r"\s+", " ", redacted).strip()
    return redacted


def redacted_discord_url(url: str) -> str:
    try:
        parsed = urlparse(url)
        file_name = Path(parsed.path).name or "discord-asset"
    except ValueError:
        file_name = "discord-asset"
    return f"[redacted-discord-url:{file_name}]"


def sanitize_url(url: str) -> tuple[str | None, str]:
    """Return a public URL if safe and a redacted display URL."""

    raw = url.strip().strip(".,);]")
    try:
        parsed = urlparse(raw)
    except ValueError:
        return None, "[redacted-malformed-url]"
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None, redact_text(raw)
    domain = parsed.netloc.lower()
    if "discord" in domain:
        return None, redacted_discord_url(raw)
    safe_query = urlencode(
        [(key, value) for key, value in parse_qsl(parsed.query, keep_blank_values=False) if key in SAFE_QUERY_KEYS],
        doseq=True,
    )
    safe_url = urlunparse((parsed.scheme, domain, parsed.path, "", safe_query, ""))
    return safe_url, safe_url


def public_links_from_text(text: str) -> list[str]:
    links: list[str] = []
    seen: set[str] = set()
    for match in URL_RE.finditer(text):
        public, _ = sanitize_url(match.group(0))
        if public and public not in seen:
            links.append(public)
            seen.add(public)
    return links


def has_private_discord_url(text: str) -> bool:
    return bool(DISCORD_URL_RE.search(text) or re.search(r"discord(?:app)?\.(?:com|net).*[?&]", text, re.I))
