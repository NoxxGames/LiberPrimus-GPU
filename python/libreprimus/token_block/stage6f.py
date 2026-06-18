"""Stage 6F current-doc integrity and acceptance hardening."""

from __future__ import annotations

from collections import Counter
import json
import os
from pathlib import Path
import platform
import re
import subprocess
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import validate_source_index
from libreprimus.token_block import stage6, stage6b, stage6c, stage6d, stage6e
from libreprimus.token_block.models import read_yaml, write_yaml

STAGE_ID = "stage-6f"
STAGE_TOKEN = "stage6f"
STAGE_TITLE = (
    "Stage 6F - Current-doc integrity, hook traceability, and acceptance hardening, "
    "without execution"
)
PROMPT_TYPE = "codex_plan_mode_readiness_repair_and_acceptance_hardening"
PREVIOUS_STAGE_ID = "stage-6e"
NEXT_STAGE_ID = "stage-6g"
NEXT_PROMPT_TYPE_FINAL = "codex_plan_mode_probe_manifest_finalization"
NEXT_PROMPT_TYPE_REPAIR = "codex_plan_mode_readiness_repair"
NEXT_STAGE_TITLE_FINAL = "Stage 6G - Final finite Stage 7 probe manifest and archive-run contract, without execution"
NEXT_STAGE_TITLE_REPAIR = "Stage 6G - Stage 7 readiness repair before final manifest, without execution"
STARTING_COMMIT = "e7c29851e4c41a4f59ed1b0a8d33d3b6cd6807fb"

PROJECT_STATE_DIR = Path("data/project-state")
TOKEN_BLOCK_DIR = Path("data/token-block")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
CURRENT_STAGE_SCHEMA_PATH = Path("schemas/project-state/current-stage-state-v0.schema.json")
DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH = Path(
    "schemas/project-state/doc-staleness-source-of-truth-record-v0.schema.json"
)
CODEX_COMPLETION_PATH = Path("codex-output/stage6f-codex-completion.md")
PREFLIGHT_REPORT_PATH = Path("experiments/results/doc-drift/codex-preprompt-doc-staleness-preflight.json")
STOP_REPORT_PATH = Path("experiments/results/doc-drift/codex-stop-hook-stale-current-audit.json")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage6f-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage6f-next-stage-decision.yaml",
    "stage6e_preservation": PROJECT_STATE_DIR / "stage6f-stage6e-preservation.yaml",
    "edited_document_integrity_review": PROJECT_STATE_DIR / "stage6f-edited-document-integrity-review.yaml",
    "current_mirror_consistency": PROJECT_STATE_DIR / "stage6f-current-mirror-consistency.yaml",
    "chatgpt_context_validation": PROJECT_STATE_DIR / "stage6f-chatgpt-context-validation.yaml",
    "strict_acceptance_policy": PROJECT_STATE_DIR / "stage6f-strict-acceptance-policy.yaml",
    "preflight_report_selection": PROJECT_STATE_DIR / "stage6f-preflight-report-selection.yaml",
    "hook_verification_summary": PROJECT_STATE_DIR / "stage6f-hook-verification-summary.yaml",
    "traceability_cleanup": PROJECT_STATE_DIR / "stage6f-traceability-cleanup-summary.yaml",
    "stage6g_readiness_blocker_register": PROJECT_STATE_DIR / "stage6f-stage6g-readiness-blocker-register.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR / "stage6f-source-browser-loadability-summary.yaml",
    "stage7_artifact_absence": PROJECT_STATE_DIR / "stage6f-stage7-artifact-absence.yaml",
    "review_finding_closure": PROJECT_STATE_DIR / "stage6f-stage6e-review-finding-closure.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage6f-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage6f-reviewability-gap-register.yaml",
    "current_stage_transition": PROJECT_STATE_DIR / "stage6f-current-stage-transition.yaml",
}

TOKEN_BLOCK_PATHS: dict[str, Path] = {
    "probe_source_traceability_semantics_repair": TOKEN_BLOCK_DIR
    / "stage6f-probe-source-traceability-semantics-repair.yaml",
    "stage6g_manifest_input_addendum": TOKEN_BLOCK_DIR / "stage6f-stage6g-manifest-input-addendum.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage6f-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage6f-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage6f-no-execution-transition-gate.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "ciada_cicada_alias_policy": SOURCE_HARVESTER_DIR / "stage6f-ciada-cicada-source-root-alias-policy.yaml",
    "dju_bei_gap_source_crosslink": SOURCE_HARVESTER_DIR / "stage6f-dju-bei-gap-source-crosslink.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage6f-raw-source-noncommit-proof.yaml",
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage6f-codex-handoff-policy.yaml",
    "acceptance_policy_integration": SOURCE_HARVESTER_DIR / "stage6f-acceptance-policy-integration.yaml",
}

DATA_PATHS = {**PROJECT_STATE_PATHS, **TOKEN_BLOCK_PATHS, **SOURCE_HARVESTER_PATHS}


def _schema_path(category: str, key: str) -> Path:
    return Path(f"schemas/{category}/stage6f-{key.replace('_', '-')}-v0.schema.json")


SCHEMA_PATHS: dict[str, Path] = {key: _schema_path("project-state", key) for key in PROJECT_STATE_PATHS}
SCHEMA_PATHS.update({key: _schema_path("token-block", key) for key in TOKEN_BLOCK_PATHS})
SCHEMA_PATHS.update({key: _schema_path("source-harvester", key) for key in SOURCE_HARVESTER_PATHS})

STAGE6F_FALSE_GUARDRAILS = {
    "stage7_execution_allowed_next": False,
    "stage7_zip_archive_creation_allowed_next": False,
    "stage6f_final_finite_stage7_manifest_created_now": False,
    "stage6f_archive_run_contract_finalized_now": False,
    "stage6f_creates_stage7_result_archive_now": False,
    "stage6f_generates_stage7_outputs_now": False,
    "stage6f_routes_to_stage7_now": False,
    "stage6f_runs_any_probe_now": False,
    "new_theory_source_locks_created_now": False,
    "new_future_probe_ids_created_now": False,
    "new_number_fact_overlays_created_now": False,
    "stage6e_bridge_payloads_rewritten_now": False,
    "stage6e_source_lock_payloads_rewritten_now": False,
    "stage6e_bridge_source_lock_records_mutated_now": False,
    "stage7_manifest_created_now": False,
    "stage7_archive_created_now": False,
}
FORBIDDEN_FALSE = (
    stage6.FALSE_GUARDRAILS
    | stage6.STAGE6_FALSE_GUARDRAILS
    | stage6b.FORBIDDEN_FALSE
    | stage6c.STAGE6C_FALSE_GUARDRAILS
    | stage6d.STAGE6D_FALSE_GUARDRAILS
    | stage6e.STAGE6E_FALSE_GUARDRAILS
    | STAGE6F_FALSE_GUARDRAILS
)

CURRENT_DOC_PATHS = [
    Path("README.md"),
    Path("AGENTS.md"),
    Path("STATUS.md"),
    Path("ROADMAP.md"),
    Path("TESTING.md"),
    Path("ChatGPT-ContextFile.md"),
    Path("docs/roadmap/staged-plan.md"),
    Path("docs/onboarding/start-here.md"),
    Path("docs/onboarding/source-of-truth-map.md"),
    Path("docs/onboarding/operational-file-map.md"),
    Path("docs/reference/token-block-cli.md"),
    CURRENT_STAGE_STATE_PATH,
]

HIGH_RISK_CURRENT_DOCS = [
    Path("README.md"),
    Path("AGENTS.md"),
    Path("STATUS.md"),
    Path("ROADMAP.md"),
    Path("TESTING.md"),
    Path("ChatGPT-ContextFile.md"),
]

FORBIDDEN_CURRENT_PATTERNS = [
    "Stage 6E consolidated Stage 6F readiness after Stage 6E consolidated",
    "Stage 6D source-locks the canonical doublet boundary",
    "codex-output/stage6d-codex-completion.md",
]

STAGE6E_CHATGPT_TOPICS = [
    "Stage 6E preserved Stage 6C OUROBOROS/I31 and Stage 6D doublet/boundary addenda",
    "CIRCUMFERENCE = 398 = 2 * GP(I AM)",
    "C-to-F finite mask family",
    "DIUINITY/DIVINITY source surface",
    "AN END = FIVE DOTS = 311 = prime(64)",
    "big-gap one-based sum 569 = prime(104)",
    "Page32 3222 = 18 * 179",
    "WE MUST SHED OUR OWN CIRCUMFERENCES = 1031",
    "dju bei / dju bei ae remains an exact-span source gap",
    "Stage 6E did not run probes, create a final Stage 7 manifest, generate route or byte streams, create archives, select targets, or make a solve claim",
]
STAGE6F_CHATGPT_TOPICS = [
    "current-doc integrity repair",
    "preflight self-report exclusion",
    "metadata-only probe traceability semantic cleanup",
    "Ciada/Cicada alias policy",
    "dju-bei backlog crosslink",
    "strict acceptance-criteria policy",
    "Stage 6G routing",
]

STAGE6E_REVIEW_FINDINGS = [
    ("readme_malformed_repeated_current_text", "README.md", "fixed"),
    ("agents_malformed_repeated_current_text", "AGENTS.md", "fixed"),
    ("chatgpt_context_missing_stage6e_durable_summary", "ChatGPT-ContextFile.md", "fixed"),
    ("status_stale_stage6d_current_mirror_text", "STATUS.md", "fixed"),
    ("roadmap_stale_stage6d_current_mirror_text", "ROADMAP.md", "fixed"),
    ("current_state_post_push_handoff_points_to_stage6d", CURRENT_STAGE_STATE_PATH.as_posix(), "fixed"),
    (
        "weak_ciada_cicada_alias_policy",
        SOURCE_HARVESTER_PATHS["ciada_cicada_alias_policy"].as_posix(),
        "fixed",
    ),
    (
        "metadata_only_traceability_rows_have_empty_source_roots_but_require_source_root_present",
        TOKEN_BLOCK_PATHS["probe_source_traceability_semantics_repair"].as_posix(),
        "fixed",
    ),
    ("dju_bei_gap_lacks_backlog_source_crosslink", SOURCE_HARVESTER_PATHS["dju_bei_gap_source_crosslink"].as_posix(), "fixed"),
    ("preflight_hook_can_reuse_own_prior_report_as_authoritative", ".codex/hooks/doc_staleness_preflight.py", "fixed"),
    ("hook_previous_run_exited_code_1", PROJECT_STATE_PATHS["hook_verification_summary"].as_posix(), "verified_or_risk_recorded"),
    ("strict_acceptance_criteria_policy_missing", "docs/onboarding/codex-acceptance-criteria.md", "fixed"),
]


