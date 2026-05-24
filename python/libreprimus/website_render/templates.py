"""HTML templates for the static Stage 5AM research index."""

from __future__ import annotations

from html import escape
from typing import Any

BANNER = "Private research metadata index. No raw source bodies. No solve claims. Publication gated."

NAV_ITEMS = [
    ("Home", "index.html"),
    ("Bundles", "bundles/index.html"),
    ("Sources", "sources/index.html"),
    ("Content", "content/index.html"),
    ("Claims", "claims/index.html"),
    ("Publication Gates", "publication-gates/index.html"),
    ("Missing Sources", "missing-sources/index.html"),
    ("Deep Research", "deep-research/index.html"),
    ("About", "about/index.html"),
]


def page(title: str, body: str, *, depth: int = 0) -> str:
    """Render a static page with local assets only."""

    prefix = "../" * depth
    nav = "\n".join(
        f'<a href="{escape(prefix + href)}">{escape(label)}</a>'
        for label, href in NAV_ITEMS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <title>{escape(title)} - Stage 5AM Research Index</title>
  <link rel="stylesheet" href="{escape(prefix)}assets/site.css">
</head>
<body>
  <header class="site-header">
    <div class="eyebrow">PRIVATE / REVIEW-GATED RESEARCH METADATA</div>
    <h1>{escape(title)}</h1>
    <p>{escape(BANNER)}</p>
    <nav>{nav}</nav>
  </header>
  <main>
{body}
  </main>
  <footer>
    <p>No raw source bodies, private identifiers, generated extracts, solve claims, CUDA execution, or Deep Research output are included.</p>
  </footer>
  <script src="{escape(prefix)}assets/site.js"></script>
</body>
</html>
"""


def summary_grid(items: dict[str, Any]) -> str:
    """Render small key/value summary cells."""

    cells = "\n".join(
        f"<div><strong>{escape(str(key).replace('_', ' '))}</strong><span>{escape(str(value))}</span></div>"
        for key, value in items.items()
    )
    return f'<section class="summary-grid">{cells}</section>'


def cards(records: list[dict[str, Any]], fields: list[str], *, id_field: str = "id") -> str:
    """Render metadata cards."""

    chunks: list[str] = []
    for record in records:
        title = record.get("title") or record.get(id_field) or record.get("source_id") or record.get("bundle_id") or "record"
        rows = []
        for field in fields:
            value = record.get(field, "")
            if isinstance(value, list):
                value = ", ".join(str(item) for item in value[:12])
            elif isinstance(value, dict):
                value = ", ".join(f"{key}: {item}" for key, item in sorted(value.items())[:8])
            rows.append(f"<dt>{escape(field.replace('_', ' '))}</dt><dd>{escape(str(value))}</dd>")
        labels = _labels(record)
        chunks.append(
            f'<article class="card"><h2>{escape(str(title))}</h2>{labels}<dl>{"".join(rows)}</dl></article>'
        )
    return '<section class="cards">' + "\n".join(chunks) + "</section>"


def table(records: list[dict[str, Any]], fields: list[str]) -> str:
    """Render a compact metadata table."""

    headers = "".join(f"<th>{escape(field.replace('_', ' '))}</th>" for field in fields)
    rows = []
    for record in records:
        cells = []
        for field in fields:
            value = record.get(field, "")
            if isinstance(value, list):
                value = ", ".join(str(item) for item in value[:8])
            elif isinstance(value, dict):
                value = ", ".join(f"{key}: {item}" for key, item in sorted(value.items())[:6])
            cells.append(f"<td>{escape(str(value))}</td>")
        rows.append(f"<tr>{''.join(cells)}</tr>")
    return f'<div class="table-wrap"><table><thead><tr>{headers}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def warning_panel() -> str:
    """Render the standard publication warning."""

    bullets = [
        "No raw source bodies are included.",
        "No private Discord/forum message bodies are included.",
        "No raw images, spreadsheets, archives, PDFs, audio, or video are included.",
        "Publication gates are not waived by this renderer.",
        "No solve claim is made.",
    ]
    lis = "".join(f"<li>{escape(item)}</li>" for item in bullets)
    return f'<section class="warning"><h2>Publication Guardrails</h2><ul>{lis}</ul></section>'


def _labels(record: dict[str, Any]) -> str:
    labels = []
    status = str(record.get("publication_status", ""))
    review = str(record.get("review_status", ""))
    if "blocked" in status or "blocked" in review:
        labels.append("review blocked")
    if record.get("private_deep_research_allowed") is True:
        labels.append("private Deep Research only")
    if record.get("raw_content_publication_allowed") is False:
        labels.append("raw source never publish")
    if not labels:
        labels.append("metadata only")
    return '<p class="labels">' + "".join(f"<span>{escape(label)}</span>" for label in labels) + "</p>"
