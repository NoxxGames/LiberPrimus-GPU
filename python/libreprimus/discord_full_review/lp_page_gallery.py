"""Liber Primus page-image gallery generation for Stage 4A."""

from __future__ import annotations

from pathlib import Path
import shutil
from typing import Any

from PIL import Image, ImageDraw

from libreprimus.discord_full_review.export import display_path, sha256_file
from libreprimus.discord_full_review.models import IMAGE_SUFFIXES
from libreprimus.discord_full_review.static_site import html_page, privacy_notice_html

THUMB_SIZE = (220, 220)


def build_lp_page_gallery(*, lp_pages_dir: Path, out_dir: Path, site_dir: Path) -> list[dict[str, Any]]:
    image_paths = sorted(
        path for path in lp_pages_dir.rglob("*") if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    ) if lp_pages_dir.is_dir() else []
    thumbnails_dir = site_dir / "lp-pages" / "thumbnails"
    full_dir = site_dir / "lp-pages" / "full"
    contact_dir = site_dir / "lp-pages" / "contact-sheets"
    thumbnails_dir.mkdir(parents=True, exist_ok=True)
    full_dir.mkdir(parents=True, exist_ok=True)
    contact_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    sheet_entries: list[tuple[str, Path]] = []
    for index, source in enumerate(image_paths, start=1):
        image_id = f"lp-page-{index:03d}"
        thumb_name = f"{image_id}.jpg"
        full_name = source.name
        thumb_path = thumbnails_dir / thumb_name
        full_path = full_dir / full_name
        with Image.open(source) as image:
            width, height = image.size
            thumb = image.convert("RGB")
            thumb.thumbnail(THUMB_SIZE)
            thumb.save(thumb_path, "JPEG", quality=85)
        shutil.copy2(source, full_path)
        sheet_entries.append((image_id, thumb_path))
        records.append(
            {
                "record_type": "lp_page_gallery_record",
                "image_id": image_id,
                "source_relative_path": display_path(source),
                "source_sha256": sha256_file(source),
                "file_name": source.name,
                "width": width,
                "height": height,
                "thumbnail_relative_path": display_path(thumb_path),
                "full_copy_relative_path": display_path(full_path),
                "site_page_relative_path": "site/lp-pages/index.html",
                "raw_source_committed": False,
                "generated_copy_committed": False,
                "solve_claim": False,
                "usable_as_experiment_seed": False,
            }
        )
    if sheet_entries:
        _write_contact_sheet(sheet_entries, contact_dir / "lp-pages-contact-sheet.jpg")
    _write_gallery_index(site_dir / "lp-pages" / "index.html", records)
    return records


def _write_gallery_index(path: Path, records: list[dict[str, Any]]) -> None:
    cards = "\n".join(
        "<figure>"
        f"<a href=\"full/{record['file_name']}\"><img src=\"thumbnails/{Path(record['thumbnail_relative_path']).name}\" alt=\"{record['image_id']}\"></a>"
        f"<figcaption>{record['image_id']} {record['file_name']} {record['width']}x{record['height']}</figcaption>"
        "</figure>"
        for record in records
    )
    path.write_text(
        html_page(
            "LP Page Gallery",
            "<h1>Liber Primus Page Image Gallery</h1>"
            f"{privacy_notice_html()}"
            "<p>Generated ignored local gallery. Source page images remain uncommitted.</p>"
            f"<div class=\"gallery\">{cards}</div>"
            "<p><a href=\"../index.html\">Back to site index</a></p>",
            css_href="../assets/site.css",
        ),
        encoding="utf-8",
        newline="\n",
    )


def _write_contact_sheet(entries: list[tuple[str, Path]], out_path: Path) -> None:
    columns = 6
    cell_w, cell_h = 240, 260
    rows = (len(entries) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_w, max(1, rows) * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (label, thumb_path) in enumerate(entries):
        col = index % columns
        row = index // columns
        x, y = col * cell_w, row * cell_h
        with Image.open(thumb_path) as image:
            paste_x = x + (cell_w - image.width) // 2
            sheet.paste(image.convert("RGB"), (paste_x, y + 8))
        draw.text((x + 8, y + cell_h - 28), label, fill=(0, 0, 0))
    sheet.save(out_path, "JPEG", quality=85)
