"""Next-stage decision records for Stage 5X."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_parity.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_native_parity.models import COMMON_RECORD_FLAGS, NATIVE_PARITY_PATH, NEXT_STAGE_DECISION_PATH, NEXT_STAGE_REASON_READY, NEXT_STAGE_TITLE_FIX, NEXT_STAGE_TITLE_READY, OUTPUT_DIR, REPORT_FILES


def build_next_stage_decision(
    *,
    native_parity: Path = NATIVE_PARITY_PATH,
    next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    parity = read_records(native_parity)
    ready = sum(1 for record in parity if record.get("parity_status") == "passed") == 2
    selected = "stage5y_prime_minus_one_native_parity_reporting_integration" if ready else "stage5y_prime_minus_one_native_parity_mismatch_fix"
    records = [
        _decision(
            "stage5y_prime_minus_one_native_parity_reporting_integration",
            selected,
            "selected" if ready else "blocked",
            NEXT_STAGE_TITLE_READY,
            NEXT_STAGE_REASON_READY,
            [],
        ),
        _decision(
            "stage5y_prime_minus_one_native_parity_mismatch_fix",
            selected,
            "blocked" if ready else "selected",
            NEXT_STAGE_TITLE_FIX,
            "A mismatch investigation is selected only if a ready mapping fails its expected hash comparison.",
            [] if not ready else ["ready_mappings_passed"],
        ),
        _decision(
            "stage5y_full_p56_token_buffer_source_expansion",
            selected,
            "deferred",
            "Stage 5Y - full p56 token-buffer source expansion preflight",
            "Full p56 parity still requires a separately scoped source-backed token-buffer expansion stage.",
            ["needs_full_committed_p56_cipher_token_buffer"],
            requires_full_p56_token_buffer=True,
        ),
        _decision(
            "stage5y_prime_minus_one_cuda_contract_preparation",
            selected,
            "blocked",
            "Stage 5Y - prime-minus-one CUDA contract preparation",
            "CUDA contract planning remains blocked until compact Stage 5X reporting is integrated and reviewed.",
            ["needs_stage5y_reporting_integration_gate"],
            requires_cuda_contract=True,
        ),
        _decision(
            "stage5y_benchmark_planning",
            selected,
            "blocked",
            "Stage 5Y - benchmark planning",
            "Benchmark planning remains premature before CUDA contract readiness and explicit benchmark scope.",
            ["needs_cuda_contract_before_benchmark_planning"],
            requires_benchmark_plan=True,
        ),
        _decision("stage5y_vigenere_explicit_key_native_contract", selected, "deferred", "Stage 5Y - explicit-key Vigenere native contract", "Prime-minus-one reporting is the selected follow-up.", []),
        _decision("stage5y_affine_reverse_native_contract", selected, "deferred", "Stage 5Y - affine/reverse native contract", "Prime-minus-one reporting is the selected follow-up.", []),
        _decision("stage5y_pause_cuda_return_to_research", selected, "deferred", "Deep Research - pause CUDA and return to research review", "No new Deep Research is required because both ready mappings can be handled by deterministic Codex reporting.", []),
        _decision("stage6_website_expansion", selected, "blocked", "Stage 6 - website expansion", "Website expansion remains outside Stage 5X and is not selected without explicit user direction.", ["requires_explicit_user_stage6_scope"]),
    ]
    write_records(next_stage_decision_out, records)
    write_json_report(out_dir, REPORT_FILES["next_stage"], {"records": records})
    return records


def _decision(
    option_id: str,
    selected_id: str,
    status: str,
    title: str,
    rationale: str,
    blockers: list[str],
    *,
    requires_full_p56_token_buffer: bool = False,
    requires_cuda_contract: bool = False,
    requires_benchmark_plan: bool = False,
) -> dict[str, Any]:
    return {
        **COMMON_RECORD_FLAGS,
        "record_type": "prime_minus_one_native_next_stage_decision_record",
        "schema": "schemas/cuda/prime-minus-one-native-next-stage-decision-record-v0.schema.json",
        "option_id": option_id,
        "status": status,
        "selected": option_id == selected_id,
        "recommended_prompt_type": "Codex" if option_id != "stage5y_pause_cuda_return_to_research" else "Deep Research",
        "recommended_stage_title": title,
        "rationale": rationale,
        "risk_level": "medium" if option_id == selected_id else "low",
        "cuda_execution_allowed": False,
        "cuda_source_changes_allowed": False,
        "benchmark_execution_allowed": False,
        "benchmark_planning_allowed": False,
        "unsolved_page_cuda_allowed": False,
        "generated_body_publication_allowed": False,
        "method_status_upgrade_allowed": False,
        "requires_stage5x_parity": True,
        "requires_full_p56_token_buffer": requires_full_p56_token_buffer,
        "requires_cuda_contract": requires_cuda_contract,
        "requires_benchmark_plan": requires_benchmark_plan,
        "blockers": blockers,
    }
