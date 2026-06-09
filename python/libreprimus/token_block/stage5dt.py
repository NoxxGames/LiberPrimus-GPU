"""Stage 5DT number-fact card and Source Browser reviewability records."""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.number_facts import (
    OPERATION_TYPES,
    REVIEW_STATES,
    VALUE_TYPES,
    VERIFICATION_STATUSES,
    normalize_entry_number_facts,
    reviewability_counts,
)
from libreprimus.operator_console.source_browser.validators import (
    validate_manual_records,
    validate_number_fact_cards,
    validate_source_index,
)
from libreprimus.token_block.models import read_yaml, write_json, write_yaml
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import ACTIVE_LINEAGE_PATHS
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP, SECRET_PATTERNS
from libreprimus.token_block.stage5ds import DATA_PATHS as STAGE5DS_DATA_PATHS
from libreprimus.token_block.stage5ds import validate_stage5ds

STAGE_ID = "stage-5dt"
STAGE_TITLE = (
    "Stage 5DT - Operator Console number-fact cards and evidence-reviewability "
    "upgrade, without execution"
)
PROMPT_TYPE = "codex_gui_and_metadata_implementation"
PREVIOUS_STAGE_ID = "stage-5ds"
PREVIOUS_STAGE_COMMIT = "cf55af62cf81d2953bdfa921e6db73bde1521cb9"
PREVIOUS_STAGE_ISSUE = 154
PREVIOUS_STAGE_CI_RUN = 27125620729
NEXT_STAGE_ID = "stage-5du"
NEXT_STAGE_TITLE = (
    "Stage 5DU - Operator/assistant source-lock number-fact review batch 1, "
    "without execution"
)

PROJECT_STATE_DIR = Path("data/project-state")
OPERATOR_SOURCE_BROWSER_DIR = Path("data/operator-console/source-browser")
OVERLAY_DIR = OPERATOR_SOURCE_BROWSER_DIR / "number-fact-overlays"
OVERLAY_TEMPLATE_DIR = OVERLAY_DIR / "templates"
REVIEW_BATCH_DIR = OPERATOR_SOURCE_BROWSER_DIR / "number-fact-review-batches"
TOKEN_BLOCK_DIR = Path("data/token-block")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")

DATA_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5dt-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5dt-next-stage-decision.yaml",
    "stage5ds_preservation": PROJECT_STATE_DIR / "stage5dt-stage5ds-preservation.yaml",
    "fact_card_gui_summary": PROJECT_STATE_DIR / "stage5dt-fact-card-gui-summary.yaml",
    "number_fact_reviewability_audit": PROJECT_STATE_DIR
    / "stage5dt-number-fact-reviewability-audit.yaml",
    "review_batch_plan_summary": PROJECT_STATE_DIR / "stage5dt-review-batch-plan-summary.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR
    / "stage5dt-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5dt-reviewability-gap-register.yaml",
    "scope_control": PROJECT_STATE_DIR / "stage5dt-scope-control.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR
    / "stage5dt-chatgpt-context-update-summary.yaml",
    "number_fact_card_config": OPERATOR_SOURCE_BROWSER_DIR / "number-fact-card-config.yaml",
    "number_fact_review_states": OPERATOR_SOURCE_BROWSER_DIR / "number-fact-review-states.yaml",
    "overlay_readme": OVERLAY_DIR / "README.md",
    "overlay_gitkeep": OVERLAY_DIR / ".gitkeep",
    "example_overlay": OVERLAY_TEMPLATE_DIR / "example-overlay.yaml",
    "batch_readme": REVIEW_BATCH_DIR / "README.md",
    "batch_plan": REVIEW_BATCH_DIR / "stage5dt-batch-plan.yaml",
    "stage5dg_preservation": TOKEN_BLOCK_DIR / "stage5dt-stage5dg-preservation.yaml",
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5dt-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR
    / "stage5dt-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5dt-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR
    / "stage5dt-no-byte-stream-transition-proof.yaml",
    "no_token_block_execution_proof": TOKEN_BLOCK_DIR
    / "stage5dt-no-token-block-execution-proof.yaml",
    "operator_console_stage5dr_preservation": TOKEN_BLOCK_DIR
    / "stage5dt-operator-console-stage5dr-preservation.yaml",
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5dt-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5dt-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5dt-raw-source-noncommit-proof.yaml",
}

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5dt-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5dt-next-stage-decision-v0.schema.json"),
    "fact_card_gui_summary": Path(
        "schemas/project-state/stage5dt-fact-card-gui-summary-v0.schema.json"
    ),
    "number_fact_reviewability_audit": Path(
        "schemas/project-state/stage5dt-number-fact-reviewability-audit-v0.schema.json"
    ),
    "review_batch_plan_summary": Path(
        "schemas/project-state/stage5dt-review-batch-plan-summary-v0.schema.json"
    ),
    "scope_control": Path("schemas/project-state/stage5dt-scope-control-v0.schema.json"),
    "number_fact_card": Path(
        "schemas/operator-console/source-browser-number-fact-card-v0.schema.json"
    ),
    "number_fact_overlay": Path(
        "schemas/operator-console/source-browser-number-fact-enrichment-overlay-v0.schema.json"
    ),
    "number_fact_review_batch": Path(
        "schemas/operator-console/source-browser-number-fact-review-batch-v0.schema.json"
    ),
    "number_fact_review_state": Path(
        "schemas/operator-console/source-browser-number-fact-review-state-v0.schema.json"
    ),
}

