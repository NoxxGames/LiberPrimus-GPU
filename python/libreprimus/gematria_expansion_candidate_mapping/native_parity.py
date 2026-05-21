"""Build Stage 5Q native parity records for mapped expansion candidates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expansion_candidate_mapping.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expansion_candidate_mapping.models import (
    CANDIDATE_SHIFTS,
    COMMON_POLICY_FLAGS,
    HASH_ALGORITHM,
    NATIVE_PARITY_PATH,
    NATIVE_PARITY_REPORT,
    OUTPUT_DIR,
    OUTPUT_ORDERING,
    TOKEN_DOMAIN,
    TOKEN_MAPPING_PATH,
)
from libreprimus.gematria_expansion_candidate_mapping.token_mapping import canonical_hash


def build_native_parity_records(
    *,
    token_mapping: Path = TOKEN_MAPPING_PATH,
    native_parity_out: Path = NATIVE_PARITY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build CPU/native output-token hashes without CUDA execution."""

    mappings = read_record_set(token_mapping)
    records = [_native_record(index=index, mapping=record) for index, record in enumerate(mappings)]
    write_record_set(native_parity_out, records)
    write_report(out_dir, NATIVE_PARITY_REPORT, {"records": records})
    return records


def _native_record(*, index: int, mapping: dict[str, Any]) -> dict[str, Any]:
    if mapping.get("mapping_status") != "mapped":
        blockers = list(mapping.get("blockers", [])) or ["blocked_mapping_not_available"]
        return {
            "record_type": "gematria_expansion_native_parity_record",
            "native_parity_record_id": f"stage5q-native-parity-{index:02d}",
            "token_mapping_record_id": mapping["token_mapping_record_id"],
            "fixture_id": mapping["fixture_id"],
            "candidate_id": mapping["candidate_id"],
            "candidate_shifts": list(CANDIDATE_SHIFTS),
            "candidate_ordering": OUTPUT_ORDERING,
            "input_token_values": [],
            "transformable_mask": [],
            "token_kinds": [],
            "expected_output_token_values": [],
            "output_token_hash": None,
            "output_hash_algorithm": HASH_ALGORITHM,
            "separator_metadata_preserved": False,
            "token_kind_metadata_preserved": False,
            "native_parity_status": "blocked",
            "future_cuda_execution_allowed": False,
            "blockers": blockers,
            "blocker_count": len(blockers),
            **COMMON_POLICY_FLAGS,
        }
    candidate_outputs = []
    expected_output_token_values = []
    for candidate_index, shift in enumerate(CANDIDATE_SHIFTS):
        output_tokens = [_shift_token(token=token, shift=shift) for token in mapping["token_records"]]
        expected_output_token_values.append(
            [token.get("index29") if token.get("transformable") else None for token in output_tokens]
        )
        candidate_outputs.append(
            {
                "candidate_index": candidate_index,
                "shift": shift,
                "output_tokens": output_tokens,
            }
        )
    hash_material = {
        "contract_id": "stage5q-expansion-output-hash-contract-v0",
        "token_mapping_record_id": mapping["token_mapping_record_id"],
        "candidate_inventory_id": mapping["candidate_inventory_id"],
        "source_input_stream_id": mapping["source_input_stream_id"],
        "fixture_id": mapping["fixture_id"],
        "candidate_id": mapping["candidate_id"],
        "token_domain": TOKEN_DOMAIN,
        "candidate_ordering": OUTPUT_ORDERING,
        "candidate_outputs": candidate_outputs,
    }
    return {
        "record_type": "gematria_expansion_native_parity_record",
        "native_parity_record_id": f"stage5q-native-parity-{index:02d}",
        "token_mapping_record_id": mapping["token_mapping_record_id"],
        "fixture_id": mapping["fixture_id"],
        "candidate_id": mapping["candidate_id"],
        "candidate_shifts": list(CANDIDATE_SHIFTS),
        "candidate_ordering": OUTPUT_ORDERING,
        "input_token_values": mapping["token_values"],
        "transformable_mask": mapping["transformable_mask"],
        "token_kinds": mapping["token_kinds"],
        "expected_output_token_values": expected_output_token_values,
        "candidate_major_outputs": candidate_outputs,
        "output_token_hash": canonical_hash(hash_material),
        "hash_material": hash_material,
        "output_hash_algorithm": HASH_ALGORITHM,
        "separator_metadata_preserved": True,
        "token_kind_metadata_preserved": True,
        "native_parity_status": "prepared",
        "future_cuda_execution_allowed": False,
        "blockers": [],
        "blocker_count": 0,
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
