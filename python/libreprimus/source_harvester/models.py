"""Constants and shared Stage 5AF source-harvester model helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5af"
SOURCE_STAGE_ID = "stage-5ae"

OUTPUT_DIR = Path("experiments/results/source-harvester/stage5af")
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
