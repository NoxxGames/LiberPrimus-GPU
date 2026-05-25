"""Stage 5AR token case/glyph ambiguity policy."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import FALSE_GUARDRAILS, STAGE5AR_ID, TOKEN_BLOCK_ID, read_yaml, write_json, write_yaml

AMBIGUITY_CLASSES = [
    ("uppercase_I_lowercase_l", ["I", "l"]),
    ("uppercase_O_zero_0", ["O", "0"]),
    ("digit_1_uppercase_I_lowercase_l", ["1", "I", "l"]),
    ("uppercase_S_digit_5", ["S", "5"]),
    ("uppercase_Z_digit_2", ["Z", "2"]),
    ("uppercase_B_digit_8", ["B", "8"]),
    ("uppercase_G_digit_6", ["G", "6"]),
    ("lowercase_o_zero_0", ["o", "0"]),
    ("lowercase_q_g_p", ["q", "g", "p"]),
]


def build_case_policy(
    *,
    stage5ap_transcription: Path,
    pixel_coordinate_records: Path,
    results_dir: Path,
    out_policy: Path,
    out_ambiguities: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    transcription = read_yaml(stage5ap_transcription)
    coordinates = read_yaml(pixel_coordinate_records)
    rows = transcription["token_grid"]
    flat = [token for row in rows for token in row]
    coordinate_by_token = {
        record["token_index_0_based"]: f"r{record['global_row_index_1_based']:02d}c{record['global_column_index_1_based']:02d}"
        for record in coordinates.get("records", [])
    }
    ambiguity_records: list[dict[str, Any]] = []
    unresolved = 0
    for class_id, candidates in AMBIGUITY_CLASSES:
        affected_indexes = [
            index for index, token in enumerate(flat) if any(candidate in token for candidate in candidates)
        ]
        present = bool(affected_indexes)
        if present:
            unresolved += 1
        ambiguity_records.append(
            {
                "record_type": "token_case_ambiguity_record",
                "schema": "schemas/token-block/token-case-ambiguity-record-v0.schema.json",
                "stage_id": STAGE5AR_ID,
                "token_block_id": TOKEN_BLOCK_ID,
                "ambiguity_class": class_id,
                "canonical_symbol": "/".join(candidates),
                "ambiguous_symbol_candidates": candidates,
                "affected_token_count": len(affected_indexes),
                "affected_token_indexes_0_based": affected_indexes,
                "coordinate_refs": [coordinate_by_token[index] for index in affected_indexes if index in coordinate_by_token],
                "source_pixel_evidence_status": "coordinate_locked_review_required"
                if present
                else "class_absent_from_stage5ap_tokens",
                "decision_status": "requires_human_review" if present else "not_present",
                "decision_reason": "Stage 5AR records ambiguity; it does not alter Stage 5AP canonical transcription.",
                "requires_human_review": present,
                "canonical_transcription_changed": False,
                "solve_claim": False,
            }
        )
    policy = {
        "record_type": "token_case_policy",
        "schema": "schemas/token-block/token-case-policy-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "canonical_transcription_source": str(stage5ap_transcription).replace("\\", "/"),
        "canonical_transcription_changed": False,
        "silent_transcription_changes_allowed": False,
        "ambiguity_class_count": len(AMBIGUITY_CLASSES),
        "unresolved_ambiguity_class_count": unresolved,
        "requires_human_review": unresolved > 0,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "semantic_image_interpretation_performed": False,
        "no_decode": True,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    payload = {
        "record_type": "token_case_ambiguity_record_set",
        "schema": "schemas/token-block/token-case-ambiguity-record-v0.schema.json",
        "stage_id": STAGE5AR_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "ambiguity_record_count": len(ambiguity_records),
        "unresolved_ambiguity_class_count": unresolved,
        "canonical_transcription_changed": False,
        "records": ambiguity_records,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out_policy, policy)
    write_yaml(out_ambiguities, payload)
    write_json(results_dir / "token_case_ambiguity_report.json", payload)
    return policy, payload
