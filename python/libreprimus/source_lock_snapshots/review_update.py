"""Stage 4J review-status integration helpers for Stage 4K."""

from __future__ import annotations


def source_lock_update_record(snapshot_record: dict) -> dict:
    """Return a lightweight source-lock status update derived from a snapshot record."""

    return {
        "source_id": snapshot_record.get("source_candidate_id"),
        "snapshot_record_id": snapshot_record.get("snapshot_record_id"),
        "source_lock_status": snapshot_record.get("lock_status"),
        "review_update_policy": "separate_stage4k_summary_record",
        "stage4j_records_rewritten": False,
    }
