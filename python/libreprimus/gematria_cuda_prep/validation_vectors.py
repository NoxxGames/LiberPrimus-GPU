"""Stage 5I validation-vector records for future Gematria CUDA parity."""

from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_cuda_prep.export import write_record_set, write_report, write_warnings
from libreprimus.gematria_cuda_prep.models import (
    COMMON_POLICY_FLAGS,
    NATIVE_FIXTURE_HASH,
    OUTPUT_DIR,
    STAGE5F_HASH,
    VALIDATION_VECTOR_ID,
    VALIDATION_VECTORS_JSON,
    VALIDATION_VECTORS_PATH,
)

INPUT_TOKEN_VALUES = [0, 1, 0, 28, 13, 0, 5]
TRANSFORMABLE_MASK = [1, 1, 0, 1, 1, 0, 1]
TOKEN_KINDS = ["rune", "rune", "word_separator", "rune", "rune", "clause_separator", "rune"]
SHIFTS = [0, 1, 3, 13, 28]
EXPECTED_OUTPUTS = [
    {"candidate_index": 0, "shift": 0, "output_token_values": [0, 1, 0, 28, 13, 0, 5]},
    {"candidate_index": 1, "shift": 1, "output_token_values": [1, 2, 0, 0, 14, 0, 6]},
    {"candidate_index": 2, "shift": 3, "output_token_values": [3, 4, 0, 2, 16, 0, 8]},
    {"candidate_index": 3, "shift": 13, "output_token_values": [13, 14, 0, 12, 26, 0, 18]},
    {"candidate_index": 4, "shift": 28, "output_token_values": [28, 0, 0, 27, 12, 0, 4]},
]


def build_validation_vector_records(
    *,
    validation_vectors_out: Path = VALIDATION_VECTORS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    """Build validation-vector records from the Stage 5H native fixture."""

    record: dict[str, object] = {
        "record_type": "gematria_cuda_validation_vector_record",
        "validation_vector_id": VALIDATION_VECTOR_ID,
        "input_token_values": INPUT_TOKEN_VALUES,
        "transformable_mask": TRANSFORMABLE_MASK,
        "token_kinds": TOKEN_KINDS,
        "shifts": SHIFTS,
        "expected_outputs": EXPECTED_OUTPUTS,
        "expected_fixture_hash": NATIVE_FIXTURE_HASH,
        "stage5f_synthetic_hash": STAGE5F_HASH,
        "stage5f_hash_is_gematria_fixture_hash": False,
        "separator_placeholder_policy": (
            "Separator placeholders use value 0 only as inert buffer material; "
            "transformable_mask=0 prevents arithmetic and host records preserve token kinds."
        ),
        "separator_positions": [2, 5],
        "host_side_result_metadata_required": True,
        "candidate_major_output_order": True,
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(validation_vectors_out, records)
    write_report(out_dir, VALIDATION_VECTORS_JSON, {"records": records})
    write_warnings(out_dir, [])
    return records
