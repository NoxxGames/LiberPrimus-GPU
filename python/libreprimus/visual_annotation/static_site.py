"""Generated local static review site for Stage 4C annotation tasks."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from libreprimus.visual_annotation.grid_overlay import write_grid_overlay
from libreprimus.visual_annotation.page_gallery import copy_or_thumbnail_image, relevant_images

NOINDEX_META = '<meta name="robots" content="noindex,nofollow,noarchive">'


def write_static_site(
    *,
    out_dir: Path,
    image_dir: Path,
    image_artifacts: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
    cuneiform: list[dict[str, Any]],
    dot: list[dict[str, Any]],
    delimiter: list[dict[str, Any]],
    negative: list[dict[str, Any]],
    summary: dict[str, Any],
) -> dict[str, Any]:
    """Write ignored static review pages and return generated counts."""

    site_dir = out_dir / "site"
    assets_dir = site_dir / "assets"
    pages_dir = site_dir / "pages"
    tasks_dir = site_dir / "tasks"
    for directory in (assets_dir, pages_dir, tasks_dir, site_dir / "templates"):
        directory.mkdir(parents=True, exist_ok=True)
    _write_css(assets_dir / "site.css")
    _write_sftp(site_dir / "SFTP_UPLOAD_INSTRUCTIONS.md")

    artifacts = relevant_images(tasks, image_artifacts)
    image_pages = _write_page_pages(
        site_dir=site_dir,
        image_dir=image_dir,
        image_artifacts=artifacts,
    )
    _write_task_pages(tasks_dir, tasks)
    _write_index(
        site_dir=site_dir,
        tasks=tasks,
        cuneiform=cuneiform,
        dot=dot,
        delimiter=delimiter,
        negative=negative,
        summary=summary,
    )
    manifest = {
        "record_type": "visual_annotation_manifest",
        "stage": "stage-4c",
        "task_count": len(tasks),
        "cuneiform_task_count": len(cuneiform),
        "dot_task_count": len(dot),
        "delimiter_task_count": len(delimiter),
        "negative_control_task_count": len(negative),
        "image_page_count": len(image_pages),
        "site_index": "site/index.html",
        "templates_dir": "site/templates",
        "noindex_enabled": True,
        "solve_claim": False,
    }
    (site_dir / "annotation_manifest.yaml").write_text(
        _manifest_yaml(manifest), encoding="utf-8", newline="\n"
    )
    return {"site_index": site_dir / "index.html", "image_page_count": len(image_pages)}


def _write_page_pages(
    *,
    site_dir: Path,
    image_dir: Path,
    image_artifacts: list[dict[str, Any]],
) -> list[Path]:
    image_pages: list[Path] = []
    image_asset_dir = site_dir / "assets" / "page-images"
    for artifact in image_artifacts:
        image_id = str(artifact.get("image_id", ""))
        relative_path = Path(str(artifact.get("relative_path", artifact.get("file_name", ""))))
        source = image_dir / relative_path.name
        thumb = image_asset_dir / f"{image_id}.jpg"
        grid = image_asset_dir / f"{image_id}-grid.jpg"
        source_available = source.is_file()
        if source_available:
            copy_or_thumbnail_image(source, thumb)
            write_grid_overlay(source, grid)
        page = site_dir / "pages" / f"{image_id}.html"
        body = f"""
<h1>{escape(image_id)}</h1>
<p><a href="../index.html">Back to annotation index</a></p>
<dl>
<dt>Source file</dt><dd>{escape(str(artifact.get('file_name', '')))}</dd>
<dt>Dimensions</dt><dd>{escape(str(artifact.get('width', 'unknown')))} x {escape(str(artifact.get('height', 'unknown')))}</dd>
<dt>Coordinate system</dt><dd>pixel_absolute on the generated review-size image unless the reviewer records otherwise.</dd>
</dl>
<p>Report x_min, y_min, x_max, y_max for the visual region. A coordinate annotation records that a region exists here; it does not establish meaning.</p>
{_image_html('../assets/page-images/' + grid.name if source_available else '', 'Grid overlay')}
{_image_html('../assets/page-images/' + thumb.name if source_available else '', 'Review image')}
"""
        page.write_text(_html_page(image_id, body, "../assets/site.css"), encoding="utf-8", newline="\n")
        image_pages.append(page)
    return image_pages


def _write_task_pages(tasks_dir: Path, tasks: list[dict[str, Any]]) -> None:
    for task in tasks:
        linked_images = "".join(
            f'<li><a href="../pages/{escape(image_ref)}.html">{escape(image_ref)}</a></li>'
            for image_ref in task.get("image_refs", [])
        )
        body = f"""
