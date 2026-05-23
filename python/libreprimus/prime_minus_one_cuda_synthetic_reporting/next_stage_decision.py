"""Build deterministic Stage 5AC next-stage decision records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import (
    BOUNDED_P56_PREFLIGHT_PATH,
    DOC_STALENESS_VALIDATION_PATH,
    NEXT_STAGE_DECISION_PATH,
    NEXT_STAGE_REASON,
    NEXT_STAGE_TITLE,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    REPORT_FILES,
    base_record,
)


OPTIONS = (
    ("stage5ad_bounded_p56_cuda_parity_run", NEXT_STAGE_TITLE, "medium", True, False, False, False, False, False, False),
    ("stage5ad_bounded_p56_preflight_gap_closure", "Stage 5AD - bounded p56 preflight gap closure", "low", False, False, False, False, False, False, False),
    ("stage5ad_full_p56_token_buffer_source_expansion_preflight", "Stage 5AD - full p56 token-buffer source expansion preflight", "medium", False, False, False, False, True, False, False),
    ("stage5ad_bounded_cpu_native_scored_experiment_manifest_gate", "Stage 5AD - bounded CPU/native scored experiment manifest gate", "medium", False, False, False, True, False, True, True),
    ("stage5ad_benchmark_planning", "Stage 5AD - benchmark planning", "high", False, False, False, False, False, False, False),
    ("stage5ad_unsolved_page_cuda_pilot", "Stage 5AD - unsolved-page CUDA pilot", "high", False, False, True, False, False, False, False),
    ("stage5ad_pause_cuda_return_to_research", "Deep Research - prime-minus-one strategy review", "medium", False, False, False, False, False, False, False),
    ("future_website_expansion_unnumbered", "Future unnumbered website expansion project", "low", False, False, False, False, False, False, False),
)


def build_next_stage_decision(
    *,
    parity_report: Path = PARITY_REPORT_PATH,
    bounded_p56_preflight: Path = BOUNDED_P56_PREFLIGHT_PATH,
    doc_staleness_validation: Path = DOC_STALENESS_VALIDATION_PATH,
    next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    parity = read_records(parity_report)[0]
    preflight = read_records(bounded_p56_preflight)[0]
    doc = read_records(doc_staleness_validation)[0]
    parity_clean = parity.get("parity_status") == "passed" and parity.get("stage5aa_hash_match") is True
    docs_clean = doc.get("doc_staleness_strict_check_passed") is True
    preflight_ready = preflight.get("bounded_p56_cuda_execution_ready_next_stage") is True
    selected_option = "stage5ad_bounded_p56_cuda_parity_run" if parity_clean and docs_clean and preflight_ready else "stage5ad_bounded_p56_preflight_gap_closure"
    records = []
    for option_id, title, risk, future_cuda, future_full, unsolved, score, full_buffer, manifest_gate, null_controls in OPTIONS:
        selected = option_id == selected_option
        blockers: list[str] = []
        if not selected:
            blockers.append("not_selected")
        if option_id == "stage5ad_full_p56_token_buffer_source_expansion_preflight":
            blockers.append("full_p56_token_buffer_missing")
        if option_id == "stage5ad_benchmark_planning":
            blockers.append("benchmark_planning_not_selected_before_bounded_p56_parity")
        if option_id == "stage5ad_unsolved_page_cuda_pilot":
            blockers.append("unsolved_page_cuda_blocked")
        if option_id == "stage5ad_bounded_cpu_native_scored_experiment_manifest_gate":
            blockers.append("scored_experiments_deferred")
        if option_id == "future_website_expansion_unnumbered":
            blockers.append("deferred_future_unnumbered_project")
        records.append(
            base_record(
                "prime_minus_one_cuda_synthetic_next_stage_decision_record",
                "schemas/cuda/prime-minus-one-cuda-synthetic-next-stage-decision-record-v0.schema.json",
                option_id=option_id,
                status="selected" if selected else ("deferred" if option_id == "future_website_expansion_unnumbered" else "not_selected"),
                selected=selected,
                recommended_prompt_type="Deep Research" if option_id == "stage5ad_pause_cuda_return_to_research" and selected else "Codex",
                recommended_stage_title=title,
                rationale=NEXT_STAGE_REASON if selected else "Recorded as an alternate, deferred, or blocked Stage 5AC decision option.",
                risk_level=risk,
                cuda_execution_allowed_current_stage=False,
                future_cuda_execution_allowed=future_cuda and selected,
                cuda_source_changes_allowed_current_stage=False,
                benchmark_execution_allowed=False,
                scored_experiment_execution_allowed=False,
                unsolved_page_scope_allowed=False,
                generated_body_publication_allowed=False,
                method_status_upgrade_allowed=False,
                requires_stage5aa_synthetic_parity=True,
                requires_stage5ab_doc_staleness_clean=True,
                requires_bounded_p56_vector=option_id in {"stage5ad_bounded_p56_cuda_parity_run", "stage5ad_bounded_p56_preflight_gap_closure"},
                requires_full_p56_token_buffer=full_buffer,
                requires_manifest_gate=manifest_gate,
                requires_null_controls=null_controls,
                requires_operator_approval=manifest_gate or null_controls or score,
                blockers=[] if selected else blockers,
            )
        )
    write_records(next_stage_decision_out, records)
    write_json_report(out_dir, REPORT_FILES["next_stage"], {"records": records})
    return records
