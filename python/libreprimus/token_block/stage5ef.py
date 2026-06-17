"""Stage 5EF current-truth and drift-audit foundation.

Stage 5EF is metadata/tooling only. It inserts a compact anti-drift
foundation before the previously routed number-fact review batch 006 and keeps
all puzzle/source-lock/execution surfaces closed.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import (
    path_canonicalization_report,
    source_browser_summary,
    validate_path_canonicalization,
    validate_source_index,
)
from libreprimus.token_block.models import read_yaml, write_json, write_yaml

STAGE_ID = "stage-5ef"
STAGE_TOKEN = "stage5ef"
STAGE_TITLE = "Stage 5EF - Plan-mode current-truth ledger and drift-audit foundation"
PROMPT_TYPE = "codex_plan_mode_metadata_tooling_implementation"
PREVIOUS_STAGE_ID = "stage-5ee"
PREVIOUS_STAGE_TITLE = (
    "Stage 5EE - Source-lock number-fact review batch 005, source-register / "
    "music-metadata / fandom-crosswalk / residual NumberFacts enrichment overlays, "
    "without execution"
)
PREVIOUS_STAGE_COMMIT = "e1d2229ed7400d9152b96310f6cf6b2cce09c8bf"
PREVIOUS_STAGE_CI_RUN = 27401498707
PREVIOUS_STAGE_CI_STATUS = "passed"
NEXT_STAGE_ID = "stage-5eg"
NEXT_STAGE_TITLE = "Stage 5EG - Source-lock number-fact review batch 006, without execution"
PARALLEL_WORKER_CAP = 10
LOCAL_PARALLEL_DEFAULT_WORKERS = 10
LOCAL_PARALLEL_DEFAULT_PYTEST_WORKERS = 10

PROJECT_STATE_DIR = Path("data/project-state")
TOKEN_BLOCK_DIR = Path("data/token-block")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
RESEARCH_DIR = Path("data/research")
CODEX_OUTPUT_DIR = Path("codex-output")
CONTEXT_PACK_DIR = Path("docs/context-packs")
CODEX_DOC_DIR = Path("docs/codex")
AUTOMATION_DOC_DIR = Path("docs/automations")
TEMPLATE_DIR = Path("docs/templates")

CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
CHATGPT_CONTEXT_PATH = Path("ChatGPT-ContextFile.md")
OPERATIONAL_FILE_MAP_PATH = PROJECT_STATE_DIR / "operational-file-map.yaml"
STAGE_SUMMARY_RECORDS_PATH = RESEARCH_DIR / "stage-summary-records-v0.yaml"
DOC_STALENESS_SOURCE_OF_TRUTH_PATH = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
DEV_LOG_PATH = Path("docs/development-logs/2026-06-12-stage-5ef-current-truth-doc-drift-context-pack-foundation.md")
RESEARCH_LOG_PATH = Path("research-log/2026-06-12-stage5ef-next-stage-decision-summary.md")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5ef-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5ef-next-stage-decision.yaml",
    "stage5ee_preservation": PROJECT_STATE_DIR / "stage5ef-stage5ee-preservation.yaml",
    "current_truth_authority_policy": PROJECT_STATE_DIR / "stage5ef-current-truth-authority-policy.yaml",
    "doc_update_policy_ledger": PROJECT_STATE_DIR / "stage5ef-doc-update-policy-ledger.yaml",
    "context_pack_registry": PROJECT_STATE_DIR / "stage5ef-context-pack-registry.yaml",
    "plan_mode_policy": PROJECT_STATE_DIR / "stage5ef-plan-mode-codex-run-policy.yaml",
    "drift_audit_policy": PROJECT_STATE_DIR / "stage5ef-drift-audit-policy.yaml",
    "automation_audit_template_registry": PROJECT_STATE_DIR
    / "stage5ef-automation-audit-template-registry.yaml",
    "advisory_hook_policy": PROJECT_STATE_DIR / "stage5ef-advisory-hook-policy.yaml",
    "skill_readiness_policy": PROJECT_STATE_DIR / "stage5ef-skill-readiness-policy.yaml",
    "doc_staleness_rule_repair": PROJECT_STATE_DIR / "stage5ef-doc-staleness-rule-repair.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5ef-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5ef-reviewability-gap-register.yaml",
    "source_browser_loadability": PROJECT_STATE_DIR / "stage5ef-source-browser-loadability-summary.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage5ef-chatgpt-context-update-summary.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5ef-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5ef-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5ef-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage5ef-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage5ef-no-execution-transition-gate.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5ef-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5ef-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5ef-raw-source-noncommit-proof.yaml",
}

DATA_PATHS: dict[str, Path] = {
    **PROJECT_STATE_PATHS,
    **TOKEN_PATHS,
    **SOURCE_HARVESTER_PATHS,
}

SCHEMA_PATHS: dict[str, Path] = {
    key: Path(f"schemas/project-state/stage5ef-{key.replace('_', '-')}-v0.schema.json")
    for key in PROJECT_STATE_PATHS
}
SCHEMA_PATHS.update(
    {
        key: Path(f"schemas/token-block/stage5ef-{key.replace('_', '-')}-v0.schema.json")
        for key in TOKEN_PATHS
    }
)
SCHEMA_PATHS.update(
    {
        key: Path(f"schemas/source-harvester/stage5ef-{key.replace('_', '-')}-v0.schema.json")
        for key in SOURCE_HARVESTER_PATHS
    }
)

CONTEXT_PACKS: list[dict[str, str]] = [
    {
        "pack_id": "number_fact_enrichment",
        "path": "docs/context-packs/context-pack-number-fact-enrichment.md",
        "purpose": "Prepare bounded future number-fact review batches without executing them.",
    },
    {
        "pack_id": "source_lock_addendum",
        "path": "docs/context-packs/context-pack-source-lock-addendum.md",
        "purpose": "Collect source-lock addenda without rewriting prior evidence.",
    },
    {
        "pack_id": "validation_repair",
        "path": "docs/context-packs/context-pack-validation-repair.md",
        "purpose": "Scope focused validator repair without broad doc churn.",
    },
    {
        "pack_id": "target_priority",
        "path": "docs/context-packs/context-pack-target-priority.md",
        "purpose": "Review target-priority proposals while keeping selection blocked.",
    },
    {
        "pack_id": "experiment_design",
        "path": "docs/context-packs/context-pack-experiment-design.md",
        "purpose": "Draft raw-data-free experiment-design scaffolds without execution.",
    },
    {
        "pack_id": "doc_drift",
        "path": "docs/context-packs/context-pack-doc-drift.md",
        "purpose": "Audit current-truth mirror drift without changing historical evidence.",
    },
]

AUTOMATION_TEMPLATES: list[dict[str, str]] = [
    {
        "template_id": "doc_drift_audit",
        "path": "docs/automations/doc-drift-audit.prompt.md",
        "purpose": "Report current-truth mirror drift only.",
    },
    {
        "template_id": "source_browser_path_audit",
        "path": "docs/automations/source-browser-path-audit.prompt.md",
        "purpose": "Report Source Browser path issues only.",
    },
    {
        "template_id": "completion_handoff_audit",
        "path": "docs/automations/completion-handoff-audit.prompt.md",
        "purpose": "Report missing completion-handoff fields only.",
    },
    {
        "template_id": "context_pack_freshness_audit",
        "path": "docs/automations/context-pack-freshness-audit.prompt.md",
        "purpose": "Report context-pack freshness gaps only.",
    },
    {
        "template_id": "guardrail_audit",
        "path": "docs/automations/guardrail-audit.prompt.md",
        "purpose": "Report closed/open guardrail states only.",
    },
]

TEMPLATE_PATHS: dict[str, Path] = {
    "plan_mode_prompt": TEMPLATE_DIR / "codex-plan-mode-prompt-template.md",
    "closeout": TEMPLATE_DIR / "codex-closeout-template.md",
}

FALSE_GUARDRAILS = {
    "historical_source_lock_records_rewritten": False,
    "new_source_lock_evidence_added_now": False,
    "source_lock_evidence_updated_now": False,
    "number_fact_enrichment_overlays_added_now": False,
    "number_fact_backfill_performed_now": False,
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
    "active_hooks_created_now": False,
    "blocking_hooks_enabled_now": False,
    "codex_automations_scheduled_now": False,
    "automation_auto_commit_enabled": False,
    "repo_local_skills_installed_now": False,
}


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: list[str]
    counts: dict[str, Any]

    @property
    def validation_error_count(self) -> int:
        return len(self.errors)

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5ef"]
        for key, value in self.counts.items():
            lines.append(f"{key}={value}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5ef() -> dict[str, Any]:
    """Build deterministic Stage 5EF records, schemas, docs, and templates."""

    source_browser = _source_browser_loadability_record()
    records = _records(source_browser)
    _write_schemas()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)
    _write_templates_and_docs(records)
    _update_current_stage_state()
    _update_stage5ah_source_of_truth()
    _update_stage_summary_records()
    _update_operational_file_map()
    _update_current_mirrors()
    _write_codex_output_handoffs()
    return records


def validate_stage5ef() -> ValidationResult:
    validators = [
        validate_required_paths,
        validate_schema_files,
        validate_stage5ef_schema_payloads,
        validate_stage5ef_stage5ee_preservation,
        validate_stage5ef_current_truth,
        validate_stage5ef_doc_update_policy,
        validate_stage5ef_context_packs,
        validate_stage5ef_plan_mode_policy,
        validate_stage5ef_drift_audit_policy,
        validate_stage5ef_automation_templates,
        validate_stage5ef_advisory_hooks,
        validate_stage5ef_skill_readiness,
        validate_stage5ef_doc_staleness_rule_repair,
        validate_stage5ef_source_browser_loadability,
        validate_stage5ef_sidecar_gates,
        validate_stage5ef_handoff_continuity,
        validate_stage5ef_credential_redaction_policy,
        validate_stage5ef_governance_scope,
    ]
    return _combine(validators)


def validate_required_paths() -> ValidationResult:
    errors = [f"missing required file: {path}" for path in _required_paths() if not path.exists()]
    return _result(errors, required_file_count=len(_required_paths()))


def validate_schema_files() -> ValidationResult:
    errors = [f"missing schema file: {path}" for path in SCHEMA_PATHS.values() if not path.exists()]
    for path in SCHEMA_PATHS.values():
        if path.exists():
            try:
                Draft202012Validator.check_schema(read_yaml(path))
            except Exception as exc:  # pragma: no cover - jsonschema gives varied exception types.
                errors.append(f"invalid schema {path}: {exc}")
    return _result(errors, schema_count=len(SCHEMA_PATHS))


def validate_stage5ef_schema_payloads() -> ValidationResult:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        schema_path = SCHEMA_PATHS[key]
        if not path.exists() or not schema_path.exists():
            continue
        try:
            Draft202012Validator(read_yaml(schema_path)).validate(read_yaml(path))
        except Exception as exc:
            errors.append(f"schema validation failed for {path}: {exc}")
    return _result(errors, validated_payload_count=len(DATA_PATHS))


def validate_stage5ef_stage5ee_preservation() -> ValidationResult:
    record = _read_record("stage5ee_preservation")
    errors = _false_guardrail_errors(record)
    if record.get("preserved_stage_id") != PREVIOUS_STAGE_ID:
        errors.append("Stage 5EE preservation record does not preserve Stage 5EE")
    if record.get("stage5ee_final_commit") != PREVIOUS_STAGE_COMMIT:
        errors.append("Stage 5EE preservation commit mismatch")
    if record.get("stage5ee_ci_status") != PREVIOUS_STAGE_CI_STATUS:
        errors.append("Stage 5EE CI status was not preserved as passed")
    return _result(errors, preserved_stage_id=record.get("preserved_stage_id"))


def validate_stage5ef_current_truth() -> ValidationResult:
    record = _read_record("current_truth_authority_policy")
    errors = _false_guardrail_errors(record)
    if record.get("authoritative_current_truth") != ["data/project-state/current-stage-state.yaml"]:
        errors.append("current-stage-state.yaml must be the only authoritative current truth")
    if "STATUS.md current-stage section" not in record.get("human_readable_current_mirrors", []):
        errors.append("STATUS current-stage mirror missing")
    if record.get("historical_sections_can_contain_old_next_stage_claims") is not True:
        errors.append("historical sections are not explicitly exempted")
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    current_pair = (current.get("latest_completed_stage_id"), current.get("recommended_next_stage_id"))
    later_stage_pairs = {
        ("stage-5eg", "stage-5eh"): Path("data/project-state/stage5eg-summary.yaml"),
        ("stage-5eh", "stage-5ei"): Path("data/project-state/stage5eh-summary.yaml"),
        ("stage-5ei", "stage-6"): Path("data/project-state/stage5ei-summary.yaml"),
        ("stage-6", "stage-6b"): Path("data/project-state/stage6-summary.yaml"),
        ("stage-6b", "stage-6c"): Path("data/project-state/stage6b-summary.yaml"),
        ("stage-6c", "stage-6d"): Path("data/project-state/stage6c-summary.yaml"),
        ("stage-6d", "stage-6e"): Path("data/project-state/stage6d-summary.yaml"),
        ("stage-6e", "stage-6f"): Path("data/project-state/stage6e-summary.yaml"),
        ("stage-6f", "stage-6g"): Path("data/project-state/stage6f-summary.yaml"),
    }
    if current_pair in later_stage_pairs and later_stage_pairs[current_pair].exists():
        return _result(errors, authority_count=len(record.get("authoritative_current_truth", [])))
    if current.get("latest_completed_stage_id") != STAGE_ID:
        errors.append("current-stage-state latest stage is not Stage 5EF")
    if current.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("current-stage-state next stage is not Stage 5EG")
    return _result(errors, authority_count=len(record.get("authoritative_current_truth", [])))


def validate_stage5ef_doc_update_policy() -> ValidationResult:
    record = _read_record("doc_update_policy_ledger")
    errors = _false_guardrail_errors(record)
    protected = {
        "CIPHER_CATALOG.md",
        "EXPERIMENTS.md",
        "RESULTS_SCHEMA.md",
        "CUDA_NOTES.md",
        "BENCHMARKS.md",
        "tutorials/**",
        "docs/wiki-source/**",
    }
    roles = {entry["path"]: entry for entry in record.get("doc_roles", [])}
    for path in protected:
        role = roles.get(path)
        if role is None or role.get("stage5ef_default_update_allowed") is not False:
            errors.append(f"protected broad doc is not fail-closed in policy: {path}")
    if record.get("repo_wide_markdown_frontmatter_migration_performed") is not False:
        errors.append("repo-wide Markdown frontmatter migration must remain false")
    return _result(errors, doc_role_count=len(roles))


def validate_stage5ef_context_packs() -> ValidationResult:
    record = _read_record("context_pack_registry")
    errors = _false_guardrail_errors(record)
    if record.get("context_pack_template_count") != len(CONTEXT_PACKS):
        errors.append("context-pack count mismatch")
    volatile_markers = ["generated_at:", "timestamp:", "O:\\", "worktree dirt", "git status --short output"]
    for pack in record.get("context_packs", []):
        path = Path(pack["path"])
        if not path.exists():
            errors.append(f"missing context-pack template: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        text_lower = text.lower()
        for marker in volatile_markers:
            if marker in text:
                errors.append(f"context-pack template contains volatile marker {marker}: {path}")
        for required in [STAGE_ID, NEXT_STAGE_ID, "current-stage-state.yaml"]:
            if required not in text:
                errors.append(f"context-pack template lacks {required}: {path}")
        if "guardrails" not in text_lower:
            errors.append(f"context-pack template lacks guardrails: {path}")
    return _result(errors, context_pack_count=record.get("context_pack_template_count"))


def validate_stage5ef_plan_mode_policy() -> ValidationResult:
    record = _read_record("plan_mode_policy")
    errors = _false_guardrail_errors(record)
    for field in [
        "plan_mode_used_for_stage5ef",
        "plan_review_performed_before_editing",
        "plan_amendment_applied_before_editing",
        "plan_mode_policy_created",
    ]:
        if record.get(field) is not True:
            errors.append(f"{field} must be true")
    if record.get("plan_deviation_count") != 0:
        errors.append("plan_deviation_count must remain zero unless a real deviation is recorded")
    if record.get("full_serial_pytest_required_for_normal_completion") is not False:
        errors.append("full serial pytest must not be normal completion policy")
    return _result(errors, plan_mode_policy_created=record.get("plan_mode_policy_created"))


def validate_stage5ef_drift_audit_policy() -> ValidationResult:
    record = _read_record("drift_audit_policy")
    errors = _false_guardrail_errors(record)
    if record.get("audit_default_mode") != "report_only_no_fix":
        errors.append("drift audits must default to report-only")
    if record.get("historical_sections_are_evidence_only") is not True:
        errors.append("historical sections must remain evidence-only")
    if record.get("generated_audit_outputs_committed") is not False:
        errors.append("generated drift audit outputs must not be committed")
    return _result(errors, drift_audit_policy_created=True)


def validate_stage5ef_automation_templates() -> ValidationResult:
    record = _read_record("automation_audit_template_registry")
    errors = _false_guardrail_errors(record)
    for template in record.get("automation_templates", []):
        path = Path(template["path"])
        if not path.exists():
            errors.append(f"missing automation template: {path}")
            continue
        text = path.read_text(encoding="utf-8").lower()
        for required in ["report-only", "do not auto-commit", "do not execute puzzle"]:
            if required not in text:
                errors.append(f"automation template lacks '{required}': {path}")
    return _result(errors, automation_template_count=len(record.get("automation_templates", [])))


def validate_stage5ef_advisory_hooks() -> ValidationResult:
    record = _read_record("advisory_hook_policy")
    errors = _false_guardrail_errors(record)
    if record.get("active_hooks_created_now") is not False:
        errors.append("active hooks must not be created")
    if record.get("blocking_hooks_enabled_now") is not False:
        errors.append("blocking hooks must not be enabled")
    active_hook_paths = [Path(".codex/hooks.json"), Path(".codex/hooks.yaml"), Path(".codex/hooks")]
    stage5eg_policy_path = Path("data/project-state/stage5eg-stop-hook-policy.yaml")
    stage5eg_declared_hooks = False
    if stage5eg_policy_path.exists():
        policy = read_yaml(stage5eg_policy_path)
        stage5eg_declared_hooks = (
            policy.get("project_hooks_declared_now") is True
            and policy.get("active_hooks_effective_now") is False
            and policy.get("hooks_use_deterministic_scanner_now") is True
        )
    if any(path.exists() for path in active_hook_paths) and not stage5eg_declared_hooks:
        errors.append("active .codex hooks configuration exists")
    return _result(errors, active_hooks_created_now=record.get("active_hooks_created_now"))


def validate_stage5ef_skill_readiness() -> ValidationResult:
    record = _read_record("skill_readiness_policy")
    errors = _false_guardrail_errors(record)
    if record.get("repo_local_skills_installed_now") is not False:
        errors.append("repo-local skills must not be installed")
    if record.get("skills_deferred_because_agents_skills_not_repo_convention") is not True:
        errors.append("skills must be explicitly deferred")
    if Path(".agents/skills").exists():
        errors.append(".agents/skills must not be introduced by Stage 5EF")
    return _result(errors, repo_local_skills_installed_now=record.get("repo_local_skills_installed_now"))


def validate_stage5ef_doc_staleness_rule_repair() -> ValidationResult:
    record = _read_record("doc_staleness_rule_repair")
    errors = _false_guardrail_errors(record)
    if record.get("validators_require_broad_historical_updates") is not False:
        errors.append("validators must not require broad historical updates")
    if record.get("current_stage_state_authoritative") is not True:
        errors.append("current-stage-state authority not recorded")
    return _result(errors, doc_staleness_rule_repair=True)


def validate_stage5ef_source_browser_loadability() -> ValidationResult:
    record = _read_record("source_browser_loadability")
    errors = _false_guardrail_errors(record)
    if record.get("source_browser_validation_error_count") != 0:
        errors.append("Source Browser validation errors are present")
    if record.get("source_browser_entries_loaded", 0) < 1:
        errors.append("Source Browser entries were not loaded")
    return _result(
        errors,
        source_browser_entries_loaded=record.get("source_browser_entries_loaded"),
        source_browser_validation_error_count=record.get("source_browser_validation_error_count"),
    )


def validate_stage5ef_sidecar_gates() -> ValidationResult:
    errors: list[str] = []
    for key in [
        "stage5bd_preservation",
        "active_lineage_preservation",
        "no_active_ingestion_proof",
        "no_byte_stream_transition_gate",
        "no_execution_transition_gate",
    ]:
        record = _read_record(key)
        errors.extend(_false_guardrail_errors(record))
        if record.get("gate_closed") is not True:
            errors.append(f"{key} does not record gate_closed=true")
    return _result(errors, sidecar_gate_records=5)


def validate_stage5ef_handoff_continuity() -> ValidationResult:
    record = _read_record("codex_handoff_policy")
    errors = _false_guardrail_errors(record)
    if record.get("codex_output_committed") is not False:
        errors.append("codex-output handoff files must not be committed")
    handoff_paths = [
        Path("codex-output/stage5ef-codex-plan.md"),
        Path("codex-output/stage5ef-codex-completion.md"),
    ]
    existing = sum(1 for path in handoff_paths if path.exists())
    return _result(errors, handoff_files_expected=2, ignored_handoff_files_present=existing)


def validate_stage5ef_credential_redaction_policy() -> ValidationResult:
    record = _read_record("credential_redaction_policy_preservation")
    errors = _false_guardrail_errors(record)
    if record.get("credentials_or_secrets_recorded") is not False:
        errors.append("credential preservation record must not contain secrets")
    if record.get("credential_redaction_policy_preserved") is not True:
        errors.append("credential redaction policy was not preserved")
    return _result(errors, credential_redaction_policy_preserved=True)


def validate_stage5ef_governance_scope() -> ValidationResult:
    summary = _read_record("summary")
    errors = _false_guardrail_errors(summary)
    for field in [
        "new_source_lock_evidence_added_now",
        "number_fact_enrichment_overlays_added_now",
        "target_priority_decision_created_now",
        "route_extraction_performed_now",
        "real_byte_stream_generated",
        "execution_performed",
        "cuda_execution_performed",
        "solve_claim",
    ]:
        if summary.get(field) is not False:
            errors.append(f"{field} must remain false")
    if summary.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("Stage 5EF must route to Stage 5EG")
    return _result(errors, recommended_next_stage_id=summary.get("recommended_next_stage_id"))


def stage5ef_summary_text() -> str:
    summary = _read_record("summary")
    return "\n".join(
        [
            f"stage_id={summary.get('stage_id')}",
            f"status={summary.get('status')}",
            f"plan_mode_used_for_stage5ef={summary.get('plan_mode_used_for_stage5ef')}",
            f"context_pack_templates_committed={summary.get('context_pack_templates_committed')}",
            f"automation_template_count={summary.get('automation_template_count')}",
            f"active_hooks_created_now={summary.get('active_hooks_created_now')}",
            f"codex_automations_scheduled_now={summary.get('codex_automations_scheduled_now')}",
            f"repo_local_skills_installed_now={summary.get('repo_local_skills_installed_now')}",
            f"source_browser_entries_loaded={summary.get('source_browser_entries_loaded')}",
            f"source_browser_validation_error_count={summary.get('source_browser_validation_error_count')}",
            f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
            f"recommended_next_stage_title={summary.get('recommended_next_stage_title')}",
        ]
    )


def render_context_pack(pack_id: str) -> str:
    pack = next((item for item in CONTEXT_PACKS if item["pack_id"] == pack_id), None)
    if pack is None:
        raise ValueError(f"unknown Stage 5EF context pack: {pack_id}")
    return _context_pack_text(pack)


def build_doc_drift_audit_report() -> dict[str, Any]:
    policy = _read_record("doc_update_policy_ledger")
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    records = []
    for entry in policy.get("doc_roles", []):
        records.append(
            {
                "path": entry["path"],
                "doc_role": entry["doc_role"],
                "current_mirror": entry.get("current_mirror", False),
                "stage5ef_default_update_allowed": entry.get("stage5ef_default_update_allowed", False),
            }
        )
    return {
        "record_type": "stage5ef_doc_drift_audit_report",
        "stage_id": STAGE_ID,
        "status": "report_only_no_fix",
        "authoritative_current_stage_id": current.get("latest_completed_stage_id"),
        "recommended_next_stage_id": current.get("recommended_next_stage_id"),
        "doc_role_records": records,
        "doc_role_count": len(records),
        "fixes_applied": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
    }


def _records(source_browser: dict[str, Any]) -> dict[str, Any]:
    common = _common_fields()
    summary = {
        **common,
        "record_type": "stage5ef_summary",
        "schema": str(SCHEMA_PATHS["summary"]),
        "status": "complete",
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "plan_mode_used_for_stage5ef": True,
        "plan_review_performed_before_editing": True,
        "plan_amendment_applied_before_editing": True,
        "plan_mode_policy_created": True,
        "plan_deviation_count": 0,
        "plan_deviation_summary": [],
        "stage5ee_recommended_stage5ef_number_fact_batch_006": True,
        "operator_inserted_antidrift_stage_before_batch_006": True,
        "number_fact_review_batch_006_deferred_to_stage5eg": True,
        "current_truth_authority_policy_created": True,
        "doc_update_policy_ledger_created": True,
        "context_pack_registry_created": True,
        "context_pack_templates_committed": len(CONTEXT_PACKS),
        "automation_template_count": len(AUTOMATION_TEMPLATES),
        "automation_templates_report_only": True,
        "advisory_hook_policy_created": True,
        "skill_readiness_policy_created": True,
        "skills_deferred_because_agents_skills_not_repo_convention": True,
        "source_browser_entries_loaded": source_browser["source_browser_entries_loaded"],
        "source_browser_record_count": source_browser["source_browser_record_count"],
        "source_browser_validation_error_count": source_browser["source_browser_validation_error_count"],
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "local_parallel_default_workers": LOCAL_PARALLEL_DEFAULT_WORKERS,
        "local_parallel_default_pytest_workers": LOCAL_PARALLEL_DEFAULT_PYTEST_WORKERS,
        "old_8_worker_cap": False,
        "old_16_worker_default_reintroduced": False,
        "full_serial_pytest_required_for_normal_completion": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
    }
    records: dict[str, Any] = {
        "summary": summary,
        "next_stage_decision": _next_stage_decision(common),
        "stage5ee_preservation": _stage5ee_preservation(common),
        "current_truth_authority_policy": _current_truth_policy(common),
        "doc_update_policy_ledger": _doc_update_policy(common),
        "context_pack_registry": _context_pack_registry(common),
        "plan_mode_policy": _plan_mode_policy(common),
        "drift_audit_policy": _drift_audit_policy(common),
        "automation_audit_template_registry": _automation_registry(common),
        "advisory_hook_policy": _advisory_hook_policy(common),
        "skill_readiness_policy": _skill_readiness_policy(common),
        "doc_staleness_rule_repair": _doc_staleness_rule_repair(common),
        "reviewable_validation_evidence": _validation_evidence(common),
        "reviewability_gap_register": _reviewability_gap_register(common),
        "source_browser_loadability": {**common, "schema": str(SCHEMA_PATHS["source_browser_loadability"]), **source_browser},
        "chatgpt_context_update_summary": _chatgpt_context_summary(common),
        "stage5bd_preservation": _gate_record(common, "stage5bd_preservation", "stage5bd_run_plan_ids_preserved"),
        "active_lineage_preservation": _gate_record(common, "active_lineage_preservation", "active_lineage_preserved"),
        "no_active_ingestion_proof": _gate_record(common, "no_active_ingestion_proof", "active_ingestion_blocked"),
        "no_byte_stream_transition_gate": _gate_record(common, "no_byte_stream_transition_gate", "byte_stream_gate_closed"),
        "no_execution_transition_gate": _gate_record(common, "no_execution_transition_gate", "execution_gate_closed"),
        "codex_handoff_policy": _codex_handoff_policy(common),
        "credential_redaction_policy_preservation": _credential_redaction_policy(common),
        "raw_source_noncommit_proof": _raw_source_noncommit_proof(common),
    }
    return records


def _common_fields() -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "previous_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "no_solve_claim": True,
        "generated_outputs_committed": False,
        **FALSE_GUARDRAILS,
    }


def _next_stage_decision(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_next_stage_decision",
        "schema": str(SCHEMA_PATHS["next_stage_decision"]),
        "status": "complete",
        "stage5ee_recommended_stage5ef_number_fact_batch_006": True,
        "operator_inserted_antidrift_stage_before_batch_006": True,
        "number_fact_review_batch_006_deferred_to_stage5eg": True,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "number_fact_batch_006_execution_authorized": False,
    }


def _stage5ee_preservation(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_stage5ee_preservation",
        "schema": str(SCHEMA_PATHS["stage5ee_preservation"]),
        "status": "complete",
        "preserved_stage_id": PREVIOUS_STAGE_ID,
        "preserved_stage_title": PREVIOUS_STAGE_TITLE,
        "stage5ee_final_commit": PREVIOUS_STAGE_COMMIT,
        "stage5ee_ci_run": PREVIOUS_STAGE_CI_RUN,
        "stage5ee_ci_status": PREVIOUS_STAGE_CI_STATUS,
        "stage5ee_reviewed_entry_count": 20,
        "stage5ee_overlay_count": 25,
        "stage5ee_original_next_stage": "stage-5ef number-fact review batch 006",
        "stage5ee_original_next_route_preserved_as_historical": True,
    }


def _current_truth_policy(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_current_truth_authority_policy",
        "schema": str(SCHEMA_PATHS["current_truth_authority_policy"]),
        "status": "complete",
        "authoritative_current_truth": ["data/project-state/current-stage-state.yaml"],
        "high_priority_operating_context": ["AGENTS.md", "ChatGPT-ContextFile.md"],
        "human_readable_current_mirrors": [
            "STATUS.md current-stage section",
            "README.md current-status/current-stage section",
            "ROADMAP.md current-next-stage section",
            "docs/roadmap/staged-plan.md current section",
        ],
        "machine_maps_and_registries": [
            "data/project-state/operational-file-map.yaml",
            "data/research/stage-summary-records-v0.yaml",
            "data/project-state/stage5ah-doc-staleness-source-of-truth.yaml",
        ],
        "historical_evidence_only": [
            "docs/development-logs/**",
            "research-log/**",
            "historical Markdown sections",
            "ignored codex-output/**",
        ],
        "current_stage_state_authoritative": True,
        "human_readable_docs_are_mirrors_only": True,
        "historical_sections_can_contain_old_next_stage_claims": True,
        "validators_must_not_force_broad_historical_rewrites": True,
    }


def _doc_update_policy(common: dict[str, Any]) -> dict[str, Any]:
    def role(path: str, doc_role: str, allowed: bool, *, current_mirror: bool = False) -> dict[str, Any]:
        return {
            "path": path,
            "doc_role": doc_role,
            "current_mirror": current_mirror,
            "stage5ef_default_update_allowed": allowed,
            "update_policy": "focused_current_section_only" if allowed else "blocked_unless_focused_validator_requires",
        }

    doc_roles = [
        role("STATUS.md", "current_mirror", True, current_mirror=True),
        role("README.md", "current_mirror", True, current_mirror=True),
        role("ROADMAP.md", "current_mirror", True, current_mirror=True),
        role("docs/roadmap/staged-plan.md", "current_mirror", True, current_mirror=True),
        role("AGENTS.md", "operating_context", True),
        role("ChatGPT-ContextFile.md", "operating_context", True),
        role("TESTING.md", "command_doc", True),
        role("docs/reference/token-block-cli.md", "command_doc", True),
        role("docs/onboarding/source-of-truth-map.md", "machine_map_doc", True),
        role("docs/onboarding/operational-file-map.md", "machine_map_doc", True),
        role("CIPHER_CATALOG.md", "domain_doc", False),
        role("EXPERIMENTS.md", "domain_doc", False),
        role("RESULTS_SCHEMA.md", "domain_doc", False),
        role("CUDA_NOTES.md", "domain_doc", False),
        role("BENCHMARKS.md", "domain_doc", False),
        role("tutorials/**", "tutorial_mirror", False),
        role("docs/wiki-source/**", "wiki_mirror", False),
        role("docs/experiments/**", "historical_stage_evidence", False),
        role("docs/operator-console/source-browser-v0.md", "stage_specific_operator_console_doc", False),
        role("docs/onboarding/contributor-module-map.md", "module_map", False),
        role("docs/development-logs/**", "historical_log", False),
        role("research-log/**", "historical_log", False),
        role("codex-output/**", "ignored_handoff", False),
        role("experiments/results/**", "ignored_generated_output", False),
        role("third_party/**", "ignored_raw_or_cache", False),
        role("data/raw/**", "ignored_raw_or_cache", False),
    ]
    return {
        **common,
        "record_type": "stage5ef_doc_update_policy_ledger",
        "schema": str(SCHEMA_PATHS["doc_update_policy_ledger"]),
        "status": "complete",
        "doc_roles": doc_roles,
        "allowed_update_reasons": [
            "declared current mirror current section stale",
            "Stage 5EF command or file documentation introduced",
            "doc-policy ledger explicitly requires update",
            "focused validator proves concrete update need",
        ],
        "repo_wide_markdown_frontmatter_migration_performed": False,
        "repo_wide_markdown_frontmatter_migration_required": False,
    }


def _context_pack_registry(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_context_pack_registry",
        "schema": str(SCHEMA_PATHS["context_pack_registry"]),
        "status": "complete",
        "context_pack_template_count": len(CONTEXT_PACKS),
        "context_packs": [
            {
                **pack,
                "deterministic_template": True,
                "contains_wall_clock_timestamp": False,
                "contains_local_worktree_path": False,
                "contains_worktree_dirt_snapshot": False,
            }
            for pack in CONTEXT_PACKS
        ],
        "generated_context_pack_outputs_committed": False,
    }


def _plan_mode_policy(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_plan_mode_codex_run_policy",
        "schema": str(SCHEMA_PATHS["plan_mode_policy"]),
        "status": "complete",
        "plan_mode_used_for_stage5ef": True,
        "plan_review_performed_before_editing": True,
        "plan_amendment_applied_before_editing": True,
        "plan_mode_policy_created": True,
        "plan_deviation_count": 0,
        "plan_deviation_summary": [],
        "full_serial_pytest_required_for_normal_completion": False,
        "full_parallel_workers": 10,
        "full_parallel_pytest_workers": 10,
        "old_8_worker_cap": False,
        "old_16_worker_default_reintroduced": False,
        "required_closeout_files_ignored": [
            "codex-output/stage5ef-codex-plan.md",
            "codex-output/stage5ef-codex-completion.md",
        ],
    }


def _drift_audit_policy(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_drift_audit_policy",
        "schema": str(SCHEMA_PATHS["drift_audit_policy"]),
        "status": "complete",
        "audit_default_mode": "report_only_no_fix",
        "current_truth_authority": "data/project-state/current-stage-state.yaml",
        "human_mirrors_scoped_to_current_sections": True,
        "historical_sections_are_evidence_only": True,
        "generated_audit_outputs_committed": False,
        "audit_outputs_preferred_root": "experiments/results/doc-drift/",
    }


def _automation_registry(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_automation_audit_template_registry",
        "schema": str(SCHEMA_PATHS["automation_audit_template_registry"]),
        "status": "complete",
        "automation_templates": [
            {
                **template,
                "report_only": True,
                "auto_commit_allowed": False,
                "scheduled_now": False,
            }
            for template in AUTOMATION_TEMPLATES
        ],
        "codex_automations_scheduled_now": False,
        "automation_auto_commit_enabled": False,
    }


def _advisory_hook_policy(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_advisory_hook_policy",
        "schema": str(SCHEMA_PATHS["advisory_hook_policy"]),
        "status": "complete",
        "policy_document": "docs/codex/advisory-hooks.md",
        "active_hooks_created_now": False,
        "blocking_hooks_enabled_now": False,
        "advisory_hook_docs_created": True,
        "active_codex_hook_config_created": False,
    }


def _skill_readiness_policy(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_skill_readiness_policy",
        "schema": str(SCHEMA_PATHS["skill_readiness_policy"]),
        "status": "complete",
        "policy_document": "docs/codex/skills-readiness.md",
        "repo_local_skills_installed_now": False,
        "skill_skeleton_count": 0,
        "skills_deferred_because_agents_skills_not_repo_convention": True,
        "agents_skills_directory_created_now": False,
    }


def _doc_staleness_rule_repair(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_doc_staleness_rule_repair",
        "schema": str(SCHEMA_PATHS["doc_staleness_rule_repair"]),
        "status": "complete",
        "current_stage_state_authoritative": True,
        "validators_require_broad_historical_updates": False,
        "historical_sections_exempt_when_clearly_historical": True,
        "repo_wide_frontmatter_migration_required": False,
        "stage_ledger_current_sections_only_policy_created": True,
    }


def _validation_evidence(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_reviewable_validation_evidence",
        "schema": str(SCHEMA_PATHS["reviewable_validation_evidence"]),
        "status": "complete",
        "focused_validators_required_first": True,
        "stage_fast_required": True,
        "local_fast_required": True,
        "full_parallel_required_once_near_end": True,
        "full_parallel_workers": 10,
        "full_parallel_pytest_workers": 10,
        "full_serial_pytest_required_for_normal_completion": False,
        "validation_commands": [
            "python -m libreprimus.cli token-block validate-stage5ef",
            "python -m libreprimus.cli token-block validate-stage5ee",
            "python -m libreprimus.cli source-browser validate-index",
            "python -m pytest -q tests/python/test_stage5ef_*.py",
            "python -m ruff check python/libreprimus/token_block/stage5ef.py tests/python/test_stage5ef_*.py",
            "scripts/ci/run-stage-validation.ps1 -Stage stage5ef -Profile stage-fast",
            "scripts/ci/run-stage-validation.ps1 -Stage stage5ef -Profile local-fast",
            "scripts/ci/run-stage-validation.ps1 -Stage stage5ef -Profile full-parallel -Workers 10 -PytestWorkers 10",
        ],
    }


def _reviewability_gap_register(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_reviewability_gap_register",
        "schema": str(SCHEMA_PATHS["reviewability_gap_register"]),
        "status": "complete",
        "open_gap_count": 1,
        "gaps": [
            {
                "gap_id": "number_fact_review_batch_006_deferred",
                "status": "deferred_to_stage5eg",
                "required_next_stage_id": NEXT_STAGE_ID,
                "execution_authorized_now": False,
            }
        ],
    }


def _chatgpt_context_summary(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_chatgpt_context_update_summary",
        "schema": str(SCHEMA_PATHS["chatgpt_context_update_summary"]),
        "status": "complete",
        "chatgpt_context_updated": True,
        "current_truth_authority_recorded": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
    }


def _gate_record(common: dict[str, Any], key: str, proof_field: str) -> dict[str, Any]:
    return {
        **common,
        "record_type": f"stage5ef_{key}",
        "schema": str(SCHEMA_PATHS[key]),
        "status": "complete",
        "gate_closed": True,
        proof_field: True,
        "string4_active": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
    }


def _codex_handoff_policy(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_codex_handoff_policy",
        "schema": str(SCHEMA_PATHS["codex_handoff_policy"]),
        "status": "complete",
        "canonical_codex_handoff_root": "codex-output",
        "required_ignored_handoff_files": [
            "codex-output/stage5ef-codex-plan.md",
            "codex-output/stage5ef-codex-completion.md",
        ],
        "codex_output_committed": False,
        "completion_summary_non_placeholder_required": True,
    }


def _credential_redaction_policy(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_credential_redaction_policy_preservation",
        "schema": str(SCHEMA_PATHS["credential_redaction_policy_preservation"]),
        "status": "complete",
        "credential_redaction_policy_preserved": True,
        "credentials_or_secrets_recorded": False,
        "secret_paths_recorded": False,
    }


def _raw_source_noncommit_proof(common: dict[str, Any]) -> dict[str, Any]:
    return {
        **common,
        "record_type": "stage5ef_raw_source_noncommit_proof",
        "schema": str(SCHEMA_PATHS["raw_source_noncommit_proof"]),
        "status": "complete",
        "raw_source_files_committed": False,
        "raw_third_party_files_committed": False,
        "generated_outputs_committed": False,
        "codex_output_committed": False,
        "sqlite_committed": False,
    }


def _source_browser_loadability_record() -> dict[str, Any]:
    validation = validate_source_index()
    index = build_source_index()
    summary = source_browser_summary(index)
    path_validation = validate_path_canonicalization()
    path_report = path_canonicalization_report(index)
    return {
        "record_type": "stage5ef_source_browser_loadability_summary",
        "status": "complete",
        "source_browser_entries_loaded": int(summary.get("entries_loaded", 0)),
        "source_browser_record_count": int(summary.get("records_scanned", 0)),
        "source_browser_validation_error_count": len(validation.errors),
        "source_browser_validation_warning_count": len(validation.warnings),
        "path_canonicalization_errors": len(path_validation.errors),
        "path_canonicalization_warnings": len(path_validation.warnings) + len(path_report.get("warnings", [])),
        "source_browser_loadable_after_stage5ef": len(validation.errors) == 0,
        "source_browser_records_modified_now": False,
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
        "status": {"enum": ["complete"]},
        "recommended_next_stage_id": {"const": NEXT_STAGE_ID},
        "no_solve_claim": {"const": True},
        "generated_outputs_committed": {"const": False},
        "solve_claim": {"const": False},
        "execution_performed": {"const": False},
        "cuda_execution_performed": {"const": False},
        "canonical_corpus_active": {"const": False},
        "page_boundaries_finalized": {"const": False},
        "new_source_lock_evidence_added_now": {"const": False},
        "number_fact_enrichment_overlays_added_now": {"const": False},
        "number_fact_backfill_performed_now": {"const": False},
        "target_priority_decision_created_now": {"const": False},
        "route_extraction_performed_now": {"const": False},
        "real_byte_stream_generated": {"const": False},
    }
    if key == "summary":
        properties.update(
            {
                "plan_mode_used_for_stage5ef": {"const": True},
                "plan_review_performed_before_editing": {"const": True},
                "plan_amendment_applied_before_editing": {"const": True},
                "plan_mode_policy_created": {"const": True},
                "plan_deviation_count": {"type": "integer", "minimum": 0},
                "active_hooks_created_now": {"const": False},
                "codex_automations_scheduled_now": {"const": False},
                "repo_local_skills_installed_now": {"const": False},
            }
        )
        required.extend(
            [
                "plan_mode_used_for_stage5ef",
                "plan_review_performed_before_editing",
                "plan_amendment_applied_before_editing",
                "plan_mode_policy_created",
                "active_hooks_created_now",
                "codex_automations_scheduled_now",
                "repo_local_skills_installed_now",
            ]
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
    for field, value in [
        ("stage_id", STAGE_ID),
        ("latest_completed_stage_id", STAGE_ID),
        ("recommended_next_stage_id", NEXT_STAGE_ID),
    ]:
        enum = props.get(field, {}).get("enum")
        if isinstance(enum, list) and value not in enum:
            enum.append(value)
    write_json(path, schema)


def _write_templates_and_docs(records: dict[str, Any]) -> None:
    for pack in CONTEXT_PACKS:
        _write_text(Path(pack["path"]), _context_pack_text(pack))
    for template in AUTOMATION_TEMPLATES:
        _write_text(Path(template["path"]), _automation_template_text(template))
    _write_text(TEMPLATE_PATHS["plan_mode_prompt"], _plan_mode_template_text())
    _write_text(TEMPLATE_PATHS["closeout"], _closeout_template_text())
    doc_texts = {
        CODEX_DOC_DIR / "current-truth-and-doc-policy.md": _current_truth_doc_text(),
        CODEX_DOC_DIR / "plan-mode-run-protocol.md": _plan_mode_doc_text(),
        CODEX_DOC_DIR / "context-packs.md": _context_packs_doc_text(records["context_pack_registry"]),
        CODEX_DOC_DIR / "automation-audit-templates.md": _automation_doc_text(records["automation_audit_template_registry"]),
        CODEX_DOC_DIR / "advisory-hooks.md": _advisory_hooks_doc_text(),
        CODEX_DOC_DIR / "skills-readiness.md": _skills_doc_text(),
        DEV_LOG_PATH: _development_log_text(),
        RESEARCH_LOG_PATH: _research_log_text(),
    }
    for path, text in doc_texts.items():
        _write_text(path, text)


def _context_pack_text(pack: dict[str, str]) -> str:
    return f"""# Stage 5EF Context Pack Template: {pack['pack_id']}