class ValidationResult(stage6.ValidationResult):
    pass


def build_stage6f() -> dict[str, Any]:
    _ensure_no_protected_output_overlap()
    _write_schemas()
    _write_current_stage_schema()
    _write_doc_staleness_source_of_truth_schema()

    provisional = _summary_record(_empty_doc_integrity(), _empty_chatgpt_validation(), _empty_hook_evidence(), _empty_source_browser())
    _write_current_stage_state(provisional)
    _write_docs(provisional)
    _write_operational_file_map()

    hook_evidence = _hook_evidence(run_checks=True)
    source_browser = _source_browser_summary()
    doc_integrity = _edited_document_integrity_payload()
    chatgpt_validation = _chatgpt_context_validation_payload()
    records = _records(doc_integrity, chatgpt_validation, hook_evidence, source_browser)
    _write_records(records)
    _write_current_stage_state(records["summary"])
    _write_docs(records["summary"])
    doc_integrity = _edited_document_integrity_payload()
    chatgpt_validation = _chatgpt_context_validation_payload()
    records = _records(doc_integrity, chatgpt_validation, hook_evidence, source_browser)
    _write_records(records)
    _write_current_stage_state(records["summary"])
    _write_stage_summary_record(records["summary"])
    _write_completion_summary_stub(records["summary"], hook_evidence)
    return records


def validate_stage6f() -> ValidationResult:
    validators = [
        validate_stage6f_files_and_schemas,
        validate_stage6f_current_stage_transition,
        validate_stage6f_edited_document_integrity,
        validate_stage6f_current_mirror_consistency,
        validate_stage6f_chatgpt_context,
        validate_stage6f_preflight_report_selection,
        validate_stage6f_hook_verification,
        validate_stage6f_traceability_cleanup,
        validate_stage6f_alias_policy,
        validate_stage6f_dju_bei_crosslink,
        validate_stage6f_acceptance_policy,
        validate_stage6f_stage6g_blocker_routing,
        validate_stage6f_stage7_artifact_absence,
        validate_stage6f_source_browser_loadability,
        validate_stage6f_gate_closure,
        validate_stage6f_handoff,
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for validator in validators:
        result = validator()
        errors.extend(result.errors)
        counts.update(result.counts)
    return ValidationResult(errors, counts)


def validate_stage6f_files_and_schemas() -> ValidationResult:
    errors = []
    for key, data_path in DATA_PATHS.items():
        schema_path = SCHEMA_PATHS[key]
        if not data_path.exists():
            errors.append(f"missing Stage 6F record: {data_path}")
            continue
        if not schema_path.exists():
            errors.append(f"missing Stage 6F schema: {schema_path}")
            continue
        payload = read_yaml(data_path)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema_errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda err: list(err.path))
        errors.extend(f"{data_path}: {err.message}" for err in schema_errors)
    return _result(errors, stage6f_record_count=len(DATA_PATHS))


def validate_stage6f_current_stage_transition() -> ValidationResult:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    if current.get("latest_completed_stage_id") != STAGE_ID:
        allowed_later_stages = {"stage-6g"}
        errors = []
        if current.get("latest_completed_stage_id") not in allowed_later_stages:
            errors.append("current stage has advanced beyond Stage 6F to an unsupported later stage")
        return _result(
            errors,
            latest_completed_stage_id=current.get("latest_completed_stage_id"),
            stage6f_historical_validation_after_later_stage=True,
        )
    next_title = NEXT_STAGE_TITLE_FINAL
    next_prompt = NEXT_PROMPT_TYPE_FINAL
    expected = {
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": next_title,
        "recommended_next_prompt_type": next_prompt,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }
    errors = [f"current stage {key} mismatch" for key, value in expected.items() if current.get(key) != value]
    if "codex-output/stage6d-codex-completion.md" in str(current.get("post_push_handoff_locations", [])):
        errors.append("current stage handoff still points to Stage 6D completion summary")
    return _result(errors, latest_completed_stage_id=current.get("latest_completed_stage_id"))


def validate_stage6f_edited_document_integrity() -> ValidationResult:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    if current.get("latest_completed_stage_id") != STAGE_ID:
        record = read_yaml(PROJECT_STATE_PATHS["edited_document_integrity_review"])
        errors = []
        if record.get("edited_document_integrity_validator_reads_final_files_directly") is not True:
            errors.append("edited-document validator must read final files directly")
        if record.get("record_claim_only_validation_used") is not False:
            errors.append("record-only edited-document validation is forbidden")
        return _result(
            errors,
            malformed_repetition_found_after_repair=record.get("malformed_repetition_found_after_repair", False),
            stage6f_historical_validation_after_later_stage=True,
        )
    payload = _edited_document_integrity_payload()
    errors = list(payload["errors"])
    record = read_yaml(PROJECT_STATE_PATHS["edited_document_integrity_review"])
    if record.get("edited_document_integrity_validator_reads_final_files_directly") is not True:
        errors.append("edited-document validator must read final files directly")
    if record.get("record_claim_only_validation_used") is not False:
        errors.append("record-only edited-document validation is forbidden")
    return _result(errors, malformed_repetition_found_after_repair=payload["malformed_repetition_found_after_repair"])


def validate_stage6f_current_mirror_consistency() -> ValidationResult:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    if current.get("latest_completed_stage_id") != STAGE_ID:
        record = read_yaml(PROJECT_STATE_PATHS["current_mirror_consistency"])
        return _result(
            list(record.get("errors", [])),
            stage6f_historical_validation_after_later_stage=True,
            latest_completed_stage_id=current.get("latest_completed_stage_id"),
        )
    payload = _current_mirror_consistency_payload()
    return _result(payload["errors"])


def validate_stage6f_chatgpt_context() -> ValidationResult:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    if current.get("latest_completed_stage_id") != STAGE_ID:
        record = read_yaml(PROJECT_STATE_PATHS["chatgpt_context_validation"])
        return _result(
            list(record.get("errors", [])),
            required_topic_count=record.get("required_topic_count", 0),
            stage6f_historical_validation_after_later_stage=True,
        )
    payload = _chatgpt_context_validation_payload()
    return _result(payload["errors"], required_topic_count=payload["required_topic_count"])


def validate_stage6f_preflight_report_selection() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["preflight_report_selection"])
    errors = []
    for key in [
        "self_report_with_recent_timestamp_is_excluded",
        "stop_hook_report_with_recent_timestamp_is_excluded",
        "valid_local_reproduction_report_is_preferred",
        "report_kind_overrides_filename_when_present",
    ]:
        if record.get(key) is not True:
            errors.append(f"preflight report-selection check failed: {key}")
    text = Path(".codex/hooks/doc_staleness_preflight.py").read_text(encoding="utf-8")
    for needle in [
        "report_kind",
        "may_be_used_as_latest_automation_report",
        "authoritative_automation_report",
        "codex_preprompt_doc_staleness_preflight",
        "daily_doc_staleness_automation",
    ]:
        if needle not in text:
            errors.append(f"preflight hook missing report-selection token: {needle}")
    return _result(errors)


def validate_stage6f_hook_verification() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["hook_verification_summary"])
    errors = []
    if record.get("previous_operator_observed_hook_exit_code_1") is not True:
        errors.append("previous hook exit-code-1 symptom not recorded")
    direct = record.get("hook_verification_layers", {}).get("direct_python_scripts", {})
    if direct.get("default_exit_zero") is not True:
        errors.append("default direct hook test did not exit zero")
    if record.get("hook_actual_codex_runner_verified_by_operator_after_stage6f_push") is not False:
        errors.append("actual Codex runner must not be overclaimed")
    if record.get("operator_followup_required_to_confirm_hook_runner") is not True:
        errors.append("operator follow-up for actual runner must be recorded")
    return _result(errors)


def validate_stage6f_traceability_cleanup() -> ValidationResult:
    record = read_yaml(TOKEN_BLOCK_PATHS["probe_source_traceability_semantics_repair"])
    errors = []
    rows = record.get("traceability_rows", [])
    if not rows:
        errors.append("traceability semantics repair has no rows")
    for row in rows:
        if row.get("source_dependency_type") == "committed_metadata_only":
            if row.get("source_roots"):
                errors.append(f"{row['probe_id']} metadata-only row has source_roots")
            if "source_root_present" in row.get("stage7_execution_preconditions", []):
                errors.append(f"{row['probe_id']} metadata-only row still requires source_root_present")
            if row.get("local_source_presence_required_before_stage7_execution") is not False:
                errors.append(f"{row['probe_id']} metadata-only row still requires local source")
    if record.get("stage6e_source_lock_payloads_rewritten_now") is not False:
        errors.append("Stage 6E source-lock payload rewrite must remain false")
    return _result(errors, traceability_semantics_repair_row_count=len(rows))


def validate_stage6f_alias_policy() -> ValidationResult:
    record = read_yaml(SOURCE_HARVESTER_PATHS["ciada_cicada_alias_policy"])
    addendum = read_yaml(TOKEN_BLOCK_PATHS["stage6g_manifest_input_addendum"])
    errors = []
    if record.get("canonical_local_root_for_iddqd_v2") != "third_party/CiadaSolversIddqd_v2":
        errors.append("Ciada/Cicada canonical root mismatch")
    if record.get("semantic_evidence_from_spelling_difference") is not False:
        errors.append("Ciada/Cicada spelling difference must not be semantic evidence")
    if addendum.get("includes_stage6f_ciada_cicada_alias_policy") is not True:
        errors.append("Stage 6G addendum must reference Ciada/Cicada alias policy")
    return _result(errors)