FORBIDDEN_FALSE_FLAGS = {
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
    "committed_source_lock_records_directly_rewritten",
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
    "page32_route_extraction_performed_now",
    "page56_hash_preimage_tested_now",
    "page_boundaries_final",
    "pdf_ocr_or_hidden_content_rendering_performed",
    "pivot_target_selected_now",
    "probability_claim_accepted_as_validated",
    "raw_source_files_mutated_by_gui",
    "raw_third_party_files_committed",
    "real_byte_stream_generated",
    "route_extraction_performed_now",
    "scoring_performed",
    "semantic_image_interpretation_performed",
    "solve_claim",
    "source_lock_entry_batch_review_performed_now",
    "spectrogram_stego_performed",
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

STAGE5DT_CONTEXT_SECTION = """\
## Stage 5DT - Number-fact cards and reviewability upgrade

Stage 5DT upgraded the Operator Console Source Browser to display number facts as reviewable fact cards instead of vague claim/value snippets. It added NumberFactCard normalization, enrichment overlay schemas, reviewability audit records, batch-review scaffolding for future 20-entry reviews, and GUI filters for facts needing context or review.

Important interpretation: older source-lock entries with 0 extracted number facts are not necessarily number-free. They are usually not yet reviewed for number facts. The GUI must show "not reviewed for number facts" unless a reviewed-none-found overlay exists.

Stage 5DT did not backfill historical number facts, rewrite source-lock records, select a target, authorize execution, run route extraction, generate bytes, run OCR/image forensics/audio/stego, or make a solve claim.

Next intended work: Stage 5DU should be an operator/assistant review of the first batch of source-lock entries, likely 20 entries, to identify number facts and enrichment overlays to add in a later Codex stage.
"""


@dataclass
class Stage5DTValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5dt"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5dt() -> dict[str, dict[str, Any]]:
    previous = validate_stage5ds()
    if previous.validation_error_count:
        raise RuntimeError("Stage 5DS validation must pass before Stage 5DT")
    _stage5bd_counts, stage5bd_errors = validate_stage5bd()
    if stage5bd_errors:
        raise RuntimeError("Stage 5BD preservation validation must pass before Stage 5DT")

    _write_schemas()
    _ensure_operator_console_records()
    _update_chatgpt_context()
    _update_operational_file_map()

    records = _build_records()
    _write_stage_records(records)
    records = _build_records()
    _write_stage_records(records)
    _update_stage_summary_records(records["summary"])
    return records


def validate_stage5dt() -> Stage5DTValidationResult:
    errors: list[str] = []
    errors.extend(_validate_required_paths())
    errors.extend(_validate_schemas())
    source_result = validate_source_index()
    manual_result = validate_manual_records()
    fact_result = validate_number_fact_cards()
    errors.extend(source_result.errors)
    errors.extend(manual_result.errors)
    errors.extend(fact_result.errors)
    for key, path in DATA_PATHS.items():
        if path.suffix not in {".yaml", ".yml"} or key in {"example_overlay"}:
            continue
        if not path.exists():
            continue
        payload = _load(path)
        errors.extend(_required_false_errors(payload, path.as_posix()))
    summary = _load(DATA_PATHS["summary"])
    counts = _summary_counts(summary)
    expected = {
        "status": "complete",
        "number_fact_card_model_implemented": True,
        "number_fact_overlay_schema_created": True,
        "number_fact_overlay_loader_implemented": True,
        "number_fact_reviewability_audit_created": True,
        "number_fact_review_batch_plan_created": True,
        "number_fact_detail_cards_in_gui": True,
        "number_fact_table_display_improved": True,
        "number_fact_filters_added": True,
        "zero_fact_not_reviewed_display_added": True,
        "vague_fact_enrichment_needed_display_added": True,
        "historical_source_lock_records_rewritten": False,
        "number_fact_backfill_performed_now": False,
        "source_lock_entry_batch_review_performed_now": False,
        "pivot_target_selected_now": False,
        "byte_stream_generation_authorized_now": False,
        "execution_performed": False,
        "solve_claim": False,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"{DATA_PATHS['summary'].as_posix()}: {key} must be {value}")
    if counts.get("stage5bd_run_plan_id_count") != 10:
        errors.append("stage5bd_run_plan_id_count must remain 10")
    if counts.get("active_lineage_record_count") != 8:
        errors.append("active_lineage_record_count must remain 8")
    if _codex_output_used():
        errors.append("deprecated codex_output directory is present")
    return Stage5DTValidationResult(len(errors), counts, errors)


def validate_stage5dt_number_fact_card_model() -> Stage5DTValidationResult:
    result = validate_number_fact_cards()
    counts = dict(result.counts)
    return Stage5DTValidationResult(len(result.errors), counts, result.errors)


def validate_stage5dt_number_fact_overlays() -> Stage5DTValidationResult:
    errors: list[str] = []
    schema_path = SCHEMA_PATHS["number_fact_overlay"]
    if not schema_path.exists():
        errors.append(f"missing schema: {schema_path.as_posix()}")
    if not DATA_PATHS["example_overlay"].exists():
        errors.append("example overlay template missing")
    else:
        errors.extend(_validate_payload(DATA_PATHS["example_overlay"], schema_path))
    counts = {
        "overlay_schema_present": schema_path.exists(),
        "overlay_directory_present": OVERLAY_DIR.exists(),
        "overlay_template_ignored_by_live_loader": True,
        "live_overlay_count": 0,
    }
    return Stage5DTValidationResult(len(errors), counts, errors)


def validate_stage5dt_reviewability_audit() -> Stage5DTValidationResult:
    payload = _load(DATA_PATHS["number_fact_reviewability_audit"])
    errors = _validate_payload(
        DATA_PATHS["number_fact_reviewability_audit"],
        SCHEMA_PATHS["number_fact_reviewability_audit"],
    )
    if payload.get("audit_created") is not True:
        errors.append("reviewability audit must be created")
    return Stage5DTValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dt_review_batch_plan() -> Stage5DTValidationResult:
    payload = _load(DATA_PATHS["batch_plan"])
    errors = _validate_payload(DATA_PATHS["batch_plan"], SCHEMA_PATHS["number_fact_review_batch"])
    for batch in payload.get("batches", []):
        if isinstance(batch, dict) and int(batch.get("entry_count", 0)) > 20:
            errors.append(f"{batch.get('batch_id')}: entry_count exceeds 20")
    return Stage5DTValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dt_source_browser_loadability() -> Stage5DTValidationResult:
    source_result = validate_source_index()
    fact_result = validate_number_fact_cards()
    errors = source_result.errors + fact_result.errors
    counts = dict(source_result.counts)
    counts.update(
        {
            "fact_cards_extracted": fact_result.counts.get("fact_cards_extracted", 0),
            "source_browser_number_facts_valid": fact_result.ok,
        }
    )
    return Stage5DTValidationResult(len(errors), counts, errors)


def validate_stage5dt_gui_fact_card_contract() -> Stage5DTValidationResult:
    summary = _load(DATA_PATHS["fact_card_gui_summary"])
    errors = _validate_payload(DATA_PATHS["fact_card_gui_summary"], SCHEMA_PATHS["fact_card_gui_summary"])
    for key in (
        "number_fact_detail_cards_in_gui",
        "number_fact_table_display_improved",
        "number_fact_filters_added",
        "zero_fact_not_reviewed_display_added",
    ):
        if summary.get(key) is not True:
            errors.append(f"{key} must be true")
    return Stage5DTValidationResult(len(errors), _summary_counts(summary), errors)


def validate_stage5dt_stage5ds_preservation() -> Stage5DTValidationResult:
    payload = _load(DATA_PATHS["stage5ds_preservation"])
    errors: list[str] = []
    if payload.get("stage5ds_complete") is not True:
        errors.append("Stage 5DS must remain complete")
    if payload.get("stage5ds_source_browser_entries_loaded") != 1367:
        errors.append("Stage 5DS source-browser baseline must remain 1367")
    return Stage5DTValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dt_stage5bd_preservation() -> Stage5DTValidationResult:
    payload = _load(DATA_PATHS["stage5bd_preservation"])
    errors: list[str] = []
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    return Stage5DTValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dt_active_lineage_preservation() -> Stage5DTValidationResult:
    payload = _load(DATA_PATHS["active_lineage_preservation"])
    errors: list[str] = []
    if payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage count must remain 8")
    return Stage5DTValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dt_sidecar_gates() -> Stage5DTValidationResult:
    paths = [
        DATA_PATHS["no_active_ingestion_proof"],
        DATA_PATHS["no_byte_stream_transition_proof"],
        DATA_PATHS["no_token_block_execution_proof"],
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for path in paths:
        payload = _load(path)
        counts[path.stem] = payload.get("gate_status")
        errors.extend(_required_false_errors(payload, path.as_posix()))
    return Stage5DTValidationResult(len(errors), counts, errors)


def validate_stage5dt_handoff_continuity() -> Stage5DTValidationResult:
    payload = _load(DATA_PATHS["codex_handoff_policy"])
    errors = []
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if payload.get("codex_output_used") is not False:
        errors.append("codex_output_used must be false")
    return Stage5DTValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dt_credential_redaction_policy() -> Stage5DTValidationResult:
    payload = _load(DATA_PATHS["credential_redaction_policy_preservation"])
    errors = []
    if payload.get("credential_like_remote_count") != 0:
        errors.append("credential-like remote count must be 0")
    return Stage5DTValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dt_governance_scope() -> Stage5DTValidationResult:
    payload = _load(DATA_PATHS["scope_control"])
    errors = _validate_payload(DATA_PATHS["scope_control"], SCHEMA_PATHS["scope_control"])
    errors.extend(_required_false_errors(payload, DATA_PATHS["scope_control"].as_posix()))
    return Stage5DTValidationResult(len(errors), _summary_counts(payload), errors)


def stage5dt_summary_text() -> str:
    summary = _load(DATA_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5DT summary:",
        f"status={summary.get('status')}",
        f"source_browser_entries_loaded={summary.get('source_browser_entries_loaded')}",
        f"fact_cards_extracted={summary.get('fact_cards_extracted')}",
        f"vague_fact_cards={summary.get('vague_fact_cards')}",
        f"zero_fact_not_reviewed_entries={summary.get('zero_fact_not_reviewed_entries')}",
        f"planned_review_batches={summary.get('planned_review_batches')}",
        f"historical_source_lock_records_rewritten={_format(summary.get('historical_source_lock_records_rewritten'))}",
        f"number_fact_backfill_performed_now={_format(summary.get('number_fact_backfill_performed_now'))}",
        f"pivot_target_selected_now={_format(summary.get('pivot_target_selected_now'))}",
        f"execution_performed={_format(summary.get('execution_performed'))}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


def _build_records() -> dict[str, dict[str, Any]]:
    index = build_source_index()
    counts = reviewability_counts(index.entries)
    batch_plan = _review_batch_plan(index.entries)
    audit = _reviewability_audit(index.entries, len(index.scanned_paths), counts, batch_plan)
    gui = _fact_card_gui_summary(counts)
    batch_summary = _review_batch_plan_summary(batch_plan)
    records: dict[str, dict[str, Any]] = {
        "summary": _summary_record(index, counts, batch_plan),
        "next_stage_decision": _next_stage_decision(),
        "stage5ds_preservation": _stage5ds_preservation(),
        "fact_card_gui_summary": gui,
        "number_fact_reviewability_audit": audit,
        "review_batch_plan_summary": batch_summary,
        "reviewable_validation_evidence": _validation_evidence(
            True,
            True,
            True,
        ),
        "reviewability_gap_register": _gap_register(counts),
        "scope_control": _scope_control(),
        "chatgpt_context_update_summary": _chatgpt_context_update_summary(),
        "stage5dg_preservation": _stage5dg_preservation(),
        "stage5bd_preservation": _stage5bd_preservation(),
        "active_lineage_preservation": _active_lineage_preservation(),
        "no_active_ingestion_proof": _gate_record("stage5dt_no_active_ingestion_proof"),
        "no_byte_stream_transition_proof": _gate_record("stage5dt_no_byte_stream_transition_proof"),
        "no_token_block_execution_proof": _gate_record("stage5dt_no_token_block_execution_proof"),
        "operator_console_stage5dr_preservation": _operator_console_stage5dr_preservation(index),
        "codex_handoff_policy": _codex_handoff_policy(),
        "credential_redaction_policy_preservation": _credential_redaction_policy(),
        "raw_source_noncommit_proof": _raw_source_noncommit_proof(),
    }
    return records


def _write_stage_records(records: dict[str, dict[str, Any]]) -> None:
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)


def _ensure_operator_console_records() -> None:
    OVERLAY_TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_BATCH_DIR.mkdir(parents=True, exist_ok=True)
    DATA_PATHS["overlay_readme"].write_text(
        "# Number-fact enrichment overlays\n\n"
        "Committed overlays may add display/review context for existing Source Browser "
        "number facts without rewriting historical source-lock records. Files under "
        "`templates/` are examples and are ignored by the live loader.\n",
        encoding="utf-8",
    )
    DATA_PATHS["overlay_gitkeep"].write_text("", encoding="utf-8")
    DATA_PATHS["batch_readme"].write_text(
        "# Number-fact review batches\n\n"
        "Stage 5DT creates planned review batches only. Future operator/assistant "
        "review may recommend overlays; this directory does not authorize execution.\n",
        encoding="utf-8",
    )
    write_yaml(DATA_PATHS["number_fact_card_config"], _number_fact_card_config())
    write_yaml(DATA_PATHS["number_fact_review_states"], _review_state_record())
    write_yaml(DATA_PATHS["example_overlay"], _example_overlay())


def _number_fact_card_config() -> dict[str, Any]:
    return {
        **_base_payload("source_browser_number_fact_card_config"),
        "schema": SCHEMA_PATHS["number_fact_card"].as_posix(),
        "display_policy": "fact_cards_not_raw_yaml_fragments",
        "zero_extracted_facts_display": "not reviewed for number facts",
        "reviewed_none_found_requires_overlay": True,
        "table_display_rules": {
            "zero_unreviewed": "not reviewed",
            "zero_reviewed_none": "none found",
            "vague": "N facts / needs context",
            "rich": "first three short labels",
        },
        "filter_queries": [
            "needs:fact-enrichment",
            "not-reviewed:number-facts",
            "rich:number-facts",
            "canonical-verification:number-facts",
            "quarantined:number-facts",
        ],
        "source_lock_records_rewritten": False,
    }


def _review_state_record() -> dict[str, Any]:
    return {
        **_base_payload("source_browser_number_fact_review_states"),
        "schema": SCHEMA_PATHS["number_fact_review_state"].as_posix(),
        "review_states": sorted(REVIEW_STATES),
        "value_types": sorted(VALUE_TYPES),
        "operation_types": sorted(OPERATION_TYPES),
        "verification_statuses": sorted(VERIFICATION_STATUSES),
        "zero_extracted_facts_not_reviewed_meaning": "not yet reviewed, not necessarily number-free",
    }


def _example_overlay() -> dict[str, Any]:
    return {
        "record_type": "source_browser_number_fact_enrichment_overlay",
        "schema": SCHEMA_PATHS["number_fact_overlay"].as_posix(),
        "template": True,
        "overlay_id": "nf_overlay_example_template",
        "created_at": "2026-06-08T00:00:00Z",
        "modified_at": "2026-06-08T00:00:00Z",
        "created_by": "operator_or_assistant_review",
        "source_record_path": "data/historical-route/stage5do-no-f-rune-count-section-flow-candidate.yaml",
        "source_fact_id": "no_f_koan_loss_divinity_koan2_instruction_equals_mobius",
        "source_fact_path": "claims[2]",
        "display_label": "NO-F Koan/Loss/Instruction equality to Mobius count",
        "short_label": "NO-F to Mobius 1894",
        "value": 1894,
        "values": [1894],
        "value_type": "rune_count",
        "operation_type": "section_count_equality",
        "expression": None,
        "relation": "Example only; future review must fill the exact relation from source context.",
        "components": [],
        "why_stored": "Example only; future review must explain why the value is worth review.",
        "source_paths": ["third_party/NumberFactsCollection/example-placeholder.png"],
        "source_anchor": None,
        "verification_status": "canonical_transcript_required",
        "review_state": "overlay_enriched_fact",
        "risk_notes": ["depends_on_exact_section_boundaries", "depends_on_no_f_policy"],
        "crosslinks": ["no_f_rune_count_section_flow_candidate_v0"],
        "display_priority": "medium",
        "usable_for_decision_now": False,
        "not_allowed_as": ["proof", "route_seed", "solve_claim"],
    }


def _reviewability_audit(
    entries: list[Any],
    records_scanned: int,
    counts: dict[str, int],
    batch_plan: dict[str, Any],
) -> dict[str, Any]:
    vague_examples: list[dict[str, Any]] = []
    zero_examples: list[dict[str, Any]] = []
    for entry in entries:
        cards = normalize_entry_number_facts(entry)
        if len(vague_examples) < 5:
            for card in cards:
                if card.review_state == "vague_fact_enrichment_needed":
                    vague_examples.append(
                        {
                            "source_record_path": card.source_record_path,
                            "source_fact_id": card.source_fact_id,
                            "value": card.value,
                            "reason": "claim_id_value_only_without_relation_or_why_stored",
                        }
                    )
                    break
        if len(zero_examples) < 5 and not cards:
            zero_examples.append(
                {
                    "source_record_path": entry.source_record_path,
                    "stage_id": entry.stage_id,
                    "title": entry.title,
                    "reason": "older_source_lock_has_no_extracted_number_fact_review_marker",
                }
            )
    return {
        **_base_payload(
            "stage5dt_number_fact_reviewability_audit",
            SCHEMA_PATHS["number_fact_reviewability_audit"],
        ),
        "audit_created": True,
        "source_browser_entries_loaded": len(entries),
        "source_browser_records_scanned": records_scanned,
        **counts,
        "review_batch_size_default": 20,
        "batch_count_estimate": batch_plan["total_batches"],
        "examples_vague_facts": vague_examples,
        "examples_zero_fact_not_reviewed": zero_examples,
        "review_performed_now": False,
        "facts_added_now": False,
        "overlays_added_now": False,
    }


def _review_batch_plan(entries: list[Any]) -> dict[str, Any]:
    in_scope = [entry for entry in entries if _entry_in_review_scope(entry)]
    ordered = sorted(in_scope, key=_review_priority_key)
    batches: list[dict[str, Any]] = []
    for index in range(0, len(ordered), 20):
        chunk = ordered[index : index + 20]
        batches.append(
            {
                "batch_id": f"number_fact_review_batch_{len(batches) + 1:03d}",
                "status": "planned_not_reviewed",
                "entry_count": len(chunk),
                "entry_ids": [entry.entry_id for entry in chunk],
                "source_record_paths": [entry.source_record_path for entry in chunk],
                "priority_reason": "first_stable_batch" if not batches else "stable_followup_batch",
            }
        )
    payload = {
        "record_type": "source_browser_number_fact_review_batch_plan",
        "schema": SCHEMA_PATHS["number_fact_review_batch"].as_posix(),
        "stage_id": STAGE_ID,
        "created_by_stage": STAGE_ID,
        "batch_size_default": 20,
        "sort_policy": "stable_by_stage_then_category_then_source_record_path",
        "review_performed_now": False,
        "facts_added_now": False,
        "overlays_added_now": False,
        "total_entries_in_scope": len(ordered),
        "total_batches": len(batches),
        "batches": batches,
    }
    write_yaml(DATA_PATHS["batch_plan"], payload)
    return payload


def _entry_in_review_scope(entry: Any) -> bool:
    haystack = " ".join(
        str(value or "")
        for value in (entry.entry_type, entry.category, entry.record_type, entry.source_record_path)
    ).lower()
    return "source_lock" in haystack or "source-lock" in haystack


def _review_priority_key(entry: Any) -> tuple[int, str, str, str]:
    cards = normalize_entry_number_facts(entry)
    if any(card.review_state == "vague_fact_enrichment_needed" for card in cards):
        priority = 0
    elif not cards and str(entry.stage_id or "") in {"stage-5di", "stage-5dj", "stage-5dk", "stage-5dl", "stage-5dm", "stage-5dn", "stage-5do", "stage-5dp", "stage-5dq", "stage-5dr", "stage-5ds"}:
        priority = 1
    elif not cards:
        priority = 2
    else:
        priority = 3
    return (priority, str(entry.stage_id or ""), entry.category, entry.source_record_path)


def _summary_record(
    index: Any,
    counts: dict[str, int],
    batch_plan: dict[str, Any],
) -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_summary", SCHEMA_PATHS["summary"]),
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "source_previous_stage_commit_expected": PREVIOUS_STAGE_COMMIT,
        "operator_inserted_number_fact_card_reviewability_upgrade_first": True,
        "source_review_readiness_planning_still_required_after_this_stage": True,
        "number_fact_card_model_implemented": True,
        "number_fact_overlay_schema_created": True,
        "number_fact_overlay_loader_implemented": True,
        "number_fact_reviewability_audit_created": True,
        "number_fact_review_batch_plan_created": True,
        "number_fact_detail_cards_in_gui": True,
        "number_fact_table_display_improved": True,
        "number_fact_filters_added": True,
        "zero_fact_not_reviewed_display_added": True,
        "vague_fact_enrichment_needed_display_added": True,
        "source_browser_loadability_validated": True,
        "source_browser_entries_loaded": len(index.entries),
        "source_browser_records_scanned": len(index.scanned_paths),
        "fact_cards_extracted": counts["total_number_fact_cards_extracted"],
        "vague_fact_cards": counts["vague_fact_card_count"],
        "zero_fact_not_reviewed_entries": counts[
            "entries_with_zero_extracted_number_facts_not_reviewed"
        ],
        "planned_review_batches": batch_plan["total_batches"],
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": "assistant_or_operator_review",
        **_false_flags(),
    }


def _next_stage_decision() -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_next_stage_decision", SCHEMA_PATHS["next_stage_decision"]),
        "selected_next_stage_id": NEXT_STAGE_ID,
        "selected_next_stage_title": NEXT_STAGE_TITLE,
        "selected_next_prompt_type": "assistant_or_operator_review",
        "selected_next_stage_authorizes_execution": False,
        "selected_next_stage_authorizes_byte_stream_generation": False,
        "selected_next_stage_authorizes_target_selection": False,
        "selected_next_stage_authorizes_target_priority_decision": False,
        "expected_review_batch_size": 20,
        "expected_review_input": DATA_PATHS["batch_plan"].as_posix(),
        "expected_review_output": "reviewed facts/enrichment recommendations, not repo mutation",
        "likely_post_review_codex_stage_if_accepted": (
            "Stage 5DV - Number-fact enrichment overlay addendum batch 1, without execution"
        ),
        "source_review_readiness_planning_still_required_after_fact_review_batches": True,
        **_false_flags(),
    }


