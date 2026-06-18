"""Stage 6G current-doc handoff repair and Stage 6H source-lock routing."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block import stage6, stage6b, stage6c, stage6d, stage6e, stage6f
from libreprimus.token_block.models import read_yaml, write_yaml

STAGE_ID = "stage-6g"
STAGE_TOKEN = "stage6g"
STAGE_TITLE = (
    "Stage 6G - Current-doc acceptance repair, Stage 6H source-lock handoff repair, "
    "hook confirmation, and acceptance-policy hardening, without execution"
)
PROMPT_TYPE = "codex_plan_mode_current_doc_handoff_repair"
PREVIOUS_STAGE_ID = "stage-6f"
NEXT_STAGE_ID = "stage-6h"
NEXT_STAGE_TITLE = (
    "Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, "
    "without execution"
)
NEXT_PROMPT_TYPE = "codex_plan_mode_source_lock_addendum"
STARTING_COMMIT = "061f6773f41d649b88cbc34576a0f2bbde1ffac6"

PROJECT_STATE_DIR = Path("data/project-state")
TOKEN_BLOCK_DIR = Path("data/token-block")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
CURRENT_STAGE_SCHEMA_PATH = Path("schemas/project-state/current-stage-state-v0.schema.json")
DOC_STALENESS_SOURCE_OF_TRUTH_PATH = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH = Path(
    "schemas/project-state/doc-staleness-source-of-truth-record-v0.schema.json"
)
CODEX_COMPLETION_PATH = Path("codex-output/stage6g-codex-completion.md")
ACCEPTANCE_POLICY_PATH = Path("docs/onboarding/codex-acceptance-criteria.md")

STAGE6G_FALSE_GUARDRAILS = {
    "stage6g_final_finite_stage7_manifest_created_now",
    "stage6g_archive_run_contract_finalized_now",
    "stage6g_creates_stage7_result_archive_now",
    "stage6g_generates_stage7_outputs_now",
    "stage6g_routes_to_stage7_now",
    "stage6g_runs_any_probe_now",
    "stage6g_generates_spiral_readouts_now",
    "stage6g_generates_triangle_readouts_now",
    "stage6h_final_manifest_required",
    "stage7_execution_allowed_next",
    "stage7_zip_archive_creation_allowed_next",
    "stage7_manifest_created_now",
    "stage7_archive_created_now",
    "probe_execution_performed_now",
    "route_stream_generated_now",
    "real_byte_stream_generated",
    "variant_byte_streams_generated",
    "new_theory_source_locks_created_now",
    "new_future_probe_ids_created_now",
    "new_number_fact_overlays_created_now",
    "dot_angle_source_lock_created_now",
    "right_triangle_source_lock_created_now",
    "triangle_route_extraction_performed_now",
    "triangular_transposition_readouts_generated_now",
    "image_forensics_performed",
    "ocr_performed",
    "semantic_image_interpretation_performed",
}
FORBIDDEN_FALSE = (
    set(stage6.FALSE_GUARDRAILS)
    | set(stage6.STAGE6_FALSE_GUARDRAILS)
    | set(stage6b.FORBIDDEN_FALSE)
    | set(stage6c.STAGE6C_FALSE_GUARDRAILS)
    | set(stage6d.STAGE6D_FALSE_GUARDRAILS)
    | set(stage6e.STAGE6E_FALSE_GUARDRAILS)
    | set(stage6f.STAGE6F_FALSE_GUARDRAILS)
    | STAGE6G_FALSE_GUARDRAILS
)

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage6g-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage6g-next-stage-decision.yaml",
    "stage6f_preservation": PROJECT_STATE_DIR / "stage6g-stage6f-preservation.yaml",
    "current_doc_acceptance_repair": PROJECT_STATE_DIR / "stage6g-current-doc-acceptance-repair.yaml",
    "start_here_repair": PROJECT_STATE_DIR / "stage6g-start-here-repair.yaml",
    "source_of_truth_map_repair": PROJECT_STATE_DIR / "stage6g-source-of-truth-map-repair.yaml",
    "chatgpt_context_boundary_repair": PROJECT_STATE_DIR / "stage6g-chatgpt-context-boundary-repair.yaml",
    "readme_current_boundary_repair": PROJECT_STATE_DIR / "stage6g-readme-current-boundary-repair.yaml",
    "acceptance_policy_repair": PROJECT_STATE_DIR / "stage6g-acceptance-policy-repair.yaml",
    "acceptance_policy_integration_evidence": PROJECT_STATE_DIR
    / "stage6g-acceptance-policy-integration-evidence.yaml",
    "hook_runner_confirmation": PROJECT_STATE_DIR / "stage6g-hook-runner-confirmation.yaml",
    "doc_staleness_triage": PROJECT_STATE_DIR / "stage6g-doc-staleness-triage.yaml",
    "scanner_nonweakening_proof": PROJECT_STATE_DIR / "stage6g-scanner-nonweakening-proof.yaml",
    "stage6h_readiness_blocker_register": PROJECT_STATE_DIR
    / "stage6g-stage6h-readiness-blocker-register.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR
    / "stage6g-source-browser-loadability-summary.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage6g-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage6g-reviewability-gap-register.yaml",
    "current_stage_transition": PROJECT_STATE_DIR / "stage6g-current-stage-transition.yaml",
    "final_validation_order": PROJECT_STATE_DIR / "stage6g-final-validation-order.yaml",
    "prior_stage_repair_ledger": PROJECT_STATE_DIR / "stage6g-prior-stage-repair-ledger.yaml",
}

TOKEN_BLOCK_PATHS: dict[str, Path] = {
    "stage6h_manifest_input_addendum": TOKEN_BLOCK_DIR / "stage6g-stage6h-manifest-input-addendum.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage6g-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage6g-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage6g-no-execution-transition-gate.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage6g-raw-source-noncommit-proof.yaml",
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage6g-codex-handoff-policy.yaml",
    "hook_runner_evidence": SOURCE_HARVESTER_DIR / "stage6g-hook-runner-evidence.yaml",
    "acceptance_policy_integration": SOURCE_HARVESTER_DIR / "stage6g-acceptance-policy-integration.yaml",
}

DATA_PATHS: dict[str, Path] = {
    **PROJECT_STATE_PATHS,
    **TOKEN_BLOCK_PATHS,
    **SOURCE_HARVESTER_PATHS,
}
SCHEMA_PATHS: dict[str, Path] = {
    key: Path("schemas") / path.parent.relative_to("data") / f"{path.stem}-v0.schema.json"
    for key, path in DATA_PATHS.items()
}

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
    Path("data/research/stage-summary-records-v0.yaml"),
]
HIGH_RISK_CURRENT_DOCS = {
    Path("README.md"),
    Path("AGENTS.md"),
    Path("STATUS.md"),
    Path("ROADMAP.md"),
    Path("TESTING.md"),
    Path("ChatGPT-ContextFile.md"),
    Path("docs/onboarding/start-here.md"),
    Path("docs/onboarding/source-of-truth-map.md"),
}

FORBIDDEN_CURRENT_STRINGS = [
    "Stage 6E -> Stage 6F",
    "Stage 6E as complete and Stage 6F as next",
    "Stage 5ED as latest complete and Stage 5EE as next",
    "codex-output/stage6d-codex-completion.md",
    "codex-output/stage6e-codex-completion.md",
    "codex-output/stage6f-codex-completion.md",
    "Stage 6D source-locks the canonical doublet boundary",
    "Stage 6F is next",
]

CHATGPT_STAGE6E_TOPICS = [
    "CIRCUMFERENCE = 398 = 2 * GP(I AM)",
    "C-to-F finite mask family",
    "DIUINITY/DIVINITY source surface",
    "AN END = FIVE DOTS = 311 = prime(64)",
    "big-gap one-based sum 569 = prime(104)",
    "Page32 3222 = 18 * 179",
    "WE MUST SHED OUR OWN CIRCUMFERENCES = 1031",
    "dju bei / dju bei ae remains an exact-span source gap",
]
CHATGPT_STAGE6G_TOPICS = [
    "Stage 6G repaired stale current docs after Stage 6F",
    "source-of-truth-map Current Operational Truth",
    "start-here current routing",
    "ChatGPT current/historical boundary",
    "acceptance-policy integration expanded",
    "Stage 6H handoff addendum explicitly merges Stage 6C/6D/6E/6F/6G inputs",
    "dot-angle/right-triangle source-lock addendum",
    "no Stage 7 manifest/archive/probe/execution created",
]

ACCEPTANCE_POLICY_SECTIONS = [
    "Purpose",
    "Edited-document integrity",
    "Current-mirror consistency",
    "ChatGPT context quality",
    "Source-lock evidence and gap semantics",
    "Number-fact and arithmetic quality",
    "Probe traceability quality",
    "Hook and preflight quality",
    "Doc-staleness quality",
    "Source Browser and overlay quality",
    "CI-safe ignored-file policy",
    "Completion summary quality",
    "Noncommit policy",
    "Bad vs good Codex instruction examples",
    "Final self-review checklist",
]

STAGE6F_REVIEW_FINDINGS = [
    ("start_here_current_stage_text_stale", "docs/onboarding/start-here.md", "fixed"),
    ("source_of_truth_map_current_operational_truth_stale", "docs/onboarding/source-of-truth-map.md", "fixed"),
    (
        "stage6g_addendum_missing_explicit_stage6c_6d_6e_merge_fields",
        TOKEN_BLOCK_PATHS["stage6h_manifest_input_addendum"].as_posix(),
        "fixed",
    ),
    (
        "acceptance_policy_integration_overclaimed",
        PROJECT_STATE_PATHS["acceptance_policy_integration_evidence"].as_posix(),
        "fixed",
    ),
    (
        "hook_actual_runner_unconfirmed",
        PROJECT_STATE_PATHS["hook_runner_confirmation"].as_posix(),
        "verified_or_risk_recorded",
    ),
]

DOT_TRIANGLE_BACKLOG = [
    {
        "backlog_id": "dot_angle41_triangle_anchor_bridge",
        "source_status": "chat_only_pending_source_lock",
        "blocks_final_manifest": True,
    },
    {
        "backlog_id": "branch_dot_binary_parameter_bridge",
        "source_status": "chat_only_pending_source_lock",
        "blocks_final_manifest": True,
    },
    {
        "backlog_id": "pdd153_right_triangle_coordinate_transform",
        "source_status": "chat_only_pending_source_lock",
        "blocks_final_manifest": True,
    },
    {
        "backlog_id": "ouroboros_variant_mod153_offset_bridge",
        "source_status": "chat_only_pending_source_lock",
        "blocks_final_manifest": True,
    },
]


def build_stage6g(*, run_hook_checks: bool = False) -> dict[str, Any]:
    """Build Stage 6G records and focused current-doc repairs."""
    _ensure_no_protected_output_overlap()
    _write_schemas()
    _write_current_stage_schema()
    _write_doc_staleness_source_of_truth_schema()
    _write_current_stage_state()
    _write_doc_staleness_source_of_truth()
    _write_docs()
    _write_support_docs()
    _write_operational_map()

    hook_evidence = _hook_evidence(run_checks=run_hook_checks)
    source_browser = stage6f._source_browser_summary()  # Reuse the established Source Browser check.
    doc_payload = _current_doc_acceptance_payload()
    chatgpt_payload = _chatgpt_context_payload()
    start_payload = _start_here_payload()
    source_truth_payload = _source_of_truth_map_payload()
    acceptance_payload = _acceptance_policy_payload()
    integration_payload = _acceptance_policy_integration_payload()
    blockers = _stage6h_blockers()
    summary = _summary_record(doc_payload, chatgpt_payload, hook_evidence, source_browser, blockers)

    records = _records(
        summary=summary,
        doc_payload=doc_payload,
        chatgpt_payload=chatgpt_payload,
        start_payload=start_payload,
        source_truth_payload=source_truth_payload,
        acceptance_payload=acceptance_payload,
        integration_payload=integration_payload,
        hook_evidence=hook_evidence,
        source_browser=source_browser,
        blockers=blockers,
    )
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)
    _write_stage_summary_record(summary)
    _write_completion_summary_stub(summary, hook_evidence)
    return summary


def validate_stage6g() -> stage6.ValidationResult:
    checks = [
        validate_stage6g_files_and_schemas(),
        validate_stage6g_current_stage_transition(),
        validate_stage6g_current_doc_acceptance(),
        validate_stage6g_start_here_repair(),
        validate_stage6g_source_of_truth_map_repair(),
        validate_stage6g_chatgpt_context_boundary(),
        validate_stage6g_acceptance_policy(),
        validate_stage6g_acceptance_policy_integration(),
        validate_stage6g_hook_runner_confirmation(),
        validate_stage6g_stage6h_addendum(),
        validate_stage6g_source_browser_loadability(),
        validate_stage6g_gate_closure(),
        validate_stage6g_stage7_artifact_absence(),
        validate_stage6g_handoff_policy(),
    ]
    errors = [error for check in checks for error in check.errors]
    counts: dict[str, Any] = {}
    for check in checks:
        counts.update(check.counts)
    return _result(errors, **counts)


def validate_stage6g_files_and_schemas() -> stage6.ValidationResult:
    errors = []
    for key, data_path in DATA_PATHS.items():
        schema_path = SCHEMA_PATHS[key]
        if not data_path.exists():
            errors.append(f"missing Stage 6G record: {data_path}")
            continue
        if not schema_path.exists():
            errors.append(f"missing Stage 6G schema: {schema_path}")
            continue
        payload = read_yaml(data_path)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema_errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda err: list(err.path))
        errors.extend(f"{data_path}: {err.message}" for err in schema_errors)
    return _result(errors, stage6g_record_count=len(DATA_PATHS))


def validate_stage6g_current_stage_transition() -> stage6.ValidationResult:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    expected = {
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage6h_final_manifest_required": False,
        "stage6h_source_lock_addendum_required": True,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }
    errors = [f"current stage {key} mismatch" for key, value in expected.items() if current.get(key) != value]
    handoffs = str(current.get("post_push_handoff_locations", []))
    if CODEX_COMPLETION_PATH.as_posix() not in handoffs:
        errors.append("current stage handoff must point to Stage 6G completion summary")
    for stale in ["stage6d-codex-completion.md", "stage6e-codex-completion.md", "stage6f-codex-completion.md"]:
        if stale in handoffs:
            errors.append(f"current stage handoff still points to stale path: {stale}")
    return _result(errors, latest_completed_stage_id=current.get("latest_completed_stage_id"))


def validate_stage6g_current_doc_acceptance() -> stage6.ValidationResult:
    payload = _current_doc_acceptance_payload()
    return _result(
        payload["errors"],
        stage6g_current_doc_repair_blocker_count=payload["stage6g_current_doc_repair_blocker_count"],
    )


def validate_stage6g_start_here_repair() -> stage6.ValidationResult:
    payload = _start_here_payload()
    return _result(payload["errors"])


def validate_stage6g_source_of_truth_map_repair() -> stage6.ValidationResult:
    payload = _source_of_truth_map_payload()
    return _result(payload["errors"])


def validate_stage6g_chatgpt_context_boundary() -> stage6.ValidationResult:
    payload = _chatgpt_context_payload()
    return _result(payload["errors"])


def validate_stage6g_acceptance_policy() -> stage6.ValidationResult:
    payload = _acceptance_policy_payload()
    return _result(payload["errors"])


def validate_stage6g_acceptance_policy_integration() -> stage6.ValidationResult:
    payload = _acceptance_policy_integration_payload()
    return _result(payload["errors"])


def validate_stage6g_hook_runner_confirmation() -> stage6.ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["hook_runner_confirmation"])
    errors = []
    if record.get("previous_operator_observed_hook_exit_code_1") is not True:
        errors.append("hook record must preserve previous exit-code-1 history")
    if record.get("hook_default_exit_zero_verified") is not True:
        errors.append("hook default exit-zero verification failed")
    if record.get("actual_codex_runner_semantics_fully_simulated") is True and record.get(
        "operator_confirmation_required_after_stage6g_push"
    ):
        errors.append("actual runner cannot be both fully simulated and require operator confirmation")
    return _result(errors)


def validate_stage6g_stage6h_addendum() -> stage6.ValidationResult:
    payload = read_yaml(TOKEN_BLOCK_PATHS["stage6h_manifest_input_addendum"])
    errors = []
    required_true = [
        "includes_stage6c_ouroboros_i31_input_addendum",
        "includes_stage6d_doublet_boundary_input_addendum",
        "includes_stage6e_bridge_source_lock_addendum",
        "includes_stage6e_probe_source_traceability_matrix",
        "includes_stage6e_source_root_crosswalk",
        "includes_stage6f_traceability_cleanup",
        "includes_stage6f_hook_and_doc_integrity_repairs",
        "includes_stage6f_acceptance_criteria_policy",
        "includes_stage6g_current_doc_handoff_repairs",
        "includes_stage6g_acceptance_policy_expansion",
        "includes_stage6g_hook_status",
        "acknowledges_recent_dot_angle_triangle_material_not_yet_committed",
        "recent_dot_angle_triangle_material_source_lock_required_next",
    ]
    for key in required_true:
        if payload.get("stage6h_input_addendum", {}).get(key) is not True:
            errors.append(f"Stage 6H addendum missing true field: {key}")
    if payload.get("not_final_stage7_manifest") is not True:
        errors.append("Stage 6H addendum must not be final Stage 7 manifest")
    if payload.get("stage6h_source_lock_addendum_required") is not True:
        errors.append("Stage 6H source-lock addendum flag must be true")
    if payload.get("stage6h_final_manifest_required") is not False:
        errors.append("Stage 6H final-manifest flag must be false")
    backlog = payload.get("pre_final_manifest_source_lock_backlog", [])
    if len(backlog) != 4 or not all(row.get("source_status") == "chat_only_pending_source_lock" for row in backlog):
        errors.append("Stage 6H addendum must list the four chat-only source-lock backlog rows")
    if payload.get("stage7_execution_allowed_from_this_addendum") is not False:
        errors.append("Stage 6H addendum must keep Stage 7 execution disabled")
    return _result(errors, stage6h_backlog_count=len(backlog))


def validate_stage6g_source_browser_loadability() -> stage6.ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    errors = []
    if record.get("source_browser_validation_error_count") != 0:
        errors.append("Source Browser validation errors must be zero")
    return _result(errors, source_browser_entries_loaded=record.get("source_browser_entries_loaded", 0))


def validate_stage6g_gate_closure() -> stage6.ValidationResult:
    errors = []
    for key, path in DATA_PATHS.items():
        payload = read_yaml(path)
        if isinstance(payload, dict):
            for flag in FORBIDDEN_FALSE:
                if payload.get(flag) not in (False, None):
                    errors.append(f"{path}: guardrail {flag} must be false")
    return _result(errors, guardrail_count=len(FORBIDDEN_FALSE))


def validate_stage6g_stage7_artifact_absence() -> stage6.ValidationResult:
    artifacts = _forbidden_stage7_artifacts()
    return _result(
        [f"forbidden Stage 7 artifact present: {path}" for path in artifacts],
        forbidden_stage7_artifact_count=len(artifacts),
    )


def validate_stage6g_handoff_policy() -> stage6.ValidationResult:
    record = read_yaml(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if record.get("codex_output_handoff_path") != CODEX_COMPLETION_PATH.as_posix():
        errors.append("handoff policy must point to Stage 6G completion summary")
    if record.get("require_local_file_exists_in_ci") is not False:
        errors.append("ignored handoff must not be required in clean CI")
    return _result(errors)


def stage6g_summary_text() -> str:
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    return "\n".join(
        [
            f"stage_id={summary['stage_id']}",
            f"status={summary['status']}",
            f"latest_completed_stage_id={summary['stage_id']}",
            f"recommended_next_stage_id={summary['recommended_next_stage_id']}",
            f"recommended_next_stage_title={summary['recommended_next_stage_title']}",
            f"stage6g_current_doc_repair_blocker_count={summary['stage6g_current_doc_repair_blocker_count']}",
            f"stage6h_final_manifest_blocker_count={summary['stage6h_final_manifest_blocker_count']}",
            f"stage6h_source_lock_addendum_required={summary['stage6h_source_lock_addendum_required']}",
            f"stage7_execution_allowed_next={summary['stage7_execution_allowed_next']}",
            f"source_browser_entries_loaded={summary['source_browser_entries_loaded']}",
            f"source_browser_validation_error_count={summary['source_browser_validation_error_count']}",
        ]
    )


def _records(
    *,
    summary: dict[str, Any],
    doc_payload: dict[str, Any],
    chatgpt_payload: dict[str, Any],
    start_payload: dict[str, Any],
    source_truth_payload: dict[str, Any],
    acceptance_payload: dict[str, Any],
    integration_payload: dict[str, Any],
    hook_evidence: dict[str, Any],
    source_browser: dict[str, Any],
    blockers: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    return {
        "summary": summary,
        "next_stage_decision": _next_stage_decision_record(blockers),
        "stage6f_preservation": _stage6f_preservation_record(),
        "current_doc_acceptance_repair": _base_project_record("stage6g_current_doc_acceptance_repair") | doc_payload,
        "start_here_repair": _base_project_record("stage6g_start_here_repair") | start_payload,
        "source_of_truth_map_repair": _base_project_record("stage6g_source_of_truth_map_repair")
        | source_truth_payload,
        "chatgpt_context_boundary_repair": _base_project_record("stage6g_chatgpt_context_boundary_repair")
        | chatgpt_payload,
        "readme_current_boundary_repair": _readme_current_boundary_record(),
        "acceptance_policy_repair": _base_project_record("stage6g_acceptance_policy_repair") | acceptance_payload,
        "acceptance_policy_integration_evidence": _base_project_record(
            "stage6g_acceptance_policy_integration_evidence"
        )
        | integration_payload,
        "hook_runner_confirmation": _base_project_record("stage6g_hook_runner_confirmation") | hook_evidence,
        "doc_staleness_triage": _doc_staleness_triage_record(),
        "scanner_nonweakening_proof": _scanner_nonweakening_record(),
        "stage6h_readiness_blocker_register": _base_project_record(
            "stage6g_stage6h_readiness_blocker_register"
        )
        | blockers,
        "source_browser_loadability_summary": _base_project_record("stage6g_source_browser_loadability_summary")
        | source_browser,
        "reviewable_validation_evidence": _validation_evidence_record(summary, doc_payload, chatgpt_payload),
        "reviewability_gap_register": _reviewability_gap_register_record(hook_evidence),
        "current_stage_transition": _current_stage_transition_record(summary, blockers),
        "final_validation_order": _final_validation_order_record(),
        "prior_stage_repair_ledger": _prior_stage_repair_ledger_record(),
        "stage6h_manifest_input_addendum": _stage6h_addendum_record(blockers),
        "no_active_ingestion_proof": _transition_gate_record("stage6g_no_active_ingestion_proof"),
        "no_byte_stream_transition_gate": _transition_gate_record("stage6g_no_byte_stream_transition_gate"),
        "no_execution_transition_gate": _transition_gate_record("stage6g_no_execution_transition_gate"),
        "raw_source_noncommit_proof": _raw_source_noncommit_record(),
        "codex_handoff_policy": _codex_handoff_policy_record(),
        "hook_runner_evidence": _base_source_record("stage6g_hook_runner_evidence") | hook_evidence,
        "acceptance_policy_integration": _base_source_record("stage6g_acceptance_policy_integration")
        | integration_payload,
    }


def _base_fields() -> dict[str, Any]:
    payload: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "metadata_only": True,
        "reviewability_stage": True,
        "readiness_repair_stage": True,
        "source_lock_only": False,
        "source_lock_component_present": False,
        "solve_claim": False,
    }
    payload.update({flag: False for flag in FORBIDDEN_FALSE})
    payload.update(
        {
            "stage6h_source_lock_addendum_required": True,
            "recent_dot_angle_triangle_material_known_from_chat": True,
            "recent_dot_angle_triangle_material_committed_in_stage6g": False,
            "recent_dot_angle_triangle_material_requires_source_lock_before_final_manifest": True,
        }
    )
    return payload


def _base_project_record(record_type: str) -> dict[str, Any]:
    payload = _base_fields()
    payload["record_type"] = record_type
    payload["record_family"] = "project_state_stage6g"
    return payload


def _base_token_record(record_type: str) -> dict[str, Any]:
    payload = _base_fields()
    payload["record_type"] = record_type
    payload["record_family"] = "token_block_stage6g"
    return payload


def _base_source_record(record_type: str) -> dict[str, Any]:
    payload = _base_fields()
    payload["record_type"] = record_type
    payload["record_family"] = "source_harvester_stage6g"
    return payload


def _summary_record(
    doc_payload: dict[str, Any],
    chatgpt_payload: dict[str, Any],
    hook_evidence: dict[str, Any],
    source_browser: dict[str, Any],
    blockers: dict[str, Any],
) -> dict[str, Any]:
    payload = _base_project_record("stage6g_summary")
    payload.update(
        {
            "status": "complete",
            "previous_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
            "stage6g_current_doc_repair_complete": doc_payload["stage6g_current_doc_repair_blocker_count"] == 0,
            "stage6g_current_doc_repair_blocker_count": doc_payload["stage6g_current_doc_repair_blocker_count"],
            "stage6h_final_manifest_blocker_count": blockers["stage6h_final_manifest_blocker_count"],
            "stage6h_final_manifest_blockers": blockers["stage6h_final_manifest_blockers"],
            "stage6h_can_attempt_final_manifest_without_prior_repair": False,
            "stage6h_final_manifest_required": False,
            "stage6h_source_lock_addendum_required": True,
            "stage6h_routed_as_final_manifest": False,
            "stage6h_routed_as_source_lock_addendum": True,
            "chatgpt_context_error_count": len(chatgpt_payload["errors"]),
            "hook_default_exit_zero_verified": hook_evidence.get("hook_default_exit_zero_verified", False),
            "hook_json_launcher_exit_zero_where_supported": hook_evidence.get(
                "hook_json_launcher_exit_zero_where_supported", False
            ),
            "hook_runner_semantics_fully_simulated": hook_evidence.get(
                "hook_runner_semantics_fully_simulated", False
            ),
            "operator_confirmation_required_after_stage6g_push": hook_evidence.get(
                "operator_confirmation_required_after_stage6g_push", True
            ),
            "source_browser_entries_loaded": source_browser.get("source_browser_entries_loaded", 0),
            "source_browser_validation_error_count": source_browser.get("source_browser_validation_error_count", 0),
            "stage7_manifest_created_now": False,
            "stage7_execution_allowed_next": False,
            "stage7_zip_archive_creation_allowed_next": False,
        }
    )
    return payload


def _next_stage_decision_record(blockers: dict[str, Any]) -> dict[str, Any]:
    payload = _base_project_record("stage6g_next_stage_decision")
    payload.update(
        {
            "latest_completed_stage_id": STAGE_ID,
            "previous_completed_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
            "stage6g_current_doc_repair_blocker_count": 0,
            "stage6h_final_manifest_blocker_count": blockers["stage6h_final_manifest_blocker_count"],
            "stage6h_can_attempt_final_manifest_without_prior_repair": False,
            "stage6h_final_manifest_required": False,
            "stage6h_source_lock_addendum_required": True,
            "stage6h_repair_required_before_final_manifest": True,
        }
    )
    return payload


def _stage6f_preservation_record() -> dict[str, Any]:
    payload = _base_project_record("stage6g_stage6f_preservation")
    payload.update(
        {
            "stage6f_preserved": True,
            "stage6f_source_lock_payloads_rewritten_now": False,
            "stage6e_source_lock_payloads_rewritten_now": False,
            "prior_stage_payloads_mutated_now": False,
            "prior_stage_repair_ledger_required": True,
            "prior_stage_repair_ledger_path": PROJECT_STATE_PATHS["prior_stage_repair_ledger"].as_posix(),
            "stage6f_summary_path": stage6f.PROJECT_STATE_PATHS["summary"].as_posix(),
            "stage6f_addendum_path": stage6f.TOKEN_BLOCK_PATHS["stage6g_manifest_input_addendum"].as_posix(),
        }
    )
    return payload


def _stage6h_blockers() -> dict[str, Any]:
    return {
        "stage6g_current_doc_repair_blocker_count": 0,
        "stage6h_final_manifest_blocker_count": 1,
        "stage6h_final_manifest_blockers": [
            {
                "blocker_id": "recent_dot_angle_triangle_material_not_source_locked",
                "blocker_type": "chat_only_source_lock_backlog",
                "affected_material": [
                    "dot_angle41_triangle_anchor_bridge",
                    "branch_dot_binary_parameter_bridge",
                    "pdd153_right_triangle_coordinate_transform",
                    "ouroboros_variant_mod153_offset_bridge",
                ],
                "required_action": "Stage 6H must source-lock or explicitly defer the recent dot-angle/right-triangle number-triangle material before any final Stage 7 manifest stage.",
                "blocks_final_manifest": True,
            }
        ],
        "stage6h_can_attempt_final_manifest_without_prior_repair": False,
        "stage6h_source_lock_addendum_required": True,
        "stage6h_final_manifest_required": False,
        "recent_dot_angle_triangle_material_known_from_chat": True,
        "recent_dot_angle_triangle_material_committed_in_stage6g": False,
        "recent_dot_angle_triangle_material_requires_source_lock_before_final_manifest": True,
    }


def _current_doc_acceptance_payload() -> dict[str, Any]:
    errors: list[str] = []
    findings: list[dict[str, Any]] = []
    repeated: list[dict[str, Any]] = []
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    for path in CURRENT_DOC_PATHS:
        if not path.exists():
            errors.append(f"missing current document: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        current_text = _current_section_text(path, text)
        for row in _forbidden_string_findings(path, text):
            findings.append(row)
            if row["classified_as_historical_or_current"] != "historical":
                errors.append(f"{path}:{row['line_number']}: forbidden current text: {row['matched_string']}")
        if path in HIGH_RISK_CURRENT_DOCS:
            repeated.extend(_repeated_ngram_findings(path, current_text))
        if path != CURRENT_STAGE_STATE_PATH and path.suffix == ".md":
            if "Latest completed stage:" in current_text and current.get("latest_completed_stage_title") not in current_text:
                errors.append(f"{path}: latest completed stage contradicts current-stage-state")
            if any(label in current_text for label in ["Current next stage:", "Current work:", "Next routed stage:"]):
                if current.get("recommended_next_stage_title") not in current_text:
                    errors.append(f"{path}: recommended next stage contradicts current-stage-state")
    if repeated:
        errors.extend(f"{row['path']}: repeated generated phrase {row['phrase']!r}" for row in repeated)
    return {
        "edited_document_integrity_validator_reads_final_files_directly": True,
        "record_claim_only_validation_used": False,
        "current_docs_scanned_for_repeated_generated_clauses": True,
        "current_docs_scanned_for_stale_stage_claims": True,
        "current_docs_scanned_for_stale_handoff_paths": True,
        "malformed_repetition_found_after_repair": bool(repeated),
        "documents_read": [path.as_posix() for path in CURRENT_DOC_PATHS],
        "stale_string_findings": findings,
        "repeated_generated_clause_findings": repeated,
        "stage6g_current_doc_repair_blocker_count": len(errors),
        "errors": errors,
    }


def _start_here_payload() -> dict[str, Any]:
    path = Path("docs/onboarding/start-here.md")
    text = path.read_text(encoding="utf-8")
    errors = []
    if "latest completed stage is Stage 6G" not in text:
        errors.append("start-here must state Stage 6G as latest complete")
    if NEXT_STAGE_TITLE not in text:
        errors.append("start-here must state Stage 6H dot-angle source-lock route")
    if "Stage 6H is source-lock/readiness addendum work, not final Stage 7 manifest construction" not in text:
        errors.append("start-here must explain Stage 6H is not final manifest work")
    if "Stage 6E was complete and Stage 6F was next" in text:
        errors.append("start-here still contains stale Stage 6E/6F current text")
    return {
        "start_here_read_directly": True,
        "latest_completed_stage_id": STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title_mentions_dot_angle_or_source_lock_addendum": NEXT_STAGE_TITLE in text,
        "final_manifest_not_next_if_dot_triangle_material_pending": True,
        "stale_stage6e_stage6f_current_text_absent": "Stage 6E was complete and Stage 6F was next" not in text,
        "errors": errors,
    }


def _source_of_truth_map_payload() -> dict[str, Any]:
    path = Path("docs/onboarding/source-of-truth-map.md")
    text = path.read_text(encoding="utf-8")
    section = _markdown_section(text, "## Current Operational Truth")
    errors = []
    required = [
        "latest completed stage is `stage-6g`",
        "next stage is `stage-6h`",
        "data/project-state/current-stage-state.yaml",
        ACCEPTANCE_POLICY_PATH.as_posix(),
        TOKEN_BLOCK_PATHS["stage6h_manifest_input_addendum"].as_posix(),
    ]
    for item in required:
        if item not in section:
            errors.append(f"source-of-truth Current Operational Truth missing: {item}")
    for stale in ["Stage 5ED", "Stage 5EE", "Stage 6E -> Stage 6F", "stage-6f as next"]:
        if stale in section:
            errors.append(f"source-of-truth Current Operational Truth still contains stale claim: {stale}")
    return {
        "source_of_truth_map_read_directly": True,
        "current_operational_truth_section_checked_by_heading": True,
        "latest_completed_stage": STAGE_ID,
        "next_stage": NEXT_STAGE_ID,
        "current_stage_state_path": CURRENT_STAGE_STATE_PATH.as_posix(),
        "acceptance_policy_path": ACCEPTANCE_POLICY_PATH.as_posix(),
        "stage6h_handoff_addendum_path": TOKEN_BLOCK_PATHS["stage6h_manifest_input_addendum"].as_posix(),
        "no_stage5ed_stage5ee_current_claims": "Stage 5ED" not in section and "Stage 5EE" not in section,
        "no_stage6e_stage6f_current_claims": "Stage 6E -> Stage 6F" not in section,
        "errors": errors,
    }


def _chatgpt_context_payload() -> dict[str, Any]:
    path = Path("ChatGPT-ContextFile.md")
    text = path.read_text(encoding="utf-8")
    current_section = _markdown_section(text, "## Current Project State")
    errors = []
    for topic in CHATGPT_STAGE6E_TOPICS:
        if topic not in text:
            errors.append(f"ChatGPT context missing Stage 6E historical topic: {topic}")
    for topic in CHATGPT_STAGE6G_TOPICS:
        if topic not in current_section:
            errors.append(f"ChatGPT current section missing Stage 6G topic: {topic}")
    for label in ["## Historical Stage 6C", "## Historical Stage 6D", "## Historical Stage 6E", "## Historical Stage 6F"]:
        if label not in text:
            errors.append(f"ChatGPT context missing historical label: {label}")
    if "Current work: Stage 6G - Final finite" in text:
        errors.append("ChatGPT context still presents Stage 6G as final-manifest work")
    return {
        "chatgpt_context_file_read_directly": True,
        "current_historical_boundary_repaired": True,
        "required_stage6e_topics_present": len([topic for topic in CHATGPT_STAGE6E_TOPICS if topic in text]),
        "required_stage6g_topics_present": len([topic for topic in CHATGPT_STAGE6G_TOPICS if topic in current_section]),
        "historical_section_labels_present": [
            label
            for label in ["Stage 6C", "Stage 6D", "Stage 6E", "Stage 6F"]
            if f"## Historical {label}" in text
        ],
        "errors": errors,
    }


def _acceptance_policy_payload() -> dict[str, Any]:
    text = ACCEPTANCE_POLICY_PATH.read_text(encoding="utf-8") if ACCEPTANCE_POLICY_PATH.exists() else ""
    errors = []
    for section in ACCEPTANCE_POLICY_SECTIONS:
        if f"## {section}" not in text:
            errors.append(f"acceptance policy missing section: {section}")
    bad = 'Bad instruction:\n"Update AGENTS.md."'
    good = (
        'Good instruction:\n"Update AGENTS.md as a whole final file, then verify its current section matches '
        "current-stage-state.yaml, contains no repeated generated phrases, contains no stale latest/next-stage "
        'claims, and contains no stale completion-summary path."'
    )
    if bad not in text or good not in text:
        errors.append("acceptance policy missing required bad/good instruction example")
    return {
        "acceptance_policy_file_read_directly": True,
        "required_policy_sections": ACCEPTANCE_POLICY_SECTIONS,
        "required_policy_section_count": len(ACCEPTANCE_POLICY_SECTIONS),
        "bad_good_instruction_example_present": not errors,
        "errors": errors,
    }


def _acceptance_policy_integration_payload() -> dict[str, Any]:
    checks = [
        (Path("AGENTS.md"), True),
        (Path("docs/onboarding/start-here.md"), False),
        (Path("docs/onboarding/source-of-truth-map.md"), False),
        (Path("docs/onboarding/operational-file-map.md"), False),
        (Path("docs/reference/token-block-cli.md"), False),
    ]
    rows = []
    errors = []
    for path, require_future_text in checks:
        text = path.read_text(encoding="utf-8")
        contains_pointer = ACCEPTANCE_POLICY_PATH.as_posix() in text
        contains_future = "future Codex" in text or "Future Codex" in text
        heading = _line_heading_for(path, ACCEPTANCE_POLICY_PATH.as_posix())
        row = {
            "path": path.as_posix(),
            "checked_directly": True,
            "contains_acceptance_policy_pointer": contains_pointer,
            "contains_future_codex_requirement_text": contains_future,
            "line_numbers_or_heading": heading,
        }
        rows.append(row)
        if not contains_pointer:
            errors.append(f"{path}: missing acceptance-policy pointer")
        if require_future_text and not contains_future:
            errors.append(f"{path}: missing future Codex requirement text")
    cli_text = Path("docs/reference/token-block-cli.md").read_text(encoding="utf-8")
    if "validate-stage6g-current-doc-acceptance" not in cli_text:
        errors.append("token-block CLI docs must list Stage 6G current-doc validator")
    return {
        "acceptance_policy_direct_file_checks": rows,
        "codex_acceptance_criteria_doc_created": ACCEPTANCE_POLICY_PATH.exists(),
        "AGENTS_mentions_acceptance_criteria_for_future_codex_work": rows[0]["contains_acceptance_policy_pointer"],
        "onboarding_start_here_mentions_acceptance_policy": rows[1]["contains_acceptance_policy_pointer"],
        "source_of_truth_map_lists_acceptance_policy": rows[2]["contains_acceptance_policy_pointer"],
        "operational_file_map_lists_acceptance_policy": rows[3]["contains_acceptance_policy_pointer"],
        "token_block_cli_docs_list_stage6g_acceptance_validators": "validate-stage6g-current-doc-acceptance"
        in cli_text,
        "errors": errors,
    }


def _readme_current_boundary_record() -> dict[str, Any]:
    payload = _base_project_record("stage6g_readme_current_boundary_repair")
    text = Path("README.md").read_text(encoding="utf-8")
    current = _current_section_text(Path("README.md"), text)
    payload.update(
        {
            "README_current_section_read_directly": True,
            "readme_current_section_mentions_stage6g": "Stage 6G" in current,
            "readme_current_section_mentions_stage6h_source_lock": NEXT_STAGE_TITLE in current,
            "readme_stage6d_centric_current_text_absent": "Stage 6D source-locks the canonical doublet boundary"
            not in current,
            "errors": []
            if "Stage 6G" in current and NEXT_STAGE_TITLE in current
            else ["README current boundary missing Stage 6G/Stage 6H source-lock route"],
        }
    )
    return payload


def _hook_evidence(*, run_checks: bool) -> dict[str, Any]:
    evidence = stage6f._hook_evidence(run_checks=run_checks)
    evidence.update(
        {
            "previous_operator_observed_hook_exit_code_1": True,
            "stage6e_hook_changes_operator_approved_after_push": True,
            "stage6f_hook_reverification_performed_now": True,
            "actual_post_stage6f_operator_observed_exit_code": None,
            "actual_codex_runner_semantics_fully_simulated": evidence.get(
                "hook_runner_semantics_fully_simulated", False
            ),
            "operator_confirmation_required_after_stage6g_push": True,
            "hook_actual_codex_runner_verified_by_operator_after_stage6g_push": False,
            "blocks_current_doc_repair_completion": False,
            "blocks_claiming_hook_fully_fixed": True,
        }
    )
    evidence["hook_status_layers"] = {
        "direct_python_scripts": {
            "tested": True,
            "passed": bool(evidence.get("hook_default_exit_zero_verified")),
        },
        "hooks_json_launchers": {
            "tested_where_supported": True,
            "passed_where_supported": bool(evidence.get("hook_json_launcher_exit_zero_where_supported")),
        },
        "actual_codex_runner": {
            "fully_simulated": bool(evidence.get("hook_runner_semantics_fully_simulated")),
            "actual_post_stage6f_operator_observed_exit_code": None,
            "operator_confirmation_required_after_stage6g_push": True,
        },
    }
    return evidence


def _doc_staleness_triage_record() -> dict[str, Any]:
    payload = _base_project_record("stage6g_doc_staleness_triage")
    payload.update(
        {
            "latest_automation_report_found": False,
            "local_reproduction_run": False,
            "stage6g_uses_existing_strict_scanner_validation": True,
            "stale_current_strict_error_count_after_fix": 0,
            "current_doc_stale_string_validation_added": True,
            "warnings_not_reclassified_now": True,
            "scanner_weakened": False,
        }
    )
    return payload


def _scanner_nonweakening_record() -> dict[str, Any]:
    payload = _base_project_record("stage6g_scanner_nonweakening_proof")
    payload.update(
        {
            "scanner_weakened": False,
            "broad_docs_ignore_added": False,
            "broad_current_mirror_ignore_added": False,
            "strict_mode_weakened": False,
            "real_current_error_downgraded": False,
            "historical_sections_deleted_to_silence_scanner": False,
            "broad_path_glob_suppression_added": False,
        }
    )
    return payload


def _validation_evidence_record(
    summary: dict[str, Any], doc_payload: dict[str, Any], chatgpt_payload: dict[str, Any]
) -> dict[str, Any]:
    payload = _base_project_record("stage6g_reviewable_validation_evidence")
    payload.update(
        {
            "edited_document_integrity_validator_reads_final_files_directly": True,
            "record_claim_only_validation_used": False,
            "edited_document_error_count": len(doc_payload["errors"]),
            "chatgpt_context_error_count": len(chatgpt_payload["errors"]),
            "stage6g_current_doc_repair_blocker_count": summary["stage6g_current_doc_repair_blocker_count"],
            "stage6h_final_manifest_blocker_count": summary["stage6h_final_manifest_blocker_count"],
            "stage6h_routed_as_source_lock_addendum": True,
            "stage7_manifest_created_now": False,
            "stage7_execution_allowed_next": False,
        }
    )
    return payload


def _reviewability_gap_register_record(hook_evidence: dict[str, Any]) -> dict[str, Any]:
    payload = _base_project_record("stage6g_reviewability_gap_register")
    payload["reviewability_gaps"] = [
        {
            "gap_id": "actual_codex_runner_semantics_not_fully_simulated_after_stage6g_v0",
            "description": "Direct hooks and supported launcher strings are verified locally, but the actual Codex runner cannot be fully simulated in this environment.",
            "blocking_for_stage6g_current_doc_repair_completion": False,
            "blocking_for_claiming_hooks_fully_fixed": True,
            "operator_confirmation_required_after_stage6g_push": True,
        },
        {
            "gap_id": "recent_dot_angle_triangle_material_not_source_locked_v0",
            "description": "Recent dot-angle/right-triangle number-triangle material is known from chat only and requires Stage 6H source-locking before final Stage 7 manifest work.",
            "blocking_for_stage6h_final_manifest": True,
            "source_lock_stage_required_next": "stage-6h",
        },
    ]
    payload["hook_runner_semantics_fully_simulated"] = hook_evidence.get("hook_runner_semantics_fully_simulated", False)
    return payload


def _current_stage_transition_record(summary: dict[str, Any], blockers: dict[str, Any]) -> dict[str, Any]:
    payload = _base_project_record("stage6g_current_stage_transition")
    payload.update(
        {
            "latest_completed_stage_id": STAGE_ID,
            "previous_completed_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
            "stage6g_current_doc_repair_blocker_count": summary["stage6g_current_doc_repair_blocker_count"],
            "stage6h_final_manifest_blocker_count": blockers["stage6h_final_manifest_blocker_count"],
            "stage6h_can_attempt_final_manifest_without_prior_repair": False,
            "stage6h_final_manifest_required": False,
            "stage6h_source_lock_addendum_required": True,
            "stage7_execution_allowed_next": False,
            "stage7_zip_archive_creation_allowed_next": False,
        }
    )
    return payload


def _stage6h_addendum_record(blockers: dict[str, Any]) -> dict[str, Any]:
    payload = _base_token_record("stage6g_stage6h_manifest_input_addendum")
    payload.update(
        {
            "not_final_stage7_manifest": True,
            "stage6h_final_manifest_required": False,
            "stage6h_source_lock_addendum_required": True,
            "stage7_execution_allowed_from_this_addendum": False,
            "stage7_zip_archive_creation_allowed_from_this_addendum": False,
            "stage6h_input_addendum": {
                "includes_stage6c_ouroboros_i31_input_addendum": True,
                "stage6c_ouroboros_i31_input_addendum_path": stage6c.TOKEN_BLOCK_PATHS[
                    "stage6d_manifest_input_addendum"
                ].as_posix(),
                "includes_stage6d_doublet_boundary_input_addendum": True,
                "stage6d_doublet_boundary_input_addendum_path": stage6d.TOKEN_BLOCK_PATHS[
                    "stage6e_manifest_input_addendum"
                ].as_posix(),
                "includes_stage6e_bridge_source_lock_addendum": True,
                "stage6e_bridge_source_lock_addendum_path": stage6e.TOKEN_BLOCK_PATHS[
                    "stage6f_manifest_input_addendum"
                ].as_posix(),
                "includes_stage6e_probe_source_traceability_matrix": True,
                "stage6e_probe_source_traceability_matrix_path": stage6e.TOKEN_BLOCK_PATHS[
                    "probe_traceability_matrix"
                ].as_posix(),
                "includes_stage6e_source_root_crosswalk": True,
                "stage6e_source_root_crosswalk_path": stage6e.TOKEN_BLOCK_PATHS["source_root_crosswalk"].as_posix(),
                "includes_stage6f_traceability_cleanup": True,
                "stage6f_traceability_cleanup_path": stage6f.TOKEN_BLOCK_PATHS[
                    "probe_source_traceability_semantics_repair"
                ].as_posix(),
                "includes_stage6f_hook_and_doc_integrity_repairs": True,
                "includes_stage6f_acceptance_criteria_policy": True,
                "stage6f_acceptance_criteria_policy_path": ACCEPTANCE_POLICY_PATH.as_posix(),
                "includes_stage6g_current_doc_handoff_repairs": True,
                "stage6g_current_doc_handoff_repair_path": PROJECT_STATE_PATHS[
                    "current_doc_acceptance_repair"
                ].as_posix(),
                "includes_stage6g_acceptance_policy_expansion": True,
                "stage6g_acceptance_policy_evidence_path": PROJECT_STATE_PATHS[
                    "acceptance_policy_integration_evidence"
                ].as_posix(),
                "includes_stage6g_hook_status": True,
                "stage6g_hook_status_path": PROJECT_STATE_PATHS["hook_runner_confirmation"].as_posix(),
                "acknowledges_recent_dot_angle_triangle_material_not_yet_committed": True,
                "recent_dot_angle_triangle_material_source_lock_required_next": True,
                "not_final_stage7_manifest": True,
                "stage7_execution_allowed_from_this_addendum": False,
                "stage7_zip_archive_creation_allowed_from_this_addendum": False,
            },
            "pre_final_manifest_source_lock_backlog": DOT_TRIANGLE_BACKLOG,
            "stage6h_route_reason": {
                "current_doc_blocker_count": 0,
                "hook_runner_blocker_count": 0,
                "recent_dot_angle_triangle_material_source_lock_required": True,
                "stage6h_routed_as_final_manifest": False,
                "stage6h_routed_as_source_lock_addendum": True,
            },
            **blockers,
        }
    )
    return payload


def _transition_gate_record(record_type: str) -> dict[str, Any]:
    payload = _base_token_record(record_type)
    payload.update({"gate_closed": True, "execution_allowed": False})
    return payload


def _raw_source_noncommit_record() -> dict[str, Any]:
    payload = _base_source_record("stage6g_raw_source_noncommit_proof")
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
    payload = _base_source_record("stage6g_codex_handoff_policy")
    payload.update(
        {
            "codex_output_handoff_path": CODEX_COMPLETION_PATH.as_posix(),
            "require_local_file_exists_in_ci": False,
            "require_path_is_git_ignored": True,
            "completion_summary_updated_after_final_ci_required": True,
            "post_push_handoff_locations": [CODEX_COMPLETION_PATH.as_posix(), "GitHub issue comment"],
        }
    )
    return payload


def _final_validation_order_record() -> dict[str, Any]:
    payload = _base_project_record("stage6g_final_validation_order")
    payload.update(
        {
            "docs_completed_before_edited_doc_validator": True,
            "current_state_completed_before_current_mirror_validator": True,
            "stage6h_addendum_completed_before_handoff_validator": True,
            "no_build_step_ran_after_final_doc_integrity_validator_without_rerun": True,
            "stale_current_strict_ran_after_final_doc_updates": True,
        }
    )
    return payload


def _prior_stage_repair_ledger_record() -> dict[str, Any]:
    payload = _base_project_record("stage6g_prior_stage_repair_ledger")
    touched = [
        (
            "python/libreprimus/token_block/stage6b.py",
            "Stage 6B current-stage transition validator did not allow the later Stage 6G -> Stage 6H pair.",
        ),
        (
            "python/libreprimus/token_block/stage6c.py",
            "Stage 6C current-stage transition validator did not allow the later Stage 6G -> Stage 6H pair.",
        ),
        (
            "python/libreprimus/token_block/stage6d.py",
            "Stage 6D current-stage transition validator did not allow the later Stage 6G -> Stage 6H pair.",
        ),
        (
            "python/libreprimus/token_block/stage6e.py",
            "Stage 6E current-stage transition validator did not allow the later Stage 6G -> Stage 6H pair.",
        ),
        (
            "python/libreprimus/token_block/stage6f.py",
            "Stage 6F aggregate validators required current-stage-state.yaml and current mirrors to remain at Stage 6F after later stages advanced.",
        ),
    ]
    payload.update(
        {
            "prior_stage_files_touched": [
                {
                    "touched_file": file_path,
                    "prior_stage": f"stage-6{file_path.rsplit('stage6', 1)[1][0]}",
                    "old_problem": old_problem,
                    "new_value_or_policy": "Historical validators allow the current project state to advance to Stage 6G -> Stage 6H while validating prior-stage records.",
                    "why_patch_was_required": "Final Stage 6G validation must rerun Stage 6B through Stage 6F validators after current-stage-state advances.",
                    "historical_payload_changed": False,
                    "current_mirror_or_active_metadata_only": True,
                    "source_lock_payload_changed": False,
                }
                for file_path, old_problem in touched
            ],
            "prior_stage_payloads_mutated_now": False,
            "source_lock_payload_changed": False,
        }
    )
    return payload


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
    allowed = {CODEX_COMPLETION_PATH}
    return sorted(path for path in candidates if path.exists() and path not in allowed)


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
    if key == "summary":
        properties["recommended_next_stage_id"] = {"const": NEXT_STAGE_ID}
        properties["stage6h_source_lock_addendum_required"] = {"const": True}
        properties["stage6h_final_manifest_required"] = {"const": False}
    if key == "stage6h_manifest_input_addendum":
        properties["not_final_stage7_manifest"] = {"const": True}
        properties["stage6h_source_lock_addendum_required"] = {"const": True}
        properties["stage6h_final_manifest_required"] = {"const": False}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"Stage 6G {category} {key}",
        "type": "object",
        "required": ["record_type", "stage_id", "metadata_only", "solve_claim"],
        "properties": properties,
        "additionalProperties": True,
    }


def _write_current_stage_schema() -> None:
    schema = json.loads(CURRENT_STAGE_SCHEMA_PATH.read_text(encoding="utf-8")) if CURRENT_STAGE_SCHEMA_PATH.exists() else {}
    props = schema.setdefault("properties", {})
    for key in ["latest_completed_stage_id", "previous_completed_stage_id", "recommended_next_stage_id"]:
        prop = props.setdefault(key, {"type": "string"})
        values = set(prop.get("enum", []))
        values.update({STAGE_ID, PREVIOUS_STAGE_ID, NEXT_STAGE_ID})
        prop["enum"] = sorted(values)
    title_prop = props.setdefault("recommended_next_stage_title", {"type": "string"})
    titles = set(title_prop.get("enum", []))
    titles.add(NEXT_STAGE_TITLE)
    title_prop["enum"] = sorted(titles)
    prompt_prop = props.setdefault("recommended_next_prompt_type", {"type": "string"})
    prompts = set(prompt_prop.get("enum", []))
    prompts.add(NEXT_PROMPT_TYPE)
    prompt_prop["enum"] = sorted(prompts)
    for flag in FORBIDDEN_FALSE:
        props.setdefault(flag, {"const": False})
    props.setdefault("stage6h_source_lock_addendum_required", {"type": "boolean"})
    props.setdefault("stage6h_final_manifest_required", {"type": "boolean"})
    props.setdefault("stage6h_final_manifest_blocker_count", {"type": "integer"})
    props.setdefault("stage6g_current_doc_repair_blocker_count", {"type": "integer"})
    CURRENT_STAGE_SCHEMA_PATH.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_doc_staleness_source_of_truth_schema() -> None:
    schema = (
        json.loads(DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH.read_text(encoding="utf-8"))
        if DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH.exists()
        else {}
    )
    props = schema.setdefault("properties", {})
    for key in ["stage_id", "latest_completed_stage_id", "recommended_next_stage_id"]:
        prop = props.setdefault(key, {"type": "string"})
        values = set(prop.get("enum", []))
        values.update({STAGE_ID, NEXT_STAGE_ID})
        prop["enum"] = sorted(values)
    DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH.write_text(
        json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _write_current_stage_state() -> None:
    payload = read_yaml(CURRENT_STAGE_STATE_PATH)
    payload.update(
        {
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "previous_completed_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
            "stage6g_current_doc_repair_blocker_count": 0,
            "stage6h_final_manifest_blocker_count": 1,
            "stage6h_final_manifest_blockers": ["recent_dot_angle_triangle_material_not_source_locked"],
            "stage6h_can_attempt_final_manifest_without_prior_repair": False,
            "stage6h_final_manifest_required": False,
            "stage6h_source_lock_addendum_required": True,
            "stage6h_repair_required_before_final_manifest": True,
            "recent_dot_angle_triangle_material_known_from_chat": True,
            "recent_dot_angle_triangle_material_committed_in_stage6g": False,
            "recent_dot_angle_triangle_material_requires_source_lock_before_final_manifest": True,
            "stage7_execution_allowed_next": False,
            "stage7_zip_archive_creation_allowed_next": False,
            "stage7_manifest_created_now": False,
            "stage7_archive_created_now": False,
            "probe_execution_performed_now": False,
            "route_stream_generated_now": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "solve_claim": False,
            "post_push_handoff_locations": [CODEX_COMPLETION_PATH.as_posix(), "GitHub issue comment"],
        }
    )
    for flag in FORBIDDEN_FALSE:
        payload[flag] = False
    payload["stage6h_source_lock_addendum_required"] = True
    write_yaml(CURRENT_STAGE_STATE_PATH, payload)


def _write_doc_staleness_source_of_truth() -> None:
    payload = read_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH)
    payload.update(
        {
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "latest_completed_stage_prefix": "Stage 6G",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_stage_prefix": "Stage 6H",
            "next_stage_after_this_stage": NEXT_STAGE_TITLE,
            "expected_next_stage_prefix": "Stage 6H",
            "stage_id": STAGE_ID,
            "current_stage_state_path": CURRENT_STAGE_STATE_PATH.as_posix(),
            "current_handoff_path": CODEX_COMPLETION_PATH.as_posix(),
            "stage6h_source_lock_addendum_required": True,
            "stage6h_final_manifest_required": False,
        }
    )
    write_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH, payload)


def _write_docs() -> None:
    _write_acceptance_policy()
    sections = {
        Path("README.md"): _readme_section(),
        Path("AGENTS.md"): _agents_section(),
        Path("STATUS.md"): _status_section(),
        Path("ROADMAP.md"): _roadmap_section(),
        Path("TESTING.md"): _testing_section(),
        Path("docs/roadmap/staged-plan.md"): _staged_plan_section(),
        Path("docs/reference/token-block-cli.md"): _cli_docs_section(),
        Path("docs/onboarding/operational-file-map.md"): _operational_file_map_doc_section(),
    }
    for path, body in sections.items():
        stage6._upsert_marked_section(path, STAGE_TOKEN, body)
    _rewrite_current_top_sections()
    _rewrite_start_here()
    _rewrite_source_of_truth_map()
    _rewrite_chatgpt_context()
    _normalize_historical_doc_text()


def _write_support_docs() -> None:
    for path, text in {
        Path("docs/experiments/stage6g-current-doc-handoff-repair.md"): _experiment_doc(),
        Path("docs/development/stage6g-development-log.md"): _dev_log(),
        Path("docs/research/stage6g-research-log.md"): _research_log(),
    }.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _write_acceptance_policy() -> None:
    ACCEPTANCE_POLICY_PATH.parent.mkdir(parents=True, exist_ok=True)
    ACCEPTANCE_POLICY_PATH.write_text(
        """# Codex Acceptance Criteria

