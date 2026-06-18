"""Stage 6H current-state repair and dot-angle/PDD153 source-lock addendum."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block import stage6, stage6b, stage6c, stage6d, stage6e, stage6f, stage6g
from libreprimus.token_block.models import read_yaml, write_yaml

STAGE_ID = "stage-6h"
STAGE_TOKEN = "stage6h"
STAGE_TITLE = (
    "Stage 6H - Current-state integrity repair and dot-angle / right-triangle "
    "number-triangle source-lock addendum, without execution"
)
PROMPT_TYPE = "codex_plan_mode_source_lock_readiness_addendum"
PREVIOUS_STAGE_ID = "stage-6g"
NEXT_STAGE_ID = "stage-6i"
NEXT_STAGE_TITLE_FINAL = "Stage 6I - Final finite Stage 7 probe manifest and archive-run contract, without execution"
NEXT_STAGE_TITLE_REPAIR = "Stage 6I - Stage 7 readiness repair before final manifest, without execution"
NEXT_PROMPT_TYPE_FINAL = "codex_plan_mode_probe_manifest_finalization"
NEXT_PROMPT_TYPE_REPAIR = "codex_plan_mode_readiness_repair"
STARTING_COMMIT = "3bbbd97f831ded8ae77ea92598aab7b1828dfae3"

PROJECT_STATE_DIR = Path("data/project-state")
HISTORICAL_ROUTE_DIR = Path("data/historical-route")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
TOKEN_BLOCK_DIR = Path("data/token-block")
OPERATOR_OVERLAY_DIR = Path("data/operator-console/source-browser/number-fact-overlays")

CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
CURRENT_STAGE_SCHEMA_PATH = Path("schemas/project-state/current-stage-state-v0.schema.json")
DOC_STALENESS_SOURCE_OF_TRUTH_PATH = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
CODEX_COMPLETION_PATH = Path("codex-output/stage6h-codex-completion.md")

STAGE6H_FALSE_GUARDRAILS = {
    "stage6h_final_finite_stage7_manifest_created_now",
    "stage6h_archive_run_contract_finalized_now",
    "stage6h_creates_stage7_result_archive_now",
    "stage6h_generates_stage7_outputs_now",
    "stage6h_routes_to_stage7_now",
    "stage6h_runs_any_probe_now",
    "stage6h_generates_spiral_readouts_now",
    "stage6h_generates_triangle_readouts_now",
    "stage7_execution_allowed_next",
    "stage7_zip_archive_creation_allowed_next",
    "stage7_manifest_created_now",
    "stage7_archive_created_now",
    "stage7_probe_execution_performed_now",
    "probe_execution_performed_now",
    "diagnostic_probe_run_now",
    "diagnostic_execution_performed_now",
    "route_stream_generated_now",
    "route_extraction_performed_now",
    "real_byte_stream_generated",
    "variant_byte_streams_generated",
    "byte_stream_generation_authorized_now",
    "cipher_execution_performed_now",
    "scoring_performed",
    "scoring_performed_now",
    "ocr_performed",
    "image_forensics_performed",
    "hidden_content_image_forensics_performed",
    "semantic_image_interpretation_performed",
    "cuda_execution_performed",
    "benchmark_performed",
    "target_selection_performed_now",
    "target_priority_decision_created_now",
    "pivot_target_selected_now",
    "solve_claim",
}

FORBIDDEN_FALSE = (
    set(stage6.FALSE_GUARDRAILS)
    | set(stage6.STAGE6_FALSE_GUARDRAILS)
    | set(stage6b.FORBIDDEN_FALSE)
    | set(stage6c.STAGE6C_FALSE_GUARDRAILS)
    | set(stage6d.STAGE6D_FALSE_GUARDRAILS)
    | set(stage6e.STAGE6E_FALSE_GUARDRAILS)
    | set(stage6f.STAGE6F_FALSE_GUARDRAILS)
    | set(stage6g.FORBIDDEN_FALSE)
    | STAGE6H_FALSE_GUARDRAILS
)

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage6h-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage6h-next-stage-decision.yaml",
    "stage6g_preservation": PROJECT_STATE_DIR / "stage6h-stage6g-preservation.yaml",
    "current_state_integrity_repair": PROJECT_STATE_DIR / "stage6h-current-state-integrity-repair.yaml",
    "doc_staleness_source_truth_repair": PROJECT_STATE_DIR / "stage6h-doc-staleness-source-truth-repair.yaml",
    "operational_file_map_repair": PROJECT_STATE_DIR / "stage6h-operational-file-map-repair.yaml",
    "source_lock_summary": PROJECT_STATE_DIR / "stage6h-dot-angle-pdd153-source-lock-summary.yaml",
    "exact_constants": PROJECT_STATE_DIR / "stage6h-exact-constants-validation.yaml",
    "number_fact_overlay_summary": PROJECT_STATE_DIR / "stage6h-number-fact-overlay-summary.yaml",
    "future_diagnostic_summary": PROJECT_STATE_DIR / "stage6h-future-diagnostic-summary.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR / "stage6h-source-browser-loadability-summary.yaml",
    "blocker_register": PROJECT_STATE_DIR / "stage6h-stage6i-readiness-blocker-register.yaml",
    "current_stage_transition": PROJECT_STATE_DIR / "stage6h-current-stage-transition.yaml",
    "prior_stage_repair_ledger": PROJECT_STATE_DIR / "stage6h-prior-stage-repair-ledger.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage6h-reviewable-validation-evidence.yaml",
    "chatgpt_context_update": PROJECT_STATE_DIR / "stage6h-chatgpt-context-update-summary.yaml",
    "gate_closure": PROJECT_STATE_DIR / "stage6h-gate-closure.yaml",
    "handoff_policy": PROJECT_STATE_DIR / "stage6h-handoff-policy.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "recent_chat_provenance": SOURCE_HARVESTER_DIR / "stage6h-recent-chat-transcript-source-lock.yaml",
    "canonical_image_root_crosswalk": SOURCE_HARVESTER_DIR
    / "stage6h-canonical-iddqd-v2-image-root-crosswalk.yaml",
    "number_triangle_crosswalk": SOURCE_HARVESTER_DIR / "stage6h-number-triangle-source-record-crosswalk.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage6h-raw-source-noncommit-proof.yaml",
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage6h-codex-handoff-policy.yaml",
}

TOKEN_BLOCK_PATHS: dict[str, Path] = {
    "stage6i_manifest_input_addendum": TOKEN_BLOCK_DIR / "stage6h-stage6i-manifest-input-addendum.yaml",
    "future_diagnostic_registry": TOKEN_BLOCK_DIR / "stage6h-future-diagnostic-registry.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage6h-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage6h-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage6h-no-execution-transition-gate.yaml",
}

OPERATOR_CONSOLE_PATHS: dict[str, Path] = {
    "number_fact_overlays": OPERATOR_OVERLAY_DIR / "stage6h-dot-angle-right-triangle-source-lock-overlays.yaml",
}

VISUAL_DOT_RECORD_IDS = [
    "stage6h-five-dot-constellation-reflection-angle-fingerprint-v0",
    "stage6h-three-dot-dinkus-scaled-7-8-angle41-bridge-v0",
    "stage6h-dot-marker-antialias-asset-fingerprint-context-v0",
    "stage6h-branch-dot-five-slot-binary-order-policy-table-v0",
    "stage6h-branch-dot-right-cluster-11111-gp31-bridge-v0",
    "stage6h-branch-dot-left-yx-01110-14-inverse17-candidate-v0",
    "stage6h-branch-dot-left-right-concat-479-lag5-bridge-v0",
    "stage6h-branch-dot-geometric-concat-primepi86-control-v0",
    "stage6h-branch-anchor-start-policy-candidate-v0",
    "stage6h-branch-dot-pentagonal-angle-gap-candidate-v0",
    "stage6h-mayfly-bottom-left-microdot-distance-angle-echo-candidate-v0",
    "stage6h-signpost-peripheral-clean-dot-inventory-candidate-v0",
    "stage6h-page-label-72-vs-74-dot-policy-control-v0",
]

PDD153_RECORD_IDS = [
    "stage6h-pdd153-existing-source-lock-crosslink-v0",
    "stage6h-pdd153-right-angle-coordinate-transform-v0",
    "stage6h-pdd153-dot-angle41-center-to-d4-position133-bridge-v0",
    "stage6h-pdd153-dot-angle-complement-8-7-route-candidate-v0",
    "stage6h-pdd153-d4-diagonal-anchor-route-candidate-v0",
    "stage6h-pdd153-folded-7-8-8-7-seam-50-51-candidate-v0",
    "stage6h-pdd153-folded-triangle-72-9-72-spine-split-candidate-v0",
    "stage6h-pdd153-shared-spine-two-81-cell-surfaces-candidate-v0",
    "stage6h-pdd153-mirror-pair-mod29-stream-policy-table-v0",
    "stage6h-pdd153-row10-seam-49-52-50-51-way-candidate-v0",
]

PDD_TRANSFORM_RECORD_IDS = [
    "stage6h-pdd153-pdd-minus-reversed-word52-way-verified-v0",
    "stage6h-pdd153-pdd-minus-reversed-word55-read-prefix-candidate-v0",
    "stage6h-pdd153-56311-skeleton-way-read-route-candidate-v0",
]

RESIDUE_RECORD_IDS = [
    "stage6h-pdd153-i-am-circumference-mod153-left-edge-bridge-v0",
    "stage6h-ouroboros-variant-mod153-offset-bridge-v0",
    "stage6h-pdd153-ouroboros-offset-cycle-policy-v0",
]

ROUTE_CIPHER_RECORD_IDS = [
    "stage6h-pdd153-route-output-cipher-family-triage-policy-v0",
    "stage6h-pdd153-candidate-key-surface-register-v0",
    "stage6h-pdd153-entropy-and-fingerprint-diagnostic-policy-v0",
]

HISTORICAL_ROUTE_PATHS: dict[str, Path] = {
    record_id: HISTORICAL_ROUTE_DIR / f"{record_id}.yaml"
    for record_id in (
        VISUAL_DOT_RECORD_IDS + PDD153_RECORD_IDS + PDD_TRANSFORM_RECORD_IDS + RESIDUE_RECORD_IDS + ROUTE_CIPHER_RECORD_IDS
    )
}

DATA_PATHS: dict[str, Path] = {
    **PROJECT_STATE_PATHS,
    **SOURCE_HARVESTER_PATHS,
    **TOKEN_BLOCK_PATHS,
    **HISTORICAL_ROUTE_PATHS,
    **OPERATOR_CONSOLE_PATHS,
}


def _schema_path_for(path: Path, key: str) -> Path:
    if path.is_relative_to(OPERATOR_OVERLAY_DIR):
        return Path("schemas/operator-console/stage6h-number-fact-overlays-v0.schema.json")
    try:
        return Path("schemas") / path.parent.relative_to("data") / f"{path.stem}-v0.schema.json"
    except ValueError:
        return Path("schemas/project-state") / f"stage6h-{key}-v0.schema.json"


SCHEMA_PATHS: dict[str, Path] = {
    key: _schema_path_for(path, key) for key, path in DATA_PATHS.items()
}

OVERLAY_IDS = [
    "stage6h_three_dot_7_8_angle41_overlay",
    "stage6h_branch_right_11111_31_overlay",
    "stage6h_branch_left_01110_14_inverse17_overlay",
    "stage6h_branch_concat_479_lag5_overlay",
    "stage6h_branch_concat_447_primepi86_overlay",
    "stage6h_pdd153_right_angle_transform_overlay",
    "stage6h_pdd153_vertical_split_72_9_72_overlay",
    "stage6h_pdd153_shared_spine_81_81_overlay",
    "stage6h_pdd153_7_8_ray_133_d4_overlay",
    "stage6h_pdd153_folded_7_8_8_7_hits_50_51_overlay",
    "stage6h_pdd153_row10_seam_49_52_50_51_overlay",
    "stage6h_pdd153_word52_way_overlay",
    "stage6h_pdd153_word55_read_prefix_overlay",
    "stage6h_i_am_circumference_mod153_overlay",
    "stage6h_ouroboros_variant_mod153_offsets_overlay",
]

DOT_DIAGNOSTICS = [
    "lp_five_dot_constellation_affine_repetition_probe_v0",
    "lp_three_dot_dinkus_scaled_spacing_probe_v0",
    "dot_motif_angle41_triangle_anchor_control_v0",
    "branch_dot_binary_order_policy_control_v0",
    "branch_dot_left_right_concat_479_lag5_control_v0",
    "branch_dot_black_white_polarity_control_v0",
    "branch_dot_anchor_start_direction_control_v0",
    "branch_dot_pentagonal_angle_gap_control_v0",
    "mayfly_microdot_angle_echo_negative_control_v0",
    "signpost_peripheral_clean_dot_body_mask_inventory_v0",
    "all_lp_dot_component_angle_distance_catalog_v0",
    "dot_motif_page_index_72_vs_74_policy_control_v0",
]

PDD153_DIAGNOSTICS = [
    "pdd153_right_triangle_coordinate_transform_inventory_v0",
    "pdd153_angle41_7_8_ray_readout_control_v0",
    "pdd153_angle41_complement_8_7_ray_control_v0",
    "pdd153_folded_7_8_8_7_billiard_route_control_v0",
    "pdd153_d4_diagonal_anchor_route_control_v0",
    "pdd153_vertical_split_mirror_pair_inventory_v0",
    "pdd153_shared_spine_9x9_projection_control_v0",
    "pdd153_row10_way_read_neighborhood_control_v0",
    "pdd153_ouroboros_variant_offset_route_control_v0",
    "pdd153_i_am_circumference_mod153_edge_control_v0",
    "pdd153_branch_binary_parameterized_route_control_v0",
    "pdd153_56311_skeleton_split_expansion_control_v0",
]

ROUTE_CIPHER_DIAGNOSTICS = [
    "pdd153_candidate_reading_order_fingerprint_control_v0",
    "pdd153_route_output_entropy_ic_lag_profile_control_v0",
    "pdd153_wrong_route_negative_control_v0",
    "pdd153_route_as_key_stream_control_v0",
    "pdd153_route_as_null_copy_mask_control_v0",
    "pdd153_route_then_gp_mod29_cipher_family_control_v0",
    "pdd153_route_then_vigenere_key_control_v0",
    "pdd153_pdd_transform_then_way_second_stage_control_v0",
    "pdd153_mirror_pair_pdd_transform_control_v0",
]

NOT_ALLOWED_AS = ["proof", "route_seed", "execution_seed", "target_selection", "solve_claim"]

EXACT_CONSTANTS = {
    "three_dot_angle": {"ratio": "7/8", "atan_degrees": 41.1859},
    "branch_binary": {
        "right_bits": "11111",
        "right_value": 31,
        "y_x_black_bits": "01110",
        "y_x_black_value": 14,
        "y_x_white_bits": "10001",
        "y_x_white_value": 17,
        "concat_y_x_bits": "0111011111",
        "concat_y_x_value": 479,
        "geometric_concat_value": 447,
        "prime_count_pi_447": 86,
    },
    "pdd153": {
        "total_cells": 153,
        "row_count": 17,
        "center_position": 41,
        "path_56311": [41, 46, 52, 55, 66],
        "offsets_56311": [5, 11, 14, 25],
        "d4_diagonal": [7, 12, 18, 25, 33, 42, 52, 63, 75, 88, 102, 117, 133, 150],
    },
    "right_triangle": {
        "visual_7_8_endpoint": 133,
        "visual_8_7_endpoint": 148,
        "folded_7_8_endpoint": 50,
        "folded_8_7_endpoint": 51,
    },
    "vertical_split": {
        "left_nonspine": 72,
        "spine": 9,
        "right_nonspine": 72,
        "shared_spine_surface": 81,
        "spine_positions": [1, 5, 13, 25, 41, 61, 85, 113, 145],
    },
    "pdd_transform": {"word52_result": "WAY", "word55_prefix": "READ", "word55_full_plaintext_claimed": False},
    "residues": {
        "I_AM_gp": 199,
        "I_AM_mod153": 46,
        "CIRCUMFERENCE_gp": 398,
        "CIRCUMFERENCE_mod153": 92,
        "UROBOROS_gp": 160,
        "UROBOROS_excess": 7,
        "OROBOROS_gp": 164,
        "OROBOROS_excess": 11,
        "OUROBOROS_gp": 167,
        "OUROBOROS_excess": 14,
    },
}


def build_stage6h() -> dict[str, Any]:
    """Build Stage 6H records, schemas, current mirrors, and handoff scaffold."""
    _ensure_no_protected_output_overlap()
    _write_schemas()
    _write_current_stage_schema()
    _write_current_stage_state()
    _write_doc_staleness_source_of_truth()
    _write_docs()
    _write_operational_map()

    records = _records()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)
    _write_stage_summary_record(records["summary"])
    _write_completion_summary_stub(records["summary"])
    return records["summary"]


def validate_stage6h() -> stage6.ValidationResult:
    checks = [
        validate_stage6h_files_and_schemas(),
        validate_stage6h_current_state_integrity(),
        validate_stage6h_doc_staleness_source_truth_repair(),
        validate_stage6h_operational_file_map_repair(),
        validate_stage6h_source_harvester_records(),
        validate_stage6h_source_lock_records(),
        validate_stage6h_exact_constants(),
        validate_stage6h_number_fact_overlays(),
        validate_stage6h_future_diagnostics(),
        validate_stage6h_stage6i_addendum(),
        validate_stage6h_source_browser_loadability(),
        validate_stage6h_current_stage_transition(),
        validate_stage6h_gate_closure(),
        validate_stage6h_handoff(),
    ]
    errors = [error for check in checks for error in check.errors]
    counts: dict[str, Any] = {}
    for check in checks:
        counts.update(check.counts)
    return _result(errors, **counts)


def validate_stage6h_files_and_schemas() -> stage6.ValidationResult:
    errors = []
    for key, data_path in DATA_PATHS.items():
        schema_path = SCHEMA_PATHS[key]
        if not data_path.exists():
            errors.append(f"missing Stage 6H record: {data_path}")
            continue
        if not schema_path.exists():
            errors.append(f"missing Stage 6H schema: {schema_path}")
            continue
        payload = read_yaml(data_path)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema_errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda err: list(err.path))
        errors.extend(f"{data_path}: {err.message}" for err in schema_errors)
        if not schema.get("required") or len(schema.get("properties", {})) < 5:
            errors.append(f"{schema_path}: schema is too permissive for Stage 6H")
    return _result(errors, stage6h_record_count=len(DATA_PATHS))


def validate_stage6h_current_state_integrity() -> stage6.ValidationResult:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    errors = _current_state_integrity_errors(current)
    return _result(errors, current_state_repair_blocker_count=len(errors))


def _current_state_integrity_errors(current: dict[str, Any]) -> list[str]:
    errors = []
    expected = {
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE_FINAL,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE_FINAL,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }
    for key, value in expected.items():
        if current.get(key) != value:
            errors.append(f"current-stage-state {key} expected {value!r}, got {current.get(key)!r}")
    if current.get("latest_completed_stage", {}).get("stage_id") != current.get("latest_completed_stage_id"):
        errors.append("nested latest_completed_stage.stage_id contradicts latest_completed_stage_id")
    if current.get("next_stage", {}).get("stage_id") != current.get("recommended_next_stage_id"):
        errors.append("nested next_stage.stage_id contradicts recommended_next_stage_id")
    handoffs = current.get("post_push_handoff_locations", [])
    if handoffs != [CODEX_COMPLETION_PATH.as_posix(), "GitHub issue comment"]:
        errors.append("post_push_handoff_locations must point to Stage 6H completion and issue comment")
    text = json.dumps(current)
    for stale in ["stage6d-codex-completion.md", "stage6e-codex-completion.md", "stage6f-codex-completion.md", "stage6g-codex-completion.md"]:
        if stale in text:
            errors.append(f"stale handoff path remains in current state: {stale}")
    if current.get("stage6g_final_manifest_required") is True:
        errors.append("stale stage6g_final_manifest_required true survives")
    if current.get("stage6g_can_attempt_final_manifest_without_prior_repair") is True:
        errors.append("stale stage6g_can_attempt_final_manifest_without_prior_repair true survives")
    return errors


def validate_stage6h_doc_staleness_source_truth_repair() -> stage6.ValidationResult:
    record = read_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH)
    errors = []
    if record.get("latest_completed_stage_id") != STAGE_ID:
        errors.append("Stage 5AH source-of-truth latest_completed_stage_id not Stage 6H")
    if record.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("Stage 5AH source-of-truth recommended_next_stage_id not Stage 6I")
    for key in ["expected_latest_after_stage5ah", "expected_next_after_stage5ah", "recommended_next_stage_after_this_stage"]:
        value = str(record.get(key, ""))
        if "Stage 6F - Final finite Stage 7" in value:
            errors.append(f"Stage 5AH source-of-truth stale Stage 6F final-manifest field remains: {key}")
    if record.get("historical_stage5ah_fields_superseded_by_stage6h_current_truth") is not True:
        errors.append("Stage 5AH source-of-truth must explicitly mark historical fields superseded")
    return _result(errors, doc_staleness_repair_blocker_count=len(errors))


def validate_stage6h_operational_file_map_repair() -> stage6.ValidationResult:
    text = Path("docs/onboarding/operational-file-map.md").read_text(encoding="utf-8")
    errors = []
    for stale in ['--expected-latest-stage "Stage 5ED"', '--expected-next-stage "Stage 5EE"']:
        if stale in text:
            errors.append(f"operational-file-map stale current command remains: {stale}")
    if "stage6h-stage6i-manifest-input-addendum.yaml" not in text:
        errors.append("operational-file-map must mention Stage 6I addendum path")
    return _result(errors, operational_file_map_repair_blocker_count=len(errors))


def validate_stage6h_source_harvester_records() -> stage6.ValidationResult:
    errors = []
    required = [
        "recent_chat_provenance",
        "canonical_image_root_crosswalk",
        "number_triangle_crosswalk",
        "raw_source_noncommit_proof",
        "codex_handoff_policy",
    ]
    for key in required:
        payload = read_yaml(SOURCE_HARVESTER_PATHS[key])
        if payload.get("stage_id") != STAGE_ID:
            errors.append(f"{SOURCE_HARVESTER_PATHS[key]} stage_id mismatch")
    recent = read_yaml(SOURCE_HARVESTER_PATHS["recent_chat_provenance"])
    if recent.get("recent_chat_transcript_prompt_attached_context_present") is not True:
        errors.append("recent chat prompt-attached context must be present")
    if recent.get("recent_chat_transcript_raw_committed_now") is not False:
        errors.append("recent chat raw transcript must not be committed")
    return _result(errors, source_harvester_record_count=len(required))


def validate_stage6h_source_lock_records() -> stage6.ValidationResult:
    errors = []
    for record_id in VISUAL_DOT_RECORD_IDS + PDD153_RECORD_IDS + PDD_TRANSFORM_RECORD_IDS + RESIDUE_RECORD_IDS + ROUTE_CIPHER_RECORD_IDS:
        payload = read_yaml(HISTORICAL_ROUTE_PATHS[record_id])
        if payload.get("stage_id") != STAGE_ID:
            errors.append(f"{record_id}: stage_id mismatch")
        if payload.get("usable_for_decision_now") is not False:
            errors.append(f"{record_id}: usable_for_decision_now must be false")
        if payload.get("not_allowed_as") != NOT_ALLOWED_AS:
            errors.append(f"{record_id}: not_allowed_as mismatch")
    branch = read_yaml(HISTORICAL_ROUTE_PATHS["stage6h-branch-dot-five-slot-binary-order-policy-table-v0"])
    if branch.get("selected_order_policy_now") is not None or branch.get("selection_status") != "no_order_selected":
        errors.append("branch-dot order policy must not select an order")
    center = read_yaml(HISTORICAL_ROUTE_PATHS["stage6h-pdd153-dot-angle41-center-to-d4-position133-bridge-v0"])
    if center.get("center_anchor_gp41_claim_policy", {}).get("center_rune_gp_value_41_source_locked_now") is not False:
        errors.append("center rune GP41 must not be source-locked without existing committed proof")
    word55 = read_yaml(HISTORICAL_ROUTE_PATHS["stage6h-pdd153-pdd-minus-reversed-word55-read-prefix-candidate-v0"])
    if word55.get("word55_read_prefix", {}).get("full_plaintext_claimed") is not False:
        errors.append("word55 READ record must not claim full plaintext")
    return _result(
        errors,
        visual_dot_source_lock_record_count=len(VISUAL_DOT_RECORD_IDS),
        pdd153_geometry_source_lock_record_count=len(PDD153_RECORD_IDS),
        pdd_transform_record_count=len(PDD_TRANSFORM_RECORD_IDS),
        residue_bridge_record_count=len(RESIDUE_RECORD_IDS),
        route_cipher_policy_record_count=len(ROUTE_CIPHER_RECORD_IDS),
    )


def validate_stage6h_exact_constants() -> stage6.ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["exact_constants"])
    errors = []
    if record.get("stage6h_exact_constants_must_be_validated") != EXACT_CONSTANTS:
        errors.append("exact constants table mismatch")
    prime_policy = record.get("prime_count_policy", {})
    if prime_policy.get("pi_447_expected_value") != 86 or prime_policy.get("not_prime_86") is not True:
        errors.append("pi(447)=86 policy missing or malformed")
    return _result(errors)


def validate_stage6h_number_fact_overlays() -> stage6.ValidationResult:
    record = read_yaml(OPERATOR_CONSOLE_PATHS["number_fact_overlays"])
    overlays = record.get("overlays", [])
    by_id = {item.get("overlay_id"): item for item in overlays}
    errors = []
    if record.get("overlay_count") != len(OVERLAY_IDS):
        errors.append("Stage 6H overlay_count must equal required overlay count")
    for overlay_id in OVERLAY_IDS:
        item = by_id.get(overlay_id)
        if not item:
            errors.append(f"missing overlay {overlay_id}")
            continue
        if item.get("usable_for_decision_now") is not False:
            errors.append(f"{overlay_id}: usable_for_decision_now must be false")
        if item.get("not_allowed_as") != NOT_ALLOWED_AS:
            errors.append(f"{overlay_id}: not_allowed_as mismatch")
        if overlay_id == "stage6h_branch_concat_447_primepi86_overlay":
            policy = item.get("prime_count_policy", {})
            if policy.get("pi_447_expected_value") != 86 or policy.get("not_prime_86") is not True:
                errors.append("prime-pi86 overlay must state pi(447), not prime(86)")
    return _result(errors, number_fact_overlay_count=len(overlays), source_browser_overlay_deferment_count=0)


def validate_stage6h_future_diagnostics() -> stage6.ValidationResult:
    record = read_yaml(TOKEN_BLOCK_PATHS["future_diagnostic_registry"])
    diagnostics = record.get("future_diagnostics", [])
    expected = DOT_DIAGNOSTICS + PDD153_DIAGNOSTICS + ROUTE_CIPHER_DIAGNOSTICS
    errors = []
    if [item.get("diagnostic_id") for item in diagnostics] != expected:
        errors.append("future diagnostic IDs/order mismatch")
    if record.get("future_diagnostic_counts", {}).get("total_stage6h_future_diagnostic_count_expected") != 33:
        errors.append("future diagnostic count must be 33")
    for item in diagnostics:
        for flag in [
            "stage6h_run_now",
            "execution_enabled_now",
            "stage7_execution_enabled_now",
            "route_stream_generated_now",
            "byte_stream_generated_now",
            "cipher_execution_performed_now",
            "scoring_performed_now",
            "result_archive_created_now",
        ]:
            if item.get(flag) is not False:
                errors.append(f"{item.get('diagnostic_id')}: {flag} must be false")
        if item.get("full_output_archive_required_when_run_later") is not True:
            errors.append(f"{item.get('diagnostic_id')}: missing full-output archive requirement")
        if item.get("no_lossy_filtering_required_when_run_later") is not True:
            errors.append(f"{item.get('diagnostic_id')}: missing no-lossy requirement")
    return _result(errors, future_diagnostic_count=len(diagnostics))


def validate_stage6h_stage6i_addendum() -> stage6.ValidationResult:
    payload = read_yaml(TOKEN_BLOCK_PATHS["stage6i_manifest_input_addendum"])
    errors = []
    if payload.get("stage6i_addendum_required") is not True:
        errors.append("Stage 6I addendum required flag missing")
    if payload.get("not_final_stage7_manifest") is not True:
        errors.append("Stage 6I addendum must not be final Stage 7 manifest")
    if payload.get("stage7_execution_allowed_from_this_addendum") is not False:
        errors.append("Stage 6I addendum must keep execution false")
    for row in payload.get("stage6i_addendum_inputs", []):
        path = Path(row.get("path", ""))
        if not path.exists():
            errors.append(f"Stage 6I addendum input path missing: {path}")
    required_labels = {
        "stage6c_ouroboros_i31_inputs",
        "stage6d_doublet_boundary_inputs",
        "stage6e_bridge_traceability_inputs",
        "stage6f_acceptance_traceability_alias_dju_bei_repairs",
        "stage6g_current_doc_handoff_backlog_repair",
        "stage6h_source_lock_records",
        "stage6h_disabled_future_diagnostics",
    }
    if {row.get("input_id") for row in payload.get("stage6i_addendum_inputs", [])} != required_labels:
        errors.append("Stage 6I addendum input IDs mismatch")
    return _result(errors)


def validate_stage6h_source_browser_loadability() -> stage6.ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    errors = []
    if record.get("source_browser_validation_error_count") != 0:
        errors.append("Source Browser validation errors must be zero")
    return _result(errors, source_browser_entries_loaded=record.get("source_browser_entries_loaded", 0))


def validate_stage6h_current_stage_transition() -> stage6.ValidationResult:
    return validate_stage6h_current_state_integrity()


def validate_stage6h_gate_closure() -> stage6.ValidationResult:
    errors = []
    for path in DATA_PATHS.values():
        payload = read_yaml(path)
        if isinstance(payload, dict):
            for flag in FORBIDDEN_FALSE:
                if payload.get(flag) not in (False, None):
                    errors.append(f"{path}: guardrail {flag} must be false")
    return _result(errors, guardrail_count=len(FORBIDDEN_FALSE))


def validate_stage6h_handoff() -> stage6.ValidationResult:
    errors = []
    if not CODEX_COMPLETION_PATH.exists():
        errors.append("Stage 6H ignored completion summary missing locally")
    if CODEX_COMPLETION_PATH.exists():
        text = CODEX_COMPLETION_PATH.read_text(encoding="utf-8")
        for required in [
            "visual_dot_source_lock_record_count:",
            "pdd153_geometry_source_lock_record_count:",
            "number_fact_overlay_count:",
            "future_diagnostic_count:",
            "stage6i_final_manifest_blocker_count:",
        ]:
            if required not in text:
                errors.append(f"completion summary missing {required}")
    return _result(errors)


def stage6h_summary_text() -> str:
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    return "\n".join(
        [
            f"stage_id: {summary.get('stage_id')}",
            f"status: {summary.get('status')}",
            f"previous_stage_id: {summary.get('previous_stage_id')}",
            f"recommended_next_stage_id: {summary.get('recommended_next_stage_id')}",
            f"stage6h_source_lock_blocker_count: {summary.get('stage6h_source_lock_blocker_count')}",
            f"number_fact_overlay_count: {summary.get('number_fact_overlay_count')}",
            f"future_diagnostic_count: {summary.get('future_diagnostic_count')}",
            f"stage6i_final_manifest_blocker_count: {summary.get('stage6i_final_manifest_blocker_count')}",
        ]
    )


def _records() -> dict[str, dict[str, Any]]:
    source_browser = stage6f._source_browser_summary()  # Reuse established Source Browser smoke.
    overlay_blockers = 0
    blocker_counts = {
        "current_state_repair_blocker_count": 0,
        "doc_staleness_repair_blocker_count": 0,
        "source_lock_record_blocker_count": 0,
        "source_browser_overlay_blocker_count": overlay_blockers,
        "future_diagnostic_blocker_count": 0,
        "canonical_source_crosscheck_blocker_count": 0,
        "stage6i_final_manifest_blocker_count": overlay_blockers,
    }
    base_summary = _base_project_record("stage6h_summary") | {
        "status": "complete",
        "previous_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE_FINAL if overlay_blockers == 0 else NEXT_STAGE_TITLE_REPAIR,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE_FINAL if overlay_blockers == 0 else NEXT_PROMPT_TYPE_REPAIR,
        "stage6i_addendum_required": True,
        "stage6i_addendum_path": TOKEN_BLOCK_PATHS["stage6i_manifest_input_addendum"].as_posix(),
        "visual_dot_source_lock_record_count": len(VISUAL_DOT_RECORD_IDS),
        "pdd153_geometry_source_lock_record_count": len(PDD153_RECORD_IDS),
        "pdd_transform_record_count": len(PDD_TRANSFORM_RECORD_IDS),
        "residue_bridge_record_count": len(RESIDUE_RECORD_IDS),
        "route_cipher_policy_record_count": len(ROUTE_CIPHER_RECORD_IDS),
        "number_fact_overlay_count": len(OVERLAY_IDS),
        "future_diagnostic_count": 33,
        "source_browser_overlay_deferment_count": overlay_blockers,
        "stage6h_source_lock_blocker_count": overlay_blockers,
        **blocker_counts,
    }
    return {
        "summary": base_summary,
        "next_stage_decision": _next_stage_decision(blocker_counts),
        "stage6g_preservation": _base_project_record("stage6h_stage6g_preservation") | {
            "stage6g_preserved": True,
            "stage6g_current_doc_repairs_preserved": True,
            "stage6g_stage6h_backlog_consumed_by_stage6h": True,
        },
        "current_state_integrity_repair": _current_state_integrity_repair(),
        "doc_staleness_source_truth_repair": _base_project_record("stage6h_doc_staleness_source_truth_repair") | {
            "repair_target": DOC_STALENESS_SOURCE_OF_TRUTH_PATH.as_posix(),
            "stale_stage6f_final_manifest_fields_repaired": True,
            "historical_stage5ah_fields_superseded_by_stage6h_current_truth": True,
        },
        "operational_file_map_repair": _base_project_record("stage6h_operational_file_map_repair") | {
            "repair_target": "docs/onboarding/operational-file-map.md",
            "stage5ed_stage5ee_current_command_examples_removed": True,
            "stage6h_stage6i_examples_added": True,
        },
        "source_lock_summary": _source_lock_summary(blocker_counts),
        "exact_constants": _base_project_record("stage6h_exact_constants_validation") | {
            "stage6h_exact_constants_must_be_validated": EXACT_CONSTANTS,
            "prime_count_policy": _prime_count_policy(),
        },
        "number_fact_overlay_summary": _base_project_record("stage6h_number_fact_overlay_summary") | {
            "stage6h_number_fact_overlays_required": True,
            "required_stage6h_overlay_count_minimum": len(OVERLAY_IDS),
            "required_overlay_ids": OVERLAY_IDS,
            "overlay_count": len(OVERLAY_IDS),
            "source_browser_overlay_deferment_allowed_only_as_blocker": True,
            "source_browser_overlay_deferment_count": overlay_blockers,
        },
        "future_diagnostic_summary": _base_project_record("stage6h_future_diagnostic_summary") | {
            "future_diagnostic_counts": _future_diagnostic_counts(),
            "future_diagnostic_count": 33,
        },
        "source_browser_loadability_summary": _base_project_record("stage6h_source_browser_loadability_summary") | {
            "source_browser_validation_error_count": source_browser.get("source_browser_validation_error_count", 0),
            "source_browser_entries_loaded": source_browser.get("source_browser_entries_loaded", 0),
            "source_browser_paths_validated": True,
            "number_fact_overlay_count": len(OVERLAY_IDS),
        },
        "blocker_register": _blocker_register(blocker_counts),
        "current_stage_transition": _base_project_record("stage6h_current_stage_transition") | {
            "latest_completed_stage_id": STAGE_ID,
            "previous_completed_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            **blocker_counts,
        },
        "prior_stage_repair_ledger": _prior_stage_repair_ledger(),
        "reviewable_validation_evidence": _base_project_record("stage6h_reviewable_validation_evidence") | {
            "final_validation_order_recorded": True,
            "current_state_integrity_tests_path": "tests/python/test_stage6h_current_state_integrity.py",
            "stage6h_tests_path": "tests/python/test_stage6h_source_lock.py",
        },
        "chatgpt_context_update": _base_project_record("stage6h_chatgpt_context_update_summary") | {
            "chatgpt_context_updated": True,
            "required_stage6h_topics_recorded": True,
        },
        "gate_closure": _base_project_record("stage6h_gate_closure") | {
            "all_guardrails_false": True,
            "guardrail_count": len(FORBIDDEN_FALSE),
        },
        "handoff_policy": _base_project_record("stage6h_handoff_policy") | {
            "codex_completion_path": CODEX_COMPLETION_PATH.as_posix(),
            "codex_completion_committed": False,
            "actual_values_required_after_ci": True,
        },
        **_source_harvester_records(),
        **_token_block_records(),
        **_historical_route_records(),
        "number_fact_overlays": _overlay_collection(),
    }


def _source_harvester_records() -> dict[str, dict[str, Any]]:
    return {
        "recent_chat_provenance": _base_source_record("stage6h_recent_chat_transcript_source_lock") | {
            "recent_chat_transcript_local_file_present": False,
            "recent_chat_transcript_prompt_attached_context_present": True,
            "recent_chat_transcript_raw_committed_now": False,
            "used_as_operator_assistant_analysis_context": True,
            "used_as_canonical_image_proof": False,
            "used_as_canonical_transcription_proof": False,
            "requires_canonical_source_crosscheck": True,
        },
        "canonical_image_root_crosswalk": _base_source_record("stage6h_canonical_iddqd_v2_image_root_crosswalk") | {
            "canonical_local_root_for_iddqd_v2": "third_party/CiadaSolversIddqd_v2",
            "canonical_image_root": "third_party/CiadaSolversIddqd_v2/liber-primus__images--full",
            "present_locally_for_stage6h_metadata": Path(
                "third_party/CiadaSolversIddqd_v2/liber-primus__images--full"
            ).exists(),
            "ci_test_policy_require_ignored_root_exists": False,
            "stage7_execution_requires_local_presence_recheck": True,
        },
        "number_triangle_crosswalk": _base_source_record("stage6h_number_triangle_source_record_crosswalk") | {
            "source_records": [
                "data/historical-route/stage5ei-pdd153-geometry-candidates.yaml",
                "data/historical-route/stage5ds-pdd153-56311-ouroboric-cycle-candidate-v0.yaml",
                "data/historical-route/stage6c-ouroboros-t16-i-pdd153-delta14-candidate-v0.yaml",
            ],
            "committed_metadata_sufficient_for_stage6h_source_lock": True,
            "canonical_source_crosscheck_required_before_execution": True,
        },
        "raw_source_noncommit_proof": _base_source_record("stage6h_raw_source_noncommit_proof") | {
            "raw_third_party_files_committed": False,
            "generated_outputs_committed": False,
            "codex_output_committed": False,
            "generated_masks_committed": False,
        },
        "codex_handoff_policy": _base_source_record("stage6h_codex_handoff_policy") | {
            "codex_completion_path": CODEX_COMPLETION_PATH.as_posix(),
            "codex_completion_committed": False,
            "post_ci_actual_values_required": True,
        },
    }


def _token_block_records() -> dict[str, dict[str, Any]]:
    return {
        "stage6i_manifest_input_addendum": _stage6i_addendum(),
        "future_diagnostic_registry": _future_diagnostic_registry(),
        "no_active_ingestion_proof": _base_token_record("stage6h_no_active_ingestion_proof") | {
            "active_ingestion_performed": False,
        },
        "no_byte_stream_transition_gate": _base_token_record("stage6h_no_byte_stream_transition_gate") | {
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "byte_stream_generation_authorized_now": False,
        },
        "no_execution_transition_gate": _base_token_record("stage6h_no_execution_transition_gate") | {
            "execution_performed": False,
            "probe_execution_performed_now": False,
            "stage7_execution_allowed_next": False,
        },
    }


def _historical_route_records() -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for record_id in VISUAL_DOT_RECORD_IDS:
        records[record_id] = _visual_dot_record(record_id)
    for record_id in PDD153_RECORD_IDS:
        records[record_id] = _pdd153_record(record_id)
    records["stage6h-pdd153-pdd-minus-reversed-word52-way-verified-v0"] = _word52_record()
    records["stage6h-pdd153-pdd-minus-reversed-word55-read-prefix-candidate-v0"] = _word55_record()
    records["stage6h-pdd153-56311-skeleton-way-read-route-candidate-v0"] = _pdd_skeleton_record()
    records["stage6h-pdd153-i-am-circumference-mod153-left-edge-bridge-v0"] = _i_am_circumference_record()
    records["stage6h-ouroboros-variant-mod153-offset-bridge-v0"] = _ouroboros_variant_record()
    records["stage6h-pdd153-ouroboros-offset-cycle-policy-v0"] = _ouroboros_cycle_policy_record()
    for record_id in ROUTE_CIPHER_RECORD_IDS:
        records[record_id] = _route_cipher_record(record_id)
    return records


def _visual_dot_record(record_id: str) -> dict[str, Any]:
    payload = _base_historical_record(record_id) | {
        "source_status": "operator_assistant_observed_context_pending_canonical_crosscheck",
        "visual_measurement_boundary": _visual_measurement_boundary(),
        "canonical_measurement_discrepancy_policy": _discrepancy_policy(),
    }
    if record_id == "stage6h-three-dot-dinkus-scaled-7-8-angle41-bridge-v0":
        payload |= {
            "three_dot_angle": EXACT_CONSTANTS["three_dot_angle"],
            "derived_angle_to_center_policy": "angle approximately 41 degrees bridges to PDD153 center position/index 41",
        }
    if record_id == "stage6h-branch-dot-five-slot-binary-order-policy-table-v0":
        payload |= _branch_order_policy()
    if record_id == "stage6h-branch-dot-left-right-concat-479-lag5-bridge-v0":
        payload |= {"branch_bridge": _branch_bridges()["direct_concat_479"]}
    if record_id == "stage6h-branch-dot-geometric-concat-primepi86-control-v0":
        payload |= {"branch_bridge": _branch_bridges()["weaker_primepi86_control"], "prime_count_policy": _prime_count_policy()}
    if "mayfly" in record_id or "signpost" in record_id:
        payload |= {"display_priority": "low", "candidate_strength": "weak_control_candidate"}
    return payload


def _pdd153_record(record_id: str) -> dict[str, Any]:
    payload = _base_historical_record(record_id) | {
        "pdd153_constants": EXACT_CONSTANTS["pdd153"],
        "right_angle_transform": _right_angle_transform(),
        "visual_measurement_boundary": _visual_measurement_boundary(),
        "canonical_measurement_discrepancy_policy": _discrepancy_policy(),
    }
    if "center-to-d4-position133" in record_id:
        payload |= {
            "visual_7_8_ray": _visual_7_8_ray(),
            "center_anchor_gp41_claim_policy": _center_anchor_gp41_policy(),
        }
    if "complement-8-7" in record_id:
        payload |= {"visual_8_7_complement": _visual_8_7_complement()}
    if "folded-7-8-8-7" in record_id:
        payload |= {"folded_7_8_8_7": _folded_7_8_8_7()}
    if "72-9-72" in record_id or "shared-spine" in record_id:
        payload |= {"vertical_split": _vertical_split()}
    return payload


def _word52_record() -> dict[str, Any]:
    return _base_historical_record("stage6h-pdd153-pdd-minus-reversed-word52-way-verified-v0") | {
        "word52_way": {
            "heading": "PDD",
            "heading_indices_zero_based": [13, 23, 2],
            "word_position": 52,
            "word_runes": "\u16b3\u16e0\u16b7",
            "word_indices_zero_based": [5, 28, 6],
            "reversed_word_indices": [6, 28, 5],
            "operation": "heading_minus_reversed_word_mod29",
            "result_indices": [7, 24, 26],
            "result_latin": "WAY",
        }
    }


def _word55_record() -> dict[str, Any]:
    return _base_historical_record("stage6h-pdd153-pdd-minus-reversed-word55-read-prefix-candidate-v0") | {
        "word55_read_prefix": {
            "heading": "PDD",
            "word_position": 55,
            "word_runes": "\u16c7\u16a3\u16dd\u16c4\u16dd\u16d7\u16b9\u16b3\u16be",
            "word_latin_tokens": ["EO", "Y", "ING", "J", "ING", "M", "W", "C", "N"],
            "word_indices_zero_based": [12, 26, 21, 11, 21, 19, 7, 5, 9],
            "reversed_word_indices": [9, 5, 7, 19, 21, 11, 21, 26, 12],
            "heading_repeated_indices": [13, 23, 2, 13, 23, 2, 13, 23, 2],
            "result_indices": [4, 18, 24, 23, 2, 20, 21, 26, 19],
            "result_latin_tokens": ["R", "E", "A", "D", "TH", "L", "ING", "Y", "M"],
            "result_prefix": "READ",
            "full_plaintext_claimed": False,
        },
        "risk_notes": [
            "READ_prefix_does_not_continue_as_full_plaintext_under_first_pass",
            "transform_does_not_solve_PDD153",
            "route_output_may_be_ciphertext_or_control_surface",
            "controls_required_for_word_selection_bias",
        ],
    }


def _pdd_skeleton_record() -> dict[str, Any]:
    return _base_historical_record("stage6h-pdd153-56311-skeleton-way-read-route-candidate-v0") | {
        "path_56311": EXACT_CONSTANTS["pdd153"]["path_56311"],
        "offsets_56311": EXACT_CONSTANTS["pdd153"]["offsets_56311"],
        "word52_result": "WAY",
        "word55_prefix": "READ",
        "full_plaintext_claimed": False,
        "candidate_fragment_caveat_required": True,
    }


def _i_am_circumference_record() -> dict[str, Any]:
    return _base_historical_record("stage6h-pdd153-i-am-circumference-mod153-left-edge-bridge-v0") | {
        "i_am_circumference_mod153": {
            "I_AM_gp": 199,
            "I_AM_mod153": 46,
            "CIRCUMFERENCE_gp": 398,
            "CIRCUMFERENCE_mod153": 92,
            "relation": ["CIRCUMFERENCE = 2 * I AM", "92 = 2 * 46"],
            "triangle_crosslinks": ["position_46_left_edge_row10", "position_46_member_of_56311_path"],
        }
    }


def _ouroboros_variant_record() -> dict[str, Any]:
    return _base_historical_record("stage6h-ouroboros-variant-mod153-offset-bridge-v0") | {
        "ouroboros_variants": {
            "UROBOROS": {"gp_total": 160, "pdd153_excess": 7, "triangle_crosslink": "d4_diagonal_starts_at_position_7"},
            "OROBOROS": {"gp_total": 164, "pdd153_excess": 11, "centre_plus_offset": 52, "crosslink": "WAY_anchor"},
            "OUROBOROS": {
                "gp_total": 167,
                "pdd153_excess": 14,
                "centre_plus_offset": 55,
                "crosslink": "READ_prefix_candidate_and_right_edge_56311_path_member",
            },
        }
    }


def _ouroboros_cycle_policy_record() -> dict[str, Any]:
    return _base_historical_record("stage6h-pdd153-ouroboros-offset-cycle-policy-v0") | {
        "offset_policy": "review_only_variant_offset_context",
        "offsets": {"UROBOROS": 7, "OROBOROS": 11, "OUROBOROS": 14},
        "route_seed_now": False,
    }


def _route_cipher_record(record_id: str) -> dict[str, Any]:
    return _base_historical_record(record_id) | {
        "route_cipher_readiness_policy": (
            "A correct reading order may emit ciphertext, key material, a control stream, "
            "a null/copy mask, an index stream, or another intermediate surface."
        ),
        "plaintext_required_for_future_interest": False,
        "vigenere_assumed_likely": False,
        "vigenere_retained_as_baseline_control": True,
        "cipher_execution_performed_now": False,
        "route_stream_generated_now": False,
    }


def _overlay_collection() -> dict[str, Any]:
    overlays = [_overlay(overlay_id, index + 1) for index, overlay_id in enumerate(OVERLAY_IDS)]
    return _base_operator_record("stage6h_dot_angle_right_triangle_source_lock_overlay_collection") | {
        "review_batch_id": "stage6h_dot_angle_right_triangle_review_only",
        "stage6h_number_fact_overlays_required": True,
        "source_browser_overlay_deferment_allowed_only_as_blocker": True,
        "overlay_count": len(overlays),
        "required_overlay_ids": OVERLAY_IDS,
        "overlays": overlays,
    }


def _overlay(overlay_id: str, display_order: int) -> dict[str, Any]:
    record_path, label, expression, relation = _overlay_spec(overlay_id)
    overlay = {
        "overlay_id": overlay_id,
        "source_record_path": record_path,
        "source_fact_id": overlay_id.replace("_overlay", "_fact"),
        "fact_class": "stage6h_review_only_number_fact",
        "display_label": label,
        "short_label": label[:64],
        "value": relation,
        "values": [relation],
        "value_type": "sequence" if "pdd153" in overlay_id else "sum",
        "operation_type": "source_observation",
        "expression": expression,
        "relation": relation,
        "why_stored": "Preserve Stage 6H dot-angle/right-triangle source-lock context as review-only metadata.",
        "verification_status": "operator_assistant_observed",
        "review_state": "overlay_enriched_fact",
        "display_priority": "low" if "447" in overlay_id else "medium",
        "source_paths": [
            record_path,
            "data/historical-route/stage5ei-pdd153-geometry-candidates.yaml",
            "data/profiles/gematria/gematria-primus-v0.json",
        ],
        "crosslinks": [record_path],
        "risk_notes": ["review_only", "not_route_evidence", "canonical_source_crosscheck_required"],
        "controls_required": [
            "canonical_source_crosscheck",
            "selection_bias_controls",
            "wrong_route_negative_controls",
            "no_plaintext_required_output_policy",
        ],
        "usable_for_decision_now": False,
        "not_allowed_as": NOT_ALLOWED_AS,
        "display_order": display_order,
    }
    if overlay_id == "stage6h_branch_concat_447_primepi86_overlay":
        overlay["prime_count_policy"] = _prime_count_policy()
    return overlay


def _overlay_spec(overlay_id: str) -> tuple[str, str, str, str]:
    specs = {
        "stage6h_three_dot_7_8_angle41_overlay": (
            "stage6h-three-dot-dinkus-scaled-7-8-angle41-bridge-v0",
            "three-dot 7:8 angle 41.1859",
            "atan(7/8) = 41.1859 degrees",
            "angle approximately 41 degrees bridges to PDD153 center index 41",
        ),
        "stage6h_branch_right_11111_31_overlay": (
            "stage6h-branch-dot-right-cluster-11111-gp31-bridge-v0",
            "branch right 11111 = 31",
            "right branch bits 11111 = 31",
            "31 review-only branch-dot candidate",
        ),
        "stage6h_branch_left_01110_14_inverse17_overlay": (
            "stage6h-branch-dot-left-yx-01110-14-inverse17-candidate-v0",
            "branch left 01110 = 14, inverse 17",
            "left y/x black bits 01110 = 14; white inverse 10001 = 17",
            "14/17 review-only branch ordering context",
        ),
        "stage6h_branch_concat_479_lag5_overlay": (
            "stage6h-branch-dot-left-right-concat-479-lag5-bridge-v0",
            "branch concat 479 and Lag5",
            "01110 + 11111 -> 0111011111 = 479",
            "479 crosslinks to Stage 6D Lag5 equal count",
        ),
        "stage6h_branch_concat_447_primepi86_overlay": (
            "stage6h-branch-dot-geometric-concat-primepi86-control-v0",
            "branch concat 447 and pi(447)=86",
            "01101 + 11111 -> 0110111111 = 447; pi(447)=86",
            "86 crosslinks to Stage 6D lag1 count as a weak control",
        ),
        "stage6h_pdd153_right_angle_transform_overlay": (
            "stage6h-pdd153-right-angle-coordinate-transform-v0",
            "PDD153 right-angle transform",
            "x=c-1, y=r-c, x+y<=16",
            "review-only coordinate transform",
        ),
        "stage6h_pdd153_vertical_split_72_9_72_overlay": (
            "stage6h-pdd153-folded-triangle-72-9-72-spine-split-candidate-v0",
            "PDD153 vertical split 72|9|72",
            "153 = 72 + 9 + 72",
            "central spine split candidate",
        ),
        "stage6h_pdd153_shared_spine_81_81_overlay": (
            "stage6h-pdd153-shared-spine-two-81-cell-surfaces-candidate-v0",
            "PDD153 shared spine 81/81",
            "72+9 = 81 on each shared-spine side",
            "9x9 surface candidate",
        ),
        "stage6h_pdd153_7_8_ray_133_d4_overlay": (
            "stage6h-pdd153-dot-angle41-center-to-d4-position133-bridge-v0",
            "PDD153 7:8 ray to 133/d4",
            "position 41 + delta row 7 col 8 -> position 133 on d4",
            "review-only angle/ray bridge",
        ),
        "stage6h_pdd153_folded_7_8_8_7_hits_50_51_overlay": (
            "stage6h-pdd153-folded-7-8-8-7-seam-50-51-candidate-v0",
            "folded 7:8/8:7 hits 50/51",
            "folded endpoints 50 and 51",
            "row10 seam candidate",
        ),
        "stage6h_pdd153_row10_seam_49_52_50_51_overlay": (
            "stage6h-pdd153-row10-seam-49-52-50-51-way-candidate-v0",
            "PDD153 row10 seam 49/52 and 50/51",
            "row10 seam around WAY/READ candidate anchors",
            "review-only seam context",
        ),
        "stage6h_pdd153_word52_way_overlay": (
            "stage6h-pdd153-pdd-minus-reversed-word52-way-verified-v0",
            "word52 PDD transform gives WAY",
            "PDD - reversed word52 mod29 = WAY",
            "verified fragment only",
        ),
        "stage6h_pdd153_word55_read_prefix_overlay": (
            "stage6h-pdd153-pdd-minus-reversed-word55-read-prefix-candidate-v0",
            "word55 PDD transform gives READ prefix",
            "PDD - reversed word55 mod29 starts READ",
            "prefix only, not full plaintext",
        ),
        "stage6h_i_am_circumference_mod153_overlay": (
            "stage6h-pdd153-i-am-circumference-mod153-left-edge-bridge-v0",
            "I AM/CIRCUMFERENCE mod153 bridge",
            "199 mod153=46; 398 mod153=92=2*46",
            "left-edge/56311 review bridge",
        ),
        "stage6h_ouroboros_variant_mod153_offsets_overlay": (
            "stage6h-ouroboros-variant-mod153-offset-bridge-v0",
            "OUROBOROS variant offsets 7/11/14",
            "UROBOROS +7, OROBOROS +11, OUROBOROS +14 over PDD153",
            "review-only offset context",
        ),
    }
    record_id, label, expression, relation = specs[overlay_id]
    return HISTORICAL_ROUTE_PATHS[record_id].as_posix(), label, expression, relation


def _future_diagnostic_registry() -> dict[str, Any]:
    diagnostics = []
    for group, ids in [
        ("dot", DOT_DIAGNOSTICS),
        ("pdd153", PDD153_DIAGNOSTICS),
        ("route_cipher", ROUTE_CIPHER_DIAGNOSTICS),
    ]:
        for diagnostic_id in ids:
            diagnostics.append(
                {
                    "diagnostic_id": diagnostic_id,
                    "diagnostic_group": group,
                    "stage6h_run_now": False,
                    "execution_enabled_now": False,
                    "stage7_execution_enabled_now": False,
                    "route_stream_generated_now": False,
                    "byte_stream_generated_now": False,
                    "cipher_execution_performed_now": False,
                    "scoring_performed_now": False,
                    "result_archive_created_now": False,
                    "full_output_archive_required_when_run_later": True,
                    "no_lossy_filtering_required_when_run_later": True,
                    "usable_for_decision_now": False,
                    "not_allowed_as": NOT_ALLOWED_AS,
                }
            )
    return _base_token_record("stage6h_future_diagnostic_registry") | {
        "future_diagnostic_counts": _future_diagnostic_counts(),
        "future_diagnostics": diagnostics,
    }


def _stage6i_addendum() -> dict[str, Any]:
    rows = [
        ("stage6c_ouroboros_i31_inputs", "data/token-block/stage6c-stage6d-manifest-input-addendum.yaml"),
        ("stage6d_doublet_boundary_inputs", "data/token-block/stage6d-stage6e-manifest-input-addendum.yaml"),
        ("stage6e_bridge_traceability_inputs", "data/token-block/stage6e-stage6f-manifest-input-addendum.yaml"),
        (
            "stage6f_acceptance_traceability_alias_dju_bei_repairs",
            "data/token-block/stage6f-stage6g-manifest-input-addendum.yaml",
        ),
        ("stage6g_current_doc_handoff_backlog_repair", "data/token-block/stage6g-stage6h-manifest-input-addendum.yaml"),
        ("stage6h_source_lock_records", PROJECT_STATE_PATHS["source_lock_summary"].as_posix()),
        ("stage6h_disabled_future_diagnostics", TOKEN_BLOCK_PATHS["future_diagnostic_registry"].as_posix()),
    ]
    return _base_token_record("stage6h_stage6i_manifest_input_addendum") | {
        "stage6i_addendum_required": True,
        "stage6i_addendum_path": TOKEN_BLOCK_PATHS["stage6i_manifest_input_addendum"].as_posix(),
        "stage6i_addendum_inputs": [
            {
                "input_id": input_id,
                "path": path,
                "path_exists_at_build_time": Path(path).exists() or input_id.startswith("stage6h_"),
            }
            for input_id, path in rows
        ],
        "path_substitution_ledger": [],
        "not_final_stage7_manifest": True,
        "stage7_execution_allowed_from_this_addendum": False,
        "stage7_zip_archive_creation_allowed_from_this_addendum": False,
    }


def _current_state_integrity_repair() -> dict[str, Any]:
    return _base_project_record("stage6h_current_state_integrity_repair") | {
        "repair_target": CURRENT_STAGE_STATE_PATH.as_posix(),
        "top_stage_id_repaired_to": STAGE_ID,
        "nested_latest_completed_stage_repaired_to": STAGE_ID,
        "nested_next_stage_repaired_to": NEXT_STAGE_ID,
        "stale_stage6g_final_manifest_required_removed": True,
        "stale_stage6g_can_attempt_final_manifest_without_prior_repair_removed": True,
        "post_push_handoff_path": CODEX_COMPLETION_PATH.as_posix(),
        "current_state_integrity_test_path": "tests/python/test_stage6h_current_state_integrity.py",
    }


def _source_lock_summary(blocker_counts: dict[str, int]) -> dict[str, Any]:
    return _base_project_record("stage6h_dot_angle_pdd153_source_lock_summary") | {
        "visual_dot_source_lock_record_count": len(VISUAL_DOT_RECORD_IDS),
        "pdd153_geometry_source_lock_record_count": len(PDD153_RECORD_IDS),
        "pdd_transform_record_count": len(PDD_TRANSFORM_RECORD_IDS),
        "residue_bridge_record_count": len(RESIDUE_RECORD_IDS),
        "route_cipher_policy_record_count": len(ROUTE_CIPHER_RECORD_IDS),
        "center_anchor_gp41_claim_policy": _center_anchor_gp41_policy(),
        "visual_measurement_boundary": _visual_measurement_boundary(),
        "canonical_measurement_discrepancy_policy": _discrepancy_policy(),
        **blocker_counts,
    }


def _next_stage_decision(blocker_counts: dict[str, int]) -> dict[str, Any]:
    blockers = blocker_counts["stage6i_final_manifest_blocker_count"]
    return _base_project_record("stage6h_next_stage_decision") | {
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE_FINAL if blockers == 0 else NEXT_STAGE_TITLE_REPAIR,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE_FINAL if blockers == 0 else NEXT_PROMPT_TYPE_REPAIR,
        "stage6i_final_manifest_required": blockers == 0,
        "stage6i_repair_required_before_final_manifest": blockers > 0,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
        **blocker_counts,
    }


def _blocker_register(blocker_counts: dict[str, int]) -> dict[str, Any]:
    return _base_project_record("stage6h_stage6i_readiness_blocker_register") | {
        **blocker_counts,
        "blockers": [],
    }


def _prior_stage_repair_ledger() -> dict[str, Any]:
    rows = [
        {
            "touched_file": DOC_STALENESS_SOURCE_OF_TRUTH_PATH.as_posix(),
            "prior_stage": "stage-5ah",
            "old_problem": "stale Stage 6F final-manifest current-ish fields survived Stage 6G",
            "new_value_or_policy": "Stage 6H current truth fields plus historical/superseded labeling",
            "why_patch_was_required": "active doc-staleness source-of-truth record must not mislead current-stage scanners",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "docs/onboarding/operational-file-map.md",
            "prior_stage": "current_doc_mirror",
            "old_problem": "Stage 5ED/Stage 5EE command examples appeared as current examples",
            "new_value_or_policy": "Stage 6H/Stage 6I placeholder/current examples",
            "why_patch_was_required": "operator called out exact stale command examples",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/token_block/stage6g.py",
            "prior_stage": "stage-6g",
            "old_problem": "current-stage validator assumed latest stage must remain Stage 6G",
            "new_value_or_policy": "validator accepts Stage 6H+ current-state while validating Stage 6G records",
            "why_patch_was_required": "prior-stage validators must not restore stale current-state fields",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/token_block/stage6b.py",
            "prior_stage": "stage-6b",
            "old_problem": "current-stage validator allowed later stages only through Stage 6G -> Stage 6H",
            "new_value_or_policy": "validator also accepts Stage 6H -> Stage 6I while preserving Stage 6B record checks",
            "why_patch_was_required": "Stage 6H must not roll back current-stage-state.yaml to satisfy historical validators",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/token_block/stage6c.py",
            "prior_stage": "stage-6c",
            "old_problem": "current-stage validator allowed later stages only through Stage 6G -> Stage 6H",
            "new_value_or_policy": "validator also accepts Stage 6H -> Stage 6I while preserving Stage 6C record checks",
            "why_patch_was_required": "Stage 6H must not roll back current-stage-state.yaml to satisfy historical validators",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/token_block/stage6d.py",
            "prior_stage": "stage-6d",
            "old_problem": "current-stage validator allowed later stages only through Stage 6G -> Stage 6H",
            "new_value_or_policy": "validator also accepts Stage 6H -> Stage 6I while preserving Stage 6D record checks",
            "why_patch_was_required": "Stage 6H must not roll back current-stage-state.yaml to satisfy historical validators",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/token_block/stage6e.py",
            "prior_stage": "stage-6e",
            "old_problem": "current-stage validator allowed later stages only through Stage 6G -> Stage 6H",
            "new_value_or_policy": "validator also accepts Stage 6H -> Stage 6I while preserving Stage 6E record checks",
            "why_patch_was_required": "Stage 6H must not roll back current-stage-state.yaml to satisfy historical validators",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/token_block/stage6f.py",
            "prior_stage": "stage-6f",
            "old_problem": "aggregate validator treated Stage 6H current state as unsupported later state",
            "new_value_or_policy": "validator accepts Stage 6H as historical-successor state while preserving Stage 6F record checks",
            "why_patch_was_required": "Stage 6H must not roll back current-stage-state.yaml to satisfy Stage 6F compatibility tests",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/token_block/stage5ea.py",
            "prior_stage": "stage-5ea",
            "old_problem": "current-stage registry validation stopped at Stage 6G",
            "new_value_or_policy": "validator accepts Stage 6H as a valid successor stage",
            "why_patch_was_required": "full pytest validates historical Stage 5EA current-registry isolation against the live Stage 6H state",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/token_block/stage5eb.py",
            "prior_stage": "stage-5eb",
            "old_problem": "current-stage registry policy allowed later stage pairs only through Stage 6G -> Stage 6H",
            "new_value_or_policy": "validator accepts Stage 6H -> Stage 6I as a valid successor pair",
            "why_patch_was_required": "full pytest validates historical Stage 5EB registry policy against the live Stage 6H state",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/token_block/stage5ef.py",
            "prior_stage": "stage-5ef",
            "old_problem": "current-truth validator allowed later stage pairs only through Stage 6G -> Stage 6H",
            "new_value_or_policy": "validator accepts Stage 6H -> Stage 6I as a valid successor pair",
            "why_patch_was_required": "historical current-truth validation must not require restoring old Stage 5EF current state",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/token_block/stage5eg.py",
            "prior_stage": "stage-5eg",
            "old_problem": "current-truth validator allowed later stage pairs only through Stage 6G -> Stage 6H",
            "new_value_or_policy": "validator accepts Stage 6H -> Stage 6I as a valid successor pair",
            "why_patch_was_required": "historical current-truth validation must not require restoring old Stage 5EG current state",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/token_block/stage5ei.py",
            "prior_stage": "stage-5ei",
            "old_problem": "current-mirror validator allowed later stage pairs only through Stage 6G -> Stage 6H",
            "new_value_or_policy": "validator accepts Stage 6H -> Stage 6I as a valid successor pair",
            "why_patch_was_required": "historical current-mirror validation must not require restoring old Stage 5EI current state",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "python/libreprimus/doc_staleness/validation.py",
            "prior_stage": "stage-5ah",
            "old_problem": "doc-staleness source-of-truth validation allowed successor stage IDs only through Stage 6G",
            "new_value_or_policy": "validator accepts Stage 6H source-of-truth repair records",
            "why_patch_was_required": "Stage 6H repairs the active Stage 5AH doc-staleness source-of-truth current fields",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
        {
            "touched_file": "schemas/project-state/doc-staleness-source-of-truth-record-v0.schema.json",
            "prior_stage": "stage-5ah",
            "old_problem": "shared source-of-truth schema rejected Stage 6I as recommended next stage",
            "new_value_or_policy": "schema accepts Stage 6I as current recommended next stage",
            "why_patch_was_required": "committed Stage 5AH source-of-truth record is active current-mirror metadata repaired by Stage 6H",
            "historical_payload_changed": False,
            "current_mirror_or_active_metadata_only": True,
            "source_lock_payload_changed": False,
        },
    ]
    return _base_project_record("stage6h_prior_stage_repair_ledger") | {"prior_stage_files_touched": rows}


def _write_current_stage_state() -> None:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    current.update(
        {
            "stage_id": STAGE_ID,
            "stage_title": STAGE_TITLE,
            "prompt_type": PROMPT_TYPE,
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "previous_completed_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE_FINAL,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE_FINAL,
            "post_push_handoff_locations": [CODEX_COMPLETION_PATH.as_posix(), "GitHub issue comment"],
            "latest_completed_stage": {
                "stage_id": STAGE_ID,
                "stage_title": STAGE_TITLE,
                "completed_commit": "",
                "completed_date": "2026-06-18",
                "status": "complete",
            },
            "next_stage": {
                "stage_id": NEXT_STAGE_ID,
                "stage_title": NEXT_STAGE_TITLE_FINAL,
                "prompt_type": NEXT_PROMPT_TYPE_FINAL,
            },
            "stage6h_current_state_integrity_repair_stage": True,
            "stage6h_source_lock_addendum_stage": True,
            "stage6i_addendum_required": True,
            "stage6i_addendum_path": TOKEN_BLOCK_PATHS["stage6i_manifest_input_addendum"].as_posix(),
            "stage6i_final_manifest_required": True,
            "stage6i_repair_required_before_final_manifest": False,
            "current_state_repair_blocker_count": 0,
            "doc_staleness_repair_blocker_count": 0,
            "source_lock_record_blocker_count": 0,
            "source_browser_overlay_blocker_count": 0,
            "future_diagnostic_blocker_count": 0,
            "canonical_source_crosscheck_blocker_count": 0,
            "stage6i_final_manifest_blocker_count": 0,
            "stage7_execution_allowed_next": False,
            "stage7_zip_archive_creation_allowed_next": False,
            "stage6h_final_finite_stage7_manifest_created_now": False,
            "stage6h_archive_run_contract_finalized_now": False,
            "stage6h_creates_stage7_result_archive_now": False,
            "stage6h_generates_stage7_outputs_now": False,
            "stage6h_routes_to_stage7_now": False,
            "stage6h_runs_any_probe_now": False,
            "stage7_manifest_created_now": False,
            "stage7_archive_created_now": False,
            "probe_execution_performed_now": False,
            "route_stream_generated_now": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "ocr_performed": False,
            "image_forensics_performed": False,
            "semantic_image_interpretation_performed": False,
            "solve_claim": False,
        }
    )
    for stale_key in [
        "stage6g_final_manifest_required",
        "stage6g_repair_required_before_final_manifest",
        "stage6g_can_attempt_final_manifest_without_prior_repair",
    ]:
        current[stale_key] = False
    write_yaml(CURRENT_STAGE_STATE_PATH, current)


def _write_doc_staleness_source_of_truth() -> None:
    payload = read_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE_FINAL,
            "recommended_next_stage_prefix": "Stage 6I",
            "latest_completed_stage_prefix": "Stage 6H",
            "expected_next_stage_prefix": "Stage 6I",
            "latest_completed_stage_after_this_stage": STAGE_TITLE,
            "next_stage_after_this_stage": NEXT_STAGE_TITLE_FINAL,
            "expected_latest_after_stage5ah": "historical; superseded by Stage 6H current truth",
            "expected_next_after_stage5ah": "historical; superseded by Stage 6H current truth",
            "recommended_next_stage_after_this_stage": NEXT_STAGE_TITLE_FINAL,
            "historical_stage5ah_fields_superseded_by_stage6h_current_truth": True,
            "current_handoff_path": CODEX_COMPLETION_PATH.as_posix(),
            "stage6h_current_truth_refresh": True,
        }
    )
    write_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH, payload)


def _write_docs() -> None:
    _replace_section(Path("README.md"), "## Current boundaries and deferred work", _readme_current_section())
    _replace_section(Path("AGENTS.md"), "## Current stage", _agents_current_section())
    _replace_section(Path("STATUS.md"), "## Current Stage", _status_current_section())
    _replace_section(Path("ROADMAP.md"), "## Current Direction", _roadmap_current_section())
    _replace_section(Path("TESTING.md"), "## Stage 6H Validation Targets", _testing_section())
    _replace_section(Path("ChatGPT-ContextFile.md"), "## Current Project State", _chatgpt_current_section())
    _replace_section(Path("docs/roadmap/staged-plan.md"), "## Current Project State", _staged_plan_current_section())
    _replace_section(Path("docs/roadmap/staged-plan.md"), "## Current Stage", _staged_plan_current_stage_section())
    _replace_section(Path("docs/onboarding/start-here.md"), "## Current State", _start_here_current_section())
    _replace_section(Path("docs/onboarding/source-of-truth-map.md"), "## Current Operational Truth", _source_truth_current_section())
    _replace_section(Path("docs/onboarding/operational-file-map.md"), "## Stage 6H Operational Files", _operational_file_map_section())
    _replace_section(Path("docs/reference/token-block-cli.md"), "## Stage 6H Token-Block CLI", _cli_docs_section())
    _remove_stale_operational_command_examples()
    _write_support_docs()


def _write_support_docs() -> None:
    _write_text(
        Path("docs/experiments/stage-6h-dot-angle-right-triangle-source-lock.md"),
        "# Stage 6H Dot-Angle Right-Triangle Source-Lock\n\nStage 6H records review-only dot-angle, branch-dot, PDD153, WAY/READ, residue, overlay, and disabled diagnostic metadata. It performs no route extraction, pixel-stream generation, OCR, image interpretation, cipher execution, Stage 7 manifest work, archive creation, or solve claim.\n",
    )
    _write_text(
        Path("docs/development-logs/2026-06-18-stage-6h-dot-angle-right-triangle-source-lock.md"),
        "# Stage 6H Development Log\n\nImplemented Stage 6H current-state repair, exact constants, source-lock records, required overlays, disabled diagnostics, and Stage 6I handoff metadata with all execution gates closed.\n",
    )
    _write_text(
        Path("research-log/2026-06-18-stage6h-next-stage-decision-summary.md"),
        "# Stage 6H Next-Stage Decision Summary\n\nStage 6H repairs Stage 6G current-state defects and source-locks dot-angle/right-triangle metadata. Stage 6I receives explicit handoff inputs by path and remains without execution.\n",
    )


def _write_operational_map() -> None:
    path = PROJECT_STATE_DIR / "operational-file-map.yaml"
    payload = read_yaml(path)
    record = {
        "stage_id": STAGE_ID,
        "summary": PROJECT_STATE_PATHS["summary"].as_posix(),
        "next_stage_decision": PROJECT_STATE_PATHS["next_stage_decision"].as_posix(),
        "stage6i_manifest_input_addendum": TOKEN_BLOCK_PATHS["stage6i_manifest_input_addendum"].as_posix(),
        "number_fact_overlays": OPERATOR_CONSOLE_PATHS["number_fact_overlays"].as_posix(),
        "future_diagnostic_registry": TOKEN_BLOCK_PATHS["future_diagnostic_registry"].as_posix(),
    }
    records = payload.setdefault("stage_records", {})
    if isinstance(records, dict):
        records[STAGE_ID] = record
    else:
        records = [item for item in records if not isinstance(item, dict) or item.get("stage_id") != STAGE_ID]
        records.append(record)
        payload["stage_records"] = records
    write_yaml(path, payload)


def _write_stage_summary_record(summary: dict[str, Any]) -> None:
    path = Path("data/research/stage-summary-records-v0.yaml")
    payload = read_yaml(path)
    records = payload.setdefault("stages", [])
    records = [item for item in records if item.get("stage_id") != STAGE_ID]
    records.append(
        {
            "stage_id": STAGE_ID,
            "stage_title": STAGE_TITLE,
            "status": "complete",
            "summary": "Repaired Stage 6G current-state/doc-staleness misses and added review-only dot-angle/right-triangle/PDD153 source-lock metadata.",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": summary["recommended_next_stage_title"],
            "guardrails": "No Stage 7 manifest, archive, probe execution, route stream, byte stream, image interpretation, target selection, or solve claim.",
        }
    )
    payload["stages"] = records
    write_yaml(path, payload)


def _write_completion_summary_stub(summary: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    _write_text(
        CODEX_COMPLETION_PATH,
        f"""# Stage 6H Codex Completion

