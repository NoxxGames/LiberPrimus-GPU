"""Validate Stage 5U Candidate Batch ABI records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import read_mapping, read_record_set, read_report
from libreprimus.cuda_candidate_batch_abi.models import (
    ABI_GAP_CLOSURE_PATH,
    BAD_TRUE_FLAGS,
    BACKEND_SURFACE_CONTRACT_PATH,
    CANDIDATE_BATCH_ABI_PATH,
    EXPECTED_COUNTS,
    KEY_SCHEDULE_CONTRACT_PATH,
    NEXT_STAGE_DECISION_PATH,
    NEXT_STAGE_TITLE,
    OUTPUT_DIR,
    RESULT_STORE_COMPATIBILITY_PATH,
    SCORE_VECTOR_CONTRACT_PATH,
    STREAM_SCHEDULE_CONTRACT_PATH,
    SUMMARY_JSON,
    SUMMARY_PATH,
    TOKEN_BUFFER_CONTRACT_PATH,
    TOPK_OUTPUT_CONTRACT_PATH,
    TRANSFORM_PARAMETER_CONTRACT_PATH,
)


def validate_stage5u_results(
    *,
    candidate_batch_abi_path: Path = CANDIDATE_BATCH_ABI_PATH,
    token_buffer_contract_path: Path = TOKEN_BUFFER_CONTRACT_PATH,
    transform_parameter_contract_path: Path = TRANSFORM_PARAMETER_CONTRACT_PATH,
    key_schedule_contract_path: Path = KEY_SCHEDULE_CONTRACT_PATH,
    stream_schedule_contract_path: Path = STREAM_SCHEDULE_CONTRACT_PATH,
    score_vector_contract_path: Path = SCORE_VECTOR_CONTRACT_PATH,
    topk_output_contract_path: Path = TOPK_OUTPUT_CONTRACT_PATH,
    backend_surface_contract_path: Path = BACKEND_SURFACE_CONTRACT_PATH,
    result_store_compatibility_path: Path = RESULT_STORE_COMPATIBILITY_PATH,
    gap_closure_path: Path = ABI_GAP_CLOSURE_PATH,
    next_stage_decision_path: Path = NEXT_STAGE_DECISION_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, int | bool | str], list[str]]:
    """Return validation counts and errors for Stage 5U records."""

    record_sets = {
        "candidate_batch_abi_records": read_record_set(candidate_batch_abi_path),
        "token_buffer_contract_records": read_record_set(token_buffer_contract_path),
        "transform_parameter_contract_records": read_record_set(transform_parameter_contract_path),
        "key_schedule_contract_records": read_record_set(key_schedule_contract_path),
        "stream_schedule_contract_records": read_record_set(stream_schedule_contract_path),
        "score_vector_contract_records": read_record_set(score_vector_contract_path),
        "topk_output_contract_records": read_record_set(topk_output_contract_path),
        "backend_surface_contract_records": read_record_set(backend_surface_contract_path),
        "result_store_compatibility_records": read_record_set(result_store_compatibility_path),
        "abi_gap_closure_records": read_record_set(gap_closure_path),
        "next_stage_decision_records": read_record_set(next_stage_decision_path),
    }
    summary = read_mapping(summary_path)
    errors: list[str] = []
    counts: dict[str, int | bool | str] = {key: len(records) for key, records in record_sets.items()}
    for key, expected in EXPECTED_COUNTS.items():
        if counts.get(key) != expected:
            errors.append(f"{key}={counts.get(key)} expected {expected}")
    _validate_common_flags([record for records in record_sets.values() for record in records] + [summary], errors)
    _validate_abi(record_sets["candidate_batch_abi_records"], errors)
    _validate_token_buffers(record_sets["token_buffer_contract_records"], errors)
    _validate_transforms(record_sets["transform_parameter_contract_records"], errors)
    _validate_schedules(record_sets["key_schedule_contract_records"], record_sets["stream_schedule_contract_records"], errors)
    _validate_score_topk(record_sets["score_vector_contract_records"], record_sets["topk_output_contract_records"], errors)
    _validate_backends(record_sets["backend_surface_contract_records"], errors)
    _validate_result_store(record_sets["result_store_compatibility_records"], errors)
    _validate_gap_closure(record_sets["abi_gap_closure_records"], errors)
    selected = [record for record in record_sets["next_stage_decision_records"] if record.get("selected")]
    if len(selected) != 1:
        errors.append("exactly_one_next_stage_decision_must_be_selected")
    elif selected[0].get("recommended_stage_title") != NEXT_STAGE_TITLE:
        errors.append("unexpected_next_stage_decision")
    try:
        read_report(results_dir, SUMMARY_JSON)
    except FileNotFoundError:
        errors.append("missing_ignored_stage5u_summary_report")
    counts.update(
        {
            "stage5t_gap_count": int(summary.get("stage5t_gap_count", 0)),
            "stage5t_gaps_closed_by_contract_count": int(summary.get("stage5t_gaps_closed_by_contract_count", 0)),
            "stage5t_implementation_pending_count": int(summary.get("stage5t_implementation_pending_count", 0)),
            "recommended_next_stage_title": str(summary.get("recommended_next_stage_title", "")),
            "deep_research_recommended_next": summary.get("deep_research_recommended_next") is True,
        }
    )
    return counts, errors


def _validate_common_flags(records: list[dict[str, Any]], errors: list[str]) -> None:
    for record in records:
        label = str(record.get("record_type", "summary"))
        for flag in BAD_TRUE_FLAGS:
            if record.get(flag) is True:
                errors.append(f"{label} has forbidden true flag {flag}")
        if record.get("no_solve_claim") is not True:
            errors.append(f"{label} missing no_solve_claim=true")


def _validate_abi(records: list[dict[str, Any]], errors: list[str]) -> None:
    record = records[0]
    required = {"variable_length_token_buffers", "vigenere_key_schedule_buffers", "score_vector_outputs", "topk_candidate_outputs"}
    if not required.issubset(set(record.get("supported_surfaces", []))):
        errors.append("candidate_batch_abi_missing_required_surfaces")
    if record.get("cuda_execution_allowed") is not False or record.get("abi_scope") != "contract_only_no_execution":
        errors.append("candidate_batch_abi_must_be_contract_only_no_cuda")


def _validate_token_buffers(records: list[dict[str, Any]], errors: list[str]) -> None:
    buffers = {record["buffer_id"]: record for record in records}
    required = {
        "token_buffer_header_v0",
        "token_values_buffer",
        "token_kind_buffer",
        "transformable_mask_buffer",
        "separator_position_buffer",
        "fixture_offset_buffer",
        "fixture_length_buffer",
        "candidate_fixture_reference_buffer",
    }
    if required - set(buffers):
        errors.append(f"missing_token_buffers={sorted(required - set(buffers))}")
    token_values = buffers.get("token_values_buffer", {})
    mask = buffers.get("transformable_mask_buffer", {})
    if "0..28" not in str(token_values.get("allowed_value_range", "")):
        errors.append("token_values_missing_rune_range")
    if "token_count" not in str(mask.get("length_field", "")):
        errors.append("transformable_mask_length_must_match_token_count")


def _validate_transforms(records: list[dict[str, Any]], errors: list[str]) -> None:
    families = {record["family_id"]: record for record in records}
    required = {"shift_mod29", "reverse_gematria", "rotated_reverse_gematria", "affine_mod29", "vigenere_explicit_key", "prime_minus_one_stream"}
    if required - set(families):
        errors.append(f"missing_transform_families={sorted(required - set(families))}")
    if families.get("vigenere_explicit_key", {}).get("requires_key_schedule") is not True:
        errors.append("vigenere_must_require_key_schedule")
    if families.get("prime_minus_one_stream", {}).get("requires_stream_schedule") is not True:
        errors.append("prime_stream_must_require_stream_schedule")
    if any(record.get("implementation_allowed_now") for record in records):
        errors.append("transform_parameter_contract_must_not_allow_implementation_now")


def _validate_schedules(keys: list[dict[str, Any]], streams: list[dict[str, Any]], errors: list[str]) -> None:
    if not any("vigenere_explicit_key" in record.get("supported_families", []) for record in keys):
        errors.append("missing_vigenere_key_schedule")
    if not any(record.get("supports_prime_minus_one") for record in streams):
        errors.append("missing_prime_minus_one_stream_schedule")
    if any(record.get("cuda_execution_allowed") for record in [*keys, *streams]):
        errors.append("schedule_contract_must_not_allow_cuda_execution")


def _validate_score_topk(score: list[dict[str, Any]], topk: list[dict[str, Any]], errors: list[str]) -> None:
    components = {record["score_component_id"] for record in score}
    if "confidence_label" not in components or "output_token_hash" not in components:
        errors.append("score_vector_missing_stage4i_components")
    if any(record.get("triage_only") is not True for record in score):
        errors.append("score_vector_must_be_triage_only")
    if topk[0].get("stable_sort_required") is not True or topk[0].get("deterministic_across_backends") is not True:
        errors.append("topk_contract_must_be_deterministic")


def _validate_backends(records: list[dict[str, Any]], errors: list[str]) -> None:
    surfaces = {record["backend_surface_id"]: record for record in records}
    if "cuda_device_kernel_surface" not in surfaces or "python_orchestration_surface" not in surfaces:
        errors.append("backend_surfaces_missing_required_layers")
    if any(record.get("allowed_to_execute_cuda") for record in records):
        errors.append("backend_surfaces_must_not_allow_cuda_execution")
    if any(record.get("cxx_launches_python_workers") for record in records):
        errors.append("backend_surfaces_must_not_launch_python_workers_from_cxx")


def _validate_result_store(records: list[dict[str, Any]], errors: list[str]) -> None:
    if any(record.get("generated_body_publication_allowed") for record in records):
        errors.append("result_store_compatibility_must_not_publish_generated_bodies")
    if any(record.get("method_status_upgrade_allowed") for record in records):
        errors.append("result_store_compatibility_must_not_upgrade_method_status")


def _validate_gap_closure(records: list[dict[str, Any]], errors: list[str]) -> None:
    surfaces = {record["surface_id"] for record in records}
    expected = {"token_buffer_header", "key_schedule_buffer", "stream_schedule_buffer", "score_vector_shape", "top_k_output_shape"}
    if surfaces != expected:
        errors.append(f"gap_closure_surfaces={sorted(surfaces)} expected {sorted(expected)}")
    if any(record.get("implementation_pending") is not True for record in records):
        errors.append("gap_closure_must_record_implementation_pending")
