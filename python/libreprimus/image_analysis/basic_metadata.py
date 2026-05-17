"""Dependency-light PNG/JPEG metadata extraction."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import struct


@dataclass(frozen=True)
class ImageMetadata:
    image_format: str
    width: int
    height: int
    color_mode: str


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SOF_MARKERS = {
    0xC0,
    0xC1,
    0xC2,
    0xC3,
    0xC5,
    0xC6,
    0xC7,
    0xC9,
    0xCA,
    0xCB,
    0xCD,
    0xCE,
    0xCF,
}


def read_image_metadata(path: Path) -> ImageMetadata:
    """Read basic metadata from a PNG or JPEG file without heavyweight dependencies."""
    data = path.read_bytes()
    if data.startswith(PNG_SIGNATURE):
        return _read_png_metadata(data, path)
    if data.startswith(b"\xff\xd8"):
        return _read_jpeg_metadata(data, path)
    raise ValueError(f"Unsupported image format: {path}")


def _read_png_metadata(data: bytes, path: Path) -> ImageMetadata:
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError(f"PNG IHDR chunk missing: {path}")
    width, height = struct.unpack(">II", data[16:24])
    color_type = data[25]
    color_mode = {
        0: "L",
        2: "RGB",
        3: "P",
        4: "LA",
        6: "RGBA",
    }.get(color_type, f"png_color_type_{color_type}")
    return ImageMetadata("PNG", width, height, color_mode)


def _read_jpeg_metadata(data: bytes, path: Path) -> ImageMetadata:
    cursor = 2
    while cursor < len(data):
        while cursor < len(data) and data[cursor] != 0xFF:
            cursor += 1
        while cursor < len(data) and data[cursor] == 0xFF:
            cursor += 1
        if cursor >= len(data):
            break
        marker = data[cursor]
        cursor += 1
        if marker in {0xD8, 0xD9} or 0xD0 <= marker <= 0xD7:
            continue
        if cursor + 2 > len(data):
            break
        segment_length = int.from_bytes(data[cursor : cursor + 2], "big")
        if segment_length < 2 or cursor + segment_length > len(data):
            break
        if marker in JPEG_SOF_MARKERS:
            segment = data[cursor + 2 : cursor + segment_length]
            if len(segment) < 6:
                break
            height = int.from_bytes(segment[1:3], "big")
            width = int.from_bytes(segment[3:5], "big")
            component_count = segment[5]
            color_mode = {1: "L", 3: "RGB", 4: "CMYK"}.get(
                component_count, f"jpeg_components_{component_count}"
            )
            return ImageMetadata("JPEG", width, height, color_mode)
        cursor += segment_length
    raise ValueError(f"JPEG SOF marker missing: {path}")
