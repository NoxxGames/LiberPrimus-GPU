"""Stage 5EH Lag5/outguess/byte-control source-lock addendum."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import mimetypes
from pathlib import Path
import struct
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.doc_staleness.stale_current_claims import audit_repository
from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import validate_source_index
from libreprimus.token_block.models import read_yaml, sha256_file, write_json, write_yaml

STAGE_ID = "stage-5eh"
STAGE_TOKEN = "stage5eh"
STAGE_TITLE = (
    "Stage 5EH - Lag5/outguess/byte-string/red-number/F5 context source-lock "
    "addendum, diagnostic probe manifests, and enriched fact cards, without execution"
)
PROMPT_TYPE = "codex_plan_mode_source_lock_addendum"
PREVIOUS_STAGE_ID = "stage-5eg"
PREVIOUS_STAGE_TITLE = (
    "Stage 5EG - Post-edit doc-staleness guardians, read-only auditor agents, "
    "stop-hook drift gate, and daily automation setup, without puzzle execution"
)
PREVIOUS_STAGE_COMMIT = "12ede40837c4bfe9ee5172e3fd21946f5057580b"
PREVIOUS_STAGE_CI_RUN = 27439042451
PREVIOUS_STAGE_CI_STATUS = "passed"
NEXT_STAGE_ID = "stage-5ei"
NEXT_STAGE_TITLE = "Stage 5EI - Source-lock number-fact review batch 006, without execution"

PROJECT_STATE_DIR = Path("data/project-state")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
HISTORICAL_ROUTE_DIR = Path("data/historical-route")
TOKEN_BLOCK_DIR = Path("data/token-block")
OPERATOR_OVERLAY_DIR = Path("data/operator-console/source-browser/number-fact-overlays")
OPERATOR_BATCH_DIR = Path("data/operator-console/source-browser/number-fact-review-batches")
RESEARCH_DIR = Path("data/research")
CODEX_OUTPUT_DIR = Path("codex-output")

LAG5_ROOT = Path("third_party/Lag5-phenomenon")
IDDQD_ROOT = Path("third_party/CiadaSolversIddqd_v2")
LP_OUTGUESSED_ROOT = IDDQD_ROOT / "lp_outguessed"
BYTE_STRINGS_SOURCE = IDDQD_ROOT / "byte-strings" / "byte-strings"
FULL_IMAGES_ROOT = IDDQD_ROOT / "liber-primus__images--full"

CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
OPERATIONAL_FILE_MAP_PATH = PROJECT_STATE_DIR / "operational-file-map.yaml"
STAGE_SUMMARY_RECORDS_PATH = RESEARCH_DIR / "stage-summary-records-v0.yaml"
DOC_STALENESS_SOURCE_OF_TRUTH_PATH = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
CHATGPT_CONTEXT_PATH = Path("ChatGPT-ContextFile.md")
DEV_LOG_PATH = Path("docs/development-logs/2026-06-13-stage-5eh-lag5-outguess-byte-control-source-lock.md")
RESEARCH_LOG_PATH = Path("research-log/2026-06-13-stage5eh-lag5-outguess-byte-control-summary.md")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5eh-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5eh-next-stage-decision.yaml",
    "stage5eg_preservation": PROJECT_STATE_DIR / "stage5eh-stage5eg-preservation.yaml",
    "stage5ef_preservation": PROJECT_STATE_DIR / "stage5eh-stage5ef-preservation.yaml",
    "stage5eb_validation_policy_preservation": PROJECT_STATE_DIR
    / "stage5eh-stage5eb-validation-policy-preservation.yaml",
    "recent_source_lock_register": PROJECT_STATE_DIR / "stage5eh-recent-source-lock-register.yaml",
    "diagnostic_probe_manifest_index": PROJECT_STATE_DIR / "stage5eh-diagnostic-probe-manifest-index.yaml",
    "enriched_fact_card_batch_result": PROJECT_STATE_DIR / "stage5eh-enriched-fact-card-batch-result.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR / "stage5eh-source-browser-loadability-summary.yaml",
    "current_truth_doc_staleness_guard_evidence": PROJECT_STATE_DIR
    / "stage5eh-current-truth-doc-staleness-guard-evidence.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5eh-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5eh-reviewability-gap-register.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage5eh-chatgpt-context-update-summary.yaml",
    "scope_control": PROJECT_STATE_DIR / "stage5eh-scope-control.yaml",
}
SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "lag5_local_source_lock_register": SOURCE_HARVESTER_DIR / "stage5eh-lag5-local-source-lock-register.yaml",
    "lag5_file_inventory": SOURCE_HARVESTER_DIR / "stage5eh-lag5-file-inventory.yaml",
    "lp_outguessed_source_lock_register": SOURCE_HARVESTER_DIR
    / "stage5eh-lp-outguessed-source-lock-register.yaml",
    "lp_outguessed_pgp_signed_output_inventory": SOURCE_HARVESTER_DIR
    / "stage5eh-lp-outguessed-pgp-signed-output-inventory.yaml",
    "cicada_solvers_iddqd_v2_crosswalk": SOURCE_HARVESTER_DIR
    / "stage5eh-cicada-solvers-iddqd-v2-crosswalk.yaml",
    "byte_strings_context_crosswalk": SOURCE_HARVESTER_DIR / "stage5eh-byte-strings-context-crosswalk.yaml",
    "page54_55_red_number_source_crosswalk": SOURCE_HARVESTER_DIR
    / "stage5eh-page54-55-red-number-source-crosswalk.yaml",
    "page13_stegdetect_operator_result_lock": SOURCE_HARVESTER_DIR
    / "stage5eh-page13-stegdetect-operator-result-lock.yaml",
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5eh-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5eh-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5eh-raw-source-noncommit-proof.yaml",
}
HISTORICAL_ROUTE_PATHS: dict[str, Path] = {
    "lag5_candidate_records": HISTORICAL_ROUTE_DIR / "stage5eh-lag5-candidate-records.yaml",
    "outguess_pgp_xor_records": HISTORICAL_ROUTE_DIR / "stage5eh-outguess-pgp-xor-records.yaml",
    "byte_string_context_records": HISTORICAL_ROUTE_DIR / "stage5eh-byte-string-context-records.yaml",
    "red_number_control_records": HISTORICAL_ROUTE_DIR / "stage5eh-red-number-control-records.yaml",
    "stegdetect_f5_signal_records": HISTORICAL_ROUTE_DIR / "stage5eh-stegdetect-f5-signal-records.yaml",
}
TOKEN_BLOCK_PATHS: dict[str, Path] = {
    "stage5bd_plan_preservation": TOKEN_BLOCK_DIR / "stage5eh-stage5bd-plan-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5eh-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5eh-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage5eh-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage5eh-no-execution-transition-gate.yaml",
    "token_block_static_context_preservation": TOKEN_BLOCK_DIR
    / "stage5eh-token-block-static-context-preservation.yaml",
    "diagnostic_probe_manifest_records": TOKEN_BLOCK_DIR / "stage5eh-diagnostic-probe-manifest-records.yaml",
}
OPERATOR_PATHS: dict[str, Path] = {
    "overlay_collection": OPERATOR_OVERLAY_DIR / "stage5eh-recent-lag5-outguess-byte-control-overlays.yaml",
    "review_batch_result": OPERATOR_BATCH_DIR / "stage5eh-recent-lag5-outguess-byte-control-result.yaml",
}
DATA_PATHS: dict[str, Path] = {
    **PROJECT_STATE_PATHS,
    **SOURCE_HARVESTER_PATHS,
    **HISTORICAL_ROUTE_PATHS,
    **TOKEN_BLOCK_PATHS,
    **OPERATOR_PATHS,
}

SCHEMA_PATHS: dict[str, Path] = {
    key: Path(f"schemas/project-state/stage5eh-{key.replace('_', '-')}-v0.schema.json")
    for key in PROJECT_STATE_PATHS
}
SCHEMA_PATHS.update(
    {
        key: Path(f"schemas/source-harvester/stage5eh-{key.replace('_', '-')}-v0.schema.json")
        for key in SOURCE_HARVESTER_PATHS
    }
)
SCHEMA_PATHS.update(
    {
        "lag5_candidate_records": Path("schemas/historical-route/stage5eh-lag5-candidate-record-v0.schema.json"),
        "outguess_pgp_xor_records": Path("schemas/historical-route/stage5eh-outguess-pgp-xor-record-v0.schema.json"),
        "byte_string_context_records": Path("schemas/historical-route/stage5eh-byte-string-context-record-v0.schema.json"),
        "red_number_control_records": Path("schemas/historical-route/stage5eh-red-number-control-record-v0.schema.json"),
        "stegdetect_f5_signal_records": Path("schemas/historical-route/stage5eh-stegdetect-f5-signal-record-v0.schema.json"),
    }
)
SCHEMA_PATHS.update(
    {
        key: Path(f"schemas/token-block/stage5eh-{key.replace('_', '-')}-v0.schema.json")
        for key in TOKEN_BLOCK_PATHS
    }
)
SCHEMA_PATHS.update(
    {
        "overlay_collection": Path(
            "schemas/operator-console/source-browser-stage5eh-number-fact-overlay-v0.schema.json"
        ),
        "review_batch_result": Path(
            "schemas/operator-console/stage5eh-source-browser-number-fact-review-batch-result-v0.schema.json"
        ),
    }
)

EXPECTED_LAG5_FILES = [
    "messages.txt",
    "lag5-phenomenon.md",
    "second pair runes.txt",
    "raw frequency data.png",
    "and less intersting.png",
]
EXPECTED_SIGNED_OUTPUTS = ["00.txt", "01.txt", "02.txt", "03.txt", "10.txt", "11.txt", "12.txt", "13.txt"]
OUTGUESS03_GP_VALUES = [5, 71, 89, 41, 2, 71, 97, 11, 3, 101, 79, 11, 79, 109, 71, 41, 2, 107]
FUTURE_PROBE_IDS = [
    "lag5_reproduction_probe_candidate_v0",
    "lag5_doublet_suppressed_null_probe_candidate_v0",
    "lag5_page_section_event_overlay_probe_candidate_v0",
    "lag5_token_block_neighborhood_probe_candidate_v0",
    "lag5_pdd153_56311_route_overlay_probe_candidate_v0",
    "lag5_page32_route_stream_fingerprint_probe_candidate_v0",
    "lag5_disk_doublet_suppression_model_constraint_probe_candidate_v0",
    "lag5_negative_space_null_marker_bridge_probe_candidate_v0",
    "outguess_pgp_signature_verification_probe_candidate_v0",
    "outguess_00_01_02_xor_reconstruction_probe_candidate_v0",
    "outguess_03_jpeg_extraction_metadata_probe_candidate_v0",
    "outguess_03_jpeg_human_transcription_verification_probe_candidate_v0",
    "xor_txt_29_symbol_alphabet_classification_probe_candidate_v0",
    "outguess_magic_square_route_mask_probe_candidate_v0",
    "byte_strings_outguess_xor_precedent_comparison_probe_candidate_v0",
    "byte_strings_03_control_key_probe_candidate_v0",
    "byte_strings_16x16_matrix_route_mask_probe_candidate_v0",
    "byte_strings_token_block_matrix_comparison_probe_candidate_v0",
    "page54_55_red_numbered_line_block_transcript_alignment_probe_candidate_v0",
    "lp_pages_stegdetect_baseline_probe_manifest_v0",
    "known_outguessed_pages_stegdetect_comparison_probe_manifest_v0",
    "star_artifact_mod8_dct_residue_probe_manifest_v0",
    "page13_canonical_image_hash_and_detector_reproduction_probe_manifest_v0",
]
CROSSLINK_FAMILIES = [
    "pdd_153_triangle_word_prime_route_v1",
    "pdd_153_triangle_56311_wynn_way_route_v1",
    "page32_moebius_fibonacci_prime_index_spiral_v1",
    "page32_tree_polar_route_v0",
    "disk_doublet_suppression_candidate_v1",
    "disk_56311_wynn_way_bridge_v1",
    "lp_doublet_scarcity_feature_v1",
    "token_block_matrix_context_v0",
    "stage5bk_iddqd_v2_byte_strings_source_lock_set",
    "lp_negative_space_layout_candidate_family_v0",
    "big_gap_vertical_phase_shift_candidate_v0",
    "star_artifacts_exact254_mask_method_v0",
    "page54_55_a_postlude_red_heading_candidate_v0",
    "page56_dwh_hash_target_contract_v0",
    "music_transform_grammar_for_cipher_methods_candidate_v1",
]
FALSE_GUARDRAILS = {
    "historical_source_lock_records_rewritten": False,
    "number_fact_backfill_performed_now": False,
    "new_source_lock_evidence_added_as_raw_body": False,
    "raw_third_party_files_committed": False,
    "route_extraction_performed_now": False,
    "route_stream_generated_now": False,
    "real_byte_stream_generated": False,
    "variant_byte_streams_generated": False,
    "xor_reconstruction_performed_now": False,
    "outguess_execution_performed": False,
    "pgp_verification_performed_now": False,
    "stegdetect_execution_performed_now": False,
    "f5_extraction_performed_now": False,
    "f5_password_search_performed_now": False,
    "image_forensics_performed": False,
    "ocr_performed": False,
    "audio_stego_performed": False,
    "spectrogram_stego_performed": False,
    "tor_network_access_performed": False,
    "target_priority_decision_created_now": False,
    "pivot_target_selected_now": False,
    "target_class_validation_implemented": False,
    "cuda_execution_performed": False,
    "scoring_performed": False,
    "benchmark_performed": False,
    "canonical_corpus_active": False,
    "page_boundaries_finalized": False,
    "page_boundaries_final": False,
    "solve_claim": False,
    "execution_performed": False,
    "generated_outputs_committed": False,
}


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: list[str]
    counts: dict[str, Any]

    @property
    def validation_error_count(self) -> int:
        return len(self.errors)

    def to_cli_text(self) -> str:
        lines = [f"{key}={value}" for key, value in self.counts.items()]
        lines.append(f"validation_error_count={len(self.errors)}")
        lines.extend(f"error={error}" for error in self.errors)
        return "\n".join(lines)


def build_stage5eh() -> dict[str, Any]:
    """Build deterministic Stage 5EH metadata/source-lock records."""

    _write_schemas()
    inventory = _inventory()
    records = _records(
        inventory,
        _empty_source_browser_record(),
        {"stale_current_error_count": 0, "stale_current_warning_count": 0},
    )
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)
    _update_current_stage_state(records["summary"])
    _update_current_mirrors()
    _update_stage5ah_source_of_truth()
    _write_docs(inventory)
    source_browser = _source_browser_loadability_record()
    stale_report = audit_repository()
    records = _records(
        inventory,
        source_browser,
        {
            "stale_current_error_count": stale_report.error_count,
            "stale_current_warning_count": stale_report.warning_count,
        },
    )
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)
    _update_stage_summary_records(records["summary"])
    _update_operational_file_map()
    _write_codex_output_handoff(records["summary"])
    return records


def validate_stage5eh() -> ValidationResult:
    return _combine(
        [
            validate_required_paths,
            validate_schema_files,
            validate_schema_payloads,
            validate_lag5_inventory,
            validate_lp_outguessed_inventory,
            validate_outguess03_context,
            validate_byte_string_crosslinks,
            validate_page54_55_red_number_context,
            validate_page13_f5_context,
            validate_stage5eh_number_fact_overlays,
            validate_stage5eh_source_browser_loadability,
            validate_stage5eh_current_truth_doc_staleness,
            validate_stage5eh_sidecar_gates,
            validate_stage5eh_handoff_continuity,
            validate_stage5eh_governance_scope,
        ]
    )


def validate_required_paths() -> ValidationResult:
    paths = [*DATA_PATHS.values(), *SCHEMA_PATHS.values(), DEV_LOG_PATH, RESEARCH_LOG_PATH]
    return _result([f"missing required file: {path}" for path in paths if not path.exists()], required_file_count=len(paths))


def validate_schema_files() -> ValidationResult:
    errors: list[str] = []
    for path in SCHEMA_PATHS.values():
        if not path.exists():
            errors.append(f"missing schema file: {path}")
            continue
        try:
            Draft202012Validator.check_schema(read_yaml(path))
        except Exception as exc:
            errors.append(f"invalid schema {path}: {exc}")
    return _result(errors, schema_count=len(SCHEMA_PATHS))


def validate_schema_payloads() -> ValidationResult:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        if not path.exists():
            errors.append(f"missing payload: {path}")
            continue
        schema_path = SCHEMA_PATHS[key]
        if not schema_path.exists():
            errors.append(f"missing schema for {path}: {schema_path}")
            continue
        try:
            Draft202012Validator(read_yaml(schema_path)).validate(read_yaml(path))
        except Exception as exc:
            errors.append(f"schema validation failed for {path}: {exc}")
    return _result(errors, validated_payload_count=len(DATA_PATHS))


def validate_lag5_inventory() -> ValidationResult:
    file_inventory = _read_record("lag5_file_inventory")
    lag5_records = _read_record("lag5_candidate_records")
    errors = _false_guardrail_errors(file_inventory) + _false_guardrail_errors(lag5_records)
    if file_inventory.get("expected_file_count_present") != 5:
        errors.append("Lag5 expected file inventory did not find all five files")
    if lag5_records.get("event_list_observed_row_count") != 57:
        errors.append("Lag5 event list row count is not 57")
    if lag5_records.get("lag5_marker_definition") != "M[i] = 1 iff C[i] = C[i+5]":
        errors.append("Lag5 marker definition mismatch")
    for key, value in {"d1": 29, "d4": 28}.items():
        if lag5_records.get("lag5_d_counts", {}).get(key) != value:
            errors.append(f"Lag5 {key} count mismatch")
    if lag5_records.get("d1_plus_d4_event_count") != 57:
        errors.append("Lag5 d1+d4 count mismatch")
    for field in [
        "statistical_significance_modest",
        "wide_nuisance_parameter_search_weakens_global_significance",
        "requires_doublet_suppressed_null_model",
        "not_solve_evidence",
    ]:
        if lag5_records.get(field) is not True:
            errors.append(f"Lag5 warning field missing/false: {field}")
    return _result(errors, lag5_file_count=file_inventory.get("expected_file_count_present", 0))


def validate_lp_outguessed_inventory() -> ValidationResult:
    record = _read_record("lp_outguessed_source_lock_register")
    gaps = _read_record("reviewability_gap_register")
    errors = _false_guardrail_errors(record) + _false_guardrail_errors(gaps)
    if record.get("lp_outguessed_inventory_performed_before_records") is not True:
        errors.append("lp_outguessed inventory was not marked as performed first")
    if record.get("lp_outguessed_xor_txt_local_presence_checked") is not True:
        errors.append("xor.txt local presence check missing")
    if record.get("expected_pgp_signed_output_present_count") != 8:
        errors.append("expected signed output present count is not 8")
    if record.get("pgp_signature_verification_status") != "key_missing_or_not_verified_now":
        errors.append("PGP verification status mismatch")
    if record.get("xor_txt_local_file_present"):
        if record.get("xor_txt_exact_hash_recorded") is not True:
            errors.append("present xor.txt did not record exact hash")
    else:
        if record.get("lp_outguessed_xor_txt_reviewability_gap") is not True:
            errors.append("absent xor.txt did not produce reviewability gap")
        if record.get("xor_txt_reconstructed_now") is not False or record.get("xor_txt_synthesized_now") is not False:
            errors.append("absent xor.txt was reconstructed or synthesized")
    if gaps.get("canonical_xor_txt_reviewability_gap") is not True:
        errors.append("canonical xor.txt reviewability gap missing")
    return _result(
        errors,
        expected_signed_output_present_count=record.get("expected_pgp_signed_output_present_count", 0),
        xor_txt_local_file_present=record.get("xor_txt_local_file_present", False),
    )


def validate_outguess03_context() -> ValidationResult:
    record = _read_record("outguess_pgp_xor_records")
    errors = _false_guardrail_errors(record)
    outguess03 = record.get("outguess03_jpeg_transcription", {})
    if outguess03.get("outguess03_rune_gp_prime_values") != OUTGUESS03_GP_VALUES:
        errors.append("Outguess 03 GP transcription values do not match operator-supplied list")
    if outguess03.get("outguess03_segment_lengths_between_literal_digits") != [8, 5, 5]:
        errors.append("Outguess 03 segment lengths mismatch")
    if outguess03.get("outguess03_rune_zero_based_index_sum") != 261:
        errors.append("Outguess 03 index sum mismatch")
    if outguess03.get("outguess03_index_sum_mod29") != 0:
        errors.append("Outguess 03 mod29 neutrality mismatch")
    if outguess03.get("outguess03_ocr_performed_now") is not False:
        errors.append("Outguess 03 OCR flag is not false")
    if outguess03.get("outguess03_used_to_decode_now") is not False:
        errors.append("Outguess 03 used-to-decode flag is not false")
    return _result(errors, outguess03_visible_item_count=outguess03.get("outguess03_visible_item_count_including_digits", 0))


def validate_byte_string_crosslinks() -> ValidationResult:
    record = _read_record("byte_string_context_records")
    errors = _false_guardrail_errors(record)
    if record.get("byte_string_count") != 4 or record.get("exact_512_hex_string_count") != 4:
        errors.append("Stage 5EH byte-string count/crosslink mismatch")
    if record.get("decoded_byte_length_each") != 256:
        errors.append("Stage 5EH decoded byte length metadata mismatch")
    if record.get("byte_strings_real_byte_stream_generated_now") is not False:
        errors.append("Stage 5EH byte-string record generated a real byte stream")
    return _result(errors, byte_string_count=record.get("byte_string_count", 0))


def validate_page54_55_red_number_context() -> ValidationResult:
    record = _read_record("red_number_control_records")
    errors = _false_guardrail_errors(record)
    candidate = record.get("page54_55_red_numbered_line_blocks_candidate_v0", {})
    if candidate.get("not_same_as_a_postlude_red_heading_theory") is not True:
        errors.append("Page54/55 red-number record was not separated from A POSTLUDE")
    if candidate.get("page54_red_numbers_observed_by_assistant_or_operator") != [2, 3, 4]:
        errors.append("Page54 red-number list mismatch")
    if candidate.get("page55_red_numbers_observed_by_operator") != [5]:
        errors.append("Page55 red-number list mismatch")
    if candidate.get("route_control_not_accepted_now") is not True:
        errors.append("Page54/55 route-control warning missing")
    return _result(errors, red_number_candidate_present=bool(candidate))


def validate_page13_f5_context() -> ValidationResult:
    record = _read_record("stegdetect_f5_signal_records")
    errors = _false_guardrail_errors(record)
    candidate = record.get("page13_stegdetect_f5_beta_signal_candidate_v0", {})
    if candidate.get("page13_stegdetect_raw_log_fragment") != "f5[1.368187]":
        errors.append("Page13 StegDetect raw fragment mismatch")
    if candidate.get("page13_stegdetect_detail_beta") != 1.368:
        errors.append("Page13 beta value mismatch")
    for field in ["stegdetect_execution_performed_now", "f5_extraction_performed_now", "known_outguess_payload_confound"]:
        expected = False if "performed" in field else True
        if candidate.get(field) is not expected:
            errors.append(f"Page13 field mismatch: {field}")
    return _result(errors, page13_f5_signal_observed=candidate.get("page13_stegdetect_f5_signal_observed", False))


def validate_stage5eh_number_fact_overlays() -> ValidationResult:
    payload = _read_record("overlay_collection")
    errors = _false_guardrail_errors(payload)
    overlays = payload.get("overlays", [])
    if payload.get("overlay_count") != 36 or len(overlays) != 36:
        errors.append("Stage 5EH overlay count is not 36")
    for overlay in overlays:
        if overlay.get("review_state") != "overlay_enriched_fact":
            errors.append(f"overlay {overlay.get('overlay_id')} does not use overlay_enriched_fact")
        if overlay.get("usable_for_decision_now") is not False:
            errors.append(f"overlay {overlay.get('overlay_id')} is usable for decision")
        if overlay.get("not_allowed_as") != ["proof", "route_seed", "execution_seed", "solve_claim"]:
            errors.append(f"overlay {overlay.get('overlay_id')} has wrong not_allowed_as list")
    return _result(errors, overlay_count=len(overlays))


def validate_stage5eh_source_browser_loadability() -> ValidationResult:
    record = _read_record("source_browser_loadability_summary")
    errors = _false_guardrail_errors(record)
    if record.get("source_browser_validation_error_count") != 0:
        errors.append("Source Browser validation errors remain after Stage 5EH")
    if record.get("source_browser_loadability_preserved") is not True:
        errors.append("Source Browser loadability not preserved")
    return _result(errors, source_browser_entries_loaded=record.get("source_browser_entries_loaded", 0))


def validate_stage5eh_current_truth_doc_staleness() -> ValidationResult:
    record = _read_record("current_truth_doc_staleness_guard_evidence")
    errors = _false_guardrail_errors(record)
    if record.get("stage5eg_doc_staleness_scanner_preserved") is not True:
        errors.append("Stage 5EG doc-staleness scanner not preserved")
    if record.get("stale_current_claim_strict_errors_after_stage5eh") != 0:
        errors.append("stale-current strict errors remain")
    if record.get("current_stage_state_authoritative") is not True:
        errors.append("current-stage-state authority not preserved")
    return _result(errors, stale_current_errors=record.get("stale_current_claim_strict_errors_after_stage5eh", 0))


def validate_stage5eh_sidecar_gates() -> ValidationResult:
    errors: list[str] = []
    for key in [
        "stage5bd_plan_preservation",
        "active_lineage_preservation",
        "no_active_ingestion_proof",
        "no_byte_stream_transition_gate",
        "no_execution_transition_gate",
        "token_block_static_context_preservation",
    ]:
        record = _read_record(key)
        errors.extend(_false_guardrail_errors(record))
        if record.get("stage5bd_run_plan_ids_preserved") is not True:
            errors.append(f"{key} does not preserve Stage 5BD run-plan IDs")
    return _result(errors, sidecar_gate_record_count=6)


def validate_stage5eh_handoff_continuity() -> ValidationResult:
    record = _read_record("codex_handoff_policy")
    errors = _false_guardrail_errors(record)
    if record.get("completion_summary_path") != "codex-output/stage5eh-codex-completion.md":
        errors.append("Stage 5EH handoff path mismatch")
    if record.get("codex_output_committed") is not False:
        errors.append("Stage 5EH codex-output handoff is marked committed")
    return _result(errors, handoff_path=record.get("completion_summary_path"))


def validate_stage5eh_governance_scope() -> ValidationResult:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        if path.exists():
            errors.extend(f"{key}: {error}" for error in _false_guardrail_errors(read_yaml(path)))
    summary = _read_record("summary")
    if summary.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("Stage 5EH summary does not route to Stage 5EI")
    if summary.get("target_priority_decision_created_now") is not False:
        errors.append("target-priority decision was created")
    return _result(errors, governance_records_checked=len(DATA_PATHS))


def stage5eh_summary_text() -> str:
    summary = _read_record("summary")
    lines = [
        f"stage_id={summary.get('stage_id')}",
        f"status={summary.get('status')}",
        f"lag5_file_inventory_count={summary.get('lag5_file_inventory_count')}",
        f"lag5_event_list_row_count={summary.get('lag5_event_list_row_count')}",
        f"lp_outguessed_signed_output_count={summary.get('lp_outguessed_signed_output_count')}",
        f"xor_txt_local_file_present={summary.get('xor_txt_local_file_present')}",
        f"future_probe_manifest_count={summary.get('future_probe_manifest_count')}",
        f"overlay_count={summary.get('overlay_count')}",
        f"reviewability_gap_count={summary.get('reviewability_gap_count')}",
        f"source_browser_validation_error_count={summary.get('source_browser_validation_error_count')}",
        f"stale_current_claim_strict_errors_after_stage5eh={summary.get('stale_current_claim_strict_errors_after_stage5eh')}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


def _inventory() -> dict[str, Any]:
    lag5_files = [_file_record(LAG5_ROOT / name) for name in EXPECTED_LAG5_FILES]
    event_path = LAG5_ROOT / "second pair runes.txt"
    event_lines = event_path.read_text(encoding="utf-8").splitlines() if event_path.exists() else []
    lp_files = sorted(p for p in LP_OUTGUESSED_ROOT.glob("*") if p.is_file()) if LP_OUTGUESSED_ROOT.exists() else []
    expected_signed = [_file_record(LP_OUTGUESSED_ROOT / name) for name in EXPECTED_SIGNED_OUTPUTS]
    canonical_xor = LP_OUTGUESSED_ROOT / "xor.txt"
    duplicate_xor = [
        _file_record(path)
        for path in sorted(Path("third_party").glob("**/xor.txt"))
        if path.resolve() != canonical_xor.resolve()
    ]
    byte_source = _file_record(BYTE_STRINGS_SOURCE)
    page_images = {name: _file_record(FULL_IMAGES_ROOT / name) for name in ["13.jpg", "54.jpg", "55.jpg"]}
    return {
        "lag5_files": lag5_files,
        "lag5_event_header": event_lines[0] if event_lines else "",
        "lag5_event_row_count": max(0, len(event_lines) - 1),
        "lp_outguessed_file_count": len(lp_files),
        "lp_outguessed_txt_file_count": sum(1 for path in lp_files if path.suffix.lower() == ".txt"),
        "lp_outguessed_jpg_file_count": sum(1 for path in lp_files if path.suffix.lower() in {".jpg", ".jpeg"}),
        "expected_signed_outputs": expected_signed,
        "expected_signed_present_count": sum(1 for record in expected_signed if record["present"]),
        "canonical_xor": _file_record(canonical_xor),
        "duplicate_xor_candidates": duplicate_xor,
        "byte_source": byte_source,
        "page_images": page_images,
    }


def _records(
    inventory: dict[str, Any],
    source_browser: dict[str, Any],
    stale_counts: dict[str, int],
) -> dict[str, Any]:
    common = _common()
    overlays = _overlays(inventory)
    gaps = _reviewability_gaps(inventory)
    probe_records = _probe_records()
    source_paths = [
        DATA_PATHS["lag5_candidate_records"].as_posix(),
        DATA_PATHS["outguess_pgp_xor_records"].as_posix(),
        DATA_PATHS["byte_string_context_records"].as_posix(),
        DATA_PATHS["red_number_control_records"].as_posix(),
        DATA_PATHS["stegdetect_f5_signal_records"].as_posix(),
        DATA_PATHS["lp_outguessed_source_lock_register"].as_posix(),
        DATA_PATHS["byte_strings_context_crosswalk"].as_posix(),
        DATA_PATHS["page54_55_red_number_source_crosswalk"].as_posix(),
        DATA_PATHS["page13_stegdetect_operator_result_lock"].as_posix(),
    ]
    summary = {
        **common,
        "record_type": "stage5eh_summary",
        "schema": str(SCHEMA_PATHS["summary"]),
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "source_lock_only": True,
        "stage5eg_doc_staleness_scanner_preserved": True,
        "stage5ef_current_truth_authority_preserved": True,
        "stage5eb_10_worker_validation_policy_preserved": True,
        "lag5_source_lock_addendum_created": True,
        "lp_outguessed_source_lock_addendum_created": True,
        "byte_strings_crosslink_created": True,
        "page54_55_red_number_control_record_created": True,
        "page13_f5_detector_context_record_created": True,
        "diagnostic_probe_manifest_index_created": True,
        "source_browser_overlay_collection_created": True,
        "direct_source_record_number_fact_backfill_performed": False,
        "source_lock_records_created_now": True,
        "source_lock_records_metadata_only": True,
        "raw_source_files_committed": False,
        "lag5_file_inventory_count": sum(1 for record in inventory["lag5_files"] if record["present"]),
        "lag5_event_list_row_count": inventory["lag5_event_row_count"],
        "lag5_d1_count": 29,
        "lag5_d4_count": 28,
        "lag5_m_sum_claimed_or_reproduced": 479,
        "lp_outguessed_signed_output_count": inventory["expected_signed_present_count"],
        "xor_txt_local_file_present": inventory["canonical_xor"]["present"],
        "outguess03_jpeg_transcript_fact_card_created": True,
        "byte_string_crosslink_status": "stage5bk_crosslinked_metadata_only",
        "page54_55_red_number_block_status": "metadata_only_review_candidate",
        "page13_f5_detector_status": "operator_supplied_detector_signal_context_only",
        "page13_stegdetect_detail_beta": 1.368,
        "future_probe_manifest_count": len(probe_records),
        "overlay_count": len(overlays),
        "reviewability_gap_count": len(gaps),
        "source_browser_entries_loaded": source_browser["source_browser_entries_loaded"],
        "source_browser_validation_error_count": source_browser["source_browser_validation_error_count"],
        "stale_current_claim_strict_errors_after_stage5eh": stale_counts["stale_current_error_count"],
        "stale_current_claim_warning_count_after_stage5eh": stale_counts["stale_current_warning_count"],
        "full_serial_pytest_run": False,
        "full_parallel_validation_workers": 10,
        "full_parallel_validation_pytest_workers": 10,
    }
    records: dict[str, Any] = {
        "summary": summary,
        "next_stage_decision": {
            **common,
            "record_type": "stage5eh_next_stage_decision",
            "schema": str(SCHEMA_PATHS["next_stage_decision"]),
            "source_previous_stage": PREVIOUS_STAGE_ID,
            "current_stage_id": STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "number_fact_review_batch_006_deferred_to_stage5ei": True,
            "lag5_source_lock_completed_as_metadata_only": True,
        },
        "stage5eg_preservation": _preservation_record(common, "stage5eg_preservation", PREVIOUS_STAGE_ID, PREVIOUS_STAGE_TITLE),
        "stage5ef_preservation": {
            **common,
            "record_type": "stage5eh_stage5ef_preservation",
            "schema": str(SCHEMA_PATHS["stage5ef_preservation"]),
            "preserved_stage_id": "stage-5ef",
            "current_stage_state_authoritative": True,
            "markdown_docs_are_mirrors_or_historical_evidence": True,
        },
        "stage5eb_validation_policy_preservation": {
            **common,
            "record_type": "stage5eh_stage5eb_validation_policy_preservation",
            "schema": str(SCHEMA_PATHS["stage5eb_validation_policy_preservation"]),
            "stage5eb_10_worker_validation_policy_preserved": True,
            "old_8_worker_cap": False,
            "old_16_worker_default_reintroduced": False,
            "full_serial_pytest_required_for_normal_completion": False,
            "full_parallel_validation_workers": 10,
            "full_parallel_validation_pytest_workers": 10,
        },
        "recent_source_lock_register": {
            **common,
            "record_type": "stage5eh_recent_source_lock_register",
            "schema": str(SCHEMA_PATHS["recent_source_lock_register"]),
            "source_lock_register_status": "metadata_only_addendum",
            "source_roots": [LAG5_ROOT.as_posix(), IDDQD_ROOT.as_posix()],
            "source_lock_record_paths": [
                DATA_PATHS["lag5_local_source_lock_register"].as_posix(),
                DATA_PATHS["lp_outguessed_source_lock_register"].as_posix(),
                DATA_PATHS["byte_strings_context_crosswalk"].as_posix(),
                DATA_PATHS["page54_55_red_number_source_crosswalk"].as_posix(),
                DATA_PATHS["page13_stegdetect_operator_result_lock"].as_posix(),
            ],
            "historical_source_lock_records_rewritten": False,
        },
        "diagnostic_probe_manifest_index": {
            **common,
            "record_type": "stage5eh_diagnostic_probe_manifest_index",
            "schema": str(SCHEMA_PATHS["diagnostic_probe_manifest_index"]),
            "probe_manifest_count": len(probe_records),
            "probe_ids": [record["probe_id"] for record in probe_records],
            "all_probes_run_now": False,
            "probe_records_path": DATA_PATHS["diagnostic_probe_manifest_records"].as_posix(),
        },
        "enriched_fact_card_batch_result": {
            **common,
            "record_type": "stage5eh_enriched_fact_card_batch_result",
            "schema": str(SCHEMA_PATHS["enriched_fact_card_batch_result"]),
            "review_batch_id": "stage5eh_recent_lag5_outguess_byte_control",
            "overlay_count": len(overlays),
            "overlay_file": DATA_PATHS["overlay_collection"].as_posix(),
            "facts_added_directly_to_source_records": False,
            "facts_added_as_overlays": True,
            "review_result_status": "overlay_enrichment_complete",
        },
        "source_browser_loadability_summary": {
            **common,
            "record_type": "stage5eh_source_browser_loadability_summary",
            "schema": str(SCHEMA_PATHS["source_browser_loadability_summary"]),
            **source_browser,
        },
        "current_truth_doc_staleness_guard_evidence": {
            **common,
            "record_type": "stage5eh_current_truth_doc_staleness_guard_evidence",
            "schema": str(SCHEMA_PATHS["current_truth_doc_staleness_guard_evidence"]),
            "stage5eg_doc_staleness_scanner_preserved": True,
            "stale_current_claim_strict_errors_after_stage5eh": stale_counts["stale_current_error_count"],
            "stale_current_claim_warning_count_after_stage5eh": stale_counts["stale_current_warning_count"],
            "current_stage_state_authoritative": True,
            "broad_doc_churn_avoided": True,
        },
        "reviewable_validation_evidence": {
            **common,
            "record_type": "stage5eh_reviewable_validation_evidence",
            "schema": str(SCHEMA_PATHS["reviewable_validation_evidence"]),
            "focused_validators": [
                "validate-stage5eh",
                "validate-stage5eh-lag5-inventory",
                "validate-stage5eh-lp-outguessed-inventory",
                "validate-stage5eh-number-fact-overlays",
                "validate-stage5eh-source-browser-loadability",
            ],
            "stage_fast_required": True,
            "local_fast_required": True,
            "full_parallel_required_workers": 10,
            "full_parallel_required_pytest_workers": 10,
            "full_serial_pytest_run": False,
        },
        "reviewability_gap_register": {
            **common,
            "record_type": "stage5eh_reviewability_gap_register",
            "schema": str(SCHEMA_PATHS["reviewability_gap_register"]),
            "reviewability_gap_count": len(gaps),
            "canonical_xor_txt_reviewability_gap": not inventory["canonical_xor"]["present"],
            "gaps": gaps,
        },
        "chatgpt_context_update_summary": {
            **common,
            "record_type": "stage5eh_chatgpt_context_update_summary",
            "schema": str(SCHEMA_PATHS["chatgpt_context_update_summary"]),
            "chatgpt_context_updated": True,
            "current_stage_context_mentions_stage5eh": True,
            "recommended_next_stage_mentions_stage5ei": True,
        },
        "scope_control": {
            **common,
            "record_type": "stage5eh_scope_control",
            "schema": str(SCHEMA_PATHS["scope_control"]),
            "metadata_source_lock_reviewability_only": True,
            "puzzle_execution_allowed": False,
            "target_priority_decision_created_now": False,
            "pivot_target_selected_now": False,
            "route_extraction_authorized_now": False,
        },
        "lag5_local_source_lock_register": {
            **common,
            "record_type": "stage5eh_lag5_local_source_lock_register",
            "schema": str(SCHEMA_PATHS["lag5_local_source_lock_register"]),
            "source_root": LAG5_ROOT.as_posix(),
            "source_root_present": LAG5_ROOT.exists(),
            "expected_file_count": len(EXPECTED_LAG5_FILES),
            "expected_file_count_present": sum(1 for record in inventory["lag5_files"] if record["present"]),
            "files": inventory["lag5_files"],
            "raw_file_bodies_committed": False,
        },
        "lag5_file_inventory": {
            **common,
            "record_type": "stage5eh_lag5_file_inventory",
            "schema": str(SCHEMA_PATHS["lag5_file_inventory"]),
            "source_root": LAG5_ROOT.as_posix(),
            "expected_filenames": EXPECTED_LAG5_FILES,
            "expected_file_count_present": sum(1 for record in inventory["lag5_files"] if record["present"]),
            "event_list_header": inventory["lag5_event_header"],
            "event_list_observed_row_count": inventory["lag5_event_row_count"],
            "files": inventory["lag5_files"],
        },
        "lp_outguessed_source_lock_register": _lp_outguessed_record(common, inventory),
        "lp_outguessed_pgp_signed_output_inventory": _pgp_inventory_record(common, inventory),
        "cicada_solvers_iddqd_v2_crosswalk": _iddqd_crosswalk_record(common, inventory),
        "byte_strings_context_crosswalk": _byte_strings_crosswalk_record(common, inventory),
        "page54_55_red_number_source_crosswalk": _red_number_crosswalk_record(common, inventory),
        "page13_stegdetect_operator_result_lock": _page13_lock_record(common, inventory),
        "codex_handoff_policy": {
            **common,
            "record_type": "stage5eh_codex_handoff_policy",
            "schema": str(SCHEMA_PATHS["codex_handoff_policy"]),
            "completion_summary_path": "codex-output/stage5eh-codex-completion.md",
            "codex_output_committed": False,
            "post_push_handoff_required": True,
        },
        "credential_redaction_policy_preservation": {
            **common,
            "record_type": "stage5eh_credential_redaction_policy_preservation",
            "schema": str(SCHEMA_PATHS["credential_redaction_policy_preservation"]),
            "credential_redaction_policy_preserved": True,
            "secrets_committed": False,
        },
        "raw_source_noncommit_proof": {
            **common,
            "record_type": "stage5eh_raw_source_noncommit_proof",
            "schema": str(SCHEMA_PATHS["raw_source_noncommit_proof"]),
            "third_party_raw_files_staged": False,
            "data_raw_files_staged": False,
            "experiments_results_staged": False,
            "codex_output_staged": False,
            "raw_source_files_committed": False,
            "raw_third_party_files_committed": False,
        },
        "lag5_candidate_records": _lag5_records(common, inventory),
        "outguess_pgp_xor_records": _outguess_records(common, inventory),
        "byte_string_context_records": _byte_string_records(common),
        "red_number_control_records": _red_number_records(common, inventory),
        "stegdetect_f5_signal_records": _stegdetect_records(common, inventory),
        "stage5bd_plan_preservation": _gate_record(common, "stage5bd_plan_preservation"),
        "active_lineage_preservation": _gate_record(common, "active_lineage_preservation"),
        "no_active_ingestion_proof": _gate_record(common, "no_active_ingestion_proof"),
        "no_byte_stream_transition_gate": _gate_record(common, "no_byte_stream_transition_gate"),
        "no_execution_transition_gate": _gate_record(common, "no_execution_transition_gate"),
        "token_block_static_context_preservation": _gate_record(common, "token_block_static_context_preservation"),
        "diagnostic_probe_manifest_records": {
            **common,
            "record_type": "stage5eh_diagnostic_probe_manifest_records",
            "schema": str(SCHEMA_PATHS["diagnostic_probe_manifest_records"]),
            "probe_manifest_count": len(probe_records),
            "all_run_now_false": True,
            "records": probe_records,
        },
        "overlay_collection": {
            **common,
            "record_type": "stage5eh_source_browser_number_fact_enrichment_overlay_collection",
            "schema": str(SCHEMA_PATHS["overlay_collection"]),
            "review_batch_id": "stage5eh_recent_lag5_outguess_byte_control",
            "review_batch_selection_policy": "metadata_only_recent_lag5_outguess_byte_control_addendum",
            "reviewed_entry_count": len(source_paths),
            "overlay_count": len(overlays),
            "overlay_only_fact_cards_supported_required": True,
            "review_state": "overlay_enriched_fact",
            "selected_source_record_paths": source_paths,
            "overlays": overlays,
        },
        "review_batch_result": {
            **common,
            "record_type": "source_browser_number_fact_review_batch_result",
            "schema": str(SCHEMA_PATHS["review_batch_result"]),
            "review_batch_id": "stage5eh_recent_lag5_outguess_byte_control",
            "review_batch_selection_policy": "metadata_only_recent_lag5_outguess_byte_control_addendum",
            "reviewed_entry_count": len(source_paths),
            "overlay_count": len(overlays),
            "overlays_added_now": True,
            "historical_source_lock_records_rewritten": False,
            "source_lock_evidence_updated_now": False,
            "number_fact_backfill_performed_now": False,
            "review_scope": "selected_recent_lag5_outguess_byte_control_records_only",
            "review_result_status": "overlay_enrichment_complete",
            "selected_source_record_paths": source_paths,
            "overlay_file": DATA_PATHS["overlay_collection"].as_posix(),
            "facts_added_directly_to_source_records": False,
            "facts_added_as_overlays": True,
        },
    }
    return records


def _common() -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "reviewability_stage": True,
        "number_fact_review_batch_stage": False,
        "puzzle_execution_allowed": False,
        "canonical_codex_handoff_root": "codex-output",
        "status": "complete",
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        **FALSE_GUARDRAILS,
    }


def _preservation_record(common: dict[str, Any], key: str, stage_id: str, stage_title: str) -> dict[str, Any]:
    return {
        **common,
        "record_type": f"stage5eh_{key}",
        "schema": str(SCHEMA_PATHS[key]),
        "preserved_stage_id": stage_id,
        "preserved_stage_title": stage_title,
        "stage5eg_doc_staleness_scanner_preserved": True,
        "stage5eg_final_commit": PREVIOUS_STAGE_COMMIT,
        "stage5eg_ci_run": PREVIOUS_STAGE_CI_RUN,
        "stage5eg_ci_status": PREVIOUS_STAGE_CI_STATUS,
    }


def _lp_outguessed_record(common: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    canonical = inventory["canonical_xor"]
    return {
        **common,
        "record_type": "stage5eh_lp_outguessed_source_lock_register",
        "schema": str(SCHEMA_PATHS["lp_outguessed_source_lock_register"]),
        "source_root": LP_OUTGUESSED_ROOT.as_posix(),
        "source_root_present": LP_OUTGUESSED_ROOT.exists(),
        "lp_outguessed_inventory_performed_before_records": True,
        "lp_outguessed_xor_txt_local_presence_checked": True,
        "lp_outguessed_file_count": inventory["lp_outguessed_file_count"],
        "lp_outguessed_txt_file_count": inventory["lp_outguessed_txt_file_count"],
        "lp_outguessed_jpg_file_count": inventory["lp_outguessed_jpg_file_count"],
        "lp_outguessed_expected_pgp_signed_output_count": 8,
        "expected_pgp_signed_output_present_count": inventory["expected_signed_present_count"],
        "expected_pgp_signed_outputs": inventory["expected_signed_outputs"],
        "pgp_signature_key_id_observed_prior": "181F01E57A35090F",
        "pgp_short_key_id_observed_prior": "7A35090F",
        "pgp_signature_verification_status": "key_missing_or_not_verified_now",
        "pgp_verification_performed_now": False,
        "outguess_xor_share_count": 3,
        "outguess_xor_share_hex_payload_length_bytes_prior_observed": 991,
        "outguess_xor_reconstruction_performed_now": False,
        "xor_txt_local_file_present": canonical["present"],
        "lp_outguessed_xor_txt_source_locked_from_local_file": canonical["present"],
        "lp_outguessed_xor_txt_reviewability_gap": not canonical["present"],
        "xor_txt_exact_hash_recorded": bool(canonical["present"] and canonical.get("sha256")),
        "xor_txt_reconstructed_now": False,
        "xor_txt_synthesized_now": False,
        "xor_txt_raw_body_committed": False,
        "xor_txt_canonical_record": canonical,
        "duplicate_or_old_xor_txt_candidate_paths": inventory["duplicate_xor_candidates"],
    }


def _pgp_inventory_record(common: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5eh_lp_outguessed_pgp_signed_output_inventory",
        "schema": str(SCHEMA_PATHS["lp_outguessed_pgp_signed_output_inventory"]),
        "expected_output_count": 8,
        "present_output_count": inventory["expected_signed_present_count"],
        "expected_outputs": inventory["expected_signed_outputs"],
        "pgp_signature_verification_status": "key_missing_or_not_verified_now",
        "pgp_verification_performed_now": False,
        "raw_signed_output_bodies_committed": False,
    }


def _iddqd_crosswalk_record(common: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5eh_cicada_solvers_iddqd_v2_crosswalk",
        "schema": str(SCHEMA_PATHS["cicada_solvers_iddqd_v2_crosswalk"]),
        "source_root": IDDQD_ROOT.as_posix(),
        "source_root_present": IDDQD_ROOT.exists(),
        "canonical_lp_outguessed_root": LP_OUTGUESSED_ROOT.as_posix(),
        "stage5bk_local_source_root_record": "data/historical-route/stage5bk-iddqd-v2-local-source-root.yaml",
        "stage5bk_byte_strings_source_lock_record": "data/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock.yaml",
        "crosslink_families": CROSSLINK_FAMILIES,
        "target_priority_decision_created_now": False,
    }


def _byte_strings_crosswalk_record(common: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5eh_byte_strings_context_crosswalk",
        "schema": str(SCHEMA_PATHS["byte_strings_context_crosswalk"]),
        "byte_strings_source_root": "third_party/CiadaSolversIddqd_v2/byte-strings",
        "byte_strings_source_file": inventory["byte_source"],
        "stage5bk_source_lock_record": "data/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock.yaml",
        "stage5bk_record_id": "stage5bk_iddqd_v2_byte_strings_source_lock_set",
        "byte_string_count": 4,
        "exact_512_hex_string_count": 4,
        "decoded_byte_length_each": 256,
        "string_roles": _byte_string_roles(),
        "byte_strings_are_not_ordinary_magic_squares_row_sum_control": True,
        "byte_strings_simple_xor_solved_now": False,
        "byte_strings_direct_decode_validated_now": False,
        "byte_strings_real_byte_stream_generated_now": False,
        "byte_strings_used_as_execution_seed_now": False,
    }


def _red_number_crosswalk_record(common: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5eh_page54_55_red_number_source_crosswalk",
        "schema": str(SCHEMA_PATHS["page54_55_red_number_source_crosswalk"]),
        "source_images": [inventory["page_images"]["54.jpg"], inventory["page_images"]["55.jpg"]],
        "candidate_record_path": DATA_PATHS["red_number_control_records"].as_posix(),
        "metadata_only_image_presence_checked": True,
        "ocr_performed": False,
        "image_forensics_performed": False,
    }


def _page13_lock_record(common: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5eh_page13_stegdetect_operator_result_lock",
        "schema": str(SCHEMA_PATHS["page13_stegdetect_operator_result_lock"]),
        "page13_image_metadata": inventory["page_images"]["13.jpg"],
        "page13_stegdetect_result_source": "operator_supplied_external_run",
        "page13_stegdetect_raw_log_fragment": "f5[1.368187]",
        "page13_stegdetect_detail_beta": 1.368,
        "stegdetect_execution_performed_now": False,
        "f5_extraction_performed_now": False,
        "f5_password_search_performed_now": False,
        "detector_result_only": True,
    }


def _lag5_records(common: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5eh_lag5_candidate_records",
        "schema": str(SCHEMA_PATHS["lag5_candidate_records"]),
        "lag5_marker_definition": "M[i] = 1 iff C[i] = C[i+5]",
        "lag_value": 5,
        "d1_definition": "M[i] = M[i+1] = 1; adjacent pair repeats 5 later",
        "d4_definition": "M[i] = M[i+4] = 1; endpoint-spaced pair repeats 5 later",
        "d1_count": 29,
        "d4_count": 28,
        "d1_plus_d4_event_count": 57,
        "event_list_expected_row_count": 57,
        "event_list_observed_row_count": inventory["lag5_event_row_count"],
        "lag5_m_sum_claimed_or_reproduced": 479,
        "unsolved_corpus_rune_count_claimed_or_reproduced": 12956,
        "lag5_d_counts": {"d1": 29, "d2": 15, "d3": 14, "d4": 28, "d5": 19, "d6": 15},
        "lag5_fourth_order_correlation_candidate": True,
        "ordinary_period5_cipher_claimed_now": False,
        "validated_cipher_mechanism_now": False,
        "statistical_significance_modest": True,
        "wide_nuisance_parameter_search_weakens_global_significance": True,
        "requires_exact_corpus_boundary": True,
        "requires_doublet_suppressed_null_model": True,
        "requires_independent_reproduction_from_canonical_transcription": True,
        "not_target_priority_evidence_alone": True,
        "not_solve_evidence": True,
        "candidate_records": [
            _candidate("lag5_paired_copy_anomaly_candidate_v0", "Lag5 paired copy anomaly", "lag5_review_only"),
            _candidate("lag5_57_event_source_lock_v0", "57-event d1+d4 source lock", "lag5_review_only"),
            _candidate("lag5_raw_frequency_source_lock_v0", "Raw frequency-data source lock", "lag5_review_only"),
            _candidate("lag5_d1_d4_fourth_order_correlation_candidate_v0", "d1/d4 fourth-order correlation", "lag5_review_only"),
            _candidate("lag5_doublet_suppressed_null_warning_v0", "Doublet-suppressed null requirement", "null_control_required"),
            _candidate("lag5_holdout_nuisance_warning_v0", "Holdout and nuisance-search warning", "reviewability_warning"),
            _candidate("lag5_copy_semantics_candidate_v0", "Copy semantics candidate", "lag5_review_only"),
            _candidate("lag5_backreference_stutter_candidate_v0", "Backreference/stutter candidate", "lag5_review_only"),
            _candidate("lag5_token_block_cluster_context_v0", "Token-block cluster bridge", "crosslink_context"),
            _candidate("lag5_pdd153_56311_distance5_bridge_v0", "PDD153/56311 distance-5 bridge", "crosslink_context"),
            _candidate("lag5_disk_doublet_model_context_v0", "Disk doublet model bridge", "crosslink_context"),
            _candidate("lag5_page32_diagnostic_context_v0", "Page32 diagnostic bridge", "crosslink_context"),
            _candidate("lag5_negative_space_bridge_v0", "Negative-space bridge", "crosslink_context"),
        ],
    }


def _outguess_records(common: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    canonical = inventory["canonical_xor"]
    return {
        **common,
        "record_type": "stage5eh_outguess_pgp_xor_records",
        "schema": str(SCHEMA_PATHS["outguess_pgp_xor_records"]),
        "lp_outguessed_expected_pgp_signed_output_count": 8,
        "pgp_signature_key_id_observed_prior": "181F01E57A35090F",
        "pgp_short_key_id_observed_prior": "7A35090F",
        "pgp_signature_verification_status": "key_missing_or_not_verified_now",
        "pgp_verification_performed_now": False,
        "outguess_xor_share_count": 3,
        "outguess_xor_share_hex_payload_length_bytes_prior_observed": 991,
        "outguess_xor_reconstruction_performed_now": False,
        "xor_txt_local_file_present": canonical["present"],
        "xor_txt_exact_local_source_gap": not canonical["present"],
        "xor_txt_observed_prior_ciphertext_length": 70,
        "xor_txt_observed_prior_grouping": "14 groups of 5",
        "xor_txt_observed_prior_digit_symbols": [4, 5, 7],
        "xor_txt_possible_29_symbol_alphabet_candidate": True,
        "xor_txt_decode_attempt_performed_now": False,
        "outguess03_jpeg_transcription": _outguess03_record(),
        "candidate_records": [
            _candidate("outguess_pgp_signed_family_candidate_v0", "Expected signed output family", "source_lock_context"),
            _candidate("outguess_00_01_02_xor_context_v0", "00/01/02 XOR-share precedent", "source_lock_context"),
            _candidate("outguess_xor_txt_signed_ciphertext_gap_v0", "xor.txt signed ciphertext surface gap", "reviewability_gap"),
            _candidate("outguess_03_jpeg_gp_transcription_v0", "03 JPEG GP transcription context", "operator_supplied_review"),
            _candidate("outguess_03_mod29_zero_candidate_v0", "03 index-sum neutral sequence", "review_only_numeric_candidate"),
            _candidate("outguess_03_digit_split_candidate_v0", "03 literal digit split candidate", "review_only_numeric_candidate"),
            _candidate("outguess_magic_square_tor_instruction_context_v0", "Magic-square Tor instruction context", "source_lock_context"),
            _candidate("outguess_magic_square_0_1_3_distinct_set_v0", "Magic-square 0/1/3 distinct set context", "review_only_context"),
            _candidate("outguess_pgp_key_id_context_v0", "PGP key ID verification gap", "reviewability_gap"),
            _candidate("outguess_staged_intermediate_model_v0", "Staged intermediate model", "review_only_context"),
        ],
    }


def _outguess03_record() -> dict[str, Any]:
    return {
        "outguess03_jpeg_transcription_source": "operator_supplied_human_transcription",
        "outguess03_jpeg_transcription_review_status": "requires_human_review",
        "outguess03_ocr_performed_now": False,
        "outguess03_image_forensics_performed_now": False,
        "outguess03_literal_digit_markers": [5, 3],
        "outguess03_rune_gp_prime_values": OUTGUESS03_GP_VALUES,
        "outguess03_rune_token_count": 18,
        "outguess03_visible_item_count_including_digits": 20,
        "outguess03_segment_lengths_between_literal_digits": [8, 5, 5],
        "outguess03_rune_zero_based_index_sum": 261,
        "outguess03_index_sum_factorization": "9 * 29",
        "outguess03_index_sum_mod29": 0,
        "outguess03_rune_gp_prime_sum": 990,
        "outguess03_segment_index_sums": [103, 72, 86],
        "outguess03_segment_prime_sums": [387, 273, 330],
        "outguess03_control_key_candidate": True,
        "outguess03_digit_split_candidate": True,
        "outguess03_mod29_neutral_sequence_candidate": True,
        "outguess03_used_to_decode_now": False,
        "outguess03_key_or_route_accepted_now": False,
        "not_solve_evidence": True,
    }


def _byte_string_records(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5eh_byte_string_context_records",
        "schema": str(SCHEMA_PATHS["byte_string_context_records"]),
        "byte_strings_source_root": "third_party/CiadaSolversIddqd_v2/byte-strings",
        "byte_string_count": 4,
        "exact_512_hex_string_count": 4,
        "decoded_byte_length_each": 256,
        "string_roles": _byte_string_roles(),
        "stage5bk_source_lock_record": "data/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock.yaml",
        "byte_strings_are_not_ordinary_magic_squares_row_sum_control": True,
        "byte_strings_simple_xor_solved_now": False,
        "byte_strings_direct_decode_validated_now": False,
        "byte_strings_real_byte_stream_generated_now": False,
        "byte_strings_used_as_execution_seed_now": False,
        "future_probe_ids": [
            "byte_strings_outguess_xor_precedent_comparison_probe_candidate_v0",
            "byte_strings_03_control_key_probe_candidate_v0",
            "byte_strings_16x16_matrix_route_mask_probe_candidate_v0",
            "byte_strings_token_block_matrix_comparison_probe_candidate_v0",
        ],
    }


def _red_number_records(common: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5eh_red_number_control_records",
        "schema": str(SCHEMA_PATHS["red_number_control_records"]),
        "page54_55_red_numbered_line_blocks_candidate_v0": {
            "source_images": [inventory["page_images"]["54.jpg"], inventory["page_images"]["55.jpg"]],
            "page54_red_numbers_observed_by_assistant_or_operator": [2, 3, 4],
            "page55_red_numbers_observed_by_operator": [5],
            "large_vertical_margin_around_numbered_blocks_observed_by_operator": True,
            "line_blocks_start_with_red_arabic_numeral_candidate": True,
            "arabic_numeral_control_token_candidate": True,
            "page55_direct_visual_verification_status": "verify_metadata_only_or_pending",
            "not_same_as_a_postlude_red_heading_theory": True,
            "red_number_role_unknown": True,
            "route_control_not_accepted_now": True,
            "future_probe_id": "page54_55_red_numbered_line_block_transcript_alignment_probe_candidate_v0",
            "run_now": False,
        },
    }


def _stegdetect_records(common: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5eh_stegdetect_f5_signal_records",
        "schema": str(SCHEMA_PATHS["stegdetect_f5_signal_records"]),
        "page13_stegdetect_f5_beta_signal_candidate_v0": {
            "page13_image_metadata": inventory["page_images"]["13.jpg"],
            "page13_stegdetect_result_source": "operator_supplied_external_run",
            "stegdetect_execution_performed_now": False,
            "f5_extraction_performed_now": False,
            "f5_password_search_performed_now": False,
            "page13_stegdetect_f5_signal_observed": True,
            "page13_stegdetect_raw_log_fragment": "f5[1.368187]",
            "page13_stegdetect_detail_beta": 1.368,
            "page13_known_lp_outguessed_output_context": True,
            "page13_lp_outguessed_13_txt_present_if_local_inventory_confirms": (LP_OUTGUESSED_ROOT / "13.txt").exists(),
            "page13_f5_signal_may_be_outguess_or_jpeg_stego_cross_hit": True,
            "page13_f5_signal_not_proof_of_second_payload": True,
            "not_proof_of_f5_payload": True,
            "detector_result_only": True,
            "canonical_image_required": True,
            "uploaded_image_may_be_recompressed": True,
            "known_outguess_payload_confound": True,
            "f5_extraction_not_authorized_now": True,
            "password_search_not_authorized_now": True,
            "no_solve_claim": True,
        },
        "context_records": [
            "page13_known_outguess_output_crosslink_v0",
            "page13_star_artifacts_f5_bridge_candidate_v0",
            "page13_f5_vs_outguess_false_positive_warning_v0",
        ],
        "future_probe_ids": [
            "lp_pages_stegdetect_baseline_probe_manifest_v0",
            "known_outguessed_pages_stegdetect_comparison_probe_manifest_v0",
            "star_artifact_mod8_dct_residue_probe_manifest_v0",
            "page13_canonical_image_hash_and_detector_reproduction_probe_manifest_v0",
        ],
    }


def _gate_record(common: dict[str, Any], key: str) -> dict[str, Any]:
    return {
        **common,
        "record_type": f"stage5eh_{key}",
        "schema": str(SCHEMA_PATHS[key]),
        "stage5bd_run_plan_ids_preserved": True,
        "stage5bd_active_lineage_preserved": True,
        "active_planning_input_authorized_now": False,
        "active_ingestion_performed": False,
        "byte_stream_generation_authorized_now": False,
        "execution_authorized_now": False,
        "token_block_experiment_executed": False,
        "stage5eh_metadata_only_addendum": True,
    }


def _probe_records() -> list[dict[str, Any]]:
    return [
        {
            "record_type": "stage5eh_future_diagnostic_probe_manifest",
            "probe_id": probe_id,
            "run_now": False,
            "execution_enabled": False,
            "metadata_only": True,
            "solve_claim": False,
            "requires_future_authorization": True,
        }
        for probe_id in FUTURE_PROBE_IDS
    ]


def _reviewability_gaps(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    if not inventory["canonical_xor"]["present"]:
        gaps.append(
            {
                "gap_id": "stage5eh-canonical-lp-outguessed-xor-txt-missing",
                "gap_type": "missing_canonical_local_source_file",
                "canonical_path": (LP_OUTGUESSED_ROOT / "xor.txt").as_posix(),
                "duplicate_candidate_paths": [record["path"] for record in inventory["duplicate_xor_candidates"]],
                "future_probe_id": "outguess_00_01_02_xor_reconstruction_probe_candidate_v0",
                "run_now": False,
            }
        )
    for record in inventory["lag5_files"]:
        if not record["present"]:
            gaps.append({"gap_id": f"stage5eh-missing-lag5-{record['filename']}", "gap_type": "missing_expected_file"})
    return gaps


def _overlays(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    refs = {
        "lag5": DATA_PATHS["lag5_candidate_records"].as_posix(),
        "outguess": DATA_PATHS["outguess_pgp_xor_records"].as_posix(),
        "byte": DATA_PATHS["byte_string_context_records"].as_posix(),
        "red": DATA_PATHS["red_number_control_records"].as_posix(),
        "f5": DATA_PATHS["stegdetect_f5_signal_records"].as_posix(),
        "gap": DATA_PATHS["reviewability_gap_register"].as_posix(),
    }
    overlay_specs = [
        ("lag5_d1_d4_57", refs["lag5"], "lag5_counts", "Lag5 d1/d4 events: 29 + 28 = 57", [29, 28, 57], "high"),
        ("lag5_msum_12956", refs["lag5"], "lag5_msum", "Lag5 M-sum 479 over claimed N=12,956", [479, 12956], "high"),
        ("lag5_d_counts", refs["lag5"], "lag5_d_counts", "Lag5 control counts d1..d6 = 29/15/14/28/19/15", [29, 15, 14, 28, 19, 15], "high"),
        ("lag5_marker_definition", refs["lag5"], "lag5_marker", "Lag5 marker M[i] = 1 iff C[i] = C[i+5]", [5], "medium"),
        ("lag5_modest_significance", refs["lag5"], "lag5_warning", "Lag5 significance remains modest and nuisance-search sensitive", [57, 479], "quarantine"),
        ("lag5_null_model_required", refs["lag5"], "lag5_null", "Lag5 requires doublet-suppressed null controls", [5, 57], "high"),
        ("outguess_expected_signed_set", refs["outguess"], "outguess_signed_set", "Expected signed outputs: 00/01/02/03/10/11/12/13", [8], "high"),
        ("outguess_pgp_key_gap", refs["outguess"], "outguess_pgp_key", "PGP key 181F01E57A35090F / 7A35090F not verified now", [181, 35090, 7], "high"),
        ("outguess_xor_share_991", refs["outguess"], "outguess_xor_share", "00/01/02 prior XOR-share context reports 991-byte payloads", [3, 991], "medium"),
        ("xor_txt_canonical_status", refs["outguess"], "xor_txt_status", "Canonical lp_outguessed/xor.txt local presence checked before records", [70, 14, 5], "high"),
        ("xor_txt_prior_surface", refs["gap"], "xor_prior_surface", "Absent xor.txt preserves prior 70 chars / 14 groups of 5 / digits 4,5,7", [70, 14, 5, 4, 5, 7], "high"),
        ("xor_txt_duplicate_candidates", refs["gap"], "xor_duplicate_candidates", "Duplicate xor.txt candidates remain non-canonical reviewability context", [len(inventory["duplicate_xor_candidates"])], "medium"),
        ("outguess03_digit_split", refs["outguess"], "outguess03_digit_split", "03 JPEG transcription split is 8/5/5 with literal digits 5 and 3", [8, 5, 5, 5, 3], "high"),
        ("outguess03_index_sum", refs["outguess"], "outguess03_index_sum", "03 JPEG index sum 261 = 9 * 29 = 0 mod29", [261, 9, 29, 0], "high"),
        ("outguess03_prime_sum", refs["outguess"], "outguess03_prime_sum", "03 JPEG GP prime sum is 990", [990], "medium"),
        ("outguess03_segment_index_sums", refs["outguess"], "outguess03_segment_index_sums", "03 JPEG segment index sums are 103/72/86", [103, 72, 86], "medium"),
        ("outguess03_segment_prime_sums", refs["outguess"], "outguess03_segment_prime_sums", "03 JPEG segment prime sums are 387/273/330", [387, 273, 330], "medium"),
        ("outguess03_human_review_required", refs["outguess"], "outguess03_review", "03 JPEG transcription is operator supplied and requires human review", [18, 20], "high"),
        ("byte_strings_4x512", refs["byte"], "byte_strings_count", "Byte strings are 4 exact 512-hex / 256-byte surfaces", [4, 512, 256], "high"),
        ("byte_string4_token_block", refs["byte"], "byte_string4_token_block", "Byte string 4 crosslinks page49-51 matrix/token-block context", [4, 49, 51], "high"),
        ("byte_strings_magic_square_warning", refs["byte"], "byte_strings_magic_warning", "Byte strings are not ordinary magic-square row-sum controls", [4, 16, 16], "medium"),
        ("byte_strings_no_real_bytes", refs["byte"], "byte_strings_no_bytes", "Stage 5EH generates no real byte streams from byte strings", [0], "quarantine"),
        ("page54_red_numbers", refs["red"], "page54_red_numbers", "Page54 red numbered line blocks observed as 2/3/4", [54, 2, 3, 4], "high"),
        ("page55_red_number", refs["red"], "page55_red_number", "Page55 red numbered line block observed as 5", [55, 5], "high"),
        ("red_numbers_separate_postlude", refs["red"], "red_numbers_separate", "Page54/55 red numbers are separate from A POSTLUDE red-heading theory", [54, 55], "high"),
        ("red_numbers_margin_control", refs["red"], "red_number_margins", "Large vertical margins around numbered blocks remain review-only context", [54, 55], "medium"),
        ("arabic_numeral_control_family", refs["red"], "arabic_numerals", "Arabic numerals are a control-token family candidate, not accepted route controls", [2, 3, 4, 5], "medium"),
        ("page13_f5_beta", refs["f5"], "page13_f5_beta", "Page13 operator StegDetect signal: f5[1.368187], beta 1.368", [13, 1368], "high"),
        ("page13_known_outguess_confound", refs["f5"], "page13_outguess_confound", "Page13 has known lp_outguessed output context; F5 signal may be cross-hit", [13], "high"),
        ("page13_no_f5_extraction", refs["f5"], "page13_no_f5", "No F5 extraction, password search, or StegDetect execution is authorized now", [0], "quarantine"),
        ("page13_canonical_image_required", refs["f5"], "page13_canonical_image", "Page13 detector reproduction requires canonical image hash in a future probe", [13], "medium"),
        ("future_lag5_probes", DATA_PATHS["diagnostic_probe_manifest_records"].as_posix(), "lag5_future_probes", "Lag5 future probes are declared with run_now=false", [8], "medium"),
        ("future_outguess_probes", DATA_PATHS["diagnostic_probe_manifest_records"].as_posix(), "outguess_future_probes", "Outguess/PGP/XOR/03 probes are declared with run_now=false", [6], "medium"),
        ("future_byte_red_page13_probes", DATA_PATHS["diagnostic_probe_manifest_records"].as_posix(), "byte_red_f5_future_probes", "Byte/red/Page13 probes are declared with run_now=false", [9], "medium"),
        ("crosslink_family_count", DATA_PATHS["cicada_solvers_iddqd_v2_crosswalk"].as_posix(), "crosslinks", "Stage 5EH crosslinks 15 prior candidate families without target selection", [15], "medium"),
        ("stage5eh_no_backfill", DATA_PATHS["scope_control"].as_posix(), "scope_control", "Stage 5EH adds overlays only and performs no source-record backfill", [0], "quarantine"),
    ]
    return [
        _overlay(
            overlay_id=f"stage5eh_{overlay_id}_overlay",
            source_record_path=source_record_path,
            source_fact_id=source_fact_id,
            display_label=label,
            values=values,
            display_priority=priority,
        )
        for overlay_id, source_record_path, source_fact_id, label, values, priority in overlay_specs
    ]


def _overlay(
    *,
    overlay_id: str,
    source_record_path: str,
    source_fact_id: str,
    display_label: str,
    values: list[int],
    display_priority: str,
) -> dict[str, Any]:
    return {
        "record_type": "source_browser_number_fact_enrichment_overlay",
        "review_state": "overlay_enriched_fact",
        "usable_for_decision_now": False,
        "not_allowed_as": ["proof", "route_seed", "execution_seed", "solve_claim"],
        "overlay_id": overlay_id,
        "source_record_path": source_record_path,
        "source_fact_id": source_fact_id,
        "fact_class": "stage5eh_lag5_outguess_byte_control_review_fact",
        "display_label": display_label,
        "short_label": display_label[:80],
        "value": values[0] if values else 0,
        "values": values,
        "value_type": "sequence",
        "operation_type": "metadata_only_source_lock_context",
        "expression": display_label,
        "relation": "Review-only Stage 5EH context; not proof, not a route seed, and not execution evidence.",
        "why_stored": "Keeps high-value numeric/source-lock context visible in the Source Browser without mutating source records.",
        "verification_status": "metadata_only_or_operator_supplied_context",
        "display_priority": display_priority,
        "risk_notes": ["review_only", "no_execution", "no_solve_claim", "future_probe_required"],
    }


def _candidate(candidate_id: str, label: str, status: str) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "label": label,
        "review_state": status,
        "usable_for_decision_now": False,
        "target_priority_decision_created_now": False,
        "run_now": False,
        "not_solve_evidence": True,
    }


def _byte_string_roles() -> dict[str, str]:
    return {
        "string1_role": "Hidden Service 2 2014 byte surface",
        "string2_role": "Hidden Service 3 2014 byte surface",
        "string3_role": "Hidden Service 4 2014 byte surface",
        "string4_role": "Matrix from pages 49-51 converted to hexadecimal / token-block crosswalk",
    }


def _file_record(path: Path) -> dict[str, Any]:
    record: dict[str, Any] = {
        "path": path.as_posix(),
        "filename": path.name,
        "present": path.exists(),
        "raw_body_committed": False,
    }
    if not path.exists():
        return record
    record.update(
        {
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
            "mime_guess": mimetypes.guess_type(path.as_posix())[0] or "application/octet-stream",
            "line_count": _line_count(path) if path.suffix.lower() in {".txt", ".md", ".csv"} else None,
            "image_metadata": _image_metadata(path),
        }
    )
    return record


def _line_count(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8").splitlines())
    except UnicodeDecodeError:
        return 0


def _image_metadata(path: Path) -> dict[str, Any] | None:
    suffix = path.suffix.lower()
    try:
        if suffix == ".png":
            with path.open("rb") as handle:
                header = handle.read(24)
            if header.startswith(b"\x89PNG\r\n\x1a\n"):
                width, height = struct.unpack(">II", header[16:24])
                return {"format": "PNG", "width": width, "height": height}
        if suffix in {".jpg", ".jpeg"}:
            return _jpeg_dimensions(path)
    except OSError:
        return None
    return None


def _jpeg_dimensions(path: Path) -> dict[str, Any] | None:
    with path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            return None
        while True:
            marker_start = handle.read(1)
            if not marker_start:
                return None
            if marker_start != b"\xff":
                continue
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            if marker in {b"\xd8", b"\xd9"}:
                continue
            length_bytes = handle.read(2)
            if len(length_bytes) != 2:
                return None
            length = int.from_bytes(length_bytes, "big")
            if marker and marker[0] in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                data = handle.read(5)
                if len(data) != 5:
                    return None
                height = int.from_bytes(data[1:3], "big")
                width = int.from_bytes(data[3:5], "big")
                return {"format": "JPEG", "width": width, "height": height}
            handle.seek(max(0, length - 2), 1)


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


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        write_json(path, _schema_for(key, path))
    _extend_current_stage_state_schema()


def _schema_for(key: str, path: Path) -> dict[str, Any]:
    required = [
        "record_type",
        "schema",
        "stage_id",
        "status",
        "recommended_next_stage_id",
        "generated_outputs_committed",
        "solve_claim",
        "execution_performed",
        "cuda_execution_performed",
        "canonical_corpus_active",
        "page_boundaries_finalized",
    ]
    properties: dict[str, Any] = {
        "record_type": {"type": "string"},
        "schema": {"const": str(path)},
        "stage_id": {"const": STAGE_ID},
        "status": {"const": "complete"},
        "recommended_next_stage_id": {"const": NEXT_STAGE_ID},
        **{field: {"const": expected} for field, expected in FALSE_GUARDRAILS.items()},
    }
    if key == "summary":
        required.extend(
            [
                "lag5_file_inventory_count",
                "lag5_event_list_row_count",
                "lp_outguessed_signed_output_count",
                "xor_txt_local_file_present",
                "outguess03_jpeg_transcript_fact_card_created",
                "future_probe_manifest_count",
                "overlay_count",
                "stale_current_claim_strict_errors_after_stage5eh",
            ]
        )
        properties.update(
            {
                "lag5_event_list_row_count": {"const": 57},
                "lp_outguessed_signed_output_count": {"const": 8},
                "outguess03_jpeg_transcript_fact_card_created": {"const": True},
                "future_probe_manifest_count": {"const": len(FUTURE_PROBE_IDS)},
                "overlay_count": {"const": 36},
                "stale_current_claim_strict_errors_after_stage5eh": {"const": 0},
            }
        )
    if key == "overlay_collection":
        required.extend(["overlay_count", "overlays", "review_state"])
        properties.update(
            {
                "overlay_count": {"const": 36},
                "review_state": {"const": "overlay_enriched_fact"},
                "overlays": {"type": "array", "minItems": 36},
            }
        )
    if key == "lag5_candidate_records":
        required.extend(["lag5_marker_definition", "lag_value", "event_list_observed_row_count"])
        properties.update(
            {
                "lag5_marker_definition": {"const": "M[i] = 1 iff C[i] = C[i+5]"},
                "lag_value": {"const": 5},
                "event_list_observed_row_count": {"const": 57},
            }
        )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://liberprimus-gpu.local/{path.as_posix()}",
        "type": "object",
        "additionalProperties": True,
        "required": sorted(set(required)),
        "properties": properties,
    }


def _extend_current_stage_state_schema() -> None:
    path = Path("schemas/project-state/current-stage-state-v0.schema.json")
    if not path.exists():
        return
    schema = read_yaml(path)
    props = schema.get("properties", {})
    for field, values in {
        "stage_id": [STAGE_ID],
        "latest_completed_stage_id": [STAGE_ID],
        "recommended_next_stage_id": [NEXT_STAGE_ID],
    }.items():
        enum = props.get(field, {}).get("enum")
        if isinstance(enum, list):
            for value in values:
                if value not in enum:
                    enum.append(value)
            enum.sort()
    write_json(path, schema)


def _update_current_stage_state(summary: dict[str, Any]) -> None:
    state = read_yaml(CURRENT_STAGE_STATE_PATH)
    state.update(
        {
            "stage_id": STAGE_ID,
            "stage_title": STAGE_TITLE,
            "prompt_type": PROMPT_TYPE,
            "metadata_only": True,
            "source_lock_only": True,
            "reviewability_stage": True,
            "number_fact_review_batch_stage": False,
            "puzzle_execution_allowed": False,
            "status": "complete",
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": "codex_plan_mode_number_fact_review_batch",
            "stage5eg_doc_staleness_scanner_preserved": True,
            "stage5ef_current_truth_authority_preserved": True,
            "stage5eb_10_worker_validation_policy_preserved": True,
            "lag5_source_lock_performed_now": True,
            "number_fact_review_batch_006_deferred_to_stage5ei": True,
            "lp_outguessed_inventory_performed_before_records": True,
            "lp_outguessed_xor_txt_local_presence_checked": True,
            "source_lock_records_created_now": True,
            "raw_source_files_committed": False,
            "raw_third_party_files_committed": False,
            "target_priority_decision_created_now": False,
            "pivot_target_selected_now": False,
            **FALSE_GUARDRAILS,
        }
    )
    state["number_fact_enrichment_overlays_added_now"] = True
    state["future_probe_manifest_count"] = summary.get("future_probe_manifest_count", len(FUTURE_PROBE_IDS))
    write_yaml(CURRENT_STAGE_STATE_PATH, state)


def _update_current_mirrors() -> None:
    _upsert_marked_section(Path("AGENTS.md"), "stage5eh", _agents_section())
    _upsert_marked_section(CHATGPT_CONTEXT_PATH, "stage5eh", _chatgpt_section())
    _upsert_marked_section(Path("STATUS.md"), "stage5eh", _status_section())
    _upsert_marked_section(Path("README.md"), "stage5eh", _readme_section())
    _upsert_marked_section(Path("ROADMAP.md"), "stage5eh", _roadmap_section())
    _upsert_marked_section(Path("docs/roadmap/staged-plan.md"), "stage5eh", _staged_plan_section())
    _upsert_marked_section(Path("docs/reference/token-block-cli.md"), "stage5eh", _cli_doc_section())
    replacements_by_path: dict[Path, dict[str, str]] = {
        Path("AGENTS.md"): {
            "Current completed stage: Stage 5EG - Post-edit doc-staleness guardians, read-only auditor agents, stop-hook drift gate, and daily automation setup, without puzzle execution.": f"Current completed stage: {STAGE_TITLE}.",
            "Current work: Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, and enriched fact cards, without execution.": f"Current work: {NEXT_STAGE_TITLE}.",
        },
        CHATGPT_CONTEXT_PATH: {
            "Current completed stage: Stage 5EG - Post-edit doc-staleness guardians, read-only auditor agents, stop-hook drift gate, and daily automation setup, without puzzle execution.": f"Current completed stage: {STAGE_TITLE}.",
            "Current work after Stage 5EG: Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, and enriched fact cards, without execution.": f"Current work after Stage 5EH: {NEXT_STAGE_TITLE}.",
            "Latest completed stage: Stage 5EG - Post-edit doc-staleness guardians, read-only auditor agents, stop-hook drift gate, and daily automation setup, without puzzle execution.": f"Latest completed stage: {STAGE_TITLE}.",
            "Current planning focus: Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, and enriched fact cards, without execution.": f"Current planning focus: {NEXT_STAGE_TITLE}.",
        },
        Path("docs/onboarding/start-here.md"): {
            "- Latest completed stage: Stage 5EG - Post-edit doc-staleness guardians, read-only auditor agents, stop-hook drift gate, and daily automation setup, without puzzle execution.": f"- Latest completed stage: {STAGE_TITLE}.",
            "- Current planning focus: Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, and enriched fact cards, without execution.": f"- Current planning focus: {NEXT_STAGE_TITLE}.",
        },
        Path("docs/roadmap/staged-plan.md"): {
            "- Latest completed stage: Stage 5EG - Post-edit doc-staleness guardians, read-only auditor agents, stop-hook drift gate, and daily automation setup, without puzzle execution.": f"- Latest completed stage: {STAGE_TITLE}.",
            "- Current planning focus: Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, and enriched fact cards, without execution.": f"- Current planning focus: {NEXT_STAGE_TITLE}.",
        },
        Path("README.md"): {
            "- Next: Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, and enriched fact cards, without execution.": f"- Next: {NEXT_STAGE_TITLE}.",
        },
        Path("ROADMAP.md"): {
            "Current next prompt: Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, and enriched fact cards, without execution.": f"Current next prompt: {NEXT_STAGE_TITLE}.",
            "The next recommended prompt is Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, and enriched fact cards, without execution.": f"The next recommended prompt is {NEXT_STAGE_TITLE}.",
        },
        Path("STATUS.md"): {
            "Next recommended prompt: Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, and enriched fact cards, without execution.": f"Next recommended prompt: {NEXT_STAGE_TITLE}.",
        },
    }
    for path, replacements in replacements_by_path.items():
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        _write_text(path, text)


def _update_stage5ah_source_of_truth() -> None:
    if not DOC_STALENESS_SOURCE_OF_TRUTH_PATH.exists():
        return
    payload = read_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "latest_completed_stage_after_this_stage": STAGE_TITLE,
            "next_stage_after_this_stage": NEXT_STAGE_TITLE,
            "latest_previous_stage": PREVIOUS_STAGE_TITLE,
            "expected_next_stage_prefix": "Stage 5EI",
            "latest_completed_stage_prefix": "Stage 5EH",
            "current_stage_state_authoritative": True,
            "historical_sections_may_retain_old_stage_claims_if_clearly_historical": True,
        }
    )
    write_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH, payload)


def _update_stage_summary_records(summary: dict[str, Any]) -> None:
    payload = read_yaml(STAGE_SUMMARY_RECORDS_PATH)
    records = payload if isinstance(payload, list) else payload.get("records", [])
    records = [record for record in records if record.get("stage_id") != STAGE_ID]
    records.append(
        {
            "record_type": "stage_summary_record",
            "stage_id": STAGE_ID,
            "title": STAGE_TITLE,
            "status": "complete",
            "category": "metadata_source_lock_reviewability",
            "summary": "Added metadata-only Lag5, lp_outguessed, byte-string, Page54/55 red-number, and Page13 detector context records plus overlay fact cards and future probe manifests.",
            "key_outputs": [
                f"Lag5 files inventoried: {summary.get('lag5_file_inventory_count')}; event rows: {summary.get('lag5_event_list_row_count')}.",
                f"lp_outguessed signed outputs present: {summary.get('lp_outguessed_signed_output_count')}; xor.txt local present: {summary.get('xor_txt_local_file_present')}.",
                f"Future probes declared with run_now=false: {summary.get('future_probe_manifest_count')}.",
                f"Source Browser overlays added: {summary.get('overlay_count')}.",
            ],
            "result_status": "metadata_source_lock_addendum_complete",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": "No route extraction, byte streams, stego execution, image forensics, OCR, CUDA, scoring, benchmarks, or solve claim.",
        }
    )
    if isinstance(payload, list):
        write_yaml(STAGE_SUMMARY_RECORDS_PATH, records)
    else:
        payload["records"] = records
        write_yaml(STAGE_SUMMARY_RECORDS_PATH, payload)


def _update_operational_file_map() -> None:
    if not OPERATIONAL_FILE_MAP_PATH.exists():
        return
    payload = read_yaml(OPERATIONAL_FILE_MAP_PATH)
    records = payload.get("records", []) if isinstance(payload, dict) else []
    additions = [
        *[path.as_posix() for path in DATA_PATHS.values()],
        *[path.as_posix() for path in SCHEMA_PATHS.values()],
        DEV_LOG_PATH.as_posix(),
        RESEARCH_LOG_PATH.as_posix(),
    ]
    addition_set = set(additions)
    records = [record for record in records if record.get("path") not in addition_set]
    for path in additions:
        records.append(
            {
                "path": path,
                "category": "historical_log" if path.startswith(("docs/development-logs/", "research-log/")) else "active_data_record",
                "purpose": "Stage 5EH metadata-only source-lock addendum, diagnostic probe, overlay, schema, or log.",
                "source_of_truth_rank": 2 if path.startswith("data/") else 3,
                "last_meaningful_update_stage": STAGE_ID,
                "expected_update_frequency": "stage_specific",
                "mutable_or_reference_only": "reference_only" if path.startswith(("docs/development-logs/", "research-log/")) else "mutable",
                "mirror_or_generated_relationships": "Stage 5EH source-lock metadata; current-stage-state remains authoritative.",
                "staleness_check_level": "historical" if path.startswith(("docs/development-logs/", "research-log/")) else "reference_only",
                "owner_context": "codex_agent",
                "notes": "Raw third_party files and generated outputs remain ignored and uncommitted.",
            }
        )
    payload["records"] = records
    write_yaml(OPERATIONAL_FILE_MAP_PATH, payload)


def _write_docs(inventory: dict[str, Any]) -> None:
    _write_text(DEV_LOG_PATH, _dev_log(inventory))
    _write_text(RESEARCH_LOG_PATH, _research_log(inventory))


def _write_codex_output_handoff(summary: dict[str, Any]) -> None:
    _write_text(
        CODEX_OUTPUT_DIR / "stage5eh-codex-completion.md",
        f"""# Stage 5EH Codex Completion

