"""Stage 5EI final Stage 5 diagnostics-transition metadata."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.doc_staleness.stage_ids import parse_stage_id
from libreprimus.doc_staleness.stale_current_claims import audit_repository, scan_text
from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import validate_source_index
from libreprimus.token_block.models import read_yaml, write_json, write_yaml

STAGE_ID = "stage-5ei"
STAGE_TOKEN = "stage5ei"
STAGE_TITLE = "Stage 5EI - Final Stage 5 triangle-transposition and diagnostics transition, without execution"
PROMPT_TYPE = "codex_plan_mode_metadata_transition"
PREVIOUS_STAGE_ID = "stage-5eh"
PREVIOUS_STAGE_TITLE = (
    "Stage 5EH - Lag5/outguess/byte-string/red-number/F5 context source-lock addendum, "
    "diagnostic probe manifests, and enriched fact cards, without execution"
)
PREVIOUS_STAGE_PRIMARY_COMMIT = "3bb0e866984602afe2914b8125ece11c3fd4224f"
PREVIOUS_STAGE_FINAL_COMMIT = "10a33e53c985c1d9c3f7a1145cd49be4a1815102"
PREVIOUS_STAGE_ISSUE = 169
PREVIOUS_STAGE_CI_RUN = 27464050325
PREVIOUS_STAGE_CI_STATUS = "passed"
NEXT_STAGE_ID = "stage-6"
NEXT_STAGE_TITLE = "Stage 6 - Probe and diagnostic readiness, without execution"

PROJECT_STATE_DIR = Path("data/project-state")
TOKEN_BLOCK_DIR = Path("data/token-block")
HISTORICAL_ROUTE_DIR = Path("data/historical-route")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
OPERATOR_OVERLAY_DIR = Path("data/operator-console/source-browser/number-fact-overlays")
OPERATOR_BATCH_DIR = Path("data/operator-console/source-browser/number-fact-review-batches")
RESEARCH_DIR = Path("data/research")
CODEX_OUTPUT_DIR = Path("codex-output")

CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
OPERATIONAL_FILE_MAP_PATH = PROJECT_STATE_DIR / "operational-file-map.yaml"
DOC_STALENESS_SOURCE_OF_TRUTH_PATH = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
STAGE_SUMMARY_RECORDS_PATH = RESEARCH_DIR / "stage-summary-records-v0.yaml"
CHATGPT_CONTEXT_PATH = Path("ChatGPT-ContextFile.md")
DEV_LOG_PATH = Path("docs/development-logs/2026-06-13-stage-5ei-triangle-transposition-diagnostics-transition.md")
RESEARCH_LOG_PATH = Path("research-log/2026-06-13-stage5ei-triangle-transposition-diagnostics-transition-summary.md")
EXPERIMENT_DOC_PATH = Path("docs/experiments/stage-5ei-triangle-transposition-diagnostics-transition.md")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5ei-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5ei-next-stage-decision.yaml",
    "stage5eh_preservation": PROJECT_STATE_DIR / "stage5ei-stage5eh-preservation.yaml",
    "current_mirror_repair": PROJECT_STATE_DIR / "stage5ei-current-mirror-repair.yaml",
    "stale_current_regression": PROJECT_STATE_DIR / "stage5ei-stale-current-regression.yaml",
    "stage6_7_8_9_roadmap": PROJECT_STATE_DIR / "stage5ei-stage6-7-8-9-roadmap.yaml",
    "route_diagnostic_transition": PROJECT_STATE_DIR / "stage5ei-route-diagnostic-transition.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5ei-reviewable-validation-evidence.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR / "stage5ei-source-browser-loadability-summary.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5ei-reviewability-gap-register.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage5ei-chatgpt-context-update-summary.yaml",
    "codex_hook_trust_record": PROJECT_STATE_DIR / "stage5ei-codex-hook-trust-record.yaml",
    "handoff_noncommit_proof": PROJECT_STATE_DIR / "stage5ei-handoff-noncommit-proof.yaml",
}
HISTORICAL_ROUTE_PATHS: dict[str, Path] = {
    "pdd153_geometry_candidates": HISTORICAL_ROUTE_DIR / "stage5ei-pdd153-geometry-candidates.yaml",
    "triangular_transposition_taxonomy": HISTORICAL_ROUTE_DIR
    / "stage5ei-triangular-transposition-taxonomy.yaml",
    "pascal_fibonacci_diagonal_context": HISTORICAL_ROUTE_DIR
    / "stage5ei-pascal-fibonacci-diagonal-context.yaml",
    "bottom_row_page32_quarantine_bridge": HISTORICAL_ROUTE_DIR
    / "stage5ei-bottom-row-page32-quarantine-bridge.yaml",
}
TOKEN_BLOCK_PATHS: dict[str, Path] = {
    "stage5eh_preservation_gate": TOKEN_BLOCK_DIR / "stage5ei-stage5eh-preservation-gate.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage5ei-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage5ei-no-execution-transition-gate.yaml",
    "stage6_probe_readiness_handoff": TOKEN_BLOCK_DIR / "stage5ei-stage6-probe-readiness-handoff.yaml",
    "route_diagnostic_policy": TOKEN_BLOCK_DIR / "stage5ei-route-diagnostic-policy.yaml",
    "triangular_transposition_probe_manifest": TOKEN_BLOCK_DIR
    / "stage5ei-triangular-transposition-probe-manifest.yaml",
}
OPERATOR_PATHS: dict[str, Path] = {
    "overlay_collection": OPERATOR_OVERLAY_DIR / "stage5ei-final-stage5-triangle-transition-overlays.yaml",
    "review_batch_result": OPERATOR_BATCH_DIR / "stage5ei-final-stage5-triangle-transition-result.yaml",
}
DATA_PATHS: dict[str, Path] = {
    **PROJECT_STATE_PATHS,
    **HISTORICAL_ROUTE_PATHS,
    **TOKEN_BLOCK_PATHS,
    **OPERATOR_PATHS,
}

SCHEMA_PATHS: dict[str, Path] = {
    key: Path(f"schemas/project-state/stage5ei-{key.replace('_', '-')}-v0.schema.json")
    for key in PROJECT_STATE_PATHS
}
SCHEMA_PATHS.update(
    {
        key: Path(f"schemas/historical-route/stage5ei-{key.replace('_', '-')}-v0.schema.json")
        for key in HISTORICAL_ROUTE_PATHS
    }
)
SCHEMA_PATHS.update(
    {
        key: Path(f"schemas/token-block/stage5ei-{key.replace('_', '-')}-v0.schema.json")
        for key in TOKEN_BLOCK_PATHS
    }
)
SCHEMA_PATHS.update(
    {
        "overlay_collection": Path(
            "schemas/operator-console/source-browser-stage5ei-number-fact-overlay-v0.schema.json"
        ),
        "review_batch_result": Path(
            "schemas/operator-console/stage5ei-source-browser-number-fact-review-batch-result-v0.schema.json"
        ),
    }
)

FALSE_GUARDRAILS: dict[str, bool] = {
    "historical_source_lock_records_rewritten": False,
    "number_fact_backfill_performed_now": False,
    "source_lock_evidence_updated_now": False,
    "new_source_lock_evidence_added_as_raw_body": False,
    "raw_source_files_committed": False,
    "raw_third_party_files_committed": False,
    "generated_outputs_committed": False,
    "probe_execution_performed_now": False,
    "diagnostic_probe_run_now": False,
    "triangular_transposition_route_stream_generated_now": False,
    "route_extraction_performed_now": False,
    "triangle_route_extraction_performed_now": False,
    "triangular_transposition_readouts_generated_now": False,
    "route_stream_generated_now": False,
    "real_byte_stream_generated": False,
    "variant_byte_streams_generated": False,
    "byte_stream_generation_authorized_now": False,
    "xor_reconstruction_performed_now": False,
    "outguess_execution_performed": False,
    "pgp_verification_performed_now": False,
    "stegdetect_execution_performed_now": False,
    "f5_extraction_performed_now": False,
    "f5_password_search_performed_now": False,
    "stego_tool_execution_performed": False,
    "image_forensics_performed": False,
    "hidden_content_image_forensics_performed": False,
    "ocr_performed": False,
    "pdf_ocr_or_hidden_content_rendering_performed": False,
    "audio_stego_performed": False,
    "spectrogram_stego_performed": False,
    "mp3stego_execution_performed": False,
    "openpuff_execution_performed": False,
    "tor_network_access_performed": False,
    "network_target_validation_performed_now": False,
    "target_priority_decision_created_now": False,
    "operator_target_priority_decision_created_now": False,
    "pivot_target_selected_now": False,
    "target_class_validation_implemented": False,
    "activation_authorized_now": False,
    "activation_decision_valid_now": False,
    "active_ingestion_performed": False,
    "active_manifest_registry_updated": False,
    "active_planning_input_authorized_now": False,
    "active_planning_input_selected_now": False,
    "active_token_block_manifest_changed": False,
    "canonical_corpus_active": False,
    "page_boundaries_finalized": False,
    "page_boundaries_final": False,
    "execution_authorized_now": False,
    "execution_performed": False,
    "community_code_executed_now": False,
    "machine_code_execution_performed_now": False,
    "native_code_execution_performed_now": False,
    "vm_bytecode_execution_performed_now": False,
    "spreadsheet_macro_execution_performed": False,
    "html_tool_executed_now": False,
    "alberti_html_executed_now": False,
    "disk_cipher_execution_performed_now": False,
    "known_plaintext_attack_performed_now": False,
    "decryption_attempt_performed_now": False,
    "decode_attempt_performed": False,
    "scoring_performed": False,
    "cuda_execution_performed": False,
    "benchmark_performed": False,
    "hash_preimage_search_performed": False,
    "dwh_hash_search_performed": False,
    "website_expansion_performed": False,
    "solve_claim": False,
}

CURRENT_MIRROR_PATHS = [
    Path("STATUS.md"),
    Path("ROADMAP.md"),
    Path("README.md"),
    Path("AGENTS.md"),
    CHATGPT_CONTEXT_PATH,
    Path("docs/roadmap/staged-plan.md"),
    Path("docs/onboarding/start-here.md"),
    Path("docs/onboarding/source-of-truth-map.md"),
    Path("docs/onboarding/operational-file-map.md"),
    Path("TESTING.md"),
    Path("docs/reference/token-block-cli.md"),
]

FUTURE_ROUTE_STREAM_FINGERPRINTS = [
    "ic_ioc",
    "doublet_rate",
    "doublet_suppression_profile",
    "lag5_d1_d4_fingerprint",
    "bigram_diagonal_or_copy_signature",
    "ngram_repeat_profile",
    "gp_index_mod29_residue_profile",
    "single_rune_anchor_distribution",
    "way_wynn_word52_geometry_preservation",
    "known_lp_cipher_family_resemblance",
    "typo_variant_and_gp_orthography_normalization_profile",
    "wrong_route_and_shuffled_surface_control_delta",
]

PDD153_ANCHORS = [
    {"position": 25, "row": 7, "column": 4, "d": 4, "role": "single_rune_word", "line_family": "median"},
    {"position": 41, "row": 9, "column": 5, "d": 5, "role": "center_word", "line_family": "median"},
    {"position": 46, "row": 10, "column": 1, "d": 10, "role": "56311_path_member", "line_family": "left_edge"},
    {"position": 52, "row": 10, "column": 7, "d": 4, "role": "56311_path_member_way_anchor"},
    {"position": 53, "row": 10, "column": 8, "d": 3, "role": "single_rune_word_adjacent_to_way"},
    {"position": 55, "row": 10, "column": 10, "d": 1, "role": "56311_path_member", "line_family": "right_edge"},
    {"position": 66, "row": 11, "column": 11, "d": 1, "role": "56311_path_member", "line_family": "right_edge"},
    {"position": 91, "row": 13, "column": 13, "d": 1, "role": "single_rune_word", "line_family": "right_edge"},
    {"position": 106, "row": 15, "column": 1, "d": 15, "role": "single_rune_word", "line_family": "left_edge"},
]
D4_DIAGONAL = [7, 12, 18, 25, 33, 42, 52, 63, 75, 88, 102, 117, 133, 150]

OVERLAY_TOPICS = [
    ("pdd153_t17_center41_geometry", "PDD153 T17 center word 41 and row-major coordinate context"),
    ("pdd153_56311_center_to_row_edge_way_path", "56311 path [41, 46, 52, 55, 66] with WAY anchor at 52"),
    ("pdd153_d4_diagonal_25_52_anchor", "d=4 diagonal includes 25 and 52 as review-only anchors"),
    ("pdd153_single_rune_edge_median_distribution", "Single-rune words cluster on edges and median positions"),
    (
        "pdd153_triangular_transposition_taxonomy_warning_22_vs_24",
        "Operator 22-count taxonomy is recorded beside an assistant-observed 24-family ambiguity",
    ),
    (
        "pdd153_route_diagnostic_no_plaintext_required_policy",
        "Route interest is fingerprint-based and does not require readable English",
    ),
    (
        "pdd153_bottom_row_2465_plus_w_index_2472_quarantine_bridge",
        "Bottom-row 2465 plus W index 7 equals 2472, quarantined for mixed-arithmetic risk",
    ),
]

REQUIRED_SCANNER_PATTERNS = [
    "Stage 5EG doc-staleness guardians is complete",
    "Stage 5EE current boundary",
    "after Stage 5EE",
    "Current next prompt: Stage 5EI - Source-lock number-fact review batch 006, without execution",
    "Next recommended prompt: Stage 5EI - Source-lock number-fact review batch 006, without execution",
]


@dataclass
class ValidationResult:
    errors: list[str]
    counts: dict[str, Any]

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def validation_error_count(self) -> int:
        return len(self.errors)

    def to_cli_text(self) -> str:
        lines = [f"{key}={_format(value)}" for key, value in self.counts.items()]
        lines.append(f"validation_error_count={len(self.errors)}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5ei() -> dict[str, Any]:
    """Build deterministic Stage 5EI records and focused current-truth mirrors."""

    _write_schemas()
    source_browser = _empty_source_browser_record()
    stale_counts = {"stale_current_error_count": 0, "stale_current_warning_count": 0}
    records = _records(source_browser, stale_counts)
    _write_records(records)
    _update_current_stage_state()
    _update_current_mirrors()
    _update_stage_summary_records()
    _update_operational_file_map()
    _update_doc_staleness_source_of_truth()
    source_browser = _source_browser_loadability_record()
    stale_counts = _stale_current_counts()
    records = _records(source_browser, stale_counts)
    _write_records(records)
    _update_docs(records["summary"])
    _write_completion_handoff(records["summary"])
    return records


def validate_stage5ei() -> ValidationResult:
    validators: list[Callable[[], ValidationResult]] = [
        validate_stage5ei_files_and_schemas,
        validate_stage5ei_stage5eh_preservation,
        validate_stage5ei_current_mirror_repair,
        validate_stage5ei_stale_current_scanner_regression,
        validate_stage5ei_triangle_transposition_geometry,
        validate_stage5ei_route_diagnostic_policy,
        validate_stage5ei_stage6_roadmap,
        validate_stage5ei_number_fact_overlays,
        validate_stage5ei_source_browser_loadability,
        validate_stage5ei_gate_closure,
        validate_stage5ei_handoff,
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for validator in validators:
        result = validator()
        errors.extend(result.errors)
        counts.update(result.counts)
    return _result(errors, **counts)


def validate_stage5ei_files_and_schemas() -> ValidationResult:
    errors: list[str] = []
    for path in [*DATA_PATHS.values(), *SCHEMA_PATHS.values(), DEV_LOG_PATH, RESEARCH_LOG_PATH, EXPERIMENT_DOC_PATH]:
        if not path.exists():
            errors.append(f"missing required Stage 5EI file: {path.as_posix()}")
    for key, schema_path in SCHEMA_PATHS.items():
        if not schema_path.exists() or key not in DATA_PATHS:
            continue
        schema = read_yaml(schema_path)
        Draft202012Validator.check_schema(schema)
        payload = read_yaml(DATA_PATHS[key])
        for error in Draft202012Validator(schema).iter_errors(payload):
            errors.append(f"{DATA_PATHS[key].as_posix()}: {error.message}")
    return _result(errors, schema_count=len(SCHEMA_PATHS), data_record_count=len(DATA_PATHS))


def validate_stage5ei_stage5eh_preservation() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["stage5eh_preservation"])
    errors: list[str] = []
    expected = {
        "previous_stage_id": PREVIOUS_STAGE_ID,
        "stage5eh_future_probe_manifest_count": 23,
        "stage5eh_overlay_count": 36,
        "stage5eh_source_browser_validation_error_count": 0,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            errors.append(f"Stage 5EH preservation {key} expected {value!r}, got {record.get(key)!r}")
    return _result(errors, **{key: record.get(key) for key in expected})


def validate_stage5ei_current_mirror_repair() -> ValidationResult:
    state = read_yaml(CURRENT_STAGE_STATE_PATH)
    errors: list[str] = []
    current_pair = (state.get("latest_completed_stage_id"), state.get("recommended_next_stage_id"))
    later_stage_pairs = {
        ("stage-6", "stage-6b"): Path("data/project-state/stage6-summary.yaml"),
    }
    if current_pair not in later_stage_pairs or not later_stage_pairs[current_pair].exists():
        if state.get("latest_completed_stage", {}).get("stage_id") != STAGE_ID:
            errors.append("current-stage-state latest completed stage is not stage-5ei")
        if state.get("next_stage", {}).get("stage_id") != NEXT_STAGE_ID:
            errors.append("current-stage-state next stage is not stage-6")
    for path in CURRENT_MIRROR_PATHS:
        if not path.exists():
            errors.append(f"missing current mirror: {path.as_posix()}")
            continue
    stale_counts = _stale_current_counts()
    if stale_counts["stale_current_error_count"] != 0:
        errors.append(f"strict stale-current scanner has {stale_counts['stale_current_error_count']} errors")
    return _result(
        errors,
        current_mirror_count=len(CURRENT_MIRROR_PATHS),
        stale_current_claim_strict_errors_after_stage5ei=stale_counts["stale_current_error_count"],
    )


def validate_stage5ei_stale_current_scanner_regression() -> ValidationResult:
    errors: list[str] = []
    for pattern in REQUIRED_SCANNER_PATTERNS:
        findings = scan_text(pattern, "STATUS.md", parse_stage_id(STAGE_ID), parse_stage_id(NEXT_STAGE_ID))
        if not findings:
            errors.append(f"scanner did not flag stale-current regression pattern: {pattern}")
    historical = scan_text(
        "At the time of Stage 5EG, Stage 5EG was complete and Stage 5EH was next.",
        "research-log/example.md",
        parse_stage_id(STAGE_ID),
        parse_stage_id(NEXT_STAGE_ID),
    )
    if historical:
        errors.append("scanner flagged explicit historical wording")
    start_here = Path("docs/onboarding/start-here.md")
    if start_here.exists():
        findings = audit_repository().to_dict()
        if findings.get("stale_current_error_count", 0) != 0:
            errors.append("repository stale-current audit still has strict errors after start-here repair")
    return _result(errors, regression_patterns=len(REQUIRED_SCANNER_PATTERNS))


def validate_stage5ei_triangle_transposition_geometry() -> ValidationResult:
    record = read_yaml(HISTORICAL_ROUTE_PATHS["pdd153_geometry_candidates"])
    errors: list[str] = []
    if record.get("position_formula") != "position n = T(r-1) + c":
        errors.append("PDD153 row-major position formula is missing")
    if record.get("diagonal_formula") != "d = r - c + 1":
        errors.append("PDD153 diagonal formula is missing")
    anchors = {item["position"]: item for item in record.get("anchor_coordinates", [])}
    for position, row, column, d_value in [
        (25, 7, 4, 4),
        (41, 9, 5, 5),
        (46, 10, 1, 10),
        (52, 10, 7, 4),
        (53, 10, 8, 3),
        (55, 10, 10, 1),
        (66, 11, 11, 1),
        (91, 13, 13, 1),
        (106, 15, 1, 15),
    ]:
        anchor = anchors.get(position)
        if anchor is None or (anchor.get("row"), anchor.get("column"), anchor.get("d")) != (row, column, d_value):
            errors.append(f"anchor {position} does not match expected T17 coordinate")
    if record.get("path_56311_positions") != [41, 46, 52, 55, 66]:
        errors.append("56311 path positions are not recorded exactly")
    if record.get("path_56311_cumulative_offsets") != [5, 11, 14, 25]:
        errors.append("56311 cumulative offsets are not recorded exactly")
    if record.get("d4_diagonal_positions") != D4_DIAGONAL:
        errors.append("d=4 diagonal positions are not recorded exactly")
    taxonomy = read_yaml(HISTORICAL_ROUTE_PATHS["triangular_transposition_taxonomy"])
    if taxonomy.get("operator_supplied_claim_22_distinct_triangular_transpositions") is not True:
        errors.append("operator 22-count triangular transposition claim is not recorded")
    if taxonomy.get("natural_triangular_readout_family_count_observed_by_assistant") != 24:
        errors.append("assistant-observed 24-family count is not recorded")
    return _result(errors, anchor_count=len(record.get("anchor_coordinates", [])))


def validate_stage5ei_route_diagnostic_policy() -> ValidationResult:
    record = read_yaml(TOKEN_BLOCK_PATHS["route_diagnostic_policy"])
    errors: list[str] = []
    if record.get("plaintext_likeness_required_for_route_interest") is not False:
        errors.append("route-diagnostic policy still gates route interest on plaintext-likeness")
    if record.get("english_readability_required_for_route_interest") is not False:
        errors.append("route-diagnostic policy still gates route interest on English readability")
    for key in [
        "high_entropy_output_can_be_interesting",
        "ciphertext_like_output_can_be_interesting",
        "key_like_output_can_be_interesting",
        "control_stream_like_output_can_be_interesting",
        "byte_like_output_can_be_interesting",
        "null_copy_mask_like_output_can_be_interesting",
        "intermediate_surface_output_can_be_interesting",
    ]:
        if record.get(key) is not True:
            errors.append(f"route-diagnostic policy missing true field {key}")
    if record.get("future_route_stream_fingerprints") != FUTURE_ROUTE_STREAM_FINGERPRINTS:
        errors.append("future route stream fingerprints differ from Stage 5EI policy")
    pascal = read_yaml(HISTORICAL_ROUTE_PATHS["pascal_fibonacci_diagonal_context"])
    if pascal.get("pdd153_diagonal_relation_accepted_as_method_now") is not False:
        errors.append("PDD153 diagonal relation was accepted as method now")
    return _result(errors, fingerprint_count=len(record.get("future_route_stream_fingerprints", [])))


def validate_stage5ei_stage6_roadmap() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["stage6_7_8_9_roadmap"])
    errors: list[str] = []
    plans = record.get("stage_roadmap", {})
    if plans.get("stage6_plan", {}).get("execution_allowed") is not False:
        errors.append("Stage 6 roadmap does not keep execution disabled")
    if plans.get("stage7_plan", {}).get("execution_allowed") != "bounded_diagnostics_only_after_stage6":
        errors.append("Stage 7 roadmap does not require Stage 6 first")
    if plans.get("stage8_plan", {}).get("execution_allowed") is not False:
        errors.append("Stage 8 roadmap does not keep execution disabled")
    if plans.get("stage9_plan", {}).get("execution_allowed") != "bounded_experiments_only_after_stage8":
        errors.append("Stage 9 roadmap does not require Stage 8 first")
    if record.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("Stage 5EI roadmap does not route to Stage 6")
    return _result(errors, roadmap_stage_count=len(plans))


def validate_stage5ei_number_fact_overlays() -> ValidationResult:
    record = read_yaml(OPERATOR_PATHS["overlay_collection"])
    errors: list[str] = []
    overlays = record.get("number_fact_overlays", [])
    topics = {overlay.get("overlay_topic") for overlay in overlays}
    for topic, _label in OVERLAY_TOPICS:
        if topic not in topics:
            errors.append(f"missing Stage 5EI overlay topic: {topic}")
    for overlay in overlays:
        if overlay.get("review_state") != "overlay_enriched_fact":
            errors.append(f"{overlay.get('overlay_id')} is not overlay_enriched_fact")
        if overlay.get("usable_for_decision_now") is not False:
            errors.append(f"{overlay.get('overlay_id')} is usable for decision now")
        if overlay.get("not_allowed_as") != ["proof", "route_seed", "execution_seed", "solve_claim"]:
            errors.append(f"{overlay.get('overlay_id')} has incorrect not_allowed_as")
    return _result(errors, overlay_count=len(overlays))


def validate_stage5ei_source_browser_loadability() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    errors: list[str] = []
    if record.get("source_browser_validation_error_count") != 0:
        errors.append("Source Browser validation errors are present after Stage 5EI")
    if record.get("source_browser_loadability_preserved") is not True:
        errors.append("Source Browser loadability is not preserved")
    return _result(
        errors,
        source_browser_entries_loaded=record.get("source_browser_entries_loaded"),
        source_browser_validation_error_count=record.get("source_browser_validation_error_count"),
    )


def validate_stage5ei_gate_closure() -> ValidationResult:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        payload = read_yaml(path)
        for field, expected in FALSE_GUARDRAILS.items():
            if payload.get(field) != expected:
                errors.append(f"{path.as_posix()} has {field}={payload.get(field)!r}, expected {expected!r}")
        if payload.get("selected_next_solve_target_id") is not None:
            errors.append(f"{path.as_posix()} selected a next solve target")
    return _result(errors, guardrail_record_count=len(DATA_PATHS))


def validate_stage5ei_handoff() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["handoff_noncommit_proof"])
    errors: list[str] = []
    if record.get("completion_summary_path") != "codex-output/stage5ei-codex-completion.md":
        errors.append("Stage 5EI handoff path is not codex-output/stage5ei-codex-completion.md")
    if record.get("completion_summary_committed") is not False:
        errors.append("Stage 5EI handoff is marked committed")
    if record.get("codex_output_root_ignored") is not True:
        errors.append("Stage 5EI handoff does not preserve codex-output ignore policy")
    return _result(errors, handoff_path=record.get("completion_summary_path"))


def stage5ei_summary_text() -> str:
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5EI summary:",
        f"status={summary.get('status')}",
        f"stage_id={summary.get('stage_id')}",
        f"previous_stage_id={summary.get('previous_stage_id')}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
        f"operator_superseded_number_fact_review_batch_006_now="
        f"{summary.get('operator_superseded_number_fact_review_batch_006_now')}",
        f"stage5eh_future_probe_manifest_count={summary.get('stage5eh_future_probe_manifest_count')}",
        f"stage5eh_overlay_count={summary.get('stage5eh_overlay_count')}",
        f"overlay_count={summary.get('overlay_count')}",
        f"triangle_geometry_record_count={summary.get('triangle_geometry_record_count')}",
        f"route_fingerprint_count={summary.get('route_fingerprint_count')}",
        f"source_browser_validation_error_count={summary.get('source_browser_validation_error_count')}",
        f"stale_current_claim_strict_errors_after_stage5ei="
        f"{summary.get('stale_current_claim_strict_errors_after_stage5ei')}",
        f"project_codex_hooks_operator_trusted_locally="
        f"{summary.get('project_codex_hooks_operator_trusted_locally')}",
        f"active_hooks_effective_now={summary.get('active_hooks_effective_now')}",
        f"full_serial_pytest_run={summary.get('full_serial_pytest_run')}",
    ]
    return "\n".join(lines)


def _records(source_browser: dict[str, Any], stale_counts: dict[str, int]) -> dict[str, Any]:
    stage5eh_summary = _safe_read(PROJECT_STATE_DIR / "stage5eh-summary.yaml")
    stage5eh_probe_count = int(stage5eh_summary.get("future_probe_manifest_count", 23))
    stage5eh_overlay_count = int(stage5eh_summary.get("overlay_count", 36))
    stage5eh_source_browser_errors = int(stage5eh_summary.get("source_browser_validation_error_count", 0))
    overlay_records = _overlay_records()
    geometry = _pdd153_geometry_record()
    route_policy = _route_diagnostic_policy_record()
    summary = {
        **_base_record("stage5ei_summary", SCHEMA_PATHS["summary"]),
        "status": "complete",
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "previous_stage_id": PREVIOUS_STAGE_ID,
        "previous_stage_title": PREVIOUS_STAGE_TITLE,
        "previous_stage_primary_commit": PREVIOUS_STAGE_PRIMARY_COMMIT,
        "previous_stage_final_commit": PREVIOUS_STAGE_FINAL_COMMIT,
        "previous_stage_issue": PREVIOUS_STAGE_ISSUE,
        "previous_stage_ci_run": PREVIOUS_STAGE_CI_RUN,
        "previous_stage_ci_status": PREVIOUS_STAGE_CI_STATUS,
        "stage5eh_recommended_stage5ei_number_fact_review_batch_006": True,
        "operator_superseded_number_fact_review_batch_006_now": True,
        "number_fact_review_batch_006_performed_now": False,
        "normal_source_lock_enrichment_paused_now": True,
        "stage5ei_final_stage5_transition_stage": True,
        "stage5_source_lock_enrichment_phase_closed_now": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "stage5eh_future_probe_manifest_count": stage5eh_probe_count,
        "stage5eh_overlay_count": stage5eh_overlay_count,
        "stage5eh_source_browser_validation_error_count": stage5eh_source_browser_errors,
        "triangle_geometry_record_count": len(geometry["candidate_records"]),
        "route_fingerprint_count": len(FUTURE_ROUTE_STREAM_FINGERPRINTS),
        "overlay_count": len(overlay_records),
        "source_browser_entries_loaded": source_browser["source_browser_entries_loaded"],
        "source_browser_records_scanned": source_browser["source_browser_records_scanned"],
        "source_browser_validation_error_count": source_browser["source_browser_validation_error_count"],
        "stale_current_claim_strict_errors_after_stage5ei": stale_counts["stale_current_error_count"],
        "stale_current_claim_warning_count_after_stage5ei": stale_counts["stale_current_warning_count"],
        "current_stage_state_authoritative": True,
        "current_mirror_drift_repaired_now": True,
        "broad_doc_churn_avoided": True,
        "project_codex_hooks_declared": True,
        "project_codex_hooks_operator_visible": True,
        "project_codex_hooks_operator_trusted_locally": True,
        "active_hooks_effective_now": True,
        "operator_hook_trust_source": "local_codex_trust_state_or_explicit_operator_action",
        "blocking_hooks_effective_now": False,
        "hook_execution_relies_on_deterministic_scanner": True,
        "custom_agents_invoked_by_hooks": False,
        "full_parallel_workers": 10,
        "full_parallel_pytest_workers": 10,
        "full_serial_pytest_run": False,
    }
    records = {
        "summary": summary,
        "next_stage_decision": {
            **_base_record("stage5ei_next_stage_decision", SCHEMA_PATHS["next_stage_decision"]),
            "previous_routed_stage_id": "stage-5ei",
            "previous_routed_stage_title": "Stage 5EI - Source-lock number-fact review batch 006, without execution",
            "operator_superseded_number_fact_review_batch_006_now": True,
            "number_fact_review_batch_006_performed_now": False,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": "codex_plan_mode_probe_diagnostic_readiness",
        },
        "stage5eh_preservation": {
            **_base_record("stage5ei_stage5eh_preservation", SCHEMA_PATHS["stage5eh_preservation"]),
            "previous_stage_id": PREVIOUS_STAGE_ID,
            "previous_stage_final_commit": PREVIOUS_STAGE_FINAL_COMMIT,
            "stage5eh_future_probe_manifest_count": stage5eh_probe_count,
            "stage5eh_overlay_count": stage5eh_overlay_count,
            "stage5eh_source_browser_validation_error_count": stage5eh_source_browser_errors,
            "stage5eh_records_rewritten_now": False,
            "stage5eh_source_lock_evidence_changed_now": False,
        },
        "current_mirror_repair": {
            **_base_record("stage5ei_current_mirror_repair", SCHEMA_PATHS["current_mirror_repair"]),
            "current_mirror_paths": [path.as_posix() for path in CURRENT_MIRROR_PATHS],
            "current_stage_state_authoritative": True,
            "current_mirror_drift_repaired_now": True,
            "broad_doc_churn_avoided": True,
            "stale_current_claim_strict_errors_after_stage5ei": stale_counts["stale_current_error_count"],
        },
        "stale_current_regression": {
            **_base_record("stage5ei_stale_current_regression", SCHEMA_PATHS["stale_current_regression"]),
            "regression_patterns": REQUIRED_SCANNER_PATTERNS,
            "known_stage5eh_drift_class_covered": True,
            "stale_current_claim_strict_errors_after_stage5ei": stale_counts["stale_current_error_count"],
        },
        "stage6_7_8_9_roadmap": _stage6_roadmap_record(),
        "route_diagnostic_transition": {
            **_base_record("stage5ei_route_diagnostic_transition", SCHEMA_PATHS["route_diagnostic_transition"]),
            "route_diagnostic_policy_id": "stage5ei_fingerprint_based_route_diagnostic_policy",
            "stage6_probe_readiness_transition_prepared": True,
            "stage7_execution_deferred_until_after_stage6": True,
            "stage8_triangle_readiness_deferred": True,
            "stage9_triangle_experiments_deferred": True,
            **_route_policy_fields(),
        },
        "reviewable_validation_evidence": {
            **_base_record("stage5ei_reviewable_validation_evidence", SCHEMA_PATHS["reviewable_validation_evidence"]),
            "required_validation_commands": [
                "token-block validate-stage5eh",
                "token-block build-stage5ei",
                "token-block validate-stage5ei",
                "consistency audit-stale-current-claims --strict",
                "operator-console source-browser validate-index",
                "scripts/ci/run-stage-validation.ps1 -Stage stage5ei -Profile stage-fast",
                "scripts/ci/run-stage-validation.ps1 -Stage stage5ei -Profile local-fast",
                "scripts/ci/run-stage-validation.ps1 -Stage stage5ei -Profile full-parallel -Workers 10 -PytestWorkers 10",
            ],
            "full_parallel_workers": 10,
            "full_parallel_pytest_workers": 10,
            "full_serial_pytest_required": False,
        },
        "source_browser_loadability_summary": {
            **_base_record("stage5ei_source_browser_loadability_summary", SCHEMA_PATHS["source_browser_loadability_summary"]),
            **source_browser,
        },
        "reviewability_gap_register": {
            **_base_record("stage5ei_reviewability_gap_register", SCHEMA_PATHS["reviewability_gap_register"]),
            "reviewability_gaps": [
                {
                    "gap_id": "stage5ei-triangular-transposition-taxonomy-22-vs-24",
                    "gap_type": "taxonomy_resolution_deferred",
                    "blocked_until": "stage6_or_stage7_probe_readiness",
                },
                {
                    "gap_id": "stage5ei-bottom-row-2472-quarantine-bridge",
                    "gap_type": "mixed_arithmetic_and_selection_bias_warning",
                    "blocked_until": "future_route_family_null_controls",
                },
            ],
            "reviewability_gap_count": 2,
        },
        "chatgpt_context_update_summary": {
            **_base_record("stage5ei_chatgpt_context_update_summary", SCHEMA_PATHS["chatgpt_context_update_summary"]),
            "chatgpt_context_path": CHATGPT_CONTEXT_PATH.as_posix(),
            "current_stage_context_mentions_stage5ei": True,
            "stage6_next_route_recorded": True,
            "hook_trust_recorded_truthfully": True,
        },
        "codex_hook_trust_record": {
            **_base_record("stage5ei_codex_hook_trust_record", SCHEMA_PATHS["codex_hook_trust_record"]),
            "project_codex_hooks_declared": True,
            "project_codex_hooks_operator_visible": True,
            "project_codex_hooks_operator_trusted_locally": True,
            "active_hooks_effective_now": True,
            "operator_hook_trust_source": "local_codex_trust_state_or_explicit_operator_action",
            "blocking_hooks_effective_now": False,
            "hook_execution_relies_on_deterministic_scanner": True,
            "custom_agents_invoked_by_hooks": False,
        },
        "handoff_noncommit_proof": {
            **_base_record("stage5ei_handoff_noncommit_proof", SCHEMA_PATHS["handoff_noncommit_proof"]),
            "completion_summary_path": "codex-output/stage5ei-codex-completion.md",
            "completion_summary_committed": False,
            "codex_output_root_ignored": True,
            "generated_reports_committed": False,
            "raw_or_generated_paths_staged": False,
        },
        "pdd153_geometry_candidates": geometry,
        "triangular_transposition_taxonomy": _triangular_transposition_record(),
        "pascal_fibonacci_diagonal_context": _pascal_fibonacci_record(),
        "bottom_row_page32_quarantine_bridge": _bottom_row_bridge_record(),
        "stage5eh_preservation_gate": _token_gate_record("stage5ei_stage5eh_preservation_gate"),
        "no_byte_stream_transition_gate": _token_gate_record("stage5ei_no_byte_stream_transition_gate"),
        "no_execution_transition_gate": _token_gate_record("stage5ei_no_execution_transition_gate"),
        "stage6_probe_readiness_handoff": _stage6_handoff_record(),
        "route_diagnostic_policy": route_policy,
        "triangular_transposition_probe_manifest": _triangular_probe_manifest_record(),
        "overlay_collection": _overlay_collection_record(overlay_records),
        "review_batch_result": _review_batch_result_record(overlay_records, source_browser),
    }
    return records


def _base_record(record_type: str, schema_path: Path) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": schema_path.as_posix(),
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "status": "complete",
        "metadata_only": True,
        "reviewability_stage": True,
        "source_lock_only": False,
        "number_fact_review_batch_stage": False,
        "puzzle_execution_allowed": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "selected_next_solve_target_id": None,
        **FALSE_GUARDRAILS,
    }


def _pdd153_geometry_record() -> dict[str, Any]:
    return {
        **_base_record("stage5ei_pdd153_geometry_candidates", SCHEMA_PATHS["pdd153_geometry_candidates"]),
        "record_id": "pdd153_t17_geometry_candidate_set_v0",
        "position_formula": "position n = T(r-1) + c",
        "diagonal_formula": "d = r - c + 1",
        "triangle_size": 17,
        "pdd_value": 153,
        "anchor_coordinates": PDD153_ANCHORS,
        "path_56311_positions": [41, 46, 52, 55, 66],
        "path_56311_cumulative_offsets": [5, 11, 14, 25],
        "path_56311_label": "center-to-row-edge WAY path candidate",
        "d4_diagonal_positions": D4_DIAGONAL,
        "row10_way_anchor_position": 52,
        "row10_way_adjacent_single_rune_position": 53,
        "edge_median_distribution": {
            "left_edge_positions": [46, 106],
            "right_edge_positions": [55, 66, 91],
            "median_positions": [25, 41],
            "interior_way_adjacency_positions": [52, 53],
        },
        "candidate_records": [
            "pdd153_56311_row_edge_geometry_candidate_v0",
            "pdd153_word52_d4_diagonal_anchor_candidate_v0",
            "pdd153_single_rune_edge_median_distribution_candidate_v0",
            "pdd153_triangular_transposition_probe_manifest_v0",
            "pdd153_t17_bottom_row_2465_plus_w_index_2472_bridge_candidate_v0",
        ],
        "review_only": True,
        "not_route_evidence_now": True,
        "not_target_priority_evidence_alone": True,
    }


def _triangular_transposition_record() -> dict[str, Any]:
    return {
        **_base_record(
            "stage5ei_triangular_transposition_taxonomy", SCHEMA_PATHS["triangular_transposition_taxonomy"]
        ),
        "triangular_transposition_cipher_context_recorded": True,
        "operator_supplied_claim_22_distinct_triangular_transpositions": True,
        "claim_22_distinct_transpositions_verified_now": False,
        "natural_triangular_readout_family_count_observed_by_assistant": 24,
        "transposition_count_taxonomy_ambiguous": True,
        "transposition_taxonomy_resolution_deferred_to_stage6_or_stage7": True,
        "triangular_transposition_probe_run_now": False,
        "route_stream_generated_now": False,
        "plaintext_required_for_success_now": False,
        "taxonomy_explanation": (
            "The exact count of distinct triangular transpositions depends on how reversals, vertex choices, "
            "diagonal families, row/column/edge reads, and boustrophedon variants are deduplicated. Stage 5EI "
            "records the operator-provided 22-count claim as a candidate taxonomy, but does not treat 22 as "
            "verified. A later probe-readiness stage should define the finite readout set explicitly before any "
            "route stream is generated."
        ),
        "future_probe_manifest_id": "pdd153_triangular_transposition_probe_manifest_v0",
    }


def _pascal_fibonacci_record() -> dict[str, Any]:
    return {
        **_base_record(
            "stage5ei_pascal_fibonacci_diagonal_context",
            SCHEMA_PATHS["pascal_fibonacci_diagonal_context"],
        ),
        "pascal_fibonacci_triangle_context_recorded": True,
        "operator_observed_direct_above_vs_diagonal_sum_difference": True,
        "pdd153_diagonal_sum_or_diagonal_relation_candidate": True,
        "pdd153_diagonal_relation_accepted_as_method_now": False,
        "pdd153_diagonal_route_probe_run_now": False,
        "crosslinks": [
            "pdd153_d4_diagonal_anchor_candidate",
            "pdd153_word52_way_anchor",
            "page32_moebius_fibonacci_prime_index_spiral_v1",
            "lag5_d1_d4_fourth_order_correlation_candidate_v0",
        ],
        "not_summation_rule_now": True,
        "not_route_evidence_now": True,
    }


def _bottom_row_bridge_record() -> dict[str, Any]:
    return {
        **_base_record(
            "stage5ei_bottom_row_page32_quarantine_bridge",
            SCHEMA_PATHS["bottom_row_page32_quarantine_bridge"],
        ),
        "pdd153_bottom_row_sum": 2465,
        "pdd153_bottom_row_range": [137, 153],
        "pdd153_bottom_row_sum_factorization_or_relation": "85 * 29",
        "wynn_w_zero_based_index": 7,
        "page32_bridge_value": 2472,
        "expression": "2465 + 7 = 2472",
        "quarantine_bridge": True,
        "mixed_position_and_gp_index_arithmetic_warning": True,
        "selection_bias_warning": True,
        "not_route_evidence_now": True,
        "not_target_priority_evidence_alone": True,
        "usable_for_decision_now": False,
    }


def _route_policy_fields() -> dict[str, Any]:
    return {
        "plaintext_likeness_required_for_route_interest": False,
        "english_readability_required_for_route_interest": False,
        "high_entropy_output_can_be_interesting": True,
        "ciphertext_like_output_can_be_interesting": True,
        "key_like_output_can_be_interesting": True,
        "control_stream_like_output_can_be_interesting": True,
        "byte_like_output_can_be_interesting": True,
        "null_copy_mask_like_output_can_be_interesting": True,
        "intermediate_surface_output_can_be_interesting": True,
        "intentional_typo_and_orthography_noise_warning": True,
        "gp_orthography_normalization_required_before_language_judgment": True,
        "future_route_stream_fingerprints": FUTURE_ROUTE_STREAM_FINGERPRINTS,
        "warning": (
            "A route readout can be correct but still appear random if it is ciphertext, key material, a control "
            "stream, a null/copy mask, byte-like payload, or an intermediate signed/staged surface. Stage 5EI "
            "does not define success as readable English."
        ),
    }


def _route_diagnostic_policy_record() -> dict[str, Any]:
    return {
        **_base_record("stage5ei_route_diagnostic_policy", SCHEMA_PATHS["route_diagnostic_policy"]),
        "policy_id": "stage5ei_fingerprint_based_route_diagnostic_policy",
        **_route_policy_fields(),
    }


def _stage6_roadmap_record() -> dict[str, Any]:
    return {
        **_base_record("stage5ei_stage6_7_8_9_roadmap", SCHEMA_PATHS["stage6_7_8_9_roadmap"]),
        "stage_roadmap": {
            "stage6_plan": {
                "stage_id": "stage-6",
                "role": "probe_diagnostic_readiness",
                "execution_allowed": False,
            },
            "stage7_plan": {
                "stage_id": "stage-7",
                "role": "actual_probes_and_diagnostics_with_results_source_locked",
                "execution_allowed": "bounded_diagnostics_only_after_stage6",
            },
            "stage8_plan": {
                "stage_id": "stage-8",
                "role": "triangle_specific_experiment_readiness",
                "execution_allowed": False,
            },
            "stage9_plan": {
                "stage_id": "stage-9",
                "role": "triangle_experiments",
                "execution_allowed": "bounded_experiments_only_after_stage8",
            },
        },
        "stage5ei_does_not_implement_stage6": True,
    }


def _token_gate_record(record_type: str) -> dict[str, Any]:
    key = record_type.replace("stage5ei_", "")
    return {
        **_base_record(record_type, SCHEMA_PATHS[key]),
        "gate_state": "closed",
        "stage5eh_preserved": True,
        "batch_006_superseded": True,
        "next_stage": NEXT_STAGE_ID,
    }


def _stage6_handoff_record() -> dict[str, Any]:
    return {
        **_base_record("stage5ei_stage6_probe_readiness_handoff", SCHEMA_PATHS["stage6_probe_readiness_handoff"]),
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "stage6_probe_execution_allowed": False,
        "stage6_expected_role": "probe_diagnostic_readiness",
        "stage6_must_define_probe_finite_sets_before_execution": True,
    }


def _triangular_probe_manifest_record() -> dict[str, Any]:
    return {
        **_base_record(
            "stage5ei_triangular_transposition_probe_manifest",
            SCHEMA_PATHS["triangular_transposition_probe_manifest"],
        ),
        "manifest_id": "pdd153_triangular_transposition_probe_manifest_v0",
        "probe_family": "triangular_transposition_readout_taxonomy",
        "run_now": False,
        "route_stream_generated_now": False,
        "finite_readout_set_required_before_run": True,
        "taxonomy_resolution_required_before_run": True,
    }


def _overlay_records() -> list[dict[str, Any]]:
    overlays: list[dict[str, Any]] = []
    for index, (topic, label) in enumerate(OVERLAY_TOPICS, start=1):
        overlays.append(
            {
                "overlay_id": f"stage5ei_overlay_{index:02d}_{topic}",
                "overlay_topic": topic,
                "title": label,
                "review_state": "overlay_enriched_fact",
                "usable_for_decision_now": False,
                "not_allowed_as": ["proof", "route_seed", "execution_seed", "solve_claim"],
                "record_source": "stage5ei_final_stage5_triangle_transition",
                "stage_id": STAGE_ID,
                "fact_class": "stage5ei_triangle_transition_review_fact",
            }
        )
    return overlays


def _overlay_collection_record(overlays: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        **_base_record(
            "stage5ei_source_browser_number_fact_enrichment_overlay_collection",
            SCHEMA_PATHS["overlay_collection"],
        ),
        "review_batch_id": "stage5ei_final_stage5_triangle_transition",
        "number_fact_overlays": overlays,
        "overlays": overlays,
        "overlay_count": len(overlays),
        "overlay_only": True,
    }


def _review_batch_result_record(overlays: list[dict[str, Any]], source_browser: dict[str, Any]) -> dict[str, Any]:
    return {
        **_base_record(
            "stage5ei_source_browser_number_fact_review_batch_result",
            SCHEMA_PATHS["review_batch_result"],
        ),
        "review_batch_id": "stage5ei_final_stage5_triangle_transition",
        "review_batch_performed_now": False,
        "ordinary_number_fact_batch_006_superseded": True,
        "overlay_count": len(overlays),
        "source_browser_entries_loaded_after_stage5ei": source_browser["source_browser_entries_loaded"],
        "source_browser_validation_error_count_after_stage5ei": source_browser["source_browser_validation_error_count"],
    }


def _write_records(records: dict[str, Any]) -> None:
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        write_json(path, _schema_for(key, path))
    _extend_current_stage_state_schema()
    _extend_doc_staleness_schema()


def _schema_for(key: str, path: Path) -> dict[str, Any]:
    required = [
        "record_type",
        "schema",
        "stage_id",
        "status",
        "metadata_only",
        "recommended_next_stage_id",
        "generated_outputs_committed",
        "execution_performed",
        "cuda_execution_performed",
        "canonical_corpus_active",
        "page_boundaries_finalized",
        "solve_claim",
    ]
    properties: dict[str, Any] = {
        "record_type": {"type": "string"},
        "schema": {"const": path.as_posix()},
        "stage_id": {"const": STAGE_ID},
        "status": {"const": "complete"},
        "metadata_only": {"const": True},
        "recommended_next_stage_id": {"const": NEXT_STAGE_ID},
        "selected_next_solve_target_id": {"const": None},
        **{field: {"const": expected} for field, expected in FALSE_GUARDRAILS.items()},
    }
    if key == "summary":
        required.extend(
            [
                "operator_superseded_number_fact_review_batch_006_now",
                "stage5ei_final_stage5_transition_stage",
                "stage5eh_future_probe_manifest_count",
                "stage5eh_overlay_count",
                "overlay_count",
                "route_fingerprint_count",
                "stale_current_claim_strict_errors_after_stage5ei",
                "project_codex_hooks_operator_trusted_locally",
                "active_hooks_effective_now",
            ]
        )
        properties.update(
            {
                "operator_superseded_number_fact_review_batch_006_now": {"const": True},
                "stage5ei_final_stage5_transition_stage": {"const": True},
                "stage5eh_future_probe_manifest_count": {"const": 23},
                "stage5eh_overlay_count": {"const": 36},
                "stale_current_claim_strict_errors_after_stage5ei": {"const": 0},
                "project_codex_hooks_operator_trusted_locally": {"const": True},
                "active_hooks_effective_now": {"const": True},
            }
        )
    if key == "pdd153_geometry_candidates":
        required.extend(["position_formula", "diagonal_formula", "anchor_coordinates", "d4_diagonal_positions"])
    if key == "route_diagnostic_policy":
        required.extend(["future_route_stream_fingerprints", "plaintext_likeness_required_for_route_interest"])
    if key == "overlay_collection":
        required.extend(["number_fact_overlays", "overlay_count", "overlay_only"])
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": path.as_posix(),
        "type": "object",
        "required": required,
        "properties": properties,
        "additionalProperties": True,
    }


def _source_browser_loadability_record() -> dict[str, Any]:
    index = build_source_index()
    validation = validate_source_index()
    return {
        "source_browser_entries_loaded": len(index.entries),
        "source_browser_records_scanned": len(index.scanned_paths),
        "source_browser_validation_error_count": len(validation.errors),
        "source_browser_warning_count": len(validation.warnings),
        "source_browser_loadability_preserved": len(validation.errors) == 0,
    }


def _empty_source_browser_record() -> dict[str, Any]:
    return {
        "source_browser_entries_loaded": 0,
        "source_browser_records_scanned": 0,
        "source_browser_validation_error_count": 0,
        "source_browser_warning_count": 0,
        "source_browser_loadability_preserved": True,
    }


def _stale_current_counts() -> dict[str, int]:
    report = audit_repository().to_dict()
    return {
        "stale_current_error_count": int(report.get("stale_current_error_count", 0)),
        "stale_current_warning_count": int(report.get("stale_current_warning_count", 0)),
    }


def _update_current_stage_state() -> None:
    payload = _safe_read(CURRENT_STAGE_STATE_PATH)
    closed_guardrails = {
        "historical_source_lock_records_rewritten": False,
        "number_fact_backfill_performed_now": False,
        "number_fact_enrichment_overlays_added_now": False,
        "number_fact_review_batch_006_performed_now": False,
        "new_source_lock_evidence_added_now": False,
        "source_lock_evidence_updated_now": False,
        "source_lock_records_created_now": False,
        "lag5_source_lock_performed_now": False,
        "target_priority_decision_created_now": False,
        "pivot_target_selected_now": False,
        "route_extraction_performed_now": False,
        "triangle_route_extraction_performed_now": False,
        "route_stream_generated_now": False,
        "real_byte_stream_generated": False,
        "variant_byte_streams_generated": False,
        "byte_stream_generation_authorized_now": False,
        "decode_attempt_performed": False,
        "decryption_attempt_performed_now": False,
        "scoring_performed": False,
        "cuda_execution_performed": False,
        "benchmark_performed": False,
        "image_forensics_performed": False,
        "hidden_content_image_forensics_performed": False,
        "ocr_performed": False,
        "audio_stego_performed": False,
        "spectrogram_stego_performed": False,
        "outguess_execution_performed": False,
        "pgp_verification_performed_now": False,
        "stegdetect_execution_performed_now": False,
        "f5_extraction_performed_now": False,
        "f5_password_search_performed_now": False,
        "tor_network_access_performed": False,
        "target_class_validation_implemented": False,
        "canonical_corpus_active": False,
        "page_boundaries_finalized": False,
        "page_boundaries_final": False,
        "solve_claim": False,
        "execution_performed": False,
        "execution_authorized_now": False,
    }
    payload.update(
        {
            **closed_guardrails,
            "schema": "schemas/project-state/current-stage-state-v0.schema.json",
            "record_type": "current_stage_state",
            "stage_id": STAGE_ID,
            "stage_title": STAGE_TITLE,
            "prompt_type": PROMPT_TYPE,
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": "codex_plan_mode_probe_diagnostic_readiness",
            "latest_completed_stage": {
                "stage_id": STAGE_ID,
                "stage_title": STAGE_TITLE,
                "completed_commit": "",
                "completed_date": "2026-06-13",
                "status": "complete",
            },
            "next_stage": {
                "stage_id": NEXT_STAGE_ID,
                "stage_title": NEXT_STAGE_TITLE,
                "prompt_type": "codex_plan_mode_probe_diagnostic_readiness",
            },
            "post_push_handoff_locations": [
                "codex-output/stage5ei-codex-completion.md",
                "GitHub issue comment",
            ],
            "current_stage_authority": "data/project-state/current-stage-state.yaml",
            "current_truth_policy": "current-stage-state.yaml is authoritative; Markdown docs are mirrors or historical evidence.",
            "stage5eh_recommended_stage5ei_number_fact_review_batch_006": True,
            "operator_superseded_number_fact_review_batch_006_now": True,
            "normal_source_lock_enrichment_paused_now": True,
            "stage5ei_final_stage5_transition_stage": True,
            "project_codex_hooks_declared": True,
            "project_codex_hooks_operator_visible": True,
            "project_codex_hooks_operator_trusted_locally": True,
            "active_hooks_effective_now": True,
            "blocking_hooks_effective_now": False,
            "hook_execution_relies_on_deterministic_scanner": True,
            "custom_agents_invoked_by_hooks": False,
            "operator_hook_trust_source": "local_codex_trust_state_or_explicit_operator_action",
        }
    )
    write_yaml(CURRENT_STAGE_STATE_PATH, payload)


def _update_current_mirrors() -> None:
    _replace_heading_section(Path("STATUS.md"), "## Current Stage", "## Completed", _status_current_section())
    _replace_roadmap_current_intro()
    _replace_heading_section(
        Path("README.md"),
        "## Current boundaries and deferred work",
        "### Permanent safety rules",
        _readme_current_section(),
    )
    _replace_literal(
        Path("README.md"),
        "- Next: Stage 5EI - Source-lock number-fact review batch 006, without execution.",
        "- Historical next after Stage 5EH: Stage 5EI - Source-lock number-fact review batch 006, without execution.",
    )
    _replace_between_literals(Path("AGENTS.md"), "## Current stage", "Current project state:", _agents_current_section())
    _update_chatgpt_context()
    _update_staged_plan_current_lines()
    _replace_heading_section(Path("docs/onboarding/start-here.md"), "## Current State", "## Where To Start", _start_here_section())
    _upsert_marked_section(Path("docs/onboarding/source-of-truth-map.md"), STAGE_TOKEN, _source_of_truth_section())
    _upsert_marked_section(Path("docs/onboarding/operational-file-map.md"), STAGE_TOKEN, _onboarding_operational_map_section())
    _upsert_marked_section(Path("TESTING.md"), STAGE_TOKEN, _testing_section())
    _upsert_marked_section(Path("docs/reference/token-block-cli.md"), STAGE_TOKEN, _cli_doc_section())


def _replace_heading_section(path: Path, start_heading: str, end_prefix: str, section_text: str) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if start_heading not in text:
        _upsert_marked_section(path, f"{STAGE_TOKEN} current-state", section_text)
        return
    before, rest = text.split(start_heading, 1)
    end_index = rest.find(end_prefix)
    if end_index == -1:
        path.write_text(before.rstrip() + "\n\n" + section_text.rstrip() + "\n", encoding="utf-8")
        return
    after = rest[end_index:]
    path.write_text(before.rstrip() + "\n\n" + section_text.rstrip() + "\n\n" + after, encoding="utf-8")


def _replace_between_literals(path: Path, start_literal: str, end_literal: str, section_text: str) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if start_literal not in text or end_literal not in text:
        _upsert_marked_section(path, f"{STAGE_TOKEN} current-state", section_text)
        return
    before, rest = text.split(start_literal, 1)
    _old, after = rest.split(end_literal, 1)
    path.write_text(before.rstrip() + "\n\n" + section_text.rstrip() + "\n\n" + end_literal + after, encoding="utf-8")


def _replace_literal(path: Path, old: str, new: str) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8")


def _update_chatgpt_context() -> None:
    path = CHATGPT_CONTEXT_PATH
    if not path.exists():
        path.write_text("# ChatGPT Context File\n\n" + _chatgpt_section().rstrip() + "\n", encoding="utf-8")
        return
    text = path.read_text(encoding="utf-8")
    end_marker = "\n## Stage 5DV Source Browser Repair"
    end_index = text.find(end_marker)
    if end_index == -1:
        _upsert_marked_section(path, f"{STAGE_TOKEN} current-state", _chatgpt_section())
        return
    candidate_starts = [
        index
        for index in (
            text.find("## Current Project State"),
            text.find("## Stage 5EI Current Boundary"),
        )
        if index != -1 and index < end_index
    ]
    if candidate_starts:
        start_index = min(candidate_starts)
    elif text.startswith("# ChatGPT Context File"):
        first_blank = text.find("\n\n")
        start_index = first_blank + 2 if first_blank != -1 else 0
    else:
        start_index = 0
    before = text[:start_index].rstrip()
    after = text[end_index:].lstrip()
    path.write_text(before + "\n\n" + _chatgpt_section().rstrip() + "\n\n" + after, encoding="utf-8")
    _remove_marked_section(path, STAGE_TOKEN)
    _remove_marked_section(path, f"{STAGE_TOKEN} current-state")


def _remove_marked_section(path: Path, token: str) -> None:
    if not path.exists():
        return
    marker = f"<!-- BEGIN {token} -->"
    end_marker = f"<!-- END {token} -->"
    text = path.read_text(encoding="utf-8")
    while marker in text and end_marker in text:
        before, rest = text.split(marker, 1)
        _body, after = rest.split(end_marker, 1)
        text = before.rstrip() + "\n\n" + after.lstrip()
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _replace_roadmap_current_intro() -> None:
    path = Path("ROADMAP.md")
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    anchor = "The durable staged plan is maintained"
    if anchor not in text:
        _upsert_marked_section(path, f"{STAGE_TOKEN} current-state", _roadmap_current_section())
        return
    _before, after = text.split(anchor, 1)
    replacement = "# Roadmap\n\n" + _roadmap_current_section().rstrip() + "\n\n" + anchor + after
    if "## Current Direction" in replacement:
        replacement = _replace_second_current_direction(replacement)
    path.write_text(replacement, encoding="utf-8")


def _replace_second_current_direction(text: str) -> str:
    first = text.find("## Current Direction")
    second = text.find("## Current Direction", first + 1)
    if second == -1:
        return text
    next_heading = text.find("\n## ", second + 1)
    if next_heading == -1:
        return text[:second].rstrip() + "\n"
    return text[:second].rstrip() + "\n\n" + text[next_heading + 1 :]


def _update_staged_plan_current_lines() -> None:
    path = Path("docs/roadmap/staged-plan.md")
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    split_marker = "## Completed Stage Timeline"
    head, separator, tail = text.partition(split_marker)
    replacements = {
        "- Latest completed stage: Stage 5EH - Lag5/outguess/byte-string/red-number/F5 context source-lock addendum, diagnostic probe manifests, and enriched fact cards, without execution.": "- Latest completed stage: Stage 5EI - Final Stage 5 triangle-transposition and diagnostics transition, without execution.",
        "- Current planning focus: Stage 5EI - Source-lock number-fact review batch 006, without execution.": "- Current planning focus: Stage 6 - Probe and diagnostic readiness, without execution.",
    }
    for old, new in replacements.items():
        head = head.replace(old, new, 1)
    text = head + separator + tail
    path.write_text(text, encoding="utf-8")
    _replace_heading_section(path, "## Current Stage", "## Planned Next Stages", _staged_plan_current_stage_section())
    _replace_heading_section(
        path,
        "## Planned Next Stages",
        "The independent review",
        _staged_plan_planned_next_section(),
    )
    _upsert_marked_section(path, STAGE_TOKEN, _staged_plan_stage5ei_section())


def _upsert_marked_section(path: Path, token: str, body: str) -> None:
    marker = f"<!-- BEGIN {token} -->"
    end_marker = f"<!-- END {token} -->"
    block = f"{marker}\n{body.rstrip()}\n{end_marker}"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker in text and end_marker in text:
        before, rest = text.split(marker, 1)
        _old, after = rest.split(end_marker, 1)
        path.write_text(before.rstrip() + "\n\n" + block + after, encoding="utf-8")
        return
    if text.endswith("\n"):
        path.write_text(text + "\n" + block + "\n", encoding="utf-8")
    else:
        path.write_text(text + "\n\n" + block + "\n", encoding="utf-8")


def _status_current_section() -> str:
    return f"""## Current Stage

