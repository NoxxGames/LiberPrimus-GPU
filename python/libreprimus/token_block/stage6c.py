"""Stage 6C OUROBOROS / I31 circumference source-lock addendum."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import validate_source_index
from libreprimus.token_block import stage6, stage6b
from libreprimus.token_block.models import read_yaml, write_yaml

STAGE_ID = "stage-6c"
STAGE_TOKEN = "stage6c"
STAGE_TITLE = (
    "Stage 6C - OUROBOROS / I=31 circumference / Page32 spiral geometry source-lock addendum, "
    "without execution"
)
PROMPT_TYPE = "codex_plan_mode_source_lock_addendum"
PREVIOUS_STAGE_ID = "stage-6b"
PREVIOUS_STAGE_TITLE = stage6b.STAGE_TITLE
NEXT_STAGE_ID = "stage-6d"
NEXT_STAGE_TITLE = "Stage 6D - Final finite Stage 7 probe manifest and archive-run contract, without execution"
NEXT_PROMPT_TYPE = "codex_plan_mode_probe_manifest_finalization"
STARTING_COMMIT = "91694129da77fa14389318e2733512c5a844aa42"

PROJECT_STATE_DIR = Path("data/project-state")
HISTORICAL_ROUTE_DIR = Path("data/historical-route")
TOKEN_BLOCK_DIR = Path("data/token-block")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
OPERATOR_OVERLAY_DIR = Path("data/operator-console/source-browser/number-fact-overlays")
CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
CURRENT_STAGE_SCHEMA_PATH = Path("schemas/project-state/current-stage-state-v0.schema.json")
DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH = Path(
    "schemas/project-state/doc-staleness-source-of-truth-record-v0.schema.json"
)
CODEX_COMPLETION_PATH = Path("codex-output/stage6c-codex-completion.md")

GP_PROFILE_PATH = Path("data/profiles/gematria/gematria-primus-v0.json")
EXACT_QUOTE = "THE I IS THE VOICE OF THE CIRCUMFERENCE"

SOURCE_CROSSLINKS = {
    "gp_profile": [GP_PROFILE_PATH.as_posix()],
    "solved_i_voice_circumference_quote": [
        "data/historical-route/stage5dn-solved-i-voice-of-circumference-precedent-v0.yaml",
        "data/historical-route/stage5dn-circumference-single-i-spiral-anchor-crosslink-v0.yaml",
    ],
    "ouroboros_gp167_and_transform_context": [
        "data/historical-route/stage5ds-ouroboros-gp-167-music-cycle-candidate-v0.yaml",
        "data/historical-route/stage5ds-ouroboros-see-also-transform-context-v0.yaml",
        "data/historical-route/stage5ds-ouroboros-see-also-gp-arithmetic-scan-v0.yaml",
    ],
    "pdd153_and_56311": [
        "data/historical-route/stage5ds-pdd153-ouroboros-167-mod153-offset14-candidate-v0.yaml",
        "data/historical-route/stage5ds-pdd153-56311-ouroboric-cycle-candidate-v0.yaml",
        "data/historical-route/stage5ei-pdd153-geometry-candidates.yaml",
    ],
    "page32_3222": [
        "data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml",
    ],
}
ALL_SOURCE_PATHS = sorted({path for paths in SOURCE_CROSSLINKS.values() for path in paths})

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage6c-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage6c-next-stage-decision.yaml",
    "stage6b_preservation": PROJECT_STATE_DIR / "stage6c-stage6b-preservation.yaml",
    "source_lock_addendum_summary": PROJECT_STATE_DIR / "stage6c-source-lock-addendum-summary.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage6c-reviewability-gap-register.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage6c-reviewable-validation-evidence.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR / "stage6c-source-browser-loadability-summary.yaml",
    "current_stage_transition": PROJECT_STATE_DIR / "stage6c-current-stage-transition.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage6c-chatgpt-context-update-summary.yaml",
}

HISTORICAL_ROUTE_PATHS: dict[str, Path] = {
    "i31_vowel_voice_circumference": HISTORICAL_ROUTE_DIR
    / "stage6c-ouroboros-i31-vowel-voice-circumference-candidate-v0.yaml",
    "t16_consonant_shell_pdd153": HISTORICAL_ROUTE_DIR
    / "stage6c-ouroboros-t16-consonant-shell-pdd153-bridge-v0.yaml",
    "o_ring_3222_page32": HISTORICAL_ROUTE_DIR
    / "stage6c-ouroboros-o-ring-3222-page32-spiral-bridge-v0.yaml",
    "pdd153_offset14_56311": HISTORICAL_ROUTE_DIR
    / "stage6c-ouroboros-pdd153-offset14-56311-phase-bridge-v0.yaml",
    "palindromic_core": HISTORICAL_ROUTE_DIR
    / "stage6c-ouroboros-palindromic-core-97-and-oro25-candidate-v0.yaml",
    "index_checksum": HISTORICAL_ROUTE_DIR / "stage6c-ouroboros-index-checksum-candidates-v0.yaml",
    "i31_geometry": HISTORICAL_ROUTE_DIR
    / "stage6c-i31-circumference-radius5-diameter10-geometry-candidate-v0.yaml",
    "variant_spelling_controls": HISTORICAL_ROUTE_DIR
    / "stage6c-ouroboros-variant-spelling-control-candidates-v0.yaml",
    "stage8_stage9_watchlist": HISTORICAL_ROUTE_DIR
    / "stage6c-ouroboros-stage8-stage9-output-watchlist-v0.yaml",
}

TOKEN_BLOCK_PATHS: dict[str, Path] = {
    "future_probe_registry": TOKEN_BLOCK_DIR / "stage6c-ouroboros-future-probe-registry.yaml",
    "route_fingerprint_watchlist": TOKEN_BLOCK_DIR / "stage6c-ouroboros-route-fingerprint-watchlist.yaml",
    "null_negative_control_policy": TOKEN_BLOCK_DIR / "stage6c-ouroboros-null-negative-control-policy.yaml",
    "keeper_taxonomy": TOKEN_BLOCK_DIR / "stage6c-ouroboros-keeper-taxonomy.yaml",
    "stage6d_manifest_input_addendum": TOKEN_BLOCK_DIR / "stage6c-stage6d-manifest-input-addendum.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage6c-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage6c-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage6c-no-execution-transition-gate.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "source_crosslink_register": SOURCE_HARVESTER_DIR / "stage6c-ouroboros-source-crosslink-register.yaml",
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage6c-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage6c-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage6c-raw-source-noncommit-proof.yaml",
}

OPERATOR_CONSOLE_PATHS: dict[str, Path] = {
    "number_fact_overlays": OPERATOR_OVERLAY_DIR / "stage6c-ouroboros-i31-circumference-overlays.yaml",
}

DATA_PATHS = {
    **PROJECT_STATE_PATHS,
    **HISTORICAL_ROUTE_PATHS,
    **TOKEN_BLOCK_PATHS,
    **SOURCE_HARVESTER_PATHS,
    **OPERATOR_CONSOLE_PATHS,
}


def _schema_path(category: str, key: str) -> Path:
    return Path(f"schemas/{category}/stage6c-{key.replace('_', '-')}-v0.schema.json")


SCHEMA_PATHS: dict[str, Path] = {key: _schema_path("project-state", key) for key in PROJECT_STATE_PATHS}
SCHEMA_PATHS.update({key: _schema_path("historical-route", key) for key in HISTORICAL_ROUTE_PATHS})
SCHEMA_PATHS.update({key: _schema_path("token-block", key) for key in TOKEN_BLOCK_PATHS})
SCHEMA_PATHS.update({key: _schema_path("source-harvester", key) for key in SOURCE_HARVESTER_PATHS})
SCHEMA_PATHS.update({key: _schema_path("operator-console", key) for key in OPERATOR_CONSOLE_PATHS})

CONTROL_BUNDLE_ID = "ouroboros_i31_circumference_controls_v0"
CONTROL_BUNDLE = [
    "spelling_variant_controls",
    "same_length_gp_phrase_controls",
    "logged_loop_self_reference_term_controls",
    "shuffled_gp_label_order_controls",
    "random_same_multiset_controls",
    "page32_grid_hit_multiple_comparison_controls",
    "alternate_o_gap_conventions",
    "pdd153_offset_controls",
    "circumference_neighbor_controls_29_30_32_41",
    "no_plaintext_required_output_policy",
]

FUTURE_PROBE_IDS = [
    "ouroboros_vowel_voice_i31_probe_v0",
    "ouroboros_consonant_t16_triangle_shell_probe_v0",
    "ouroboros_variant_voice_layer_control_probe_v0",
    "ouroboros_o_ring_3222_page32_control_probe_v0",
    "i31_circumference_radius5_diameter10_pdd_center_probe_v0",
    "i31_56311_phase_ring_probe_v0",
    "pdd153_mod31_gp29_decomposition_probe_v0",
    "page32_spiral_mod31_residue_probe_v0",
    "multi_spiral_same_center_phase_offset_probe_v0",
    "ouroboros_output_watchlist_for_stage8_stage9_v0",
]

SOURCE_LOCKED_REVIEW_FACTS = [
    "ouroboros_gp167_total",
    "ouroboros_vowel_voice_i31",
    "ouroboros_consonant_t16_shell",
    "ouroboros_pdd153_delta14",
    "ouroboros_o_ring_3222",
    "i31_circumference_radius5_diameter10_candidate",
    "ouroboros_inter_o_segments_offset14",
    "ouroboros_palindromic_core_robor97_oro25",
    "ouroboros_index_checksum_53_62",
    "finite_variant_controls_ouroboros_uroboros_oroboros",
]

OVERLAY_IDS = [
    "stage6c_ouroboros_gp167_total_overlay",
    "stage6c_ouroboros_vowel_voice_i31_overlay",
    "stage6c_ouroboros_consonant_shell_t16_overlay",
    "stage6c_ouroboros_t16_i_pdd153_delta14_overlay",
    "stage6c_ouroboros_o_ring_3222_page32_overlay",
    "stage6c_i31_circumference_radius5_diameter10_overlay",
    "stage6c_i31_56311_phase_ring_overlay",
    "stage6c_ouroboros_variant_control_overlay",
    "stage6c_pdd153_mod31_gp29_overlay",
    "stage6c_ouroboros_palindromic_core_overlay",
    "stage6c_ouroboros_inter_o_segments_offset14_overlay",
    "stage6c_ouroboros_index_checksum_overlay",
]

NOT_ALLOWED_AS = ["proof", "route_seed", "target_selection", "activation_decision", "execution_seed", "solve_claim"]

STAGE6C_FALSE_GUARDRAILS = {
    "stage6c_final_finite_stage7_manifest_created_now": False,
    "stage6c_archive_run_contract_finalized_now": False,
    "stage6c_creates_stage7_result_archive_now": False,
    "stage6c_generates_stage7_outputs_now": False,
    "stage6c_routes_to_stage7_now": False,
    "stage6c_runs_any_probe_now": False,
    "stage6c_generates_spiral_readouts_now": False,
    "stage6c_generates_triangle_readouts_now": False,
    "stage6c_confirms_3222_red_highlight_now": False,
    "stage6c_uses_image_interpretation_now": False,
    "stage7_execution_allowed_next": False,
    "stage7_zip_archive_creation_allowed_next": False,
    "stage8_triangle_readiness_started_now": False,
    "stage9_experiments_started_now": False,
    "triangular_transposition_readouts_generated_now": False,
    "spiral_route_readouts_generated_now": False,
}

FORBIDDEN_FALSE = stage6.FALSE_GUARDRAILS | stage6.STAGE6_FALSE_GUARDRAILS | STAGE6C_FALSE_GUARDRAILS


class ValidationResult(stage6.ValidationResult):
    pass


def build_stage6c() -> dict[str, Any]:
    _ensure_no_protected_output_overlap()
    _write_schemas()
    _update_current_stage_schema()
    arithmetic = _arithmetic()
    counts = _source_browser_counts()
    records = _records(arithmetic, counts)
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)
    records["summary"].update(counts)
    records["source_browser_loadability_summary"].update(counts)
    write_yaml(PROJECT_STATE_PATHS["summary"], records["summary"])
    write_yaml(PROJECT_STATE_PATHS["source_browser_loadability_summary"], records["source_browser_loadability_summary"])
    _write_current_stage_state(records["summary"])
    _write_docs(records["summary"])
    _write_completion_summary_stub(records["summary"])
    return records


def validate_stage6c() -> ValidationResult:
    validators = [
        validate_stage6c_stage6b_preservation,
        validate_stage6c_source_lock_records,
        validate_stage6c_ouroboros_arithmetic,
        validate_stage6c_page32_3222_policy,
        validate_stage6c_number_fact_overlays,
        validate_stage6c_future_probe_registry,
        validate_stage6c_stage8_watchlist,
        validate_stage6c_source_browser_loadability,
        validate_stage6c_current_stage_transition,
        validate_stage6c_gate_closure,
        validate_stage6c_handoff,
        validate_stage6c_files_and_schemas,
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for validator in validators:
        result = validator()
        errors.extend(result.errors)
        counts.update(result.counts)
    counts["validation_error_count"] = len(errors)
    return ValidationResult(errors, counts)


def validate_stage6c_files_and_schemas() -> ValidationResult:
    errors: list[str] = []
    for key, data_path in DATA_PATHS.items():
        schema_path = SCHEMA_PATHS[key]
        if not data_path.exists():
            errors.append(f"missing data file: {data_path}")
            continue
        if not schema_path.exists():
            errors.append(f"missing schema file: {schema_path}")
            continue
        schema = read_yaml(schema_path)
        payload = read_yaml(data_path)
        Draft202012Validator.check_schema(schema)
        schema_errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda err: err.path)
        errors.extend(f"{data_path}: {error.message}" for error in schema_errors)
    return _result(errors, stage6c_schema_count=len(SCHEMA_PATHS), stage6c_data_record_count=len(DATA_PATHS))


def validate_stage6c_stage6b_preservation() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["stage6b_preservation"])
    errors = []
    for key in [
        "stage6b_preserved",
        "stage6b_probe_mapping_repairs_preserved",
        "stage6b_hook_report_only_default_preserved",
        "stage6b_default_hook_exit_zero_preserved",
        "stage6b_strict_hook_mode_preserved",
    ]:
        if record.get(key) is not True:
            errors.append(f"missing {key}=true")
    return _result(errors, stage6b_preserved=record.get("stage6b_preserved"))


def validate_stage6c_source_lock_records() -> ValidationResult:
    errors = []
    for key, path in HISTORICAL_ROUTE_PATHS.items():
        record = read_yaml(path)
        if record.get("stage_id") != STAGE_ID:
            errors.append(f"{path}: wrong stage_id")
        source_paths = record.get("source_paths", [])
        if not source_paths:
            errors.append(f"{path}: source_paths missing")
        if "exact_quote" in record and record["exact_quote"] != EXACT_QUOTE:
            errors.append(f"{path}: exact quote mismatch")
        for source_path in source_paths:
            if source_path not in ALL_SOURCE_PATHS:
                errors.append(f"{path}: unexpected source path {source_path}")
    return _result(errors, source_lock_record_count=len(HISTORICAL_ROUTE_PATHS))


def validate_stage6c_ouroboros_arithmetic() -> ValidationResult:
    record = read_yaml(HISTORICAL_ROUTE_PATHS["i31_vowel_voice_circumference"])
    shell = read_yaml(HISTORICAL_ROUTE_PATHS["t16_consonant_shell_pdd153"])
    page32 = read_yaml(HISTORICAL_ROUTE_PATHS["o_ring_3222_page32"])
    internal = read_yaml(HISTORICAL_ROUTE_PATHS["palindromic_core"])
    checksum = read_yaml(HISTORICAL_ROUTE_PATHS["index_checksum"])
    geometry = read_yaml(HISTORICAL_ROUTE_PATHS["i31_geometry"])
    variants = read_yaml(HISTORICAL_ROUTE_PATHS["variant_spelling_controls"])
    errors = []
    expected_pairs = [
        (record.get("ouroboros_total"), 167, "ouroboros_total"),
        (record.get("vowel_sum"), 31, "vowel_sum"),
        (shell.get("consonant_sum"), 136, "consonant_sum"),
        (shell.get("t16"), 136, "t16"),
        (shell.get("pdd153"), 153, "pdd153"),
        (shell.get("delta_ouroboros_minus_pdd153"), 14, "delta"),
        (page32.get("o_cyclic_distances"), [3, 2, 2, 2], "o_cyclic_distances"),
        (page32.get("o_cyclic_distance_compact"), "3222", "o_cyclic_distance_compact"),
        (internal.get("inter_o_segment_gp_values"), [14, 61, 11, 53], "inter_o_segment_gp_values"),
        (internal.get("robor_gp_sum"), 97, "robor_gp_sum"),
        (internal.get("oro_gp_sum"), 25, "oro_gp_sum"),
        (checksum.get("zero_based_index_sum"), 53, "zero_based_index_sum"),
        (checksum.get("one_based_index_sum"), 62, "one_based_index_sum"),
    ]
    for observed, expected, label in expected_pairs:
        if observed != expected:
            errors.append(f"{label} expected {expected!r}, got {observed!r}")
    if abs(float(geometry.get("radius_if_circumference_31", 0)) - 4.93) >= 0.01:
        errors.append("radius tolerance failed")
    if abs(float(geometry.get("diameter_if_circumference_31", 0)) - 9.87) >= 0.01:
        errors.append("diameter tolerance failed")
    variant_by_name = {item["spelling"]: item for item in variants.get("variant_controls", [])}
    for spelling, total, vowel, excess in [("OUROBOROS", 167, 31, 14), ("UROBOROS", 160, 24, 7), ("OROBOROS", 164, 28, 11)]:
        item = variant_by_name.get(spelling, {})
        if item.get("gp_total") != total or item.get("vowel_sum") != vowel or item.get("excess_over_pdd153") != excess:
            errors.append(f"{spelling} variant control mismatch")
    return _result(errors, future_probe_count=len(FUTURE_PROBE_IDS))


def validate_stage6c_page32_3222_policy() -> ValidationResult:
    record = read_yaml(HISTORICAL_ROUTE_PATHS["o_ring_3222_page32"])
    status = record.get("page32_3222_status", {})
    errors = []
    if status.get("source_backed_as_grid_value") is not True:
        errors.append("3222 must be source-backed as grid value")
    if status.get("source_backed_as_spiral_sequence_value") is not True:
        errors.append("3222 must be source-backed as spiral value")
    if status.get("source_backed_as_red_or_highlighted") is not False:
        errors.append("3222 red/highlighted status must remain false without committed proof")
    if status.get("image_inspection_performed_now") is not False:
        errors.append("image inspection must be false")
    return _result(errors, page32_3222_red_highlighted_status="not_source_confirmed")


def validate_stage6c_number_fact_overlays() -> ValidationResult:
    record = read_yaml(OPERATOR_CONSOLE_PATHS["number_fact_overlays"])
    overlays = record.get("overlays", [])
    by_id = {item["overlay_id"]: item for item in overlays}
    errors = []
    required_fields = [
        "overlay_id",
        "source_record_path",
        "source_fact_id",
        "fact_class",
        "display_label",
        "short_label",
        "value",
        "values",
        "value_type",
        "operation_type",
        "expression",
        "relation",
        "why_stored",
        "verification_status",
        "display_priority",
        "source_paths",
        "crosslinks",
        "risk_notes",
        "not_allowed_as",
        "usable_for_decision_now",
    ]
    for overlay_id in OVERLAY_IDS:
        item = by_id.get(overlay_id)
        if item is None:
            errors.append(f"missing overlay {overlay_id}")
            continue
        for field in required_fields:
            if field not in item:
                errors.append(f"{overlay_id} missing {field}")
        if item.get("usable_for_decision_now") is not False:
            errors.append(f"{overlay_id} usable_for_decision_now must be false")
        if item.get("not_allowed_as") != NOT_ALLOWED_AS:
            errors.append(f"{overlay_id} not_allowed_as mismatch")
    return _result(errors, overlay_count=len(overlays))


def validate_stage6c_future_probe_registry() -> ValidationResult:
    record = read_yaml(TOKEN_BLOCK_PATHS["future_probe_registry"])
    addendum = read_yaml(TOKEN_BLOCK_PATHS["stage6d_manifest_input_addendum"])
    errors = []
    if record.get("future_probe_ids") != FUTURE_PROBE_IDS:
        errors.append("future probe ids mismatch")
    if addendum.get("source_locked_review_facts") != SOURCE_LOCKED_REVIEW_FACTS:
        errors.append("Stage 6D source-locked fact list mismatch")
    if addendum.get("future_probe_ids") != FUTURE_PROBE_IDS:
        errors.append("Stage 6D future probe list mismatch")
    if addendum.get("not_final_stage7_manifest") is not True:
        errors.append("Stage 6D addendum must not be final manifest")
    for item in record.get("future_probes", []):
        if item.get("stage6c_run_now") is not False:
            errors.append(f"{item.get('probe_id')} run flag must be false")
        if item.get("execution_enabled_now") is not False:
            errors.append(f"{item.get('probe_id')} execution flag must be false")
        if item.get("stage7_execution_enabled_now") is not False:
            errors.append(f"{item.get('probe_id')} stage7 execution flag must be false")
        if item.get("control_bundle_id") != CONTROL_BUNDLE_ID:
            errors.append(f"{item.get('probe_id')} control bundle mismatch")
    return _result(errors, future_probe_count=len(record.get("future_probes", [])))


def validate_stage6c_stage8_watchlist() -> ValidationResult:
    record = read_yaml(HISTORICAL_ROUTE_PATHS["stage8_stage9_watchlist"])
    errors = []
    required = {
        "I31_voice_layer",
        "OUROBOROS_167",
        "T16_plus_I",
        "delta14",
        "3222",
        "phase_offsets_0_5_11_14_25",
        "circumference31_radius5_diameter10",
        "second_stage_surface_not_plaintext_policy",
    }
    if set(record.get("stage8_stage9_watchlist_terms", [])) != required:
        errors.append("Stage 8/9 watchlist terms mismatch")
    for key in [
        "stage8_triangle_readiness_started_now",
        "stage9_experiments_started_now",
        "triangular_transposition_readouts_generated_now",
        "spiral_route_readouts_generated_now",
    ]:
        if record.get(key) is not False:
            errors.append(f"{key} must be false")
    return _result(errors, watchlist_term_count=len(record.get("stage8_stage9_watchlist_terms", [])))


def validate_stage6c_source_browser_loadability() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    errors = []
    if int(record.get("source_browser_validation_error_count", -1)) != 0:
        errors.append("Source Browser validation errors must be zero")
    return _result(errors, source_browser_entries_loaded=record.get("source_browser_entries_loaded"))


def validate_stage6c_current_stage_transition() -> ValidationResult:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    errors = []
    expected = {
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }
    for key, value in expected.items():
        if current.get(key) != value:
            errors.append(f"current-stage {key} expected {value!r}")
    return _result(errors, recommended_next_stage_id=current.get("recommended_next_stage_id"))


def validate_stage6c_gate_closure() -> ValidationResult:
    errors: list[str] = []
    for path in DATA_PATHS.values():
        payload = read_yaml(path)
        for guard, expected in FORBIDDEN_FALSE.items():
            if guard in payload and payload[guard] is not expected:
                errors.append(f"{path}: {guard} must be {expected}")
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    for guard, expected in FORBIDDEN_FALSE.items():
        if summary.get(guard) is not expected:
            errors.append(f"summary: {guard} must be {expected}")
    return _result(errors, guardrail_record_count=len(DATA_PATHS))


def validate_stage6c_handoff() -> ValidationResult:
    record = read_yaml(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if record.get("completion_summary_path") != CODEX_COMPLETION_PATH.as_posix():
        errors.append("completion summary path mismatch")
    if Path("codex_output").exists():
        errors.append("deprecated codex_output path exists")
    return _result(errors, handoff_path=record.get("completion_summary_path"))


def stage6c_summary_text() -> str:
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    return "\n".join(
        [
            "LiberPrimus Stage 6C summary:",
            f"status={summary.get('status')}",
            f"stage_id={summary.get('stage_id')}",
            f"previous_stage_id={summary.get('previous_stage_id')}",
            f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
            f"ouroboros_total={summary.get('ouroboros_total')}",
            f"vowel_sum={summary.get('vowel_sum')}",
            f"o_cyclic_distance_compact={summary.get('o_cyclic_distance_compact')}",
            f"future_probe_count={summary.get('future_probe_count')}",
            f"overlay_count={summary.get('overlay_count')}",
            f"page32_3222_red_highlighted_status={summary.get('page32_3222_red_highlighted_status')}",
        ]
    )


def _records(arithmetic: dict[str, Any], source_browser: dict[str, int]) -> dict[str, dict[str, Any]]:
    historical = _historical_records(arithmetic)
    future = _future_probe_registry()
    stage6d_addendum = _stage6d_manifest_input_addendum()
    overlays = _overlay_collection(arithmetic)
    return {
        "summary": _summary_record(arithmetic, source_browser, overlays, future),
        "next_stage_decision": _next_stage_decision_record(),
        "stage6b_preservation": _stage6b_preservation_record(),
        "source_lock_addendum_summary": _source_lock_addendum_summary(arithmetic),
        "reviewability_gap_register": _reviewability_gap_record(arithmetic),
        "reviewable_validation_evidence": _validation_evidence_record(arithmetic),
        "source_browser_loadability_summary": _base_project_record("stage6c_source_browser_loadability_summary")
        | source_browser,
        "current_stage_transition": _current_stage_transition_record(),
        "chatgpt_context_update_summary": _base_project_record("stage6c_chatgpt_context_update_summary")
        | {"chatgpt_context_updated_to_stage6c": True, "stage6d_routed_next": True},
        **historical,
        "future_probe_registry": future,
        "route_fingerprint_watchlist": _route_fingerprint_watchlist(),
        "null_negative_control_policy": _null_negative_control_policy(),
        "keeper_taxonomy": _keeper_taxonomy(),
        "stage6d_manifest_input_addendum": stage6d_addendum,
        "no_active_ingestion_proof": _gate_record("stage6c_no_active_ingestion_proof"),
        "no_byte_stream_transition_gate": _gate_record("stage6c_no_byte_stream_transition_gate"),
        "no_execution_transition_gate": _gate_record("stage6c_no_execution_transition_gate"),
        "source_crosslink_register": _source_crosslink_register(),
        "codex_handoff_policy": _source_record("stage6c_codex_handoff_policy")
        | {"completion_summary_path": CODEX_COMPLETION_PATH.as_posix()},
        "credential_redaction_policy_preservation": _source_record("stage6c_credential_redaction_policy_preservation")
        | {"secrets_written_now": False, "credential_redaction_policy_preserved": True},
        "raw_source_noncommit_proof": _noncommit_record("stage6c_raw_source_noncommit_proof"),
        "number_fact_overlays": overlays,
    }


def _summary_record(
    arithmetic: dict[str, Any],
    source_browser: dict[str, int],
    overlays: dict[str, Any],
    future: dict[str, Any],
) -> dict[str, Any]:
    return _base_project_record("stage6c_summary") | {
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "previous_stage_id": PREVIOUS_STAGE_ID,
        "previous_stage_title": PREVIOUS_STAGE_TITLE,
        "starting_commit": STARTING_COMMIT,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage6b_preserved": True,
        "stage6b_probe_mapping_repairs_preserved": True,
        "stage6b_hook_report_only_default_preserved": True,
        "stage6b_default_hook_exit_zero_preserved": True,
        "stage6b_strict_hook_mode_preserved": True,
        "exact_quote": EXACT_QUOTE,
        "quote_source_status": "solved_translation_precedent",
        "quote_used_as": ["thematic_bridge", "source_locked_context", "future_probe_watchlist_context"],
        "quote_not_used_as": ["route_rule", "proof", "decryption_key", "solve_claim"],
        "ouroboros_total": arithmetic["ouroboros_total"],
        "vowel_sum": arithmetic["vowel_sum"],
        "consonant_sum": arithmetic["consonant_sum"],
        "delta_ouroboros_minus_pdd153": arithmetic["delta_ouroboros_minus_pdd153"],
        "o_cyclic_distance_compact": arithmetic["o_cyclic_distance_compact"],
        "inter_o_segment_gp_values": arithmetic["inter_o_segment_gp_values"],
        "robor_gp_sum": arithmetic["robor_gp_sum"],
        "oro_gp_sum": arithmetic["oro_gp_sum"],
        "zero_based_index_sum": arithmetic["zero_based_index_sum"],
        "one_based_index_sum": arithmetic["one_based_index_sum"],
        "radius_if_circumference_31_approx": arithmetic["radius_if_circumference_31"],
        "diameter_if_circumference_31_approx": arithmetic["diameter_if_circumference_31"],
        "page32_3222_red_highlighted_status": arithmetic["page32_3222_red_highlighted_status"],
        "operator_observed_highlight_claim_pending_source_confirmation": True,
        "source_lock_record_count": len(HISTORICAL_ROUTE_PATHS),
        "future_probe_count": len(future["future_probes"]),
        "overlay_count": len(overlays["overlays"]),
        "stage6d_manifest_input_addendum_created": True,
        "not_final_stage7_manifest": True,
        "stage6d_final_manifest_required": True,
        "stage8_stage9_watchlist_created": True,
        "full_parallel_validation_workers": 10,
        "full_parallel_validation_pytest_workers": 10,
        "full_serial_pytest_run": False,
        **source_browser,
    }


def _historical_records(arithmetic: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "i31_vowel_voice_circumference": _historical_record("stage6c_ouroboros_i31_vowel_voice_circumference_candidate")
        | {
            "phrase": "OUROBOROS",
            "profile_form": "OUROBOROS",
            "exact_quote": EXACT_QUOTE,
            "quote_source_status": "solved_translation_precedent",
            "quote_used_as": ["thematic_bridge", "source_locked_context", "future_probe_watchlist_context"],
            "quote_not_used_as": ["route_rule", "proof", "decryption_key", "solve_claim"],
            "text_layer_policy": _text_layer_policy(),
            "gp_values": arithmetic["ouroboros_gp_sequence"],
            "ouroboros_total": arithmetic["ouroboros_total"],
            "vowel_positions_one_based": arithmetic["vowel_positions_one_based"],
            "vowel_letters": arithmetic["vowel_letters"],
            "vowel_gp_values": arithmetic["vowel_gp_values"],
            "vowel_sum": arithmetic["vowel_sum"],
            "vowel_sum_equals_gp_i": True,
            "proof_status": "not_proof",
            "source_paths": _paths("gp_profile", "solved_i_voice_circumference_quote", "ouroboros_gp167_and_transform_context"),
        },
        "t16_consonant_shell_pdd153": _historical_record("stage6c_ouroboros_t16_consonant_shell_pdd153_bridge")
        | {
            "consonant_letters": arithmetic["consonant_letters"],
            "consonant_gp_values": arithmetic["consonant_gp_values"],
            "consonant_sum": arithmetic["consonant_sum"],
            "consonant_sum_equals_t16": True,
            "t16": 136,
            "t17": 153,
            "pdd153": 153,
            "delta_ouroboros_minus_pdd153": arithmetic["delta_ouroboros_minus_pdd153"],
            "delta_i_minus_17": 14,
            "rewritten_expression": "(T16 + I) - (T16 + 17) = I - 17 = 31 - 17 = 14",
            "source_paths": _paths("gp_profile", "ouroboros_gp167_and_transform_context", "pdd153_and_56311"),
        },
        "o_ring_3222_page32": _historical_record("stage6c_ouroboros_o_ring_3222_page32_spiral_bridge")
        | {
            "o_positions_one_based": arithmetic["o_positions_one_based"],
            "o_cyclic_distances": arithmetic["o_cyclic_distances"],
            "o_cyclic_distance_compact": arithmetic["o_cyclic_distance_compact"],
            "alternative_gap_convention": {"intervening_non_o_counts": [2, 1, 1, 1]},
            "page32_3222_status": {
                "source_backed_as_grid_value": True,
                "source_backed_as_spiral_sequence_value": True,
                "source_backed_as_red_or_highlighted": False,
                "image_inspection_performed_now": False,
                "image_interpretation_performed_now": False,
            },
            "operator_observed_highlight_claim_pending_source_confirmation": True,
            "source_paths": _paths("ouroboros_gp167_and_transform_context", "page32_3222"),
        },
        "pdd153_offset14_56311": _historical_record("stage6c_ouroboros_pdd153_offset14_56311_phase_bridge")
        | {
            "sequence": [5, 6, 3, 11],
            "cumulative_offsets": [5, 11, 14, 25],
            "delta_ouroboros_minus_pdd153": 14,
            "ring_size": 31,
            "phase_points": [0, 5, 11, 14, 25],
            "closure_arc": 6,
            "partition_candidate": [5, 6, 3, 11, 6],
            "source_paths": _paths("gp_profile", "pdd153_and_56311"),
        },
        "palindromic_core": _historical_record("stage6c_ouroboros_palindromic_core_97_and_oro25_candidate")
        | {
            "inter_o_segmentation": "O [UR] O [B] O [R] O [S]",
            "inter_o_segment_labels": ["UR", "B", "R", "S"],
            "inter_o_segment_gp_values": arithmetic["inter_o_segment_gp_values"],
            "inter_o_segment_key_observation": "UR = 14, matching OUROBOROS 167 minus PDD153 153 and the 56311 cumulative offset 14.",
            "robor_substring": "ROBOR",
            "robor_positions_one_based": [3, 4, 5, 6, 7],
            "robor_gp_sum": arithmetic["robor_gp_sum"],
            "robor_gp_relation": "97 = GP(A)",
            "oro_substring": "ORO",
            "oro_gp_sum": arithmetic["oro_gp_sum"],
            "oro_gp_relation": "25 matches the 56311 net step sum 5+6+3+11.",
            "status": "review_only_future_probe_context",
            "source_paths": _paths("gp_profile", "ouroboros_gp167_and_transform_context", "pdd153_and_56311"),
        },
        "index_checksum": _historical_record("stage6c_ouroboros_index_checksum_candidates")
        | {
            "zero_based_profile_indices": arithmetic["zero_based_profile_indices"],
            "zero_based_index_sum": arithmetic["zero_based_index_sum"],
            "zero_based_gp_relation": "53 = GP(S), and S is the final rune/letter of OUROBOROS.",
            "one_based_profile_indices": arithmetic["one_based_profile_indices"],
            "one_based_index_sum": arithmetic["one_based_index_sum"],
            "one_based_gp_relation": "62 = 2 * 31, and 31 is both GP(I) and the OUROBOROS vowel/voice layer.",
            "status": "review_only_future_probe_context",
            "source_paths": _paths("gp_profile", "ouroboros_gp167_and_transform_context"),
        },
        "i31_geometry": _historical_record("stage6c_i31_circumference_radius5_diameter10_geometry_candidate")
        | {
            "circumference_candidate": 31,
            "radius_if_circumference_31": arithmetic["radius_if_circumference_31"],
            "diameter_if_circumference_31": arithmetic["diameter_if_circumference_31"],
            "radius5_diameter10_are_approximate": True,
            "proof_status": "geometric_model_candidate_only",
            "source_paths": _paths("gp_profile", "solved_i_voice_circumference_quote", "pdd153_and_56311"),
        },
        "variant_spelling_controls": _historical_record("stage6c_ouroboros_variant_spelling_control_candidates")
        | {
            "text_layer_policy": _text_layer_policy(),
            "variant_controls": arithmetic["variant_controls"],
            "finite_variant_family_only": True,
            "arbitrary_dictionary_or_spelling_search_performed": False,
            "source_paths": _paths("gp_profile", "ouroboros_gp167_and_transform_context"),
        },
        "stage8_stage9_watchlist": _historical_record("stage6c_ouroboros_stage8_stage9_output_watchlist")
        | {
            "stage8_stage9_watchlist_terms": [
                "I31_voice_layer",
                "OUROBOROS_167",
                "T16_plus_I",
                "delta14",
                "3222",
                "phase_offsets_0_5_11_14_25",
                "circumference31_radius5_diameter10",
                "second_stage_surface_not_plaintext_policy",
            ],
            "second_stage_surface_not_plaintext_policy": True,
            "source_paths": ALL_SOURCE_PATHS,
        },
    }


def _future_probe_registry() -> dict[str, Any]:
    return _token_record("stage6c_ouroboros_future_probe_registry") | {
        "future_probe_ids": FUTURE_PROBE_IDS,
        "control_bundle_id": CONTROL_BUNDLE_ID,
        "control_bundle": CONTROL_BUNDLE,
        "not_final_stage7_manifest": True,
        "stage6d_final_manifest_required": True,
        "future_probes": [
            {
                "probe_id": probe_id,
                "stage6c_run_now": False,
                "execution_enabled_now": False,
                "stage7_execution_enabled_now": False,
                "full_output_archive_required_when_run": True,
                "usable_for_decision_now": False,
                "not_solve_evidence": True,
                "control_bundle_id": CONTROL_BUNDLE_ID,
                "controls_required": CONTROL_BUNDLE,
                "blocked_actions": [
                    "solve_claim",
                    "target_selection",
                    "route_stream_generation_unless_later_stage_explicitly_allows",
                    "byte_stream_generation_unless_later_stage_explicitly_allows",
                ],
            }
            for probe_id in FUTURE_PROBE_IDS
        ],
    }


def _stage6d_manifest_input_addendum() -> dict[str, Any]:
    return _token_record("stage6c_stage6d_manifest_input_addendum") | {
        "stage6d_manifest_input_addendum": {
            "source_locked_review_facts": SOURCE_LOCKED_REVIEW_FACTS,
            "future_probe_ids": FUTURE_PROBE_IDS,
            "not_final_stage7_manifest": True,
            "stage6d_final_manifest_required": True,
        },
        "source_locked_review_facts": SOURCE_LOCKED_REVIEW_FACTS,
        "future_probe_ids": FUTURE_PROBE_IDS,
        "not_final_stage7_manifest": True,
        "stage6d_final_manifest_required": True,
    }


def _overlay_collection(arithmetic: dict[str, Any]) -> dict[str, Any]:
    overlays = [
        _overlay(
            "stage6c_ouroboros_gp167_total_overlay",
            "stage6c_ouroboros_i31_vowel_voice_circumference_candidate_v0",
            "OUROBOROS = 167",
            "OUROBOROS = 167",
            167,
            [167],
            "Existing cycle/self-reference GP fact, now crosslinked to I31 voice/circumference structure.",
            HISTORICAL_ROUTE_PATHS["i31_vowel_voice_circumference"],
            "high",
        ),
        _overlay(
            "stage6c_ouroboros_vowel_voice_i31_overlay",
            "stage6c_ouroboros_i31_vowel_voice_circumference_candidate_v0",
            "O+U+O+O+O = 31 = GP(I)",
            "O+U+O+O+O = 31 = GP(I)",
            31,
            [31, 7, 3, 7, 7, 7],
            "The vowel/voice layer of OUROBOROS lands on I=31 and crosslinks to THE I IS THE VOICE OF THE CIRCUMFERENCE.",
            HISTORICAL_ROUTE_PATHS["i31_vowel_voice_circumference"],
            "high",
        ),
        _overlay(
            "stage6c_ouroboros_consonant_shell_t16_overlay",
            "stage6c_ouroboros_t16_consonant_shell_pdd153_bridge_v0",
            "R+B+R+S = 136 = T16",
            "R+B+R+S = 136 = T16",
            136,
            [136, 16, 17],
            "OUROBOROS consonant shell equals the triangular number immediately before PDD T17.",
            HISTORICAL_ROUTE_PATHS["t16_consonant_shell_pdd153"],
            "high",
        ),
        _overlay(
            "stage6c_ouroboros_t16_i_pdd153_delta14_overlay",
            "stage6c_ouroboros_t16_consonant_shell_pdd153_bridge_v0",
            "OUROBOROS = T16 + I = 136 + 31 = 167; PDD153 = T16 + 17 = 153; delta = 14.",
            "OUROBOROS = T16 + I; delta 14",
            14,
            [167, 136, 31, 153, 14],
            "Rewrites OUROBOROS-PDD153 as I-17 and crosslinks to the 56311 cumulative offset 14.",
            HISTORICAL_ROUTE_PATHS["t16_consonant_shell_pdd153"],
            "high",
        ),
        _overlay(
            "stage6c_ouroboros_o_ring_3222_page32_overlay",
            "stage6c_ouroboros_o_ring_3222_page32_spiral_bridge_v0",
            "O positions in OUROBOROS are [1,4,6,8]; cyclic distances are [3,2,2,2] -> 3222.",
            "O-ring 3222",
            3222,
            [1, 4, 6, 8, 3, 2, 2, 2],
            "3222 may be source-locked as a Page32 grid/spiral value only. Do not source-lock red/highlighted status unless an existing committed record proves it.",
            HISTORICAL_ROUTE_PATHS["o_ring_3222_page32"],
            "high",
        ),
        _overlay(
            "stage6c_i31_circumference_radius5_diameter10_overlay",
            "stage6c_i31_circumference_radius5_diameter10_geometry_candidate_v0",
            "If C=31, r=31/(2*pi)=4.93 and d=9.87.",
            "C31 radius5 diameter10",
            31,
            [31, arithmetic["radius_if_circumference_31"], arithmetic["diameter_if_circumference_31"], 5, 10],
            "Radius about 5 / diameter about 10 is approximate geometric candidate context only.",
            HISTORICAL_ROUTE_PATHS["i31_geometry"],
            "medium",
        ),
        _overlay(
            "stage6c_i31_56311_phase_ring_overlay",
            "stage6c_ouroboros_pdd153_offset14_56311_phase_bridge_v0",
            "56311 cumulative offsets [5,11,14,25] can be viewed as candidate phases [0,5,11,14,25] on a 31-unit ring; closure arc is 6.",
            "I31 56311 phase ring",
            31,
            [0, 5, 11, 14, 25, 6],
            "No route readout generated.",
            HISTORICAL_ROUTE_PATHS["pdd153_offset14_56311"],
            "medium",
        ),
        _overlay(
            "stage6c_ouroboros_variant_control_overlay",
            "stage6c_ouroboros_variant_spelling_control_candidates_v0",
            "OUROBOROS has vowel layer 31; UROBOROS and OROBOROS preserve consonant shell 136 but change the vowel layer.",
            "variant controls",
            31,
            [167, 160, 164, 31, 24, 28, 136],
            "Variant controls for the voice/I31 claim; UROBOROS is not an O/U alias.",
            HISTORICAL_ROUTE_PATHS["variant_spelling_controls"],
            "medium",
        ),
        _overlay(
            "stage6c_pdd153_mod31_gp29_overlay",
            "stage6c_i31_circumference_radius5_diameter10_geometry_candidate_v0",
            "153 = 4*31 + 29.",
            "PDD153 mod31 GP29",
            153,
            [153, 4, 31, 29],
            "Selection-risk warning required.",
            HISTORICAL_ROUTE_PATHS["i31_geometry"],
            "low",
        ),
        _overlay(
            "stage6c_ouroboros_palindromic_core_overlay",
            "stage6c_ouroboros_palindromic_core_97_and_oro25_candidate_v0",
            "ROBOR = 97 = GP(A); ORO = 25.",
            "ROBOR97 ORO25",
            97,
            [97, 25],
            "Control scan required before assigning significance.",
            HISTORICAL_ROUTE_PATHS["palindromic_core"],
            "medium",
        ),
        _overlay(
            "stage6c_ouroboros_inter_o_segments_offset14_overlay",
            "stage6c_ouroboros_palindromic_core_97_and_oro25_candidate_v0",
            "O[UR]O[B]O[R]O[S]; inter-O segment sums are [14,61,11,53]; UR=14.",
            "inter-O UR14",
            14,
            [14, 61, 11, 53],
            "UR=14 crosslinks to OUROBOROS 167 - PDD153 153 = 14 and the 56311 cumulative offset 14. Review-only bridge, not a route rule.",
            HISTORICAL_ROUTE_PATHS["palindromic_core"],
            "medium",
        ),
        _overlay(
            "stage6c_ouroboros_index_checksum_overlay",
            "stage6c_ouroboros_index_checksum_candidates_v0",
            "OUROBOROS zero-based GP profile indices sum to 53=GP(S), final rune S; one-based indices sum to 62=2*31.",
            "index checksum",
            53,
            [53, 62, 31],
            "Candidate self-terminal checksum and I31/vowel-layer double relation. Control scan required before assigning significance.",
            HISTORICAL_ROUTE_PATHS["index_checksum"],
            "low",
        ),
    ]
    return _overlay_record("stage6c_source_browser_number_fact_enrichment_overlay_collection") | {
        "review_batch_id": "stage6c_ouroboros_i31_circumference_review_only",
        "review_batch_selection_policy": "source_lock_addendum_not_number_fact_review_batch",
        "overlay_count": len(overlays),
        "usable_for_decision_now": False,
        "overlays": overlays,
    }


def _overlay(
    overlay_id: str,
    source_fact_id: str,
    expression: str,
    short_label: str,
    value: int | float,
    values: list[int | float],
    relation: str,
    source_record_path: Path,
    display_priority: str,
) -> dict[str, Any]:
    return {
        "overlay_id": overlay_id,
        "source_record_path": source_record_path.as_posix(),
        "source_fact_id": source_fact_id,
        "fact_class": "stage6c_ouroboros_i31_review_fact",
        "display_label": expression,
        "short_label": short_label,
        "value": value,
        "values": values,
        "value_type": "gp_arithmetic_or_geometry_candidate",
        "operation_type": "review_only_source_lock_addendum",
        "expression": expression,
        "relation": relation,
        "why_stored": "Preserve the OUROBOROS/I31 circumference bridge as review-only Stage 6D input context.",
        "verification_status": "arithmetic_verified_metadata_only",
        "display_priority": display_priority,
        "source_paths": ALL_SOURCE_PATHS,
        "crosslinks": SOURCE_CROSSLINKS,
        "risk_notes": ["not_proof", "not_route_seed", "requires_controls", "no_execution_now"],
        "controls_required": CONTROL_BUNDLE,
        "not_allowed_as": NOT_ALLOWED_AS,
        "usable_for_decision_now": False,
    }


def _next_stage_decision_record() -> dict[str, Any]:
    return _base_project_record("stage6c_next_stage_decision") | {
        "selected_next_stage_id": NEXT_STAGE_ID,
        "selected_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }


def _stage6b_preservation_record() -> dict[str, Any]:
    return _base_project_record("stage6c_stage6b_preservation") | {
        "stage6b_preserved": True,
        "stage6b_commit_preserved": STARTING_COMMIT,
        "stage6b_probe_mapping_repairs_preserved": True,
        "stage6b_hook_report_only_default_preserved": True,
        "stage6b_default_hook_exit_zero_preserved": True,
        "stage6b_strict_hook_mode_preserved": True,
        "stage6_records_mutated_now": False,
        "stage6b_records_mutated_now": False,
    }


def _source_lock_addendum_summary(arithmetic: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6c_source_lock_addendum_summary") | {
        "source_lock_record_count": len(HISTORICAL_ROUTE_PATHS),
        "source_paths": ALL_SOURCE_PATHS,
        "exact_quote": EXACT_QUOTE,
        "ouroboros_total": arithmetic["ouroboros_total"],
        "vowel_sum": arithmetic["vowel_sum"],
        "consonant_sum": arithmetic["consonant_sum"],
        "o_cyclic_distance_compact": arithmetic["o_cyclic_distance_compact"],
        "page32_3222_red_highlighted_status": arithmetic["page32_3222_red_highlighted_status"],
    }


def _reviewability_gap_record(arithmetic: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6c_reviewability_gap_register") | {
        "reviewability_gaps": [
            {
                "gap_id": "page32_3222_red_highlight_pending_source_confirmation",
                "page32_3222_red_highlighted_status": arithmetic["page32_3222_red_highlighted_status"],
                "operator_observed_highlight_claim_pending_source_confirmation": True,
                "image_inspection_performed_now": False,
                "image_interpretation_performed_now": False,
            }
        ],
        "reviewability_gap_count": 1,
    }


def _validation_evidence_record(arithmetic: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6c_reviewable_validation_evidence") | {
        "exact_integer_assertions": {
            "ouroboros_total": arithmetic["ouroboros_total"],
            "vowel_sum": arithmetic["vowel_sum"],
            "consonant_sum": arithmetic["consonant_sum"],
            "t16": 136,
            "pdd153": 153,
            "delta": arithmetic["delta_ouroboros_minus_pdd153"],
            "o_cyclic_distances": arithmetic["o_cyclic_distances"],
            "o_cyclic_distance_compact": arithmetic["o_cyclic_distance_compact"],
            "inter_o_segment_gp_values": arithmetic["inter_o_segment_gp_values"],
            "robor_gp_sum": arithmetic["robor_gp_sum"],
            "oro_gp_sum": arithmetic["oro_gp_sum"],
            "zero_based_index_sum": arithmetic["zero_based_index_sum"],
            "one_based_index_sum": arithmetic["one_based_index_sum"],
        },
        "float_assertions": {
            "radius_if_circumference_31": arithmetic["radius_if_circumference_31"],
            "diameter_if_circumference_31": arithmetic["diameter_if_circumference_31"],
            "tolerance": 0.01,
        },
        "protected_local_paths": stage6.PROTECTED_LOCAL_PATHS,
        "protected_local_paths_staged": False,
    }


def _current_stage_transition_record() -> dict[str, Any]:
    return _base_project_record("stage6c_current_stage_transition") | {
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
        "stage8_triangle_readiness_started_now": False,
        "stage9_experiments_started_now": False,
    }


def _route_fingerprint_watchlist() -> dict[str, Any]:
    return _token_record("stage6c_ouroboros_route_fingerprint_watchlist") | {
        "watchlist_terms": [
            "I31_voice_layer",
            "OUROBOROS_167",
            "T16_plus_I",
            "delta14",
            "3222",
            "phase_offsets_0_5_11_14_25",
            "circumference31_radius5_diameter10",
            "second_stage_surface_not_plaintext_policy",
        ],
        "plaintext_required_for_interest": False,
    }


def _null_negative_control_policy() -> dict[str, Any]:
    return _token_record("stage6c_ouroboros_null_negative_control_policy") | {
        "control_bundle_id": CONTROL_BUNDLE_ID,
        "controls": CONTROL_BUNDLE,
        "controls_attached_to_each_future_probe": True,
    }


def _keeper_taxonomy() -> dict[str, Any]:
    return _token_record("stage6c_ouroboros_keeper_taxonomy") | {
        "keeper_categories": [
            "circumference_value_bridge",
            "vowel_voice_layer_bridge",
            "triangle_shell_bridge",
            "pdd_offset_bridge",
            "page32_spiral_residue_bridge",
            "multi_spiral_phase_candidate",
            "spelling_variant_control",
            "second_stage_surface_watchlist",
            "transform_grammar_bridge",
        ],
        "not_allowed_as": NOT_ALLOWED_AS,
    }


def _gate_record(record_type: str) -> dict[str, Any]:
    return _token_record(record_type) | {
        "active_ingestion_performed": False,
        "real_byte_stream_generated": False,
        "route_stream_generated_now": False,
        "execution_performed": False,
    }


def _source_crosslink_register() -> dict[str, Any]:
    return _source_record("stage6c_ouroboros_source_crosslink_register") | {
        "source_crosslinks": SOURCE_CROSSLINKS,
        "all_source_paths": ALL_SOURCE_PATHS,
        "raw_source_files_committed": False,
        "raw_third_party_files_committed": False,
    }


def _noncommit_record(record_type: str) -> dict[str, Any]:
    return _source_record(record_type) | {
        "protected_local_paths": stage6.PROTECTED_LOCAL_PATHS,
        "protected_local_paths_staged": False,
        "third_party_staged": False,
        "data_raw_staged": False,
        "experiments_results_staged": False,
        "codex_output_staged": False,
        "wiki_worktree_staged": False,
        "sqlite_or_database_staged": False,
        "binary_or_archive_staged": False,
    }


def _arithmetic() -> dict[str, Any]:
    profile = _profile_lookup()
    values = {label: profile[label]["prime"] for label in ["O", "U", "R", "B", "S", "I", "A"]}
    indices = {label: profile[label]["index"] for label in ["O", "U", "R", "B", "S", "I", "A"]}
    letters = list("OUROBOROS")
    gp_sequence = [values[letter] for letter in letters]
    zero_indices = [indices[letter] for letter in letters]
    one_indices = [index + 1 for index in zero_indices]
    variant_controls = [
        _variant_control("OUROBOROS", values, "canonical_test_surface_for_i31_voice_candidate"),
        _variant_control("UROBOROS", values, "spelling_variant_control_not_alias"),
        _variant_control("OROBOROS", values, "spelling_variant_control_not_alias"),
    ]
    return {
        "profile_values": values,
        "profile_indices": indices,
        "ouroboros_profile_form": "OUROBOROS",
        "ouroboros_gp_sequence": gp_sequence,
        "ouroboros_total": sum(gp_sequence),
        "vowel_positions_one_based": [1, 2, 4, 6, 8],
        "vowel_letters": ["O", "U", "O", "O", "O"],
        "vowel_gp_values": [values["O"], values["U"], values["O"], values["O"], values["O"]],
        "vowel_sum": 31,
        "consonant_letters": ["R", "B", "R", "S"],
        "consonant_gp_values": [values["R"], values["B"], values["R"], values["S"]],
        "consonant_sum": 136,
        "delta_ouroboros_minus_pdd153": 14,
        "o_positions_one_based": [1, 4, 6, 8],
        "o_cyclic_distances": [3, 2, 2, 2],
        "o_cyclic_distance_compact": "3222",
        "inter_o_segment_gp_values": [values["U"] + values["R"], values["B"], values["R"], values["S"]],
        "robor_gp_sum": values["R"] + values["O"] + values["B"] + values["O"] + values["R"],
        "oro_gp_sum": values["O"] + values["R"] + values["O"],
        "zero_based_profile_indices": zero_indices,
        "zero_based_index_sum": sum(zero_indices),
        "one_based_profile_indices": one_indices,
        "one_based_index_sum": sum(one_indices),
        "radius_if_circumference_31": round(31 / (2 * math.pi), 2),
        "diameter_if_circumference_31": round(31 / math.pi, 2),
        "radius5_diameter10_are_approximate": True,
        "variant_controls": variant_controls,
        "page32_3222_red_highlighted_status": _page32_3222_red_status(),
    }


def _variant_control(spelling: str, values: dict[str, int], status: str) -> dict[str, Any]:
    letters = list(spelling)
    total = sum(values[letter] for letter in letters)
    vowel_sum = sum(values[letter] for letter in letters if letter in {"O", "U"})
    consonant_sum = sum(values[letter] for letter in letters if letter in {"R", "B", "S"})
    excess = total - 153
    label = None
    for candidate, prime in values.items():
        if prime == excess:
            label = candidate
            break
    return {
        "spelling": spelling,
        "gp_total": total,
        "vowel_sum": vowel_sum,
        "consonant_sum": consonant_sum,
        "excess_over_pdd153": excess,
        "excess_label": label,
        "special_status": status,
    }


def _profile_lookup() -> dict[str, dict[str, int]]:
    data = json.loads(GP_PROFILE_PATH.read_text(encoding="utf-8"))
    lookup: dict[str, dict[str, int]] = {}
    for entry in data["entries"]:
        for label in entry["latin_labels"]:
            lookup[label] = {"prime": int(entry["prime"]), "index": int(entry["index"])}
    return lookup


def _page32_3222_red_status() -> str:
    text = SOURCE_CROSSLINKS["page32_3222"][0]
    page32_text = Path(text).read_text(encoding="utf-8").lower()
    if "red_3222" in page32_text or "highlighted_3222" in page32_text:
        return "source_confirmed"
    return "not_source_confirmed"


def _text_layer_policy() -> dict[str, Any]:
    return {
        "exact_rune_tokens": "required_where_available",
        "gp_profile_preferred_latin_labels": "required_for_arithmetic",
        "editorial_english": "display_only_or_source_quote_only",
        "alias_groups": ["U/V", "C/K", "S/Z", "ING/NG", "IA/IO"],
        "important_negative_alias_note": "O and U are distinct GP runes; UROBOROS is a spelling variant/control, not an O/U alias.",
    }


def _paths(*keys: str) -> list[str]:
    return sorted({path for key in keys for path in SOURCE_CROSSLINKS[key]})


def _source_browser_counts() -> dict[str, int]:
    index = build_source_index()
    result = validate_source_index()
    return {
        "source_browser_entries_loaded": len(index.entries),
        "source_browser_records_scanned": len(index.scanned_paths),
        "source_browser_validation_error_count": len(result.errors),
    }


def _base_record(record_type: str, schema_path: Path) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": schema_path.as_posix(),
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "reviewability_stage": True,
        "source_lock_addendum_stage": True,
        "probe_diagnostic_readiness_stage": True,
        "number_fact_review_batch_stage": False,
        "source_lock_only": False,
        "source_lock_component_present": True,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        **FORBIDDEN_FALSE,
    }


def _base_project_record(record_type: str) -> dict[str, Any]:
    key = record_type.removeprefix("stage6c_")
    return _base_record(record_type, SCHEMA_PATHS[key])


def _historical_record(record_type: str) -> dict[str, Any]:
    key = record_type.removeprefix("stage6c_").removesuffix("_candidate").removesuffix("_bridge")
    path_key = {
        "ouroboros_i31_vowel_voice_circumference": "i31_vowel_voice_circumference",
        "ouroboros_t16_consonant_shell_pdd153": "t16_consonant_shell_pdd153",
        "ouroboros_o_ring_3222_page32_spiral": "o_ring_3222_page32",
        "ouroboros_pdd153_offset14_56311_phase": "pdd153_offset14_56311",
        "ouroboros_palindromic_core_97_and_oro25": "palindromic_core",
        "ouroboros_index_checksum_candidates": "index_checksum",
        "i31_circumference_radius5_diameter10_geometry": "i31_geometry",
        "ouroboros_variant_spelling_control_candidates": "variant_spelling_controls",
        "ouroboros_stage8_stage9_output_watchlist": "stage8_stage9_watchlist",
    }[key]
    return _base_record(record_type, SCHEMA_PATHS[path_key]) | {
        "usable_for_decision_now": False,
        "not_allowed_as": NOT_ALLOWED_AS,
    }


def _token_record(record_type: str) -> dict[str, Any]:
    key = {
        "stage6c_ouroboros_future_probe_registry": "future_probe_registry",
        "stage6c_ouroboros_route_fingerprint_watchlist": "route_fingerprint_watchlist",
        "stage6c_ouroboros_null_negative_control_policy": "null_negative_control_policy",
        "stage6c_ouroboros_keeper_taxonomy": "keeper_taxonomy",
    }.get(record_type, record_type.removeprefix("stage6c_"))
    return _base_record(record_type, SCHEMA_PATHS[key])


def _source_record(record_type: str) -> dict[str, Any]:
    key = {
        "stage6c_ouroboros_source_crosslink_register": "source_crosslink_register",
    }.get(record_type, record_type.removeprefix("stage6c_"))
    return _base_record(record_type, SCHEMA_PATHS[key])


def _overlay_record(record_type: str) -> dict[str, Any]:
    return _base_record(record_type, SCHEMA_PATHS["number_fact_overlays"])


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_schema_for(key), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _update_doc_staleness_source_of_truth_schema()


def _schema_for(key: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"type": "string"},
        "schema": {"type": "string"},
        "stage_id": {"const": STAGE_ID},
        "stage_title": {"const": STAGE_TITLE},
        "metadata_only": {"const": True},
        "puzzle_execution_allowed": {"const": False},
        "solve_claim": {"const": False},
        "generated_outputs_committed": {"const": False},
        "raw_source_files_committed": {"const": False},
        "raw_third_party_files_committed": {"const": False},
        "route_stream_generated_now": {"const": False},
        "real_byte_stream_generated": {"const": False},
        "cuda_execution_performed": {"const": False},
        "scoring_performed": {"const": False},
        "benchmark_performed": {"const": False},
        "stage6c_routes_to_stage7_now": {"const": False},
        "stage6c_runs_any_probe_now": {"const": False},
        "stage7_execution_allowed_next": {"const": False},
    }
    if key == "summary":
        properties.update(
            {
                "status": {"const": "complete"},
                "recommended_next_stage_id": {"const": NEXT_STAGE_ID},
                "exact_quote": {"const": EXACT_QUOTE},
                "ouroboros_total": {"const": 167},
                "vowel_sum": {"const": 31},
                "page32_3222_red_highlighted_status": {"const": "not_source_confirmed"},
            }
        )
    if key == "number_fact_overlays":
        properties["overlays"] = {"type": "array", "minItems": len(OVERLAY_IDS)}
    if key == "future_probe_registry":
        properties["future_probe_ids"] = {"const": FUTURE_PROBE_IDS}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://liberprimus-gpu.local/schemas/stage6c/{key}",
        "type": "object",
        "required": ["record_type", "schema", "stage_id", "stage_title", "metadata_only", "puzzle_execution_allowed", "solve_claim"],
        "properties": properties,
        "additionalProperties": True,
    }


def _update_current_stage_schema() -> None:
    schema = json.loads(CURRENT_STAGE_SCHEMA_PATH.read_text(encoding="utf-8"))
    stage_ids = schema["properties"]["stage_id"]["enum"]
    if STAGE_ID not in stage_ids:
        stage_ids.append(STAGE_ID)
    latest = schema["properties"]["latest_completed_stage_id"]["enum"]
    if STAGE_ID not in latest:
        latest.append(STAGE_ID)
    next_stages = schema["properties"]["recommended_next_stage_id"]["enum"]
    if NEXT_STAGE_ID not in next_stages:
        next_stages.append(NEXT_STAGE_ID)
    CURRENT_STAGE_SCHEMA_PATH.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _update_doc_staleness_source_of_truth_schema() -> None:
    schema = json.loads(DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH.read_text(encoding="utf-8"))
    stage_ids = schema["properties"]["stage_id"]["enum"]
    if STAGE_ID not in stage_ids:
        stage_ids.append(STAGE_ID)
    DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH.write_text(
        json.dumps(schema, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_current_stage_state(summary: dict[str, Any]) -> None:
    payload = read_yaml(CURRENT_STAGE_STATE_PATH)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "stage_title": STAGE_TITLE,
            "prompt_type": PROMPT_TYPE,
            "metadata_only": True,
            "source_lock_only": False,
            "source_lock_component_present": True,
            "source_lock_addendum_stage": True,
            "probe_diagnostic_readiness_stage": True,
            "puzzle_execution_allowed": False,
            "solve_claim": False,
            "status": "complete",
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "previous_completed_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
            "latest_completed_stage": {
                "stage_id": STAGE_ID,
                "stage_title": STAGE_TITLE,
                "completed_commit": "",
                "completed_date": "2026-06-15",
                "status": "complete",
            },
            "next_stage": {"stage_id": NEXT_STAGE_ID, "stage_title": NEXT_STAGE_TITLE, "prompt_type": NEXT_PROMPT_TYPE},
            "post_push_handoff_locations": [CODEX_COMPLETION_PATH.as_posix(), "GitHub issue comment"],
            "stage7_execution_allowed_next": False,
            "stage7_zip_archive_creation_allowed_next": False,
            "stage8_triangle_readiness_started_now": False,
            "stage9_experiments_started_now": False,
            "stage6b_preserved": True,
            "stage6b_probe_mapping_repairs_preserved": True,
            "stage6b_hook_report_only_default_preserved": True,
            "stage6b_default_hook_exit_zero_preserved": True,
            "stage6b_strict_hook_mode_preserved": True,
            "stage6d_final_manifest_required": True,
            "exact_quote": EXACT_QUOTE,
            "ouroboros_total": summary["ouroboros_total"],
            "vowel_sum": summary["vowel_sum"],
            "o_cyclic_distance_compact": summary["o_cyclic_distance_compact"],
            "page32_3222_red_highlighted_status": summary["page32_3222_red_highlighted_status"],
        }
    )
    payload.update(FORBIDDEN_FALSE)
    write_yaml(CURRENT_STAGE_STATE_PATH, payload)


def _write_docs(summary: dict[str, Any]) -> None:
    stage6._upsert_marked_section(Path("AGENTS.md"), STAGE_TOKEN, _agents_section())
    stage6._upsert_marked_section(Path("ChatGPT-ContextFile.md"), STAGE_TOKEN, _chatgpt_section())
    stage6._upsert_marked_section(Path("STATUS.md"), STAGE_TOKEN, _status_section())
    stage6._upsert_marked_section(Path("README.md"), STAGE_TOKEN, _readme_section())
    stage6._upsert_marked_section(Path("ROADMAP.md"), STAGE_TOKEN, _roadmap_section())
    stage6._upsert_marked_section(Path("TESTING.md"), STAGE_TOKEN, _testing_section())
    stage6._upsert_marked_section(Path("docs/roadmap/staged-plan.md"), STAGE_TOKEN, _staged_plan_section())
    stage6._upsert_marked_section(Path("docs/onboarding/start-here.md"), STAGE_TOKEN, _onboarding_section())
    stage6._upsert_marked_section(Path("docs/onboarding/source-of-truth-map.md"), STAGE_TOKEN, _source_truth_section())
    stage6._upsert_marked_section(Path("docs/onboarding/operational-file-map.md"), STAGE_TOKEN, _operational_docs_section())
    stage6._upsert_marked_section(Path("docs/reference/token-block-cli.md"), STAGE_TOKEN, _cli_section())
    stage6._upsert_marked_section(
        Path("docs/experiments/stage-6c-ouroboros-i31-circumference-source-lock.md"),
        STAGE_TOKEN,
        _experiment_doc(summary),
    )
    stage6._upsert_marked_section(
        Path("docs/development-logs/2026-06-15-stage-6c-ouroboros-i31-source-lock.md"),
        STAGE_TOKEN,
        _dev_log(summary),
    )
    stage6._upsert_marked_section(
        Path("research-log/2026-06-15-stage6c-ouroboros-i31-source-lock-summary.md"),
        STAGE_TOKEN,
        _research_log(summary),
    )
    _write_doc_staleness_source_of_truth()
    _write_operational_file_map()
    _write_stage_summary_record(summary)


def _write_doc_staleness_source_of_truth() -> None:
    path = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
    payload = read_yaml(path)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "latest_completed_stage_after_this_stage": STAGE_TITLE,
            "latest_completed_stage_prefix": "Stage 6C",
            "next_stage_after_this_stage": NEXT_STAGE_TITLE,
            "expected_next_stage_prefix": "Stage 6D",
            "expected_latest_after_stage5ah": STAGE_TITLE,
            "expected_next_after_stage5ah": NEXT_STAGE_TITLE,
            "latest_completed_stage_id": STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "stage6c_current_truth_refresh": True,
        }
    )
    write_yaml(path, payload)


def _write_operational_file_map() -> None:
    path = PROJECT_STATE_DIR / "operational-file-map.yaml"
    payload = read_yaml(path)
    record = {
        "stage_id": STAGE_ID,
        "summary": PROJECT_STATE_PATHS["summary"].as_posix(),
        "current_stage_transition": PROJECT_STATE_PATHS["current_stage_transition"].as_posix(),
        "future_probe_registry": TOKEN_BLOCK_PATHS["future_probe_registry"].as_posix(),
        "stage6d_manifest_input_addendum": TOKEN_BLOCK_PATHS["stage6d_manifest_input_addendum"].as_posix(),
        "number_fact_overlays": OPERATOR_CONSOLE_PATHS["number_fact_overlays"].as_posix(),
        "next_stage": NEXT_STAGE_ID,
    }
    records = payload.setdefault("stage_records", {})
    if isinstance(records, dict):
        records[STAGE_ID] = record
    elif isinstance(records, list):
        payload["stage_records"] = [item for item in records if item.get("stage_id") != STAGE_ID]
        payload["stage_records"].append(record)
    else:
        payload["stage_records"] = {STAGE_ID: record}
    write_yaml(path, payload)


def _write_stage_summary_record(summary: dict[str, Any]) -> None:
    path = Path("data/research/stage-summary-records-v0.yaml")
    payload = read_yaml(path)
    records = payload if isinstance(payload, list) else payload.get("records", [])
    records = [record for record in records if record.get("stage_id") != STAGE_ID]
    records.append(
        {
            "record_type": "stage_summary_record",
            "stage_id": STAGE_ID,
            "title": STAGE_TITLE,
            "status": "complete",
            "category": "source_lock_addendum",
            "summary": (
                "Source-locked the OUROBOROS/I31 circumference/Page32 3222 bridge as review-only metadata, "
                "preserved Stage 6B repairs, and routed final finite Stage 7 manifest work to Stage 6D."
            ),
            "key_outputs": [
                "Recorded the exact solved quote THE I IS THE VOICE OF THE CIRCUMFERENCE as source-layered context.",
                "Recorded OUROBOROS=167, vowel/voice layer 31=GP(I), consonant shell 136=T16, delta14, and Page32 3222 bridge metadata.",
                "Added 12 review-only Source Browser overlays and 10 disabled future probe records with control-bundle requirements.",
                "Added the Stage 6D manifest-input addendum while keeping Stage 7 execution and archive creation blocked.",
            ],
            "result_status": "metadata_source_lock_complete",
            "summary_path": PROJECT_STATE_PATHS["summary"].as_posix(),
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "metadata_only": True,
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                "No probes, final Stage 7 manifest, ZIP/archive, route extraction, byte streams, image/OCR/stego "
                "interpretation, CUDA, scoring, benchmarks, target selection, canonical-corpus activation, "
                "page-boundary finalisation, or solve claim."
            ),
            "ouroboros_total": summary["ouroboros_total"],
            "future_probe_count": summary["future_probe_count"],
        }
    )
    if isinstance(payload, list):
        write_yaml(path, records)
    else:
        payload["records"] = records
        write_yaml(path, payload)


def _write_completion_summary_stub(summary: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CODEX_COMPLETION_PATH.write_text(
        "\n".join(
            [
                "# Stage 6C Codex Completion",
                "",
                f"starting_commit: {STARTING_COMMIT}",
                "final_commit: to be filled after commit",
                "origin_main_commit: to be filled after push",
                "github_issue: to be filled after issue update",
                "ci_run_url: to be filled after CI",
                "ci_status: to be filled after CI",
                f"stage: {STAGE_TITLE}",
                f"ouroboros_total: {summary['ouroboros_total']}",
                f"vowel_sum: {summary['vowel_sum']}",
                f"future_probe_count: {summary['future_probe_count']}",
                f"overlay_count: {summary['overlay_count']}",
                f"page32_3222_red_highlighted_status: {summary['page32_3222_red_highlighted_status']}",
                "operator_observed_highlight_claim_pending_source_confirmation: true",
                "no_probe_execution: true",
                "no_stage7_manifest_created: true",
                "stage6d_routed_next: true",
                "protected_local_paths_not_staged: true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _agents_section() -> str:
    return f"""## Stage 6C Current Boundary

