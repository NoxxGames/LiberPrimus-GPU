"""Deterministic synthetic JPEG controls for stego tests and local runs."""

from __future__ import annotations

from pathlib import Path


def write_synthetic_image(kind: str, path: Path) -> Path:
    """Write a deterministic JPEG control image."""
    try:
        from PIL import Image
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("Pillow is required for synthetic JPEG controls") from exc
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (64, 64), color=(240, 240, 240))
    pixels = image.load()
    for y in range(64):
        for x in range(64):
            if kind == "clean_jpeg":
                value = 220 if (x // 8 + y // 8) % 2 == 0 else 245
                pixels[x, y] = (value, value, value)
            elif kind == "noise_jpeg":
                r = (x * 37 + y * 17) % 256
                g = (x * 11 + y * 53) % 256
                b = (x * 71 + y * 7) % 256
                pixels[x, y] = (r, g, b)
            else:
                raise ValueError(f"unsupported synthetic image kind: {kind}")
    image.save(path, format="JPEG", quality=90)
    return path
