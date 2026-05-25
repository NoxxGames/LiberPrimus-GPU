"""Alphabet registry for Stage 5AP base-60 token mapping preflight."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import FALSE_GUARDRAILS, PRIMARY_ALPHABET, STAGE_ID, TOKEN_BLOCK_ID, read_yaml, write_yaml


def observed_suffixes(tokens: list[str]) -> list[str]:
    return sorted({token[1] for token in tokens}, key=lambda value: PRIMARY_ALPHABET.find(value))


def build_alphabet_registry(*, transcription: Path, out: Path) -> dict[str, Any]:
    source = read_yaml(transcription)
    tokens = [token for row in source["token_grid"] for token in row]
    observed = observed_suffixes(tokens)
    missing = [char for char in PRIMARY_ALPHABET if char not in observed]
    record = {
        "record_type": "token_block_alphabet_registry",
        "schema": "schemas/token-block/token-block-alphabet-registry-v0.schema.json",
        "stage_id": STAGE_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "primary_alphabet_id": "stage5ap-primary-60-ascii-candidate",
        "primary_alphabet": PRIMARY_ALPHABET,
        "primary_alphabet_length": len(PRIMARY_ALPHABET),
        "alphabet_candidate_status": "preflight_candidate_not_canonical",
        "allowed_first_characters": ["0", "1", "2", "3", "4"],
        "observed_suffixes": observed,
        "observed_suffix_count": len(observed),
        "missing_suffixes": missing,
        "lowercase_f_absent": "f" in missing,
        "suffix_order_declared": True,
        "mapping_formula": "int(first_character) * 60 + primary_alphabet.index(suffix_character)",
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, record)
    return record
