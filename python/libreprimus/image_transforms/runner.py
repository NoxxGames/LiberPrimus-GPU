"""Stage 3P deterministic image-transform runner."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
import hashlib
from pathlib import Path
from typing import Any

from PIL import Image

from libreprimus.image_analysis.components import component_summary
from libreprimus.image_analysis.grayscale_stats import border_statistics, to_grayscale
from libreprimus.image_transforms import RUN_ID
from libreprimus.image_transforms.basic_transforms import basic_transform_images
from libreprimus.image_transforms.bitplanes import bitplane_transform_images
from libreprimus.image_transforms.candidate_flags import build_candidate_flags
from libreprimus.image_transforms.channel_transforms import channel_transform_images
from libreprimus.image_transforms.components_overlay import component_overlay_images
from libreprimus.image_transforms.contact_sheets import (
    create_contact_sheet,
    create_global_contact_sheet,
)
from libreprimus.image_transforms.edges import difference_edge_map
from libreprimus.image_transforms.export import sha256_file, write_json, write_jsonl
from libreprimus.image_transforms.loader import (
    display_path,
    iter_image_paths,
    load_image,
    load_image_locks,
)
from libreprimus.image_transforms.models import THRESHOLDS
from libreprimus.image_transforms.review_index import write_review_pages
from libreprimus.image_transforms.split_mirror import split_mirror_transform_images
from libreprimus.paths import repo_root

REVIEW_MAX_DIMENSION = 900


def run_local_page_transforms(
    *,
    source_dir: Path,
    image_locks: Path,
    out_dir: Path,
    allow_missing: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Generate deterministic review transforms for local Liber Primus page images."""
    resolved_source = _resolve(source_dir)
    resolved_locks = _resolve(image_locks)
    resolved_out = _resolve(out_dir)
    warnings: list[str] = []

    if resolved_source.is_dir():
        image_paths = iter_image_paths(resolved_source)
    elif allow_missing:
        image_paths = []
        warnings.append("source_dir_missing_transform_run_skipped")
    else:
        raise FileNotFoundError(resolved_source)

    locks = load_image_locks(resolved_locks)
    generated_at = _utc_now()
    transform_records: list[dict[str, Any]] = []
    metric_records: list[dict[str, Any]] = []
    candidate_records: list[dict[str, Any]] = []
    contact_records: list[dict[str, Any]] = []
    image_summaries: list[dict[str, Any]] = []
    per_image_sheets: list[tuple[str, Path]] = []

    for image_path in image_paths:
        image_summary = _process_image(
            image_path=image_path,
            locks=locks,
            out_dir=resolved_out,
            generated_at=generated_at,
            transform_records=transform_records,
            metric_records=metric_records,
            candidate_records=candidate_records,
            contact_records=contact_records,
            warnings=warnings,
        )
        image_summaries.append(image_summary)
        per_image_sheets.append((image_summary["image_id"], _resolve(Path(image_summary["contact_sheet"]))))

    global_sheet_path = resolved_out / "contact_sheets" / "stage3p-global-contact-sheet.jpg"
    global_contact = create_global_contact_sheet(
        sheet_entries=per_image_sheets,
        out_path=global_sheet_path,
        generated_at=generated_at,
    )
    contact_records.append(global_contact)
    review_index_path, review_page_count = write_review_pages(
        out_dir=resolved_out,
        image_summaries=image_summaries,
        global_contact_sheet=global_contact["output_relative_path"],
    )
    summary = _build_summary(
        generated_at=generated_at,
        image_count=len(image_paths),
        transform_records=transform_records,
        metric_records=metric_records,
        candidate_records=candidate_records,
        contact_records=contact_records,
        review_page_count=review_page_count,
        review_index_path=review_index_path,
        warnings=warnings,
    )
    resolved_out.mkdir(parents=True, exist_ok=True)
    write_jsonl(resolved_out / "transform_records.jsonl", transform_records)
    write_jsonl(resolved_out / "transform_metric_records.jsonl", metric_records)
    write_jsonl(resolved_out / "visual_transform_candidates.jsonl", candidate_records)
    write_jsonl(resolved_out / "contact_sheet_manifest.jsonl", contact_records)
    write_jsonl(resolved_out / "warnings.jsonl", [{"warning": warning} for warning in warnings])
    write_json(resolved_out / "summary.json", summary)

    if warnings and not allow_warnings:
        raise RuntimeError("; ".join(warnings))
    return summary


