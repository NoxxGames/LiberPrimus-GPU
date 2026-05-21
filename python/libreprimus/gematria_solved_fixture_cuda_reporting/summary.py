"""Build Stage 5N reporting summaries."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.gematria_solved_fixture_cuda_reporting.export import read_record_set, write_report, write_warnings
from libreprimus.gematria_solved_fixture_cuda_reporting.models import (
    BOUNDARY_REVIEW_PATH,
    CONTROLLED_EXPANSION_GATE_PATH,
    NEXT_STAGE,
    NEXT_STAGE_REASON,
    NO_UNSOLVED_GUARDRAIL_PATH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    RESULT_STORE_PREFLIGHT_PATH,
    STAGE5M_SUMMARY,
    SUMMARY_JSON,
    SUMMARY_PATH,
)


def build_summary(
    *,
    parity_report: Path = PARITY_REPORT_PATH,
    controlled_expansion_gate: Path = CONTROLLED_EXPANSION_GATE_PATH,
    boundary_review: Path = BOUNDARY_REVIEW_PATH,
    result_store_preflight: Path = RESULT_STORE_PREFLIGHT_PATH,
    no_unsolved_guardrail: Path = NO_UNSOLVED_GUARDRAIL_PATH,
    stage5m_summary: Path = STAGE5M_SUMMARY,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    parity = read_record_set(parity_report)
    gates = read_record_set(controlled_expansion_gate)
    boundaries = read_record_set(boundary_review)
    preflight = read_record_set(result_store_preflight)
    guardrails = read_record_set(no_unsolved_guardrail)
    stage5m = read_yaml(stage5m_summary)
    gate_counts = dict(sorted(Counter(record["gate_status"] for record in gates).items()))
    guardrail_counts = dict(sorted(Counter(record["guardrail_status"] for record in guardrails).items()))
    summary = {
        "record_type": "stage5n_solved_fixture_cuda_reporting_summary",
        "stage_id": "stage-5n",
        "status": "complete",
        "parity_report_records": len(parity),
        "gate_records": len(gates),
        "boundary_review_records": len(boundaries),
        "result_store_preflight_records": len(preflight),
        "no_unsolved_guardrail_records": len(guardrails),
        "stage5m_run_records": int(stage5m["run_records"]),
        "stage5m_parity_records": int(stage5m["parity_records"]),
        "parity_pass_count": int(stage5m["parity_pass_count"]),
        "parity_fail_count": int(stage5m["parity_fail_count"]),
        "parity_skip_count": int(stage5m["parity_skip_count"]),
        "stage5m_exact_scope_confirmed": True,
        "controlled_expansion_gate_status_counts": gate_counts,
        "no_unsolved_guardrail_status_counts": guardrail_counts,
        "unsolved_page_cuda_allowed": False,
        "additional_cuda_execution_performed": False,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "cuda_source_modified": False,
        "gpu_benchmark_performed": False,
        "speedup_claim": False,
        "performance_claim": False,
        "solve_claim": False,
        "no_solve_claim": True,
        "real_liber_primus_cuda_data_used": False,
        "solved_fixture_cuda_used": False,
        "generated_outputs_committed": False,
        "raw_data_processed": False,
        "codex_output_committed": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "no_gpu_ci_safe": True,
        "selected_next_stage": NEXT_STAGE,
        "next_stage": NEXT_STAGE,
        "selected_next_stage_reason": NEXT_STAGE_REASON,
        "remaining_blockers": [
            "additional_solved_fixture_candidates_not_selected",
            "result_store_preflight_not_executed",
            "unsolved_page_cuda_blocked",
        ],
        "newly_discovered_blockers": [],
        "stage5m_does_not_authorize": [
            "unsolved_page_cuda",
            "real_liber_primus_page_data_cuda",
            "gpu_benchmarking",
            "broad_solved_fixture_classes",
            "reverse_rotated_reverse_vigenere_prime_stream_cuda_semantics",
        ],
    }
    write_yaml(summary_out, summary)
    write_report(out_dir, SUMMARY_JSON, summary)
    write_warnings(out_dir, [])
    return summary


def load_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    payload = read_yaml(summary_path)
    if not isinstance(payload, dict):
        raise ValueError(f"summary must be a mapping: {summary_path}")
    return payload
