"""Stage 5H Gematria mod-29 shift_score contract generation."""

from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_shift_contract.export import write_record_set, write_report, write_warnings
from libreprimus.gematria_shift_contract.models import (
    ARITHMETIC_DIRECTION,
    ARITHMETIC_FORMULA,
    COMMON_POLICY_FLAGS,
    CONTRACT_ID,
    CONTRACT_JSON,
    CONTRACT_PATH,
    OUTPUT_DIR,
    OUTPUT_ORDERING,
    SEPARATOR_POLICY,
    STAGE5F_HASH,
    TOKEN_DOMAIN,
)


def build_contract_records(*, contract_out: Path = CONTRACT_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, object]]:
    """Build the production Gematria mod-29 shift_score contract record."""

    record: dict[str, object] = {
        "record_type": "gematria_shift_score_contract_record",
        "contract_id": CONTRACT_ID,
        "token_domain": TOKEN_DOMAIN,
        "token_domain_min": 0,
        "token_domain_max": 28,
        "transformable_token_kind": "rune",
        "non_transformable_token_kinds": [
            "word_separator",
            "clause_separator",
            "paragraph_separator",
            "segment_separator",
            "chapter_separator",
            "page_separator_or_marker",
            "whitespace",
            "unknown_symbol",
        ],
        "separator_policy": SEPARATOR_POLICY,
        "output_ordering": OUTPUT_ORDERING,
        "arithmetic_direction": ARITHMETIC_DIRECTION,
        "arithmetic_formula": ARITHMETIC_FORMULA,
        "candidate_shifts": [0, 1, 3, 13, 28],
        "candidate_shift_scope": "small_synthetic_native_fixture_set_not_broad_search",
        "score_summary_required_for_future_cuda": True,
        "stage5f_synthetic_hash": STAGE5F_HASH,
        "stage5f_hash_is_gematria_fixture_hash": False,
        "semantic_notes": [
            "The Stage 5F CUDA kernel remains uppercase Latin A-Z synthetic parity only.",
            "This contract defines future production numeric Gematria mod-29 token semantics.",
            "Forward Caesar adapter semantics in the existing CPU batch adapter use (token + shift) % 29.",
        ],
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(contract_out, records)
    write_report(out_dir, CONTRACT_JSON, {"records": records})
    write_warnings(out_dir, [])
    return records