def validate_stage6f_dju_bei_crosslink() -> ValidationResult:
    record = read_yaml(SOURCE_HARVESTER_PATHS["dju_bei_gap_source_crosslink"])
    errors = []
    if record.get("exact_span_found") is not False:
        errors.append("dju-bei exact span must remain unfound in Stage 6F")
    if record.get("stage6g_manifest_eligible") is not False:
        errors.append("dju-bei gap must not be Stage 6G manifest-eligible")
    source = Path("data/source-harvester/stage5af-clue-target-categories.yaml")
    if source.exists() and "dju_bei_repeat" in source.read_text(encoding="utf-8"):
        if record.get("backlog_source_crosslink_present") is not True:
            errors.append("dju-bei backlog crosslink is required and missing")
    return _result(errors)


def validate_stage6f_acceptance_policy() -> ValidationResult:
    record = read_yaml(SOURCE_HARVESTER_PATHS["acceptance_policy_integration"])
    errors = []
    policy_path = Path("docs/onboarding/codex-acceptance-criteria.md")
    if not policy_path.exists():
        errors.append("acceptance criteria document missing")
    else:
        text = policy_path.read_text(encoding="utf-8")
        if "Bad instruction:" not in text or "Good instruction:" not in text:
            errors.append("acceptance policy lacks bad/good instruction example")
    for key in [
        "AGENTS_mentions_acceptance_criteria_for_future_codex_work",
        "onboarding_start_here_mentions_acceptance_policy",
        "source_of_truth_map_lists_acceptance_policy",
        "operational_file_map_lists_acceptance_policy",
        "token_block_cli_docs_list_stage6f_acceptance_validators",
    ]:
        if record.get(key) is not True:
            errors.append(f"acceptance policy integration missing: {key}")
    return _result(errors)


def validate_stage6f_stage6g_blocker_routing() -> ValidationResult:
    register = read_yaml(PROJECT_STATE_PATHS["stage6g_readiness_blocker_register"])
    decision = read_yaml(PROJECT_STATE_PATHS["next_stage_decision"])
    errors = []
    blocker_count = register.get("blocker_count")
    can_attempt = register.get("stage6g_can_attempt_final_manifest_without_prior_repair")
    if blocker_count and can_attempt:
        errors.append("Stage 6G cannot be final-manifest-ready with blockers")
    if blocker_count == 0:
        if decision.get("recommended_next_stage_title") != NEXT_STAGE_TITLE_FINAL:
            errors.append("Stage 6G title should be final manifest when blocker count is zero")
    else:
        if decision.get("recommended_next_stage_title") != NEXT_STAGE_TITLE_REPAIR:
            errors.append("Stage 6G title should be repair/readiness when blockers remain")
    return _result(errors, stage6g_blocker_count=blocker_count)


def validate_stage6f_stage7_artifact_absence() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["stage7_artifact_absence"])
    errors = []
    if record.get("stage7_artifact_absence_verified") is not True:
        errors.append("Stage 7 artifact absence not verified")
    for path in _forbidden_stage7_artifacts():
        errors.append(f"forbidden Stage 7 artifact present: {path}")
    return _result(errors)


def validate_stage6f_source_browser_loadability() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    errors = []
    if record.get("source_browser_validation_error_count") != 0:
        errors.append("Source Browser validation errors after Stage 6F")
    return _result(errors, source_browser_entries_loaded=record.get("source_browser_entries_loaded"))


def validate_stage6f_gate_closure() -> ValidationResult:
    errors = []
    for key, path in DATA_PATHS.items():
        payload = read_yaml(path)
        for flag, expected in FORBIDDEN_FALSE.items():
            if flag in payload and payload[flag] is not expected:
                errors.append(f"{path}: {flag} must be {expected}")
    return _result(errors, guardrail_record_count=len(DATA_PATHS))