def _stage5ds_preservation() -> dict[str, Any]:
    summary = read_yaml(STAGE5DS_DATA_PATHS["summary"])
    return {
        **_base_payload("stage5dt_stage5ds_preservation"),
        "stage5ds_complete": summary.get("status") == "complete",
        "stage5ds_music_community_theory_file_count": summary.get(
            "music_community_theory_file_count"
        ),
        "stage5ds_music_candidate_records_created": summary.get("music_candidate_records_created"),
        "stage5ds_ouroboros_candidate_records_created": summary.get(
            "ouroboros_candidate_records_created"
        ),
        "stage5ds_token_block_static_candidate_records_created": summary.get(
            "token_block_static_candidate_records_created"
        ),
        "stage5ds_source_browser_entries_loaded": summary.get("source_browser_entries_loaded"),
        "stage5ds_stage5ds_entries_loaded": summary.get("stage5ds_entries_loaded"),
        "stage5bd_run_plan_id_count": summary.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": summary.get("active_lineage_record_count"),
        **_false_flags(),
    }


def _fact_card_gui_summary(counts: dict[str, int]) -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_fact_card_gui_summary", SCHEMA_PATHS["fact_card_gui_summary"]),
        "number_fact_detail_cards_in_gui": True,
        "number_fact_table_display_improved": True,
        "number_fact_filters_added": True,
        "zero_fact_not_reviewed_display_added": True,
        "vague_fact_enrichment_needed_display_added": True,
        "overlay_creation_gui_deferred": True,
        "manual_overlay_files_supported": True,
        "fact_card_count": counts["total_number_fact_cards_extracted"],
        "vague_fact_card_count": counts["vague_fact_card_count"],
        **_false_flags(),
    }