starting_commit: {STARTING_COMMIT}
stage6h_implementation_commit: pending_commit
final_commit: pending_commit
origin_main_commit: pending_push
github_issue: pending_issue
final_ci_run_url: pending_ci
final_ci_status: pending_ci

visual_dot_source_lock_record_count: {summary['visual_dot_source_lock_record_count']}
pdd153_geometry_source_lock_record_count: {summary['pdd153_geometry_source_lock_record_count']}
pdd_transform_record_count: {summary['pdd_transform_record_count']}
residue_bridge_record_count: {summary['residue_bridge_record_count']}
route_cipher_policy_record_count: {summary['route_cipher_policy_record_count']}
number_fact_overlay_count: {summary['number_fact_overlay_count']}
future_diagnostic_count: {summary['future_diagnostic_count']}
source_browser_overlay_deferment_count: {summary['source_browser_overlay_deferment_count']}
current_state_repair_blocker_count: {summary['current_state_repair_blocker_count']}
doc_staleness_repair_blocker_count: {summary['doc_staleness_repair_blocker_count']}
source_lock_record_blocker_count: {summary['source_lock_record_blocker_count']}
source_browser_overlay_blocker_count: {summary['source_browser_overlay_blocker_count']}
future_diagnostic_blocker_count: {summary['future_diagnostic_blocker_count']}
canonical_source_crosscheck_blocker_count: {summary['canonical_source_crosscheck_blocker_count']}
stage6i_final_manifest_blocker_count: {summary['stage6i_final_manifest_blocker_count']}

