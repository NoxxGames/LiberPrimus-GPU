"""Dry-run harvesting plan builders."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .export import write_json, write_jsonl, write_yaml
from .manifest import manifest_records
from .models import (
    DRY_RUN_SUMMARY_REPORT,
    HARVEST_PLAN_REPORT,
    OUTPUT_DIR,
    WARNINGS_REPORT,
    common_record_flags,
)


def build_plan(
    *,
    manifest_path: Path,
    out_path: Path = OUTPUT_DIR / HARVEST_PLAN_REPORT,
    dry_run_summary_out: Path | None = None,
    out_dir: Path = OUTPUT_DIR,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Build a dry-run source collection plan without network access."""

    records = manifest_records(manifest_path)
    plan_records = [_plan_record(record) for record in records]
    warnings = _plan_warnings(plan_records)
    summary = {
        "record_type": "stage5af_harvest_dry_run_summary",
        **common_record_flags(),
        "source_manifest_records": len(records),
        "dry_run_plan_records": len(plan_records),
        "network_default_allowed": False,
        "download_default_allowed": False,
        "browser_default_allowed": False,
        "network_fetch_performed": False,
        "live_web_scrape_performed": False,
        "raw_downloads_committed": False,
        "raw_archives_processed": False,
        "plan_status_counts": dict(sorted(Counter(record["plan_status"] for record in plan_records).items())),
        "manual_collection_required_count": sum(
            1 for record in plan_records if record["manual_collection_required"] is True
        ),
        "network_fetch_deferred_count": sum(
            1 for record in plan_records if record["plan_status"] == "network_fetch_deferred"
        ),
        "warnings_count": len(warnings),
    }
    write_json(out_path, {"records": plan_records, "summary": summary})
    write_json(out_dir / DRY_RUN_SUMMARY_REPORT, summary)
    write_jsonl(out_dir / WARNINGS_REPORT, [{"warning": warning} for warning in warnings])
    if dry_run_summary_out is not None:
        write_yaml(dry_run_summary_out, summary)
    return plan_records, summary


def _plan_record(record: dict[str, Any]) -> dict[str, Any]:
    source_type = record.get("source_type")
    manual = bool(record.get("manual_collection_required"))
    allow_network = bool(record.get("allow_network_fetch"))
    if source_type == "local_user_upload":
        plan_status = "local_file_required"
    elif manual:
        plan_status = "manual_collection_required"
    elif allow_network:
        plan_status = "network_fetch_deferred"
    else:
        plan_status = "metadata_only"
    return {
        "record_type": "harvest_plan_record",
        "schema": "schemas/source-harvester/harvest-plan-record-v0.schema.json",
        **common_record_flags(),
        "source_id": record["source_id"],
        "title": record["title"],
        "url": record.get("url"),
        "source_type": source_type,
        "priority": record.get("priority"),
        "source_tier": record.get("source_tier"),
        "recommended_capture_modes": list(record.get("recommended_capture_modes", [])),
        "manual_collection_required": manual,
        "network_allowed_by_manifest": allow_network,
        "dynamic_browser_allowed_by_manifest": bool(record.get("allow_dynamic_browser")),
        "dry_run_only": True,
        "plan_status": plan_status,
        "execution_enabled": False,
        "fetch_performed": False,
        "download_performed": False,
    }


def _plan_warnings(records: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    for record in records:
        if record["plan_status"] == "manual_collection_required":
            warnings.append(f"{record['source_id']}: manual collection/export required")
        if record["dynamic_browser_allowed_by_manifest"]:
            warnings.append(f"{record['source_id']}: dynamic browser adapter disabled by default")
        if record["source_type"] in {"youtube_video", "youtube_channel"}:
            warnings.append(f"{record['source_id']}: video download disabled by default")
    return warnings