<h1>{escape(str(task['task_id']))}</h1>
<p><a href="../index.html">Back to annotation index</a></p>
<dl>
<dt>Task family</dt><dd>{escape(str(task.get('task_family', '')))}</dd>
<dt>Source observation</dt><dd>{escape(str(task.get('source_observation_id', '')))}</dd>
<dt>Annotation status</dt><dd>{escape(str(task.get('annotation_status', '')))}</dd>
<dt>Review status</dt><dd>{escape(str(task.get('review_status', '')))}</dd>
<dt>Coordinate system</dt><dd>{escape(str(task.get('coordinate_system', '')))}</dd>
</dl>
<h2>Instructions</h2>
<p>{escape(str(task.get('instructions', '')))}</p>
<h2>Candidate Summary</h2>
<p>{escape(str(task.get('candidate_summary', '')))}</p>
<h2>Ambiguity Notes</h2>
<p>{escape(str(task.get('ambiguity_notes', '')))}</p>
<h2>Images</h2>
<ul>{linked_images or '<li>No page image resolved yet.</li>'}</ul>
<h2>Template</h2>
<p><a href="../templates/{escape(str(task['task_id']))}.annotation.yaml">Blank annotation template</a></p>
"""
        (tasks_dir / f"{task['task_id']}.html").write_text(
            _html_page(str(task["task_id"]), body, "../assets/site.css"),
            encoding="utf-8",
            newline="\n",
        )


def _write_index(
    *,
    site_dir: Path,
    tasks: list[dict[str, Any]],
    cuneiform: list[dict[str, Any]],
    dot: list[dict[str, Any]],
    delimiter: list[dict[str, Any]],
    negative: list[dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    grouped = {
        "Cuneiform": [record["task_id"] for record in cuneiform],
        "Delimiters": [record["task_id"] for record in delimiter],
        "Dot Patterns": [record["task_id"] for record in dot],
        "Negative Controls": [record["task_id"] for record in negative],
        "All Tasks": [record["task_id"] for record in tasks],
    }
    sections = "\n".join(
        f"<h2>{escape(title)}</h2><ol>{''.join(_task_link(task_id) for task_id in task_ids)}</ol>"
        for title, task_ids in grouped.items()
    )
    body = f"""
<h1>LiberPrimus Stage 4C Visual Annotation Pack</h1>
<p class="notice">This generated local review site records coordinate tasks only. Coordinates and readings are separate. Nothing here verifies visual meaning, creates experiment seeds, or supports a solve claim.</p>
<ul>
<li>Annotation tasks: {summary.get('task_count')}</li>
<li>Cuneiform tasks: {summary.get('cuneiform_task_count')}</li>
<li>Dot tasks: {summary.get('dot_task_count')}</li>
<li>Delimiter tasks: {summary.get('delimiter_task_count')}</li>
<li>Negative-control tasks: {summary.get('negative_control_task_count')}</li>
<li>Unresolved page references: {summary.get('unresolved_page_reference_count')}</li>
</ul>
<p><a href="annotation_manifest.yaml">Annotation manifest</a> | <a href="SFTP_UPLOAD_INSTRUCTIONS.md">Local upload/use notes</a></p>
{sections}
"""
    (site_dir / "index.html").write_text(
        _html_page("Stage 4C Visual Annotation Pack", body, "assets/site.css"),
        encoding="utf-8",
        newline="\n",
    )


def _write_css(path: Path) -> None:
    path.write_text(
        "body{font-family:system-ui,sans-serif;line-height:1.45;margin:2rem;color:#1f2528;background:#fbfbf8}"
        "a{color:#2459a6}.notice{border-left:4px solid #9a6b00;background:#fff7dd;padding:.8rem}"
        "img{max-width:100%;height:auto;border:1px solid #ccd3d8;background:white}dt{font-weight:700}",
        encoding="utf-8",
        newline="\n",
    )


def _write_sftp(path: Path) -> None:
    path.write_text(
        "# Stage 4C Annotation Site Notes\n\n"
        "This is a generated local review workspace. Upload only if a human reviewer needs static access.\n\n"
        "- Do not upload `third_party/`.\n"
        "- Do not upload raw page-image directories.\n"
        "- Keep generated templates blank until a reviewer fills them locally.\n"
        "- Coordinate annotations record regions only; readings require separate review.\n",
        encoding="utf-8",
        newline="\n",
    )


def _html_page(title: str, body: str, css_href: str) -> str:
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        f"{NOINDEX_META}<title>{escape(title)}</title><link rel=\"stylesheet\" href=\"{css_href}\">"
        f"</head><body>{body}</body></html>\n"
    )


def _task_link(task_id: str) -> str:
    return f'<li><a href="tasks/{escape(task_id)}.html">{escape(task_id)}</a></li>'


def _image_html(src: str, alt: str) -> str:
    if not src:
        return "<p>Image copy unavailable in this generated site.</p>"
    return f'<figure><img src="{escape(src)}" alt="{escape(alt)}"><figcaption>{escape(alt)}</figcaption></figure>'


def _manifest_yaml(payload: dict[str, Any]) -> str:
    lines = []
    for key, value in payload.items():
        if isinstance(value, bool):
            rendered = str(value).lower()
        else:
            rendered = str(value)
        lines.append(f"{key}: {rendered}")
    return "\n".join(lines) + "\n"