path_evidence:
  current_state_repair: {CURRENT_STAGE_STATE_PATH.as_posix()}
  overlays: {OPERATOR_CONSOLE_PATHS['number_fact_overlays'].as_posix()}
  stage6i_addendum: {TOKEN_BLOCK_PATHS['stage6i_manifest_input_addendum'].as_posix()}
  source_lock_summary: {PROJECT_STATE_PATHS['source_lock_summary'].as_posix()}
  current_state_integrity_tests: tests/python/test_stage6h_current_state_integrity.py

stage6g_review_finding_closure:
  - finding_id: current_stage_state_top_identity_stage6f
    status: fixed
    evidence_path: {CURRENT_STAGE_STATE_PATH.as_posix()}
  - finding_id: current_stage_state_nested_latest_stage6f
    status: fixed
    evidence_path: {CURRENT_STAGE_STATE_PATH.as_posix()}
  - finding_id: current_stage_state_nested_next_stage6g_final_manifest
    status: fixed
    evidence_path: {CURRENT_STAGE_STATE_PATH.as_posix()}
  - finding_id: contradictory_stage6g_final_manifest_booleans
    status: fixed
    evidence_path: {CURRENT_STAGE_STATE_PATH.as_posix()}
  - finding_id: stage5ah_doc_staleness_source_truth_stale_stage6f_fields
    status: fixed_or_historicized
    evidence_path: {DOC_STALENESS_SOURCE_OF_TRUTH_PATH.as_posix()}
  - finding_id: operational_file_map_stage5ed_stage5ee_current_commands
    status: fixed
    evidence_path: docs/onboarding/operational-file-map.md
  - finding_id: stage6g_validators_missed_nested_current_state_contradictions
    status: fixed
    evidence_path: tests/python/test_stage6h_current_state_integrity.py