Purpose: {pack['purpose']}

Authority:
- Authoritative current truth: `data/project-state/current-stage-state.yaml`
- Current stage: `{STAGE_ID}`
- Next routed stage: `{NEXT_STAGE_ID}` - {NEXT_STAGE_TITLE}

Required Guardrails:
- Do not add source-lock evidence.
- Do not add number-fact enrichment overlays.
- Do not backfill source records.
- Do not select a target or pivot.
- Do not generate byte streams.
- Do not execute puzzle, CUDA, scoring, benchmark, image, OCR, audio, stego, Tor, or website work.
- Do not claim a solve.

Inputs To Review:
- Current-stage registry and Stage 5EF policy ledgers.
- Existing committed source records only.
- Focused validator output, if provided.

Output Shape:
- Summary of scoped records consulted.
- Exact blocker list.
- Recommended next action, if any.
- Confirmation that generated outputs remain ignored and uncommitted.

Determinism:
- This template contains no wall-clock timestamp, local path, temporary output path, or worktree-dirt snapshot.
"""


def _automation_template_text(template: dict[str, str]) -> str:
    return f"""# Stage 5EF Report-Only Automation Template: {template['template_id']}

Purpose: {template['purpose']}

Rules:
- Report-only.
- Do not auto-commit.
- Do not execute puzzle work.
- Do not add source-lock evidence.
- Do not mutate raw, third-party, generated, or `codex-output` roots.
- Do not schedule this template automatically; a later explicit prompt is required.

