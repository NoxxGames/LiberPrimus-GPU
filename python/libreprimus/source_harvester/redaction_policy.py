"""Stage 5AJ redaction policy records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json, write_yaml
from .models import STAGE5AJ_ID, STAGE5AJ_OUTPUT_DIR, STAGE5AJ_REDACTION_POLICY_PATH, STAGE5AJ_REPORTS, STAGE5AJ_SOURCE_STAGE_ID


def build_redaction_policy(
    *,
    out: Path = STAGE5AJ_REDACTION_POLICY_PATH,
    results_dir: Path = STAGE5AJ_OUTPUT_DIR,
) -> dict[str, Any]:
    """Write private/public redaction boundaries for future capture."""

    policy = {
        "record_type": "stage5aj_redaction_policy",
        "schema": "schemas/source-harvester/redaction-policy-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "private_extract_no_over_redaction_rules": [
            "Do not redact runes, transliterations, punctuation, separators, cell coordinates, formula text, highlights, counts, hashes, or public URLs.",
            "Do not redact tables, code blocks, citation text, image captions, or source references merely because they are technical.",
            "Do not flatten spreadsheet formatting when formatting is part of the source claim.",
        ],
        "redaction_targets": [
            "private Discord identities",
            "private Discord URLs",
            "credential-like tokens",
            "private local absolute paths in public views",
            "copyrighted raw full-body dumps in public views",
        ],
        "redaction_log_required": True,
        "redaction_log_required_fields": [
            "record_id",
            "source_id",
            "field",
            "redaction_reason",
            "replacement_token",
            "review_required",
        ],
        "public_website_rules": {
            "conservative_metadata_first": True,
            "publication_review_required": True,
            "raw_private_material_allowed": False,
            "generated_extract_allowed_without_review": False,
        },
        "network_fetch_performed": False,
        "website_expansion_performed": False,
        "solve_claim": False,
    }
    write_yaml(out, policy)
    write_json(results_dir / STAGE5AJ_REPORTS["redaction_policy"], policy)
    return policy