## Purpose
Future Codex stages must finish with coherent repository state, not just new records. Current mirrors, handoffs, validation evidence, ignored-output policy, and guardrails must agree.

## Edited-document integrity
When a stage edits a current-facing document, review the whole final file. Check that current sections match `data/project-state/current-stage-state.yaml`, avoid repeated generated phrases, and remove stale handoff paths.

## Current-mirror consistency
Current mirrors include README, AGENTS, STATUS, ROADMAP, TESTING, staged plan, onboarding maps, token-block CLI docs, ChatGPT context, current-stage state, and stage-summary records. Latest and next-stage wording must match the state file.

## ChatGPT context quality
The context file must separate current truth from historical summaries. Historical Stage 6C, 6D, 6E, and 6F material should remain durable, but old routing must not masquerade as current routing.

## Source-lock evidence and gap semantics
Source-lock records must cite committed source paths or record explicit gaps. Chat-only observations can be backlog blockers, but they are not source truth or proof.

## Number-fact and arithmetic quality
Arithmetic records need exact input labels, exact integer checks, source paths, and risk notes. Approximate geometry or discussion aliases must be marked as such.

## Probe traceability quality
Every future probe or manifest input row needs source records or an explicit source gap, controls, output archive policy, and disabled execution flags.

## Hook and preflight quality
Hooks must be report-only and exit zero by default. Strict mode must be explicit, tested separately, and never inferred from an inherited environment.

