"""Copyright and commit-snapshot policy helpers for Stage 4K."""

from __future__ import annotations

from libreprimus.source_lock_snapshots.snapshot_policy import artifact_kind


def copyright_note(source_url: str, source_class: str) -> str:
    """Return a conservative copyright note for a source."""

    if source_class.startswith("github_"):
        return "Public GitHub source metadata locked; repository licence must be checked before copying content."
    if source_class == "uncovering_cicada_page":
        return "Public wiki page metadata/hash locked; full page HTML is cached locally only and not committed."
    if source_class == "archive_reference":
        return "Archive reference metadata locked; snapshot content is not committed by default."
    return "Public source metadata locked; content copying requires separate licence review."


def committed_snapshot_allowed(source_url: str, snapshot_policy: str, artifact_type: str | None = None) -> tuple[bool, str]:
    """Return whether a committed snapshot is allowed and why."""

    if snapshot_policy != "committed_small_text_snapshot":
        return False, "Stage 4K defaults to metadata/hash locks; no committed snapshot requested."
    if artifact_kind(source_url, artifact_type) != "text":
        return False, "Only safe small text snapshots may be committed."
    return True, "Safe small text snapshot policy explicitly selected."
