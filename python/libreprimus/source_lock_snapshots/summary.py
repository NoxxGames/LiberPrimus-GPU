"""Summary helpers for Stage 4K source-lock snapshots."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import yaml


def summarize_source_locks(
    *,
    considered_count: int,
    allowlisted_count: int,
    snapshot_records: list[dict[str, Any]],
    rejected_records: list[dict[str, Any]],
    duplicate_records: list[dict[str, Any]],
    source_lock_updates: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build the committed Stage 4K source-lock summary."""

    status_counts = Counter(str(record.get("lock_status")) for record in snapshot_records)
    retrieval_counts = Counter(str(record.get("retrieval_status")) for record in snapshot_records)
    return {
        "record_type": "source_lock_snapshot_summary",
        "stage": "Stage 4K",
        "summary_id": "stage4k-source-lock-summary",
        "sources_considered": considered_count,
        "sources_allowlisted": allowlisted_count,
        "sources_locked": sum(
            status_counts[status]
            for status in ("source_locked", "metadata_locked", "snapshot_cached_ignored", "commit_address_locked")
        ),
        "sources_fetched": retrieval_counts["fetched"],
        "github_commit_blob_locks": status_counts["commit_address_locked"],
        "metadata_only_records": sum(
            1 for record in snapshot_records if record.get("snapshot_policy") in {"metadata_only", "commit_addressed_reference"}
        ),
        "ignored_local_snapshots": sum(1 for record in snapshot_records if record.get("snapshot_policy") == "ignored_local_snapshot"),
        "committed_small_text_snapshots": sum(1 for record in snapshot_records if record.get("committed_snapshot") is True),
        "rejected_unsafe_noisy_sources": len(rejected_records),
        "duplicate_sources": len(duplicate_records),
        "fetch_failures": retrieval_counts["fetch_failed"],
        "source_lock_status_counts": dict(sorted(status_counts.items())),
        "retrieval_status_counts": dict(sorted(retrieval_counts.items())),
        "source_lock_updates": source_lock_updates,
        "generated_outputs_committed": False,
        "raw_private_data_committed": False,
        "binary_committed": False,
        "image_committed": False,
        "audio_committed": False,
        "font_committed": False,
        "archive_committed": False,
        "solve_claim": False,
        "trusted_as_canonical": False,
        "notes": [
            "Source locks strengthen reproducibility; they do not create solve evidence.",
            "Stage 4J observation decisions are not destructively rewritten.",
        ],
    }


def load_summary(path: Path) -> dict[str, Any]:
    """Load a Stage 4K summary document."""

    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
