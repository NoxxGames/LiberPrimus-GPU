"""Build and load Stage 5Q aggregate summaries."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.gematria_expansion_candidate_mapping.export import read_record_set, write_report, write_warnings
from libreprimus.gematria_expansion_candidate_mapping.models import (
    CANDIDATE_INVENTORY_PATH,
    COMMON_POLICY_FLAGS,
    EXPANSION_GATE_PATH,
    NATIVE_PARITY_PATH,
    OUTPUT_DIR,
    RESULT_STORE_PREFLIGHT_PATH,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    TOKEN_MAPPING_PATH,
)


def build_summary(
    *,
    candidate_inventory: Path = CANDIDATE_INVENTORY_PATH,
    token_mapping: Path = TOKEN_MAPPING_PATH,
    native_parity: Path = NATIVE_PARITY_PATH,
    result_store_preflight: Path = RESULT_STORE_PREFLIGHT_PATH,
    expansion_gate: Path = EXPANSION_GATE_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    """Build the committed and generated Stage 5Q summary."""

    inventory = read_record_set(candidate_inventory)
    mappings = read_record_set(token_mapping)
    native = read_record_set(native_parity)
    preflight = read_record_set(result_store_preflight)
    gate = read_record_set(expansion_gate)[0]
    candidate_status_counts = dict(Counter(str(record["candidate_status"]) for record in inventory))
    candidate_class_counts = dict(Counter(str(record["candidate_class"]) for record in inventory))
    mapping_status_counts = dict(Counter(str(record["mapping_status"]) for record in mappings))
    native_status_counts = dict(Counter(str(record["native_parity_status"]) for record in native))
    preflight_status_counts = dict(Counter(str(record["preflight_status"]) for record in preflight))
    payload = {
        "record_type": "stage5q_expansion_candidate_mapping_summary",
        "stage_id": "stage-5q",
        "status": "complete",
        "source_stage_id": "stage-5p",
        "candidate_inventory_records": len(inventory),
        "new_candidate_count": candidate_status_counts.get("candidate_for_mapping", 0),
        "already_consumed_control_records": candidate_status_counts.get("already_consumed_control", 0),
        "blocked_candidate_records": sum(
            value for key, value in candidate_status_counts.items() if key.startswith("blocked")
        ),
        "candidate_status_counts": candidate_status_counts,
        "candidate_class_counts": candidate_class_counts,
        "token_mapping_records": len(mappings),
        "mapped_count": mapping_status_counts.get("mapped", 0),
        "blocked_mapping_count": len(mappings) - mapping_status_counts.get("mapped", 0),
        "mapping_status_counts": mapping_status_counts,
        "native_parity_records": len(native),
        "native_parity_prepared_count": native_status_counts.get("prepared", 0),
        "blocked_native_parity_count": native_status_counts.get("blocked", 0),
        "native_parity_status_counts": native_status_counts,
        "result_store_preflight_records": len(preflight),
        "result_store_preflight_status_counts": preflight_status_counts,
        "stage4p_compatibility": all(record.get("stage4p_compatibility") is True for record in preflight),
        "stage4i_compatibility": all(record.get("stage4i_compatibility") is True for record in preflight),
        "stage5l_5m_5o_duplicate_exclusion_status": "exact_five_buffer_pack_labelled_as_consumed_controls_not_new_candidates",
        "output_hash_algorithm": "sha256_canonical_json_v1",
        "generated_body_publication_allowed": False,
        "method_status_upgrade_allowed": False,
        "stage5r_ready": gate["stage5r_ready"],
        "selected_next_stage": gate["selected_next_stage"],
        "next_stage": gate["selected_next_stage"],
        "selected_next_stage_reason": gate["selected_next_stage_reason"],
        "deep_research_recommended": gate["deep_research_recommended"],
        "broad_solved_fixture_cuda_status": gate["broad_solved_fixture_cuda_status"],
        "unsolved_page_cuda_status": gate["unsolved_page_cuda_status"],
        "source_paths_inspected": sorted({str(record["source_path"]) for record in inventory}),
        **COMMON_POLICY_FLAGS,
    }
    write_yaml(summary_out, payload)
    write_report(out_dir, SUMMARY_REPORT, payload)
    write_warnings(out_dir, [])
    return payload


def load_summary(path: Path = SUMMARY_PATH) -> dict[str, Any]:
    return read_yaml(path)
