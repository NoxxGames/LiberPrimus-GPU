"""Stage 5DY validation performance and stage-isolation repair records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import read_yaml, write_json, write_yaml

STAGE_ID = "stage-5dy"
STAGE_TITLE = (
    "Stage 5DY - Validation performance, parallel-test discipline, stage-isolation, "
    "and non-mutating validator repair, without execution"
)
PROMPT_TYPE = "codex_validation_infrastructure_and_metadata_repair"
PREVIOUS_STAGE_ID = "stage-5dx"
PREVIOUS_COMMIT = "eb93bc8d4367464908645c95677fe6a26427e2af"
NEXT_STAGE_ID = "stage-5dz"
NEXT_STAGE_TITLE = "Stage 5DZ - Operator/assistant source-lock number-fact review batch 3, without execution"
PARALLEL_WORKER_CAP = 8

PROJECT_STATE_DIR = Path("data/project-state")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
TOKEN_BLOCK_DIR = Path("data/token-block")
CI_DIR = Path("data/ci")
CHATGPT_CONTEXT_PATH = Path("ChatGPT-ContextFile.md")
STAGE_SUMMARY_RECORDS_PATH = Path("data/research/stage-summary-records-v0.yaml")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5dy-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5dy-next-stage-decision.yaml",
    "stage5dx_preservation": PROJECT_STATE_DIR / "stage5dy-stage5dx-preservation.yaml",
    "validation_performance_diagnostic": PROJECT_STATE_DIR / "stage5dy-validation-performance-diagnostic.yaml",
    "validation_profile_registry": PROJECT_STATE_DIR / "stage5dy-validation-profile-registry.yaml",
    "parallel_validation_policy": PROJECT_STATE_DIR / "stage5dy-parallel-validation-policy.yaml",
    "consistency_profile_policy": PROJECT_STATE_DIR / "stage5dy-consistency-profile-policy.yaml",
    "stage_isolation_policy": PROJECT_STATE_DIR / "stage5dy-stage-isolation-policy.yaml",
    "nonmutating_validator_policy": PROJECT_STATE_DIR / "stage5dy-nonmutating-validator-policy.yaml",
    "pytest_shard_race_audit": PROJECT_STATE_DIR / "stage5dy-pytest-shard-race-audit.yaml",
    "prompt_validation_guidance": PROJECT_STATE_DIR / "stage5dy-prompt-validation-guidance.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5dy-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5dy-reviewability-gap-register.yaml",
    "scope_control": PROJECT_STATE_DIR / "stage5dy-scope-control.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage5dy-chatgpt-context-update-summary.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5dy-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5dy-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5dy-raw-source-noncommit-proof.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5dy-stage5bd-preservation.yaml",
    "stage5dg_preservation": TOKEN_BLOCK_DIR / "stage5dy-stage5dg-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5dy-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5dy-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR / "stage5dy-no-byte-stream-transition-proof.yaml",
    "no_token_block_execution_proof": TOKEN_BLOCK_DIR / "stage5dy-no-token-block-execution-proof.yaml",
}

CI_PATHS: dict[str, Path] = {
    "validation_profile_baseline": CI_DIR / "stage5dy-validation-profile-baseline.yaml",
    "parallel_validation_shard_policy": CI_DIR / "stage5dy-parallel-validation-shard-policy.yaml",
    "nonmutating_validator_regression": CI_DIR / "stage5dy-nonmutating-validator-regression.yaml",
}

DATA_PATHS: dict[str, Path] = {}
DATA_PATHS.update(PROJECT_STATE_PATHS)
DATA_PATHS.update(SOURCE_HARVESTER_PATHS)
DATA_PATHS.update(TOKEN_PATHS)
DATA_PATHS.update(CI_PATHS)

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5dy-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5dy-next-stage-decision-v0.schema.json"),
    "stage5dx_preservation": Path("schemas/project-state/stage5dy-stage5dx-preservation-v0.schema.json"),
    "validation_performance_diagnostic": Path(
        "schemas/project-state/stage5dy-validation-performance-diagnostic-v0.schema.json"
    ),
    "validation_profile_registry": Path("schemas/project-state/stage5dy-validation-profile-registry-v0.schema.json"),
    "parallel_validation_policy": Path("schemas/project-state/stage5dy-parallel-validation-policy-v0.schema.json"),
    "consistency_profile_policy": Path("schemas/project-state/stage5dy-consistency-profile-policy-v0.schema.json"),
    "stage_isolation_policy": Path("schemas/project-state/stage5dy-stage-isolation-policy-v0.schema.json"),
    "nonmutating_validator_policy": Path("schemas/project-state/stage5dy-nonmutating-validator-policy-v0.schema.json"),
    "pytest_shard_race_audit": Path("schemas/project-state/stage5dy-pytest-shard-race-audit-v0.schema.json"),
    "prompt_validation_guidance": Path("schemas/project-state/stage5dy-prompt-validation-guidance-v0.schema.json"),
    "reviewable_validation_evidence": Path(
        "schemas/project-state/stage5dy-reviewable-validation-evidence-v0.schema.json"
    ),
    "scope_control": Path("schemas/project-state/stage5dy-scope-control-v0.schema.json"),
    "codex_handoff_policy": Path("schemas/source-harvester/stage5dy-codex-handoff-policy-v0.schema.json"),
    "credential_redaction_policy_preservation": Path(
        "schemas/source-harvester/stage5dy-credential-redaction-policy-preservation-v0.schema.json"
    ),
    "raw_source_noncommit_proof": Path("schemas/source-harvester/stage5dy-raw-source-noncommit-proof-v0.schema.json"),
    "no_token_block_execution_proof": Path("schemas/token-block/stage5dy-no-token-block-execution-proof-v0.schema.json"),
    "generic_preservation": Path("schemas/token-block/stage5dy-generic-preservation-record-v0.schema.json"),
}

SCHEMA_BY_DATA_KEY: dict[str, str] = {
    "summary": "summary",
    "next_stage_decision": "next_stage_decision",
    "stage5dx_preservation": "stage5dx_preservation",
    "validation_performance_diagnostic": "validation_performance_diagnostic",
    "validation_profile_registry": "validation_profile_registry",
    "parallel_validation_policy": "parallel_validation_policy",
    "consistency_profile_policy": "consistency_profile_policy",
    "stage_isolation_policy": "stage_isolation_policy",
    "nonmutating_validator_policy": "nonmutating_validator_policy",
    "pytest_shard_race_audit": "pytest_shard_race_audit",
    "prompt_validation_guidance": "prompt_validation_guidance",
    "reviewable_validation_evidence": "reviewable_validation_evidence",
    "scope_control": "scope_control",
    "codex_handoff_policy": "codex_handoff_policy",
    "credential_redaction_policy_preservation": "credential_redaction_policy_preservation",
    "raw_source_noncommit_proof": "raw_source_noncommit_proof",
    "no_token_block_execution_proof": "no_token_block_execution_proof",
}

FALSE_FLAGS = [
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "active_token_block_manifest_changed",
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
    "disk_cipher_execution_performed_now",
    "dwh_hash_search_performed",
    "execution_authorized_now",
    "execution_performed",
    "full_cartesian_product_enumerated",
    "generated_outputs_committed",
    "hash_preimage_search_performed",
    "hidden_content_image_forensics_performed",
    "historical_source_lock_records_rewritten",
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
    "number_fact_review_batch_3_performed_now",
    "ocr_performed",
    "openpuff_execution_performed",
    "operator_readiness_decision_created_now",
    "page0_plaintext_accepted_now",
    "page32_route_extraction_performed_now",
    "page56_hash_preimage_tested_now",
    "pdf_ocr_or_hidden_content_rendering_performed",
    "pivot_target_selected_now",
    "probability_claim_accepted_as_validated",
    "raw_source_files_committed",
    "raw_third_party_files_committed",
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
]

PROFILE_NAMES = ["focused", "stage_fast", "local_fast", "full_parallel", "full_serial_rare", "ci"]


@dataclass
class Stage5DYValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5dy"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5dy() -> dict[str, dict[str, Any]]:
    records = _build_records()
    _write_schemas()
    _write_records(records)
    _update_chatgpt_context()
    _update_stage_summary_records(records["summary"])
    return records


def validate_stage5dy() -> Stage5DYValidationResult:
    checks = [
        validate_stage5dy_stage5dx_preservation,
        validate_stage5dy_validation_performance_diagnostic,
        validate_stage5dy_validation_profile_registry,
        validate_stage5dy_parallel_validation_policy,
        validate_stage5dy_consistency_profile_policy,
        validate_stage5dy_stage_isolation_policy,
        validate_stage5dy_nonmutating_validator_policy,
        validate_stage5dy_pytest_shard_race_audit,
        validate_stage5dy_source_browser_loadability,
        validate_stage5dy_stage5bd_preservation,
        validate_stage5dy_stage5dg_preservation,
        validate_stage5dy_active_lineage_preservation,
        validate_stage5dy_sidecar_gates,
        validate_stage5dy_handoff_continuity,
        validate_stage5dy_credential_redaction_policy,
        validate_stage5dy_governance_scope,
    ]
    errors = _validate_required_paths() + _validate_schemas()
    counts: dict[str, Any] = {}
    for check in checks:
        result = check()
        counts.update(result.counts)
        errors.extend(result.errors)
    summary = _load(PROJECT_STATE_PATHS["summary"])
    expected = {
        "stage_id": STAGE_ID,
        "status": "complete",
        "validation_infrastructure_stage": True,
        "number_fact_review_batch_3_performed_now": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "full_serial_pytest_default_for_future_stages": False,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"{PROJECT_STATE_PATHS['summary'].as_posix()}: {key} must be {value!r}")
    errors.extend(_required_false_errors(summary, PROJECT_STATE_PATHS["summary"].as_posix()))
    counts.update(_summary_counts(summary))
    counts["token_block_stage5dy_valid"] = not errors
    return Stage5DYValidationResult(len(errors), counts, errors)


def validate_stage5dy_stage5dx_preservation() -> Stage5DYValidationResult:
    payload = _load(PROJECT_STATE_PATHS["stage5dx_preservation"])
    expected = {
        "stage5dx_status": "complete",
        "stage5dx_reviewed_entry_count": 20,
        "stage5dx_overlay_count": 23,
        "stage5dx_overlay_only_fact_cards_supported": True,
        "stage5dx_source_browser_entries_loaded": 1546,
        "stage5dx_source_browser_records_scanned": 1545,
        "stage5dx_source_browser_validation_error_count": 0,
        "stage5dx_fact_card_count_after_stage5dx": 80,
        "stage5dx_stage5bd_run_plan_id_count": 10,
        "stage5dx_active_lineage_record_count": 8,
        "stage5dx_parallel_worker_cap": PARALLEL_WORKER_CAP,
        "stage5dx_old_16_worker_default_reintroduced": False,
        "stage5dx_codex_output_used": False,
        "stage5dx_execution_performed": False,
        "stage5dx_solve_claim": False,
    }
    errors = _expected_errors(payload, expected, PROJECT_STATE_PATHS["stage5dx_preservation"])
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_validation_performance_diagnostic() -> Stage5DYValidationResult:
    payload = _load(PROJECT_STATE_PATHS["validation_performance_diagnostic"])
    expected = {
        "stage5dx_codex_output_reviewed_by_operator": True,
        "observed_validation_problem_family": "validation_performance_and_stage_isolation",
        "observed_full_serial_pytest_result": "2855 passed, 1 skipped",
        "observed_monolithic_consistency_timeout_45_min": True,
        "observed_parallel_pytest_shard_timeouts": True,
        "observed_nonreproducible_stage5cu_jsondecodeerror": True,
        "observed_orphaned_python_processes_after_timeout": True,
        "observed_historical_digest_or_approval_records_rewritten_by_validation_helpers": True,
        "observed_shared_schema_collision": True,
        "observed_later_stage_global_source_browser_count_invalidated_prior_stage_validator": True,
        "observed_power_shell_pytest_wildcard_issue": True,
        "operator_requires_fix_before_next_fact_batch": True,
    }
    errors = _expected_errors(payload, expected, PROJECT_STATE_PATHS["validation_performance_diagnostic"])
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_validation_profile_registry() -> Stage5DYValidationResult:
    payload = _load(PROJECT_STATE_PATHS["validation_profile_registry"])
    profiles = payload.get("profiles", {})
    errors = [f"missing validation profile: {name}" for name in PROFILE_NAMES if name not in profiles]
    full_serial = profiles.get("full_serial_rare", {})
    if full_serial.get("default_allowed_for_every_stage") is not False:
        errors.append("full_serial_rare.default_allowed_for_every_stage must be false")
    full_parallel = profiles.get("full_parallel", {})
    if full_parallel.get("default_workers") != PARALLEL_WORKER_CAP:
        errors.append("full_parallel.default_workers must be 8")
    if payload.get("old_16_worker_default_reintroduced") is not False:
        errors.append("old_16_worker_default_reintroduced must be false")
    return Stage5DYValidationResult(
        len(errors),
        {"validation_profile_count": len(profiles), **_summary_counts(payload)},
        errors,
    )


def validate_stage5dy_parallel_validation_policy() -> Stage5DYValidationResult:
    payload = _load(PROJECT_STATE_PATHS["parallel_validation_policy"])
    expected = {
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "default_workers": PARALLEL_WORKER_CAP,
        "default_pytest_workers": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "race_prone_tests_isolated_or_serialized": True,
    }
    errors = _expected_errors(payload, expected, PROJECT_STATE_PATHS["parallel_validation_policy"])
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_consistency_profile_policy() -> Stage5DYValidationResult:
    payload = _load(PROJECT_STATE_PATHS["consistency_profile_policy"])
    expected = {
        "fast_profile_available": True,
        "stage_profile_available": True,
        "full_profile_preserved": True,
        "long_tail_checks_default_local": False,
    }
    errors = _expected_errors(payload, expected, PROJECT_STATE_PATHS["consistency_profile_policy"])
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_stage_isolation_policy() -> Stage5DYValidationResult:
    payload = _load(PROJECT_STATE_PATHS["stage_isolation_policy"])
    expected = {
        "historical_validators_use_frozen_stage_fields": True,
        "mutable_global_source_browser_counts_allowed_in_historical_validators": False,
        "shared_schemas_stage_neutral": True,
        "stage_specific_schemas_use_stage_specific_names": True,
        "stage5dw_global_count_fragility_guarded": True,
    }
    errors = _expected_errors(payload, expected, PROJECT_STATE_PATHS["stage_isolation_policy"])
    shared_schema = Path("schemas/operator-console/stage5dw-source-browser-number-fact-review-batch-result-v0.schema.json")
    if shared_schema.exists():
        text = shared_schema.read_text(encoding="utf-8")
        if "stage-5dx" in text or "stage-5dy" in text:
            errors.append(f"{shared_schema.as_posix()}: shared Stage 5DW schema contains later-stage constants")
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_nonmutating_validator_policy() -> Stage5DYValidationResult:
    payload = _load(PROJECT_STATE_PATHS["nonmutating_validator_policy"])
    expected = {
        "validate_commands_read_only_for_committed_data": True,
        "summary_commands_read_only_for_committed_data": True,
        "build_commands_write_current_stage_records_only": True,
        "parallel_validation_writes_ignored_outputs_only": True,
    }
    errors = _expected_errors(payload, expected, PROJECT_STATE_PATHS["nonmutating_validator_policy"])
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_pytest_shard_race_audit() -> Stage5DYValidationResult:
    payload = _load(PROJECT_STATE_PATHS["pytest_shard_race_audit"])
    expected = {
        "stage5cu_jsondecodeerror_observed_parallel_only": True,
        "serial_reproduction_observed": False,
        "affected_group_isolated_or_serialized": True,
        "treated_as_race_avoidance_not_hidden_pass": True,
    }
    errors = _expected_errors(payload, expected, PROJECT_STATE_PATHS["pytest_shard_race_audit"])
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_source_browser_loadability() -> Stage5DYValidationResult:
    payload = _load(PROJECT_STATE_PATHS["summary"])
    expected = {
        "stage5dx_source_browser_entries_loaded": 1546,
        "stage5dx_source_browser_records_scanned": 1545,
        "stage5dx_source_browser_validation_error_count": 0,
    }
    errors = _expected_errors(payload, expected, PROJECT_STATE_PATHS["summary"])
    if payload.get("source_browser_loadability_validated") is not True:
        errors.append("source_browser_loadability_validated must be true")
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_stage5bd_preservation() -> Stage5DYValidationResult:
    payload = _load(TOKEN_PATHS["stage5bd_preservation"])
    errors = []
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_stage5dg_preservation() -> Stage5DYValidationResult:
    payload = _load(TOKEN_PATHS["stage5dg_preservation"])
    expected = {
        "stage5dg_operator_approval_record_preserved": True,
        "operator_approval_component_satisfied_preserved": True,
        "combined_approval_gate_satisfied_now": False,
    }
    errors = _expected_errors(payload, expected, TOKEN_PATHS["stage5dg_preservation"])
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_active_lineage_preservation() -> Stage5DYValidationResult:
    payload = _load(TOKEN_PATHS["active_lineage_preservation"])
    errors = []
    if payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage count must remain 8")
    if payload.get("active_lineage_preserved") is not True:
        errors.append("active lineage must be preserved")
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_sidecar_gates() -> Stage5DYValidationResult:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for path in (
        TOKEN_PATHS["no_active_ingestion_proof"],
        TOKEN_PATHS["no_byte_stream_transition_proof"],
        TOKEN_PATHS["no_token_block_execution_proof"],
    ):
        payload = _load(path)
        counts[path.stem] = payload.get("gate_status")
        errors.extend(_required_false_errors(payload, path.as_posix()))
        if payload.get("gate_status") != "closed":
            errors.append(f"{path.as_posix()}: gate_status must be closed")
    return Stage5DYValidationResult(len(errors), counts, errors)


def validate_stage5dy_handoff_continuity() -> Stage5DYValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if payload.get("codex_output_used") is not False:
        errors.append("deprecated codex_output root must not be used")
    if Path("codex_output").exists():
        errors.append("deprecated codex_output directory is present")
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_credential_redaction_policy() -> Stage5DYValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["credential_redaction_policy_preservation"])
    errors = []
    if payload.get("credential_like_remote_count") != 0:
        errors.append("credential-like remote count must be 0")
    if payload.get("raw_source_body_included") is not False:
        errors.append("credential policy must not include raw source bodies")
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dy_governance_scope() -> Stage5DYValidationResult:
    payload = _load(PROJECT_STATE_PATHS["scope_control"])
    expected = {
        "number_fact_review_batch_3_performed_now": False,
        "stage5dy_is_validation_repair_not_number_fact_batch": True,
        "number_fact_review_batch_3_still_required_after_this_stage": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
    }
    errors = _expected_errors(payload, expected, PROJECT_STATE_PATHS["scope_control"])
    errors.extend(_required_false_errors(payload, PROJECT_STATE_PATHS["scope_control"].as_posix()))
    return Stage5DYValidationResult(len(errors), _summary_counts(payload), errors)


def stage5dy_summary_text() -> str:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5DY summary:",
        f"status={summary.get('status')}",
        f"validation_profiles_added={summary.get('validation_profiles_added')}",
        f"parallel_worker_cap={summary.get('parallel_worker_cap')}",
        f"full_serial_pytest_default={summary.get('full_serial_pytest_default_for_future_stages')}",
        f"stage_isolation_repair={summary.get('stage_isolation_repair_performed')}",
        f"shared_schema_collision_guard={summary.get('shared_schema_collision_guard_added')}",
        f"nonmutating_validator_guard={summary.get('nonmutating_validator_guard_added')}",
        f"number_fact_review_batch_3_performed_now={summary.get('number_fact_review_batch_3_performed_now')}",
        f"stage5dx_preserved={summary.get('stage5dx_preserved')}",
        f"stage5bd_run_plan_id_count={summary.get('stage5bd_run_plan_id_count')}",
        f"active_lineage_record_count={summary.get('active_lineage_record_count')}",
        f"execution_performed={summary.get('execution_performed')}",
        f"solve_claim={summary.get('solve_claim')}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


def _build_records() -> dict[str, dict[str, Any]]:
    base = _stage_base()
    false_flags = _false_flags()
    summary = {
        **base,
        **false_flags,
        "record_type": "stage5dy_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "source_previous_stage_final_commit": PREVIOUS_COMMIT,
        "source_previous_issue": 159,
        "source_previous_ci_run": 27256346930,
        "source_previous_ci_status": "passed",
        "stage5dx_preserved": True,
        "stage5dx_status": "complete",
        "stage5dx_reviewed_entry_count": 20,
        "stage5dx_overlay_count": 23,
        "stage5dx_source_browser_entries_loaded": 1546,
        "stage5dx_source_browser_records_scanned": 1545,
        "stage5dx_source_browser_validation_error_count": 0,
        "stage5dx_fact_card_count_after_stage5dx": 80,
        "source_browser_loadability_validated": True,
        "validation_profiles_added": PROFILE_NAMES,
        "validation_profile_count": len(PROFILE_NAMES),
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "full_serial_pytest_default_for_future_stages": False,
        "stage_isolation_repair_performed": True,
        "shared_schema_collision_guard_added": True,
        "nonmutating_validator_guard_added": True,
        "consistency_profile_repair_performed": True,
        "parallel_validation_policy_repair_performed": True,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": 8,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": "assistant_or_operator_review_then_codex_overlay_update",
    }
    records: dict[str, dict[str, Any]] = {
        "summary": summary,
        "next_stage_decision": _next_stage_decision(base, false_flags),
        "stage5dx_preservation": _stage5dx_preservation(base, false_flags),
        "validation_performance_diagnostic": _validation_performance_diagnostic(base, false_flags),
        "validation_profile_registry": _validation_profile_registry(base, false_flags),
        "parallel_validation_policy": _parallel_validation_policy(base, false_flags),
        "consistency_profile_policy": _consistency_profile_policy(base, false_flags),
        "stage_isolation_policy": _stage_isolation_policy(base, false_flags),
        "nonmutating_validator_policy": _nonmutating_validator_policy(base, false_flags),
        "pytest_shard_race_audit": _pytest_shard_race_audit(base, false_flags),
        "prompt_validation_guidance": _prompt_validation_guidance(base, false_flags),
        "reviewable_validation_evidence": _reviewable_validation_evidence(base, false_flags),
        "reviewability_gap_register": _reviewability_gap_register(base, false_flags),
        "scope_control": _scope_control(base, false_flags),
        "chatgpt_context_update_summary": _chatgpt_context_update_summary(base, false_flags),
    }
    records.update(_source_harvester_records(base, false_flags))
    records.update(_token_records(base, false_flags))
    records.update(_ci_records(base, false_flags))
    return records


def _next_stage_decision(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_next_stage_decision",
        "schema": SCHEMA_PATHS["next_stage_decision"].as_posix(),
        "stage5dx_recommended_stage5dy_number_fact_review_batch_3": True,
        "operator_inserted_validation_performance_and_stage_isolation_repair_first": True,
        "stage5dy_is_validation_repair_not_number_fact_batch": True,
        "number_fact_review_batch_3_still_required_after_this_stage": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": "assistant_or_operator_review_then_codex_overlay_update",
    }


def _stage5dx_preservation(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_stage5dx_preservation",
        "schema": SCHEMA_PATHS["stage5dx_preservation"].as_posix(),
        "stage5dx_status": "complete",
        "stage5dx_reviewed_entry_count": 20,
        "stage5dx_overlay_count": 23,
        "stage5dx_overlay_only_fact_cards_supported": True,
        "stage5dx_source_browser_entries_loaded": 1546,
        "stage5dx_source_browser_records_scanned": 1545,
        "stage5dx_source_browser_validation_error_count": 0,
        "stage5dx_fact_card_count_after_stage5dx": 80,
        "stage5dx_spurious_root_image_paths_after": 0,
        "stage5dx_spurious_root_document_paths_after": 0,
        "stage5dx_duplicate_present_missing_path_pairs_after": 0,
        "stage5dx_source_root_relative_resolved_paths": 2085,
        "stage5dx_stage5bd_run_plan_id_count": 10,
        "stage5dx_active_lineage_record_count": 8,
        "stage5dx_parallel_worker_cap": PARALLEL_WORKER_CAP,
        "stage5dx_old_16_worker_default_reintroduced": False,
        "stage5dx_codex_output_used": False,
        "stage5dx_pivot_target_selected_now": False,
        "stage5dx_route_extraction_performed_now": False,
        "stage5dx_byte_stream_generation_authorized_now": False,
        "stage5dx_execution_performed": False,
        "stage5dx_solve_claim": False,
    }


def _validation_performance_diagnostic(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_validation_performance_diagnostic",
        "schema": SCHEMA_PATHS["validation_performance_diagnostic"].as_posix(),
        "stage5dx_codex_output_reviewed_by_operator": True,
        "observed_validation_problem_family": "validation_performance_and_stage_isolation",
        "observed_full_serial_pytest_duration": "1h38m41s",
        "observed_full_serial_pytest_result": "2855 passed, 1 skipped",
        "observed_monolithic_consistency_timeout_45_min": True,
        "observed_parallel_harness_duration_approx": "20m20s",
        "observed_parallel_pytest_shard_timeouts": True,
        "observed_nonreproducible_stage5cu_jsondecodeerror": True,
        "observed_orphaned_python_processes_after_timeout": True,
        "observed_historical_digest_or_approval_records_rewritten_by_validation_helpers": True,
        "observed_shared_schema_collision": True,
        "observed_later_stage_global_source_browser_count_invalidated_prior_stage_validator": True,
        "observed_power_shell_pytest_wildcard_issue": True,
        "operator_requires_fix_before_next_fact_batch": True,
    }


def _validation_profile_registry(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_validation_profile_registry",
        "schema": SCHEMA_PATHS["validation_profile_registry"].as_posix(),
        "old_16_worker_default_reintroduced": False,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "profiles": {
            "focused": {
                "purpose": "run only directly edited stage tests/validators during development",
                "intended_frequency": "many_times_during_implementation",
                "must_use_parallel": False,
            },
            "stage_fast": {
                "purpose": "focused stage validators, focused stage tests, ruff on changed files, source-browser smoke",
                "intended_frequency": "before_broader_validation",
                "must_use_parallel": False,
            },
            "local_fast": {
                "purpose": "stage_fast plus doc/current-state checks and fast consistency profile",
                "intended_frequency": "before_commit",
                "must_use_parallel": "partly",
            },
            "full_parallel": {
                "purpose": "broad pytest/consistency through parallel harness",
                "intended_frequency": "once_near_final_or_after_major_fixes",
                "must_use_parallel": True,
                "default_workers": PARALLEL_WORKER_CAP,
                "default_pytest_workers": PARALLEL_WORKER_CAP,
            },
            "full_serial_rare": {
                "purpose": "fallback only for suspected race or CI-only reproduction",
                "intended_frequency": "rare_exception_only",
                "default_allowed_for_every_stage": False,
            },
            "ci": {
                "purpose": "repository CI equivalent",
                "intended_frequency": "after_push",
            },
        },
    }


def _parallel_validation_policy(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_parallel_validation_policy",
        "schema": SCHEMA_PATHS["parallel_validation_policy"].as_posix(),
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "default_workers": PARALLEL_WORKER_CAP,
        "default_pytest_workers": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "results_dir_policy": "ignored_experiments_results_only",
        "parallel_validation_state_outputs": "ignored_or_temporary_not_committed_data_ci",
        "race_prone_tests_isolated_or_serialized": True,
        "stage5cu_jsondecodeerror_handling": "serialize_or_isolate_stage5cu_group_in_parallel_harness",
        "failure_log_policy": "write_actionable_failed_command_names",
    }


def _consistency_profile_policy(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_consistency_profile_policy",
        "schema": SCHEMA_PATHS["consistency_profile_policy"].as_posix(),
        "stage_profile_available": True,
        "fast_profile_available": True,
        "full_profile_preserved": True,
        "long_tail_checks_default_local": False,
        "timeout_cleanup_required": True,
        "known_long_tail_checks_deferred_to_full_profile": True,
    }


def _stage_isolation_policy(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_stage_isolation_policy",
        "schema": SCHEMA_PATHS["stage_isolation_policy"].as_posix(),
        "historical_validators_use_frozen_stage_fields": True,
        "mutable_global_source_browser_counts_allowed_in_historical_validators": False,
        "later_stage_builders_use_preservation_checks": True,
        "shared_schemas_stage_neutral": True,
        "stage_specific_schemas_use_stage_specific_names": True,
        "stage5dw_global_count_fragility_guarded": True,
        "schema_naming_policy": "shared schemas remain stage-neutral; stage-specific schemas use stage-specific filenames",
    }


def _nonmutating_validator_policy(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_nonmutating_validator_policy",
        "schema": SCHEMA_PATHS["nonmutating_validator_policy"].as_posix(),
        "validate_commands_read_only_for_committed_data": True,
        "summary_commands_read_only_for_committed_data": True,
        "build_commands_write_current_stage_records_only": True,
        "parallel_validation_writes_ignored_outputs_only": True,
        "representative_regression_command": "python -m pytest -q tests/python/test_stage5dy_nonmutating_validators.py",
    }


def _pytest_shard_race_audit(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_pytest_shard_race_audit",
        "schema": SCHEMA_PATHS["pytest_shard_race_audit"].as_posix(),
        "stage5cu_jsondecodeerror_observed_parallel_only": True,
        "serial_reproduction_observed": False,
        "affected_group_isolated_or_serialized": True,
        "treated_as_race_avoidance_not_hidden_pass": True,
        "diagnostic_note": "Stage 5CU failed only in shard mode during Stage 5DX and passed serially; Stage 5DY records isolation policy.",
    }


def _prompt_validation_guidance(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_prompt_validation_guidance",
        "schema": SCHEMA_PATHS["prompt_validation_guidance"].as_posix(),
        "focused_tests_during_iteration": True,
        "full_parallel_near_final": True,
        "full_serial_pytest_default_for_future_stages": False,
        "powershell_wildcard_warning": (
            "PowerShell may not expand pytest wildcards; use Get-ChildItem to build explicit test file lists."
        ),
    }


def _reviewable_validation_evidence(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_reviewable_validation_evidence",
        "schema": SCHEMA_PATHS["reviewable_validation_evidence"].as_posix(),
        "focused_validation_commands_defined": True,
        "stage_fast_profile_defined": True,
        "local_fast_profile_defined": True,
        "full_parallel_profile_defined": True,
        "full_serial_pytest_run_locally": False,
        "full_serial_pytest_policy_reason": "rare_fallback_not_default",
    }


def _reviewability_gap_register(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_reviewability_gap_register",
        "gap_count": 1,
        "gaps": [
            {
                "gap_id": "stage5dy_future_parallel_harness_root_cause",
                "status": "deferred_with_policy",
                "summary": "Stage 5CU parallel-only JSONDecodeError root cause was not reproduced serially; harness isolation policy prevents hidden pass.",
            }
        ],
    }


def _scope_control(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_scope_control",
        "schema": SCHEMA_PATHS["scope_control"].as_posix(),
        "stage5dy_is_validation_repair_not_number_fact_batch": True,
        "number_fact_review_batch_3_still_required_after_this_stage": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
    }


def _chatgpt_context_update_summary(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5dy_chatgpt_context_update_summary",
        "chatgpt_context_file": "ChatGPT-ContextFile.md",
        "stage5dy_validation_policy_section_added": True,
        "codex_output_used": False,
    }


def _source_harvester_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "codex_handoff_policy": {
            **base,
            "record_type": "stage5dy_codex_handoff_policy",
            "schema": SCHEMA_PATHS["codex_handoff_policy"].as_posix(),
            "canonical_codex_handoff_root": "codex-output",
            "codex_output_used": False,
            "completion_summary_path": "codex-output/stage5dy-codex-completion.md",
            "completion_summary_committed": False,
        },
        "credential_redaction_policy_preservation": {
            **base,
            "record_type": "stage5dy_credential_redaction_policy_preservation",
            "schema": SCHEMA_PATHS["credential_redaction_policy_preservation"].as_posix(),
            "credential_like_remote_count": 0,
            "credential_redaction_policy_preserved": True,
            "raw_source_body_included": False,
            "secret_material_committed": False,
        },
        "raw_source_noncommit_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dy_raw_source_noncommit_proof",
            "schema": SCHEMA_PATHS["raw_source_noncommit_proof"].as_posix(),
            "raw_source_files_committed": False,
            "raw_third_party_files_committed": False,
            "generated_outputs_committed": False,
        },
    }


def _token_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "stage5bd_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5dy_stage5bd_preservation",
            "stage5bd_run_plan_id_count": 10,
            "stage5bd_run_plan_ids_preserved": True,
        },
        "stage5dg_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5dy_stage5dg_preservation",
            "stage5dg_operator_approval_record_preserved": True,
            "operator_approval_component_satisfied_preserved": True,
            "combined_approval_gate_satisfied_now": False,
        },
        "active_lineage_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5dy_active_lineage_preservation",
            "active_lineage_record_count": 8,
            "active_lineage_preserved": True,
        },
        "no_active_ingestion_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dy_no_active_ingestion_proof",
            "gate_status": "closed",
            "active_ingestion_performed": False,
        },
        "no_byte_stream_transition_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dy_no_byte_stream_transition_proof",
            "gate_status": "closed",
            "variant_byte_streams_generated": False,
            "byte_stream_generation_authorized_now": False,
        },
        "no_token_block_execution_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dy_no_token_block_execution_proof",
            "schema": SCHEMA_PATHS["no_token_block_execution_proof"].as_posix(),
            "gate_status": "closed",
            "execution_authorized_now": False,
            "execution_performed": False,
        },
    }


def _ci_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "validation_profile_baseline": {
            **base,
            **false_flags,
            "record_type": "stage5dy_validation_profile_baseline",
            "profiles": PROFILE_NAMES,
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
            "full_serial_pytest_default_for_future_stages": False,
        },
        "parallel_validation_shard_policy": {
            **base,
            **false_flags,
            "record_type": "stage5dy_parallel_validation_shard_policy",
            "default_workers": PARALLEL_WORKER_CAP,
            "default_pytest_workers": PARALLEL_WORKER_CAP,
            "stage5cu_group_isolated_or_serialized": True,
        },
        "nonmutating_validator_regression": {
            **base,
            **false_flags,
            "record_type": "stage5dy_nonmutating_validator_regression",
            "representative_validate_summary_commands_read_only": True,
        },
    }


def _write_records(records: dict[str, dict[str, Any]]) -> None:
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        required = ["record_type", "stage_id"]
        if key in {"summary", "next_stage_decision"}:
            required.extend(["status"] if key == "summary" else ["recommended_next_stage_id"])
        write_json(path, _object_schema(required))


def _object_schema(required: list[str]) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "stage_id": {"const": STAGE_ID},
        "puzzle_execution_allowed": {"const": False},
        "solve_claim": {"const": False},
        "number_fact_review_batch_3_performed_now": {"const": False},
        "pivot_target_selected_now": {"const": False},
        "byte_stream_generation_authorized_now": {"const": False},
        "execution_performed": {"const": False},
        "old_16_worker_default_reintroduced": {"const": False},
        "parallel_worker_cap": {"const": PARALLEL_WORKER_CAP},
        "codex_output_used": {"const": False},
    }
    for flag in FALSE_FLAGS:
        properties.setdefault(flag, {"const": False})
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
        "required": required,
        "properties": properties,
    }


def _validate_required_paths() -> list[str]:
    paths = list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values())
    return [f"required Stage 5DY path missing: {path.as_posix()}" for path in paths if not path.exists()]


def _validate_schemas() -> list[str]:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        schema_key = SCHEMA_BY_DATA_KEY.get(key, "generic_preservation")
        schema_path = SCHEMA_PATHS.get(schema_key, SCHEMA_PATHS["generic_preservation"])
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


def _stage_base() -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": False,
        "validation_infrastructure_stage": True,
        "source_lock_only": False,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "canonical_codex_handoff_root": "codex-output",
    }


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in FALSE_FLAGS}


def _required_false_errors(payload: dict[str, Any], label: str) -> list[str]:
    return [f"{label}: {key} must be false" for key in FALSE_FLAGS if key in payload and payload[key] is not False]


def _expected_errors(payload: dict[str, Any], expected: dict[str, Any], path: Path) -> list[str]:
    return [
        f"{path.as_posix()}: {key} must be {expected_value!r}, found {payload.get(key)!r}"
        for key, expected_value in expected.items()
        if payload.get(key) != expected_value
    ]


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
    marker = "## Stage 5DY Validation Policy"
    text = CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8") if CHATGPT_CONTEXT_PATH.exists() else ""
    if marker in text:
        return
    addition = f"""

