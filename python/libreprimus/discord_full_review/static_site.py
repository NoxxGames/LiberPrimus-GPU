"""Static site generation for Stage 4A review bundles."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
from typing import Any

from libreprimus.discord_full_review.models import TOPIC_DEFINITIONS

NOINDEX_META = '<meta name="robots" content="noindex,nofollow,noarchive">'
PRIVACY_NOTICE = (
    "This is a redacted research review site generated from Discord-derived material. "
    "Do not treat chat-derived claims as facts. Do not index or redistribute casually."
)


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


def write_site_privacy_files(site_dir: Path, summary: dict[str, Any]) -> dict[str, str]:
    """Write static-site privacy and upload helper files."""

    important_paths = {
        "root_index": "index.html",
        "privacy_notice": "SITE_PRIVACY_NOTICE.md",
        "sftp_upload_checklist": "SFTP_UPLOAD_CHECKLIST.md",
        "robots": "robots.txt",
        "htaccess_example": ".htaccess.example",
        "deep_research_manifest": "../deep_research_bundle_manifest.yaml",
        "channel_index": "../channel_index.md",
        "lp_page_gallery": "lp-pages/index.html",
    }
    (site_dir / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8", newline="\n")
    (site_dir / "SITE_PRIVACY_NOTICE.md").write_text(
        "# Site Privacy Notice\n\n"
        f"{PRIVACY_NOTICE}\n\n"
        "This generated site uses `redacted_public` mode. Usernames, user IDs, message IDs, avatar URLs, "
        "private Discord-hosted URLs, raw Discord HTML, and raw LP page image source paths are not intended "
        "for public redistribution.\n\n"
        "Use this site as a review aid only. Promote claims through the repository's source-lock and "
        "observation review process before treating them as evidence.\n",
        encoding="utf-8",
        newline="\n",
    )
    (site_dir / "SFTP_UPLOAD_CHECKLIST.md").write_text(
        "# SFTP Upload Checklist\n\n"
        "- Upload only the contents of `experiments/results/discord-full-review/stage4a/site/`.\n"
        "- Do not upload `third_party/` directories.\n"
        "- Do not upload raw Discord HTML exports.\n"
        "- Do not upload raw Liber Primus page-image directories.\n"
        "- Do not upload generated parent folders unless you intentionally want non-site JSONL/Markdown review files hosted.\n"
        "- Keep `robots.txt` and noindex metadata with the site.\n"
        "- Consider basic authentication, restricted URLs, or server-level noindex headers for public hosting.\n"
        "- After upload, test `index.html`, a channel part, a topic page, an index page, and the LP gallery.\n",
        encoding="utf-8",
        newline="\n",
    )
    (site_dir / ".htaccess.example").write_text(
        "# Optional Apache hardening example. Rename to .htaccess only on servers that support it.\n"
        "Header set X-Robots-Tag \"noindex, nofollow, noarchive\"\n"
        "Options -Indexes\n"
        "# Basic auth example:\n"
        "# AuthType Basic\n"
        "# AuthName \"LiberPrimus Review\"\n"
        "# AuthUserFile /absolute/path/outside/webroot/.htpasswd\n"
        "# Require valid-user\n",
        encoding="utf-8",
        newline="\n",
    )
    manifest = {
        "record_type": "discord_full_review_site_manifest",
        "generated_at_utc": summary.get("generated_at_utc"),
        "privacy_mode": summary.get("privacy_mode"),
        "noindex_enabled": True,
        "robots_disallow_all": True,
        "channel_count": summary.get("channel_count", 0),
        "channel_part_count": summary.get("channel_shard_count", 0),
        "topic_count": summary.get("topic_shard_count", 0),
        "public_link_count": summary.get("public_link_count", 0),
        "image_reference_count": summary.get("image_reference_count", 0),
        "attachment_reference_count": summary.get("attachment_reference_count", 0),
        "lp_page_image_count": summary.get("lp_page_image_count", 0),
        "root_index": "index.html",
        "important_paths": important_paths,
        "raw_discord_html_committed": False,
        "generated_site_committed": False,
        "solve_claim": False,
    }
    (site_dir / "site_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (site_dir / "site_manifest.md").write_text(
        "# Site Manifest\n\n"
        f"- Generated at UTC: `{manifest['generated_at_utc']}`\n"
        f"- Privacy mode: `{manifest['privacy_mode']}`\n"
        f"- Noindex enabled: `{str(manifest['noindex_enabled']).lower()}`\n"
        f"- Channels: `{manifest['channel_count']}`\n"
        f"- Channel parts: `{manifest['channel_part_count']}`\n"
        f"- Topic pages: `{manifest['topic_count']}`\n"
        f"- Public links: `{manifest['public_link_count']}`\n"
        f"- Image references: `{manifest['image_reference_count']}`\n"
        f"- Attachment references: `{manifest['attachment_reference_count']}`\n"
        f"- LP page gallery images: `{manifest['lp_page_image_count']}`\n\n"
        "Raw Discord HTML, raw LP page images, generated parent bundles, and private identifiers are not part of the hosted site contract.\n",
        encoding="utf-8",
        newline="\n",
    )
    return important_paths


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
    body = f"""
