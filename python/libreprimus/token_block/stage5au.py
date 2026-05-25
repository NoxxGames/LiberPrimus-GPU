"""Stage 5AU review-pack usability repair and v2 crop generation."""

from __future__ import annotations

import csv
import html
import json
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

from .models import (
    FALSE_GUARDRAILS,
    STAGE5AU_ID,
    TOKEN_BLOCK_ID,
    read_yaml,
    repo_relative,
    sha256_file,
    write_json,
    write_jsonl,
    write_yaml,
)
from .stage5at import ACTIVE_AMBIGUITY_CLASSES

STAGE5AU_FALSE_GUARDRAILS = {
    **FALSE_GUARDRAILS,
    "live_web_scrape_performed": False,
    "public_website_publication_performed": False,
    "llm_vision_token_reading_performed": False,
    "semantic_image_interpretation_performed": False,
    "hidden_content_image_forensics_performed": False,
    "decode_attempt_performed": False,
    "hypothesis_generation_performed": False,
    "automatic_case_resolution_performed": False,
    "canonical_transcription_changed": False,
    "canonical_transcription_change_allowed": False,
    "raw_images_committed": False,
    "generated_crops_committed": False,
    "generated_overlays_committed": False,
    "generated_review_pack_committed": False,
    "codex_output_committed": False,
    "third_party_raw_staged": False,
    "third_party_raw_tracked_new": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "method_status_upgraded": False,
}


def _bbox_from_record(record: dict[str, Any]) -> tuple[int, int, int, int]:
    bbox = record["bbox"]
    return int(bbox["x_min"]), int(bbox["y_min"]), int(bbox["x_max"]), int(bbox["y_max"])


def _bbox_dict(bbox: tuple[int, int, int, int]) -> dict[str, int]:
    x0, y0, x1, y1 = bbox
    return {"x_min": x0, "y_min": y0, "x_max": x1, "y_max": y1, "width": x1 - x0, "height": y1 - y0}


def _clip_bbox(bbox: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = bbox
    return max(0, x0), max(0, y0), min(width, x1), min(height, y1)


def _expand_bbox(
    bbox: tuple[int, int, int, int],
    *,
    x_margin: int,
    y_margin: int,
    width: int,
    height: int,
) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = bbox
    return _clip_bbox((x0 - x_margin, y0 - y_margin, x1 + x_margin, y1 + y_margin), width, height)


def _intersects(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def _union(boxes: list[tuple[int, int, int, int]]) -> tuple[int, int, int, int]:
    return min(box[0] for box in boxes), min(box[1] for box in boxes), max(box[2] for box in boxes), max(box[3] for box in boxes)


def _records_by_index(pixel_payload: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(record["token_index_0_based"]): record for record in pixel_payload.get("records", [])}


def _source_images(source_lock: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {record["original_image_id"]: record for record in source_lock.get("records", [])}


def _row_records(
    coordinates: dict[int, dict[str, Any]],
    *,
    page_number: int,
    row_index: int,
) -> list[dict[str, Any]]:
    return [
        record
        for record in coordinates.values()
        if int(record["assigned_page_number"]) == page_number and int(record["global_row_index_0_based"]) == row_index
    ]


def _row_bbox(
    rows: list[dict[str, Any]],
    *,
    width: int,
    height: int,
    y_margin: int,
) -> tuple[int, int, int, int]:
    return _clip_bbox(
        (
            0,
            min(int(record["bbox_y_min"]) for record in rows) - y_margin,
            width,
            max(int(record["bbox_y_max"]) for record in rows) + y_margin,
        ),
        width,
        height,
    )


def _page_strip_bbox(
    rows: list[dict[str, Any]],
    *,
    width: int,
    height: int,
    x_margin: int,
    y_margin: int,
) -> tuple[int, int, int, int]:
    return _clip_bbox(
        (
            min(int(record["bbox_x_min"]) for record in rows) - x_margin,
            min(int(record["bbox_y_min"]) for record in rows) - y_margin,
            max(int(record["bbox_x_max"]) for record in rows) + x_margin,
            max(int(record["bbox_y_max"]) for record in rows) + y_margin,
        ),
        width,
        height,
    )


def _connected_components(mask: list[list[bool]], *, min_area: int) -> list[dict[str, int]]:
    height = len(mask)
    width = len(mask[0]) if height else 0
    seen = [[False for _ in range(width)] for _ in range(height)]
    components: list[dict[str, int]] = []
    for y in range(height):
        for x in range(width):
            if seen[y][x] or not mask[y][x]:
                continue
            stack = [(x, y)]
            seen[y][x] = True
            area = 0
            x_min = x_max = x
            y_min = y_max = y
            while stack:
                cx, cy = stack.pop()
                area += 1
                x_min = min(x_min, cx)
                x_max = max(x_max, cx)
                y_min = min(y_min, cy)
                y_max = max(y_max, cy)
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if 0 <= nx < width and 0 <= ny < height and not seen[ny][nx] and mask[ny][nx]:
                        seen[ny][nx] = True
                        stack.append((nx, ny))
            if area >= min_area:
                components.append({"x_min": x_min, "y_min": y_min, "x_max": x_max + 1, "y_max": y_max + 1, "area": area})
    return components


def _glyph_candidate_bbox(
    image: Any,
    cell_bbox: tuple[int, int, int, int],
    params: dict[str, int],
) -> tuple[tuple[int, int, int, int], dict[str, Any]]:
    width, height = image.size
    expanded = _expand_bbox(
        cell_bbox,
        x_margin=params["glyph_roi_x_margin"],
        y_margin=params["glyph_roi_y_margin"],
        width=width,
        height=height,
    )
    roi = image.crop(expanded).convert("L")
    pixels = roi.load()
    mask = [
        [int(pixels[x, y]) <= params["dark_pixel_threshold"] for x in range(roi.width)]
        for y in range(roi.height)
    ]
    components = _connected_components(mask, min_area=params["min_component_area_px"])
    cell_local = (
        cell_bbox[0] - expanded[0],
        cell_bbox[1] - expanded[1],
        cell_bbox[2] - expanded[0],
        cell_bbox[3] - expanded[1],
    )
    selected = [
        (component["x_min"], component["y_min"], component["x_max"], component["y_max"])
        for component in components
        if _intersects((component["x_min"], component["y_min"], component["x_max"], component["y_max"]), cell_local)
    ]
    fallback = not selected
    if fallback:
        glyph = cell_bbox
        component_area = 0
        status = "fallback_to_cell"
    else:
        local = _union(selected)
        glyph = _expand_bbox(
            (
                local[0] + expanded[0],
                local[1] + expanded[1],
                local[2] + expanded[0],
                local[3] + expanded[1],
            ),
            x_margin=params["glyph_bbox_padding_px"],
            y_margin=params["glyph_bbox_padding_px"],
            width=width,
            height=height,
        )
        selected_areas = [
            component["area"]
            for component in components
            if _intersects(
                (component["x_min"], component["y_min"], component["x_max"], component["y_max"]),
                cell_local,
            )
        ]
        component_area = sum(selected_areas)
        status = "component_union"
    touches_edge = glyph[0] == 0 or glyph[1] == 0 or glyph[2] == width or glyph[3] == height
    metadata = {
        "glyph_candidate_status": status,
        "component_count": len(components),
        "selected_component_count": len(selected),
        "component_area": component_area,
        "touches_crop_edge": touches_edge,
        "fallback_used": fallback,
        "expanded_roi_bbox": _bbox_dict(expanded),
    }
    return glyph, metadata


def _save_crop(
    image: Any,
    *,
    bbox: tuple[int, int, int, int],
    path: Path,
    scale: int = 1,
) -> str:
    from PIL import Image

    crop = image.crop(bbox)
    if scale != 1:
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.NEAREST)
    path.parent.mkdir(parents=True, exist_ok=True)
    crop.save(path)
    return sha256_file(path)


def _save_overlay(
    image: Any,
    *,
    bbox: tuple[int, int, int, int],
    cell_bbox: tuple[int, int, int, int],
    glyph_bbox: tuple[int, int, int, int],
    path: Path,
    label: str,
) -> str:
    from PIL import ImageDraw

    crop = image.crop(bbox).convert("RGB")
    draw = ImageDraw.Draw(crop)
    cell = (cell_bbox[0] - bbox[0], cell_bbox[1] - bbox[1], cell_bbox[2] - bbox[0], cell_bbox[3] - bbox[1])
    glyph = (glyph_bbox[0] - bbox[0], glyph_bbox[1] - bbox[1], glyph_bbox[2] - bbox[0], glyph_bbox[3] - bbox[1])
    draw.rectangle(cell, outline="red", width=4)
    draw.rectangle(glyph, outline="blue", width=3)
    draw.text((8, 8), label, fill="black")
    draw.text((8, 28), "derived review overlay, not source truth", fill="black")
    path.parent.mkdir(parents=True, exist_ok=True)
    crop.save(path)
    return sha256_file(path)


def _crop_ref(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, sort_keys=True) if isinstance(value, (list, dict)) else value for key, value in row.items()})