- Latest completed stage: {STAGE_TITLE}.
- Current next stage: {NEXT_STAGE_TITLE}.
- Next recommended prompt: {NEXT_STAGE_TITLE}.
- Stage 5EI supersedes the previously routed ordinary number-fact review batch 006 and routes the project to Stage 6 probe/diagnostic readiness.
- Stage 5EI records PDD153/T17 geometry, triangular-transposition taxonomy ambiguity, Pascal/Fibonacci diagonal context, and fingerprint-based route-diagnostic policy as review-only metadata.
- No probe, route, byte-stream, OCR/image/stego, PGP/OutGuess/F5/StegDetect, CUDA, scoring, target-selection, canonical-corpus, page-boundary, or solve work is authorized.
"""


def _roadmap_current_section() -> str:
    return f"""## Current Direction

Current completed stage: {STAGE_TITLE}.

Next routed stage: {NEXT_STAGE_TITLE}.

Stage 6 is a readiness stage only. It should define finite probe sets, fingerprints, null controls, and result-source requirements before any later bounded diagnostic execution. Stage 7 may run bounded diagnostics only after Stage 6 records the readiness contract. Stage 8 remains triangle-specific experiment readiness, and Stage 9 is the earliest triangle-experiment stage.
"""


def _readme_current_section() -> str:
    return f"""## Current boundaries and deferred work

