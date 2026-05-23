"""Deterministic next-stage decisions for Stage 5AD."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json_report, write_records
from .models import (
    CUDA_PARITY_PATH,
    NEXT_STAGE_DECISION_PATH,
    NEXT_STAGE_IF_MISMATCH,
    NEXT_STAGE_IF_PASSED,
    NEXT_STAGE_IF_SKIPPED,
    OUTPUT_DIR,
    REPORT_FILES,
    base_record,
)

OPTIONS = [
    ("stage5ae_bounded_p56_cuda_parity_reporting_integration", NEXT_STAGE_IF_PASSED, "low"),
    ("stage5ad_followup_bounded_p56_cuda_toolchain_repair", NEXT_STAGE_IF_SKIPPED, "medium"),
    ("stage5ad_fix_bounded_p56_cuda_mismatch_investigation", NEXT_STAGE_IF_MISMATCH, "high"),
    ("stage5ae_full_p56_token_buffer_source_expansion_preflight", "Stage 5AE - full p56 token-buffer source expansion preflight", "medium"),
    ("stage5ae_visual_clue_deep_research_prompt", "Stage 5AE - visual clue Deep Research prompt", "medium"),
    ("stage5ae_bounded_cpu_native_scored_experiment_manifest_gate", "Stage 5AE - bounded CPU/native scored experiment manifest gate", "medium"),
    ("stage5ae_benchmark_planning", "Stage 5AE - benchmark planning", "high"),
    ("stage5ae_unsolved_page_cuda_pilot", "Stage 5AE - unsolved-page CUDA pilot", "high"),
    ("stage5ae_pause_cuda_return_to_research", "Stage 5AE - pause CUDA and return to research review", "low"),
    ("future_website_expansion_unnumbered", "Future unnumbered website expansion", "low"),
]


def build_next_stage_decision(
    *, cuda_parity: Path = CUDA_PARITY_PATH, next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    parity = read_records(cuda_parity)[0]
    selected_id = _selected_option(str(parity["parity_status"]))
    records: list[dict[str, Any]] = []
    for option_id, title, risk in OPTIONS:
        selected = option_id == selected_id
        records.append(
            base_record(
                "bounded_p56_cuda_next_stage_decision_record",
                "schemas/cuda/bounded-p56-cuda-next-stage-decision-record-v0.schema.json",
                option_id=option_id,
                status="selected" if selected else _status_for_option(option_id),
                selected=selected,
                recommended_prompt_type="Codex" if option_id != "stage5ae_visual_clue_deep_research_prompt" else "Deep Research",
                recommended_stage_title=title,
                rationale=_rationale(option_id, str(parity["parity_status"])),
                risk_level=risk,
                cuda_execution_allowed_current_stage=False,
                future_cuda_execution_allowed=option_id in {
                    "stage5ae_bounded_p56_cuda_parity_reporting_integration",
                    "stage5ad_followup_bounded_p56_cuda_toolchain_repair",
                    "stage5ad_fix_bounded_p56_cuda_mismatch_investigation",
                },
                cuda_source_changes_allowed_current_stage=option_id in {
                    "stage5ad_followup_bounded_p56_cuda_toolchain_repair",
                    "stage5ad_fix_bounded_p56_cuda_mismatch_investigation",
                },
                benchmark_execution_allowed=False,
                scored_experiment_execution_allowed=False,
                unsolved_page_scope_allowed=False,
                generated_body_publication_allowed=False,
                method_status_upgrade_allowed=False,
                requires_stage5ad_bounded_p56_parity=option_id == "stage5ae_bounded_p56_cuda_parity_reporting_integration",
                requires_full_p56_token_buffer=option_id == "stage5ae_full_p56_token_buffer_source_expansion_preflight",
                requires_manifest_gate=option_id == "stage5ae_bounded_cpu_native_scored_experiment_manifest_gate",
                requires_null_controls=option_id in {"stage5ae_bounded_cpu_native_scored_experiment_manifest_gate", "stage5ae_visual_clue_deep_research_prompt"},
                requires_operator_approval=option_id in {"stage5ae_unsolved_page_cuda_pilot", "stage5ae_benchmark_planning"},
                blockers=[] if selected else _blockers(option_id),
            )
        )
    write_records(next_stage_decision_out, records)
    write_json_report(out_dir, REPORT_FILES["next_stage"], {"records": records})
    return records


def _selected_option(parity_status: str) -> str:
    if parity_status == "passed":
        return "stage5ae_bounded_p56_cuda_parity_reporting_integration"
    if parity_status == "failed_hash_mismatch":
        return "stage5ad_fix_bounded_p56_cuda_mismatch_investigation"
    return "stage5ad_followup_bounded_p56_cuda_toolchain_repair"


def _status_for_option(option_id: str) -> str:
    if option_id in {"stage5ae_benchmark_planning", "stage5ae_unsolved_page_cuda_pilot"}:
        return "blocked"
    return "deferred"


def _blockers(option_id: str) -> list[str]:
    if option_id == "stage5ae_full_p56_token_buffer_source_expansion_preflight":
        return ["full_p56_token_buffer_missing"]
    if option_id == "stage5ae_benchmark_planning":
        return ["benchmark_planning_not_current_stage"]
    if option_id == "stage5ae_unsolved_page_cuda_pilot":
        return ["unsolved_page_cuda_not_authorized"]
    if option_id == "future_website_expansion_unnumbered":
        return ["website_expansion_deferred_future_project"]
    return ["not_selected_by_stage5ad_parity_status"]


def _rationale(option_id: str, parity_status: str) -> str:
    if option_id == _selected_option(parity_status):
        if parity_status == "passed":
            return "The exact bounded p56 CUDA vector matched the Stage 5X expected hash; the next stage can report and gate expansion without running full p56."
        if parity_status == "failed_hash_mismatch":
            return "The exact bounded p56 CUDA vector ran but the host-computed CUDA output hash did not match the Stage 5X expected hash; investigate the mismatch before any expansion."
        return "CUDA could not complete the bounded p56 vector locally; repair the bounded toolchain path before reporting or expansion."
    return "Recorded as an alternate Stage 5AD decision option; not selected by the bounded p56 parity result."
