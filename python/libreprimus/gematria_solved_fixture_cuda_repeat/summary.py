"""Build and print Stage 5O repeat-verification summaries."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.gematria_solved_fixture_cuda_repeat.export import read_record_set, write_report, write_warnings
from libreprimus.gematria_solved_fixture_cuda_repeat.models import (
    EXPANSION_DECISION_PATH,
    HASH_ALGORITHM,
    OUTPUT_DIR,
    REPEAT_PARITY_PATH,
    REPEAT_RUN_PATH,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORE_SUMMARY_CONTRACT,
    SCORE_SUMMARY_PREFLIGHT_PATH,
    STAGE5M_SUMMARY,
    STAGE5N_SUMMARY,
    SUMMARY_PATH,
    SUMMARY_REPORT,
)


def build_summary(
    *,
    repeat_run_records: Path = REPEAT_RUN_PATH,
    repeat_parity_records: Path = REPEAT_PARITY_PATH,
    result_store_preflight: Path = RESULT_STORE_PREFLIGHT_PATH,
    score_summary_preflight: Path = SCORE_SUMMARY_PREFLIGHT_PATH,
    expansion_decision: Path = EXPANSION_DECISION_PATH,
    stage5m_summary: Path = STAGE5M_SUMMARY,
    stage5n_summary: Path = STAGE5N_SUMMARY,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    runs = read_record_set(repeat_run_records)
    parity = read_record_set(repeat_parity_records)
    result_store = read_record_set(result_store_preflight)
    score = read_record_set(score_summary_preflight)
    decisions = read_record_set(expansion_decision)
    stage5m = read_yaml(stage5m_summary)
    stage5n = read_yaml(stage5n_summary)
    pass_count = sum(1 for record in parity if record["repeat_parity_status"] == "passed")
    fail_count = sum(1 for record in parity if str(record["repeat_parity_status"]).startswith("failed"))
    skip_count = len(parity) - pass_count - fail_count
    attempted_count = sum(1 for record in runs if record.get("repeat_cuda_attempted") is True)
    decision = decisions[0]
    summary = {
        "record_type": "stage5o_repeat_verification_result_store_summary",
        "stage_id": "stage-5o",
        "status": "complete",
        "implemented_kernel_name": "gematria_mod29_shift_score_kernel",
        "executed_kernel": "gematria_mod29_shift_score_kernel",
        "source_contract_id": "gematria_mod29_shift_score_contract_v0",
        "executed_semantics": "gematria_shift_score_only",
        "stage5m_run_records": int(stage5m["run_records"]),
        "stage5m_parity_pass_count": int(stage5m["parity_pass_count"]),
        "stage5n_gate_next_stage": stage5n.get("selected_next_stage"),
        "repeat_run_records": len(runs),
        "repeat_cuda_attempted_count": attempted_count,
        "repeat_cuda_pass_count": pass_count,
        "repeat_cuda_fail_count": fail_count,
        "repeat_cuda_skip_count": skip_count,
        "repeat_parity_records": len(parity),
        "repeat_parity_pass_count": pass_count,
        "repeat_parity_fail_count": fail_count,
        "repeat_parity_skip_count": skip_count,
        "stage5l_native_hash_match_count": sum(1 for record in parity if record.get("stage5l_native_hash_match") is True),
        "stage5m_cuda_hash_match_count": sum(1 for record in parity if record.get("stage5m_cuda_hash_match") is True),
        "result_store_preflight_records": len(result_store),
        "result_store_preflight_ready_count": sum(1 for record in result_store if record.get("stage5p_ready") is True),
        "score_summary_preflight_records": len(score),
        "score_summary_preflight_ready_count": sum(1 for record in score if record.get("stage5p_ready") is True),
        "expansion_decision_records": len(decisions),
        "expansion_decision_status_counts": dict(sorted(Counter(record["decision_status"] for record in decisions).items())),
        "result_store_preflight_status_counts": dict(sorted(Counter(record["preflight_status"] for record in result_store).items())),
        "score_summary_shape_status_counts": dict(sorted(Counter(record["score_summary_shape_status"] for record in score).items())),
        "stage5p_ready": decision.get("stage5p_ready") is True,
        "selected_next_stage": decision["selected_next_stage"],
        "next_stage": decision["selected_next_stage"],
        "selected_next_stage_reason": decision["selected_next_stage_reason"],
        "remaining_blockers": decision["remaining_blockers"],
        "output_hash_algorithm": HASH_ALGORITHM,
        "score_summary_contract": SCORE_SUMMARY_CONTRACT,
        "per_fixture_repeat_parity": [
            {
                "mapping_id": record["mapping_id"],
                "fixture_id": record["fixture_id"],
                "stage5l_native_hash": record["expected_native_output_token_hash"],
                "stage5m_cuda_hash": record["stage5m_cuda_output_token_hash"],
                "stage5o_repeat_cuda_hash": record["stage5o_repeat_cuda_output_token_hash"],
                "status": record["repeat_parity_status"],
            }
            for record in parity
        ],
        "solved_fixture_cuda_execution_allowed": True,
        "solved_fixture_cuda_execution_scope": "exact_stage5l_mapped_token_buffers_only",
        "additional_cuda_execution_scope": "exact_stage5m_repeat_only",
        "cuda_execution_performed": attempted_count > 0,
        "solved_fixture_cuda_used": attempted_count > 0,
        "additional_cuda_execution_performed": attempted_count > 0,
        "unsolved_page_cuda_used": False,
        "real_liber_primus_cuda_data_used": False,
        "real_liber_primus_data_used": False,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "cuda_source_modified": False,
        "device_kernel_arithmetic_modified": False,
        "gpu_benchmark_performed": False,
        "performance_claim": False,
        "speedup_claim": False,
        "performance_or_speedup_claims": False,
        "broad_experiment_executed": False,
        "raw_data_processed": False,
        "generated_outputs_committed": False,
        "codex_output_committed": False,
        "website_expansion": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "ci_gpu_required": False,
        "no_gpu_ci_safe": True,
        "cxx_launches_python_workers": False,
        "no_solve_claim": True,
        "solve_claim": False,
    }
    write_yaml(summary_out, summary)
    write_report(out_dir, SUMMARY_REPORT, summary)
    write_warnings(out_dir, [])
    return summary


def load_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    payload = read_yaml(summary_path)
    if not isinstance(payload, dict):
        raise ValueError(f"summary must be a mapping: {summary_path}")
    return payload
