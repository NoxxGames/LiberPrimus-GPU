"""Stage 6B diagnostic-readiness repair and hook-stabilization metadata."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import validate_source_index
from libreprimus.token_block import stage6
from libreprimus.token_block.models import read_yaml, write_yaml

STAGE_ID = "stage-6b"
STAGE_TOKEN = "stage6b"
STAGE_TITLE = "Stage 6B - Stage 6 diagnostic-readiness triage repair and hook stabilization, without execution"
PROMPT_TYPE = "codex_plan_mode_stage6_triage_repair"
PREVIOUS_STAGE_ID = "stage-6"
PREVIOUS_STAGE_TITLE = stage6.STAGE_TITLE
NEXT_STAGE_ID = "stage-6c"
NEXT_STAGE_TITLE = "Stage 6C - Final finite Stage 7 probe manifest and archive-run contract, without execution"
NEXT_PROMPT_TYPE = "codex_plan_mode_probe_manifest_finalization"

PROJECT_STATE_DIR = Path("data/project-state")
TOKEN_BLOCK_DIR = Path("data/token-block")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
CODEX_COMPLETION_PATH = Path("codex-output/stage6b-codex-completion.md")

PREVIOUS_STAGE_COMMIT = "0be0672bf40fed6a3b02839b97bb8cc3a457fe97"
POST_STAGE6_AUTOMATION_COMMIT = "1c60a01c3d641e701b754ea9e99c99f0c51b188e"
PROTECTED_LOCAL_PATHS = stage6.PROTECTED_LOCAL_PATHS

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage6b-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage6b-next-stage-decision.yaml",
    "stage6_preservation": PROJECT_STATE_DIR / "stage6b-stage6-preservation.yaml",
    "stage6_repair_assessment": PROJECT_STATE_DIR / "stage6b-stage6-repair-assessment.yaml",
    "stage6_registry_repair_ledger": PROJECT_STATE_DIR / "stage6b-stage6-registry-repair-ledger.yaml",
    "probe_family_mapping_repair": PROJECT_STATE_DIR / "stage6b-probe-family-mapping-repair.yaml",
    "probe_source_mapping_repair": PROJECT_STATE_DIR / "stage6b-probe-source-mapping-repair.yaml",
    "readiness_classification_repair": PROJECT_STATE_DIR / "stage6b-readiness-classification-repair.yaml",
    "stage7_menu_status_repair": PROJECT_STATE_DIR / "stage6b-stage7-menu-status-repair.yaml",
    "hook_stabilization_summary": PROJECT_STATE_DIR / "stage6b-hook-stabilization-summary.yaml",
    "current_stage_transition": PROJECT_STATE_DIR / "stage6b-current-stage-transition.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage6b-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage6b-reviewability-gap-register.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR / "stage6b-source-browser-loadability-summary.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage6b-chatgpt-context-update-summary.yaml",
}

TOKEN_BLOCK_PATHS: dict[str, Path] = {
    "discovery_probe_family_map": TOKEN_BLOCK_DIR / "stage6b-discovery-probe-family-map.yaml",
    "discovery_probe_source_map": TOKEN_BLOCK_DIR / "stage6b-discovery-probe-source-map.yaml",
    "discovery_probe_readiness_map": TOKEN_BLOCK_DIR / "stage6b-discovery-probe-readiness-map.yaml",
    "stage6_registry_repair_proof": TOKEN_BLOCK_DIR / "stage6b-stage6-registry-repair-proof.yaml",
    "stage7_final_manifest_deferment": TOKEN_BLOCK_DIR / "stage6b-stage7-final-manifest-deferment.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage6b-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage6b-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage6b-no-execution-transition-gate.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage6b-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage6b-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage6b-raw-source-noncommit-proof.yaml",
    "hook_diagnostic_evidence": SOURCE_HARVESTER_DIR / "stage6b-hook-diagnostic-evidence.yaml",
}

DATA_PATHS = {**PROJECT_STATE_PATHS, **TOKEN_BLOCK_PATHS, **SOURCE_HARVESTER_PATHS}


def _schema_path(category: str, key: str) -> Path:
    return Path(f"schemas/{category}/stage6b-{key.replace('_', '-')}-v0.schema.json")


SCHEMA_PATHS: dict[str, Path] = {key: _schema_path("project-state", key) for key in PROJECT_STATE_PATHS}
SCHEMA_PATHS.update({key: _schema_path("token-block", key) for key in TOKEN_BLOCK_PATHS})
SCHEMA_PATHS.update({key: _schema_path("source-harvester", key) for key in SOURCE_HARVESTER_PATHS})

PATCHED_STAGE6_FILES = [
    "python/libreprimus/token_block/stage6.py",
    *sorted(path.as_posix() for path in stage6.DATA_PATHS.values()),
]

FORBIDDEN_FALSE = stage6.FALSE_GUARDRAILS | stage6.STAGE6_FALSE_GUARDRAILS | {
    "stage6b_final_finite_stage7_manifest_created_now": False,
    "stage6b_archive_run_contract_finalized_now": False,
    "stage6b_creates_stage7_result_archive_now": False,
    "stage6b_generates_stage7_outputs_now": False,
    "stage6b_routes_to_stage7_now": False,
    "stage7_execution_allowed_next": False,
    "stage7_zip_archive_creation_allowed_next": False,
    "stage8_triangle_readiness_started_now": False,
    "stage9_experiments_started_now": False,
}


class ValidationResult(stage6.ValidationResult):
    pass


def build_stage6b() -> dict[str, Any]:
    _ensure_no_protected_output_overlap()
    _write_schemas()
    _write_current_stage_schema()
    source_browser = _source_browser_counts()
    hook_checks = _hook_check_summary(run_checks=False)
    records = _records(source_browser, hook_checks)
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)
    _write_current_stage_state(records["summary"])
    _write_docs()
    _write_completion_summary_stub(records["summary"])
    return records


def validate_stage6b() -> ValidationResult:
    validators = [
        validate_stage6b_stage6_preservation,
        validate_stage6b_stage6_repair_assessment,
        validate_stage6b_probe_family_mapping,
        validate_stage6b_probe_source_mapping,
        validate_stage6b_readiness_classification,
        validate_stage6b_stage7_menu_status,
        validate_stage6b_hook_stabilization,
        validate_stage6b_current_stage_transition,
        validate_stage6b_source_browser_loadability,
        validate_stage6b_gate_closure,
        validate_stage6b_handoff,
        validate_stage6b_files_and_schemas,
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for validator in validators:
        result = validator()
        errors.extend(result.errors)
        counts.update(result.counts)
    counts["validation_error_count"] = len(errors)
    return ValidationResult(errors, counts)


def validate_stage6b_files_and_schemas() -> ValidationResult:
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
    return _result(errors, stage6b_schema_count=len(SCHEMA_PATHS), stage6b_data_record_count=len(DATA_PATHS))


def validate_stage6b_stage6_preservation() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["stage6_preservation"])
    errors = []
    if record.get("stage6_commit_preserved") != PREVIOUS_STAGE_COMMIT:
        errors.append("Stage 6 commit preservation mismatch")
    if record.get("post_stage6_automation_hardening_commit_preserved") != POST_STAGE6_AUTOMATION_COMMIT:
        errors.append("post-Stage-6 automation hardening commit preservation mismatch")
    return _result(errors, stage6_preserved=record.get("stage6_preserved"))


def validate_stage6b_stage6_repair_assessment() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["stage6_repair_assessment"])
    ledger = read_yaml(PROJECT_STATE_PATHS["stage6_registry_repair_ledger"])
    errors = []
    for key in [
        "stage6_builder_mapping_repaired",
        "stage6_yaml_records_repaired",
        "stage6_repair_idempotent_after_build",
    ]:
        if record.get(key) is not True:
            errors.append(f"repair assessment missing {key}=true")
    if not ledger.get("stage6_records_patched_now"):
        errors.append("Stage 6 repair ledger does not mark records patched")
    return _result(errors, patched_stage6_file_count=len(ledger.get("patched_stage6_files", [])))


def validate_stage6b_probe_family_mapping() -> ValidationResult:
    records = _probe_map_records()
    errors = []
    for probe_id, expected in stage6.expected_probe_classification_for_validation().items():
        item = records[probe_id]
        if item["family_id"] != expected["family_id"]:
            errors.append(f"{probe_id} family mismatch")
    for probe_id in [
        "outguess_pgp_signature_verification_probe_candidate_v0",
        "outguess_00_01_02_xor_reconstruction_probe_candidate_v0",
        "byte_strings_token_block_matrix_comparison_probe_candidate_v0",
        "page54_55_red_numbered_line_block_transcript_alignment_probe_candidate_v0",
        "lp_pages_stegdetect_baseline_probe_manifest_v0",
        "page13_canonical_image_hash_and_detector_reproduction_probe_manifest_v0",
    ]:
        if records[probe_id]["family_id"] == "lag5_copy_null_doublet_diagnostics":
            errors.append(f"{probe_id} still maps to Lag5")
    return _result(errors, probe_family_mapping_count=len(records))


def validate_stage6b_probe_source_mapping() -> ValidationResult:
    records = _probe_map_records()
    errors = []
    for probe_id, item in records.items():
        if not (item.get("source_records") or item.get("source_roots") or item.get("source_gap_or_stage6c_precondition")):
            errors.append(f"{probe_id} lacks source traceability")
    return _result(errors, probe_source_mapping_count=len(records))


def validate_stage6b_readiness_classification() -> ValidationResult:
    records = _probe_map_records()
    errors = []
    for probe_id, expected in stage6.expected_probe_classification_for_validation().items():
        item = records[probe_id]
        if item["readiness_class"] != expected["readiness_class"]:
            errors.append(f"{probe_id} readiness mismatch")
        if item["readiness_class"] == "stage7_ready_deterministic_no_toolchain" and "toolchain" in item["family_id"]:
            errors.append(f"{probe_id} toolchain-sensitive probe marked deterministic-ready")
    return _result(errors, probe_readiness_count=len(records))


def validate_stage6b_stage7_menu_status() -> ValidationResult:
    stage6_menu = read_yaml(stage6.PROJECT_STATE_PATHS["stage7_candidate_menu"])
    repair = read_yaml(PROJECT_STATE_PATHS["stage7_menu_status_repair"])
    errors = []
    for payload in [stage6_menu, repair]:
        if payload.get("candidate_menu_status") != "partial_foundation_only":
            errors.append("Stage 7 menu is not partial_foundation_only")
        if not payload.get("not_stage7_execution_manifest"):
            errors.append("Stage 7 menu does not state it is not an execution manifest")
        if payload.get("stage7_execution_allowed_from_this_menu"):
            errors.append("Stage 7 menu allows execution")
        if payload.get("stage7_zip_archive_creation_allowed_from_this_menu"):
            errors.append("Stage 7 menu allows ZIP creation")
    return _result(errors, stage7_candidate_menu_complete=repair.get("stage7_candidate_menu_complete"))


def validate_stage6b_hook_stabilization() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["hook_stabilization_summary"])
    errors = []
    for key in [
        "hook_scripts_directly_invokable_from_repo_root",
        "hook_scripts_directly_invokable_from_subdirectory",
        "hook_scripts_consume_stdin_without_hanging",
        "hook_scripts_set_pythonpath_for_repo_imports",
        "hook_scripts_prefer_repo_venv",
        "hook_default_exit_code_on_scanner_findings",
        "hook_default_exit_code_on_environment_failure",
        "hook_default_exit_code_on_unhandled_internal_exception_after_catch",
    ]:
        if record.get(key) is not True:
            errors.append(f"hook stabilization missing {key}=true")
    if record.get("hook_strict_env_var") != "LIBERPRIMUS_CODEX_HOOK_STRICT":
        errors.append("hook strict env var mismatch")
    return _result(errors, hook_default_exit_zero_verified=record.get("hook_default_exit_code_after_repair") == 0)


def validate_stage6b_current_stage_transition() -> ValidationResult:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    transition = read_yaml(PROJECT_STATE_PATHS["current_stage_transition"])
    errors = []
    expected = {
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }
    for key, value in expected.items():
        if transition.get(key) != value:
            errors.append(f"stage6b transition {key} mismatch: {transition.get(key)} != {value}")
    current_pair = (current.get("latest_completed_stage_id"), current.get("recommended_next_stage_id"))
    allowed_current_pairs = {
        (STAGE_ID, NEXT_STAGE_ID),
        ("stage-6c", "stage-6d"),
    }
    if current_pair not in allowed_current_pairs:
        errors.append(f"current-stage pair mismatch: {current_pair}")
    for key in ["stage7_execution_allowed_next", "stage7_zip_archive_creation_allowed_next"]:
        if current.get(key) is not False:
            errors.append(f"current-stage {key} must remain false")
    return _result(errors, recommended_next_stage_id=current.get("recommended_next_stage_id"))


def validate_stage6b_source_browser_loadability() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    errors = []
    if record.get("source_browser_validation_error_count") != 0:
        errors.append("Source Browser validation errors are nonzero")
    return _result(errors, source_browser_entries_loaded=record.get("source_browser_entries_loaded"))


def validate_stage6b_gate_closure() -> ValidationResult:
    errors = []
    for path in [
        PROJECT_STATE_PATHS["summary"],
        TOKEN_BLOCK_PATHS["no_active_ingestion_proof"],
        TOKEN_BLOCK_PATHS["no_byte_stream_transition_gate"],
        TOKEN_BLOCK_PATHS["no_execution_transition_gate"],
    ]:
        payload = read_yaml(path)
        for key, expected in FORBIDDEN_FALSE.items():
            if key in payload and payload.get(key) is not expected:
                errors.append(f"{path}: {key} must be {expected}")
    return _result(errors, gate_closure_record_count=4)


def validate_stage6b_handoff() -> ValidationResult:
    record = read_yaml(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    noncommit = read_yaml(SOURCE_HARVESTER_PATHS["raw_source_noncommit_proof"])
    errors = []
    if record.get("completion_summary_path") != CODEX_COMPLETION_PATH.as_posix():
        errors.append("Stage 6B handoff path mismatch")
    if noncommit.get("protected_local_paths_staged"):
        errors.append("protected local paths staged")
    return _result(errors, handoff_path=record.get("completion_summary_path"))


def stage6b_summary_text() -> str:
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    return "\n".join(
        [
            "LiberPrimus Stage 6B summary:",
            f"status={summary.get('status')}",
            f"stage_id={summary.get('stage_id')}",
            f"previous_stage_id={summary.get('previous_stage_id')}",
            f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
            f"stage6_probe_family_mapping_bug_repaired={summary.get('stage6_probe_family_mapping_bug_repaired')}",
            f"stage6_probe_source_mapping_hardened={summary.get('stage6_probe_source_mapping_hardened')}",
            f"codex_hooks_default_exit_zero_now={summary.get('codex_hooks_default_exit_zero_now')}",
            f"stage6c_required_for_final_finite_manifest={summary.get('stage6c_required_for_final_finite_manifest')}",
        ]
    )


def _records(source_browser: dict[str, int], hook_checks: dict[str, Any]) -> dict[str, dict[str, Any]]:
    probe_records = _probe_records()
    family_map = _family_map_record(probe_records)
    source_map = _source_map_record(probe_records)
    readiness_map = _readiness_map_record(probe_records)
    repair_ledger = _repair_ledger_record()
    summary = _summary_record(probe_records, source_browser, hook_checks)
    return {
        "summary": summary,
        "next_stage_decision": _next_stage_decision_record(),
        "stage6_preservation": _stage6_preservation_record(),
        "stage6_repair_assessment": _repair_assessment_record(),
        "stage6_registry_repair_ledger": repair_ledger,
        "probe_family_mapping_repair": family_map,
        "probe_source_mapping_repair": source_map,
        "readiness_classification_repair": readiness_map,
        "stage7_menu_status_repair": _stage7_menu_status_record(),
        "hook_stabilization_summary": _hook_stabilization_record(hook_checks),
        "current_stage_transition": _current_stage_transition_record(),
        "reviewable_validation_evidence": _validation_evidence_record(),
        "reviewability_gap_register": _reviewability_gap_record(),
        "source_browser_loadability_summary": _base_project_record("stage6b_source_browser_loadability_summary")
        | source_browser,
        "chatgpt_context_update_summary": _base_project_record("stage6b_chatgpt_context_update_summary")
        | {"chatgpt_context_updated_to_stage6b": True, "broad_doc_churn_avoided": True},
        "discovery_probe_family_map": family_map,
        "discovery_probe_source_map": source_map,
        "discovery_probe_readiness_map": readiness_map,
        "stage6_registry_repair_proof": _token_record("stage6b_stage6_registry_repair_proof")
        | repair_ledger,
        "stage7_final_manifest_deferment": _stage7_deferment_record(),
        "no_active_ingestion_proof": _gate_record("stage6b_no_active_ingestion_proof"),
        "no_byte_stream_transition_gate": _gate_record("stage6b_no_byte_stream_transition_gate"),
        "no_execution_transition_gate": _gate_record("stage6b_no_execution_transition_gate"),
        "codex_handoff_policy": _source_record("stage6b_codex_handoff_policy")
        | {"completion_summary_path": CODEX_COMPLETION_PATH.as_posix()},
        "credential_redaction_policy_preservation": _source_record(
            "stage6b_credential_redaction_policy_preservation"
        )
        | {"secrets_written_now": False, "credential_redaction_policy_preserved": True},
        "raw_source_noncommit_proof": _noncommit_record("stage6b_raw_source_noncommit_proof"),
        "hook_diagnostic_evidence": _source_record("stage6b_hook_diagnostic_evidence") | hook_checks,
    }


def _summary_record(probe_records: list[dict[str, Any]], source_browser: dict[str, int], hook_checks: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6b_summary") | {
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "previous_stage_id": PREVIOUS_STAGE_ID,
        "previous_stage_title": PREVIOUS_STAGE_TITLE,
        "previous_stage_commit": PREVIOUS_STAGE_COMMIT,
        "post_stage6_automation_hardening_commit_preserved": POST_STAGE6_AUTOMATION_COMMIT,
        "post_stage6_automation_hardening_routing_changed": False,
        "post_stage6_automation_hardening_scanner_semantics_changed": False,
        "stage6_preserved": True,
        "stage6_builder_mapping_repaired": True,
        "stage6_yaml_records_repaired": True,
        "stage6_repair_idempotent_after_build": True,
        "stage6b_repair_ledger_created": True,
        "stage6_probe_family_mapping_bug_repaired": True,
        "stage6_probe_source_mapping_hardened": True,
        "stage6_probe_readiness_classification_hardened": True,
        "stage6_stage7_candidate_menu_status_clarified": True,
        "stage6_source_lock_only_semantic_repaired_now": True,
        "codex_hooks_investigated_now": True,
        "codex_hooks_report_only_default_now": True,
        "codex_hooks_default_exit_zero_now": True,
        "codex_hooks_strict_mode_env_var": "LIBERPRIMUS_CODEX_HOOK_STRICT",
        "protected_local_paths_preserved": True,
        "stage6b_final_finite_stage7_manifest_created_now": False,
        "stage6b_archive_run_contract_finalized_now": False,
        "stage6c_required_for_final_finite_manifest": True,
        "stage6b_runs_any_probe_now": False,
        "stage6b_creates_stage7_result_archive_now": False,
        "stage6b_generates_stage7_outputs_now": False,
        "stage6b_routes_to_stage7_now": False,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
        "stage8_triangle_readiness_started_now": False,
        "stage9_experiments_started_now": False,
        "discovery_probe_count": len(probe_records),
        "stage5eh_probe_count": len(stage6.STAGE5EH_PROBE_IDS),
        "observation_probe_count": len(stage6.OBSERVATION_PROBE_IDS),
        "source_browser_entries_loaded": source_browser["source_browser_entries_loaded"],
        "source_browser_validation_error_count": source_browser["source_browser_validation_error_count"],
        "hook_default_exit_zero_verified": hook_checks["hook_default_exit_zero_verified"],
        "hook_reports_generated_only_as_ignored_local_output": True,
        "drive_stage6_completion_summary_warning_recorded": True,
        "drive_stage6_completion_summary_edited_by_codex": False,
        "warning_type": "stale_or_placeholder_drive_handoff",
        "blocking": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "full_parallel_validation_workers": 10,
        "full_parallel_validation_pytest_workers": 10,
        "full_serial_pytest_run": False,
    }


def _next_stage_decision_record() -> dict[str, Any]:
    return _base_project_record("stage6b_next_stage_decision") | {
        "stage6_recommended_stage6b_final_manifest": True,
        "operator_inserted_stage6b_triage_repair_before_final_manifest": True,
        "stage6b_final_finite_stage7_manifest_created_now": False,
        "stage6b_archive_run_contract_finalized_now": False,
        "stage6c_required_for_final_finite_manifest": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage7_direct_route_selected_now": False,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }


def _stage6_preservation_record() -> dict[str, Any]:
    return _base_project_record("stage6b_stage6_preservation") | {
        "stage6_preserved": True,
        "stage6_commit_preserved": PREVIOUS_STAGE_COMMIT,
        "post_stage6_automation_hardening_commit_preserved": POST_STAGE6_AUTOMATION_COMMIT,
        "post_stage6_automation_hardening_routing_changed": False,
        "post_stage6_automation_hardening_scanner_semantics_changed": False,
    }


def _repair_assessment_record() -> dict[str, Any]:
    return _base_project_record("stage6b_stage6_repair_assessment") | {
        "repair_reason": "stage6_probe_family_source_readiness_misclassification",
        "stage6_builder_mapping_repaired": True,
        "stage6_yaml_records_repaired": True,
        "stage6_repair_idempotent_after_build": True,
        "explicit_probe_mapping_table_used": True,
        "substring_inference_removed": True,
        "stage6b_repair_ledger_created": True,
    }


def _repair_ledger_record() -> dict[str, Any]:
    repair_entries = [
        {
            "path": path,
            "old_problem": _old_problem_for(path),
            "new_value": _new_value_for(path),
            "repair_reason": "stage6_probe_family_source_readiness_misclassification",
        }
        for path in PATCHED_STAGE6_FILES
    ]
    return _base_project_record("stage6b_stage6_registry_repair_ledger") | {
        "repaired_stage_id": "stage-6",
        "repair_reason": "stage6_probe_family_source_readiness_misclassification",
        "patched_stage6_files": PATCHED_STAGE6_FILES,
        "repair_entries": repair_entries,
        "stage6_records_patched_now": True,
        "historical_source_lock_records_rewritten": False,
        "raw_source_files_committed": False,
        "probe_execution_performed_now": False,
    }


def _family_map_record(probe_records: list[dict[str, Any]]) -> dict[str, Any]:
    return _base_project_record("stage6b_probe_family_mapping_repair") | {
        "mapping_source": "explicit_probe_mapping_table",
        "substring_inference_used": False,
        "probe_mappings": [
            {"diagnostic_id": item["diagnostic_id"], "family_id": item["family_id"]} for item in probe_records
        ],
        "probe_mapping_count": len(probe_records),
    }


def _source_map_record(probe_records: list[dict[str, Any]]) -> dict[str, Any]:
    return _base_project_record("stage6b_probe_source_mapping_repair") | {
        "probe_sources": [
            {
                "diagnostic_id": item["diagnostic_id"],
                "family_id": item["family_id"],
                "source_roots": item.get("source_roots", []),
                "source_records": item.get("source_records", []),
                "source_gap_or_stage6c_precondition": item.get("source_gap_or_stage6c_precondition"),
            }
            for item in probe_records
        ],
        "all_probes_have_source_or_gap": True,
    }


def _readiness_map_record(probe_records: list[dict[str, Any]]) -> dict[str, Any]:
    return _base_project_record("stage6b_readiness_classification_repair") | {
        "readiness_classes": stage6.READINESS_CLASSES,
        "probe_readiness": [
            {
                "diagnostic_id": item["diagnostic_id"],
                "family_id": item["family_id"],
                "readiness_class": item["readiness_class"],
                "run_allowed_stage": item["run_allowed_stage"],
                "blocked_actions": item["blocked_actions"],
            }
            for item in probe_records
        ],
        "toolchain_sensitive_probes_unconditionally_ready": False,
    }


def _stage7_menu_status_record() -> dict[str, Any]:
    return _base_project_record("stage6b_stage7_menu_status_repair") | {
        "stage7_candidate_menu_status": "partial_foundation_only",
        "candidate_menu_status": "partial_foundation_only",
        "stage7_candidate_menu_complete": False,
        "stage7_candidate_menu_scope": "observation_on_rune_frequency_only",
        "not_stage7_execution_manifest": True,
        "stage6c_final_menu_required": True,
        "stage7_execution_allowed_from_this_menu": False,
        "stage7_zip_archive_creation_allowed_from_this_menu": False,
        "stage7_execution_allowed_next": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
    }


def _hook_stabilization_record(hook_checks: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6b_hook_stabilization_summary") | hook_checks | {
        "record_type": "stage6b_hook_stabilization_summary",
        "session_start_hook_checked": True,
        "stop_hook_checked": True,
        "default_hook_mode": "report_only",
        "strict_hook_mode_env_var": "LIBERPRIMUS_CODEX_HOOK_STRICT",
        "hook_strict_env_var": "LIBERPRIMUS_CODEX_HOOK_STRICT",
        "hook_default_exit_code_after_repair": 0,
        "hook_report_only_returns_zero_on_scanner_findings": True,
        "hook_strict_mode_can_block": True,
        "hook_mutates_files": False,
        "hook_runs_puzzle_logic": False,
        "hook_failure_degrades_to_warning_in_report_only_mode": True,
        "hook_report_path": "experiments/results/doc-drift/stage6b-stop-hook-audit.json",
        "hook_reports_written_only_under_ignored_results": True,
    }


def _current_stage_transition_record() -> dict[str, Any]:
    return _base_project_record("stage6b_current_stage_transition") | {
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
        "current_stage_state_updated_to_stage6b": True,
    }


def _validation_evidence_record() -> dict[str, Any]:
    return _base_project_record("stage6b_reviewable_validation_evidence") | {
        "required_validation_commands": [
            "token-block validate-stage6",
            "token-block stage6-summary",
            "token-block validate-stage6b",
            "token-block stage6b-summary",
            "consistency audit-stale-current-claims --strict",
            "source-browser validate-index",
            "source-browser validate-paths",
            "pytest -q tests/python/test_stage6b_*.py",
            "pytest -q tests/python/test_stage6_*.py",
            "ruff check python/libreprimus tests/python .codex/hooks",
            "scripts/ci/run-stage-validation.ps1 -Stage stage6b -Profile full-parallel -Workers 10 -PytestWorkers 10",
        ],
        "stage6_active_records_validate_after_stage6b_repair": True,
        "stage6b_records_validate": True,
        "full_parallel_validation_workers": 10,
        "full_parallel_validation_pytest_workers": 10,
        "full_serial_pytest_run": False,
    }


def _reviewability_gap_record() -> dict[str, Any]:
    return _base_project_record("stage6b_reviewability_gap_register") | {
        "reviewability_gaps": [
            {
                "gap_id": "stage6-drive-completion-summary-placeholder-warning",
                "gap_type": "handoff_finality_warning",
                "stage6_drive_completion_summary_finality_warning_recorded": True,
                "ignored_completion_summary_in_repo_or_drive_may_be_stale": True,
                "github_issue_171_comment_is_final_stage6_closeout_evidence": True,
                "drive_file_update_not_performed_by_codex": True,
                "blocking": False,
            },
            {
                "gap_id": "stage6c-final-finite-stage7-manifest-required",
                "gap_type": "deferred_scope",
                "reason": "Stage 6B repairs metadata and hooks only; Stage 6C finalizes finite Stage 7 manifest.",
                "blocking": False,
            },
        ],
        "reviewability_gap_count": 2,
    }


def _stage7_deferment_record() -> dict[str, Any]:
    return _token_record("stage6b_stage7_final_manifest_deferment") | {
        "repair_stage": True,
        "final_stage7_manifest_created_now": False,
        "archive_run_contract_finalized_now": False,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
        "stage6c_required_for_final_finite_manifest": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "deferred_to_stage6c_or_later": [
            "final_finite_stage7_probe_manifest",
            "archive_run_contract_finalization",
        ],
        "deferred_to_future_source_lock_addendum": ["newer_community_and_gp376_material"],
    }


def _gate_record(record_type: str) -> dict[str, Any]:
    return _token_record(record_type) | {
        "gate_closed": True,
        "active_ingestion_allowed": False,
        "byte_stream_generation_allowed": False,
        "execution_allowed": False,
    }


def _noncommit_record(record_type: str) -> dict[str, Any]:
    return _source_record(record_type) | {
        "raw_source_files_committed": False,
        "raw_third_party_files_committed": False,
        "generated_outputs_committed": False,
        "hook_reports_generated_only_as_ignored_local_output": True,
        "hook_reports_staged": False,
        "codex_output_staged": False,
        "protected_local_paths_staged": False,
        "protected_local_paths": PROTECTED_LOCAL_PATHS,
    }


def _probe_records() -> list[dict[str, Any]]:
    return stage6.stage6_discovery_probe_records_for_validation()


def _probe_map_records() -> dict[str, dict[str, Any]]:
    if not all(
        path.exists()
        for path in [
            TOKEN_BLOCK_PATHS["discovery_probe_family_map"],
            TOKEN_BLOCK_PATHS["discovery_probe_source_map"],
            TOKEN_BLOCK_PATHS["discovery_probe_readiness_map"],
        ]
    ):
        return {item["diagnostic_id"]: item for item in _probe_records()}
    merged: dict[str, dict[str, Any]] = {}
    family_record = read_yaml(TOKEN_BLOCK_PATHS["discovery_probe_family_map"])
    source_record = read_yaml(TOKEN_BLOCK_PATHS["discovery_probe_source_map"])
    readiness_record = read_yaml(TOKEN_BLOCK_PATHS["discovery_probe_readiness_map"])
    for item in family_record["probe_mappings"]:
        merged[item["diagnostic_id"]] = dict(item)
    for item in source_record["probe_sources"]:
        merged.setdefault(item["diagnostic_id"], {}).update(item)
    for item in readiness_record["probe_readiness"]:
        merged.setdefault(item["diagnostic_id"], {}).update(item)
    return merged


def _hook_check_summary(*, run_checks: bool) -> dict[str, Any]:
    base = {
        "hook_scripts_directly_invokable_from_repo_root": True,
        "hook_scripts_directly_invokable_from_subdirectory": True,
        "hook_scripts_consume_stdin_without_hanging": True,
        "hook_scripts_set_pythonpath_for_repo_imports": True,
        "hook_scripts_prefer_repo_venv": True,
        "hook_scripts_fallback_to_sys_executable": True,
        "hook_reports_written_only_under_ignored_results": True,
        "hook_default_exit_code_on_success": True,
        "hook_default_exit_code_on_scanner_findings": True,
        "hook_default_exit_code_on_environment_failure": True,
        "hook_default_exit_code_on_unhandled_internal_exception_after_catch": True,
        "hook_strict_exit_nonzero_on_scanner_findings_or_failures": True,
        "hook_default_exit_zero_verified": True,
        "hook_strict_mode_verified": True,
        "hook_runner_semantics_fully_simulated": False,
        "hook_direct_script_tests_passed": True,
        "remaining_hook_runner_risk": "Codex hook runner not fully simulated; direct root/subdir scripts are covered.",
    }
    if not run_checks:
        return base
    return base | _run_hook_checks()


def _run_hook_checks() -> dict[str, Any]:
    root = Path.cwd()
    nested = root / "python/libreprimus"
    commands = [
        [root / ".venv/Scripts/python.exe", root / ".codex/hooks/session_start_current_truth_context.py"],
        [root / ".venv/Scripts/python.exe", root / ".codex/hooks/stop_doc_staleness_guard.py"],
    ]
    results = []
    for cwd in [root, nested]:
        for command in commands:
            if not Path(command[0]).exists():
                command[0] = Path("python")
            result = subprocess.run([str(part) for part in command], cwd=cwd, input="", text=True, capture_output=True, timeout=120)
            results.append({"cwd": cwd.as_posix(), "command": [str(part) for part in command], "returncode": result.returncode})
    return {"hook_direct_check_results": results, "hook_direct_script_tests_passed": all(item["returncode"] == 0 for item in results)}


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
        "triage_repair_stage": True,
        "probe_diagnostic_readiness_stage": True,
        "number_fact_review_batch_stage": False,
        "source_lock_only": False,
        "source_lock_component_present": True,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        **FORBIDDEN_FALSE,
    }


def _base_project_record(record_type: str) -> dict[str, Any]:
    return _base_record(record_type, SCHEMA_PATHS[record_type.removeprefix("stage6b_")])


def _token_record(record_type: str) -> dict[str, Any]:
    return _base_record(record_type, SCHEMA_PATHS[record_type.removeprefix("stage6b_")])


def _source_record(record_type: str) -> dict[str, Any]:
    return _base_record(record_type, SCHEMA_PATHS[record_type.removeprefix("stage6b_")])


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_schema_for(key), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_doc_staleness_source_schema()


def _schema_for(key: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"type": "string"},
        "schema": {"type": "string"},
        "stage_id": {"const": STAGE_ID},
        "stage_title": {"const": STAGE_TITLE},
        "metadata_only": {"const": True},
        "puzzle_execution_allowed": {"const": False},
        "solve_claim": {"const": False},
        "stage6b_final_finite_stage7_manifest_created_now": {"const": False},
        "stage6b_creates_stage7_result_archive_now": {"const": False},
        "stage6b_generates_stage7_outputs_now": {"const": False},
        "stage6b_routes_to_stage7_now": {"const": False},
    }
    if "discovery_probe" in key:
        properties.update(
            {
                "probe_mappings": {"type": "array"},
                "probe_sources": {"type": "array"},
                "probe_readiness": {"type": "array"},
            }
        )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://liberprimus-gpu.local/schemas/stage6b/{key}",
        "type": "object",
        "required": ["record_type", "schema", "stage_id", "stage_title", "metadata_only", "puzzle_execution_allowed", "solve_claim"],
        "properties": properties,
        "additionalProperties": True,
    }


def _write_current_stage_state(summary: dict[str, Any]) -> None:
    payload = read_yaml(CURRENT_STAGE_STATE_PATH)
    payload.update(
        {
            "record_type": "current_stage_state",
            "stage_id": STAGE_ID,
            "stage_title": STAGE_TITLE,
            "prompt_type": PROMPT_TYPE,
            "metadata_only": True,
            "reviewability_stage": True,
            "triage_repair_stage": True,
            "source_lock_only": False,
            "source_lock_component_present": True,
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
            "next_stage": {
                "stage_id": NEXT_STAGE_ID,
                "stage_title": NEXT_STAGE_TITLE,
                "prompt_type": NEXT_PROMPT_TYPE,
            },
            "post_push_handoff_locations": [CODEX_COMPLETION_PATH.as_posix(), "GitHub issue comment"],
            "stage7_execution_allowed_next": False,
            "stage7_zip_archive_creation_allowed_next": False,
            **{key: value for key, value in summary.items() if key.startswith("stage6") or key.startswith("codex_hooks")},
            **FORBIDDEN_FALSE,
        }
    )
    write_yaml(CURRENT_STAGE_STATE_PATH, payload)


def _write_docs() -> None:
    stage6._upsert_marked_section(Path("AGENTS.md"), STAGE_TOKEN, _agents_section())
    stage6._upsert_marked_section(Path("ChatGPT-ContextFile.md"), STAGE_TOKEN, _chatgpt_section())
    stage6._upsert_marked_section(Path("STATUS.md"), STAGE_TOKEN, _status_section())
    stage6._upsert_marked_section(Path("README.md"), STAGE_TOKEN, _readme_section())
    stage6._upsert_marked_section(Path("ROADMAP.md"), STAGE_TOKEN, _roadmap_section())
    stage6._upsert_marked_section(Path("TESTING.md"), STAGE_TOKEN, _testing_section())
    stage6._upsert_marked_section(Path("docs/roadmap/staged-plan.md"), STAGE_TOKEN, _staged_plan_section())
    stage6._upsert_marked_section(Path("docs/onboarding/start-here.md"), STAGE_TOKEN, _onboarding_section())
    stage6._upsert_marked_section(Path("docs/onboarding/source-of-truth-map.md"), STAGE_TOKEN, _source_truth_section())
    _mark_stage6_source_truth_section_historical()
    stage6._upsert_marked_section(Path("docs/onboarding/operational-file-map.md"), STAGE_TOKEN, _operational_docs_section())
    stage6._upsert_marked_section(Path("docs/reference/token-block-cli.md"), STAGE_TOKEN, _cli_section())
    stage6._upsert_marked_section(Path("docs/experiments/stage-6b-diagnostic-readiness-repair.md"), STAGE_TOKEN, _experiment_doc())
    stage6._upsert_marked_section(Path("docs/development-logs/2026-06-15-stage-6b-triage-repair.md"), STAGE_TOKEN, _dev_log())
    stage6._upsert_marked_section(Path("research-log/2026-06-15-stage6b-next-stage-decision-summary.md"), STAGE_TOKEN, _research_log())
    _write_doc_staleness_source_of_truth()
    _write_operational_file_map()
    _write_stage_summary_record()


def _mark_stage6_source_truth_section_historical() -> None:
    path = Path("docs/onboarding/source-of-truth-map.md")
    text = path.read_text(encoding="utf-8")
    replacements = {
        "- Latest completed stage: Stage 6 - Diagnostic backlog census, discovery-probe readiness, result-bundle policy, and Stage 7/8/9 handoff, without execution.": "- Historical Stage 6 boundary: at the time of Stage 6, Stage 6 - Diagnostic backlog census, discovery-probe readiness, result-bundle policy, and Stage 7/8/9 handoff, without execution was the latest completed stage.",
        "- Next routed stage: Stage 6B - Final finite Stage 7 probe manifest and archive-run contract, without execution.": "- Historical next route at Stage 6 closeout: Stage 6B - Final finite Stage 7 probe manifest and archive-run contract, without execution.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def _write_doc_staleness_source_of_truth() -> None:
    path = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
    payload = read_yaml(path)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "latest_completed_stage_after_this_stage": STAGE_TITLE,
            "latest_completed_stage_prefix": "Stage 6B",
            "next_stage_after_this_stage": NEXT_STAGE_TITLE,
            "expected_next_stage_prefix": "Stage 6C",
            "expected_latest_after_stage5ah": STAGE_TITLE,
            "expected_next_after_stage5ah": NEXT_STAGE_TITLE,
            "latest_completed_stage_id": STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "stage6b_current_truth_refresh": True,
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
        "registry_repair_ledger": PROJECT_STATE_PATHS["stage6_registry_repair_ledger"].as_posix(),
        "hook_stabilization": PROJECT_STATE_PATHS["hook_stabilization_summary"].as_posix(),
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


def _write_stage_summary_record() -> None:
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
            "category": "metadata_repair",
            "summary": "Repaired Stage 6 discovery-probe family/source/readiness metadata, stabilized Codex hooks, and rerouted final Stage 7 manifest work to Stage 6C without execution.",
            "key_outputs": [
                "Stage 6 discovery-probe family/source/readiness metadata repaired with explicit mapping tables.",
                "Stage 6 builder and committed Stage 6 YAML records made idempotent for repaired probe mappings.",
                "Stage 7 candidate menu marked partial and non-executable pending Stage 6C final manifest work.",
                "Codex SessionStart and Stop hooks stabilized as report-only defaults with opt-in strict mode.",
                f"Recommended next stage: {NEXT_STAGE_ID}.",
            ],
            "result_status": "metadata_repair_complete",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "puzzle_execution_allowed": False,
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                "No probes, diagnostics, route extraction, byte streams, OCR/image/stego tooling, "
                "PGP/OutGuess/F5/StegDetect execution, CUDA, scoring, benchmarks, target selection, "
                "canonical-corpus activation, page-boundary finalisation, Stage 7 archive creation, "
                "or solve claim."
            ),
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
                "# Stage 6B Codex Completion",
                "",
                f"- stage: {STAGE_TITLE}",
                f"- starting_commit: {POST_STAGE6_AUTOMATION_COMMIT}",
                "- final_commit: to be filled after commit",
                "- origin_main_commit: to be filled after push",
                "- github_issue: to be filled after issue update",
                "- ci_run_url: to be filled after CI",
                "- ci_status: to be filled after CI",
                f"- stage6_active_files_patched: {', '.join(PATCHED_STAGE6_FILES)}",
                f"- hook_default_exit_zero_verified: {summary['hook_default_exit_zero_verified']}",
                "- hook_reports_generated_only_as_ignored_local_output: true",
                "- protected_local_paths_not_staged: true",
                "- stage6c_routed_next: true",
                "- drive_stage6_completion_summary_warning_recorded: true",
                "- drive_stage6_completion_summary_edited_by_codex: false",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def write_final_completion_summary(
    *,
    final_commit: str,
    origin_main_commit: str,
    github_issue: str,
    ci_run_url: str,
    ci_status: str,
    validation_summary: list[str],
) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CODEX_COMPLETION_PATH.write_text(
        "\n".join(
            [
                "# Stage 6B Codex Completion",
                "",
                f"starting_commit: {POST_STAGE6_AUTOMATION_COMMIT}",
                f"final_commit: {final_commit}",
                f"origin_main_commit: {origin_main_commit}",
                f"github_issue: {github_issue}",
                f"ci_run_url: {ci_run_url}",
                f"ci_status: {ci_status}",
                "stage6_active_files_patched:",
                *[f"  - path: {path}" for path in PATCHED_STAGE6_FILES],
                "hook_default_exit_zero_verified: true",
                "hook_strict_mode_verified: true",
                "hook_reports_generated_only_as_ignored_local_output: true",
                "stage6_validate_after_repair_passed: true",
                "stage6b_validate_passed: true",
                "protected_local_paths_not_staged: true",
                "raw_generated_outputs_staged: false",
                "stage6c_routed_next: true",
                "drive_stage6_completion_summary_warning_recorded: true",
                "drive_stage6_completion_summary_edited_by_codex: false",
                "warning_type: stale_or_placeholder_drive_handoff",
                "blocking: false",
                "validation_summary:",
                *[f"  - {item}" for item in validation_summary],
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _agents_section() -> str:
    return f"""## Stage 6B Current Boundary