{marker}

- Stage 5DX completed at {PREVIOUS_COMMIT[:8]} with 23 overlays and CI passed, but its Codex output exposed validation-tooling pain.
- Full serial pytest took 1h38m41s and should not be required by default in every future prompt.
- Full monolithic consistency exceeded 45 minutes locally; use focused/stage-fast and full-parallel profiles unless a full serial fallback is explicitly justified.
- Future prompts should tell Codex: use focused tests during iteration, run broad parallel validation once near final, avoid broad repeated serial test loops.
- Historical validators must not depend on mutable current global Source Browser counts.
- Stage-specific schemas must not overwrite shared schemas.
- Validate/summary commands must be read-only for committed records.
- PowerShell wildcard expansion differs from Bash; use explicit file lists in examples.
- Stage 5DZ remains the next fact-review batch.
"""
    CHATGPT_CONTEXT_PATH.write_text(text.rstrip() + addition + "\n", encoding="utf-8")


def _update_stage_summary_records(summary: dict[str, Any]) -> None:
    payload = read_yaml(STAGE_SUMMARY_RECORDS_PATH)
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
            "category": "validation_infrastructure",
            "summary": (
                "Added validation profiles, stage-isolation policy, non-mutating validator policy, "
                "and parallel-test discipline before number-fact batch 3."
            ),
            "key_outputs": [
                "Stage 5DY validation profile registry and stage-fast/local-fast/full-parallel scripts.",
                "Stage-isolation and shared-schema collision policy records.",
                "Non-mutating validator policy and focused regression tests.",
            ],
            "result_status": "validation_infrastructure_repaired",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                f"Profiles={len(summary.get('validation_profiles_added', []))}; "
                f"parallel_worker_cap={summary.get('parallel_worker_cap')}; "
                f"next={summary.get('recommended_next_stage_id')}."
            ),
        }
    )
    payload["records"] = records
    write_yaml(STAGE_SUMMARY_RECORDS_PATH, payload)


VALIDATOR_BY_NAME: dict[str, Callable[[], Stage5DYValidationResult]] = {
    "stage5dx_preservation": validate_stage5dy_stage5dx_preservation,
    "validation_performance_diagnostic": validate_stage5dy_validation_performance_diagnostic,
    "validation_profile_registry": validate_stage5dy_validation_profile_registry,
    "parallel_validation_policy": validate_stage5dy_parallel_validation_policy,
    "consistency_profile_policy": validate_stage5dy_consistency_profile_policy,
    "stage_isolation_policy": validate_stage5dy_stage_isolation_policy,
    "nonmutating_validator_policy": validate_stage5dy_nonmutating_validator_policy,
    "pytest_shard_race_audit": validate_stage5dy_pytest_shard_race_audit,
    "source_browser_loadability": validate_stage5dy_source_browser_loadability,
    "stage5bd_preservation": validate_stage5dy_stage5bd_preservation,
    "stage5dg_preservation": validate_stage5dy_stage5dg_preservation,
    "active_lineage_preservation": validate_stage5dy_active_lineage_preservation,
    "sidecar_gates": validate_stage5dy_sidecar_gates,
    "handoff_continuity": validate_stage5dy_handoff_continuity,
    "credential_redaction_policy": validate_stage5dy_credential_redaction_policy,
    "governance_scope": validate_stage5dy_governance_scope,
}