Stage: {STAGE_ID} - {STAGE_TITLE}
Starting commit: {PREVIOUS_STAGE_COMMIT}
Final commit: pending until commit.
Origin/main commit: pending until push.
GitHub issue: pending.
CI run/status: pending.
Stage 5EG preservation status: true.
Lag5 source root: {LAG5_ROOT.as_posix()}
Lag5 file inventory count: {summary.get('lag5_file_inventory_count')}
Lag5 event-list row count: {summary.get('lag5_event_list_row_count')}
Lag5 d1/d4/M-sum facts: 29 / 28 / 479.
lp_outguessed signed-output count: {summary.get('lp_outguessed_signed_output_count')}
xor.txt local presence status: {summary.get('xor_txt_local_file_present')}
03 JPEG transcript fact-card status: {summary.get('outguess03_jpeg_transcript_fact_card_created')}
Byte-string crosslink status: {summary.get('byte_string_crosslink_status')}
Page54/55 red-number block status: {summary.get('page54_55_red_number_block_status')}
Page13 F5 detector status and beta value: {summary.get('page13_f5_detector_status')} / {summary.get('page13_stegdetect_detail_beta')}
Future probe manifest count: {summary.get('future_probe_manifest_count')}
Overlay count: {summary.get('overlay_count')}
Reviewability gap count: {summary.get('reviewability_gap_count')}
Source Browser entries/errors: {summary.get('source_browser_entries_loaded')} / {summary.get('source_browser_validation_error_count')}
Stale-current scanner errors after closeout: {summary.get('stale_current_claim_strict_errors_after_stage5eh')}
Full-parallel validation: Workers=10 / PytestWorkers=10 pending.
Full serial pytest run: false.
Guardrails closed: true.
Recommended next stage: {NEXT_STAGE_TITLE}

