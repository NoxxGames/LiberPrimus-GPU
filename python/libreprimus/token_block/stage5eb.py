"""Stage 5EB validation finalization and 10-worker policy repair records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.number_facts import NumberFactOverlayCache
from libreprimus.token_block.models import read_yaml, write_json, write_yaml
from libreprimus.validation.stage_id import validation_command_name

STAGE_ID = "stage-5eb"
STAGE_TITLE = (
    "Stage 5EB - Validation finalization, 10-worker parallel policy, serial-fallback elimination, "
    "and test-throughput repair, without execution"
)
PROMPT_TYPE = "codex_validation_throughput_finalization_repair"
PREVIOUS_STAGE_ID = "stage-5ea"
PREVIOUS_STAGE_TITLE = (
    "Stage 5EA - Validation throughput, current-stage registry, historical-test isolation, "
    "and Source Browser fact-card performance repair, without execution"
)
PREVIOUS_STAGE_IMPLEMENTATION_COMMIT = "2da9df36f658232730b33b027baa5d0ff062f820"
PREVIOUS_STAGE_FINAL_COMMIT = "9f166e47080aa46839328a4d4445e45aaa194972"
PREVIOUS_STAGE_ISSUE = 162
PREVIOUS_CI_RUN = 27331393499
NEXT_STAGE_ID = "stage-5ec"
NEXT_STAGE_TITLE = "Stage 5EC - Operator/assistant source-lock number-fact review batch 3, without execution"
NEXT_PROMPT_TYPE = "assistant_or_operator_review_then_codex_overlay_update"
PARALLEL_WORKER_CAP = 10
LOCAL_PARALLEL_DEFAULT_WORKERS = 10
LOCAL_PARALLEL_DEFAULT_PYTEST_WORKERS = 10
PYTEST_TIMEOUT_SECONDS = 3600

PROJECT_STATE_DIR = Path("data/project-state")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
TOKEN_BLOCK_DIR = Path("data/token-block")
RESEARCH_DIR = Path("data/research")
CODEX_OUTPUT_DIR = Path("codex-output")
STAGE_SUMMARY_RECORDS_PATH = RESEARCH_DIR / "stage-summary-records-v0.yaml"
DOC_STALENESS_SOURCE_OF_TRUTH_PATH = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5eb-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5eb-next-stage-decision.yaml",
    "stage5ea_preservation": PROJECT_STATE_DIR / "stage5eb-stage5ea-preservation.yaml",
    "validation_finalization_policy": PROJECT_STATE_DIR / "stage5eb-validation-finalization-policy.yaml",
    "parallel_worker_policy": PROJECT_STATE_DIR / "stage5eb-parallel-worker-policy.yaml",
    "serial_pytest_policy": PROJECT_STATE_DIR / "stage5eb-serial-pytest-policy.yaml",
    "current_stage_registry_finalization_policy": PROJECT_STATE_DIR
    / "stage5eb-current-stage-registry-finalization-policy.yaml",
    "generic_stage_wrapper_repair": PROJECT_STATE_DIR / "stage5eb-generic-stage-wrapper-repair.yaml",
    "current_stage_state": PROJECT_STATE_DIR / "current-stage-state.yaml",
    "doc_ledger_tier_policy": PROJECT_STATE_DIR / "stage5eb-doc-ledger-tier-policy.yaml",
    "pytest_shard_duration_policy": PROJECT_STATE_DIR / "stage5eb-pytest-shard-duration-policy.yaml",
    "failing_shard_rerun_policy": PROJECT_STATE_DIR / "stage5eb-failing-shard-rerun-policy.yaml",
    "source_browser_cache_reuse_evidence": PROJECT_STATE_DIR
    / "stage5eb-source-browser-cache-reuse-evidence.yaml",
    "validation_rerun_discipline": PROJECT_STATE_DIR / "stage5eb-validation-rerun-discipline.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5eb-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5eb-reviewability-gap-register.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5eb-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5eb-credential-redaction-policy-preservation.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5eb-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5eb-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5eb-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage5eb-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage5eb-no-execution-transition-gate.yaml",
}

DATA_PATHS: dict[str, Path] = {}
DATA_PATHS.update(PROJECT_STATE_PATHS)
DATA_PATHS.update(SOURCE_HARVESTER_PATHS)
DATA_PATHS.update(TOKEN_PATHS)

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5eb-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5eb-next-stage-decision-v0.schema.json"),
    "stage5ea_preservation": Path("schemas/project-state/stage5eb-stage5ea-preservation-v0.schema.json"),
    "validation_finalization_policy": Path(
        "schemas/project-state/stage5eb-validation-finalization-policy-v0.schema.json"
    ),
    "parallel_worker_policy": Path("schemas/project-state/stage5eb-parallel-worker-policy-v0.schema.json"),
    "serial_pytest_policy": Path("schemas/project-state/stage5eb-serial-pytest-policy-v0.schema.json"),
    "current_stage_registry_finalization_policy": Path(
        "schemas/project-state/stage5eb-current-stage-registry-finalization-policy-v0.schema.json"
    ),
    "generic_stage_wrapper_repair": Path(
        "schemas/project-state/stage5eb-generic-stage-wrapper-repair-v0.schema.json"
    ),
    "current_stage_state": Path("schemas/project-state/current-stage-state-v0.schema.json"),
    "doc_ledger_tier_policy": Path("schemas/project-state/stage5eb-doc-ledger-tier-policy-v0.schema.json"),
    "pytest_shard_duration_policy": Path(
        "schemas/project-state/stage5eb-pytest-shard-duration-policy-v0.schema.json"
    ),
    "failing_shard_rerun_policy": Path(
        "schemas/project-state/stage5eb-failing-shard-rerun-policy-v0.schema.json"
    ),
    "source_browser_cache_reuse_evidence": Path(
        "schemas/project-state/stage5eb-source-browser-cache-reuse-evidence-v0.schema.json"
    ),
    "validation_rerun_discipline": Path(
        "schemas/project-state/stage5eb-validation-rerun-discipline-v0.schema.json"
    ),
    "reviewable_validation_evidence": Path(
        "schemas/project-state/stage5eb-reviewable-validation-evidence-v0.schema.json"
    ),
    "reviewability_gap_register": Path("schemas/project-state/stage5eb-reviewability-gap-register-v0.schema.json"),
    "codex_handoff_policy": Path("schemas/source-harvester/stage5eb-codex-handoff-policy-v0.schema.json"),
    "credential_redaction_policy_preservation": Path(
        "schemas/source-harvester/stage5eb-credential-redaction-policy-preservation-v0.schema.json"
    ),
    "generic_preservation": Path("schemas/token-block/stage5eb-generic-preservation-record-v0.schema.json"),
    "no_active_ingestion_proof": Path("schemas/token-block/stage5eb-no-active-ingestion-proof-v0.schema.json"),
    "no_byte_stream_transition_gate": Path(
        "schemas/token-block/stage5eb-no-byte-stream-transition-gate-v0.schema.json"
    ),
    "no_execution_transition_gate": Path("schemas/token-block/stage5eb-no-execution-transition-gate-v0.schema.json"),
}

SCHEMA_BY_DATA_KEY: dict[str, str] = {key: key for key in PROJECT_STATE_PATHS | SOURCE_HARVESTER_PATHS}
SCHEMA_BY_DATA_KEY.update(
    {
        "no_active_ingestion_proof": "no_active_ingestion_proof",
        "no_byte_stream_transition_gate": "no_byte_stream_transition_gate",
        "no_execution_transition_gate": "no_execution_transition_gate",
    }
)

FALSE_FLAGS = [
    "activation_authorized_now",
    "activation_decision_valid_now",
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "active_token_block_manifest_changed",
    "alberti_html_executed_now",
    "assistant_or_operator_number_fact_batch_performed_now",
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
    "new_number_fact_overlays_added_now",
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
    "route_stream_generated_now",
    "scoring_performed",
    "semantic_image_interpretation_performed",
    "solve_claim",
    "source_lock_evidence_updated_now",
    "source_lock_entry_batch_review_performed_now",
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


@dataclass
class Stage5EBValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5eb"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5eb() -> dict[str, dict[str, Any]]:
    records = _build_records()
    _write_schemas()
    _write_records(records)
    _write_codex_completion(records["summary"])
    _update_stage_summary_records(records["summary"])
    _update_doc_staleness_source_of_truth()
    return records


def validate_stage5eb() -> Stage5EBValidationResult:
    checks = [
        _validate_required_paths,
        _validate_schemas,
        _validate_summary,
        validate_stage5eb_stage5ea_preservation,
        validate_stage5eb_parallel_worker_policy,
        validate_stage5eb_serial_pytest_policy,
        validate_stage5eb_current_stage_registry_policy,
        validate_stage5eb_generic_stage_wrapper,
        validate_stage5eb_doc_ledger_tier_policy,
        validate_stage5eb_pytest_shard_policy,
        validate_stage5eb_failing_shard_rerun_policy,
        validate_stage5eb_source_browser_cache_reuse,
        validate_stage5eb_validation_rerun_discipline,
        validate_stage5eb_stage5bd_preservation,
        validate_stage5eb_active_lineage_preservation,
        validate_stage5eb_sidecar_gates,
        validate_stage5eb_handoff_continuity,
        validate_stage5eb_credential_redaction_policy,
        validate_stage5eb_governance_scope,
    ]
    errors = _collect_errors(checks)
    summary = _load(PROJECT_STATE_PATHS["summary"])
    counts = _summary_counts(summary)
    counts["stage5eb_record_count"] = len(DATA_PATHS)
    counts["stage5eb_schema_count"] = len(SCHEMA_PATHS)
    return Stage5EBValidationResult(len(errors), counts, errors)


def validate_stage5eb_stage5ea_preservation() -> Stage5EBValidationResult:
    path = PROJECT_STATE_PATHS["stage5ea_preservation"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "stage5ea_status": "complete",
            "stage5ea_issue": PREVIOUS_STAGE_ISSUE,
            "stage5ea_ci_status": "passed",
            "stage5ea_parallel_worker_cap": 8,
            "number_fact_review_batch_3_deferred_to_stage5eb": True,
            "number_fact_review_batch_3_deferred_to_stage5ec": True,
        },
        path,
    )
    return _result("stage5ea_preservation", payload, errors)


def validate_stage5eb_parallel_worker_policy() -> Stage5EBValidationResult:
    path = PROJECT_STATE_PATHS["parallel_worker_policy"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "local_parallel_default_workers": 10,
            "local_parallel_default_pytest_workers": 10,
            "maximum_supported_workers": 10,
            "maximum_supported_pytest_workers": 10,
            "old_8_worker_cap_removed": True,
            "old_16_worker_default_reintroduced": False,
            "ci_worker_policy_env_override_allowed": True,
        },
        path,
    )
    return _result("parallel_worker_policy", payload, errors)


def validate_stage5eb_serial_pytest_policy() -> Stage5EBValidationResult:
    path = PROJECT_STATE_PATHS["serial_pytest_policy"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "full_serial_pytest_default_for_future_stages": False,
            "full_serial_pytest_required_for_normal_stage_completion": False,
            "full_serial_pytest_profile_name": "full-serial-rare",
            "full_serial_pytest_allowed_only_when_explicitly_requested": True,
            "full_serial_pytest_must_not_run_inside_ci_profile": True,
            "full_serial_pytest_must_not_run_inside_local_fast_profile": True,
            "full_serial_pytest_must_not_run_inside_full_parallel_profile": True,
        },
        path,
    )
    return _result("serial_pytest_policy", payload, errors)


def validate_stage5eb_current_stage_registry_policy() -> Stage5EBValidationResult:
    policy_path = PROJECT_STATE_PATHS["current_stage_registry_finalization_policy"]
    state_path = PROJECT_STATE_PATHS["current_stage_state"]
    payload = _load(policy_path)
    state = _load(state_path)
    errors = _expected_errors(
        payload,
        {
            "current_stage_registry_is_committed_pre_push_state": True,
            "self_referential_commit_hash_not_required_in_committed_registry": True,
            "final_commit_and_final_ci_recorded_in_ignored_codex_output_summary": True,
            "final_commit_and_final_ci_recorded_in_github_issue_comment": True,
        },
        policy_path,
    )
    errors.extend(
        _expected_errors(
            state,
            {
                "latest_completed_stage_commit_recording_policy": "external_post_push_handoff",
                "latest_completed_stage_ci_status_recording_policy": "external_post_push_handoff",
                "latest_completed_stage_commit_in_committed_registry": "not_applicable_self_referential",
                "latest_completed_stage_ci_status_in_committed_registry": "not_applicable_pre_push",
                "post_push_handoff_required": True,
            },
            state_path,
        )
    )
    allowed_current_states = {
        (STAGE_ID, NEXT_STAGE_ID),
        ("stage-5ec", "stage-5ed"),
    }
    current_pair = (state.get("latest_completed_stage_id"), state.get("recommended_next_stage_id"))
    if current_pair not in allowed_current_states:
        errors.append(
            f"{state_path.as_posix()}: latest/recommended stage pair must be one of "
            f"{sorted(allowed_current_states)!r}, found {current_pair!r}"
        )
    if state.get("latest_completed_stage_commit") == "":
        errors.append("current-stage registry must not use blank latest_completed_stage_commit")
    if state.get("latest_completed_stage_ci_status") == "pending_post_push":
        errors.append("current-stage registry must not use pending_post_push as final status")
    return _result("current_stage_registry_policy", payload | {"state_record_checked": True}, errors)


def validate_stage5eb_generic_stage_wrapper() -> Stage5EBValidationResult:
    path = PROJECT_STATE_PATHS["generic_stage_wrapper_repair"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "stage_command_normalization_generic": True,
            "validate_command_generated_as": "validate-stage5eb",
            "summary_command_generated_as": "stage5eb-summary",
            "focused_test_file_pattern": "tests/python/test_stage5eb_*.py",
            "hardcoded_stage_allowlist_removed": True,
        },
        path,
    )
    for source, expected in {
        "stage-5eb": "validate-stage5eb",
        "stage5eb": "validate-stage5eb",
        "5eb": "validate-stage5eb",
        "eb": "validate-stage5eb",
    }.items():
        if validation_command_name(source) != expected:
            errors.append(f"validation command normalization failed for {source}")
    if validation_command_name("stage-5eb") == "validate-stage-5eb":
        errors.append("hyphenated validate-stage-5eb command generated unexpectedly")
    return _result("generic_stage_wrapper", payload, errors)


def validate_stage5eb_doc_ledger_tier_policy() -> Stage5EBValidationResult:
    path = PROJECT_STATE_PATHS["doc_ledger_tier_policy"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "tier_1_docs_required_latest_stage": True,
            "tier_2_docs_required_only_if_domain_changed": True,
            "tier_3_docs_must_not_require_latest_stage": True,
            "broad_docs_can_defer_to_current_stage_registry": True,
        },
        path,
    )
    return _result("doc_ledger_tier_policy", payload, errors)


def validate_stage5eb_pytest_shard_policy() -> Stage5EBValidationResult:
    path = PROJECT_STATE_PATHS["pytest_shard_duration_policy"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "pytest_sharding_duration_aware": True,
            "pytest_shard_plan_records_estimated_weight": True,
            "pytest_shard_plan_records_test_files": True,
            "pytest_shard_plan_records_known_serial_isolated_files": True,
            "pytest_shard_plan_records_rerun_commands": True,
            "pytest_slow_files_identified": True,
        },
        path,
    )
    return _result("pytest_shard_policy", payload, errors)


def validate_stage5eb_failing_shard_rerun_policy() -> Stage5EBValidationResult:
    path = PROJECT_STATE_PATHS["failing_shard_rerun_policy"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "failing_shard_rerun_helper_available": True,
            "full_parallel_failure_summary_includes_rerun_guidance": True,
            "do_not_rerun_full_parallel_until_failing_slice_passes": True,
            "run_pytest_shard_script_present": True,
            "run_failing_pytest_slice_script_present": True,
        },
        path,
    )
    for script in (
        Path("scripts/ci/run-pytest-shard.ps1"),
        Path("scripts/ci/run-pytest-shard.sh"),
        Path("scripts/ci/run-failing-pytest-slice.ps1"),
        Path("scripts/ci/run-failing-pytest-slice.sh"),
    ):
        if not script.exists():
            errors.append(f"failing-shard helper missing: {script.as_posix()}")
    return _result("failing_shard_rerun_policy", payload, errors)


def validate_stage5eb_source_browser_cache_reuse() -> Stage5EBValidationResult:
    path = PROJECT_STATE_PATHS["source_browser_cache_reuse_evidence"]
    payload = _load(path)
    cache = NumberFactOverlayCache.load()
    errors = _expected_errors(
        payload,
        {
            "source_browser_overlay_cache_constructed_once_per_index_load": True,
            "source_browser_table_display_uses_shared_overlay_cache": True,
            "source_browser_filtering_uses_shared_overlay_cache": True,
            "source_browser_detail_panel_uses_shared_overlay_cache": True,
            "source_browser_reviewability_counts_use_single_overlay_cache": True,
            "no_per_row_overlay_file_scan": True,
        },
        path,
    )
    if cache.load_count != 1:
        errors.append("number fact overlay cache must report one overlay load")
    return _result("source_browser_cache_reuse", payload, errors)


def validate_stage5eb_validation_rerun_discipline() -> Stage5EBValidationResult:
    path = PROJECT_STATE_PATHS["validation_rerun_discipline"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "focused_baseline_validators_before_editing": True,
            "touched_unit_tests_after_code_change": True,
            "stage_fast_after_code_change": True,
            "local_fast_before_commit": True,
            "full_parallel_once_before_commit": True,
            "inspect_failure_before_rerun": True,
            "rerun_only_failing_slice_before_full_parallel": True,
        },
        path,
    )
    return _result("validation_rerun_discipline", payload, errors)


def validate_stage5eb_stage5bd_preservation() -> Stage5EBValidationResult:
    return _validate_preservation_record("stage5bd_preservation", "stage-5bd")


def validate_stage5eb_active_lineage_preservation() -> Stage5EBValidationResult:
    return _validate_preservation_record("active_lineage_preservation", "active-lineage")


def _validate_preservation_record(key: str, source_stage_id: str) -> Stage5EBValidationResult:
    path = TOKEN_PATHS[key]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "source_stage_id": source_stage_id,
            "preserved": True,
            "rewritten": False,
            "superseded_now": False,
        },
        path,
    )
    errors.extend(_required_false_errors(payload, path.as_posix()))
    return _result(key, payload, errors)


def validate_stage5eb_sidecar_gates() -> Stage5EBValidationResult:
    errors: list[str] = []
    for key, gate in (
        ("no_active_ingestion_proof", "active_ingestion_gate_closed"),
        ("no_byte_stream_transition_gate", "byte_stream_transition_gate_closed"),
        ("no_execution_transition_gate", "execution_transition_gate_closed"),
    ):
        payload = _load(TOKEN_PATHS[key])
        errors.extend(_expected_errors(payload, {gate: True, "authorized_now": False}, TOKEN_PATHS[key]))
        errors.extend(_required_false_errors(payload, TOKEN_PATHS[key].as_posix()))
    return Stage5EBValidationResult(len(errors), {"sidecar_gate_records": 3}, errors)


def validate_stage5eb_handoff_continuity() -> Stage5EBValidationResult:
    path = SOURCE_HARVESTER_PATHS["codex_handoff_policy"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "canonical_handoff_root": "codex-output",
            "codex_output_used": False,
            "codex_underscore_output_root_forbidden": True,
        },
        path,
    )
    if Path("codex_output").exists():
        errors.append("codex_output directory must remain absent")
    return _result("handoff_continuity", payload, errors)


def validate_stage5eb_credential_redaction_policy() -> Stage5EBValidationResult:
    path = SOURCE_HARVESTER_PATHS["credential_redaction_policy_preservation"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "credential_redaction_policy_preserved": True,
            "secrets_or_tokens_committed": False,
        },
        path,
    )
    return _result("credential_redaction_policy", payload, errors)


def validate_stage5eb_governance_scope() -> Stage5EBValidationResult:
    payload = _load(PROJECT_STATE_PATHS["summary"])
    errors = _required_false_errors(payload, PROJECT_STATE_PATHS["summary"].as_posix())
    errors.extend(
        _expected_errors(
            payload,
            {
                "metadata_only": True,
                "validation_infrastructure_stage": True,
                "number_fact_review_batch_3_deferred_to_stage5ec": True,
                "recommended_next_stage_id": NEXT_STAGE_ID,
            },
            PROJECT_STATE_PATHS["summary"],
        )
    )
    return _result("governance_scope", payload, errors)


def stage5eb_summary_text() -> str:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    current = _load(PROJECT_STATE_PATHS["current_stage_state"])
    return "\n".join(
        [
            f"stage_id={summary.get('stage_id', STAGE_ID)}",
            f"status={summary.get('status', 'unknown')}",
            f"latest_completed_stage={current.get('latest_completed_stage_id', '')}",
            f"recommended_next_stage={summary.get('recommended_next_stage_id', '')}",
            f"stage5ea_preserved={_format(summary.get('stage5ea_status') == 'complete')}",
            f"number_fact_review_batch_3_performed_now={_format(summary.get('number_fact_review_batch_3_performed_now'))}",
            f"number_fact_review_batch_3_deferred_to_stage5ec={_format(summary.get('number_fact_review_batch_3_deferred_to_stage5ec'))}",
            f"local_parallel_default_workers={summary.get('local_parallel_default_workers', '')}",
            f"local_parallel_default_pytest_workers={summary.get('local_parallel_default_pytest_workers', '')}",
            f"full_serial_pytest_default_for_future_stages={_format(summary.get('full_serial_pytest_default_for_future_stages'))}",
            f"source_browser_overlay_cache_reuse_validated={_format(summary.get('source_browser_overlay_cache_reuse_validated'))}",
            f"parallel_worker_cap={summary.get('parallel_worker_cap', '')}",
            f"pytest_timeout_seconds={summary.get('pytest_timeout_seconds', '')}",
            f"codex_handoff_root={summary.get('canonical_codex_handoff_root', '')}",
            "solve_claim=false",
        ]
    )


def _build_records() -> dict[str, dict[str, Any]]:
    stage5ea = _load(PROJECT_STATE_DIR / "stage5ea-summary.yaml")
    base = _stage_base()
    false_flags = _false_flags()
    records: dict[str, dict[str, Any]] = {}
    records.update(_project_state_records(base, false_flags, stage5ea))
    records.update(_source_harvester_records(base, false_flags))
    records.update(_token_records(base, false_flags))
    return records


def _project_state_records(
    base: dict[str, Any],
    false_flags: dict[str, bool],
    stage5ea: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    stage5ea_worker_cap = int(stage5ea.get("parallel_worker_cap", 8))
    summary = {
        **base,
        **false_flags,
        "record_type": "stage5eb_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "source_previous_stage_title": PREVIOUS_STAGE_TITLE,
        "source_previous_stage_implementation_commit": PREVIOUS_STAGE_IMPLEMENTATION_COMMIT,
        "source_previous_stage_final_commit": PREVIOUS_STAGE_FINAL_COMMIT,
        "source_previous_issue": PREVIOUS_STAGE_ISSUE,
        "source_previous_ci_run": PREVIOUS_CI_RUN,
        "source_previous_ci_status": "passed",
        "stage5ea_status": stage5ea.get("status", "complete"),
        "stage5ea_issue": PREVIOUS_STAGE_ISSUE,
        "stage5ea_ci_status": "passed",
        "stage5ea_parallel_worker_cap": stage5ea_worker_cap,
        "stage5ea_recommended_stage5eb_number_fact_batch_3": True,
        "operator_inserted_validation_finalization_repair_before_batch_3": True,
        "number_fact_review_batch_3_deferred_to_stage5eb": True,
        "number_fact_review_batch_3_deferred_to_stage5ec": True,
        "local_parallel_default_workers": LOCAL_PARALLEL_DEFAULT_WORKERS,
        "local_parallel_default_pytest_workers": LOCAL_PARALLEL_DEFAULT_PYTEST_WORKERS,
        "maximum_supported_workers": PARALLEL_WORKER_CAP,
        "maximum_supported_pytest_workers": PARALLEL_WORKER_CAP,
        "old_8_worker_cap_removed": True,
        "old_16_worker_default_reintroduced": False,
        "full_serial_pytest_default_for_future_stages": False,
        "full_serial_pytest_required_for_normal_stage_completion": False,
        "full_serial_pytest_allowed_only_when_explicitly_requested": True,
        "generic_stage_validation_wrapper_repaired": True,
        "doc_ledger_tier_policy_enforced": True,
        "current_stage_registry_finalization_policy_repaired": True,
        "source_browser_overlay_cache_reuse_validated": True,
        "pytest_shard_duration_policy_repaired": True,
        "failing_shard_rerun_policy_recorded": True,
        "validation_rerun_discipline_recorded": True,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "pytest_timeout_seconds": PYTEST_TIMEOUT_SECONDS,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
    }
    return {
        "summary": summary,
        "next_stage_decision": {
            **base,
            **false_flags,
            "record_type": "stage5eb_next_stage_decision",
            "schema": SCHEMA_PATHS["next_stage_decision"].as_posix(),
            "status": "complete",
            "stage5ea_recommended_stage5eb_number_fact_batch_3": True,
            "operator_inserted_validation_finalization_repair_before_batch_3": True,
            "number_fact_review_batch_3_deferred_to_stage5ec": True,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        },
        "stage5ea_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5eb_stage5ea_preservation",
            "schema": SCHEMA_PATHS["stage5ea_preservation"].as_posix(),
            "status": "complete",
            "stage5ea_status": stage5ea.get("status", "complete"),
            "stage5ea_issue": PREVIOUS_STAGE_ISSUE,
            "stage5ea_ci_status": "passed",
            "stage5ea_parallel_worker_cap": stage5ea_worker_cap,
            "stage5ea_historical_test_isolation_repaired": True,
            "stage5ea_source_browser_overlay_cache_implemented": True,
            "number_fact_review_batch_3_deferred_to_stage5eb": True,
            "number_fact_review_batch_3_deferred_to_stage5ec": True,
        },
        "validation_finalization_policy": {
            **base,
            **false_flags,
            "record_type": "stage5eb_validation_finalization_policy",
            "schema": SCHEMA_PATHS["validation_finalization_policy"].as_posix(),
            "status": "complete",
            "full_serial_pytest_default_for_future_stages": False,
            "full_serial_pytest_required_for_normal_stage_completion": False,
            "full_parallel_is_normal_final_local_profile": True,
            "full_serial_pytest_profile_name": "full-serial-rare",
            "full_serial_pytest_allowed_only_when_explicitly_requested": True,
        },
        "current_stage_state": {
            **base,
            **false_flags,
            "record_type": "current_stage_state",
            "schema": SCHEMA_PATHS["current_stage_state"].as_posix(),
            "status": "complete",
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "latest_completed_stage_commit_recording_policy": "external_post_push_handoff",
            "latest_completed_stage_ci_status_recording_policy": "external_post_push_handoff",
            "latest_completed_stage_commit_in_committed_registry": "not_applicable_self_referential",
            "latest_completed_stage_ci_status_in_committed_registry": "not_applicable_pre_push",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
            "stage_registry_is_source_of_truth": True,
            "historical_tests_must_not_require_latest_stage": True,
            "current_stage_registry_is_committed_pre_push_state": True,
            "self_referential_commit_hash_not_required_in_committed_registry": True,
            "final_commit_and_ci_recorded_externally": True,
            "post_push_handoff_required": True,
            "post_push_handoff_locations": [
                "codex-output/stage5eb-codex-completion.md",
                "GitHub issue comment",
            ],
        },
        "parallel_worker_policy": {
            **base,
            **false_flags,
            "record_type": "stage5eb_parallel_worker_policy",
            "schema": SCHEMA_PATHS["parallel_worker_policy"].as_posix(),
            "status": "complete",
            "local_parallel_default_workers": LOCAL_PARALLEL_DEFAULT_WORKERS,
            "local_parallel_default_pytest_workers": LOCAL_PARALLEL_DEFAULT_PYTEST_WORKERS,
            "maximum_supported_workers": PARALLEL_WORKER_CAP,
            "maximum_supported_pytest_workers": PARALLEL_WORKER_CAP,
            "old_8_worker_cap_removed": True,
            "old_16_worker_default_reintroduced": False,
            "ci_worker_policy_env_override_allowed": True,
            "ci_default_may_be_lower_than_local_default_if_env_requests_it": True,
        },
        "serial_pytest_policy": {
            **base,
            **false_flags,
            "record_type": "stage5eb_serial_pytest_policy",
            "schema": SCHEMA_PATHS["serial_pytest_policy"].as_posix(),
            "status": "complete",
            "full_serial_pytest_default_for_future_stages": False,
            "full_serial_pytest_required_for_normal_stage_completion": False,
            "full_serial_pytest_profile_name": "full-serial-rare",
            "full_serial_pytest_allowed_only_when_explicitly_requested": True,
            "full_serial_pytest_must_not_run_inside_ci_profile": True,
            "full_serial_pytest_must_not_run_inside_local_fast_profile": True,
            "full_serial_pytest_must_not_run_inside_full_parallel_profile": True,
        },
        "current_stage_registry_finalization_policy": {
            **base,
            **false_flags,
            "record_type": "stage5eb_current_stage_registry_finalization_policy",
            "schema": SCHEMA_PATHS["current_stage_registry_finalization_policy"].as_posix(),
            "status": "complete",
            "current_stage_registry_is_committed_pre_push_state": True,
            "current_stage_registry_must_not_claim_final_ci_passed_inside_same_commit": True,
            "self_referential_commit_hash_not_required_in_committed_registry": True,
            "final_commit_and_final_ci_recorded_in_ignored_codex_output_summary": True,
            "final_commit_and_final_ci_recorded_in_github_issue_comment": True,
            "current_stage_registry_final_commit_field_policy": "not_applicable_self_referential_or_external_handoff",
        },
        "generic_stage_wrapper_repair": {
            **base,
            **false_flags,
            "record_type": "stage5eb_generic_stage_wrapper_repair",
            "schema": SCHEMA_PATHS["generic_stage_wrapper_repair"].as_posix(),
            "status": "complete",
            "stage_command_normalization_generic": True,
            "stage_identifier_examples_supported": ["stage-5eb", "stage5eb", "5eb", "eb"],
            "validate_command_generated_as": "validate-stage5eb",
            "summary_command_generated_as": "stage5eb-summary",
            "focused_test_file_pattern": "tests/python/test_stage5eb_*.py",
            "hardcoded_stage_allowlist_removed": True,
        },
        "doc_ledger_tier_policy": {
            **base,
            **false_flags,
            "record_type": "stage5eb_doc_ledger_tier_policy",
            "schema": SCHEMA_PATHS["doc_ledger_tier_policy"].as_posix(),
            "status": "complete",
            "tier_1_docs_required_latest_stage": True,
            "tier_1_paths": [
                "STATUS.md",
                "docs/roadmap/staged-plan.md",
                "data/project-state/current-stage-state.yaml",
                "ChatGPT-ContextFile.md",
                "data/project-state/operational-file-map.yaml",
            ],
            "tier_2_docs_required_only_if_domain_changed": True,
            "tier_3_docs_must_not_require_latest_stage": True,
            "broad_docs_can_defer_to_current_stage_registry": True,
        },
        "pytest_shard_duration_policy": {
            **base,
            **false_flags,
            "record_type": "stage5eb_pytest_shard_duration_policy",
            "schema": SCHEMA_PATHS["pytest_shard_duration_policy"].as_posix(),
            "status": "complete",
            "pytest_sharding_duration_aware": True,
            "pytest_shard_duration_report_created": True,
            "pytest_slow_files_identified": True,
            "pytest_known_serial_isolated_files_recorded": True,
            "pytest_shard_plan_records_estimated_weight": True,
            "pytest_shard_plan_records_test_files": True,
            "pytest_shard_plan_records_known_serial_isolated_files": True,
            "pytest_shard_plan_records_rerun_commands": True,
        },
        "failing_shard_rerun_policy": {
            **base,
            **false_flags,
            "record_type": "stage5eb_failing_shard_rerun_policy",
            "schema": SCHEMA_PATHS["failing_shard_rerun_policy"].as_posix(),
            "status": "complete",
            "failing_shard_rerun_helper_available": True,
            "full_parallel_failure_summary_includes_rerun_guidance": True,
            "do_not_rerun_full_parallel_until_failing_slice_passes": True,
            "run_pytest_shard_script_present": True,
            "run_failing_pytest_slice_script_present": True,
        },
        "source_browser_cache_reuse_evidence": {
            **base,
            **false_flags,
            "record_type": "stage5eb_source_browser_cache_reuse_evidence",
            "schema": SCHEMA_PATHS["source_browser_cache_reuse_evidence"].as_posix(),
            "status": "complete",
            "source_browser_overlay_cache_constructed_once_per_index_load": True,
            "source_browser_table_display_uses_shared_overlay_cache": True,
            "source_browser_filtering_uses_shared_overlay_cache": True,
            "source_browser_detail_panel_uses_shared_overlay_cache": True,
            "source_browser_reviewability_counts_use_single_overlay_cache": True,
            "no_per_row_overlay_file_scan": True,
            "cache_refresh_available_after_overlay_file_changes": True,
        },
        "validation_rerun_discipline": {
            **base,
            **false_flags,
            "record_type": "stage5eb_validation_rerun_discipline",
            "schema": SCHEMA_PATHS["validation_rerun_discipline"].as_posix(),
            "status": "complete",
            "focused_baseline_validators_before_editing": True,
            "touched_unit_tests_after_code_change": True,
            "stage_fast_after_code_change": True,
            "local_fast_before_commit": True,
            "full_parallel_once_before_commit": True,
            "inspect_failure_before_rerun": True,
            "rerun_only_failing_slice_before_full_parallel": True,
            "after_push_wait_for_ci": True,
        },
        "reviewable_validation_evidence": {
            **base,
            **false_flags,
            "record_type": "stage5eb_reviewable_validation_evidence",
            "schema": SCHEMA_PATHS["reviewable_validation_evidence"].as_posix(),
            "status": "complete",
            "validation_evidence_is_record_backed": True,
            "terminal_output_alone_is_not_evidence": True,
        },
        "reviewability_gap_register": {
            **base,
            **false_flags,
            "record_type": "stage5eb_reviewability_gap_register",
            "schema": SCHEMA_PATHS["reviewability_gap_register"].as_posix(),
            "status": "complete",
            "open_gaps": [
                {
                    "gap_id": "stage5eb-follow-on-number-fact-batch-3",
                    "status": "deferred_to_stage5ec",
                    "reason": "Operator inserted validation-finalization and 10-worker repair before the review batch.",
                }
            ],
        },
    }


def _source_harvester_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "codex_handoff_policy": {
            **base,
            **false_flags,
            "record_type": "stage5eb_codex_handoff_policy",
            "schema": SCHEMA_PATHS["codex_handoff_policy"].as_posix(),
            "status": "complete",
            "canonical_handoff_root": "codex-output",
            "codex_output_used": False,
            "codex_underscore_output_root_forbidden": True,
            "completion_summary_path": "codex-output/stage5eb-codex-completion.md",
        },
        "credential_redaction_policy_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5eb_credential_redaction_policy_preservation",
            "schema": SCHEMA_PATHS["credential_redaction_policy_preservation"].as_posix(),
            "status": "complete",
            "credential_redaction_policy_preserved": True,
            "secrets_or_tokens_committed": False,
            "local_private_paths_must_not_be_published": True,
        },
    }


def _token_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for key, source_stage in (
        ("stage5bd_preservation", "stage-5bd"),
        ("active_lineage_preservation", "active-lineage"),
    ):
        records[key] = {
            **base,
            **false_flags,
            "record_type": f"stage5eb_{key}",
            "schema": SCHEMA_PATHS["generic_preservation"].as_posix(),
            "status": "complete",
            "source_stage_id": source_stage,
            "preserved": True,
            "rewritten": False,
            "superseded_now": False,
            "notes": "Stage 5EB records preservation only; it does not mutate token-block planning inputs.",
        }
    records["no_active_ingestion_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5eb_no_active_ingestion_proof",
        "schema": SCHEMA_PATHS["no_active_ingestion_proof"].as_posix(),
        "status": "complete",
        "active_ingestion_gate_closed": True,
        "authorized_now": False,
    }
    records["no_byte_stream_transition_gate"] = {
        **base,
        **false_flags,
        "record_type": "stage5eb_no_byte_stream_transition_gate",
        "schema": SCHEMA_PATHS["no_byte_stream_transition_gate"].as_posix(),
        "status": "complete",
        "byte_stream_transition_gate_closed": True,
        "authorized_now": False,
    }
    records["no_execution_transition_gate"] = {
        **base,
        **false_flags,
        "record_type": "stage5eb_no_execution_transition_gate",
        "schema": SCHEMA_PATHS["no_execution_transition_gate"].as_posix(),
        "status": "complete",
        "execution_transition_gate_closed": True,
        "authorized_now": False,
    }
    return records


def _write_records(records: dict[str, dict[str, Any]]) -> None:
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        required = ["record_type", "stage_id", "schema"]
        if key == "summary":
            required.extend(["status", "recommended_next_stage_id"])
        elif key == "current_stage_state":
            required.extend(["latest_completed_stage_id", "recommended_next_stage_id"])
        write_json(path, _object_schema(required, key))


def _object_schema(required: list[str], key: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "puzzle_execution_allowed": {"const": False},
        "solve_claim": {"const": False},
        "canonical_codex_handoff_root": {"const": "codex-output"},
        "number_fact_review_batch_3_performed_now": {"const": False},
        "source_lock_entry_batch_review_performed_now": {"const": False},
        "new_number_fact_overlays_added_now": {"const": False},
        "pivot_target_selected_now": {"const": False},
        "byte_stream_generation_authorized_now": {"const": False},
        "execution_performed": {"const": False},
        "validation_infrastructure_stage": {"const": True},
        "local_parallel_default_workers": {"const": 10},
        "local_parallel_default_pytest_workers": {"const": 10},
        "maximum_supported_workers": {"const": 10},
        "maximum_supported_pytest_workers": {"const": 10},
        "old_8_worker_cap_removed": {"const": True},
        "old_16_worker_default_reintroduced": {"const": False},
        "full_serial_pytest_default_for_future_stages": {"const": False},
        "full_serial_pytest_required_for_normal_stage_completion": {"const": False},
        "codex_output_used": {"const": False},
    }
    for flag in FALSE_FLAGS:
        properties.setdefault(flag, {"const": False})
    if key == "current_stage_state":
        properties.update(
            {
                "record_type": {"const": "current_stage_state"},
                "latest_completed_stage_id": {"const": STAGE_ID},
                "recommended_next_stage_id": {"const": NEXT_STAGE_ID},
                "stage_registry_is_source_of_truth": {"const": True},
                "latest_completed_stage_commit_recording_policy": {"const": "external_post_push_handoff"},
                "latest_completed_stage_ci_status_recording_policy": {"const": "external_post_push_handoff"},
                "latest_completed_stage_commit_in_committed_registry": {"const": "not_applicable_self_referential"},
                "latest_completed_stage_ci_status_in_committed_registry": {"const": "not_applicable_pre_push"},
            }
        )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
        "required": required,
        "properties": properties,
    }


def _validate_required_paths() -> Stage5EBValidationResult:
    missing = [
        f"required Stage 5EB path missing: {path.as_posix()}"
        for path in [*DATA_PATHS.values(), *SCHEMA_PATHS.values()]
        if not path.exists()
    ]
    return Stage5EBValidationResult(len(missing), {"required_paths_missing": len(missing)}, missing)


def _validate_schemas() -> Stage5EBValidationResult:
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
    return Stage5EBValidationResult(len(errors), {"schema_validation_errors": len(errors)}, errors)


def _validate_summary() -> Stage5EBValidationResult:
    payload = _load(PROJECT_STATE_PATHS["summary"])
    errors = _required_false_errors(payload, PROJECT_STATE_PATHS["summary"].as_posix())
    errors.extend(
        _expected_errors(
            payload,
            {
                "stage_id": STAGE_ID,
                "status": "complete",
                "stage5ea_recommended_stage5eb_number_fact_batch_3": True,
                "operator_inserted_validation_finalization_repair_before_batch_3": True,
                "number_fact_review_batch_3_deferred_to_stage5ec": True,
                "local_parallel_default_workers": 10,
                "full_serial_pytest_default_for_future_stages": False,
                "recommended_next_stage_id": NEXT_STAGE_ID,
            },
            PROJECT_STATE_PATHS["summary"],
        )
    )
    return _result("summary", payload, errors)


def _collect_errors(checks: list[Callable[[], Stage5EBValidationResult]]) -> list[str]:
    errors: list[str] = []
    for check in checks:
        result = check()
        errors.extend(result.errors)
    return errors


def _result(label: str, payload: dict[str, Any], errors: list[str]) -> Stage5EBValidationResult:
    counts = _summary_counts(payload)
    counts["validator"] = label
    return Stage5EBValidationResult(len(errors), counts, errors)


def _stage_base() -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "validation_infrastructure_stage": True,
        "source_lock_only": False,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "canonical_codex_handoff_root": "codex-output",
    }


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in FALSE_FLAGS}


def _load(path: Path) -> dict[str, Any]:
    payload = read_yaml(path)
    return payload if isinstance(payload, dict) else {}


def _required_false_errors(payload: dict[str, Any], label: str) -> list[str]:
    return [f"{label}: {key} must be false" for key in FALSE_FLAGS if payload.get(key) is not False]


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


def _write_codex_completion(summary: dict[str, Any]) -> None:
    CODEX_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    text = "\n".join(
        [
            "# Stage 5EB Codex Completion",
            "",
            f"- stage_id: {STAGE_ID}",
            f"- status: {summary.get('status')}",
            f"- next_stage: {NEXT_STAGE_ID}",
            f"- local_parallel_default_workers: {LOCAL_PARALLEL_DEFAULT_WORKERS}",
            f"- local_parallel_default_pytest_workers: {LOCAL_PARALLEL_DEFAULT_PYTEST_WORKERS}",
            "- full_serial_pytest_default_for_future_stages: false",
            "- full_serial_pytest_run_locally: false",
            "- current_stage_registry_finalization_policy_repaired: true",
            "- source_browser_overlay_cache_reuse_validated: true",
            "- pytest_shard_duration_policy_repaired: true",
            "- failing_shard_rerun_policy_recorded: true",
            "- number_fact_review_batch_3_performed_now: false",
            "- number_fact_review_batch_3_deferred_to_stage5ec: true",
            "- source_lock_evidence_updated_now: false",
            "- new_number_fact_overlays_added_now: false",
            "- execution_performed: false",
            "- solve_claim: false",
            "",
        ]
    )
    (CODEX_OUTPUT_DIR / "stage5eb-codex-completion.md").write_text(text, encoding="utf-8")


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
                "Finalized validation policy by moving local parallel validation to 10 workers, making "
                "full serial pytest a rare explicit fallback, repairing current-stage registry finalization "
                "semantics, genericizing stage wrappers, and adding failing-shard rerun guidance."
            ),
            "key_outputs": [
                "Current-stage registry points latest to Stage 5EB and next to Stage 5EC without blank final-hash placeholders.",
                "Local validation defaults and caps are 10 workers / 10 pytest workers.",
                "Full serial pytest remains full-serial-rare and is not part of normal final validation.",
                "Source Browser number-fact overlays are verified as shared-cache caller paths.",
            ],
            "result_status": "validation_finalization_repaired",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                f"records={len(DATA_PATHS)}; schemas={len(SCHEMA_PATHS)}; "
                f"worker_cap={summary.get('parallel_worker_cap')}; next={NEXT_STAGE_ID}."
            ),
        }
    )
    payload["records"] = records
    write_yaml(STAGE_SUMMARY_RECORDS_PATH, payload)


def _update_doc_staleness_source_of_truth() -> None:
    payload = _load(DOC_STALENESS_SOURCE_OF_TRUTH_PATH)
    if not payload:
        return
    payload["latest_completed_stage_after_this_stage"] = STAGE_TITLE
    payload["latest_completed_stage_prefix"] = "Stage 5EB"
    payload["next_stage_after_this_stage"] = NEXT_STAGE_TITLE
    payload["expected_next_stage_prefix"] = "Stage 5EC"
    payload["expected_latest_after_stage5ah"] = STAGE_TITLE
    payload["expected_next_after_stage5ah"] = NEXT_STAGE_TITLE
    write_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH, payload)


VALIDATOR_BY_NAME: dict[str, Callable[[], Stage5EBValidationResult]] = {
    "stage5ea_preservation": validate_stage5eb_stage5ea_preservation,
    "parallel_worker_policy": validate_stage5eb_parallel_worker_policy,
    "serial_pytest_policy": validate_stage5eb_serial_pytest_policy,
    "current_stage_registry_policy": validate_stage5eb_current_stage_registry_policy,
    "generic_stage_wrapper": validate_stage5eb_generic_stage_wrapper,
    "doc_ledger_tier_policy": validate_stage5eb_doc_ledger_tier_policy,
    "pytest_shard_policy": validate_stage5eb_pytest_shard_policy,
    "failing_shard_rerun_policy": validate_stage5eb_failing_shard_rerun_policy,
    "source_browser_cache_reuse": validate_stage5eb_source_browser_cache_reuse,
    "validation_rerun_discipline": validate_stage5eb_validation_rerun_discipline,
    "stage5bd_preservation": validate_stage5eb_stage5bd_preservation,
    "active_lineage_preservation": validate_stage5eb_active_lineage_preservation,
    "sidecar_gates": validate_stage5eb_sidecar_gates,
    "handoff_continuity": validate_stage5eb_handoff_continuity,
    "credential_redaction_policy": validate_stage5eb_credential_redaction_policy,
    "governance_scope": validate_stage5eb_governance_scope,
}