stage7_manifest_created_now: false
stage7_archive_created_now: false
probe_execution_performed_now: false
route_stream_generated_now: false
byte_stream_generated_now: false
solve_claim: false
completion_summary_updated_after_final_ci: false
""",
    )


def _write_schemas() -> None:
    for key, path in DATA_PATHS.items():
        schema_path = SCHEMA_PATHS[key]
        schema = _schema_for(key, path)
        schema_path.parent.mkdir(parents=True, exist_ok=True)
        schema_path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_current_stage_schema() -> None:
    schema = json.loads(CURRENT_STAGE_SCHEMA_PATH.read_text(encoding="utf-8"))
    props = schema.setdefault("properties", {})
    props.setdefault("stage_id", {})["enum"] = sorted(set(props.get("stage_id", {}).get("enum", [])) | {STAGE_ID})
    props.setdefault("latest_completed_stage_id", {})["enum"] = sorted(
        set(props.get("latest_completed_stage_id", {}).get("enum", [])) | {STAGE_ID}
    )
    props.setdefault("previous_completed_stage_id", {})["enum"] = sorted(
        set(props.get("previous_completed_stage_id", {}).get("enum", [])) | {PREVIOUS_STAGE_ID}
    )
    props.setdefault("recommended_next_stage_id", {})["enum"] = sorted(
        set(props.get("recommended_next_stage_id", {}).get("enum", [])) | {NEXT_STAGE_ID}
    )
    props.setdefault("recommended_next_stage_title", {})["enum"] = sorted(
        set(props.get("recommended_next_stage_title", {}).get("enum", [])) | {NEXT_STAGE_TITLE_FINAL, NEXT_STAGE_TITLE_REPAIR}
    )
    props.setdefault("recommended_next_prompt_type", {})["enum"] = sorted(
        set(props.get("recommended_next_prompt_type", {}).get("enum", []))
        | {NEXT_PROMPT_TYPE_FINAL, NEXT_PROMPT_TYPE_REPAIR}
    )
    props.setdefault("stage6h_final_finite_stage7_manifest_created_now", {})["const"] = False
    props.setdefault("stage6h_archive_run_contract_finalized_now", {})["const"] = False
    props.setdefault("stage6h_creates_stage7_result_archive_now", {})["const"] = False
    props.setdefault("stage6h_runs_any_probe_now", {})["const"] = False
    props.setdefault("stage6i_final_manifest_required", {})["type"] = "boolean"
    props.setdefault("stage6i_addendum_required", {})["const"] = True
    CURRENT_STAGE_SCHEMA_PATH.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _schema_for(key: str, path: Path) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"type": "string"},
        "schema": {"type": "string"},
        "stage_id": {"const": STAGE_ID},
        "stage_title": {"const": STAGE_TITLE},
        "metadata_only": {"const": True},
        "solve_claim": {"const": False},
        "stage7_execution_allowed_next": {"const": False},
        "stage7_zip_archive_creation_allowed_next": {"const": False},
        "stage7_manifest_created_now": {"const": False},
        "stage7_archive_created_now": {"const": False},
        "probe_execution_performed_now": {"const": False},
        "route_stream_generated_now": {"const": False},
        "real_byte_stream_generated": {"const": False},
        "ocr_performed": {"const": False},
        "image_forensics_performed": {"const": False},
        "semantic_image_interpretation_performed": {"const": False},
    }
    required = ["record_type", "schema", "stage_id", "stage_title", "metadata_only", "solve_claim"]
    if key == "number_fact_overlays":
        properties.update(
            {
                "overlays": {"type": "array", "minItems": len(OVERLAY_IDS)},
                "overlay_count": {"const": len(OVERLAY_IDS)},
                "usable_for_decision_now": {"const": False},
            }
        )
        required.append("overlays")
    if key == "future_diagnostic_registry":
        properties["future_diagnostics"] = {"type": "array", "minItems": 33, "maxItems": 33}
        required.append("future_diagnostics")
    if key == "stage6i_manifest_input_addendum":
        properties["not_final_stage7_manifest"] = {"const": True}
        properties["stage7_execution_allowed_from_this_addendum"] = {"const": False}
        required.append("stage6i_addendum_inputs")
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
        "required": required,
        "properties": properties,
    }


def _base_flags() -> dict[str, Any]:
    return {
        "metadata_only": True,
        "reviewability_stage": True,
        "source_lock_addendum_stage": True,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
        "stage7_manifest_created_now": False,
        "stage7_archive_created_now": False,
        "probe_execution_performed_now": False,
        "diagnostic_probe_run_now": False,
        "diagnostic_execution_performed_now": False,
        "route_extraction_performed_now": False,
        "route_stream_generated_now": False,
        "real_byte_stream_generated": False,
        "variant_byte_streams_generated": False,
        "byte_stream_generation_authorized_now": False,
        "ocr_performed": False,
        "image_forensics_performed": False,
        "hidden_content_image_forensics_performed": False,
        "semantic_image_interpretation_performed": False,
        "cuda_execution_performed": False,
        "scoring_performed": False,
        "benchmark_performed": False,
        "target_priority_decision_created_now": False,
        "pivot_target_selected_now": False,
        "raw_source_files_committed": False,
        "raw_third_party_files_committed": False,
        "generated_outputs_committed": False,
        "stage6h_final_finite_stage7_manifest_created_now": False,
        "stage6h_archive_run_contract_finalized_now": False,
        "stage6h_creates_stage7_result_archive_now": False,
        "stage6h_generates_stage7_outputs_now": False,
        "stage6h_routes_to_stage7_now": False,
        "stage6h_runs_any_probe_now": False,
        "stage6h_generates_spiral_readouts_now": False,
        "stage6h_generates_triangle_readouts_now": False,
    }


def _base_record(record_type: str, schema_path: Path) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": schema_path.as_posix(),
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        **_base_flags(),
    }


def _base_project_record(record_type: str) -> dict[str, Any]:
    key = _key_for_record_type(record_type)
    return _base_record(record_type, SCHEMA_PATHS[key])


def _base_source_record(record_type: str) -> dict[str, Any]:
    key = _key_for_record_type(record_type)
    return _base_record(record_type, SCHEMA_PATHS[key])


def _base_token_record(record_type: str) -> dict[str, Any]:
    key = _key_for_record_type(record_type)
    return _base_record(record_type, SCHEMA_PATHS[key])


def _base_operator_record(record_type: str) -> dict[str, Any]:
    return _base_record(record_type, SCHEMA_PATHS["number_fact_overlays"]) | {"usable_for_decision_now": False}


def _base_historical_record(record_id: str) -> dict[str, Any]:
    return _base_record(record_id.replace("-", "_"), SCHEMA_PATHS[record_id]) | {
        "source_record_id": record_id,
        "usable_for_decision_now": False,
        "not_allowed_as": NOT_ALLOWED_AS,
        "verification_status": "operator_assistant_observed_context_pending_canonical_crosscheck",
        "review_only": True,
        "route_seed_now": False,
        "target_selection_now": False,
        "execution_seed_now": False,
    }


def _key_for_record_type(record_type: str) -> str:
    for key, path in DATA_PATHS.items():
        if path.stem.replace("-", "_") == record_type or key == record_type:
            return key
    # Historical record types use the hyphenated record id as key.
    hyphen = record_type.replace("_", "-")
    for key in DATA_PATHS:
        if key == hyphen:
            return key
    raise KeyError(record_type)


def _branch_order_policy() -> dict[str, Any]:
    return {
        "branch_dot_ordering_policies": {
            "y_x_black_1": {"bits": "01110", "value": 14},
            "y_x_white_1": {"bits": "10001", "value": 17},
            "geometric_black_1": {"bits": "01101", "value": 13},
            "geometric_white_1": {"bits": "10010", "value": 18},
            "centroid_angle_black_1": {"bits": "10101", "value": 21},
            "centroid_angle_white_1": {"bits": "01010", "value": 10},
            "left_to_right_black_1": {"bits": "10011", "value": 19},
            "left_to_right_white_1": {"bits": "01100", "value": 12},
            "branch_anchor_black_1": {"bits": "10110", "value": 22},
            "branch_anchor_white_1": {"bits": "01001", "value": 9},
        },
        "selected_order_policy_now": None,
        "selection_status": "no_order_selected",
        "branch_bridges_required": _branch_bridges(),
    }


def _branch_bridges() -> dict[str, Any]:
    return {
        "direct_concat_479": {
            "left_policy": "y_x_black_1",
            "left_bits": "01110",
            "left_value": 14,
            "right_bits": "11111",
            "right_value": 31,
            "concat_bits": "0111011111",
            "concat_value": 479,
            "crosslink": "stage6d_lag5_equal_count_479",
        },
        "weaker_primepi86_control": {
            "left_policy": "geometric_black_1",
            "left_bits": "01101",
            "left_value": 13,
            "right_bits": "11111",
            "right_value": 31,
            "concat_bits": "0110111111",
            "concat_value": 447,
            "prime_count_pi_447": 86,
            "crosslink": "stage6d_lag1_equal_count_86",
        },
    }


def _prime_count_policy() -> dict[str, Any]:
    return {
        "pi_447_means_number_of_primes_less_than_or_equal_to_447": True,
        "pi_447_expected_value": 86,
        "not_prime_86": True,
        "not_one_indexed_prime_lookup": True,
    }


def _right_angle_transform() -> dict[str, Any]:
    return {
        "position_formula": "n = T(r - 1) + c",
        "d_formula": "d = r - c + 1",
        "x": "c - 1",
        "y": "r - c",
        "bounds": ["x >= 0", "y >= 0", "x + y <= 16"],
    }


def _visual_7_8_ray() -> dict[str, Any]:
    return {
        "start_position": 41,
        "start_coordinate": "row_9_col_5",
        "delta_row": 7,
        "delta_col": 8,
        "endpoint_position": 133,
        "endpoint_coordinate": "row_16_col_13",
        "endpoint_diagonal": "d4",
    }


def _visual_8_7_complement() -> dict[str, Any]:
    return {
        "start_position": 41,
        "delta_row": 8,
        "delta_col": 7,
        "endpoint_position": 148,
        "endpoint_coordinate": "row_17_col_12",
    }


def _folded_7_8_8_7() -> dict[str, Any]:
    return {
        "center_position": 41,
        "center_xy": [4, 4],
        "seven_eight_raw": [11, 12],
        "seven_eight_reflected": [4, 5],
        "seven_eight_endpoint_position": 50,
        "eight_seven_raw": [12, 11],
        "eight_seven_reflected": [5, 4],
        "eight_seven_endpoint_position": 51,
    }


def _vertical_split() -> dict[str, Any]:
    return {
        "total_cells": 153,
        "left_nonspine_cells": 72,
        "spine_cells": 9,
        "right_nonspine_cells": 72,
        "spine_positions": [1, 5, 13, 25, 41, 61, 85, 113, 145],
        "shared_spine_left_surface_cells": 81,
        "shared_spine_right_surface_cells": 81,
        "surface_shape_candidate": "9x9",
    }


def _center_anchor_gp41_policy() -> dict[str, Any]:
    return {
        "center_position_41_source_locked": True,
        "center_word_index_41_source_locked": True,
        "center_rune_gp_value_41_source_locked_now": False,
        "operator_claim_pending_source_confirmation": True,
        "do_not_assert_as_source_locked_fact": True,
    }


def _visual_measurement_boundary() -> dict[str, Any]:
    return {
        "allowed_now": [
            "dimensions",
            "hashes",
            "centroids",
            "bounding_boxes",
            "dot_areas",
            "pairwise_distances",
            "pairwise_angles",
            "affine_reflection_scale_fit",
        ],
        "forbidden_now": [
            "OCR",
            "hidden_content_detection",
            "semantic_image_interpretation",
            "generated_masks_committed",
            "route_extraction_from_pixels",
            "pixel_stream_generation",
            "target_selection",
        ],
    }


def _discrepancy_policy() -> dict[str, Any]:
    return {
        "if_canonical_measurement_differs_from_chat_value": {
            "commit_computed_value": True,
            "create_discrepancy_record": True,
            "do_not_force_chat_value": True,
        }
    }


def _future_diagnostic_counts() -> dict[str, int]:
    return {
        "dot_diagnostic_count_expected": len(DOT_DIAGNOSTICS),
        "pdd153_diagnostic_count_expected": len(PDD153_DIAGNOSTICS),
        "route_cipher_diagnostic_count_expected": len(ROUTE_CIPHER_DIAGNOSTICS),
        "total_stage6h_future_diagnostic_count_expected": len(DOT_DIAGNOSTICS)
        + len(PDD153_DIAGNOSTICS)
        + len(ROUTE_CIPHER_DIAGNOSTICS),
    }


def _replace_section(path: Path, heading: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    if heading in text:
        before, rest = text.split(heading, 1)
        marker = "\n## "
        next_index = rest.find(marker)
        if next_index >= 0:
            text = before.rstrip() + "\n\n" + replacement.rstrip() + "\n\n" + rest[next_index + 1 :].lstrip()
        else:
            text = before.rstrip() + "\n\n" + replacement.rstrip() + "\n"
    else:
        text = replacement.rstrip() + "\n\n" + text.lstrip()
    _write_text(path, text)


def _remove_stale_operational_command_examples() -> None:
    path = Path("docs/onboarding/operational-file-map.md")
    text = path.read_text(encoding="utf-8")
    text = text.replace('--expected-latest-stage "Stage 5ED"', '--expected-latest-stage "Stage 6H"')
    text = text.replace('--expected-next-stage "Stage 5EE"', '--expected-next-stage "Stage 6I"')
    _write_text(path, text)
    _repair_stale_stage6h_prior_route_labels()


def _repair_stale_stage6h_prior_route_labels() -> None:
    paths = [
        Path("README.md"),
        Path("AGENTS.md"),
        Path("STATUS.md"),
        Path("ROADMAP.md"),
        Path("TESTING.md"),
        Path("docs/roadmap/staged-plan.md"),
        Path("docs/onboarding/start-here.md"),
        Path("docs/onboarding/source-of-truth-map.md"),
        Path("docs/onboarding/operational-file-map.md"),
        Path("docs/reference/token-block-cli.md"),
    ]
    replacements = {
        "Current next prompt: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.": (
            "Historical next prompt from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution."
        ),
        "Current next stage: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.": (
            "Historical Stage 6G route pointed to Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution."
        ),
        "- Current next stage: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.": (
            "- Historical Stage 6G route pointed to Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution."
        ),
        "Next routed stage: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.": (
            "Historical routed stage from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution."
        ),
        "- Next routed stage: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.": (
            "- Historical routed stage from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution."
        ),
        "The latest completed stage is Stage 6G. The next routed stage is Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.": (
            f"The latest completed stage is Stage 6H. The next routed stage is {NEXT_STAGE_TITLE_FINAL}."
        ),
        "Stage 6H is source-lock/readiness addendum work, not final Stage 7 manifest construction, because recent dot-angle/right-triangle material remains chat-only pending source-lock.": (
            "Stage 6I receives the explicit Stage 6H handoff addendum and remains without execution unless a later prompt explicitly opens execution gates."
        ),
        "Their old next-stage wording is historical only and is superseded by the current Stage 6G -> Stage 6H source-lock/readiness route above.": (
            "Their old next-stage wording is historical only and is superseded by the current Stage 6H -> Stage 6I route above."
        ),
        "## Stage 6G Current Boundary": "## Historical Stage 6G Boundary",
        "Latest completed stage: Stage 6G - Current-doc acceptance repair, Stage 6H source-lock handoff repair, hook confirmation, and acceptance-policy hardening, without execution.": (
            "Historical latest stage at Stage 6G closeout: Stage 6G - Current-doc acceptance repair, Stage 6H source-lock handoff repair, hook confirmation, and acceptance-policy hardening, without execution."
        ),
        "Current completed stage: Stage 6G - Current-doc acceptance repair, Stage 6H source-lock handoff repair, hook confirmation, and acceptance-policy hardening, without execution.": (
            "Historical completed stage at Stage 6G closeout: Stage 6G - Current-doc acceptance repair, Stage 6H source-lock handoff repair, hook confirmation, and acceptance-policy hardening, without execution."
        ),
        "- Stage 7 - Actual probes and diagnostics only after Stage 6G finite-manifest approval gates.": (
            "- Stage 7 - Actual probes and diagnostics only after a later final manifest/archive-run contract stage explicitly opens execution gates."
        ),
        "- Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.": (
            "- Stage 6I - Final finite Stage 7 probe manifest and archive-run contract, without execution."
        ),
    }
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            _write_text(path, text)


def _readme_current_section() -> str:
    return f"""## Current boundaries and deferred work