This file is ignored and must not be committed.
""",
    )


def _agents_section() -> str:
    return f"""## Stage 5EH Lag5/Outguess/Byte-Control Source-Lock Addendum

- Current completed stage: {STAGE_TITLE}.
- Current work: {NEXT_STAGE_TITLE}.
- Stage 5EH is metadata/source-lock/reviewability only: it inventories local Lag5 and iddqd-v2 source files, creates future probe manifests with `run_now=false`, and adds overlay-only NumberFactCards.
- Do not run OutGuess, StegDetect, F5 extraction/password search, XOR reconstruction, OCR, image forensics, route extraction, byte-stream generation, CUDA, scoring, benchmarks, Tor, or solve workflows from Stage 5EH records.
- `third_party/CiadaSolversIddqd_v2/lp_outguessed` is the canonical local lp_outguessed root unless a future validator proves otherwise; duplicate `xor.txt` candidates elsewhere are reviewability context only.
"""


def _chatgpt_section() -> str:
    return f"""## Stage 5EH Current Context

Latest completed stage: {STAGE_TITLE}.

Current planning focus: {NEXT_STAGE_TITLE}.

Stage 5EH source-locks Lag5, `lp_outguessed`, byte-string, Page54/55 red-number, and Page13 detector context as metadata only. It adds future diagnostic probe manifests with `run_now=false` and overlay-only fact cards, but it performs no route extraction, byte generation, XOR reconstruction, PGP verification, OutGuess/StegDetect/F5 execution, OCR, image forensics, CUDA, scoring, benchmark, or solve claim.
"""


def _status_section() -> str:
    return f"""## Stage 5EH Status

