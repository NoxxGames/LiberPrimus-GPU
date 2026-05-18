"""Build redacted review leads from Stage 3O promotions and Stage 3N records."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from libreprimus.discord_review.export import iter_jsonl, read_yaml
from libreprimus.discord_review.redacted_stream import public_links_from_text, sanitize_public_url
from libreprimus.discord_review.topic_classifier import classify_topic
from libreprimus.paths import repo_root

PROMOTED_LINKS = repo_root() / "data/observations/discord/promoted-public-source-links-stage3o.yaml"
PROMOTED_METHODS = repo_root() / "data/observations/discord/promoted-method-claim-candidates-stage3o.yaml"
PROMOTED_NUMERICS = repo_root() / "data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml"


def build_review_leads(*, ingestion_dir: Path, promotion_dir: Path) -> list[dict[str, Any]]:
    """Build bounded redacted review leads from promoted records and generated indexes."""
    leads: list[dict[str, Any]] = []
    leads.extend(_leads_from_promoted_links(PROMOTED_LINKS))
    leads.extend(_leads_from_promoted_methods(PROMOTED_METHODS))
    leads.extend(_leads_from_promoted_numerics(PROMOTED_NUMERICS))
    if not leads:
        leads.extend(_fallback_leads_from_ingestion(ingestion_dir))
    return leads


def _leads_from_promoted_links(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    payload = read_yaml(path)
    leads: list[dict[str, Any]] = []
    for record in payload.get("records", []):
        if not isinstance(record, dict):
            continue
        url = sanitize_public_url(str(record.get("url", "")))
        if not url:
            continue
        summary = (
            f"Public source-discovery link from Stage 3O: domain={record.get('domain', '')}; "
            f"kind={record.get('url_kind', '')}; occurrences={record.get('occurrence_count', 1)}."
        )
        leads.append(
            _lead(
                source_id=str(record.get("promoted_id", "")),
                topic=classify_topic(text=summary, public_links=[url]),
                evidence_type="source_link",
                public_links=[url],
                numeric_values=[],
                method_keywords=[str(record.get("url_kind", "source"))],
                redacted_summary=summary,
                suggested_next_action="Review the public source independently before promoting it to the source registry.",
                source_channel="discord-promoted-stage3o",
            )
        )
    return leads


def _leads_from_promoted_methods(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    payload = read_yaml(path)
    leads: list[dict[str, Any]] = []
    for record in payload.get("records", []):
        if not isinstance(record, dict):
            continue
        keywords = [str(keyword) for keyword in record.get("extracted_keywords", [])]
        claim_type = str(record.get("claim_type", "unknown"))
        evidence_type = "debunk_or_false_positive" if claim_type in {"tried_and_failed", "false_positive_warning"} else "method_claim"
        summary = str(record.get("redacted_summary") or f"method keyword cluster: {'/'.join(keywords)}")
        leads.append(
            _lead(
                source_id=str(record.get("promoted_id", "")),
                topic=classify_topic(text=summary, method_keywords=keywords),
                evidence_type=evidence_type,
                public_links=public_links_from_text(summary),
                numeric_values=[],
                method_keywords=keywords,
                redacted_summary=f"{summary}; occurrences={record.get('occurrence_count', 1)}.",
                suggested_next_action="Review against public provenance and negative controls before any experiment proposal.",
                source_channel="discord-promoted-stage3o",
            )
        )
    return leads


def _leads_from_promoted_numerics(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    payload = read_yaml(path)
    leads: list[dict[str, Any]] = []
    for record in payload.get("records", []):
        if not isinstance(record, dict):
            continue
        numbers = _numbers(record.get("numbers", []))
        keywords = [str(keyword) for keyword in record.get("context_keywords", [])]
        summary = str(record.get("redacted_summary") or f"numeric observation: {numbers}")
        leads.append(
            _lead(
                source_id=str(record.get("promoted_id", "")),
                topic=classify_topic(text=summary, method_keywords=keywords, numeric_values=numbers),
                evidence_type="numeric_observation",
                public_links=public_links_from_text(summary),
                numeric_values=numbers,
                method_keywords=keywords,
                redacted_summary=f"{summary}; occurrences={record.get('occurrence_count', 1)}.",
                suggested_next_action="Compare against source-locked observations; do not use as a seed without review.",
                source_channel="discord-promoted-stage3o",
            )
        )
    return leads


def _fallback_leads_from_ingestion(ingestion_dir: Path) -> list[dict[str, Any]]:
    leads: list[dict[str, Any]] = []
    for ordinal, record in enumerate(iter_jsonl(ingestion_dir / "discord_method_claim_candidates.jsonl") or [], start=1):
        keywords = [str(keyword) for keyword in record.get("extracted_keywords", [])]
        summary = str(record.get("redacted_summary") or f"method keyword cluster: {'/'.join(keywords)}")
        leads.append(
            _lead(
                source_id=f"stage3n-method-{ordinal}",
                topic=classify_topic(text=summary, method_keywords=keywords),
                evidence_type="method_claim",
                public_links=[],
                numeric_values=[],
                method_keywords=keywords,
                redacted_summary=summary,
                suggested_next_action="Review source context locally before promotion.",
                source_channel="stage3n-method-claim-extraction",
            )
        )
        if len(leads) >= 100:
            break
    return leads


def _lead(
    *,
    source_id: str,
    topic: str,
    evidence_type: str,
    public_links: list[str],
    numeric_values: list[int],
    method_keywords: list[str],
    redacted_summary: str,
    suggested_next_action: str,
    source_channel: str,
) -> dict[str, Any]:
    key = f"{source_id}:{topic}:{evidence_type}:{redacted_summary}"
    return {
        "record_type": "discord_review_lead_record",
        "lead_id": f"stage3q-lead-{hashlib.sha256(key.encode('utf-8')).hexdigest()[:24]}",
        "topic": topic,
        "source_channel": source_channel,
        "approximate_date": "unknown",
        "evidence_type": evidence_type,
        "public_links": public_links,
        "numeric_values": sorted(set(numeric_values)),
        "method_keywords": sorted(set(method_keywords)),
        "redacted_summary": redacted_summary[:1000],
        "suggested_next_action": suggested_next_action,
        "caution_notes": "Discord-derived review lead only; not canonical evidence, not an experiment seed, and not a solve claim.",
        "review_status": "human_review_required",
        "raw_message_committed": False,
        "username_committed": False,
        "private_url_committed": False,
        "trusted_as_canonical": False,
        "solve_claim": False,
    }


def _numbers(values: Any) -> list[int]:
    numbers: list[int] = []
    if not isinstance(values, list):
        return numbers
    for value in values:
        try:
            numbers.append(int(value))
        except (TypeError, ValueError):
            continue
    return numbers
