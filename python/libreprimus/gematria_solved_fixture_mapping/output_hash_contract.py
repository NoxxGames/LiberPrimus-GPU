"""Build Stage 5L solved-fixture output hash contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_mapping.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_solved_fixture_mapping.models import (
    COMMON_POLICY_FLAGS,
    HASH_ALGORITHM,
    NATIVE_PARITY_PATH,
    OUTPUT_DIR,
    OUTPUT_HASH_CONTRACT_JSON,
    OUTPUT_HASH_CONTRACT_PATH,
    OUTPUT_ORDERING,
    SCORE_SUMMARY_CONTRACT,
)


def build_output_hash_contract_records(
    *,
    native_parity: Path = NATIVE_PARITY_PATH,
    output_hash_contract_out: Path = OUTPUT_HASH_CONTRACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build the durable hash contract for future solved-fixture-safe CUDA parity."""

    native_records = read_record_set(native_parity)
    prepared = [record for record in native_records if record.get("native_parity_status") == "prepared"]
    record: dict[str, Any] = {
        "record_type": "gematria_solved_fixture_output_hash_contract_record",
        "contract_record_id": "stage5l-output-hash-contract-v0",
        "hash_contract_id": "stage5l-solved-fixture-output-hash-contract-v0",
        "hash_algorithm": HASH_ALGORITHM,
        "hash_input_material": [
            "mapping_id",
            "source_input_stream_id",
            "fixture_id",
            "candidate_id",
            "token_domain",
            "candidate_ordering",
            "candidate_shifts",
            "candidate-major output token values",
            "token kinds",
            "separator preservation metadata",
        ],
        "candidate_ordering_required": OUTPUT_ORDERING,
        "output_token_hash_required": True,
        "output_text_hash_required": False,
        "output_text_hash_policy": "blocked_until_transliteration_policy_is_explicit",
        "separator_metadata_required": True,
        "token_kind_metadata_required": True,
        "compatible_with_stage4p_unified_result_surface": True,
        "stage4p_compatibility_reason": "Uses explicit result-source kind, output_token_hash, no-CUDA, no-solve, and generated-output flags.",
        "compatible_with_stage4i_score_summary": True,
        "stage4i_compatibility_reason": "Score summaries remain triage-only and cite the output_token_hash.",
        "prepared_native_parity_records": len(prepared),
        "prepared_output_token_hashes": [str(record["output_token_hash"]) for record in prepared],
        "blockers": ["need_explicit_future_stage_approval"],
        "blocker_count": 1,
        **COMMON_POLICY_FLAGS,
        "score_summary_contract": SCORE_SUMMARY_CONTRACT,
    }
    records = [record]
    write_record_set(output_hash_contract_out, records)
    write_report(out_dir, OUTPUT_HASH_CONTRACT_JSON, {"records": records})
    return records
