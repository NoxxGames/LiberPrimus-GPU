"""Markdown topic shard writer for Stage 3Q review bundles."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from libreprimus.discord_review.models import DEFAULT_SHARD_MAX_BYTES, SHARD_FILENAMES, TOPIC_TITLES, TOPICS
from libreprimus.paths import repo_root


def write_topic_shards(
    *,
    out_dir: Path,
    leads: list[dict[str, Any]],
    generated_at: str,
    max_bytes: int = DEFAULT_SHARD_MAX_BYTES,
) -> list[dict[str, Any]]:
    shard_dir = out_dir / "topic_shards"
    shard_dir.mkdir(parents=True, exist_ok=True)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for lead in leads:
        grouped[str(lead.get("topic", TOPICS[-1]))].append(lead)

    records: list[dict[str, Any]] = []
    for topic in TOPICS:
        topic_leads = grouped.get(topic, [])
        pages = _split_leads(topic, topic_leads, generated_at, max_bytes)
        for index, text in enumerate(pages, start=1):
            base_name = SHARD_FILENAMES[topic]
            if len(pages) == 1:
                file_name = base_name
                shard_id = f"stage3q-shard-{topic}"
            else:
                stem = base_name.removesuffix(".md")
                file_name = f"{stem}.part{index:03d}.md"
                shard_id = f"stage3q-shard-{topic}-part{index:03d}"
            path = shard_dir / file_name
            path.write_text(text, encoding="utf-8")
            page_leads = _page_leads(topic_leads, index, len(pages), max_bytes, generated_at)
            records.append(
                {
                    "record_type": "discord_topic_shard_record",
                    "shard_id": shard_id,
                    "topic": topic,
                    "output_relative_path": _display_path(path),
                    "lead_count": len(page_leads),
                    "source_file_count": len({lead.get("source_channel", "") for lead in page_leads}),
                    "link_count": sum(len(lead.get("public_links", [])) for lead in page_leads),
                    "numeric_observation_count": sum(1 for lead in page_leads if lead.get("numeric_values")),
                    "method_claim_count": sum(1 for lead in page_leads if lead.get("method_keywords")),
                    "raw_message_committed": False,
                    "username_committed": False,
                    "private_url_committed": False,
                    "solve_claim": False,
                    "notes": "Generated ignored Markdown shard for AI/deep-review workflows.",
                }
            )
    return records


def _split_leads(topic: str, leads: list[dict[str, Any]], generated_at: str, max_bytes: int) -> list[str]:
    header = _header(topic, generated_at)
    if not leads:
        return [header + "\nNo redacted review leads were assigned to this topic.\n"]
    pages: list[str] = []
    current = header
    for lead in leads:
        entry = _entry(lead)
        if len((current + entry).encode("utf-8")) > max_bytes and current != header:
            pages.append(current)
            current = header + "\n"
        current += entry
    pages.append(current)
    return pages


def _page_leads(
    leads: list[dict[str, Any]], page_index: int, page_count: int, max_bytes: int, generated_at: str
) -> list[dict[str, Any]]:
    if page_count == 1:
        return leads
    pages = _split_leads(str(leads[0].get("topic", TOPICS[-1])) if leads else TOPICS[-1], leads, generated_at, max_bytes)
    marker_ids: set[str] = set()
    for match in pages[page_index - 1].split("- lead_id: ")[1:]:
        marker_ids.add(match.splitlines()[0].strip())
    return [lead for lead in leads if lead.get("lead_id") in marker_ids]


def _header(topic: str, generated_at: str) -> str:
    title = TOPIC_TITLES.get(topic, topic)
    return (
        f"# {title}\n\n"
        "- generated_at_utc: " + generated_at + "\n"
        "- source: admin_provided_discord_html_export\n"
        "- privacy_notice: Redacted, topic-bounded review shard. Repo docs and registries remain source of truth.\n"
        "- raw_logs_committed: false\n"
        "- usernames_redacted: true\n"
        "- message_bodies_redacted_or_summarized: true\n"
        "- solve_claim: false\n\n"
    )


def _entry(lead: dict[str, Any]) -> str:
    links = ", ".join(str(link) for link in lead.get("public_links", [])) or "none"
    numbers = ", ".join(str(number) for number in lead.get("numeric_values", [])) or "none"
    keywords = ", ".join(str(keyword) for keyword in lead.get("method_keywords", [])) or "none"
    return (
        f"## Lead: {lead.get('evidence_type', 'review lead')}\n"
        f"- lead_id: {lead.get('lead_id')}\n"
        f"- topic: {lead.get('topic')}\n"
        f"- source_channel: {lead.get('source_channel')}\n"
        f"- approximate_date: {lead.get('approximate_date')}\n"
        f"- evidence_type: {lead.get('evidence_type')}\n"
        f"- public_links: {links}\n"
        f"- numeric_values: {numbers}\n"
        f"- method_keywords: {keywords}\n"
        f"- redacted_summary: {lead.get('redacted_summary')}\n"
        f"- review_status: {lead.get('review_status')}\n"
        f"- suggested_next_action: {lead.get('suggested_next_action')}\n"
        f"- caution_notes: {lead.get('caution_notes')}\n\n"
    )


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
