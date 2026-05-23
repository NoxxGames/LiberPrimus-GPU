"""Constants for Stage 5AD-fix bounded p56 mismatch records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5ad-fix"
SOURCE_STAGE_ID = "stage-5ad"
SOURCE_NATIVE_STAGE_ID = "stage-5x"
SOURCE_CONTRACT_STAGE_ID = "stage-5w"
SOURCE_TOKEN_MAPPING_STAGE_ID = "stage-5l"
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
NATIVE_PARITY_ID = "stage5l-native-parity-04"
FIXTURE_ID = "p56-an-end-prime-minus-one"
CANDIDATE_ID = "stage4o-prime-minus-one-an-v0"
STREAM_SCHEDULE_REF = "stage5w-p56-stage4o-bounded-prime-minus-one-schedule-v0"
STAGE5AD_EXPECTED_HASH = "4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87"
STAGE5AD_COMPUTED_CUDA_HASH = "6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387"
STAGE5X_FORMULA_HASH = STAGE5AD_COMPUTED_CUDA_HASH
SOURCE_SYNTHETIC_HASH = "06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab"

INPUT_TOKENS = [
    {"position": 0, "token_kind": "rune", "transformable": True, "index29": 25, "raw_text": None},
    {"position": 1, "token_kind": "rune", "transformable": True, "index29": 11, "raw_text": None},
]
FORMULA_OUTPUT_TOKENS = [
    {"position": 0, "token_kind": "rune", "transformable": True, "index29": 24, "raw_text": None},
    {"position": 1, "token_kind": "rune", "transformable": True, "index29": 9, "raw_text": None},
]
STAGE5L_CANDIDATE_MAJOR_LAST_OUTPUT_TOKENS = [
    {"position": 0, "token_kind": "rune", "transformable": True, "index29": 24, "raw_text": None},
    {"position": 1, "token_kind": "rune", "transformable": True, "index29": 10, "raw_text": None},
]
STREAM_VALUES_USED = [1, 2]
FIRST_PRIMES_USED = [2, 3]

OUTPUT_DIR = Path("experiments/results/prime-minus-one-bounded-p56-mismatch/stage5ad-fix")
HASH_LINEAGE_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-hash-lineage.yaml")
TOKEN_TRACE_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-token-trace.yaml")
STREAM_TRACE_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-stream-trace.yaml")
FORMULA_TRACE_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-formula-trace.yaml")
HASH_MATERIAL_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-hash-material.yaml")
REFERENCE_CONTRACT_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-reference-contract.yaml")
ROOT_CAUSE_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-root-cause.yaml")
REPAIR_READINESS_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-repair-readiness.yaml")
GUARDRAIL_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-guardrail.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-summary.yaml")

REPORT_FILES = {
    "hash_lineage": "hash_lineage_report.json",
    "token_trace": "token_trace_report.json",
    "stream_trace": "stream_trace_report.json",
    "formula_trace": "formula_trace_report.json",
    "hash_material": "hash_material_trace_report.json",
    "reference_contract": "reference_contract_report.json",
    "root_cause": "root_cause_report.json",
    "repair_readiness": "repair_readiness_report.json",
    "guardrail": "guardrail_report.json",
    "next_stage": "next_stage_decision.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

EXPECTED_COUNTS = {
    "hash_lineage_records": 3,
    "token_trace_records": 1,
    "stream_trace_records": 1,
    "formula_trace_records": 1,
    "hash_material_records": 2,
    "reference_contract_records": 1,
    "root_cause_records": 4,
    "repair_readiness_records": 3,
    "guardrail_records": 1,
    "next_stage_decision_records": 11,
}

COMMON_FALSE_FLAGS: dict[str, Any] = {
    "bounded_p56_cuda_executed": False,
    "cuda_execution_performed": False,
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
    "ci_gpu_required": False,
    "local_16gb_profile_required": False,
    "cxx_launches_python_workers": False,
}

COMMON_RECORD_FLAGS: dict[str, Any] = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "source_native_stage_id": SOURCE_NATIVE_STAGE_ID,
    "source_contract_stage_id": SOURCE_CONTRACT_STAGE_ID,
    "source_token_mapping_stage_id": SOURCE_TOKEN_MAPPING_STAGE_ID,
    "source_cuda_contract_stage_id": SOURCE_CUDA_CONTRACT_STAGE_ID,
    "source_synthetic_stage_id": SOURCE_SYNTHETIC_STAGE_ID,
    "candidate_batch_abi_id": ABI_ID,
    "cuda_contract_id": CUDA_CONTRACT_ID,
    "kernel_id": KERNEL_ID,
    "kernel_entrypoint": KERNEL_ENTRYPOINT,
    "validation_vector_id": VALIDATION_VECTOR_ID,
    "mapping_id": MAPPING_ID,
    "fixture_id": FIXTURE_ID,
    "candidate_id": CANDIDATE_ID,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "device_kernel_arithmetic_modified": False,
    "no_solve_claim": True,
    "no_gpu_ci_safe": True,
    **COMMON_FALSE_FLAGS,
}

RECOMMENDED_NEXT_OPTION_ID = "stage5ae_corrected_bounded_p56_cuda_formula_parity_reporting"
RECOMMENDED_NEXT_STAGE_TITLE = "Stage 5AE - corrected bounded p56 CUDA formula parity reporting and reference-contract repair"


def base_record(record_type: str, schema: str, **extra: Any) -> dict[str, Any]:
    """Return a Stage 5AD-fix record with shared guardrails."""

    return {
        **COMMON_RECORD_FLAGS,
        "record_type": record_type,
        "schema": schema,
        **extra,
    }