Latest completed stage: {STAGE_TITLE}.

Recommended next stage: {NEXT_STAGE_TITLE}.

Stage 5EH records Lag5 29/28/57 event context, M-sum 479 over claimed N=12,956, lp_outguessed signed-output metadata, the canonical xor.txt presence/gap result, operator-supplied 03 JPEG transcription facts, Stage 5BK byte-string crosslinks, Page54/55 red-number controls, and Page13 detector context. All probe manifests are disabled with `run_now=false`.
"""


def _readme_section() -> str:
    return f"""## Stage 5EH Current Status

The authoritative current-stage registry is `data/project-state/current-stage-state.yaml`.

Latest completed: {STAGE_TITLE}.

Next routed: {NEXT_STAGE_TITLE}.
"""


def _roadmap_section() -> str:
    return f"""## Stage 5EH Routing

- Complete: {STAGE_TITLE}.
- Next: {NEXT_STAGE_TITLE}.
- Batch 006 remains deferred to Stage 5EI.
"""


def _staged_plan_section() -> str:
    return f"""## Stage 5EH - Lag5/Outguess/Byte-Control Source-Lock Addendum

- Latest completed stage: {STAGE_TITLE}.
- Current planning focus: {NEXT_STAGE_TITLE}.
- Stage 5EH is source-lock/reviewability metadata only and does not authorize route extraction, byte streams, stego execution, OCR, image forensics, CUDA, scoring, benchmarks, or solve claims.
"""


def _cli_doc_section() -> str:
    return """## Stage 5EH Token-Block Commands

