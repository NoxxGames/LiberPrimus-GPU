"""Keyword-only method-claim candidate extraction."""

from __future__ import annotations

import hashlib
import re

from libreprimus.discord_ingestion.models import (
    ARCHIVE_ID,
    FAILURE_KEYWORDS,
    METHOD_KEYWORDS,
    SOURCE_KEYWORDS,
)
from libreprimus.discord_ingestion.redaction import redacted_summary


def extract_claim_candidates(text: str, *, source_file_sha256: str, ordinal: int) -> list[dict]:
    lower = _normalize(text)
    keywords = sorted(keyword for keyword in METHOD_KEYWORDS | FAILURE_KEYWORDS | SOURCE_KEYWORDS if keyword in lower)
    if not keywords:
        return []
    claim_type = _claim_type(keywords)
    claim_id = hashlib.sha256(f"{source_file_sha256}:claim:{ordinal}:{','.join(keywords)}".encode("utf-8")).hexdigest()[:24]
    return [
        {
            "record_type": "discord_method_claim_candidate",
            "claim_id": f"discord-claim-{claim_id}",
            "archive_id": ARCHIVE_ID,
            "source_file_sha256": source_file_sha256,
            "claim_type": claim_type,
            "extracted_keywords": keywords,
            "redacted_summary": redacted_summary(keywords, prefix="method keyword cluster"),
            "raw_message_committed": False,
            "usernames_committed": False,
            "confidence": "review_required",
            "review_status": "human_review_required",
            "notes": "Keyword-only source-discovery lead; raw message body is not committed.",
        }
    ]


def _claim_type(keywords: list[str]) -> str:
    keyword_set = set(keywords)
    if keyword_set & FAILURE_KEYWORDS:
        if "tried" in keyword_set or "failed" in keyword_set or "no result" in keyword_set:
            return "tried_and_failed"
        return "false_positive_warning"
    if "gp sum" in keyword_set:
        return "gp_sum_claim"
    if "rune count" in keyword_set:
        return "rune_count_claim"
    if keyword_set & {"cuneiform", "base60", "base 60", "binary", "spectrogram"}:
        return "visual_observation"
    if keyword_set & {"prime", "totient", "phi", "fibonacci", "mersenne"}:
        return "stream_candidate"
    if keyword_set & {"vigenere", "affine", "caesar", "atbash"}:
        return "transform_method"
    if keyword_set & {"github", "pastebin", "archive", "fandom", "transcript", "rtkd", "scream314"}:
        return "source_reference"
    if "hash" in keyword_set or "cookie" in keyword_set:
        return "transform_method"
    return "unknown"


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())
