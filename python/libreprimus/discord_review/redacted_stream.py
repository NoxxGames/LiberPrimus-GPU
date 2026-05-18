"""Redaction and redacted-stream construction for Discord review bundles."""

from __future__ import annotations

from datetime import UTC, datetime
import hashlib
import re
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from libreprimus.discord_review import ARCHIVE_ID
from libreprimus.discord_review.export import iter_jsonl
from libreprimus.discord_review.models import REDACTED_STREAM_LIMITS

URL_PATTERN = re.compile(r"https?://[^\s<>'\")]+", re.IGNORECASE)
DISCORD_CDN_PATTERN = re.compile(
    r"https?://(?:cdn|media)\.discord(?:app)?\.(?:com|net)/attachments/[^\s<>'\")]+",
    re.IGNORECASE,
)
MENTION_PATTERN = re.compile(r"<@!?\d+>")
SNOWFLAKE_PATTERN = re.compile(r"\b\d{17,20}\b")
AVATAR_PATTERN = re.compile(r"https?://(?:cdn|media)\.discord(?:app)?\.(?:com|net)/avatars/[^\s<>'\")]+", re.IGNORECASE)

SAFE_QUERY_KEYS = {"id", "page", "q", "v"}


def redact_text(text: str) -> str:
    """Return compact research text with identities and private Discord URLs removed."""
    redacted = AVATAR_PATTERN.sub("[redacted-avatar-url]", text)
    redacted = DISCORD_CDN_PATTERN.sub(lambda match: _redacted_attachment(match.group(0)), redacted)
    redacted = MENTION_PATTERN.sub("[redacted-user]", redacted)
    redacted = SNOWFLAKE_PATTERN.sub("[redacted-id]", redacted)
    redacted = re.sub(r"\s+", " ", redacted).strip()
    return redacted[:2000]


def sanitize_public_url(url: str) -> str | None:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    domain = parsed.netloc.lower()
    if "discord" in domain:
        return None
    safe_query = urlencode(
        [(key, value) for key, value in parse_qsl(parsed.query, keep_blank_values=False) if key in SAFE_QUERY_KEYS],
        doseq=True,
    )
    return urlunparse((parsed.scheme, domain, parsed.path, "", safe_query, ""))


def public_links_from_text(text: str) -> list[str]:
    links: list[str] = []
    seen: set[str] = set()
    for match in URL_PATTERN.finditer(text):
        safe_url = sanitize_public_url(match.group(0))
        if safe_url and safe_url not in seen:
            links.append(safe_url)
            seen.add(safe_url)
    return links


def build_redacted_stream(ingestion_dir: Path, *, generated_at: str | None = None) -> list[dict[str, Any]]:
    """Build a bounded redacted stream from Stage 3N generated records."""
    timestamp = generated_at or _utc_now()
    records: list[dict[str, Any]] = []
    records.extend(
        _stream_links(ingestion_dir / "discord_extracted_links.jsonl", REDACTED_STREAM_LIMITS["links"], timestamp)
    )
    records.extend(
        _stream_methods(
            ingestion_dir / "discord_method_claim_candidates.jsonl",
            REDACTED_STREAM_LIMITS["methods"],
            timestamp,
        )
    )
    records.extend(
        _stream_numerics(
            ingestion_dir / "discord_numeric_observation_candidates.jsonl",
            REDACTED_STREAM_LIMITS["numerics"],
            timestamp,
        )
    )
    records.extend(
        _stream_attachments(
            ingestion_dir / "discord_attachment_candidates.jsonl",
            REDACTED_STREAM_LIMITS["attachments"],
            timestamp,
        )
    )
    return records


