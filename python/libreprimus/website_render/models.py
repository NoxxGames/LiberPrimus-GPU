"""Constants for the Stage 5AM static research website renderer."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5am"
SOURCE_STAGE_ID = "stage-5al"
STAGE5AL_COMMIT = "66d6ba9f7739861bc5f797d0896f32082af92326"

WEBSITE_INGEST_DIR = Path("data/website-ingest/stage5al")
SITE_ROOT = Path("website-export/stage5am/research-index")
WEBSITE_EXPORT_ROOT = Path("website-export")
WEBSITE_EXPORT_STAGE_DIR = Path("website-export/stage5am")
RESULTS_DIR = Path("experiments/results/website-render/stage5am")

DATA_DIR = Path("data/website-render")
RENDER_POLICY_PATH = DATA_DIR / "stage5am-render-policy.yaml"
RENDER_INPUTS_PATH = DATA_DIR / "stage5am-render-inputs.yaml"
OUTPUT_MANIFEST_PATH = DATA_DIR / "stage5am-render-output-manifest.yaml"
SITE_VALIDATION_PATH = DATA_DIR / "stage5am-static-site-validation.yaml"
PRIVACY_AUDIT_PATH = DATA_DIR / "stage5am-privacy-publication-audit.yaml"
UPLOAD_INSTRUCTIONS_PATH = DATA_DIR / "stage5am-upload-instructions.yaml"
GUARDRAIL_PATH = DATA_DIR / "stage5am-guardrail.yaml"
NEXT_STAGE_DECISION_PATH = DATA_DIR / "stage5am-next-stage-decision.yaml"
SUMMARY_PATH = DATA_DIR / "stage5am-summary.yaml"

STAGE5AL_SUMMARY_PATH = Path("data/source-harvester/stage5al-summary.yaml")

REQUIRED_PAGES = [
    "index.html",
    "bundles/index.html",
    "sources/index.html",
    "content/index.html",
    "claims/index.html",
    "publication-gates/index.html",
    "missing-sources/index.html",
    "deep-research/index.html",
    "about/index.html",
]

REQUIRED_DATA_FILES = [
    "data/research-index.json",
    "data/research-bundles.json",
    "data/source-cards.json",
    "data/content-index.json",
    "data/community-claims.json",
    "data/publication-gates.json",
    "data/deep-research-export.json",
    "data/missing-sources.json",
]

REQUIRED_ASSETS = [
    "assets/site.css",
    "assets/site.js",
    "assets/search-index.json",
    "robots.txt",
    "README.md",
]

SAFE_DATASETS = {
    "research-index": "research-index.json",
    "research-bundles": "research-bundles.json",
    "source-cards": "source-cards.json",
    "content-index": "content-index.json",
    "community-claims": "community-claims.json",
    "publication-gates": "publication-gates.json",
    "deep-research-export": "deep-research-export.json",
    "missing-sources": "missing-sources.json",
}

FALSE_GUARDRAILS: dict[str, Any] = {
    "network_fetch_performed": False,
    "live_web_scrape_performed": False,
    "online_repo_clone_performed": False,
    "google_drive_storage_used": False,
    "raw_data_committed": False,
    "raw_text_committed": False,
    "raw_images_committed": False,
    "raw_xlsx_committed": False,
    "raw_archives_committed": False,
    "generated_private_bodies_committed": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "third_party_raw_staged": False,
    "third_party_raw_tracked_new": False,
    "deep_research_performed": False,
    "public_website_publication_performed": False,
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
    "benchmark_performed": False,
    "scored_experiments_executed": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "method_status_upgraded": False,
    "solve_claim": False,
}
