"""Build native parity fixture records from Stage 5L token mappings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_mapping.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_solved_fixture_mapping.models import (
    CANDIDATE_SHIFTS,
    COMMON_POLICY_FLAGS,
    HASH_ALGORITHM,
    NATIVE_PARITY_JSON,
    NATIVE_PARITY_PATH,
    OUTPUT_DIR,
    OUTPUT_ORDERING,
    REMAINING_APPROVAL_BLOCKER,
    TOKEN_DOMAIN,
    TOKEN_MAPPING_PATH,
)
from libreprimus.gematria_solved_fixture_mapping.token_mapping import canonical_hash


def build_native_parity_records(
    *,
    token_mapping: Path = TOKEN_MAPPING_PATH,
    native_parity_out: Path = NATIVE_PARITY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build CPU/native output-token hash records without CUDA execution."""

    mapping_records = read_record_set(token_mapping)
    records = [_build_record(index=index, mapping=record) for index, record in enumerate(mapping_records)]
    write_record_set(native_parity_out, records)
    write_report(out_dir, NATIVE_PARITY_JSON, {"records": records})
    return records


def _build_record(*, index: int, mapping: dict[str, Any]) -> dict[str, Any]:
    mapped = mapping.get("mapping_status") == "mapped"
    if not mapped:
        blockers = list(mapping.get("blockers", [])) or ["blocked_mapping_not_available"]
        return {
            "record_type": "gematria_solved_fixture_native_parity_record",
            "native_parity_record_id": f"stage5l-native-parity-{index:02d}",
            "mapping_id": mapping["mapping_id"],
            "source_input_stream_id": mapping["source_input_stream_id"],
            "fixture_id": mapping["fixture_id"],
            "candidate_id": mapping["candidate_id"],
            "native_parity_status": "blocked",
            "readiness_status": "blocked",
            "blockers": blockers,
            "blocker_count": len(blockers),
            "output_token_hash": None,
            "candidate_shifts": list(CANDIDATE_SHIFTS),
            **COMMON_POLICY_FLAGS,
        }
    candidate_outputs = []
    for candidate_index, shift in enumerate(CANDIDATE_SHIFTS):
        output_tokens = []
        for token in mapping["token_records"]:
            output_tokens.append(_shift_token(token=token, shift=shift))
        candidate_outputs.append(
            {
                "candidate_index": candidate_index,
                "shift": shift,
                "output_tokens": output_tokens,
            }
        )
    hash_material = {
        "contract_id": "stage5l-solved-fixture-output-hash-contract-v0",
        "mapping_id": mapping["mapping_id"],
        "source_input_stream_id": mapping["source_input_stream_id"],
        "fixture_id": mapping["fixture_id"],
        "candidate_id": mapping["candidate_id"],
        "token_domain": TOKEN_DOMAIN,
        "candidate_ordering": OUTPUT_ORDERING,
        "candidate_outputs": candidate_outputs,
    }
    output_token_hash = canonical_hash(hash_material)
    return {
        "record_type": "gematria_solved_fixture_native_parity_record",
        "native_parity_record_id": f"stage5l-native-parity-{index:02d}",
        "native_fixture_id": f"stage5l-native-fixture-{index:02d}",
        "mapping_id": mapping["mapping_id"],
        "source_input_stream_id": mapping["source_input_stream_id"],
        "fixture_id": mapping["fixture_id"],
        "transform_family": mapping["transform_family"],
        "candidate_id": mapping["candidate_id"],
        "native_parity_status": "prepared",
        "readiness_status": "ready_for_future_cuda_approval",
        "candidate_shifts": list(CANDIDATE_SHIFTS),
        "candidate_ordering": OUTPUT_ORDERING,
        "candidate_major_outputs": candidate_outputs,
        "output_token_hash": output_token_hash,
        "output_text_hash": None,
        "output_text_hash_required": False,
        "output_token_hash_required": True,
        "hash_algorithm": HASH_ALGORITHM,
        "hash_material": hash_material,
        "separator_metadata_preserved": True,
        "token_kind_metadata_preserved": True,
        "stage4o_parity_expectation_linkage_status": mapping["stage4o_parity_expectation_linkage_status"],
        "score_summary_shape_required": True,
        "blockers": [REMAINING_APPROVAL_BLOCKER],
        "blocker_count": 1,
        "future_stage_approval_required": True,
        **COMMON_POLICY_FLAGS,
    }


def _shift_token(*, token: dict[str, Any], shift: int) -> dict[str, Any]:
    output = {
        "position": token["position"],
        "token_kind": token["token_kind"],
        "transformable": token["transformable"],
    }
    if token["transformable"]:
        output["index29"] = (int(token["index29"]) + shift) % 29
        output["raw_text"] = None
    else:
        output["index29"] = None
        output["raw_text"] = token.get("raw_text")
    return output