Current completed stage: {STAGE_TITLE}.

Current next prompt: {NEXT_STAGE_TITLE}.

The Stage 5 source-lock/enrichment chain is closed for now. Stage 5EI did not run number-fact batch 006, generate route streams, execute probes, perform image/stego/OCR work, run CUDA/scoring/benchmarks, activate the canonical corpus, finalize page boundaries, or claim a solve.

These are not permanent project exclusions. CUDA and broad campaigns are deferred, not permanently excluded.
"""


def _staged_plan_stage5ei_section() -> str:
    return f"""## Stage 5EI - Final Stage 5 Triangle Diagnostics Transition

Stage 5EI records PDD153/T17 geometry, triangular-transposition taxonomy ambiguity, Pascal/Fibonacci diagonal context, bottom-row quarantine warnings, review-only overlays, and a fingerprint-based route-diagnostic policy. It runs no probes, routes, byte streams, OCR/image/stego tools, CUDA, scoring, benchmarks, target selection, canonical-corpus activation, page-boundary finalisation, or solve claims.

Next: {NEXT_STAGE_TITLE}.
"""


def _staged_plan_current_stage_section() -> str:
    return f"""## Current Stage

{STAGE_TITLE} is the latest completed stage. It supersedes the previously routed ordinary number-fact review batch 006, records final Stage 5 triangle/route diagnostic context, preserves Stage 5EH counts, and keeps all probe, route, byte-stream, OCR/image/stego, PGP/OutGuess/F5/StegDetect, CUDA, scoring, target-selection, canonical-corpus, page-boundary, and solve gates closed.

