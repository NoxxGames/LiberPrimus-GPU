"""Stage 5AR deterministic original-image pixel coordinate records."""

from __future__ import annotations

from pathlib import Path
from statistics import median
from typing import Any

from .models import FALSE_GUARDRAILS, STAGE5AR_ID, TOKEN_BLOCK_ID, read_yaml, write_jsonl, write_yaml
from .page_split import COMMUNITY_SPLIT


def _dark_bands(path: Path, *, x_min: int = 550, x_max: int = 1850) -> list[tuple[int, int]]:
    from PIL import Image

    image = Image.open(path).convert("L")
    pixels = image.load()
    counts: list[int] = []
    for y in range(image.height):
        dark = 0
        for x in range(x_min, min(x_max, image.width)):
            if pixels[x, y] < 80:
                dark += 1
        counts.append(dark)
    rows = [index for index, count in enumerate(counts) if count > 20]
    bands: list[tuple[int, int]] = []
    if not rows:
        return bands
    start = previous = rows[0]
    for row in rows[1:]:
        if row - previous > 8:
            if previous - start > 5:
                bands.append((start, previous))
            start = row
        previous = row
    if previous - start > 5:
        bands.append((start, previous))
    return bands


def _token_bands(page: int, path: Path) -> list[tuple[int, int]]:
    bands = _dark_bands(path)
    if page == 49:
        return bands[-10:]
    if page == 50:
        return bands[:13]
    if page == 51:
        return bands[:9]
    return []


def _row_x_extent(path: Path, y_min: int, y_max: int) -> tuple[int, int] | None:
    from PIL import Image

    image = Image.open(path).convert("L")
    pixels = image.load()
    xs: list[int] = []
    for x in range(620, min(1780, image.width)):
        dark = 0
        for y in range(max(0, y_min), min(image.height, y_max + 1)):
            if pixels[x, y] < 100:
                dark += 1
        if dark > 2:
            xs.append(x)
    if not xs:
        return None
    return min(xs), max(xs)


def _page_x_extent(path: Path, bands: list[tuple[int, int]]) -> tuple[int, int]:
    extents = [extent for y_min, y_max in bands if (extent := _row_x_extent(path, y_min, y_max)) is not None]
    if not extents:
        return 650, 1750
    starts = [start for start, _ in extents]
    ends = [end for _, end in extents]
    return max(0, min(starts) - 8), max(ends) + 8


def _page_for_global_row(row_index: int) -> tuple[int, int]:
    for page, split in COMMUNITY_SPLIT.items():
        first, last = split["global_rows_0_based"]
        if first <= row_index <= last:
            return page, row_index - first
    raise ValueError(f"row out of page split: {row_index}")


