"""Generated local HTML review index."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from libreprimus.image_transforms.loader import display_path


def write_review_pages(
    *,
    out_dir: Path,
    image_summaries: list[dict[str, Any]],
    global_contact_sheet: str,
) -> tuple[str, int]:
    """Write ignored local HTML review pages and return index path/count."""
    review_dir = out_dir / "review_pages"
    review_dir.mkdir(parents=True, exist_ok=True)
    for image in image_summaries:
        page_path = review_dir / f"{image['image_id']}.html"
        page_path.write_text(_image_page(image), encoding="utf-8")
        image["review_page"] = display_path(page_path)
    index = out_dir / "review_index.html"
    index.write_text(_index_page(image_summaries, global_contact_sheet), encoding="utf-8")
    return display_path(index), len(image_summaries)


def _index_page(image_summaries: list[dict[str, Any]], global_contact_sheet: str) -> str:
    rows = "\n".join(
        "<tr>"
        f"<td>{escape(str(image['image_id']))}</td>"
        f"<td>{escape(str(image['file_name']))}</td>"
        f"<td><a href='{_rel(image['contact_sheet'])}'>contact</a></td>"
        f"<td>{escape(', '.join(image['candidate_types']))}</td>"
        f"<td><a href='{_rel(image['review_page'])}'>review</a></td>"
        "</tr>"
        for image in image_summaries
    )
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Stage 3P Visual Review Index</title></head>
<body>
<h1>Stage 3P Visual Review Index</h1>
<p>Generated local review aid. No OCR, AI/ML interpretation, image-derived cipher execution, or solve claim.</p>
<p><a href="{_rel(global_contact_sheet)}">Global contact sheet</a></p>
<table border="1" cellspacing="0" cellpadding="4">
<thead><tr><th>Image ID</th><th>File</th><th>Contact Sheet</th><th>Candidate Flags</th><th>Page</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</body>
</html>
"""


def _image_page(image: dict[str, Any]) -> str:
    candidates = "".join(
        f"<li>{escape(candidate)}</li>" for candidate in image.get("candidate_types", [])
    )
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{escape(str(image['image_id']))}</title></head>
<body>
<h1>{escape(str(image['image_id']))}</h1>
<p>File: {escape(str(image['file_name']))}</p>
<p><a href="{_rel(image['contact_sheet'])}">Contact sheet</a></p>
<h2>Candidate Flags</h2>
<ul>{candidates}</ul>
<p>Flags are review aids only. They are not experiment seeds and not solve evidence.</p>
</body>
</html>
"""


def _rel(path: str) -> str:
    prefix = "experiments/results/image-transforms/stage3p/"
    return path.removeprefix(prefix)
