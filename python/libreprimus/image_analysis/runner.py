"""Stage 3M deterministic local page-image analysis runner."""

from __future__ import annotations

from datetime import UTC, datetime
import hashlib
from pathlib import Path
from typing import Any

from PIL import Image

from libreprimus.image_analysis.bitplanes import bitplane_records
from libreprimus.image_analysis.export import read_jsonl, write_json, write_jsonl
from libreprimus.image_analysis.features import feature_candidates
from libreprimus.image_analysis.grayscale_stats import (
    average_hash_8x8,
    border_statistics,
    channel_statistics,
    foreground_bbox,
    histogram_stats,
    to_grayscale,
)
from libreprimus.image_analysis.primes import is_prime
from libreprimus.image_analysis.symmetry import symmetry_record
from libreprimus.image_analysis.thresholds import DEFAULT_THRESHOLDS, threshold_and_component_records
from libreprimus.paths import repo_root

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
DEFAULT_SOURCE_ID = "local-liber-primus-pages-stage3m"
RUN_ID = "stage3m-deterministic-local-image-analysis"


def analyze_local_pages(
    *,
    source_dir: Path,
    image_locks: Path,
    out_dir: Path,
    allow_missing: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Analyze local page images and write ignored generated records."""
    resolved_source = _resolve(source_dir)
    resolved_locks = _resolve(image_locks)
    resolved_out = _resolve(out_dir)
    warnings: list[str] = []
    image_paths: list[Path] = []
    if resolved_source.is_dir():
        image_paths = sorted(
            path
            for path in resolved_source.rglob("*")
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
        )
    elif allow_missing:
        warnings.append("source_dir_missing_analysis_skipped")
    else:
        raise FileNotFoundError(resolved_source)

    lock_by_relative_path = _load_locks(resolved_locks)
    analysis_records: list[dict[str, Any]] = []
    threshold_records: list[dict[str, Any]] = []
    symmetry_records: list[dict[str, Any]] = []
    bitplane_records_all: list[dict[str, Any]] = []
    component_records: list[dict[str, Any]] = []
    feature_records: list[dict[str, Any]] = []

    for image_path in image_paths:
        relative_path = _display_path(image_path)
        data = image_path.read_bytes()
        sha256 = hashlib.sha256(data).hexdigest()
        lock_record = lock_by_relative_path.get(relative_path, {})
        if lock_record and lock_record.get("sha256") != sha256:
            warnings.append(f"{relative_path}: image_lock_sha256_mismatch")
        elif not lock_record:
            warnings.append(f"{relative_path}: image_lock_missing")

        with Image.open(image_path) as image:
            image.load()
            analysis_record, thresholds, components, symmetry, bitplanes = _analyze_image(
                image=image,
                image_path=image_path,
                relative_path=relative_path,
                sha256=sha256,
                file_size_bytes=len(data),
                lock_record=lock_record,
            )
        features = feature_candidates(
            analysis_record=analysis_record,
            threshold_records=thresholds,
            symmetry_record=symmetry,
            bitplane_records=bitplanes,
        )
        analysis_records.append(analysis_record)
        threshold_records.extend(thresholds)
        component_records.extend(components)
        symmetry_records.append(symmetry)
        bitplane_records_all.extend(bitplanes)
        feature_records.extend(features)

    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    output_paths = {
        "image_analysis_records": _display_path(resolved_out / "image_analysis_records.jsonl"),
        "threshold_summary_records": _display_path(resolved_out / "threshold_summary_records.jsonl"),
        "symmetry_records": _display_path(resolved_out / "symmetry_records.jsonl"),
        "bitplane_summary_records": _display_path(resolved_out / "bitplane_summary_records.jsonl"),
        "component_summary_records": _display_path(resolved_out / "component_summary_records.jsonl"),
        "visual_feature_candidates": _display_path(resolved_out / "visual_feature_candidates.jsonl"),
        "summary": _display_path(resolved_out / "summary.json"),
        "warnings": _display_path(resolved_out / "warnings.jsonl"),
    }
    summary = _build_summary(
        generated_at=generated_at,
        analysis_records=analysis_records,
        threshold_records=threshold_records,
        component_records=component_records,
        symmetry_records=symmetry_records,
        bitplane_records=bitplane_records_all,
        feature_records=feature_records,
        output_paths=output_paths,
        warnings=warnings,
    )
    resolved_out.mkdir(parents=True, exist_ok=True)
    write_jsonl(resolved_out / "image_analysis_records.jsonl", analysis_records)
    write_jsonl(resolved_out / "threshold_summary_records.jsonl", threshold_records)
    write_jsonl(resolved_out / "symmetry_records.jsonl", symmetry_records)
    write_jsonl(resolved_out / "bitplane_summary_records.jsonl", bitplane_records_all)
    write_jsonl(resolved_out / "component_summary_records.jsonl", component_records)
    write_jsonl(resolved_out / "visual_feature_candidates.jsonl", feature_records)
    write_jsonl(resolved_out / "warnings.jsonl", [{"warning": warning} for warning in warnings])
    write_json(resolved_out / "summary.json", summary)

    if warnings and not allow_warnings:
        raise RuntimeError("; ".join(warnings))
    return summary


def _analyze_image(
    *,
    image: Image.Image,
    image_path: Path,
    relative_path: str,
    sha256: str,
    file_size_bytes: int,
    lock_record: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    gray = to_grayscale(image)
    image_id = f"liber-primus-page-image-{image_path.stem}"
    source_id = str(lock_record.get("source_id") or DEFAULT_SOURCE_ID)
    stats = histogram_stats(gray)
    width_is_prime = is_prime(image.width)
    height_is_prime = is_prime(image.height)
    analysis_record: dict[str, Any] = {
        "record_type": "image_analysis_record",
        "image_id": image_id,
        "source_id": source_id,
        "image_sha256": sha256,
        "relative_path": relative_path,
        "file_name": image_path.name,
        "file_size_bytes": file_size_bytes,
        "width": image.width,
        "height": image.height,
        "image_format": str(image.format or "UNKNOWN"),
        "color_mode": image.mode,
        "width_is_prime": width_is_prime,
        "height_is_prime": height_is_prime,
        "both_dimensions_prime": width_is_prime and height_is_prime,
        **stats,
        "channel_statistics": channel_statistics(image),
        "border_statistics": border_statistics(gray),
        "foreground_bbox": foreground_bbox(gray),
        "average_hash_8x8": average_hash_8x8(gray),
        "trusted_as_canonical": False,
        "solve_claim": False,
        "notes": "Deterministic Stage 3M local image features only; no OCR, AI, or image-derived cipher run.",
    }
    thresholds, components = threshold_and_component_records(image_id, gray)
    symmetry = symmetry_record(image_id, gray)
    bitplanes = bitplane_records(image_id, gray)
    return analysis_record, thresholds, components, symmetry, bitplanes


def _build_summary(
    *,
    generated_at: str,
    analysis_records: list[dict[str, Any]],
    threshold_records: list[dict[str, Any]],
    component_records: list[dict[str, Any]],
    symmetry_records: list[dict[str, Any]],
    bitplane_records: list[dict[str, Any]],
    feature_records: list[dict[str, Any]],
    output_paths: dict[str, str],
    warnings: list[str],
) -> dict[str, Any]:
    feature_counts: dict[str, int] = {}
    for record in feature_records:
        feature_type = str(record["feature_type"])
        feature_counts[feature_type] = feature_counts.get(feature_type, 0) + 1

    def symmetry_score(record: dict[str, Any]) -> float:
        return min(
            float(record["horizontal_mirror_difference"]),
            float(record["vertical_mirror_difference"]),
            float(record["rotational_180_difference"]),
        )

    top_symmetric = [record["image_id"] for record in sorted(symmetry_records, key=symmetry_score)[:10]]
    top_asymmetric = [record["image_id"] for record in sorted(symmetry_records, key=symmetry_score, reverse=True)[:10]]
    sparse = [
        record["image_id"]
        for record in sorted(
            (item for item in feature_records if item["feature_type"] == "sparse_dot_like_candidate"),
            key=lambda item: float(item["feature_score"]),
            reverse=True,
        )[:10]
    ]
    return {
        "record_type": "image_analysis_run_summary",
        "run_id": RUN_ID,
        "generated_at_utc": generated_at,
        "image_count": len(analysis_records),
        "threshold_values": list(DEFAULT_THRESHOLDS),
        "symmetry_metrics": [
            "horizontal_mirror_difference",
            "vertical_mirror_difference",
            "rotational_180_difference",
        ],
        "component_record_count": len(component_records),
        "symmetry_record_count": len(symmetry_records),
        "bitplane_record_count": len(bitplane_records),
        "threshold_record_count": len(threshold_records),
        "feature_candidate_count": len(feature_records),
        "feature_counts": feature_counts,
        "top_symmetric_image_ids": top_symmetric,
        "top_asymmetric_image_ids": top_asymmetric,
        "top_sparse_dot_like_image_ids": sparse,
        "output_paths": output_paths,
        "warnings": warnings,
        "trusted_as_canonical": False,
        "solve_claim": False,
        "notes": "Generated Stage 3M summary; feature candidates are review aids only.",
    }


def _load_locks(path: Path) -> dict[str, dict[str, Any]]:
    records = read_jsonl(path)
    return {str(record.get("relative_path")): record for record in records if record.get("relative_path")}


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