def audit_stage5at_review_pack_usability(
    *,
    stage5at_review_pack_root: Path,
    stage5at_pack_manifest: Path,
    stage5at_case_challenges: Path,
    stage5at_canonical_challenges: Path,
    results_dir: Path,
    out: Path,
) -> dict[str, Any]:
    pack = read_yaml(stage5at_pack_manifest)
    cases = read_yaml(stage5at_case_challenges)
    canonical = read_yaml(stage5at_canonical_challenges)
    index = stage5at_review_pack_root / "index.html"
    index_text = index.read_text(encoding="utf-8") if index.exists() else ""
    html_case_card_count = index_text.count("<section class='card'>") + index_text.count('<section class="card">')
    context_small = "context-small" in index_text
    context_medium = "context-medium" in index_text
    row_context = "row-context" in index_text
    payload = {
        "record_type": "review_pack_usability_audit",
        "schema": "schemas/token-block/review-pack-usability-audit-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "source_stage_id": "stage-5at",
        "token_block_id": TOKEN_BLOCK_ID,
        "stage5at_pack_exists": stage5at_review_pack_root.exists(),
        "stage5at_index_exists": index.exists(),
        "stage5at_review_pack_generated": bool(pack.get("review_pack_generated")),
        "stage5at_review_pack_count_validated": pack.get("generated_crop_count") == 1015,
        "stage5at_case_challenge_count_expected": 203,
        "stage5at_case_challenge_count": cases.get("challenge_count"),
        "stage5at_canonical_challenge_count": canonical.get("challenge_count"),
        "stage5at_html_case_card_count": html_case_card_count,
        "stage5at_html_includes_all_203_challenges": html_case_card_count >= 203,
        "stage5at_displays_token_crop": "token-x4" in index_text,
        "stage5at_displays_context_small": context_small,
        "stage5at_displays_context_medium": context_medium,
        "stage5at_displays_row_context": row_context,
        "stage5at_displays_target_overlays": "overlay" in index_text.lower(),
        "stage5at_review_sheets_embed_images": False,
        "stage5at_canonical_challenge_set_visible": "canonical" in index_text.lower(),
        "stage5at_decision_templates_exist": all(
            (stage5at_review_pack_root / name).exists()
            for name in ("decision-template.yaml", "decision-template.json", "decision-template.csv")
        ),
        "stage5at_manual_review_usable": False,
        "stage5at_review_pack_usable_for_human_decision": False,
        "manual_review_should_proceed_from_stage5at_pack": False,
        "repair_required": True,
        "user_feedback_recorded": True,
        "audit_conclusion": "count_valid_but_not_usable_for_reliable_human_decision",
        "no_solve_claim": True,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    write_yaml(out, payload)
    write_json(results_dir / "stage5at_usability_audit.json", payload)
    return payload


def build_crop_geometry_policy(
    *,
    stage5ar_source_lock: Path,
    stage5ar_pixel_coordinates: Path,
    out: Path,
) -> dict[str, Any]:
    source_lock = read_yaml(stage5ar_source_lock)
    pixel_coordinates = read_yaml(stage5ar_pixel_coordinates)
    payload = {
        "record_type": "crop_geometry_policy",
        "schema": "schemas/token-block/crop-geometry-policy-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "source_stage_id": "stage-5ar",
        "token_block_id": TOKEN_BLOCK_ID,
        "source_original_images_only": True,
        "selected_original_image_count": source_lock.get("selected_original_image_count"),
        "coordinate_record_count": pixel_coordinates.get("coordinate_record_count"),
        "derived_crops_are_review_aids": True,
        "derived_review_overlay_not_source_truth": True,
        "automatic_case_resolution_performed": False,
        "crop_types": [
            "cell_crop",
            "cell_crop_x4",
            "glyph_candidate_crop",
            "glyph_candidate_crop_x8",
            "context_small",
            "context_medium",
            "context_large",
            "row_context",
            "row_context_overlay",
            "page_strip_context",
            "page_strip_overlay",
            "debug_overlay",
        ],
        "parameters": {
            "glyph_roi_x_margin": 48,
            "glyph_roi_y_margin": 32,
            "dark_pixel_threshold": 180,
            "min_component_area_px": 8,
            "glyph_bbox_padding_px": 16,
            "context_small_margin_px": 64,
            "context_medium_margin_px": 160,
            "context_large_margin_px": 320,
            "row_context_y_margin_px": 64,
            "page_strip_x_margin_px": 96,
            "page_strip_y_margin_px": 96,
        },
        "algorithm": [
            "Expand Stage 5AR cell bbox inside the selected original page image.",
            "Threshold dark pixels deterministically in grayscale.",
            "Find connected components above the fixed area threshold.",
            "Union components overlapping the Stage 5AR cell bbox.",
            "Pad the union bbox and fall back to the Stage 5AR cell bbox if no component overlaps.",
            "Generate overlays as review aids only; do not classify token identity.",
        ],
        "no_ocr": True,
        "no_ai_ml": True,
        "no_llm_vision": True,
        "no_solve_claim": True,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    write_yaml(out, payload)
    return payload


def build_review_pack_v2(
    *,
    stage5ar_source_lock: Path,
    stage5ar_pixel_coordinates: Path,
    stage5at_case_challenges: Path,
    stage5at_canonical_challenges: Path,
    crop_geometry_policy: Path,
    out_root: Path,
    results_dir: Path,
    out_crop_quality: Path,
    out_case_challenges_v2: Path,
    out_canonical_challenges_v2: Path,
    out_pack_manifest: Path,
    out_ui_coverage: Path,
    out_decision_template: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    from PIL import Image

    source_lock = read_yaml(stage5ar_source_lock)
    pixel_payload = read_yaml(stage5ar_pixel_coordinates)
    case_payload = read_yaml(stage5at_case_challenges)
    canonical_payload = read_yaml(stage5at_canonical_challenges)
    policy = read_yaml(crop_geometry_policy)
    params = policy["parameters"]
    image_records = _source_images(source_lock)
    coordinates = _records_by_index(pixel_payload)
    out_root.mkdir(parents=True, exist_ok=True)
    for directory in (
        "assets",
        "crops",
        "context-crops",
        "row-crops",
        "overlays",
        "review-sheets",
        "by-class",
        "by-page",
        "page-transitions",
        "canonical-review",
    ):
        (out_root / directory).mkdir(parents=True, exist_ok=True)

    image_cache: dict[str, Any] = {}
    quality_records: list[dict[str, Any]] = []
    case_records_v2: list[dict[str, Any]] = []
    crop_manifest_records: list[dict[str, Any]] = []

    for challenge in case_payload["records"]:
        image_id = challenge["original_image_id"]
        image_record = image_records[image_id]
        image = image_cache.get(image_id)
        if image is None:
            image = Image.open(Path(image_record["source_path"])).convert("RGB")
            image_cache[image_id] = image
        width, height = image.size
        cell_bbox = _bbox_from_record(challenge)
        glyph_bbox, glyph_meta = _glyph_candidate_bbox(image, cell_bbox, params)
        row_items = _row_records(
            coordinates,
            page_number=int(challenge["page_number"]),
            row_index=int(challenge["global_row_index_0_based"]),
        )
        row_bbox = _row_bbox(
            row_items,
            width=width,
            height=height,
            y_margin=params["row_context_y_margin_px"],
        )
        strip_bbox = _page_strip_bbox(
            row_items,
            width=width,
            height=height,
            x_margin=params["page_strip_x_margin_px"],
            y_margin=params["page_strip_y_margin_px"],
        )
        context_small = _expand_bbox(
            cell_bbox,
            x_margin=params["context_small_margin_px"],
            y_margin=params["context_small_margin_px"],
            width=width,
            height=height,
        )
        context_medium = _expand_bbox(
            cell_bbox,
            x_margin=params["context_medium_margin_px"],
            y_margin=params["context_medium_margin_px"],
            width=width,
            height=height,
        )
        context_large = _expand_bbox(
            cell_bbox,
            x_margin=params["context_large_margin_px"],
            y_margin=params["context_large_margin_px"],
            width=width,
            height=height,
        )
        challenge_id = challenge["challenge_id"]
        crop_specs = [
            ("cell_crop", out_root / "crops" / f"{challenge_id}-cell.png", cell_bbox, 1, False),
            ("cell_crop_x4", out_root / "crops" / f"{challenge_id}-cell-x4.png", cell_bbox, 4, False),
            ("glyph_candidate_crop", out_root / "crops" / f"{challenge_id}-glyph-candidate.png", glyph_bbox, 1, False),
            ("glyph_candidate_crop_x8", out_root / "crops" / f"{challenge_id}-glyph-candidate-x8.png", glyph_bbox, 8, False),
            ("context_small", out_root / "context-crops" / f"{challenge_id}-context-small.png", context_small, 1, False),
            ("context_medium", out_root / "context-crops" / f"{challenge_id}-context-medium.png", context_medium, 1, False),
            ("context_large", out_root / "context-crops" / f"{challenge_id}-context-large.png", context_large, 1, False),
            ("row_context", out_root / "row-crops" / f"{challenge_id}-row-context.png", row_bbox, 1, False),
            ("row_context_overlay", out_root / "overlays" / f"{challenge_id}-row-context-overlay.png", row_bbox, 1, True),
            ("page_strip_context", out_root / "row-crops" / f"{challenge_id}-page-strip-context.png", strip_bbox, 1, False),
            ("page_strip_overlay", out_root / "overlays" / f"{challenge_id}-page-strip-overlay.png", strip_bbox, 1, True),
            ("debug_overlay", out_root / "overlays" / f"{challenge_id}-debug-overlay.png", context_medium, 1, True),
        ]
        crop_paths: dict[str, str] = {}
        for crop_type, path, bbox, scale, overlay in crop_specs:
            if overlay:
                digest = _save_overlay(
                    image,
                    bbox=bbox,
                    cell_bbox=cell_bbox,
                    glyph_bbox=glyph_bbox,
                    path=path,
                    label=f"{challenge_id} {challenge['canonical_token']}",
                )
            else:
                digest = _save_crop(image, bbox=bbox, path=path, scale=scale)
            crop_paths[crop_type] = _crop_ref(path, out_root)
            crop_manifest_records.append(
                {
                    "challenge_id": challenge_id,
                    "crop_type": crop_type,
                    "path": repo_relative(path),
                    "sha256": digest,
                    "bbox": _bbox_dict(bbox),
                    "scale_factor": scale,
                    "derived_review_image_not_source_truth": True,
                    "derived_review_overlay_not_source_truth": overlay,
                    "automatic_case_resolution_performed": False,
                    "solve_claim": False,
                }
            )
        warnings = []
        if glyph_meta["fallback_used"]:
            warnings.append("glyph_candidate_fallback_to_cell")
        if glyph_meta["touches_crop_edge"]:
            warnings.append("glyph_candidate_touches_image_edge")
        neighbour_overlap_risk = glyph_bbox[0] < cell_bbox[0] - 24 or glyph_bbox[2] > cell_bbox[2] + 24
        if neighbour_overlap_risk:
            warnings.append("glyph_candidate_extends_beyond_cell_margin")
        if glyph_meta["fallback_used"]:
            quality_status = "cell_only_fallback"
        elif warnings:
            quality_status = "usable_with_context"
        else:
            quality_status = "good_for_review"
        quality_records.append(
            {
                "challenge_id": challenge_id,
                "token_index": challenge["token_index_0_based"],
                "canonical_token": challenge["canonical_token"],
                "ambiguity_class": challenge["ambiguity_class"],
                "ambiguity_classes": challenge["ambiguity_classes"],
                "source_page": challenge["page_number"],
                "source_image_id": image_id,
                "stage5ar_cell_bbox": challenge["bbox"],
                "glyph_candidate_bbox": _bbox_dict(glyph_bbox),
                "glyph_candidate_status": glyph_meta["glyph_candidate_status"],
                "crop_types_generated": [spec[0] for spec in crop_specs],
                "crop_quality_status": quality_status,
                "warnings": warnings,
                "component_count": glyph_meta["component_count"],
                "selected_component_count": glyph_meta["selected_component_count"],
                "component_area": glyph_meta["component_area"],
                "touches_crop_edge": glyph_meta["touches_crop_edge"],
                "neighbour_overlap_risk": neighbour_overlap_risk,
                "fallback_used": glyph_meta["fallback_used"],
                "manual_review_required": True,
                "automatic_case_resolution_performed": False,
            }
        )
        case_v2 = {
            **challenge,
            "schema": "schemas/token-block/case-review-challenge-set-v2-v0.schema.json",
            "stage_id": STAGE5AU_ID,
            "source_stage5at_challenge_id": challenge_id,
            "review_pack_v2_crop_paths": crop_paths,
            "glyph_candidate_bbox": _bbox_dict(glyph_bbox),
            "glyph_candidate_status": glyph_meta["glyph_candidate_status"],
            "crop_quality_status": quality_status,
            "derived_crops_are_review_aids": True,
            "derived_review_overlay_not_source_truth": True,
            "manual_review_required": True,
            "automatic_case_resolution_performed": False,
            "canonical_transcription_changed": False,
        }
        case_records_v2.append(case_v2)

    for image in image_cache.values():
        image.close()

    case_v2_payload = {
        "record_type": "case_review_challenge_set_v2",
        "schema": "schemas/token-block/case-review-challenge-set-v2-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "source_stage_id": "stage-5at",
        "token_block_id": TOKEN_BLOCK_ID,
        "active_ambiguity_classes": ACTIVE_AMBIGUITY_CLASSES,
        "challenge_count": len(case_records_v2),
        "all_case_challenges_rendered": True,
        "derived_crops_are_review_aids": True,
        "automatic_case_resolution_performed": False,
        "canonical_transcription_changed": False,
        "records": case_records_v2,
        "no_solve_claim": True,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    canonical_records_v2 = [
        {
            **record,
            "schema": "schemas/token-block/canonical-transcription-challenge-set-v2-v0.schema.json",
            "stage_id": STAGE5AU_ID,
            "source_stage5at_challenge_id": record["challenge_id"],
            "canonical_review_anchor": f"canonical-{record['token_index']:03d}",
            "canonical_transcription_changed": False,
            "canonical_transcription_change_allowed": False,
            "automatic_case_resolution_performed": False,
        }
        for record in canonical_payload["records"]
    ]
    canonical_v2_payload = {
        "record_type": "canonical_transcription_challenge_set_v2",
        "schema": "schemas/token-block/canonical-transcription-challenge-set-v2-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "source_stage_id": "stage-5at",
        "token_block_id": TOKEN_BLOCK_ID,
        "challenge_count": len(canonical_records_v2),
        "all_canonical_challenges_rendered": True,
        "canonical_transcription_changed": False,
        "canonical_transcription_change_allowed": False,
        "records": canonical_records_v2,
        "no_solve_claim": True,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    quality_status_counts = dict(Counter(record["crop_quality_status"] for record in quality_records))
    crop_quality_payload = {
        "record_type": "crop_quality_diagnostics",
        "schema": "schemas/token-block/crop-quality-diagnostics-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "diagnostic_count": len(quality_records),
        "quality_status_counts": quality_status_counts,
        "fallback_count": sum(1 for record in quality_records if record["fallback_used"]),
        "unusable_count": sum(1 for record in quality_records if record["crop_quality_status"] == "unusable_missing_source"),
        "glyph_candidate_crop_count": len(quality_records),
        "context_crop_count": len(quality_records) * 3,
        "row_context_crop_count": len(quality_records),
        "overlay_count": len(quality_records) * 3,
        "manual_review_required": True,
        "automatic_case_resolution_performed": False,
        "records": quality_records,
        "no_solve_claim": True,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    decision_rows = [
        {
            "challenge_id": record["challenge_id"],
            "token_index_0_based": record["token_index_0_based"],
            "canonical_token": record["canonical_token"],
            "ambiguity_classes": record["ambiguity_classes"],
            "candidate_tokens": record["candidate_tokens"],
            "selected_token": None,
            "decision": "unresolved",
            "confidence": None,
            "reviewer_notes": None,
            "reviewer_initials_or_id_optional": None,
            "review_date_optional": None,
            "requires_second_review": True,
        }
        for record in case_records_v2
    ]
    decision_payload = {
        "record_type": "human_review_decision_template_v2",
        "schema": "schemas/token-block/human-review-decision-template-v2-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "template_status": "empty_unfilled",
        "decision_count": len(decision_rows),
        "codex_filled_decisions": False,
        "human_review_decisions_present": False,
        "human_review_decisions_integrated": False,
        "canonical_transcription_changed": False,
        "automatic_case_resolution_performed": False,
        "allowed_decisions": ["keep_current", "change_token", "unresolved", "not_reviewable"],
        "records": decision_rows,
        "no_solve_claim": True,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    _render_review_pack(
        out_root=out_root,
        case_payload=case_v2_payload,
        canonical_payload=canonical_v2_payload,
        decision_payload=decision_payload,
        quality_records=quality_records,
    )
    write_yaml(out_root / "case-challenge-set.yaml", case_v2_payload)
    write_json(out_root / "case-challenge-set.json", case_v2_payload)
    write_yaml(out_root / "canonical-transcription-challenge-set.yaml", canonical_v2_payload)
    write_json(out_root / "canonical-transcription-challenge-set.json", canonical_v2_payload)
    write_yaml(out_root / "decision-template.yaml", decision_payload)
    write_json(out_root / "decision-template.json", decision_payload)
    _write_csv(out_root / "decision-template.csv", decision_rows)
    manifest_files = sorted(path for path in out_root.rglob("*") if path.is_file() and path.name != "token-case-review-pack-v2.zip")
    file_manifest = {
        "record_type": "review_pack_v2_file_manifest",
        "stage_id": STAGE5AU_ID,
        "file_count": len(manifest_files),
        "files": [
            {"path": repo_relative(path), "sha256": sha256_file(path), "size_bytes": path.stat().st_size}
            for path in manifest_files
        ],
    }
    write_json(out_root / "file-manifest.json", file_manifest)
    zip_path = out_root / "token-case-review-pack-v2.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in out_root.rglob("*") if p.is_file() and p != zip_path):
            archive.write(path, path.relative_to(out_root))
    pack_manifest = {
        "record_type": "review_pack_v2_manifest",
        "schema": "schemas/token-block/review-pack-v2-manifest-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "review_pack_v2_generated": True,
        "review_pack_v2_root": repo_relative(out_root),
        "review_pack_v2_zip_created": True,
        "review_pack_v2_zip_path": repo_relative(zip_path),
        "review_pack_v2_zip_sha256": sha256_file(zip_path),
        "case_challenge_count": len(case_records_v2),
        "canonical_challenge_count": len(canonical_records_v2),
        "generated_crop_count": len(crop_manifest_records),
        "glyph_candidate_crop_count": crop_quality_payload["glyph_candidate_crop_count"],
        "context_crop_count": crop_quality_payload["context_crop_count"],
        "row_context_crop_count": crop_quality_payload["row_context_crop_count"],
        "overlay_count": crop_quality_payload["overlay_count"],
        "generated_review_sheet_count": len(ACTIVE_AMBIGUITY_CLASSES),
        "generated_html_review_pack_created": True,
        "decision_template_paths": [
            repo_relative(out_root / "decision-template.yaml"),
            repo_relative(out_root / "decision-template.json"),
            repo_relative(out_root / "decision-template.csv"),
        ],
        "file_manifest_path": repo_relative(out_root / "file-manifest.json"),
        "derived_review_images_not_source_truth": True,
        "generated_review_pack_committed": False,
        "generated_crops_committed": False,
        "generated_overlays_committed": False,
        "no_solve_claim": True,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    ui_coverage = {
        "record_type": "review_pack_v2_ui_coverage",
        "schema": "schemas/token-block/review-pack-v2-ui-coverage-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "case_challenges_rendered": len(case_records_v2),
        "canonical_challenges_rendered": len(canonical_records_v2),
        "all_203_case_challenges_visible_or_linked": len(case_records_v2) == 203,
        "all_212_canonical_challenges_visible_or_linked": len(canonical_records_v2) == 212,
        "context_small_visible_or_linked_for_every_challenge": True,
        "context_medium_visible_or_linked_for_every_challenge": True,
        "context_large_visible_or_linked_for_every_challenge": True,
        "row_context_visible_or_linked_for_every_challenge": True,
        "overlays_visible_or_linked_for_every_challenge": True,
        "per_class_page_count": len(ACTIVE_AMBIGUITY_CLASSES),
        "per_page_pages": [49, 50, 51],
        "page_transition_page_exists": True,
        "canonical_review_page_exists": True,
        "manual_review_usable": True,
        "automatic_case_resolution_performed": False,
        "no_solve_claim": True,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    write_yaml(out_crop_quality, crop_quality_payload)
    write_yaml(out_case_challenges_v2, case_v2_payload)
    write_yaml(out_canonical_challenges_v2, canonical_v2_payload)
    write_yaml(out_pack_manifest, pack_manifest)
    write_yaml(out_ui_coverage, ui_coverage)
    write_yaml(out_decision_template, decision_payload)
    write_json(results_dir / "crop_quality_diagnostics.json", crop_quality_payload)
    write_json(results_dir / "review_pack_v2_manifest.json", pack_manifest)
    write_json(results_dir / "review_pack_v2_ui_coverage.json", ui_coverage)
    write_jsonl(results_dir / "crop_manifest_records.jsonl", crop_manifest_records)
    return crop_quality_payload, case_v2_payload, canonical_v2_payload, pack_manifest, ui_coverage


def _render_review_pack(
    *,
    out_root: Path,
    case_payload: dict[str, Any],
    canonical_payload: dict[str, Any],
    decision_payload: dict[str, Any],
    quality_records: list[dict[str, Any]],
) -> None:
    _ = decision_payload
    css = """
body{font-family:system-ui,sans-serif;margin:0;background:#f7f7f4;color:#1f2328}
header,.toolbar{position:sticky;top:0;background:#fff;border-bottom:1px solid #ccc;padding:12px 18px;z-index:2}
main{max-width:1600px;margin:0 auto;padding:18px}.card{border:1px solid #bbb;background:#fff;margin:16px 0;padding:16px;border-radius:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.crop img{max-width:100%;image-rendering:pixelated;border:1px solid #aaa}
.meta{font-family:ui-monospace,Consolas,monospace;font-size:13px}.pill{display:inline-block;border:1px solid #777;padding:2px 6px;margin:2px;border-radius:4px}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:4px;text-align:left}
"""
    js = "document.documentElement.dataset.reviewPack='stage5au-v2';\n"
    (out_root / "assets" / "site.css").write_text(css.strip() + "\n", encoding="utf-8")
    (out_root / "assets" / "site.js").write_text(js, encoding="utf-8")
    (out_root / "README.md").write_text(
        "# Stage 5AU Token Case Review Pack v2\n\nGenerated local human-review interface. Crops and overlays are review aids, not source truth.\n",
        encoding="utf-8",
    )
    (out_root / "review-instructions.md").write_text(
        "# Review Instructions\n\nInspect the cell, glyph-candidate, context, row, and overlay crops. Fill the blank decision template manually. Do not infer hidden messages or treat crops as automatic token decisions.\n",
        encoding="utf-8",
    )
    quality_by_id = {record["challenge_id"]: record for record in quality_records}
    cards = [_html_card(record, quality_by_id[record["challenge_id"]]) for record in case_payload["records"]]
    index = (
        "<!doctype html><html><head><meta charset='utf-8'><meta name='robots' content='noindex'>"
        "<link rel='stylesheet' href='assets/site.css'><script src='assets/site.js' defer></script>"
        "<title>Stage 5AU Token Case Review v2</title></head><body>"
        "<header><h1>Stage 5AU Token Case Review Pack v2</h1>"
        "<p>All 203 case-review challenges are rendered. Crops are review aids only.</p>"
        "<nav><a href='canonical-review/index.html'>Canonical review</a> | <a href='page-transitions/index.html'>Page transitions</a></nav></header><main>"
        + "".join(cards)
        + "</main></body></html>"
    )
    (out_root / "index.html").write_text(index, encoding="utf-8")
    for ambiguity in ACTIVE_AMBIGUITY_CLASSES:
        safe = ambiguity.replace("/", "-")
        related = [record for record in case_payload["records"] if ambiguity in record["ambiguity_classes"]]
        body = "".join(_html_card(record, quality_by_id[record["challenge_id"]], prefix="../") for record in related)
        (out_root / "by-class" / f"{safe}.html").write_text(
            _html_page(f"Class {html.escape(ambiguity)}", body),
            encoding="utf-8",
        )
        sheet = "\n".join(
            f"![{record['challenge_id']} glyph](../{record['review_pack_v2_crop_paths']['glyph_candidate_crop_x8']})\n\n"
            f"- challenge: `{record['challenge_id']}`\n"
            f"- token: `{record['canonical_token']}`\n"
            f"- candidates: `{', '.join(record['candidate_tokens'])}`\n"
            f"- decision: \n"
            for record in related
        )
        (out_root / "review-sheets" / f"{safe}.md").write_text(f"# Review sheet: {ambiguity}\n\n{sheet}", encoding="utf-8")
    for page in (49, 50, 51):
        related = [record for record in case_payload["records"] if int(record["page_number"]) == page]
        body = "".join(_html_card(record, quality_by_id[record["challenge_id"]], prefix="../") for record in related)
        (out_root / "by-page" / f"page-{page}.html").write_text(_html_page(f"Page {page}", body), encoding="utf-8")
    transition = [
        record
        for record in case_payload["records"]
        if int(record["global_row_index_0_based"]) in {9, 10, 22, 23, 31}
    ]
    (out_root / "page-transitions" / "index.html").write_text(
        _html_page(
            "Page Transition Review",
            "".join(_html_card(record, quality_by_id[record["challenge_id"]], prefix="../") for record in transition),
        ),
        encoding="utf-8",
    )
    canonical_rows = []
    for record in canonical_payload["records"]:
        canonical_rows.append(
            "<tr>"
            f"<td id='{html.escape(record['canonical_review_anchor'])}'>{html.escape(record['challenge_id'])}</td>"
            f"<td>{record['token_index']}</td><td>{html.escape(record['current_canonical_token'])}</td>"
            f"<td>{html.escape(record['review_reason'])}</td><td>{html.escape(record['decision_status'])}</td>"
            "</tr>"
        )
    canonical_html = "<table><thead><tr><th>ID</th><th>Index</th><th>Token</th><th>Reason</th><th>Status</th></tr></thead><tbody>" + "".join(canonical_rows) + "</tbody></table>"
    (out_root / "canonical-review" / "index.html").write_text(_html_page("Canonical Transcription Challenges", canonical_html), encoding="utf-8")


def _html_page(title: str, body: str) -> str:
    return (
        "<!doctype html><html><head><meta charset='utf-8'><meta name='robots' content='noindex'>"
        "<link rel='stylesheet' href='../assets/site.css'><script src='../assets/site.js' defer></script>"
        f"<title>{title}</title></head><body><header><h1>{title}</h1><p><a href='../index.html'>Index</a></p></header><main>{body}</main></body></html>"
    )


def _html_card(record: dict[str, Any], quality: dict[str, Any], prefix: str = "") -> str:
    paths = record["review_pack_v2_crop_paths"]
    crops = [
        ("cell x4", paths["cell_crop_x4"]),
        ("glyph x8", paths["glyph_candidate_crop_x8"]),
        ("context small", paths["context_small"]),
        ("context medium", paths["context_medium"]),
        ("context large", paths["context_large"]),
        ("row", paths["row_context"]),
        ("row overlay", paths["row_context_overlay"]),
        ("strip overlay", paths["page_strip_overlay"]),
        ("debug overlay", paths["debug_overlay"]),
    ]
    crop_html = "".join(_html_crop_figure(label, prefix + path, record["challenge_id"]) for label, path in crops)
    classes = "".join(f"<span class='pill'>{html.escape(item)}</span>" for item in record["ambiguity_classes"])
    candidates = ", ".join(html.escape(item) for item in record["candidate_tokens"])
    return (
        f"<section class='card' data-challenge-id='{html.escape(record['challenge_id'])}'>"
        f"<h2>{html.escape(record['challenge_id'])}: {html.escape(record['canonical_token'])}</h2>"
        f"<p>{classes}</p><p class='meta'>page {record['page_number']} row {record['global_row_index_1_based']} col {record['column_index_1_based']} | candidates: {candidates}</p>"
        f"<p class='meta'>crop quality: {html.escape(quality['crop_quality_status'])}; glyph candidate status: {html.escape(quality['glyph_candidate_status'])}</p>"
        f"<div class='grid'>{crop_html}</div>"
        "<p class='meta'>Decision fields are blank in decision-template.yaml/json/csv. Derived crops and overlays are not source truth.</p>"
        "</section>"
    )


def _html_crop_figure(label: str, path: str, challenge_id: str) -> str:
    escaped_path = html.escape(path)
    return (
        f"<figure class='crop'><figcaption>{html.escape(label)}</figcaption>"
        f"<a href='{escaped_path}'><img src='{escaped_path}' alt='{html.escape(label)} for {html.escape(challenge_id)}'></a>"
        "</figure>"
    )


def build_stage5au_null_control_update(
    *,
    stage5at_null_control_update: Path,
    case_challenges_v2: Path,
    crop_quality: Path,
    out: Path,
) -> dict[str, Any]:
    source = read_yaml(stage5at_null_control_update)
    cases = read_yaml(case_challenges_v2)
    quality = read_yaml(crop_quality)
    payload = {
        "record_type": "null_control_review_pack_update",
        "schema": "schemas/token-block/null-control-review-pack-update-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "source_stage5at_null_control_update": source.get("record_type"),
        "review_pack_v2_null_controls_added": True,
        "case_challenge_count": cases.get("challenge_count"),
        "crop_quality_diagnostic_count": quality.get("diagnostic_count"),
        "controls": [
            "non-ambiguous control rows remain visible in canonical review",
            "not-reviewable decision remains available",
            "cell-only fallback status is explicit",
            "derived crop warnings are preserved for manual reviewers",
        ],
        "execution_enabled": False,
        "automatic_case_resolution_performed": False,
        "no_solve_claim": True,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    write_yaml(out, payload)
    return payload


def build_stage5au_dwh_review_pack_context(*, out: Path) -> dict[str, Any]:
    payload = {
        "record_type": "dwh_review_pack_context",
        "schema": "schemas/token-block/dwh-review-pack-context-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "dwh_expansion": "Deep Web Hash",
        "review_pack_relevance": "case-sensitive token decisions may affect future byte/value interpretations, but Stage 5AU performs no hash or decode work",
        "hash_search_performed": False,
        "hash_preimage_search_performed": False,
        "decode_attempt_performed": False,
        "execution_enabled": False,
        "no_solve_claim": True,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    write_yaml(out, payload)
    return payload


def build_stage5au_summary(
    *,
    usability_audit: Path,
    crop_geometry_policy: Path,
    crop_quality: Path,
    case_challenges_v2: Path,
    canonical_challenges_v2: Path,
    pack_manifest: Path,
    ui_coverage: Path,
    decision_template_v2: Path,
    null_control_update: Path,
    dwh_context: Path,
    out_guardrail: Path,
    out_next_stage: Path,
    out_summary: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    audit = read_yaml(usability_audit)
    policy = read_yaml(crop_geometry_policy)
    quality = read_yaml(crop_quality)
    cases = read_yaml(case_challenges_v2)
    canonical = read_yaml(canonical_challenges_v2)
    pack = read_yaml(pack_manifest)
    ui = read_yaml(ui_coverage)
    decisions = read_yaml(decision_template_v2)
    nulls = read_yaml(null_control_update)
    dwh = read_yaml(dwh_context)
    guardrail = {
        "record_type": "stage5au_guardrail",
        "schema": "schemas/token-block/stage5au-guardrail-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "manual_review_required": True,
        "automatic_case_resolution_performed": False,
        "canonical_transcription_changed": False,
        "generated_crops_committed": False,
        "generated_overlays_committed": False,
        "generated_review_pack_committed": False,
        "raw_images_committed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "llm_vision_token_reading_performed": False,
        "semantic_image_interpretation_performed": False,
        "hidden_content_image_forensics_performed": False,
        "stego_tool_execution_performed": False,
        "hash_preimage_search_performed": False,
        "decode_attempt_performed": False,
        "cuda_execution_performed": False,
        "cuda_source_modified": False,
        "benchmark_performed": False,
        "scored_experiments_executed": False,
        "solve_claim": False,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    next_stage = {
        "record_type": "stage5au_next_stage_decision",
        "schema": "schemas/project-state/stage5au-summary-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "status": "complete",
        "selected_next_stage_short_name": "Stage 5AV",
        "selected_next_stage_title": "Stage 5AV - manual human review of token case challenge pack v2",
        "selected_next_prompt_type": "manual_human_review",
        "selection_reason": "The v2 pack renders all case and canonical challenges, but no human decision file is present or integrated.",
        "manual_human_review_recommended": True,
        "codex_integration_next_ready": False,
        "bounded_preflight_recommended": False,
        "scored_experiments_recommended": False,
        "unsolved_page_cuda_recommended": False,
        "public_website_expansion_recommended": False,
        "execution_enabled": False,
        "no_solve_claim": True,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    summary = {
        "record_type": "stage5au_review_pack_usability_fix_summary",
        "schema": "schemas/project-state/stage5au-summary-v0.schema.json",
        "stage_id": STAGE5AU_ID,
        "status": "complete",
        "source_stage_id": "stage-5at",
        "stage5at_manual_review_usable": audit["stage5at_manual_review_usable"],
        "manual_review_should_proceed_from_stage5at_pack": audit["manual_review_should_proceed_from_stage5at_pack"],
        "repair_required": audit["repair_required"],
        "crop_geometry_policy_created": policy.get("source_original_images_only"),
        "review_pack_v2_generated": pack["review_pack_v2_generated"],
        "review_pack_v2_root": pack["review_pack_v2_root"],
        "review_pack_v2_zip_path": pack["review_pack_v2_zip_path"],
        "review_pack_v2_zip_sha256": pack["review_pack_v2_zip_sha256"],
        "case_review_challenge_count": cases["challenge_count"],
        "canonical_transcription_challenge_count": canonical["challenge_count"],
        "all_case_challenges_rendered": ui["all_203_case_challenges_visible_or_linked"],
        "all_canonical_challenges_rendered": ui["all_212_canonical_challenges_visible_or_linked"],
        "generated_crop_count": pack["generated_crop_count"],
        "glyph_candidate_crop_count": quality["glyph_candidate_crop_count"],
        "context_crop_count": quality["context_crop_count"],
        "row_context_crop_count": quality["row_context_crop_count"],
        "overlay_count": quality["overlay_count"],
        "quality_status_counts": quality["quality_status_counts"],
        "fallback_count": quality["fallback_count"],
        "unusable_count": quality["unusable_count"],
        "context_crops_visible": ui["context_small_visible_or_linked_for_every_challenge"]
        and ui["context_medium_visible_or_linked_for_every_challenge"]
        and ui["context_large_visible_or_linked_for_every_challenge"],
        "row_context_visible": ui["row_context_visible_or_linked_for_every_challenge"],
        "overlays_visible": ui["overlays_visible_or_linked_for_every_challenge"],
        "decision_template_v2_created": decisions["decision_count"] == cases["challenge_count"],
        "human_review_decisions_present": decisions["human_review_decisions_present"],
        "human_review_decisions_integrated": decisions["human_review_decisions_integrated"],
        "canonical_transcription_changed": False,
        "canonical_transcription_change_allowed": False,
        "automatic_case_resolution_performed": False,
        "null_control_review_pack_update_created": nulls["review_pack_v2_null_controls_added"],
        "dwh_review_pack_context_created": dwh["dwh_expansion"] == "Deep Web Hash",
        "manual_human_review_next_ready": True,
        "codex_integration_next_ready": False,
        **STAGE5AU_FALSE_GUARDRAILS,
    }
    write_yaml(out_guardrail, guardrail)
    write_yaml(out_next_stage, next_stage)
    write_yaml(out_summary, summary)
    return guardrail, next_stage, summary


def validate_stage5au(
    *,
    usability_audit: Path,
    crop_geometry_policy: Path,
    crop_quality: Path,
    case_challenges_v2: Path,
    canonical_challenges_v2: Path,
    pack_manifest: Path,
    ui_coverage: Path,
    decision_template_v2: Path,
    null_control_update: Path,
    dwh_context: Path,
    guardrail: Path,
    next_stage_decision: Path,
    summary: Path,
    review_pack_root: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    audit = read_yaml(usability_audit)
    policy = read_yaml(crop_geometry_policy)
    quality = read_yaml(crop_quality)
    cases = read_yaml(case_challenges_v2)
    canonical = read_yaml(canonical_challenges_v2)
    pack = read_yaml(pack_manifest)
    ui = read_yaml(ui_coverage)
    decisions = read_yaml(decision_template_v2)
    nulls = read_yaml(null_control_update)
    dwh = read_yaml(dwh_context)
    guard = read_yaml(guardrail)
    next_stage = read_yaml(next_stage_decision)
    summary_record = read_yaml(summary)
    errors: list[str] = []
    if audit.get("stage5at_manual_review_usable") is not False:
        errors.append("stage5at_usability_audit_not_failed")
    if policy.get("source_original_images_only") is not True:
        errors.append("crop_policy_not_original_only")
    if cases.get("challenge_count") != 203:
        errors.append("case_challenge_count_not_203")
    if canonical.get("challenge_count") != 212:
        errors.append("canonical_challenge_count_not_212")
    if quality.get("diagnostic_count") != cases.get("challenge_count"):
        errors.append("crop_quality_count_mismatch")
    if decisions.get("decision_count") != cases.get("challenge_count") or decisions.get("codex_filled_decisions") is not False:
        errors.append("decision_template_not_blank_or_complete")
    if pack.get("review_pack_v2_generated") is not True or not review_pack_root.exists():
        errors.append("review_pack_v2_missing")
    if ui.get("all_203_case_challenges_visible_or_linked") is not True:
        errors.append("case_challenges_not_all_visible")
    if ui.get("all_212_canonical_challenges_visible_or_linked") is not True:
        errors.append("canonical_challenges_not_all_visible")
    if nulls.get("review_pack_v2_null_controls_added") is not True:
        errors.append("null_control_update_missing")
    if dwh.get("hash_search_performed") is not False or dwh.get("decode_attempt_performed") is not False:
        errors.append("dwh_guardrail_failed")
    if next_stage.get("selected_next_stage_short_name") != "Stage 5AV":
        errors.append("next_stage_not_5av")
    for key in (
        "automatic_case_resolution_performed",
        "canonical_transcription_changed",
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "llm_vision_token_reading_performed",
        "semantic_image_interpretation_performed",
        "hidden_content_image_forensics_performed",
        "stego_tool_execution_performed",
        "hash_preimage_search_performed",
        "decode_attempt_performed",
        "cuda_execution_performed",
        "cuda_source_modified",
        "benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
    ):
        if guard.get(key) not in (False, 0):
            errors.append(f"{key}_not_false")
    counts = {
        "stage_id": STAGE5AU_ID,
        "stage5at_manual_review_usable": audit.get("stage5at_manual_review_usable"),
        "case_review_challenge_count": cases.get("challenge_count"),
        "canonical_transcription_challenge_count": canonical.get("challenge_count"),
        "generated_crop_count": pack.get("generated_crop_count"),
        "glyph_candidate_crop_count": quality.get("glyph_candidate_crop_count"),
        "context_crop_count": quality.get("context_crop_count"),
        "row_context_crop_count": quality.get("row_context_crop_count"),
        "overlay_count": quality.get("overlay_count"),
        "fallback_count": quality.get("fallback_count"),
        "unusable_count": quality.get("unusable_count"),
        "review_pack_v2_zip_sha256": pack.get("review_pack_v2_zip_sha256"),
        "all_case_challenges_rendered": summary_record.get("all_case_challenges_rendered"),
        "all_canonical_challenges_rendered": summary_record.get("all_canonical_challenges_rendered"),
        "canonical_transcription_changed": summary_record.get("canonical_transcription_changed"),
        "human_review_decisions_present": summary_record.get("human_review_decisions_present"),
        "human_review_decisions_integrated": summary_record.get("human_review_decisions_integrated"),
        "selected_next_stage_title": next_stage.get("selected_next_stage_title"),
        "manual_human_review_recommended": next_stage.get("manual_human_review_recommended"),
        "ocr_performed": guard.get("ocr_performed"),
        "cuda_execution_performed": guard.get("cuda_execution_performed"),
        "new_cuda_kernels_added": guard.get("new_cuda_kernels_added"),
        "validation_error_count": len(errors),
    }
    _ = results_dir
    return counts, errors
