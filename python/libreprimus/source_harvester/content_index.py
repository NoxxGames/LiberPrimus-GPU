"""Stage 5AI content-index aggregation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .export import write_json, write_jsonl, write_records
from .models import (
    STAGE5AI_BUNDLE_ROOT,
    STAGE5AI_CONTENT_INDEX_SUMMARY_PATH,
    STAGE5AI_ID,
    STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
    STAGE5AI_OUTPUT_DIR,
    STAGE5AI_REPORTS,
    STAGE5AI_SOURCE_STAGE_ID,
)


def build_content_index(
    *,
    bundle_root: Path = STAGE5AI_BUNDLE_ROOT,
    results_dir: Path = STAGE5AI_OUTPUT_DIR,
    out: Path = STAGE5AI_CONTENT_INDEX_SUMMARY_PATH,
) -> dict[str, Any]:
    """Aggregate bundle content-index JSONL files into root and report outputs."""

    records = []
    for path in sorted(bundle_root.glob("*/content_index.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(json.loads(line))
    records.sort(key=lambda record: (record.get("bundle_id", ""), record.get("source_id", "")))
    write_jsonl(bundle_root / "content_index.jsonl", records)
    write_jsonl(results_dir / STAGE5AI_REPORTS["content_index"], records)
    summary = {
        "record_type": "stage5ai_curated_content_index_summary",
        "schema": "schemas/source-harvester/curated-content-index-summary-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "content_index_records": len(records),
        "bundle_count": len({record.get("bundle_id") for record in records}),
        "generated_extract_review_required_count": sum(1 for record in records if record.get("publication_status") == "generated_extract_review_required"),
        "blocked_private_or_sensitive_count": sum(1 for record in records if record.get("publication_status") == "blocked_private_or_sensitive"),
        "website_publication_allowed_count": 0,
        "generated_bundle_bodies_committed": False,
        "website_expansion_performed": False,
        "solve_claim": False,
    }
    write_records(out, records, **summary)
    write_json(results_dir / "curated_content_index_summary.json", {**summary, "records": records})
    return {**summary, "records": records}