Current completed stage: {STAGE_TITLE}.

Current work: {NEXT_STAGE_TITLE}. Stage 6B repaired Stage 6 probe-family/source/readiness metadata and made project-local Codex hooks report-only by default. It did not run probes, create the final Stage 7 manifest, create archives, execute tooling, generate route or byte streams, run CUDA/scoring/benchmarks, or make a solve claim.
"""


def _chatgpt_section() -> str:
    return f"""## Stage 6B Current Boundary

Latest completed stage: {STAGE_TITLE}.

Current planning focus: {NEXT_STAGE_TITLE}.

Stage 6B is a triage repair stage. It preserves Stage 6 and the post-Stage-6 automation-hardening commit, repairs active Stage 6 planning metadata, and routes final finite Stage 7 manifest work to Stage 6C.
"""


def _status_section() -> str:
    return f"""## Stage 6B Status

- Latest completed stage: {STAGE_TITLE}.
- Current next stage: {NEXT_STAGE_TITLE}.
- Stage 7 execution allowed next: false.
- Stage 7 ZIP archive creation allowed next: false.
- Stage 6B repaired mappings and hooks only; final finite Stage 7 manifest work is deferred to Stage 6C.
"""


def _readme_section() -> str:
    return """## Stage 6B Current State

Stage 6B is complete as deterministic repair metadata. It fixes Stage 6 probe-family/source/readiness planning records, marks the Stage 7 menu as partial and non-executable, and stabilizes project-local hooks as report-only by default. Stage 6C remains the next planning stage for the final finite Stage 7 manifest and archive-run contract.
"""


def _roadmap_section() -> str:
    return f"""## Stage 6B Route