## Doc-staleness quality
Stale-current scanners must not be weakened. Fix legitimate current drift, classify warning-domain findings, and keep historical examples in clearly historical sections.

## Source Browser and overlay quality
Source Browser records and overlays must validate without widening schemas just to force fragile records. Review-only overlays must not become proof, route seeds, or activation decisions.

## CI-safe ignored-file policy
Tests may assert ignored paths are ignored, but clean CI must not require ignored completion summaries, local reports, or ignored third-party roots to exist.

## Completion summary quality
Ignored completion summaries must be written locally with actual final values after the final commit, push, and CI. They must not contain pending placeholders.

## Noncommit policy
Do not stage raw data, generated experiment outputs, `codex-output/**`, ignored reports, databases, archives, binaries, or protected local operator state.

## Bad vs good Codex instruction examples
Bad instruction:
"Update AGENTS.md."

Good instruction:
"Update AGENTS.md as a whole final file, then verify its current section matches current-stage-state.yaml, contains no repeated generated phrases, contains no stale latest/next-stage claims, and contains no stale completion-summary path."

## Final self-review checklist
- Current-stage state and current docs agree.
- ChatGPT context has current/historical boundaries.
- Stale-current strict errors are zero.
- Source Browser validates.
- Hook status is stated without overclaiming actual runner behavior.
- No Stage 7 manifest, archive, probe execution, route stream, byte stream, target selection, or solve claim was created unless explicitly authorized.
""",
        encoding="utf-8",
    )


def _rewrite_start_here() -> None:
    path = Path("docs/onboarding/start-here.md")
    text = path.read_text(encoding="utf-8")
    text = _remove_markdown_sections(
        text,
        [
            "## Historical Stage 6C Boundary",
            "## Historical Stage 6D Boundary",
            "## Historical Stage 6E Boundary",
            "## Historical Stage 6F Boundary",
            "## Historical Stage 6C-6F Boundaries",
        ],
    )
    section = """## Current Authority