Current completed stage: {STAGE_TITLE}.

Current next prompt: {NEXT_STAGE_TITLE_FINAL}.

Stage 6H repairs Stage 6G current-state and doc-staleness misses, source-locks dot-angle/right-triangle/PDD153 review metadata, creates required Source Browser overlays, and hands explicit inputs to Stage 6I. Stage 6H created no final Stage 7 manifest, archive, probe execution, route stream, byte stream, target selection, image interpretation, or solve claim.

These are not permanent project exclusions. CUDA and broad campaigns are deferred, not permanently excluded.

### Permanent safety rules

No generated output is a solve by itself. No Liber Primus page is claimed solved unless a future reproducible manifest and matching output prove it. Any page still unsolved must not receive a solve claim.

### Current boundaries

- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Broad unsolved-page search campaigns: not started.
- Scoring campaigns: not started; Stage 3A/3B minimal triage scoring exists only for sorting and inspecting bounded 841-candidate CPU runs, Stage 3C calibration uses small local controls only, Stage 3D applies that scorer to a four-key explicit Vigenere preview only, Stage 3F applies it to the bounded 48-candidate LP evidence-key Vigenere pack only, Stage 3G applies it to a bounded 256-candidate p56-local prime-minus-one offset sweep only, Stage 3H applies it to a bounded 64-candidate reset/advance ablation with 100 negative controls only, Stage 3I applies it to a bounded 56-candidate historical motif Vigenere pack only, Stage 3J applies it to a bounded 192-candidate Mersenne/perfect-number stream probe only, and Stage 3S applies it to the bounded 72-candidate Onion 7 explicit seed pack only.
- Cookie/hash preimage work: Stage 3L tests two explicit SHA-256 packs only.
- Visual/image-derived observations: registry and deterministic feature summaries only.
- CUDA experiment campaigns: not started.

