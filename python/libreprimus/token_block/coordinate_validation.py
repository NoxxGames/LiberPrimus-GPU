"""Stage 5AR coordinate validation helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import FALSE_GUARDRAILS, STAGE5AR_ID, TOKEN_BLOCK_ID, read_yaml, write_json, write_yaml
from .original_images import FORBIDDEN_VARIANT_CLASSES


def validate_coordinate_payload(
    *,
    original_image_source_lock: Path,
    page_split_records: Path,
    pixel_coordinate_policy: Path,
    pixel_coordinate_records: Path,
    case_policy: Path,
    case_ambiguities: Path,
    results_dir: Path,
    out: Path,
) -> dict[str, Any]:
    source_lock = read_yaml(original_image_source_lock)
    page_split = read_yaml(page_split_records)
    policy = read_yaml(pixel_coordinate_policy)
    coordinates = read_yaml(pixel_coordinate_records)
    cases = read_yaml(case_policy)
    ambiguities = read_yaml(case_ambiguities)
    errors: list[str] = []
    warnings: list[str] = []
    records = coordinates.get("records", [])
    if len(records) != 256:
        errors.append("pixel_coordinate_record_count_not_256")
    if page_split.get("row_count_sum") != 32:
        errors.append("page_split_row_count_sum_not_32")
    if page_split.get("accepted") is not True:
        errors.append("page_split_not_accepted")
    invalid_bbox_count = 0
    forbidden_reference_count = 0
    for record in records:
        if record.get("bbox_width", 0) <= 0 or record.get("bbox_height", 0) <= 0:
            invalid_bbox_count += 1
        width = record.get("original_image_width")
        height = record.get("original_image_height")
        if width is not None and record.get("bbox_x_max", 0) > width:
            invalid_bbox_count += 1
        if height is not None and record.get("bbox_y_max", 0) > height:
            invalid_bbox_count += 1
        if record.get("coordinate_source_class") in FORBIDDEN_VARIANT_CLASSES:
            forbidden_reference_count += 1
    if invalid_bbox_count:
        errors.append("invalid_pixel_bbox")
    if forbidden_reference_count:
        errors.append("coordinate_records_reference_forbidden_image_class")
    if cases.get("canonical_transcription_changed") is not False:
        errors.append("canonical_transcription_changed")
    if ambiguities.get("ambiguity_record_count", 0) < 9:
        errors.append("case_ambiguity_records_missing")
    if policy.get("ocr_performed") is not False:
        errors.append("ocr_performed_not_false")
    if source_lock.get("coordinate_source_available") is not True:
        warnings.append("controlled_source_gap_missing_original_images")
    validation_status = "valid_with_review_required" if not errors else "invalid"
    record = {
        "record_type": "token_coordinate_validation",
        "schema": "schemas/token-block/token-coordinate-validation-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "coordinate_validation_status": validation_status,
        "validation_error_count": len(errors),
        "validation_warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "token_coordinate_record_count": len(records),
        "invalid_bbox_count": invalid_bbox_count,
        "forbidden_image_reference_count": forbidden_reference_count,
        "unresolved_coordinate_count": sum(1 for item in records if str(item.get("coordinate_status", "")).startswith("blocked")),
        "case_policy_unresolved_count": cases.get("unresolved_ambiguity_class_count", 0),
        "page_split_row_count_sum": page_split.get("row_count_sum"),
        "page_split_status": page_split.get("page_split_status"),
        "original_images_available": source_lock.get("coordinate_source_available") is True,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "semantic_image_interpretation_performed": False,
        "hidden_content_image_forensics_performed": False,
        "decode_attempted": False,
        "hash_preimage_search_performed": False,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, record)
    write_json(results_dir / "token_coordinate_validation.json", record)
    return record