Current planning focus: {NEXT_STAGE_TITLE}. Stage 6 is a readiness stage only; Stage 5EI does not run Stage 6 probes or generate route streams.
"""


def _staged_plan_planned_next_section() -> str:
    return """## Planned Next Stages

- Stage 6 - Probe and diagnostic readiness, without execution.
- Stage 7 - Actual probes and diagnostics only after Stage 6 approval gates.
- Stage 8 - Triangle-specific experiment readiness, without execution.
- Stage 9 - Triangle experiments only after Stage 8 approval gates.
- Future unnumbered website expansion project after CUDA reporting boundaries are stable.
"""


def _agents_current_section() -> str:
    return f"""## Current stage

Current completed stage: {STAGE_TITLE}.

Current work: {NEXT_STAGE_TITLE}. Stage 5EI superseded the previously routed ordinary number-fact review batch 006 and records final Stage 5 triangle/route diagnostic context as review-only metadata.

No Deep Research activation-acceptance record exists, the combined gate is not satisfied, no valid activation decision exists, and no active planning input authorization or selection exists. String 4 remains inactive; no target-priority selection, source-lock browser puzzle execution, direct source-record number-fact backfill, historical source-lock rewrite, triangle/Page32 route extraction, music route extraction, audio/stego/OCR/image forensics/AI interpretation, active ingestion, byte-stream generation, machine-code/VM execution, manifest supersession, execution, target-class validation, Tor access, DWH/hash/preimage search, decode, scoring, CUDA, benchmark, website expansion, method-status upgrade, canonical corpus activation, page-boundary finalisation, or solve claim is authorized.

