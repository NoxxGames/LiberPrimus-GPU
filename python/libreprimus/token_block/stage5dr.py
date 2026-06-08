"""Stage 5DR Operator Console source-browser detail-panel refinement records."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.status_display import (
    STATUS_UNSPECIFIED_LABEL,
    STATUS_UNSPECIFIED_TOOLTIP,
    display_status,
)
from libreprimus.operator_console.source_browser.validators import (
    source_browser_summary,
    validate_manual_records,
    validate_source_index,
)
from libreprimus.token_block.models import read_yaml, write_yaml
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import ACTIVE_LINEAGE_PATHS
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP
from libreprimus.token_block.stage5dq import (
    DATA_PATHS as STAGE5DQ_DATA_PATHS,
    validate_stage5dq,
)

STAGE_ID = "stage-5dr"
STAGE_TITLE = (
    "Stage 5DR - Operator Console Source Browser details panel and interaction fixes, "
    "without puzzle execution"
)
PROMPT_TYPE = "codex_gui_implementation"
SOURCE_PREVIOUS_STAGE_ID = "stage-5dq"
SOURCE_PREVIOUS_STAGE_COMMIT = "a551d8fa50fbb450d0b3231bac8fb4cbbc130d69"
SOURCE_PREVIOUS_ISSUE = 152
SOURCE_PREVIOUS_CI_RUN = 27103705448
NEXT_STAGE_ID = "stage-5ds"
NEXT_STAGE_TITLE = "Stage 5DS - Operator Console source-review readiness planning, without execution"
CODEX_COMPLETION_PATH = Path("codex-output/stage5dr-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

DATA_PATHS = {
    "summary": Path("data/project-state/stage5dr-summary.yaml"),
    "gui_refinement_summary": Path("data/project-state/stage5dr-gui-refinement-summary.yaml"),
    "reviewable_validation_evidence": Path(
        "data/project-state/stage5dr-reviewable-validation-evidence.yaml"
    ),
    "next_stage_decision": Path("data/project-state/stage5dr-next-stage-decision.yaml"),
    "stage5dq_preservation": Path("data/project-state/stage5dr-stage5dq-preservation.yaml"),
    "scope_control": Path("data/project-state/stage5dr-operator-console-scope-control.yaml"),
    "stage5dg_preservation": Path("data/token-block/stage5dr-stage5dg-preservation.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5dr-stage5bd-preservation.yaml"),
    "active_lineage_preservation": Path("data/token-block/stage5dr-active-lineage-preservation.yaml"),
    "no_active_ingestion_proof": Path("data/token-block/stage5dr-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5dr-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path("data/token-block/stage5dr-no-execution-transition-gate.yaml"),
}

SCHEMA_PATHS = {
    "summary": Path("schemas/project-state/stage5dr-summary-v0.schema.json"),
    "gui_refinement_summary": Path(
        "schemas/project-state/stage5dr-gui-refinement-summary-v0.schema.json"
    ),
    "scope_control": Path("schemas/project-state/stage5dr-operator-console-scope-control-v0.schema.json"),
}

FORBIDDEN_FALSE_FLAGS = {
    "activation_authorized_now",
    "activation_decision_valid_now",
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "ai_ml_interpretation_performed",
    "alberti_html_executed_now",
    "audio_stego_performed",
    "benchmark_performed",
    "branch_enumeration_performed",
    "byte_stream_generation_authorized_now",
    "canonical_corpus_active",
    "committed_stage_records_modified_by_gui",
    "committed_source_lock_records_directly_rewritten",
    "cuda_execution_performed",
    "decode_attempt_performed",
    "decryption_attempt_performed_now",
    "disk_cipher_execution_performed_now",
    "dwh_hash_search_performed",
    "execution_authorized_now",
    "execution_performed",
    "full_cartesian_product_enumerated",
    "generated_reports_committed",
    "hash_preimage_search_performed",
    "image_forensics_performed",
    "known_plaintext_attack_performed_now",
    "mayfly_route_extraction_performed_now",
    "method_status_upgraded",
    "mp3stego_execution_performed",
    "network_target_validation_performed_now",
    "ocr_performed",
    "openpuff_execution_performed",
    "operator_readiness_decision_created_now",
    "page32_route_extraction_performed_now",
    "page_boundaries_finalized",
    "pivot_target_selected_now",
    "raw_source_files_mutated_by_gui",
    "raw_third_party_files_committed",
    "raw_third_party_files_mutated_by_gui",
    "raw_webpage_bodies_committed",
    "real_byte_stream_generated",
    "route_extraction_performed_now",
    "scoring_performed",
    "secret_values_printed_or_committed",
    "source_lock_record_semantics_rewritten",
    "solve_claim",
    "spectrogram_stego_performed",
    "target_class_validation_implemented",
    "target_priority_decision_created_now",
    "token_block_experiment_executed",
    "tor_network_access_performed",
    "triangle_route_extraction_performed_now",
    "variant_byte_streams_generated",
    "variant_materialisation_performed",
    "website_expansion_performed",
    "codex_output_used",
}

REQUIRED_SUMMARY_TRUE_FLAGS = {
    "bottom_details_panel_spans_categories_and_table",
    "details_panel_hideable",
    "details_panel_structured_sections",
    "image_thumbnails_in_details_panel",
    "image_thumbnail_click_opens_viewer",
    "url_controls_in_details_panel",
    "file_location_controls_in_details_panel",
    "table_context_menu_added",
    "status_unspecified_display_added",
    "status_legend_or_tooltip_added",
    "stage5dq_preserved",
}


@dataclass
class Stage5DRValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5dr"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5dr() -> dict[str, dict[str, Any]]:
    stage5dq_result = validate_stage5dq()
    if stage5dq_result.validation_error_count:
        raise RuntimeError("Stage 5DQ validation must pass before Stage 5DR")
    _stage5bd_counts, stage5bd_errors = validate_stage5bd()
    if stage5bd_errors:
        raise RuntimeError("Stage 5BD preservation validation must pass before Stage 5DR")
    source_result = validate_source_index()
    manual_result = validate_manual_records()
    source_summary = source_browser_summary()
    stage5dq_summary = read_yaml(STAGE5DQ_DATA_PATHS["summary"])
    base = _base_payload()
    summary = {
        **base,
        "record_type": "stage5dr_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "status": "complete",
        "gui_refinement_stage": True,
        "puzzle_execution_allowed": False,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_commit": SOURCE_PREVIOUS_STAGE_COMMIT,
        "previous_stage_issue": SOURCE_PREVIOUS_ISSUE,
        "previous_stage_ci_run": SOURCE_PREVIOUS_CI_RUN,
        "stage5dq_preserved": True,
        "source_browser_entries_loaded": source_summary["entries_loaded"],
        "source_browser_records_scanned": source_summary["records_scanned"],
        "source_browser_missing_paths": source_summary["missing_paths"],
        "stage5dq_source_browser_entries_loaded_count": stage5dq_summary.get(
            "source_browser_entries_loaded"
        ),
        "stage5dq_source_records_scanned_count": stage5dq_summary.get(
            "source_browser_records_scanned"
        ),
        "stage5dq_missing_local_paths_recorded_as_warnings": stage5dq_summary.get(
            "source_browser_missing_paths"
        ),
        "manual_entry_count": source_summary["manual_entries"],
        "manual_override_count": source_summary["overrides"],
        "tombstone_count": source_summary["tombstones"],
        "bottom_details_panel_spans_categories_and_table": True,
        "details_panel_hideable": True,
        "details_panel_structured_sections": True,
        "image_thumbnails_in_details_panel": True,
        "image_thumbnail_click_opens_viewer": True,
        "url_controls_in_details_panel": True,
        "file_location_controls_in_details_panel": True,
        "table_context_menu_added": True,
        "status_unspecified_display_added": True,
        "status_legend_or_tooltip_added": True,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
    }
    gui = {
        **base,
        "record_type": "stage5dr_gui_refinement_summary",
        "schema": SCHEMA_PATHS["gui_refinement_summary"].as_posix(),
        "layout": "bottom_detail_panel_spanning_category_list_and_table",
        "detail_tabs": [
            "Overview",
            "Media & Files",
            "Number facts",
            "Warnings & links",
            "Raw record",
        ],
        "view_menu_action": "Show Details Panel",
        "toolbar_action": "Toggle Details",
        "thumbnail_size": "128x96",
        "status_unspecified_display": STATUS_UNSPECIFIED_LABEL,
        "status_unspecified_tooltip": STATUS_UNSPECIFIED_TOOLTIP,
        "table_context_menu_actions": [
            "Show Details",
            "Open Image Viewer",
            "Open First File",
            "Open File Location",
            "Open First URL",
            "Copy Entry ID",
            "Copy Source Record Path",
            "Copy First File Path",
            "Copy First URL",
        ],
    }
    validation = {
        **base,
        "record_type": "stage5dr_reviewable_validation_evidence",
        "focused_validators_required": [
            "operator-console validate-source-index",
            "operator-console validate-manual-entries",
            "operator-console summary",
            "source-browser validate-index",
            "token-block build-stage5dr",
            "token-block validate-stage5dr",
            "token-block stage5dr-summary",
        ],
        "source_index_validation_error_count": len(source_result.errors),
        "manual_entry_validation_error_count": len(manual_result.errors),
        "source_browser_entries_loaded": source_summary["entries_loaded"],
        "source_browser_records_scanned": source_summary["records_scanned"],
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
    }
    next_stage = {
        **base,
        "record_type": "stage5dr_next_stage_decision",
        "selected_next_stage_id": NEXT_STAGE_ID,
        "selected_next_stage_title": NEXT_STAGE_TITLE,
        "selection_rationale": (
            "After source-browser usability repair, the next safe step is another "
            "review/planning stage, not puzzle execution."
        ),
    }
    stage5dq_preservation = {
        **base,
        "record_type": "stage5dr_stage5dq_preservation",
        "stage5dq_summary_path": STAGE5DQ_DATA_PATHS["summary"].as_posix(),
        "stage5dq_operator_console_v0_created": True,
        "stage5dq_source_browser_entries_loaded_count": stage5dq_summary.get(
            "source_browser_entries_loaded"
        ),
        "stage5dq_source_records_scanned_count": stage5dq_summary.get(
            "source_browser_records_scanned"
        ),
        "stage5dq_missing_local_paths_recorded_as_warnings": stage5dq_summary.get(
            "source_browser_missing_paths"
        ),
        "manual_entry_semantics_preserved": True,
        "source_lock_record_semantics_rewritten": False,
    }
    scope = {
        **base,
        "record_type": "stage5dr_operator_console_scope_control",
        "schema": SCHEMA_PATHS["scope_control"].as_posix(),
        "scope": "operator_console_source_browser_detail_panel_and_interaction_refinement_only",
        "committed_source_lock_records_read_only": True,
        "manual_entry_semantics_unchanged": True,
        "url_opening_explicit_operator_action_only": True,
        "image_thumbnail_generation_interpretation_free": True,
    }
    records = {
        "summary": summary,
        "gui_refinement_summary": gui,
        "reviewable_validation_evidence": validation,
        "next_stage_decision": next_stage,
        "stage5dq_preservation": stage5dq_preservation,
        "scope_control": scope,
        "stage5dg_preservation": _token_guardrail("stage5dr_stage5dg_preservation"),
        "stage5bd_preservation": _token_guardrail("stage5dr_stage5bd_preservation"),
        "active_lineage_preservation": _token_guardrail("stage5dr_active_lineage_preservation"),
        "no_active_ingestion_proof": _token_guardrail("stage5dr_no_active_ingestion_proof"),
        "no_byte_stream_transition_gate": _token_guardrail("stage5dr_no_byte_stream_transition_gate"),
        "no_execution_transition_gate": _token_guardrail("stage5dr_no_execution_transition_gate"),
    }
    for key, path in DATA_PATHS.items():
        write_yaml(path, records[key])
    return records


def validate_stage5dr() -> Stage5DRValidationResult:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for key, path in DATA_PATHS.items():
        if not path.exists():
            errors.append(f"missing Stage 5DR record: {path.as_posix()}")
            continue
        payload = read_yaml(path)
        if key in SCHEMA_PATHS:
            _validate_schema(path, payload, SCHEMA_PATHS[key], errors)
        _validate_common_payload(path, payload, errors)
    summary = read_yaml(DATA_PATHS["summary"]) if DATA_PATHS["summary"].exists() else {}
    for flag in REQUIRED_SUMMARY_TRUE_FLAGS:
        if summary.get(flag) is not True:
            errors.append(f"{DATA_PATHS['summary'].as_posix()}: {flag} must be true")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output must not exist or be used")
    counts.update(
        {
            "stage_id": summary.get("stage_id", ""),
            "status": summary.get("status", ""),
            "source_browser_entries_loaded": summary.get("source_browser_entries_loaded", 0),
            "bottom_details_panel_spans_categories_and_table": summary.get(
                "bottom_details_panel_spans_categories_and_table", False
            ),
            "details_panel_structured_sections": summary.get("details_panel_structured_sections", False),
            "image_thumbnails_in_details_panel": summary.get("image_thumbnails_in_details_panel", False),
            "table_context_menu_added": summary.get("table_context_menu_added", False),
            "status_unspecified_display_added": summary.get("status_unspecified_display_added", False),
            "route_extraction_performed_now": summary.get("route_extraction_performed_now", False),
            "ocr_performed": summary.get("ocr_performed", False),
            "image_forensics_performed": summary.get("image_forensics_performed", False),
            "execution_performed": summary.get("execution_performed", False),
            "pivot_target_selected_now": summary.get("pivot_target_selected_now", False),
            "recommended_next_stage_id": summary.get("recommended_next_stage_id", ""),
        }
    )
    return Stage5DRValidationResult(len(errors), counts, errors)


def validate_stage5dr_detail_panel() -> Stage5DRValidationResult:
    text = Path("python/libreprimus/operator_console/source_browser/detail_panel.py").read_text(
        encoding="utf-8"
    )
    required = ["EntryDetailPanel", "QTabWidget", "Overview", "Media && Files", "Raw record"]
    errors = [f"detail panel missing {item}" for item in required if item not in text]
    return Stage5DRValidationResult(len(errors), {"detail_panel_structured_sections": not errors}, errors)


def validate_stage5dr_table_context_menu() -> Stage5DRValidationResult:
    text = Path("python/libreprimus/operator_console/main_window.py").read_text(encoding="utf-8")
    required = ["customContextMenuRequested", "_build_table_context_menu", "Copy Entry ID"]
    errors = [f"table context menu missing {item}" for item in required if item not in text]
    return Stage5DRValidationResult(len(errors), {"table_context_menu_added": not errors}, errors)


def validate_stage5dr_status_display() -> Stage5DRValidationResult:
    table_text = Path("python/libreprimus/operator_console/source_browser/table_model.py").read_text(
        encoding="utf-8"
    )
    display = display_status(None)
    errors: list[str] = []
    if display != STATUS_UNSPECIFIED_LABEL:
        errors.append("blank status did not display as unspecified")
    if "STATUS_UNSPECIFIED_TOOLTIP" not in table_text:
        errors.append("blank status tooltip is not wired into table model")
    if "entry.source_status" not in table_text:
        errors.append("table model no longer reads source_status")
    return Stage5DRValidationResult(
        len(errors),
        {"status_unspecified_display": display, "source_status_mutated": False},
        errors,
    )


def validate_stage5dr_image_thumbnail_actions() -> Stage5DRValidationResult:
    text = Path("python/libreprimus/operator_console/source_browser/detail_panel.py").read_text(
        encoding="utf-8"
    )
    required = ["ThumbnailButton", "image_requested", "Open Image Viewer", "Copy SHA/hash"]
    errors = [f"thumbnail action missing {item}" for item in required if item not in text]
    return Stage5DRValidationResult(len(errors), {"image_thumbnail_actions_added": not errors}, errors)


def validate_stage5dr_url_file_actions() -> Stage5DRValidationResult:
    text = Path("python/libreprimus/operator_console/source_browser/detail_panel.py").read_text(
        encoding="utf-8"
    )
    required = ["Open URL", "Copy URL", "Open Location", "Copy Path"]
    errors = [f"url/file action missing {item}" for item in required if item not in text]
    return Stage5DRValidationResult(len(errors), {"url_file_actions_added": not errors}, errors)


def validate_stage5dr_preservation() -> Stage5DRValidationResult:
    result = validate_stage5dr()
    errors = list(result.errors)
    stage5dq_result = validate_stage5dq()
    if stage5dq_result.validation_error_count:
        errors.append("Stage 5DQ validation no longer passes")
    return Stage5DRValidationResult(
        len(errors),
        {
            **result.counts,
            "stage5dq_preserved": stage5dq_result.validation_error_count == 0,
        },
        errors,
    )


def stage5dr_summary_text() -> str:
    summary = read_yaml(DATA_PATHS["summary"])
    keys = [
        "stage_id",
        "status",
        "source_browser_entries_loaded",
        "bottom_details_panel_spans_categories_and_table",
        "details_panel_hideable",
        "details_panel_structured_sections",
        "image_thumbnails_in_details_panel",
        "image_thumbnail_click_opens_viewer",
        "url_controls_in_details_panel",
        "file_location_controls_in_details_panel",
        "table_context_menu_added",
        "status_unspecified_display_added",
        "route_extraction_performed_now",
        "ocr_performed",
        "image_forensics_performed",
        "execution_performed",
        "pivot_target_selected_now",
        "recommended_next_stage_id",
    ]
    return "\n".join(f"{key}={_format(summary.get(key, ''))}" for key in keys)


def _base_payload() -> dict[str, Any]:
    payload: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": False,
        "source_lock_only": False,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "canonical_codex_handoff_root": "codex-output",
    }
    for flag in FORBIDDEN_FALSE_FLAGS:
        payload[flag] = False
    return payload


def _token_guardrail(record_type: str) -> dict[str, Any]:
    return {
        **_base_payload(),
        "record_type": record_type,
        "source_stage5dg_preserved": True,
        "source_stage5bd_preserved": True,
        "active_lineage_preserved": True,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "gui_refinement_only": True,
    }


def _validate_schema(
    record_path: Path,
    payload: dict[str, Any],
    schema_path: Path,
    errors: list[str],
) -> None:
    if not schema_path.exists():
        errors.append(f"missing Stage 5DR schema: {schema_path.as_posix()}")
        return
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(payload):
        errors.append(f"{record_path.as_posix()}: schema error: {error.message}")


def _validate_common_payload(path: Path, payload: dict[str, Any], errors: list[str]) -> None:
    if payload.get("stage_id") != STAGE_ID:
        errors.append(f"{path.as_posix()}: stage_id must be {STAGE_ID}")
    if payload.get("stage_title") != STAGE_TITLE:
        errors.append(f"{path.as_posix()}: stage_title mismatch")
    if payload.get("prompt_type") != PROMPT_TYPE:
        errors.append(f"{path.as_posix()}: prompt_type mismatch")
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append(f"{path.as_posix()}: canonical handoff root must be codex-output")
    for flag in FORBIDDEN_FALSE_FLAGS:
        if payload.get(flag) is not False:
            errors.append(f"{path.as_posix()}: {flag} must be false")


def _format(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


__all__ = [
    "DATA_PATHS",
    "SCHEMA_PATHS",
    "build_stage5dr",
    "stage5dr_summary_text",
    "validate_stage5dr",
    "validate_stage5dr_detail_panel",
    "validate_stage5dr_image_thumbnail_actions",
    "validate_stage5dr_preservation",
    "validate_stage5dr_status_display",
    "validate_stage5dr_table_context_menu",
    "validate_stage5dr_url_file_actions",
]