Report Fields:
- stage_id: `{STAGE_ID}`
- current_truth_authority: `data/project-state/current-stage-state.yaml`
- findings
- warnings
- recommended_next_stage_id: `{NEXT_STAGE_ID}`
"""


def _plan_mode_template_text() -> str:
    return """# Codex Plan-Mode Prompt Template

Use this template for multi-file, governance, source-lock, validation, or stage-routing work.

Required Fields:
- stage_id
- scope
- authoritative_current_truth: `data/project-state/current-stage-state.yaml`
- guardrails
- files expected to change
- files explicitly not to change
- validation plan
- commit/push/CI plan

Stage 5EF Evidence Fields:
- plan_mode_used_for_stage5ef: true
- plan_review_performed_before_editing: true
- plan_amendment_applied_before_editing: true
- plan_deviation_count: 0 unless real deviations occur
"""


def _closeout_template_text() -> str:
    return f"""# Codex Closeout Template

Include:
- final commit
- origin/main commit
- GitHub issue
- CI run/status
- plan-mode used
- plan amendment applied
- doc-policy files created
- context-pack templates created
- automation templates created
- active hooks created: false
- automations scheduled: false
- skills installed: false
- full serial pytest run: false
- full-parallel validation with 10/10 workers
- guardrails closed
- recommended next stage: `{NEXT_STAGE_ID}` - {NEXT_STAGE_TITLE}
"""


def _current_truth_doc_text() -> str:
    return f"""# Current Truth And Document Policy

