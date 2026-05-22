"""Build Stage 5Z next-stage decision records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_contract.models import NEXT_STAGE_DECISION_PATH, NEXT_STAGE_REASON, NEXT_STAGE_TITLE, OUTPUT_DIR, base_record


def build_next_stage_decision(
    next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict]:
    specs = [
        (
            "stage5aa_prime_minus_one_cuda_synthetic_kernel_implementation",
            True,
            "Codex",
            NEXT_STAGE_TITLE,
            "selected",
            NEXT_STAGE_REASON,
        ),
        (
            "stage5aa_gap_closure_if_contract_validation_fails",
            False,
            "Codex",
            "Stage 5AA - prime-minus-one CUDA contract gap closure",
            "fallback_only",
            "Use only if Stage 5Z validation fails after commit review.",
        ),
        (
            "bounded_cpu_native_scored_experiment",
            False,
            "Codex",
            "Stage 5AA - bounded CPU/native scored experiment",
            "deferred_manifest_gate_required",
            "Scored experiments remain manifest-gated and should not precede synthetic CUDA parity.",
        ),
        (
            "prime_minus_one_cuda_benchmark",
            False,
            "Codex",
            "Stage 5AA - CUDA benchmark planning",
            "blocked_benchmark_disallowed",
            "Benchmarks require a parity-passing implementation first.",
        ),
        (
            "unsolved_page_cuda_micro_pilot",
            False,
            "Codex",
            "Stage 5AA - unsolved page CUDA pilot",
            "blocked_unsolved_page_cuda_disallowed",
            "Unsolved-page CUDA remains blocked.",
        ),
        (
            "deep_research_prime_minus_one_review",
            False,
            "Deep Research",
            "Deep Research - prime-minus-one evidence review",
            "not_selected",
            "No new research question blocks the next synthetic engineering step.",
        ),
        (
            "website_or_report_expansion",
            False,
            "Codex",
            "Stage 5AA - website expansion",
            "deferred_no_website_scope",
            "Stage 5Z creates compact metadata only and does not publish generated bodies.",
        ),
    ]
    records = [
        base_record(
            "prime_minus_one_cuda_next_stage_decision_record",
            "schemas/cuda/prime-minus-one-cuda-next-stage-decision-record-v0.schema.json",
            option_id=option_id,
            selected=selected,
            recommended_prompt_type=prompt_type,
            recommended_stage_title=stage_title,
            status=status,
            rationale=rationale,
            execution_enabled=False,
            cuda_execution_allowed=False,
            cuda_source_changes_allowed=False,
            benchmark_execution_allowed=False,
            unsolved_page_scope_allowed=False,
            generated_body_publication_allowed=False,
        )
        for option_id, selected, prompt_type, stage_title, status, rationale in specs
    ]
    write_records(next_stage_decision_out, records)
    write_json_report(out_dir, "next_stage_decision.json", {"records": records})
    return records


__all__ = ["build_next_stage_decision"]