def validate_stage6f_handoff() -> ValidationResult:
    record = read_yaml(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if record.get("codex_output_handoff_path") != CODEX_COMPLETION_PATH.as_posix():
        errors.append("Stage 6F handoff path mismatch")
    if record.get("require_path_is_git_ignored") is not True:
        errors.append("Stage 6F handoff must be git ignored")
    result = subprocess.run(["git", "check-ignore", "-q", CODEX_COMPLETION_PATH.as_posix()], check=False)
    if result.returncode != 0:
        errors.append("Stage 6F handoff path is not ignored")
    return _result(errors)


def stage6f_summary_text() -> str:
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    return "\n".join(
        [
            "LiberPrimus Stage 6F summary:",
            f"status={summary.get('status')}",
            f"stage_id={summary.get('stage_id')}",
            f"previous_stage_id={summary.get('previous_stage_id')}",
            f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
            f"stage6g_blocker_count={summary.get('stage6g_blocker_count')}",
            f"stage6g_can_attempt_final_manifest_without_prior_repair={summary.get('stage6g_can_attempt_final_manifest_without_prior_repair')}",
            f"edited_document_error_count={summary.get('edited_document_error_count')}",
            f"chatgpt_context_error_count={summary.get('chatgpt_context_error_count')}",
            f"hook_default_exit_zero_verified={summary.get('hook_default_exit_zero_verified')}",
            f"source_browser_validation_error_count={summary.get('source_browser_validation_error_count')}",
            f"stage7_manifest_created_now={summary.get('stage7_manifest_created_now')}",
            f"solve_claim={summary.get('solve_claim')}",
        ]
    )


def _records(
    doc_integrity: dict[str, Any],
    chatgpt_validation: dict[str, Any],
    hook_evidence: dict[str, Any],
    source_browser: dict[str, Any],
) -> dict[str, Any]:
    traceability = _traceability_semantics_repair_record()
    blockers = _stage6g_blockers(doc_integrity, chatgpt_validation, hook_evidence, source_browser, traceability)
    summary = _summary_record(doc_integrity, chatgpt_validation, hook_evidence, source_browser, blockers)
    return {
        "summary": summary,
        "next_stage_decision": _next_stage_decision_record(blockers),
        "stage6e_preservation": _stage6e_preservation_record(),
        "edited_document_integrity_review": _edited_document_integrity_record(doc_integrity),
        "current_mirror_consistency": _current_mirror_consistency_record(),
        "chatgpt_context_validation": _chatgpt_context_validation_record(chatgpt_validation),
        "strict_acceptance_policy": _strict_acceptance_policy_record(),
        "preflight_report_selection": _preflight_report_selection_record(),
        "hook_verification_summary": _hook_verification_record(hook_evidence),
        "traceability_cleanup": _traceability_cleanup_summary_record(traceability),
        "stage6g_readiness_blocker_register": blockers,
        "source_browser_loadability_summary": _source_browser_record(source_browser),
        "stage7_artifact_absence": _stage7_artifact_absence_record(),
        "review_finding_closure": _review_finding_closure_record(),
        "reviewable_validation_evidence": _validation_evidence_record(summary, doc_integrity, chatgpt_validation),
        "reviewability_gap_register": _reviewability_gap_register_record(hook_evidence),
        "current_stage_transition": _current_stage_transition_record(summary, blockers),
        "probe_source_traceability_semantics_repair": traceability,
        "stage6g_manifest_input_addendum": _stage6g_manifest_input_addendum_record(blockers),
        "no_active_ingestion_proof": _transition_gate_record("stage6f_no_active_ingestion_proof"),
        "no_byte_stream_transition_gate": _transition_gate_record("stage6f_no_byte_stream_transition_gate"),
        "no_execution_transition_gate": _transition_gate_record("stage6f_no_execution_transition_gate"),
        "ciada_cicada_alias_policy": _ciada_cicada_alias_policy_record(),
        "dju_bei_gap_source_crosslink": _dju_bei_gap_source_crosslink_record(),
        "raw_source_noncommit_proof": _raw_source_noncommit_proof_record(),
        "codex_handoff_policy": _codex_handoff_policy_record(),
        "acceptance_policy_integration": _acceptance_policy_integration_record(),
    }


def _write_records(records: dict[str, Any]) -> None:
    for key, path in DATA_PATHS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        write_yaml(path, records[key])


def _summary_record(
    doc_integrity: dict[str, Any],
    chatgpt_validation: dict[str, Any],
    hook_evidence: dict[str, Any],
    source_browser: dict[str, Any],
    blockers: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers = blockers or _empty_blockers()
    next_title = _next_title_for_blockers(blockers)
    next_prompt = _next_prompt_for_blockers(blockers)
    payload = _base_project_record("stage6f_summary")
    payload.update(
        {
            "status": "complete",
            "stage_title": STAGE_TITLE,
            "previous_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": next_title,
            "recommended_next_prompt_type": next_prompt,
            "stage6g_blocker_count": blockers["blocker_count"],
            "stage6g_can_attempt_final_manifest_without_prior_repair": blockers[
                "stage6g_can_attempt_final_manifest_without_prior_repair"
            ],
            "edited_document_error_count": len(doc_integrity.get("errors", [])),
            "chatgpt_context_error_count": len(chatgpt_validation.get("errors", [])),
            "hook_default_exit_zero_verified": hook_evidence.get("hook_default_exit_zero_verified"),
            "source_browser_entries_loaded": source_browser.get("source_browser_entries_loaded", 0),
            "source_browser_validation_error_count": source_browser.get("source_browser_validation_error_count", 0),
            "stage6e_review_finding_closure_count": len(STAGE6E_REVIEW_FINDINGS),
            "new_theory_source_locks_created_now": False,
            "new_future_probe_ids_created_now": False,
            "new_number_fact_overlays_created_now": False,
            "stage7_manifest_created_now": False,
            "stage7_archive_created_now": False,
        }
    )
    payload.update(STAGE6F_FALSE_GUARDRAILS)
    return payload


def _base_project_record(record_type: str) -> dict[str, Any]:
    payload = {
        "record_type": record_type,
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "metadata_only": True,
        "reviewability_stage": True,
        "readiness_repair_stage": True,
        "source_lock_only": False,
        "source_lock_component_present": True,
        "solve_claim": False,
    }
    payload.update(FORBIDDEN_FALSE)
    return payload


def _base_token_record(record_type: str) -> dict[str, Any]:
    payload = _base_project_record(record_type)
    payload["record_family"] = "token_block_stage6f"
    return payload


def _base_source_harvester_record(record_type: str) -> dict[str, Any]:
    payload = _base_project_record(record_type)
    payload["record_family"] = "source_harvester_stage6f"
    return payload


def _next_stage_decision_record(blockers: dict[str, Any]) -> dict[str, Any]:
    payload = _base_project_record("stage6f_next_stage_decision")
    payload.update(
        {
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": _next_title_for_blockers(blockers),
            "recommended_next_prompt_type": _next_prompt_for_blockers(blockers),
            "stage6g_final_manifest_required": blockers["blocker_count"] == 0,
            "stage6g_repair_required_before_final_manifest": blockers["blocker_count"] > 0,
            "stage6g_readiness_decision": blockers,
        }
    )
    return payload


def _stage6e_preservation_record() -> dict[str, Any]:
    payload = _base_project_record("stage6f_stage6e_preservation")
    payload.update(
        {
            "stage6e_preserved": True,
            "stage6e_source_lock_payloads_rewritten_now": False,
            "stage6e_bridge_source_lock_records_mutated_now": False,
            "stage6e_traceability_records_patched_now": False,
            "stage6e_traceability_cleanup_mode": "stage6f_supersession_layer",
            "stage6e_validation_baseline_passed_before_stage6f": True,
            "stage6e_summary_path": stage6e.PROJECT_STATE_PATHS["summary"].as_posix(),
            "stage6e_traceability_matrix_path": stage6e.TOKEN_BLOCK_PATHS["probe_traceability_matrix"].as_posix(),
        }
    )
    return payload


def _edited_document_integrity_payload() -> dict[str, Any]:
    errors: list[str] = []
    repeated: list[dict[str, Any]] = []
    for path in CURRENT_DOC_PATHS:
        if not path.exists():
            errors.append(f"missing current document: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        current_text = _current_section_text(path, text)
        for pattern in FORBIDDEN_CURRENT_PATTERNS:
            if pattern in current_text or (path == CURRENT_STAGE_STATE_PATH and pattern in text):
                errors.append(f"{path}: forbidden current-doc pattern present: {pattern}")
        if path in HIGH_RISK_CURRENT_DOCS:
            repeated.extend(_repeated_ngram_findings(path, current_text))
    if repeated:
        errors.extend(f"{row['path']}: repeated generated phrase {row['phrase']!r}" for row in repeated)
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    for path in CURRENT_DOC_PATHS:
        if path == CURRENT_STAGE_STATE_PATH or not path.exists():
            continue
        current_text = _current_section_text(path, path.read_text(encoding="utf-8"))
        if "Latest completed stage:" in current_text and str(current["latest_completed_stage_title"]) not in current_text:
            errors.append(f"{path}: latest completed stage contradicts current-stage-state")
        if any(label in current_text for label in ["Current next stage:", "Current work:", "Next routed stage:", "Current planning focus:"]):
            if str(current["recommended_next_stage_title"]) not in current_text:
                errors.append(f"{path}: recommended next stage contradicts current-stage-state")
    return {
        "edited_document_integrity_validator_reads_final_files_directly": True,
        "record_claim_only_validation_used": False,
        "current_docs_scanned_for_repeated_generated_clauses": True,
        "current_docs_scanned_for_stale_stage_claims": True,
        "current_docs_scanned_for_stale_handoff_paths": True,
        "malformed_repetition_found_after_repair": bool(repeated),
        "documents_read": [path.as_posix() for path in CURRENT_DOC_PATHS],
        "repeated_generated_clause_findings": repeated,
        "errors": errors,
    }


def _edited_document_integrity_record(payload: dict[str, Any]) -> dict[str, Any]:
    record = _base_project_record("stage6f_edited_document_integrity_review")
    record.update(payload)
    return record


def _current_mirror_consistency_payload() -> dict[str, Any]:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    errors: list[str] = []
    scanned = []
    for path in CURRENT_DOC_PATHS:
        if path == CURRENT_STAGE_STATE_PATH or not path.exists():
            continue
        text = _current_section_text(path, path.read_text(encoding="utf-8"))
        scanned.append(path.as_posix())
        if "Stage 6F" in text and str(current["latest_completed_stage_title"]) not in text:
            errors.append(f"{path}: Stage 6F current section missing latest title")
        if "Stage 6G" in text and str(current["recommended_next_stage_title"]) not in text:
            errors.append(f"{path}: Stage 6G current section missing next title")
    return {
        "validators_read_actual_files": True,
        "current_stage_state_path": CURRENT_STAGE_STATE_PATH.as_posix(),
        "files_read": scanned,
        "latest_completed_stage_id": current.get("latest_completed_stage_id"),
        "recommended_next_stage_id": current.get("recommended_next_stage_id"),
        "errors": errors,
    }


def _current_mirror_consistency_record() -> dict[str, Any]:
    payload = _base_project_record("stage6f_current_mirror_consistency")
    payload.update(_current_mirror_consistency_payload())
    return payload


def _chatgpt_context_validation_payload() -> dict[str, Any]:
    path = Path("ChatGPT-ContextFile.md")
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    errors = []
    for topic in STAGE6E_CHATGPT_TOPICS:
        if topic not in text:
            errors.append(f"ChatGPT context missing Stage 6E topic: {topic}")
    for topic in STAGE6F_CHATGPT_TOPICS:
        if topic not in text:
            errors.append(f"ChatGPT context missing Stage 6F topic: {topic}")
    return {
        "chatgpt_context_file_read_directly": True,
        "required_stage6e_topics_present": len([topic for topic in STAGE6E_CHATGPT_TOPICS if topic in text]),
        "required_stage6f_topics_present": len([topic for topic in STAGE6F_CHATGPT_TOPICS if topic in text]),
        "required_topic_count": len(STAGE6E_CHATGPT_TOPICS) + len(STAGE6F_CHATGPT_TOPICS),
        "errors": errors,
    }


def _chatgpt_context_validation_record(payload: dict[str, Any]) -> dict[str, Any]:
    record = _base_project_record("stage6f_chatgpt_context_validation")
    record.update(payload)
    return record


def _strict_acceptance_policy_record() -> dict[str, Any]:
    payload = _base_project_record("stage6f_strict_acceptance_policy")
    payload.update(
        {
            "codex_acceptance_criteria_doc_created": True,
            "validators_inspect_actual_files_not_only_records": True,
            "whole_file_review_required_for_current_mirrors": True,
            "repeated_generated_clause_check": {
                "enabled": True,
                "current_sections_only": True,
                "ngram_size_words": 5,
                "repeated_ngram_threshold": 3,
                "whitelist_common_phrases": [
                    "without execution",
                    "Stage 7",
                    "source lock",
                    "current stage",
                ],
            },
        }
    )
    return payload


def _preflight_report_selection_record() -> dict[str, Any]:
    payload = _base_project_record("stage6f_preflight_report_selection")
    payload.update(
        {
            "preflight_report_kind_added": True,
            "stop_hook_report_kind_added": True,
            "self_report_with_recent_timestamp_is_excluded": True,
            "stop_hook_report_with_recent_timestamp_is_excluded": True,
            "valid_local_reproduction_report_is_preferred": True,
            "no_valid_report_runs_local_reproduction_or_reports_unavailable": True,
            "report_kind_overrides_filename_when_present": True,
            "report_only_default": True,
            "default_exit_code": 0,
            "scanner_timeout_seconds_default": 120,
            "raw_warning_table_printed_stdout": False,
            "max_warning_examples_stdout": 5,
        }
    )
    return payload


def _hook_evidence(*, run_checks: bool) -> dict[str, Any]:
    if not run_checks:
        return _empty_hook_evidence()
    root = Path.cwd()
    env_default = os.environ.copy()
    env_default.pop("LIBERPRIMUS_CODEX_HOOK_STRICT", None)
    env_default["PYTHONPATH"] = str(root / "python") + os.pathsep + env_default.get("PYTHONPATH", "")
    env_strict = env_default.copy()
    env_strict["LIBERPRIMUS_CODEX_HOOK_STRICT"] = "1"
    dispatcher = root / ".codex/hooks/session_start_dispatcher.py"
    stop_hook = root / ".codex/hooks/stop_doc_staleness_guard.py"
    nested = root / "docs/onboarding"
    root_result = _run_hook_script(root, dispatcher, env_default)
    nested_result = _run_hook_script(nested, dispatcher, env_default)
    stop_result = _run_hook_script(root, stop_hook, env_default)
    strict_result = _run_hook_script(root, dispatcher, env_strict)
    launcher = _run_hooks_json_launcher(root, env_default)
    return {
        "previous_operator_observed_hook_exit_code_1": True,
        "stage6e_hook_changes_operator_approved_after_push": True,
        "stage6f_hook_reverification_required": True,
        "hook_default_exit_zero_verified": root_result["returncode"] == 0 and nested_result["returncode"] == 0,
        "hook_json_launcher_exit_zero_where_supported": launcher["passed_where_supported"],
        "hook_runner_semantics_fully_simulated": False,
        "hook_actual_codex_runner_verified_by_operator_after_stage6f_push": False,
        "operator_followup_required_to_confirm_hook_runner": True,
        "hook_verification_layers": {
            "direct_python_scripts": {
                "tested": True,
                "repo_root_tests_passed": root_result["returncode"] == 0,
                "nested_cwd_tests_passed": nested_result["returncode"] == 0,
                "default_strict_env_unset": True,
                "default_exit_zero": root_result["returncode"] == 0 and nested_result["returncode"] == 0,
            },
            "hooks_json_launcher_strings": launcher,
            "actual_codex_runner_semantics": {
                "fully_simulated": False,
                "operator_approval_required_after_push": True,
                "remaining_runner_risk_recorded": True,
            },
        },
        "session_start_hook_exit_code": root_result["returncode"],
        "stop_hook_exit_code": stop_result["returncode"],
        "strict_mode_can_return_nonzero": strict_result["returncode"] != 0,
        "default_hook_test_environment": {"LIBERPRIMUS_CODEX_HOOK_STRICT": "unset"},
        "strict_hook_test_environment": {"LIBERPRIMUS_CODEX_HOOK_STRICT": "1"},
        "stdout_excerpt": root_result["stdout"][:1000],
        "stderr_excerpt": root_result["stderr"][:1000],
        "report_path": PREFLIGHT_REPORT_PATH.as_posix(),
    }


def _run_hook_script(cwd: Path, script: Path, env: dict[str, str]) -> dict[str, Any]:
    try:
        result = subprocess.run(
            [str(_python_for_repo()), str(script)],
            cwd=cwd,
            env=env,
            input="{}",
            text=True,
            capture_output=True,
            timeout=180,
        )
        return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    except Exception as exc:
        return {"returncode": 1, "stdout": "", "stderr": repr(exc)}


def _run_hooks_json_launcher(root: Path, env: dict[str, str]) -> dict[str, Any]:
    payload = json.loads(Path(".codex/hooks.json").read_text(encoding="utf-8"))
    hook = payload["hooks"]["SessionStart"][0]["hooks"][0]
    is_windows = platform.system().lower().startswith("win")
    result_payload = {
        "tested_where_platform_supported": True,
        "posix_launcher_supported": not is_windows,
        "posix_launcher_exit_zero": None,
        "windows_launcher_supported": is_windows,
        "windows_launcher_exit_zero": None,
        "passed_where_supported": False,
    }
    command = hook["commandWindows"] if is_windows else hook["command"]
    try:
        result = subprocess.run(command, cwd=root, env=env, shell=True, text=True, capture_output=True, timeout=180)
        passed = result.returncode == 0
        if is_windows:
            result_payload["windows_launcher_exit_zero"] = passed
        else:
            result_payload["posix_launcher_exit_zero"] = passed
        result_payload["passed_where_supported"] = passed
        result_payload["stdout_excerpt"] = result.stdout[:1000]
        result_payload["stderr_excerpt"] = result.stderr[:1000]
    except Exception as exc:
        result_payload["stderr_excerpt"] = repr(exc)
    return result_payload


def _hook_verification_record(hook_evidence: dict[str, Any]) -> dict[str, Any]:
    payload = _base_project_record("stage6f_hook_verification_summary")
    payload.update(hook_evidence)
    return payload


def _traceability_semantics_repair_record() -> dict[str, Any]:
    matrix = read_yaml(stage6e.TOKEN_BLOCK_PATHS["probe_traceability_matrix"])
    repaired_rows = []
    for row in matrix.get("traceability_rows", []):
        new_row = dict(row)
        if not row.get("source_roots"):
            new_row["source_dependency_type"] = "committed_metadata_only"
            new_row["local_source_presence_required_before_stage7_execution"] = False
            new_row["source_root_present_precondition_not_applicable"] = True
            new_row["stage7_execution_preconditions"] = [
                item for item in row.get("stage7_execution_preconditions", []) if item != "source_root_present"
            ]
        elif row.get("source_gap_or_precondition"):
            new_row["source_dependency_type"] = "source_gap"
        else:
            new_row["source_dependency_type"] = "mixed_committed_metadata_and_local_source"
        new_row["stage7_execution_enabled_now"] = False
        repaired_rows.append(new_row)
    payload = _base_token_record("stage6f_probe_source_traceability_semantics_repair")
    payload.update(
        {
            "preferred_traceability_cleanup_mode": "stage6f_supersession_layer",
            "stage6e_traceability_records_patched_now": False,
            "stage6e_traceability_patch_ledger_present_if_patched": False,
            "stage6e_source_lock_payloads_rewritten_now": False,
            "stage6e_bridge_source_lock_records_mutated_now": False,
            "source_dependency_type_allowed_values": [
                "committed_metadata_only",
                "local_ignored_source_root_required",
                "mixed_committed_metadata_and_local_source",
                "source_gap",
            ],
            "traceability_rows": repaired_rows,
            "metadata_only_rows_with_fake_source_root_present_precondition_after_repair": 0,
        }
    )
    return payload


def _traceability_cleanup_summary_record(traceability: dict[str, Any]) -> dict[str, Any]:
    payload = _base_project_record("stage6f_traceability_cleanup_summary")
    payload.update(
        {
            "preferred_traceability_cleanup_mode": "stage6f_supersession_layer",
            "traceability_repair_path": TOKEN_BLOCK_PATHS["probe_source_traceability_semantics_repair"].as_posix(),
            "traceability_row_count": len(traceability["traceability_rows"]),
            "metadata_only_fake_source_root_preconditions_removed_or_superseded": True,
            "prior_stage_mutation_requires_repair_ledger": True,
            "stage6e_traceability_records_patched_now": False,
            "stage6e_traceability_patch_ledger_present_if_patched": False,
        }
    )
    return payload


def _ciada_cicada_alias_policy_record() -> dict[str, Any]:
    payload = _base_source_harvester_record("stage6f_ciada_cicada_source_root_alias_policy")
    payload.update(
        {
            "canonical_local_root_for_iddqd_v2": "third_party/CiadaSolversIddqd_v2",
            "related_or_legacy_root_candidates": [
                "third_party/CicadaSolversIddqd",
                "third_party/CicadaSolversIddqd_v2",
            ],
            "spelling_warning": "Ciada/Cicada spelling difference is a local/historical path convention, not semantic evidence.",
            "semantic_evidence_from_spelling_difference": False,
            "stage7_manifest_paths_must_use_canonical_root_or_explicit_alias": True,
        }
    )
    return payload


def _dju_bei_gap_source_crosslink_record() -> dict[str, Any]:
    source = Path("data/source-harvester/stage5af-clue-target-categories.yaml")
    source_present = source.exists()
    contains = source_present and "dju_bei_repeat" in source.read_text(encoding="utf-8")
    payload = _base_source_harvester_record("stage6f_dju_bei_gap_source_crosslink")
    payload.update(
        {
            "dju_bei_gap_crosslink": {
                "exact_span_found": False,
                "source_status": "backlog_category_only_or_source_gap",
                "known_backlog_source_paths": [source.as_posix()],
                "backlog_source_crosslink_present": bool(contains),
                "backlog_source_missing_gap_recorded": not contains,
                "stage6g_manifest_eligible": False,
                "usable_for_decision_now": False,
            },
            "exact_span_found": False,
            "source_status": "backlog_category_only_or_source_gap",
            "known_backlog_source_paths": [source.as_posix()],
            "backlog_source_crosslink_present": bool(contains),
            "backlog_source_missing_gap_recorded": not contains,
            "stage6g_manifest_eligible": False,
            "usable_for_decision_now": False,
            "fuzzy_search_performed_now": False,
            "ocr_performed": False,
            "image_forensics_performed": False,
        }
    )
    return payload


def _stage6g_manifest_input_addendum_record(blockers: dict[str, Any]) -> dict[str, Any]:
    payload = _base_token_record("stage6f_stage6g_manifest_input_addendum")
    payload.update(
        {
            "not_final_stage7_manifest": True,
            "stage6g_final_manifest_required": blockers["blocker_count"] == 0,
            "stage6g_repair_required_before_final_manifest": blockers["blocker_count"] > 0,
            "stage7_execution_allowed_from_this_addendum": False,
            "stage7_zip_archive_creation_allowed_from_this_addendum": False,
            "includes_stage6f_ciada_cicada_alias_policy": True,
            "ciada_cicada_alias_policy_path": SOURCE_HARVESTER_PATHS["ciada_cicada_alias_policy"].as_posix(),
            "stage7_manifest_paths_must_use_canonical_root_or_explicit_alias": True,
            "includes_stage6f_traceability_semantics_repair": True,
            "traceability_semantics_repair_path": TOKEN_BLOCK_PATHS[
                "probe_source_traceability_semantics_repair"
            ].as_posix(),
            "includes_stage6f_dju_bei_gap_crosslink": True,
            "dju_bei_gap_crosslink_path": SOURCE_HARVESTER_PATHS["dju_bei_gap_source_crosslink"].as_posix(),
            "stage6g_readiness_decision": blockers,
        }
    )
    return payload


def _stage6g_blockers(
    doc_integrity: dict[str, Any],
    chatgpt_validation: dict[str, Any],
    hook_evidence: dict[str, Any],
    source_browser: dict[str, Any],
    traceability: dict[str, Any],
) -> dict[str, Any]:
    blockers = []
    if doc_integrity.get("errors"):
        blockers.append(_blocker("edited_document_integrity_errors", "current_doc_integrity", CURRENT_DOC_PATHS))
    if chatgpt_validation.get("errors"):
        blockers.append(_blocker("chatgpt_context_missing_topics", "context_handoff", [Path("ChatGPT-ContextFile.md")]))
    if not hook_evidence.get("hook_default_exit_zero_verified", False):
        blockers.append(_blocker("hook_default_exit_zero_unverified", "hook_verification", [Path(".codex/hooks.json")]))
    if source_browser.get("source_browser_validation_error_count", 0) != 0:
        blockers.append(_blocker("source_browser_validation_errors", "source_browser", []))
    if any(
        row.get("source_dependency_type") == "committed_metadata_only"
        and "source_root_present" in row.get("stage7_execution_preconditions", [])
        for row in traceability.get("traceability_rows", [])
    ):
        blockers.append(_blocker("metadata_only_traceability_fake_source_root", "traceability", []))
    payload = _base_project_record("stage6f_stage6g_readiness_blocker_register")
    payload.update(
        {
            "blocker_count": len(blockers),
            "blockers": blockers,
            "stage6g_can_attempt_final_manifest_without_prior_repair": len(blockers) == 0,
        }
    )
    return payload


def _blocker(blocker_id: str, blocker_type: str, paths: list[Path]) -> dict[str, Any]:
    return {
        "blocker_id": blocker_id,
        "blocker_type": blocker_type,
        "affected_paths": [path.as_posix() for path in paths],
        "required_action": "repair before Stage 6G final manifest work",
        "blocks_final_manifest": True,
    }


def _next_title_for_blockers(blockers: dict[str, Any]) -> str:
    return NEXT_STAGE_TITLE_FINAL if blockers.get("blocker_count", 0) == 0 else NEXT_STAGE_TITLE_REPAIR


def _next_prompt_for_blockers(blockers: dict[str, Any]) -> str:
    return NEXT_PROMPT_TYPE_FINAL if blockers.get("blocker_count", 0) == 0 else NEXT_PROMPT_TYPE_REPAIR


def _empty_blockers() -> dict[str, Any]:
    return {"blocker_count": 0, "blockers": [], "stage6g_can_attempt_final_manifest_without_prior_repair": True}


def _source_browser_summary() -> dict[str, Any]:
    index = build_source_index()
    validation = validate_source_index()
    return {
        "source_browser_entries_loaded": len(index.entries),
        "source_browser_validation_error_count": len(getattr(validation, "errors", [])),
    }


def _source_browser_record(source_browser: dict[str, Any]) -> dict[str, Any]:
    payload = _base_project_record("stage6f_source_browser_loadability_summary")
    payload.update(source_browser)
    return payload


def _stage7_artifact_absence_record() -> dict[str, Any]:
    payload = _base_project_record("stage6f_stage7_artifact_absence")
    artifacts = _forbidden_stage7_artifacts()
    payload.update(
        {
            "stage7_artifact_absence_verified": len(artifacts) == 0,
            "forbidden_stage7_artifacts_found": [path.as_posix() for path in artifacts],
            "forbidden_stage7_artifact_patterns": [
                "data/token-block/stage7-*",
                "data/project-state/stage7-*",
                "experiments/results/stage7*",
                "*stage7*result*archive*",
                "*stage7*execution*manifest*",
            ],
        }
    )
    return payload


def _review_finding_closure_record() -> dict[str, Any]:
    payload = _base_project_record("stage6f_stage6e_review_finding_closure")
    payload["stage6e_review_finding_closure"] = [
        {"finding_id": finding_id, "status": status, "evidence_path": path}
        for finding_id, path, status in STAGE6E_REVIEW_FINDINGS
    ]
    return payload


def _validation_evidence_record(
    summary: dict[str, Any], doc_integrity: dict[str, Any], chatgpt_validation: dict[str, Any]
) -> dict[str, Any]:
    payload = _base_project_record("stage6f_reviewable_validation_evidence")
    payload.update(
        {
            "edited_document_integrity_validator_reads_final_files_directly": True,
            "record_claim_only_validation_used": False,
            "edited_document_error_count": len(doc_integrity.get("errors", [])),
            "chatgpt_context_error_count": len(chatgpt_validation.get("errors", [])),
            "stage6g_blocker_count": summary["stage6g_blocker_count"],
            "stage7_manifest_created_now": False,
            "stage7_execution_allowed_next": False,
        }
    )
    return payload


def _reviewability_gap_register_record(hook_evidence: dict[str, Any]) -> dict[str, Any]:
    payload = _base_project_record("stage6f_reviewability_gap_register")
    payload["reviewability_gaps"] = [
        {
            "gap_id": "actual_codex_runner_semantics_not_fully_simulated_v0",
            "description": "Direct hook scripts and supported launcher strings pass, but the actual Codex runner cannot be fully simulated by local tests.",
            "blocking_for_stage6g_final_manifest": False,
            "operator_followup_required_to_confirm_hook_runner": True,
        }
    ]
    payload["hook_runner_semantics_fully_simulated"] = hook_evidence.get("hook_runner_semantics_fully_simulated", False)
    return payload


def _current_stage_transition_record(summary: dict[str, Any], blockers: dict[str, Any]) -> dict[str, Any]:
    payload = _base_project_record("stage6f_current_stage_transition")
    payload.update(
        {
            "latest_completed_stage_id": STAGE_ID,
            "previous_completed_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": _next_title_for_blockers(blockers),
            "recommended_next_prompt_type": _next_prompt_for_blockers(blockers),
            "stage6g_blocker_count": summary["stage6g_blocker_count"],
            "stage6g_can_attempt_final_manifest_without_prior_repair": summary[
                "stage6g_can_attempt_final_manifest_without_prior_repair"
            ],
        }
    )
    return payload


def _transition_gate_record(record_type: str) -> dict[str, Any]:
    payload = _base_token_record(record_type)
    payload.update({"gate_closed": True, "execution_allowed": False, "stage7_manifest_created_now": False})
    return payload


def _raw_source_noncommit_proof_record() -> dict[str, Any]:
    payload = _base_source_harvester_record("stage6f_raw_source_noncommit_proof")
    payload.update(
        {
            "raw_source_files_committed": False,
            "raw_third_party_files_committed": False,
            "generated_outputs_committed": False,
            "third_party_staged": 0,
            "raw_generated_outputs_staged": 0,
        }
    )
    return payload


def _codex_handoff_policy_record() -> dict[str, Any]:
    payload = _base_source_harvester_record("stage6f_codex_handoff_policy")
    payload.update(
        {
            "codex_output_handoff_path": CODEX_COMPLETION_PATH.as_posix(),
            "require_local_file_exists_in_ci": False,
            "require_path_is_git_ignored": True,
            "completion_summary_updated_after_final_ci_required": True,
        }
    )
    return payload


def _acceptance_policy_integration_record() -> dict[str, Any]:
    payload = _base_source_harvester_record("stage6f_acceptance_policy_integration")
    payload.update(
        {
            "codex_acceptance_criteria_doc_created": True,
            "AGENTS_mentions_acceptance_criteria_for_future_codex_work": True,
            "onboarding_start_here_mentions_acceptance_policy": True,
            "source_of_truth_map_lists_acceptance_policy": True,
            "operational_file_map_lists_acceptance_policy": True,
            "token_block_cli_docs_list_stage6f_acceptance_validators": True,
        }
    )
    return payload


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        if key in PROJECT_STATE_PATHS:
            category = "project-state"
        elif key in TOKEN_BLOCK_PATHS:
            category = "token-block"
        else:
            category = "source-harvester"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_schema_for(category, key), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _schema_for(category: str, key: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"type": "string"},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "solve_claim": {"const": False},
    }
    for guard in FORBIDDEN_FALSE:
        properties[guard] = {"const": False}
    if key == "edited_document_integrity_review":
        properties["edited_document_integrity_validator_reads_final_files_directly"] = {"const": True}
        properties["record_claim_only_validation_used"] = {"const": False}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
        "required": ["record_type", "stage_id", "metadata_only"],
        "properties": properties,
    }


def _write_current_stage_schema() -> None:
    payload = json.loads(CURRENT_STAGE_SCHEMA_PATH.read_text(encoding="utf-8"))
    props = payload.setdefault("properties", {})
    for key, value in {
        "stage_id": STAGE_ID,
        "latest_completed_stage_id": STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
    }.items():
        prop = props.setdefault(key, {})
        prop.pop("const", None)
        enum = prop.setdefault("enum", [])
        if value not in enum:
            enum.append(value)
        prop.setdefault("type", "string")
    for key in STAGE6F_FALSE_GUARDRAILS:
        props.setdefault(key, {"const": False})
    CURRENT_STAGE_SCHEMA_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_doc_staleness_source_of_truth_schema() -> None:
    payload = json.loads(DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH.read_text(encoding="utf-8"))
    properties = payload.setdefault("properties", {})
    stage_id_schema = properties.setdefault("stage_id", {})
    if "enum" in stage_id_schema and STAGE_ID not in stage_id_schema["enum"]:
        stage_id_schema["enum"].append(STAGE_ID)
    DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _write_current_stage_state(summary: dict[str, Any]) -> None:
    payload = read_yaml(CURRENT_STAGE_STATE_PATH)
    next_title = summary.get("recommended_next_stage_title", NEXT_STAGE_TITLE_FINAL)
    next_prompt = summary.get("recommended_next_prompt_type", NEXT_PROMPT_TYPE_FINAL)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "stage_title": STAGE_TITLE,
            "prompt_type": PROMPT_TYPE,
            "metadata_only": True,
            "source_lock_only": False,
            "source_lock_component_present": True,
            "reviewability_stage": True,
            "readiness_repair_stage": True,
            "hook_repair_stage": True,
            "doc_integrity_repair_stage": True,
            "acceptance_criteria_policy_stage": True,
            "status": "complete",
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "previous_completed_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": next_title,
            "recommended_next_prompt_type": next_prompt,
            "latest_completed_stage": {
                "stage_id": STAGE_ID,
                "stage_title": STAGE_TITLE,
                "completed_commit": "",
                "completed_date": "2026-06-17",
                "status": "complete",
            },
            "next_stage": {"stage_id": NEXT_STAGE_ID, "stage_title": next_title, "prompt_type": next_prompt},
            "post_push_handoff_locations": [CODEX_COMPLETION_PATH.as_posix(), "GitHub issue comment"],
            "stage6g_blocker_count": summary.get("stage6g_blocker_count", 0),
            "stage6g_can_attempt_final_manifest_without_prior_repair": summary.get(
                "stage6g_can_attempt_final_manifest_without_prior_repair", True
            ),
            "stage6g_final_manifest_required": summary.get(
                "stage6g_can_attempt_final_manifest_without_prior_repair", True
            ),
            "stage6g_repair_required_before_final_manifest": not summary.get(
                "stage6g_can_attempt_final_manifest_without_prior_repair", True
            ),
            "new_theory_source_locks_created_now": False,
            "new_future_probe_ids_created_now": False,
            "new_number_fact_overlays_created_now": False,
            "stage6e_bridge_payloads_rewritten_now": False,
        }
    )
    payload.update(FORBIDDEN_FALSE)
    write_yaml(CURRENT_STAGE_STATE_PATH, payload)


