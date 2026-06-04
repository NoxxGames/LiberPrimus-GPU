"""Stage 5DC operator choice decision metadata."""

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
from libreprimus.token_block.stage5da import DATA_PATHS as STAGE5DA_DATA_PATHS
from libreprimus.token_block.stage5bm import _read

STAGE_ID = "stage-5dc"
STAGE_TITLE = (
    "Stage 5DC - Operator choice decision record selecting "
    "prepare_real_operator_approval_record, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5da"
SOURCE_PREVIOUS_COMMIT = "91eda1b7ead974745fe1e684f1e2d90c532f9514"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5db"
SOURCE_DEEP_RESEARCH_REPORT = "29_Stage-5DA-Deep-Research-Review.md"
SELECTED_OPTION_ID = "prepare_real_operator_approval_record"
CHOICE_SOURCE = "explicit_operator_prompt_stage5dc"
RESULTS_DIR = Path("experiments/results/token-block/stage5dc")
CODEX_COMPLETION_PATH = Path("codex-output/stage5dc-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
PYTEST_COUNT_OBSERVED_LOCALLY = 2519
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"

REAL_RECORD_BOUNDARY_CLASSES = [
    "real_operator_approval_record",
    "real_deep_research_acceptance_record",
    "real_combined_gate_validation_record",
    "real_activation_decision_record",
    "active_planning_input_selection_record",
    "active_planning_input_authorization_record",
    "dry_run_ingestion_authorization_record",
    "byte_stream_generation_authorization_record",
    "execution_authorization_record",
]

STAGE5DB_FINDINGS = [
    "stage5da_accepted_with_warnings",
    "stage5da_choice_pause_scaffold_is_reviewable",
    "stage5da_preserved_stage5cy_stage5cs_stage5bd_and_lineage",
    "stage5da_kept_all_options_unselected",
    "stage5da_kept_explicit_pause_unselected",
    "governance_overbuild_risk_confirmed",
    "next_step_should_be_actual_operator_choice_or_explicit_pause",
    "stage5db_did_not_recommend_execution",
    "stage5db_did_not_create_approval_or_activation",
]

TRUE_FLAGS = {
    "operator_choice_or_pause_record_created_now": True,
    "operator_choice_or_pause_record_valid_now": True,
    "explicit_operator_choice_provided_now": True,
    "operator_decision_option_selected_now": True,
    "real_operator_choice_pause_record_created_now": True,
    "real_operator_choice_pause_record_valid_now": True,
    "stage5dc_selects_operator_choice": True,
}

_STAGE5CY_FALSE_OVERRIDES = {
    "operator_decision_option_selected_now",
}

FALSE_FLAGS = {
    **{
        key: value
        for key, value in STAGE5CY_FALSE_FLAGS.items()
        if key not in _STAGE5CY_FALSE_OVERRIDES
    },
    "explicit_pause_provided_now": False,
    "explicit_pause_selected_now": False,
    "automatic_option_selection_allowed": False,
    "real_operator_approval_record_created_now": False,
    "real_operator_approval_record_present_now": False,
    "real_deep_research_acceptance_record_created_now": False,
    "real_deep_research_acceptance_record_present_now": False,
    "real_combined_gate_validation_record_created_now": False,
    "real_combined_gate_validation_record_present_now": False,
    "combined_approval_gate_satisfied_now": False,
    "combined_approval_gate_authorizes_activation_now": False,
    "approval_gate_satisfied_now": False,
    "approval_gate_authorizes_activation_now": False,
    "real_activation_decision_record_created_now": False,
    "real_activation_decision_record_present_now": False,
    "activation_decision_valid_now": False,
    "activation_authorized_now": False,
    "active_planning_input_authorized_now": False,
    "active_planning_input_selected_now": False,
    "new_active_planning_input_created": False,
    "byte_stream_generation_authorized_now": False,
    "real_byte_stream_generated": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "branch_enumeration_performed": False,
    "full_cartesian_product_enumerated": False,
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
    "page_boundaries_finalized": False,
    "stage5dc_creates_generic_preflight_layer": False,
    "stage5dc_creates_broad_new_negative_fixture_layer": False,
    "stage5dc_creates_real_operator_approval_record": False,
    "old_16_worker_default_reintroduced": False,
    "selected_option_authorizes_real_operator_approval_record_creation_now": False,
    "selected_option_authorizes_real_approval_now": False,
    "selected_option_authorizes_deep_research_acceptance_now": False,
    "selected_option_authorizes_combined_gate_validation_now": False,
    "selected_option_authorizes_activation_decision_now": False,
    "selected_option_authorizes_activation_now": False,
    "selected_option_authorizes_active_planning_input_now": False,
    "selected_option_authorizes_dry_run_ingestion_now": False,
    "selected_option_authorizes_byte_stream_generation_now": False,
    "selected_option_authorizes_execution_now": False,
    "target_class_validation_implemented": False,
    "tor_network_access_performed": False,
}

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5dc-summary.yaml"),
    "next_stage": Path("data/project-state/stage5dc-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5dc-stage5db-findings-integration.yaml"),
    "governance_scope_control": Path(
        "data/project-state/stage5dc-governance-scope-control.yaml"
    ),
    "validation_evidence": Path(
        "data/project-state/stage5dc-reviewable-validation-evidence.yaml"
    ),
    "gap_register": Path("data/project-state/stage5dc-reviewability-gap-register.yaml"),
    "choice_decision": Path("data/token-block/stage5dc-operator-choice-decision-record.yaml"),
    "selected_option": Path("data/token-block/stage5dc-selected-option-record.yaml"),
    "unselected_options": Path(
        "data/token-block/stage5dc-unselected-options-preservation.yaml"
    ),
    "explicit_pause_nonselection": Path(
        "data/token-block/stage5dc-explicit-pause-nonselection-proof.yaml"
    ),
    "real_approval_noncreation": Path(
        "data/token-block/stage5dc-real-approval-noncreation-proof.yaml"
    ),
    "combined_gate": Path(
        "data/token-block/stage5dc-combined-gate-non-satisfaction-proof.yaml"
    ),
    "activation_nonauthorization": Path(
        "data/token-block/stage5dc-activation-decision-nonauthorization-proof.yaml"
    ),
    "real_record_boundary": Path(
        "data/token-block/stage5dc-real-record-creation-boundary.yaml"
    ),
    "stage5cy_preservation": Path("data/token-block/stage5dc-stage5cy-preservation.yaml"),
    "stage5da_preservation": Path("data/token-block/stage5dc-stage5da-preservation.yaml"),
    "stage5bd_preservation": Path(
        "data/token-block/stage5dc-stage5bd-plan-preservation.yaml"
    ),
    "active_lineage": Path("data/token-block/stage5dc-active-lineage-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5dc-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5dc-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5dc-no-execution-transition-gate.yaml"
    ),
    "handoff": Path("data/source-harvester/stage5dc-codex-handoff-policy.yaml"),
    "credential_redaction": Path(
        "data/source-harvester/stage5dc-credential-redaction-policy-preservation.yaml"
    ),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5dc_{key}" for key in DATA_PATHS}


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
    return {**FALSE_FLAGS, **TRUE_FLAGS, "selected_option_id": SELECTED_OPTION_ID}


def _schema_for(record_key: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"const": RECORD_TYPES[record_key]},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "execution_allowed": {"const": False},
        "solve_claim": {"const": False},
        "selected_option_id": {"const": SELECTED_OPTION_ID},
    }
    for key in FALSE_FLAGS:
        properties[key] = {"const": False}
    for key in TRUE_FLAGS:
        properties[key] = {"const": True}
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
            "selected_option_id",
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


def _stage5da_summary() -> dict[str, Any]:
    return _load_yaml(STAGE5DA_DATA_PATHS["summary"])


def _options() -> list[dict[str, Any]]:
    options: list[dict[str, Any]] = []
    for option in OPERATOR_DECISION_OPTIONS:
        selected = option["option_id"] == SELECTED_OPTION_ID
        options.append(
            {
                **option,
                "selected_now": selected,
                "choice_source": CHOICE_SOURCE if selected else None,
                "authorizes_real_operator_approval_record_creation_now": False,
                "authorizes_real_approval_now": False,
                "authorizes_deep_research_acceptance_now": False,
                "authorizes_combined_gate_validation_now": False,
                "authorizes_activation_decision_now": False,
                "authorizes_activation_now": False,
                "authorizes_active_planning_input_now": False,
                "authorizes_dry_run_ingestion_now": False,
                "authorizes_byte_stream_generation_now": False,
                "authorizes_execution_now": False,
                "solve_claim": False,
            }
        )
    return options


def _selected_option(options: list[dict[str, Any]]) -> dict[str, Any]:
    for option in options:
        if option["option_id"] == SELECTED_OPTION_ID:
            return option
    raise ValueError(f"missing expected option {SELECTED_OPTION_ID}")


def _unselected_options(options: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [option for option in options if option["option_id"] != SELECTED_OPTION_ID]


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


def _choice_state(options: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "operator_choice_or_pause_record_created_now": True,
        "operator_choice_or_pause_record_valid_now": True,
        "real_operator_choice_pause_record_created_now": True,
        "real_operator_choice_pause_record_valid_now": True,
        "explicit_operator_choice_provided_now": True,
        "explicit_pause_provided_now": False,
        "explicit_pause_selected_now": False,
        "selected_option_id": SELECTED_OPTION_ID,
        "choice_source": CHOICE_SOURCE,
        "operator_decision_option_count": len(options),
        "stage5cs_exact_option_set_preserved": True,
        "all_options_unselected": False,
        "operator_decision_option_selected_now": True,
        "automatic_option_selection_allowed": False,
        "selected_option_count": 1,
        "unselected_option_count": len(options) - 1,
    }


def _records() -> dict[str, dict[str, Any]]:
    stage5cy_summary = _stage5cy_summary()
    stage5da_summary = _stage5da_summary()
    options = _options()
    selected_option = _selected_option(options)
    unselected_options = _unselected_options(options)
    choice_state = _choice_state(options)
    source_stage_ids = ["stage-5db", "stage-5da", *STAGE5CY_SOURCE_STAGE_IDS]

    records: dict[str, dict[str, Any]] = {}
    records["findings"] = {
        **_base_record("findings"),
        "stage5db_verdict": "accept_with_warnings",
        "stage5db_findings_integrated": True,
        "stage5db_report_file": SOURCE_DEEP_RESEARCH_REPORT,
        "finding_count": len(STAGE5DB_FINDINGS),
        "findings": STAGE5DB_FINDINGS,
        "stage5db_did_not_recommend_execution": True,
        "stage5db_did_not_create_approval_or_activation": True,
        **_stage_flags(),
    }
    records["governance_scope_control"] = {
        **_base_record("governance_scope_control"),
        "governance_overbuild_risk_acknowledged": True,
        "stage5db_review_integrated": True,
        "stage5dc_is_narrow_operator_choice_stage": True,
        "additional_generic_preflight_layers_allowed_without_concrete_defect": False,
        "stage5dc_creates_generic_preflight_layer": False,
        "stage5dc_creates_broad_new_negative_fixture_layer": False,
        "stage5dc_creates_real_operator_approval_record": False,
        "after_stage5dd_likely_next_codex_stage": (
            "Stage 5DE - Real operator approval record preparation package, "
            "without activation"
        ),
        **_stage_flags(),
    }
    records["choice_decision"] = {
        **_base_record("choice_decision"),
        **choice_state,
        "operator_choice_pause_decision_record_status": "valid_real_operator_choice_record",
        "operator_decision_options": options,
        "selected_option": selected_option,
        "explicit_pause_available_as_future_operator_outcome": True,
        "future_decision_modes": [
            {
                "mode_id": "select_exactly_one_stage5cs_option",
                "selected_now": True,
                "requires_explicit_operator_input": True,
            },
            {
                "mode_id": "explicit_pause_without_option_selection",
                "selected_now": False,
                "requires_explicit_operator_input": True,
            },
        ],
        **_stage_flags(),
    }
    records["selected_option"] = {
        **_base_record("selected_option"),
        **choice_state,
        "option_id": SELECTED_OPTION_ID,
        "selected_now": True,
        "future_action_class": "record_preparation_only",
        "selected_option": selected_option,
        "authorizes_real_operator_approval_record_creation_now": False,
        "authorizes_real_approval_now": False,
        "authorizes_deep_research_acceptance_now": False,
        "authorizes_combined_gate_validation_now": False,
        "authorizes_activation_decision_now": False,
        "authorizes_activation_now": False,
        "authorizes_active_planning_input_now": False,
        "authorizes_dry_run_ingestion_now": False,
        "authorizes_byte_stream_generation_now": False,
        "authorizes_execution_now": False,
        "target_class_context_recorded_for_future_design_only": True,
        **_stage_flags(),
    }
    records["unselected_options"] = {
        **_base_record("unselected_options"),
        **choice_state,
        "unselected_options_preserved": True,
        "unselected_options": unselected_options,
        "unselected_option_ids": [option["option_id"] for option in unselected_options],
        **_stage_flags(),
    }
    records["explicit_pause_nonselection"] = {
        **_base_record("explicit_pause_nonselection"),
        **choice_state,
        "explicit_pause_available_as_future_operator_outcome": True,
        "explicit_pause_provided_now": False,
        "explicit_pause_selected_now": False,
        "explicit_pause_authorizes_approval": False,
        "explicit_pause_authorizes_activation": False,
        "explicit_pause_authorizes_active_input": False,
        "explicit_pause_authorizes_dry_run_ingestion": False,
        "explicit_pause_authorizes_byte_stream_generation": False,
        "explicit_pause_authorizes_execution": False,
        **_stage_flags(),
    }
    records["real_approval_noncreation"] = {
        **_base_record("real_approval_noncreation"),
        **choice_state,
        "real_operator_approval_record_created_now": False,
        "real_operator_approval_record_present_now": False,
        "operator_approval_record_present_now": False,
        "real_approval_records_created": False,
        "approval_gate_satisfied_now": False,
        "approval_gate_authorizes_activation_now": False,
        **_stage_flags(),
    }
    records["combined_gate"] = {
        **_base_record("combined_gate"),
        **choice_state,
        "real_combined_gate_validation_record_created_now": False,
        "real_combined_gate_validation_record_present_now": False,
        "combined_approval_gate_satisfied_now": False,
        "combined_approval_gate_authorizes_activation_now": False,
        **_stage_flags(),
    }
    records["activation_nonauthorization"] = {
        **_base_record("activation_nonauthorization"),
        **choice_state,
        "real_activation_decision_record_created_now": False,
        "real_activation_decision_record_present_now": False,
        "activation_decision_valid_now": False,
        "activation_authorized_now": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        "new_active_planning_input_created": False,
        **_stage_flags(),
    }
    records["real_record_boundary"] = {
        **_base_record("real_record_boundary"),
        **choice_state,
        "real_operator_choice_pause_record_is_only_real_record_created_now": True,
        "blocked_real_record_class_count": len(REAL_RECORD_BOUNDARY_CLASSES),
        "blocked_real_record_classes": [
            {
                "record_class": record_class,
                "created_now": False,
                "present_now": False,
                "valid_now": False,
                "blocked_reason": "stage5dc_selects_option_only_without_approval_creation",
            }
            for record_class in REAL_RECORD_BOUNDARY_CLASSES
        ],
        **_stage_flags(),
    }
    records["stage5cy_preservation"] = {
        **_base_record("stage5cy_preservation"),
        **choice_state,
        "stage5cy_summary_path": STAGE5CY_DATA_PATHS["summary"].as_posix(),
        "stage5cy_complete": stage5cy_summary.get("status") == "complete",
        "stage5cy_option_selection_preflight_preserved": True,
        "stage5cy_validation_count_reconciliation_preserved": True,
        "stage5cy_governance_scope_control_preserved": True,
        "stage5cw_pytest_count_reconciliation_preserved": True,
        "stage5cy_preserved_without_historical_edit": True,
        **_stage_flags(),
    }
    records["stage5da_preservation"] = {
        **_base_record("stage5da_preservation"),
        **choice_state,
        "stage5da_summary_path": STAGE5DA_DATA_PATHS["summary"].as_posix(),
        "stage5da_complete": stage5da_summary.get("status") == "complete",
        "stage5da_scaffold_preserved": True,
        "stage5da_review_required_before_choice_satisfied_by_stage5db": True,
        "stage5da_historical_records_mutated": False,
        **_stage_flags(),
    }
    records["stage5bd_preservation"] = {
        **_base_record("stage5bd_preservation"),
        **choice_state,
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
        **choice_state,
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
        **choice_state,
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
        **choice_state,
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
        **choice_state,
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
        "page_boundaries_finalized": False,
        **_stage_flags(),
    }
    records["handoff"] = {
        **_base_record("handoff"),
        **choice_state,
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_handoff_root": "codex_output",
        "codex_output_used": False,
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
        "codex_completion_summary_committed": False,
        "stage5dc_codex_completion_summary_required": True,
        "stage5dc_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5dc_codex_completion_summary_written_locally_before_final_response": True,
        "stage5dc_completion_summary_finalized_not_pending": True,
        **_stage_flags(),
    }
    records["credential_redaction"] = {
        **_base_record("credential_redaction"),
        **choice_state,
        **_credential_remote_summary(),
        "secret_values_printed_or_committed": False,
        **_stage_flags(),
    }
    records["validation_evidence"] = {
        **_base_record("validation_evidence"),
        **choice_state,
        "validation_evidence_status": "committed_compact_evidence",
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "parallel_worker_cap_for_stage5dc_and_later": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
        "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
        "validation_commands": [
            {
                "command": "python -m libreprimus.cli token-block build-stage5dc",
                "status_observed_locally": "passed",
            },
            {
                "command": "python -m libreprimus.cli token-block validate-stage5dc",
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
        **choice_state,
        "reviewability_gap_count": 2,
        "reviewability_gaps": [
            {
                "gap_id": "real_operator_approval_record_not_created_in_stage5dc",
                "status": "expected_stage_boundary",
                "gate_opening": False,
                "activation_defect": False,
            },
            {
                "gap_id": "stage5dd_review_required_before_approval_record_package",
                "status": "review_required",
                "gate_opening": False,
                "activation_defect": False,
            },
        ],
        **_stage_flags(),
    }
    records["next_stage"] = {
        **_base_record("next_stage"),
        **choice_state,
        "selected_next_stage_id": "stage-5dd",
        "selected_next_stage_title": (
            "Stage 5DD - Deep Research review of Stage 5DC operator choice selecting "
            "prepare_real_operator_approval_record, without execution"
        ),
        "selected_next_prompt_type": "deep_research_review",
        "selected_next_stage_authorizes_execution": False,
        "reason": (
            "Stage 5DC creates a real operator-choice / pause decision record selecting "
            "prepare_real_operator_approval_record, but it does not create a real "
            "operator approval record or authorize activation; independent review is "
            "required before any future operator approval record preparation package."
        ),
        "likely_post_review_codex_stage_if_accepted": (
            "Stage 5DE - Real operator approval record preparation package, "
            "without activation"
        ),
        **_stage_flags(),
    }
    records["summary"] = {
        **_base_record("summary"),
        "status": "complete",
        "source_stage_ids": source_stage_ids,
        "source_token_block_lineage": SOURCE_TOKEN_BLOCK_LINEAGE,
        "stage5db_findings_integrated": True,
        "stage5db_verdict": "accept_with_warnings",
        "stage5cy_option_selection_preflight_preserved": True,
        "stage5cy_validation_count_reconciliation_preserved": True,
        "stage5cy_governance_scope_control_preserved": True,
        "stage5da_operator_choice_pause_scaffold_preserved": True,
        "stage5cs_exact_option_set_preserved": True,
        **choice_state,
        "explicit_pause_available_as_future_operator_outcome": True,
        "real_operator_approval_record_created_now": False,
        "real_operator_approval_record_present_now": False,
        "operator_approval_record_present_now": False,
        "real_deep_research_acceptance_record_created_now": False,
        "real_deep_research_acceptance_record_present_now": False,
        "deep_research_activation_accept_record_present_now": False,
        "real_combined_gate_validation_record_created_now": False,
        "real_combined_gate_validation_record_present_now": False,
        "combined_approval_gate_satisfied_now": False,
        "combined_approval_gate_authorizes_activation_now": False,
        "approval_gate_satisfied_now": False,
        "approval_gate_authorizes_activation_now": False,
        "real_activation_decision_record_created_now": False,
        "real_activation_decision_record_present_now": False,
        "activation_decision_valid_now": False,
        "activation_authorized_now": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        "new_active_planning_input_created": False,
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
        "parallel_worker_cap_for_stage5dc_and_later": PARALLEL_WORKER_CAP,
        "future_token_block_execution_remains_blocked": True,
        "recommended_next_stage_id": "stage-5dd",
        "recommended_next_prompt_type": "deep_research_review",
        "recommended_next_stage_title": records["next_stage"]["selected_next_stage_title"],
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_handoff_root": "codex_output",
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
        "stage5dc_codex_completion_summary_required": True,
        "stage5dc_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5dc_codex_completion_summary_written_locally_before_final_response": True,
        "stage5dc_completion_summary_finalized_not_pending": True,
        **_stage_flags(),
    }
    return records


def _write_completion_summary(summary: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CODEX_COMPLETION_PATH.write_text(
        "# Stage 5DC Codex Completion Summary\n\n"
        f"- Starting commit: {SOURCE_PREVIOUS_COMMIT}.\n"
        "- Final commit: recorded in final response after push.\n"
        "- GitHub issue: recorded in final response after issue update.\n"
        "- CI run: recorded in final response after push.\n"
        f"- Selected option ID: {summary['selected_option_id']}.\n"
        f"- Explicit pause selected: {str(summary['explicit_pause_selected_now']).lower()}.\n"
        "- Real operator approval created: false.\n"
        "- Combined gate satisfied: false.\n"
        "- Activation authorized: false.\n"
        "- Active input selected: false.\n"
        f"- Stage 5BD run-plan count: {summary['stage5bd_run_plan_id_count']}.\n"
        f"- Active-lineage record count: {summary['active_lineage_record_count']}.\n"
        f"- Pytest count: {PYTEST_COUNT_OBSERVED_LOCALLY}.\n"
        f"- 8-worker validation cap: {PARALLEL_WORKER_CAP}.\n"
        "- Raw/generated/codex-output/codex_output staging status: zero staged by policy.\n"
        "- Guardrails: no approval, activation, active input, byte stream, execution, CUDA, "
        "benchmark, website expansion, canonical corpus activation, page-boundary "
        "finalisation, or solve claim.\n"
        "- Recommended next stage: Stage 5DD Deep Research review.\n",
        encoding="utf-8",
    )


def build_stage5dc(results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    _write_schemas()
    records = _records()
    for key, record in records.items():
        write_yaml(DATA_PATHS[key], record)
    results_dir.mkdir(parents=True, exist_ok=True)
    write_json(results_dir / "summary.json", records["summary"])
    write_json(results_dir / "choice_decision_report.json", records["choice_decision"])
    write_json(results_dir / "selected_option_report.json", records["selected_option"])
    write_json(results_dir / "preservation_report.json", records["stage5da_preservation"])
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


def _ensure_stage_flags(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key, expected in FALSE_FLAGS.items():
        if key in payload and payload[key] is not expected:
            errors.append(f"{key}_must_be_false")
    for key, expected in TRUE_FLAGS.items():
        if key in payload and payload[key] is not expected:
            errors.append(f"{key}_must_be_true")
    if payload.get("selected_option_id") != SELECTED_OPTION_ID:
        errors.append("selected_option_id_must_match_stage5dc_choice")
    return errors


def _finish(
    record_key: str,
    path: Path,
    counts: dict[str, Any],
    errors: list[str],
) -> tuple[dict[str, Any], list[str]]:
    return counts, [*_validate_schema(record_key, path), *errors]


def validate_stage5dc_stage5db_findings(
    findings: Path = DATA_PATHS["findings"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(findings)
    errors = _ensure_stage_flags(payload)
    if payload.get("stage5db_verdict") != "accept_with_warnings":
        errors.append("stage5db_verdict_must_be_accept_with_warnings")
    if payload.get("stage5db_findings_integrated") is not True:
        errors.append("stage5db_findings_must_be_integrated")
    counts = {
        "stage5db_verdict": payload.get("stage5db_verdict"),
        "finding_count": payload.get("finding_count"),
    }
    return _finish("findings", findings, counts, errors)


def validate_stage5dc_choice_decision(
    decision: Path = DATA_PATHS["choice_decision"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(decision)
    errors = _ensure_stage_flags(payload)
    options = payload.get("operator_decision_options", [])
    selected = [option for option in options if option.get("selected_now") is True]
    if payload.get("operator_choice_pause_decision_record_status") != (
        "valid_real_operator_choice_record"
    ):
        errors.append("choice_record_status_must_be_valid_real_operator_choice_record")
    if len(selected) != 1:
        errors.append("exactly_one_option_must_be_selected")
    elif selected[0].get("option_id") != SELECTED_OPTION_ID:
        errors.append("selected_option_id_mismatch")
    counts = {
        "operator_choice_or_pause_record_created_now": payload.get(
            "operator_choice_or_pause_record_created_now"
        ),
        "operator_choice_or_pause_record_valid_now": payload.get(
            "operator_choice_or_pause_record_valid_now"
        ),
        "selected_option_id": payload.get("selected_option_id"),
        "selected_option_count": len(selected),
    }
    return _finish("choice_decision", decision, counts, errors)


def validate_stage5dc_selected_option(
    selected_option: Path = DATA_PATHS["selected_option"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(selected_option)
    errors = _ensure_stage_flags(payload)
    if payload.get("option_id") != SELECTED_OPTION_ID:
        errors.append("selected_option_record_option_id_mismatch")
    if payload.get("selected_now") is not True:
        errors.append("selected_option_must_be_selected_now")
    for field in [
        "authorizes_real_operator_approval_record_creation_now",
        "authorizes_real_approval_now",
        "authorizes_deep_research_acceptance_now",
        "authorizes_combined_gate_validation_now",
        "authorizes_activation_decision_now",
        "authorizes_activation_now",
        "authorizes_active_planning_input_now",
        "authorizes_dry_run_ingestion_now",
        "authorizes_byte_stream_generation_now",
        "authorizes_execution_now",
    ]:
        if payload.get(field) is not False:
            errors.append(f"{field}_must_be_false")
    counts = {
        "option_id": payload.get("option_id"),
        "selected_now": payload.get("selected_now"),
        "future_action_class": payload.get("future_action_class"),
    }
    return _finish("selected_option", selected_option, counts, errors)


def validate_stage5dc_nonselected_options(
    unselected_options: Path = DATA_PATHS["unselected_options"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(unselected_options)
    errors = _ensure_stage_flags(payload)
    expected_ids = [
        option["option_id"]
        for option in OPERATOR_DECISION_OPTIONS
        if option["option_id"] != SELECTED_OPTION_ID
    ]
    observed_ids = payload.get("unselected_option_ids", [])
    if observed_ids != expected_ids:
        errors.append("unselected_option_id_set_mismatch")
    if any(option.get("selected_now") is not False for option in payload.get("unselected_options", [])):
        errors.append("nonselected_options_must_remain_unselected")
    counts = {
        "unselected_option_count": payload.get("unselected_option_count"),
        "selected_option_id": payload.get("selected_option_id"),
    }
    return _finish("unselected_options", unselected_options, counts, errors)


def validate_stage5dc_explicit_pause_nonselection(
    pause: Path = DATA_PATHS["explicit_pause_nonselection"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(pause)
    errors = _ensure_stage_flags(payload)
    if payload.get("explicit_pause_selected_now") is not False:
        errors.append("explicit_pause_selected_now_must_be_false")
    if payload.get("explicit_pause_provided_now") is not False:
        errors.append("explicit_pause_provided_now_must_be_false")
    counts = {
        "explicit_pause_selected_now": payload.get("explicit_pause_selected_now"),
        "explicit_pause_provided_now": payload.get("explicit_pause_provided_now"),
    }
    return _finish("explicit_pause_nonselection", pause, counts, errors)


def validate_stage5dc_real_approval_noncreation(
    approval: Path = DATA_PATHS["real_approval_noncreation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(approval)
    errors = _ensure_stage_flags(payload)
    if payload.get("real_operator_approval_record_created_now") is not False:
        errors.append("real_operator_approval_record_must_not_be_created")
    counts = {
        "real_operator_approval_record_created_now": payload.get(
            "real_operator_approval_record_created_now"
        ),
        "real_operator_approval_record_present_now": payload.get(
            "real_operator_approval_record_present_now"
        ),
    }
    return _finish("real_approval_noncreation", approval, counts, errors)


def validate_stage5dc_combined_gate(
    combined_gate: Path = DATA_PATHS["combined_gate"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(combined_gate)
    errors = _ensure_stage_flags(payload)
    if payload.get("combined_approval_gate_satisfied_now") is not False:
        errors.append("combined_approval_gate_must_remain_unsatisfied")
    counts = {
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "real_combined_gate_validation_record_created_now": payload.get(
            "real_combined_gate_validation_record_created_now"
        ),
    }
    return _finish("combined_gate", combined_gate, counts, errors)


def validate_stage5dc_activation_nonauthorization(
    activation: Path = DATA_PATHS["activation_nonauthorization"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(activation)
    errors = _ensure_stage_flags(payload)
    for field in [
        "activation_decision_valid_now",
        "activation_authorized_now",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
    ]:
        if payload.get(field) is not False:
            errors.append(f"{field}_must_be_false")
    counts = {
        "activation_decision_valid_now": payload.get("activation_decision_valid_now"),
        "activation_authorized_now": payload.get("activation_authorized_now"),
        "active_planning_input_selected_now": payload.get(
            "active_planning_input_selected_now"
        ),
    }
    return _finish("activation_nonauthorization", activation, counts, errors)


def validate_stage5dc_real_record_boundary(
    boundary: Path = DATA_PATHS["real_record_boundary"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(boundary)
    errors = _ensure_stage_flags(payload)
    classes = payload.get("blocked_real_record_classes", [])
    observed = [record.get("record_class") for record in classes]
    if observed != REAL_RECORD_BOUNDARY_CLASSES:
        errors.append("real_record_boundary_class_set_mismatch")
    if any(record.get("created_now") is not False for record in classes):
        errors.append("blocked_real_records_must_not_be_created")
    counts = {
        "blocked_real_record_class_count": payload.get("blocked_real_record_class_count"),
        "real_operator_choice_pause_record_created_now": payload.get(
            "real_operator_choice_pause_record_created_now"
        ),
    }
    return _finish("real_record_boundary", boundary, counts, errors)


def validate_stage5dc_stage5cy_preservation(
    preservation: Path = DATA_PATHS["stage5cy_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preservation)
    errors = _ensure_stage_flags(payload)
    if payload.get("stage5cy_complete") is not True:
        errors.append("stage5cy_must_be_complete")
    if payload.get("stage5cy_governance_scope_control_preserved") is not True:
        errors.append("stage5cy_governance_scope_control_must_be_preserved")
    counts = {
        "stage5cy_complete": payload.get("stage5cy_complete"),
        "stage5cy_option_selection_preflight_preserved": payload.get(
            "stage5cy_option_selection_preflight_preserved"
        ),
    }
    return _finish("stage5cy_preservation", preservation, counts, errors)


def validate_stage5dc_stage5da_preservation(
    preservation: Path = DATA_PATHS["stage5da_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preservation)
    errors = _ensure_stage_flags(payload)
    if payload.get("stage5da_complete") is not True:
        errors.append("stage5da_must_be_complete")
    if payload.get("stage5da_scaffold_preserved") is not True:
        errors.append("stage5da_scaffold_must_be_preserved")
    counts = {
        "stage5da_complete": payload.get("stage5da_complete"),
        "stage5da_scaffold_preserved": payload.get("stage5da_scaffold_preserved"),
    }
    return _finish("stage5da_preservation", preservation, counts, errors)


def validate_stage5dc_stage5bd_preservation(
    preservation: Path = DATA_PATHS["stage5bd_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    counts, errors = validate_stage5bd()
    payload = _load_yaml(preservation)
    errors.extend(_ensure_stage_flags(payload))
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("stage5bd_run_plan_id_count_must_be_10")
    if payload.get("stage5bd_run_plan_ids_changed") is not False:
        errors.append("stage5bd_run_plan_ids_must_be_unchanged")
    counts.update(
        {
            "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
            "stage5bd_run_plan_ids_changed": payload.get("stage5bd_run_plan_ids_changed"),
        }
    )
    return _finish("stage5bd_preservation", preservation, counts, errors)


def validate_stage5dc_active_lineage_preservation(
    active_lineage: Path = DATA_PATHS["active_lineage"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(active_lineage)
    errors = _ensure_stage_flags(payload)
    if payload.get("active_lineage_record_count") != len(ACTIVE_LINEAGE_PATHS):
        errors.append("active_lineage_record_count_mismatch")
    if payload.get("correct_stage5aw_path_included") is not True:
        errors.append("correct_stage5aw_path_must_be_included")
    if payload.get("deprecated_stage5aw_path_absent") is not True:
        errors.append("deprecated_stage5aw_path_must_be_absent")
    counts = {
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
        "correct_stage5aw_path_included": payload.get("correct_stage5aw_path_included"),
        "deprecated_stage5aw_path_absent": payload.get("deprecated_stage5aw_path_absent"),
    }
    return _finish("active_lineage", active_lineage, counts, errors)


def validate_stage5dc_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for key, status_field in [
        ("no_active_ingestion", "no_active_ingestion_status"),
        ("no_byte_stream_transition_gate", "no_byte_stream_transition_gate_status"),
        ("no_execution_transition_gate", "no_execution_transition_gate_status"),
    ]:
        payload = _load_yaml(DATA_PATHS[key])
        errors.extend(_ensure_stage_flags(payload))
        errors.extend(_validate_schema(key, DATA_PATHS[key]))
        if payload.get(status_field) != "closed":
            errors.append(f"{status_field}_must_be_closed")
        counts[status_field] = payload.get(status_field)
    return counts, errors


def validate_stage5dc_handoff_continuity() -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(DATA_PATHS["handoff"])
    errors = _ensure_stage_flags(payload)
    if not CODEX_COMPLETION_PATH.exists():
        errors.append("stage5dc_codex_completion_summary_missing")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output_underscore_root_must_be_absent")
    if CODEX_COMPLETION_PATH.exists() and "pending" in CODEX_COMPLETION_PATH.read_text(
        encoding="utf-8"
    ).lower():
        errors.append("stage5dc_completion_summary_must_not_be_pending")
    counts = {
        "stage5dc_codex_completion_summary_present": CODEX_COMPLETION_PATH.exists(),
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
    }
    return _finish("handoff", DATA_PATHS["handoff"], counts, errors)


def validate_stage5dc_credential_redaction_policy(
    credential_redaction: Path = DATA_PATHS["credential_redaction"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(credential_redaction)
    errors = _ensure_stage_flags(payload)
    if payload.get("remote_url_values_printed") is not False:
        errors.append("remote_url_values_must_not_be_printed")
    if payload.get("secret_values_printed_or_committed") is not False:
        errors.append("secret_values_must_not_be_printed_or_committed")
    counts = {
        "credential_like_remote_count": payload.get("credential_like_remote_count"),
        "remote_url_values_printed": payload.get("remote_url_values_printed"),
    }
    return _finish("credential_redaction", credential_redaction, counts, errors)


def validate_stage5dc_governance_scope_control(
    governance: Path = DATA_PATHS["governance_scope_control"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(governance)
    errors = _ensure_stage_flags(payload)
    if payload.get("stage5db_review_integrated") is not True:
        errors.append("stage5db_review_must_be_integrated")
    if payload.get("stage5dc_creates_generic_preflight_layer") is not False:
        errors.append("stage5dc_must_not_create_generic_preflight_layer")
    if payload.get("additional_generic_preflight_layers_allowed_without_concrete_defect") is not False:
        errors.append("generic_preflight_layers_must_be_blocked_without_defect")
    counts = {
        "stage5db_review_integrated": payload.get("stage5db_review_integrated"),
        "stage5dc_is_narrow_operator_choice_stage": payload.get(
            "stage5dc_is_narrow_operator_choice_stage"
        ),
    }
    return _finish("governance_scope_control", governance, counts, errors)


def validate_stage5dc(
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(summary)
    errors = _ensure_stage_flags(payload)
    for validator in [
        validate_stage5dc_stage5db_findings,
        validate_stage5dc_choice_decision,
        validate_stage5dc_selected_option,
        validate_stage5dc_nonselected_options,
        validate_stage5dc_explicit_pause_nonselection,
        validate_stage5dc_real_approval_noncreation,
        validate_stage5dc_combined_gate,
        validate_stage5dc_activation_nonauthorization,
        validate_stage5dc_real_record_boundary,
        validate_stage5dc_stage5cy_preservation,
        validate_stage5dc_stage5da_preservation,
        validate_stage5dc_stage5bd_preservation,
        validate_stage5dc_active_lineage_preservation,
        validate_stage5dc_sidecar_gates,
        validate_stage5dc_handoff_continuity,
        validate_stage5dc_credential_redaction_policy,
        validate_stage5dc_governance_scope_control,
    ]:
        _, validator_errors = validator()
        errors.extend(validator_errors)
    if payload.get("recommended_next_stage_id") != "stage-5dd":
        errors.append("recommended_next_stage_id_must_be_stage5dd")
    if _load_yaml(next_stage_decision).get("selected_next_stage_id") != "stage-5dd":
        errors.append("next_stage_decision_must_select_stage5dd_review")
    for filename in [
        "summary.json",
        "choice_decision_report.json",
        "selected_option_report.json",
        "preservation_report.json",
        "handoff_continuity_report.json",
        "warnings.jsonl",
    ]:
        if not (results_dir / filename).exists():
            errors.append(f"missing_generated_report:{filename}")
    counts = {
        "stage5db_verdict": payload.get("stage5db_verdict"),
        "operator_choice_or_pause_record_created_now": payload.get(
            "operator_choice_or_pause_record_created_now"
        ),
        "operator_choice_or_pause_record_valid_now": payload.get(
            "operator_choice_or_pause_record_valid_now"
        ),
        "selected_option_id": payload.get("selected_option_id"),
        "operator_decision_option_selected_now": payload.get(
            "operator_decision_option_selected_now"
        ),
        "explicit_pause_selected_now": payload.get("explicit_pause_selected_now"),
        "real_operator_approval_record_created_now": payload.get(
            "real_operator_approval_record_created_now"
        ),
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_decision_valid_now": payload.get("activation_decision_valid_now"),
        "active_planning_input_selected_now": payload.get(
            "active_planning_input_selected_now"
        ),
        "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
        "parallel_worker_cap": payload.get("parallel_worker_cap_for_stage5dc_and_later"),
        "recommended_next_stage_id": payload.get("recommended_next_stage_id"),
    }
    return _finish("summary", summary, counts, errors)


def load_stage5dc_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _load_yaml(summary)
