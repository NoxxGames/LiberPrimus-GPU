"""Coordinate-grid overlay generation for Stage 4C annotation pages."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


def write_grid_overlay(source: Path, target: Path, *, max_size: int = 1200, grid_step: int = 100) -> tuple[int, int]:
    """Write a generated image copy with pixel-ruler grid overlays."""

    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image.thumbnail((max_size, max_size))
        canvas = image.convert("RGB")
    draw = ImageDraw.Draw(canvas)
    width, height = canvas.size
    for x_pos in range(0, width, grid_step):
        draw.line((x_pos, 0, x_pos, height), fill=(220, 40, 40), width=1)
        draw.text((x_pos + 3, 3), str(x_pos), fill=(220, 40, 40))
    for y_pos in range(0, height, grid_step):
        draw.line((0, y_pos, width, y_pos), fill=(40, 80, 220), width=1)
        draw.text((3, y_pos + 3), str(y_pos), fill=(40, 80, 220))
    canvas.save(target)
    return width, height
