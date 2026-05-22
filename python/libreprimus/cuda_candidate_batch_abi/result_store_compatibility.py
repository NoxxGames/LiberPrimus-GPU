"""Build result-store and score-summary compatibility records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import write_record_set, write_report
from libreprimus.cuda_candidate_batch_abi.models import (
    ABI_ID,
    COMMON_FLAGS,
    OUTPUT_DIR,
    RESULT_STORE_COMPATIBILITY_PATH,
    RESULT_STORE_REPORT_JSON,
)


def build_result_store_compatibility(
    *,
    result_store_compatibility_out: Path = RESULT_STORE_COMPATIBILITY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Link Candidate Batch ABI v0 to Stage 4P and Stage 4I contracts."""

    rows = [
        ("stage4p_compact_result_store", "compact summaries may be committed; generated bodies remain ignored"),
        ("stage4i_score_summary", "finite triage labels only; scores are not solve evidence"),
        ("output_hash_policy", "output token hashes are required; output text hashes wait for transliteration policy"),
    ]
    records = [
        {
            "record_type": "candidate_batch_result_store_compatibility_record",
            "result_store_compatibility_id": f"stage5u-{compat_id}",
            "abi_id": ABI_ID,
            "result_store_contract": "stage4p",
            "score_summary_contract": "stage4i",
            "allowed_committed_record_type": "compact_summary_metadata",
            "generated_body_publication_allowed": False,
            "output_token_hash_required": True,
            "output_text_hash_policy": "blocked_pending_transliteration_policy",
            "score_summary_label_policy": "finite_triage_only",
            "confidence_label_policy": "stage4i_labels_only",
            "method_status_upgrade_allowed": False,
            "performance_claim_allowed": False,
            "speedup_claim_allowed": False,
            "solve_claim": False,
            "notes": notes,
            **COMMON_FLAGS,
        }
        for compat_id, notes in rows
    ]
    write_record_set(result_store_compatibility_out, records)
    write_report(out_dir, RESULT_STORE_REPORT_JSON, {"records": records})
    return records
