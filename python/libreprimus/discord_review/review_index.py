"""Local HTML review index for Stage 3Q generated bundles."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root


def write_review_index(
    *,
    out_dir: Path,
    shard_records: list[dict[str, Any]],
    summary: dict[str, Any],
) -> Path:
    rows = "\n".join(
        "<tr>"
        f"<td>{escape(str(record['topic']))}</td>"
        f"<td>{int(record['lead_count'])}</td>"
        f"<td><a href=\"{escape(_relative_to_index(record['output_relative_path']))}\">{escape(str(record['output_relative_path']))}</a></td>"
        "</tr>"
        for record in shard_records
    )
    html = (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        "<title>Stage 3Q Discord Review Bundles</title>"
        "<style>body{font-family:system-ui,sans-serif;margin:2rem;max-width:1100px}"
        "table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:.4rem;text-align:left}"
        "code{background:#eee;padding:.1rem .2rem}</style></head><body>"
        "<h1>Stage 3Q Discord Review Bundles</h1>"
        "<p>Generated local review index. Raw logs, usernames, message IDs, and private URLs are not included.</p>"
        f"<p><strong>Review leads:</strong> {int(summary.get('review_lead_count', 0))}; "
        f"<strong>Topic shards:</strong> {int(summary.get('topic_shard_count', 0))}</p>"
        "<table><thead><tr><th>Topic</th><th>Leads</th><th>Shard</th></tr></thead><tbody>"
        f"{rows}</tbody></table></body></html>\n"
    )
    path = out_dir / "review_index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path


def _relative_to_index(path: str) -> str:
    repo_path = repo_root() / path
    try:
        return repo_path.relative_to((repo_root() / "experiments/results/discord-review-bundles/stage3q")).as_posix()
    except ValueError:
        return path
