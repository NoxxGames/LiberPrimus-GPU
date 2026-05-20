"""Constants for Stage 5D native CPU backend records."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5d"
BACKEND_ID = "stage5d-native-cpu-backend-v0"
FIXTURE_ID = "stage5d-native-synthetic-shift-fixture-v0"

OUTPUT_DIR = Path("experiments/results/native-cpu/stage5d")
CAPABILITIES_PATH = Path("data/native-cpu/stage5d-native-cpu-backend-capabilities.yaml")
THREADING_PATH = Path("data/native-cpu/stage5d-native-cpu-threading-records.yaml")
PARITY_PATH = Path("data/native-cpu/stage5d-native-cpu-parity-records.yaml")
DIAGNOSTICS_PATH = Path("data/native-cpu/stage5d-native-cpu-diagnostic-records.yaml")
SUMMARY_PATH = Path("data/native-cpu/stage5d-native-cpu-summary.yaml")

CAPABILITY_SCHEMA = Path("schemas/native-cpu/native-cpu-backend-capability-record-v0.schema.json")
THREADING_SCHEMA = Path("schemas/native-cpu/native-cpu-threading-record-v0.schema.json")
PARITY_SCHEMA = Path("schemas/native-cpu/native-cpu-parity-record-v0.schema.json")
DIAGNOSTIC_SCHEMA = Path("schemas/native-cpu/native-cpu-diagnostic-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/native-cpu/stage5d-native-cpu-summary-v0.schema.json")

CAPABILITIES_JSON = "native_backend_capabilities.json"
THREADING_JSON = "threading_parity_report.json"
PARITY_JSON = "native_python_parity_report.json"
DIAGNOSTICS_JSON = "native_cpu_diagnostics.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

THREAD_COUNTS = (1, 2, 4, 8, 16)
NEXT_STAGE = "Stage 5E - first CUDA kernel contract and CPU/native parity adapter selection"

POLICY_FLAGS = {
    "native_cpu_only": True,
    "cuda_used": False,
    "cuda_required": False,
    "gpu_required": False,
    "gpu_benchmark_performed": False,
    "cuda_kernel_added": False,
    "cuda_source_modified": False,
    "performance_claim": False,
    "speedup_claim": False,
    "broad_experiment_executed": False,
    "raw_data_processed": False,
    "solve_claim": False,
    "no_solve_claim": True,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "website_expansion": False,
    "python_semantic_reference_preserved": True,
    "cxx_launches_python_workers": False,
}

BAD_TRUE_FLAGS = (
    "cuda_used",
    "cuda_required",
    "gpu_required",
    "gpu_benchmark_performed",
    "cuda_kernel_added",
    "cuda_source_modified",
    "performance_claim",
    "speedup_claim",
    "broad_experiment_executed",
    "raw_data_processed",
    "solve_claim",
    "canonical_corpus_active",
    "page_boundaries_final",
    "generated_outputs_committed",
    "codex_output_committed",
    "website_expansion",
    "cxx_launches_python_workers",
)
