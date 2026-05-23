"""Stage 5AG research-bundle readiness helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json, write_records
from .models import RESEARCH_BUNDLE_READINESS_REPORT, STAGE5AG_BUNDLE_READINESS_PATH, STAGE5AG_ID, STAGE5AG_OUTPUT_DIR, STAGE5AG_SOURCE_STAGE_ID


def build_bundle_readiness(
    *,
    bundle_plan_path: Path,
    local_linkage_path: Path,
    out: Path = STAGE5AG_BUNDLE_READINESS_PATH,
    results_dir: Path = STAGE5AG_OUTPUT_DIR,
) -> dict[str, Any]:
    """Build deterministic readiness records for Stage 5AF research bundles."""

    bundles = read_records(bundle_plan_path)
    linkages = read_records(local_linkage_path)
    matched_source_ids = {
        record["source_id"]
        for record in linkages
        if record.get("local_match_status") in {"matched_exact", "matched_probable"}
    }
    records = []
    for bundle in bundles:
        required = list(bundle.get("included_source_ids", []))
        matched = [source_id for source_id in required if source_id in matched_source_ids]
        missing = [source_id for source_id in required if source_id not in matched_source_ids]
        readiness = _readiness_status(required, matched)
        records.append(
            {
                "record_type": "stage5ag_research_bundle_readiness_record",
                "schema": "schemas/source-harvester/research-bundle-readiness-record-v0.schema.json",
                "stage_id": STAGE5AG_ID,
                "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
                "bundle_id": bundle["bundle_id"],
                "required_source_ids": required,
                "matched_source_ids": matched,
                "missing_source_ids": missing,
                "local_material_count": len(matched),
                "readiness_status": readiness,
                "do_not_assume_notes_present": bool(bundle.get("do_not_assume_notes")),
                "recommended_next_action": _next_action(readiness),
                "solve_claim": False,
            }
        )
    summary = {
        "record_type": "stage5ag_research_bundle_readiness",
        "schema": "schemas/source-harvester/research-bundle-readiness-record-v0.schema.json",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "bundle_records": len(records),
        "ready_for_extraction_prep_count": sum(1 for record in records if record["readiness_status"] == "ready_for_extraction_prep"),
        "partial_count": sum(1 for record in records if record["readiness_status"] == "partially_ready"),
        "not_ready_count": sum(1 for record in records if record["readiness_status"] == "not_ready"),
        "records": records,
        "solve_claim": False,
    }
    write_records(out, records, **{key: summary[key] for key in ("record_type", "schema", "stage_id", "source_stage_id", "bundle_records", "ready_for_extraction_prep_count", "partial_count", "not_ready_count", "solve_claim")})
    write_json(results_dir / RESEARCH_BUNDLE_READINESS_REPORT, summary)
    return summary


def _readiness_status(required: list[str], matched: list[str]) -> str:
    if required and len(required) == len(matched):
        return "ready_for_extraction_prep"
    if matched:
        return "partially_ready"
    return "not_ready"


def _next_action(readiness: str) -> str:
    if readiness == "ready_for_extraction_prep":
        return "prepare curated ignored extraction bundle metadata"
    if readiness == "partially_ready":
        return "close missing source gaps or build partial curated bundle"
    return "collect or classify local source material first"
