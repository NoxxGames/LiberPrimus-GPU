"""Build Stage 5Q expansion token-mapping records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.cpu_batch.solved_fixture_streams import tokens_from_fixture_expected_plaintext
from libreprimus.gematria_expansion_candidate_mapping.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expansion_candidate_mapping.models import (
    CANDIDATE_INVENTORY_PATH,
    COMMON_POLICY_FLAGS,
    OUTPUT_DIR,
    TARGET_KERNEL,
    TOKEN_DOMAIN,
    TOKEN_MAPPING_PATH,
    TOKEN_MAPPING_REPORT,
)


def canonical_hash(payload: Any) -> str:
    """Return the Stage 5Q stable SHA-256 hash over canonical JSON."""

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_token_mapping_records(
    *,
    candidate_inventory: Path = CANDIDATE_INVENTORY_PATH,
    token_mapping_out: Path = TOKEN_MAPPING_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build token mapping records for every Stage 5Q inventory row."""

    inventory = read_record_set(candidate_inventory)
    records = [_mapping_record(index=index, inventory_record=record) for index, record in enumerate(inventory)]
    write_record_set(token_mapping_out, records)
    write_report(out_dir, TOKEN_MAPPING_REPORT, {"records": records})
    return records


def _mapping_record(*, index: int, inventory_record: dict[str, Any]) -> dict[str, Any]:
    status = str(inventory_record["candidate_status"])
    if status != "candidate_for_mapping":
        return _blocked_mapping_record(index=index, inventory_record=inventory_record)
    tokens = tokens_from_fixture_expected_plaintext(resolve_repo_path(Path(str(inventory_record["source_path"]))))
    token_values: list[int | None] = []
    token_kinds: list[str] = []
    transformable_mask: list[bool] = []
    separator_positions: list[int] = []
    token_records: list[dict[str, Any]] = []
    blockers: list[str] = []
    for position, token in enumerate(tokens):
        token_kind = str(token.get("token_kind", "unknown"))
        is_rune = token_kind == "rune"
        token_kinds.append(token_kind)
        transformable_mask.append(is_rune)
        value = token.get("index29")
        if is_rune:
            if not isinstance(value, int) or value < 0 or value > 28:
                token_values.append(None)
                blockers.append("blocked_invalid_token_domain")
            else:
                token_values.append(value)
        else:
            token_values.append(None)
            separator_positions.append(position)
        token_records.append(
            {
                "position": position,
                "token_kind": token_kind,
                "index29": value if isinstance(value, int) else None,
                "latin_label": token.get("latin_label"),
                "raw_text": token.get("raw_text"),
                "transformable": is_rune,
            }
        )
    if len(transformable_mask) != len(tokens):
        blockers.append("blocked_transformable_mask_length_mismatch")
    mapping_status = "mapped" if not blockers else "blocked_invalid_token_domain"
    hash_material = {
        "candidate_inventory_id": inventory_record["candidate_inventory_id"],
        "fixture_id": inventory_record["fixture_id"],
        "source_input_stream_id": inventory_record["source_input_stream_id"],
        "token_domain": TOKEN_DOMAIN,
        "tokens": token_records,
        "transformable_mask": transformable_mask,
        "separator_positions": separator_positions,
    }
    return {
        "record_type": "gematria_expansion_token_mapping_record",
        "token_mapping_record_id": f"stage5q-token-mapping-{index:02d}",
        "candidate_inventory_id": inventory_record["candidate_inventory_id"],
        "fixture_id": inventory_record["fixture_id"],
        "candidate_id": inventory_record["candidate_id"],
        "source_input_stream_id": inventory_record["source_input_stream_id"],
        "source_transform_family": inventory_record["source_transform_family"],
        "target_kernel": TARGET_KERNEL,
        "executed_semantics_if_future_cuda": "gematria_shift_score_only",
        "original_transform_family_semantics_exercised": False,
        "source_backed_token_values": mapping_status == "mapped",
        "token_domain": TOKEN_DOMAIN,
        "token_values": token_values,
        "token_kinds": token_kinds,
        "transformable_mask": transformable_mask,
        "separator_positions": separator_positions,
        "token_records": token_records,
        "token_count": len(tokens),
        "transformable_token_count": sum(1 for item in transformable_mask if item),
        "mapping_status": mapping_status,
        "mapping_hash": canonical_hash(hash_material) if mapping_status == "mapped" else None,
        "blockers": blockers,
        "blocker_count": len(blockers),
        **COMMON_POLICY_FLAGS,
    }


def _blocked_mapping_record(*, index: int, inventory_record: dict[str, Any]) -> dict[str, Any]:
    candidate_status = str(inventory_record["candidate_status"])
    if candidate_status == "already_consumed_control":
        mapping_status = "blocked_already_consumed_control"
        blockers = ["blocked_already_consumed_stage5l_5m_5o_exact_pack"]
    elif candidate_status == "blocked_requires_separate_kernel_contract":
        mapping_status = "blocked_transform_family_requires_separate_kernel"
        blockers = ["blocked_original_transform_family_requires_separate_kernel_contract"]
    elif candidate_status == "blocked_raw_or_generated_source_only":
        mapping_status = "blocked_missing_source_tokens"
        blockers = ["blocked_raw_or_generated_source_only"]
    else:
        mapping_status = "blocked_missing_source_tokens"
        blockers = ["blocked_missing_source_tokens"]
    return {
        "record_type": "gematria_expansion_token_mapping_record",
        "token_mapping_record_id": f"stage5q-token-mapping-{index:02d}",
        "candidate_inventory_id": inventory_record["candidate_inventory_id"],
        "fixture_id": inventory_record["fixture_id"],
        "candidate_id": inventory_record["candidate_id"],
        "source_input_stream_id": inventory_record["source_input_stream_id"],
        "source_transform_family": inventory_record["source_transform_family"],
        "target_kernel": TARGET_KERNEL,
        "executed_semantics_if_future_cuda": "gematria_shift_score_only",
        "original_transform_family_semantics_exercised": False,
        "source_backed_token_values": False,
        "token_domain": TOKEN_DOMAIN,
        "token_values": [],
        "token_kinds": [],
        "transformable_mask": [],
        "separator_positions": [],
        "token_records": [],
        "token_count": 0,
        "transformable_token_count": 0,
        "mapping_status": mapping_status,
        "mapping_hash": None,
        "blockers": blockers,
        "blocker_count": len(blockers),
        **COMMON_POLICY_FLAGS,
    }
