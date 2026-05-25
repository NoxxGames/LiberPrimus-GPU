"""Logical coordinate records for the Stage 5AP token block."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import FALSE_GUARDRAILS, STAGE_ID, TOKEN_BLOCK_ID, read_yaml, write_jsonl, write_yaml


def build_coordinate_records(*, transcription: Path, out: Path, results_dir: Path | None = None) -> dict[str, Any]:
    source = read_yaml(transcription)
    rows: list[list[str]] = source["token_grid"]
    records = [
        {
            "record_type": "token_block_coordinate_record",
            "stage_id": STAGE_ID,
            "token_block_id": TOKEN_BLOCK_ID,
            "token": token,
            "token_index_zero_based": row_index * len(row) + column_index,
            "row_index_zero_based": row_index,
            "row_index_one_based": row_index + 1,
            "column_index_zero_based": column_index,
            "column_index_one_based": column_index + 1,
            "logical_coordinate": f"r{row_index + 1:02d}c{column_index + 1:02d}",
            "source_page_candidate": "pages_49_to_51_unassigned",
            "page_assignment_status": "not_finalized_stage5ap",
            "pixel_coordinate_status": "not_available_stage5ap",
            "pixel_x": None,
            "pixel_y": None,
            "coordinate_review_required": True,
            "usable_as_experiment_seed": False,
            "trusted_as_canonical": False,
            "solve_claim": False,
        }
        for row_index, row in enumerate(rows)
        for column_index, token in enumerate(row)
    ]
    payload = {
        "record_type": "token_block_coordinate_record_set",
        "schema": "schemas/token-block/token-block-coordinate-record-v0.schema.json",
        "stage_id": STAGE_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "coordinate_system": "logical_grid_only",
        "row_count": source["row_count"],
        "column_count": source["column_count"],
        "coordinate_record_count": len(records),
        "page_boundaries_final": False,
        "pixel_coordinates_available": False,
        "coordinate_review_required": True,
        "records": records,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, payload)
    if results_dir is not None:
        write_jsonl(results_dir / "logical_coordinates.jsonl", records)
    return payload
