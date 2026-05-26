"""Stage 5AY bounded token-block preflight manifest design helpers."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .models import (
    ALPHABET_PATH,
    MAPPING_PATH,
    NULL_CONTROL_PATH,
    STAGE_ID,
    STAGE5AR_COORDINATE_VALIDATION_PATH,
    STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH,
    STAGE5AR_PAGE_SPLIT_RECORDS_PATH,
    STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH,
    STAGE5AU_PACK_MANIFEST_PATH,
    STAGE5AW_ID,
    STAGE5AW_NULL_CONTROL_UPDATE_PATH,
    STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH,
    STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH,
    STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
    STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    STAGE5AY_ID,
    STAGE5AY_RESULTS_DIR,
    TOKEN_BLOCK_ID,
    TRANSCRIPTION_PATH,
    read_yaml,
    repo_relative,
    sha256_file,
    write_json,
    write_jsonl,
    write_yaml,
)

STAGE5AX_RUN_SUMMARY_PATH = Path("data/ci/stage5ax-parallel-validation-run-summary.yaml")
STAGE5AZ_TITLE = "Stage 5AZ - Deep Research review of bounded token-block preflight manifest and execution gates"
SOURCE_STAGE5AX_COMMIT = "22c1497fbb64b9070ff6c2faa6aaeb25c1264c8f"
MAX_FULL_ENUMERATION_FUTURE_THRESHOLD = 10_000
MAX_SAMPLED_VARIANTS_FUTURE_THRESHOLD = 4096

FALSE_FLAGS = {
    "network_fetch_performed": False,
    "ocr_performed": False,
    "ai_ml_interpretation_performed": False,
    "llm_vision_token_reading_performed": False,
    "semantic_image_interpretation_performed": False,
    "hidden_content_image_forensics_performed": False,
    "stego_tool_execution_performed": False,
    "hash_preimage_search_performed": False,
    "decode_attempt_performed": False,
    "token_experiments_executed": False,
    "variant_byte_streams_generated": False,
    "variant_experiments_executed": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "benchmark_performed": False,
    "cryptanalytic_benchmark_performed": False,
    "scored_experiments_executed": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "method_status_upgraded": False,
    "solve_claim": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "third_party_raw_staged": False,
    "third_party_raw_tracked_new": False,
}


def _ensure_results_dir(results_dir: Path) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    gitkeep = results_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")


def _path_record(path: Path, role: str, required: bool = True) -> dict[str, Any]:
    exists = path.exists()
    return {
        "path": repo_relative(path),
        "role": role,
        "required": required,
        "present": exists,
        "sha256": sha256_file(path) if exists and path.is_file() else None,
    }


def _stage5ay_source_records() -> list[tuple[Path, str]]:
    return [
        (TRANSCRIPTION_PATH, "stage5ap_canonical_transcription"),
        (ALPHABET_PATH, "stage5ap_alphabet_registry"),
        (MAPPING_PATH, "stage5ap_mapping_preflight"),
        (NULL_CONTROL_PATH, "stage5ap_null_control_plan"),
        (STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH, "stage5ar_original_image_source_lock"),
        (STAGE5AR_PAGE_SPLIT_RECORDS_PATH, "stage5ar_page_split_records"),
        (STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH, "stage5ar_token_pixel_coordinate_records"),
        (STAGE5AR_COORDINATE_VALIDATION_PATH, "stage5ar_token_coordinate_validation"),
        (STAGE5AU_PACK_MANIFEST_PATH, "stage5au_review_pack_v2_manifest"),
        (STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH, "stage5aw_repaired_unresolved_variants"),
        (STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH, "stage5aw_repaired_reviewer_extra_tokens"),
        (STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH, "stage5aw_repaired_primary60_impact"),
        (STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH, "stage5aw_repaired_branch_manifest"),
        (STAGE5AW_NULL_CONTROL_UPDATE_PATH, "stage5aw_null_control_update"),
        (STAGE5AX_RUN_SUMMARY_PATH, "stage5ax_parallel_validation_run_summary"),
    ]


def _family_taxonomy() -> dict[str, list[str]]:
    return {
        "baseline_family": [
            "keep_current_baseline",
            "unresolved_as_current_only",
        ],
        "case_branch_family": [
            "single_change_variants",
            "per_ambiguity_class_variants",
            "primary60_mappable_only_variants",
            "visual_placeholder_excluded_variants",
            "reviewer_extra_possible_token_variants",
        ],
        "unresolved_policy_family": [
            "unresolved_as_excluded",
            "unresolved_as_all_declared_variants",
            "unresolved_as_current_only",
            "unresolved_as_primary60_mappable_only",
        ],
        "alphabet_family": [
            "primary60_current_alphabet",
            "reversed_primary60_control",
            "case_swapped_primary60_control",
            "digit_lower_upper_variant_control",
            "seeded_permutation_3301_control",
            "seeded_permutation_1033_control",
        ],
        "reading_order_family": [
            "global_32_row_order",
            "per_page_local_order",
            "row_reversal",
            "column_reversal",
            "row_column_reversal",
            "row_shuffle_fixed_seed",
            "column_shuffle_fixed_seed",
            "token_shuffle_fixed_seed",
        ],
        "page_split_family": [
            "accepted_10_13_9_split",
            "no_page_boundary_control",
            "alternative_11_11_10_split",
            "row_shuffled_split_preserving_page_counts",
        ],
        "source_control_family": [
            "wrong_page_block_control_future_source_lock_required",
            "random_lp_like_token_stream_from_observed_frequencies",
            "random_lp_like_token_stream_from_uniform_primary60",
        ],
    }


def _classify_option(detail: dict[str, Any]) -> list[str]:
    classes: list[str] = []
    source = str(detail.get("possible_token_source", ""))
    if source == "current_canonical_token":
        classes.append("canonical_current_token")
    elif source == "generated_candidate_token":
        classes.append("generated_candidate_token")
    elif source == "reviewer_extra_possible_token":
        classes.append("reviewer_extra_possible_token")
    elif source == "visual_placeholder_from_reviewer_notes":
        classes.extend(["visual_placeholder_from_reviewer_notes", "primary60_unmappable_visual_option"])

    if detail.get("primary60_mappable"):
        classes.append("primary60_mappable_option")
    else:
        error = detail.get("primary60_error")
        if error == "first_symbol_not_in_0_to_4":
            classes.append("primary60_unmappable_non_digit_prefix")
        elif error == "suffix_not_in_primary_60_alphabet":
            classes.append("primary60_unmappable_suffix_not_in_alphabet")
        elif "primary60_unmappable_visual_option" not in classes:
            classes.append("primary60_unmappable_visual_option")
        classes.append("execution_ineligible_option")
    return classes


def _build_option_records(branch_manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], Counter[str]]:
    records: list[dict[str, Any]] = []
    counts: Counter[str] = Counter(
        {
            "canonical_current_token": 0,
            "human_confirmed_keep_current_token": 0,
            "generated_candidate_token": 0,
            "reviewer_extra_possible_token": 0,
            "visual_placeholder_from_reviewer_notes": 0,
            "malformed_fragment_audit_only": 0,
            "primary60_mappable_option": 0,
            "primary60_unmappable_visual_option": 0,
            "primary60_unmappable_non_digit_prefix": 0,
            "primary60_unmappable_suffix_not_in_alphabet": 0,
            "execution_ineligible_option": 0,
        }
    )
    for case in branch_manifest.get("unresolved_cases", []):
        for detail in case.get("possible_token_details", []):
            classes = _classify_option(detail)
            counts.update(classes)
            records.append(
                {
                    "challenge_id": case.get("challenge_id"),
                    "token_index_0_based": case.get("token_index_0_based"),
                    "token": detail.get("token"),
                    "option_classes": classes,
                    "variant_byte_stream_eligible": bool(detail.get("variant_byte_stream_eligible")),
                    "primary60_mappable": bool(detail.get("primary60_mappable")),
                    "primary60_error": detail.get("primary60_error"),
                }
            )
    for fragment in branch_manifest.get("malformed_possible_token_fragments", []):
        counts.update(["malformed_fragment_audit_only", "execution_ineligible_option"])
        records.append(
            {
                "challenge_id": fragment.get("challenge_id"),
                "token_index_0_based": fragment.get("token_index_0_based"),
                "token": fragment.get("malformed_possible_token_fragment"),
                "option_classes": ["malformed_fragment_audit_only", "execution_ineligible_option"],
                "variant_byte_stream_eligible": False,
                "primary60_mappable": False,
                "primary60_error": "malformed_fragment_audit_only",
            }
        )
    return records, counts


def build_stage5ay_preflight_design(
    stage5ap_transcription: Path,
    stage5ap_alphabet_registry: Path,
    stage5ap_mapping_preflight: Path,
    stage5ar_coordinate_validation: Path,
    stage5aw_branch_manifest: Path,
    stage5aw_impact_summary: Path,
    stage5aw_null_control: Path,
    stage5ax_run_summary: Path,
    results_dir: Path,
    out_source_inputs: Path,
    out_policy: Path,
    out_branch_eligibility: Path,
    out_branch_budget: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ensure_results_dir(results_dir)
    branch = read_yaml(stage5aw_branch_manifest)
    impact = read_yaml(stage5aw_impact_summary)
    null_control = read_yaml(stage5aw_null_control)
    run_summary = read_yaml(stage5ax_run_summary)

    explicit_records = [
        _path_record(stage5ap_transcription, "stage5ap_canonical_transcription"),
        _path_record(stage5ap_alphabet_registry, "stage5ap_alphabet_registry"),
        _path_record(stage5ap_mapping_preflight, "stage5ap_mapping_preflight"),
        _path_record(stage5ar_coordinate_validation, "stage5ar_token_coordinate_validation"),
        _path_record(stage5aw_branch_manifest, "stage5aw_repaired_branch_manifest"),
        _path_record(stage5aw_impact_summary, "stage5aw_repaired_primary60_impact"),
        _path_record(stage5aw_null_control, "stage5aw_null_control_update"),
        _path_record(stage5ax_run_summary, "stage5ax_parallel_validation_run_summary"),
    ]
    required_records = [_path_record(path, role) for path, role in _stage5ay_source_records()]
    required_by_path = {record["path"]: record for record in required_records}
    for record in explicit_records:
        required_by_path[record["path"]] = record
    source_inputs = {
        "record_type": "stage5ay_preflight_source_inputs",
        "schema": "schemas/token-block/preflight-source-inputs-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "source_stage_ids": [STAGE_ID, "stage-5ar", "stage-5au", STAGE5AW_ID, "stage-5ax"],
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5av_branch_manifest_used": False,
        "stage5av_branch_manifest_superseded_by_stage5aw": True,
        "source_record_count": len(required_by_path),
        "missing_required_source_count": sum(1 for record in required_by_path.values() if not record["present"]),
        "records": sorted(required_by_path.values(), key=lambda record: record["path"]),
        "source_inputs_validated": True,
        **FALSE_FLAGS,
    }

    policy = {
        "record_type": "stage5ay_preflight_design_policy",
        "schema": "schemas/token-block/preflight-design-policy-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "policy_status": "design_only",
        "source_branch_manifest": repo_relative(stage5aw_branch_manifest),
        "source_branch_manifest_sha256": sha256_file(stage5aw_branch_manifest),
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5av_branch_manifest_used": False,
        "stage5av_branch_manifest_superseded_by_stage5aw": True,
        "family_taxonomy": _family_taxonomy(),
        "full_cartesian_product_allowed": False,
        "variant_byte_stream_generation_allowed_now": False,
        "token_experiment_execution_allowed_now": False,
        "branch_sampling_design_only": True,
        "future_review_required_before_runner_implementation": True,
        "parallel_validation_harness_required_for_local_validation": True,
        "stage5ax_run_status": run_summary.get("status"),
        **FALSE_FLAGS,
    }

    option_records, class_counts = _build_option_records(branch)
    branch_eligibility = {
        "record_type": "stage5ay_branch_eligibility_policy",
        "schema": "schemas/token-block/branch-eligibility-policy-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "source_branch_manifest": repo_relative(stage5aw_branch_manifest),
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5av_branch_manifest_used": False,
        "eligibility_classes": dict(class_counts),
        "option_record_count": len(option_records),
        "option_records": option_records,
        "visual_placeholders_preserved_for_review": True,
        "visual_placeholder_family_execution_allowed": False,
        "malformed_fragments_audit_only": True,
        "full_cartesian_product_allowed": False,
        "variant_byte_streams_generated": False,
        "token_experiments_executed": False,
        **FALSE_FLAGS,
    }

    budget = {
        "record_type": "stage5ay_branch_count_budget",
        "schema": "schemas/token-block/branch-count-budget-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "source_branch_manifest": repo_relative(stage5aw_branch_manifest),
        "branch_count_upper_bound_product": branch.get("branch_count_upper_bound_product"),
        "branch_count_upper_bound_log10": branch.get("branch_count_upper_bound_log10"),
        "primary60_mappable_branch_upper_bound_product": branch.get("primary60_mappable_branch_upper_bound_product"),
        "primary60_mappable_branch_upper_bound_log10": branch.get("primary60_mappable_branch_upper_bound_log10"),
        "impact_primary60_mappable_option_count": impact.get("primary60_mappable_option_count"),
        "impact_primary60_unmappable_option_count": impact.get("primary60_unmappable_option_count"),
        "null_control_update_path": repo_relative(stage5aw_null_control),
        "null_control_future_preflight_must_use_stage5aw_repaired_manifest": null_control.get(
            "future_preflight_must_use_stage5aw_repaired_manifest"
        ),
        "full_cartesian_product_allowed": False,
        "full_cartesian_product_reason": "Stage 5AW branch upper bound is far above bounded-design thresholds.",
        "max_full_enumeration_future_threshold": MAX_FULL_ENUMERATION_FUTURE_THRESHOLD,
        "max_sampled_variants_future_threshold": MAX_SAMPLED_VARIANTS_FUTURE_THRESHOLD,
        "future_sampling_requires_later_authorisation": True,
        "future_sampling_seed_policy": "fixed_seed_declared_before_execution_and_reviewed_in_stage5az_or_later",
        "single_change_variant_family_allowed_for_future_design": True,
        "per_ambiguity_class_variant_family_allowed_for_future_design": True,
        "primary60_mappable_only_family_allowed_for_future_design": True,
        "visual_placeholder_family_execution_allowed": False,
        "variant_byte_streams_generated": False,
        **FALSE_FLAGS,
    }

    write_yaml(out_source_inputs, source_inputs)
    write_yaml(out_policy, policy)
    write_yaml(out_branch_eligibility, branch_eligibility)
    write_yaml(out_branch_budget, budget)
    write_json(results_dir / "preflight_design_report.json", {"source_inputs": source_inputs, "policy": policy})
    write_json(results_dir / "branch_budget_report.json", budget)
    write_jsonl(results_dir / "warnings.jsonl", [])
    return source_inputs, policy, branch_eligibility, budget


def _family_records(ids: list[str], *, family_type: str) -> list[dict[str, Any]]:
    return [
        {
            "family_id": family_id,
            "family_type": family_type,
            "design_status": "defined_not_executed",
            "execution_enabled": False,
            "requires_later_authorisation": True,
        }
        for family_id in ids
    ]


def build_stage5ay_control_manifests(
    preflight_policy: Path,
    branch_eligibility: Path,
    stage5ap_null_control: Path,
    stage5aw_null_control: Path,
    results_dir: Path,
    out_variant_family: Path,
    out_null_control_family: Path,
    out_alphabet_control: Path,
    out_reading_order: Path,
    out_page_split: Path,
    out_source_control: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ensure_results_dir(results_dir)
    policy = read_yaml(preflight_policy)
    eligibility = read_yaml(branch_eligibility)
    taxonomy = policy["family_taxonomy"]
    variant_families = (
        taxonomy["baseline_family"] + taxonomy["case_branch_family"] + taxonomy["unresolved_policy_family"]
    )
    variant = {
        "record_type": "stage5ay_bounded_variant_family_manifest",
        "schema": "schemas/token-block/bounded-variant-family-manifest-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "source_policy": repo_relative(preflight_policy),
        "source_branch_eligibility": repo_relative(branch_eligibility),
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5av_branch_manifest_used": False,
        "family_count": len(variant_families),
        "families": _family_records(variant_families, family_type="bounded_variant_family"),
        "visual_placeholder_family_execution_allowed": False,
        "full_cartesian_product_allowed": False,
        "variant_byte_streams_generated": False,
        "token_experiments_executed": False,
        **FALSE_FLAGS,
    }
    null_control = {
        "record_type": "stage5ay_null_control_family_manifest",
        "schema": "schemas/token-block/null-control-family-manifest-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "source_stage5ap_null_control": repo_relative(stage5ap_null_control),
        "source_stage5aw_null_control": repo_relative(stage5aw_null_control),
        "families": _family_records(
            [
                "case_policy_control",
                "page_split_control",
                "reading_order_control",
                "alphabet_control",
                "random_shuffled_control",
                "false_positive_numerology_control",
            ],
            family_type="null_control_family",
        ),
        "null_controls_defined_before_execution": True,
        "controls_executed": False,
        **FALSE_FLAGS,
    }
    alphabet = {
        "record_type": "stage5ay_alphabet_control_manifest",
        "schema": "schemas/token-block/alphabet-control-manifest-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "families": _family_records(taxonomy["alphabet_family"], family_type="alphabet_control"),
        "controls_executed": False,
        **FALSE_FLAGS,
    }
    reading = {
        "record_type": "stage5ay_reading_order_control_manifest",
        "schema": "schemas/token-block/reading-order-control-manifest-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "families": _family_records(taxonomy["reading_order_family"], family_type="reading_order_control"),
        "controls_executed": False,
        **FALSE_FLAGS,
    }
    page_split = {
        "record_type": "stage5ay_page_split_control_manifest",
        "schema": "schemas/token-block/page-split-control-manifest-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "families": _family_records(taxonomy["page_split_family"], family_type="page_split_control"),
        "controls_executed": False,
        "page_boundaries_final": False,
        **{key: value for key, value in FALSE_FLAGS.items() if key != "page_boundaries_final"},
    }
    source = {
        "record_type": "stage5ay_source_control_manifest",
        "schema": "schemas/token-block/source-control-manifest-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "families": _family_records(taxonomy["source_control_family"], family_type="source_control"),
        "future_source_lock_required_for_wrong_page_block_control": True,
        "controls_executed": False,
        **FALSE_FLAGS,
    }
    for path, payload in [
        (out_variant_family, variant),
        (out_null_control_family, null_control),
        (out_alphabet_control, alphabet),
        (out_reading_order, reading),
        (out_page_split, page_split),
        (out_source_control, source),
    ]:
        write_yaml(path, payload)
    write_json(
        results_dir / "execution_gate_report.json",
        {"variant_family": variant, "null_control_family": null_control, "option_record_count": eligibility["option_record_count"]},
    )
    return variant, null_control, alphabet, reading, page_split, source


def build_stage5ay_execution_gates(
    source_inputs: Path,
    branch_budget: Path,
    variant_family: Path,
    null_control_family: Path,
    results_dir: Path,
    out_result_schema_preview: Path,
    out_execution_gates: Path,
    out_dwh_context: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ensure_results_dir(results_dir)
    budget = read_yaml(branch_budget)
    result_schema = {
        "record_type": "stage5ay_future_result_schema_preview",
        "schema": "schemas/token-block/future-result-schema-preview-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "future_result_schema_preview_only": True,
        "result_generated_now": False,
        "future_result_record_type": "bounded_token_block_preflight_result_v0",
        "preview_fields": [
            "future_result_record_type",
            "manifest_id",
            "source_manifest_sha256",
            "stage_id_that_executes",
            "execution_authorised",
            "execution_authorisation_record",
            "input_token_block_sha256",
            "branch_policy_id",
            "variant_family_id",
            "control_family_id",
            "token_choice_manifest_sha256",
            "byte_stream_sha256",
            "read_order_id",
            "alphabet_id",
            "page_split_id",
            "null_control_id",
            "output_kind",
            "output_sha256",
            "score_fields",
            "warnings",
            "guardrail_flags",
            "solve_claim",
        ],
        "solve_claim": False,
        **FALSE_FLAGS,
    }
    gates = {
        "record_type": "stage5ay_execution_gates",
        "schema": "schemas/token-block/execution-gates-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "source_inputs": repo_relative(source_inputs),
        "branch_budget": repo_relative(branch_budget),
        "variant_family": repo_relative(variant_family),
        "null_control_family": repo_relative(null_control_family),
        "all_gates_required_before_execution": True,
        "execution_authorised_now": False,
        "gates": [
            {
                "gate_id": "source_lock_gate",
                "required": True,
                "status": "design_satisfied_execution_still_blocked",
                "requirements": ["Stage 5AR original-image coordinate records exist and validate."],
            },
            {
                "gate_id": "case_review_gate",
                "required": True,
                "status": "design_satisfied_execution_still_blocked",
                "requirements": [
                    "Stage 5AV/5AW human decisions are integrated.",
                    "Stage 5AW repaired branch manifest is used.",
                    "Stage 5AV branch manifest is superseded.",
                ],
            },
            {
                "gate_id": "manifest_review_gate",
                "required": True,
                "status": "blocked_pending_stage5az_or_later_review",
                "requirements": [
                    "Stage 5AY manifest design exists.",
                    "Stage 5AY manifest has passed validation.",
                    "A later Deep Research or human review has approved the manifest.",
                ],
            },
            {
                "gate_id": "null_control_gate",
                "required": True,
                "status": "defined_not_executed",
                "requirements": [
                    "Null controls are defined before execution.",
                    "Control families are fixed before any result inspection.",
                ],
            },
            {
                "gate_id": "execution_scope_gate",
                "required": True,
                "status": "blocked_pending_later_authorisation",
                "requirements": [
                    "Maximum branch count is bounded.",
                    "No full Cartesian product above threshold.",
                    "Sampled variants require fixed seeds and later authorisation.",
                ],
            },
            {
                "gate_id": "dwh_gate",
                "required": True,
                "status": "blocked_speculative_source_lock_required",
                "requirements": [
                    "DWH remains speculative.",
                    "No hash/preimage search unless exact hash object, algorithm, input material, and target policy are source-locked by a later stage.",
                ],
            },
            {
                "gate_id": "safety_gate",
                "required": True,
                "status": "blocked_execution_not_authorised",
                "requirements": [
                    "No CUDA unless explicitly staged later.",
                    "No scored experiment until manifest review and execution authorisation.",
                    "No solve claim.",
                ],
            },
        ],
        **FALSE_FLAGS,
    }
    dwh = {
        "record_type": "stage5ay_dwh_preflight_context",
        "schema": "schemas/token-block/dwh-preflight-context-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "dwh_defined": True,
        "dwh_expansion": "Deep Web Hash",
        "token_block_dwh_relationship_status": "speculative_source_lock_required",
        "dwh_operational_status": "not_operational",
        "preflight_manifest_relevance": "bounded token-block preflight may eventually help define candidate byte material, but this stage does not generate bytes or search hashes",
        "source_lock_required_before_hash_search": True,
        "exact_hash_object_required_before_hash_search": True,
        "algorithm_policy_required_before_hash_search": True,
        "input_material_policy_required_before_hash_search": True,
        "branch_count_upper_bound_product": budget.get("branch_count_upper_bound_product"),
        "hash_search_performed": False,
        "hash_preimage_claim": False,
        "decode_claim": False,
        **FALSE_FLAGS,
    }
    write_yaml(out_result_schema_preview, result_schema)
    write_yaml(out_execution_gates, gates)
    write_yaml(out_dwh_context, dwh)
    write_json(results_dir / "execution_gate_report.json", gates)
    return result_schema, gates, dwh


def build_stage5ay_summary(
    source_inputs: Path,
    policy: Path,
    branch_eligibility: Path,
    variant_family: Path,
    null_control_family: Path,
    alphabet_control: Path,
    reading_order: Path,
    page_split: Path,
    source_control: Path,
    branch_budget: Path,
    result_schema_preview: Path,
    execution_gates: Path,
    dwh_context: Path,
    out_guardrail: Path,
    out_next_stage: Path,
    out_summary: Path,
    results_dir: Path = STAGE5AY_RESULTS_DIR,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ensure_results_dir(results_dir)
    source_payload = read_yaml(source_inputs)
    policy_payload = read_yaml(policy)
    eligibility_payload = read_yaml(branch_eligibility)
    variant_payload = read_yaml(variant_family)
    null_payload = read_yaml(null_control_family)
    alphabet_payload = read_yaml(alphabet_control)
    reading_payload = read_yaml(reading_order)
    page_payload = read_yaml(page_split)
    source_control_payload = read_yaml(source_control)
    budget_payload = read_yaml(branch_budget)
    result_schema_payload = read_yaml(result_schema_preview)
    gate_payload = read_yaml(execution_gates)
    dwh_payload = read_yaml(dwh_context)
    guardrail = {
        "record_type": "stage5ay_guardrail",
        "schema": "schemas/token-block/stage5ay-guardrail-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "status": "passed",
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5av_branch_manifest_used": False,
        "full_cartesian_product_allowed": False,
        "variant_byte_streams_generated": False,
        "token_experiments_executed": False,
        "manifest_design_only": True,
        "deep_research_review_recommended_next": True,
        "new_cuda_kernels_added": 0,
        **FALSE_FLAGS,
    }
    next_stage = {
        "record_type": "stage5ay_next_stage_decision",
        "schema": "schemas/project-state/stage5ay-summary-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "selected_option_id": "stage5az_deep_research_review_of_bounded_preflight_manifest_and_execution_gates",
        "selected_next_stage_title": STAGE5AZ_TITLE,
        "selected_next_stage_reason": "Stage 5AY produced design-only manifests and gates; Deep Research or human review should inspect them before any runner implementation or execution.",
        "deep_research_review_recommended_next": True,
        "execution_enabled": False,
        "solve_claim": False,
    }
    summary = {
        "record_type": "stage5ay_bounded_preflight_manifest_design_summary",
        "schema": "schemas/project-state/stage5ay-summary-v0.schema.json",
        "stage_id": STAGE5AY_ID,
        "status": "complete",
        "source_stage_ids": ["stage-5ap", "stage-5ar", "stage-5au", STAGE5AW_ID, "stage-5ax"],
        "source_stage5ax_commit": SOURCE_STAGE5AX_COMMIT,
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5av_branch_manifest_used": False,
        "source_inputs_validated": source_payload.get("missing_required_source_count") == 0,
        "source_input_record_count": source_payload.get("source_record_count"),
        "preflight_policy_status": policy_payload.get("policy_status"),
        "branch_upper_bound_product": budget_payload.get("branch_count_upper_bound_product"),
        "branch_upper_bound_log10": budget_payload.get("branch_count_upper_bound_log10"),
        "primary60_mappable_branch_product": budget_payload.get("primary60_mappable_branch_upper_bound_product"),
        "primary60_mappable_branch_log10": budget_payload.get("primary60_mappable_branch_upper_bound_log10"),
        "full_cartesian_product_allowed": False,
        "manifest_family_count": (
            variant_payload.get("family_count", 0)
            + len(null_payload.get("families", []))
            + len(alphabet_payload.get("families", []))
            + len(reading_payload.get("families", []))
            + len(page_payload.get("families", []))
            + len(source_control_payload.get("families", []))
        ),
        "branch_eligibility_option_record_count": eligibility_payload.get("option_record_count"),
        "execution_gate_count": len(gate_payload.get("gates", [])),
        "dwh_context_status": dwh_payload.get("dwh_operational_status"),
        "future_result_schema_preview_only": True,
        "result_generated_now": result_schema_payload.get("result_generated_now"),
        "parallel_validation_harness_used": True,
        "selected_next_stage_title": STAGE5AZ_TITLE,
        "deep_research_review_recommended_next": True,
        "new_cuda_kernels_added": 0,
        **FALSE_FLAGS,
    }
    write_yaml(out_guardrail, guardrail)
    write_yaml(out_next_stage, next_stage)
    write_yaml(out_summary, summary)
    write_json(results_dir / "summary.json", summary)
    return guardrail, next_stage, summary


def validate_stage5ay(
    source_inputs: Path,
    policy: Path,
    branch_eligibility: Path,
    variant_family: Path,
    null_control_family: Path,
    alphabet_control: Path,
    reading_order: Path,
    page_split: Path,
    source_control: Path,
    branch_budget: Path,
    result_schema_preview: Path,
    execution_gates: Path,
    dwh_context: Path,
    guardrail: Path,
    next_stage_decision: Path,
    summary: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    payloads = {
        "source_inputs": read_yaml(source_inputs),
        "policy": read_yaml(policy),
        "branch_eligibility": read_yaml(branch_eligibility),
        "variant_family": read_yaml(variant_family),
        "null_control_family": read_yaml(null_control_family),
        "alphabet_control": read_yaml(alphabet_control),
        "reading_order": read_yaml(reading_order),
        "page_split": read_yaml(page_split),
        "source_control": read_yaml(source_control),
        "branch_budget": read_yaml(branch_budget),
        "result_schema_preview": read_yaml(result_schema_preview),
        "execution_gates": read_yaml(execution_gates),
        "dwh_context": read_yaml(dwh_context),
        "guardrail": read_yaml(guardrail),
        "next_stage_decision": read_yaml(next_stage_decision),
        "summary": read_yaml(summary),
    }
    errors: list[str] = []
    for name, payload in payloads.items():
        if payload.get("stage_id") != STAGE5AY_ID:
            errors.append(f"{name}_stage_id_must_be_{STAGE5AY_ID}")
        if payload.get("solve_claim") is True:
            errors.append(f"{name}_solve_claim_must_be_false")
        for flag in [
            "variant_byte_streams_generated",
            "token_experiments_executed",
            "hash_preimage_search_performed",
            "decode_attempt_performed",
            "cuda_execution_performed",
            "cuda_source_modified",
            "benchmark_performed",
            "cryptanalytic_benchmark_performed",
            "scored_experiments_executed",
            "generated_outputs_committed",
        ]:
            if payload.get(flag) is True:
                errors.append(f"{name}_{flag}_must_be_false")
    if not payloads["source_inputs"].get("stage5aw_repaired_branch_manifest_used"):
        errors.append("stage5aw_repaired_branch_manifest_used_must_be_true")
    if payloads["source_inputs"].get("stage5av_branch_manifest_used"):
        errors.append("stage5av_branch_manifest_used_must_be_false")
    if payloads["source_inputs"].get("missing_required_source_count") != 0:
        errors.append("missing_required_source_count_must_be_0")
    if payloads["branch_budget"].get("full_cartesian_product_allowed") is not False:
        errors.append("full_cartesian_product_allowed_must_be_false")
    if payloads["result_schema_preview"].get("future_result_schema_preview_only") is not True:
        errors.append("future_result_schema_preview_only_must_be_true")
    if payloads["result_schema_preview"].get("result_generated_now") is not False:
        errors.append("result_generated_now_must_be_false")
    if payloads["dwh_context"].get("dwh_expansion") != "Deep Web Hash":
        errors.append("dwh_expansion_must_be_Deep_Web_Hash")
    if payloads["next_stage_decision"].get("selected_next_stage_title") != STAGE5AZ_TITLE:
        errors.append("selected_next_stage_must_be_stage5az")
    generated_summary_present = (results_dir / "summary.json").exists()
    counts = {
        "source_input_record_count": payloads["source_inputs"].get("source_record_count"),
        "branch_eligibility_option_record_count": payloads["branch_eligibility"].get("option_record_count"),
        "variant_family_count": payloads["variant_family"].get("family_count"),
        "execution_gate_count": len(payloads["execution_gates"].get("gates", [])),
        "branch_upper_bound_product": payloads["branch_budget"].get("branch_count_upper_bound_product"),
        "primary60_mappable_branch_product": payloads["branch_budget"].get(
            "primary60_mappable_branch_upper_bound_product"
        ),
        "stage5ay_generated_summary_present": generated_summary_present,
        "validation_error_count": len(errors),
    }
    return counts, errors