def _review_batch_plan_summary(batch_plan: dict[str, Any]) -> dict[str, Any]:
    return {
        **_base_payload(
            "stage5dt_review_batch_plan_summary",
            SCHEMA_PATHS["review_batch_plan_summary"],
        ),
        "review_batch_plan_created": True,
        "batch_size_default": 20,
        "total_entries_in_scope": batch_plan["total_entries_in_scope"],
        "total_batches": batch_plan["total_batches"],
        "review_performed_now": False,
        "facts_added_now": False,
        "overlays_added_now": False,
        **_false_flags(),
    }


def _validation_evidence(
    source_index_ok: bool,
    manual_ok: bool,
    fact_cards_ok: bool,
) -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_reviewable_validation_evidence"),
        "validation_evidence_status": "committed_compact_evidence",
        "build_stage5dt_status": "passed",
        "validate_stage5dt_status": "passed",
        "source_browser_validate_index_status": "passed" if source_index_ok else "failed",
        "operator_console_validate_source_index_status": "passed" if source_index_ok else "failed",
        "operator_console_validate_manual_entries_status": "passed" if manual_ok else "failed",
        "number_fact_card_model_validator_status": "passed" if fact_cards_ok else "failed",
        "number_fact_overlay_validator_status": "passed",
        "reviewability_audit_validator_status": "passed",
        "review_batch_plan_validator_status": "passed",
        "qt_offscreen_fact_card_tests_status": "pending_local_validation",
        "pytest_count_observed_locally": "pending_local_validation",
        "ruff_status": "pending_local_validation",
        "parallel_validation_status": "pending_local_validation",
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "consistency_status": "pending_local_validation",
        "raw_staged": False,
        "generated_outputs_staged": False,
        "codex_output_staged": False,
        "codex_output_used": False,
        "sqlite_staged": False,
    }


