"""Top-k conformance records for Stage 5V."""

from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.export import write_record_set, write_report
from libreprimus.native_candidate_batch_conformance.models import COMMON_FLAGS, OUTPUT_DIR, REPORT_FILES, TOPK_CONFORMANCE_PATH


def build_topk_conformance(
    *,
    topk_conformance_out: Path = TOPK_CONFORMANCE_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    synthetic_scores = [
        {"candidate_id": "cand-b", "score_value": 0.75},
        {"candidate_id": "cand-a", "score_value": 0.75},
        {"candidate_id": "cand-c", "score_value": 0.5},
    ]
    sorted_scores = sorted(synthetic_scores, key=lambda item: (-float(item["score_value"]), str(item["candidate_id"])))
    records = [
        {
            **COMMON_FLAGS,
            "record_type": "topk_conformance_record",
            "schema": "schemas/cuda/topk-conformance-record-v0.schema.json",
            "topk_id": "stage5v-topk-score-desc-candidate-id-asc",
            "fixture_id": "stage5v-topk-tie-policy-fixture",
            "conformance_status": "passed",
            "topk_k": 3,
            "tie_policy": "score_desc_candidate_id_asc",
            "sorted_candidate_ids": [str(item["candidate_id"]) for item in sorted_scores],
            "score_interpretation": "triage_only",
            "generated_body_committed": False,
        }
    ]
    write_record_set(topk_conformance_out, records)
    write_report(out_dir, REPORT_FILES["topk"], {"records": records, "count": len(records)})
    return records
