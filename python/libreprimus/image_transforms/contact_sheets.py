"""Contact sheet generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from libreprimus.image_transforms.export import sha256_file
from libreprimus.image_transforms.loader import display_path
from libreprimus.image_transforms.models import CONTACT_TRANSFORMS

THUMB_SIZE = (180, 140)
LABEL_HEIGHT = 22


def create_contact_sheet(
    *,
    image_id: str,
    transform_outputs: dict[str, Path],
    out_path: Path,
    generated_at: str,
) -> dict[str, Any]:
    """Create a per-image contact sheet from selected transforms."""
    selected = [(name, transform_outputs[name]) for name in CONTACT_TRANSFORMS if name in transform_outputs]
    if not selected:
        selected = list(transform_outputs.items())[:1]
    sheet = _sheet_from_entries(selected)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)
    return {
        "record_type": "contact_sheet_record",
        "contact_sheet_id": f"{image_id}-contact-sheet",
        "image_id": image_id,
        "output_relative_path": display_path(out_path),
        "output_sha256": sha256_file(out_path),
        "included_transforms": [name for name, _ in selected],
        "thumbnail_count": len(selected),
        "generated_at_utc": generated_at,
        "trusted_as_canonical": False,
        "solve_claim": False,
    }


def create_global_contact_sheet(
    *,
    sheet_entries: list[tuple[str, Path]],
    out_path: Path,
    generated_at: str,
) -> dict[str, Any]:
    """Create a global contact sheet from per-image sheets."""
    selected = sheet_entries[:120]
    sheet = _sheet_from_entries(selected, columns=5)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)
    return {
        "record_type": "contact_sheet_record",
        "contact_sheet_id": "stage3p-global-contact-sheet",
        "image_id": "all-images",
        "output_relative_path": display_path(out_path),
        "output_sha256": sha256_file(out_path),
        "included_transforms": [name for name, _ in selected],
        "thumbnail_count": len(selected),
        "generated_at_utc": generated_at,
        "trusted_as_canonical": False,
        "solve_claim": False,
    }


def _sheet_from_entries(entries: list[tuple[str, Path]], *, columns: int = 4) -> Image.Image:
    rows = (len(entries) + columns - 1) // columns
    width = columns * THUMB_SIZE[0]
    height = max(1, rows) * (THUMB_SIZE[1] + LABEL_HEIGHT)
    sheet = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (label, path) in enumerate(entries):
        col = index % columns
        row = index // columns
        x = col * THUMB_SIZE[0]
        y = row * (THUMB_SIZE[1] + LABEL_HEIGHT)
        with Image.open(path) as image:
            image.thumbnail(THUMB_SIZE)
            paste_x = x + (THUMB_SIZE[0] - image.width) // 2
            paste_y = y + (THUMB_SIZE[1] - image.height) // 2
            sheet.paste(image.convert("RGB"), (paste_x, paste_y))
        draw.text((x + 4, y + THUMB_SIZE[1] + 3), label[:28], fill=(0, 0, 0))
    return sheet