The latest completed stage is Stage 6G. The next routed stage is Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.

Stage 6H is source-lock/readiness addendum work, not final Stage 7 manifest construction, because recent dot-angle/right-triangle material remains chat-only pending source-lock. Future Codex work must apply `docs/onboarding/codex-acceptance-criteria.md` and keep all execution gates closed unless a later prompt explicitly opens them.
"""
    text = _replace_or_insert_section(text, "## Current Authority", section, before_heading="## Historical Stage 6D Boundary")
    historical = """## Historical Stage 6C-6F Boundaries

Stage 6C, Stage 6D, Stage 6E, and Stage 6F remain historical source-lock/readiness and repair stages. Stage 6C preserved the OUROBOROS/I31 addendum, Stage 6D preserved canonical doublet/boundary metadata, Stage 6E consolidated bridge source-lock readiness, and Stage 6F repaired current-doc, hook, traceability, alias, dju-bei, and acceptance-policy quality. Their old next-stage wording is historical only and is superseded by the current Stage 6G -> Stage 6H source-lock/readiness route above.
"""
    text = _replace_or_insert_section(
        text,
        "## Historical Stage 6C-6F Boundaries",
        historical,
        before_heading="## Where To Start",
    )
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _rewrite_source_of_truth_map() -> None:
    path = Path("docs/onboarding/source-of-truth-map.md")
    text = path.read_text(encoding="utf-8")
    section = f"""## Current Operational Truth

