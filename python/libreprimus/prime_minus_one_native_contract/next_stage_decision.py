"""Next-stage decisions for Stage 5W."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_native_contract.models import COMMON_FLAGS, NEXT_STAGE_DECISION_PATH, NEXT_STAGE_REASON_READY, NEXT_STAGE_TITLE_READY, OUTPUT_DIR, REPORT_FILES


def build_next_stage_decision(
    *, next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    records = [
        _record(
            "stage5x_prime_minus_one_native_parity_execution",
            "selected",
            True,
            "Codex",
            NEXT_STAGE_TITLE_READY,
            NEXT_STAGE_REASON_READY,
            "medium",
            requires_stage5w_contract=True,
            requires_native_execution=True,
            requires_token_values=True,
        ),
        _record(
            "stage5x_prime_minus_one_contract_blocker_closure",
            "deferred",
            False,
            "Codex",
            "Stage 5X - prime-minus-one stream contract blocker closure",
            "Formula direction and bounded p56 mapping are source-backed, so blocker closure is deferred to full p56 token-buffer expansion rather than selected now.",
            "medium",
            requires_stage5w_contract=True,
            requires_formula_direction_confirmation=False,
            requires_token_values=True,
            blockers=["full_p56_page_token_buffer_not_committed"],
        ),
        _record(
            "stage5x_vigenere_explicit_key_native_contract",
            "deferred",
            False,
            "Codex",
            "Stage 5X - explicit-key Vigenere native parity contract preparation",
            "Prime-minus-one remains the selected high-value stream family after Stage 5W.",
            "medium",
        ),
        _record(
            "stage5x_affine_reverse_native_contract",
            "deferred",
            False,
            "Codex",
            "Stage 5X - affine/reverse native parity contract preparation",
            "Affine and reverse-family contracts should wait until the selected prime-minus-one native execution/preflight stage is complete.",
            "low",
        ),
        _record(
            "stage5x_cuda_kernel_contract",
            "blocked",
            False,
            "Codex",
            "Stage 5X - prime-minus-one CUDA kernel contract",
            "CUDA kernel contracts remain blocked until no-GPU native prime-minus-one parity execution records exist.",
            "high",
            requires_cuda_contract=True,
            blockers=["needs_stage5x_no_gpu_native_prime_minus_one_parity_execution"],
        ),
        _record(
            "stage5x_benchmark_planning",
            "blocked",
            False,
            "Codex",
            "Stage 5X - CUDA benchmark planning",
            "Benchmark planning is premature before family-specific native parity execution and CUDA contract records.",
            "high",
            benchmark_planning_allowed=True,
            blockers=["needs_native_parity_execution_and_cuda_contract_before_benchmark_planning"],
        ),
        _record(
            "stage5x_pause_cuda_return_to_research",
            "deferred",
            False,
            "Deep Research",
            "Deep Research - prime stream evidence review",
            "No further Deep Research is required before the bounded no-GPU native parity execution stage.",
            "low",
        ),
        _record(
            "stage6_website_expansion",
            "deferred",
            False,
            "Codex",
            "Stage 6 - website expansion",
            "Website expansion remains outside Stage 5W and is not selected without explicit user direction.",
            "low",
        ),
    ]
    write_records(next_stage_decision_out, records)
    write_json_report(out_dir, REPORT_FILES["next_stage"], {"records": records})
    return records


def _record(
    option_id: str,
    status: str,
    selected: bool,
    recommended_prompt_type: str,
    recommended_stage_title: str,
    rationale: str,
    risk_level: str,
    *,
    requires_stage5w_contract: bool = True,
    requires_native_execution: bool = False,
    requires_formula_direction_confirmation: bool = False,
    requires_token_values: bool = False,
    requires_skip_policy: bool = False,
    requires_cuda_contract: bool = False,
    benchmark_planning_allowed: bool = False,
    blockers: list[str] | None = None,
) -> dict[str, Any]:
    return {
        **COMMON_FLAGS,
        "record_type": "prime_minus_one_next_stage_decision_record",
        "schema": "schemas/cuda/prime-minus-one-next-stage-decision-record-v0.schema.json",
        "option_id": option_id,
        "status": status,
        "selected": selected,
        "recommended_prompt_type": recommended_prompt_type,
        "recommended_stage_title": recommended_stage_title,
        "rationale": rationale,
        "risk_level": risk_level,
        "cuda_execution_allowed": False,
        "cuda_source_changes_allowed": False,
        "benchmark_execution_allowed": False,
        "benchmark_planning_allowed": benchmark_planning_allowed,
        "unsolved_page_cuda_allowed": False,
        "generated_body_publication_allowed": False,
        "method_status_upgrade_allowed": False,
        "requires_stage5w_contract": requires_stage5w_contract,
        "requires_native_execution": requires_native_execution,
        "requires_formula_direction_confirmation": requires_formula_direction_confirmation,
        "requires_token_values": requires_token_values,
        "requires_skip_policy": requires_skip_policy,
        "requires_cuda_contract": requires_cuda_contract,
        "blockers": blockers or [],
    }
