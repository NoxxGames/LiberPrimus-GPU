"""Build bounded scored-experiment readiness records for Stage 5Y."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import write_json_report, write_records
from libreprimus.prime_minus_one_native_reporting.models import COMMON_RECORD_FLAGS, OUTPUT_DIR, REPORT_FILES, SCORED_EXPERIMENT_READINESS_PATH


READINESS = [
    {
        "experiment_class": "bounded_cpu_native_prime_minus_one_scored_experiment",
        "readiness_status": "ready_after_stage5y_or_stage5z_manifest_gate",
        "recommended_next_stage_if_selected": "Stage 5Z - bounded CPU/native scored experiment manifest gate",
        "blockers": ["needs_explicit_manifest_gate", "needs_null_controls", "needs_operator_approval"],
        "requires_null_controls": True,
        "requires_operator_approval": True,
        "unsolved_scope_allowed": False,
    },
    {
        "experiment_class": "bounded_solved_fixture_score_regression",
        "readiness_status": "ready_with_manifest_gate",
        "recommended_next_stage_if_selected": "Stage 5Z - bounded solved-fixture score regression manifest gate",
        "blockers": ["needs_explicit_manifest_gate"],
        "requires_null_controls": False,
        "requires_operator_approval": True,
        "unsolved_scope_allowed": False,
    },
    {
        "experiment_class": "bounded_unsolved_page_micro_pilot",
        "readiness_status": "blocked_pending_corpus_page_boundary_source_lock_null_control_operator_gates",
        "recommended_next_stage_if_selected": "No action until explicit corpus/source/null-control/operator gates exist",
        "blockers": ["canonical_corpus_inactive", "page_boundaries_not_final", "needs_source_lock", "needs_null_controls", "needs_operator_approval"],
        "requires_null_controls": True,
        "requires_operator_approval": True,
        "unsolved_scope_allowed": False,
    },
    {
        "experiment_class": "cuda_scored_experiment",
        "readiness_status": "blocked_pending_cuda_contract_and_parity",
        "recommended_next_stage_if_selected": "Stage 5Z - prime-minus-one CUDA contract preparation",
        "blockers": ["needs_cuda_contract", "needs_cuda_parity"],
        "requires_null_controls": True,
        "requires_operator_approval": True,
        "unsolved_scope_allowed": False,
    },
    {
        "experiment_class": "benchmark_experiment",
        "readiness_status": "blocked_pending_benchmark_planning_stage",
        "recommended_next_stage_if_selected": "Stage 5Z-later - benchmark planning",
        "blockers": ["needs_cuda_contract_before_benchmark_planning"],
        "requires_null_controls": False,
        "requires_operator_approval": True,
        "unsolved_scope_allowed": False,
    },
    {
        "experiment_class": "website_stage6",
        "readiness_status": "deferred_until_user_explicitly_moves_website",
        "recommended_next_stage_if_selected": "Stage 6 - website expansion",
        "blockers": ["not_stage5y_scope"],
        "requires_null_controls": False,
        "requires_operator_approval": True,
        "unsolved_scope_allowed": False,
    },
]


def build_scored_experiment_readiness(
    *,
    scored_experiment_readiness_out: Path = SCORED_EXPERIMENT_READINESS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = []
    for item in READINESS:
        experiment_class = item["experiment_class"]
        records.append(
            {
                **COMMON_RECORD_FLAGS,
                "record_type": "bounded_scored_experiment_readiness_record",
                "schema": "schemas/cuda/bounded-scored-experiment-readiness-record-v0.schema.json",
                "readiness_id": f"stage5y-readiness-{experiment_class}",
                "experiment_class": experiment_class,
                "readiness_status": item["readiness_status"],
                "recommended_next_stage_if_selected": item["recommended_next_stage_if_selected"],
                "requires_canonical_corpus": experiment_class == "bounded_unsolved_page_micro_pilot",
                "requires_page_boundaries_final": experiment_class == "bounded_unsolved_page_micro_pilot",
                "requires_full_p56_token_buffer": False,
                "requires_result_store_contract": True,
                "requires_score_summary_contract": True,
                "requires_null_controls": item["requires_null_controls"],
                "requires_operator_approval": item["requires_operator_approval"],
                "cuda_required": experiment_class == "cuda_scored_experiment",
                "benchmark_allowed": False,
                "generated_body_publication_allowed": False,
                "unsolved_scope_allowed": item["unsolved_scope_allowed"],
                "rationale": "Stage 5Y records readiness only; any execution requires an explicit future manifest gate.",
                "blockers": item["blockers"],
            }
        )
    write_records(scored_experiment_readiness_out, records)
    write_json_report(out_dir, REPORT_FILES["scored_experiment"], {"records": records})
    return records
