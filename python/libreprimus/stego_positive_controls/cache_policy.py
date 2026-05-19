"""Fixture cache policy and ignored-cache metadata for Stage 4N."""

from __future__ import annotations

import hashlib
import mimetypes
from pathlib import Path
from typing import Any

from libreprimus.stego_positive_controls.models import COMMON_FALSE_FLAGS


def build_cache_record(record: dict[str, Any], *, category: str, cache_dir: Path, source_kind: str) -> dict[str, Any]:
    """Build a cache record without fetching or committing fixture bytes."""

    source_record_id = str(record.get("fixture_id") or record.get("artifact_id") or "unknown")
    cache_path = cache_dir / _safe_cache_name(record, source_record_id)
    is_reference = "reference_only" in category
    is_synthetic = category.startswith("synthetic_")
    if cache_path.is_file():
        local_availability = "present_ignored_cache"
        cache_policy = "cached_ignored"
        sha256 = _sha256(cache_path)
        file_size = cache_path.stat().st_size
        media_type = mimetypes.guess_type(cache_path.name)[0]
    elif is_synthetic:
        local_availability = "generated_test_only"
        cache_policy = "synthetic_generated_for_tests"
        sha256 = None
        file_size = None
        media_type = "application/octet-stream"
    elif is_reference:
        local_availability = "not_applicable"
        cache_policy = "reference_only"
        sha256 = None
        file_size = None
        media_type = None
    else:
        local_availability = str(record.get("local_availability") or record.get("local_path_status") or "source_only")
        if local_availability in {"missing", "absent"}:
            local_availability = "absent"
        cache_policy = "cache_candidate" if local_availability in {"source_only", "absent"} else "deferred"
        sha256 = None
        file_size = None
        media_type = mimetypes.guess_type(str(record.get("source_path") or record.get("file_name") or ""))[0]
    return {
        "record_type": "stego_fixture_cache_record",
        "cache_record_id": f"stage4n-cache-{source_record_id}",
        "source_record_id": source_record_id,
        "source_kind": source_kind,
        "fixture_category": category,
        "cache_policy": cache_policy,
        "local_availability": local_availability,
        "ignored_cache_path": str(cache_path.as_posix()) if not is_reference else None,
        "file_size_bytes": file_size,
        "sha256": sha256,
        "media_type": media_type,
        "notes": "No fixture bytes are committed; cache path is ignored and optional.",
        **COMMON_FALSE_FLAGS,
    }


def _safe_cache_name(record: dict[str, Any], source_record_id: str) -> str:
    name = str(record.get("file_name") or Path(str(record.get("source_path") or "")).name or source_record_id)
    if not name or name in {".", "/"}:
        name = source_record_id
    return "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in name)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
