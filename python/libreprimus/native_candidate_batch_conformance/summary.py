"""Stage 5V native Candidate Batch ABI conformance summary."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.native_candidate_batch_conformance.export import (
    read_mapping,
    read_record_set,
    write_mapping,
    write_report,
    write_warnings,
)
from libreprimus.native_candidate_batch_conformance.models import (
    ADAPTER_RECORDS_PATH,
    COMMON_FLAGS,
    CONFORMANCE_FIXTURES_PATH,
    EXPECTED_COUNTS,
    IMPLEMENTATION_STATUS_PATH,
    NEXT_STAGE_DECISION_PATH,
    NEXT_STAGE_REASON,
    NEXT_STAGE_TITLE,
    OUTPUT_DIR,
    REPORT_FILES,
    RESULT_STORE_CONFORMANCE_PATH,
    SCHEDULE_CONFORMANCE_PATH,
    SCORE_VECTOR_CONFORMANCE_PATH,
    SOURCE_STAGE_ID,
    STAGE5U_SUMMARY,
    STAGE_ID,
    SUMMARY_PATH,
    TOKEN_BUFFER_CONFORMANCE_PATH,
    TOPK_CONFORMANCE_PATH,
)


def build_summary(
    *,
    adapter_records: Path = ADAPTER_RECORDS_PATH,
    conformance_fixtures: Path = CONFORMANCE_FIXTURES_PATH,
    token_buffer_conformance: Path = TOKEN_BUFFER_CONFORMANCE_PATH,
    schedule_conformance: Path = SCHEDULE_CONFORMANCE_PATH,
    score_vector_conformance: Path = SCORE_VECTOR_CONFORMANCE_PATH,
    topk_conformance: Path = TOPK_CONFORMANCE_PATH,
    result_store_conformance: Path = RESULT_STORE_CONFORMANCE_PATH,
    implementation_status: Path = IMPLEMENTATION_STATUS_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    stage5u_summary: Path = STAGE5U_SUMMARY,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    adapters = read_record_set(adapter_records)
    fixtures = read_record_set(conformance_fixtures)
    token = read_record_set(token_buffer_conformance)
    schedule = read_record_set(schedule_conformance)
    score = read_record_set(score_vector_conformance)
    topk = read_record_set(topk_conformance)
    result_store = read_record_set(result_store_conformance)
    statuses = read_record_set(implementation_status)
    decisions = read_record_set(next_stage_decision)
    stage5u = read_mapping(stage5u_summary)
    selected = next(record for record in decisions if record.get("selected") is True)
    executed = [record for record in fixtures if record.get("execution_status") == "executed_python_reference"]
    output_hash_records = [record for record in executed if record.get("expected_output_token_hash")]
    payload: dict[str, Any] = {
        **COMMON_FLAGS,
        "record_type": "stage5v_native_candidate_batch_conformance_summary",
        "schema": "schemas/cuda/stage5v-native-candidate-batch-conformance-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "source_stage_id": SOURCE_STAGE_ID,
        "candidate_batch_abi_id": "candidate_batch_abi_v0",
        "native_adapter_records": len(adapters),
        "conformance_fixture_records": len(fixtures),
        "token_buffer_conformance_records": len(token),
        "schedule_conformance_records": len(schedule),
        "score_vector_conformance_records": len(score),
        "topk_conformance_records": len(topk),
        "result_store_conformance_records": len(result_store),
        "abi_implementation_status_records": len(statuses),
        "next_stage_decision_records": len(decisions),
        "stage5u_gap_count": int(stage5u.get("stage5t_gap_count", EXPECTED_COUNTS["stage5u_gap_count"])),
        "native_conformance_pass_count": sum(1 for record in statuses if record.get("implementation_status") == "passed"),
        "native_conformance_shape_only_count": sum(1 for record in statuses if record.get("implementation_status") == "shape_only"),
        "native_conformance_blocked_count": sum(1 for record in statuses if record.get("implementation_status") == "blocked"),
        "cpp_reference_adapter_implemented": False,
        "python_reference_adapter_implemented": True,
        "cpp_python_hash_match_count": 0,
        "executed_conformance_fixture_count": len(executed),
        "shape_only_fixture_count": sum(1 for record in fixtures if record.get("shape_only") is True),
        "output_hash_records": len(output_hash_records),
        "recommended_next_prompt_type": str(selected["recommended_prompt_type"]),
        "recommended_next_stage_title": str(selected["recommended_stage_title"]),
        "recommended_next_stage_reason": str(selected["rationale"]),
        "deep_research_recommended_next": False,
        "default_next_stage_title": NEXT_STAGE_TITLE,
        "default_next_stage_reason": NEXT_STAGE_REASON,
        "codex_output_written": False,
    }
    write_mapping(summary_out, payload)
    write_report(out_dir, REPORT_FILES["summary"], payload)
    write_warnings(
        out_dir,
        [
            {
                "stage_id": STAGE_ID,
                "warning_id": "cpp_reference_adapter_deferred",
                "message": "Stage 5V used the Python no-GPU reference adapter; C++ Candidate Batch ABI adapter remains pending.",
            }
        ],
    )
    return payload


def load_summary(summary: Path = SUMMARY_PATH) -> dict[str, Any]:
    return read_mapping(summary)