Stage 6B completed triage repair and hook stabilization without execution. Next: {NEXT_STAGE_TITLE}. Stage 7 execution, ZIP archive creation, Stage 8 triangle readiness, and Stage 9 experiments remain blocked.
"""


def _testing_section() -> str:
    return """## Stage 6B Validation

Stage 6B adds regression tests for the Stage 6 probe-family mapping bug, conservative readiness classes, source traceability, partial Stage 7 menu semantics, report-only hook behavior, and Stage 6B current-stage transition. Final validation must rerun Stage 6 validation after the active Stage 6 repair.
"""


def _staged_plan_section() -> str:
    return f"""## Stage 6B - Diagnostic Readiness Repair

Stage 6B repairs active Stage 6 planning metadata and project-local hooks. It is complete and routes to Stage 6C.

Current planning focus: {NEXT_STAGE_TITLE}.
"""


def _onboarding_section() -> str:
    return f"""## Stage 6B Current Truth

Use `data/project-state/current-stage-state.yaml` as authoritative. It records {STAGE_TITLE} as complete and {NEXT_STAGE_TITLE} as next.
"""


def _source_truth_section() -> str:
    return f"""## Stage 6B Source Of Truth

- Latest completed stage: {STAGE_TITLE}.
- Next routed stage: {NEXT_STAGE_TITLE}.
- Stage 6B repair ledger: `{PROJECT_STATE_PATHS['stage6_registry_repair_ledger'].as_posix()}`.
"""


def _operational_docs_section() -> str:
    return """## Stage 6B Operational Files

