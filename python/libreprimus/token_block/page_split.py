"""Stage 5AR page-split policy records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import FALSE_GUARDRAILS, STAGE5AR_ID, TOKEN_BLOCK_ID, read_yaml, repo_relative, write_json, write_yaml

COMMUNITY_SPLIT = {
    49: {"global_rows_0_based": [0, 9], "global_rows_1_based": [1, 10], "row_count": 10},
    50: {"global_rows_0_based": [10, 22], "global_rows_1_based": [11, 23], "row_count": 13},
    51: {"global_rows_0_based": [23, 31], "global_rows_1_based": [24, 32], "row_count": 9},
}


def build_page_split(
    *,
    stage5ap_transcription: Path,
    original_image_source_lock: Path,
    results_dir: Path,
    out_policy: Path,
    out_records: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    transcription = read_yaml(stage5ap_transcription)
    source_lock = read_yaml(original_image_source_lock)
    originals = source_lock.get("records", [])
    original_pages = {record["page_number"] for record in originals}
    row_sum = sum(record["row_count"] for record in COMMUNITY_SPLIT.values())
    accepted = original_pages == {49, 50, 51} and transcription.get("row_count") == 32 and row_sum == 32
    page_split_status = "source_locked_logical_page_split" if accepted else "unresolved_source_gap"
    policy = {
        "record_type": "page_split_policy",
        "schema": "schemas/token-block/page-split-policy-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "candidate_page_split_id": "community_10_13_9",
        "page_split_status": page_split_status,
        "source_basis": "original page images show 10, 13, and 9 token rows for pages 49, 50, and 51; Stage 5AR records this as coordinate substrate only.",
        "accepted": accepted,
        "confidence": "medium_high" if accepted else "blocked_missing_original_images",
        "review_status": "accepted_review_required" if accepted else "blocked_source_gap",
        "row_count_sum": row_sum,
        "no_decode": True,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    records = []
    by_page = {record["page_number"]: record for record in originals}
    for page, split in COMMUNITY_SPLIT.items():
        image = by_page.get(page, {})
        records.append(
            {
                "record_type": "page_split_record",
                "schema": "schemas/token-block/page-split-record-v0.schema.json",
                "stage_id": STAGE5AR_ID,
                "token_block_id": TOKEN_BLOCK_ID,
                "candidate_page_split_id": "community_10_13_9",
                "page_number": page,
                "row_count": split["row_count"],
                "global_rows_0_based": split["global_rows_0_based"],
                "global_rows_1_based": split["global_rows_1_based"],
                "supporting_original_images": [image.get("original_image_id")] if image else [],
                "supporting_original_image_paths": [image.get("source_path")] if image else [],
                "supporting_non_original_images": [],
                "source_basis": "original_liber_primus_page_image" if image else "missing_original_image",
                "confidence": "medium_high" if image else "blocked",
                "review_status": "accepted_review_required" if image else "blocked_source_gap",
                "accepted": accepted and bool(image),
                "reason": "community 10/13/9 split matches visible token-row counts in selected original page images"
                if accepted and image
                else "missing original page image prevents source-locked page split",
                "raw_image_committed": False,
                "solve_claim": False,
            }
        )
    payload = {
        "record_type": "page_split_record_set",
        "schema": "schemas/token-block/page-split-record-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "candidate_page_split_id": "community_10_13_9",
        "page_split_status": page_split_status,
        "accepted": accepted,
        "page_49_row_count": COMMUNITY_SPLIT[49]["row_count"],
        "page_50_row_count": COMMUNITY_SPLIT[50]["row_count"],
        "page_51_row_count": COMMUNITY_SPLIT[51]["row_count"],
        "row_count_sum": row_sum,
        "records": records,
        "source_path": repo_relative(original_image_source_lock),
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out_policy, policy)
    write_yaml(out_records, payload)
    write_json(results_dir / "page_split_validation.json", payload)
    return policy, payload
