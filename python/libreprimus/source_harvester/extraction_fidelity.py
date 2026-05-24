"""Stage 5AJ extraction-fidelity policy records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json, write_yaml
from .models import STAGE5AJ_FIDELITY_POLICY_PATH, STAGE5AJ_ID, STAGE5AJ_OUTPUT_DIR, STAGE5AJ_SOURCE_STAGE_ID


def build_extraction_fidelity_policy(
    *,
    out: Path = STAGE5AJ_FIDELITY_POLICY_PATH,
    results_dir: Path = STAGE5AJ_OUTPUT_DIR,
) -> dict[str, Any]:
    """Write the Stage 5AJ policy for preserving technical extraction fidelity."""

    policy = {
        "record_type": "stage5aj_extraction_fidelity_policy",
        "schema": "schemas/source-harvester/extraction-fidelity-policy-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "raw_snapshot_view": {
            "stored_in_ignored_local_paths": True,
            "committed": False,
            "redacted": False,
            "purpose": "hashing, provenance, and repeat deterministic extraction",
        },
        "private_deep_research_extract_view": {
            "preserve_runes": True,
            "preserve_numbers": True,
            "preserve_hashes": True,
            "preserve_urls_when_public": True,
            "preserve_tables": True,
            "preserve_code_blocks": True,
            "preserve_cell_coordinates": True,
            "preserve_highlight_colors": True,
            "minimal_redaction_only": True,
            "redaction_log_required": True,
        },
        "public_website_ingest_view": {
            "metadata_first": True,
            "publication_review_required": True,
            "raw_full_body_dumps_allowed_by_default": False,
            "private_discord_identity_allowed": False,
            "private_urls_allowed": False,
        },
        "xlsx_profile": {
            "preserve_sheet_order": True,
            "preserve_formulas": True,
            "preserve_comments": True,
            "preserve_hyperlinks": True,
            "preserve_fill_colors": True,
            "preserve_images_as_inventory_only": True,
            "full_cell_metadata_committed": False,
        },
        "network_fetch_performed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "solve_claim": False,
    }
    write_yaml(out, policy)
    write_json(results_dir / "extraction_fidelity_policy_report.json", policy)
    return policy