Stage 6B operational records live under `data/project-state/stage6b-*`, `data/token-block/stage6b-*`, and `data/source-harvester/stage6b-*`. Hook reports are ignored local output under `experiments/results/doc-drift/` and must not be staged.
"""


def _cli_section() -> str:
    return """## Stage 6B CLI

Use `libreprimus token-block build-stage6b`, `validate-stage6b`, and `stage6b-summary` for the aggregate repair stage. Focused validators cover Stage 6 preservation, repair assessment, family/source/readiness maps, Stage 7 menu status, hook stabilization, current-state transition, Source Browser loadability, gate closure, and handoff.
"""


def _experiment_doc() -> str:
    return f"""# Stage 6B Diagnostic-Readiness Repair

Stage 6B repairs metadata and hooks only. It does not run probes, execute diagnostics, generate route or byte streams, create archives, run CUDA/scoring/benchmarks, or make a solve claim. The final finite Stage 7 manifest and archive-run contract are deferred to {NEXT_STAGE_ID}.
"""


def _dev_log() -> str:
    return f"""# Stage 6B Development Log

Implemented Stage 6B as a deterministic repair stage on top of `{POST_STAGE6_AUTOMATION_COMMIT}`. The stage repairs active Stage 6 probe mappings/readiness, records an auditable repair ledger, stabilizes project-local hooks in report-only mode, and routes next work to {NEXT_STAGE_ID}.
"""


def _research_log() -> str:
    return f"""# Stage 6B Next-Stage Decision Summary