Current completed stage: {STAGE_TITLE}.

Current work: {NEXT_STAGE_TITLE}. Stage 6C source-locked the OUROBOROS/I31 circumference bridge as review-only metadata and preserved Stage 6B probe-map and hook repairs. It did not run probes, finalize Stage 7, create archives, generate route or byte streams, inspect images, run OCR/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
"""


def _chatgpt_section() -> str:
    return f"""## Stage 6C Current Boundary

Latest completed stage: {STAGE_TITLE}.

Current planning focus: {NEXT_STAGE_TITLE}.

Stage 6C source-locked the OUROBOROS / I31 circumference bridge as review-only metadata. OUROBOROS=167; vowel/voice layer O+U+O+O+O=31=GP(I); consonant shell R+B+R+S=136=T16. This crosslinks to the solved quote THE I IS THE VOICE OF THE CIRCUMFERENCE, PDD153=T17, delta 14, 56311 offsets, and Page32 grid/spiral value 3222. 3222 is source-backed as a Page32 grid/spiral value; red/highlighted status is not accepted unless separately source-confirmed. Stage 6C added future probes/watchlists only, no execution, no Stage 7 manifest, no route extraction, no solve claim. Stage 6D is next for final finite Stage 7 manifest and archive-run contract.
"""


def _status_section() -> str:
    return f"""## Stage 6C Status

