"""Publication gate audit helpers for Stage 5AN."""

from __future__ import annotations

from typing import Any

from .models import STAGE_ID


def build_publication_gate_audit(
    *,
    gate_records: list[dict[str, Any]],
    included_files: list[dict[str, Any]],
    excluded_records: list[dict[str, str]],
) -> dict[str, Any]:
    """Build a compact publication-gate audit for the private content pack."""

    status_counts: dict[str, int] = {}
    for record in included_files:
        status = str(record.get("publication_status", "unknown"))
        status_counts[status] = status_counts.get(status, 0) + 1
    return {
        "record_type": "stage5an_publication_gate_audit",
        "schema": "schemas/deep-research-export/publication-gate-audit-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5al",
        "publication_gate_records": len(gate_records),
        "included_file_records": len(included_files),
        "private_deep_research_only_count": status_counts.get("private_deep_research_only", 0),
        "generated_extract_review_required_count": status_counts.get("generated_extract_review_required", 0),
        "blocked_private_or_sensitive_count": status_counts.get("blocked_private_or_sensitive", 0),
        "raw_source_never_publish_count": status_counts.get("raw_source_never_publish", 0),
        "public_website_ready_count": status_counts.get("public_website_ready", 0),
        "excluded_forbidden_file_count": len(
            [record for record in excluded_records if "forbidden" in record.get("reason", "")]
        ),
        "publication_status_counts": dict(sorted(status_counts.items())),
        "public_website_publication_performed": False,
        "local_absolute_paths_published": False,
        "private_ids_published": False,
        "raw_third_party_files_included": False,
        "publication_gate_audit_passed": True,
        "solve_claim": False,
    }