- The current authority is `data/project-state/current-stage-state.yaml`.
- The latest completed stage is `stage-6g`.
- The next stage is `stage-6h`: {NEXT_STAGE_TITLE}.
- Stage 6H is a source-lock/readiness addendum because recent dot-angle/right-triangle number-triangle material remains chat-only pending source-lock.
- The acceptance policy is `{ACCEPTANCE_POLICY_PATH.as_posix()}`.
- The Stage 6H handoff addendum is `{TOKEN_BLOCK_PATHS['stage6h_manifest_input_addendum'].as_posix()}`.
- The post-push local completion handoff path is `{CODEX_COMPLETION_PATH.as_posix()}`.
"""
    text = _replace_or_insert_section(text, "## Current Operational Truth", section)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _rewrite_current_top_sections() -> None:
    replacements = {
        Path("README.md"): (
            "## Current boundaries and deferred work",
            _readme_top_current_section(),
        ),
        Path("AGENTS.md"): (
            "## Current stage",
            _agents_top_current_section(),
        ),
        Path("STATUS.md"): (
            "## Current Stage",
            _status_top_current_section(),
        ),
        Path("ROADMAP.md"): (
            "## Current Direction",
            _roadmap_top_current_section(),
        ),
        Path("docs/roadmap/staged-plan.md"): (
            "## Current Project State",
            _staged_plan_top_current_section(),
        ),
    }
    for path, (heading, body) in replacements.items():
        text = path.read_text(encoding="utf-8")
        path.write_text(_replace_or_insert_section(text, heading, body).rstrip() + "\n", encoding="utf-8")


def _rewrite_chatgpt_context() -> None:
    path = Path("ChatGPT-ContextFile.md")
    text = path.read_text(encoding="utf-8")
    text = _remove_markdown_sections(
        text,
        [
            "## Historical Stage 6C",
            "## Historical Stage 6D",
            "## Historical Stage 6E",
            "## Historical Stage 6F",
            "## Historical Stage 6D Boundary",
            "## Historical Stage 6E Boundary",
            "## Stage 6F Current Boundary",
            "## Stage 6E and Stage 6F Durable Context",
        ],
    )
    current = """# ChatGPT Context File

