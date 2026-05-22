"""Constants for Stage 5V native Candidate Batch ABI conformance records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5v"
SOURCE_STAGE_ID = "stage-5u"
ABI_ID = "candidate_batch_abi_v0"
ABI_VERSION = 0
RESULT_SOURCE_KIND = "native_candidate_batch_abi_conformance"

OUTPUT_DIR = Path("experiments/results/cuda-candidate-batch-abi-conformance/stage5v")

STAGE5U_SUMMARY = Path("data/cuda/stage5u-candidate-batch-abi-summary.yaml")
STAGE5U_ABI = Path("data/cuda/stage5u-candidate-batch-abi.yaml")
STAGE5U_TOKEN_BUFFER = Path("data/cuda/stage5u-token-buffer-contract.yaml")
STAGE5U_KEY_SCHEDULE = Path("data/cuda/stage5u-key-schedule-contract.yaml")
STAGE5U_STREAM_SCHEDULE = Path("data/cuda/stage5u-stream-schedule-contract.yaml")
STAGE5U_SCORE_VECTOR = Path("data/cuda/stage5u-score-vector-contract.yaml")
STAGE5U_TOPK = Path("data/cuda/stage5u-topk-output-contract.yaml")
STAGE5U_GAP_CLOSURE = Path("data/cuda/stage5u-abi-gap-closure.yaml")
STAGE4I_SCORING_DIR = Path("data/scoring")
STAGE4P_SUMMARY = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")

ADAPTER_RECORDS_PATH = Path("data/cuda/stage5v-native-candidate-batch-adapter.yaml")
CONFORMANCE_FIXTURES_PATH = Path("data/cuda/stage5v-candidate-batch-conformance-fixtures.yaml")
TOKEN_BUFFER_CONFORMANCE_PATH = Path("data/cuda/stage5v-token-buffer-conformance.yaml")
SCHEDULE_CONFORMANCE_PATH = Path("data/cuda/stage5v-schedule-conformance.yaml")
SCORE_VECTOR_CONFORMANCE_PATH = Path("data/cuda/stage5v-score-vector-conformance.yaml")
TOPK_CONFORMANCE_PATH = Path("data/cuda/stage5v-topk-conformance.yaml")
RESULT_STORE_CONFORMANCE_PATH = Path("data/cuda/stage5v-native-conformance-result-store.yaml")
IMPLEMENTATION_STATUS_PATH = Path("data/cuda/stage5v-abi-implementation-status.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5v-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5v-native-candidate-batch-conformance-summary.yaml")

REPORT_FILES = {
    "native_adapter": "native_adapter_report.json",
    "conformance_fixture": "conformance_fixture_report.json",
    "token_buffer": "token_buffer_conformance_report.json",
    "schedule": "schedule_conformance_report.json",
    "score_vector": "score_vector_conformance_report.json",
    "topk": "topk_conformance_report.json",
    "result_store": "result_store_conformance_report.json",
    "gap_closure": "gap_closure_report.json",
    "next_stage": "next_stage_decision.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

NEXT_STAGE_TITLE = "Stage 5W - prime-minus-one stream native parity contract preparation"
NEXT_STAGE_REASON = (
    "Stage 5V proves token-buffer, score-vector, top-k, and stream-schedule shape "
    "conformance without CUDA, so the next bounded native contract should prepare the "
    "prime-minus-one stream family before any family-specific CUDA contract."
)

COMMON_FLAGS: dict[str, Any] = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "candidate_batch_abi_id": ABI_ID,
    "candidate_batch_abi_version": ABI_VERSION,
    "result_source_kind": RESULT_SOURCE_KIND,
    "metadata_only": False,
    "contract_only": False,
    "compact_summary_only": True,
    "native_cpu_execution_performed": False,
    "python_reference_adapter_implemented": True,
    "cpp_reference_adapter_implemented": False,
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
        "python_reference_adapter_implemented",
        "cpp_reference_adapter_implemented",
        "no_solve_claim",
        "no_gpu_ci_safe",
    }
)

EXPECTED_COUNTS = {
    "native_adapter_records": 2,
    "conformance_fixture_records": 7,
    "token_buffer_conformance_records": 7,
    "schedule_conformance_records": 2,
    "score_vector_conformance_records": 7,
    "topk_conformance_records": 1,
    "result_store_conformance_records": 3,
    "abi_implementation_status_records": 8,
    "next_stage_decision_records": 9,
    "stage5u_gap_count": 5,
    "native_conformance_pass_count": 4,
    "native_conformance_shape_only_count": 2,
    "native_conformance_blocked_count": 2,
    "executed_conformance_fixture_count": 3,
    "output_hash_records": 3,
}