Stage 5EF defines one authoritative current-stage source:

- `data/project-state/current-stage-state.yaml`

`AGENTS.md` and `ChatGPT-ContextFile.md` are high-priority operating context. `STATUS.md`, `README.md`,
`ROADMAP.md`, and `docs/roadmap/staged-plan.md` are human-readable mirrors only, and only their current
sections are expected to track the latest stage.

Historical development logs, research logs, experiment notes, and older sections in Markdown are evidence.
They may contain old next-stage claims when clearly historical. Validators should not force broad historical
rewrites.

Stage 5EF routes `{PREVIOUS_STAGE_ID}` to `{NEXT_STAGE_ID}` by inserting this anti-drift foundation before
number-fact review batch 006.
"""


def _plan_mode_doc_text() -> str:
    return """# Plan-Mode Run Protocol

Stage 5EF records the first explicit plan-mode governance policy for this repository.

Required for future broad work:
- review the plan before editing;
- apply any operator amendment before editing;
- record deviations explicitly;
- keep `codex-output/**` handoff files ignored;
- run focused validators before broad validation;
- use final full-parallel validation with 10 workers and 10 pytest workers;
- do not require full serial pytest for normal completion.
"""


def _context_packs_doc_text(registry: dict[str, Any]) -> str:
    rows = "\n".join(f"- `{pack['pack_id']}` -> `{pack['path']}`" for pack in registry["context_packs"])
    return f"""# Context Packs

