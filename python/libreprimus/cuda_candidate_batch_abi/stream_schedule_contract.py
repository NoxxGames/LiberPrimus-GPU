"""Build stream-schedule contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import write_record_set, write_report
from libreprimus.cuda_candidate_batch_abi.models import COMMON_FLAGS, OUTPUT_DIR, STREAM_SCHEDULE_CONTRACT_PATH, STREAM_SCHEDULE_REPORT_JSON


def build_stream_schedule_contract(
    *,
    stream_schedule_contract_out: Path = STREAM_SCHEDULE_CONTRACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Define prime-stream schedule surfaces without enabling execution."""

    rows = [
        {
            "stream_schedule_contract_id": "stage5u-prime-minus-one-stream-schedule-v0",
            "supported_families": ["prime_minus_one_stream", "p56_prime_minus_one", "phi_prime_stream"],
            "contract_status": "defined_for_stage5v_planning_implementation_pending",
            "stream_value_formula": "(prime_i - 1) mod 29",
            "start_index_policy": "per_candidate_stream_start_index_required",
            "advance_policy": "advance_on_transformable_rune_only_pending_native_conformance",
            "reset_policy": "reset_per_fixture_or_manifest_declared",
            "skip_policy": "separators_do_not_advance_stream",
            "supports_arbitrary_integer_streams": False,
        },
        {
            "stream_schedule_contract_id": "stage5u-arbitrary-stream-blocking-policy-v0",
            "supported_families": ["arbitrary_integer_stream"],
            "contract_status": "blocked_out_of_scope",
            "stream_value_formula": "not_defined",
            "start_index_policy": "blocked",
            "advance_policy": "blocked",
            "reset_policy": "blocked",
            "skip_policy": "blocked",
            "supports_arbitrary_integer_streams": False,
        },
    ]
    records = [
        {
            "record_type": "stream_schedule_contract_record",
            "stream_value_domain": "0..28",
            "stream_length_field": "stream_length",
            "stream_offset_field": "stream_offset",
            "per_candidate_stream_reference": "stream_schedule_ref",
            "separator_policy": "separators_do_not_advance_stream",
            "supports_prime_minus_one": "prime_minus_one_stream" in row["supported_families"],
            "supports_phi_prime_alias": "phi_prime_stream" in row["supported_families"],
            "generated_body_publication_allowed": False,
            "cuda_execution_allowed": False,
            "unsolved_page_cuda_allowed": False,
            "notes": "Stream values must be source-backed or generated from a declared deterministic stream record.",
            **row,
            **COMMON_FLAGS,
        }
        for row in rows
    ]
    write_record_set(stream_schedule_contract_out, records)
    write_report(out_dir, STREAM_SCHEDULE_REPORT_JSON, {"records": records})
    return records
