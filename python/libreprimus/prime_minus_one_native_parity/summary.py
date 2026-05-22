"""Summary builder for Stage 5X."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_parity.export import read_records, write_json_report, write_summary
from libreprimus.prime_minus_one_native_parity.models import (
    COMMON_FALSE_FLAGS,
    COMMON_TRUE_FLAGS,
    CONTRACT_ID,
    HASH_ALGORITHM,
    NATIVE_PARITY_PATH,
    NATIVE_RUN_PATH,
    NEXT_STAGE_DECISION_PATH,
    NEXT_STAGE_REASON_READY,
    OUTPUT_DIR,
    REPORT_FILES,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORE_SUMMARY_PREFLIGHT_PATH,
    FULL_P56_BLOCKER_PATH,
    GUARDRAIL_PATH,
    SUMMARY_PATH,
    ABI_ID,
    SOURCE_STAGE_ID,
    STAGE_ID,
)


def build_summary(
    *,
    native_run: Path = NATIVE_RUN_PATH,
    native_parity: Path = NATIVE_PARITY_PATH,
    result_store_preflight: Path = RESULT_STORE_PREFLIGHT_PATH,
    score_summary_preflight: Path = SCORE_SUMMARY_PREFLIGHT_PATH,
    full_p56_blocker: Path = FULL_P56_BLOCKER_PATH,
    guardrail: Path = GUARDRAIL_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    runs = read_records(native_run)
    parity = read_records(native_parity)
    result_store = read_records(result_store_preflight)
    score = read_records(score_summary_preflight)
    blockers = read_records(full_p56_blocker)
    guardrails = read_records(guardrail)
    decisions = read_records(next_stage_decision)
    selected = next(record for record in decisions if record.get("selected") is True)
    passed = [record for record in parity if record.get("parity_status") == "passed"]
    failed = [record for record in parity if record.get("parity_status") == "failed_hash_mismatch"]
    skipped = [record for record in runs if str(record.get("native_execution_status", "")).startswith("skipped")]
    summary = {
        "record_type": "stage5x_prime_minus_one_native_parity_summary",
        "schema": "schemas/cuda/stage5x-prime-minus-one-native-parity-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "source_stage_id": SOURCE_STAGE_ID,
        "candidate_batch_abi_id": ABI_ID,
        "contract_id": CONTRACT_ID,
        "native_run_records": len(runs),
        "native_parity_records": len(parity),
        "result_store_preflight_records": len(result_store),
        "score_summary_preflight_records": len(score),
        "full_p56_blocker_records": len(blockers),
        "guardrail_records": len(guardrails),
        "next_stage_decision_records": len(decisions),
        "ready_mapping_count": 2,
        "blocked_mapping_count": len(blockers),
        "native_execution_attempted_count": sum(1 for record in runs if record.get("native_execution_performed") is True),
        "native_pass_count": len(passed),
        "native_fail_count": len(failed),
        "native_skip_count": len(skipped),
        "synthetic_control_status": _status(parity, "stage5w-mapping-synthetic-prime-control-v0"),
        "p56_bounded_mapping_status": _status(parity, "stage5w-mapping-p56-stage4o-bounded-v0"),
        "full_p56_status": "blocked_full_p56_token_buffer_missing",
        "stage5w_expected_hash_match_count": len(passed),
        "output_hash_algorithm": HASH_ALGORITHM,
        "stage5y_ready": len(passed) == 2 and not failed,
        "recommended_next_prompt_type": selected["recommended_prompt_type"],
        "recommended_next_stage_title": selected["recommended_stage_title"],
        "recommended_next_stage_reason": selected["rationale"] if selected.get("selected") else NEXT_STAGE_REASON_READY,
        "deep_research_recommended_next": selected["recommended_prompt_type"] == "Deep Research",
        "native_execution_performed": True,
        "python_reference_execution_performed": True,
        **COMMON_FALSE_FLAGS,
        **COMMON_TRUE_FLAGS,
    }
    write_summary(summary_out, summary)
    write_json_report(out_dir, REPORT_FILES["summary"], summary)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / REPORT_FILES["warnings"]).write_text(json.dumps({"warnings": []}, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def _status(records: list[dict[str, Any]], mapping_id: str) -> str:
    for record in records:
        if record.get("mapping_id") == mapping_id:
            return str(record.get("parity_status"))
    return "missing"
