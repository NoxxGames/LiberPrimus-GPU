"""Search and category filters for Source Browser entries."""

from __future__ import annotations

from .entries import SourceBrowserEntry


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
    filtered: list[SourceBrowserEntry] = []
    for entry in entries:
        if category != "All" and entry.category != category:
            continue
        if query and query not in searchable_text(entry):
            continue
        if has_images is not None and bool(entry.image_paths) != has_images:
            continue
        if has_urls is not None and bool(entry.urls) != has_urls:
            continue
        if has_warnings is not None and bool(entry.warnings) != has_warnings:
            continue
        filtered.append(entry)
    return filtered
