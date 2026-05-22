"""Build deterministic Stage 5Y next-stage decision records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_native_reporting.models import COMMON_RECORD_FLAGS, CUDA_CONTRACT_READINESS_PATH, NEXT_STAGE_DECISION_PATH, NEXT_STAGE_REASON, NEXT_STAGE_TITLE, OUTPUT_DIR, REPORT_FILES


OPTIONS = [
    ("stage5z_prime_minus_one_cuda_contract_preparation", "selected", NEXT_STAGE_TITLE, "medium", False, False, False, False, False, []),
    ("stage5z_full_p56_token_buffer_source_expansion_preflight", "deferred", "Stage 5Z - full p56 token-buffer source expansion preflight", "medium", True, False, False, False, False, ["not_required_before_contract_preparation"]),
    ("stage5z_bounded_cpu_native_scored_experiment_manifest_gate", "alternate_ready", "Stage 5Z - bounded CPU/native scored experiment manifest gate", "medium", False, False, True, True, False, ["needs_explicit_manifest_gate"]),
    ("stage5z_bounded_solved_fixture_score_regression", "alternate_ready", "Stage 5Z - bounded solved-fixture score regression", "low", False, False, True, False, False, ["needs_explicit_manifest_gate"]),
    ("stage5z_prime_minus_one_reporting_gap_closure", "not_selected", "Stage 5Z - prime-minus-one reporting gap closure", "low", False, False, False, False, False, ["no_reporting_gap_detected"]),
    ("stage5z_vigenere_explicit_key_native_contract", "deferred", "Stage 5Z - Vigenere explicit-key native contract", "medium", False, False, False, False, False, ["prime_minus_one_contract_path_selected_first"]),
    ("stage5z_affine_reverse_native_contract", "deferred", "Stage 5Z - affine/reverse native contract", "medium", False, False, False, False, False, ["prime_minus_one_contract_path_selected_first"]),
    ("stage5z_benchmark_planning", "blocked", "Stage 5Z - benchmark planning", "high", False, False, False, False, True, ["needs_cuda_contract_before_benchmark_planning"]),
    ("stage5z_pause_cuda_return_to_research", "not_selected", "Deep Research - prime-minus-one strategy review", "medium", False, False, False, False, False, ["no_strategic_ambiguity_detected"]),
    ("stage6_website_expansion", "deferred", "Stage 6 - website expansion", "low", False, False, False, False, False, ["not_stage5y_scope"]),
]


def build_next_stage_decision(
    *,
    cuda_contract_readiness_gate: Path = CUDA_CONTRACT_READINESS_PATH,
    next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    gate = read_records(cuda_contract_readiness_gate)[0]
    contract_ready = gate.get("prime_minus_one_cuda_contract_preparation_ready") is True
    records = []
    for option_id, base_status, title, risk, requires_full, requires_cuda, requires_score, requires_null, benchmark_planning, blockers in OPTIONS:
        selected = option_id == "stage5z_prime_minus_one_cuda_contract_preparation" and contract_ready
        status = "selected" if selected else ("blocked_reporting_integration_gap" if option_id == "stage5z_prime_minus_one_cuda_contract_preparation" else base_status)
        prompt_type = "Deep Research" if option_id == "stage5z_pause_cuda_return_to_research" and selected else "Codex"
        records.append(
            {
                **COMMON_RECORD_FLAGS,
                "record_type": "prime_minus_one_native_reporting_next_stage_decision_record",
                "schema": "schemas/cuda/prime-minus-one-native-reporting-next-stage-decision-record-v0.schema.json",
                "option_id": option_id,
                "status": status,
                "selected": selected,
                "recommended_prompt_type": prompt_type,
                "recommended_stage_title": title,
                "rationale": NEXT_STAGE_REASON if selected else "Recorded as an alternate, deferred, or blocked option by Stage 5Y readiness policy.",
                "risk_level": risk,
                "native_execution_allowed": False,
                "cuda_execution_allowed": False,
                "cuda_source_changes_allowed": False,
                "benchmark_execution_allowed": False,
                "benchmark_planning_allowed": benchmark_planning and False,
                "unsolved_page_scope_allowed": False,
                "generated_body_publication_allowed": False,
                "method_status_upgrade_allowed": False,
                "requires_stage5y_reporting": True,
                "requires_full_p56_token_buffer": requires_full,
                "requires_cuda_contract": requires_cuda,
                "requires_score_manifest": requires_score,
                "requires_null_controls": requires_null,
                "requires_operator_approval": requires_score or requires_null,
                "blockers": [] if selected else blockers,
            }
        )
    write_records(next_stage_decision_out, records)
    write_json_report(out_dir, REPORT_FILES["next_stage"], {"records": records})
    return records
