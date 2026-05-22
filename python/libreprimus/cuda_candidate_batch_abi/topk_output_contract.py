"""Build deterministic top-k output contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import write_record_set, write_report
from libreprimus.cuda_candidate_batch_abi.models import COMMON_FLAGS, OUTPUT_DIR, TOPK_OUTPUT_CONTRACT_PATH, TOPK_REPORT_JSON


def build_topk_output_contract(
    *,
    topk_output_contract_out: Path = TOPK_OUTPUT_CONTRACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Define deterministic top-k output ordering without implementing reducers."""

    record = {
        "record_type": "topk_output_contract_record",
        "topk_contract_id": "stage5u-topk-output-contract-v0",
        "candidate_ordering": "candidate_major",
        "score_ordering": "score_component_specific_direction_required",
        "tie_break_policy": [
            "score descending unless component declares lower_is_better",
            "candidate_id ascending",
            "source_fixture_id ascending",
            "output_token_hash ascending",
        ],
        "max_k_policy": "manifest_declared_k_with_ci_fixture_caps",
        "required_candidate_ids": True,
        "required_hashes": ["output_token_hash"],
        "required_score_vector_reference": True,
        "generated_body_publication_allowed": False,
        "compact_summary_only": True,
        "stable_sort_required": True,
        "deterministic_across_threads": True,
        "deterministic_across_backends": True,
        "benchmark_execution_allowed": False,
        "implementation_allowed_now": False,
        **COMMON_FLAGS,
    }
    records = [record]
    write_record_set(topk_output_contract_out, records)
    write_report(out_dir, TOPK_REPORT_JSON, {"records": records})
    return records