Stage 5EF adds deterministic context-pack templates only. They contain no wall-clock timestamps, local paths,
temporary output paths, or worktree-dirt snapshots.

Templates:
{rows}

Generated or volatile context-pack outputs belong under ignored output roots, not committed docs.
"""


def _automation_doc_text(registry: dict[str, Any]) -> str:
    rows = "\n".join(f"- `{item['template_id']}` -> `{item['path']}`" for item in registry["automation_templates"])
    return f"""# Automation Audit Templates

Stage 5EF creates report-only automation prompt templates. No automation is scheduled now, and auto-commit
remains disabled.

Templates:
{rows}
"""


def _advisory_hooks_doc_text() -> str:
    return """# Advisory Hooks

Stage 5EF documents advisory hook policy only.

No active `.codex/hooks` configuration is created, no blocking hook is enabled, and no hook may mutate raw,
third-party, generated, or `codex-output` roots. A later explicit prompt is required before any hook can
become active.
"""


def _skills_doc_text() -> str:
    return """# Skills Readiness

Stage 5EF defers repo-local skills. `.agents/skills` is not an established repository convention here, so
no skill skeletons are installed and no skill is activated by this stage.
"""


def _development_log_text() -> str:
    return f"""# Stage 5EF Development Log

Stage 5EF added a current-truth authority ledger, doc update-policy ledger, deterministic context-pack
templates, report-only automation templates, inactive advisory-hook policy, skill-readiness deferral, and
focused validators.

