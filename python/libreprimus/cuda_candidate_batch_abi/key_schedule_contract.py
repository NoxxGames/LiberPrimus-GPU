"""Build key-schedule contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import write_record_set, write_report
from libreprimus.cuda_candidate_batch_abi.models import COMMON_FLAGS, KEY_SCHEDULE_CONTRACT_PATH, KEY_SCHEDULE_REPORT_JSON, OUTPUT_DIR


def build_key_schedule_contract(
    *,
    key_schedule_contract_out: Path = KEY_SCHEDULE_CONTRACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Define key schedule surfaces for explicit-key transforms."""

    rows = [
        {
            "key_schedule_contract_id": "stage5u-vigenere-explicit-key-schedule-v0",
            "supported_families": ["vigenere_explicit_key"],
            "contract_status": "defined_for_stage5v_planning_implementation_pending",
            "advance_policy": "advance_on_transformable_rune_only_pending_native_conformance",
            "reset_policy": "reset_per_fixture_or_manifest_declared",
            "skip_policy": "separators_do_not_advance_key",
            "supports_known_skip_positions": True,
            "supports_candidate_key_list": True,
        },
        {
            "key_schedule_contract_id": "stage5u-future-keyed-transform-schedule-v0",
            "supported_families": ["future_key_based_transform"],
            "contract_status": "placeholder_not_execution_ready",
            "advance_policy": "must_be_declared_by_future_family_contract",
            "reset_policy": "must_be_declared_by_future_family_contract",
            "skip_policy": "must_be_declared_by_future_family_contract",
            "supports_known_skip_positions": False,
            "supports_candidate_key_list": False,
        },
    ]
    records = [
        {
            "record_type": "key_schedule_contract_record",
            "key_token_domain": "0..28",
            "key_length_field": "key_length",
            "key_offset_field": "key_offset",
            "per_candidate_key_reference": "key_schedule_ref",
            "separator_policy": "separators_do_not_advance_key",
            "supports_dictionary_key_list": False,
            "generated_body_publication_allowed": False,
            "cuda_execution_allowed": False,
            "unsolved_page_cuda_allowed": False,
            "notes": "Dictionary-scale key batches and unsolved-page CUDA remain out of scope.",
            **row,
            **COMMON_FLAGS,
        }
        for row in rows
    ]
    write_record_set(key_schedule_contract_out, records)
    write_report(out_dir, KEY_SCHEDULE_REPORT_JSON, {"records": records})
    return records
