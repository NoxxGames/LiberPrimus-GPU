"""Constants for Stage 5U Candidate Batch ABI records."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5u"
SOURCE_STAGE_ID = "stage-5t"
ABI_ID = "candidate_batch_abi_v0"
ABI_VERSION = 0
RESULT_SOURCE_KIND = "cuda_candidate_batch_abi_contract"

OUTPUT_DIR = Path("experiments/results/cuda-candidate-batch-abi/stage5u")

STAGE5T_GAPS = Path("data/cuda/stage5t-cuda-candidate-batch-abi-gaps.yaml")
STAGE5T_SUMMARY = Path("data/cuda/stage5t-cuda-solved-family-readiness-summary.yaml")
STAGE5T_KERNEL_READINESS = Path("data/cuda/stage5t-cuda-kernel-readiness.yaml")
STAGE4P_SUMMARY = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")
STAGE4I_SCORING_DIR = Path("data/scoring")

CANDIDATE_BATCH_ABI_PATH = Path("data/cuda/stage5u-candidate-batch-abi.yaml")
TOKEN_BUFFER_CONTRACT_PATH = Path("data/cuda/stage5u-token-buffer-contract.yaml")
TRANSFORM_PARAMETER_CONTRACT_PATH = Path("data/cuda/stage5u-transform-parameter-contract.yaml")
KEY_SCHEDULE_CONTRACT_PATH = Path("data/cuda/stage5u-key-schedule-contract.yaml")
STREAM_SCHEDULE_CONTRACT_PATH = Path("data/cuda/stage5u-stream-schedule-contract.yaml")
SCORE_VECTOR_CONTRACT_PATH = Path("data/cuda/stage5u-score-vector-contract.yaml")
TOPK_OUTPUT_CONTRACT_PATH = Path("data/cuda/stage5u-topk-output-contract.yaml")
BACKEND_SURFACE_CONTRACT_PATH = Path("data/cuda/stage5u-backend-surface-contract.yaml")
RESULT_STORE_COMPATIBILITY_PATH = Path("data/cuda/stage5u-result-store-compatibility.yaml")
ABI_GAP_CLOSURE_PATH = Path("data/cuda/stage5u-abi-gap-closure.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5u-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5u-candidate-batch-abi-summary.yaml")

CANDIDATE_BATCH_ABI_REPORT_JSON = "candidate_batch_abi_report.json"
TOKEN_BUFFER_REPORT_JSON = "token_buffer_contract_report.json"
TRANSFORM_PARAMETER_REPORT_JSON = "transform_parameter_contract_report.json"
KEY_SCHEDULE_REPORT_JSON = "key_schedule_contract_report.json"
STREAM_SCHEDULE_REPORT_JSON = "stream_schedule_contract_report.json"
SCORE_VECTOR_REPORT_JSON = "score_vector_contract_report.json"
TOPK_REPORT_JSON = "topk_contract_report.json"
BACKEND_REPORT_JSON = "backend_contract_report.json"
RESULT_STORE_REPORT_JSON = "result_store_compatibility_report.json"
GAP_CLOSURE_REPORT_JSON = "gap_closure_report.json"
NEXT_STAGE_DECISION_JSON = "next_stage_decision.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

NEXT_STAGE_TITLE = "Stage 5V - native candidate batch ABI reference adapter and conformance fixtures"
NEXT_STAGE_REASON = (
    "Stage 5U is contract-only, so a no-GPU native reference adapter and conformance fixture pack "
    "should prove Candidate Batch ABI v0 semantics before family-specific CUDA contracts or benchmarks."
)

COMMON_FLAGS = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "abi_id": ABI_ID,
    "abi_version": ABI_VERSION,
    "result_source_kind": RESULT_SOURCE_KIND,
    "metadata_only": True,
    "contract_only": True,
    "compact_summary_only": True,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "device_kernel_arithmetic_modified": False,
    "gpu_benchmark_performed": False,
    "benchmark_execution_allowed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "unsolved_page_cuda_used": False,
    "unsolved_page_cuda_allowed": False,
    "real_liber_primus_cuda_data_used": False,
    "solved_fixture_cuda_used": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "generated_body_publication_allowed": False,
    "generated_outputs_committed": False,
    "raw_data_processed": False,
    "codex_output_committed": False,
    "method_status_upgrade_allowed": False,
    "method_status_upgraded": False,
    "solve_claim": False,
    "no_solve_claim": True,
    "no_gpu_ci_safe": True,
    "ci_gpu_required": False,
    "local_16gb_profile_required": False,
    "cxx_launches_python_workers": False,
}

BAD_TRUE_FLAGS = tuple(
    key
    for key, value in COMMON_FLAGS.items()
    if value is False
    and key
    not in {
        "metadata_only",
        "contract_only",
        "compact_summary_only",
        "no_solve_claim",
        "no_gpu_ci_safe",
    }
)

EXPECTED_COUNTS = {
    "candidate_batch_abi_records": 1,
    "token_buffer_contract_records": 8,
    "transform_parameter_contract_records": 6,
    "key_schedule_contract_records": 2,
    "stream_schedule_contract_records": 2,
    "score_vector_contract_records": 7,
    "topk_output_contract_records": 1,
    "backend_surface_contract_records": 7,
    "result_store_compatibility_records": 3,
    "abi_gap_closure_records": 5,
    "next_stage_decision_records": 9,
}