def build_pixel_coordinates(
    *,
    stage5ap_transcription: Path,
    stage5ap_logical_coordinates: Path,
    original_image_source_lock: Path,
    page_split_records: Path,
    results_dir: Path,
    out_policy: Path,
    out_records: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    transcription = read_yaml(stage5ap_transcription)
    read_yaml(stage5ap_logical_coordinates)
    page_split = read_yaml(page_split_records)
    source_lock = read_yaml(original_image_source_lock)
    image_records = {record["page_number"]: record for record in source_lock.get("records", [])}
    image_paths = {page: Path(record["source_path"]) for page, record in image_records.items()}
    page_bands = {page: _token_bands(page, path) for page, path in image_paths.items()}
    page_x_extents = {page: _page_x_extent(image_paths[page], bands) for page, bands in page_bands.items()}
    records: list[dict[str, Any]] = []
    rows: list[list[str]] = transcription["token_grid"]
    for row_index, row in enumerate(rows):
        page, page_row = _page_for_global_row(row_index)
        image = image_records.get(page)
        bands = page_bands.get(page, [])
        x_start, x_end = page_x_extents.get(page, (650, 1750))
        cell_width = (x_end - x_start + 1) / 8
        y_min, y_max = bands[page_row] if page_row < len(bands) else (0, 0)
        for column_index, token in enumerate(row):
            bbox_x_min = int(round(x_start + (cell_width * column_index)))
            bbox_x_max = int(round(x_start + (cell_width * (column_index + 1))))
            bbox_y_min = max(0, y_min - 8)
            bbox_y_max = min(int(image.get("height", 0)), y_max + 9) if image else y_max + 9
            records.append(
                {
                    "record_type": "token_pixel_coordinate_record",
                    "schema": "schemas/token-block/token-pixel-coordinate-record-v0.schema.json",
                    "stage_id": STAGE5AR_ID,
                    "token_block_id": TOKEN_BLOCK_ID,
                    "token_index_0_based": (row_index * 8) + column_index,
                    "token_index_1_based": (row_index * 8) + column_index + 1,
                    "global_row_index_0_based": row_index,
                    "global_row_index_1_based": row_index + 1,
                    "global_column_index_0_based": column_index,
                    "global_column_index_1_based": column_index + 1,
                    "token": token,
                    "first_symbol": token[0],
                    "suffix_symbol": token[1],
                    "assigned_page_number": page,
                    "assigned_page_row_index_0_based": page_row,
                    "assigned_page_row_index_1_based": page_row + 1,
                    "original_image_id": image.get("original_image_id") if image else None,
                    "original_image_sha256": image.get("sha256") if image else None,
                    "original_image_width": image.get("width") if image else None,
                    "original_image_height": image.get("height") if image else None,
                    "coordinate_source_class": image.get("coordinate_source_class") if image else "missing_original_image",
                    "bbox_x_min": bbox_x_min,
                    "bbox_y_min": bbox_y_min,
                    "bbox_x_max": bbox_x_max,
                    "bbox_y_max": bbox_y_max,
                    "bbox_width": bbox_x_max - bbox_x_min,
                    "bbox_height": bbox_y_max - bbox_y_min,
                    "coordinate_method": "deterministic_projection_from_original_image" if image else "blocked_no_original_image",
                    "coordinate_confidence": "medium_review_required" if image else "blocked",
                    "coordinate_status": "source_locked_review_required" if image else "blocked_missing_original_image",
                    "case_policy_status": "covered_by_stage5ar_case_policy",
                    "review_notes": "Deterministic row projection and equal-column grid from original image; not OCR.",
                    "ocr_performed": False,
                    "ai_ml_interpretation_performed": False,
                    "semantic_image_interpretation_performed": False,
                    "solve_claim": False,
                }
            )
    heights = [record["bbox_height"] for record in records]
    policy = {
        "record_type": "token_pixel_coordinate_policy",
        "schema": "schemas/token-block/token-pixel-coordinate-policy-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "coordinate_system": "original_image_pixel_space",
        "origin": "top_left",
        "x_increases": "right",
        "y_increases": "down",
        "units": "integer_pixels",
        "inclusive_exclusive_policy": "x_min/y_min inclusive, x_max/y_max exclusive",
        "coordinate_method": "deterministic_projection_from_original_image",
        "manual_roi_seed_points_used": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "semantic_image_interpretation_performed": False,
        "hidden_content_image_forensics_performed": False,
        "token_coordinate_record_count": len(records),
        "median_bbox_height": median(heights) if heights else None,
        "page_split_status": page_split.get("page_split_status"),
        "review_required": True,
        "no_decode": True,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    payload = {
        "record_type": "token_pixel_coordinate_record_set",
        "schema": "schemas/token-block/token-pixel-coordinate-record-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "coordinate_record_count": len(records),
        "coordinate_status": "source_locked_review_required" if len(records) == 256 else "blocked_no_coordinate_source",
        "records": records,
        "no_decode": True,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out_policy, policy)
    write_yaml(out_records, payload)
    write_jsonl(results_dir / "token_pixel_coordinate_records.jsonl", records)
    return policy, payload