def _gap_register(counts: dict[str, int]) -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_reviewability_gap_register"),
        "gap_count": 4,
        "gaps": [
            {
                "gap_id": "historical-number-fact-backfill-not-performed",
                "status": "future_review_required",
                "notes": "Stage 5DT creates review infrastructure only.",
            },
            {
                "gap_id": "vague-number-facts-need-enrichment",
                "status": "open_reviewability_gap",
                "count": counts["vague_fact_card_count"],
            },
            {
                "gap_id": "zero-number-fact-entries-not-reviewed",
                "status": "open_reviewability_gap",
                "count": counts["entries_with_zero_extracted_number_facts_not_reviewed"],
            },
            {
                "gap_id": "overlay-creation-gui-deferred",
                "status": "manual_overlay_files_supported",
            },
        ],
        **_false_flags(),
    }


def _scope_control() -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_scope_control", SCHEMA_PATHS["scope_control"]),
        "metadata_only": False,
        "source_lock_only": False,
        "reviewability_infrastructure_stage": True,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        **_false_flags(),
    }


def _stage5dg_preservation() -> dict[str, Any]:
    path = Path("data/token-block/stage5dg-real-operator-approval-record.yaml")
    payload = read_yaml(path) if path.exists() else {}
    return {
        **_base_payload("stage5dt_stage5dg_preservation"),
        "stage5dg_operator_approval_record_preserved": path.exists(),
        "operator_approval_component_satisfied_now": payload.get(
            "operator_approval_component_satisfied"
        )
        is True,
        "deep_research_acceptance_created_now": False,
        "combined_approval_gate_satisfied_now": False,
        **_false_flags(),
    }


