"""Channel shard generation for Stage 4A."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from libreprimus.discord_full_review.export import display_path
from libreprimus.discord_full_review.models import SHARD_TARGET_MARKDOWN_BYTES, SHARD_TARGET_MESSAGES


def split_messages(messages: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    shards: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_size = 0
    for record in messages:
        rendered = _message_markdown(record)
        if current and (len(current) >= SHARD_TARGET_MESSAGES or current_size + len(rendered.encode("utf-8")) > SHARD_TARGET_MARKDOWN_BYTES):
            shards.append(current)
            current = []
            current_size = 0
        current.append(record)
        current_size += len(rendered.encode("utf-8"))
    if current:
        shards.append(current)
    return shards


def write_channel_shards(
    *,
    out_dir: Path,
    site_dir: Path,
    channel_slug: str,
    channel_name: str,
    channel_id: str,
    messages: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    shard_records: list[dict[str, Any]] = []
    shards = split_messages(messages)
    channel_site_dir = site_dir / "channels" / channel_slug
    channel_site_dir.mkdir(parents=True, exist_ok=True)
    channel_md_dir = out_dir / "channel_shards"
    channel_md_dir.mkdir(parents=True, exist_ok=True)
    part_links: list[str] = []
    for part_number, shard in enumerate(shards, start=1):
        part_name = f"part{part_number:03d}"
        markdown_path = channel_md_dir / f"{channel_slug}.{part_name}.md"
        html_path = channel_site_dir / f"{part_name}.html"
        markdown = _channel_part_markdown(channel_name, part_number, shard)
        markdown_path.write_text(markdown, encoding="utf-8", newline="\n")
        html_path.write_text(_html_page(f"{channel_name} {part_name}", _messages_html(shard)), encoding="utf-8", newline="\n")
        part_links.append(f"{part_name}.html")
        shard_records.append(
            {
                "record_type": "discord_full_review_shard_record",
                "shard_id": f"{channel_id}-{part_name}",
                "channel_id": channel_id,
                "channel_slug": channel_slug,
                "part_number": part_number,
                "message_count": len(shard),
                "approximate_start_timestamp": shard[0].get("approximate_timestamp") if shard else None,
                "approximate_end_timestamp": shard[-1].get("approximate_timestamp") if shard else None,
                "markdown_relative_path": display_path(markdown_path),
                "html_relative_path": display_path(html_path),
                "raw_message_committed": False,
                "username_committed": False,
                "private_url_committed": False,
                "solve_claim": False,
            }
        )
    index_html = _channel_index_html(channel_name, len(messages), part_links)
    (channel_site_dir / "index.html").write_text(index_html, encoding="utf-8", newline="\n")
    return shard_records


def _channel_part_markdown(channel_name: str, part_number: int, shard: list[dict[str, Any]]) -> str:
    lines = [f"# {channel_name} Part {part_number:03d}", "", "Redacted chronological shard.", ""]
    for record in shard:
        lines.append(_message_markdown(record))
    return "\n".join(lines) + "\n"


def _message_markdown(record: dict[str, Any]) -> str:
    timestamp = record.get("approximate_timestamp") or "timestamp unavailable"
    text = str(record.get("redacted_text", ""))
    links = " ".join(f"<{link}>" for link in record.get("public_links", []))
    extras = f" {links}" if links else ""
    return f"- `{record.get('message_ref')}` `{timestamp}` {text}{extras}"


def _messages_html(messages: list[dict[str, Any]]) -> str:
    rows = []
    for record in messages:
        links = " ".join(
            f'<a href="{escape(link)}">{escape(link)}</a>' for link in record.get("public_links", [])
        )
        rows.append(
            "<article class=\"message\">"
            f"<div class=\"meta\">{escape(str(record.get('message_ref')))} "
            f"{escape(str(record.get('approximate_timestamp') or 'timestamp unavailable'))}</div>"
            f"<p>{escape(str(record.get('redacted_text', '')))}</p>"
            f"<div class=\"links\">{links}</div>"
            "</article>"
        )
    return "\n".join(rows)


def _channel_index_html(channel_name: str, message_count: int, part_links: list[str]) -> str:
    links = "\n".join(f'<li><a href="{escape(link)}">{escape(link)}</a></li>' for link in part_links)
    body = (
        f"<h1>{escape(channel_name)}</h1>"
        f"<p>{message_count} redacted messages split into {len(part_links)} parts.</p>"
        f"<ul>{links}</ul>"
        '<p><a href="../../index.html">Back to site index</a></p>'
    )
    return _html_page(channel_name, body)


def _html_page(title: str, body: str) -> str:
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>{escape(title)}</title><link rel=\"stylesheet\" href=\"../../assets/site.css\"></head>"
        f"<body>{body}</body></html>\n"
    )