def _process_image(
    *,
    image_path: Path,
    locks: dict[str, dict[str, Any]],
    out_dir: Path,
    generated_at: str,
    transform_records: list[dict[str, Any]],
    metric_records: list[dict[str, Any]],
    candidate_records: list[dict[str, Any]],
    contact_records: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    source_bytes = image_path.read_bytes()
    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
    relative_path = display_path(image_path)
    lock = locks.get(relative_path, {})
    if lock and lock.get("sha256") != source_sha256:
        warnings.append(f"{relative_path}: image_lock_sha256_mismatch")
    elif not lock:
        warnings.append(f"{relative_path}: image_lock_missing")

    image = load_image(image_path)
    review_image = _review_image(image)
    if review_image.size != image.size:
        warnings.append(
            f"{relative_path}: transform previews downscaled from {image.width}x{image.height} "
            f"to {review_image.width}x{review_image.height}"
        )
    image_id = f"liber-primus-page-image-{image_path.stem}"
    derived_dir = out_dir / "derived_images" / image_id
    transforms, image_warnings = _all_transforms(review_image)
    warnings.extend(f"{relative_path}: {warning}" for warning in image_warnings)
    transform_outputs: dict[str, Path] = {}
    output_references: dict[str, str] = {}
    metric_values: dict[str, float] = {}

    for transform_name, parameters, transformed, metrics in transforms:
        output_path = derived_dir / f"{transform_name}.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_image = transformed.convert("RGB") if transformed.mode not in {"L", "RGB", "RGBA"} else transformed
        save_image.save(output_path)
        output_sha256 = sha256_file(output_path)
        transform_records.append(
            {
                "record_type": "image_transform_record",
                "transform_record_id": f"{image_id}-{transform_name}",
                "image_id": image_id,
                "source_image_sha256": source_sha256,
                "transform_name": transform_name,
                "transform_parameters": parameters,
                "output_relative_path": display_path(output_path),
                "output_sha256": output_sha256,
                "output_width": transformed.width,
                "output_height": transformed.height,
                "generated_at_utc": generated_at,
                "trusted_as_canonical": False,
                "usable_as_experiment_seed": False,
                "solve_claim": False,
                "notes": "Generated deterministic review transform; not source truth or cipher output.",
            }
        )
        transform_outputs[transform_name] = output_path
        output_references[transform_name] = display_path(output_path)
        for metric_name, metric_value in metrics.items():
            metric_values[f"{transform_name}_{metric_name}"] = float(metric_value)
            metric_records.append(_metric_record(image_id, transform_name, metric_name, metric_value))

    _add_threshold_metrics(image_id, review_image, metric_values, metric_records)
    _add_border_metrics(image_id, review_image, metric_values, metric_records)
    candidates = build_candidate_flags(
        image_id=image_id,
        metrics=metric_values,
        output_references=output_references,
    )
    candidate_records.extend(candidates)
    sheet_path = out_dir / "contact_sheets" / f"{image_id}.jpg"
    contact = create_contact_sheet(
        image_id=image_id,
        transform_outputs=transform_outputs,
        out_path=sheet_path,
        generated_at=generated_at,
    )
    contact_records.append(contact)
    return {
        "image_id": image_id,
        "file_name": image_path.name,
        "contact_sheet": contact["output_relative_path"],
        "candidate_types": [candidate["feature_type"] for candidate in candidates],
    }


def _all_transforms(image: Image.Image) -> tuple[list[tuple[str, dict, Image.Image, dict[str, float]]], list[str]]:
    transforms: list[tuple[str, dict, Image.Image, dict[str, float]]] = []
    warnings: list[str] = []
    transforms.extend((name, params, output, {}) for name, params, output in basic_transform_images(image))
    channels, channel_warnings = channel_transform_images(image)
    warnings.extend(channel_warnings)
    transforms.extend((name, params, output, {}) for name, params, output in channels)
    transforms.extend(bitplane_transform_images(image))
    edge, edge_metrics = difference_edge_map(image)
    transforms.append(("edge_difference", {}, edge, edge_metrics))
    transforms.extend(split_mirror_transform_images(image))
    transforms.extend(component_overlay_images(image))
    return transforms, warnings


def _review_image(image: Image.Image) -> Image.Image:
    """Return a bounded deterministic preview image for Stage 3P review artefacts."""
    width, height = image.size
    largest = max(width, height)
    if largest <= REVIEW_MAX_DIMENSION:
        return image.copy()
    scale = REVIEW_MAX_DIMENSION / largest
    resized = (max(1, round(width * scale)), max(1, round(height * scale)))
    resample = getattr(Image, "Resampling", Image).LANCZOS
    return image.resize(resized, resample=resample)


def _add_threshold_metrics(
    image_id: str,
    image: Image.Image,
    metric_values: dict[str, float],
    metric_records: list[dict[str, Any]],
) -> None:
    gray = to_grayscale(image)
    pixels = list(gray.getdata())
    total = max(1, len(pixels))
    for threshold in THRESHOLDS:
        foreground_ratio = sum(1 for pixel in pixels if pixel <= threshold) / total
        metric_values[f"threshold_{threshold}_foreground_ratio"] = foreground_ratio
        metric_records.append(
            _metric_record(image_id, f"threshold_{threshold}", "foreground_ratio", foreground_ratio)
        )


def _add_border_metrics(
    image_id: str,
    image: Image.Image,
    metric_values: dict[str, float],
    metric_records: list[dict[str, Any]],
) -> None:
    stats = border_statistics(to_grayscale(image))
    ratios = [
        float(stats["top_dark_ratio"]),
        float(stats["bottom_dark_ratio"]),
        float(stats["left_dark_ratio"]),
        float(stats["right_dark_ratio"]),
    ]
    border_dark_ratio = max(ratios)
    metric_values["border_dark_ratio"] = border_dark_ratio
    metric_records.append(_metric_record(image_id, "border_statistics", "border_dark_ratio", border_dark_ratio))

    for threshold in (64, 128, 192):
        summary = component_summary(to_grayscale(image), threshold=threshold)
        key = f"component_overlay_{threshold}_largest_component_area_ratio"
        metric_values[key] = summary.largest_component_area_ratio


def _metric_record(
    image_id: str,
    transform_name: str,
    metric_name: str,
    metric_value: float,
) -> dict[str, Any]:
    return {
        "record_type": "image_transform_metric_record",
        "image_id": image_id,
        "transform_name": transform_name,
        "metric_name": metric_name,
        "metric_value": round(float(metric_value), 8),
        "metric_unit": "ratio",
        "metric_notes": "Deterministic Stage 3P review metric.",
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "solve_claim": False,
    }


def _build_summary(
    *,
    generated_at: str,
    image_count: int,
    transform_records: list[dict[str, Any]],
    metric_records: list[dict[str, Any]],
    candidate_records: list[dict[str, Any]],
    contact_records: list[dict[str, Any]],
    review_page_count: int,
    review_index_path: str,
    warnings: list[str],
) -> dict[str, Any]:
    feature_counts = Counter(str(record["feature_type"]) for record in candidate_records)
    by_feature: dict[str, list[str]] = {}
    for record in sorted(candidate_records, key=lambda item: float(item["feature_score"]), reverse=True):
        by_feature.setdefault(str(record["feature_type"]), [])
        if len(by_feature[str(record["feature_type"])]) < 10:
            by_feature[str(record["feature_type"])].append(str(record["image_id"]))
    return {
        "record_type": "image_transform_run_summary",
        "run_id": RUN_ID,
        "generated_at_utc": generated_at,
        "image_count": image_count,
        "transform_count": len({record["transform_name"] for record in transform_records}),
        "derived_image_count": len(transform_records),
        "contact_sheet_count": len(contact_records),
        "review_page_count": review_page_count,
        "visual_candidate_count": len(candidate_records),
        "feature_counts": dict(feature_counts),
        "top_candidate_image_ids_by_feature_type": by_feature,
        "output_paths": {
            "transform_records": "experiments/results/image-transforms/stage3p/transform_records.jsonl",
            "transform_metric_records": "experiments/results/image-transforms/stage3p/transform_metric_records.jsonl",
            "visual_transform_candidates": "experiments/results/image-transforms/stage3p/visual_transform_candidates.jsonl",
            "contact_sheet_manifest": "experiments/results/image-transforms/stage3p/contact_sheet_manifest.jsonl",
            "review_index": review_index_path,
            "summary": "experiments/results/image-transforms/stage3p/summary.json",
            "warnings": "experiments/results/image-transforms/stage3p/warnings.jsonl",
        },
        "warnings": warnings,
        "trusted_as_canonical": False,
        "solve_claim": False,
        "notes": "Generated Stage 3P image-transform review summary. No OCR, AI/ML, or solve claim.",
    }


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path
