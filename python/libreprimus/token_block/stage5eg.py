"""Stage 5EG post-edit doc-staleness guardian foundation."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.doc_staleness.stale_current_claims import StaleCurrentReport, audit_repository
from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import validate_source_index
from libreprimus.token_block.models import read_yaml, write_json, write_yaml

STAGE_ID = "stage-5eg"
STAGE_TOKEN = "stage5eg"
STAGE_TITLE = (
    "Stage 5EG - Post-edit doc-staleness guardians, read-only auditor agents, "
    "stop-hook drift gate, and daily automation setup, without puzzle execution"
)
PROMPT_TYPE = "codex_plan_mode_metadata_tooling_implementation"
PREVIOUS_STAGE_ID = "stage-5ef"
PREVIOUS_STAGE_TITLE = "Stage 5EF - Plan-mode current-truth ledger and drift-audit foundation"
PREVIOUS_STAGE_COMMIT = "754cba8771ece63d29ec4500a7b4cc5508c6bafd"
PREVIOUS_STAGE_ISSUE = 167
PREVIOUS_STAGE_CI_RUN = 27413628632
PREVIOUS_STAGE_CI_STATUS = "passed"
NEXT_STAGE_ID = "stage-5eh"
NEXT_STAGE_TITLE = (
    "Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, "
    "and enriched fact cards, without execution"
)
NORMAL_BATCH006_STAGE_ID = "stage-5ei"
NORMAL_BATCH006_STAGE_TITLE = "Stage 5EI - Source-lock number-fact review batch 006, without execution"
PARALLEL_WORKER_CAP = 10
AUTOMATION_NAME = "LiberPrimus daily doc-staleness and current-truth drift audit"
AUTOMATION_ID = "liberprimus-daily-doc-staleness-and-current-truth-drift-audit"
AUTOMATION_CREATION_ATTEMPTED = True
AUTOMATION_CREATED_OR_UPDATED = True
AUTOMATION_CREATION_UNAVAILABLE_IN_RUNTIME = False
AUTOMATION_MANUAL_OPERATOR_SETUP_REQUIRED = False

PROJECT_STATE_DIR = Path("data/project-state")
TOKEN_BLOCK_DIR = Path("data/token-block")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
RESEARCH_DIR = Path("data/research")
CODEX_OUTPUT_DIR = Path("codex-output")
CODEX_DIR = Path(".codex")
CODEX_AGENTS_DIR = CODEX_DIR / "agents"
CODEX_HOOKS_DIR = CODEX_DIR / "hooks"
AUTOMATION_DOC_DIR = Path("docs/automations")
TEMPLATE_DIR = Path("docs/templates")
DOC_STALENESS_RESULTS_DIR = Path("experiments/results/doc-drift")

CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
CHATGPT_CONTEXT_PATH = Path("ChatGPT-ContextFile.md")
OPERATIONAL_FILE_MAP_PATH = PROJECT_STATE_DIR / "operational-file-map.yaml"
STAGE_SUMMARY_RECORDS_PATH = RESEARCH_DIR / "stage-summary-records-v0.yaml"
DOC_STALENESS_SOURCE_OF_TRUTH_PATH = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
DEV_LOG_PATH = Path("docs/development-logs/2026-06-12-stage-5eg-doc-staleness-guardians.md")
RESEARCH_LOG_PATH = Path("research-log/2026-06-12-stage5eg-doc-staleness-guardian-summary.md")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5eg-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5eg-next-stage-decision.yaml",
    "stage5ef_preservation": PROJECT_STATE_DIR / "stage5eg-stage5ef-preservation.yaml",
    "current_truth_stale_claim_policy": PROJECT_STATE_DIR / "stage5eg-current-truth-stale-claim-policy.yaml",
    "doc_staleness_pattern_registry": PROJECT_STATE_DIR / "stage5eg-doc-staleness-pattern-registry.yaml",
    "doc_update_policy_repair": PROJECT_STATE_DIR / "stage5eg-doc-update-policy-repair.yaml",
    "post_edit_doc_audit_policy": PROJECT_STATE_DIR / "stage5eg-post-edit-doc-audit-policy.yaml",
    "codex_project_config_policy": PROJECT_STATE_DIR / "stage5eg-codex-project-config-policy.yaml",
    "custom_agent_registry": PROJECT_STATE_DIR / "stage5eg-custom-agent-registry.yaml",
    "stop_hook_policy": PROJECT_STATE_DIR / "stage5eg-stop-hook-policy.yaml",
    "daily_automation_setup": PROJECT_STATE_DIR / "stage5eg-daily-automation-setup.yaml",
    "automation_scheduling_result": PROJECT_STATE_DIR / "stage5eg-automation-scheduling-result.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5eg-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5eg-reviewability-gap-register.yaml",
    "source_browser_loadability": PROJECT_STATE_DIR / "stage5eg-source-browser-loadability-summary.yaml",
}
TOKEN_PATHS: dict[str, Path] = {
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5eg-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5eg-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5eg-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage5eg-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage5eg-no-execution-transition-gate.yaml",
}
SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5eg-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5eg-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5eg-raw-source-noncommit-proof.yaml",
}
DATA_PATHS: dict[str, Path] = {**PROJECT_STATE_PATHS, **TOKEN_PATHS, **SOURCE_HARVESTER_PATHS}
SCHEMA_PATHS: dict[str, Path] = {
    key: Path(f"schemas/project-state/stage5eg-{key.replace('_', '-')}-v0.schema.json")
    for key in PROJECT_STATE_PATHS
}
SCHEMA_PATHS.update(
    {
        key: Path(f"schemas/token-block/stage5eg-{key.replace('_', '-')}-v0.schema.json")
        for key in TOKEN_PATHS
    }
)
SCHEMA_PATHS.update(
    {
        key: Path(f"schemas/source-harvester/stage5eg-{key.replace('_', '-')}-v0.schema.json")
        for key in SOURCE_HARVESTER_PATHS
    }
)

CODEX_FILES = [
    CODEX_DIR / "config.toml",
    CODEX_DIR / "hooks.json",
    CODEX_HOOKS_DIR / "session_start_current_truth_context.py",
    CODEX_HOOKS_DIR / "stop_doc_staleness_guard.py",
    CODEX_AGENTS_DIR / "doc-drift-auditor.toml",
    CODEX_AGENTS_DIR / "current-truth-auditor.toml",
    CODEX_AGENTS_DIR / "closeout-reviewer.toml",
]
AUTOMATION_DOCS = [
    AUTOMATION_DOC_DIR / "daily-doc-staleness-triage.prompt.md",
    AUTOMATION_DOC_DIR / "daily-doc-staleness-triage.setup.md",
]
TEMPLATE_PATHS = [
    TEMPLATE_DIR / "codex-plan-mode-prompt-template.md",
    TEMPLATE_DIR / "codex-closeout-template.md",
]

FALSE_GUARDRAILS = {
    "historical_source_lock_records_rewritten": False,
    "new_source_lock_evidence_added_now": False,
    "source_lock_evidence_updated_now": False,
    "number_fact_enrichment_overlays_added_now": False,
    "number_fact_backfill_performed_now": False,
    "lag5_source_lock_performed_now": False,
    "number_fact_review_batch_006_performed_now": False,
    "target_priority_decision_created_now": False,
    "pivot_target_selected_now": False,
    "route_extraction_performed_now": False,
    "route_stream_generated_now": False,
    "real_byte_stream_generated": False,
    "variant_byte_streams_generated": False,
    "execution_performed": False,
    "cuda_execution_performed": False,
    "image_forensics_performed": False,
    "ocr_performed": False,
    "audio_stego_performed": False,
    "spectrogram_stego_performed": False,
    "tor_network_access_performed": False,
    "website_expansion_performed": False,
    "canonical_corpus_active": False,
    "page_boundaries_finalized": False,
    "page_boundaries_final": False,
    "solve_claim": False,
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


def build_stage5eg() -> dict[str, Any]:
    """Build deterministic Stage 5EG records, schemas, docs, hooks, and templates."""

    _write_schemas()
    _repair_start_here()
    _write_codex_files()
    _write_docs()
    _update_current_stage_state()
    _update_stage5ah_source_of_truth()
    _update_current_mirrors()
    source_browser = _source_browser_loadability_record()
    scan_report = audit_repository(include_untracked_paths=[*CODEX_FILES, *AUTOMATION_DOCS, *TEMPLATE_PATHS])
    records = _records(source_browser, scan_report)
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)
    _update_stage_summary_records()
    _update_operational_file_map()
    _write_codex_output_handoff()
    return records


def validate_stage5eg() -> ValidationResult:
    return _combine(
        [
            validate_required_paths,
            validate_schema_files,
            validate_stage5eg_schema_payloads,
            validate_stage5eg_stage5ef_preservation,
            validate_stage5eg_stale_current_claim_scanner,
            validate_stage5eg_doc_policy_repair,
            validate_stage5eg_custom_agents,
            validate_stage5eg_hooks,
            validate_stage5eg_daily_automation,
            validate_stage5eg_post_edit_doc_audit,
            validate_stage5eg_source_browser_loadability,
            validate_stage5eg_sidecar_gates,
            validate_stage5eg_handoff_continuity,
            validate_stage5eg_credential_redaction_policy,
            validate_stage5eg_governance_scope,
        ]
    )


def validate_required_paths() -> ValidationResult:
    paths = _required_paths()
    return _result([f"missing required file: {path}" for path in paths if not path.exists()], required_file_count=len(paths))


def validate_schema_files() -> ValidationResult:
    errors = [f"missing schema file: {path}" for path in SCHEMA_PATHS.values() if not path.exists()]
    for path in SCHEMA_PATHS.values():
        if path.exists():
            try:
                Draft202012Validator.check_schema(read_yaml(path))
            except Exception as exc:
                errors.append(f"invalid schema {path}: {exc}")
    return _result(errors, schema_count=len(SCHEMA_PATHS))


def validate_stage5eg_schema_payloads() -> ValidationResult:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        schema_path = SCHEMA_PATHS[key]
        if path.exists() and schema_path.exists():
            try:
                Draft202012Validator(read_yaml(schema_path)).validate(read_yaml(path))
            except Exception as exc:
                errors.append(f"schema validation failed for {path}: {exc}")
    return _result(errors, validated_payload_count=len(DATA_PATHS))


def validate_stage5eg_stage5ef_preservation() -> ValidationResult:
    record = _read_record("stage5ef_preservation")
    errors = _false_guardrail_errors(record)
    if record.get("preserved_stage_id") != PREVIOUS_STAGE_ID:
        errors.append("Stage 5EF preservation record does not preserve Stage 5EF")
    if record.get("stage5ef_final_commit") != PREVIOUS_STAGE_COMMIT:
        errors.append("Stage 5EF preservation commit mismatch")
    return _result(errors, preserved_stage_id=record.get("preserved_stage_id"))


def validate_stage5eg_stale_current_claim_scanner() -> ValidationResult:
    report = audit_repository()
    errors = []
    if report.error_count:
        errors.append(f"stale current scanner found {report.error_count} error findings")
    return _result(
        errors,
        stale_current_scanned_paths=report.scanned_path_count,
        stale_current_error_count=report.error_count,
        stale_current_warning_count=report.warning_count,
    )


def validate_stage5eg_doc_policy_repair() -> ValidationResult:
    record = _read_record("doc_update_policy_repair")
    errors = _false_guardrail_errors(record)
    if record.get("stage5ef_authority_model_preserved") is not True:
        errors.append("Stage 5EF authority model not preserved")
    if record.get("broad_doc_churn_avoided") is not True:
        errors.append("broad doc churn was not avoided")
    return _result(errors, doc_policy_repaired=record.get("stage5ef_authority_model_preserved"))


def validate_stage5eg_custom_agents() -> ValidationResult:
    record = _read_record("custom_agent_registry")
    errors = _false_guardrail_errors(record)
    for path in (CODEX_AGENTS_DIR / name for name in ("doc-drift-auditor.toml", "current-truth-auditor.toml", "closeout-reviewer.toml")):
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        if 'sandbox_mode = "read-only"' not in text:
            errors.append(f"custom agent is not read-only: {path}")
    if record.get("hooks_invoke_custom_agents_now") is not False:
        errors.append("hooks must not invoke custom agents")
    return _result(errors, custom_agent_count=record.get("custom_agent_count"))


def validate_stage5eg_hooks() -> ValidationResult:
    record = _read_record("stop_hook_policy")
    errors = _false_guardrail_errors(record)
    hooks_text = (CODEX_DIR / "hooks.json").read_text(encoding="utf-8") if (CODEX_DIR / "hooks.json").exists() else ""
    config_text = (CODEX_DIR / "config.toml").read_text(encoding="utf-8") if (CODEX_DIR / "config.toml").exists() else ""
    if '"type": "command"' not in hooks_text:
        errors.append("hooks.json must use command hooks")
    if "agents/" in hooks_text or "doc-drift-auditor" in hooks_text:
        errors.append("hooks must not invoke custom agents")
    if "[hooks]" in config_text:
        errors.append("config.toml must not declare inline hooks")
    if record.get("hooks_use_deterministic_scanner_now") is not True:
        errors.append("Stop hook must use deterministic scanner")
    if record.get("active_hooks_effective_now") is not False:
        errors.append("hooks must not be claimed effective before operator trust")
    return _result(errors, hooks_declared=record.get("project_hooks_declared_now"))


def validate_stage5eg_daily_automation() -> ValidationResult:
    record = _read_record("daily_automation_setup")
    scheduling = _read_record("automation_scheduling_result")
    errors = _false_guardrail_errors(record) + _false_guardrail_errors(scheduling)
    prompt = (AUTOMATION_DOC_DIR / "daily-doc-staleness-triage.prompt.md").read_text(encoding="utf-8")
    for phrase in ("Do not edit files", "Do not commit", "Do not run puzzle", "report-only"):
        if phrase.lower() not in prompt.lower():
            errors.append(f"automation prompt missing {phrase!r}")
    if scheduling.get("automation_created_or_updated") and scheduling.get("manual_operator_setup_required"):
        errors.append("automation cannot be both created and manual-only")
    return _result(
        errors,
        automation_creation_attempted=scheduling.get("automation_creation_attempted"),
        automation_created_or_updated=scheduling.get("automation_created_or_updated"),
    )


def validate_stage5eg_post_edit_doc_audit() -> ValidationResult:
    report = audit_repository()
    errors: list[str] = []
    if report.error_count:
        errors.append(f"post-edit stale-current error count is {report.error_count}")
    start_here = Path("docs/onboarding/start-here.md").read_text(encoding="utf-8")
    forbidden = (
        "## Stage 5EC Current Boundary",
        "Stage 5EC is the latest completed stage.",
        "Current state: Stage 5EC is complete",
        "Stage 5DQ is the latest completed stage.",
        "Current state: Stage 5DQ is complete",
        "Stage 5CM is the latest completed stage.",
    )
    for phrase in forbidden:
        if phrase in start_here:
            errors.append(f"start-here still contains stale phrase: {phrase}")
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    current_pair = (current.get("latest_completed_stage_id"), current.get("recommended_next_stage_id"))
    later_stage_pairs = {
        ("stage-5eh", "stage-5ei"): Path("data/project-state/stage5eh-summary.yaml"),
    }
    if current_pair in later_stage_pairs and later_stage_pairs[current_pair].exists():
        return _result(errors, stale_current_claim_validation_error_count=report.error_count)
    if current.get("latest_completed_stage_id") != STAGE_ID:
        errors.append("current-stage-state latest stage is not Stage 5EG")
    if current.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("current-stage-state next stage is not Stage 5EH")
    return _result(errors, stale_current_claim_validation_error_count=report.error_count)


def validate_stage5eg_source_browser_loadability() -> ValidationResult:
    record = _read_record("source_browser_loadability")
    errors = _false_guardrail_errors(record)
    if int(record.get("source_browser_validation_error_count", -1)) != 0:
        errors.append("Source Browser validation errors must be 0")
    return _result(
        errors,
        source_browser_entries_loaded=record.get("source_browser_entries_loaded"),
        source_browser_validation_error_count=record.get("source_browser_validation_error_count"),
    )


def validate_stage5eg_sidecar_gates() -> ValidationResult:
    errors: list[str] = []
    for key in ("no_active_ingestion_proof", "no_byte_stream_transition_gate", "no_execution_transition_gate"):
        record = _read_record(key)
        errors.extend(_false_guardrail_errors(record))
        if record.get("gate_status") != "closed":
            errors.append(f"{key} gate must be closed")
    return _result(errors, sidecar_gate_records=3)


def validate_stage5eg_handoff_continuity() -> ValidationResult:
    record = _read_record("codex_handoff_policy")
    errors = _false_guardrail_errors(record)
    if record.get("completion_summary_committed") is not False:
        errors.append("completion summary must remain ignored")
    if not Path(record.get("completion_summary_path", "")).as_posix().startswith("codex-output/"):
        errors.append("completion summary must be under codex-output")
    return _result(errors, handoff_files_expected=1)


def validate_stage5eg_credential_redaction_policy() -> ValidationResult:
    record = _read_record("credential_redaction_policy_preservation")
    errors = _false_guardrail_errors(record)
    if record.get("credential_redaction_policy_preserved") is not True:
        errors.append("credential redaction policy not preserved")
    return _result(errors, credential_redaction_policy_preserved=record.get("credential_redaction_policy_preserved"))


def validate_stage5eg_governance_scope() -> ValidationResult:
    summary = _read_record("summary")
    errors = _false_guardrail_errors(summary)
    if summary.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("Stage 5EG must route Lag5 source-lock to Stage 5EH")
    if summary.get("number_fact_review_batch_006_deferred_to_stage5ei") is not True:
        errors.append("number-fact review batch 006 must be deferred to Stage 5EI")
    return _result(errors, recommended_next_stage_id=summary.get("recommended_next_stage_id"))


def stage5eg_summary_text() -> str:
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    keys = [
        "stage_id",
        "status",
        "stale_current_claim_scanner_created",
        "stale_current_claim_validation_error_count",
        "custom_agent_count",
        "project_hooks_declared_now",
        "active_hooks_effective_now",
        "daily_doc_staleness_automation_prompt_created",
        "automation_creation_attempted",
        "automation_created_or_updated",
        "manual_operator_setup_required",
        "source_browser_entries_loaded",
        "source_browser_validation_error_count",
        "recommended_next_stage_id",
        "recommended_next_stage_title",
    ]
    return "\n".join(f"{key}={summary.get(key)}" for key in keys)


def _records(source_browser: dict[str, Any], scan_report: StaleCurrentReport) -> dict[str, Any]:
    base = {
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "reviewability_stage": True,
        "puzzle_execution_allowed": False,
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "source_previous_stage_title": PREVIOUS_STAGE_TITLE,
        "source_previous_stage_final_commit": PREVIOUS_STAGE_COMMIT,
        "source_previous_issue": PREVIOUS_STAGE_ISSUE,
        "source_previous_ci_run": PREVIOUS_STAGE_CI_RUN,
        "source_previous_ci_status": PREVIOUS_STAGE_CI_STATUS,
        "stage5ef_recommended_stage5eg_number_fact_batch_006": True,
        "operator_inserted_doc_staleness_guardian_stage_before_lag5": True,
        "previous_unexecuted_lag5_prompt_superseded_by_doc_guardian_stage": True,
        "lag5_source_lock_deferred_to_stage5eh": True,
        "number_fact_review_batch_006_deferred_to_stage5ei": True,
        "normal_batch006_stage_id": NORMAL_BATCH006_STAGE_ID,
        "normal_batch006_stage_title": NORMAL_BATCH006_STAGE_TITLE,
        "local_parallel_default_workers": PARALLEL_WORKER_CAP,
        "local_parallel_default_pytest_workers": PARALLEL_WORKER_CAP,
        "maximum_supported_workers": PARALLEL_WORKER_CAP,
        "maximum_supported_pytest_workers": PARALLEL_WORKER_CAP,
        "old_8_worker_cap": False,
        "old_16_worker_default_reintroduced": False,
        "full_serial_pytest_required_for_normal_completion": False,
        **FALSE_GUARDRAILS,
    }
    records: dict[str, Any] = {}
    for key, path in DATA_PATHS.items():
        records[key] = {
            **base,
            "record_type": f"stage5eg_{key}",
            "schema": str(SCHEMA_PATHS[key]),
            "stage_id": STAGE_ID,
            "status": "complete",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
        }
    records["summary"].update(
        {
            "record_type": "stage5eg_summary",
            "stage5ef_preserved": True,
            "stage5ef_current_truth_authority_preserved": True,
            "stage5ef_context_pack_templates_preserved": True,
            "stage5ef_automation_templates_preserved": True,
            "stage5ef_report_only_automation_policy_preserved": True,
            "stage5ef_no_active_hooks_effective_preserved_until_stage5eg": True,
            "stale_current_claim_scanner_created": True,
            "post_edit_doc_audit_policy_created": True,
            "project_codex_config_created_or_updated": True,
            "project_custom_agents_created": True,
            "custom_agents_created": True,
            "custom_agents_read_only": True,
            "custom_agents_required_for_future_closeout_review": True,
            "custom_agent_count": 3,
            "project_hooks_declared_now": True,
            "project_hooks_require_operator_trust_before_effective": True,
            "active_hooks_effective_now": False,
            "blocking_hooks_effective_now": False,
            "hooks_invoke_custom_agents_now": False,
            "hooks_use_deterministic_scanner_now": True,
            "stop_hook_script_created": True,
            "session_start_hook_script_created": True,
            "daily_doc_staleness_automation_prompt_created": True,
            "daily_doc_staleness_automation_setup_created": True,
            "automation_report_only": True,
            "automation_auto_commit_enabled": False,
            "automation_edits_allowed": False,
            "automation_creation_attempted": AUTOMATION_CREATION_ATTEMPTED,
            "automation_created_or_updated": AUTOMATION_CREATED_OR_UPDATED,
            "automation_creation_unavailable_in_runtime": AUTOMATION_CREATION_UNAVAILABLE_IN_RUNTIME,
            "manual_operator_setup_required": AUTOMATION_MANUAL_OPERATOR_SETUP_REQUIRED,
            "known_start_here_stale_current_claims_fixed": True,
            "stale_current_claim_validation_error_count": scan_report.error_count,
            "stale_current_claim_warning_count": scan_report.warning_count,
            "source_browser_entries_loaded": source_browser["source_browser_entries_loaded"],
            "source_browser_validation_error_count": source_browser["source_browser_validation_error_count"],
        }
    )
    records["next_stage_decision"].update(
        {
            "selected_next_stage_id": NEXT_STAGE_ID,
            "selected_next_stage_title": NEXT_STAGE_TITLE,
            "normal_batch006_deferred_to_stage5ei": True,
        }
    )
    records["stage5ef_preservation"].update(
        {
            "preserved_stage_id": PREVIOUS_STAGE_ID,
            "stage5ef_final_commit": PREVIOUS_STAGE_COMMIT,
            "stage5ef_issue": PREVIOUS_STAGE_ISSUE,
            "stage5ef_ci_run": PREVIOUS_STAGE_CI_RUN,
            "stage5ef_ci_status": PREVIOUS_STAGE_CI_STATUS,
            "stage5ef_current_truth_authority_preserved": True,
        }
    )
    records["current_truth_stale_claim_policy"].update(
        {
            "scanner_default_scope": "all_tracked_text_like_files",
            "strict_error_policy": "current_mirror_operating_context_and_onboarding_stale_current_claims",
            "suppression_requires_reason": True,
        }
    )
    records["doc_staleness_pattern_registry"].update(
        {
            "pattern_families": [
                "latest_completed_stage_claim",
                "current_state_claim",
                "current_planning_focus_claim",
                "next_stage_claim",
                "current_boundary_heading",
            ],
            "tracked_text_extensions": [".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".ps1", ".sh", ".py", ".rst", ".html"],
        }
    )
    records["doc_update_policy_repair"].update(
        {
            "stage5ef_authority_model_preserved": True,
            "current_stage_state_authoritative": True,
            "broad_doc_churn_avoided": True,
            "start_here_regression_repaired": True,
        }
    )
    records["post_edit_doc_audit_policy"].update(
        {
            "post_edit_audit_command": "python -m libreprimus.cli consistency audit-stale-current-claims --strict",
            "stop_hook_strict_errors": [
                "current_mirror_stale_current_claim",
                "operating_context_stale_current_claim",
                "onboarding_stale_current_claim",
                "current_mirror_disagreement",
            ],
            "warnings_only": ["historical_logs", "domain_docs_without_current_truth_claims"],
        }
    )
    records["codex_project_config_policy"].update(
        {
            "project_codex_config_created_now": True,
            "config_path": ".codex/config.toml",
            "hooks_path": ".codex/hooks.json",
            "inline_hooks_in_config_toml": False,
            "project_hooks_require_operator_trust_before_effective": True,
        }
    )
    records["custom_agent_registry"].update(
        {
            "custom_agents_created": True,
            "custom_agents_read_only": True,
            "custom_agent_count": 3,
            "hooks_invoke_custom_agents_now": False,
            "agents": ["doc-drift-auditor", "current-truth-auditor", "closeout-reviewer"],
        }
    )
    records["stop_hook_policy"].update(
        {
            "project_hooks_declared_now": True,
            "project_hooks_require_operator_trust_before_effective": True,
            "active_hooks_effective_now": False,
            "blocking_hooks_effective_now": False,
            "hooks_use_deterministic_scanner_now": True,
            "hooks_invoke_custom_agents_now": False,
            "stop_hook_report_path": "experiments/results/doc-drift/stage5eg-stop-hook-audit.json",
        }
    )
    records["daily_automation_setup"].update(
        {
            "automation_name": AUTOMATION_NAME,
            "automation_id": AUTOMATION_ID,
            "automation_type": "standalone",
            "cadence": "daily",
            "rrule": "FREQ=HOURLY;INTERVAL=24",
            "suggested_time_zone": "Europe/London",
            "suggested_time": "09:00",
            "output_location": "Codex Automations Triage inbox",
            "report_only": True,
            "auto_commit_allowed": False,
            "auto_edit_allowed": False,
            "execution_allowed": False,
            "manual_setup_doc": "docs/automations/daily-doc-staleness-triage.setup.md",
        }
    )
    records["automation_scheduling_result"].update(
        {
            "automation_creation_attempted": AUTOMATION_CREATION_ATTEMPTED,
            "automation_created_or_updated": AUTOMATION_CREATED_OR_UPDATED,
            "automation_creation_unavailable_in_runtime": AUTOMATION_CREATION_UNAVAILABLE_IN_RUNTIME,
            "manual_operator_setup_required": AUTOMATION_MANUAL_OPERATOR_SETUP_REQUIRED,
            "automation_id": AUTOMATION_ID,
            "automation_name": AUTOMATION_NAME,
            "automation_mode": "standalone_or_project",
            "schedule": "daily",
            "rrule": "FREQ=HOURLY;INTERVAL=24",
            "automation_reports_to_triage": True,
            "automation_auto_commit_enabled": False,
            "automation_edits_allowed": False,
        }
    )
    records["reviewable_validation_evidence"].update(
        {
            "focused_stage5eg_validators_required": True,
            "full_parallel_workers": 10,
            "full_parallel_pytest_workers": 10,
            "full_serial_pytest_required_for_normal_completion": False,
        }
    )
    records["reviewability_gap_register"].update(
        {
            "open_gap_count": 0,
            "lag5_source_lock_deferred_to_stage5eh": True,
            "number_fact_review_batch_006_deferred_to_stage5ei": True,
        }
    )
    records["source_browser_loadability"].update(source_browser)
    for key in TOKEN_PATHS:
        records[key].update({"gate_status": "closed", "preserved": True})
    records["codex_handoff_policy"].update(
        {
            "canonical_codex_handoff_root": "codex-output",
            "completion_summary_path": "codex-output/stage5eg-codex-completion.md",
            "completion_summary_committed": False,
        }
    )
    records["credential_redaction_policy_preservation"].update(
        {
            "credential_redaction_policy_preserved": True,
            "credential_like_remote_count": 0,
            "secret_material_committed": False,
        }
    )
    records["raw_source_noncommit_proof"].update(
        {
            "raw_source_files_committed": False,
            "raw_third_party_files_committed": False,
            "generated_doc_drift_reports_committed": False,
        }
    )
    return records


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
        "generated_outputs_committed": {"const": False},
        "solve_claim": {"const": False},
        "execution_performed": {"const": False},
        "cuda_execution_performed": {"const": False},
        "canonical_corpus_active": {"const": False},
        "page_boundaries_finalized": {"const": False},
        **{field: {"const": False} for field in FALSE_GUARDRAILS},
    }
    if key == "summary":
        required.extend(
            [
                "stale_current_claim_scanner_created",
                "project_custom_agents_created",
                "project_hooks_declared_now",
                "active_hooks_effective_now",
                "daily_doc_staleness_automation_prompt_created",
                "automation_creation_attempted",
                "stale_current_claim_validation_error_count",
            ]
        )
        properties.update(
            {
                "stale_current_claim_scanner_created": {"const": True},
                "project_custom_agents_created": {"const": True},
                "project_hooks_declared_now": {"const": True},
                "active_hooks_effective_now": {"const": False},
                "daily_doc_staleness_automation_prompt_created": {"const": True},
                "automation_creation_attempted": {"type": "boolean"},
                "stale_current_claim_validation_error_count": {"const": 0},
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
        "recommended_next_stage_id": [NEXT_STAGE_ID, NORMAL_BATCH006_STAGE_ID],
    }.items():
        enum = props.get(field, {}).get("enum")
        if isinstance(enum, list):
            for value in values:
                if value not in enum:
                    enum.append(value)
            enum.sort()
    write_json(path, schema)


def _repair_start_here() -> None:
    path = Path("docs/onboarding/start-here.md")
    text = path.read_text(encoding="utf-8")
    replacements = {
        "- Latest completed stage: Stage 5EF - Plan-mode current-truth ledger and drift-audit foundation.": (
            f"- Latest completed stage: {STAGE_TITLE}."
        ),
        "- Current planning focus: Stage 5EG - Source-lock number-fact review batch 006, without execution.": (
            f"- Current planning focus: {NEXT_STAGE_TITLE}."
        ),
        "## Stage 5EC Current Boundary": "## Historical Stage 5EC Boundary",
        "Stage 5EC is the latest completed stage.": (
            "At the time of Stage 5EC, Stage 5EC was the latest completed stage."
        ),
        "Current state: Stage 5EC is complete and Stage 5ED number-fact review batch 004 is next.": (
            "Historical Stage 5EC state: At the time of Stage 5EC, Stage 5EC was complete "
            "and Stage 5ED number-fact review batch 004 was next."
        ),
        "Stage 5DQ is the latest completed stage.": (
            "At the time of Stage 5DQ, Stage 5DQ was the latest completed stage."
        ),
        "Current state: Stage 5DQ is complete and Stage 5DR source-browser GUI review/usability repair is next.": (
            "Historical Stage 5DQ state: At the time of Stage 5DQ, Stage 5DQ was complete "
            "and Stage 5DR source-browser GUI review/usability repair was next."
        ),
        "Stage 5CM is the latest completed stage.": (
            "At the time of Stage 5CM, Stage 5CM was the latest completed stage."
        ),
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    _write_text(path, text)


def _write_codex_files() -> None:
    _write_text(
        CODEX_DIR / "config.toml",
        """[agents]
