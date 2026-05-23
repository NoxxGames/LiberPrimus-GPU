"""Build the committed Stage 5AD-fix summary."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json_report, write_summary, write_warnings
from .models import (
    EXPECTED_COUNTS,
    FIXTURE_ID,
    GUARDRAIL_PATH,
    HASH_LINEAGE_PATH,
    HASH_MATERIAL_PATH,
    KERNEL_ID,
    MAPPING_ID,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    RECOMMENDED_NEXT_OPTION_ID,
    RECOMMENDED_NEXT_STAGE_TITLE,
    REFERENCE_CONTRACT_PATH,
    REPAIR_READINESS_PATH,
    REPORT_FILES,
    ROOT_CAUSE_PATH,
    SOURCE_SYNTHETIC_HASH,
    STAGE5AD_COMPUTED_CUDA_HASH,
    STAGE5AD_EXPECTED_HASH,
    STAGE5X_FORMULA_HASH,
    SUMMARY_PATH,
    TOKEN_MAPPING_ID,
    TOKEN_TRACE_PATH,
    STREAM_TRACE_PATH,
    FORMULA_TRACE_PATH,
    VALIDATION_VECTOR_ID,
)


def build_summary(
    *,
    hash_lineage: Path = HASH_LINEAGE_PATH,
    token_trace: Path = TOKEN_TRACE_PATH,
    stream_trace: Path = STREAM_TRACE_PATH,
    formula_trace: Path = FORMULA_TRACE_PATH,
    hash_material: Path = HASH_MATERIAL_PATH,
    reference_contract: Path = REFERENCE_CONTRACT_PATH,
    root_cause: Path = ROOT_CAUSE_PATH,
    repair_readiness: Path = REPAIR_READINESS_PATH,
    guardrail: Path = GUARDRAIL_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    groups = {
        "hash_lineage_records": read_records(hash_lineage),
        "token_trace_records": read_records(token_trace),
        "stream_trace_records": read_records(stream_trace),
        "formula_trace_records": read_records(formula_trace),
        "hash_material_records": read_records(hash_material),
        "reference_contract_records": read_records(reference_contract),
        "root_cause_records": read_records(root_cause),
        "repair_readiness_records": read_records(repair_readiness),
        "guardrail_records": read_records(guardrail),
        "next_stage_decision_records": read_records(next_stage_decision),
    }
    root = next(record for record in groups["root_cause_records"] if record.get("primary_root_cause") is True)
    decision = next(record for record in groups["next_stage_decision_records"] if record.get("selected") is True)
    reference = groups["reference_contract_records"][0]
    formula = groups["formula_trace_records"][0]
    summary: dict[str, Any] = {
        "record_type": "stage5ad_fix_bounded_p56_mismatch_summary",
        "schema": "schemas/cuda/stage5ad-fix-bounded-p56-mismatch-summary-v0.schema.json",
        "stage_id": "stage-5ad-fix",
        "status": "complete",
        "source_stage_id": "stage-5ad",
        "source_native_stage_id": "stage-5x",
        "source_contract_stage_id": "stage-5w",
        "source_token_mapping_stage_id": "stage-5l",
        "source_synthetic_stage_id": "stage-5aa",
        "candidate_batch_abi_id": "candidate_batch_abi_v0",
        "cuda_contract_id": "prime_minus_one_stream_cuda_contract_v0",
        "kernel_id": KERNEL_ID,
        "bounded_p56_vector_id": VALIDATION_VECTOR_ID,
        "mapping_id": MAPPING_ID,
        "token_mapping_id": TOKEN_MAPPING_ID,
        "fixture_id": FIXTURE_ID,
        "candidate_id": "stage4o-prime-minus-one-an-v0",
        "stage5ad_expected_hash": STAGE5AD_EXPECTED_HASH,
        "stage5ad_computed_cuda_hash": STAGE5AD_COMPUTED_CUDA_HASH,
        "stage5x_formula_hash": STAGE5X_FORMULA_HASH,
        "stage5aa_synthetic_reference_hash": SOURCE_SYNTHETIC_HASH,
        "primary_root_cause": root["cause_id"],
        "root_cause_confidence": root["confidence"],
        "cuda_formula_matches_stage5x_formula": reference["cuda_formula_matches_stage5x_formula"],
        "cuda_formula_matches_stage5w_expected": reference["cuda_formula_matches_stage5w_expected"],
        "reference_contract_repair_required": reference["reference_contract_repair_required"],
        "cuda_kernel_repair_required": reference["cuda_kernel_repair_required"],
        "hash_material_policy_repair_required": reference["hash_material_policy_repair_required"],
        "stage5ad_historical_failure_preserved": True,
        "recommended_next_option_id": decision["option_id"],
        "recommended_next_stage_title": decision["recommended_stage_title"],
        "recommended_next_prompt_type": decision["recommended_prompt_type"],
        "recommended_next_stage_reason": decision["rationale"],
        "deep_research_recommended_next": False,
        "bounded_p56_cuda_executed": False,
        "cuda_execution_performed": False,
        "python_reference_execution_performed": formula["python_reference_execution_performed"],
        "full_p56_cuda_executed": False,
        "full_p56_cuda_allowed": False,
        "unsolved_page_cuda_used": False,
        "unsolved_page_cuda_allowed": False,
        "real_liber_primus_cuda_data_used": False,
        "raw_data_processed": False,
        "gpu_benchmark_performed": False,
        "benchmark_execution_allowed": False,
        "performance_claim": False,
        "speedup_claim": False,
        "scored_experiment_executed": False,
        "scored_experiment_execution_allowed": False,
        "website_expansion_performed": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_body_publication_allowed": False,
        "generated_outputs_committed": False,
        "codex_output_committed": False,
        "method_status_upgrade_allowed": False,
        "method_status_upgraded": False,
        "solve_claim": False,
        "no_solve_claim": True,
        "cuda_source_modified": False,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "device_kernel_arithmetic_modified": False,
        "ci_gpu_required": False,
        "local_16gb_profile_required": False,
        "cxx_launches_python_workers": False,
        "no_gpu_ci_safe": True,
        "next_stage_decision_is_corrected_reporting": decision["option_id"] == RECOMMENDED_NEXT_OPTION_ID,
    }
    for key, records in groups.items():
        summary[key] = len(records)
    for key, expected in EXPECTED_COUNTS.items():
        summary.setdefault(key, expected)
    write_summary(summary_out, summary)
    write_json_report(out_dir, REPORT_FILES["summary"], summary)
    write_warnings(out_dir, ["stage5ad_expected_hash_reference_contract_requires_repair"])
    if summary["recommended_next_stage_title"] != RECOMMENDED_NEXT_STAGE_TITLE:
        raise ValueError("Stage 5AD-fix selected an unexpected next stage.")
    return summary