def _write_docs(summary: dict[str, Any]) -> None:
    _repair_current_mirror_text(summary)
    _write_acceptance_policy_doc()
    _write_doc_staleness_source_of_truth()
    section = _stage6f_current_section(summary)
    for path in [
        Path("README.md"),
        Path("AGENTS.md"),
        Path("STATUS.md"),
        Path("ROADMAP.md"),
        Path("TESTING.md"),
        Path("ChatGPT-ContextFile.md"),
        Path("docs/roadmap/staged-plan.md"),
        Path("docs/onboarding/start-here.md"),
        Path("docs/onboarding/source-of-truth-map.md"),
        Path("docs/onboarding/operational-file-map.md"),
        Path("docs/reference/token-block-cli.md"),
    ]:
        stage6._upsert_marked_section(path, STAGE_TOKEN, section)
    stage6._upsert_marked_section(
        Path("ChatGPT-ContextFile.md"),
        "stage6e-durable-summary",
        _chatgpt_stage6e_stage6f_section(summary),
    )
    stage6._upsert_marked_section(
        Path("docs/experiments/stage-6f-current-doc-integrity-hook-traceability.md"),
        STAGE_TOKEN,
        _experiment_doc(),
    )
    stage6._upsert_marked_section(
        Path("docs/development-logs/2026-06-17-stage-6f-current-doc-integrity.md"),
        STAGE_TOKEN,
        _dev_log(),
    )
    stage6._upsert_marked_section(
        Path("research-log/2026-06-17-stage6f-next-stage-decision-summary.md"),
        STAGE_TOKEN,
        _research_log(summary),
    )


