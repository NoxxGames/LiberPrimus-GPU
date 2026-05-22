"""Implementation-status records for Stage 5V ABI gap closure."""

from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.export import write_record_set, write_report
from libreprimus.native_candidate_batch_conformance.models import COMMON_FLAGS, IMPLEMENTATION_STATUS_PATH, OUTPUT_DIR, REPORT_FILES


def build_implementation_status(
    *,
    implementation_status_out: Path = IMPLEMENTATION_STATUS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    records = [
        _record("stage5v-token-buffer-header", "token_buffer_header", "passed", []),
        _record("stage5v-key-schedule-buffer", "key_schedule_buffer", "shape_only", ["family_specific_vigenere_execution_contract_pending"]),
        _record("stage5v-stream-schedule-buffer", "stream_schedule_buffer", "shape_only", ["family_specific_prime_stream_execution_contract_pending"]),
        _record("stage5v-score-vector-shape", "score_vector_shape", "passed", []),
        _record("stage5v-topk-output-shape", "top_k_output_shape", "passed", []),
        _record("stage5v-python-reference-backend", "python_reference_backend", "passed", []),
        _record("stage5v-cpp-reference-backend", "cpp_reference_backend", "blocked", ["cpp_reference_adapter_deferred"]),
        _record("stage5v-cuda-backend", "cuda_backend", "blocked", ["cuda_execution_not_allowed_in_stage5v"]),
    ]
    write_record_set(implementation_status_out, records)
    write_report(out_dir, REPORT_FILES["gap_closure"], {"records": records, "count": len(records)})
    return records


def _record(status_id: str, gap_id: str, status: str, blockers: list[str]) -> dict[str, object]:
    return {
        **COMMON_FLAGS,
        "record_type": "candidate_batch_abi_implementation_status_record",
        "schema": "schemas/cuda/candidate-batch-abi-implementation-status-record-v0.schema.json",
        "implementation_status_id": status_id,
        "stage5u_gap_id": gap_id,
        "implementation_status": status,
        "blockers": blockers,
        "native_conformance_status": status,
        "notes": "Stage 5V converts Stage 5U contract closure into no-GPU conformance status.",
    }
