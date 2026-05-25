"""Deep Web Hash context record for the Stage 5AP token block."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import FALSE_GUARDRAILS, STAGE_ID, TOKEN_BLOCK_ID, write_yaml


def build_dwh_context(*, out: Path) -> dict[str, Any]:
    record = {
        "record_type": "token_block_dwh_context",
        "schema": "schemas/token-block/token-block-dwh-context-v0.schema.json",
        "stage_id": STAGE_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "context_label": "Deep Web Hash / DWH",
        "context_status": "review_only_external_deep_research_context",
        "source_context": "Stage 5AO external Deep Research report summarized by the Stage 5AP prompt.",
        "claims_preserved": [
            "The page 49-51 32x8 token block may be relevant to Deep Web Hash context.",
            "A primary-60 ASCII-like mapping is a preflight candidate only.",
        ],
        "blocked_actions": [
            "hash_preimage_search",
            "plaintext_decode",
            "hypothesis_execution",
            "scored_experiment",
            "cuda_execution",
        ],
        "required_next_review": [
            "exact token-to-value source-lock review",
            "page-image source provenance review",
            "source-backed DWH context review",
            "null-control definition before any pattern test",
        ],
        "execution_enabled": False,
        "hash_preimage_search_performed": False,
        "decode_attempted": False,
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, record)
    return record
