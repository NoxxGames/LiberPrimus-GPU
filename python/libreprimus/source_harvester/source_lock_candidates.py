"""Stage 5AG source-lock candidate and gap summaries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_records
from .models import STAGE5AG_CANDIDATE_SUMMARY_PATH, STAGE5AG_GAP_REPORT_PATH, STAGE5AG_ID, STAGE5AG_SOURCE_STAGE_ID


def build_source_lock_candidates(
    *,
    local_linkage_path: Path,
    out: Path = STAGE5AG_CANDIDATE_SUMMARY_PATH,
    gap_report: Path = STAGE5AG_GAP_REPORT_PATH,
) -> dict[str, Any]:
    """Classify local linkage records into source-lock readiness buckets."""

    linkage_records = read_records(local_linkage_path)
    candidate_records = []
    gap_records = []
    for record in linkage_records:
        status = _candidate_status(record)
        candidate = {
            "record_type": "stage5ag_source_lock_candidate_record",
            "schema": "schemas/source-harvester/source-lock-candidate-summary-record-v0.schema.json",
            "stage_id": STAGE5AG_ID,
            "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
            "source_id": record["source_id"],
            "candidate_status": status,
            "matched_paths": record.get("matched_paths", []),
            "manual_action_required": status not in {"ready_for_source_lock_inventory", "duplicate_or_redundant"},
            "metadata_only": True,
            "raw_content_committed": False,
            "solve_claim": False,
        }
        candidate_records.append(candidate)
        if status in {"missing", "needs_manual_export", "needs_manual_classification", "unsupported_archive_type"}:
            gap_records.append(
                {
                    "record_type": "stage5ag_local_source_gap_record",
                    "schema": "schemas/source-harvester/local-source-gap-report-record-v0.schema.json",
                    "stage_id": STAGE5AG_ID,
                    "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
                    "source_id": record["source_id"],
                    "gap_status": status,
                    "recommended_action": _recommended_action(status),
                    "solve_claim": False,
                }
            )
    summary = {
        "record_type": "stage5ag_source_lock_candidate_summary",
        "schema": "schemas/source-harvester/source-lock-candidate-summary-record-v0.schema.json",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "ready_count": sum(1 for record in candidate_records if record["candidate_status"] == "ready_for_source_lock_inventory"),
        "needs_review_count": sum(1 for record in candidate_records if record["candidate_status"] == "needs_manual_classification"),
        "missing_count": sum(1 for record in candidate_records if record["candidate_status"] == "missing"),
        "records": candidate_records,
        "solve_claim": False,
    }
    gaps = {
        "record_type": "stage5ag_local_source_gap_report",
        "schema": "schemas/source-harvester/local-source-gap-report-record-v0.schema.json",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "gap_count": len(gap_records),
        "records": gap_records,
        "solve_claim": False,
    }
    write_records(out, candidate_records, **{key: summary[key] for key in ("record_type", "schema", "stage_id", "source_stage_id", "ready_count", "needs_review_count", "missing_count", "solve_claim")})
    write_records(gap_report, gap_records, **{key: gaps[key] for key in ("record_type", "schema", "stage_id", "source_stage_id", "gap_count", "solve_claim")})
    return {"summary": summary, "gap_report": gaps}


def _candidate_status(record: dict[str, Any]) -> str:
    if record.get("source_id", "").startswith("local_unclassified_"):
        return "needs_manual_classification"
    if record.get("local_match_status") in {"matched_exact", "matched_probable"}:
        return "ready_for_source_lock_inventory"
    if record.get("manual_collection_required"):
        return "needs_manual_export"
    return "missing"


def _recommended_action(status: str) -> str:
    return {
        "missing": "provide local ignored source material or defer to a later explicit online-fetch stage",
        "needs_manual_export": "export manually into an ignored local source root",
        "needs_manual_classification": "classify local material and assign a source_id before source locking",
        "unsupported_archive_type": "install a local archive lister or extract manually into an ignored root",
    }.get(status, "review")
