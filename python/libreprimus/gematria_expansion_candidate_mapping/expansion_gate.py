"""Build Stage 5Q controlled expansion gate records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expansion_candidate_mapping.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expansion_candidate_mapping.models import (
    CANDIDATE_INVENTORY_PATH,
    COMMON_POLICY_FLAGS,
    EXPANSION_GATE_PATH,
    EXPANSION_GATE_REPORT,
    NATIVE_PARITY_PATH,
    NEXT_STAGE_BLOCKERS,
    NEXT_STAGE_DEEP_RESEARCH,
    NEXT_STAGE_READY,
    OUTPUT_DIR,
    RESULT_STORE_PREFLIGHT_PATH,
    TOKEN_MAPPING_PATH,
)


def build_expansion_gate_records(
    *,
    candidate_inventory: Path = CANDIDATE_INVENTORY_PATH,
    token_mapping: Path = TOKEN_MAPPING_PATH,
    native_parity: Path = NATIVE_PARITY_PATH,
    result_store_preflight: Path = RESULT_STORE_PREFLIGHT_PATH,
    expansion_gate_out: Path = EXPANSION_GATE_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build the Stage 5Q gate for future bounded CUDA parity."""

    inventory = read_record_set(candidate_inventory)
    mappings = read_record_set(token_mapping)
    native = read_record_set(native_parity)
    preflight = read_record_set(result_store_preflight)
    new_candidates = [record for record in inventory if record.get("candidate_status") == "candidate_for_mapping"]
    mapped = [record for record in mappings if record.get("mapping_status") == "mapped"]
    prepared = [record for record in native if record.get("native_parity_status") == "prepared"]
    ready_preflight = [record for record in preflight if record.get("preflight_status") == "ready_for_future_result_store_integration"]
    blockers: list[str] = []
    if not new_candidates:
        gate_status = "blocked_no_additional_candidates"
        next_stage = NEXT_STAGE_DEEP_RESEARCH
        stage5r_ready = False
        blockers.append("blocked_no_additional_candidates")
    elif len(mapped) != len(new_candidates):
        gate_status = "needs_candidate_mapping"
        next_stage = NEXT_STAGE_BLOCKERS
        stage5r_ready = False
        blockers.append("needs_candidate_mapping")
    elif len(prepared) != len(mapped):
        gate_status = "needs_native_parity_hashes"
        next_stage = NEXT_STAGE_BLOCKERS
        stage5r_ready = False
        blockers.append("needs_native_parity_hashes")
    elif len(ready_preflight) != len(mapped):
        gate_status = "needs_result_store_preflight"
        next_stage = NEXT_STAGE_BLOCKERS
        stage5r_ready = False
        blockers.append("needs_result_store_preflight")
    else:
        gate_status = "stage5r_ready_for_bounded_expanded_cuda_parity"
        next_stage = NEXT_STAGE_READY
        stage5r_ready = True
    records = [
        {
            "record_type": "gematria_expansion_gate_record",
            "expansion_gate_id": "stage5q-controlled-expansion-gate",
            "gate_status": gate_status,
            "stage5r_ready": stage5r_ready,
            "new_candidate_count": len(new_candidates),
            "mapped_count": len(mapped),
            "native_parity_prepared_count": len(prepared),
            "result_store_preflight_ready_count": len(ready_preflight),
            "already_consumed_control_count": sum(
                1 for record in inventory if record.get("candidate_status") == "already_consumed_control"
            ),
            "blocked_count": sum(
                1
                for record in inventory
                if str(record.get("candidate_status", "")).startswith("blocked")
            ),
            "remaining_blockers": blockers,
            "newly_discovered_blockers": [],
            "selected_next_stage": next_stage,
            "selected_next_stage_reason": _reason(stage5r_ready=stage5r_ready, blockers=blockers),
            "deep_research_recommended": next_stage == NEXT_STAGE_DEEP_RESEARCH,
            "broad_solved_fixture_cuda_status": "blocked_broad_scope",
            "unsolved_page_cuda_status": "blocked_unsolved",
            **COMMON_POLICY_FLAGS,
        }
    ]
    write_record_set(expansion_gate_out, records)
    write_report(out_dir, EXPANSION_GATE_REPORT, {"records": records})
    return records


def _reason(*, stage5r_ready: bool, blockers: list[str]) -> str:
    if stage5r_ready:
        return "Three additional direct-translation solved-fixture-safe token buffers were mapped, native parity hashes were prepared, and Stage 4P/Stage 4I preflight is ready without CUDA execution."
    if blockers == ["blocked_no_additional_candidates"]:
        return "No additional source-backed solved-fixture-safe token buffers were found, so Deep Research review is recommended before further CUDA expansion."
    return "Additional candidates exist, but mapping, native parity, or result-store preflight blockers remain."
