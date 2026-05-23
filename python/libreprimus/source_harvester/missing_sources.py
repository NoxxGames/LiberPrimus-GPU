"""Stage 5AI missing-source planning."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json, write_jsonl, write_records
from .models import (
    STAGE5AI_BUNDLE_ROOT,
    STAGE5AI_ID,
    STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
    STAGE5AI_MISSING_SOURCE_PLAN_PATH,
    STAGE5AI_OUTPUT_DIR,
    STAGE5AI_REPORTS,
    STAGE5AI_SOURCE_STAGE_ID,
)


def build_missing_source_plan(
    *,
    stage5ag_readiness_path: Path,
    local_linkage_path: Path,
    out: Path = STAGE5AI_MISSING_SOURCE_PLAN_PATH,
    results_dir: Path = STAGE5AI_OUTPUT_DIR,
    bundle_root: Path = STAGE5AI_BUNDLE_ROOT,
) -> dict[str, Any]:
    """Build deterministic next-action records for Stage 5AG missing sources."""

    linkage_by_source = {record["source_id"]: record for record in read_records(local_linkage_path)}
    missing: dict[str, set[str]] = {}
    for bundle in read_records(stage5ag_readiness_path):
        for source_id in bundle.get("missing_source_ids", []):
            missing.setdefault(source_id, set()).add(bundle["bundle_id"])
    records = []
    for source_id, bundle_ids in sorted(missing.items()):
        linkage = linkage_by_source.get(source_id, {})
        source_type = str(linkage.get("source_type", "unknown"))
        priority = str(linkage.get("expected_priority", "unknown"))
        records.append(
            {
                "record_type": "stage5ai_missing_source_plan_record",
                "schema": "schemas/source-harvester/missing-source-plan-v0.schema.json",
                "stage_id": STAGE5AI_ID,
                "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
                "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
                "source_id": source_id,
                "source_type": source_type,
                "priority": priority,
                "bundle_ids": sorted(bundle_ids),
                "next_action": _next_action(source_type, priority),
                "network_fetch_performed": False,
                "online_repo_clone_performed": False,
                "google_drive_storage_used": False,
                "manual_review_required": True,
                "solve_claim": False,
            }
        )
    summary = {
        "record_type": "stage5ai_missing_source_plan",
        "schema": "schemas/source-harvester/missing-source-plan-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "missing_source_records": len(records),
        "missing_a1_a2_count": sum(1 for record in records if record["priority"] in {"A1", "A2"}),
        "manual_export_count": sum(1 for record in records if record["next_action"] == "manual_export"),
        "online_fetch_later_count": sum(1 for record in records if record["next_action"] == "online_fetch_later"),
        "repo_clone_later_count": sum(1 for record in records if record["next_action"] == "repo_clone_later"),
        "targeted_forum_capture_later_count": sum(1 for record in records if record["next_action"] == "targeted_forum_capture_later"),
        "optional_low_priority_count": sum(1 for record in records if record["next_action"] == "optional_low_priority"),
        "network_fetch_performed": False,
        "online_repo_clone_performed": False,
        "google_drive_storage_used": False,
        "solve_claim": False,
    }
    write_records(out, records, **summary)
    bundle_root.mkdir(parents=True, exist_ok=True)
    write_jsonl(bundle_root / "missing_sources.jsonl", records)
    write_json(results_dir / STAGE5AI_REPORTS["missing_sources"], {**summary, "records": records})
    return {**summary, "records": records}


def _next_action(source_type: str, priority: str) -> str:
    if source_type in {"google_sheet", "google_doc", "google_colab", "browser_tool", "shiny_app"}:
        return "manual_export"
    if source_type in {"github_repo", "github_org"}:
        return "repo_clone_later"
    if source_type in {"forum_index", "forum_thread"}:
        return "targeted_forum_capture_later"
    if priority in {"B", "C"} or source_type in {"youtube_video", "youtube_channel"}:
        return "optional_low_priority"
    return "online_fetch_later"