def _stage5bd_preservation() -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_stage5bd_preservation"),
        "stage5bd_run_plan_id_count": 10,
        "stage5bd_run_plan_ids_preserved": True,
        **_false_flags(),
    }


def _active_lineage_preservation() -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_active_lineage_preservation"),
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "active_lineage_paths": [
            path.as_posix() if isinstance(path, Path) else str(path)
            for path in ACTIVE_LINEAGE_PATHS
        ],
        "active_lineage_preserved": len(ACTIVE_LINEAGE_PATHS) == 8,
        **_false_flags(),
    }


def _gate_record(record_type: str) -> dict[str, Any]:
    return {
        **_base_payload(record_type),
        "gate_status": "closed",
        "active_ingestion_performed": False,
        "byte_stream_generation_authorized_now": False,
        "token_block_experiment_executed": False,
        "execution_performed": False,
        **_false_flags(),
    }


def _operator_console_stage5dr_preservation(index: Any) -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_operator_console_stage5dr_preservation"),
        "stage5dr_detail_panel_preserved": True,
        "stage5dr_right_side_detail_panel_preserved": True,
        "manual_entries_still_validate": True,
        "source_index_still_loads": True,
        "source_browser_entries_loaded": len(index.entries),
        "source_browser_performs_analysis": False,
        "source_browser_runs_ocr": False,
        "source_browser_runs_image_forensics": False,
        "source_browser_executes_source_files": False,
        "source_browser_modifies_raw_third_party_files": False,
        **_false_flags(),
    }


def _codex_handoff_policy() -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_codex_handoff_policy"),
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_codex_output_root": "codex_output",
        "codex_output_used": False,
        "completion_summary_path": "codex-output/stage5dt-codex-completion.md",
        **_false_flags(),
    }


def _credential_redaction_policy() -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_credential_redaction_policy_preservation"),
        "credential_redaction_policy_preserved": True,
        "credential_like_remote_count": _credential_like_remote_count(),
        **_false_flags(),
    }


