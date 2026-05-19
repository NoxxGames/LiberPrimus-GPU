"""Build and export Stage 4K source-lock snapshot records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root
from libreprimus.source_lock_snapshots.allowlist import (
    canonicalize_url,
    is_allowlisted_url,
    is_priority_candidate,
    is_rejected_url,
)
from libreprimus.source_lock_snapshots.copyright_policy import (
    committed_snapshot_allowed,
    copyright_note,
)
from libreprimus.source_lock_snapshots.fetcher import fetch_to_ignored_cache, utc_now
from libreprimus.source_lock_snapshots.github_metadata import github_lock_metadata
from libreprimus.source_lock_snapshots.loaders import load_source_candidates, write_yaml_document, write_yaml_records
from libreprimus.source_lock_snapshots.models import (
    DEFAULT_CACHE_DIR,
    DEFAULT_COPYRIGHT_RECORDS_OUT,
    DEFAULT_FETCH_RECORDS_OUT,
    DEFAULT_OUT_DIR,
    DEFAULT_SNAPSHOT_RECORDS_OUT,
    DEFAULT_SUMMARY_OUT,
    FetchResult,
    common_policy_flags,
)
from libreprimus.source_lock_snapshots.review_update import source_lock_update_record
from libreprimus.source_lock_snapshots.snapshot_policy import (
    artifact_kind,
    choose_snapshot_policy,
    classify_source_class,
)
from libreprimus.source_lock_snapshots.summary import summarize_source_locks


def build_source_lock_snapshots(
    *,
    out_dir: Path = repo_root() / DEFAULT_OUT_DIR,
    cache_dir: Path = repo_root() / DEFAULT_CACHE_DIR,
    snapshot_records_out: Path = repo_root() / DEFAULT_SNAPSHOT_RECORDS_OUT,
    fetch_records_out: Path = repo_root() / DEFAULT_FETCH_RECORDS_OUT,
    copyright_records_out: Path = repo_root() / DEFAULT_COPYRIGHT_RECORDS_OUT,
    summary_out: Path = repo_root() / DEFAULT_SUMMARY_OUT,
    allow_network: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Build Stage 4K source-lock snapshot records."""

    del allow_warnings  # Warnings are recorded, not fatal, in Stage 4K.
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    candidates = load_source_candidates()
    considered_count = len(candidates)
    seen: set[str] = set()
    allowlisted_count = 0
    snapshot_records: list[dict[str, Any]] = []
    fetch_records: list[dict[str, Any]] = []
    copyright_records: list[dict[str, Any]] = []
    rejected_records: list[dict[str, Any]] = []
    duplicate_records: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    for candidate in candidates:
        canonical = canonicalize_url(candidate.source_url)
        base_report = {
            "candidate_id": candidate.candidate_id,
            "source_url": candidate.source_url,
            "canonical_url": canonical,
            "source_family": candidate.source_family,
        }
        if canonical in seen:
            duplicate_records.append({**base_report, "reason": "duplicate_canonical_url"})
            continue
        seen.add(canonical)
        if is_rejected_url(candidate.source_url) or not is_priority_candidate(candidate) or not is_allowlisted_url(candidate.source_url):
            rejected_records.append(
                {
                    **base_report,
                    "reason": "not_priority_allowlisted_or_rejected_domain",
                    **common_policy_flags(),
                }
            )
            continue
        allowlisted_count += 1
        snapshot_record, fetch_record, copyright_record = _build_one_record(
            candidate=candidate,
            canonical=canonical,
            cache_dir=cache_dir,
            allow_network=allow_network,
        )
        snapshot_records.append(snapshot_record)
        fetch_records.append(fetch_record)
        copyright_records.append(copyright_record)
        if snapshot_record.get("retrieval_status") == "fetch_failed":
            warnings.append(
                {
                    "snapshot_record_id": snapshot_record["snapshot_record_id"],
                    "warning": "fetch_failed_metadata_preserved",
                    "source_url": candidate.source_url,
                    "error": fetch_record.get("error"),
                }
            )
        if snapshot_record.get("retrieval_status") == "network_disabled":
            warnings.append(
                {
                    "snapshot_record_id": snapshot_record["snapshot_record_id"],
                    "warning": "network_disabled_deferred_record",
                    "source_url": candidate.source_url,
                }
            )

    source_lock_updates = [source_lock_update_record(record) for record in snapshot_records]
    summary = summarize_source_locks(
        considered_count=considered_count,
        allowlisted_count=allowlisted_count,
        snapshot_records=snapshot_records,
        rejected_records=rejected_records,
        duplicate_records=duplicate_records,
        source_lock_updates=source_lock_updates,
    )
    write_yaml_records(
        snapshot_records_out,
        record_set_id="stage4k-source-lock-snapshot-records",
        schema="schemas/history/source-lock-snapshot-record-v0.schema.json",
        records=snapshot_records,
    )
    write_yaml_records(
        fetch_records_out,
        record_set_id="stage4k-source-fetch-records",
        schema="schemas/history/source-fetch-record-v0.schema.json",
        records=fetch_records,
    )
    write_yaml_records(
        copyright_records_out,
        record_set_id="stage4k-source-copyright-policy-records",
        schema="schemas/history/source-copyright-policy-record-v0.schema.json",
        records=copyright_records,
    )
    write_yaml_document(summary_out, summary)

    _write_json(out_dir / "fetch_report.json", {"records": fetch_records, "summary": summary})
    _write_jsonl(out_dir / "rejected_sources.jsonl", rejected_records)
    _write_jsonl(out_dir / "duplicate_sources.jsonl", duplicate_records)
    _write_jsonl(out_dir / "warnings.jsonl", warnings)
    return summary