### Deferred future work

CUDA kernels after CPU references and parity tests exist. Broad search/scoring/CUDA campaigns: not started.

### Already implemented since Stage 0A

Stage 3X CLI modularisation completed without behavior change. Stage 5AE corrected formula-parity reporting repaired the bounded p56 hash lineage while preserving Stage 5AD as historical failed parity.
"""


def _agents_current_section() -> str:
    return f"""## Current stage

Current completed stage: {STAGE_TITLE}.

Next routed stage: {NEXT_STAGE_TITLE_FINAL}. Stage 6I receives explicit Stage 6C/6D/6E/6F/6G/6H handoff inputs and remains without execution until a later prompt explicitly authorizes any Stage 7 work.

No Deep Research activation-acceptance record exists, the combined gate is not satisfied, no valid activation decision exists, and no active planning input authorization or selection exists. String 4 remains inactive; no target-priority selection, source-lock browser puzzle execution, direct source-record number-fact backfill, historical source-lock rewrite, triangle/Page32 route extraction, music route extraction, audio/stego/OCR/image forensics/AI interpretation, active ingestion, byte-stream generation, machine-code/VM execution, manifest supersession, execution, target-class validation, Tor access, DWH/hash/preimage search, decode, scoring, CUDA, benchmark, website expansion, method-status upgrade, canonical corpus activation, page-boundary finalisation, or solve claim is authorized.

