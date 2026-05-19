"""Classify cicada-solvers/iddqd tree paths into source-lock categories."""

from __future__ import annotations

from collections import Counter
from pathlib import PurePosixPath
from typing import Any

from libreprimus.source_delta_audit.models import SELECTED_CATEGORY_ORDER, SOURCE_ID

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg"}
FONT_EXTENSIONS = {".ttf", ".otf", ".woff", ".woff2"}
ARCHIVE_EXTENSIONS = {".zip", ".tar", ".gz", ".iso", ".7z", ".rar"}


def classify_path(path: str) -> str:
    """Classify one repository path."""

    normalized = path.replace("\\", "/")
    lower = normalized.lower()
    suffix = PurePosixPath(lower).suffix
    if lower.startswith("liber-primus__images--full/"):
        return "lp_full_image"
    if lower.startswith("liber-primus__images--unsolved/"):
        return "lp_unsolved_image"
    if lower.startswith("lp_outguessed/"):
        return "lp_outguessed"
    if lower.startswith("2012/"):
        if suffix in AUDIO_EXTENSIONS:
            return "audio_fixture_candidate"
        if suffix in IMAGE_EXTENSIONS:
            return "image_fixture_candidate"
        return "historical_2012"
    if lower.startswith("2013/"):
        if suffix in AUDIO_EXTENSIONS or "761.mp3" in lower:
            return "audio_fixture_candidate"
        if suffix in IMAGE_EXTENSIONS:
            return "image_fixture_candidate"
        return "historical_2013"
    if lower.startswith("2014/"):
        if suffix in AUDIO_EXTENSIONS:
            return "audio_fixture_candidate"
        return "historical_2014"
    if lower.startswith("2016/"):
        if suffix in IMAGE_EXTENSIONS:
            return "image_fixture_candidate"
        return "historical_2016"
    if lower.startswith("byte-strings/") or "byte-string" in lower:
        return "byte_string"
    if "transcription" in lower:
        return "transcription"
    if "translation" in lower:
        return "translation"
    if "/key" in lower or "__key" in lower or lower.endswith("key"):
        return "key"
    if suffix in FONT_EXTENSIONS or "/ttf" in lower or lower.startswith("ttf"):
        return "font_metadata_only"
    if suffix in ARCHIVE_EXTENSIONS:
        return "tooling"
    return "unknown"


def category_counts(paths: list[str]) -> dict[str, int]:
    """Return sorted category counts."""

    counter = Counter(classify_path(path) for path in paths)
    return dict(sorted(counter.items()))


def selected_path_candidates(paths: list[str]) -> list[dict[str, Any]]:
    """Create one or more selected metadata-only path candidates per high-value category."""

    records: list[dict[str, Any]] = []
    by_category: dict[str, list[str]] = {}
    for path in paths:
        by_category.setdefault(classify_path(path), []).append(path)
    for category in SELECTED_CATEGORY_ORDER:
        category_paths = sorted(by_category.get(category, []))
        if not category_paths:
            continue
        sample_paths = category_paths[:5]
        duplicate_of = "stage4b-cicada-solvers-iddqd-lp-outguessed" if category == "lp_outguessed" else None
        records.append(
            {
                "record_type": "source_path_candidate_record",
                "candidate_id": f"stage4e-iddqd-{category}",
                "source_id": SOURCE_ID,
                "path": sample_paths[0],
                "path_count": len(category_paths),
                "sample_paths": sample_paths,
                "artifact_type": category,
                "source_class": _source_class(category),
                "recommended_action": _recommended_action(category),
                "duplicate_of": duplicate_of,
                "raw_file_committed": False,
                "binary_committed": False,
                "font_committed": False,
                "trusted_as_canonical": False,
                "solve_claim": False,
                "notes": _notes(category),
            }
        )
    return records


def _source_class(category: str) -> str:
    if category in {"tooling", "font_metadata_only"}:
        return "reference_only_tooling"
    if category in {"lp_full_image", "lp_unsolved_image", "lp_outguessed", "transcription", "translation", "key"}:
        return "strong_community_technical"
    return "secondary_archive"


def _recommended_action(category: str) -> str:
    if category == "font_metadata_only":
        return "record metadata only"
    if category in {"lp_full_image", "lp_unsolved_image"}:
        return "queue source-variant comparison"
    if category in {"lp_outguessed", "audio_fixture_candidate", "image_fixture_candidate"}:
        return "queue fixture source-lock"
    return "source-lock metadata"


def _notes(category: str) -> str:
    if category == "font_metadata_only":
        return "Font binaries must not be committed or shared; metadata only."
    if category.startswith("lp_"):
        return "Candidate for future source-lock/delta comparison; raw image or payload files remain ignored."
    if category == "audio_fixture_candidate":
        return "Candidate for future audio fixture source-locking; no audio analysis in Stage 4E."
    return "Selected path category recorded for future bounded source-lock work."