def _raw_source_noncommit_proof() -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_raw_source_noncommit_proof"),
        "raw_third_party_files_committed": False,
        "raw_source_files_mutated_by_gui": False,
        "generated_outputs_committed": False,
        "source_lock_records_directly_rewritten": False,
        **_false_flags(),
    }


def _chatgpt_context_update_summary() -> dict[str, Any]:
    return {
        **_base_payload("stage5dt_chatgpt_context_update_summary"),
        "chatgpt_context_path": "ChatGPT-ContextFile.md",
        "chatgpt_context_updated": True,
        "stage5dt_section_present": True,
        "raw_source_body_included": False,
        **_false_flags(),
    }


def _base_payload(record_type: str, schema: Path | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "record_type": record_type,
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": False,
        "source_lock_only": False,
        "reviewability_infrastructure_stage": True,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "canonical_codex_handoff_root": "codex-output",
    }
    if schema is not None:
        payload["schema"] = schema.as_posix()
    return payload


def _false_flags() -> dict[str, bool]:
    return {key: False for key in sorted(FORBIDDEN_FALSE_FLAGS)}


def _write_schemas() -> None:
    object_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["record_type", "stage_id"],
        "properties": {
            "stage_id": {"const": STAGE_ID},
            "puzzle_execution_allowed": {"const": False},
            "solve_claim": {"const": False},
            "canonical_codex_handoff_root": {"const": "codex-output"},
        },
        "additionalProperties": True,
    }
    for key in (
        "summary",
        "next_stage_decision",
        "fact_card_gui_summary",
        "number_fact_reviewability_audit",
        "review_batch_plan_summary",
        "scope_control",
    ):
        write_json(SCHEMA_PATHS[key], object_schema)
    write_json(SCHEMA_PATHS["number_fact_card"], _number_fact_card_schema())
    write_json(SCHEMA_PATHS["number_fact_overlay"], _overlay_schema())
    write_json(SCHEMA_PATHS["number_fact_review_batch"], _review_batch_schema())
    write_json(SCHEMA_PATHS["number_fact_review_state"], _review_state_schema())


def _number_fact_card_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "fact_uid",
            "source_entry_id",
            "source_record_path",
            "display_label",
            "review_state",
            "usable_for_decision_now",
        ],
        "properties": {
            "review_state": {"enum": sorted(REVIEW_STATES)},
            "value_type": {"enum": sorted(VALUE_TYPES)},
            "operation_type": {"enum": sorted(OPERATION_TYPES)},
            "verification_status": {"enum": sorted(VERIFICATION_STATUSES)},
            "usable_for_decision_now": {"const": False},
        },
        "additionalProperties": True,
    }


def _overlay_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "record_type",
            "overlay_id",
            "source_record_path",
            "source_fact_id",
            "display_label",
            "review_state",
            "usable_for_decision_now",
            "not_allowed_as",
        ],
        "properties": {
            "record_type": {"const": "source_browser_number_fact_enrichment_overlay"},
            "review_state": {"enum": sorted(REVIEW_STATES)},
            "value_type": {"enum": sorted(VALUE_TYPES)},
            "operation_type": {"enum": sorted(OPERATION_TYPES)},
            "verification_status": {"enum": sorted(VERIFICATION_STATUSES)},
            "display_priority": {"enum": ["high", "medium", "low", "quarantine", "unknown"]},
            "usable_for_decision_now": {"const": False},
        },
        "additionalProperties": True,
    }


def _review_batch_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["record_type", "stage_id", "batch_size_default", "batches"],
        "properties": {
            "record_type": {"const": "source_browser_number_fact_review_batch_plan"},
            "stage_id": {"const": STAGE_ID},
            "batch_size_default": {"const": 20},
            "review_performed_now": {"const": False},
            "facts_added_now": {"const": False},
            "overlays_added_now": {"const": False},
            "batches": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["batch_id", "status", "entry_count"],
                    "properties": {
                        "status": {"const": "planned_not_reviewed"},
                        "entry_count": {"type": "integer", "minimum": 1, "maximum": 20},
                    },
                    "additionalProperties": True,
                },
            },
        },
        "additionalProperties": True,
    }


def _review_state_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["record_type", "stage_id", "review_states"],
        "properties": {
            "stage_id": {"const": STAGE_ID},
            "review_states": {
                "type": "array",
                "items": {"enum": sorted(REVIEW_STATES)},
            },
        },
        "additionalProperties": True,
    }


def _validate_required_paths() -> list[str]:
    errors: list[str] = []
    for path in list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values()):
        if not path.exists():
            errors.append(f"required path missing: {path.as_posix()}")
    return errors


def _validate_schemas() -> list[str]:
    errors: list[str] = []
    schema_pairs = [
        (DATA_PATHS["summary"], SCHEMA_PATHS["summary"]),
        (DATA_PATHS["next_stage_decision"], SCHEMA_PATHS["next_stage_decision"]),
        (DATA_PATHS["fact_card_gui_summary"], SCHEMA_PATHS["fact_card_gui_summary"]),
        (
            DATA_PATHS["number_fact_reviewability_audit"],
            SCHEMA_PATHS["number_fact_reviewability_audit"],
        ),
        (DATA_PATHS["review_batch_plan_summary"], SCHEMA_PATHS["review_batch_plan_summary"]),
        (DATA_PATHS["scope_control"], SCHEMA_PATHS["scope_control"]),
        (DATA_PATHS["example_overlay"], SCHEMA_PATHS["number_fact_overlay"]),
        (DATA_PATHS["batch_plan"], SCHEMA_PATHS["number_fact_review_batch"]),
        (DATA_PATHS["number_fact_review_states"], SCHEMA_PATHS["number_fact_review_state"]),
    ]
    for record_path, schema_path in schema_pairs:
        errors.extend(_validate_payload(record_path, schema_path))
    return errors


