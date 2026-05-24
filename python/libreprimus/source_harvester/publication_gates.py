"""Stage 5AL publication-gate records for website-ingest metadata."""

from __future__ import annotations

from typing import Any


PUBLICATION_GATE_STATUSES = (
    "metadata_only_safe",
    "private_deep_research_only",
    "generated_extract_review_required",
    "blocked_private_or_sensitive",
    "raw_source_never_publish",
    "public_website_review_required",
    "external_link_only",
)


def build_publication_gate_records() -> list[dict[str, Any]]:
    """Return deterministic Stage 5AL publication gate policy records."""

    specs = {
        "metadata_only_safe": (
            "Only redacted metadata may be consumed by future website tooling after review.",
            True,
            False,
            False,
        ),
        "private_deep_research_only": (
            "Material may be referenced by private Deep Research exports but not public pages.",
            False,
            True,
            False,
        ),
        "generated_extract_review_required": (
            "Generated extract metadata exists, but generated bodies require explicit review before publication.",
            False,
            True,
            True,
        ),
        "blocked_private_or_sensitive": (
            "Private or sensitive community material is blocked from public website publication.",
            False,
            True,
            True,
        ),
        "raw_source_never_publish": (
            "Raw third-party files, private logs, images, archives, and workbook bodies are never publishable by default.",
            False,
            False,
            True,
        ),
        "public_website_review_required": (
            "The record is metadata-only but still needs a public website review gate before display.",
            False,
            True,
            True,
        ),
        "external_link_only": (
            "Only source URLs or source identifiers may be displayed; no copied body content is allowed.",
            False,
            True,
            False,
        ),
    }
    records = []
    for status in PUBLICATION_GATE_STATUSES:
        description, metadata_may_be_public_after_review, deep_research_allowed, blocks_publication = specs[status]
        records.append(
            {
                "record_type": "stage5al_publication_gate",
                "schema": "schemas/website-ingest/publication-gate-v0.schema.json",
                "stage_id": "stage-5al",
                "status": status,
                "description": description,
                "metadata_may_be_public_after_review": metadata_may_be_public_after_review,
                "private_deep_research_allowed": deep_research_allowed,
                "website_publication_allowed": False,
                "raw_content_publication_allowed": False,
                "generated_extract_publication_allowed": False,
                "blocks_publication_by_default": blocks_publication,
                "private_ids_allowed": False,
                "raw_bodies_allowed": False,
                "solve_claim": False,
            }
        )
    return records
