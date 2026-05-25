"""Stage 5AP aggregate summary, next-stage, and research-summary builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import (
    FALSE_GUARDRAILS,
    STAGE_ID,
    TOKEN_BLOCK_ID,
    read_yaml,
    write_json,
    write_yaml,
)


def build_research_summary(
    *,
    source_lock: Path,
    transcription: Path,
    alphabet_registry: Path,
    mapping_preflight: Path,
    dwh_context: Path,
    out: Path,
) -> dict[str, Any]:
    source = read_yaml(source_lock)
    transcript = read_yaml(transcription)
    alphabet = read_yaml(alphabet_registry)
    mapping = read_yaml(mapping_preflight)
    dwh = read_yaml(dwh_context)
    record = {
        "record_type": "stage5ap_page49_51_source_lock_research_summary",
        "schema": "schemas/project-state/stage5ap-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "token_block_id": TOKEN_BLOCK_ID,
        "source_locked_page_image_count": source.get("source_locked_page_image_count", 0),
        "token_count": transcript.get("token_count", 0),
        "row_count": transcript.get("row_count", 0),
        "column_count": transcript.get("column_count", 0),
        "unique_token_count": transcript.get("unique_token_count", 0),
        "observed_suffix_count": alphabet.get("observed_suffix_count", 0),
        "lowercase_f_absent": alphabet.get("lowercase_f_absent", False),
        "primary_mapping_value_min": mapping.get("value_min"),
        "primary_mapping_value_max": mapping.get("value_max"),
        "primary_mapping_all_values_in_byte_range": mapping.get("all_values_in_byte_range", False),
        "dwh_context_status": dwh.get("context_status"),
        "research_result": "source_lock_and_preflight_only",
        "no_decode": True,
        "no_hash_preimage_search": True,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, record)
    return record


def build_next_stage_decision(
    *,
    source_lock: Path,
    transcription: Path,
    mapping_preflight: Path,
    out: Path,
) -> dict[str, Any]:
    source = read_yaml(source_lock)
    transcript = read_yaml(transcription)
    mapping = read_yaml(mapping_preflight)
    ready = (
        source.get("source_locked_page_image_count", 0) >= 3
        and transcript.get("token_count") == 256
        and transcript.get("row_count") == 32
        and transcript.get("column_count") == 8
        and mapping.get("all_values_in_byte_range") is True
    )
    selected_title = (
        "Stage 5AQ - Deep Research page 49-51 token-block, Deep Web Hash context, and exact token-to-value source-lock review"
        if ready
        else "Stage 5AQ - page 49-51 token-block source-lock gap closure"
    )
    record = {
        "record_type": "stage5ap_next_stage_decision",
        "schema": "schemas/project-state/stage5ap-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "source_stage_id": "stage-5ao-external",
        "selected_next_stage_title": selected_title,
        "selected_next_stage_short_name": "Stage 5AQ",
        "deep_research_next_ready": ready,
        "gap_closure_next_ready": not ready,
        "selection_reason": (
            "Token transcription, primary-60 mapping, and local page-image metadata hashes are present."
            if ready
            else "Token transcription is present but local page-image source-lock metadata is incomplete."
        ),
        "execution_enabled": False,
        "cuda_execution_enabled": False,
        "hash_preimage_search_enabled": False,
        "scored_experiment_enabled": False,
        "solve_claim": False,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, record)
    return record


def build_summary(
    *,
    source_lock: Path,
    image_provenance: Path,
    transcription: Path,
    coordinates: Path,
    alphabet_registry: Path,
    mapping_preflight: Path,
    null_control_plan: Path,
    dwh_context: Path,
    outguess_toolchain: Path,
    outguess_matrix: Path,
    outguess_historical: Path,
    outguess_guardrail: Path,
    research_summary: Path,
    next_stage_decision: Path,
    out: Path,
    results_dir: Path | None = None,
) -> dict[str, Any]:
    source = read_yaml(source_lock)
    provenance = read_yaml(image_provenance)
    transcript = read_yaml(transcription)
    coord = read_yaml(coordinates)
    alphabet = read_yaml(alphabet_registry)
    mapping = read_yaml(mapping_preflight)
    nulls = read_yaml(null_control_plan)
    dwh = read_yaml(dwh_context)
    toolchain = read_yaml(outguess_toolchain)
    matrix = read_yaml(outguess_matrix)
    historical = read_yaml(outguess_historical)
    guardrail = read_yaml(outguess_guardrail)
    research = read_yaml(research_summary)
    decision = read_yaml(next_stage_decision)
    summary = {
        "record_type": "stage5ap_summary",
        "schema": "schemas/project-state/stage5ap-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "token_block_id": TOKEN_BLOCK_ID,
        "source_lock_status": source.get("source_lock_status"),
        "source_locked_page_image_count": source.get("source_locked_page_image_count", 0),
        "page_image_provenance_records": provenance.get("page_image_record_count", 0),
        "row_count": transcript.get("row_count", 0),
        "column_count": transcript.get("column_count", 0),
        "token_count": transcript.get("token_count", 0),
        "unique_token_count": transcript.get("unique_token_count", 0),
        "first_character_counts": transcript.get("first_character_counts", {}),
        "coordinate_record_count": coord.get("coordinate_record_count", 0),
        "primary_alphabet_length": alphabet.get("primary_alphabet_length", 0),
        "observed_suffix_count": alphabet.get("observed_suffix_count", 0),
        "lowercase_f_absent": alphabet.get("lowercase_f_absent", False),
        "mapping_value_min": mapping.get("value_min"),
        "mapping_value_max": mapping.get("value_max"),
        "mapping_all_values_in_byte_range": mapping.get("all_values_in_byte_range", False),
        "null_control_count": nulls.get("null_control_count", 0),
        "dwh_context_status": dwh.get("context_status"),
        "outguess_toolchain_state": toolchain.get("toolchain_state"),
        "outguess_positive_control_matrix_records": matrix.get("matrix_record_count", 0),
        "outguess_synthetic_control_count": matrix.get("synthetic_control_count", 0),
        "outguess_historical_fixture_records": historical.get("historical_fixture_count", 0),
        "outguess_historical_fixture_ready_count": historical.get("historical_fixture_ready_count", 0),
        "outguess_guardrail_status": guardrail.get("guardrail_status"),
        "research_result": research.get("research_result"),
        "selected_next_stage_title": decision.get("selected_next_stage_title"),
        "deep_research_next_ready": decision.get("deep_research_next_ready", False),
        "canonical_token_transcription_created": True,
        "primary_60_mapping_preflight_created": True,
        "outguess_policy_created": True,
        "outguess_tool_execution_performed": False,
        "lp_page_outguess_run_performed": False,
        "no_decode": True,
        "no_text_interpretation": True,
        "no_hash_preimage_search": True,
        "no_solve_claim": True,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out, summary)
    if results_dir is not None:
        write_json(results_dir / "stage5ap_token_block_summary.json", summary)
    return summary
