"""Stage 5AR summary, updates, guardrails, and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import FALSE_GUARDRAILS, STAGE5AR_ID, TOKEN_BLOCK_ID, read_yaml, repo_relative, write_json, write_yaml


def build_stage5ar_updates(
    *,
    stage5ap_source_lock: Path,
    stage5ap_null_control_plan: Path,
    coordinate_validation: Path,
    case_policy: Path,
    page_split_records: Path,
    out_source_lock_update: Path,
    out_null_control_update: Path,
    out_dwh_context: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    stage5ap_source = read_yaml(stage5ap_source_lock)
    stage5ap_nulls = read_yaml(stage5ap_null_control_plan)
    validation = read_yaml(coordinate_validation)
    read_yaml(case_policy)
    split = read_yaml(page_split_records)
    source_update = {
        "record_type": "token_block_source_lock_update",
        "schema": "schemas/token-block/token-block-source-lock-update-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "source_stage_id": stage5ap_source.get("stage_id"),
        "previous_source_lock_status": stage5ap_source.get("source_lock_status"),
        "updated_source_lock_status": "original_image_pixel_coordinate_review_required",
        "page_split_status": split.get("page_split_status"),
        "coordinate_validation_status": validation.get("coordinate_validation_status"),
        "execution_enabled": False,
        "no_decode": True,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    null_controls = {
        "case_confusion_controls": [
            "I/l swap control",
            "O/0 swap control",
            "1/I/l ambiguity control",
            "S/5 ambiguity control",
        ],
        "page_split_controls": [
            "accepted 10/13/9 split",
            "alternative 11/11/10 split",
            "row-shuffled split preserving page row counts",
            "no-page-boundary control",
        ],
        "coordinate_controls": [
            "row-order reversal",
            "column-order reversal",
            "per-page local reading order",
            "global 32-row reading order",
        ],
    }
    null_update = {
        "record_type": "token_block_null_control_update",
        "schema": "schemas/token-block/token-block-null-control-update-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "source_null_control_plan": repo_relative(stage5ap_null_control_plan),
        "source_null_control_count": stage5ap_nulls.get("null_control_count"),
        "coordinate_specific_controls_created": True,
        **null_controls,
        "execution_enabled": False,
        "no_decode": True,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    dwh = {
        "record_type": "dwh_coordinate_context",
        "schema": "schemas/token-block/dwh-coordinate-context-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "dwh_defined": True,
        "dwh_expansion": "Deep Web Hash",
        "page56_an_end_context": True,
        "token_block_dwh_relationship_status": "speculative_source_lock_required",
        "coordinate_lock_relevance": "page split and pixel coordinates are prerequisites for any physical-layout DWH interpretation",
        "hash_search_performed": False,
        "hash_preimage_claim": False,
        "decode_claim": False,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out_source_lock_update, source_update)
    write_yaml(out_null_control_update, null_update)
    write_yaml(out_dwh_context, dwh)
    return source_update, null_update, dwh


def build_stage5ar_summary(
    *,
    original_source_lock: Path,
    variants: Path,
    page_split_policy: Path,
    page_split_records: Path,
    pixel_coordinate_policy: Path,
    pixel_coordinate_records: Path,
    case_policy: Path,
    case_ambiguities: Path,
    coordinate_validation: Path,
    source_lock_update: Path,
    null_control_update: Path,
    dwh_context: Path,
    out_guardrail: Path,
    out_next_stage: Path,
    out_summary: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source = read_yaml(original_source_lock)
    variant_data = read_yaml(variants)
    split_policy = read_yaml(page_split_policy)
    split_records = read_yaml(page_split_records)
    pixel_policy = read_yaml(pixel_coordinate_policy)
    pixel_records = read_yaml(pixel_coordinate_records)
    case_data = read_yaml(case_policy)
    ambiguity_data = read_yaml(case_ambiguities)
    validation = read_yaml(coordinate_validation)
    source_update = read_yaml(source_lock_update)
    null_update = read_yaml(null_control_update)
    dwh = read_yaml(dwh_context)
    coordinate_valid = validation.get("coordinate_validation_status") == "valid_with_review_required"
    original_ready = source.get("coordinate_source_available") is True
    selected_next = (
        "Stage 5AS - Deep Research page 49-51 original-image coordinate review and bounded token-block preflight planning"
        if coordinate_valid and original_ready
        else "Stage 5AS - targeted original page-image source-gap closure"
    )
    guardrail = {
        "record_type": "stage5ar_guardrail",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "original_images_required": True,
        "screenshots_forbidden_as_coordinate_sources": True,
        "raw_images_committed": False,
        "generated_overlays_committed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "semantic_image_interpretation_performed": False,
        "hidden_content_image_forensics_performed": False,
        "stego_tool_execution_performed": False,
        "decode_attempted": False,
        "hash_preimage_search_performed": False,
        "cuda_execution_performed": False,
        "cuda_source_modified": False,
        "new_cuda_kernels_added": 0,
        "benchmark_performed": False,
        "scored_experiments_executed": False,
        "solve_claim": False,
        **FALSE_GUARDRAILS,
    }
    next_stage = {
        "record_type": "stage5ar_next_stage_decision",
        "schema": "schemas/project-state/stage5ar-summary-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "status": "complete",
        "selected_next_stage_short_name": "Stage 5AS",
        "selected_next_stage_title": selected_next,
        "selected_next_prompt_type": "deep_research_coordinate_review" if coordinate_valid else "codex_source_gap_closure",
        "selection_reason": "Original images are available and coordinate records validate with review-required confidence."
        if coordinate_valid and original_ready
        else "Original-image coordinate source gap remains unresolved.",
        "deep_research_recommended_next": coordinate_valid and original_ready,
        "source_gap_closure_recommended_next": not (coordinate_valid and original_ready),
        "scored_experiments_recommended": False,
        "unsolved_page_cuda_recommended": False,
        "public_website_expansion_recommended": False,
        "execution_enabled": False,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    guardrail_fields = {
        key: value
        for key, value in guardrail.items()
        if key not in {"record_type", "stage_id", "token_block_id"}
    }
    summary = {
        "record_type": "stage5ar_summary",
        "schema": "schemas/project-state/stage5ar-summary-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "status": "complete",
        "token_block_id": TOKEN_BLOCK_ID,
        "original_page_images_found": source.get("selected_original_image_count", 0),
        "original_page_images_selected": source.get("selected_original_image_count", 0),
        "original_page_images_missing": len(source.get("missing_original_pages", [])),
        "variant_record_count": variant_data.get("variant_record_count", 0),
        "page_split_status": split_policy.get("page_split_status"),
        "page_split_accepted": split_policy.get("accepted"),
        "page_49_row_count": split_records.get("page_49_row_count"),
        "page_50_row_count": split_records.get("page_50_row_count"),
        "page_51_row_count": split_records.get("page_51_row_count"),
        "token_pixel_coordinate_record_count": pixel_records.get("coordinate_record_count", 0),
        "coordinate_validation_status": validation.get("coordinate_validation_status"),
        "coordinate_method": pixel_policy.get("coordinate_method"),
        "unresolved_coordinate_count": validation.get("unresolved_coordinate_count", 0),
        "case_ambiguity_record_count": ambiguity_data.get("ambiguity_record_count", 0),
        "case_policy_unresolved_count": case_data.get("unresolved_ambiguity_class_count", 0),
        "canonical_transcription_changed": case_data.get("canonical_transcription_changed"),
        "null_control_update_created": null_update.get("coordinate_specific_controls_created"),
        "dwh_coordinate_context_created": dwh.get("dwh_defined"),
        "source_lock_update_status": source_update.get("updated_source_lock_status"),
        "selected_next_stage_title": selected_next,
        "deep_research_recommended_next": next_stage["deep_research_recommended_next"],
        "source_gap_closure_recommended_next": next_stage["source_gap_closure_recommended_next"],
        "original_images_required": True,
        "screenshots_forbidden_as_coordinate_sources": True,
        "no_decode": True,
        "no_hash_preimage_search": True,
        "no_solve_claim": True,
        **guardrail_fields,
    }
    write_yaml(out_guardrail, guardrail)
    write_yaml(out_next_stage, next_stage)
    write_yaml(out_summary, summary)
    write_json(results_dir / "summary.json", summary)
    return guardrail, next_stage, summary


def validate_stage5ar(
    *,
    original_source_lock: Path,
    variants: Path,
    page_split_policy: Path,
    page_split_records: Path,
    pixel_coordinate_policy: Path,
    pixel_coordinate_records: Path,
    case_policy: Path,
    case_ambiguities: Path,
    coordinate_validation: Path,
    source_lock_update: Path,
    null_control_update: Path,
    dwh_context: Path,
    guardrail: Path,
    next_stage_decision: Path,
    summary: Path,
) -> tuple[dict[str, Any], list[str]]:
    source = read_yaml(original_source_lock)
    read_yaml(variants)
    split_policy = read_yaml(page_split_policy)
    split_records = read_yaml(page_split_records)
    read_yaml(pixel_coordinate_policy)
    pixel_records = read_yaml(pixel_coordinate_records)
    cases = read_yaml(case_policy)
    read_yaml(case_ambiguities)
    validation = read_yaml(coordinate_validation)
    read_yaml(source_lock_update)
    null_update = read_yaml(null_control_update)
    dwh = read_yaml(dwh_context)
    guard = read_yaml(guardrail)
    next_stage = read_yaml(next_stage_decision)
    summary_record = read_yaml(summary)
    errors: list[str] = []
    if source.get("coordinate_source_available") is not True:
        errors.append("original_coordinate_source_missing")
    if split_policy.get("accepted") is not True or split_records.get("row_count_sum") != 32:
        errors.append("page_split_not_valid")
    if pixel_records.get("coordinate_record_count") != 256:
        errors.append("pixel_coordinate_record_count_not_256")
    if validation.get("coordinate_validation_status") != "valid_with_review_required":
        errors.append("coordinate_validation_not_valid")
    if cases.get("canonical_transcription_changed") is not False:
        errors.append("canonical_transcription_changed")
    if null_update.get("coordinate_specific_controls_created") is not True:
        errors.append("null_control_update_missing")
    if dwh.get("hash_search_performed") is not False or dwh.get("decode_claim") is not False:
        errors.append("dwh_guardrail_failed")
    for key in ("ocr_performed", "ai_ml_interpretation_performed", "semantic_image_interpretation_performed", "hidden_content_image_forensics_performed", "cuda_execution_performed", "cuda_source_modified", "benchmark_performed", "scored_experiments_executed", "solve_claim"):
        if guard.get(key) not in (False, 0):
            errors.append(f"{key}_not_false")
    counts = {
        "stage_id": STAGE5AR_ID,
        "original_page_images_selected": source.get("selected_original_image_count", 0),
        "page_split_status": split_policy.get("page_split_status"),
        "token_pixel_coordinate_records": pixel_records.get("coordinate_record_count", 0),
        "coordinate_validation_status": validation.get("coordinate_validation_status"),
        "case_policy_unresolved_count": cases.get("unresolved_ambiguity_class_count", 0),
        "null_control_update_created": null_update.get("coordinate_specific_controls_created"),
        "dwh_coordinate_context_created": dwh.get("dwh_defined"),
        "selected_next_stage_title": next_stage.get("selected_next_stage_title"),
        "deep_research_recommended_next": next_stage.get("deep_research_recommended_next"),
        "network_fetch_performed": summary_record.get("network_fetch_performed"),
        "ocr_performed": guard.get("ocr_performed"),
        "cuda_execution_performed": guard.get("cuda_execution_performed"),
        "new_cuda_kernels_added": guard.get("new_cuda_kernels_added"),
        "validation_error_count": len(errors),
    }
    return counts, errors