Discord raw logs are not committed. Raw page images, raw historical stego artefacts, generated outputs, SQLite databases, and local reports remain ignored and uncommitted.
"""


def _agents_section() -> str:
    return f"""## Stage 5EI Current Boundary

Current completed stage: {STAGE_TITLE}.

Current work: {NEXT_STAGE_TITLE}.

Project-local `.codex` hooks are declared and operator-approved locally for Stage 5EI recording purposes. They remain deterministic scanner hooks, not custom-agent execution hooks: `blocking_hooks_effective_now=false`, `hook_execution_relies_on_deterministic_scanner=true`, and `custom_agents_invoked_by_hooks=false`.

Stage 5EI superseded the ordinary number-fact review batch 006. Do not run probes, route extraction, byte-stream generation, OCR/image/stego, PGP/OutGuess/F5/StegDetect, CUDA, scoring, benchmarks, target selection, canonical corpus activation, page-boundary finalisation, or solve claims under the Stage 5EI records. Stage 6 must be readiness-only unless a later prompt explicitly changes scope.
"""


def _chatgpt_section() -> str:
    return f"""## Current Project State

## Stage 5EI Current Boundary

Latest completed stage: {STAGE_TITLE}.

Current planning focus: {NEXT_STAGE_TITLE}.

Stage 5EI is the final Stage 5 metadata transition. It records PDD153/T17 geometry, triangular-transposition taxonomy ambiguity, Pascal/Fibonacci diagonal context, and fingerprint-based route-diagnostic policy as review-only metadata. The ordinary number-fact review batch 006 was superseded and was not performed.
"""


def _start_here_section() -> str:
    return f"""## Stage 5EI Current Boundary

