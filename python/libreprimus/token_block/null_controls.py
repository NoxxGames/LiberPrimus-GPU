"""Null-control plan for Stage 5AP token-block follow-up."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import FALSE_GUARDRAILS, STAGE_ID, TOKEN_BLOCK_ID, write_yaml


def build_null_control_plan(*, out: Path) -> dict[str, Any]:
    controls = [
        {
            "control_id": "stage5ap-null-random-primary60-32x8",
            "control_type": "random_primary60_grid",
            "purpose": "Estimate chance structure in random 32x8 primary-60 token grids.",
            "execution_enabled": False,
        },
        {
            "control_id": "stage5ap-null-alphabet-order-permutation",
            "control_type": "alphabet_order_sensitivity",
            "purpose": "Check whether any claimed byte pattern depends on post-hoc alphabet order.",
            "execution_enabled": False,
        },
        {
            "control_id": "stage5ap-null-row-column-permutation",
            "control_type": "coordinate_order_sensitivity",
            "purpose": "Check whether row/column order choices change any later pattern claims.",
            "execution_enabled": False,
        },
        {
            "control_id": "stage5ap-null-lowercase-f-absence",
            "control_type": "missing_symbol_false_positive",
            "purpose": "Track lowercase f absence as an observation, not intentional evidence.",
            "execution_enabled": False,
        },
        {
            "control_id": "stage5ap-null-dwh-blind-hash",
            "control_type": "hash_context_blind_control",
            "purpose": "Prevent Deep Web Hash context from becoming a post-hoc hash/preimage search.",
            "execution_enabled": False,
        },
    ]
    record = {
        "record_type": "token_block_null_control_plan",
        "schema": "schemas/token-block/token-block-null-control-plan-v0.schema.json",
        "stage_id": STAGE_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "null_control_count": len(controls),
        "null_controls_required_before_hypothesis_execution": True,
        "execution_enabled": False,
        "hash_preimage_search_enabled": False,
        "scored_experiment_enabled": False,
        "records": controls,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, record)
    return record