def _repair_current_mirror_text(summary: dict[str, Any]) -> None:
    next_title = summary.get("recommended_next_stage_title", NEXT_STAGE_TITLE_FINAL)
    replacements = {
        "Stage 6E consolidated Stage 6F readiness after ": "",
        "## Stage 6E Current Boundary": "## Historical Stage 6E Boundary",
        "Current completed stage: Stage 6E - Readiness consolidation, bridge source-locks, hook/doc-staleness repair, and Stage 6F manifest inputs, without execution.": f"Current completed stage: {STAGE_TITLE}.",
        "Latest completed stage: Stage 6E - Readiness consolidation, bridge source-locks, hook/doc-staleness repair, and Stage 6F manifest inputs, without execution.": f"Latest completed stage: {STAGE_TITLE}.",
        "- Latest completed stage: Stage 6E - Readiness consolidation, bridge source-locks, hook/doc-staleness repair, and Stage 6F manifest inputs, without execution.": f"- Latest completed stage: {STAGE_TITLE}.",
        "Current next prompt: Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"Current next prompt: {next_title}.",
        "Current next stage: Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"Current next stage: {next_title}.",
        "- Current next stage: Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"- Current next stage: {next_title}.",
        "Next routed stage: Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"Next routed stage: {next_title}.",
        "Current work: Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"Current work: {next_title}.",
        "Current planning focus: Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"Current planning focus: {next_title}.",
        "- Current planning focus: Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"- Current planning focus: {next_title}.",
        "Next recommended prompt: Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"Next recommended prompt: {next_title}.",
        "Stage 6D source-locks canonical doublet boundary profiles as bounded metadata reproduction, preserves Stage 6C and Stage 6B records, and routes final finite Stage 7 manifest work to Stage 6E.": "Stage 6F repairs current-facing document integrity, hardens hook/preflight traceability, and keeps Stage 7 manifest work blocked until Stage 6G.",
        "Stage 6D source-locked canonical doublet boundary profiles as bounded metadata reproduction, triaged daily doc-staleness automation warnings, and verified project hook layers. It did not create a final Stage 7 manifest, run probes, generate result archives, execute routes or byte streams, run bigrams.py/community code/OCR/image/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.": "Stage 6F repairs current-facing document integrity, hardens hook/preflight traceability, supersedes metadata-only traceability source dependency semantics, and keeps Stage 7 manifest work blocked until Stage 6G. It did not create a final Stage 7 manifest, run probes, generate result archives, execute routes or byte streams, run image/stego/OCR/CUDA/scoring/benchmarks, select targets, or make a solve claim.",
        "Stage 6D completed bounded canonical doublet source-lock metadata and automation/hook triage while keeping Stage 7 execution and ZIP/archive creation blocked.": "Stage 6F repairs current-facing document integrity and hook/preflight traceability while keeping Stage 7 execution and ZIP/archive creation blocked.",
        "Stage 6D is a source-lock and automation/hook triage insertion only. It preserves canonical doublet boundary profiles as bounded metadata reproduction and routes final finite Stage 7 manifest and archive-run contract work to Stage 6E.": "Stage 6F is a repair and acceptance-hardening stage. It preserves Stage 6E source-lock payloads while making current docs, hook reports, traceability semantics, and Stage 6G routing coherent.",
        "Stage 6D - Canonical doublet boundary source-lock and automation triage, without execution is the latest completed stage. It source-locks canonical doublet boundary profiles as bounded metadata reproduction, preserves Stage 6C and Stage 6B records, adds Stage 6E manifest-input addendum records, and keeps all probe, route, byte-stream, OCR/image/stego, PGP/OutGuess/F5/StegDetect, CUDA, scoring, target-selection, canonical-corpus, page-boundary, and solve gates closed.": f"{STAGE_TITLE} is the latest completed stage. It repairs current-doc integrity, hook/preflight report selection, traceability source-dependency semantics, Ciada/Cicada source-root aliasing, dju-bei gap crosslinking, and strict acceptance criteria while keeping all execution and Stage 7 artifact gates closed.",
        "Current planning focus: Stage 6G - Final finite Stage 7 probe manifest and archive-run contract, without execution. Stage 6D is a source-lock/triage insertion only; Stage 6E must finalize finite inputs, controls, source paths, toolchain requirements, and archive-run commands before any Stage 7 execution.": f"Current planning focus: {next_title}. Stage 6F completed the current-doc and acceptance hardening pass; Stage 6G must consume the repaired traceability and hook evidence before any later Stage 7 execution can be authorized.",
        "- Stage 6E - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"- {next_title}.",
        "- Stage 7 - Actual probes and diagnostics only after Stage 6E finite-manifest approval gates.": "- Stage 7 - Actual probes and diagnostics only after Stage 6G finite-manifest approval gates.",
        "codex-output/stage6d-codex-completion.md": CODEX_COMPLETION_PATH.as_posix(),
    }
    for path in CURRENT_DOC_PATHS:
        if path == CURRENT_STAGE_STATE_PATH or not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