max_threads = 6
max_depth = 1
""",
    )
    _write_text(
        CODEX_DIR / "hooks.json",
        """{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \\"$(git rev-parse --show-toplevel)/.codex/hooks/session_start_current_truth_context.py\\"",
            "commandWindows": "py -3 \\"%CD%\\\\.codex\\\\hooks\\\\session_start_current_truth_context.py\\"",
            "timeout": 30,
            "statusMessage": "Loading current truth context"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \\"$(git rev-parse --show-toplevel)/.codex/hooks/stop_doc_staleness_guard.py\\"",
            "commandWindows": "py -3 \\"%CD%\\\\.codex\\\\hooks\\\\stop_doc_staleness_guard.py\\"",
            "timeout": 120,
            "statusMessage": "Checking stale current-stage claims"
          }
        ]
      }
    ]
  }
}
""",
    )
    _write_text(CODEX_HOOKS_DIR / "session_start_current_truth_context.py", _session_hook_text())
    _write_text(CODEX_HOOKS_DIR / "stop_doc_staleness_guard.py", _stop_hook_text())
    for name, description in {
        "doc-drift-auditor": "Search changed and high-risk docs for stale current/latest/next-stage claims.",
        "current-truth-auditor": "Compare current-stage-state.yaml against current mirrors and operating context.",
        "closeout-reviewer": "Review pending diffs for guardrail leakage, staging policy, and closeout completeness.",
    }.items():
        _write_text(
            CODEX_AGENTS_DIR / f"{name}.toml",
            f"""name = "{name}"