Future Codex work must apply `docs/onboarding/codex-acceptance-criteria.md`.

- Canonical corpus: inactive.
- Page boundaries: reviewable.
- CUDA: deferred.

Discord raw logs are not committed. Raw page images, raw historical stego artefacts, generated outputs, SQLite databases, and local reports remain ignored and uncommitted.
"""


def _status_current_section() -> str:
    return f"""## Current Stage

- Latest completed stage: {STAGE_TITLE}.
- Current next stage: {NEXT_STAGE_TITLE_FINAL}.
- Next recommended prompt: {NEXT_STAGE_TITLE_FINAL}.
- Stage 6H current-state repair blockers: 0.
- Stage 6H doc-staleness repair blockers: 0.
- Stage 6H source-lock record blockers: 0.
- Stage 6H Source Browser overlay blockers: 0.
- Stage 6H future diagnostic blockers: 0.
- Stage 6H canonical-source crosscheck blockers: 0.
- Stage 6I final-manifest readiness blockers: 0.
- No probe, route, byte-stream, OCR/image/stego, PGP/OutGuess/F5/StegDetect, CUDA, scoring, target-selection, canonical-corpus, page-boundary, Stage 7 manifest/archive, or solve work is authorized.
"""


def _roadmap_current_section() -> str:
    return f"""## Current Direction