- `python -m libreprimus.cli token-block build-stage5eh`
- `python -m libreprimus.cli token-block validate-stage5eh`
- `python -m libreprimus.cli token-block stage5eh-summary`
- focused validators include Lag5 inventory, lp_outguessed inventory, overlays, Source Browser loadability, sidecar gates, handoff continuity, and governance scope.
"""


def _dev_log(inventory: dict[str, Any]) -> str:
    return f"""# Stage 5EH Development Log

Stage 5EH built metadata-only source-lock addendum records for Lag5, lp_outguessed, byte-string, Page54/55 red-number, and Page13 detector context.

- Lag5 expected files present: {sum(1 for record in inventory['lag5_files'] if record['present'])} / 5.
- Lag5 event rows observed: {inventory['lag5_event_row_count']}.
- lp_outguessed expected signed outputs present: {inventory['expected_signed_present_count']} / 8.
- canonical lp_outguessed/xor.txt present: {inventory['canonical_xor']['present']}.
- duplicate xor.txt candidates outside canonical root: {len(inventory['duplicate_xor_candidates'])}.

No raw source bodies, generated outputs, execution outputs, byte streams, or detector outputs were committed.
"""


def _research_log(inventory: dict[str, Any]) -> str:
    return f"""# Stage 5EH Research Summary

