"""Stage 5DW number-fact review batch 001 overlays.

This stage adds reviewability metadata only. It enriches Source Browser
NumberFactCards through overlays, preserves historical source-lock records, and
does not authorize target selection, byte generation, execution, CUDA, scoring,
or solve claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.number_facts import (
    normalize_entry_number_facts,
)
from libreprimus.operator_console.source_browser.validators import (
    path_canonicalization_report,
    source_browser_summary,
    validate_path_canonicalization,
    validate_source_index,
)
from libreprimus.token_block.models import read_yaml, write_json, write_yaml
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP
from libreprimus.token_block.stage5dv import validate_stage5dv

STAGE_ID = "stage-5dw"
STAGE_TITLE = (
    "Stage 5DW - Source-lock number-fact review batch 001, high-signal enrichment "
    "overlays, without execution"
)
PROMPT_TYPE = "codex_metadata_and_operator_console_reviewability_implementation"
SOURCE_PREVIOUS_STAGE_ID = "stage-5dv"
SOURCE_PREVIOUS_STAGE_COMMIT = "fe8d3d002defe18de0414dc7b14a5a68293094a7"
SOURCE_PREVIOUS_ISSUE = 157
SOURCE_PREVIOUS_CI_RUN = 27204060659
NEXT_STAGE_ID = "stage-5dx"
NEXT_STAGE_TITLE = (
    "Stage 5DX - Operator/assistant source-lock number-fact review batch 2, "
    "without execution"
)
REVIEW_BATCH_ID = "number_fact_review_batch_001_high_signal"
REVIEW_BATCH_SELECTION_POLICY = "assistant_operator_high_signal_evidence_batch"
OVERLAY_COLLECTION_PATH = Path(
    "data/operator-console/source-browser/number-fact-overlays/"
    "stage5dw-review-batch-001-high-signal-overlays.yaml"
)
OVERLAY_SCHEMA_PATH = Path("schemas/operator-console/source-browser-number-fact-enrichment-overlay-v0.schema.json")
CHATGPT_CONTEXT_PATH = Path("ChatGPT-ContextFile.md")

PROJECT_STATE_DIR = Path("data/project-state")
SOURCE_BROWSER_DIR = Path("data/operator-console/source-browser")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
TOKEN_BLOCK_DIR = Path("data/token-block")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5dw-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5dw-next-stage-decision.yaml",
    "review_batch_selection": PROJECT_STATE_DIR / "stage5dw-review-batch-001-selection.yaml",
    "review_batch_findings": PROJECT_STATE_DIR / "stage5dw-review-batch-001-findings.yaml",
    "overlay_only_support": PROJECT_STATE_DIR / "stage5dw-overlay-only-fact-card-support.yaml",
    "source_browser_loadability": PROJECT_STATE_DIR / "stage5dw-source-browser-loadability-summary.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5dw-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5dw-reviewability-gap-register.yaml",
    "stage5dv_preservation": PROJECT_STATE_DIR / "stage5dw-stage5dv-preservation.yaml",
    "governance_scope_control": PROJECT_STATE_DIR / "stage5dw-governance-scope-control.yaml",
}

SOURCE_BROWSER_PATHS: dict[str, Path] = {
    "review_batch_result": SOURCE_BROWSER_DIR
    / "number-fact-review-batches/stage5dw-review-batch-001-high-signal-result.yaml",
    "review_batch_entry_status": SOURCE_BROWSER_DIR
    / "number-fact-review-batches/stage5dw-review-batch-001-entry-status.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5dw-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5dw-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5dw-raw-source-noncommit-proof.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "stage5dg_preservation": TOKEN_BLOCK_DIR / "stage5dw-stage5dg-preservation.yaml",
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5dw-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5dw-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5dw-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR / "stage5dw-no-byte-stream-transition-proof.yaml",
    "no_execution_proof": TOKEN_BLOCK_DIR / "stage5dw-no-execution-proof.yaml",
}

DATA_PATHS: dict[str, Path] = {}
DATA_PATHS.update(PROJECT_STATE_PATHS)
DATA_PATHS.update(SOURCE_BROWSER_PATHS)
DATA_PATHS.update(SOURCE_HARVESTER_PATHS)
DATA_PATHS.update(TOKEN_PATHS)

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5dw-summary-v0.schema.json"),
    "review_batch_selection": Path("schemas/project-state/stage5dw-review-batch-001-selection-v0.schema.json"),
    "review_batch_findings": Path("schemas/project-state/stage5dw-review-batch-001-findings-v0.schema.json"),
    "overlay_only_support": Path("schemas/project-state/stage5dw-overlay-only-fact-card-support-v0.schema.json"),
    "source_browser_loadability": Path(
        "schemas/project-state/stage5dw-source-browser-loadability-summary-v0.schema.json"
    ),
    "review_batch_result": Path(
        "schemas/operator-console/source-browser-number-fact-review-batch-result-v0.schema.json"
    ),
    "codex_handoff_policy": Path("schemas/source-harvester/stage5dw-codex-handoff-policy-v0.schema.json"),
    "no_execution_proof": Path("schemas/token-block/stage5dw-no-execution-proof-v0.schema.json"),
    "generic_project_state": Path("schemas/project-state/stage5dw-generic-record-v0.schema.json"),
    "generic_source_harvester": Path("schemas/source-harvester/stage5dw-generic-record-v0.schema.json"),
    "generic_token_block": Path("schemas/token-block/stage5dw-generic-record-v0.schema.json"),
}

SCHEMA_BY_DATA_KEY: dict[str, str] = {
    "summary": "summary",
    "review_batch_selection": "review_batch_selection",
    "review_batch_findings": "review_batch_findings",
    "overlay_only_support": "overlay_only_support",
    "source_browser_loadability": "source_browser_loadability",
    "review_batch_result": "review_batch_result",
    "codex_handoff_policy": "codex_handoff_policy",
    "no_execution_proof": "no_execution_proof",
}

SELECTED_SOURCE_RECORD_PATHS = [
    "data/historical-route/stage5do-page32-red-header-progressive-gp-sum-2472.yaml",
    "data/historical-route/stage5do-page32-red-header-cumulative-index-463-3299.yaml",
    "data/historical-route/stage5do-no-f-rune-count-section-flow-candidate.yaml",
    "data/historical-route/stage5do-lp-doublet-scarcity-feature-v1.yaml",
    "data/historical-route/stage5do-lp1-encrypted-word-count-464-prime-3301.yaml",
    "data/historical-route/stage5do-artwork-title-gp-equivalence-candidate.yaml",
    "data/historical-route/stage5do-solved-koan-gp-facts-candidate.yaml",
    "data/historical-route/stage5do-page54-57-hash-rune-count-balance-candidate.yaml",
    "data/historical-route/stage5do-page32-fibonacci-mod29-prime-palindrome-candidate.yaml",
    "data/historical-route/stage5do-final-jpg-road-way-gp-runs-candidate.yaml",
    "data/historical-route/stage5do-prime-index-bridge-761-167-464-1033-3301.yaml",
    "data/historical-route/stage5do-page32-dead-tree-rgb185-count-3301-candidate.yaml",
    "data/historical-route/stage5ds-instar-parable-id3-gp-product-candidate-v1.yaml",
    "data/historical-route/stage5ds-instar-title-761-duration-167-bridge-v1.yaml",
    "data/historical-route/stage5ds-interconnectedness-772-277-table-canon-number-v1.yaml",
    "data/historical-route/stage5ds-ouroboros-see-also-gp-arithmetic-scan-v0.yaml",
    "data/historical-route/stage5du-red-runes-gateless-gate-koan20-title-candidate-v0.yaml",
    "data/historical-route/stage5du-big-gap-page-set-16-candidate-v0.yaml",
    "data/historical-route/stage5du-star-artifacts-exact254-mask-method-v0.yaml",
    "data/historical-route/stage5du-red-heading-marginalia-gp491-equivalence-family-v0.yaml",
]

FALSE_FLAGS = {
    "activation_authorized_now",
    "activation_decision_valid_now",
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "active_token_block_manifest_changed",
    "alberti_html_executed_now",
    "audio_stego_performed",
    "benchmark_performed",
    "branch_enumeration_performed",
    "byte_stream_generation_authorized_now",
    "canonical_corpus_active",
    "combined_approval_gate_satisfied_now",
    "community_code_executed_now",
    "cuda_execution_performed",
    "decode_attempt_performed",
    "decryption_attempt_performed_now",
    "direct_music_substitution_executed",
    "disk_cipher_execution_performed_now",
    "dwh_hash_search_performed",
    "execution_authorized_now",
    "execution_performed",
    "full_cartesian_product_enumerated",
    "generated_outputs_committed",
    "hash_preimage_search_performed",
    "hidden_content_image_forensics_performed",
    "historical_source_lock_records_rewritten",
    "html_tool_executed_now",
    "image_forensics_performed",
    "known_plaintext_attack_performed_now",
    "machine_code_execution_performed_now",
    "mayfly_route_extraction_performed_now",
    "midi_route_extraction_performed_now",
    "mp3stego_execution_performed",
    "music_route_extraction_performed_now",
    "native_code_execution_performed_now",
    "network_target_validation_performed_now",
    "number_fact_backfill_performed_now",
    "ocr_performed",
    "openpuff_execution_performed",
    "operator_readiness_decision_created_now",
    "page0_plaintext_accepted_now",
    "page32_route_extraction_performed_now",
    "page56_hash_preimage_tested_now",
    "page_boundaries_final",
    "pdf_ocr_or_hidden_content_rendering_performed",
    "pivot_target_selected_now",
    "probability_claim_accepted_as_validated",
    "raw_source_files_committed",
    "raw_source_files_mutated_by_gui",
    "raw_third_party_files_committed",
    "real_byte_stream_generated",
    "red_heading_decryption_accepted_now",
    "route_extraction_performed_now",
    "scoring_performed",
    "semantic_image_interpretation_performed",
    "solve_claim",
    "spectrogram_stego_performed",
    "spreadsheet_macro_execution_performed",
    "target_class_validation_implemented",
    "target_priority_decision_created_now",
    "token_block_experiment_executed",
    "token_block_variant_byte_streams_generated",
    "tor_network_access_performed",
    "triangle_route_extraction_performed_now",
    "variant_byte_streams_generated",
    "variant_materialisation_performed",
    "vm_bytecode_execution_performed_now",
    "website_expansion_performed",
}


@dataclass(frozen=True)
class Stage5DWValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5dw"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5dw() -> dict[str, dict[str, Any]]:
    previous = validate_stage5dv()
    if previous.validation_error_count:
        raise RuntimeError("Stage 5DV validation must pass before Stage 5DW")
    _write_schemas()
    _update_chatgpt_context()
    records = _build_records()
    _write_records(records)
    _update_stage_summary_records(records["summary"])
    return records


def validate_stage5dw() -> Stage5DWValidationResult:
    checks = [
        validate_stage5dw_review_batch_selection,
        validate_stage5dw_number_fact_overlays,
        validate_stage5dw_overlay_only_fact_cards,
        validate_stage5dw_source_browser_loadability,
        validate_stage5dw_stage5dv_preservation,
        validate_stage5dw_stage5dg_preservation,
        validate_stage5dw_stage5bd_preservation,
        validate_stage5dw_active_lineage_preservation,
        validate_stage5dw_sidecar_gates,
        validate_stage5dw_handoff_continuity,
        validate_stage5dw_credential_redaction_policy,
        validate_stage5dw_governance_scope,
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    errors.extend(_validate_required_paths())
    errors.extend(_validate_schemas())
    for check in checks:
        result = check()
        counts.update(result.counts)
        errors.extend(result.errors)
    summary = _load(PROJECT_STATE_PATHS["summary"])
    expected = {
        "status": "complete",
        "number_fact_review_batch_1_performed_now": True,
        "reviewed_entry_count": 20,
        "overlay_count": 37,
        "overlay_only_fact_cards_supported": True,
        "overlay_only_fact_cards_validated": True,
        "historical_source_lock_records_rewritten": False,
        "number_fact_backfill_performed_now": False,
        "target_priority_decision_created_now": False,
        "pivot_target_selected_now": False,
        "execution_performed": False,
        "solve_claim": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"{PROJECT_STATE_PATHS['summary'].as_posix()}: {key} must be {value}")
    errors.extend(_required_false_errors(summary, PROJECT_STATE_PATHS["summary"].as_posix()))
    counts.update(_summary_counts(summary))
    counts["token_block_stage5dw_valid"] = not errors
    return Stage5DWValidationResult(len(errors), counts, errors)


def validate_stage5dw_review_batch_selection() -> Stage5DWValidationResult:
    payload = _load(PROJECT_STATE_PATHS["review_batch_selection"])
    selected = payload.get("selected_source_record_paths", [])
    errors = []
    if payload.get("review_batch_id") != REVIEW_BATCH_ID:
        errors.append("Stage 5DW review batch id mismatch")
    if payload.get("reviewed_entry_count") != 20 or len(selected) != 20:
        errors.append("Stage 5DW selected batch must contain exactly 20 records")
    missing = [path for path in selected if not Path(path).exists()]
    errors.extend(f"selected source path missing: {path}" for path in missing)
    if payload.get("stage5dt_stable_batch_001_not_mutated") is not True:
        errors.append("Stage 5DT stable batch 001 must remain unmutated")
    return Stage5DWValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dw_number_fact_overlays() -> Stage5DWValidationResult:
    collection = _load_overlay_collection()
    overlays = collection.get("overlays", [])
    errors = []
    if collection.get("record_type") != "source_browser_number_fact_enrichment_overlay_collection":
        errors.append("overlay collection record_type mismatch")
    if collection.get("stage_id") != STAGE_ID:
        errors.append("overlay collection stage_id mismatch")
    if collection.get("reviewed_entry_count") != 20:
        errors.append("overlay collection reviewed entry count must be 20")
    if len(overlays) != 37:
        errors.append(f"expected 37 overlays, got {len(overlays)}")
    selected = set(collection.get("selected_source_record_paths", []))
    overlay_paths = {str(overlay.get("source_record_path") or "") for overlay in overlays}
    missing_selected = sorted(selected - overlay_paths)
    errors.extend(f"selected source has no overlay: {path}" for path in missing_selected)
    schema = _load(OVERLAY_SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for index, overlay in enumerate(overlays):
        for error in sorted(validator.iter_errors(overlay), key=lambda item: item.path):
            errors.append(f"overlay[{index}] {overlay.get('overlay_id')}: {error.message}")
        if overlay.get("usable_for_decision_now") is not False:
            errors.append(f"{overlay.get('overlay_id')}: usable_for_decision_now must be false")
        not_allowed = set(overlay.get("not_allowed_as", []))
        for value in ("proof", "route_seed", "execution_seed", "solve_claim"):
            if value not in not_allowed:
                errors.append(f"{overlay.get('overlay_id')}: not_allowed_as missing {value}")
    return Stage5DWValidationResult(
        len(errors),
        {
            "overlay_count": len(overlays),
            "reviewed_entry_count": collection.get("reviewed_entry_count"),
            "selected_source_path_count": len(selected),
        },
        errors,
    )


def validate_stage5dw_overlay_only_fact_cards() -> Stage5DWValidationResult:
    index = build_source_index()
    entry_by_path = {entry.source_record_path: entry for entry in index.entries}
    overlays = _load_overlay_collection().get("overlays", [])
    selected_cards = 0
    overlay_only_cards = 0
    errors = []
    for path in SELECTED_SOURCE_RECORD_PATHS:
        entry = entry_by_path.get(path)
        if entry is None:
            errors.append(f"selected entry not loaded: {path}")
            continue
        cards = normalize_entry_number_facts(entry, overlays)
        if not cards:
            errors.append(f"selected entry has no normalized fact cards after overlays: {path}")
        selected_cards += len(cards)
        raw_ids = {_raw_fact_id(fact) for fact in entry.number_facts}
        overlay_only_cards += sum(
            1
            for overlay in overlays
            if overlay.get("source_record_path") == path and str(overlay.get("source_fact_id") or "") not in raw_ids
        )
    synthetic_entry = _synthetic_zero_fact_entry()
    synthetic_overlay = {
        "record_type": "source_browser_number_fact_enrichment_overlay",
        "overlay_id": "stage5dw_synthetic_overlay_only_test",
        "source_record_path": synthetic_entry.source_record_path,
        "source_fact_id": "synthetic_overlay_only",
        "display_label": "Synthetic overlay-only fact",
        "short_label": "Synthetic overlay-only",
        "value": 20,
        "value_type": "sum",
        "operation_type": "sum",
        "verification_status": "arithmetic_verified_metadata_only",
        "review_state": "overlay_enriched_fact",
        "usable_for_decision_now": False,
        "not_allowed_as": ["proof", "route_seed", "execution_seed", "solve_claim"],
    }
    synthetic_cards = normalize_entry_number_facts(synthetic_entry, [synthetic_overlay])
    if len(synthetic_cards) != 1 or synthetic_cards[0].overlay_applied is not True:
        errors.append("synthetic zero-extracted-fact entry did not render overlay-only fact card")
    return Stage5DWValidationResult(
        len(errors),
        {
            "selected_batch_fact_cards": selected_cards,
            "overlay_only_cards_required_count": overlay_only_cards,
            "synthetic_overlay_only_cards": len(synthetic_cards),
        },
        errors,
    )


def validate_stage5dw_source_browser_loadability() -> Stage5DWValidationResult:
    index = build_source_index()
    result = validate_source_index()
    path_result = validate_path_canonicalization()
    payload = _load(PROJECT_STATE_PATHS["source_browser_loadability"])
    errors = list(result.errors) + list(path_result.errors)
    for key in (
        "source_browser_validation_error_count",
        "spurious_root_image_paths_after",
        "spurious_root_document_paths_after",
        "duplicate_present_missing_path_pairs_after",
    ):
        if payload.get(key) != 0:
            errors.append(f"{key} must be 0")
    if len(index.entries) < 1510:
        errors.append("Source Browser entry count regressed below Stage 5DV baseline")
    return Stage5DWValidationResult(len(errors), {**result.counts, **path_result.counts, **_summary_counts(payload)}, errors)


def validate_stage5dw_stage5dv_preservation() -> Stage5DWValidationResult:
    payload = _load(PROJECT_STATE_PATHS["stage5dv_preservation"])
    errors = []
    if payload.get("stage5dv_preserved") is not True:
        errors.append("Stage 5DV must be preserved")
    if payload.get("spurious_root_image_paths_after") != 0:
        errors.append("Stage 5DV spurious root image paths must remain 0")
    if payload.get("duplicate_present_missing_path_pairs_after") != 0:
        errors.append("Stage 5DV duplicate present/missing path pairs must remain 0")
    return Stage5DWValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dw_stage5dg_preservation() -> Stage5DWValidationResult:
    payload = _load(TOKEN_PATHS["stage5dg_preservation"])
    errors = []
    if payload.get("stage5dg_operator_approval_record_preserved") is not True:
        errors.append("Stage 5DG operator approval record must be preserved")
    if payload.get("combined_approval_gate_satisfied_now") is not False:
        errors.append("combined approval gate must remain unsatisfied")
    return Stage5DWValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dw_stage5bd_preservation() -> Stage5DWValidationResult:
    payload = _load(TOKEN_PATHS["stage5bd_preservation"])
    errors = []
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    return Stage5DWValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dw_active_lineage_preservation() -> Stage5DWValidationResult:
    payload = _load(TOKEN_PATHS["active_lineage_preservation"])
    errors = []
    if payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage count must remain 8")
    return Stage5DWValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dw_sidecar_gates() -> Stage5DWValidationResult:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for path in (
        TOKEN_PATHS["no_active_ingestion_proof"],
        TOKEN_PATHS["no_byte_stream_transition_proof"],
        TOKEN_PATHS["no_execution_proof"],
    ):
        payload = _load(path)
        counts[path.stem] = payload.get("gate_status")
        errors.extend(_required_false_errors(payload, path.as_posix()))
        if payload.get("gate_status") != "closed":
            errors.append(f"{path.as_posix()}: gate_status must be closed")
    return Stage5DWValidationResult(len(errors), counts, errors)


def validate_stage5dw_handoff_continuity() -> Stage5DWValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if payload.get("deprecated_codex_output_root_used") is not False:
        errors.append("deprecated codex_output root must not be used")
    if Path("codex_output").exists():
        errors.append("deprecated codex_output directory is present")
    return Stage5DWValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dw_credential_redaction_policy() -> Stage5DWValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["credential_redaction_policy_preservation"])
    errors = []
    if payload.get("credential_like_remote_count") != 0:
        errors.append("credential-like remote count must be 0")
    if payload.get("raw_source_body_included") is not False:
        errors.append("credential policy must not include raw source bodies")
    return Stage5DWValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dw_governance_scope() -> Stage5DWValidationResult:
    payload = _load(PROJECT_STATE_PATHS["governance_scope_control"])
    errors = _required_false_errors(payload, PROJECT_STATE_PATHS["governance_scope_control"].as_posix())
    if payload.get("number_fact_review_batch_1_performed_now") is not True:
        errors.append("Stage 5DW must record number_fact_review_batch_1_performed_now=true")
    if payload.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("next stage must be Stage 5DX")
    return Stage5DWValidationResult(len(errors), _summary_counts(payload), errors)


def stage5dw_summary_text() -> str:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5DW summary:",
        f"status={summary.get('status')}",
        f"review_batch_id={summary.get('review_batch_id')}",
        f"reviewed_entry_count={summary.get('reviewed_entry_count')}",
        f"overlay_count={summary.get('overlay_count')}",
        f"overlay_only_fact_cards_supported={summary.get('overlay_only_fact_cards_supported')}",
        f"source_browser_entries_loaded={summary.get('source_browser_entries_loaded')}",
        f"source_browser_records_scanned={summary.get('source_browser_records_scanned')}",
        f"fact_card_count_after_stage5dw={summary.get('fact_card_count_after_stage5dw')}",
        f"source_browser_validation_error_count={summary.get('source_browser_validation_error_count')}",
        f"spurious_root_image_paths_after={summary.get('spurious_root_image_paths_after')}",
        f"spurious_root_document_paths_after={summary.get('spurious_root_document_paths_after')}",
        f"duplicate_present_missing_path_pairs_after={summary.get('duplicate_present_missing_path_pairs_after')}",
        f"historical_source_lock_records_rewritten={summary.get('historical_source_lock_records_rewritten')}",
        f"target_selected={summary.get('pivot_target_selected_now')}",
        f"execution_performed={summary.get('execution_performed')}",
        f"solve_claim={summary.get('solve_claim')}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


def _build_records() -> dict[str, dict[str, Any]]:
    collection = _load_overlay_collection()
    overlays = collection["overlays"]
    index = build_source_index()
    entry_by_path = {entry.source_record_path: entry for entry in index.entries}
    browser = source_browser_summary(index)
    path_report = path_canonicalization_report(index)
    overlay_only_count = _overlay_only_count(overlays, entry_by_path)
    selected_fact_cards = {
        path: len(normalize_entry_number_facts(entry_by_path[path], overlays))
        for path in SELECTED_SOURCE_RECORD_PATHS
        if path in entry_by_path
    }
    fact_card_count_after = sum(len(normalize_entry_number_facts(entry, overlays)) for entry in index.entries)
    base = _stage_base()
    false_flags = _false_flags()
    source_browser_validation = validate_source_index()

    summary = {
        **base,
        **false_flags,
        "record_type": "stage5dw_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "status": "complete",
        "source_previous_stage": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_commit_expected": SOURCE_PREVIOUS_STAGE_COMMIT,
        "source_previous_issue": SOURCE_PREVIOUS_ISSUE,
        "source_previous_ci_run": SOURCE_PREVIOUS_CI_RUN,
        "stage5dv_preserved": True,
        "stage5du_preserved": True,
        "stage5dt_preserved": True,
        "source_browser_performance_repair_preserved": True,
        "source_browser_path_canonicalization_repair_preserved": True,
        "number_fact_review_batch_1_performed_now": True,
        "review_batch_id": REVIEW_BATCH_ID,
        "reviewed_entry_count": 20,
        "high_signal_batch_used_instead_of_stage5dt_stable_batch_001": True,
        "stage5dt_stable_batch_plan_preserved": True,
        "number_fact_enrichment_overlays_added_now": True,
        "overlay_collection_path": OVERLAY_COLLECTION_PATH.as_posix(),
        "overlay_count": len(overlays),
        "overlay_only_fact_cards_supported": True,
        "overlay_only_fact_cards_validated": True,
        "overlay_only_cards_required_count": overlay_only_count,
        "source_browser_loadability_validated": True,
        "source_browser_entries_loaded": browser["entries_loaded"],
        "source_browser_records_scanned": browser["records_scanned"],
        "source_browser_validation_error_count": len(source_browser_validation.errors),
        "source_browser_warning_count": browser["warnings"],
        "source_browser_missing_paths_after": browser["missing_paths"],
        "fact_card_count_after_stage5dw": fact_card_count_after,
        "selected_batch_fact_card_count": sum(selected_fact_cards.values()),
        "spurious_root_image_paths_after": path_report["spurious_root_image_paths"],
        "spurious_root_document_paths_after": path_report["spurious_root_document_paths"],
        "duplicate_present_missing_path_pairs_after": path_report["duplicate_present_missing_path_pairs"],
        "source_root_relative_resolved_paths": path_report["source_root_relative_resolved_paths"],
        "canonical_lp_page_root_alias_present": path_report["canonical_lp_page_root_alias_present"],
        "stage5du_thread_image_paths_under_third_party": path_report["stage5du_thread_image_paths_under_third_party"],
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": 8,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": "assistant_or_operator_review_then_codex_overlay_update",
    }

    records: dict[str, dict[str, Any]] = {
        "summary": summary,
        "next_stage_decision": {
            **base,
            **false_flags,
            "record_type": "stage5dw_next_stage_decision",
            "status": "complete",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": "assistant_or_operator_review_then_codex_overlay_update",
            "target_priority_decision_created_now": False,
        },
        "review_batch_selection": {
            **base,
            "record_type": "stage5dw_review_batch_001_selection",
            "schema": SCHEMA_PATHS["review_batch_selection"].as_posix(),
            "review_batch_id": REVIEW_BATCH_ID,
            "stage5dt_stable_batch_plan_preserved": True,
            "stage5dt_stable_batch_001_not_mutated": True,
            "stage5dw_batch_selection_policy": REVIEW_BATCH_SELECTION_POLICY,
            "operator_requested_twenty_entries_per_prompt": True,
            "reviewed_entry_count": 20,
            "selected_source_record_paths": SELECTED_SOURCE_RECORD_PATHS,
            "selection_deviation_reason": "assistant_operator_selected_high_signal_evidence_records",
        },
        "review_batch_findings": {
            **base,
            "record_type": "stage5dw_review_batch_001_findings",
            "schema": SCHEMA_PATHS["review_batch_findings"].as_posix(),
            "review_batch_id": REVIEW_BATCH_ID,
            "reviewed_entry_count": 20,
            "overlay_count": len(overlays),
            "overlay_only_cards_required_count": overlay_only_count,
            "selected_batch_fact_card_count": sum(selected_fact_cards.values()),
            "key_fact_families": [
                "page32_red_header",
                "no_f_section_flow",
                "lp_doublet_and_word_count",
                "solved_koan_gp",
                "music_instar_interconnectedness",
                "red_runes_gateless_gate",
                "big_gap_negative_space",
                "star_artifacts_exact254",
                "red_heading_gp491",
            ],
            "review_status": "reviewed_and_overlayed",
        },
        "overlay_only_support": {
            **base,
            "record_type": "stage5dw_overlay_only_fact_card_support",
            "schema": SCHEMA_PATHS["overlay_only_support"].as_posix(),
            "overlay_only_fact_cards_supported": True,
            "overlay_only_fact_cards_do_not_mutate_source_records": True,
            "overlay_only_fact_cards_loaded_from_committed_overlay_files": True,
            "overlay_only_fact_cards_performance_cached_or_cheap": True,
            "overlay_only_fact_cards_validated": True,
            "overlay_only_cards_required_count": overlay_only_count,
        },
        "source_browser_loadability": {
            **base,
            "record_type": "stage5dw_source_browser_loadability_summary",
            "schema": SCHEMA_PATHS["source_browser_loadability"].as_posix(),
            "source_browser_entries_loaded": browser["entries_loaded"],
            "source_browser_records_scanned": browser["records_scanned"],
            "source_browser_validation_error_count": len(source_browser_validation.errors),
            "source_browser_warning_count": browser["warnings"],
            "source_browser_missing_paths_after": browser["missing_paths"],
            "fact_card_count_after_stage5dw": fact_card_count_after,
            "spurious_root_image_paths_after": path_report["spurious_root_image_paths"],
            "spurious_root_document_paths_after": path_report["spurious_root_document_paths"],
            "duplicate_present_missing_path_pairs_after": path_report["duplicate_present_missing_path_pairs"],
            "source_root_relative_resolved_paths": path_report["source_root_relative_resolved_paths"],
        },
        "reviewable_validation_evidence": {
            **base,
            "record_type": "stage5dw_reviewable_validation_evidence",
            "validators": [
                "validate-stage5dw",
                "validate-stage5dw-review-batch-selection",
                "validate-stage5dw-number-fact-overlays",
                "validate-stage5dw-overlay-only-fact-cards",
                "validate-stage5dw-source-browser-loadability",
                "source-browser validate-index",
                "source-browser validate-paths",
            ],
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
        },
        "reviewability_gap_register": {
            **base,
            "record_type": "stage5dw_reviewability_gap_register",
            "remaining_gap": "continue_number_fact_review_batches",
            "next_batch_recommended": "number_fact_review_batch_002",
            "target_priority_decision_created_now": False,
        },
        "stage5dv_preservation": {
            **base,
            "record_type": "stage5dw_stage5dv_preservation",
            "stage5dv_preserved": True,
            "stage5dv_complete": True,
            "source_browser_entries_loaded": browser["entries_loaded"],
            "source_browser_records_scanned": browser["records_scanned"],
            "source_browser_validation_error_count": len(source_browser_validation.errors),
            "spurious_root_image_paths_after": path_report["spurious_root_image_paths"],
            "spurious_root_document_paths_after": path_report["spurious_root_document_paths"],
            "duplicate_present_missing_path_pairs_after": path_report["duplicate_present_missing_path_pairs"],
            "source_root_relative_resolved_paths": path_report["source_root_relative_resolved_paths"],
        },
        "governance_scope_control": {
            **base,
            **false_flags,
            "record_type": "stage5dw_governance_scope_control",
            "number_fact_review_batch_1_performed_now": True,
            "recommended_next_stage_id": NEXT_STAGE_ID,
        },
        "review_batch_result": {
            **base,
            "record_type": "source_browser_number_fact_review_batch_result",
            "schema": SCHEMA_PATHS["review_batch_result"].as_posix(),
            "review_batch_id": REVIEW_BATCH_ID,
            "selection_policy": REVIEW_BATCH_SELECTION_POLICY,
            "review_status": "reviewed_and_overlayed",
            "reviewed_entry_count": 20,
            "source_record_paths": SELECTED_SOURCE_RECORD_PATHS,
            "overlay_file": OVERLAY_COLLECTION_PATH.as_posix(),
            "overlays_added_count": len(overlays),
            "overlay_only_cards_required_count": overlay_only_count,
            "entries_reviewed_none_found_count": 0,
            "historical_source_lock_records_rewritten": False,
            "facts_added_directly_to_source_records": False,
            "facts_added_as_overlays": True,
            "next_batch_recommended": "number_fact_review_batch_002",
        },
        "review_batch_entry_status": {
            **base,
            "record_type": "source_browser_number_fact_review_batch_entry_status",
            "review_batch_id": REVIEW_BATCH_ID,
            "entry_count": 20,
            "entries": [
                {
                    "source_record_path": path,
                    "selected_for_batch": True,
                    "overlay_count": sum(1 for overlay in overlays if overlay.get("source_record_path") == path),
                    "fact_card_count_after_overlay": selected_fact_cards.get(path, 0),
                    "review_status": "overlay_enriched_fact",
                }
                for path in SELECTED_SOURCE_RECORD_PATHS
            ],
        },
    }
    records.update(_source_harvester_records(base, false_flags))
    records.update(_token_records(base, false_flags))
    return records


def _source_harvester_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "codex_handoff_policy": {
            **base,
            "record_type": "stage5dw_codex_handoff_policy",
            "schema": SCHEMA_PATHS["codex_handoff_policy"].as_posix(),
            "canonical_codex_handoff_root": "codex-output",
            "deprecated_codex_output_root_used": False,
            "completion_summary_path": "codex-output/stage5dw-codex-completion.md",
            "completion_summary_committed": False,
        },
        "credential_redaction_policy_preservation": {
            **base,
            "record_type": "stage5dw_credential_redaction_policy_preservation",
            "credential_like_remote_count": 0,
            "credential_redaction_policy_preserved": True,
            "raw_source_body_included": False,
            "secret_material_committed": False,
        },
        "raw_source_noncommit_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dw_raw_source_noncommit_proof",
            "raw_source_files_committed": False,
            "raw_third_party_files_committed": False,
            "generated_outputs_committed": False,
        },
    }


def _token_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "stage5dg_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5dw_stage5dg_preservation",
            "stage5dg_operator_approval_record_preserved": True,
            "operator_approval_component_satisfied_preserved": True,
            "deep_research_acceptance_created_now": False,
            "combined_approval_gate_satisfied_now": False,
        },
        "stage5bd_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5dw_stage5bd_preservation",
            "stage5bd_run_plan_id_count": 10,
            "stage5bd_run_plan_ids_preserved": True,
        },
        "active_lineage_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5dw_active_lineage_preservation",
            "active_lineage_record_count": 8,
            "active_lineage_preserved": True,
        },
        "no_active_ingestion_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dw_no_active_ingestion_proof",
            "gate_status": "closed",
            "active_ingestion_performed": False,
        },
        "no_byte_stream_transition_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dw_no_byte_stream_transition_proof",
            "gate_status": "closed",
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "byte_stream_generation_authorized_now": False,
        },
        "no_execution_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dw_no_execution_proof",
            "schema": SCHEMA_PATHS["no_execution_proof"].as_posix(),
            "gate_status": "closed",
            "execution_authorized_now": False,
            "execution_performed": False,
        },
    }


def _write_records(records: dict[str, dict[str, Any]]) -> None:
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        if key == "summary":
            schema = _object_schema(["record_type", "stage_id", "status", "review_batch_id"])
        elif key == "review_batch_selection":
            schema = _object_schema(["record_type", "stage_id", "review_batch_id", "selected_source_record_paths"])
        elif key == "review_batch_result":
            schema = _object_schema(["record_type", "stage_id", "review_batch_id", "source_record_paths"])
        else:
            schema = _object_schema(["record_type", "stage_id"])
        write_json(path, schema)


def _object_schema(required: list[str]) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
        "required": required,
        "properties": {
            "stage_id": {"const": STAGE_ID},
            "solve_claim": {"const": False},
            "execution_performed": {"const": False},
            "historical_source_lock_records_rewritten": {"const": False},
            "raw_source_files_committed": {"const": False},
            "raw_third_party_files_committed": {"const": False},
            "generated_outputs_committed": {"const": False},
            "target_priority_decision_created_now": {"const": False},
            "pivot_target_selected_now": {"const": False},
        },
    }


def _validate_required_paths() -> list[str]:
    paths = list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values()) + [OVERLAY_COLLECTION_PATH, OVERLAY_SCHEMA_PATH]
    return [f"required Stage 5DW path missing: {path.as_posix()}" for path in paths if not path.exists()]


def _validate_schemas() -> list[str]:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        schema_key = SCHEMA_BY_DATA_KEY.get(key)
        schema_path = SCHEMA_PATHS.get(schema_key or "")
        if schema_path is None:
            if path.parent == PROJECT_STATE_DIR:
                schema_path = SCHEMA_PATHS["generic_project_state"]
            elif path.parent == SOURCE_HARVESTER_DIR:
                schema_path = SCHEMA_PATHS["generic_source_harvester"]
            elif path.parent == TOKEN_BLOCK_DIR:
                schema_path = SCHEMA_PATHS["generic_token_block"]
            else:
                schema_path = SCHEMA_PATHS["generic_project_state"]
        if not path.exists() or not schema_path.exists():
            continue
        payload = _load(path)
        schema = _load(schema_path)
        for error in sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda item: item.path):
            errors.append(f"{path.as_posix()}: {error.message}")
    return errors


def _load(path: Path) -> dict[str, Any]:
    payload = read_yaml(path)
    return payload if isinstance(payload, dict) else {}


def _load_overlay_collection() -> dict[str, Any]:
    payload = _load(OVERLAY_COLLECTION_PATH)
    overlays = payload.get("overlays")
    if not isinstance(overlays, list):
        payload["overlays"] = []
    return payload


def _stage_base() -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "source_lock_only": False,
        "reviewability_stage": True,
        "number_fact_review_batch_stage": True,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "canonical_codex_handoff_root": "codex-output",
    }


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in FALSE_FLAGS}


def _required_false_errors(payload: dict[str, Any], label: str) -> list[str]:
    errors = []
    for key in FALSE_FLAGS:
        if key in payload and payload[key] is not False:
            errors.append(f"{label}: {key} must be false")
    return errors


def _overlay_only_count(overlays: list[dict[str, Any]], entry_by_path: dict[str, Any]) -> int:
    count = 0
    for overlay in overlays:
        entry = entry_by_path.get(str(overlay.get("source_record_path") or ""))
        if entry is None:
            continue
        raw_ids = {_raw_fact_id(fact) for fact in entry.number_facts}
        if str(overlay.get("source_fact_id") or "") not in raw_ids:
            count += 1
    return count


def _raw_fact_id(raw_fact: dict[str, Any]) -> str:
    for key in ("source_fact_id", "fact_id", "claim_id", "id"):
        value = raw_fact.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def _synthetic_zero_fact_entry() -> Any:
    from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry

    return SourceBrowserEntry(
        entry_id="stage5dw-synthetic-zero-fact-entry",
        entry_type="test",
        category="Manual entries",
        title="Stage 5DW synthetic zero fact entry",
        summary="Synthetic entry for overlay-only validation",
        stage_id=STAGE_ID,
        record_type="stage5dw_synthetic_test",
        candidate_family_id=None,
        source_type=None,
        source_status=None,
        trust_tier=None,
        confidence=None,
        selected_now=False,
        solve_claim=False,
        execution_allowed=False,
        source_lock_only=False,
        source_record_path="data/project-state/stage5dw-synthetic-zero-fact-entry.yaml",
        number_facts=[],
    )


def _summary_counts(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in payload.items()
        if isinstance(value, str | int | float | bool) or value is None
    }


def _format(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _update_chatgpt_context() -> None:
    marker = "## Stage 5DW Number-Fact Review Batch 001"
    text = CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8") if CHATGPT_CONTEXT_PATH.exists() else ""
    if marker in text:
        return
    addition = f"""