The current authority is `data/project-state/current-stage-state.yaml`. It now records {STAGE_TITLE} as complete and {NEXT_STAGE_TITLE} as next.

Historical Stage 5EE, Stage 5EG, and Stage 5EH sections are evidence of their time, not current routing instructions. If they mention old next prompts, read them as historical only when the section says so explicitly.
"""


def _source_of_truth_section() -> str:
    return f"""## Stage 5EI Source-Of-Truth Update

- Authoritative current state: `data/project-state/current-stage-state.yaml`.
- Current mirrors: `STATUS.md`, `README.md`, `ROADMAP.md`, `AGENTS.md`, `ChatGPT-ContextFile.md`, and `docs/roadmap/staged-plan.md`.
- Latest completed stage: {STAGE_TITLE}.
- Next routed stage: {NEXT_STAGE_TITLE}.
- Historical logs and previous stage sections remain evidence, not current truth.
"""


def _onboarding_operational_map_section() -> str:
    return """## Stage 5EI Operational Map Update

Use `data/project-state/current-stage-state.yaml` for latest/next-stage truth. Stage 5EI is complete and Stage 6 is the next routed readiness stage. Older examples that mention Stage 5EI as batch 006 are historical and must not be used as current routing.
"""


def _testing_section() -> str:
    return """## Stage 5EI Validation Policy

