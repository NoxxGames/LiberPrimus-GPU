"""Constants for Stage 5AE corrected bounded p56 reporting."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5ae"
SOURCE_STAGE_ID = "stage-5ad-fix"
HISTORICAL_FAILED_STAGE_ID = "stage-5ad"
SOURCE_FORMULA_STAGE_ID = "stage-5x"
SOURCE_REFERENCE_STAGE_ID = "stage-5l"
SOURCE_CONTRACT_STAGE_ID = "stage-5w"
SOURCE_CUDA_CONTRACT_STAGE_ID = "stage-5z"
SOURCE_SYNTHETIC_STAGE_ID = "stage-5aa"

ABI_ID = "candidate_batch_abi_v0"
CUDA_CONTRACT_ID = "prime_minus_one_stream_cuda_contract_v0"
KERNEL_ID = "prime_minus_one_stream_cuda_kernel_v0"
KERNEL_ENTRYPOINT = "prime_minus_one_stream_kernel_v0"
HASH_ALGORITHM = "sha256_canonical_json_v1"

VALIDATION_VECTOR_ID = "stage5z-validation-p56-bounded-v0"
MAPPING_ID = "stage5w-mapping-p56-stage4o-bounded-v0"
TOKEN_MAPPING_ID = "stage5l-token-mapping-04"
FIXTURE_ID = "p56-an-end-prime-minus-one"
CANDIDATE_ID = "stage4o-prime-minus-one-an-v0"

HISTORICAL_EXPECTED_HASH = "4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87"
HISTORICAL_COMPUTED_CUDA_HASH = "6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387"
CORRECTED_FORMULA_HASH = HISTORICAL_COMPUTED_CUDA_HASH
SYNTHETIC_CONTROL_HASH = "06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab"

INPUT_TOKENS = [
    {"position": 0, "token_kind": "rune", "transformable": True, "index29": 25, "raw_text": None},
    {"position": 1, "token_kind": "rune", "transformable": True, "index29": 11, "raw_text": None},
]
FORMULA_OUTPUT_TOKENS = [
    {"position": 0, "token_kind": "rune", "transformable": True, "index29": 24, "raw_text": None},
    {"position": 1, "token_kind": "rune", "transformable": True, "index29": 9, "raw_text": None},
]
REFERENCE_OUTPUT_TAIL = [
    {"position": 0, "token_kind": "rune", "transformable": True, "index29": 24, "raw_text": None},
    {"position": 1, "token_kind": "rune", "transformable": True, "index29": 10, "raw_text": None},
]
STREAM_VALUES_USED = [1, 2]

SOURCE_SUMMARY_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-summary.yaml")
OUTPUT_DIR = Path("experiments/results/prime-minus-one-bounded-p56-corrected-reporting/stage5ae")

FORMULA_PARITY_REPORT_PATH = Path("data/cuda/stage5ae-corrected-bounded-p56-formula-parity-report.yaml")
REFERENCE_CONTRACT_REPAIR_PATH = Path("data/cuda/stage5ae-bounded-p56-reference-contract-repair.yaml")
HASH_MATERIAL_POLICY_PATH = Path("data/cuda/stage5ae-hash-material-policy.yaml")
RESULT_STORE_INTEGRATION_PATH = Path("data/cuda/stage5ae-corrected-bounded-p56-result-store-integration.yaml")
SCORE_SUMMARY_INTEGRATION_PATH = Path("data/cuda/stage5ae-corrected-bounded-p56-score-summary-integration.yaml")
METHOD_STATUS_IMPACT_PATH = Path("data/cuda/stage5ae-corrected-bounded-p56-method-status-impact.yaml")
GENERATED_BODY_POLICY_PATH = Path("data/cuda/stage5ae-corrected-bounded-p56-generated-body-policy.yaml")
FULL_P56_BLOCKER_PATH = Path("data/cuda/stage5ae-corrected-bounded-p56-full-p56-blocker.yaml")
SCORED_EXPERIMENT_DEFERRAL_PATH = Path("data/cuda/stage5ae-corrected-bounded-p56-scored-experiment-deferral.yaml")
ARCHIVE_SOURCE_LOCK_DEFERRAL_PATH = Path("data/cuda/stage5ae-archive-source-lock-deferral.yaml")
DOC_STALENESS_VALIDATION_PATH = Path("data/cuda/stage5ae-corrected-bounded-p56-doc-staleness-validation.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5ae-corrected-bounded-p56-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5ae-corrected-bounded-p56-reporting-summary.yaml")

REPORT_FILES = {
    "formula_parity": "corrected_formula_parity_report.json",
    "reference_contract": "reference_contract_repair_report.json",
    "hash_material": "hash_material_policy_report.json",
    "result_store": "result_store_integration_report.json",
    "score_summary": "score_summary_integration_report.json",
    "method_status": "method_status_impact_report.json",
    "generated_body": "generated_body_policy_report.json",
    "full_p56": "full_p56_blocker_report.json",
    "scored_experiment": "scored_experiment_deferral_report.json",
    "archive_source_lock": "archive_source_lock_deferral_report.json",
    "doc_staleness": "doc_staleness_validation_report.json",
    "next_stage": "next_stage_decision_report.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

EXPECTED_COUNTS = {
    "corrected_formula_parity_report_records": 1,
    "reference_contract_repair_records": 3,
    "hash_material_policy_records": 3,
    "result_store_integration_records": 1,
    "score_summary_integration_records": 1,
    "method_status_impact_records": 1,
    "generated_body_policy_records": 1,
    "full_p56_blocker_records": 1,
    "scored_experiment_deferral_records": 1,
    "archive_source_lock_deferral_records": 3,
    "doc_staleness_validation_records": 1,
    "next_stage_decision_records": 8,
}

COMMON_FALSE_FLAGS: dict[str, Any] = {
    "cuda_execution_performed": False,
    "bounded_p56_cuda_executed": False,
    "full_p56_cuda_executed": False,
    "full_p56_cuda_allowed": False,
    "unsolved_page_cuda_used": False,
    "unsolved_page_cuda_allowed": False,
    "real_liber_primus_cuda_data_used": False,
    "raw_data_processed": False,
    "archive_raw_data_processed": False,
    "native_execution_performed": False,
    "python_reference_execution_performed": False,
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
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "device_kernel_arithmetic_modified": False,
    "ci_gpu_required": False,
    "local_16gb_profile_required": False,
    "cxx_launches_python_workers": False,
}

COMMON_RECORD_FLAGS: dict[str, Any] = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "historical_failed_stage_id": HISTORICAL_FAILED_STAGE_ID,
    "source_formula_stage_id": SOURCE_FORMULA_STAGE_ID,
    "source_reference_stage_id": SOURCE_REFERENCE_STAGE_ID,
    "source_contract_stage_id": SOURCE_CONTRACT_STAGE_ID,
    "source_cuda_contract_stage_id": SOURCE_CUDA_CONTRACT_STAGE_ID,
    "source_synthetic_stage_id": SOURCE_SYNTHETIC_STAGE_ID,
    "candidate_batch_abi_id": ABI_ID,
    "cuda_contract_id": CUDA_CONTRACT_ID,
    "kernel_id": KERNEL_ID,
    "kernel_entrypoint": KERNEL_ENTRYPOINT,
    "bounded_p56_vector_id": VALIDATION_VECTOR_ID,
    "mapping_id": MAPPING_ID,
    "fixture_id": FIXTURE_ID,
    "candidate_id": CANDIDATE_ID,
    "token_mapping_id": TOKEN_MAPPING_ID,
    "stage5ad_historical_failure_preserved": True,
    "historical_stage5ad_status": "failed_hash_mismatch",
    "historical_stage5ad_reclassified_as_passed": False,
    "new_cuda_kernels_added": 0,
    "no_solve_claim": True,
    "no_gpu_ci_safe": True,
    **COMMON_FALSE_FLAGS,
}

SELECTED_NEXT_OPTION_ID = "stage5af_archive_visual_numeric_source_lock"
SELECTED_NEXT_STAGE_TITLE = "Stage 5AF - archive visual numeric source-lock and provenance inventory"
SELECTED_NEXT_STAGE_REASON = (
    "Stage 5AE completes the bounded p56 formula reporting repair; the next safe work is "
    "source-lock/provenance inventory for archive, visual, numeric, and stego leads without execution."
)


def base_record(record_type: str, schema: str, **extra: Any) -> dict[str, Any]:
    """Return a Stage 5AE record with shared guardrails."""

    return {
        **COMMON_RECORD_FLAGS,
        "record_type": record_type,
        "schema": schema,
        **extra,
    }
