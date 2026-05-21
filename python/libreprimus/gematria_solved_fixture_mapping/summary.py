"""Aggregate Stage 5L solved-fixture-safe mapping summary."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.gematria_solved_fixture_mapping.export import read_record_set, write_report, write_warnings
from libreprimus.gematria_solved_fixture_mapping.models import (
    BLOCKERS_BEFORE,
    COMMON_POLICY_FLAGS,
    NATIVE_PARITY_PATH,
    NEXT_STAGE_BLOCKER_CLOSURE,
    NEXT_STAGE_EXECUTION,
    NEXT_STAGE_TOKEN_GAP,
    OUTPUT_DIR,
    OUTPUT_HASH_CONTRACT_PATH,
    SCORE_SUMMARY_SHAPE_PATH,
    SUMMARY_JSON,
    SUMMARY_PATH,
    TOKEN_MAPPING_PATH,
)


def build_summary(
    *,
    token_mapping: Path = TOKEN_MAPPING_PATH,
    native_parity: Path = NATIVE_PARITY_PATH,
    output_hash_contract: Path = OUTPUT_HASH_CONTRACT_PATH,
    score_summary_shape: Path = SCORE_SUMMARY_SHAPE_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    mapping_records = read_record_set(token_mapping)
    native_records = read_record_set(native_parity)
    hash_records = read_record_set(output_hash_contract)
    score_records = read_record_set(score_summary_shape)
    mapped_count = sum(1 for record in mapping_records if record.get("mapping_status") == "mapped")
    blocked_count = len(mapping_records) - mapped_count
    native_prepared_count = sum(
        1 for record in native_records if record.get("native_parity_status") == "prepared"
    )
    blockers_after = sorted(
        {
            str(blocker)
            for record in [*mapping_records, *native_records, *hash_records, *score_records]
            for blocker in record.get("blockers", [])
        }
    )
    blockers_before = list(BLOCKERS_BEFORE)
    blockers_resolved = sorted(set(blockers_before) - set(blockers_after))
    blockers_new = sorted(set(blockers_after) - set(blockers_before))
    mapping_status_counts = dict(
        sorted(Counter(str(record.get("mapping_status")) for record in mapping_records).items())
    )
    readiness_status_counts = dict(
        sorted(Counter(str(record.get("readiness_status")) for record in mapping_records).items())
    )
    next_stage, next_reason = _next_stage(mapped_count=mapped_count, blockers_after=blockers_after)
    summary: dict[str, Any] = {
        "record_type": "stage5l_solved_fixture_token_mapping_summary",
        "stage_id": "stage-5l",
        "status": "complete",
        "token_mapping_records": len(mapping_records),
        "solved_fixture_token_mapping_records": len(mapping_records),
        "mapped_count": mapped_count,
        "blocked_count": blocked_count,
        "token_mapping_status_counts": mapping_status_counts,
        "native_parity_fixture_records": len(native_records),
        "native_parity_prepared_count": native_prepared_count,
        "output_hash_contract_records": len(hash_records),
        "score_summary_shape_records": len(score_records),
        "blocker_count_before": len(blockers_before),
        "blockers_before": blockers_before,
        "blocker_count_after": len(blockers_after),
        "blockers_after": blockers_after,
        "blockers_resolved": blockers_resolved,
        "blockers_remaining": blockers_after,
        "blockers_newly_discovered": blockers_new,
        "readiness_status_counts": readiness_status_counts,
        "selected_next_stage": next_stage,
        "next_stage": next_stage,
        "selected_next_stage_reason": next_reason,
        "recommended_next_prompt": next_stage,
        "score_summary_contract": "stage4i",
        "result_store_contract": "stage5l",
        "output_hash_algorithm": "sha256_canonical_json_v1",
        "cross_stage_report_written": True,
        **COMMON_POLICY_FLAGS,
    }
    write_yaml(summary_out, summary)
    write_report(out_dir, SUMMARY_JSON, summary)
    write_warnings(out_dir, [])
    return summary


def load_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    payload = read_yaml(summary_path)
    if not isinstance(payload, dict):
        raise ValueError(f"summary must be a mapping: {summary_path}")
    return payload


def _next_stage(*, mapped_count: int, blockers_after: list[str]) -> tuple[str, str]:
    if mapped_count == 0:
        return (
            NEXT_STAGE_TOKEN_GAP,
            "Every mapping remains blocked for missing source-backed Gematria token values.",
        )
    if blockers_after == ["need_explicit_future_stage_approval"]:
        return (
            NEXT_STAGE_EXECUTION,
            "All non-execution blockers are closed; only explicit future-stage approval remains before a solved-fixture-safe CUDA parity run.",
        )
    return (
        NEXT_STAGE_BLOCKER_CLOSURE,
        "At least one mapping exists, but non-execution solved-fixture CUDA blockers remain.",
    )
