"""Stage 5AI provisional classification for local unclassified sources."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json, write_records
from .models import (
    STAGE5AI_CLASSIFICATION_PATH,
    STAGE5AI_ID,
    STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
    STAGE5AI_OUTPUT_DIR,
    STAGE5AI_SOURCE_STAGE_ID,
)


CLASSIFICATION_MAP: dict[str, dict[str, Any]] = {
    "depictions_original.png": {
        "bundle_ids": ["05-red-markers-and-visual-numerics"],
        "clue_categories": ["depictions_tree_cicada_mayfly_wing_spiral_cuneiform"],
        "classification_status": "provisionally_classified",
    },
    "depictions_modified.png": {
        "bundle_ids": ["05-red-markers-and-visual-numerics"],
        "clue_categories": ["modified_image_review_only"],
        "classification_status": "provisionally_classified",
    },
    "cunieform_numbers.png": {
        "bundle_ids": ["04-cuneiform-base60-base59"],
        "clue_categories": ["cuneiform_base60_base59"],
        "classification_status": "provisionally_classified",
    },
    "more_numbers_mixed_with_runes_page.png": {
        "bundle_ids": ["05-red-markers-and-visual-numerics"],
        "clue_categories": ["mixed_numeric_rune_page"],
        "classification_status": "provisionally_classified",
    },
    "page_modified_example.png": {
        "bundle_ids": ["06-outguess-stego-hidden-formatting"],
        "clue_categories": ["modified_page_artifact_claim"],
        "classification_status": "provisionally_classified",
    },
    "rune_pixel_diff_example.png": {
        "bundle_ids": ["05-red-markers-and-visual-numerics"],
        "clue_categories": ["rune_pixel_variants"],
        "classification_status": "provisionally_classified",
    },
    "repeat-rune.png": {
        "bundle_ids": ["07-boundary-mobius-repeated-fragments"],
        "clue_categories": ["dju_bei_repeat"],
        "classification_status": "provisionally_classified",
    },
    "interconnected-chapters": {
        "bundle_ids": ["07-boundary-mobius-repeated-fragments"],
        "clue_categories": ["interconnected_chapters"],
        "classification_status": "provisionally_classified",
    },
    "communityobservations": {
        "bundle_ids": ["09-community-hypotheses"],
        "clue_categories": ["discord_community_hypothesis_leads"],
        "classification_status": "provisionally_classified",
    },
    "liberprimusdiscordchats": {
        "bundle_ids": ["09-community-hypotheses"],
        "clue_categories": ["discord_private_or_sensitive"],
        "classification_status": "provisionally_classified_private",
        "publication_status": "blocked_private_or_sensitive",
        "redaction_required": True,
    },
    "fib421.jpg": {
        "bundle_ids": ["09-community-hypotheses", "10-known-negative-retired-ideas"],
        "clue_categories": ["bigram_fibonacci_421_review_needed", "false_positive_control_candidate"],
        "classification_status": "needs_review",
    },
    "sourcesnapshots": {
        "bundle_ids": ["cross-bundle-source-snapshots"],
        "clue_categories": ["source_lock_snapshots_review_needed"],
        "classification_status": "needs_review",
    },
    "1348008594460774501.png": {
        "bundle_ids": ["unknown-review-needed"],
        "clue_categories": ["unknown_visual_clue_review_needed"],
        "classification_status": "needs_review",
    },
    "community-sources-of-datasets-depiction-images-plausable-methods-worth-exploring.md": {
        "bundle_ids": ["09-community-hypotheses"],
        "clue_categories": ["source_discovery_notes"],
        "classification_status": "provisionally_classified",
    },
}


def classify_local_sources(
    *,
    candidate_summary_path: Path,
    local_linkage_path: Path,
    out: Path = STAGE5AI_CLASSIFICATION_PATH,
    results_dir: Path = STAGE5AI_OUTPUT_DIR,
) -> dict[str, Any]:
    """Classify Stage 5AG unclassified local sources without upgrading evidence."""

    del candidate_summary_path
    records = []
    for linkage in read_records(local_linkage_path):
        source_id = str(linkage.get("source_id", ""))
        if not source_id.startswith("local_unclassified_"):
            continue
        path = str((linkage.get("matched_paths") or [""])[0])
        key = Path(path).name.lower()
        mapping = CLASSIFICATION_MAP.get(key, {})
        publication_status = mapping.get("publication_status", "metadata_only")
        record = {
            "record_type": "stage5ai_unclassified_source_classification_record",
            "schema": "schemas/source-harvester/unclassified-source-classification-v0.schema.json",
            "stage_id": STAGE5AI_ID,
            "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
            "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
            "source_id": source_id,
            "source_path": path,
            "provisional_bundle_ids": list(mapping.get("bundle_ids", ["unknown-review-needed"])),
            "provisional_clue_categories": list(mapping.get("clue_categories", ["review_needed"])),
            "classification_status": str(mapping.get("classification_status", "needs_review")),
            "evidence_status_upgraded": False,
            "usable_as_evidence": False,
            "publication_status": publication_status,
            "website_publication_allowed": False,
            "redaction_required": bool(mapping.get("redaction_required", False)),
            "review_required": True,
            "solve_claim": False,
        }
        records.append(record)
    records.sort(key=lambda item: item["source_id"])
    summary = {
        "record_type": "stage5ai_unclassified_source_classification",
        "schema": "schemas/source-harvester/unclassified-source-classification-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "classification_records": len(records),
        "provisionally_classified_count": sum(1 for record in records if str(record["classification_status"]).startswith("provisionally")),
        "needs_review_count": sum(1 for record in records if record["classification_status"] == "needs_review"),
        "private_or_sensitive_count": sum(1 for record in records if record["publication_status"] == "blocked_private_or_sensitive"),
        "evidence_status_upgraded": False,
        "solve_claim": False,
    }
    write_records(out, records, **summary)
    write_json(results_dir / "unclassified_source_classification.json", {**summary, "records": records})
    return {**summary, "records": records}