def _stream_links(path: Path, limit: int, timestamp: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for ordinal, record in enumerate(iter_jsonl(path) or [], start=1):
        safe_url = sanitize_public_url(str(record.get("normalized_url") or record.get("url") or ""))
        if not safe_url:
            continue
        output.append(
            _record(
                source_file_sha256=str(record.get("source_file_sha256", "")),
                source_channel="stage3n-link-extraction",
                approximate_timestamp=timestamp,
                text=f"public source link: {safe_url} domain={record.get('domain', '')} kind={record.get('url_kind', '')}",
                public_links=[safe_url],
                method_keywords=[],
                numeric_values=[],
                visual_keywords=[],
                attachment_filenames=[],
                ordinal=ordinal,
            )
        )
        if len(output) >= limit:
            break
    return output


def _stream_methods(path: Path, limit: int, timestamp: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for ordinal, record in enumerate(iter_jsonl(path) or [], start=1):
        keywords = [str(keyword) for keyword in record.get("extracted_keywords", [])]
        text = str(record.get("redacted_summary") or f"method keyword cluster: {'/'.join(keywords)}")
        output.append(
            _record(
                source_file_sha256=str(record.get("source_file_sha256", "")),
                source_channel="stage3n-method-claim-extraction",
                approximate_timestamp=timestamp,
                text=text,
                public_links=public_links_from_text(text),
                method_keywords=keywords,
                numeric_values=_numbers_from_record(record),
                visual_keywords=_visual_keywords(keywords),
                attachment_filenames=[],
                ordinal=ordinal,
            )
        )
        if len(output) >= limit:
            break
    return output


def _stream_numerics(path: Path, limit: int, timestamp: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for ordinal, record in enumerate(iter_jsonl(path) or [], start=1):
        numbers = _numbers_from_record(record)
        keywords = [str(keyword) for keyword in record.get("context_keywords", [])]
        text = str(record.get("redacted_summary") or f"numeric observation: {numbers}")
        output.append(
            _record(
                source_file_sha256=str(record.get("source_file_sha256", "")),
                source_channel="stage3n-numeric-extraction",
                approximate_timestamp=timestamp,
                text=text,
                public_links=public_links_from_text(text),
                method_keywords=keywords,
                numeric_values=numbers,
                visual_keywords=_visual_keywords(keywords),
                attachment_filenames=[],
                ordinal=ordinal,
            )
        )
        if len(output) >= limit:
            break
    return output


def _stream_attachments(path: Path, limit: int, timestamp: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for ordinal, record in enumerate(iter_jsonl(path) or [], start=1):
        file_name = str(record.get("file_name") or record.get("extension") or "attachment")
        text = f"attachment reference: [redacted-discord-attachment:{file_name}] kind={record.get('media_kind', '')}"
        output.append(
            _record(
                source_file_sha256=str(record.get("source_file_sha256", "")),
                source_channel="stage3n-attachment-extraction",
                approximate_timestamp=timestamp,
                text=text,
                public_links=[],
                method_keywords=[],
                numeric_values=[],
                visual_keywords=[],
                attachment_filenames=[file_name],
                ordinal=ordinal,
            )
        )
        if len(output) >= limit:
            break
    return output


def _record(
    *,
    source_file_sha256: str,
    source_channel: str,
    approximate_timestamp: str,
    text: str,
    public_links: list[str],
    attachment_filenames: list[str],
    method_keywords: list[str],
    numeric_values: list[int],
    visual_keywords: list[str],
    ordinal: int,
) -> dict[str, Any]:
    source_hash = source_file_sha256 if re.fullmatch(r"[0-9a-fA-F]{64}", source_file_sha256) else _hash_text(source_channel)
    redacted = redact_text(text)
    record_key = f"{source_hash}:{source_channel}:{ordinal}:{redacted}"
    return {
        "record_type": "discord_redacted_message_record",
        "record_id": f"stage3q-redacted-{hashlib.sha256(record_key.encode('utf-8')).hexdigest()[:24]}",
        "archive_id": ARCHIVE_ID,
        "source_file_sha256": source_hash.lower(),
        "source_channel": source_channel,
        "approximate_timestamp": approximate_timestamp,
        "redaction_level": "summary",
        "redacted_text": redacted,
        "public_links": public_links,
        "attachment_filenames": attachment_filenames,
        "method_keywords": sorted(set(method_keywords)),
        "numeric_values": sorted(set(numeric_values)),
        "visual_keywords": sorted(set(visual_keywords)),
        "raw_message_committed": False,
        "username_committed": False,
        "user_id_committed": False,
        "message_id_committed": False,
        "private_url_committed": False,
        "solve_claim": False,
        "notes": "Generated redacted review stream entry; not committed as source evidence.",
    }


def _redacted_attachment(url: str) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path).name or Path(parsed.path).suffix or "attachment"
    return f"[redacted-discord-attachment:{name}]"


def _numbers_from_record(record: dict[str, Any]) -> list[int]:
    numbers: list[int] = []
    for value in record.get("numbers", []):
        try:
            numbers.append(int(value))
        except (TypeError, ValueError):
            continue
    return numbers


def _visual_keywords(keywords: list[str]) -> list[str]:
    visual_set = {
        "cuneiform",
        "base60",
        "base 60",
        "binary",
        "braille",
        "dot",
        "dots",
        "artwork",
        "image",
        "spectrogram",
        "outguess",
    }
    return sorted({keyword for keyword in keywords if keyword.lower() in visual_set})


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