<h1>LiberPrimus Stage 4A Discord Review Site</h1>
{privacy_notice_html()}
<h2>Summary</h2>
<ul>
<li>Channels: {summary.get('channel_count')}</li>
<li>Redacted messages: {summary.get('redacted_message_count')}</li>
<li>Channel shards: {summary.get('channel_shard_count')}</li>
<li>Topic shards: {summary.get('topic_shard_count')}</li>
<li>LP page images in generated gallery: {summary.get('lp_page_image_count')}</li>
</ul>
<h2>Review And Upload Documents</h2>
<ul>
<li><a href="SITE_PRIVACY_NOTICE.md">Site privacy notice</a></li>
<li><a href="SFTP_UPLOAD_CHECKLIST.md">SFTP upload checklist</a></li>
<li><a href="site_manifest.md">Site manifest</a> and <a href="site_manifest.json">JSON manifest</a></li>
<li><a href="robots.txt">robots.txt</a></li>
<li><a href=".htaccess.example">optional .htaccess example</a></li>
<li><a href="../deep_research_bundle_manifest.yaml">Deep Research manifest</a></li>
<li><a href="../README_FOR_DEEP_RESEARCH.md">README for Deep Research</a></li>
<li><a href="../SFTP_UPLOAD_INSTRUCTIONS.md">Stage 4A root SFTP upload instructions</a></li>
</ul>
<h2>Channels</h2>
<table><thead><tr><th>Channel</th><th>Messages</th><th>Parts</th><th>Public links</th><th>Image refs</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Topic Views</h2><ul>{topics}</ul>
<h2>Indexes</h2><ul>{indexes}</ul>
<h2>LP Page Gallery</h2><p><a href="lp-pages/index.html">Open generated LP page image gallery</a></p>
<h2>Warnings And Limits</h2><p>This site is a generated review aid, not source truth and not a solve claim. Classification creates views over a redacted chronological layer; it does not delete records.</p>
"""
    path.write_text(html_page("LiberPrimus Stage 4A Discord Review Site", body, css_href="assets/site.css"), encoding="utf-8", newline="\n")
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
        html_page(
            title,
            f"<h1>{escape(title)}</h1>{privacy_notice_html()}<table><thead><tr><th>Ref</th><th>Channel</th><th>Value</th><th>Excerpt</th></tr></thead><tbody>{rows}</tbody></table>"
            "<p><a href=\"../index.html\">Back to site index</a></p>",
            css_href="../assets/site.css",
        ),
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
        html_page(
            topic,
            f"<h1>{escape(topic)}</h1>{privacy_notice_html()}{rows}<p><a href=\"../index.html\">Back to site index</a></p>",
            css_href="../assets/site.css",
        ),
        encoding="utf-8",
        newline="\n",
    )


def privacy_notice_html() -> str:
    return f"<p class=\"notice\">{escape(PRIVACY_NOTICE)}</p>"


def html_page(title: str, body: str, *, css_href: str) -> str:
    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head>"
        "<meta charset=\"utf-8\">"
        f"{NOINDEX_META}"
        f"<title>{escape(title)}</title>"
        f"<link rel=\"stylesheet\" href=\"{escape(css_href)}\">"
        "</head>\n"
        f"<body>{body}<footer>{privacy_notice_html()}</footer></body></html>\n"
    )


def _record_ref(record: dict[str, Any]) -> str:
    return str(
        record.get(
            "message_ref",
            record.get("image_reference_id", record.get("attachment_reference_id", "")),
        )
    )