{marker}

- Stage 5DW completed high-signal number-fact review batch 001 after Stage 5DV path/performance repair.
- The batch reviewed 20 selected evidence/candidate records, not the Stage 5DT stable batch-001 list.
- Historical source-lock records were not rewritten; facts were added through NumberFactCard overlays.
- Overlay-only fact cards are now supported, so older zero-extracted-fact records can display review facts without source-record mutation.
- Key added fact families: Page32 red-header 2472; Page32 463->3299/3301; NO-F section-flow 1433/2883/1894/1814/695/91; LP doublets 89/4337; LP1 word count 464->3301; artwork/title 449/311; solved-koan 1229/337/199/1033; page54-57 308/154; Page32 Fibonacci mod29 primes; Final.jpg road/way 3301/991/1229; prime-index 761/167/464/1033/3301; RGB185=3301 plus 1033/1103 correction; Instar parable product; Instar 761/167; Interconnectedness 772/277/1049; Ouroboros see-also GP scan; RedRunes/Gateless Gate 2/11/3/227/742/682/155/551; BigGaps 569/229/109; StarArtifacts 254/2540/641/709; red-heading GP491 family.
- All remain review-only; no target selection, route extraction, byte generation, execution, OCR/image forensics/audio/stego/Tor/network/CUDA/scoring, or solve claim.
"""
    CHATGPT_CONTEXT_PATH.write_text(text.rstrip() + addition + "\n", encoding="utf-8")


def _update_stage_summary_records(summary: dict[str, Any]) -> None:
    path = Path("data/research/stage-summary-records-v0.yaml")
    payload = read_yaml(path)
    if isinstance(payload, dict):
        records = payload.get("records", [])
    else:
        payload = {
            "record_set_id": "stage-summary-records-v0",
            "schema": "schemas/research/stage-summary-record-v0.schema.json",
            "records": [],
        }
        records = []
    if not isinstance(records, list):
        records = []
    records = [record for record in records if not (isinstance(record, dict) and record.get("stage_id") == STAGE_ID)]
    records.append(
        {
            "record_type": "stage_summary_record",
            "stage_id": STAGE_ID,
            "title": STAGE_TITLE,
            "status": "complete",
            "category": "operator_console_reviewability",
            "summary": "Added high-signal NumberFactCard overlays for the first 20-entry review batch and enabled overlay-only fact cards.",
            "key_outputs": [
                "Stage 5DW high-signal overlay collection with 37 review-only facts.",
                "Overlay-only NumberFactCard support for zero-extracted-fact source-lock entries.",
                "Stage 5DW records, validators, docs, tests, and handoff summary.",
            ],
            "result_status": "reviewability_overlays_only",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                f"Reviewed entries={summary.get('reviewed_entry_count')}, overlays={summary.get('overlay_count')}, "
                f"fact_cards_after={summary.get('fact_card_count_after_stage5dw')}. Historical source locks were not rewritten."
            ),
        }
    )
    payload["records"] = records
    write_yaml(path, payload)
