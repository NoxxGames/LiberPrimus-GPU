"""Search and category filters for Source Browser entries."""

from __future__ import annotations

from .entries import SourceBrowserEntry
from .number_facts import entry_matches_fact_filter, normalize_entry_number_facts, zero_fact_review_state

FACT_FILTER_QUERIES = {
    "needs:fact-enrichment": "needs_fact_enrichment",
    "needs enrichment": "needs_fact_enrichment",
    "not-reviewed:number-facts": "not_reviewed_for_number_facts",
    "not reviewed for number facts": "not_reviewed_for_number_facts",
    "rich:number-facts": "has_rich_number_facts",
    "rich number facts": "has_rich_number_facts",
    "canonical-verification:number-facts": "canonical_verification_required",
    "canonical verification required": "canonical_verification_required",
    "quarantined:number-facts": "quarantined_number_facts",
    "quarantined number facts": "quarantined_number_facts",
}


def searchable_text(entry: SourceBrowserEntry) -> str:
    parts = [
        entry.title,
        entry.summary,
        entry.notes or "",
        entry.record_type or "",
        entry.candidate_family_id or "",
        entry.stage_id or "",
        entry.source_record_path,
        " ".join(entry.local_paths),
        " ".join(entry.urls),
        " ".join(entry.warnings),
        " ".join(str(fact) for fact in entry.number_facts),
        zero_fact_review_state(entry) if not entry.number_facts else "",
        " ".join(card.review_state for card in normalize_entry_number_facts(entry)),
        " ".join(card.display_label for card in normalize_entry_number_facts(entry)),
    ]
    return " ".join(parts).lower()


def filter_entries(
    entries: list[SourceBrowserEntry],
    *,
    category: str = "All",
    search: str = "",
    has_images: bool | None = None,
    has_urls: bool | None = None,
    has_warnings: bool | None = None,
) -> list[SourceBrowserEntry]:
    query = search.strip().lower()
    fact_filter = FACT_FILTER_QUERIES.get(query)
    filtered: list[SourceBrowserEntry] = []
    for entry in entries:
        if category != "All" and entry.category != category:
            continue
        if fact_filter and not entry_matches_fact_filter(entry, fact_filter):
            continue
        if query and not fact_filter and query not in searchable_text(entry):
            continue
        if has_images is not None and bool(entry.image_paths) != has_images:
            continue
        if has_urls is not None and bool(entry.urls) != has_urls:
            continue
        if has_warnings is not None and bool(entry.warnings) != has_warnings:
            continue
        filtered.append(entry)
    return filtered
