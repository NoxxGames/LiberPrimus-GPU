"""Primary-60 byte mapping preflight for Stage 5AP tokens."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import FALSE_GUARDRAILS, PRIMARY_ALPHABET, STAGE_ID, TOKEN_BLOCK_ID, read_yaml, write_json, write_yaml


def token_to_value(token: str, alphabet: str = PRIMARY_ALPHABET) -> int:
    return int(token[0]) * len(alphabet) + alphabet.index(token[1])


def build_mapping_preflight(
    *,
    transcription: Path,
    alphabet_registry: Path,
    out: Path,
    results_dir: Path | None = None,
) -> dict[str, Any]:
    source = read_yaml(transcription)
    alphabet = read_yaml(alphabet_registry)["primary_alphabet"]
    rows = source["token_grid"]
    value_records = [
        {
            "token": token,
            "row_index_one_based": row_index + 1,
            "column_index_one_based": column_index + 1,
            "suffix_index": alphabet.index(token[1]),
            "mapped_value": token_to_value(token, alphabet),
        }
        for row_index, row in enumerate(rows)
        for column_index, token in enumerate(row)
    ]
    values = [record["mapped_value"] for record in value_records]
    payload = {
        "record_type": "token_block_mapping_preflight",
        "schema": "schemas/token-block/token-block-mapping-preflight-v0.schema.json",
        "stage_id": STAGE_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "mapping_id": "stage5ap-primary-60-byte-preflight",
        "mapping_status": "preflight_only",
        "mapping_formula": "int(first_character) * 60 + suffix_index",
        "alphabet": alphabet,
        "alphabet_length": len(alphabet),
        "token_count": len(value_records),
        "value_min": min(values),
        "value_max": max(values),
        "all_values_in_byte_range": all(0 <= value <= 255 for value in values),
        "known_mapping_checks": [
            {"token": "00", "expected_value": 0, "actual_value": token_to_value("00", alphabet), "passed": token_to_value("00", alphabet) == 0},
            {"token": "4F", "expected_value": 255, "actual_value": token_to_value("4F", alphabet), "passed": token_to_value("4F", alphabet) == 255},
        ],
        "value_records": value_records,
        "decode_attempted": False,
        "hash_preimage_search_performed": False,
        "hypothesis_execution_performed": False,
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, payload)
    if results_dir is not None:
        write_json(results_dir / "token_byte_preflight_primary_60.json", payload)
    return payload


def validate_mapping_preflight(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if record.get("token_count") != 256:
        errors.append("mapping_token_count_not_256")
    if record.get("value_min") != 0:
        errors.append("mapping_value_min_not_0")
    if record.get("value_max") != 255:
        errors.append("mapping_value_max_not_255")
    if record.get("all_values_in_byte_range") is not True:
        errors.append("mapping_values_outside_byte_range")
    checks = {check["token"]: check for check in record.get("known_mapping_checks", [])}
    if checks.get("00", {}).get("actual_value") != 0:
        errors.append("mapping_00_not_0")
    if checks.get("4F", {}).get("actual_value") != 255:
        errors.append("mapping_4f_not_255")
    if record.get("decode_attempted") is not False:
        errors.append("mapping_decode_attempted")
    if record.get("solve_claim") is not False:
        errors.append("mapping_solve_claim_not_false")
    return errors