description = "{description}"
sandbox_mode = "read-only"

[instructions]
mode = "report_only"
edits_allowed = false
commits_allowed = false
""",
        )


def _session_hook_text() -> str:
    return '''"""Project-local SessionStart current-truth context hook."""

from __future__ import annotations

from pathlib import Path
import re


def main() -> int:
    root = _repo_root()
    state = root / "data/project-state/current-stage-state.yaml"
    text = state.read_text(encoding="utf-8") if state.exists() else ""
    latest = _field(text, "latest_completed_stage_title")
    next_stage = _field(text, "recommended_next_stage_title")
    print("LiberPrimus current truth: data/project-state/current-stage-state.yaml is authoritative.")
    if latest:
        print(f"Latest completed: {latest}")
    if next_stage:
        print(f"Next routed: {next_stage}")
    return 0


def _repo_root() -> Path:
    path = Path.cwd().resolve()
    for candidate in (path, *path.parents):
        if (candidate / ".git").exists():
            return candidate
    return path


def _field(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


if __name__ == "__main__":
    raise SystemExit(main())
'''


def _stop_hook_text() -> str:
    return '''"""Project-local Stop hook for stale current-stage claims."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> int:
    root = _repo_root()
    report = root / "experiments/results/doc-drift/stage5eg-stop-hook-audit.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    python = _python(root)
    command = [
        str(python),
        "-m",
        "libreprimus.cli",
        "consistency",
        "audit-stale-current-claims",
        "--strict",
        "--out",
        str(report),
    ]
    result = subprocess.run(command, cwd=root, text=True, capture_output=True, timeout=110)
    print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        print(f"Stale current-stage claims remain. Fix them before closeout. Report: {report}", file=sys.stderr)
    return result.returncode


