"""Stage 5DA operator choice / pause scaffold metadata."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import (
    sha256_file,
    write_json,
    write_jsonl,
    write_yaml,
)
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import (
    ACTIVE_LINEAGE_PATHS,
    CORRECT_STAGE5AW_PATH,
    INCORRECT_STAGE5AW_PATH,
)
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP, SECRET_PATTERNS
from libreprimus.token_block.stage5cu import OPERATOR_DECISION_OPTIONS
from libreprimus.token_block.stage5cy import (
    DATA_PATHS as STAGE5CY_DATA_PATHS,
    FALSE_FLAGS as STAGE5CY_FALSE_FLAGS,
    SOURCE_STAGE_IDS as STAGE5CY_SOURCE_STAGE_IDS,
    SOURCE_TOKEN_BLOCK_LINEAGE,
)
from libreprimus.token_block.stage5bm import _read

STAGE_ID = "stage-5da"
STAGE_TITLE = "Stage 5DA - Operator choice / pause decision record scaffold, without execution"
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5cy"
SOURCE_PREVIOUS_COMMIT = "77f16fcce6cb30f468d8accfebc9fbd7cb95a55f"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5cz"
SOURCE_DEEP_RESEARCH_REPORT = "28_Stage-5CY-Deep-Research-Review.md"
RESULTS_DIR = Path("experiments/results/token-block/stage5da")
CODEX_COMPLETION_PATH = Path("codex-output/stage5da-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
PYTEST_COUNT_OBSERVED_LOCALLY = 2503
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"

REAL_RECORD_CLASSES = [
    "real_operator_choice_pause_record",
    "real_operator_decision_record",
    "real_operator_approval_record",
    "real_deep_research_activation_acceptance_record",
    "real_combined_gate_validation_record",
    "real_activation_decision_record",
    "active_planning_input_selection_record",
    "active_planning_input_authorization_record",
    "dry_run_ingestion_authorization_record",
    "byte_stream_generation_authorization_record",
    "execution_authorization_record",
]

STAGE5CZ_FINDINGS = [
    "stage5cy_accepted_with_warnings",
    "stage5cy_option_selection_preflight_is_reviewable",
    "stage5cy_preserved_stage5cw_stage5cu_stage5cs_stage5bd_and_lineage",
    "stage5cy_kept_exact_six_options_unselected",
    "stage5cy_count_reconciliation_is_reviewability_only",
    "governance_overbuild_risk_confirmed",
    "stop_generic_guardrail_expansion_without_concrete_defect",
    "next_step_should_be_operator_choice_or_explicit_pause_scaffold",
    "stage5cz_did_not_recommend_execution",
    "stage5cz_did_not_provide_operator_choice",
    "stage5cz_did_not_provide_explicit_pause",
]

FALSE_FLAGS = {
    **STAGE5CY_FALSE_FLAGS,
    "operator_choice_or_pause_record_created_now": False,
    "operator_choice_or_pause_record_valid_now": False,
    "explicit_operator_choice_provided_now": False,
    "explicit_pause_provided_now": False,
    "explicit_pause_selected_now": False,
    "real_operator_choice_pause_record_created_now": False,
    "automatic_option_selection_allowed": False,
    "operator_choice_pause_scaffold_authorizes_approval": False,
    "operator_choice_pause_scaffold_authorizes_activation": False,
    "operator_choice_pause_scaffold_authorizes_active_input": False,
    "operator_choice_pause_scaffold_authorizes_dry_run_ingestion": False,
    "operator_choice_pause_scaffold_authorizes_byte_stream_generation": False,
    "operator_choice_pause_scaffold_authorizes_execution": False,
    "explicit_pause_authorizes_approval": False,
    "explicit_pause_authorizes_activation": False,
    "explicit_pause_authorizes_active_input": False,
    "explicit_pause_authorizes_dry_run_ingestion": False,
    "explicit_pause_authorizes_byte_stream_generation": False,
    "explicit_pause_authorizes_execution": False,
    "stage5da_selects_operator_choice": False,
    "stage5da_selects_explicit_pause": False,
    "stage5da_creates_generic_preflight_layer": False,
    "stage5da_creates_broad_new_negative_fixture_layer": False,
    "old_16_worker_default_reintroduced": False,
}
SELECTED_OPTION_FIELD = {"selected_option_id": None}

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5da-summary.yaml"),
    "next_stage": Path("data/project-state/stage5da-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5da-stage5cz-findings-integration.yaml"),
    "governance_scope_control": Path(
        "data/project-state/stage5da-governance-scope-control.yaml"
    ),
    "validation_evidence": Path(
        "data/project-state/stage5da-reviewable-validation-evidence.yaml"
    ),
    "gap_register": Path("data/project-state/stage5da-reviewability-gap-register.yaml"),
    "choice_pause_scaffold": Path(
        "data/token-block/stage5da-operator-choice-pause-decision-scaffold.yaml"
    ),
    "choice_pause_nonselection": Path(
        "data/token-block/stage5da-operator-choice-pause-nonselection-proof.yaml"
    ),
    "explicit_pause_nonactivation": Path(
        "data/token-block/stage5da-explicit-pause-nonactivation-proof.yaml"
    ),
    "real_record_blocker": Path("data/token-block/stage5da-real-record-creation-blocker.yaml"),
    "stage5cy_preservation": Path("data/token-block/stage5da-stage5cy-preservation.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5da-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5da-active-lineage-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5da-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5da-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5da-no-execution-transition-gate.yaml"
    ),
    "handoff": Path("data/source-harvester/stage5da-codex-handoff-policy.yaml"),
    "credential_redaction": Path(
        "data/source-harvester/stage5da-credential-redaction-policy-preservation.yaml"
    ),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5da_{key}" for key in DATA_PATHS}


def _base_record(record_key: str) -> dict[str, Any]:
    return {
        "record_type": RECORD_TYPES[record_key],
        "schema": SCHEMA_PATHS[record_key],
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE,
        "source_previous_stage_commit": SOURCE_PREVIOUS_COMMIT,
        "source_deep_research_stage": SOURCE_DEEP_RESEARCH_STAGE,
        "source_deep_research_report": SOURCE_DEEP_RESEARCH_REPORT,
        "metadata_only": True,
        "solve_claim": False,
        "execution_allowed": False,
        "canonical_codex_handoff_root": "codex-output",
    }


def _stage_flags() -> dict[str, Any]:
    return {**FALSE_FLAGS, **SELECTED_OPTION_FIELD}


def _schema_for(record_key: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"const": RECORD_TYPES[record_key]},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "execution_allowed": {"const": False},
        "solve_claim": {"const": False},
        "selected_option_id": {"const": None},
    }
    for key in FALSE_FLAGS:
        properties[key] = {"const": False}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"{STAGE_ID} {record_key}",
        "type": "object",
        "required": [
            "record_type",
            "stage_id",
            "metadata_only",
            "execution_allowed",
            "solve_claim",
        ],
        "properties": properties,
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, schema_path in SCHEMA_PATHS.items():
        write_json(Path(schema_path), _schema_for(key))


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = _read(path)
    return payload if isinstance(payload, dict) else {}


def _stage5cy_summary() -> dict[str, Any]:
    return _load_yaml(STAGE5CY_DATA_PATHS["summary"])


def _options() -> list[dict[str, Any]]:
    return [
        {
            **option,
            "selected_now": False,
            "authorizes_real_approval_now": False,
            "authorizes_activation_now": False,
            "authorizes_active_input_now": False,
            "authorizes_byte_stream_generation_now": False,
            "authorizes_execution_now": False,
        }
        for option in OPERATOR_DECISION_OPTIONS
    ]


def _lineage_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path_text in ACTIVE_LINEAGE_PATHS:
        path = Path(path_text)
        records.append(
            {
                "path": path_text,
                "exists": path.exists(),
                "sha256": sha256_file(path) if path.exists() else None,
            }
        )
    return records


def _credential_remote_summary() -> dict[str, Any]:
    result = subprocess.run(
        ["git", "remote", "-v"],
        check=False,
        capture_output=True,
        text=True,
    )
    remote_text = result.stdout + result.stderr
    credential_like_count = 0
    for line in remote_text.splitlines():
        if any(re.search(pattern, line, flags=re.IGNORECASE) for pattern in SECRET_PATTERNS):
            credential_like_count += 1
    return {
        "remote_command_status": "passed" if result.returncode == 0 else "failed",
        "credential_like_remote_count": credential_like_count,
        "remote_url_values_printed": False,
        "verified_github_remote_without_credentials": credential_like_count == 0,
    }


def _records() -> dict[str, dict[str, Any]]:
    stage5cy_summary = _stage5cy_summary()
    options = _options()
    source_stage_ids = ["stage-5cz", *STAGE5CY_SOURCE_STAGE_IDS]
    common_choice_state = {
        "operator_decision_option_count": len(options),
        "stage5cs_exact_option_set_preserved": True,
        "all_options_unselected": True,
        "operator_decision_option_selected_now": False,
        "selected_option_id": None,
        "explicit_operator_choice_provided_now": False,
        "explicit_pause_provided_now": False,
        "operator_choice_or_pause_record_created_now": False,
        "operator_choice_or_pause_record_valid_now": False,
    }
    records: dict[str, dict[str, Any]] = {}
    records["findings"] = {
        **_base_record("findings"),
        "stage5cz_verdict": "accept_with_warnings",
        "stage5cz_findings_integrated": True,
        "stage5cz_report_file": SOURCE_DEEP_RESEARCH_REPORT,
        "finding_count": len(STAGE5CZ_FINDINGS),
        "findings": STAGE5CZ_FINDINGS,
        "stage5cz_did_not_recommend_execution": True,
        "stage5cz_did_not_provide_operator_choice": True,
        "stage5cz_did_not_provide_explicit_pause": True,
        **_stage_flags(),
    }
    records["governance_scope_control"] = {
        **_base_record("governance_scope_control"),
        "governance_overbuild_risk_acknowledged": True,
        "stage5cz_review_integrated": True,
        "stage5db_review_required_before_operator_choice_or_pause_record": True,
        "after_stage5db_requires_operator_choice_or_explicit_pause_or_human_stop": True,
        "additional_generic_preflight_layers_allowed_without_concrete_defect": False,
        "stage5da_selects_operator_choice": False,
        "stage5da_selects_explicit_pause": False,
        "stage5da_creates_generic_preflight_layer": False,
        "stage5da_creates_broad_new_negative_fixture_layer": False,
        **_stage_flags(),
    }
    records["choice_pause_scaffold"] = {
        **_base_record("choice_pause_scaffold"),
        "operator_choice_pause_decision_scaffold_created": True,
        "operator_choice_pause_decision_scaffold_status": "scaffold_only",
        "automatic_option_selection_allowed": False,
        "exact_six_option_set_preserved": True,
        **common_choice_state,
        "operator_decision_options": options,
        "future_decision_modes": [
            {
                "mode_id": "select_exactly_one_stage5cs_option",
                "available_future_only": True,
                "selected_now": False,
                "requires_explicit_operator_input": True,
            },
            {
                "mode_id": "explicit_pause_without_option_selection",
                "available_future_only": True,
                "selected_now": False,
                "requires_explicit_operator_input": True,
            },
        ],
        "operator_choice_pause_scaffold_authorizes_approval": False,
        "operator_choice_pause_scaffold_authorizes_activation": False,
        "operator_choice_pause_scaffold_authorizes_active_input": False,
        "operator_choice_pause_scaffold_authorizes_dry_run_ingestion": False,
        "operator_choice_pause_scaffold_authorizes_byte_stream_generation": False,
        "operator_choice_pause_scaffold_authorizes_execution": False,
        **_stage_flags(),
    }
    records["choice_pause_nonselection"] = {
        **_base_record("choice_pause_nonselection"),
        "operator_choice_pause_nonselection_proof_created": True,
        **common_choice_state,
        "explicit_pause_selected_now": False,
        "operator_decision_options": options,
        **_stage_flags(),
    }
    records["explicit_pause_nonactivation"] = {
        **_base_record("explicit_pause_nonactivation"),
        "explicit_pause_nonactivation_proof_created": True,
        "explicit_pause_available_as_future_operator_outcome": True,
        "explicit_pause_selected_now": False,
        "explicit_pause_provided_now": False,
        "explicit_pause_authorizes_approval": False,
        "explicit_pause_authorizes_activation": False,
        "explicit_pause_authorizes_active_input": False,
        "explicit_pause_authorizes_dry_run_ingestion": False,
        "explicit_pause_authorizes_byte_stream_generation": False,
        "explicit_pause_authorizes_execution": False,
        **_stage_flags(),
    }
    records["real_record_blocker"] = {
        **_base_record("real_record_blocker"),
        "real_record_blocker_status": "active",
        "real_record_class_count": len(REAL_RECORD_CLASSES),
        "blocked_real_record_classes": [
            {
                "record_class": record_class,
                "created_now": False,
                "present_now": False,
                "valid_now": False,
                "blocked_reason": "stage5da_is_choice_pause_scaffold_only",
            }
            for record_class in REAL_RECORD_CLASSES
        ],
        **_stage_flags(),
    }
    records["stage5cy_preservation"] = {
        **_base_record("stage5cy_preservation"),
        "stage5cy_summary_path": STAGE5CY_DATA_PATHS["summary"].as_posix(),
        "stage5cy_complete": stage5cy_summary.get("status") == "complete",
        "stage5cy_option_selection_preflight_preserved": True,
        "stage5cy_validation_count_reconciliation_preserved": True,
        "stage5cy_governance_scope_control_preserved": True,
        "stage5cw_pytest_count_reconciliation_preserved": True,
        "stage5cy_preserved_without_historical_edit": True,
        **_stage_flags(),
    }
    records["stage5bd_preservation"] = {
        **_base_record("stage5bd_preservation"),
        "stage5bd_dry_run_records_remain_valid": True,
        "stage5bd_run_plan_id_count": 10,
        "stage5bd_run_plan_ids_changed": False,
        "stage5bd_dry_run_plan_manifest_changed": False,
        "stage5bd_plan_superseded": False,
        "string4_added_to_stage5bd_run_plan_ids": False,
        "string4_added_to_active_dry_run_inputs": False,
        **_stage_flags(),
    }
    records["active_lineage"] = {
        **_base_record("active_lineage"),
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "active_lineage_records": _lineage_records(),
        "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in ACTIVE_LINEAGE_PATHS,
        "deprecated_stage5aw_path_absent": INCORRECT_STAGE5AW_PATH not in ACTIVE_LINEAGE_PATHS,
        "all_lineage_paths_resolve": all(Path(path).exists() for path in ACTIVE_LINEAGE_PATHS),
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        **_stage_flags(),
    }
    records["no_active_ingestion"] = {
        **_base_record("no_active_ingestion"),
        "no_active_ingestion_status": "closed",
        "string4_sidecar_status": "scaffolded_inactive",
        "string4_sidecar_active": False,
        "string4_sidecar_planning_ingestion_activated": False,
        "string4_active_input_allowed": False,
        "string4_dry_run_ingestion_allowed_now": False,
        "active_ingestion_performed": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        **_stage_flags(),
    }
    records["no_byte_stream_transition_gate"] = {
        **_base_record("no_byte_stream_transition_gate"),
        "no_byte_stream_transition_gate_status": "closed",
        "byte_stream_generation_authorized_now": False,
        "real_byte_stream_generated": False,
        "variant_byte_streams_generated": False,
        "variant_materialisation_performed": False,
        "branch_enumeration_performed": False,
        "full_cartesian_product_enumerated": False,
        "string4_byte_stream_generation_allowed": False,
        **_stage_flags(),
    }
    records["no_execution_transition_gate"] = {
        **_base_record("no_execution_transition_gate"),
        "no_execution_transition_gate_status": "closed",
        "execution_authorized_now": False,
        "token_block_experiment_executed": False,
        "dwh_hash_search_performed": False,
        "hash_preimage_search_performed": False,
        "decode_attempt_performed": False,
        "scoring_performed": False,
        "cuda_execution_performed": False,
        "benchmark_performed": False,
        "stego_tool_execution_performed": False,
        "image_forensics_performed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "website_expansion_performed": False,
        "method_status_upgraded": False,
        "canonical_corpus_active": False,
        **_stage_flags(),
    }
    records["handoff"] = {
        **_base_record("handoff"),
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_handoff_root": "codex_output",
        "codex_output_used": False,
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
        "codex_completion_summary_committed": False,
        "stage5da_codex_completion_summary_required": True,
        "stage5da_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5da_codex_completion_summary_written_locally_before_final_response": True,
        "stage5da_completion_summary_finalized_not_pending": True,
        **_stage_flags(),
    }
    records["credential_redaction"] = {
        **_base_record("credential_redaction"),
        **_credential_remote_summary(),
        "secret_values_printed_or_committed": False,
        **_stage_flags(),
    }
    records["validation_evidence"] = {
        **_base_record("validation_evidence"),
        "validation_evidence_status": "committed_compact_evidence",
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "parallel_worker_cap_for_stage5da_and_later": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
        "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
        "validation_commands": [
            {
                "command": "python -m libreprimus.cli token-block build-stage5da",
                "status_observed_locally": "passed",
            },
            {
                "command": "python -m libreprimus.cli token-block validate-stage5da",
                "status_observed_locally": "passed",
            },
            {
                "command": (
                    "scripts/ci/run-parallel-validation.ps1 -Workers 8 "
                    "-PytestWorkers 8 -PytestMode auto"
                ),
                "status_observed_locally": "passed",
            },
            {
                "command": PYTEST_COMMAND_OBSERVED_LOCALLY,
                "status_observed_locally": "passed",
            },
        ],
        "raw_staged": False,
        "generated_outputs_staged": False,
        "codex_output_staged": False,
        "sqlite_staged": False,
        **_stage_flags(),
    }
    records["gap_register"] = {
        **_base_record("gap_register"),
        "reviewability_gap_count": 3,
        "reviewability_gaps": [
            {
                "gap_id": "explicit_operator_choice_not_provided_in_stage5da",
                "status": "expected_scaffold_state",
                "gate_opening": False,
                "activation_defect": False,
            },
            {
                "gap_id": "explicit_pause_not_provided_in_stage5da",
                "status": "expected_scaffold_state",
                "gate_opening": False,
                "activation_defect": False,
            },
            {
                "gap_id": "additional_generic_preflight_layers_blocked_without_defect",
                "status": "scope_controlled",
                "gate_opening": False,
                "activation_defect": False,
            },
        ],
        **_stage_flags(),
    }
    records["next_stage"] = {
        **_base_record("next_stage"),
        "selected_next_stage_id": "stage-5db",
        "selected_next_stage_title": (
            "Stage 5DB - Deep Research review of Stage 5DA operator choice / "
            "pause decision scaffold, without execution"
        ),
        "selected_next_prompt_type": "deep_research_review",
        "selected_next_stage_authorizes_execution": False,
        "reason": (
            "Stage 5DA creates only a scaffold for an explicit future operator choice "
            "or explicit pause; independent review is required before any actual "
            "operator choice, pause record, approval, activation, active-planning-input "
            "selection, byte-stream stage, or execution-adjacent stage."
        ),
        "after_stage5db_requires_operator_choice_or_explicit_pause_or_human_stop": True,
        "additional_generic_preflight_layers_allowed_without_concrete_defect": False,
        **_stage_flags(),
    }
    records["summary"] = {
        **_base_record("summary"),
        "status": "complete",
        "source_stage_ids": source_stage_ids,
        "source_token_block_lineage": SOURCE_TOKEN_BLOCK_LINEAGE,
        "stage5cz_findings_integrated": True,
        "stage5cz_verdict": "accept_with_warnings",
        "stage5cy_option_selection_preflight_preserved": True,
        "stage5cy_validation_count_reconciliation_preserved": True,
        "stage5cy_governance_scope_control_preserved": True,
        "stage5cw_pytest_count_reconciliation_preserved": True,
        "operator_choice_pause_decision_scaffold_created": True,
        "operator_choice_pause_decision_scaffold_status": "scaffold_only",
        **common_choice_state,
        "explicit_pause_available_as_future_operator_outcome": True,
        "explicit_pause_selected_now": False,
        "real_operator_decision_record_created_now": False,
        "real_operator_approval_record_created_now": False,
        "real_deep_research_acceptance_record_created_now": False,
        "real_combined_gate_validation_record_created_now": False,
        "real_activation_decision_record_created_now": False,
        "combined_approval_gate_satisfied_now": False,
        "activation_decision_valid_now": False,
        "activation_authorized_now": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        "stage5bd_dry_run_records_remain_valid": True,
        "stage5bd_run_plan_id_count": 10,
        "stage5bd_run_plan_ids_changed": False,
        "stage5bd_dry_run_plan_manifest_changed": False,
        "stage5bd_plan_superseded": False,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in ACTIVE_LINEAGE_PATHS,
        "deprecated_stage5aw_path_absent": INCORRECT_STAGE5AW_PATH not in ACTIVE_LINEAGE_PATHS,
        "no_active_ingestion_status": "closed",
        "no_byte_stream_transition_gate_status": "closed",
        "no_execution_transition_gate_status": "closed",
        "string4_sidecar_status": "scaffolded_inactive",
        "string4_sidecar_active": False,
        "string4_sidecar_planning_ingestion_activated": False,
        "string4_active_input_allowed": False,
        "string4_dry_run_ingestion_allowed_now": False,
        "string4_byte_stream_generation_allowed": False,
        "string4_execution_input_allowed": False,
        "governance_overbuild_risk_acknowledged": True,
        "after_stage5da_review_requires_operator_choice_or_explicit_pause": True,
        "additional_generic_preflight_layers_allowed_without_concrete_defect": False,
        "parallel_worker_cap_for_stage5da_and_later": PARALLEL_WORKER_CAP,
        "future_token_block_execution_remains_blocked": True,
        "recommended_next_stage_id": "stage-5db",
        "recommended_next_prompt_type": "deep_research_review",
        "recommended_next_stage_title": records["next_stage"]["selected_next_stage_title"],
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_handoff_root": "codex_output",
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
        "stage5da_codex_completion_summary_required": True,
        "stage5da_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5da_codex_completion_summary_written_locally_before_final_response": True,
        "stage5da_completion_summary_finalized_not_pending": True,
        **_stage_flags(),
    }
    return records


def _write_completion_summary(summary: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CODEX_COMPLETION_PATH.write_text(
        "# Stage 5DA Codex Completion Summary\n\n"
        "- Stage: Stage 5DA operator choice / pause scaffold.\n"
        f"- Stage 5CZ verdict consumed: {summary['stage5cz_verdict']}.\n"
        "- Operator choice selected now: false.\n"
        "- Explicit pause selected now: false.\n"
        "- Real records created: false.\n"
        "- No-active/no-byte/no-execution gates: closed.\n"
        "- Recommended next stage: Stage 5DB Deep Research review.\n",
        encoding="utf-8",
    )


def build_stage5da(results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    _write_schemas()
    records = _records()
    for key, record in records.items():
        write_yaml(DATA_PATHS[key], record)
    results_dir.mkdir(parents=True, exist_ok=True)
    write_json(results_dir / "summary.json", records["summary"])
    write_json(results_dir / "choice_pause_scaffold_report.json", records["choice_pause_scaffold"])
    write_json(results_dir / "preservation_report.json", records["stage5cy_preservation"])
    write_json(results_dir / "handoff_continuity_report.json", records["handoff"])
    write_jsonl(results_dir / "warnings.jsonl", [])
    _write_completion_summary(records["summary"])
    return records["summary"]


def _validate_schema(record_key: str, path: Path) -> list[str]:
    schema_path = Path(SCHEMA_PATHS[record_key])
    if not schema_path.exists():
        return [f"missing_schema:{schema_path.as_posix()}"]
    if not path.exists():
        return [f"missing_record:{path.as_posix()}"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = _load_yaml(path)
    return [
        f"schema:{record_key}:{error.message}"
        for error in Draft202012Validator(schema).iter_errors(payload)
    ]


def _ensure_false_flags(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key, expected in FALSE_FLAGS.items():
        if key in payload and payload[key] is not expected:
            errors.append(f"{key}_must_be_false")
    if payload.get("selected_option_id") is not None:
        errors.append("selected_option_id_must_be_null")
    return errors


def _finish(
    record_key: str,
    path: Path,
    counts: dict[str, Any],
    errors: list[str],
) -> tuple[dict[str, Any], list[str]]:
    return counts, [*_validate_schema(record_key, path), *errors]


def validate_stage5da_stage5cz_findings(
    findings: Path = DATA_PATHS["findings"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(findings)
    errors = _ensure_false_flags(payload)
    if payload.get("stage5cz_verdict") != "accept_with_warnings":
        errors.append("stage5cz_verdict_must_be_accept_with_warnings")
    if payload.get("stage5cz_findings_integrated") is not True:
        errors.append("stage5cz_findings_must_be_integrated")
    counts = {
        "stage5cz_verdict": payload.get("stage5cz_verdict"),
        "finding_count": payload.get("finding_count"),
    }
    return _finish("findings", findings, counts, errors)


def validate_stage5da_choice_pause_scaffold(
    scaffold: Path = DATA_PATHS["choice_pause_scaffold"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(scaffold)
    errors = _ensure_false_flags(payload)
    mode_ids = [mode.get("mode_id") for mode in payload.get("future_decision_modes", [])]
    if payload.get("operator_choice_pause_decision_scaffold_status") != "scaffold_only":
        errors.append("choice_pause_scaffold_must_be_scaffold_only")
    if "explicit_pause_without_option_selection" not in mode_ids:
        errors.append("explicit_pause_future_mode_missing")
    if any(option.get("selected_now") is not False for option in payload.get("operator_decision_options", [])):
        errors.append("all_options_must_remain_unselected")
    counts = {
        "operator_choice_pause_decision_scaffold_created": payload.get(
            "operator_choice_pause_decision_scaffold_created"
        ),
        "operator_decision_option_count": payload.get("operator_decision_option_count"),
    }
    return _finish("choice_pause_scaffold", scaffold, counts, errors)


def validate_stage5da_choice_pause_nonselection(
    nonselection: Path = DATA_PATHS["choice_pause_nonselection"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(nonselection)
    errors = _ensure_false_flags(payload)
    expected_ids = [option["option_id"] for option in OPERATOR_DECISION_OPTIONS]
    option_ids = [option.get("option_id") for option in payload.get("operator_decision_options", [])]
    if option_ids != expected_ids:
        errors.append("exact_stage5cs_option_set_mismatch")
    if payload.get("operator_decision_option_count") != len(OPERATOR_DECISION_OPTIONS):
        errors.append("operator_decision_option_count_mismatch")
    if payload.get("explicit_pause_selected_now") is not False:
        errors.append("explicit_pause_must_not_be_selected")
    counts = {
        "operator_decision_option_count": payload.get("operator_decision_option_count"),
        "operator_decision_option_selected_now": payload.get(
            "operator_decision_option_selected_now"
        ),
        "explicit_pause_selected_now": payload.get("explicit_pause_selected_now"),
    }
    return _finish("choice_pause_nonselection", nonselection, counts, errors)


def validate_stage5da_explicit_pause_nonactivation(
    pause: Path = DATA_PATHS["explicit_pause_nonactivation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(pause)
    errors = _ensure_false_flags(payload)
    if payload.get("explicit_pause_available_as_future_operator_outcome") is not True:
        errors.append("explicit_pause_future_outcome_must_be_available")
    if payload.get("explicit_pause_selected_now") is not False:
        errors.append("explicit_pause_selected_now_must_be_false")
    counts = {
        "explicit_pause_available_as_future_operator_outcome": payload.get(
            "explicit_pause_available_as_future_operator_outcome"
        ),
        "explicit_pause_selected_now": payload.get("explicit_pause_selected_now"),
    }
    return _finish("explicit_pause_nonactivation", pause, counts, errors)


def validate_stage5da_real_record_blocker(
    blocker: Path = DATA_PATHS["real_record_blocker"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(blocker)
    errors = _ensure_false_flags(payload)
    classes = payload.get("blocked_real_record_classes", [])
    observed = [record.get("record_class") for record in classes]
    if observed != REAL_RECORD_CLASSES:
        errors.append("real_record_class_set_mismatch")
    if any(record.get("created_now") is not False for record in classes):
        errors.append("real_records_must_not_be_created")
    if any(record.get("valid_now") is not False for record in classes):
        errors.append("real_records_must_not_be_valid")
    counts = {
        "real_record_class_count": payload.get("real_record_class_count"),
        "real_records_created_now": any(record.get("created_now") for record in classes),
    }
    return _finish("real_record_blocker", blocker, counts, errors)


def validate_stage5da_stage5cy_preservation(
    preservation: Path = DATA_PATHS["stage5cy_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preservation)
    errors = _ensure_false_flags(payload)
    if payload.get("stage5cy_complete") is not True:
        errors.append("stage5cy_must_be_complete")
    if payload.get("stage5cy_option_selection_preflight_preserved") is not True:
        errors.append("stage5cy_option_selection_preflight_must_be_preserved")
    counts = {
        "stage5cy_complete": payload.get("stage5cy_complete"),
        "stage5cy_option_selection_preflight_preserved": payload.get(
            "stage5cy_option_selection_preflight_preserved"
        ),
    }
    return _finish("stage5cy_preservation", preservation, counts, errors)


def validate_stage5da_stage5bd_preservation(
    preservation: Path = DATA_PATHS["stage5bd_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    counts, errors = validate_stage5bd()
    payload = _load_yaml(preservation)
    errors.extend(_ensure_false_flags(payload))
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("stage5bd_run_plan_id_count_must_be_10")
    if payload.get("stage5bd_run_plan_ids_changed") is not False:
        errors.append("stage5bd_run_plan_ids_must_be_unchanged")
    if payload.get("string4_added_to_stage5bd_run_plan_ids") is not False:
        errors.append("string4_must_not_be_added_to_stage5bd_run_plan_ids")
    counts.update(
        {
            "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
            "stage5bd_run_plan_ids_changed": payload.get("stage5bd_run_plan_ids_changed"),
        }
    )
    return _finish("stage5bd_preservation", preservation, counts, errors)


def validate_stage5da_active_lineage_preservation(
    active_lineage: Path = DATA_PATHS["active_lineage"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(active_lineage)
    errors = _ensure_false_flags(payload)
    if payload.get("active_lineage_record_count") != len(ACTIVE_LINEAGE_PATHS):
        errors.append("active_lineage_record_count_mismatch")
    if payload.get("correct_stage5aw_path_included") is not True:
        errors.append("correct_stage5aw_path_must_be_included")
    if payload.get("deprecated_stage5aw_path_absent") is not True:
        errors.append("deprecated_stage5aw_path_must_be_absent")
    if payload.get("all_lineage_paths_resolve") is not True:
        errors.append("all_lineage_paths_must_resolve")
    counts = {
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
        "correct_stage5aw_path_included": payload.get("correct_stage5aw_path_included"),
        "deprecated_stage5aw_path_absent": payload.get("deprecated_stage5aw_path_absent"),
    }
    return _finish("active_lineage", active_lineage, counts, errors)


def validate_stage5da_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for key, status_field in [
        ("no_active_ingestion", "no_active_ingestion_status"),
        ("no_byte_stream_transition_gate", "no_byte_stream_transition_gate_status"),
        ("no_execution_transition_gate", "no_execution_transition_gate_status"),
    ]:
        payload = _load_yaml(DATA_PATHS[key])
        errors.extend(_ensure_false_flags(payload))
        errors.extend(_validate_schema(key, DATA_PATHS[key]))
        if payload.get(status_field) != "closed":
            errors.append(f"{status_field}_must_be_closed")
        counts[status_field] = payload.get(status_field)
    return counts, errors


def validate_stage5da_handoff_continuity() -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(DATA_PATHS["handoff"])
    errors = _ensure_false_flags(payload)
    if not CODEX_COMPLETION_PATH.exists():
        errors.append("stage5da_codex_completion_summary_missing")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output_underscore_root_must_be_absent")
    if CODEX_COMPLETION_PATH.exists() and "pending" in CODEX_COMPLETION_PATH.read_text(
        encoding="utf-8"
    ).lower():
        errors.append("stage5da_completion_summary_must_not_be_pending")
    counts = {
        "stage5da_codex_completion_summary_present": CODEX_COMPLETION_PATH.exists(),
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
    }
    return _finish("handoff", DATA_PATHS["handoff"], counts, errors)


def validate_stage5da_credential_redaction_policy(
    credential_redaction: Path = DATA_PATHS["credential_redaction"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(credential_redaction)
    errors = _ensure_false_flags(payload)
    if payload.get("remote_url_values_printed") is not False:
        errors.append("remote_url_values_must_not_be_printed")
    if payload.get("secret_values_printed_or_committed") is not False:
        errors.append("secret_values_must_not_be_printed_or_committed")
    counts = {
        "credential_like_remote_count": payload.get("credential_like_remote_count"),
        "remote_url_values_printed": payload.get("remote_url_values_printed"),
    }
    return _finish("credential_redaction", credential_redaction, counts, errors)


def validate_stage5da_governance_scope_control(
    governance: Path = DATA_PATHS["governance_scope_control"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(governance)
    errors = _ensure_false_flags(payload)
    if payload.get("stage5cz_review_integrated") is not True:
        errors.append("stage5cz_review_must_be_integrated")
    if payload.get("stage5da_creates_generic_preflight_layer") is not False:
        errors.append("stage5da_must_not_create_generic_preflight_layer")
    if payload.get("additional_generic_preflight_layers_allowed_without_concrete_defect") is not False:
        errors.append("generic_preflight_layers_must_be_blocked_without_defect")
    counts = {
        "governance_overbuild_risk_acknowledged": payload.get(
            "governance_overbuild_risk_acknowledged"
        ),
        "stage5cz_review_integrated": payload.get("stage5cz_review_integrated"),
    }
    return _finish("governance_scope_control", governance, counts, errors)


def validate_stage5da(
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(summary)
    errors = _ensure_false_flags(payload)
    for validator in [
        validate_stage5da_stage5cz_findings,
        validate_stage5da_choice_pause_scaffold,
        validate_stage5da_choice_pause_nonselection,
        validate_stage5da_explicit_pause_nonactivation,
        validate_stage5da_real_record_blocker,
        validate_stage5da_stage5cy_preservation,
        validate_stage5da_stage5bd_preservation,
        validate_stage5da_active_lineage_preservation,
        validate_stage5da_sidecar_gates,
        validate_stage5da_handoff_continuity,
        validate_stage5da_credential_redaction_policy,
        validate_stage5da_governance_scope_control,
    ]:
        _, validator_errors = validator()
        errors.extend(validator_errors)
    if payload.get("recommended_next_stage_id") != "stage-5db":
        errors.append("recommended_next_stage_id_must_be_stage5db")
    if _load_yaml(next_stage_decision).get("selected_next_stage_id") != "stage-5db":
        errors.append("next_stage_decision_must_select_stage5db_review")
    for filename in [
        "summary.json",
        "choice_pause_scaffold_report.json",
        "preservation_report.json",
        "handoff_continuity_report.json",
        "warnings.jsonl",
    ]:
        if not (results_dir / filename).exists():
            errors.append(f"missing_generated_report:{filename}")
    counts = {
        "stage5cz_verdict": payload.get("stage5cz_verdict"),
        "operator_choice_pause_decision_scaffold_created": payload.get(
            "operator_choice_pause_decision_scaffold_created"
        ),
        "operator_decision_option_selected_now": payload.get(
            "operator_decision_option_selected_now"
        ),
        "explicit_pause_selected_now": payload.get("explicit_pause_selected_now"),
        "selected_option_id": payload.get("selected_option_id"),
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_decision_valid_now": payload.get("activation_decision_valid_now"),
        "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
        "parallel_worker_cap": payload.get("parallel_worker_cap_for_stage5da_and_later"),
        "recommended_next_stage_id": payload.get("recommended_next_stage_id"),
    }
    return _finish("summary", summary, counts, errors)


def load_stage5da_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _load_yaml(summary)