Latest completed stage: {STAGE_TITLE}.

Next routed stage: {NEXT_STAGE_TITLE}. Stage 6C added review-only OUROBOROS/I31 source-lock records, Source Browser overlays, and Stage 6D manifest-input addendum records. All execution, target-selection, image/OCR/stego, CUDA/scoring, archive, and solve gates remain closed.
"""


def _readme_section() -> str:
    return f"""## Stage 6C Current Status

Current completed stage: {STAGE_TITLE}.

Current next prompt: {NEXT_STAGE_TITLE}. The OUROBOROS/I31 bridge is review-only metadata: OUROBOROS=167, the vowel/voice layer is 31=GP(I), and Page32 3222 remains source-backed only as a grid/spiral value unless separately source-confirmed as highlighted.
"""


def _roadmap_section() -> str:
    return f"""## Stage 6C Roadmap Note

Current completed stage: {STAGE_TITLE}.

Next: {NEXT_STAGE_TITLE}. Stage 6D must consume the Stage 6C source-locked facts and future-probe addendum before finalizing any finite Stage 7 manifest. Stage 7 execution is still blocked.
"""


def _testing_section() -> str:
    return """## Stage 6C Validation

Stage 6C validation includes token-block Stage 6C build/validate/summary commands, focused OUROBOROS arithmetic tests, Source Browser validation, stale-current strict scanning, Stage 6/6B regression tests, ruff, and stage-fast/local-fast/full-parallel validation with 10 workers and 10 pytest workers. Full serial pytest remains opt-in only.
"""


def _staged_plan_section() -> str:
    return f"""## Stage 6C - Complete

