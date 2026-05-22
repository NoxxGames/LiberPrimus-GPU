"""Build Stage 5Z scored-experiment deferral records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_contract.models import OUTPUT_DIR, SCORED_EXPERIMENT_DEFERRAL_PATH, base_record


def build_scored_experiment_deferral(
    scored_experiment_deferral_out: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict]:
    specs = [
        ("bounded_cpu_native_prime_minus_one_scored_experiment", "deferred_manifest_gate_required", "CPU/native only; not Stage 5Z."),
        ("bounded_cuda_synthetic_scored_experiment", "blocked_until_synthetic_kernel_parity_exists", "No kernel exists in Stage 5Z."),
        ("bounded_cuda_p56_scored_experiment", "blocked_until_explicit_future_manifest_gate", "P56 CUDA execution is not Stage 5Z scope."),
        ("bounded_unsolved_page_micro_pilot", "blocked_unsolved_page_cuda_disallowed", "Unsolved pages remain out of scope."),
        ("benchmark_scored_experiment", "blocked_benchmark_disallowed", "Diagnostic planning only; no benchmark."),
        ("deep_research_scored_experiment", "not_selected_no_action", "No Deep Research handoff is selected as the immediate next prompt."),
    ]
    records = [
        base_record(
            "prime_minus_one_scored_experiment_deferral_record",
            "schemas/cuda/prime-minus-one-scored-experiment-deferral-record-v0.schema.json",
            scored_experiment_deferral_record_id=f"stage5z-scored-deferral-{experiment_class}",
            experiment_class=experiment_class,
            readiness_status=status,
            rationale=rationale,
            manifest_required_before_execution=True,
            execution_enabled=False,
            cuda_execution_allowed=False,
            benchmark_allowed=False,
            unsolved_page_scope_allowed=False,
            score_interpretation="triage_only",
        )
        for experiment_class, status, rationale in specs
    ]
    write_records(scored_experiment_deferral_out, records)
    write_json_report(out_dir, "scored_experiment_deferral_report.json", {"records": records})
    return records


__all__ = ["build_scored_experiment_deferral"]