No puzzle execution, source-lock evidence, number-fact overlays, target selection, byte-stream generation,
CUDA, scoring, benchmark, raw-source processing, website expansion, or solve claim was added.

Next routed stage: `{NEXT_STAGE_ID}` - {NEXT_STAGE_TITLE}.
"""


def _research_log_text() -> str:
    return f"""# Stage 5EF Next-Stage Decision Summary

Stage 5EE originally routed the next prompt to Stage 5EF as number-fact review batch 006. The operator inserted
Stage 5EF as anti-drift/current-truth infrastructure, so batch 006 is deferred to Stage 5EG.

Current truth authority: `data/project-state/current-stage-state.yaml`.

Recommended next stage: `{NEXT_STAGE_ID}` - {NEXT_STAGE_TITLE}.
"""


def _update_current_stage_state() -> None:
    prior = read_yaml(CURRENT_STAGE_STATE_PATH)
    updated = {
        **prior,
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "source_lock_only": False,
        "reviewability_stage": True,
        "number_fact_review_batch_stage": False,
        "plan_mode_policy_stage": True,
        "latest_completed_stage_id": STAGE_ID,
        "latest_completed_stage_title": STAGE_TITLE,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": "assistant_or_operator_review_then_codex_overlay_update",
        "stage5ee_recommended_stage5ef_number_fact_batch_006": True,
        "operator_inserted_antidrift_stage_before_batch_006": True,
        "number_fact_review_batch_006_deferred_to_stage5eg": True,
        "plan_mode_used_for_stage5ef": True,
        "plan_amendment_applied_before_editing": True,
        "active_hooks_created_now": False,
        "blocking_hooks_enabled_now": False,
        "codex_automations_scheduled_now": False,
        "automation_auto_commit_enabled": False,
        "repo_local_skills_installed_now": False,
        **FALSE_GUARDRAILS,
    }
    updated["post_push_handoff_locations"] = [
        "codex-output/stage5ef-codex-completion.md",
        "GitHub issue comment",
    ]
    write_yaml(CURRENT_STAGE_STATE_PATH, updated)


def _update_stage5ah_source_of_truth() -> None:
    record = read_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH)
    record.update(
        {
            "latest_completed_stage_after_this_stage": STAGE_TITLE,
            "latest_completed_stage_prefix": "Stage 5EF",
            "next_stage_after_this_stage": NEXT_STAGE_TITLE,
            "expected_next_stage_prefix": "Stage 5EG",
            "expected_latest_after_stage5ah": STAGE_TITLE,
            "expected_next_after_stage5ah": NEXT_STAGE_TITLE,
            "current_stage_state_authoritative": True,
            "human_readable_docs_are_mirrors_only": True,
            "historical_sections_can_contain_old_next_stage_claims": True,
        }
    )
    write_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH, record)


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
            "summary": (
                "Inserted a current-truth authority ledger, doc update-policy ledger, deterministic "
                "context-pack templates, report-only automation templates, inactive advisory-hook policy, "
                "and Stage 5EG routing for number-fact review batch 006."
            ),
            "key_outputs": [
                "Authoritative current-stage truth narrowed to data/project-state/current-stage-state.yaml.",
                "Doc update-policy ledger classifies current mirrors, operating context, historical logs, generated handoffs, and ignored roots.",
                "Deterministic context-pack templates and report-only automation templates were added without active hooks, scheduled automations, or repo-local skills.",
                "Stage 5EE's historical route to Stage 5EF batch 006 is preserved and number-fact review batch 006 is deferred to Stage 5EG.",
            ],
            "result_status": "metadata_tooling_complete",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                f"next={NEXT_STAGE_ID}; plan_mode_used=true; full_serial_pytest_required=false; "
                "source-lock evidence, number-fact overlays, execution, CUDA, scoring, benchmarks, "
                "website expansion, and solve claims remain blocked."
            ),
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
    additions = [
        "data/project-state/stage5ef-summary.yaml",
        "data/project-state/stage5ef-current-truth-authority-policy.yaml",
        "data/project-state/stage5ef-doc-update-policy-ledger.yaml",
        "data/project-state/stage5ef-context-pack-registry.yaml",
        "data/project-state/stage5ef-plan-mode-codex-run-policy.yaml",
        "data/project-state/stage5ef-drift-audit-policy.yaml",
        "docs/codex/current-truth-and-doc-policy.md",
        "docs/codex/plan-mode-run-protocol.md",
        "docs/codex/context-packs.md",
        "docs/reference/token-block-cli.md",
    ]
    addition_set = set(additions)
    records = [record for record in records if record.get("path") not in addition_set]

    def build_record(path: str) -> dict[str, object]:
        is_data = path.startswith("data/")
        is_reference_doc = path.startswith("docs/reference/")
        if is_data:
            category = "active_data_record"
            purpose = "Stage 5EF machine-readable current-truth, policy, or validation record."
            rank = 1 if path == "data/project-state/stage5ef-current-truth-authority-policy.yaml" else 2
            relationships = "machine-readable Stage 5EF source record; mirrored by focused docs only where declared"
            staleness = "reference_only"
            mutable = "mutable"
        elif is_reference_doc:
            category = "policy_doc"
            purpose = "Reference documentation for Stage 5EF token-block and current-truth commands."
            rank = 3
            relationships = "human-readable mirror of Stage 5EF CLI behavior; not authoritative current truth"
            staleness = "mirror"
            mutable = "mutable"
        else:
            category = "policy_doc"
            purpose = "Stage 5EF Codex operating policy documentation."
            rank = 3
            relationships = "human-readable policy mirror of committed Stage 5EF records; not authoritative current truth"
            staleness = "reference_only"
            mutable = "mutable"
        return {
            "path": path,
            "category": category,
            "purpose": purpose,
            "source_of_truth_rank": rank,
            "last_meaningful_update_stage": STAGE_ID,
            "expected_update_frequency": "stage_specific",
            "mutable_or_reference_only": mutable,
            "mirror_or_generated_relationships": relationships,
            "staleness_check_level": staleness,
            "owner_context": "codex_agent",
            "notes": (
                "Added by Stage 5EF current-truth/doc-drift foundation. "
                "current-stage-state.yaml remains the authoritative current truth."
            ),
            "stage5ef_role": "stage5ef_current_truth_or_policy",
            "current_truth_authority": path
            == "data/project-state/stage5ef-current-truth-authority-policy.yaml",
        }

    for path in additions:
        records.append(build_record(path))
    payload["records"] = records
    write_yaml(OPERATIONAL_FILE_MAP_PATH, payload)


def _update_current_mirrors() -> None:
    replacements = {
        "AGENTS.md": _agents_stage_section(),
        "ChatGPT-ContextFile.md": _chatgpt_stage_section(),
        "STATUS.md": _status_stage_section(),
        "README.md": _readme_stage_section(),
        "ROADMAP.md": _roadmap_stage_section(),
        "TESTING.md": _testing_stage_section(),
        "docs/roadmap/staged-plan.md": _staged_plan_section(),
        "docs/onboarding/source-of-truth-map.md": _source_of_truth_map_section(),
        "docs/onboarding/operational-file-map.md": _operational_map_doc_section(),
        "docs/reference/token-block-cli.md": _token_block_cli_section(),
    }
    for path_text, block in replacements.items():
        _upsert_marked_section(Path(path_text), "stage5ef", block)


def _agents_stage_section() -> str:
    return f"""## Stage 5EF Current-Truth Amendment