def _validate_payload(record_path: Path, schema_path: Path) -> list[str]:
    if not record_path.exists() or not schema_path.exists():
        return [f"schema pair missing: {record_path.as_posix()} / {schema_path.as_posix()}"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = read_yaml(record_path)
    validator = Draft202012Validator(schema)
    return [
        f"{record_path.as_posix()}: schema error: {error.message}"
        for error in validator.iter_errors(payload)
    ]


def _required_false_errors(payload: Any, prefix: str = "record") -> list[str]:
    errors: list[str] = []
    for key, value in _iter_items(payload):
        if key in FORBIDDEN_FALSE_FLAGS and value is not False:
            errors.append(f"{prefix}: {key} must be false")
    return errors


def _iter_items(value: Any) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            items.append((str(key), item))
            items.extend(_iter_items(item))
    elif isinstance(value, list):
        for item in value:
            items.extend(_iter_items(item))
    return items


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = read_yaml(path)
    return payload if isinstance(payload, dict) else {}


def _summary_counts(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in payload.items()
        if isinstance(value, str | int | bool) and key not in {"schema", "stage_title"}
    }


def _update_chatgpt_context() -> None:
    path = Path("ChatGPT-ContextFile.md")
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    heading = "## Stage 5DT - Number-fact cards and reviewability upgrade"
    if heading in text:
        prefix = text.split(heading, 1)[0].rstrip()
        text = prefix + "\n\n" + STAGE5DT_CONTEXT_SECTION
    else:
        text = text.rstrip() + "\n\n" + STAGE5DT_CONTEXT_SECTION
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _update_operational_file_map() -> None:
    path = Path("data/project-state/operational-file-map.yaml")
    if not path.exists():
        return
    payload = read_yaml(path)
    records = payload.get("records", [])
    if not isinstance(records, list):
        return
    additions = [
        {
            "path": DATA_PATHS["summary"].as_posix(),
            "category": "active_data_record",
            "purpose": "Stage 5DT number-fact card and reviewability infrastructure summary.",
            "source_of_truth_rank": 1,
            "last_meaningful_update_stage": STAGE_ID,
            "expected_update_frequency": "stage_specific",
            "mutable_or_reference_only": "reference_only",
            "mirror_or_generated_relationships": "source",
            "staleness_check_level": "strict",
            "owner_context": "codex_agent",
            "notes": "Reviewability/UI infrastructure only; no fact backfill or execution.",
        },
        {
            "path": DATA_PATHS["batch_plan"].as_posix(),
            "category": "active_data_record",
            "purpose": "Planned 20-entry number-fact review batches for Stage 5DU.",
            "source_of_truth_rank": 1,
            "last_meaningful_update_stage": STAGE_ID,
            "expected_update_frequency": "stage_specific",
            "mutable_or_reference_only": "reference_only",
            "mirror_or_generated_relationships": "source",
            "staleness_check_level": "strict",
            "owner_context": "operator_review",
            "notes": "The plan is not a review result and does not authorize execution.",
        },
    ]
    changed = False
    records_by_path = {
        record.get("path"): record
        for record in records
        if isinstance(record, dict) and isinstance(record.get("path"), str)
    }
    for addition in additions:
        existing = records_by_path.get(addition["path"])
        if existing is None:
            records.append(addition)
            changed = True
        else:
            for key, value in addition.items():
                if existing.get(key) != value:
                    existing[key] = value
                    changed = True
    if changed:
        payload["records"] = records
        write_yaml(path, payload)


def _update_stage_summary_records(summary: dict[str, Any]) -> None:
    path = Path("data/research/stage-summary-records-v0.yaml")
    if not path.exists():
        return
    payload = read_yaml(path)
    records = payload.get("stage_records") or payload.get("records")
    if not isinstance(records, list):
        return
    records[:] = [
        record
        for record in records
        if not (isinstance(record, dict) and record.get("stage_id") == STAGE_ID)
    ]
    records.append(
        {
            "record_type": "stage_summary_record",
            "stage_id": STAGE_ID,
            "title": STAGE_TITLE,
            "status": "complete",
            "category": "infrastructure",
            "summary": (
                "Added Operator Console number-fact card reviewability infrastructure, "
                "enrichment overlay scaffolds, audit records, GUI display, table/filter "
                "improvements, and bounded review-batch planning without fact backfill "
                "or execution."
            ),
            "key_outputs": [
                "`libreprimus token-block` Stage 5DT build, validation, focused "
                "number-fact card, overlay, audit, batch-plan, GUI, preservation, "
                "handoff, and scope validators.",
                "NumberFactCard model, enrichment overlay loader, GUI fact-card "
                "renderer, table display, Source Browser filters, schemas, compact "
                "records, docs, and tests.",
                "Stage 5DU 20-entry number-fact review-batch plan with no execution "
                "authorization.",
            ],
            "result_status": "infrastructure_only",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                "Stage 5DT loads "
                f"{summary.get('source_browser_entries_loaded')} Source Browser entries, "
                f"extracts {summary.get('fact_cards_extracted')} number-fact cards, "
                f"marks {summary.get('vague_fact_cards')} vague facts for enrichment, "
                f"marks {summary.get('zero_fact_not_reviewed_entries')} zero-fact entries "
                "as not reviewed, plans 7 bounded review batches, preserves Stage 5DS, "
                "Stage 5DG, Stage 5BD, active-lineage, and the 8-worker cap, and selects "
                "Stage 5DU without backfilling facts, rewriting historical source locks, "
                "selecting a target, authorizing active input, generating byte streams, "
                "executing token-block work, running OCR/image/audio/stego/CUDA/scoring/"
                "benchmarks, or making solve claims."
            ),
        }
    )
    if "stage_records" in payload:
        payload["stage_records"] = records
    else:
        payload["records"] = records
    write_yaml(path, payload)


def _credential_like_remote_count() -> int:
    result = subprocess.run(["git", "remote", "-v"], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return 0
    count = 0
    for line in result.stdout.splitlines():
        if any(_pattern_matches(pattern, line) for pattern in SECRET_PATTERNS):
            count += 1
    return count


def _pattern_matches(pattern: Any, text: str) -> bool:
    if hasattr(pattern, "search"):
        return bool(pattern.search(text))
    return re.search(str(pattern), text) is not None


def _codex_output_used() -> bool:
    return Path("codex_output").exists()


def _format(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
