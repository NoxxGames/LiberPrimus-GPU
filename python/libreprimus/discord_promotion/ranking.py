"""Ranking utilities for Stage 3O promoted Discord-discovered records."""

from __future__ import annotations

from libreprimus.discord_promotion.models import HIGH_PRIORITY_DOMAINS, KNOWN_NUMBERS, MEDIUM_PRIORITY_KINDS


def link_priority(domain: str, url_kind: str) -> int:
    if domain in HIGH_PRIORITY_DOMAINS:
        return 0
    if any(domain.endswith(f".{item}") for item in HIGH_PRIORITY_DOMAINS):
        return 1
    if url_kind in MEDIUM_PRIORITY_KINDS:
        return 2
    return 3


def method_priority(record: dict) -> tuple[int, str]:
    claim_type = str(record.get("claim_type", "unknown"))
    keywords = set(record.get("extracted_keywords", []))
    if claim_type in {"source_reference", "false_positive_warning", "tried_and_failed"}:
        return (0, claim_type)
    if keywords & {"p56", "p57", "page 56", "page 57", "prime", "totient", "outguess"}:
        return (1, claim_type)
    return (2, claim_type)


def numeric_priority(record: dict) -> tuple[int, int]:
    numbers = set(int(number) for number in record.get("numbers", []))
    known_hits = len(numbers & KNOWN_NUMBERS)
    candidate_kind = str(record.get("candidate_kind", "unknown"))
    kind_score = 0 if candidate_kind in {"gp_sum", "rune_count", "base60", "binary"} else 1
    return (kind_score, -known_hits)
