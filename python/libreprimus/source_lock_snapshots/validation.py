"""Validation for Stage 4K source-lock snapshot records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.source_lock_snapshots.loaders import load_yaml_records
from libreprimus.source_lock_snapshots.models import LOCK_STATUSES, SNAPSHOT_POLICIES


def validate_source_lock_snapshot_records(
    *,
    snapshot_records: Path,
    fetch_records: Path,
    copyright_records: Path,
    summary: Path,
) -> tuple[dict[str, int], list[str]]:
    """Validate committed Stage 4K source-lock records."""

    snapshots = load_yaml_records(snapshot_records)
    fetches = load_yaml_records(fetch_records)
    copyrights = load_yaml_records(copyright_records)
    summary_records = load_yaml_records(summary)
    errors: list[str] = []
    counts = {
        "snapshot_records": len(snapshots),
        "fetch_records": len(fetches),
        "copyright_records": len(copyrights),
        "summary_records": len(summary_records),
    }
    if not snapshots:
        errors.append("snapshot_records_missing")
    if not fetches:
        errors.append("fetch_records_missing")
    if len(summary_records) != 1:
        errors.append("summary_record_missing")
    snapshot_ids = {str(record.get("snapshot_record_id")) for record in snapshots}
    fetch_snapshot_ids = {str(record.get("snapshot_record_id")) for record in fetches}
    if snapshot_ids != fetch_snapshot_ids:
        errors.append("snapshot_fetch_id_mismatch")
    for record in [*snapshots, *fetches, *copyrights, *summary_records]:
        _validate_common_flags(record, errors)
    for record in snapshots:
        _validate_snapshot(record, errors)
    for record in fetches:
        if record.get("retrieval_status") == "fetched" and not record.get("content_sha256"):
            errors.append(f"fetch_missing_content_sha256:{record.get('fetch_record_id')}")
    for record in copyrights:
        if record.get("record_type") == "public_source_lock_policy":
            continue
        if not record.get("licence_or_copyright_note"):
            errors.append(f"copyright_note_missing:{record.get('copyright_record_id')}")
    if summary_records:
        summary_record = summary_records[0]
        if int(summary_record.get("sources_allowlisted") or -1) != len(snapshots):
            errors.append("summary_allowlisted_count_mismatch")
        if int(summary_record.get("committed_small_text_snapshots") or 0) != 0:
            errors.append("unexpected_committed_snapshots")
    return counts, errors


def _validate_snapshot(record: dict[str, Any], errors: list[str]) -> None:
    label = str(record.get("snapshot_record_id"))
    if not record.get("source_url"):
        errors.append(f"source_url_missing:{label}")
    if not record.get("canonical_url"):
        errors.append(f"canonical_url_missing:{label}")
    if record.get("snapshot_policy") not in SNAPSHOT_POLICIES:
        errors.append(f"invalid_snapshot_policy:{label}")
    if record.get("lock_status") not in LOCK_STATUSES:
        errors.append(f"invalid_lock_status:{label}")
    if not record.get("licence_or_copyright_note"):
        errors.append(f"copyright_note_missing:{label}")
    if record.get("retrieval_status") == "fetched" and not record.get("content_sha256"):
        errors.append(f"fetched_snapshot_missing_hash:{label}")
    if record.get("committed_snapshot") is True:
        if record.get("snapshot_policy") != "committed_small_text_snapshot":
            errors.append(f"committed_snapshot_policy_mismatch:{label}")
        if not record.get("committed_snapshot_path"):
            errors.append(f"committed_snapshot_path_missing:{label}")


def _validate_common_flags(record: dict[str, Any], errors: list[str]) -> None:
    label = str(
        record.get("snapshot_record_id")
        or record.get("fetch_record_id")
        or record.get("copyright_record_id")
        or record.get("summary_id")
        or record.get("policy_id")
        or record.get("record_type")
    )
    for key in (
        "raw_private_data_committed",
        "binary_committed",
        "image_committed",
        "audio_committed",
        "font_committed",
        "archive_committed",
        "solve_claim",
    ):
        if key in record and record.get(key) is not False:
            errors.append(f"{key}_not_false:{label}")
