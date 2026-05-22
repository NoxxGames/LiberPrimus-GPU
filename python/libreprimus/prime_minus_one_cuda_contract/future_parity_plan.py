"""Build Stage 5Z future parity plan records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_contract.models import FUTURE_PARITY_PLAN_PATH, NEXT_STAGE_TITLE, OUTPUT_DIR, base_record


def build_future_parity_plan(
    future_parity_plan_out: Path = FUTURE_PARITY_PLAN_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict]:
    specs = [
        (
            "stage5z-future-parity-synthetic-kernel-v0",
            NEXT_STAGE_TITLE,
            "ready_for_contract_scoped_future_stage",
            ["synthetic_validation_vectors_only", "no_p56_fixture_execution", "no_unsolved_pages"],
        ),
        (
            "stage5z-future-parity-p56-bounded-v0",
            "Future bounded p56 parity after synthetic kernel success",
            "deferred_requires_explicit_future_stage",
            ["requires_stage5aa_success", "requires_explicit_p56_bounded_cuda_scope"],
        ),
        (
            "stage5z-future-parity-full-p56-v0",
            "Future full p56 parity",
            "blocked_full_p56_token_buffer_missing",
            ["needs_full_committed_p56_cipher_token_buffer_before_full_fixture_cuda_execution"],
        ),
        (
            "stage5z-future-parity-scored-experiment-v0",
            "Future scored experiment",
            "blocked_manifest_gate_required",
            ["requires_manifest_gate", "requires_cpu_native_scored_scope_before_cuda_scored_scope"],
        ),
    ]
    records = [
        base_record(
            "prime_minus_one_cuda_future_parity_plan_record",
            "schemas/cuda/prime-minus-one-cuda-future-parity-plan-record-v0.schema.json",
            future_parity_plan_record_id=record_id,
            future_stage_title=stage_title,
            readiness_status=status,
            prerequisites=prerequisites,
            execution_enabled=False,
            cuda_execution_allowed=False,
            benchmark_allowed=False,
            unsolved_page_scope_allowed=False,
            generated_body_publication_allowed=False,
        )
        for record_id, stage_title, status, prerequisites in specs
    ]
    write_records(future_parity_plan_out, records)
    write_json_report(out_dir, "future_parity_plan_report.json", {"records": records})
    return records


__all__ = ["build_future_parity_plan"]