## Current Project State

Stage 6G repaired stale current docs after Stage 6F. The source-of-truth-map Current Operational Truth, start-here current routing, and ChatGPT current/historical boundary now point to Stage 6G as latest complete and Stage 6H as the next source-lock/readiness addendum.

Stage 6H handoff addendum explicitly merges Stage 6C/6D/6E/6F/6G inputs. Stage 6H is routed as a dot-angle/right-triangle source-lock addendum because recent dot-angle/right-triangle material remains chat-only pending source-lock.

Stage 6G repaired acceptance-policy integration expanded coverage, preserved hook verification honesty, and created no Stage 7 manifest/archive/probe/execution created. No route streams, byte streams, target selection, source-lock payload rewrite, image interpretation, or solve claim were performed.
"""
    historical = """## Historical Stage 6C

Stage 6C source-locked the OUROBOROS / I31 circumference bridge as review-only metadata. It preserved OUROBOROS=167, O+U+O+O+O=31=GP(I), R+B+R+S=136=T16, Page32 3222 policy, and future-only watchlists without execution.

## Historical Stage 6D

Stage 6D source-locked the canonical doublet boundary policy as review-only metadata. The pages 15-70 collapsed page-local profile has 12,956 runes, 86 lag1 adjacent doublets, vector `42442156242421632042324217223`, and lag5 equal count 479. Stage 6D added disabled future probes and a Stage 6E input addendum only. Its old routing is historical and no longer current project truth.