Stage 6C is complete as a source-lock addendum for OUROBOROS / I31 / circumference / Page32 3222 review metadata. It routes to {NEXT_STAGE_TITLE}. No probes, Stage 7 manifest, route extraction, byte streams, image interpretation, CUDA/scoring, or solve claim were added.
"""


def _onboarding_section() -> str:
    return f"""## Stage 6C Current Boundary

Latest completed stage: {STAGE_TITLE}.

Next routed stage: {NEXT_STAGE_TITLE}. Use `data/project-state/current-stage-state.yaml` as authoritative current truth.
"""


def _source_truth_section() -> str:
    return """## Stage 6C Source Of Truth

`data/project-state/current-stage-state.yaml` is authoritative for the latest completed stage. Stage 6C records are committed metadata only and must not be treated as proof, route seeds, or execution authorization.
"""


def _operational_docs_section() -> str:
    return """## Stage 6C Operational Files

Stage 6C primary records live under `data/project-state/`, `data/historical-route/`, `data/token-block/`, `data/source-harvester/`, and `data/operator-console/source-browser/number-fact-overlays/`. The local handoff lives under ignored `codex-output/`.
"""


def _cli_section() -> str:
    return """## Stage 6C Commands

- `python -m libreprimus.cli token-block build-stage6c`
- `python -m libreprimus.cli token-block validate-stage6c`
- `python -m libreprimus.cli token-block stage6c-summary`
- focused validators: `validate-stage6c-stage6b-preservation`, `validate-stage6c-source-lock-records`, `validate-stage6c-ouroboros-arithmetic`, `validate-stage6c-page32-3222-policy`, `validate-stage6c-number-fact-overlays`, `validate-stage6c-future-probe-registry`, `validate-stage6c-stage8-watchlist`, `validate-stage6c-source-browser-loadability`, `validate-stage6c-current-stage-transition`, `validate-stage6c-gate-closure`, and `validate-stage6c-handoff`.
"""


def _experiment_doc(summary: dict[str, Any]) -> str:
    return f"""# Stage 6C OUROBOROS / I31 Source-Lock Addendum