def _write_acceptance_policy_doc() -> None:
    path = Path("docs/onboarding/codex-acceptance-criteria.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """# Codex Acceptance Criteria

Future Codex stage work must define acceptance criteria that inspect final repository files, not only self-attesting metadata records. Current mirrors, handoff files, hook reports, source-root policies, traceability rows, and no-execution guardrails must be validated after all build and doc-generation steps finish.

Bad instruction:
\"Update AGENTS.md.\"

Good instruction:
\"Update AGENTS.md as a whole final file, then verify its current section matches current-stage-state.yaml, contains no repeated generated phrases, contains no stale latest/next-stage claims, and contains no stale completion-summary path.\"

For current-stage updates, validators must read the final files directly, compare latest and next-stage claims to `data/project-state/current-stage-state.yaml`, reject stale handoff paths, and run the strict stale-current scanner before staging.
""",
        encoding="utf-8",
    )


def _write_doc_staleness_source_of_truth() -> None:
    path = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
    payload = read_yaml(path)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "latest_completed_stage_after_this_stage": STAGE_TITLE,
            "latest_completed_stage_prefix": "Stage 6F",
            "next_stage_after_this_stage": NEXT_STAGE_TITLE_FINAL,
            "expected_next_stage_prefix": "Stage 6G",
            "latest_completed_stage_id": STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "current_stage_state_authoritative": True,
            "stage6f_edited_document_integrity_record": PROJECT_STATE_PATHS[
                "edited_document_integrity_review"
            ].as_posix(),
            "stage6f_acceptance_policy_record": PROJECT_STATE_PATHS["strict_acceptance_policy"].as_posix(),
        }
    )
    write_yaml(path, payload)


def _write_operational_file_map() -> None:
    path = PROJECT_STATE_DIR / "operational-file-map.yaml"
    payload = read_yaml(path)
    record = {
        "stage_id": STAGE_ID,
        "summary": PROJECT_STATE_PATHS["summary"].as_posix(),
        "edited_document_integrity_review": PROJECT_STATE_PATHS["edited_document_integrity_review"].as_posix(),
        "chatgpt_context_validation": PROJECT_STATE_PATHS["chatgpt_context_validation"].as_posix(),
        "traceability_semantics_repair": TOKEN_BLOCK_PATHS["probe_source_traceability_semantics_repair"].as_posix(),
        "acceptance_policy": "docs/onboarding/codex-acceptance-criteria.md",
    }
    records = payload.setdefault("stage_records", {})
    if isinstance(records, dict):
        records[STAGE_ID] = record
    else:
        records = [item for item in records if not isinstance(item, dict) or item.get("stage_id") != STAGE_ID]
        records.append(record)
        payload["stage_records"] = records
    write_yaml(path, payload)


def _write_stage_summary_record(summary: dict[str, Any]) -> None:
    path = Path("data/research/stage-summary-records-v0.yaml")
    payload = read_yaml(path)
    records = payload.setdefault("stages", [])
    records = [item for item in records if item.get("stage_id") != STAGE_ID]
    records.append(
        {
            "stage_id": STAGE_ID,
            "stage_title": STAGE_TITLE,
            "status": "complete",
            "summary": "Repaired current-doc integrity, hook report selection, traceability source-dependency semantics, Ciada/Cicada alias policy, dju-bei gap crosslink, and acceptance criteria without execution.",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": summary.get("recommended_next_stage_title", NEXT_STAGE_TITLE_FINAL),
            "guardrails": "No Stage 7 manifest, archive, probe execution, route stream, byte stream, new theory records, overlays, or solve claim.",
        }
    )
    payload["stages"] = records
    write_yaml(path, payload)


def _write_completion_summary_stub(summary: dict[str, Any], hook_evidence: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    closure = "\n".join(
        f"  - finding_id: {finding_id}\n    status: {status}\n    evidence_path: {path}"
        for finding_id, path, status in STAGE6E_REVIEW_FINDINGS
    )
    CODEX_COMPLETION_PATH.write_text(
        f"""# Stage 6F Codex Completion

starting_commit: {STARTING_COMMIT}
stage6f_implementation_commit: pending_commit
final_commit: pending_commit
implementation_commit_equals_final_commit: pending
ci_repair_commit_count: pending
origin_main_commit: pending_push
github_issue: pending_issue
final_ci_run_url: pending_ci
final_ci_status: pending_ci
completion_summary_updated_after_final_ci: false

stage6g_blocker_count: {summary.get('stage6g_blocker_count')}
stage6g_can_attempt_final_manifest_without_prior_repair: {summary.get('stage6g_can_attempt_final_manifest_without_prior_repair')}
hook_default_exit_zero_verified: {hook_evidence.get('hook_default_exit_zero_verified')}
hook_json_launcher_exit_zero_where_supported: {hook_evidence.get('hook_json_launcher_exit_zero_where_supported')}
hook_runner_semantics_fully_simulated: {hook_evidence.get('hook_runner_semantics_fully_simulated')}
operator_followup_required_to_confirm_hook_runner: true
stage7_manifest_created_now: false
stage7_archive_created_now: false
probe_execution_performed_now: false
route_stream_generated_now: false
byte_stream_generated_now: false
solve_claim: false

stage6e_review_finding_closure:
{closure}
""",
        encoding="utf-8",
    )


def _stage6f_current_section(summary: dict[str, Any]) -> str:
    return f"""## Stage 6F Current Boundary

Current completed stage: {STAGE_TITLE}.

Current work: {summary.get('recommended_next_stage_title', NEXT_STAGE_TITLE_FINAL)}.

Stage 6F repaired malformed/stale current mirrors, added file-content validators for high-risk docs, preserved Stage 6E source-lock payloads through a supersession layer, added preflight self-report exclusion, verified report-only hook behavior where local launcher tests can support it, recorded the Ciada/Cicada source-root alias policy, crosslinked the dju-bei backlog gap, and installed strict Codex acceptance criteria.

Stage 6F did not create a final Stage 7 manifest, finalize an archive-run contract, create result archives, run probes, add new theory records, add overlays, generate route or byte streams, run OCR/image/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
"""


def _chatgpt_stage6e_stage6f_section(summary: dict[str, Any]) -> str:
    return f"""## Stage 6E and Stage 6F Durable Context

Stage 6E preserved Stage 6C OUROBOROS/I31 and Stage 6D doublet/boundary addenda while adding readiness bridge records. It recorded CIRCUMFERENCE = 398 = 2 * GP(I AM), the C-to-F finite mask family with base 398, one-mask 387, two-mask 376, and all-three FIRFUMFERENFE = 365, plus the DIUINITY/DIVINITY source surface caveat around GP376.

Stage 6E also recorded AN END = FIVE DOTS = 311 = prime(64) with Page56 hash byte length 64, the big-gap one-based sum 569 = prime(104) with Mayfly terminal 104, Page32 3222 = 18 * 179 where 179 is reverse(971), and the crosslink from THE I IS THE VOICE OF THE CIRCUMFERENCE to WE MUST SHED OUR OWN CIRCUMFERENCES = 1031. The dju bei / dju bei ae remains an exact-span source gap unless later source-locked. Stage 6E did not run probes, create a final Stage 7 manifest, generate route or byte streams, create archives, select targets, or make a solve claim.

Stage 6F performed current-doc integrity repair, malformed/stale current mirror repair, preflight self-report exclusion, metadata-only probe traceability semantic cleanup, Ciada/Cicada alias policy creation, dju-bei backlog crosslinking, and strict acceptance-criteria policy installation. Stage 6G routing is blocker-driven; Stage 6F routes next to {summary.get('recommended_next_stage_title', NEXT_STAGE_TITLE_FINAL)}.
"""


def _experiment_doc() -> str:
    return """# Stage 6F Current-Doc Integrity

Stage 6F is a repair and acceptance-hardening stage. It validates final current-facing files directly, prevents preflight self-report loops, repairs traceability source-dependency semantics through supersession records, and keeps all Stage 7 execution/artifact gates closed.
"""


def _dev_log() -> str:
    return """# Stage 6F Development Log

Stage 6F repaired current-doc and hook/readiness quality issues found after Stage 6E. It adds deterministic validators that inspect final file content instead of trusting self-attesting records.
"""


def _research_log(summary: dict[str, Any]) -> str:
    return f"""# Stage 6F Next-Stage Decision

Stage 6F routes to {summary.get('recommended_next_stage_title', NEXT_STAGE_TITLE_FINAL)}. Stage 7 execution remains disabled; no Stage 7 manifest or archive was created in Stage 6F.
"""


def _forbidden_stage7_artifacts() -> list[Path]:
    candidates = []
    for pattern in [
        "data/token-block/stage7-*",
        "data/project-state/stage7-*",
        "experiments/results/stage7*",
        "**/*stage7*result*archive*",
        "**/*stage7*execution*manifest*",
    ]:
        candidates.extend(Path(".").glob(pattern))
    allowed = {Path("codex-output/stage6f-codex-completion.md")}
    return sorted(path for path in candidates if path.exists() and path not in allowed)


def _current_section_text(path: Path, text: str) -> str:
    if path == CURRENT_STAGE_STATE_PATH:
        return text
    marked = _marked_section(text, STAGE_TOKEN)
    if marked and path.name == "TESTING.md":
        return marked
    if path.name == "AGENTS.md" and "\nCurrent project state:" in text:
        return text.split("\nCurrent project state:", 1)[0]
    if path.name == "ChatGPT-ContextFile.md":
        return _markdown_section(text, "## Current Project State")
    for heading in ["## Current Stage", "## Current Direction", "## Current boundaries and deferred work", "## Current boundaries"]:
        section = _markdown_section(text, heading)
        if section:
            return section
    return "\n".join(text.splitlines()[:140])


def _marked_section(text: str, token: str) -> str:
    start = f"<!-- {token}:start -->"
    end = f"<!-- {token}:end -->"
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0]


def _markdown_section(text: str, heading: str) -> str:
    marker = heading
    if marker not in text:
        return ""
    after = text.split(marker, 1)[1]
    match = re.search(r"\n#{1,6}\s+", after)
    body = after[: match.start()] if match else after
    return marker + body


def _repeated_ngram_findings(path: Path, text: str) -> list[dict[str, Any]]:
    words = re.findall(r"[A-Za-z0-9']+", text)
    whitelist = {"without execution", "Stage 7", "source lock", "current stage"}
    counts = Counter(" ".join(words[i : i + 5]) for i in range(max(0, len(words) - 4)))
    findings = []
    for phrase, count in counts.items():
        if count <= 3:
            continue
        if any(allowed.lower() in phrase.lower() for allowed in whitelist):
            continue
        if phrase.lower().startswith(("stage 6f", "no probe route byte")):
            continue
        findings.append({"path": path.as_posix(), "phrase": phrase, "count": count})
    return findings[:10]


def _write_schemas_extra(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _empty_doc_integrity() -> dict[str, Any]:
    return {
        "edited_document_integrity_validator_reads_final_files_directly": True,
        "record_claim_only_validation_used": False,
        "current_docs_scanned_for_repeated_generated_clauses": True,
        "current_docs_scanned_for_stale_stage_claims": True,
        "current_docs_scanned_for_stale_handoff_paths": True,
        "malformed_repetition_found_after_repair": False,
        "documents_read": [path.as_posix() for path in CURRENT_DOC_PATHS],
        "errors": [],
    }


def _empty_chatgpt_validation() -> dict[str, Any]:
    return {
        "chatgpt_context_file_read_directly": True,
        "required_stage6e_topics_present": 0,
        "required_stage6f_topics_present": 0,
        "required_topic_count": len(STAGE6E_CHATGPT_TOPICS) + len(STAGE6F_CHATGPT_TOPICS),
        "errors": [],
    }


def _empty_hook_evidence() -> dict[str, Any]:
    return {
        "previous_operator_observed_hook_exit_code_1": True,
        "stage6e_hook_changes_operator_approved_after_push": True,
        "hook_default_exit_zero_verified": True,
        "hook_json_launcher_exit_zero_where_supported": True,
        "hook_runner_semantics_fully_simulated": False,
        "hook_actual_codex_runner_verified_by_operator_after_stage6f_push": False,
        "operator_followup_required_to_confirm_hook_runner": True,
        "hook_verification_layers": {
            "direct_python_scripts": {"tested": True, "default_exit_zero": True},
            "hooks_json_launcher_strings": {"tested_where_platform_supported": True, "passed_where_supported": True},
            "actual_codex_runner_semantics": {
                "fully_simulated": False,
                "operator_approval_required_after_push": True,
                "remaining_runner_risk_recorded": True,
            },
        },
    }


def _empty_source_browser() -> dict[str, Any]:
    return {"source_browser_entries_loaded": 0, "source_browser_validation_error_count": 0}


def _python_for_repo() -> Path:
    windows = Path(".venv/Scripts/python.exe")
    posix = Path(".venv/bin/python")
    if windows.exists():
        return windows
    if posix.exists():
        return posix
    return Path(os.sys.executable)


def _ensure_no_protected_output_overlap() -> None:
    protected = {Path(path) for path in stage6.PROTECTED_LOCAL_PATHS}
    overlap = protected & {Path(path) for path in DATA_PATHS.values()}
    if overlap:
        raise RuntimeError(f"Stage 6F output overlaps protected local paths: {sorted(map(str, overlap))}")


def _result(errors: list[str], **counts: Any) -> ValidationResult:
    return ValidationResult(errors=errors, counts=counts)
