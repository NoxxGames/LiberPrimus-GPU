"""Build Stage 5Y CUDA contract readiness-gate records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_native_reporting.models import COMMON_RECORD_FLAGS, CUDA_CONTRACT_READINESS_PATH, OUTPUT_DIR, PARITY_REPORT_PATH, REPORT_FILES, RESULT_STORE_INTEGRATION_PATH, SCORE_SUMMARY_INTEGRATION_PATH


def build_cuda_contract_readiness_gate(
    *,
    parity_report: Path = PARITY_REPORT_PATH,
    result_store_integration: Path = RESULT_STORE_INTEGRATION_PATH,
    score_summary_integration: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    cuda_contract_readiness_gate_out: Path = CUDA_CONTRACT_READINESS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    parity = read_records(parity_report)
    result_store = read_records(result_store_integration)
    score = read_records(score_summary_integration)
    ready_passes = sum(1 for record in parity if record.get("hash_match") is True)
    reporting_integrated = len(result_store) == 3 and len(score) == 3
    contract_ready = ready_passes == 2 and reporting_integrated
    record = {
        **COMMON_RECORD_FLAGS,
        "record_type": "prime_minus_one_cuda_contract_readiness_gate_record",
        "schema": "schemas/cuda/prime-minus-one-cuda-contract-readiness-gate-record-v0.schema.json",
        "gate_record_id": "stage5y-prime-minus-one-cuda-contract-readiness",
        "stage5w_contract_ready": True,
        "stage5x_bounded_native_parity_passed": ready_passes == 2,
        "result_store_reporting_integrated": len(result_store) == 3,
        "score_summary_reporting_integrated": len(score) == 3,
        "full_p56_required_for_cuda_contract": False,
        "prime_minus_one_cuda_contract_preparation_ready": contract_ready,
        "readiness_status": "ready_for_stage5z_cuda_contract_preparation" if contract_ready else "blocked_reporting_integration_gap",
        "cuda_execution_allowed": False,
        "cuda_source_changes_allowed": False,
        "new_kernel_allowed": False,
        "cuda_kernel_implementation_allowed": False,
        "benchmark_planning_allowed": False,
        "benchmark_execution_allowed": False,
        "unsolved_page_cuda_allowed": False,
        "blockers": [] if contract_ready else ["reporting_integration_not_clean"],
        "rationale": (
            "Stage 5X bounded no-GPU native parity passed for both ready mappings and Stage 5Y compact reporting "
            "integrates result-store and score-summary metadata. This permits a future CUDA contract-preparation "
            "stage only; it does not permit CUDA execution, source changes, kernels, or benchmarks."
        ),
    }
    records = [record]
    write_records(cuda_contract_readiness_gate_out, records)
    write_json_report(out_dir, REPORT_FILES["cuda_contract"], {"records": records})
    return records
