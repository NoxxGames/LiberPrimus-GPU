"""Build Stage 5Z implementation-readiness gate records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_contract.models import IMPLEMENTATION_READINESS_PATH, NEXT_STAGE_TITLE, OUTPUT_DIR, base_record


def build_implementation_readiness_gate(
    implementation_readiness_out: Path = IMPLEMENTATION_READINESS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict]:
    record = base_record(
        "prime_minus_one_cuda_implementation_readiness_gate_record",
        "schemas/cuda/prime-minus-one-cuda-implementation-readiness-gate-record-v0.schema.json",
        implementation_readiness_gate_record_id="stage5z-prime-minus-one-implementation-readiness-gate-v0",
        readiness_status="ready_for_synthetic_cuda_kernel_implementation_contract_only",
        future_synthetic_kernel_implementation_ready=True,
        future_stage_title=NEXT_STAGE_TITLE,
        allowed_future_scope=[
            "synthetic_validation_vectors_only",
            "no_p56_fixture_execution",
            "no_unsolved_pages",
            "no_benchmarking",
            "no_generated_body_publication",
        ],
        current_stage_allows_kernel_implementation=False,
        current_stage_allows_cuda_execution=False,
        current_stage_allows_native_execution=False,
        full_p56_status="blocked_full_p56_token_buffer_missing",
        scored_experiment_status="deferred_manifest_gate_required",
        blockers=[],
    )
    records = [record]
    write_records(implementation_readiness_out, records)
    write_json_report(out_dir, "implementation_readiness_gate.json", {"records": records})
    return records


__all__ = ["build_implementation_readiness_gate"]
