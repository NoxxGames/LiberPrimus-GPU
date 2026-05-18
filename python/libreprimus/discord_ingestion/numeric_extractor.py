"""Numeric observation candidate extraction for redacted Discord review."""

from __future__ import annotations

import hashlib
import re

from libreprimus.discord_ingestion.models import ARCHIVE_ID, KNOWN_NUMBERS, METHOD_KEYWORDS
from libreprimus.discord_ingestion.redaction import redacted_summary

NUMBER_RE = re.compile(r"\b\d{1,13}\b")


def extract_numeric_candidates(text: str, *, source_file_sha256: str, ordinal: int) -> list[dict]:
    lower = text.lower()
    numbers = sorted({int(match.group(0)) for match in NUMBER_RE.finditer(text)})
    context_keywords = sorted(keyword for keyword in METHOD_KEYWORDS if keyword in lower)
    selected = [number for number in numbers if number in KNOWN_NUMBERS]
    if not selected and context_keywords:
        selected = numbers[:20]
    if not selected:
        return []
    candidate_kind = _candidate_kind(selected, context_keywords)
    observation_id = hashlib.sha256(
        f"{source_file_sha256}:numeric:{ordinal}:{selected}:{context_keywords}".encode("utf-8")
    ).hexdigest()[:24]
    return [
        {
            "record_type": "discord_numeric_observation_candidate",
            "observation_id": f"discord-numeric-{observation_id}",
            "archive_id": ARCHIVE_ID,
            "source_file_sha256": source_file_sha256,
            "numbers": selected,
            "context_keywords": context_keywords,
            "candidate_kind": candidate_kind,
            "redacted_summary": redacted_summary(context_keywords, prefix=f"numeric cluster {candidate_kind}"),
            "raw_message_committed": False,
            "review_status": "human_review_required",
            "notes": "Numeric source-discovery lead only; raw message body is not committed.",
        }
    ]


def _candidate_kind(numbers: list[int], keywords: list[str]) -> str:
    keyword_set = set(keywords)
    if "gp sum" in keyword_set or "gematria" in keyword_set:
        return "gp_sum"
    if "rune count" in keyword_set:
        return "rune_count"
    if "cookie" in keyword_set or "hash" in keyword_set:
        return "cookie_hash"
    if "binary" in keyword_set:
        return "binary"
    if "base60" in keyword_set or "base 60" in keyword_set or "cuneiform" in keyword_set:
        return "base60"
    if keyword_set & {"page 56", "page 57", "p56", "p57"}:
        return "page_number"
    if any(number in {509, 503, 563, 569} for number in numbers):
        return "dimension"
    if any(number in {29, 31, 13} for number in numbers):
        return "prime"
    return "unknown"