Stage 5EI uses focused validators first, then the stale-current scanner in strict mode, Source Browser validation, focused Stage 5EI pytest files, ruff, `stage-fast`, `local-fast`, and one `full-parallel` run with `Workers=10` and `PytestWorkers=10`. Full serial pytest is not required for normal closeout.
"""


def _cli_doc_section() -> str:
    return """## Stage 5EI Token-Block Commands

- `libreprimus token-block build-stage5ei`
- `libreprimus token-block validate-stage5ei`
- `libreprimus token-block stage5ei-summary`
- focused validators are available for Stage 5EH preservation, current mirrors, stale-current scanner regressions, PDD153 geometry, route-diagnostic policy, Stage 6 roadmap, overlays, Source Browser loadability, gate closure, and handoff.
"""


def _update_docs(summary: dict[str, Any]) -> None:
    DEV_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEV_LOG_PATH.write_text(
        f"""# Stage 5EI Development Log

Date: 2026-06-13

Stage: {STAGE_TITLE}

Summary:
- Built Stage 5EI metadata records for final Stage 5 transition to Stage 6.
- Preserved Stage 5EH counts: probes {summary.get('stage5eh_future_probe_manifest_count')}, overlays {summary.get('stage5eh_overlay_count')}, Source Browser errors {summary.get('stage5eh_source_browser_validation_error_count')}.
- Recorded PDD153/T17 geometry, triangular-transposition taxonomy ambiguity, Pascal/Fibonacci diagonal context, and fingerprint-based route diagnostics.
- Repaired focused current mirrors and preserved the Stage 5EG stale-current scanner.

