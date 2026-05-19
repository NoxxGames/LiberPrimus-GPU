"""Cheap deterministic compression artifact metrics for Stage 4M."""

from __future__ import annotations

from pathlib import Path
from statistics import fmean
from typing import Any

from libreprimus.image_preflight.models import COMMON_FALSE_FLAGS

try:  # Pillow is already used by image stages, but validation should degrade clearly.
    from PIL import Image, ImageChops, ImageFilter, ImageStat
except ImportError:  # pragma: no cover - covered by explicit read_failed behavior when absent.
    Image = None  # type: ignore[assignment]
    ImageChops = None  # type: ignore[assignment]
    ImageFilter = None  # type: ignore[assignment]
    ImageStat = None  # type: ignore[assignment]


def compression_record(metadata: dict[str, Any], *, repo_root: Path) -> dict[str, Any]:
    """Build deterministic compression metric record for one metadata record."""

    path = Path(str(metadata["relative_path"]))
    if not path.is_absolute():
        path = repo_root / path
    base = {
        "record_type": "image_compression_preflight_record",
        "compression_record_id": f"stage4m-compression-{metadata['image_id']}",
        "image_id": metadata["image_id"],
        "relative_path": metadata["relative_path"],
        "file_name": metadata["file_name"],
        "sha256": metadata["sha256"],
        "file_size_bytes": metadata["file_size_bytes"],
        "width": metadata["width"],
        "height": metadata["height"],
        "color_mode": metadata["color_mode"],
        "image_format": metadata["image_format"],
        "metric_only": True,
        **COMMON_FALSE_FLAGS,
    }
    if Image is None:
        return {
            **base,
            "compression_metric_status": "read_failed",
            "blockiness_proxy": None,
            "jpeg_grid_artifact_score": None,
            "noise_residual_mean": None,
            "edge_residual_mean": None,
            "channel_histogram_summary": {},
            "bitplane_summary": {},
            "jpeg_like_metric_flag": False,
            "notes": "Pillow unavailable; no image interpretation attempted.",
        }
    try:
        with Image.open(path) as opened:
            image = opened.convert("RGB")
            gray = opened.convert("L")
            image.thumbnail((768, 768))
            gray.thumbnail((768, 768))
            blockiness = _blockiness_proxy(gray)
            noise_mean, noise_max = _noise_residual(gray)
            edge_mean = _edge_residual(gray)
            histogram = _channel_histogram_summary(image)
            bitplanes = _bitplane_summary(gray)
    except Exception as error:  # noqa: BLE001 - deterministic record should preserve failure state.
        return {
            **base,
            "compression_metric_status": "read_failed",
            "blockiness_proxy": None,
            "jpeg_grid_artifact_score": None,
            "noise_residual_mean": None,
            "edge_residual_mean": None,
            "channel_histogram_summary": {},
            "bitplane_summary": {},
            "jpeg_like_metric_flag": False,
            "notes": f"metric read failed: {error}",
        }
    jpeg_like = metadata["image_format"] == "JPEG" or blockiness >= 1.2
    return {
        **base,
        "compression_metric_status": "computed",
        "blockiness_proxy": blockiness,
        "jpeg_grid_artifact_score": blockiness,
        "noise_residual_mean": noise_mean,
        "noise_residual_max": noise_max,
        "edge_residual_mean": edge_mean,
        "channel_histogram_summary": histogram,
        "bitplane_summary": bitplanes,
        "jpeg_like_metric_flag": jpeg_like,
        "notes": "Metric-only preflight; no hidden-message or intentionality claim.",
    }


def build_compression_records(metadata_records: list[dict[str, Any]], *, repo_root: Path) -> list[dict[str, Any]]:
    """Build metric records for all image metadata records."""

    return [compression_record(record, repo_root=repo_root) for record in metadata_records]


def _blockiness_proxy(gray: Any) -> float:
    width, height = gray.size
    pixels = gray.load()
    boundary: list[int] = []
    interior: list[int] = []
    for x in range(1, width):
        target = boundary if x % 8 == 0 else interior
        for y in range(height):
            target.append(abs(int(pixels[x, y]) - int(pixels[x - 1, y])))
    for y in range(1, height):
        target = boundary if y % 8 == 0 else interior
        for x in range(width):
            target.append(abs(int(pixels[x, y]) - int(pixels[x, y - 1])))
    boundary_mean = fmean(boundary) if boundary else 0.0
    interior_mean = fmean(interior) if interior else 0.0
    if interior_mean <= 0.0:
        return round(boundary_mean, 6)
    return round(boundary_mean / interior_mean, 6)


def _noise_residual(gray: Any) -> tuple[float, int]:
    blurred = gray.filter(ImageFilter.BoxBlur(1))
    residual = ImageChops.difference(gray, blurred)
    stat = ImageStat.Stat(residual)
    extrema = residual.getextrema()
    return round(float(stat.mean[0]), 6), int(extrema[1])


def _edge_residual(gray: Any) -> float:
    width, height = gray.size
    pixels = gray.load()
    values: list[int] = []
    for y in range(0, height, max(1, height // 256)):
        for x in range(1, width, max(1, width // 256)):
            values.append(abs(int(pixels[x, y]) - int(pixels[x - 1, y])))
    for x in range(0, width, max(1, width // 256)):
        for y in range(1, height, max(1, height // 256)):
            values.append(abs(int(pixels[x, y]) - int(pixels[x, y - 1])))
    return round(fmean(values) if values else 0.0, 6)


def _channel_histogram_summary(image: Any) -> dict[str, dict[str, float | int]]:
    summaries: dict[str, dict[str, float | int]] = {}
    total = max(1, image.size[0] * image.size[1])
    for name, channel in zip(("red", "green", "blue"), image.split(), strict=True):
        hist = channel.histogram()
        bins = [sum(hist[index : index + 16]) for index in range(0, 256, 16)]
        max_bin = max(bins) if bins else 0
        summaries[name] = {
            "bin_count": len(bins),
            "max_bin_ratio": round(max_bin / total, 6),
            "first_bin_ratio": round((bins[0] if bins else 0) / total, 6),
            "last_bin_ratio": round((bins[-1] if bins else 0) / total, 6),
        }
    return summaries


def _bitplane_summary(gray: Any) -> dict[str, float]:
    data = list(gray.getdata())
    total = max(1, len(data))
    return {f"bit_{bit}_one_ratio": round(sum((value >> bit) & 1 for value in data) / total, 6) for bit in range(8)}