- Current completed stage: {STAGE_TITLE}.
- Current work: {NEXT_STAGE_TITLE}.
- Authoritative current truth is `data/project-state/current-stage-state.yaml`.
- Broad Markdown docs are mirrors or historical evidence, not authoritative state.
- Stage 5EE originally routed Stage 5EF to number-fact review batch 006; that batch is now deferred to Stage 5EG.
- Stage 5EF creates no source-lock evidence, number-fact overlays, target selection, byte streams, execution, CUDA,
  scoring, benchmarks, website expansion, or solve claim.
"""


def _chatgpt_stage_section() -> str:
    return f"""## Stage 5EF Current Context

Current completed stage: {STAGE_TITLE}.

Current work / recommended next stage: {NEXT_STAGE_TITLE}.

Authoritative current truth is `data/project-state/current-stage-state.yaml`. `AGENTS.md` and this file are
operating context. README, STATUS, ROADMAP, and staged-plan current sections are mirrors only. Historical logs
remain evidence and may retain old next-stage claims when clearly historical.
"""


def _status_stage_section() -> str:
    return f"""## Stage 5EF Status

Latest completed stage: {STAGE_TITLE}.

Recommended next stage: {NEXT_STAGE_TITLE}.

Stage 5EF is metadata/tooling only: current-truth authority, doc update policy, deterministic context-pack
templates, report-only automation templates, inactive advisory-hook policy, skill-readiness deferral, and
Stage 5EG routing. No puzzle execution or source-lock evidence changed.
"""


def _readme_stage_section() -> str:
    return f"""## Stage 5EF Current Status

