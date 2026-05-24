"""Stage 5AJ guardrail, decision, category, and summary records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_yaml, write_json, write_jsonl, write_records, write_yaml
from .local_inventory import _staged_raw_files_present, _tracked_raw_files_present
from .models import (
    STAGE5AJ_FALSE_FLAGS,
    STAGE5AJ_GUARDRAIL_PATH,
    STAGE5AJ_ID,
    STAGE5AJ_NEW_CLUE_CATEGORIES_PATH,
    STAGE5AJ_NEXT_STAGE_DECISION_PATH,
    STAGE5AJ_OUTPUT_DIR,
    STAGE5AJ_REPORTS,
    STAGE5AJ_SOURCE_ROOT,
    STAGE5AJ_SOURCE_STAGE_ID,
    STAGE5AJ_SUMMARY_PATH,
)


CLUE_CATEGORIES = [
    "delimiter_preserving_lp_transcript",
    "manual_highlight_repeat_fragments",
    "section_boundary_repeat_network",
    "lp_count_policy_reconciliation",
    "p56_p57_gp_sum_3301_1033",
    "magic_square_diagonal_3301_1033",
    "page32_tree_path_lies_empty",
    "brown_corpus_word_length_controls",
    "bibliographic_liber_primus_euler_lead",
    "2016_prime_layering",
    "twitter_1033_3301_fibonacci_prime_context",
    "low_doublet_statistical_texture",
    "unverified_shift_pattern_warning",
    "excel_highlight_color_annotations",
    "workbook_formula_and_image_inventory",
    "reddit_claims_targeted_capture",
]


def build_stage5aj_new_clue_categories(
    *,
    out: Path = STAGE5AJ_NEW_CLUE_CATEGORIES_PATH,
) -> dict[str, Any]:
    """Write new Stage 5AJ clue category records."""

    records = [
        {
            "record_type": "stage5aj_new_clue_category_record",
            "schema": "schemas/source-harvester/stage5aj-summary-v0.schema.json",
            "stage_id": STAGE5AJ_ID,
            "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
            "category_id": category,
            "description": category.replace("_", " "),
            "source_lock_priority": "A1" if category in {"delimiter_preserving_lp_transcript", "p56_p57_gp_sum_3301_1033"} else "A2",
            "execution_ready": False,
            "requires_null_controls": category
            in {
                "brown_corpus_word_length_controls",
                "magic_square_diagonal_3301_1033",
                "low_doublet_statistical_texture",
                "reddit_claims_targeted_capture",
            },
            "risk_level": "high_false_positive_risk" if category.startswith(("magic_", "low_", "reddit_")) else "review_required",
            "recommended_sources": _recommended_sources(category),
            "what_not_to_assume": "Do not treat local/source-card presence as execution readiness or solve evidence.",
            "solve_claim": False,
        }
        for category in CLUE_CATEGORIES
    ]
    header = {
        "record_type": "stage5aj_new_clue_categories",
        "schema": "schemas/source-harvester/stage5aj-summary-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "new_clue_category_records": len(records),
        "execution_ready_count": 0,
        "solve_claim": False,
    }
    write_records(out, records, **header)
    return {**header, "records": records}


def build_stage5aj_guardrail(
    *,
    source_root: Path = STAGE5AJ_SOURCE_ROOT,
    results_dir: Path = STAGE5AJ_OUTPUT_DIR,
    out: Path = STAGE5AJ_GUARDRAIL_PATH,
) -> dict[str, Any]:
    """Write Stage 5AJ guardrail record."""

    root = source_root
    guardrail = {
        "record_type": "stage5aj_guardrail",
        "schema": "schemas/source-harvester/stage5aj-summary-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "local_folder": source_root.as_posix(),
        "local_folder_exists": source_root.exists(),
        **STAGE5AJ_FALSE_FLAGS,
        "third_party_raw_staged": _staged_raw_files_present(root),
        "third_party_raw_tracked_new": _tracked_raw_files_present(root),
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }
    write_yaml(out, guardrail)
    write_json(results_dir / "guardrail.json", guardrail)
    return guardrail


def build_stage5aj_next_stage_decision(
    *,
    summary_inputs: list[Path],
    out: Path = STAGE5AJ_NEXT_STAGE_DECISION_PATH,
) -> dict[str, Any]:
    """Select the next stage after UsefulFiles integration."""

    readiness = read_yaml(summary_inputs[0])
    missing = read_yaml(summary_inputs[1])
    selected = _select_next(readiness, missing)
    records = []
    for option_id, title, reason in _decision_options():
        is_selected = option_id == selected
        records.append(
            {
                "record_type": "stage5aj_next_stage_decision_record",
                "schema": "schemas/source-harvester/stage5aj-summary-v0.schema.json",
                "stage_id": STAGE5AJ_ID,
                "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
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
        "record_type": "stage5aj_next_stage_decisions",
        "schema": "schemas/source-harvester/stage5aj-summary-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "selected_option_id": selected,
        "solve_claim": False,
    }
    write_records(out, records, **header)
    return {**header, "records": records}


def build_stage5aj_summary(
    *,
    inventory_path: Path,
    manifest_extension_path: Path,
    source_card_summary_path: Path,
    content_index_summary_path: Path,
    xlsx_summary_path: Path,
    important_links_path: Path,
    new_clue_categories_path: Path,
    fidelity_policy_path: Path,
    redaction_policy_path: Path,
    scraper_policy_path: Path,
    website_update_path: Path,
    deep_research_update_path: Path,
    readiness_path: Path,
    missing_source_plan_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    out: Path = STAGE5AJ_SUMMARY_PATH,
    results_dir: Path = STAGE5AJ_OUTPUT_DIR,
) -> dict[str, Any]:
    """Build the committed Stage 5AJ aggregate summary."""

    del fidelity_policy_path, redaction_policy_path, scraper_policy_path
    inventory = read_yaml(inventory_path)
    manifest = read_yaml(manifest_extension_path)
    cards = read_yaml(source_card_summary_path)
    content = read_yaml(content_index_summary_path)
    xlsx = read_yaml(xlsx_summary_path)
    links = read_yaml(important_links_path)
    categories = read_yaml(new_clue_categories_path)
    website = read_yaml(website_update_path)
    deep = read_yaml(deep_research_update_path)
    readiness = read_yaml(readiness_path)
    missing = read_yaml(missing_source_plan_path)
    guardrail = read_yaml(guardrail_path)
    decision = read_yaml(next_stage_decision_path)
    selected = [record for record in decision.get("records", []) if record.get("selected") is True][0]
    summary = {
        "record_type": "stage5aj_usefulfiles_integration_summary",
        "schema": "schemas/source-harvester/stage5aj-summary-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "status": "complete",
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "local_folder": inventory.get("source_root"),
        "local_folder_exists": inventory.get("local_folder_exists", False),
        "usefulfiles_local_file_count": inventory.get("usefulfiles_local_file_count", 0),
        "usefulfiles_total_size_bytes": inventory.get("usefulfiles_total_size_bytes", 0),
        "new_local_source_records": manifest.get("local_source_records", 0),
        "new_url_source_records": manifest.get("new_url_source_records", 0),
        "new_clue_category_records": categories.get("new_clue_category_records", 0),
        "xlsx_workbooks_detected": xlsx.get("xlsx_workbooks_detected", 0),
        "xlsx_workbooks_summarized": xlsx.get("xlsx_workbooks_summarized", 0),
        "lp_excel_detected": xlsx.get("lp_excel_detected", False),
        "translations_decryptions_detected": xlsx.get("translations_decryptions_detected", False),
        "important_links_detected": links.get("important_links_detected", False),
        "important_links_urls_found": links.get("important_links_urls_found", 0),
        "important_links_new_urls": links.get("important_links_new_urls", 0),
        "ideas_file_detected": inventory.get("ideas_found", False),
        "gematria_image_detected": inventory.get("gematria_image_found", False),
        "source_card_updates": cards.get("source_card_records", 0),
        "content_index_updates": content.get("content_index_records", 0),
        "website_ingest_updates": website.get("website_ingest_content_records", 0),
        "deep_research_pack_updates": deep.get("deep_research_pack_records", 0),
        "bundle_readiness_before": readiness.get("bundle_readiness_before", 0),
        "bundle_readiness_after": readiness.get("bundle_readiness_after", 0),
        "bundles_ready_for_private_deep_research": readiness.get("bundles_ready_for_private_deep_research", 0),
        "bundles_public_website_ready": readiness.get("bundles_public_website_ready", 0),
        "extraction_fidelity_policy_created": True,
        "redaction_policy_created": True,
        "scraper_capture_policy_created": True,
        "no_over_redaction_policy_created": True,
        "missing_source_records": missing.get("missing_source_records", 0),
        "website_ingest_metadata_ready": website.get("website_ingest_metadata_ready", False),
        "recommended_next_prompt_type": selected.get("recommended_next_prompt_type"),
        "recommended_next_stage_title": selected.get("recommended_next_stage_title"),
        "recommended_next_stage_reason": selected.get("recommended_next_stage_reason"),
        "deep_research_recommended_next": selected.get("deep_research_recommended_next", False),
        **{key: guardrail.get(key, False) for key in STAGE5AJ_FALSE_FLAGS},
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }
    write_yaml(out, summary)
    write_json(results_dir / STAGE5AJ_REPORTS["summary"], summary)
    write_jsonl(results_dir / STAGE5AJ_REPORTS["warnings"], [])
    return summary


def _recommended_sources(category: str) -> list[str]:
    if "excel" in category or "delimiter" in category or "highlight" in category:
        return ["lp_excel_workbook_local"]
    if category.startswith("reddit") or "page32" in category or "magic_square" in category:
        return ["usefulfiles_important_links_local"]
    if "brown" in category or "bibliographic" in category:
        return ["usefulfiles_ideas_local"]
    return ["stage5aj-usefulfiles-source-manifest-extension"]


def _select_next(readiness: dict[str, Any], missing: dict[str, Any]) -> str:
    if readiness.get("bundles_ready_for_private_deep_research", 0) > 0:
        return "stage5ak_deep_research_source_inventory_and_reliability_prompt"
    if missing.get("still_missing_online_fetch_count", 0) > 0:
        return "stage5ak_targeted_online_fetch_for_new_links"
    return "stage5ak_lp_excel_delimiter_transcript_source_lock"


def _decision_options() -> list[tuple[str, str, str]]:
    return [
        (
            "stage5ak_deep_research_source_inventory_and_reliability_prompt",
            "Stage 5AK - Deep Research source inventory and reliability prompt",
            "UsefulFilesAndIdeas is integrated and private bundle metadata remains ready; Deep Research should consume curated manifests and source cards.",
        ),
        (
            "stage5ak_targeted_online_fetch_for_new_links",
            "Stage 5AK - targeted online fetch for new links",
            "Use only if newly added source links dominate the remaining source gaps.",
        ),
        (
            "stage5ak_source_gap_closure_for_missing_priority_sources",
            "Stage 5AK - source gap closure for missing priority sources",
            "Deferred unless A1/A2 source gaps dominate after UsefulFiles integration.",
        ),
        (
            "stage5ak_lp_excel_delimiter_transcript_source_lock",
            "Stage 5AK - LP Excel delimiter transcript source-lock",
            "Deferred; useful if workbook extraction needs deeper transcript policy work before Deep Research.",
        ),
        (
            "stage5ak_benchmark_planning",
            "Stage 5AK - benchmark planning",
            "Rejected; Stage 5AJ is source curation only.",
        ),
        (
            "stage5ak_unsolved_page_cuda_pilot",
            "Stage 5AK - unsolved-page CUDA pilot",
            "Rejected; unsolved-page CUDA remains blocked.",
        ),
        (
            "future_website_expansion_unnumbered",
            "Future unnumbered website expansion",
            "Deferred; Stage 5AJ prepares metadata only and does not publish website content.",
        ),
    ]