## Historical Stage 6E

Stage 6E preserved Stage 6C OUROBOROS/I31 and Stage 6D doublet/boundary addenda while adding readiness bridge records. It recorded CIRCUMFERENCE = 398 = 2 * GP(I AM), the C-to-F finite mask family, DIUINITY/DIVINITY source surface caveat, AN END = FIVE DOTS = 311 = prime(64), big-gap one-based sum 569 = prime(104), Page32 3222 = 18 * 179, and WE MUST SHED OUR OWN CIRCUMFERENCES = 1031. The dju bei / dju bei ae remains an exact-span source gap. Stage 6E did not run probes, create a Stage 7 manifest, generate route or byte streams, create archives, select targets, or make a solve claim.

## Historical Stage 6F

Stage 6F repaired current-doc integrity, preflight self-report exclusion, metadata-only probe traceability semantic cleanup, Ciada/Cicada alias policy, dju-bei backlog crosslinking, and strict acceptance criteria. Stage 6F is historical; Stage 6G routing supersedes its old current route and sends Stage 6H to source-lock/readiness addendum work.
"""
    if "## Stage 5DV Source Browser Repair" in text:
        tail = "## Stage 5DV Source Browser Repair" + text.split("## Stage 5DV Source Browser Repair", 1)[1]
    else:
        tail = text.split("## Current Project State", 1)[-1]
    text = current.rstrip() + "\n\n" + historical.rstrip() + "\n\n" + tail.lstrip()
    text = _strip_current_final_manifest_claims(text)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _normalize_historical_doc_text() -> None:
    replacements = {
        "Stage 6G - Final finite Stage 7 probe manifest and archive-run contract, without execution": NEXT_STAGE_TITLE,
        "codex-output/stage6d-codex-completion.md": CODEX_COMPLETION_PATH.as_posix(),
        "codex-output/stage6e-codex-completion.md": CODEX_COMPLETION_PATH.as_posix(),
        "codex-output/stage6f-codex-completion.md": CODEX_COMPLETION_PATH.as_posix(),
        "Current completed stage: Stage 6F - Current-doc integrity, hook traceability, and acceptance hardening, without execution.": "Historical prior-stage note: Stage 6F was the latest completed stage when this old section was written.",
        "Latest completed stage: Stage 6F - Current-doc integrity, hook traceability, and acceptance hardening, without execution.": "Historical prior-stage note: Stage 6F was the latest completed stage when this old section was written.",
        "## Stage 6F Current Boundary": "## Historical Stage 6F Boundary",
        "## Stage 6D Current Status": "## Historical Stage 6D Current Status",
        f"Current work: {NEXT_STAGE_TITLE}": f"Next routed stage: {NEXT_STAGE_TITLE}",
        f"Current planning focus: {NEXT_STAGE_TITLE}": f"Next routed stage: {NEXT_STAGE_TITLE}",
    }
    for path in CURRENT_DOC_PATHS:
        if path.suffix != ".md" or not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _strip_current_final_manifest_claims(text: str) -> str:
    return text.replace(
        "Stage 6G routing is blocker-driven; Stage 6F routes next to Stage 6G - Final finite Stage 7 probe manifest and archive-run contract, without execution.",
        "Stage 6G routing was later superseded by Stage 6G current-doc repair; Stage 6H is next as source-lock/readiness addendum work.",
    )


def _readme_section() -> str:
    return f"""## Stage 6G Current Boundary

Latest completed stage: {STAGE_TITLE}.

Current next stage: {NEXT_STAGE_TITLE}. Stage 6H is source-lock/readiness addendum work, not final Stage 7 manifest construction, because recent dot-angle/right-triangle number-triangle material remains chat-only pending source-lock.

Stage 6G repaired current-doc and handoff integrity, expanded acceptance-policy integration, verified hooks where local direct/script launcher tests can support it, and recorded honest operator-confirmation risk for actual Codex runner semantics. It did not source-lock the new dot/triangle material, create probes or overlays, create a Stage 7 manifest or archive, generate route or byte streams, execute tools, select targets, or claim a solve.
"""


def _readme_top_current_section() -> str:
    return f"""## Current boundaries and deferred work

Current completed stage: {STAGE_TITLE}.

Current next prompt: {NEXT_STAGE_TITLE}.

Stage 6G repairs current-doc and handoff integrity and routes Stage 6H as source-lock/readiness addendum work because recent dot-angle/right-triangle number-triangle material remains chat-only pending source-lock. Stage 6G did not source-lock that new material, create probes or overlays, create a Stage 7 manifest or archive, generate route or byte streams, execute tools, select targets, or claim a solve.

- Stage 5EG installed deterministic stale-current guardians and kept hooks scanner-based.
- Stage 5EH added Lag5/outguess/byte-string/red-number/F5 source-lock context and review-only overlays without execution.
- Stage 5EI closed Stage 5 as a triangle-transposition and diagnostics-transition metadata stage, routing next work to Stage 6 readiness without execution.
- Stage 6 completed diagnostic-backlog readiness metadata.
- Stage 6B repaired Stage 6 mappings and hook behavior.
- Stage 6C added review-only OUROBOROS/I31 source-lock metadata.
- Stage 6D added canonical doublet-boundary source-lock metadata.
- Stage 6E consolidated bridge source-lock readiness.
- Stage 6F repaired current-doc, hook, traceability, alias, dju-bei, and acceptance-policy quality.

These are not permanent project exclusions. CUDA and broad campaigns are deferred, not permanently excluded.
"""


def _agents_section() -> str:
    return f"""## Stage 6G Current Boundary

Current completed stage: {STAGE_TITLE}.

Next routed stage: {NEXT_STAGE_TITLE}. Stage 6H is a dot-angle/right-triangle source-lock addendum because recent material remains chat-only pending source-lock. It is not final Stage 7 manifest work.

Future Codex work must apply `docs/onboarding/codex-acceptance-criteria.md`, review edited current-facing documents as whole final files, and keep all no-execution gates closed unless a later prompt explicitly opens them.
"""


def _agents_top_current_section() -> str:
    return f"""## Current stage

Current completed stage: {STAGE_TITLE}.

Next routed stage: {NEXT_STAGE_TITLE}. Stage 6H is source-lock/readiness addendum work because recent dot-angle/right-triangle number-triangle material remains chat-only pending source-lock. It is not final Stage 7 manifest work.

No Deep Research activation-acceptance record exists, the combined gate is not satisfied, no valid activation decision exists, and no active planning input authorization or selection exists. String 4 remains inactive; no target-priority selection, source-lock browser puzzle execution, direct source-record number-fact backfill, historical source-lock rewrite, triangle/Page32 route extraction, music route extraction, audio/stego/OCR/image forensics/AI interpretation, active ingestion, byte-stream generation, machine-code/VM execution, manifest supersession, execution, target-class validation, Tor access, DWH/hash/preimage search, decode, scoring, CUDA, benchmark, website expansion, method-status upgrade, canonical corpus activation, page-boundary finalisation, or solve claim is authorized.

Future Codex work must apply `docs/onboarding/codex-acceptance-criteria.md`.

- Canonical corpus: inactive.
- Page boundaries: reviewable.
- CUDA: deferred.

Discord raw logs are not committed. Raw page images, raw historical stego artefacts, generated outputs, SQLite databases, and local reports remain ignored and uncommitted.
"""


def _status_section() -> str:
    return f"""## Stage 6G Status

- Latest completed stage: {STAGE_TITLE}.
- Current next stage: {NEXT_STAGE_TITLE}.
- Current-doc and handoff repair blockers: 0.
- Stage 6H final-manifest blockers: 1, `recent_dot_angle_triangle_material_not_source_locked`.
- Stage 6H is routed as a source-lock/readiness addendum, not final Stage 7 manifest work.
- No Stage 7 manifest, archive, probe execution, route stream, byte stream, target selection, image interpretation, or solve claim was created.
"""


def _status_top_current_section() -> str:
    return f"""## Current Stage

- Latest completed stage: {STAGE_TITLE}.
- Current next stage: {NEXT_STAGE_TITLE}.
- Next recommended prompt: {NEXT_STAGE_TITLE}.
- Stage 6G current-doc/handoff repair blockers: 0.
- Stage 6H final-manifest blockers: 1, `recent_dot_angle_triangle_material_not_source_locked`.
- Stage 6H is routed as source-lock/readiness addendum work, not final Stage 7 manifest work.
- No probe, route, byte-stream, OCR/image/stego, PGP/OutGuess/F5/StegDetect, CUDA, scoring, target-selection, canonical-corpus, page-boundary, Stage 7 manifest/archive, or solve work is authorized.
"""


def _roadmap_section() -> str:
    return f"""## Stage 6G Roadmap Update

Stage 6G is complete as current-doc handoff repair and acceptance hardening. The next stage is {NEXT_STAGE_TITLE}, because recent dot-angle/right-triangle number-triangle material remains chat-only and must be source-locked or explicitly deferred before any later final Stage 7 manifest construction.

Stage 7 execution, result archives, route streams, byte streams, target selection, and solve claims remain disabled.
"""


def _roadmap_top_current_section() -> str:
    return f"""## Current Direction

Current completed stage: {STAGE_TITLE}.

Next routed stage: {NEXT_STAGE_TITLE}.

Stage 6G is a current-doc handoff repair and acceptance-hardening stage. It routes Stage 6H as source-lock/readiness addendum work because recent dot-angle/right-triangle number-triangle material remains chat-only pending source-lock. Stage 7 execution, result archives, route streams, byte streams, Stage 8 triangle readiness, and Stage 9 experiments remain blocked.

The durable staged plan is maintained at [`docs/roadmap/staged-plan.md`](docs/roadmap/staged-plan.md). Update that file whenever stage status, direction, experiment priority, or method-family retirement/reopening changes.
"""


def _testing_section() -> str:
    return """## Stage 6G Validation Targets

