"""Canonical Stage 5AP token-block transcription records."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

from .models import FALSE_GUARDRAILS, STAGE_ID, TOKEN_BLOCK_ID, canonical_text, sha256_text, token_rows, write_json, write_yaml

TOKEN_RE = re.compile(r"^[0-4][0-9A-Za-z]$")


def build_transcription(*, out: Path, results_dir: Path | None = None) -> dict[str, Any]:
    """Write the canonical 32x8 token-block transcription."""

    rows = token_rows()
    flat = [token for row in rows for token in row]
    first_counts = Counter(token[0] for token in flat)
    token_records = [
        {
            "token_index_zero_based": index,
            "row_index_one_based": row_index + 1,
            "column_index_one_based": column_index + 1,
            "token": token,
        }
        for row_index, row in enumerate(rows)
        for column_index, token in enumerate(row)
        for index in [row_index * len(row) + column_index]
    ]
    invalid = [token for token in flat if not TOKEN_RE.match(token)]
    record = {
        "record_type": "token_block_transcription",
        "schema": "schemas/token-block/token-block-transcription-v0.schema.json",
        "stage_id": STAGE_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "source_context": "Stage 5AP user-supplied canonical transcription from the Stage 5AO external Deep Research context.",
        "review_state": "source_lock_candidate",
        "row_count": len(rows),
        "column_count": len(rows[0]) if rows else 0,
        "token_count": len(flat),
        "unique_token_count": len(set(flat)),
        "first_character_counts": dict(sorted(first_counts.items())),
        "invalid_token_count": len(invalid),
        "invalid_tokens": invalid,
        "canonical_text_sha256": sha256_text(canonical_text()),
        "token_grid": rows,
        "token_records": token_records,
        "decode_attempted": False,
        "text_interpretation_attempted": False,
        "usable_as_experiment_seed": False,
        "trusted_as_canonical": False,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, record)
    if results_dir is not None:
        write_json(results_dir / "canonical_token_grid.json", record)
        (results_dir / "canonical_token_grid.csv").write_text(
            "\n".join(",".join(row) for row in rows) + "\n",
            encoding="utf-8",
        )
    return record


def validate_transcription_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rows = record.get("token_grid", [])
    flat = [token for row in rows for token in row]
    if record.get("row_count") != 32:
        errors.append("row_count_not_32")
    if record.get("column_count") != 8:
        errors.append("column_count_not_8")
    if record.get("token_count") != 256 or len(flat) != 256:
        errors.append("token_count_not_256")
    if record.get("unique_token_count") != len(set(flat)):
        errors.append("unique_token_count_mismatch")
    if any(not TOKEN_RE.match(token) for token in flat):
        errors.append("invalid_token_shape")
    if record.get("decode_attempted") is not False:
        errors.append("decode_attempted_not_false")
    if record.get("solve_claim") is not False:
        errors.append("solve_claim_not_false")
    return errors