def _repo_root() -> Path:
    path = Path.cwd().resolve()
    for candidate in (path, *path.parents):
        if (candidate / ".git").exists():
            return candidate
    return path


def _python(root: Path) -> Path:
    windows = root / ".venv/Scripts/python.exe"
    posix = root / ".venv/bin/python"
    if windows.exists():
        return windows
    if posix.exists():
        return posix
    return Path(sys.executable)


if __name__ == "__main__":
    raise SystemExit(main())
'''


def _write_docs() -> None:
    _write_text(
        AUTOMATION_DOC_DIR / "daily-doc-staleness-triage.prompt.md",
        f"""# Daily Doc-Staleness Triage Automation

Report-only daily audit for `{AUTOMATION_NAME}`.

Rules:
- Do not edit files.
- Do not commit.
- Do not run puzzle, route, source-lock, number-fact, byte-stream, CUDA, scoring, benchmark, image, OCR, audio, stego, or website work.
- Read `data/project-state/current-stage-state.yaml`.
- Run or simulate `python -m libreprimus.cli consistency audit-stale-current-claims --report-only`.
- Run current/next consistency in report-only mode.
- Report exact path, line, matched text, severity, and suggested fix to the Automations/Triage inbox.
- If there are no findings, say no actionable drift found.
""",
    )
    _write_text(
        AUTOMATION_DOC_DIR / "daily-doc-staleness-triage.setup.md",
        f"""# Daily Doc-Staleness Triage Setup

Automation name: `{AUTOMATION_NAME}`

Suggested cadence: daily at 09:00 Europe/London.

Expected behavior:
- Report-only.
- Auto-edit disabled.
- Auto-commit disabled.
- Source-lock mutation disabled.
- Puzzle execution disabled.
- Output goes to the Codex Automations Triage inbox.

If runtime automation creation is unavailable, create this manually from
`docs/automations/daily-doc-staleness-triage.prompt.md`.
""",
    )
    _upsert_marked_section(Path("AGENTS.md"), "stage5eg", _agents_section())
    _upsert_marked_section(Path("ChatGPT-ContextFile.md"), "stage5eg", _chatgpt_section())
    _upsert_marked_section(Path("STATUS.md"), "stage5eg", _status_section())
    _upsert_marked_section(Path("README.md"), "stage5eg", _readme_section())
    _upsert_marked_section(Path("ROADMAP.md"), "stage5eg", _roadmap_section())
    _upsert_marked_section(Path("docs/roadmap/staged-plan.md"), "stage5eg", _staged_plan_section())
    _upsert_marked_section(Path("docs/onboarding/source-of-truth-map.md"), "stage5eg", _source_truth_section())
    _upsert_marked_section(Path("docs/onboarding/operational-file-map.md"), "stage5eg", _operational_map_section())
    _upsert_marked_section(Path("docs/reference/token-block-cli.md"), "stage5eg", _cli_doc_section())
    _upsert_marked_section(TEMPLATE_DIR / "codex-plan-mode-prompt-template.md", "stage5eg", _plan_template_section())
    _upsert_marked_section(TEMPLATE_DIR / "codex-closeout-template.md", "stage5eg", _closeout_template_section())
    _write_text(DEV_LOG_PATH, _dev_log())
    _write_text(RESEARCH_LOG_PATH, _research_log())


def _update_current_stage_state() -> None:
    state = read_yaml(CURRENT_STAGE_STATE_PATH)
    state.update(
        {
            "stage_id": STAGE_ID,
            "stage_title": STAGE_TITLE,
            "prompt_type": PROMPT_TYPE,
            "metadata_only": True,
            "reviewability_stage": True,
            "number_fact_review_batch_stage": False,
            "puzzle_execution_allowed": False,
            "status": "complete",
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": "codex_plan_mode_source_lock_addendum",
            "stage5ef_recommended_stage5eg_number_fact_batch_006": True,
            "operator_inserted_doc_staleness_guardian_stage_before_lag5": True,
            "previous_unexecuted_lag5_prompt_superseded_by_doc_guardian_stage": True,
            "lag5_source_lock_deferred_to_stage5eh": True,
            "number_fact_review_batch_006_deferred_to_stage5ei": True,
            "project_hooks_declared_now": True,
            "active_hooks_effective_now": False,
            "blocking_hooks_effective_now": False,
            **FALSE_GUARDRAILS,
        }
    )
    write_yaml(CURRENT_STAGE_STATE_PATH, state)


def _update_stage5ah_source_of_truth() -> None:
    payload = read_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "latest_completed_stage_after_this_stage": STAGE_TITLE,
            "next_stage_after_this_stage": NEXT_STAGE_TITLE,
            "latest_previous_stage": PREVIOUS_STAGE_TITLE,
            "expected_next_stage_prefix": "Stage 5EH",
            "latest_completed_stage_prefix": "Stage 5EG",
            "expected_latest_after_stage5ah": STAGE_TITLE,
            "expected_next_after_stage5ah": NEXT_STAGE_TITLE,
            "current_stage_state_authoritative": True,
            "historical_sections_may_retain_old_stage_claims_if_clearly_historical": True,
        }
    )
    write_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH, payload)


def _update_current_mirrors() -> None:
    replacements_by_path: dict[Path, dict[str, str]] = {
        Path("AGENTS.md"): {
            "Current completed stage: Stage 5EF - Plan-mode current-truth ledger and drift-audit foundation.": (
                f"Current completed stage: {STAGE_TITLE}."
            ),
            "Current work: Stage 5EG - Source-lock number-fact review batch 006, without execution.": (
                f"Current work: {NEXT_STAGE_TITLE}. Stage 5EG inserted deterministic doc-staleness guardians before "
                "Lag5 source-lock and the previously deferred number-fact review batch 006."
            ),
        },
        CHATGPT_CONTEXT_PATH: {
            "Current completed stage: Stage 5EF - Plan-mode current-truth ledger and drift-audit foundation.": (
                f"Current completed stage: {STAGE_TITLE}."
            ),
            "Current work after Stage 5EF: Stage 5EG - Source-lock number-fact review batch 006, without execution.": (
                f"Current work after Stage 5EG: {NEXT_STAGE_TITLE}."
            ),
            "Stage 5EF inserted anti-drift/current-truth infrastructure before the previously routed batch 006, made `data/project-state/current-stage-state.yaml` authoritative, added deterministic context-pack and report-only automation templates, kept hooks/automations/skills inactive, and deferred batch 006 to Stage 5EG.": (
                "Stage 5EF inserted anti-drift/current-truth infrastructure before the previously routed batch 006, made `data/project-state/current-stage-state.yaml` authoritative, added deterministic context-pack and report-only automation templates, kept hooks/automations/skills inactive, and deferred batch 006. Stage 5EG then added the deterministic stale-current scanner, declared project hooks, read-only agents, and daily report-only drift-audit setup; Lag5 is Stage 5EH and batch 006 is Stage 5EI."
            ),
        },
        Path("ROADMAP.md"): {
            "Current next prompt: Stage 5EF - Source-lock number-fact review batch 006, without execution.": (
                f"Current next prompt: {NEXT_STAGE_TITLE}."
            ),
            "Stage 5EE is complete as the fifth Source Browser number-fact review batch. It reviewed 20 selected source-register/music-metadata/Fandom-crosswalk/residual NumberFacts source-lock entries and added 25 review-only NumberFactCard overlays while preserving Stage 5ED overlays and Stage 5EB's 10-worker validation policy and authorizing no source rewrite, new source-lock evidence, target selection, byte generation, execution, CUDA, scoring, benchmark, website expansion, or solve claim.": (
                "Stage 5EG is complete as deterministic doc-staleness guardian infrastructure. It adds a tracked-file stale-current scanner, declared project Stop hook, read-only closeout agents, and daily report-only automation setup while authorizing no source rewrite, new source-lock evidence, target selection, byte generation, execution, CUDA, scoring, benchmark, website expansion, or solve claim."
            ),
            "Stage 5EE number-fact review batch 005 is complete. It keeps the reviewed facts as Source Browser overlays only, keeps historical source-lock records immutable, preserves the 10-worker/full-parallel validation policy, and leaves all no-active/no-byte/no-execution gates closed.": (
                "Stage 5EG doc-staleness guardian work is complete. It keeps `data/project-state/current-stage-state.yaml` authoritative, treats broad Markdown as mirrors or historical evidence, and leaves all no-active/no-byte/no-execution gates closed."
            ),
            "The next recommended prompt is Stage 5EF - Source-lock number-fact review batch 006, without execution.": (
                f"The next recommended prompt is {NEXT_STAGE_TITLE}."
            ),
        },
        Path("STATUS.md"): {
            "Stage 5EF plan-mode current-truth ledger and drift-audit foundation is complete.": (
                f"{STAGE_TITLE} is complete."
            ),
            "Next recommended prompt: Stage 5EG - Source-lock number-fact review batch 006, without execution. Public website expansion remains deferred to a future review-gated project.": (
                f"Next recommended prompt: {NEXT_STAGE_TITLE}. Public website expansion remains deferred to a future review-gated project."
            ),
            "## Completed in Stage 5EF": "## Completed in Stage 5EG",
            "Stage 5EF inserts anti-drift/current-truth infrastructure before the previously routed number-fact review batch 006. It makes `data/project-state/current-stage-state.yaml` the authoritative current-stage truth, classifies broad Markdown docs as mirrors or historical evidence, adds deterministic context-pack templates, report-only automation templates, inactive advisory-hook policy, skill-readiness deferral, focused validators, and ignored `codex-output` handoff files.": (
                "Stage 5EG adds deterministic post-edit doc-staleness guardians after Stage 5EF. It scans tracked text-like files for stale latest/current/next-stage claims, declares project-local Codex hooks that run deterministic commands, creates read-only closeout auditor agents, and creates daily report-only automation setup material."
            ),
            "Stage 5EF does not add source-lock evidence, number-fact overlays, direct source-record backfill, target or pivot selection, route extraction, byte-stream generation, execution, CUDA/scoring/benchmark work, website expansion, canonical corpus activation, page-boundary finalisation, or solve claims.": (
                "Stage 5EG does not add source-lock evidence, number-fact overlays, direct source-record backfill, target or pivot selection, Lag5 source-lock, route extraction, byte-stream generation, execution, CUDA/scoring/benchmark work, website expansion, canonical corpus activation, page-boundary finalisation, or solve claims."
            ),
        },
        Path("docs/roadmap/staged-plan.md"): {
            "- Latest completed stage: Stage 5EF - Plan-mode current-truth ledger and drift-audit foundation.": (
                f"- Latest completed stage: {STAGE_TITLE}."
            ),
            "- Current planning focus: Stage 5EG - Source-lock number-fact review batch 006, without execution.": (
                f"- Current planning focus: {NEXT_STAGE_TITLE}."
            ),
        },
        Path("README.md"): {
            "- Next: Stage 5EG - Source-lock number-fact review batch 006, without execution.": (
                f"- Next: {NEXT_STAGE_TITLE}."
            ),
        },
        Path("docs/onboarding/deep-research-handoff-map.md"): {
            "Stage 5DG selects Stage 5DH assistant/operator review as the next prompt, with Deep Research optional rather than required.": (
                "Historical Stage 5DG handoff: at the time of Stage 5DG, Stage 5DG selected Stage 5DH assistant/operator review as the next prompt, with Deep Research optional rather than required."
            ),
        },
    }
    for path, replacements in replacements_by_path.items():
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        _write_text(path, text)


def _update_stage_summary_records() -> None:
    payload = read_yaml(STAGE_SUMMARY_RECORDS_PATH)
    records = payload if isinstance(payload, list) else payload.get("records", [])
    records = [record for record in records if record.get("stage_id") != STAGE_ID]
    records.append(
        {
            "record_type": "stage_summary_record",
            "stage_id": STAGE_ID,
            "title": STAGE_TITLE,
            "status": "complete",
            "category": "metadata_tooling",
            "summary": "Added deterministic stale-current-claim scanning, declared project hooks, read-only auditor agents, and daily report-only automation setup.",
            "key_outputs": [
                "Tracked-file stale-current scanner added with strict errors for current mirrors, operating context, and onboarding stale claims.",
                "Known docs/onboarding/start-here.md stale current/latest claims repaired as regression fixture.",
                "Project-local .codex config, hooks, and read-only custom agents declared but not effective until operator trust.",
                "Lag5 source-lock deferred to Stage 5EH and number-fact review batch 006 deferred to Stage 5EI.",
            ],
            "result_status": "metadata_tooling_complete",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": "No source-lock evidence, overlays, route extraction, byte streams, execution, CUDA, scoring, benchmarks, or solve claim.",
        }
    )
    if isinstance(payload, list):
        write_yaml(STAGE_SUMMARY_RECORDS_PATH, records)
    else:
        payload["records"] = records
        write_yaml(STAGE_SUMMARY_RECORDS_PATH, payload)


def _update_operational_file_map() -> None:
    payload = read_yaml(OPERATIONAL_FILE_MAP_PATH)
    records = payload.get("records", []) if isinstance(payload, dict) else []
    additions = [str(path).replace("\\", "/") for path in [*DATA_PATHS.values(), *CODEX_FILES, *AUTOMATION_DOCS, DEV_LOG_PATH, RESEARCH_LOG_PATH]]
    addition_set = set(additions)
    records = [record for record in records if record.get("path") not in addition_set]
    for path in additions:
        is_data = path.startswith("data/")
        is_log = path.startswith("docs/development-logs/") or path.startswith("research-log/")
        records.append(
            {
                "path": path,
                "category": "historical_log" if is_log else ("active_data_record" if is_data else "policy_doc"),
                "purpose": "Stage 5EG doc-staleness guardian record, config, hook, agent, automation doc, or log.",
                "source_of_truth_rank": 2 if is_data else 3,
                "last_meaningful_update_stage": STAGE_ID,
                "expected_update_frequency": "stage_specific",
                "mutable_or_reference_only": "reference_only" if is_log else "mutable",
                "mirror_or_generated_relationships": "Stage 5EG source record or focused policy mirror; current-stage-state remains authoritative.",
                "staleness_check_level": "historical" if is_log else "reference_only",
                "owner_context": "codex_agent",
                "notes": "Added by Stage 5EG deterministic stale-current-claim guard.",
            }
        )
    payload["records"] = records
    write_yaml(OPERATIONAL_FILE_MAP_PATH, payload)


def _write_codex_output_handoff() -> None:
    _write_text(
        CODEX_OUTPUT_DIR / "stage5eg-codex-completion.md",
        f"""# Stage 5EG Codex Completion

Final commit: pending until commit.
Origin/main commit: pending until push.
GitHub issue: pending.
CI run/status: pending.
Stale-current scanner command: pending validation.
Custom agents created: 3.
Hooks effective now: false; awaiting operator trust.
Automation outcome: pending runtime creation/update attempt.
Recommended next stage: {NEXT_STAGE_ID} - {NEXT_STAGE_TITLE}.

This file is ignored and must not be committed.
""",
    )


def _agents_section() -> str:
    return f"""## Stage 5EG Doc-Staleness Guard

- Current completed stage: {STAGE_TITLE}.
- Current work: {NEXT_STAGE_TITLE}.
- Future closeout must run or explicitly report `python -m libreprimus.cli consistency audit-stale-current-claims --strict`.
- Project `.codex` hooks are declared only; they are not effective until operator trust.
- Read-only custom agents are available for explicit closeout review, but hooks use deterministic scanner commands, not agents.
- Stage 5EG creates no source-lock evidence, number-fact overlays, route extraction, byte streams, execution, CUDA, scoring, benchmarks, website expansion, or solve claim.
"""


def _chatgpt_section() -> str:
    return f"""## Stage 5EG Current Context

Latest completed stage: {STAGE_TITLE}.

Current planning focus: {NEXT_STAGE_TITLE}.

Stage 5EG supersedes the unexecuted Lag5 Stage 5EG prompt. Lag5 source-lock is deferred to Stage 5EH; ordinary number-fact review batch 006 is deferred to Stage 5EI.
"""


def _status_section() -> str:
    return f"""## Stage 5EG Status

Latest completed stage: {STAGE_TITLE}.

Recommended next stage: {NEXT_STAGE_TITLE}.

Doc-staleness guard: strict tracked-file stale-current scanner plus declared Stop hook, read-only closeout agents, and daily report-only automation setup.
"""


def _readme_section() -> str:
    return f"""## Stage 5EG Current Status

The authoritative current-stage registry is `data/project-state/current-stage-state.yaml`.

Latest completed: {STAGE_TITLE}.

Next routed: {NEXT_STAGE_TITLE}.
"""


def _roadmap_section() -> str:
    return f"""## Stage 5EG Routing

- Complete: {STAGE_TITLE}.
- Next: {NEXT_STAGE_TITLE}.
- Then: {NORMAL_BATCH006_STAGE_TITLE}.
"""


def _staged_plan_section() -> str:
    return """## Stage 5EG - Post-Edit Doc-Staleness Guardians

Status: complete.

Stage 5EG adds deterministic stale-current-claim scanning, project-local declared hooks, read-only auditor-agent definitions, and daily report-only automation setup. Lag5 source-lock is deferred to Stage 5EH. Number-fact review batch 006 is deferred to Stage 5EI.
"""


def _source_truth_section() -> str:
    return """## Stage 5EG Source-Of-Truth Note

`data/project-state/current-stage-state.yaml` is the authoritative current-stage truth. The Stage 5EG scanner audits tracked text-like files for stale current/latest/next-stage claims.
"""


def _operational_map_section() -> str:
    return """## Stage 5EG Operational Map Note

Stage 5EG adds `.codex/` project-local hook and agent declarations plus daily doc-staleness automation docs. Hooks are declared only until operator trust.
"""


def _cli_doc_section() -> str:
    return """## Stage 5EG Commands

- `python -m libreprimus.cli token-block build-stage5eg`
- `python -m libreprimus.cli token-block validate-stage5eg`
- `python -m libreprimus.cli token-block stage5eg-summary`
- `python -m libreprimus.cli consistency audit-stale-current-claims --strict`
"""


def _plan_template_section() -> str:
    return """## Stage 5EG Plan-Mode Closeout Guard

Plans that edit docs should include a deterministic stale-current-claim scanner step before final validation.
"""


def _closeout_template_section() -> str:
    return """## Doc-Staleness Guard

- stale-current scanner command:
- result:
- findings count:
- current mirror drift count:
- onboarding stale-current finding count:
- suppressions used:
- generated report path, if any:
"""


def _dev_log() -> str:
    return """# Stage 5EG Development Log

Stage 5EG implements deterministic post-edit doc-staleness protection. It is metadata/tooling only and keeps all execution/source-lock/overlay guardrails closed.
"""


def _research_log() -> str:
    return f"""# Stage 5EG Doc-Staleness Guardian Summary

Stage 5EG adds a tracked-file stale-current scanner, declared project hooks, read-only custom agents, and a daily report-only automation package. Next: {NEXT_STAGE_TITLE}.
"""


def _required_paths() -> list[Path]:
    return list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values()) + [
        CURRENT_STAGE_STATE_PATH,
        CHATGPT_CONTEXT_PATH,
        OPERATIONAL_FILE_MAP_PATH,
        STAGE_SUMMARY_RECORDS_PATH,
        DOC_STALENESS_SOURCE_OF_TRUTH_PATH,
        *CODEX_FILES,
        *AUTOMATION_DOCS,
        DEV_LOG_PATH,
        RESEARCH_LOG_PATH,
    ]


def _read_record(key: str) -> dict[str, Any]:
    return read_yaml(DATA_PATHS[key])


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