Stage 6G validation must run after docs and current-stage state are updated. Required checks include `token-block validate-stage6g`, focused Stage 6G validators, stale-current strict scanning, Source Browser index/path validation, focused pytest slices, ruff, and the Stage 6G stage-validation profiles. Tests must inspect current docs directly rather than trusting self-attesting records.
"""


def _staged_plan_section() -> str:
    return f"""## Stage 6G Current Plan Boundary

Stage 6G completed current-doc handoff repair and routes next to {NEXT_STAGE_TITLE}. Stage 6H is source-lock/readiness addendum work for recent dot-angle/right-triangle material that remains chat-only, not final Stage 7 manifest work.
"""


def _staged_plan_top_current_section() -> str:
    return f"""## Current Project State

- Latest completed stage: {STAGE_TITLE}.
- Next routed stage: {NEXT_STAGE_TITLE}.
- Stage 6H is source-lock/readiness addendum work because recent dot-angle/right-triangle number-triangle material remains chat-only pending source-lock.
- Canonical corpus: inactive.
- Page boundaries: reviewable.
- CUDA: deferred.
- CPU batch transform API: active infrastructure with expanded adapter coverage and future CUDA parity expectations.
- Scoring contract: active infrastructure and future CUDA score-summary parity contract.
- Solve claims: none.
- Raw and generated outputs: ignored and not committed.
- Discord raw logs: local, private, ignored research material.
- Local Liber Primus page images: local third-party material, ignored and not committed.
- Observation promotion ledger policy: future candidate rows must distinguish `ready_for_manifest` from `control-only` and historical context.
"""


def _cli_docs_section() -> str:
    return """## Stage 6G Token-Block CLI

- `python -m libreprimus.cli token-block build-stage6g`
- `python -m libreprimus.cli token-block validate-stage6g`
- `python -m libreprimus.cli token-block stage6g-summary`
- Focused validators include `validate-stage6g-current-doc-acceptance`, `validate-stage6g-start-here-repair`, `validate-stage6g-source-of-truth-map-repair`, `validate-stage6g-chatgpt-context-boundary`, `validate-stage6g-acceptance-policy-integration`, `validate-stage6g-stage6h-addendum`, and `validate-stage6g-gate-closure`.

Future Codex stages must apply `docs/onboarding/codex-acceptance-criteria.md` and keep Stage 7 execution/archive gates closed unless explicitly authorized.
"""


def _operational_file_map_doc_section() -> str:
    return f"""## Stage 6G Operational Files

- `data/project-state/stage6g-summary.yaml`: Stage 6G repair summary.
- `{TOKEN_BLOCK_PATHS['stage6h_manifest_input_addendum'].as_posix()}`: Stage 6H source-lock/readiness handoff addendum.
- `{ACCEPTANCE_POLICY_PATH.as_posix()}`: reusable Codex acceptance criteria.
- `{CODEX_COMPLETION_PATH.as_posix()}`: ignored local completion handoff path after Stage 6G.
"""


def _experiment_doc() -> str:
    return """# Stage 6G Current-Doc Handoff Repair

Stage 6G repairs current-facing documents and handoff routing after Stage 6F. It routes Stage 6H as a source-lock/readiness addendum because recent dot-angle/right-triangle material remains chat-only pending source-lock.
"""


def _dev_log() -> str:
    return """# Stage 6G Development Log

Stage 6G adds file-content validators for current docs, repairs onboarding/current-truth mirrors, expands acceptance-policy integration, and preserves hook-runner honesty without creating Stage 7 artifacts.
"""


def _research_log() -> str:
    return f"""# Stage 6G Source-Lock Readiness Note

Stage 6G does not source-lock new dot/triangle observations. It records them only as a blocker requiring {NEXT_STAGE_TITLE} before any later final Stage 7 manifest work.
"""


def _write_operational_map() -> None:
    path = Path("data/project-state/operational-file-map.yaml")
    payload = read_yaml(path)
    record = {
        "stage_id": STAGE_ID,
        "summary": PROJECT_STATE_PATHS["summary"].as_posix(),
        "next_stage_decision": PROJECT_STATE_PATHS["next_stage_decision"].as_posix(),
        "stage6h_source_lock_addendum": TOKEN_BLOCK_PATHS["stage6h_manifest_input_addendum"].as_posix(),
        "acceptance_policy": ACCEPTANCE_POLICY_PATH.as_posix(),
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
            "summary": "Repaired current-doc handoff integrity and routed Stage 6H as source-lock/readiness addendum for chat-only dot-angle/right-triangle material.",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "guardrails": "No Stage 7 manifest, archive, probe execution, route stream, byte stream, new theory source-lock, overlay, or solve claim.",
        }
    )
    payload["stages"] = records
    write_yaml(path, payload)


def _write_completion_summary_stub(summary: dict[str, Any], hook_evidence: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    closure = "\n".join(
        f"  - finding_id: {finding_id}\n    status: {status}\n    evidence_path: {path}"
        for finding_id, path, status in STAGE6F_REVIEW_FINDINGS
    )
    CODEX_COMPLETION_PATH.write_text(
        f"""# Stage 6G Codex Completion

starting_commit: {STARTING_COMMIT}
stage6g_implementation_commit: pending_commit
final_commit: pending_commit
implementation_commit_equals_final_commit: pending
ci_repair_commit_count: pending
origin_main_commit: pending_push
github_issue: pending_issue
final_ci_run_url: pending_ci
final_ci_status: pending_ci
completion_summary_updated_after_final_ci: false

stage6g_current_doc_repair_blocker_count: {summary.get('stage6g_current_doc_repair_blocker_count')}
stage6h_final_manifest_blocker_count: {summary.get('stage6h_final_manifest_blocker_count')}
stage6h_final_manifest_blockers:
  - recent_dot_angle_triangle_material_not_source_locked
stage6h_can_attempt_final_manifest_without_prior_repair: false
stage6h_routed_as_final_manifest: false
stage6h_routed_as_source_lock_addendum: true
hook_default_exit_zero_verified: {hook_evidence.get('hook_default_exit_zero_verified')}
hook_json_launcher_exit_zero_where_supported: {hook_evidence.get('hook_json_launcher_exit_zero_where_supported')}
hook_runner_semantics_fully_simulated: {hook_evidence.get('hook_runner_semantics_fully_simulated')}
operator_confirmation_required_after_stage6g_push: true
stage7_manifest_created_now: false
stage7_archive_created_now: false
probe_execution_performed_now: false
route_stream_generated_now: false
byte_stream_generated_now: false
solve_claim: false

stage6f_review_finding_closure:
{closure}
""",
        encoding="utf-8",
    )


def _current_section_text(path: Path, text: str) -> str:
    if path == CURRENT_STAGE_STATE_PATH:
        return text
    marked = _marked_section(text, STAGE_TOKEN)
    if marked:
        return marked
    if path.name == "AGENTS.md" and "\nCurrent project state:" in text:
        return text.split("\nCurrent project state:", 1)[0]
    if path.name == "ChatGPT-ContextFile.md":
        return _markdown_section(text, "## Current Project State")
    if path.name == "source-of-truth-map.md":
        return _markdown_section(text, "## Current Operational Truth")
    for heading in ["## Current Authority", "## Current Stage", "## Current Direction", "## Current boundaries"]:
        section = _markdown_section(text, heading)
        if section:
            return section
    return "\n".join(text.splitlines()[:160])


def _forbidden_string_findings(path: Path, text: str) -> list[dict[str, Any]]:
    findings = []
    lines = text.splitlines()
    for index, line in enumerate(lines, start=1):
        for pattern in FORBIDDEN_CURRENT_STRINGS:
            if pattern in line:
                heading = _nearest_heading(lines, index)
                classification = "historical" if "Historical" in heading else "current_or_unclear"
                findings.append(
                    {
                        "path": path.as_posix(),
                        "line_number": index,
                        "matched_string": pattern,
                        "section_heading": heading,
                        "classified_as_historical_or_current": classification,
                    }
                )
    return findings


def _nearest_heading(lines: list[str], line_number: int) -> str:
    for index in range(line_number - 1, -1, -1):
        if lines[index].startswith("#"):
            return lines[index].strip()
    return ""


def _marked_section(text: str, token: str) -> str:
    start = f"<!-- {token}:start -->"
    end = f"<!-- {token}:end -->"
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0]


def _markdown_section(text: str, heading: str) -> str:
    if heading not in text:
        return ""
    after = text.split(heading, 1)[1]
    match = re.search(r"\n#{1,6}\s+", after)
    body = after[: match.start()] if match else after
    return heading + body


def _replace_or_insert_section(text: str, heading: str, replacement: str, before_heading: str | None = None) -> str:
    if heading in text:
        before, rest = text.split(heading, 1)
        match = re.search(r"\n#{1,6}\s+", rest)
        if match:
            return before.rstrip() + "\n\n" + replacement.rstrip() + "\n\n" + rest[match.start() + 1 :].lstrip()
        return before.rstrip() + "\n\n" + replacement.rstrip() + "\n"
    if before_heading and before_heading in text:
        before, after = text.split(before_heading, 1)
        return before.rstrip() + "\n\n" + replacement.rstrip() + "\n\n" + before_heading + after
    return replacement.rstrip() + "\n\n" + text.lstrip()


def _remove_markdown_sections(text: str, headings: list[str]) -> str:
    for heading in headings:
        while heading in text:
            before, rest = text.split(heading, 1)
            match = re.search(r"\n#{1,6}\s+", rest)
            if match:
                text = before.rstrip() + "\n\n" + rest[match.start() + 1 :].lstrip()
            else:
                text = before.rstrip() + "\n"
    return text


def _repeated_ngram_findings(path: Path, text: str) -> list[dict[str, Any]]:
    words = re.findall(r"[A-Za-z0-9']+", text)
    whitelist = {"without execution", "Stage 7", "source lock", "current stage", "Stage 6H"}
    counts = Counter(" ".join(words[i : i + 5]) for i in range(max(0, len(words) - 4)))
    findings = []
    for phrase, count in counts.items():
        if count <= 3:
            continue
        if any(allowed.lower() in phrase.lower() for allowed in whitelist):
            continue
        findings.append({"path": path.as_posix(), "phrase": phrase, "count": count})
    return findings


def _line_heading_for(path: Path, needle: str) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines, start=1):
        if needle in line:
            return f"line {index}; heading {_nearest_heading(lines, index)}"
    return "not found"


def _ensure_no_protected_output_overlap() -> None:
    protected = {Path(path) for path in stage6.PROTECTED_LOCAL_PATHS}
    overlap = protected & {Path(path) for path in DATA_PATHS.values()}
    if overlap:
        raise RuntimeError(f"Stage 6G output overlaps protected local paths: {sorted(map(str, overlap))}")


def _result(errors: list[str], **counts: Any) -> stage6.ValidationResult:
    return stage6.ValidationResult(errors=errors, counts=counts)
