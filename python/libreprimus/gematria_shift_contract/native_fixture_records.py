"""Stage 5H synthetic native Gematria mod-29 fixture preparation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from libreprimus.gematria_shift_contract.export import write_record_set, write_report, write_warnings
from libreprimus.gematria_shift_contract.models import (
    ARITHMETIC_DIRECTION,
    ARITHMETIC_FORMULA,
    COMMON_POLICY_FLAGS,
    FIXTURE_ID,
    FIXTURE_JSON,
    FIXTURES_PATH,
    OUTPUT_DIR,
    SEPARATOR_POLICY,
    STAGE5F_HASH,
)


SYNTHETIC_INPUT_TOKENS: tuple[dict[str, Any], ...] = (
    {"position": 0, "token_kind": "rune", "value": 0},
    {"position": 1, "token_kind": "rune", "value": 1},
    {"position": 2, "token_kind": "word_separator", "raw_text": " "},
    {"position": 3, "token_kind": "rune", "value": 28},
    {"position": 4, "token_kind": "rune", "value": 13},
    {"position": 5, "token_kind": "clause_separator", "raw_text": "."},
    {"position": 6, "token_kind": "rune", "value": 5},
)

SYNTHETIC_SHIFTS = (0, 1, 3, 13, 28)


def build_native_fixture_records(*, fixtures_out: Path = FIXTURES_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    """Build deterministic synthetic numeric Gematria mod-29 fixture records."""

    expected_outputs = [
        {
            "candidate_index": index,
            "shift": shift,
            "expected_output_tokens": shifted_tokens(SYNTHETIC_INPUT_TOKENS, shift),
        }
        for index, shift in enumerate(SYNTHETIC_SHIFTS)
    ]
    fixture_hash = fixture_expected_hash(SYNTHETIC_INPUT_TOKENS, expected_outputs)
    record: dict[str, Any] = {
        "record_type": "gematria_native_parity_fixture_record",
        "fixture_id": FIXTURE_ID,
        "native_fixture_prepared": True,
        "synthetic_numeric_gematria_fixture": True,
        "input_tokens": list(SYNTHETIC_INPUT_TOKENS),
        "shifts": list(SYNTHETIC_SHIFTS),
        "expected_outputs": expected_outputs,
        "expected_output_hash": fixture_hash,
        "stage5f_synthetic_hash": STAGE5F_HASH,
        "stage5f_hash_is_gematria_fixture_hash": fixture_hash == STAGE5F_HASH,
        "arithmetic_direction": ARITHMETIC_DIRECTION,
        "arithmetic_formula": ARITHMETIC_FORMULA,
        "separator_policy": SEPARATOR_POLICY,
        "intended_future_reference": "future_gematria_mod29_cuda_kernel_reference_not_experiment_result",
        "compatibility_notes": [
            "Stage 5F validates CUDA plumbing against uppercase Latin A-Z synthetic text only.",
            "This fixture uses numeric rune tokens in 0..28 and preserves separator tokens unshifted.",
        ],
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(fixtures_out, records)
    write_report(out_dir, FIXTURE_JSON, {"records": records})
    write_warnings(out_dir, [])
    return records


def shifted_tokens(tokens: tuple[dict[str, Any], ...] | list[dict[str, Any]], shift: int) -> list[dict[str, Any]]:
    """Return expected tokens under forward Gematria mod-29 shift semantics."""

    output: list[dict[str, Any]] = []
    for token in tokens:
        item = dict(token)
        if item.get("token_kind") == "rune":
            item["value"] = (int(item["value"]) + shift) % 29
        output.append(item)
    return output


def fixture_expected_hash(tokens: tuple[dict[str, Any], ...] | list[dict[str, Any]], outputs: list[dict[str, Any]]) -> str:
    """Return the deterministic fixture hash used by Stage 5H records."""

    material = {
        "fixture_id": FIXTURE_ID,
        "arithmetic_direction": ARITHMETIC_DIRECTION,
        "arithmetic_formula": ARITHMETIC_FORMULA,
        "input_tokens": list(tokens),
        "expected_outputs": outputs,
    }
    return hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