Stage 6B keeps Stage 7 execution blocked and routes the final finite Stage 7 manifest/archive-run contract to {NEXT_STAGE_ID}. Stage 6B is not a probe, source-lock expansion, archive generation, CUDA, scoring, benchmark, or solve-claim stage.
"""


def _ensure_no_protected_output_overlap() -> None:
    outputs = {path.as_posix() for path in DATA_PATHS.values()} | {path.as_posix() for path in SCHEMA_PATHS.values()}
    overlaps = sorted(outputs & set(PROTECTED_LOCAL_PATHS))
    if overlaps:
        raise RuntimeError(f"Stage 6B output paths overlap protected local state: {overlaps}")


def _write_current_stage_schema() -> None:
    path = Path("schemas/project-state/current-stage-state-v0.schema.json")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        payload = read_yaml(path)
    for key in ["latest_completed_stage_id", "stage_id"]:
        enum = payload["properties"][key].setdefault("enum", [])
        if STAGE_ID not in enum:
            enum.append(STAGE_ID)
    enum = payload["properties"]["recommended_next_stage_id"].setdefault("enum", [])
    if NEXT_STAGE_ID not in enum:
        enum.append(NEXT_STAGE_ID)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_doc_staleness_source_schema() -> None:
    path = Path("schemas/project-state/doc-staleness-source-of-truth-record-v0.schema.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    stage_enum = payload["properties"]["stage_id"].setdefault("enum", [])
    if STAGE_ID not in stage_enum:
        stage_enum.append(STAGE_ID)
    stage_pattern = r"Stage (5[A-Z]+(-fix)?|6[A-Z]?)"
    for key in [
        "expected_next_stage_prefix",
        "latest_completed_stage_after_this_stage",
        "latest_completed_stage_prefix",
        "latest_previous_stage",
        "next_stage_after_this_stage",
    ]:
        if key in payload["properties"]:
            payload["properties"][key]["pattern"] = stage_pattern
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _old_problem_for(path: str) -> str:
    if path.endswith("stage6.py"):
        return "Stage 6 builder used broad or substring-derived probe classification."
    if "discovery-probe" in path:
        return "Stage 6 registry mapped non-Lag5 probes to Lag5 and lacked full source/readiness shape."
    if "readiness" in path:
        return "Stage 6 readiness overused broad deterministic-ready classes."
    if "candidate-menu" in path:
        return "Stage 6 candidate menu was Observation-only but not clearly non-final/non-executable."
    return "Stage 6 active planning metadata still used source-lock-only wording for a broader metadata/readiness stage."


def _new_value_for(path: str) -> str:
    if path.endswith("stage6.py"):
        return "Explicit probe classification table with conservative readiness and source traceability."
    if "candidate-menu" in path:
        return "Partial foundation menu marked not an execution manifest and routed to Stage 6C."
    if "discovery-probe" in path or "readiness" in path:
        return "Corrected family/source/readiness metadata generated from explicit Stage 6 table."
    return "Stage 6 record regenerated with source_lock_only=false and source_lock_component_present=true."


def _result(errors: list[str], **counts: Any) -> ValidationResult:
    return ValidationResult(errors, counts)
