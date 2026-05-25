"""Stage 5AR original page-image source-lock records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import (
    FALSE_GUARDRAILS,
    STAGE5AR_ID,
    TOKEN_BLOCK_ID,
    repo_relative,
    sha256_file,
    write_json,
    write_yaml,
)

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
PAGE_NUMBERS = (49, 50, 51)
FORBIDDEN_VARIANT_CLASSES = {
    "derived_screenshot",
    "crop",
    "annotated_or_highlighted",
    "modified_or_composite",
    "web_rendered",
    "private_content_generated",
}


def _image_metadata(path: Path) -> dict[str, Any]:
    from PIL import Image

    with Image.open(path) as image:
        width, height = image.size
        image_format = image.format
        color_mode = image.mode
    return {
        "source_path": repo_relative(path),
        "file_name": path.name,
        "extension": path.suffix.lower(),
        "file_size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "width": width,
        "height": height,
        "image_format": image_format,
        "color_mode": color_mode,
    }


def _page_number(path: Path) -> int | None:
    stem = path.stem.lower().replace("page", "")
    if stem.isdigit() and int(stem) in PAGE_NUMBERS:
        return int(stem)
    return None


def _candidate_paths(search_roots: list[Path]) -> list[Path]:
    candidates: dict[str, Path] = {}
    for root in search_roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES and _page_number(path) in PAGE_NUMBERS:
                candidates[repo_relative(path)] = path
    return [candidates[key] for key in sorted(candidates)]


def _selected_originals(search_roots: list[Path]) -> dict[int, Path]:
    selected: dict[int, Path] = {}
    for page in PAGE_NUMBERS:
        path = Path("third_party/LiberPrimusPages") / f"{page}.jpg"
        if path.exists():
            selected[page] = path
    if len(selected) == len(PAGE_NUMBERS):
        return selected
    for path in _candidate_paths(search_roots):
        page = _page_number(path)
        if page is not None and page not in selected:
            selected[page] = path
    return selected


def classify_variant(path: Path, selected_hashes: dict[int, str]) -> tuple[str, str, bool]:
    """Classify a page-image variant without using it as visual interpretation."""

    page = _page_number(path)
    lower_path = repo_relative(path).lower()
    if any(term in lower_path for term in ("screenshot", "screen-shot", "capture")):
        return "derived_screenshot", "forbidden_supporting_only", False
    if any(term in lower_path for term in ("crop", "cropped")):
        return "crop", "forbidden_supporting_only", False
    if any(term in lower_path for term in ("annotated", "highlight", "overlay", "circled")):
        return "annotated_or_highlighted", "forbidden_supporting_only", False
    if any(term in lower_path for term in ("modified", "composite", "page_modified", "depictions_modified")):
        return "modified_or_composite", "forbidden_supporting_only", False
    if lower_path.startswith(("website-export/", "research-inputs/", "deep-research-content-packs/")):
        return "private_content_generated", "forbidden_supporting_only", False
    if "liberprimuspages" in lower_path and path.name.lower() in {f"{p}.jpg" for p in PAGE_NUMBERS}:
        return "original_candidate", "original_liber_primus_page_image", True
    if page in selected_hashes and sha256_file(path) == selected_hashes[page]:
        return "byte_identical_original_copy", "byte_identical_original_copy", True
    if "the-complete-cicada3301-archive" in lower_path:
        return "near_original_variant", "original_archive_page_image", False
    return "unknown", "unknown", False


def build_original_image_source_lock(
    *,
    search_roots: list[Path],
    stage5ap_image_provenance: Path,
    results_dir: Path,
    out_source_lock: Path,
    out_variants: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    selected = _selected_originals(search_roots)
    selected_hashes = {page: sha256_file(path) for page, path in selected.items()}
    selected_records = []
    for page, path in sorted(selected.items()):
        metadata = _image_metadata(path)
        image_id = f"stage5ar-original-page-{page}-liberprimuspages-jpg"
        selected_records.append(
            {
                "record_type": "original_page_image_source_lock_record",
                "stage_id": STAGE5AR_ID,
                "token_block_id": TOKEN_BLOCK_ID,
                "original_image_id": image_id,
                "page_number": page,
                "source_path": metadata["source_path"],
                "sha256": metadata["sha256"],
                "width": metadata["width"],
                "height": metadata["height"],
                "image_format": metadata["image_format"],
                "color_mode": metadata["color_mode"],
                "file_size_bytes": metadata["file_size_bytes"],
                "coordinate_source_class": "original_liber_primus_page_image",
                "variant_class": "original_candidate",
                "coordinate_truth_allowed": True,
                "raw_image_committed": False,
                "ocr_performed": False,
                "ai_ml_interpretation_performed": False,
                "semantic_image_interpretation_performed": False,
                "solve_claim": False,
            }
        )

    variant_records = []
    for path in _candidate_paths(search_roots):
        page = _page_number(path)
        if page is None:
            continue
        metadata = _image_metadata(path)
        variant_class, source_class, coordinate_allowed = classify_variant(path, selected_hashes)
        variant_records.append(
            {
                "record_type": "original_page_image_variant_record",
                "stage_id": STAGE5AR_ID,
                "token_block_id": TOKEN_BLOCK_ID,
                "page_number": page,
                "source_path": metadata["source_path"],
                "sha256": metadata["sha256"],
                "width": metadata["width"],
                "height": metadata["height"],
                "image_format": metadata["image_format"],
                "color_mode": metadata["color_mode"],
                "variant_class": variant_class,
                "coordinate_source_class": source_class,
                "coordinate_truth_allowed": coordinate_allowed,
                "raw_image_committed": False,
                "generated_image_committed": False,
                "supporting_metadata_only": not coordinate_allowed,
                "solve_claim": False,
            }
        )

    selected_pages = sorted(record["page_number"] for record in selected_records)
    missing_pages = [page for page in PAGE_NUMBERS if page not in selected_pages]
    source_lock_status = "original_images_available" if not missing_pages else "blocked_missing_original_images"
    source_lock = {
        "record_type": "original_page_image_source_lock",
        "schema": "schemas/token-block/original-page-image-source-lock-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "source_lock_status": source_lock_status,
        "stage5ap_image_provenance": repo_relative(stage5ap_image_provenance),
        "selected_original_image_count": len(selected_records),
        "missing_original_pages": missing_pages,
        "coordinate_source_available": not missing_pages,
        "original_images_required": True,
        "screenshots_forbidden_as_coordinate_sources": True,
        "records": selected_records,
        "raw_image_committed": False,
        "generated_image_committed": False,
        "no_decode": True,
        "no_hash_preimage_search": True,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    variants = {
        "record_type": "original_page_image_variants",
        "schema": "schemas/token-block/original-page-image-variant-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "variant_record_count": len(variant_records),
        "coordinate_truth_candidate_count": sum(1 for record in variant_records if record["coordinate_truth_allowed"]),
        "forbidden_variant_count": sum(1 for record in variant_records if record["variant_class"] in FORBIDDEN_VARIANT_CLASSES),
        "records": variant_records,
        "raw_image_committed": False,
        "generated_image_committed": False,
        "solve_claim": False,
    }
    write_yaml(out_source_lock, source_lock)
    write_yaml(out_variants, variants)
    write_json(results_dir / "original_image_source_lock_report.json", source_lock)
    write_json(results_dir / "original_image_variant_report.json", variants)
    return source_lock, variants