Stage 6C preserves review-only arithmetic and source crosslinks for OUROBOROS=167, vowel layer 31=GP(I), consonant shell T16, delta14, Page32 3222, and I31 circumference geometry. It created {summary['future_probe_count']} future probes and {summary['overlay_count']} Source Browser overlays, all disabled for execution.
"""


def _dev_log(summary: dict[str, Any]) -> str:
    return f"""# 2026-06-15 Stage 6C Development Log

Implemented Stage 6C source-lock addendum scaffolding, records, schemas, CLI validators, Source Browser overlays, and Stage 6D input addendum. Page32 3222 red/highlighted status is `{summary['page32_3222_red_highlighted_status']}`.
"""


def _research_log(summary: dict[str, Any]) -> str:
    return f"""# Stage 6C Research Summary

Stage 6C records the OUROBOROS/I31/circumference bridge as review-only metadata. It keeps Stage 7 execution blocked and routes final manifest work to Stage 6D. Future probe count: {summary['future_probe_count']}; overlay count: {summary['overlay_count']}.
"""


def _ensure_no_protected_output_overlap() -> None:
    outputs = {path.as_posix() for path in DATA_PATHS.values()} | {path.as_posix() for path in SCHEMA_PATHS.values()}
    overlap = outputs.intersection(stage6.PROTECTED_LOCAL_PATHS)
    if overlap:
        raise RuntimeError(f"Stage 6C outputs overlap protected local state: {sorted(overlap)}")


def _result(errors: list[str], **counts: Any) -> ValidationResult:
    return ValidationResult(errors, counts)
