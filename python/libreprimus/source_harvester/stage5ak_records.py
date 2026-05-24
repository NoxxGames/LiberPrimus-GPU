"""Stage 5AK guardrail, next-stage, and summary records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_yaml, write_json, write_jsonl, write_records, write_yaml
from .local_inventory import _staged_raw_files_present, _tracked_raw_files_present
from .models import (
    STAGE5AK_ATTACHMENT_INDEX_PATH,
    STAGE5AK_CLAIM_POLICY_PATH,
    STAGE5AK_CLAIM_RECORDS_PATH,
    STAGE5AK_CLUE_CATEGORIES_PATH,
    STAGE5AK_CONTENT_INDEX_SUMMARY_PATH,
    STAGE5AK_DEEP_RESEARCH_UPDATE_PATH,
    STAGE5AK_FALSE_FLAGS,
    STAGE5AK_GUARDRAIL_PATH,
    STAGE5AK_ID,
    STAGE5AK_INVENTORY_PATH,
    STAGE5AK_MISSING_SOURCE_PLAN_PATH,
    STAGE5AK_NEXT_STAGE_DECISION_PATH,
    STAGE5AK_OUTPUT_DIR,
    STAGE5AK_READINESS_PATH,
    STAGE5AK_REPORTS,
    STAGE5AK_SOURCE_CARD_SUMMARY_PATH,
    STAGE5AK_SOURCE_ROOT,
    STAGE5AK_SOURCE_STAGE_ID,
    STAGE5AK_SUMMARY_PATH,
    STAGE5AK_WEBSITE_UPDATE_PATH,
)


def build_stage5ak_guardrail(
    *,
    source_root: Path = STAGE5AK_SOURCE_ROOT,
    results_dir: Path = STAGE5AK_OUTPUT_DIR,
    out: Path = STAGE5AK_GUARDRAIL_PATH,
) -> dict[str, Any]:
    """Write Stage 5AK guardrail record."""

    guardrail = {
        "record_type": "stage5ak_guardrail",
        "schema": "schemas/source-harvester/stage5ak-summary-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "local_folder": source_root.as_posix(),
        "local_folder_exists": source_root.exists(),
        **STAGE5AK_FALSE_FLAGS,
        "third_party_raw_staged": _staged_raw_files_present(source_root),
        "third_party_raw_tracked_new": _tracked_raw_files_present(source_root),
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }
    write_yaml(out, guardrail)
    write_json(results_dir / "guardrail.json", guardrail)
    return guardrail


def build_stage5ak_next_stage_decision(
    *,
    readiness_path: Path = STAGE5AK_READINESS_PATH,
    claim_records_path: Path = STAGE5AK_CLAIM_RECORDS_PATH,
    missing_source_plan_path: Path = STAGE5AK_MISSING_SOURCE_PLAN_PATH,
    out: Path = STAGE5AK_NEXT_STAGE_DECISION_PATH,
) -> dict[str, Any]:
    """Select the next stage after community-facts integration."""

    readiness = read_yaml(readiness_path)
    claims = read_yaml(claim_records_path)
    missing = read_yaml(missing_source_plan_path)
    selected = _select_next(readiness, claims, missing)
    records = []
    for option_id, title, reason in _decision_options():
        is_selected = option_id == selected
        records.append(
            {
                "record_type": "stage5ak_next_stage_decision_record",
                "schema": "schemas/source-harvester/stage5ak-summary-v0.schema.json",
                "stage_id": STAGE5AK_ID,
                "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
                "option_id": option_id,
                "selected": is_selected,
                "recommended_next_prompt_type": "Deep Research" if is_selected and "deep_research" in option_id else ("Codex" if is_selected else None),
                "recommended_next_stage_title": title,
                "recommended_next_stage_reason": reason,
                "deep_research_recommended_next": is_selected and "deep_research" in option_id,
                "scored_experiment_recommended_next": False,
                "benchmark_recommended_next": False,
                "unsolved_page_cuda_recommended_next": False,
                "website_expansion_recommended_next": False,
                "execution_enabled": False,
                "solve_claim": False,
            }
        )
    header = {
        "record_type": "stage5ak_next_stage_decisions",
        "schema": "schemas/source-harvester/stage5ak-summary-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "selected_option_id": selected,
        "solve_claim": False,
    }
    write_records(out, records, **header)
    return {**header, "records": records}


def build_stage5ak_summary(
    *,
    inventory_path: Path = STAGE5AK_INVENTORY_PATH,
    source_card_summary_path: Path = STAGE5AK_SOURCE_CARD_SUMMARY_PATH,
    content_index_summary_path: Path = STAGE5AK_CONTENT_INDEX_SUMMARY_PATH,
    attachment_index_path: Path = STAGE5AK_ATTACHMENT_INDEX_PATH,
    clue_categories_path: Path = STAGE5AK_CLUE_CATEGORIES_PATH,
    claim_policy_path: Path = STAGE5AK_CLAIM_POLICY_PATH,
    claim_records_path: Path = STAGE5AK_CLAIM_RECORDS_PATH,
    correction_log_path: Path | None = None,
    arithmetic_preflight_path: Path | None = None,
    website_update_path: Path = STAGE5AK_WEBSITE_UPDATE_PATH,
    deep_research_update_path: Path = STAGE5AK_DEEP_RESEARCH_UPDATE_PATH,
    readiness_path: Path = STAGE5AK_READINESS_PATH,
    missing_source_plan_path: Path = STAGE5AK_MISSING_SOURCE_PLAN_PATH,
    guardrail_path: Path = STAGE5AK_GUARDRAIL_PATH,
    next_stage_decision_path: Path = STAGE5AK_NEXT_STAGE_DECISION_PATH,
    out: Path = STAGE5AK_SUMMARY_PATH,
    results_dir: Path = STAGE5AK_OUTPUT_DIR,
) -> dict[str, Any]:
    """Build the committed Stage 5AK aggregate summary."""

    from .models import STAGE5AK_ARITHMETIC_PREFLIGHT_PATH, STAGE5AK_CORRECTION_LOG_PATH

    correction_log_path = correction_log_path or STAGE5AK_CORRECTION_LOG_PATH
    arithmetic_preflight_path = arithmetic_preflight_path or STAGE5AK_ARITHMETIC_PREFLIGHT_PATH
    inventory = read_yaml(inventory_path)
    cards = read_yaml(source_card_summary_path)
    content = read_yaml(content_index_summary_path)
    attachments = read_yaml(attachment_index_path)
    categories = read_yaml(clue_categories_path)
    del claim_policy_path
    claims = read_yaml(claim_records_path)
    corrections = read_yaml(correction_log_path)
    arithmetic = read_yaml(arithmetic_preflight_path)
    website = read_yaml(website_update_path)
    deep = read_yaml(deep_research_update_path)
    readiness = read_yaml(readiness_path)
    missing = read_yaml(missing_source_plan_path)
    guardrail = read_yaml(guardrail_path)
    decision = read_yaml(next_stage_decision_path)
    selected = [record for record in decision.get("records", []) if record.get("selected") is True][0]
    summary = {
        "record_type": "stage5ak_community_facts_integration_summary",
        "schema": "schemas/source-harvester/stage5ak-summary-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "status": "complete",
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "local_folder": inventory.get("source_root"),
        "local_folder_exists": inventory.get("local_folder_exists", False),
        "community_facts_file_count": inventory.get("community_facts_file_count", 0),
        "community_facts_total_size_bytes": inventory.get("community_facts_total_size_bytes", 0),
        "message_log_detected": inventory.get("message_log_detected", False),
        "message_log_hash": inventory.get("message_log_hash"),
        "attachment_count": attachments.get("attachment_images_detected", 0),
        "attachment_images_detected": attachments.get("attachment_images_detected", 0),
        "attachment_index_records": attachments.get("attachment_index_records", 0),
        "new_local_source_records": inventory.get("new_local_source_records", 0),
        "new_clue_category_records": categories.get("new_clue_category_records", 0),
        "community_claim_records": claims.get("claim_record_count", 0),
        "community_correction_records": corrections.get("correction_record_count", 0),
        "arithmetic_preflight_records": arithmetic.get("arithmetic_preflight_records", 0),
        "arithmetic_verified_count": arithmetic.get("arithmetic_verified_count", 0),
        "arithmetic_error_count": arithmetic.get("arithmetic_error_count", 0),
        "source_lock_required_count": claims.get("source_lock_required_count", 0),
        "requires_null_controls_count": claims.get("requires_null_controls_count", 0),
        "requires_image_coordinate_policy_count": sum(
            1 for record in claims.get("records", []) if record.get("verification_status") == "requires_image_coordinate_policy"
        ),
        "requires_transcript_policy_count": sum(1 for record in claims.get("records", []) if record.get("requires_exact_transcript")),
        "source_card_updates": cards.get("source_card_updates", cards.get("source_card_records", 0)),
        "content_index_updates": content.get("content_index_updates", content.get("content_index_records", 0)),
        "website_ingest_updates": website.get("website_ingest_updates", 0),
        "deep_research_pack_updates": deep.get("deep_research_pack_updates", 0),
        "bundle_readiness_before": readiness.get("bundle_readiness_before", 0),
        "bundle_readiness_after": readiness.get("bundle_readiness_after", 0),
        "bundles_ready_for_private_deep_research": readiness.get("bundles_ready_for_private_deep_research", 0),
        "bundles_public_website_ready": readiness.get("bundles_public_website_ready", 0),
        "community_facts_private_publication_blocked": True,
        "website_ingest_metadata_ready": website.get("website_ingest_metadata_ready", False),
        "missing_source_records": missing.get("missing_source_records", 0),
        "recommended_next_prompt_type": selected.get("recommended_next_prompt_type"),
        "recommended_next_stage_title": selected.get("recommended_next_stage_title"),
        "recommended_next_stage_reason": selected.get("recommended_next_stage_reason"),
        "deep_research_recommended_next": selected.get("deep_research_recommended_next", False),
        **{key: guardrail.get(key, False) for key in STAGE5AK_FALSE_FLAGS},
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }
    write_yaml(out, summary)
    write_json(results_dir / STAGE5AK_REPORTS["summary"], summary)
    write_jsonl(results_dir / STAGE5AK_REPORTS["warnings"], [])
    return summary


def _select_next(readiness: dict[str, Any], claims: dict[str, Any], missing: dict[str, Any]) -> str:
    if readiness.get("bundles_ready_for_private_deep_research", 0) >= 10 and claims.get("claim_record_count", 0) >= 12:
        return "stage5al_deep_research_source_inventory_and_reliability_prompt"
    if claims.get("claim_record_count", 0) >= 12:
        return "stage5al_deep_research_community_number_facts_review_prompt"
    if missing.get("missing_source_records", 0) > 1:
        return "stage5al_source_gap_closure_for_missing_priority_sources"
    return "stage5al_deep_research_source_inventory_and_reliability_prompt"


def _decision_options() -> list[tuple[str, str, str]]:
    return [
        (
            "stage5al_deep_research_source_inventory_and_reliability_prompt",
            "Stage 5AL - Deep Research source inventory and reliability prompt",
            "Community-facts metadata and claim records integrated cleanly; Deep Research can consume curated manifests and source cards.",
        ),
        (
            "stage5al_deep_research_community_number_facts_review_prompt",
            "Stage 5AL - Deep Research community number facts review prompt",
            "Use only if the community number-fact claim layer should be reviewed before broader source inventory.",
        ),
        ("stage5al_targeted_online_fetch_for_new_links", "Stage 5AL - targeted online fetch for new links", "Deferred; Stage 5AK used local files only."),
        ("stage5al_source_gap_closure_for_missing_priority_sources", "Stage 5AL - source gap closure for missing priority sources", "Deferred unless Deep Research exposes blocking source gaps."),
        ("stage5al_count_policy_reconciliation_preflight", "Stage 5AL - count policy reconciliation preflight", "Deferred; useful after Deep Research reviews claim reliability."),
        ("stage5al_lp_excel_delimiter_transcript_source_lock", "Stage 5AL - LP Excel delimiter transcript source-lock", "Deferred; UsefulFiles workbooks remain source-lock metadata only."),
        ("stage5al_visual_page_image_provenance_inventory", "Stage 5AL - visual page image provenance inventory", "Deferred; no image forensics in Stage 5AK."),
        ("stage5al_page49_51_token_block_extraction", "Stage 5AL - page 49-51 token block extraction", "Deferred; not selected by community-facts curation."),
        ("stage5al_cuneiform_red_marker_visual_numeric_extraction", "Stage 5AL - cuneiform red marker visual numeric extraction", "Deferred; would require explicit visual-source policy."),
        ("stage5al_discord_private_lead_redaction_plan", "Stage 5AL - Discord private lead redaction plan", "Deferred; private metadata is ready but not public."),
        ("stage5al_bounded_cpu_native_scored_experiment_manifest_gate", "Stage 5AL - bounded CPU/native scored experiment manifest gate", "Rejected; claim records are not execution-ready."),
        ("stage5al_benchmark_planning", "Stage 5AL - benchmark planning", "Rejected; Stage 5AK is source curation only."),
        ("stage5al_unsolved_page_cuda_pilot", "Stage 5AL - unsolved-page CUDA pilot", "Rejected; unsolved-page CUDA remains blocked."),
        ("future_website_expansion_unnumbered", "Future unnumbered website expansion", "Deferred; public website publication is review-gated."),
    ]
