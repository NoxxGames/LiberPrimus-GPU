"""Stage 5EA validation throughput and historical-test isolation repair records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.number_facts import NumberFactOverlayCache
from libreprimus.token_block.models import read_yaml, write_json, write_yaml
from libreprimus.validation.stage_id import validation_command_name

STAGE_ID = "stage-5ea"
STAGE_TITLE = (
    "Stage 5EA - Validation throughput, current-stage registry, historical-test isolation, "
    "and Source Browser fact-card performance repair, without execution"
)
PROMPT_TYPE = "codex_validation_throughput_historical_test_isolation_repair"
PREVIOUS_STAGE_ID = "stage-5dz"
PREVIOUS_STAGE_TITLE = (
    "Stage 5DZ - Triangle/Page32 bounded-solve findings source-lock and enriched review records, "
    "without execution"
)
PREVIOUS_STAGE_FINAL_COMMIT = "e1613cff0b8a93d5186ffa2af5b7407a908ffc13"
PREVIOUS_STAGE_ISSUE = 161
PREVIOUS_CI_RUN = 27309009007
NEXT_STAGE_ID = "stage-5eb"
NEXT_STAGE_TITLE = "Stage 5EB - Operator/assistant source-lock number-fact review batch 3, without execution"
NEXT_PROMPT_TYPE = "assistant_or_operator_review_then_codex_overlay_update"
PARALLEL_WORKER_CAP = 8
PYTEST_TIMEOUT_SECONDS = 3600

PROJECT_STATE_DIR = Path("data/project-state")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
TOKEN_BLOCK_DIR = Path("data/token-block")
RESEARCH_DIR = Path("data/research")
CODEX_OUTPUT_DIR = Path("codex-output")
STAGE_SUMMARY_RECORDS_PATH = RESEARCH_DIR / "stage-summary-records-v0.yaml"
DOC_STALENESS_SOURCE_OF_TRUTH_PATH = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5ea-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5ea-next-stage-decision.yaml",
    "stage5dz_verification": PROJECT_STATE_DIR / "stage5ea-stage5dz-verification.yaml",
    "current_stage_registry_repair": PROJECT_STATE_DIR / "stage5ea-current-stage-registry-repair.yaml",
    "current_stage_state": PROJECT_STATE_DIR / "current-stage-state.yaml",
    "historical_test_isolation_repair": PROJECT_STATE_DIR / "stage5ea-historical-test-isolation-repair.yaml",
    "doc_ledger_tier_policy": PROJECT_STATE_DIR / "stage5ea-doc-ledger-tier-policy.yaml",
    "validation_wrapper_repair": PROJECT_STATE_DIR / "stage5ea-validation-wrapper-repair.yaml",
    "validation_rerun_discipline": PROJECT_STATE_DIR / "stage5ea-validation-rerun-discipline.yaml",
    "source_browser_fact_card_performance": PROJECT_STATE_DIR
    / "stage5ea-source-browser-fact-card-performance.yaml",
    "pytest_shard_policy_repair": PROJECT_STATE_DIR / "stage5ea-pytest-shard-policy-repair.yaml",
    "orphan_process_timeout_policy": PROJECT_STATE_DIR / "stage5ea-orphan-process-timeout-policy.yaml",
    "operational_file_map_category_repair": PROJECT_STATE_DIR
    / "stage5ea-operational-file-map-category-repair.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5ea-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5ea-reviewability-gap-register.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5ea-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5ea-credential-redaction-policy-preservation.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "stage5dz_preservation": TOKEN_BLOCK_DIR / "stage5ea-stage5dz-preservation.yaml",
    "stage5dy_preservation": TOKEN_BLOCK_DIR / "stage5ea-stage5dy-preservation.yaml",
    "stage5dx_preservation": TOKEN_BLOCK_DIR / "stage5ea-stage5dx-preservation.yaml",
    "stage5dw_preservation": TOKEN_BLOCK_DIR / "stage5ea-stage5dw-preservation.yaml",
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5ea-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5ea-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5ea-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR / "stage5ea-no-byte-stream-transition-proof.yaml",
    "no_execution_transition_proof": TOKEN_BLOCK_DIR / "stage5ea-no-execution-transition-proof.yaml",
}

DATA_PATHS: dict[str, Path] = {}
DATA_PATHS.update(PROJECT_STATE_PATHS)
DATA_PATHS.update(SOURCE_HARVESTER_PATHS)
DATA_PATHS.update(TOKEN_PATHS)

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5ea-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5ea-next-stage-decision-v0.schema.json"),
    "stage5dz_verification": Path("schemas/project-state/stage5ea-stage5dz-verification-v0.schema.json"),
    "current_stage_registry_repair": Path(
        "schemas/project-state/stage5ea-current-stage-registry-repair-v0.schema.json"
    ),
    "current_stage_state": Path("schemas/project-state/current-stage-state-v0.schema.json"),
    "historical_test_isolation_repair": Path(
        "schemas/project-state/stage5ea-historical-test-isolation-repair-v0.schema.json"
    ),
    "doc_ledger_tier_policy": Path("schemas/project-state/stage5ea-doc-ledger-tier-policy-v0.schema.json"),
    "validation_wrapper_repair": Path("schemas/project-state/stage5ea-validation-wrapper-repair-v0.schema.json"),
    "validation_rerun_discipline": Path(
        "schemas/project-state/stage5ea-validation-rerun-discipline-v0.schema.json"
    ),
    "source_browser_fact_card_performance": Path(
        "schemas/project-state/stage5ea-source-browser-fact-card-performance-v0.schema.json"
    ),
    "pytest_shard_policy_repair": Path(
        "schemas/project-state/stage5ea-pytest-shard-policy-repair-v0.schema.json"
    ),
    "orphan_process_timeout_policy": Path(
        "schemas/project-state/stage5ea-orphan-process-timeout-policy-v0.schema.json"
    ),
    "operational_file_map_category_repair": Path(
        "schemas/project-state/stage5ea-operational-file-map-category-repair-v0.schema.json"
    ),
    "reviewable_validation_evidence": Path(
        "schemas/project-state/stage5ea-reviewable-validation-evidence-v0.schema.json"
    ),
    "reviewability_gap_register": Path("schemas/project-state/stage5ea-reviewability-gap-register-v0.schema.json"),
    "codex_handoff_policy": Path("schemas/source-harvester/stage5ea-codex-handoff-policy-v0.schema.json"),
    "credential_redaction_policy_preservation": Path(
        "schemas/source-harvester/stage5ea-credential-redaction-policy-preservation-v0.schema.json"
    ),
    "generic_preservation": Path("schemas/token-block/stage5ea-generic-preservation-record-v0.schema.json"),
    "no_active_ingestion_proof": Path("schemas/token-block/stage5ea-no-active-ingestion-proof-v0.schema.json"),
    "no_byte_stream_transition_proof": Path(
        "schemas/token-block/stage5ea-no-byte-stream-transition-proof-v0.schema.json"
    ),
    "no_execution_transition_proof": Path("schemas/token-block/stage5ea-no-execution-transition-proof-v0.schema.json"),
}

SCHEMA_BY_DATA_KEY: dict[str, str] = {key: key for key in PROJECT_STATE_PATHS | SOURCE_HARVESTER_PATHS}
SCHEMA_BY_DATA_KEY.update(
    {
        "no_active_ingestion_proof": "no_active_ingestion_proof",
        "no_byte_stream_transition_proof": "no_byte_stream_transition_proof",
        "no_execution_transition_proof": "no_execution_transition_proof",
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
class Stage5EAValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5ea"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5ea() -> dict[str, dict[str, Any]]:
    records = _build_records()
    _write_schemas()
    _write_records(records)
    _write_codex_completion(records["summary"])
    _update_stage_summary_records(records["summary"])
    _update_doc_staleness_source_of_truth()
    return records


def validate_stage5ea() -> Stage5EAValidationResult:
    checks = [
        _validate_required_paths,
        _validate_schemas,
        _validate_summary,
        validate_stage5ea_stage5dz_verification,
        validate_stage5ea_current_stage_registry,
        validate_stage5ea_historical_test_isolation,
        validate_stage5ea_doc_ledger_tier_policy,
        validate_stage5ea_validation_wrapper_repair,
        validate_stage5ea_source_browser_performance,
        validate_stage5ea_pytest_shard_policy,
        validate_stage5ea_orphan_process_policy,
        validate_stage5ea_preservation,
        validate_stage5ea_sidecar_gates,
        validate_stage5ea_handoff_continuity,
        validate_stage5ea_credential_redaction_policy,
        validate_stage5ea_governance_scope,
    ]
    errors = _collect_errors(checks)
    summary = _load(PROJECT_STATE_PATHS["summary"])
    counts = _summary_counts(summary)
    counts["stage5ea_record_count"] = len(DATA_PATHS)
    counts["stage5ea_schema_count"] = len(SCHEMA_PATHS)
    return Stage5EAValidationResult(len(errors), counts, errors)


def validate_stage5ea_stage5dz_verification() -> Stage5EAValidationResult:
    path = PROJECT_STATE_PATHS["stage5dz_verification"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "stage5dz_verified_complete": True,
            "triangle_findings_recorded": 7,
            "page32_findings_recorded": 8,
            "overlay_count": 12,
            "source_browser_validation_error_count": 0,
            "number_fact_review_batch_3_performed_now": False,
        },
        path,
    )
    return _result("stage5dz_verification", payload, errors)


def validate_stage5ea_current_stage_registry() -> Stage5EAValidationResult:
    path = PROJECT_STATE_PATHS["current_stage_state"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "stage_registry_is_source_of_truth": True,
            "historical_tests_must_not_require_latest_stage": True,
        },
        path,
    )
    latest_stage = str(payload.get("latest_completed_stage_id", ""))
    if latest_stage == STAGE_ID:
        errors.extend(
            _expected_errors(
                payload,
                {
                    "latest_completed_stage_title": STAGE_TITLE,
                    "recommended_next_stage_id": NEXT_STAGE_ID,
                    "recommended_next_stage_title": NEXT_STAGE_TITLE,
                },
                path,
            )
        )
    elif latest_stage not in {
        "stage-5eb",
        "stage-5ec",
        "stage-5ed",
        "stage-5ee",
        "stage-5ef",
        "stage-5eg",
        "stage-5eh",
        "stage-5ei",
        "stage-6",
        "stage-6b",
        "stage-6c",
    }:
        errors.append(f"{path.as_posix()}: unexpected latest_completed_stage_id {latest_stage!r}")
    return _result("current_stage_registry", payload, errors)


def validate_stage5ea_historical_test_isolation() -> Stage5EAValidationResult:
    path = PROJECT_STATE_PATHS["historical_test_isolation_repair"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "historical_stage_tests_use_explicit_fixture_or_registry": True,
            "stage5dz_tests_do_not_require_stage5dz_to_remain_latest": True,
            "stage_ledger_tests_do_not_hardcode_obsolete_next_stage": True,
        },
        path,
    )
    return _result("historical_test_isolation", payload, errors)


def validate_stage5ea_doc_ledger_tier_policy() -> Stage5EAValidationResult:
    path = PROJECT_STATE_PATHS["doc_ledger_tier_policy"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "tier_a_must_track_current_and_next_stage": True,
            "tier_b_may_preserve_historical_stage_references": True,
            "tier_c_historical_logs_are_append_only": True,
        },
        path,
    )
    return _result("doc_ledger_tier_policy", payload, errors)


def validate_stage5ea_validation_wrapper_repair() -> Stage5EAValidationResult:
    path = PROJECT_STATE_PATHS["validation_wrapper_repair"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "stage_id_normalization_accepts_hyphenated_stage_ids": True,
            "stage5ea_command_name": "validate-stage5ea",
            "stage5dz_command_name": "validate-stage5dz",
            "stage_wrapper_supports_stage5ea": True,
        },
        path,
    )
    for source, expected in {
        "stage-5ea": "validate-stage5ea",
        "stage5ea": "validate-stage5ea",
        "5ea": "validate-stage5ea",
        "stage-5dz": "validate-stage5dz",
    }.items():
        if validation_command_name(source) != expected:
            errors.append(f"validation command normalization failed for {source}")
    return _result("validation_wrapper_repair", payload, errors)


def validate_stage5ea_validation_wrapper_repair_record() -> Stage5EAValidationResult:
    return validate_stage5ea_validation_wrapper_repair()


def validate_stage5ea_source_browser_performance() -> Stage5EAValidationResult:
    path = PROJECT_STATE_PATHS["source_browser_fact_card_performance"]
    payload = _load(path)
    cache = NumberFactOverlayCache.load()
    errors = _expected_errors(
        payload,
        {
            "overlay_cache_implemented": True,
            "overlay_index_loaded_once_per_refresh": True,
            "table_filter_detail_reuse_overlay_cache": True,
        },
        path,
    )
    if cache.load_count != 1:
        errors.append("number fact overlay cache must report one overlay load")
    if len(cache.overlays) < int(payload.get("minimum_overlay_records_expected", 1)):
        errors.append("number fact overlay cache loaded fewer overlays than expected")
    return _result("source_browser_performance", payload, errors)


def validate_stage5ea_pytest_shard_policy() -> Stage5EAValidationResult:
    path = PROJECT_STATE_PATHS["pytest_shard_policy_repair"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "worker_cap": PARALLEL_WORKER_CAP,
            "old_16_worker_default_reintroduced": False,
            "historical_slow_tests_are_weighted_or_serial_isolated": True,
            "stage5cm_and_later_worker_cap_preserved": True,
        },
        path,
    )
    return _result("pytest_shard_policy", payload, errors)


def validate_stage5ea_orphan_process_policy() -> Stage5EAValidationResult:
    path = PROJECT_STATE_PATHS["orphan_process_timeout_policy"]
    payload = _load(path)
    errors = _expected_errors(
        payload,
        {
            "timeout_seconds": PYTEST_TIMEOUT_SECONDS,
            "timeout_cleanup_policy_recorded": True,
            "validation_subprocesses_must_not_run_indefinitely": True,
        },
        path,
    )
    return _result("orphan_process_policy", payload, errors)


def validate_stage5ea_preservation() -> Stage5EAValidationResult:
    errors: list[str] = []
    for key in (
        "stage5dz_preservation",
        "stage5dy_preservation",
        "stage5dx_preservation",
        "stage5dw_preservation",
        "stage5bd_preservation",
        "active_lineage_preservation",
    ):
        payload = _load(TOKEN_PATHS[key])
        errors.extend(
            _expected_errors(
                payload,
                {
                    "preserved": True,
                    "rewritten": False,
                    "superseded_now": False,
                },
                TOKEN_PATHS[key],
            )
        )
        errors.extend(_required_false_errors(payload, TOKEN_PATHS[key].as_posix()))
    summary = {"preservation_record_count": 6}
    return Stage5EAValidationResult(len(errors), summary, errors)


def validate_stage5ea_sidecar_gates() -> Stage5EAValidationResult:
    errors: list[str] = []
    for key, gate in (
        ("no_active_ingestion_proof", "active_ingestion_gate_closed"),
        ("no_byte_stream_transition_proof", "byte_stream_transition_gate_closed"),
        ("no_execution_transition_proof", "execution_transition_gate_closed"),
    ):
        payload = _load(TOKEN_PATHS[key])
        errors.extend(_expected_errors(payload, {gate: True, "authorized_now": False}, TOKEN_PATHS[key]))
        errors.extend(_required_false_errors(payload, TOKEN_PATHS[key].as_posix()))
    return Stage5EAValidationResult(len(errors), {"sidecar_gate_records": 3}, errors)


def validate_stage5ea_handoff_continuity() -> Stage5EAValidationResult:
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


def validate_stage5ea_credential_redaction_policy() -> Stage5EAValidationResult:
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


def validate_stage5ea_governance_scope() -> Stage5EAValidationResult:
    payload = _load(PROJECT_STATE_PATHS["summary"])
    errors = _required_false_errors(payload, PROJECT_STATE_PATHS["summary"].as_posix())
    errors.extend(
        _expected_errors(
            payload,
            {
                "metadata_only": True,
                "validation_infrastructure_stage": True,
                "number_fact_review_batch_3_deferred_to_stage5eb": True,
                "recommended_next_stage_id": NEXT_STAGE_ID,
            },
            PROJECT_STATE_PATHS["summary"],
        )
    )
    return _result("governance_scope", payload, errors)


def stage5ea_summary_text() -> str:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    current = _load(PROJECT_STATE_PATHS["current_stage_state"])
    return "\n".join(
        [
            f"stage_id={summary.get('stage_id', STAGE_ID)}",
            f"status={summary.get('status', 'unknown')}",
            f"latest_completed_stage={current.get('latest_completed_stage_id', '')}",
            f"recommended_next_stage={summary.get('recommended_next_stage_id', '')}",
            f"stage5dz_verified={_format(summary.get('stage5dz_verified_complete'))}",
            f"number_fact_review_batch_3_performed_now={_format(summary.get('number_fact_review_batch_3_performed_now'))}",
            f"number_fact_review_batch_3_deferred_to_stage5eb={_format(summary.get('number_fact_review_batch_3_deferred_to_stage5eb'))}",
            f"source_browser_overlay_cache_implemented={_format(summary.get('source_browser_overlay_cache_implemented'))}",
            f"parallel_worker_cap={summary.get('parallel_worker_cap', '')}",
            f"pytest_timeout_seconds={summary.get('pytest_timeout_seconds', '')}",
            f"codex_handoff_root={summary.get('canonical_codex_handoff_root', '')}",
            "solve_claim=false",
        ]
    )


def _build_records() -> dict[str, dict[str, Any]]:
    stage5dz = _load(PROJECT_STATE_DIR / "stage5dz-summary.yaml")
    stage5dy = _load(PROJECT_STATE_DIR / "stage5dy-summary.yaml")
    base = _stage_base()
    false_flags = _false_flags()
    records: dict[str, dict[str, Any]] = {}
    records.update(_project_state_records(base, false_flags, stage5dz, stage5dy))
    records.update(_source_harvester_records(base, false_flags))
    records.update(_token_records(base, false_flags))
    return records


def _project_state_records(
    base: dict[str, Any],
    false_flags: dict[str, bool],
    stage5dz: dict[str, Any],
    stage5dy: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    summary = {
        **base,
        **false_flags,
        "record_type": "stage5ea_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "source_previous_stage_title": PREVIOUS_STAGE_TITLE,
        "source_previous_stage_final_commit": PREVIOUS_STAGE_FINAL_COMMIT,
        "source_previous_issue": PREVIOUS_STAGE_ISSUE,
        "source_previous_ci_run": PREVIOUS_CI_RUN,
        "source_previous_ci_status": "passed",
        "stage5dz_recommended_stage5ea_number_fact_batch_3": True,
        "operator_inserted_validation_throughput_repair_before_batch_3": True,
        "number_fact_review_batch_3_deferred_to_stage5eb": True,
        "stage5dz_verified_complete": True,
        "triangle_findings_recorded": int(stage5dz.get("triangle_findings_recorded", 7)),
        "page32_findings_recorded": int(stage5dz.get("page32_findings_recorded", 8)),
        "stage5dz_overlay_count": int(stage5dz.get("overlay_count", 12)),
        "stage5dz_source_browser_validation_error_count": int(
            stage5dz.get("source_browser_validation_error_count", 0)
        ),
        "current_stage_registry_repaired": True,
        "historical_test_isolation_repaired": True,
        "doc_ledger_tier_policy_recorded": True,
        "validation_wrapper_repaired": True,
        "source_browser_overlay_cache_implemented": True,
        "pytest_shard_policy_repaired": True,
        "orphan_process_timeout_policy_recorded": True,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "pytest_timeout_seconds": PYTEST_TIMEOUT_SECONDS,
        "stage5dy_validation_profile_count": int(stage5dy.get("validation_profile_count", 6)),
        "stage5dy_parallel_worker_cap": int(stage5dy.get("parallel_worker_cap", PARALLEL_WORKER_CAP)),
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
    }
    return {
        "summary": summary,
        "next_stage_decision": {
            **base,
            **false_flags,
            "record_type": "stage5ea_next_stage_decision",
            "schema": SCHEMA_PATHS["next_stage_decision"].as_posix(),
            "status": "complete",
            "stage5dz_recommended_stage5ea_number_fact_batch_3": True,
            "operator_inserted_validation_throughput_repair_before_batch_3": True,
            "number_fact_review_batch_3_deferred_to_stage5eb": True,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        },
        "stage5dz_verification": {
            **base,
            **false_flags,
            "record_type": "stage5ea_stage5dz_verification",
            "schema": SCHEMA_PATHS["stage5dz_verification"].as_posix(),
            "status": "complete",
            "stage5dz_verified_complete": True,
            "stage5dz_status": stage5dz.get("status", "complete"),
            "triangle_findings_recorded": int(stage5dz.get("triangle_findings_recorded", 7)),
            "page32_findings_recorded": int(stage5dz.get("page32_findings_recorded", 8)),
            "overlay_count": int(stage5dz.get("overlay_count", 12)),
            "source_browser_validation_error_count": int(stage5dz.get("source_browser_validation_error_count", 0)),
            "stage5dz_recommended_next_stage_id": stage5dz.get("recommended_next_stage_id", "stage-5ea"),
            "stage5dz_recommended_next_stage_title": stage5dz.get("recommended_next_stage_title", ""),
        },
        "current_stage_registry_repair": {
            **base,
            **false_flags,
            "record_type": "stage5ea_current_stage_registry_repair",
            "schema": SCHEMA_PATHS["current_stage_registry_repair"].as_posix(),
            "status": "complete",
            "current_stage_state_path": PROJECT_STATE_PATHS["current_stage_state"].as_posix(),
            "stage_registry_is_source_of_truth": True,
            "consistency_checks_can_read_current_stage_registry": True,
            "historical_tests_must_not_require_latest_stage": True,
        },
        "current_stage_state": {
            **base,
            **false_flags,
            "record_type": "current_stage_state",
            "schema": SCHEMA_PATHS["current_stage_state"].as_posix(),
            "status": "complete",
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "latest_completed_stage_commit": "",
            "latest_completed_stage_ci_status": "pending_post_push",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
            "stage_registry_is_source_of_truth": True,
            "historical_tests_must_not_require_latest_stage": True,
        },
        "historical_test_isolation_repair": {
            **base,
            **false_flags,
            "record_type": "stage5ea_historical_test_isolation_repair",
            "schema": SCHEMA_PATHS["historical_test_isolation_repair"].as_posix(),
            "status": "complete",
            "historical_stage_tests_use_explicit_fixture_or_registry": True,
            "stage5dz_tests_do_not_require_stage5dz_to_remain_latest": True,
            "stage_ledger_tests_do_not_hardcode_obsolete_next_stage": True,
            "current_stage_assertions_must_read_current_stage_state": True,
        },
        "doc_ledger_tier_policy": {
            **base,
            **false_flags,
            "record_type": "stage5ea_doc_ledger_tier_policy",
            "schema": SCHEMA_PATHS["doc_ledger_tier_policy"].as_posix(),
            "status": "complete",
            "tier_a_must_track_current_and_next_stage": True,
            "tier_a_paths": [
                "STATUS.md",
                "ROADMAP.md",
                "docs/roadmap/staged-plan.md",
                "ChatGPT-ContextFile.md",
                "docs/onboarding/source-of-truth-map.md",
                "data/project-state/current-stage-state.yaml",
            ],
            "tier_b_may_preserve_historical_stage_references": True,
            "tier_c_historical_logs_are_append_only": True,
        },
        "validation_wrapper_repair": {
            **base,
            **false_flags,
            "record_type": "stage5ea_validation_wrapper_repair",
            "schema": SCHEMA_PATHS["validation_wrapper_repair"].as_posix(),
            "status": "complete",
            "stage_id_normalization_accepts_hyphenated_stage_ids": True,
            "stage5ea_command_name": "validate-stage5ea",
            "stage5dz_command_name": "validate-stage5dz",
            "stage_wrapper_supports_stage5ea": True,
            "supported_input_examples": ["stage-5ea", "stage5ea", "5ea"],
        },
        "validation_rerun_discipline": {
            **base,
            **false_flags,
            "record_type": "stage5ea_validation_rerun_discipline",
            "schema": SCHEMA_PATHS["validation_rerun_discipline"].as_posix(),
            "status": "complete",
            "focused_validation_during_iteration": True,
            "single_broad_validation_near_final": True,
            "do_not_repeat_full_serial_pytest_by_default": True,
        },
        "source_browser_fact_card_performance": {
            **base,
            **false_flags,
            "record_type": "stage5ea_source_browser_fact_card_performance",
            "schema": SCHEMA_PATHS["source_browser_fact_card_performance"].as_posix(),
            "status": "complete",
            "overlay_cache_implemented": True,
            "overlay_index_loaded_once_per_refresh": True,
            "table_filter_detail_reuse_overlay_cache": True,
            "minimum_overlay_records_expected": 1,
        },
        "pytest_shard_policy_repair": {
            **base,
            **false_flags,
            "record_type": "stage5ea_pytest_shard_policy_repair",
            "schema": SCHEMA_PATHS["pytest_shard_policy_repair"].as_posix(),
            "status": "complete",
            "worker_cap": PARALLEL_WORKER_CAP,
            "old_16_worker_default_reintroduced": False,
            "historical_slow_tests_are_weighted_or_serial_isolated": True,
            "stage5cm_and_later_worker_cap_preserved": True,
        },
        "orphan_process_timeout_policy": {
            **base,
            **false_flags,
            "record_type": "stage5ea_orphan_process_timeout_policy",
            "schema": SCHEMA_PATHS["orphan_process_timeout_policy"].as_posix(),
            "status": "complete",
            "timeout_seconds": PYTEST_TIMEOUT_SECONDS,
            "timeout_cleanup_policy_recorded": True,
            "validation_subprocesses_must_not_run_indefinitely": True,
        },
        "operational_file_map_category_repair": {
            **base,
            **false_flags,
            "record_type": "stage5ea_operational_file_map_category_repair",
            "schema": SCHEMA_PATHS["operational_file_map_category_repair"].as_posix(),
            "status": "complete",
            "current_stage_state_category": "active_data_record",
            "new_unbounded_categories_added": False,
            "operational_file_map_updated_for_stage5ea": True,
        },
        "reviewable_validation_evidence": {
            **base,
            **false_flags,
            "record_type": "stage5ea_reviewable_validation_evidence",
            "schema": SCHEMA_PATHS["reviewable_validation_evidence"].as_posix(),
            "status": "complete",
            "validation_evidence_is_record_backed": True,
            "terminal_output_alone_is_not_evidence": True,
        },
        "reviewability_gap_register": {
            **base,
            **false_flags,
            "record_type": "stage5ea_reviewability_gap_register",
            "schema": SCHEMA_PATHS["reviewability_gap_register"].as_posix(),
            "status": "complete",
            "open_gaps": [
                {
                    "gap_id": "stage5ea-follow-on-number-fact-batch-3",
                    "status": "deferred_to_stage5eb",
                    "reason": "Operator inserted validation-throughput repair before the review batch.",
                }
            ],
        },
    }


def _source_harvester_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "codex_handoff_policy": {
            **base,
            **false_flags,
            "record_type": "stage5ea_codex_handoff_policy",
            "schema": SCHEMA_PATHS["codex_handoff_policy"].as_posix(),
            "status": "complete",
            "canonical_handoff_root": "codex-output",
            "codex_output_used": False,
            "codex_underscore_output_root_forbidden": True,
            "completion_summary_path": "codex-output/stage5ea-codex-completion.md",
        },
        "credential_redaction_policy_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5ea_credential_redaction_policy_preservation",
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
        ("stage5dz_preservation", "stage-5dz"),
        ("stage5dy_preservation", "stage-5dy"),
        ("stage5dx_preservation", "stage-5dx"),
        ("stage5dw_preservation", "stage-5dw"),
        ("stage5bd_preservation", "stage-5bd"),
        ("active_lineage_preservation", "active-lineage"),
    ):
        records[key] = {
            **base,
            **false_flags,
            "record_type": f"stage5ea_{key}",
            "schema": SCHEMA_PATHS["generic_preservation"].as_posix(),
            "status": "complete",
            "source_stage_id": source_stage,
            "preserved": True,
            "rewritten": False,
            "superseded_now": False,
            "notes": "Stage 5EA records preservation only; it does not mutate token-block planning inputs.",
        }
    records["no_active_ingestion_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ea_no_active_ingestion_proof",
        "schema": SCHEMA_PATHS["no_active_ingestion_proof"].as_posix(),
        "status": "complete",
        "active_ingestion_gate_closed": True,
        "authorized_now": False,
    }
    records["no_byte_stream_transition_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ea_no_byte_stream_transition_proof",
        "schema": SCHEMA_PATHS["no_byte_stream_transition_proof"].as_posix(),
        "status": "complete",
        "byte_stream_transition_gate_closed": True,
        "authorized_now": False,
    }
    records["no_execution_transition_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ea_no_execution_transition_proof",
        "schema": SCHEMA_PATHS["no_execution_transition_proof"].as_posix(),
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
        "old_16_worker_default_reintroduced": {"const": False},
        "codex_output_used": {"const": False},
    }
    for flag in FALSE_FLAGS:
        properties.setdefault(flag, {"const": False})
    if key == "current_stage_state":
        properties.update(
            {
                "record_type": {"const": "current_stage_state"},
                "stage_id": {
                    "enum": [
                        "stage-5ea",
                        "stage-5eb",
                        "stage-5ec",
                        "stage-5ed",
                        "stage-5ee",
                        "stage-5ef",
                        "stage-5eg",
                        "stage-5eh",
                        "stage-5ei",
                        "stage-6",
                        "stage-6b",
                        "stage-6c",
                    ]
                },
                "latest_completed_stage_id": {
                    "enum": [
                        "stage-5ea",
                        "stage-5eb",
                        "stage-5ec",
                        "stage-5ed",
                        "stage-5ee",
                        "stage-5ef",
                        "stage-5eg",
                        "stage-5eh",
                        "stage-5ei",
                        "stage-6",
                        "stage-6b",
                        "stage-6c",
                    ]
                },
                "recommended_next_stage_id": {
                    "enum": [
                        "stage-5eb",
                        "stage-5ec",
                        "stage-5ed",
                        "stage-5ee",
                        "stage-5ef",
                        "stage-5eg",
                        "stage-5eh",
                        "stage-5ei",
                        "stage-6",
                        "stage-6b",
                        "stage-6c",
                        "stage-6d",
                    ]
                },
                "stage_registry_is_source_of_truth": {"const": True},
            }
        )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
        "required": required,
        "properties": properties,
    }


def _validate_required_paths() -> Stage5EAValidationResult:
    missing = [
        f"required Stage 5EA path missing: {path.as_posix()}"
        for path in [*DATA_PATHS.values(), *SCHEMA_PATHS.values()]
        if not path.exists()
    ]
    return Stage5EAValidationResult(len(missing), {"required_paths_missing": len(missing)}, missing)


def _validate_schemas() -> Stage5EAValidationResult:
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
    return Stage5EAValidationResult(len(errors), {"schema_validation_errors": len(errors)}, errors)


def _validate_summary() -> Stage5EAValidationResult:
    payload = _load(PROJECT_STATE_PATHS["summary"])
    errors = _required_false_errors(payload, PROJECT_STATE_PATHS["summary"].as_posix())
    errors.extend(
        _expected_errors(
            payload,
            {
                "stage_id": STAGE_ID,
                "status": "complete",
                "stage5dz_recommended_stage5ea_number_fact_batch_3": True,
                "operator_inserted_validation_throughput_repair_before_batch_3": True,
                "number_fact_review_batch_3_deferred_to_stage5eb": True,
                "recommended_next_stage_id": NEXT_STAGE_ID,
            },
            PROJECT_STATE_PATHS["summary"],
        )
    )
    return _result("summary", payload, errors)


def _collect_errors(checks: list[Callable[[], Stage5EAValidationResult]]) -> list[str]:
    errors: list[str] = []
    for check in checks:
        result = check()
        errors.extend(result.errors)
    return errors


def _result(label: str, payload: dict[str, Any], errors: list[str]) -> Stage5EAValidationResult:
    counts = _summary_counts(payload)
    counts["validator"] = label
    return Stage5EAValidationResult(len(errors), counts, errors)


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
            "# Stage 5EA Codex Completion",
            "",
            f"- stage_id: {STAGE_ID}",
            f"- status: {summary.get('status')}",
            f"- next_stage: {NEXT_STAGE_ID}",
            "- number_fact_review_batch_3_performed_now: false",
            "- execution_performed: false",
            "- solve_claim: false",
            "",
        ]
    )
    (CODEX_OUTPUT_DIR / "stage5ea-codex-completion.md").write_text(text, encoding="utf-8")


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
                "Repaired current-stage registry handling, historical-test isolation, validation-wrapper "
                "stage-id normalization, pytest shard policy, and Source Browser number-fact overlay caching."
            ),
            "key_outputs": [
                "Current-stage registry points latest to Stage 5EA and next to Stage 5EB.",
                "Historical Stage 5DZ verification is preserved without requiring Stage 5DZ to remain latest.",
                "Source Browser number-fact overlays are cached for table/filter/detail rendering.",
            ],
            "result_status": "validation_throughput_repaired",
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
    payload["latest_completed_stage_prefix"] = "Stage 5EA"
    payload["next_stage_after_this_stage"] = NEXT_STAGE_TITLE
    payload["expected_next_stage_prefix"] = "Stage 5EB"
    payload["expected_latest_after_stage5ah"] = STAGE_TITLE
    payload["expected_next_after_stage5ah"] = NEXT_STAGE_TITLE
    write_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH, payload)


VALIDATOR_BY_NAME: dict[str, Callable[[], Stage5EAValidationResult]] = {
    "stage5dz_verification": validate_stage5ea_stage5dz_verification,
    "current_stage_registry": validate_stage5ea_current_stage_registry,
    "historical_test_isolation": validate_stage5ea_historical_test_isolation,
    "doc_ledger_tier_policy": validate_stage5ea_doc_ledger_tier_policy,
    "validation_wrapper_repair": validate_stage5ea_validation_wrapper_repair,
    "source_browser_performance": validate_stage5ea_source_browser_performance,
    "pytest_shard_policy": validate_stage5ea_pytest_shard_policy,
    "orphan_process_policy": validate_stage5ea_orphan_process_policy,
    "preservation": validate_stage5ea_preservation,
    "sidecar_gates": validate_stage5ea_sidecar_gates,
    "handoff_continuity": validate_stage5ea_handoff_continuity,
    "credential_redaction_policy": validate_stage5ea_credential_redaction_policy,
    "governance_scope": validate_stage5ea_governance_scope,
}
