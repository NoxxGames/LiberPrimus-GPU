"""Build and print Stage 5P summaries."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.gematria_cuda_result_store.export import read_record_set, write_report
from libreprimus.gematria_cuda_result_store.models import (
    CONTROLLED_EXPANSION_CANDIDATES_PATH,
    GENERATED_BODY_POLICY_PATH,
    HASH_ALGORITHM,
    METHOD_STATUS_IMPACT_PATH,
    NEXT_STAGE_READY,
    OUTPUT_DIR,
    RESULT_STORE_CONTRACT,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_CONTRACT,
    SCORE_SUMMARY_INTEGRATION_PATH,
    STAGE5O_SUMMARY,
    SUMMARY_PATH,
    SUMMARY_REPORT,
)


def build_summary(
    *,
    result_store_integration: Path = RESULT_STORE_INTEGRATION_PATH,
    score_summary_integration: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    method_status_impact: Path = METHOD_STATUS_IMPACT_PATH,
    generated_body_policy: Path = GENERATED_BODY_POLICY_PATH,
    controlled_expansion_candidates: Path = CONTROLLED_EXPANSION_CANDIDATES_PATH,
    stage5o_summary: Path = STAGE5O_SUMMARY,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    result_store = read_record_set(result_store_integration)
    score = read_record_set(score_summary_integration)
    impacts = read_record_set(method_status_impact)
    policies = read_record_set(generated_body_policy)
    candidates = read_record_set(controlled_expansion_candidates)
    stage5o = read_yaml(stage5o_summary)
    ready_candidates = [
        record
        for record in candidates
        if record.get("candidate_status") == "ready_for_stage5q_candidate_mapping"
    ]
    selected_next_stage = NEXT_STAGE_READY if ready_candidates else str(stage5o.get("selected_next_stage"))
    selected_next_stage_reason = (
        "Stage 5P integrated compact Stage 5O parity metadata and identified a bounded solved-fixture-safe "
        "shift_score candidate mapping stage as the next controlled step."
        if ready_candidates
        else "No controlled Stage 5Q candidate class was ready."
    )
    summary = {
        "record_type": "stage5p_cuda_result_store_integration_summary",
        "stage_id": "stage-5p",
        "status": "complete",
        "source_stage_id": "stage-5o",
        "source_stage5o_repeat_parity_records": int(stage5o.get("repeat_parity_records", 0)),
        "source_stage5o_repeat_parity_pass_count": int(stage5o.get("repeat_parity_pass_count", 0)),
        "result_store_integration_records": len(result_store),
        "score_summary_integration_records": len(score),
        "method_status_impact_records": len(impacts),
        "generated_body_policy_records": len(policies),
        "controlled_expansion_candidate_records": len(candidates),
        "integrated_compact_summary_records": sum(
            1 for record in result_store if record["stage5p_integration_status"] == "integrated_compact_summary"
        ),
        "stage4p_compatibility": all(record.get("stage4p_compatibility") is True for record in result_store),
        "stage4i_compatibility": all(record.get("stage4i_compatibility") is True for record in score),
        "compact_summary_only": True,
        "score_summary_contract": SCORE_SUMMARY_CONTRACT,
        "result_store_contract": RESULT_STORE_CONTRACT,
        "output_hash_algorithm": HASH_ALGORITHM,
        "confidence_label_counts": dict(sorted(Counter(record["confidence_label"] for record in score).items())),
        "score_status_counts": dict(sorted(Counter(record["score_status"] for record in score).items())),
        "method_impact_status_counts": dict(sorted(Counter(record["impact_status"] for record in impacts).items())),
        "generated_body_policy_status_counts": dict(sorted(Counter(record["policy_status"] for record in policies).items())),
        "controlled_expansion_status_counts": dict(
            sorted(Counter(record["candidate_status"] for record in candidates).items())
        ),
        "records_with_output_hashes": sum(1 for record in result_store if record.get("output_token_hash")),
        "per_fixture_integration": [
            {
                "fixture_id": record["fixture_id"],
                "candidate_id": record["candidate_id"],
                "source_transform_family": record["source_transform_family"],
                "output_token_hash": record["output_token_hash"],
                "integration_status": record["stage5p_integration_status"],
            }
            for record in result_store
        ],
        "generated_body_publication_allowed": False,
        "method_status_upgrade_allowed": False,
        "method_status_upgraded": False,
        "deep_research_recommended": False,
        "selected_next_stage": selected_next_stage,
        "next_stage": selected_next_stage,
        "selected_next_stage_reason": selected_next_stage_reason,
        "cuda_execution_performed": False,
        "solved_fixture_cuda_used": False,
        "additional_cuda_execution_performed": False,
        "cuda_source_modified": False,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "device_kernel_arithmetic_modified": False,
        "unsolved_page_cuda_used": False,
        "real_liber_primus_cuda_data_used": False,
        "real_liber_primus_data_used": False,
        "gpu_benchmark_performed": False,
        "performance_claim": False,
        "speedup_claim": False,
        "performance_or_speedup_claims": False,
        "broad_experiment_executed": False,
        "new_experiment_executed": False,
        "raw_data_processed": False,
        "generated_outputs_committed": False,
        "codex_output_committed": False,
        "website_expansion": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "ci_gpu_required": False,
        "no_gpu_ci_safe": True,
        "local_16gb_profile_required": False,
        "cxx_launches_python_workers": False,
        "no_solve_claim": True,
        "solve_claim": False,
    }
    write_yaml(summary_out, summary)
    write_report(out_dir, SUMMARY_REPORT, summary)
    return summary


def load_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    payload = read_yaml(summary_path)
    if not isinstance(payload, dict):
        raise ValueError(f"summary must be a mapping: {summary_path}")
    return payload
