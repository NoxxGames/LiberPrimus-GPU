"""Constants for Stage 5AN private Deep Research exports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5an"
SOURCE_STAGE_ID = "stage-5am"
STAGE5AM_COMMIT = "3eb35cc692cdf636b95b91822e9667c230fed7a4"

METADATA_SITE_URL = "http://liberprimus-gpu-data.info/index.html"
PRIVATE_CONTENT_URL = "http://liberprimus-gpu-data.info/private-content/"
PRIVATE_CONTENT_MANIFEST_URL = "http://liberprimus-gpu-data.info/private-content/data/content-pack-manifest.json"

METADATA_SITE_ROOT = Path("website-export/stage5am/research-index")
WEBSITE_INGEST_DIR = Path("data/website-ingest/stage5al")
CONTENT_PACK_ROOT = Path("deep-research-content-packs/stage5an")
HOSTED_CONTENT_ROOT = Path("website-export/stage5an/private-content")
COMBINED_WEBROOT = Path("website-export/stage5an/webserver-root")

DATA_DIR = Path("data/deep-research-export")
POLICY_PATH = DATA_DIR / "stage5an-content-pack-policy.yaml"
INPUTS_PATH = DATA_DIR / "stage5an-content-pack-inputs.yaml"
MANIFEST_SUMMARY_PATH = DATA_DIR / "stage5an-content-pack-manifest-summary.yaml"
HOSTED_SUMMARY_PATH = DATA_DIR / "stage5an-hosted-content-export-summary.yaml"
COMBINED_SUMMARY_PATH = DATA_DIR / "stage5an-combined-webroot-summary.yaml"
FILE_SELECTION_SUMMARY_PATH = DATA_DIR / "stage5an-file-selection-summary.yaml"
PUBLICATION_GATE_AUDIT_PATH = DATA_DIR / "stage5an-publication-gate-audit.yaml"
UPLOAD_INSTRUCTIONS_PATH = DATA_DIR / "stage5an-upload-instructions.yaml"
CONSUMPTION_GUIDE_PATH = DATA_DIR / "stage5an-deep-research-consumption-guide.yaml"
GUARDRAIL_PATH = DATA_DIR / "stage5an-guardrail.yaml"
NEXT_STAGE_DECISION_PATH = DATA_DIR / "stage5an-next-stage-decision.yaml"
SUMMARY_PATH = DATA_DIR / "stage5an-summary.yaml"

DEFAULT_RESEARCH_INPUT_ROOTS = [
    Path("research-inputs/stage5ai"),
    Path("research-inputs/stage5aj"),
    Path("research-inputs/stage5ak"),
    Path("research-inputs/stage5al"),
]
DEFAULT_SAFE_LOCAL_SOURCE_ROOTS = [
    Path("third_party/UsefulFilesAndIdeas"),
    Path("third_party/UsefulFilesAndIdeas/community-facts"),
]

ALLOWED_PRIVATE_EXTENSIONS = {
    ".csv",
    ".html",
    ".json",
    ".jsonl",
    ".md",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}

FORBIDDEN_RAW_EXTENSIONS = {
    ".7z",
    ".avi",
    ".db",
    ".docx",
    ".gif",
    ".jpg",
    ".jpeg",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".rar",
    ".sqlite",
    ".sqlite3",
    ".tar",
    ".webp",
    ".xls",
    ".xlsx",
    ".zip",
}

SAFE_EXTRACT_SOURCE_NAMES = {
    "LP Excel.xlsx",
    "tranlsations_decryptions.xlsx",
    "translations_decryptions.xlsx",
    "important_links.txt",
    "ideas.txt",
    "community-facts-collection.txt",
}

PRIVATE_BANNER = "PRIVATE DEEP RESEARCH CONTENT LIBRARY"
PRIVATE_NOTICE = "Review-gated. Not public evidence. No solve claims. Do not mirror publicly without manual review."
NOINDEX = '<meta name="robots" content="noindex,nofollow,noarchive">'

FALSE_GUARDRAILS: dict[str, Any] = {
    "network_fetch_performed": False,
    "live_web_scrape_performed": False,
    "online_repo_clone_performed": False,
    "google_drive_storage_used": False,
    "raw_data_committed": False,
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

REQUIRED_HOSTED_FILES = [
    "index.html",
    "bundles/index.html",
    "sources/index.html",
    "claims/index.html",
    "files/index.html",
    "deep-research/index.html",
    "data/content-pack-manifest.json",
    "data/source-cards.json",
    "data/content-index.json",
    "data/claim-index.json",
    "data/file-index.json",
    "data/publication-gates.json",
    "assets/site.css",
    "assets/site.js",
    "robots.txt",
    "README.md",
]

REQUIRED_COMBINED_FILES = [
    "index.html",
    "private-content/index.html",
    "private-content/data/content-pack-manifest.json",
    "robots.txt",
    "README.md",
]