The current authoritative stage registry is `data/project-state/current-stage-state.yaml`.

Latest completed: {STAGE_TITLE}.

Next routed: {NEXT_STAGE_TITLE}.

Stage 5EF is an anti-drift/current-truth foundation inserted before number-fact review batch 006. Batch 006 is
deferred to Stage 5EG.
"""


def _roadmap_stage_section() -> str:
    return f"""## Stage 5EF Route

Stage 5EF is complete as current-truth and drift-audit infrastructure. It preserves Stage 5EE and routes the
deferred number-fact review batch 006 to Stage 5EG.

Next: {NEXT_STAGE_TITLE}.
"""


def _testing_stage_section() -> str:
    return """## Stage 5EF Validation Policy

Stage 5EF keeps the Stage 5EB validation discipline: run focused validators first, then `stage-fast`,
`local-fast`, and one final `full-parallel` validation with `Workers=10` and `PytestWorkers=10`. Full serial
pytest is not required for normal completion.
"""


def _staged_plan_section() -> str:
    return f"""## Stage 5EF

Status: complete.

Scope: current-truth ledger, doc update-policy ledger, deterministic context-pack templates, report-only
automation templates, inactive advisory-hook policy, and skills deferral.

Preserved fact: Stage 5EE originally routed to Stage 5EF as number-fact review batch 006. Operator inserted
Stage 5EF as anti-drift infrastructure; batch 006 is deferred to Stage 5EG.

Next: {NEXT_STAGE_TITLE}.
"""


def _source_of_truth_map_section() -> str:
    return """## Stage 5EF Source-Of-Truth Amendment

`data/project-state/current-stage-state.yaml` is the authoritative current-stage truth. README, STATUS,
ROADMAP, and staged-plan current sections are mirrors only. Historical logs and historical Markdown sections
are evidence, not current truth.
"""


def _operational_map_doc_section() -> str:
    return """## Stage 5EF Operational Map Amendment

Stage 5EF records current-truth, doc update-policy, context-pack, plan-mode, drift-audit, automation-template,
advisory-hook, and skill-readiness files in `data/project-state/operational-file-map.yaml`.
"""


def _token_block_cli_section() -> str:
    return """## Stage 5EF CLI

Stage 5EF commands:

- `python -m libreprimus.cli token-block build-stage5ef`
- `python -m libreprimus.cli token-block validate-stage5ef`
- `python -m libreprimus.cli token-block stage5ef-summary`
- focused validators such as `validate-stage5ef-current-truth`, `validate-stage5ef-context-packs`, and
  `validate-stage5ef-sidecar-gates`

These commands build and validate metadata/tooling records only. They do not execute puzzle work.
"""


def _write_codex_output_handoffs() -> None:
    _write_text(
        CODEX_OUTPUT_DIR / "stage5ef-codex-plan.md",
        f"""# Stage 5EF Codex Plan

Plan-mode used: true.
Plan amendment applied before editing: true.
Scope: current-truth ledger, context-pack templates, report-only automation templates, inactive hooks, skills
deferral, and focused validators.
Recommended next stage: {NEXT_STAGE_TITLE}.

This file is ignored and must not be committed.
""",
    )
    _write_text(
        CODEX_OUTPUT_DIR / "stage5ef-codex-completion.md",
        f"""# Stage 5EF Codex Completion

Final commit: pending until commit.
Origin/main commit: pending until push.
GitHub issue: pending.
CI run/status: pending.
Plan-mode used: true.
Plan amendment applied: true.
Context-pack templates created: {len(CONTEXT_PACKS)}.
Automation templates created: {len(AUTOMATION_TEMPLATES)}.
Active hooks created: false.
Automations scheduled: false.
Skills installed: false.
Full serial pytest run: false.
Full-parallel validation: pending 10/10.
Guardrails closed: true.
Recommended next stage: {NEXT_STAGE_ID} - {NEXT_STAGE_TITLE}.

This file is ignored and must not be committed.
""",
    )


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


def _required_paths() -> list[Path]:
    return list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values()) + [
        CURRENT_STAGE_STATE_PATH,
        CHATGPT_CONTEXT_PATH,
        OPERATIONAL_FILE_MAP_PATH,
        STAGE_SUMMARY_RECORDS_PATH,
        DOC_STALENESS_SOURCE_OF_TRUTH_PATH,
        *[Path(pack["path"]) for pack in CONTEXT_PACKS],
        *[Path(template["path"]) for template in AUTOMATION_TEMPLATES],
        *TEMPLATE_PATHS.values(),
        CODEX_DOC_DIR / "current-truth-and-doc-policy.md",
        CODEX_DOC_DIR / "plan-mode-run-protocol.md",
        CODEX_DOC_DIR / "context-packs.md",
        CODEX_DOC_DIR / "automation-audit-templates.md",
        CODEX_DOC_DIR / "advisory-hooks.md",
        CODEX_DOC_DIR / "skills-readiness.md",
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
    if record.get("solve_claim") is not False:
        errors.append(f"{record.get('record_type', 'record')} must have solve_claim=false")
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
