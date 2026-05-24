"""Stage 5AJ future scraper capture profiles."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json, write_yaml
from .models import STAGE5AJ_ID, STAGE5AJ_OUTPUT_DIR, STAGE5AJ_REPORTS, STAGE5AJ_SCRAPER_POLICY_PATH, STAGE5AJ_SOURCE_STAGE_ID


def build_scraper_capture_policy(
    *,
    out: Path = STAGE5AJ_SCRAPER_POLICY_PATH,
    results_dir: Path = STAGE5AJ_OUTPUT_DIR,
) -> dict[str, Any]:
    """Write non-executing future capture profiles for public sources."""

    policy = {
        "record_type": "stage5aj_scraper_capture_policy",
        "schema": "schemas/source-harvester/scraper-capture-policy-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "capture_profiles": [
            {
                "source_type": "fandom_page",
                "future_capture_modes": ["html", "markdown", "text", "tables", "images", "links"],
                "preserve": ["headings", "tables", "image_links", "captions", "citations", "numbers", "runes", "punctuation"],
                "rate_limit_required": True,
                "one_hop_default": False,
            },
            {
                "source_type": "reddit_post",
                "future_capture_modes": ["targeted_post_capture", "comments_metadata", "links"],
                "preserve": ["post_title", "permalink", "author_redacted_for_public", "body_text", "public_urls", "numbers", "tables"],
                "subreddit_bulk_scrape_allowed": False,
                "rate_limit_required": True,
            },
            {
                "source_type": "github_repo",
                "future_capture_modes": ["commit_sha", "file_inventory", "hash_inventory", "selected_text_files"],
                "preserve": ["commit_sha", "paths", "file_hashes", "license", "README", "selected_source_text"],
                "whole_repo_commit_allowed": False,
            },
            {
                "source_type": "xlsx_local_export",
                "future_capture_modes": ["workbook_hash", "sheet_inventory", "cell_metadata", "formatting_metadata"],
                "preserve": ["sheet_order", "cell_addresses", "formulas", "comments", "hyperlinks", "fill_colors", "font_styles"],
                "raw_workbook_commit_allowed": False,
            },
        ],
        "live_web_scrape_performed": False,
        "network_fetch_performed": False,
        "online_repo_clone_performed": False,
        "google_drive_storage_used": False,
        "solve_claim": False,
    }
    write_yaml(out, policy)
    write_json(results_dir / STAGE5AJ_REPORTS["scraper_policy"], policy)
    return policy