Guardrails:
- No source-lock evidence rewrite.
- No ordinary number-fact batch 006.
- No route stream, byte stream, probe execution, CUDA, scoring, image/stego/OCR, target selection, corpus activation, page-boundary finalisation, or solve claim.
""",
        encoding="utf-8",
    )
    RESEARCH_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_LOG_PATH.write_text(
        f"""# Stage 5EI Triangle Diagnostics Transition Summary

Stage 5EI closes the Stage 5 metadata/source-lock chain and routes future work to Stage 6 readiness.

Key records:
- T17/PDD153 geometry anchors: {summary.get('triangle_geometry_record_count')} candidate records.
- Route fingerprints: {summary.get('route_fingerprint_count')}.
- Review-only overlays: {summary.get('overlay_count')}.
- Stale-current strict errors after repair: {summary.get('stale_current_claim_strict_errors_after_stage5ei')}.

The stage records candidate context only. It does not execute probes, generate route streams, score outputs, run CUDA, or claim a solve.
""",
        encoding="utf-8",
    )
    EXPERIMENT_DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXPERIMENT_DOC_PATH.write_text(
        f"""# Stage 5EI Triangle-Transposition Diagnostics Transition

Stage 5EI is a metadata-only transition. It records PDD153/T17 geometry and route-diagnostic policies for future readiness work.

It does not run triangular transpositions, generate route streams, attempt decryption, score outputs, run CUDA, or activate corpus/page-boundary decisions.

Next: {NEXT_STAGE_TITLE}.
""",
        encoding="utf-8",
    )


def _update_stage_summary_records() -> None:
    records = _safe_read(STAGE_SUMMARY_RECORDS_PATH)
    if isinstance(records, dict) and isinstance(records.get("records"), list):
        items = records["records"]
        wrapper = records
    elif isinstance(records, list):
        items = records
        wrapper = None
    else:
        items = []
        wrapper = None
    item = {
        "record_type": "stage_summary_record",
        "stage_id": STAGE_ID,
        "title": STAGE_TITLE,
        "status": "complete",
        "category": "metadata_transition",
        "summary": (
            "Completed final Stage 5 triangle-transposition and diagnostics transition metadata, "
            "preserved Stage 5EH counts, repaired focused current mirrors, and routed the project "
            "to Stage 6 probe/diagnostic readiness without execution."
        ),
        "key_outputs": [
            "PDD153/T17 geometry, 56311 row-edge path, d=4 diagonal anchor, and bottom-row/Page32 quarantine bridge recorded as review-only metadata.",
            "Triangular-transposition 22-count operator claim and 24-family assistant observation preserved as unresolved taxonomy context.",
            "Fingerprint-based route-diagnostic policy recorded without requiring plaintext likeness or generating route streams.",
            "Stage 5EH probe, overlay, and Source Browser counts preserved; ordinary number-fact review batch 006 superseded.",
            "Focused current mirrors repaired for Stage 5EI -> Stage 6 and stale-current strict scanner remains at zero errors.",
        ],
        "result_status": "metadata_transition_complete",
        "solve_claim": False,
        "cuda_used": False,
        "raw_outputs_committed": False,
        "generated_outputs_committed": False,
        "notes": (
            f"next={NEXT_STAGE_ID}; full_serial_pytest_required=false; no probes, route extraction, "
            "byte streams, OCR/image/stego, PGP/OutGuess/F5/StegDetect, CUDA, scoring, target selection, "
            "canonical-corpus activation, page-boundary finalisation, or solve claim."
        ),
    }
    items = [existing for existing in items if existing.get("stage_id") != STAGE_ID]
    items.append(item)
    if wrapper is not None:
        wrapper["records"] = items
        write_yaml(STAGE_SUMMARY_RECORDS_PATH, wrapper)
    else:
        write_yaml(STAGE_SUMMARY_RECORDS_PATH, items)


def _update_operational_file_map() -> None:
    payload = _safe_read(OPERATIONAL_FILE_MAP_PATH)
    stage_entry = {
        "stage_id": STAGE_ID,
        "summary": PROJECT_STATE_PATHS["summary"].as_posix(),
        "current_stage_state": CURRENT_STAGE_STATE_PATH.as_posix(),
        "route_policy": TOKEN_BLOCK_PATHS["route_diagnostic_policy"].as_posix(),
        "overlays": OPERATOR_PATHS["overlay_collection"].as_posix(),
        "next_stage": NEXT_STAGE_ID,
    }
    if isinstance(payload.get("stage5ei"), dict):
        payload["stage5ei"] = stage_entry
    else:
        payload.setdefault("stage_records", {})
        if isinstance(payload["stage_records"], dict):
            payload["stage_records"][STAGE_ID] = stage_entry
        else:
            payload["stage5ei"] = stage_entry
    write_yaml(OPERATIONAL_FILE_MAP_PATH, payload)


def _update_doc_staleness_source_of_truth() -> None:
    payload = _safe_read(DOC_STALENESS_SOURCE_OF_TRUTH_PATH)
    payload["stage_id"] = STAGE_ID
    payload["latest_completed_stage_id"] = STAGE_ID
    payload["latest_completed_stage_after_this_stage"] = STAGE_TITLE
    payload["latest_completed_stage_prefix"] = "Stage 5EI"
    payload["recommended_next_stage_id"] = NEXT_STAGE_ID
    payload["next_stage_after_this_stage"] = NEXT_STAGE_TITLE
    payload["expected_next_stage_prefix"] = "Stage 6"
    payload.setdefault("current_truth_mirrors", [path.as_posix() for path in CURRENT_MIRROR_PATHS])
    payload["stage5ei_current_mirror_repair_record"] = PROJECT_STATE_PATHS["current_mirror_repair"].as_posix()
    write_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH, payload)


def _write_completion_handoff(summary: dict[str, Any]) -> None:
    CODEX_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = CODEX_OUTPUT_DIR / "stage5ei-codex-completion.md"
    path.write_text(
        f"""# Stage 5EI Completion Handoff

Stage: {STAGE_TITLE}
Starting commit: {PREVIOUS_STAGE_FINAL_COMMIT}
Final commit: pending
Origin/main commit: pending
GitHub issue: pending
CI run/status: pending

Plan Mode used: true
Hook trust state: operator-approved locally; active deterministic hooks effective now true; blocking hooks false.

Stage 5EH preservation:
- probe manifests: {summary.get('stage5eh_future_probe_manifest_count')}
- overlays: {summary.get('stage5eh_overlay_count')}
- Source Browser errors: {summary.get('stage5eh_source_browser_validation_error_count')}

Stage 5EI:
- mirror repair status: focused current mirrors repaired
- stale-current errors: {summary.get('stale_current_claim_strict_errors_after_stage5ei')}
- route fingerprints: {summary.get('route_fingerprint_count')}
- overlays: {summary.get('overlay_count')}
- Stage 6/7/8/9 roadmap: recorded
- full parallel target: Workers=10 / PytestWorkers=10
- full serial pytest run: false

Guardrails: all execution/solve guardrails remain false.

Recommended next stage: {NEXT_STAGE_TITLE}.
""",
        encoding="utf-8",
    )


def _extend_current_stage_state_schema() -> None:
    path = Path("schemas/project-state/current-stage-state-v0.schema.json")
    if not path.exists():
        return
    schema = read_yaml(path)
    _add_enum_value(schema, STAGE_ID)
    _add_enum_value(schema, NEXT_STAGE_ID)
    write_json(path, schema)


def _extend_doc_staleness_schema() -> None:
    path = Path("schemas/project-state/doc-staleness-source-of-truth-record-v0.schema.json")
    if not path.exists():
        return
    schema = read_yaml(path)
    _add_enum_value(schema, STAGE_ID)
    _add_enum_value(schema, NEXT_STAGE_ID)
    write_json(path, schema)


def _add_enum_value(node: Any, value: str) -> None:
    if isinstance(node, dict):
        enum = node.get("enum")
        if isinstance(enum, list) and all(isinstance(item, str) for item in enum) and any(
            item.startswith("stage-") for item in enum
        ):
            if value not in enum:
                enum.append(value)
                enum.sort()
        for child in node.values():
            _add_enum_value(child, value)
    elif isinstance(node, list):
        for child in node:
            _add_enum_value(child, value)


def _safe_read(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = read_yaml(path)
    return payload if isinstance(payload, dict) else {}


def _result(errors: list[str], **counts: Any) -> ValidationResult:
    return ValidationResult(errors=errors, counts=counts)


def _format(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
