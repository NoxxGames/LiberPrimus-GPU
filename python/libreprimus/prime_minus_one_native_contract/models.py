"""Constants for Stage 5W prime-minus-one native contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5w"
SOURCE_STAGE_ID = "stage-5v"
ABI_ID = "candidate_batch_abi_v0"
RESULT_SOURCE_KIND = "prime_minus_one_native_contract_preparation"
CONTRACT_ID = "prime_minus_one_stream_native_contract_v0"
FAMILY_ID = "prime_minus_one_stream"
P56_FIXTURE_ID = "p56-an-end-prime-minus-one"
P56_CANDIDATE_ID = "stage4o-prime-minus-one-an-v0"
P56_INPUT_STREAM_ID = "stage4o-fixture-prime-an-v0"

OUTPUT_DIR = Path("experiments/results/prime-minus-one-native-contract/stage5w")

SOURCE_INVENTORY_PATH = Path("data/cuda/stage5w-prime-minus-one-source-inventory.yaml")
STREAM_CONTRACT_PATH = Path("data/cuda/stage5w-prime-minus-one-stream-contract.yaml")
PRIME_SCHEDULE_PATH = Path("data/cuda/stage5w-prime-minus-one-schedule.yaml")
CANDIDATE_BATCH_MAPPING_PATH = Path("data/cuda/stage5w-prime-minus-one-candidate-batch-mapping.yaml")
NATIVE_PARITY_PREPARATION_PATH = Path("data/cuda/stage5w-prime-minus-one-native-parity-preparation.yaml")
RESULT_STORE_PREFLIGHT_PATH = Path("data/cuda/stage5w-prime-minus-one-result-store-preflight.yaml")
GUARDRAIL_PATH = Path("data/cuda/stage5w-prime-minus-one-guardrail.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5w-prime-minus-one-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5w-prime-minus-one-native-contract-summary.yaml")

STAGE5V_SUMMARY_PATH = Path("data/cuda/stage5v-native-candidate-batch-conformance-summary.yaml")
STAGE5U_ABI_PATH = Path("data/cuda/stage5u-candidate-batch-abi.yaml")
STAGE5U_STREAM_CONTRACT_PATH = Path("data/cuda/stage5u-stream-schedule-contract.yaml")
STAGE5L_TOKEN_MAPPING_PATH = Path("data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml")
STAGE5L_NATIVE_PARITY_PATH = Path("data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml")
STAGE5T_INVENTORY_PATH = Path("data/cuda/stage5t-solved-family-cuda-inventory.yaml")
STAGE5T_KERNEL_READINESS_PATH = Path("data/cuda/stage5t-cuda-kernel-readiness.yaml")
STAGE4O_MANIFEST_PATH = Path("experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml")
P56_FIXTURE_PATH = Path("data/fixtures/solved-pages/prime-stream-v0/p56-an-end-prime-minus-one.fixture.json")
TRANSFORM_REGISTRY_PATH = Path("data/transform-registry/cpu-reference-transforms-v0.json")

REPORT_FILES = {
    "source_inventory": "source_inventory_report.json",
    "stream_contract": "stream_contract_report.json",
    "prime_schedule": "prime_schedule_report.json",
    "candidate_batch_mapping": "candidate_batch_mapping_report.json",
    "native_parity_preparation": "native_parity_preparation_report.json",
    "result_store_preflight": "result_store_preflight_report.json",
    "guardrail": "guardrail_report.json",
    "next_stage": "next_stage_decision.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

NEXT_STAGE_TITLE_READY = "Stage 5X - prime-minus-one stream no-GPU native parity execution and result-store preflight"
NEXT_STAGE_TITLE_BLOCKED = "Stage 5X - prime-minus-one stream contract blocker closure"
NEXT_STAGE_TITLE_SYNTHETIC = "Stage 5X - prime-minus-one synthetic native parity controls"
NEXT_STAGE_REASON_READY = (
    "Stage 5W found source-backed formula direction, skip policy, stream schedule, "
    "and a committed Stage 4O/5L p56 solved-fixture-safe token mapping, so the next "
    "bounded stage can execute no-GPU native parity against compact source-backed "
    "fixtures while keeping full p56 token-buffer expansion blocked until separately scoped."
)

COMMON_FLAGS: dict[str, Any] = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "candidate_batch_abi_id": ABI_ID,
    "result_source_kind": RESULT_SOURCE_KIND,
    "metadata_only": True,
    "contract_preparation_only": True,
    "native_execution_performed": False,
    "python_reference_execution_performed": False,
    "cuda_execution_allowed": False,
    "cuda_execution_performed": False,
    "cuda_source_changes_allowed": False,
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
        "contract_preparation_only",
        "no_solve_claim",
        "no_gpu_ci_safe",
    }
)

EXPECTED_COUNTS = {
    "source_inventory_records": 7,
    "stream_contract_records": 2,
    "prime_schedule_records": 3,
    "candidate_batch_mapping_records": 3,
    "native_parity_preparation_records": 3,
    "result_store_preflight_records": 3,
    "guardrail_records": 6,
    "next_stage_decision_records": 8,
    "synthetic_control_schedule_records": 1,
    "synthetic_control_ready_count": 1,
}
