"""Build token-buffer contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import write_record_set, write_report
from libreprimus.cuda_candidate_batch_abi.models import COMMON_FLAGS, OUTPUT_DIR, TOKEN_BUFFER_CONTRACT_PATH, TOKEN_BUFFER_REPORT_JSON


def build_token_buffer_contract(
    *,
    token_buffer_contract_out: Path = TOKEN_BUFFER_CONTRACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Define token, mask, separator, offset, and length surfaces."""

    rows = [
        (
            "token_buffer_header_v0",
            "header",
            "pod_struct_u32_fields",
            "not_applicable",
            "token_count>=0; fixture_count>=0; candidate_count>=0",
            "token_count",
            "token_offset",
            "4_byte_aligned",
            "Defines counts and offsets shared by all buffers.",
        ),
        (
            "token_values_buffer",
            "token_values",
            "int16",
            "separator_numeric_value=-1",
            "rune:0..28; separator:-1",
            "token_count",
            "token_offset",
            "2_byte_aligned",
            "Stores Gematria index-29 tokens and a sentinel for separators.",
        ),
        (
            "token_kind_buffer",
            "token_kind",
            "uint8",
            "separator_kind=2",
            "0=rune;1=payload;2=separator;3=unknown_preserved",
            "token_count",
            "token_offset",
            "1_byte_aligned",
            "Preserves token-kind metadata through output hashing.",
        ),
        (
            "transformable_mask_buffer",
            "transformable_mask",
            "uint8",
            "separator_mask=0",
            "0=not_transformable;1=transformable",
            "token_count",
            "token_offset",
            "1_byte_aligned",
            "Length must equal token_count; separators must be non-transformable.",
        ),
        (
            "separator_position_buffer",
            "separator_positions",
            "uint32",
            "not_applicable",
            "0..token_count-1",
            "separator_count",
            "separator_offset",
            "4_byte_aligned",
            "Optional index surface for validation and reset policies.",
        ),
        (
            "fixture_offset_buffer",
            "fixture_offsets",
            "uint32",
            "not_applicable",
            "0..token_count",
            "fixture_count",
            "fixture_offset",
            "4_byte_aligned",
            "Maps each fixture to its first token.",
        ),
        (
            "fixture_length_buffer",
            "fixture_lengths",
            "uint32",
            "not_applicable",
            "0..token_count",
            "fixture_count",
            "fixture_offset",
            "4_byte_aligned",
            "Maps each fixture to token length.",
        ),
        (
            "candidate_fixture_reference_buffer",
            "candidate_fixture_reference",
            "uint32",
            "not_applicable",
            "0..fixture_count-1",
            "candidate_count",
            "candidate_offset",
            "4_byte_aligned",
            "Maps each candidate-major row to the source fixture.",
        ),
    ]
    records = [
        {
            "record_type": "token_buffer_contract_record",
            "token_buffer_contract_id": f"stage5u-{buffer_id}",
            "buffer_id": buffer_id,
            "buffer_type": buffer_type,
            "element_type": element_type,
            "null_or_separator_encoding": encoding,
            "allowed_value_range": value_range,
            "length_field": length_field,
            "offset_field": offset_field,
            "alignment_requirement": alignment,
            "host_validation_required": True,
            "device_validation_required": False,
            "result_store_visibility": "compact_hashes_only",
            "separator_policy": "separator_numeric_value_minus_one_and_transformable_mask_zero",
            "token_kind_metadata_preserved_in_output_hash": True,
            "output_token_hashes_require_full_array_commit": False,
            "notes": notes,
            **COMMON_FLAGS,
        }
        for buffer_id, buffer_type, element_type, encoding, value_range, length_field, offset_field, alignment, notes in rows
    ]
    write_record_set(token_buffer_contract_out, records)
    write_report(out_dir, TOKEN_BUFFER_REPORT_JSON, {"records": records})
    return records
