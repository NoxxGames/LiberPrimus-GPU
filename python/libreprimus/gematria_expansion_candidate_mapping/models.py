"""Constants for Stage 5Q Gematria expansion candidate mapping."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5q"
SOURCE_STAGE_ID = "stage-5p"
TARGET_KERNEL = "gematria_mod29_shift_score_kernel"
EXECUTED_SEMANTICS = "gematria_shift_score_only"
SOURCE_CONTRACT_ID = "gematria_mod29_shift_score_contract_v0"
TOKEN_DOMAIN = "integers_0_to_28"
HASH_ALGORITHM = "sha256_canonical_json_v1"
CANDIDATE_SHIFTS = [0, 1, 3, 13, 28]
OUTPUT_ORDERING = "candidate-major"
RESULT_STORE_CONTRACT = "stage4p"
SCORE_SUMMARY_CONTRACT = "stage4i"
NEXT_STAGE_READY = "Stage 5R - controlled expanded solved-fixture-safe Gematria shift_score CUDA parity run"
NEXT_STAGE_BLOCKERS = "Stage 5R - controlled solved-fixture-safe Gematria expansion blocker closure"
NEXT_STAGE_DEEP_RESEARCH = "Deep Research - Stage 5P/5Q CUDA parity integration and expansion review"

OUTPUT_DIR = Path("experiments/results/gematria-expansion-candidate-mapping/stage5q")
STAGE4O_SOLVED_FIXTURE_MANIFEST = Path("experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml")
STAGE5L_TOKEN_MAPPING = Path("data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml")
DIRECT_FIXTURE_DIR = Path("data/fixtures/solved-pages/direct-translation-v0")
ATBASH_FIXTURE_DIR = Path("data/fixtures/solved-pages/atbash-family-v0")
VIGENERE_FIXTURE_DIR = Path("data/fixtures/solved-pages/vigenere-v0")
PRIME_FIXTURE_DIR = Path("data/fixtures/solved-pages/prime-stream-v0")
STAGE4P_SUMMARY = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")
STAGE4I_CONFIDENCE_LABELS = Path("data/scoring/confidence-label-records-v0.yaml")
STAGE5P_SUMMARY = Path("data/cuda/stage5p-cuda-result-store-integration-summary.yaml")

CANDIDATE_INVENTORY_PATH = Path("data/cuda/stage5q-gematria-expansion-candidate-inventory.yaml")
TOKEN_MAPPING_PATH = Path("data/cuda/stage5q-gematria-expansion-token-mapping.yaml")
NATIVE_PARITY_PATH = Path("data/cuda/stage5q-gematria-expansion-native-parity.yaml")
RESULT_STORE_PREFLIGHT_PATH = Path("data/cuda/stage5q-gematria-expansion-result-store-preflight.yaml")
EXPANSION_GATE_PATH = Path("data/cuda/stage5q-gematria-expansion-gate.yaml")
SUMMARY_PATH = Path("data/cuda/stage5q-expansion-candidate-mapping-summary.yaml")

CANDIDATE_INVENTORY_REPORT = "candidate_inventory_report.json"
TOKEN_MAPPING_REPORT = "token_mapping_report.json"
NATIVE_PARITY_REPORT = "native_parity_report.json"
RESULT_STORE_PREFLIGHT_REPORT = "result_store_preflight_report.json"
EXPANSION_GATE_REPORT = "controlled_expansion_gate_report.json"
SUMMARY_REPORT = "summary.json"
WARNINGS_REPORT = "warnings.jsonl"

CANDIDATE_INVENTORY_SCHEMA = Path("schemas/cuda/gematria-expansion-candidate-inventory-record-v0.schema.json")
TOKEN_MAPPING_SCHEMA = Path("schemas/cuda/gematria-expansion-token-mapping-record-v0.schema.json")
NATIVE_PARITY_SCHEMA = Path("schemas/cuda/gematria-expansion-native-parity-record-v0.schema.json")
RESULT_STORE_PREFLIGHT_SCHEMA = Path("schemas/cuda/gematria-expansion-result-store-preflight-record-v0.schema.json")
EXPANSION_GATE_SCHEMA = Path("schemas/cuda/gematria-expansion-gate-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5q-expansion-candidate-mapping-summary-v0.schema.json")

COMMON_POLICY_FLAGS = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "compact_summary_only": True,
    "generated_body_publication_allowed": False,
    "generated_outputs_committed": False,
    "raw_data_processed": False,
    "codex_output_committed": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "cuda_source_modified": False,
    "device_kernel_arithmetic_modified": False,
    "cuda_execution_performed": False,
    "additional_cuda_execution_performed": False,
    "unsolved_page_cuda_used": False,
    "real_liber_primus_cuda_data_used": False,
    "real_liber_primus_data_used": False,
    "solved_fixture_cuda_used": False,
    "gpu_benchmark_performed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "performance_or_speedup_claims": False,
    "method_status_upgrade_allowed": False,
    "method_status_upgraded": False,
    "solve_claim": False,
    "no_solve_claim": True,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "no_gpu_ci_safe": True,
    "local_16gb_profile_required": False,
    "ci_gpu_required": False,
    "cxx_launches_python_workers": False,
}

BAD_TRUE_FLAGS = (
    "generated_body_publication_allowed",
    "generated_outputs_committed",
    "raw_data_processed",
    "codex_output_committed",
    "new_cuda_kernel_added",
    "cuda_source_modified",
    "device_kernel_arithmetic_modified",
    "cuda_execution_performed",
    "additional_cuda_execution_performed",
    "unsolved_page_cuda_used",
    "real_liber_primus_cuda_data_used",
    "real_liber_primus_data_used",
    "solved_fixture_cuda_used",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "performance_or_speedup_claims",
    "method_status_upgrade_allowed",
    "method_status_upgraded",
    "solve_claim",
    "canonical_corpus_active",
    "page_boundaries_final",
    "local_16gb_profile_required",
    "ci_gpu_required",
    "cxx_launches_python_workers",
)

REQUIRED_TRUE_FLAGS = ("compact_summary_only", "no_solve_claim", "no_gpu_ci_safe")