def _build_one_record(
    *,
    candidate,
    canonical: str,
    cache_dir: Path,
    allow_network: bool,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    timestamp = utc_now()
    source_class = classify_source_class(candidate.source_url, candidate.artifact_type)
    snapshot_policy = choose_snapshot_policy(candidate.source_url, source_class, candidate.artifact_type)
    gh_metadata = github_lock_metadata(candidate.source_url, allow_network=allow_network, cwd=repo_root())
    canonical_url = gh_metadata.get("canonical_url") or canonical
    kind = artifact_kind(candidate.source_url, candidate.artifact_type)
    fetch_result = _fetch_for_policy(
        candidate=candidate,
        cache_dir=cache_dir,
        allow_network=allow_network,
        snapshot_policy=snapshot_policy,
        kind=kind,
    )
    lock_status = _lock_status(snapshot_policy, fetch_result.retrieval_status, bool(gh_metadata.get("commit_address_locked")))
    record_id = f"stage4k-{candidate.candidate_id}".replace("--", "-")
    base = {
        "snapshot_record_id": record_id,
        "source_candidate_id": candidate.candidate_id,
        "source_family": candidate.source_family,
        "source_url": candidate.source_url,
        "canonical_url": canonical_url,
        "source_class": source_class,
        "source_path": candidate.source_path,
        "artifact_type": candidate.artifact_type,
        "source_basis": candidate.source_basis,
        "retrieval_timestamp_utc": timestamp,
        "retrieval_status": fetch_result.retrieval_status,
        "snapshot_policy": snapshot_policy,
        "lock_status": lock_status,
        "http_status": fetch_result.http_status,
        "content_type": fetch_result.content_type,
        "content_length": fetch_result.content_length,
        "content_sha256": fetch_result.content_sha256,
        "ignored_cache_path": _repo_relative_or_none(fetch_result.ignored_cache_path),
        "github_owner": gh_metadata.get("github_owner"),
        "github_repo": gh_metadata.get("github_repo"),
        "github_ref": gh_metadata.get("github_ref"),
        "github_path": gh_metadata.get("github_path"),
        "github_reference_kind": gh_metadata.get("github_reference_kind"),
        "github_commit_sha": gh_metadata.get("github_commit_sha"),
        "github_blob_sha": None,
        "committed_snapshot": False,
        "committed_snapshot_path": None,
        "licence_or_copyright_note": copyright_note(candidate.source_url, source_class),
        **common_policy_flags(),
    }
    fetch_record = {
        "record_type": "source_fetch_record",
        "fetch_record_id": f"{record_id}-fetch",
        "error": fetch_result.error,
        **base,
    }
    snapshot_record = {
        "record_type": "source_lock_snapshot_record",
        **base,
    }
    allowed, reason = committed_snapshot_allowed(candidate.source_url, snapshot_policy, candidate.artifact_type)
    copyright_record = {
        "record_type": "source_copyright_policy_record",
        "copyright_record_id": f"{record_id}-copyright",
        "snapshot_record_id": record_id,
        "source_url": candidate.source_url,
        "licence_or_copyright_note": base["licence_or_copyright_note"],
        "committed_snapshot_allowed": allowed,
        "committed_snapshot_reason": reason,
        **common_policy_flags(),
    }
    return snapshot_record, fetch_record, copyright_record


def _fetch_for_policy(*, candidate, cache_dir: Path, allow_network: bool, snapshot_policy: str, kind: str):
    if snapshot_policy == "ignored_local_snapshot" and kind in {"page_or_repo", "text"}:
        return fetch_to_ignored_cache(
            url=candidate.source_url,
            cache_dir=cache_dir,
            record_id=f"stage4k-{candidate.candidate_id}",
            allow_network=allow_network,
        )
    if snapshot_policy == "commit_addressed_reference":
        status = "metadata_only" if allow_network else "network_disabled"
        return FetchResult(retrieval_status=status)
    if kind in {"binary", "image", "audio", "font", "archive"}:
        return FetchResult(retrieval_status="not_fetched_binary_policy")
    return FetchResult(retrieval_status="metadata_only")


def _lock_status(snapshot_policy: str, retrieval_status: str, commit_locked: bool) -> str:
    if retrieval_status == "fetch_failed":
        return "fetch_failed"
    if commit_locked:
        return "commit_address_locked"
    if retrieval_status == "network_disabled":
        return "deferred_requires_manual_review"
    if snapshot_policy == "ignored_local_snapshot" and retrieval_status == "fetched":
        return "snapshot_cached_ignored"
    if snapshot_policy == "commit_addressed_reference":
        return "metadata_locked"
    if snapshot_policy == "archive_reference_only":
        return "metadata_locked"
    if snapshot_policy == "rejected_unsafe_or_noisy":
        return "rejected_unsafe"
    return "metadata_locked"


def _repo_relative_or_none(path_text: str | None) -> str | None:
    if path_text is None:
        return None
    path = Path(path_text)
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except (OSError, ValueError):
        return path.as_posix()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")
