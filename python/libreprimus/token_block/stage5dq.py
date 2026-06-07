"""Stage 5DQ Operator Console source-browser GUI records.

This stage implements local GUI infrastructure. It creates an Operator Console
shell and Source Browser module for reviewing committed source-lock/evidence
metadata and manual annotations. It does not run route extraction, OCR, image
forensics, target validation, byte-stream generation, CUDA, scoring, or puzzle
execution.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.validators import (
    source_browser_summary,
    validate_manual_records,
    validate_source_index,
)
from libreprimus.token_block.models import read_yaml, write_yaml
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import ACTIVE_LINEAGE_PATHS
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP
from libreprimus.token_block.stage5dp import validate_stage5dp

STAGE_ID = "stage-5dq"
STAGE_TITLE = (
    "Stage 5DQ - Liber Primus Operator Console v0 Source-Browser GUI, "
    "without puzzle execution"
)
PROMPT_TYPE = "codex_gui_implementation"
SOURCE_PREVIOUS_STAGE_ID = "stage-5dp"
SOURCE_PREVIOUS_STAGE_COMMIT = "c336025048b28864d8f4273749f2700e9edc5968"
SOURCE_PREVIOUS_ISSUE = 151
SOURCE_PREVIOUS_CI_RUN = 27087036371
NEXT_STAGE_ID = "stage-5dr"
NEXT_STAGE_TITLE = "Stage 5DR - Source-browser GUI review and usability repair, without puzzle execution"
CODEX_COMPLETION_PATH = Path("codex-output/stage5dq-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

DATA_PATHS = {
    "summary": Path("data/project-state/stage5dq-summary.yaml"),
    "gui_implementation_summary": Path("data/project-state/stage5dq-gui-implementation-summary.yaml"),
    "scope_control": Path("data/project-state/stage5dq-operator-console-scope-control.yaml"),
    "reviewable_validation_evidence": Path("data/project-state/stage5dq-reviewable-validation-evidence.yaml"),
    "next_stage_decision": Path("data/project-state/stage5dq-next-stage-decision.yaml"),
}

SCHEMA_PATHS = {
    "summary": Path("schemas/project-state/stage5dq-summary-v0.schema.json"),
    "gui_implementation_summary": Path(
        "schemas/project-state/stage5dq-gui-implementation-summary-v0.schema.json"
    ),
    "scope_control": Path("schemas/project-state/stage5dq-operator-console-scope-control-v0.schema.json"),
    "reviewable_validation_evidence": Path(
        "schemas/project-state/stage5dq-reviewable-validation-evidence-v0.schema.json"
    ),
    "next_stage_decision": Path("schemas/project-state/stage5dq-next-stage-decision-v0.schema.json"),
}

FORBIDDEN_FALSE_FLAGS = {
    "activation_authorized_now",
    "activation_decision_valid_now",
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "alberti_cipher_execution_performed_now",
    "ai_ml_interpretation_performed",
    "audio_stego_performed",
    "benchmark_performed",
    "branch_enumeration_performed",
    "byte_stream_generation_authorized_now",
    "canonical_corpus_active",
    "combined_approval_gate_satisfied_now",
    "cuda_execution_performed",
    "decode_attempt_performed",
    "decryption_attempt_performed_now",
    "disk_cipher_execution_performed_now",
    "dwh_hash_search_performed",
    "execution_authorized_now",
    "execution_performed",
    "full_cartesian_product_enumerated",
    "generated_outputs_committed",
    "hash_preimage_search_performed",
    "html_tool_executed_now",
    "image_forensics_performed",
    "known_plaintext_attack_performed_now",
    "mayfly_route_extraction_performed_now",
    "mp3stego_execution_performed",
    "network_target_validation_performed_now",
    "ocr_performed",
    "openpuff_execution_performed",
    "operator_approval_management_implemented_now",
    "operator_readiness_decision_created_now",
    "page32_route_extraction_performed_now",
    "page56_hash_preimage_tested_now",
    "pivot_target_selected_now",
    "probability_claim_accepted_as_validated",
    "real_byte_stream_generated",
    "route_extraction_performed_now",
    "scoring_performed",
    "solve_claim",
    "spectrogram_stego_performed",
    "target_class_validation_implemented",
    "target_decision_management_implemented_now",
    "target_priority_decision_created_now",
    "token_block_experiment_executed",
    "tor_network_access_performed",
    "triangle_route_extraction_performed_now",
    "variant_materialisation_performed",
    "website_expansion_performed",
    "experiment_execution_ui_implemented_now",
    "source_browser_performs_analysis",
    "source_browser_executes_source_files",
    "source_browser_follows_urls_automatically",
    "source_browser_runs_ocr",
    "source_browser_runs_image_forensics",
    "source_browser_runs_ai_image_interpretation",
    "source_browser_modifies_raw_third_party_files",
    "source_browser_directly_rewrites_committed_stage_records",
}

REQUIRED_TRUE_FLAGS = {
    "source_browser_gui_implemented_now",
    "operator_console_shell_implemented_now",
    "source_browser_component_implemented_now",
}


@dataclass
class Stage5DQValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5dq"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5dq() -> dict[str, dict[str, Any]]:
    stage5dp_result = validate_stage5dp()
    if stage5dp_result.validation_error_count:
        raise RuntimeError("Stage 5DP validation must pass before Stage 5DQ")
    _stage5bd_counts, stage5bd_errors = validate_stage5bd()
    if stage5bd_errors:
        raise RuntimeError("Stage 5BD preservation validation must pass before Stage 5DQ")

    source_result = validate_source_index()
    manual_result = validate_manual_records()
    summary_payload = source_browser_summary()
    base = _base_payload()
    summary = {
        **base,
        "record_type": "stage5dq_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "source_previous_stage": SOURCE_PREVIOUS_STAGE_ID,
        "previous_stage_final_commit": SOURCE_PREVIOUS_STAGE_COMMIT,
        "previous_stage_issue": SOURCE_PREVIOUS_ISSUE,
        "previous_stage_ci_run": SOURCE_PREVIOUS_CI_RUN,
        "status": "complete",
        "operator_console_shell_implemented_now": True,
        "source_browser_component_implemented_now": True,
        "source_browser_gui_implemented_now": True,
        "operator_approval_management_implemented_now": False,
        "target_decision_management_implemented_now": False,
        "puzzle_execution_allowed": False,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "source_browser_entries_loaded": summary_payload["entries_loaded"],
        "source_browser_records_scanned": summary_payload["records_scanned"],
        "source_browser_missing_paths": summary_payload["missing_paths"],
        "manual_entry_count": summary_payload["manual_entries"],
        "manual_override_count": summary_payload["overrides"],
        "tombstone_count": summary_payload["tombstones"],
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
    }
    gui = {
        **base,
        "record_type": "stage5dq_gui_implementation_summary",
        "schema": SCHEMA_PATHS["gui_implementation_summary"].as_posix(),
        "operator_console_package_files": [
            "python/libreprimus/operator_console/app.py",
            "python/libreprimus/operator_console/main_window.py",
            "python/libreprimus/operator_console/cli.py",
            "python/libreprimus/operator_console/source_browser/loaders.py",
            "python/libreprimus/operator_console/source_browser/normalizer.py",
            "python/libreprimus/operator_console/source_browser/table_model.py",
            "python/libreprimus/operator_console/source_browser/dialogs.py",
            "python/libreprimus/operator_console/source_browser/image_viewer.py",
        ],
        "cli_commands_added": [
            "operator-console run",
            "operator-console build-source-index",
            "operator-console validate-source-index",
            "operator-console validate-manual-entries",
            "operator-console open-context",
            "operator-console summary",
            "source-browser run",
            "source-browser validate-index",
        ],
        "optional_gui_dependency": "PySide6>=6.7",
        "gui_dependency_failure_message": "GUI dependencies are not installed. Install with: pip install -e .[gui]",
        "chatgpt_context_file_supported": True,
        "image_thumbnail_support": True,
        "image_zoom_support": True,
        "explicit_file_url_opening_only": True,
        "source_browser_entries_loaded": summary_payload["entries_loaded"],
    }
    scope = {
        **base,
        "record_type": "stage5dq_operator_console_scope_control",
        "schema": SCHEMA_PATHS["scope_control"].as_posix(),
        "scope": "operator_console_source_browser_v0_only",
        "manual_entries_editable": True,
        "manual_overrides_editable": True,
        "tombstones_editable": True,
        "committed_source_lock_records_read_only": True,
        "future_modules_deferred": [
            "operator_approval_records",
            "target_priority_decisions",
            "run_plan_review",
            "evidence_atlas_review",
            "experiment_readiness_review",
            "source_lock_maintenance",
        ],
    }
    validation = {
        **base,
        "record_type": "stage5dq_reviewable_validation_evidence",
        "schema": SCHEMA_PATHS["reviewable_validation_evidence"].as_posix(),
        "focused_validators_required": [
            "operator-console validate-source-index",
            "operator-console validate-manual-entries",
            "operator-console summary",
            "token-block validate-stage5dq",
            "token-block stage5dq-summary",
        ],
        "source_index_validation_error_count": len(source_result.errors),
        "manual_entry_validation_error_count": len(manual_result.errors),
        "source_browser_records_scanned": summary_payload["records_scanned"],
        "source_browser_entries_loaded": summary_payload["entries_loaded"],
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
    }
    next_stage = {
        **base,
        "record_type": "stage5dq_next_stage_decision",
        "schema": SCHEMA_PATHS["next_stage_decision"].as_posix(),
        "selected_next_stage_id": NEXT_STAGE_ID,
        "selected_next_stage_title": NEXT_STAGE_TITLE,
        "selection_rationale": (
            "The first GUI pass should be reviewed for usability, table behavior, "
            "and manual-entry ergonomics before future operator modules are added."
        ),
    }
    records = {
        "summary": summary,
        "gui_implementation_summary": gui,
        "scope_control": scope,
        "reviewable_validation_evidence": validation,
        "next_stage_decision": next_stage,
    }
    for key, path in DATA_PATHS.items():
        write_yaml(path, records[key])
    return records


def validate_stage5dq() -> Stage5DQValidationResult:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for key, path in DATA_PATHS.items():
        if not path.exists():
            errors.append(f"missing Stage 5DQ record: {path.as_posix()}")
            continue
        payload = read_yaml(path)
        schema_path = SCHEMA_PATHS[key]
        if not schema_path.exists():
            errors.append(f"missing Stage 5DQ schema: {schema_path.as_posix()}")
        else:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            for error in Draft202012Validator(schema).iter_errors(payload):
                errors.append(f"{path.as_posix()}: schema error: {error.message}")
        _validate_common_payload(path, payload, errors)
    summary = read_yaml(DATA_PATHS["summary"]) if DATA_PATHS["summary"].exists() else {}
    counts.update(
        {
            "stage_id": summary.get("stage_id", ""),
            "status": summary.get("status", ""),
            "source_browser_gui_implemented_now": summary.get("source_browser_gui_implemented_now", False),
            "operator_console_shell_implemented_now": summary.get(
                "operator_console_shell_implemented_now", False
            ),
            "source_browser_component_implemented_now": summary.get(
                "source_browser_component_implemented_now", False
            ),
            "source_browser_entries_loaded": summary.get("source_browser_entries_loaded", 0),
            "source_browser_records_scanned": summary.get("source_browser_records_scanned", 0),
            "manual_entry_count": summary.get("manual_entry_count", 0),
            "manual_override_count": summary.get("manual_override_count", 0),
            "tombstone_count": summary.get("tombstone_count", 0),
            "pivot_target_selected_now": summary.get("pivot_target_selected_now", False),
            "execution_performed": summary.get("execution_performed", False),
            "recommended_next_stage_id": summary.get("recommended_next_stage_id", ""),
        }
    )
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output must not exist or be used")
    return Stage5DQValidationResult(len(errors), counts, errors)


def stage5dq_summary_text() -> str:
    summary = read_yaml(DATA_PATHS["summary"])
    keys = [
        "stage_id",
        "status",
        "operator_console_shell_implemented_now",
        "source_browser_component_implemented_now",
        "source_browser_gui_implemented_now",
        "source_browser_entries_loaded",
        "source_browser_records_scanned",
        "source_browser_missing_paths",
        "manual_entry_count",
        "manual_override_count",
        "tombstone_count",
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
        "solve_claim": False,
        "execution_allowed": False,
        "canonical_codex_handoff_root": "codex-output",
    }
    for flag in FORBIDDEN_FALSE_FLAGS:
        payload[flag] = False
    for flag in REQUIRED_TRUE_FLAGS:
        payload[flag] = True
    return payload


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
    for flag in REQUIRED_TRUE_FLAGS:
        if payload.get(flag) is not True:
            errors.append(f"{path.as_posix()}: {flag} must be true")


def _format(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
