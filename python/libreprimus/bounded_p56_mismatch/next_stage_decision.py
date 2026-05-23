"""Next-stage decision records for Stage 5AD-fix."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json_report, write_records
from .models import NEXT_STAGE_DECISION_PATH, OUTPUT_DIR, RECOMMENDED_NEXT_OPTION_ID, RECOMMENDED_NEXT_STAGE_TITLE, REPORT_FILES, base_record

OPTIONS = (
    (
        "stage5ae_corrected_bounded_p56_cuda_formula_parity_reporting",
        RECOMMENDED_NEXT_STAGE_TITLE,
        "selected",
        "Repair the reference-contract/reporting split while preserving the Stage 5AD failed record.",
    ),
    (
        "stage5ad_fix2_cuda_kernel_or_host_mismatch_repair",
        "Stage 5AD-fix2 - CUDA kernel or host mismatch repair",
        "deferred",
        "No CUDA/device bug is evidenced by Stage 5AD-fix records.",
    ),
    (
        "stage5ad_fix2_hash_material_policy_repair",
        "Stage 5AD-fix2 - hash-material policy repair",
        "deferred",
        "Hash-material policy repair is needed but can be bundled into Stage 5AE reporting repair.",
    ),
    (
        "stage5ad_fix2_reference_contract_repair",
        "Stage 5AD-fix2 - reference-contract repair",
        "deferred",
        "Reference-contract repair is needed but can be bundled into Stage 5AE reporting repair.",
    ),
    (
        "stage5ae_full_p56_token_buffer_source_expansion_preflight",
        "Stage 5AE - full p56 token-buffer source expansion preflight",
        "blocked",
        "Full p56 remains blocked pending committed source-backed token buffers.",
    ),
    (
        "stage5ae_visual_clue_deep_research_prompt",
        "Stage 5AE - visual clue Deep Research prompt",
        "deferred",
        "The mismatch is a hash-lineage issue, not a visual clue research trigger.",
    ),
    (
        "stage5ae_bounded_cpu_native_scored_experiment_manifest_gate",
        "Stage 5AE - bounded CPU/native scored experiment manifest gate",
        "blocked",
        "Scored experiments remain out of scope for mismatch repair.",
    ),
    (
        "stage5ae_benchmark_planning",
        "Stage 5AE - benchmark planning",
        "blocked",
        "Benchmark planning must wait for corrected parity/reporting semantics.",
    ),
    (
        "stage5ae_unsolved_page_cuda_pilot",
        "Stage 5AE - unsolved-page CUDA pilot",
        "blocked",
        "Unsolved-page CUDA remains blocked.",
    ),
    (
        "stage5ae_pause_cuda_return_to_research",
        "Deep Research - pause CUDA and return to research",
        "deferred",
        "The mismatch has a bounded engineering repair path.",
    ),
    (
        "future_website_expansion_unnumbered",
        "Future unnumbered website expansion",
        "deferred",
        "Website expansion remains separate from Stage 5AD-fix.",
    ),
)


def build_next_stage_decision(
    *, next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    records = []
    for option_id, title, status, rationale in OPTIONS:
        selected = option_id == RECOMMENDED_NEXT_OPTION_ID
        records.append(
            base_record(
                "bounded_p56_mismatch_next_stage_decision_record",
                "schemas/cuda/bounded-p56-mismatch-next-stage-decision-record-v0.schema.json",
                next_stage_decision_record_id=f"stage5ad-fix-next-{option_id}",
                option_id=option_id,
                status=status,
                selected=selected,
                recommended_prompt_type="Codex",
                recommended_stage_title=title,
                rationale=rationale,
                execution_enabled=False,
                future_cuda_execution_allowed=selected,
                cuda_source_changes_allowed_current_stage=False,
                unsolved_page_scope_allowed=False,
                benchmark_execution_allowed=False,
                scored_experiment_execution_allowed=False,
                deep_research_recommended_next=False,
                blockers=[] if selected else ["not_selected_by_stage5ad_fix_root_cause"],
            )
        )
    write_records(next_stage_decision_out, records)
    write_json_report(out_dir, REPORT_FILES["next_stage"], {"records": records})
    return records
