"""Stage 5AI website-ingest metadata generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .export import write_json, write_yaml
from .models import (
    STAGE5AI_BUNDLE_ROOT,
    STAGE5AI_ID,
    STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
    STAGE5AI_OUTPUT_DIR,
    STAGE5AI_REPORTS,
    STAGE5AI_SOURCE_STAGE_ID,
    STAGE5AI_WEBSITE_INGEST_FORMAT_PATH,
)


def build_website_ingest_index(
    *,
    bundle_root: Path = STAGE5AI_BUNDLE_ROOT,
    results_dir: Path = STAGE5AI_OUTPUT_DIR,
    out: Path = STAGE5AI_WEBSITE_INGEST_FORMAT_PATH,
) -> dict[str, Any]:
    """Build conservative website-ingest metadata without website expansion."""

    source_cards = _read_jsonl(bundle_root / "source_cards.jsonl")
    content_records = _read_jsonl(bundle_root / "content_index.jsonl")
    bundle_records = _bundle_records(bundle_root)
    index = {
        "record_type": "stage5ai_website_ingest_index",
        "schema": "schemas/source-harvester/website-ingest-bundle-index-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "publication_default": "generated_extract_review_required",
        "website_expansion_performed": False,
        "source_cards": source_cards,
        "content_records": content_records,
        "bundles": bundle_records,
        "solve_claim": False,
    }
    write_json(bundle_root / "website_ingest_index.json", index)
    write_json(results_dir / STAGE5AI_REPORTS["website_ingest"], index)
    summary = {
        "record_type": "stage5ai_website_ingest_format",
        "schema": "schemas/source-harvester/website-ingest-bundle-index-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "website_ingest_metadata_ready": True,
        "website_ingest_source_card_records": len(source_cards),
        "website_ingest_content_records": len(content_records),
        "website_ingest_bundle_records": len(bundle_records),
        "public_website_ready_count": 0,
        "generated_extract_review_required_count": sum(1 for record in content_records if record.get("publication_status") == "generated_extract_review_required"),
        "blocked_private_or_sensitive_count": sum(1 for record in content_records if record.get("publication_status") == "blocked_private_or_sensitive"),
        "website_expansion_performed": False,
        "solve_claim": False,
    }
    write_yaml(out, summary)
    return {**summary, "source_cards": source_cards, "content_records": content_records, "bundles": bundle_records}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _bundle_records(bundle_root: Path) -> list[dict[str, Any]]:
    records = []
    for manifest in sorted(bundle_root.glob("*/manifest.yaml")):
        bundle_id = manifest.parent.name
        # Avoid coupling this lightweight index to YAML internals; the compact
        # committed summary carries the validated counts.
        records.append(
            {
                "bundle_id": bundle_id,
                "relative_manifest_path": f"{bundle_id}/manifest.yaml",
                "publication_status": "generated_extract_review_required",
                "website_publication_allowed": False,
                "solve_claim": False,
            }
        )
    return records
