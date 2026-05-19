"""Static site generation for Stage 4A review bundles."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from libreprimus.discord_full_review.models import TOPIC_DEFINITIONS


def write_site_assets(site_dir: Path) -> None:
    css = """
body { font-family: system-ui, sans-serif; line-height: 1.45; margin: 2rem; color: #1e2428; background: #fbfbf8; }
a { color: #2459a6; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
th, td { border: 1px solid #ccd3d8; padding: 0.45rem; vertical-align: top; }
th { background: #edf1f4; text-align: left; }
.notice { border-left: 4px solid #9a6b00; background: #fff7dd; padding: 0.8rem; }
.message { border-bottom: 1px solid #dfe4e8; padding: 0.6rem 0; }
.meta { color: #66737c; font-size: 0.9rem; }
.gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 1rem; }
.gallery img { max-width: 100%; height: auto; border: 1px solid #ccd3d8; background: white; }
"""
    (site_dir / "assets").mkdir(parents=True, exist_ok=True)
    (site_dir / "assets" / "site.css").write_text(css.strip() + "\n", encoding="utf-8")


def write_site_index(
    *,
    site_dir: Path,
    summary: dict[str, Any],
    channel_records: list[dict[str, Any]],
) -> Path:
    rows = "\n".join(
        "<tr>"
        f"<td><a href=\"channels/{record['channel_slug']}/index.html\">{escape(record['channel_name'])}</a></td>"
        f"<td>{record['estimated_message_count']}</td><td>{record['part_count']}</td>"
        f"<td>{record['public_link_count']}</td><td>{record['image_reference_count']}</td>"
        "</tr>"
        for record in channel_records
    )
    topics = "\n".join(
        f"<li><a href=\"topics/{topic}.html\">{escape(topic)}</a></li>" for topic in TOPIC_DEFINITIONS
    )
    indexes = "\n".join(
        f"<li><a href=\"indexes/{name}.html\">{escape(name)}</a></li>"
        for name in (
            "public-links",
            "image-references",
            "attachment-references",
            "method-claims",
            "numeric-claims",
            "visual-claims",
            "debunks",
        )
    )
    path = site_dir / "index.html"
    body = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>LiberPrimus Stage 4A Discord Review Site</title><link rel="stylesheet" href="assets/site.css"></head>
<body>
<h1>LiberPrimus Stage 4A Discord Review Site</h1>
<p class="notice">Redacted public review mode. Raw Discord logs, usernames, IDs, private URLs, and raw LP source images are not part of committed repository state.</p>
<h2>Summary</h2>
<ul>
<li>Channels: {summary.get('channel_count')}</li>
<li>Redacted messages: {summary.get('redacted_message_count')}</li>
<li>Channel shards: {summary.get('channel_shard_count')}</li>
<li>Topic shards: {summary.get('topic_shard_count')}</li>
<li>LP page images in generated gallery: {summary.get('lp_page_image_count')}</li>
</ul>
<p><a href="../deep_research_bundle_manifest.yaml">Deep Research manifest</a> | <a href="../README_FOR_DEEP_RESEARCH.md">README for Deep Research</a> | <a href="../SFTP_UPLOAD_INSTRUCTIONS.md">SFTP upload instructions</a></p>
<h2>Channels</h2>
<table><thead><tr><th>Channel</th><th>Messages</th><th>Parts</th><th>Public links</th><th>Image refs</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Topic Views</h2><ul>{topics}</ul>
<h2>Indexes</h2><ul>{indexes}</ul>
<h2>LP Page Gallery</h2><p><a href="lp-pages/index.html">Open generated LP page image gallery</a></p>
<h2>Warnings And Limits</h2><p>This site is a generated review aid, not source truth and not a solve claim. Classification creates views over a redacted chronological layer; it does not delete records.</p>
</body></html>
"""
    path.write_text(body, encoding="utf-8", newline="\n")
    return path


def write_index_page(path: Path, title: str, records: list[dict[str, Any]]) -> None:
    rows = "\n".join(
        "<tr>"
        f"<td>{escape(_record_ref(record))}</td>"
        f"<td>{escape(str(record.get('channel_name', record.get('channel_id', ''))))}</td>"
        f"<td>{escape(str(record.get('value', record.get('file_name', ''))))}</td>"
        f"<td>{escape(str(record.get('redacted_excerpt', ''))[:500])}</td>"
        "</tr>"
        for record in records[:10_000]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>{escape(title)}</title><link rel=\"stylesheet\" href=\"../assets/site.css\"></head><body>"
        f"<h1>{escape(title)}</h1><table><thead><tr><th>Ref</th><th>Channel</th><th>Value</th><th>Excerpt</th></tr></thead><tbody>{rows}</tbody></table>"
        "<p><a href=\"../index.html\">Back to site index</a></p></body></html>\n",
        encoding="utf-8",
        newline="\n",
    )


def write_topic_page(path: Path, topic: str, records: list[dict[str, Any]]) -> None:
    rows = "\n".join(
        "<article class=\"message\">"
        f"<div class=\"meta\">{escape(str(record.get('message_ref')))} {escape(str(record.get('channel_name', '')))}</div>"
        f"<p>{escape(str(record.get('redacted_text', '')))}</p></article>"
        for record in records[:10_000]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>{escape(topic)}</title><link rel=\"stylesheet\" href=\"../assets/site.css\"></head><body>"
        f"<h1>{escape(topic)}</h1>{rows}<p><a href=\"../index.html\">Back to site index</a></p></body></html>\n",
        encoding="utf-8",
        newline="\n",
    )


def _record_ref(record: dict[str, Any]) -> str:
    return str(
        record.get(
            "message_ref",
            record.get("image_reference_id", record.get("attachment_reference_id", "")),
        )
    )