Stage 5EH records review-only metadata for the Lag5 and outguess/byte-control context.

Lag5 facts preserved: marker lag 5, d1=29, d4=28, d1+d4=57, M-sum=479, claimed N=12,956, and d-counts 29/15/14/28/19/15.

Outguess facts preserved: expected signed outputs 00/01/02/03/10/11/12/13, PGP key 181F01E57A35090F / 7A35090F as unverified, prior 991-byte XOR-share context, canonical xor.txt presence {inventory['canonical_xor']['present']}, and operator-supplied 03 JPEG transcription facts.

All future probes remain `run_now=false`; no extraction, route, byte-stream, F5, StegDetect, OutGuess, OCR, image-forensics, CUDA, scoring, benchmark, Tor, or solve workflow was performed.
"""


def _extend_sequence_schema(schema_path: Path, stage_id: str, next_stage_id: str) -> None:
    if not schema_path.exists():
        return
    schema = read_yaml(schema_path)
    props = schema.get("properties", {})
    for field, values in {
        "stage_id": [stage_id],
        "latest_completed_stage_id": [stage_id],
        "recommended_next_stage_id": [next_stage_id],
    }.items():
        enum = props.get(field, {}).get("enum")
        if isinstance(enum, list):
            for value in values:
                if value not in enum:
                    enum.append(value)
            enum.sort()
    write_json(schema_path, schema)


def _false_guardrail_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key, expected in FALSE_GUARDRAILS.items():
        if key in record and record[key] is not expected:
            errors.append(f"{record.get('record_type', 'record')} has {key}={record[key]!r}, expected {expected!r}")
    return errors


def _combine(validators: list[Callable[[], ValidationResult]]) -> ValidationResult:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for validator in validators:
        result = validator()
        errors.extend(result.errors)
        counts.update(result.counts)
    return ValidationResult(not errors, errors, counts)


def _result(errors: list[str], **counts: Any) -> ValidationResult:
    return ValidationResult(not errors, errors, counts)


def _read_record(key: str) -> dict[str, Any]:
    return read_yaml(DATA_PATHS[key])


def _upsert_marked_section(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    start = f"<!-- BEGIN {marker} -->"
    end = f"<!-- END {marker} -->"
    section = f"{start}\n{block.rstrip()}\n{end}\n"
    if start in text and end in text:
        before, rest = text.split(start, 1)
        _, after = rest.split(end, 1)
        new_text = before.rstrip() + "\n\n" + section + after.lstrip()
    else:
        new_text = text.rstrip() + "\n\n" + section
    _write_text(path, new_text)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