Current completed stage: {STAGE_TITLE}.

Next routed stage: {NEXT_STAGE_TITLE_FINAL}.

Stage 6H is a current-state repair and source-lock addendum stage. It hands Stage 6I explicit input paths for final manifest planning while keeping Stage 7 execution, result archives, route streams, byte streams, Stage 8 triangle readiness, and Stage 9 experiments blocked.
"""


def _testing_section() -> str:
    return """## Stage 6H Validation Targets

Stage 6H validation must run after docs and current-stage state are updated. Required checks include `token-block validate-stage6h`, focused Stage 6H validators, stale-current strict scanning, Source Browser index/path validation, focused pytest slices, ruff, and the Stage 6H stage-validation profiles. Tests inspect current-state root/nested fields, required overlay IDs, exact diagnostic counts, and Stage 6I addendum paths directly.
"""


def _chatgpt_current_section() -> str:
    return """## Current Project State

Stage 6H repaired Stage 6G current-state defects and stale doc-staleness source-truth fields. The current state is Stage 6H complete with Stage 6I next, using `data/token-block/stage6h-stage6i-manifest-input-addendum.yaml` as the explicit path-based handoff input.

Stage 6H source-locked review-only dot-angle/right-triangle/PDD153 metadata: the three-dot 7:8 angle41 bridge, branch-dot binary 14/17/31/479 bridge, PDD153 right-angle transform, visual 7:8 ray to 133/d4, folded 7:8/8:7 hits 50/51, vertical split 72|9|72, shared spine 81/81 surfaces, row10 seam 49/52 and 50/51, word52 WAY and word55 READ prefix under PDD-minus-reversed-word, I AM/CIRCUMFERENCE mod153 edge bridge, and OUROBOROS variants 7/11/14 offsets.

The center bridge is source-locked as center position/index 41 only. Center-rune GP value 41 remains an operator claim pending source confirmation unless a committed record later proves it.

All Stage 6H future diagnostics remain disabled. Stage 6H created no Stage 7 manifest, result archive, probe execution, route stream, byte stream, OCR/image/stego/CUDA/scoring/benchmark output, target selection, or solve claim.
"""


def _staged_plan_current_section() -> str:
    return f"""## Current Project State

- Latest completed stage: {STAGE_TITLE}.
- Next routed stage: {NEXT_STAGE_TITLE_FINAL}.
- Stage 6H repairs current-state integrity and source-locks dot-angle/right-triangle/PDD153 review metadata.
- Stage 6I receives explicit handoff input paths and remains without execution.
- Stage 7 manifest/archive/probe execution: not created and not allowed now.
- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Solve claims: none.
- Update policy: `data/project-state/current-stage-state.yaml` is authoritative; human-readable docs are mirrors and must be refreshed after current-stage changes.
- Observation promotion remains gated by a promotion ledger; entries require `ready_for_manifest` status and `control-only` rows stay non-executable.
- Discord raw logs remain local, private, ignored, and uncommitted.
"""


def _staged_plan_current_stage_section() -> str:
    return f"""## Current Stage

Stage 6H - Current-state integrity repair and dot-angle / right-triangle number-triangle source-lock addendum, without execution is the latest completed stage. It repairs Stage 6G current-state/doc-staleness misses, adds review-only dot-angle/right-triangle/PDD153 source-lock metadata, creates required overlays, and keeps all execution and Stage 7 artifact gates closed.

Next routed stage: {NEXT_STAGE_TITLE_FINAL}. Stage 6I receives the explicit path-based handoff addendum and remains without execution unless a later prompt explicitly opens execution gates.
"""


def _start_here_current_section() -> str:
    return f"""## Current State

The latest completed stage is Stage 6H. The next routed stage is {NEXT_STAGE_TITLE_FINAL}.

Stage 6H repaired Stage 6G current-state/doc-staleness misses and source-locked dot-angle/right-triangle/PDD153 review metadata. The Stage 6I addendum is `data/token-block/stage6h-stage6i-manifest-input-addendum.yaml`; it is a handoff input, not a final Stage 7 manifest.
"""


def _source_truth_current_section() -> str:
    return f"""## Current Operational Truth

- The latest completed stage is `stage-6h`.
- The next stage is `stage-6i`: {NEXT_STAGE_TITLE_FINAL}.
- The authoritative current-state path is `data/project-state/current-stage-state.yaml`.
- The acceptance policy path is `docs/onboarding/codex-acceptance-criteria.md`.
- The Stage 6I handoff addendum is `data/token-block/stage6h-stage6i-manifest-input-addendum.yaml`.
- The post-push local completion handoff path is `codex-output/stage6h-codex-completion.md`.
- No Stage 5ED/5EE or Stage 6F/6G current claim is authoritative here.
"""


def _operational_file_map_section() -> str:
    return """## Stage 6H Operational Files

- `data/project-state/stage6h-summary.yaml`: Stage 6H repair/source-lock summary.
- `data/token-block/stage6h-stage6i-manifest-input-addendum.yaml`: explicit Stage 6I handoff input addendum.
- `data/operator-console/source-browser/number-fact-overlays/stage6h-dot-angle-right-triangle-source-lock-overlays.yaml`: required review-only Source Browser overlays.
- `data/token-block/stage6h-future-diagnostic-registry.yaml`: disabled future diagnostics.
- `codex-output/stage6h-codex-completion.md`: ignored local completion handoff path after Stage 6H.
"""


def _cli_docs_section() -> str:
    return """## Stage 6H Token-Block CLI

- `python -m libreprimus.cli token-block build-stage6h`
- `python -m libreprimus.cli token-block validate-stage6h`
- `python -m libreprimus.cli token-block stage6h-summary`
- Focused validators include `validate-stage6h-current-state-integrity`, `validate-stage6h-doc-staleness-source-truth-repair`, `validate-stage6h-operational-file-map-repair`, `validate-stage6h-source-harvester-records`, `validate-stage6h-source-lock-records`, `validate-stage6h-exact-constants`, `validate-stage6h-number-fact-overlays`, `validate-stage6h-future-diagnostics`, `validate-stage6h-stage6i-addendum`, `validate-stage6h-source-browser-loadability`, `validate-stage6h-gate-closure`, and `validate-stage6h-handoff`.
"""


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _ensure_no_protected_output_overlap() -> None:
    protected = {Path(path) for path in stage6.PROTECTED_LOCAL_PATHS}
    outputs = set(DATA_PATHS.values()) | {CURRENT_STAGE_STATE_PATH, DOC_STALENESS_SOURCE_OF_TRUTH_PATH}
    overlap = protected & outputs
    if overlap:
        raise RuntimeError(f"Stage 6H output overlaps protected local paths: {sorted(map(str, overlap))}")


def _result(errors: list[str], **counts: Any) -> stage6.ValidationResult:
    return stage6.ValidationResult(errors=errors, counts=counts)
