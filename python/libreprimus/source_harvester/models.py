"""Constants and shared Stage 5AF source-harvester model helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5af"
SOURCE_STAGE_ID = "stage-5ae"
STAGE5AG_ID = "stage-5ag"
STAGE5AG_SOURCE_STAGE_ID = "stage-5af"
STAGE5AI_ID = "stage-5ai"
STAGE5AI_SOURCE_STAGE_ID = "stage-5ah"
STAGE5AI_LOCAL_INVENTORY_STAGE_ID = "stage-5ag"
STAGE5AJ_ID = "stage-5aj"
STAGE5AJ_SOURCE_STAGE_ID = "stage-5ai"
STAGE5AK_ID = "stage-5ak"
STAGE5AK_SOURCE_STAGE_ID = "stage-5aj"

OUTPUT_DIR = Path("experiments/results/source-harvester/stage5af")
STAGE5AG_OUTPUT_DIR = Path("experiments/results/source-harvester-local/stage5ag")
SOURCE_MANIFEST_PATH = Path("data/source-harvester/stage5af-cicada-source-manifest.yaml")
COLLECTION_PRIORITIES_PATH = Path("data/source-harvester/stage5af-source-collection-priorities.yaml")
CLUE_TARGET_CATEGORIES_PATH = Path("data/source-harvester/stage5af-clue-target-categories.yaml")
RESEARCH_BUNDLE_PLAN_PATH = Path("data/source-harvester/stage5af-research-bundle-plan.yaml")
TOOL_POLICY_PATH = Path("data/source-harvester/stage5af-harvest-tool-policy.yaml")
DRY_RUN_SUMMARY_PATH = Path("data/source-harvester/stage5af-harvest-dry-run-summary.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/source-harvester/stage5af-source-harvester-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/source-harvester/stage5af-source-harvester-summary.yaml")

HARVEST_PLAN_REPORT = "harvest_plan.json"
MANIFEST_VALIDATION_REPORT = "source_manifest_validation.json"
DRY_RUN_SUMMARY_REPORT = "dry_run_summary.json"
RESEARCH_BUNDLE_PLAN_REPORT = "research_bundle_plan.json"
FAILURES_REPORT = "failures.jsonl"
SUMMARY_REPORT = "summary.json"
WARNINGS_REPORT = "warnings.jsonl"
FULL_FILE_INVENTORY_REPORT = "full_file_inventory.jsonl"
FULL_FILE_INVENTORY_CSV_REPORT = "full_file_inventory.csv"
FULL_HASH_INVENTORY_REPORT = "full_hash_inventory.jsonl"
FULL_ARCHIVE_INVENTORY_REPORT = "full_archive_inventory.jsonl"
SOURCE_MANIFEST_LINKAGE_REPORT = "source_manifest_linkage.json"
DUPLICATE_HASHES_REPORT = "duplicate_hashes.json"
MISSING_SOURCES_REPORT = "missing_sources.json"
UNCLASSIFIED_LOCAL_SOURCES_REPORT = "unclassified_local_sources.json"
RESEARCH_BUNDLE_READINESS_REPORT = "research_bundle_readiness.json"

STAGE5AG_ROOT_INVENTORY_PATH = Path("data/source-harvester/stage5ag-local-source-root-inventory.yaml")
STAGE5AG_FILE_SUMMARY_PATH = Path("data/source-harvester/stage5ag-local-source-file-inventory-summary.yaml")
STAGE5AG_ARCHIVE_SUMMARY_PATH = Path("data/source-harvester/stage5ag-local-archive-inventory-summary.yaml")
STAGE5AG_HASH_SUMMARY_PATH = Path("data/source-harvester/stage5ag-local-source-hash-inventory-summary.yaml")
STAGE5AG_LOCAL_LINKAGE_PATH = Path("data/source-harvester/stage5ag-manifest-local-linkage.yaml")
STAGE5AG_MANIFEST_EXTENSION_PATH = Path("data/source-harvester/stage5ag-local-source-manifest-extension.yaml")
STAGE5AG_CANDIDATE_SUMMARY_PATH = Path("data/source-harvester/stage5ag-source-lock-candidate-summary.yaml")
STAGE5AG_GAP_REPORT_PATH = Path("data/source-harvester/stage5ag-local-source-gap-report.yaml")
STAGE5AG_BUNDLE_READINESS_PATH = Path("data/source-harvester/stage5ag-research-bundle-readiness.yaml")
STAGE5AG_GUARDRAIL_PATH = Path("data/source-harvester/stage5ag-local-source-guardrail.yaml")
STAGE5AG_NEXT_STAGE_DECISION_PATH = Path("data/source-harvester/stage5ag-source-harvester-next-stage-decision.yaml")
STAGE5AG_SUMMARY_PATH = Path("data/source-harvester/stage5ag-source-harvester-summary.yaml")

STAGE5AI_BUNDLE_ROOT = Path("research-inputs/stage5ai")
STAGE5AI_OUTPUT_DIR = Path("experiments/results/research-bundles/stage5ai")
STAGE5AI_POLICY_PATH = Path("data/source-harvester/stage5ai-curated-bundle-extraction-policy.yaml")
STAGE5AI_SOURCE_CARD_SUMMARY_PATH = Path("data/source-harvester/stage5ai-curated-source-card-summary.yaml")
STAGE5AI_CONTENT_INDEX_SUMMARY_PATH = Path("data/source-harvester/stage5ai-curated-content-index-summary.yaml")
STAGE5AI_WEBSITE_INGEST_FORMAT_PATH = Path("data/source-harvester/stage5ai-website-ingest-format.yaml")
STAGE5AI_DEEP_RESEARCH_PACK_FORMAT_PATH = Path("data/source-harvester/stage5ai-deep-research-pack-format.yaml")
STAGE5AI_BUNDLE_GENERATION_SUMMARY_PATH = Path("data/source-harvester/stage5ai-bundle-generation-summary.yaml")
STAGE5AI_CLASSIFICATION_PATH = Path("data/source-harvester/stage5ai-unclassified-source-classification.yaml")
STAGE5AI_MISSING_SOURCE_PLAN_PATH = Path("data/source-harvester/stage5ai-missing-source-plan.yaml")
STAGE5AI_READINESS_PATH = Path("data/source-harvester/stage5ai-research-bundle-readiness.yaml")
STAGE5AI_GUARDRAIL_PATH = Path("data/source-harvester/stage5ai-curated-extraction-guardrail.yaml")
STAGE5AI_NEXT_STAGE_DECISION_PATH = Path("data/source-harvester/stage5ai-next-stage-decision.yaml")
STAGE5AI_SUMMARY_PATH = Path("data/source-harvester/stage5ai-curated-research-bundle-summary.yaml")

STAGE5AJ_SOURCE_ROOT = Path("third_party/UsefulFilesAndIdeas")
STAGE5AJ_BUNDLE_ROOT = Path("research-inputs/stage5aj")
STAGE5AJ_RESEARCH_BUNDLE_OUTPUT_DIR = Path("experiments/results/research-bundles/stage5aj")
STAGE5AJ_OUTPUT_DIR = Path("experiments/results/source-harvester-usefulfiles/stage5aj")
STAGE5AJ_INVENTORY_PATH = Path("data/source-harvester/stage5aj-usefulfiles-local-inventory.yaml")
STAGE5AJ_MANIFEST_EXTENSION_PATH = Path("data/source-harvester/stage5aj-usefulfiles-source-manifest-extension.yaml")
STAGE5AJ_SOURCE_CARD_SUMMARY_PATH = Path("data/source-harvester/stage5aj-usefulfiles-source-card-summary.yaml")
STAGE5AJ_CONTENT_INDEX_SUMMARY_PATH = Path("data/source-harvester/stage5aj-usefulfiles-content-index-summary.yaml")
STAGE5AJ_XLSX_SUMMARY_PATH = Path("data/source-harvester/stage5aj-xlsx-extraction-summary.yaml")
STAGE5AJ_IMPORTANT_LINKS_PATH = Path("data/source-harvester/stage5aj-important-links-source-index.yaml")
STAGE5AJ_NEW_CLUE_CATEGORIES_PATH = Path("data/source-harvester/stage5aj-new-clue-categories.yaml")
STAGE5AJ_FIDELITY_POLICY_PATH = Path("data/source-harvester/stage5aj-extraction-fidelity-policy.yaml")
STAGE5AJ_REDACTION_POLICY_PATH = Path("data/source-harvester/stage5aj-redaction-policy.yaml")
STAGE5AJ_SCRAPER_POLICY_PATH = Path("data/source-harvester/stage5aj-scraper-capture-policy.yaml")
STAGE5AJ_WEBSITE_UPDATE_PATH = Path("data/source-harvester/stage5aj-website-ingest-update-summary.yaml")
STAGE5AJ_DEEP_RESEARCH_UPDATE_PATH = Path("data/source-harvester/stage5aj-deep-research-pack-update-summary.yaml")
STAGE5AJ_READINESS_PATH = Path("data/source-harvester/stage5aj-research-bundle-readiness.yaml")
STAGE5AJ_MISSING_SOURCE_PLAN_PATH = Path("data/source-harvester/stage5aj-missing-source-plan-update.yaml")
STAGE5AJ_GUARDRAIL_PATH = Path("data/source-harvester/stage5aj-guardrail.yaml")
STAGE5AJ_NEXT_STAGE_DECISION_PATH = Path("data/source-harvester/stage5aj-next-stage-decision.yaml")
STAGE5AJ_SUMMARY_PATH = Path("data/source-harvester/stage5aj-summary.yaml")

STAGE5AJ_REPORTS = {
    "inventory": "usefulfiles_inventory.json",
    "xlsx_index": "xlsx_workbook_extract_index.json",
    "xlsx_cells": "xlsx_cell_metadata_index.jsonl",
    "important_links": "important_links_url_index.json",
    "manifest_preview": "source_manifest_extension_preview.yaml",
    "redaction_policy": "redaction_policy_report.json",
    "scraper_policy": "scraper_capture_policy_report.json",
    "deep_research_update": "deep_research_pack_update_report.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

STAGE5AK_SOURCE_ROOT = Path("third_party/UsefulFilesAndIdeas/community-facts")
STAGE5AK_BUNDLE_ROOT = Path("research-inputs/stage5ak")
STAGE5AK_RESEARCH_BUNDLE_OUTPUT_DIR = Path("experiments/results/research-bundles/stage5ak")
STAGE5AK_OUTPUT_DIR = Path("experiments/results/source-harvester-community-facts/stage5ak")
STAGE5AK_INVENTORY_PATH = Path("data/source-harvester/stage5ak-community-facts-local-inventory.yaml")
STAGE5AK_SOURCE_CARD_SUMMARY_PATH = Path("data/source-harvester/stage5ak-community-facts-source-card-summary.yaml")
STAGE5AK_CONTENT_INDEX_SUMMARY_PATH = Path("data/source-harvester/stage5ak-community-facts-content-index-summary.yaml")
STAGE5AK_ATTACHMENT_INDEX_PATH = Path("data/source-harvester/stage5ak-community-facts-attachment-index.yaml")
STAGE5AK_CLUE_CATEGORIES_PATH = Path("data/source-harvester/stage5ak-community-facts-clue-categories.yaml")
STAGE5AK_CLAIM_POLICY_PATH = Path("data/source-harvester/stage5ak-community-claim-policy.yaml")
STAGE5AK_CLAIM_RECORDS_PATH = Path("data/source-harvester/stage5ak-community-facts-claim-records.yaml")
STAGE5AK_CORRECTION_LOG_PATH = Path("data/source-harvester/stage5ak-community-facts-correction-log.yaml")
STAGE5AK_ARITHMETIC_PREFLIGHT_PATH = Path("data/source-harvester/stage5ak-community-facts-arithmetic-preflight.yaml")
STAGE5AK_WEBSITE_UPDATE_PATH = Path("data/source-harvester/stage5ak-website-ingest-update-summary.yaml")
STAGE5AK_DEEP_RESEARCH_UPDATE_PATH = Path("data/source-harvester/stage5ak-deep-research-pack-update-summary.yaml")
STAGE5AK_READINESS_PATH = Path("data/source-harvester/stage5ak-research-bundle-readiness.yaml")
STAGE5AK_MISSING_SOURCE_PLAN_PATH = Path("data/source-harvester/stage5ak-missing-source-plan-update.yaml")
STAGE5AK_GUARDRAIL_PATH = Path("data/source-harvester/stage5ak-guardrail.yaml")
STAGE5AK_NEXT_STAGE_DECISION_PATH = Path("data/source-harvester/stage5ak-next-stage-decision.yaml")
STAGE5AK_SUMMARY_PATH = Path("data/source-harvester/stage5ak-summary.yaml")

STAGE5AK_REPORTS = {
    "inventory": "community_facts_inventory.json",
    "message_index": "community_message_index.json",
    "attachment_index": "community_attachment_index.json",
    "claim_records": "community_claim_records.jsonl",
    "correction_log": "community_correction_log.jsonl",
    "arithmetic_preflight": "arithmetic_preflight_report.json",
    "deep_research_update": "deep_research_pack_update_report.json",
    "website_update": "website_ingest_update_report.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

STAGE5AI_REPORTS = {
    "bundle_generation": "bundle_generation_report.json",
    "source_cards": "source_card_index.jsonl",
    "content_index": "content_extract_index.jsonl",
    "website_ingest": "website_ingest_index.json",
    "deep_research_pack": "deep_research_pack_index.json",
    "missing_sources": "missing_sources.json",
    "warnings": "warnings.jsonl",
    "summary": "summary.json",
}

REQUIRED_SOURCE_IDS = {
    "liber_primus_dropbox_files",
    "cicada_solvers_iddqd",
    "complete_cicada3301_archive",
    "pastebin_vgmk330j_lp_runes_prime_values",
    "solved_page_google_sheet",
    "solved_pages_colab_notebook",
    "chapterized_rune_map_google_doc",
    "fandom_main_wiki",
    "fandom_possible_hints_never_used",
    "fandom_second_chance_2012",
    "fandom_post_2014_liber_primus",
    "fandom_liber_primus_ideas",
    "fandom_solved_pages_methods",
    "fandom_liber_primus_solved_pages",
    "fandom_liber_primus_unsolved_pages",
    "cicada_boards_forum",
    "spiderpuck_pastebin_profile",
    "tweqx_dwh_hashkit",
    "tweqx_3301_hash_alarm",
    "gp_prime_view",
    "joutguess_rebirth",
    "isitcicada_pgp_checker",
    "cicada_solvers_isitcicada_repo",
    "taiiwo_cicada",
    "mortlach_rune_decrypter_prime",
    "cicada_solvers_github_org",
    "gematria_web_tools",
    "rune_frequency_shiny_app",
    "noxpopuli_youtube_channel",
    "cicada_documentary_youtube",
    "khan_cryptography",
    "gamedetectives_academy",
    "user_uploaded_2012_archive",
    "user_uploaded_2013_archive",
    "user_uploaded_2014_archive",
    "user_uploaded_assets_archive",
    "user_uploaded_extra_wiki_pages",
}

REQUIRED_BUNDLE_IDS = {
    "01-signed-messages-and-authenticity",
    "02-liber-primus-images-and-transcriptions",
    "03-page-49-51-token-block",
    "04-cuneiform-base60-base59",
    "05-red-markers-and-visual-numerics",
    "06-outguess-stego-hidden-formatting",
    "07-boundary-mobius-repeated-fragments",
    "08-tools-gpprime-dwh-gematria",
    "09-community-hypotheses",
    "10-known-negative-retired-ideas",
}

PRIORITIES = {"A1", "A2", "B", "C", "deferred"}
SOURCE_TYPES = {
    "github_repo",
    "github_org",
    "dropbox_folder",
    "google_sheet",
    "google_doc",
    "google_colab",
    "pastebin",
    "fandom_page",
    "static_webpage",
    "forum_index",
    "forum_thread",
    "youtube_video",
    "youtube_channel",
    "browser_tool",
    "shiny_app",
    "image_file",
    "archive_zip",
    "local_user_upload",
    "manual_export_required",
}
SOURCE_TIERS = {
    "tier0_original_signed_or_verified",
    "tier1_committed_repo_record",
    "tier2_archived_community_page_with_references",
    "tier3_reproducible_community_data",
    "tier4_social_claim_or_screenshot",
    "tier5_modified_image_or_speculative_claim",
    "unknown",
}

MANUAL_SOURCE_TYPES = {
    "dropbox_folder",
    "google_sheet",
    "google_doc",
    "google_colab",
    "forum_index",
    "local_user_upload",
    "manual_export_required",
}

DOWNLOAD_CAPTURE_MODES = {
    "download_zip",
    "git_clone_or_zip",
    "xlsx_export",
    "ipynb_export",
    "pdf_export",
    "docx_export",
    "thumbnail",
}

COMMON_FALSE_FLAGS: dict[str, Any] = {
    "network_fetch_performed": False,
    "live_web_scrape_performed": False,
    "raw_downloads_committed": False,
    "raw_archives_processed": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "full_p56_cuda_executed": False,
    "unsolved_page_cuda_used": False,
    "gpu_benchmark_performed": False,
    "benchmark_execution_allowed": False,
    "scored_experiment_executed": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "method_status_upgraded": False,
    "solve_claim": False,
}

STAGE5AG_FALSE_FLAGS: dict[str, Any] = {
    "network_fetch_performed": False,
    "live_web_scrape_performed": False,
    "online_repo_clone_performed": False,
    "google_drive_storage_used": False,
    "raw_downloads_committed": False,
    "raw_archives_committed": False,
    "raw_images_committed": False,
    "raw_html_committed": False,
    "raw_pdf_docx_committed": False,
    "raw_audio_video_committed": False,
    "raw_data_committed": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "third_party_raw_staged": False,
    "third_party_raw_tracked_new": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "full_p56_cuda_executed": False,
    "unsolved_page_cuda_used": False,
    "gpu_benchmark_performed": False,
    "benchmark_execution_allowed": False,
    "scored_experiment_executed": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "method_status_upgraded": False,
    "solve_claim": False,
}

STAGE5AI_FALSE_FLAGS: dict[str, Any] = {
    "network_fetch_performed": False,
    "live_web_scrape_performed": False,
    "online_repo_clone_performed": False,
    "google_drive_storage_used": False,
    "raw_downloads_committed": False,
    "raw_archives_committed": False,
    "raw_images_committed": False,
    "raw_html_committed": False,
    "raw_pdf_docx_committed": False,
    "raw_audio_video_committed": False,
    "raw_data_committed": False,
    "generated_bundle_bodies_committed": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "third_party_raw_staged": False,
    "third_party_raw_tracked_new": False,
    "ocr_performed": False,
    "ai_ml_interpretation_performed": False,
    "stego_tool_execution_performed": False,
    "image_forensics_performed": False,
    "audio_analysis_performed": False,
    "hypothesis_generation_performed": False,
    "hypothesis_execution_performed": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "full_p56_cuda_executed": False,
    "unsolved_page_cuda_used": False,
    "gpu_benchmark_performed": False,
    "benchmark_execution_allowed": False,
    "scored_experiment_executed": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "method_status_upgraded": False,
    "website_expansion_performed": False,
    "solve_claim": False,
}

STAGE5AJ_FALSE_FLAGS: dict[str, Any] = {
    "network_fetch_performed": False,
    "live_web_scrape_performed": False,
    "online_repo_clone_performed": False,
    "google_drive_storage_used": False,
    "raw_downloads_committed": False,
    "raw_archives_committed": False,
    "raw_images_committed": False,
    "raw_html_committed": False,
    "raw_pdf_docx_committed": False,
    "raw_xlsx_committed": False,
    "raw_audio_video_committed": False,
    "raw_data_committed": False,
    "generated_bundle_bodies_committed": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "third_party_raw_staged": False,
    "third_party_raw_tracked_new": False,
    "ocr_performed": False,
    "ai_ml_interpretation_performed": False,
    "stego_tool_execution_performed": False,
    "image_forensics_performed": False,
    "audio_analysis_performed": False,
    "hypothesis_generation_performed": False,
    "hypothesis_execution_performed": False,
    "deep_research_performed": False,
    "website_expansion_performed": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "benchmark_performed": False,
    "scored_experiments_executed": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "method_status_upgraded": False,
    "solve_claim": False,
}

STAGE5AK_FALSE_FLAGS: dict[str, Any] = {
    "network_fetch_performed": False,
    "live_web_scrape_performed": False,
    "online_repo_clone_performed": False,
    "google_drive_storage_used": False,
    "raw_downloads_committed": False,
    "raw_archives_committed": False,
    "raw_images_committed": False,
    "raw_html_committed": False,
    "raw_pdf_docx_committed": False,
    "raw_text_committed": False,
    "raw_audio_video_committed": False,
    "raw_data_committed": False,
    "generated_bundle_bodies_committed": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "third_party_raw_staged": False,
    "third_party_raw_tracked_new": False,
    "ocr_performed": False,
    "ai_ml_interpretation_performed": False,
    "stego_tool_execution_performed": False,
    "image_forensics_performed": False,
    "audio_analysis_performed": False,
    "hypothesis_generation_performed": False,
    "hypothesis_execution_performed": False,
    "deep_research_performed": False,
    "website_expansion_performed": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "benchmark_performed": False,
    "scored_experiments_executed": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "method_status_upgraded": False,
    "solve_claim": False,
}


def common_record_flags() -> dict[str, Any]:
    """Return common guardrail fields for Stage 5AF records."""

    return {
        "stage_id": STAGE_ID,
        "source_stage_id": SOURCE_STAGE_ID,
        "no_solve_claim": True,
        "no_gpu_ci_safe": True,
        "ci_network_required": False,
        "new_cuda_kernels_added": 0,
        **COMMON_FALSE_FLAGS,
    }


def stage5ag_common_record_flags() -> dict[str, Any]:
    """Return common guardrail fields for Stage 5AG records."""

    return {
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "no_solve_claim": True,
        "no_gpu_ci_safe": True,
        "ci_network_required": False,
        "new_cuda_kernels_added": 0,
        **STAGE5AG_FALSE_FLAGS,
    }


def stage5ai_common_record_flags() -> dict[str, Any]:
    """Return common guardrail fields for Stage 5AI records."""

    return {
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "no_solve_claim": True,
        "no_gpu_ci_safe": True,
        "ci_network_required": False,
        "new_cuda_kernels_added": 0,
        **STAGE5AI_FALSE_FLAGS,
    }
