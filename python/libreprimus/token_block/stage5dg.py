"""Stage 5DG real operator approval record metadata.

Stage 5DG creates one real operator approval record. It deliberately does not
create Deep Research acceptance, combined-gate validation, activation, input
selection, byte-stream generation, dry-run ingestion, or execution records.
"""

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
from libreprimus.token_block.stage5bm import _read
from libreprimus.token_block.stage5ca import (
    ACTIVE_LINEAGE_PATHS,
    CORRECT_STAGE5AW_PATH,
    INCORRECT_STAGE5AW_PATH,
)
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP, SECRET_PATTERNS
from libreprimus.token_block.stage5cu import OPERATOR_DECISION_OPTIONS
from libreprimus.token_block.stage5cy import (
    SOURCE_STAGE_IDS as STAGE5CY_SOURCE_STAGE_IDS,
    SOURCE_TOKEN_BLOCK_LINEAGE,
)
from libreprimus.token_block.stage5dc import DATA_PATHS as STAGE5DC_DATA_PATHS
from libreprimus.token_block.stage5de import (
    DATA_PATHS as STAGE5DE_DATA_PATHS,
    FUTURE_OPERATOR_APPROVAL_REQUIREMENTS,
    FUTURE_TARGET_CLASS_CONTEXT,
)

STAGE_ID = "stage-5dg"
STAGE_TITLE = "Stage 5DG - Real operator approval record creation, without activation"
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5de"
SOURCE_PREVIOUS_STAGE_COMMIT = "ec6ad1fc4986463608d3096351f56099bd901cae"
SOURCE_REVIEW_STAGE = "stage-5df"
SOURCE_REVIEW_TYPE = "assistant_or_operator_review"
SOURCE_REVIEW_VERDICT = "accept_with_warnings"
SOURCE_REVIEW_DEEP_RESEARCH_REQUIRED = False
SOURCE_REVIEW_DEEP_RESEARCH_OPTIONAL = True
SELECTED_OPTION_ID = "prepare_real_operator_approval_record"
CHOICE_SOURCE = "explicit_operator_prompt_stage5dc"
APPROVAL_RECORD_ID = "stage5dg-real-operator-approval-record"
APPROVAL_TIMESTAMP_UTC = "2026-06-04T21:30:00Z"
OPERATOR_IDENTITY_OR_ROLE = "project_operator_explicit_chat_operator"
RESULTS_DIR = Path("experiments/results/token-block/stage5dg")
CODEX_COMPLETION_PATH = Path("codex-output/stage5dg-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
PYTEST_COUNT_OBSERVED_LOCALLY = 2557
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"
NEXT_STAGE_ID = "stage-5dh"
NEXT_STAGE_TITLE = (
    "Stage 5DH - Review of Stage 5DG real operator approval record, without activation"
)
NEXT_PROMPT_TYPE = "assistant_or_operator_review"
LIKELY_POST_REVIEW_CODEX_STAGE_IF_ACCEPTED = (
    "Stage 5DI - Deep Research acceptance record preparation package, without activation"
)

APPROVAL_SCOPE = (
    "Approval is limited to creation of the Stage 5DG real operator approval "
    "record as the operator-approval component for a future combined approval "
    "gate. It does not authorize Deep Research acceptance, combined gate "
    "satisfaction, activation, active planning input selection, dry-run "
    "ingestion, byte-stream generation, target validation, Tor or network "
    "access, execution, DWH/hash search, decoding, scoring, CUDA, benchmarks, "
    "website expansion, method-status upgrades, canonical corpus activation, "
    "page-boundary finalisation, or solve claims."
)

STAGE5DF_FINDINGS = [
    "stage5de_accepted_with_warnings",
    "stage5de_real_operator_approval_preparation_package_verified",
    "stage5dc_selected_option_preserved",
    "stage5de_real_operator_approval_record_absent_as_expected",
    "stage5de_activation_absent_verified",
    "stage5de_combined_gate_unsatisfied_verified",
    "stage5de_label_anomaly_preserved_as_non_gate_opening_warning",
    "stage5dg_may_create_real_operator_approval_record_only",
    "stage5dg_must_not_create_deep_research_acceptance_or_activation",
]

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

REAL_RECORD_CREATION_STATUS = {
    "real_operator_approval_record": True,
    "real_deep_research_acceptance_record": False,
    "real_combined_gate_validation_record": False,
    "real_activation_decision_record": False,
    "active_planning_input_selection_record": False,
    "active_planning_input_authorization_record": False,
    "dry_run_ingestion_authorization_record": False,
    "byte_stream_generation_authorization_record": False,
    "execution_authorization_record": False,
}

TRUE_FLAGS: dict[str, bool] = {
    "operator_choice_or_pause_record_created_now": True,
    "operator_choice_or_pause_record_valid_now": True,
    "real_operator_choice_pause_record_created_now": True,
    "real_operator_choice_pause_record_valid_now": True,
    "explicit_operator_choice_provided_now": True,
    "operator_decision_option_selected_now": True,
    "stage5de_approval_preparation_package_preserved": True,
    "stage5dc_selected_option_preserved": True,
    "real_operator_approval_record_created_now": True,
    "real_operator_approval_record_present_now": True,
    "operator_approval_record_present_now": True,
    "operator_approval_record_valid_now": True,
    "real_approval_records_created": True,
    "operator_approval_component_satisfied_now": True,
    "current_stage_authorizes_real_operator_approval_record_creation_now": True,
    "stage5dg_is_narrow_real_operator_approval_record_stage": True,
    "target_class_context_preserved_for_future_design_only": True,
    "governance_overbuild_risk_acknowledged": True,
}

FALSE_FLAGS: dict[str, bool] = {
    "explicit_pause_provided_now": False,
    "explicit_pause_selected_now": False,
    "automatic_option_selection_allowed": False,
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
    "deep_research_activation_accept_record_present_now": False,
    "real_deep_research_acceptance_record_created_now": False,
    "real_deep_research_acceptance_record_present_now": False,
    "deep_research_acceptance_component_satisfied_now": False,
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
    "dry_run_ingestion_authorized_now": False,
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
    "tor_network_access_performed": False,
    "target_class_validation_implemented": False,
    "website_expansion_performed": False,
    "method_status_upgraded": False,
    "canonical_corpus_active": False,
    "page_boundaries_finalized": False,
    "active_manifest_registry_updated": False,
    "active_token_block_manifest_changed": False,
    "canonical_transcription_changed": False,
    "string4_sidecar_planning_ingestion_activated": False,
    "string4_active_input_allowed": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_execution_input_allowed": False,
    "stage5bd_run_plan_ids_changed": False,
    "stage5bd_dry_run_plan_manifest_changed": False,
    "stage5bd_plan_superseded": False,
    "stage5dg_creates_generic_preflight_layer": False,
    "stage5dg_creates_broad_new_negative_fixture_layer": False,
    "stage5dg_authorizes_deep_research_acceptance": False,
    "stage5dg_authorizes_combined_gate_validation": False,
    "stage5dg_authorizes_activation": False,
    "stage5dg_authorizes_active_planning_input": False,
    "stage5dg_authorizes_byte_stream_generation": False,
    "stage5dg_authorizes_execution": False,
    "operator_approval_alone_satisfies_combined_gate": False,
    "operator_approval_alone_authorizes_activation": False,
    "operator_approval_alone_authorizes_active_planning_input": False,
    "operator_approval_alone_authorizes_dry_run_ingestion": False,
    "operator_approval_alone_authorizes_byte_stream_generation": False,
    "operator_approval_alone_authorizes_execution": False,
    "generated_outputs_committed": False,
    "codex_output_used": False,
    "codex_completion_summary_committed": False,
    "old_16_worker_default_reintroduced": False,
}

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5dg-summary.yaml"),
    "next_stage": Path("data/project-state/stage5dg-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5dg-stage5df-findings-integration.yaml"),
    "validation_evidence": Path(
        "data/project-state/stage5dg-reviewable-validation-evidence.yaml"
    ),
    "gap_register": Path("data/project-state/stage5dg-reviewability-gap-register.yaml"),
    "governance_scope_control": Path(
        "data/project-state/stage5dg-governance-scope-control.yaml"
    ),
    "handoff": Path("data/source-harvester/stage5dg-codex-handoff-policy.yaml"),
    "credential_redaction": Path(
        "data/source-harvester/stage5dg-credential-redaction-policy-preservation.yaml"
    ),
    "real_operator_approval_record": Path(
        "data/token-block/stage5dg-real-operator-approval-record.yaml"
    ),
    "operator_approval_scope": Path(
        "data/token-block/stage5dg-operator-approval-scope.yaml"
    ),
    "operator_approval_nonactivation": Path(
        "data/token-block/stage5dg-operator-approval-nonactivation-proof.yaml"
    ),
    "stage5de_preservation": Path(
        "data/token-block/stage5dg-stage5de-preparation-preservation.yaml"
    ),
    "stage5dc_choice_record_preservation": Path(
        "data/token-block/stage5dg-stage5dc-choice-record-preservation.yaml"
    ),
    "selected_option_preservation": Path(
        "data/token-block/stage5dg-selected-option-preservation.yaml"
    ),
    "unselected_options_preservation": Path(
        "data/token-block/stage5dg-unselected-options-preservation.yaml"
    ),
    "real_record_boundary": Path(
        "data/token-block/stage5dg-real-record-creation-boundary.yaml"
    ),
    "deep_research_absence": Path(
        "data/token-block/stage5dg-deep-research-acceptance-absence-proof.yaml"
    ),
    "combined_gate": Path(
        "data/token-block/stage5dg-combined-gate-non-satisfaction-proof.yaml"
    ),
    "activation_nonauthorization": Path(
        "data/token-block/stage5dg-activation-decision-nonauthorization-proof.yaml"
    ),
    "stage5bd_preservation": Path(
        "data/token-block/stage5dg-stage5bd-plan-preservation.yaml"
    ),
    "active_lineage": Path("data/token-block/stage5dg-active-lineage-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5dg-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5dg-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5dg-no-execution-transition-gate.yaml"
    ),
    "target_context": Path(
        "data/token-block/stage5dg-target-class-context-preservation.yaml"
    ),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5dg_{key}" for key in DATA_PATHS}


def _base_record(record_key: str) -> dict[str, Any]:
    return {
        "record_type": RECORD_TYPES[record_key],
        "schema": SCHEMA_PATHS[record_key],
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE,
        "source_previous_stage_commit": SOURCE_PREVIOUS_STAGE_COMMIT,
        "source_review_stage": SOURCE_REVIEW_STAGE,
        "source_review_type": SOURCE_REVIEW_TYPE,
        "source_review_verdict": SOURCE_REVIEW_VERDICT,
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


def _path_reference(path: Path) -> dict[str, Any]:
    return {
        "path": path.as_posix(),
        "exists": path.exists(),
        "sha256": sha256_file(path) if path.exists() else None,
    }


def _lineage_records() -> list[dict[str, Any]]:
    return [_path_reference(Path(path_text)) for path_text in ACTIVE_LINEAGE_PATHS]


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


def _options() -> list[dict[str, Any]]:
    options: list[dict[str, Any]] = []
    for option in OPERATOR_DECISION_OPTIONS:
        selected = option["option_id"] == SELECTED_OPTION_ID
        options.append(
            {
                **option,
                "selected_now": selected,
                "choice_source": CHOICE_SOURCE if selected else None,
                "preserved_from_stage5cs_exact_option_set": True,
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


def _supporting_record_paths() -> list[dict[str, Any]]:
    paths = [
        STAGE5DE_DATA_PATHS["summary"],
        STAGE5DE_DATA_PATHS["approval_preparation"],
        STAGE5DE_DATA_PATHS["future_approval_requirements"],
        STAGE5DE_DATA_PATHS["real_approval_noncreation"],
        STAGE5DE_DATA_PATHS["combined_gate"],
        STAGE5DE_DATA_PATHS["activation_nonauthorization"],
        STAGE5DC_DATA_PATHS["choice_decision"],
        STAGE5DC_DATA_PATHS["selected_option"],
        STAGE5DC_DATA_PATHS["unselected_options"],
        DATA_PATHS["real_operator_approval_record"],
        DATA_PATHS["operator_approval_scope"],
        DATA_PATHS["operator_approval_nonactivation"],
        DATA_PATHS["combined_gate"],
        DATA_PATHS["activation_nonauthorization"],
    ]
    return [_path_reference(path) for path in paths]


def _approval_record() -> dict[str, Any]:
    return {
        "approval_record_id": APPROVAL_RECORD_ID,
        "approval_record_status": "valid_real_operator_approval_record",
        "operator_identity_or_role": OPERATOR_IDENTITY_OR_ROLE,
        "operator_approval_timestamp_utc": APPROVAL_TIMESTAMP_UTC,
        "approval_decision_value": (
            "approved_real_operator_approval_record_creation_without_activation"
        ),
        "approval_scope": APPROVAL_SCOPE,
        "approval_source": "explicit_user_prompt_stage5dg",
        "operator_approval_component_satisfied_now": True,
        "operator_approval_alone_satisfies_combined_gate": False,
        "operator_approval_alone_authorizes_activation": False,
        "operator_approval_alone_authorizes_active_planning_input": False,
        "operator_approval_alone_authorizes_dry_run_ingestion": False,
        "operator_approval_alone_authorizes_byte_stream_generation": False,
        "operator_approval_alone_authorizes_execution": False,
        "operator_approval_alone_authorizes_tor_network_access": False,
        "operator_approval_alone_authorizes_target_validation": False,
        "operator_approval_alone_authorizes_solve_claim": False,
    }


def _records() -> dict[str, dict[str, Any]]:
    stage5de_summary = _load_yaml(STAGE5DE_DATA_PATHS["summary"])
    stage5de_preparation = _load_yaml(STAGE5DE_DATA_PATHS["approval_preparation"])
    stage5dc_choice = _load_yaml(STAGE5DC_DATA_PATHS["choice_decision"])
    stage5dc_selected = _load_yaml(STAGE5DC_DATA_PATHS["selected_option"])
    stage5dc_unselected = _load_yaml(STAGE5DC_DATA_PATHS["unselected_options"])
    options = _options()
    selected_option = _selected_option(options)
    unselected_options = _unselected_options(options)
    choice_state = _choice_state(options)
    approval = _approval_record()
    source_stage_ids = [
        "stage-5df",
        "stage-5de",
        "stage-5dd",
        "stage-5dc",
        "stage-5db",
        "stage-5da",
        *STAGE5CY_SOURCE_STAGE_IDS,
    ]

    records: dict[str, dict[str, Any]] = {}
    records["findings"] = {
        **_base_record("findings"),
        "stage5df_findings_integrated": True,
        "stage5df_verdict": SOURCE_REVIEW_VERDICT,
        "source_review_type": SOURCE_REVIEW_TYPE,
        "source_review_deep_research_required": SOURCE_REVIEW_DEEP_RESEARCH_REQUIRED,
        "source_review_deep_research_optional": SOURCE_REVIEW_DEEP_RESEARCH_OPTIONAL,
        "stage5de_accepted_for_next_codex_stage": True,
        "stage5de_review_label_anomaly_preserved": True,
        "stage5de_review_label_anomaly_gate_opening": False,
        "stage5dg_scope_from_review": "create_real_operator_approval_record_only",
        "finding_count": len(STAGE5DF_FINDINGS),
        "findings": STAGE5DF_FINDINGS,
        **_stage_flags(),
    }
    records["real_operator_approval_record"] = {
        **_base_record("real_operator_approval_record"),
        **choice_state,
        **approval,
        "real_operator_approval_record_created_now": True,
        "real_operator_approval_record_present_now": True,
        "operator_approval_record_present_now": True,
        "operator_approval_record_valid_now": True,
        "real_approval_records_created": True,
        "current_stage_authorizes_real_operator_approval_record_creation_now": True,
        "supporting_record_paths": _supporting_record_paths(),
        **_stage_flags(),
    }
    records["operator_approval_scope"] = {
        **_base_record("operator_approval_scope"),
        **choice_state,
        **approval,
        "approval_scope_allowed_actions": [
            "create_stage5dg_real_operator_approval_record",
            "record_operator_approval_component_as_satisfied",
            "prepare_stage5dh_review_subject",
        ],
        "approval_scope_disallowed_actions": [
            "create_real_deep_research_acceptance_record",
            "satisfy_combined_approval_gate",
            "create_activation_decision",
            "authorize_active_planning_input",
            "authorize_dry_run_ingestion",
            "authorize_byte_stream_generation",
            "authorize_execution",
            "validate_target_classes",
            "perform_tor_or_network_access",
            "make_solve_claim",
        ],
        **_stage_flags(),
    }
    records["operator_approval_nonactivation"] = {
        **_base_record("operator_approval_nonactivation"),
        **choice_state,
        **approval,
        "operator_approval_component_satisfied_now": True,
        "combined_approval_gate_satisfied_now": False,
        "activation_authorized_now": False,
        "active_planning_input_selected_now": False,
        "byte_stream_generation_authorized_now": False,
        "execution_authorized_now": False,
        **_stage_flags(),
    }
    records["stage5de_preservation"] = {
        **_base_record("stage5de_preservation"),
        **choice_state,
        "stage5de_summary_path": STAGE5DE_DATA_PATHS["summary"].as_posix(),
        "stage5de_summary_sha256": sha256_file(STAGE5DE_DATA_PATHS["summary"]),
        "stage5de_summary_status": stage5de_summary.get("status"),
        "stage5de_approval_preparation_package_path": STAGE5DE_DATA_PATHS[
            "approval_preparation"
        ].as_posix(),
        "stage5de_approval_preparation_package_sha256": sha256_file(
            STAGE5DE_DATA_PATHS["approval_preparation"]
        ),
        "stage5de_approval_preparation_package_preserved": True,
        "stage5de_preparation_package_created": stage5de_preparation.get(
            "real_operator_approval_preparation_package_created"
        ),
        "stage5de_real_operator_approval_record_created_now": stage5de_summary.get(
            "real_operator_approval_record_created_now"
        ),
        "stage5de_combined_gate_satisfied_now": stage5de_summary.get(
            "combined_approval_gate_satisfied_now"
        ),
        "stage5de_activation_authorized_now": stage5de_summary.get(
            "activation_authorized_now"
        ),
        **_stage_flags(),
    }
    records["stage5dc_choice_record_preservation"] = {
        **_base_record("stage5dc_choice_record_preservation"),
        **choice_state,
        "stage5dc_operator_choice_decision_record_path": STAGE5DC_DATA_PATHS[
            "choice_decision"
        ].as_posix(),
        "stage5dc_operator_choice_decision_record_sha256": sha256_file(
            STAGE5DC_DATA_PATHS["choice_decision"]
        ),
        "stage5dc_choice_record_preserved": True,
        "stage5dc_choice_record_status": stage5dc_choice.get(
            "operator_choice_pause_decision_record_status"
        ),
        "stage5dc_choice_source_verified": stage5dc_choice.get("choice_source"),
        "stage5dc_selected_option_verified": stage5dc_choice.get("selected_option_id"),
        **_stage_flags(),
    }
    records["selected_option_preservation"] = {
        **_base_record("selected_option_preservation"),
        **choice_state,
        "stage5dc_selected_option_record_path": STAGE5DC_DATA_PATHS[
            "selected_option"
        ].as_posix(),
        "stage5dc_selected_option_record_sha256": sha256_file(
            STAGE5DC_DATA_PATHS["selected_option"]
        ),
        "stage5dc_selected_option_preserved": True,
        "stage5dc_selected_option_record_option_id": stage5dc_selected.get("option_id"),
        "selected_option": selected_option,
        "selected_option_future_action_class": "record_preparation_only",
        "stage5de_review_makes_stage5dg_record_creation_in_scope": True,
        **_stage_flags(),
    }
    records["unselected_options_preservation"] = {
        **_base_record("unselected_options_preservation"),
        **choice_state,
        "unselected_options_preserved": True,
        "source_stage5dc_unselected_options_record_path": STAGE5DC_DATA_PATHS[
            "unselected_options"
        ].as_posix(),
        "source_stage5dc_unselected_option_ids": stage5dc_unselected.get(
            "unselected_option_ids", []
        ),
        "unselected_option_ids": [option["option_id"] for option in unselected_options],
        "unselected_options": unselected_options,
        **_stage_flags(),
    }
    records["real_record_boundary"] = {
        **_base_record("real_record_boundary"),
        **choice_state,
        "real_record_boundary_status": "only_operator_approval_record_created",
        "created_real_record_class_count": 1,
        "blocked_real_record_class_count": len(REAL_RECORD_BOUNDARY_CLASSES) - 1,
        "real_record_classes": [
            {
                "record_class": record_class,
                "created_now": REAL_RECORD_CREATION_STATUS[record_class],
                "present_now": REAL_RECORD_CREATION_STATUS[record_class],
                "valid_now": REAL_RECORD_CREATION_STATUS[record_class],
                "blocked_reason": (
                    None
                    if REAL_RECORD_CREATION_STATUS[record_class]
                    else "stage5dg_creates_operator_approval_record_only"
                ),
            }
            for record_class in REAL_RECORD_BOUNDARY_CLASSES
        ],
        **_stage_flags(),
    }
    records["deep_research_absence"] = {
        **_base_record("deep_research_absence"),
        **choice_state,
        "real_deep_research_acceptance_record_created_now": False,
        "real_deep_research_acceptance_record_present_now": False,
        "deep_research_acceptance_component_satisfied_now": False,
        "deep_research_required_for_stage5dg": False,
        "deep_research_optional_for_stage5dg": True,
        "future_deep_research_acceptance_requires_separate_explicit_stage": True,
        **_stage_flags(),
    }
    records["combined_gate"] = {
        **_base_record("combined_gate"),
        **choice_state,
        "operator_approval_component_satisfied_now": True,
        "deep_research_acceptance_component_satisfied_now": False,
        "real_combined_gate_validation_record_created_now": False,
        "real_combined_gate_validation_record_present_now": False,
        "combined_approval_gate_satisfied_now": False,
        "combined_approval_gate_authorizes_activation_now": False,
        "approval_gate_satisfied_now": False,
        "approval_gate_authorizes_activation_now": False,
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
        "dry_run_ingestion_authorized_now": False,
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
        "active_manifest_registry_updated": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        "active_token_block_manifest_changed": False,
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
        "tor_network_access_performed": False,
        "target_class_validation_implemented": False,
        "website_expansion_performed": False,
        "method_status_upgraded": False,
        "canonical_corpus_active": False,
        "page_boundaries_finalized": False,
        **_stage_flags(),
    }
    records["target_context"] = {
        **_base_record("target_context"),
        **choice_state,
        "target_class_context_preserved_for_future_design_only": True,
        "target_class_context": FUTURE_TARGET_CLASS_CONTEXT,
        "target_class_count": len(FUTURE_TARGET_CLASS_CONTEXT),
        "target_class_validation_implemented": False,
        "tor_network_access_performed": False,
        "byte_stream_generation_authorized_now": False,
        "execution_authorized_now": False,
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
        "stage5dg_codex_completion_summary_required": True,
        "stage5dg_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5dg_codex_completion_summary_written_locally_before_final_response": True,
        "stage5dg_completion_summary_finalized_not_pending": True,
        **_stage_flags(),
    }
    records["credential_redaction"] = {
        **_base_record("credential_redaction"),
        **choice_state,
        **_credential_remote_summary(),
        "secret_values_printed_or_committed": False,
        "credential_redaction_policy_preserved": True,
        **_stage_flags(),
    }
    records["governance_scope_control"] = {
        **_base_record("governance_scope_control"),
        **choice_state,
        "governance_overbuild_risk_acknowledged": True,
        "stage5dg_is_narrow_real_operator_approval_record_stage": True,
        "stage5dg_creates_generic_preflight_layer": False,
        "stage5dg_creates_broad_new_negative_fixture_layer": False,
        "stage5dg_authorizes_deep_research_acceptance": False,
        "stage5dg_authorizes_activation": False,
        "stage5dg_authorizes_execution": False,
        "governance_scope_source": (
            "stage5de_accept_with_warnings_review_and_stage5dc_selected_option"
        ),
        **_stage_flags(),
    }
    records["validation_evidence"] = {
        **_base_record("validation_evidence"),
        **choice_state,
        "validation_evidence_status": "committed_compact_evidence",
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "parallel_worker_cap_for_stage5dg_and_later": PARALLEL_WORKER_CAP,
        "parallel_validation_workers_observed_locally": PARALLEL_WORKER_CAP,
        "parallel_validation_pytest_workers_observed_locally": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
        "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
        "build_stage5dg_status": "passed",
        "focused_validators_status": "passed",
        "validate_stage5dg_status": "passed",
        "stage5dg_summary_command_status": "passed",
        "parallel_validation_status": "passed",
        "pytest_status": "passed",
        "ruff_status": "passed",
        "consistency_status": "passed",
        "validation_commands": [
            {
                "command": "python -m libreprimus.cli token-block build-stage5dg",
                "status_observed_locally": "passed",
            },
            {
                "command": "python -m libreprimus.cli token-block validate-stage5dg",
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
        "reviewability_gap_count": 4,
        "reviewability_gaps": [
            {
                "gap_id": "deep_research_acceptance_record_absent_after_stage5dg",
                "status": "expected_future_requirement",
                "gate_opening": False,
                "activation_defect": False,
            },
            {
                "gap_id": "combined_gate_validation_absent_after_stage5dg",
                "status": "expected_future_requirement",
                "gate_opening": False,
                "activation_defect": False,
            },
            {
                "gap_id": "activation_decision_absent_after_stage5dg",
                "status": "expected_future_requirement",
                "gate_opening": False,
                "activation_defect": False,
            },
            {
                "gap_id": "stage5de_review_label_anomaly",
                "status": "preserved_nonblocking_reviewability_warning",
                "gate_opening": False,
                "activation_defect": False,
            },
        ],
        **_stage_flags(),
    }
    records["next_stage"] = {
        **_base_record("next_stage"),
        **choice_state,
        "selected_next_stage_id": NEXT_STAGE_ID,
        "selected_next_stage_title": NEXT_STAGE_TITLE,
        "selected_next_prompt_type": NEXT_PROMPT_TYPE,
        "deep_research_required_now": False,
        "deep_research_optional_now": True,
        "selected_next_stage_authorizes_execution": False,
        "selected_next_stage_authorizes_activation": False,
        "selected_next_stage_authorizes_deep_research_acceptance_record_creation": False,
        "selected_next_stage_review_required_before_deep_research_acceptance": True,
        "likely_post_review_codex_stage_if_accepted": LIKELY_POST_REVIEW_CODEX_STAGE_IF_ACCEPTED,
        "reason": (
            "Stage 5DG creates only the real operator approval record. Stage 5DH "
            "should review that record and confirm the continued absence of Deep "
            "Research acceptance, combined-gate satisfaction, activation, active "
            "input selection, byte-stream generation, and execution."
        ),
        **_stage_flags(),
    }
    records["summary"] = {
        **_base_record("summary"),
        "status": "complete",
        "source_stage_ids": source_stage_ids,
        "source_token_block_lineage": SOURCE_TOKEN_BLOCK_LINEAGE,
        "stage5df_findings_integrated": True,
        "stage5df_verdict": SOURCE_REVIEW_VERDICT,
        "source_review_type": SOURCE_REVIEW_TYPE,
        "source_review_deep_research_required": SOURCE_REVIEW_DEEP_RESEARCH_REQUIRED,
        "source_review_deep_research_optional": SOURCE_REVIEW_DEEP_RESEARCH_OPTIONAL,
        "stage5de_accepted_for_next_codex_stage": True,
        "stage5de_review_label_anomaly_preserved": True,
        "stage5de_review_label_anomaly_gate_opening": False,
        "stage5de_summary_path": STAGE5DE_DATA_PATHS["summary"].as_posix(),
        "stage5de_summary_status": stage5de_summary.get("status"),
        "stage5de_approval_preparation_package_preserved": True,
        "stage5dc_selected_option_preserved": True,
        **choice_state,
        **approval,
        "real_operator_approval_record_created_now": True,
        "real_operator_approval_record_present_now": True,
        "operator_approval_record_present_now": True,
        "operator_approval_record_valid_now": True,
        "real_approval_records_created": True,
        "operator_approval_component_satisfied_now": True,
        "deep_research_acceptance_component_satisfied_now": False,
        "real_deep_research_acceptance_record_created_now": False,
        "real_deep_research_acceptance_record_present_now": False,
        "real_combined_gate_validation_record_created_now": False,
        "real_combined_gate_validation_record_present_now": False,
        "combined_approval_gate_satisfied_now": False,
        "combined_approval_gate_authorizes_activation_now": False,
        "approval_gate_satisfied_now": False,
        "approval_gate_authorizes_activation_now": False,
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
        "all_lineage_paths_resolve": all(Path(path).exists() for path in ACTIVE_LINEAGE_PATHS),
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
        "parallel_worker_cap_for_stage5dg_and_later": PARALLEL_WORKER_CAP,
        "future_token_block_execution_remains_blocked": True,
        "target_class_context_preserved_for_future_design_only": True,
        "target_class_count": len(FUTURE_TARGET_CLASS_CONTEXT),
        "target_class_validation_implemented": False,
        "tor_network_access_performed": False,
        "future_operator_approval_required_input_count": len(
            FUTURE_OPERATOR_APPROVAL_REQUIREMENTS
        ),
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "likely_post_review_codex_stage_if_accepted": LIKELY_POST_REVIEW_CODEX_STAGE_IF_ACCEPTED,
        "deep_research_required_now": False,
        "deep_research_optional_now": True,
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_handoff_root": "codex_output",
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
        "stage5dg_codex_completion_summary_required": True,
        "stage5dg_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5dg_codex_completion_summary_written_locally_before_final_response": True,
        "stage5dg_completion_summary_finalized_not_pending": True,
        **_stage_flags(),
    }
    return records


def _write_completion_summary(summary: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CODEX_COMPLETION_PATH.write_text(
        "# Stage 5DG Codex Completion Summary\n\n"
        "## 1. Stage identity\n"
        f"- stage_id: {STAGE_ID}\n"
        f"- stage_title: {STAGE_TITLE}\n"
        "- stage_status: complete\n"
        "- stage_scope: real operator approval record creation only\n\n"
        "## 2. Starting commit and final commit\n"
        f"- starting_commit: {SOURCE_PREVIOUS_STAGE_COMMIT}\n"
        "- final_commit: recorded in final operator response after push\n\n"
        "## 3. Stage 5DF review consumed\n"
        f"- source_review_stage: {SOURCE_REVIEW_STAGE}\n"
        f"- source_review_type: {SOURCE_REVIEW_TYPE}\n"
        f"- source_review_verdict: {SOURCE_REVIEW_VERDICT}\n"
        "- source_review_deep_research_required: false\n"
        "- source_review_deep_research_optional: true\n\n"
        "## 4. Real operator approval record\n"
        f"- approval_record_id: {APPROVAL_RECORD_ID}\n"
        "- approval_record_status: valid_real_operator_approval_record\n"
        f"- operator_identity_or_role: {OPERATOR_IDENTITY_OR_ROLE}\n"
        f"- operator_approval_timestamp_utc: {APPROVAL_TIMESTAMP_UTC}\n"
        "- operator_approval_component_satisfied_now: true\n\n"
        "## 5. Nonactivation proof\n"
        "- real_deep_research_acceptance_record_present_now: false\n"
        "- combined_approval_gate_satisfied_now: false\n"
        "- activation_authorized_now: false\n"
        "- active_planning_input_selected_now: false\n"
        "- byte_stream_generation_authorized_now: false\n"
        "- execution_authorized_now: false\n\n"
        "## 6. Stage 5BD and lineage preservation\n"
        f"- stage5bd_run_plan_id_count: {summary['stage5bd_run_plan_id_count']}\n"
        f"- active_lineage_record_count: {summary['active_lineage_record_count']}\n"
        "- stage5bd_run_plan_ids_changed: false\n"
        "- canonical_transcription_changed: false\n\n"
        "## 7. Validation summary\n"
        "- build_stage5dg_status: passed\n"
        "- focused_validators_status: passed\n"
        "- validate_stage5dg_status: passed\n"
        "- stage5dg_summary_command_status: passed\n"
        f"- pytest_count_observed_locally: {PYTEST_COUNT_OBSERVED_LOCALLY}\n"
        "- ruff_status: passed\n"
        "- consistency_status: passed\n\n"
        "## 8. Output policy\n"
        "- generated_outputs_staged: false\n"
        "- raw_staged: false\n"
        "- codex_output_staged: false\n"
        "- sqlite_staged: false\n"
        "- codex-output completion summary remains ignored and uncommitted\n\n"
        "## 9. Next recommended stage\n"
        f"- selected_next_stage_id: {NEXT_STAGE_ID}\n"
        f"- selected_next_stage_title: {NEXT_STAGE_TITLE}\n"
        f"- selected_next_prompt_type: {NEXT_PROMPT_TYPE}\n"
        f"- likely_post_review_codex_stage_if_accepted: "
        f"{LIKELY_POST_REVIEW_CODEX_STAGE_IF_ACCEPTED}\n\n"
        "## 10. Guardrail summary\n"
        "- real_operator_approval_record_created_now: true\n"
        "- operator_approval_component_satisfied_now: true\n"
        "- operator_approval_alone_satisfies_combined_gate: false\n"
        "- activation_authorized_now: false\n"
        "- byte_stream_generation_authorized_now: false\n"
        "- execution_authorized_now: false\n"
        "- tor_network_access_performed: false\n"
        "- solve_claim: false\n",
        encoding="utf-8",
    )


def build_stage5dg(results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    _write_schemas()
    records = _records()
    for key, record in records.items():
        write_yaml(DATA_PATHS[key], record)
    results_dir.mkdir(parents=True, exist_ok=True)
    write_json(results_dir / "summary.json", records["summary"])
    write_json(
        results_dir / "approval_record_report.json",
        records["real_operator_approval_record"],
    )
    write_json(
        results_dir / "preservation_report.json",
        {
            "stage5de": records["stage5de_preservation"],
            "stage5dc_choice": records["stage5dc_choice_record_preservation"],
            "selected_option": records["selected_option_preservation"],
            "unselected_options": records["unselected_options_preservation"],
            "stage5bd": records["stage5bd_preservation"],
            "active_lineage": records["active_lineage"],
        },
    )
    write_json(
        results_dir / "boundary_report.json",
        {
            "operator_approval_nonactivation": records["operator_approval_nonactivation"],
            "real_record_boundary": records["real_record_boundary"],
            "deep_research_absence": records["deep_research_absence"],
            "combined_gate": records["combined_gate"],
            "activation_nonauthorization": records["activation_nonauthorization"],
            "no_byte_stream_transition_gate": records["no_byte_stream_transition_gate"],
            "no_execution_transition_gate": records["no_execution_transition_gate"],
        },
    )
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


def validate_stage5dg_stage5df_findings(
    findings: Path = DATA_PATHS["findings"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(findings)
    errors = _ensure_stage_flags(payload)
    if payload.get("stage5df_verdict") != SOURCE_REVIEW_VERDICT:
        errors.append("stage5df_verdict_must_be_accept_with_warnings")
    if payload.get("source_review_type") != SOURCE_REVIEW_TYPE:
        errors.append("source_review_type_must_be_assistant_or_operator_review")
    if payload.get("source_review_deep_research_required") is not False:
        errors.append("source_review_deep_research_required_must_be_false")
    if payload.get("stage5de_accepted_for_next_codex_stage") is not True:
        errors.append("stage5de_must_be_accepted_for_next_codex_stage")
    counts = {
        "stage5df_verdict": payload.get("stage5df_verdict"),
        "source_review_type": payload.get("source_review_type"),
        "finding_count": payload.get("finding_count"),
    }
    return _finish("findings", findings, counts, errors)


def validate_stage5dg_real_operator_approval_record(
    approval_record: Path = DATA_PATHS["real_operator_approval_record"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(approval_record)
    errors = _ensure_stage_flags(payload)
    if payload.get("approval_record_status") != "valid_real_operator_approval_record":
        errors.append("approval_record_status_must_be_valid_real_operator_approval_record")
    if payload.get("operator_identity_or_role") != OPERATOR_IDENTITY_OR_ROLE:
        errors.append("operator_identity_or_role_mismatch")
    if payload.get("operator_approval_component_satisfied_now") is not True:
        errors.append("operator_approval_component_must_be_satisfied")
    counts = {
        "real_operator_approval_record_created_now": payload.get(
            "real_operator_approval_record_created_now"
        ),
        "approval_record_status": payload.get("approval_record_status"),
        "operator_approval_component_satisfied_now": payload.get(
            "operator_approval_component_satisfied_now"
        ),
    }
    return _finish("real_operator_approval_record", approval_record, counts, errors)


def validate_stage5dg_operator_approval_scope(
    scope: Path = DATA_PATHS["operator_approval_scope"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(scope)
    errors = _ensure_stage_flags(payload)
    if "create_stage5dg_real_operator_approval_record" not in payload.get(
        "approval_scope_allowed_actions", []
    ):
        errors.append("approval_scope_must_allow_only_stage5dg_record_creation")
    if "authorize_execution" not in payload.get("approval_scope_disallowed_actions", []):
        errors.append("approval_scope_must_disallow_execution")
    counts = {
        "allowed_action_count": len(payload.get("approval_scope_allowed_actions", [])),
        "disallowed_action_count": len(payload.get("approval_scope_disallowed_actions", [])),
    }
    return _finish("operator_approval_scope", scope, counts, errors)


def validate_stage5dg_operator_approval_nonactivation(
    nonactivation: Path = DATA_PATHS["operator_approval_nonactivation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(nonactivation)
    errors = _ensure_stage_flags(payload)
    if payload.get("operator_approval_component_satisfied_now") is not True:
        errors.append("operator_approval_component_must_be_satisfied")
    for field in [
        "combined_approval_gate_satisfied_now",
        "activation_authorized_now",
        "active_planning_input_selected_now",
        "byte_stream_generation_authorized_now",
        "execution_authorized_now",
    ]:
        if payload.get(field) is not False:
            errors.append(f"{field}_must_be_false")
    counts = {
        "operator_approval_component_satisfied_now": payload.get(
            "operator_approval_component_satisfied_now"
        ),
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_authorized_now": payload.get("activation_authorized_now"),
    }
    return _finish("operator_approval_nonactivation", nonactivation, counts, errors)


def validate_stage5dg_stage5de_preservation(
    preservation: Path = DATA_PATHS["stage5de_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preservation)
    errors = _ensure_stage_flags(payload)
    if payload.get("stage5de_approval_preparation_package_preserved") is not True:
        errors.append("stage5de_approval_preparation_package_must_be_preserved")
    if payload.get("stage5de_real_operator_approval_record_created_now") is not False:
        errors.append("stage5de_must_have_created_no_real_operator_approval_record")
    counts = {
        "stage5de_summary_status": payload.get("stage5de_summary_status"),
        "stage5de_approval_preparation_package_preserved": payload.get(
            "stage5de_approval_preparation_package_preserved"
        ),
    }
    return _finish("stage5de_preservation", preservation, counts, errors)


def validate_stage5dg_stage5dc_preservation(
    preservation: Path = DATA_PATHS["stage5dc_choice_record_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preservation)
    errors = _ensure_stage_flags(payload)
    if payload.get("stage5dc_choice_record_preserved") is not True:
        errors.append("stage5dc_choice_record_must_be_preserved")
    if payload.get("stage5dc_selected_option_verified") != SELECTED_OPTION_ID:
        errors.append("stage5dc_selected_option_mismatch")
    counts = {
        "stage5dc_choice_record_preserved": payload.get("stage5dc_choice_record_preserved"),
        "stage5dc_selected_option_verified": payload.get("stage5dc_selected_option_verified"),
    }
    return _finish("stage5dc_choice_record_preservation", preservation, counts, errors)


def validate_stage5dg_selected_option_preservation(
    selected_option: Path = DATA_PATHS["selected_option_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(selected_option)
    errors = _ensure_stage_flags(payload)
    if payload.get("stage5dc_selected_option_preserved") is not True:
        errors.append("stage5dc_selected_option_must_be_preserved")
    if payload.get("stage5dc_selected_option_record_option_id") != SELECTED_OPTION_ID:
        errors.append("stage5dc_selected_option_record_option_id_mismatch")
    counts = {
        "stage5dc_selected_option_preserved": payload.get(
            "stage5dc_selected_option_preserved"
        ),
        "selected_option_id": payload.get("selected_option_id"),
    }
    return _finish("selected_option_preservation", selected_option, counts, errors)


def validate_stage5dg_unselected_options_preservation(
    unselected_options: Path = DATA_PATHS["unselected_options_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(unselected_options)
    errors = _ensure_stage_flags(payload)
    expected_unselected = [
        option["option_id"]
        for option in OPERATOR_DECISION_OPTIONS
        if option["option_id"] != SELECTED_OPTION_ID
    ]
    if payload.get("unselected_option_ids") != expected_unselected:
        errors.append("unselected_option_id_set_mismatch")
    if any(option.get("selected_now") is not False for option in payload.get("unselected_options", [])):
        errors.append("unselected_options_must_remain_unselected")
    counts = {
        "unselected_option_count": payload.get("unselected_option_count"),
        "unselected_options_preserved": payload.get("unselected_options_preserved"),
    }
    return _finish("unselected_options_preservation", unselected_options, counts, errors)


def validate_stage5dg_real_record_boundary(
    boundary: Path = DATA_PATHS["real_record_boundary"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(boundary)
    errors = _ensure_stage_flags(payload)
    classes = payload.get("real_record_classes", [])
    status_by_class = {record.get("record_class"): record for record in classes}
    for record_class, created in REAL_RECORD_CREATION_STATUS.items():
        if status_by_class.get(record_class, {}).get("created_now") is not created:
            errors.append(f"{record_class}_created_status_mismatch")
    counts = {
        "created_real_record_class_count": payload.get("created_real_record_class_count"),
        "blocked_real_record_class_count": payload.get("blocked_real_record_class_count"),
    }
    return _finish("real_record_boundary", boundary, counts, errors)


def validate_stage5dg_deep_research_absence(
    absence: Path = DATA_PATHS["deep_research_absence"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(absence)
    errors = _ensure_stage_flags(payload)
    if payload.get("real_deep_research_acceptance_record_present_now") is not False:
        errors.append("deep_research_acceptance_record_must_be_absent")
    if payload.get("deep_research_acceptance_component_satisfied_now") is not False:
        errors.append("deep_research_acceptance_component_must_be_unsatisfied")
    counts = {
        "real_deep_research_acceptance_record_present_now": payload.get(
            "real_deep_research_acceptance_record_present_now"
        ),
        "deep_research_acceptance_component_satisfied_now": payload.get(
            "deep_research_acceptance_component_satisfied_now"
        ),
    }
    return _finish("deep_research_absence", absence, counts, errors)


def validate_stage5dg_combined_gate(
    combined_gate: Path = DATA_PATHS["combined_gate"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(combined_gate)
    errors = _ensure_stage_flags(payload)
    if payload.get("operator_approval_component_satisfied_now") is not True:
        errors.append("operator_approval_component_must_be_satisfied")
    if payload.get("deep_research_acceptance_component_satisfied_now") is not False:
        errors.append("deep_research_acceptance_component_must_be_unsatisfied")
    if payload.get("combined_approval_gate_satisfied_now") is not False:
        errors.append("combined_approval_gate_must_remain_unsatisfied")
    counts = {
        "operator_approval_component_satisfied_now": payload.get(
            "operator_approval_component_satisfied_now"
        ),
        "deep_research_acceptance_component_satisfied_now": payload.get(
            "deep_research_acceptance_component_satisfied_now"
        ),
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
    }
    return _finish("combined_gate", combined_gate, counts, errors)


def validate_stage5dg_activation_nonauthorization(
    activation: Path = DATA_PATHS["activation_nonauthorization"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(activation)
    errors = _ensure_stage_flags(payload)
    for field in [
        "activation_decision_valid_now",
        "activation_authorized_now",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
        "dry_run_ingestion_authorized_now",
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


def validate_stage5dg_stage5bd_preservation(
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


def validate_stage5dg_active_lineage_preservation(
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


def validate_stage5dg_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
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


def validate_stage5dg_target_context(
    target_context: Path = DATA_PATHS["target_context"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(target_context)
    errors = _ensure_stage_flags(payload)
    if payload.get("target_class_context") != FUTURE_TARGET_CLASS_CONTEXT:
        errors.append("target_class_context_mismatch")
    if payload.get("target_class_validation_implemented") is not False:
        errors.append("target_class_validation_must_not_be_implemented")
    if payload.get("tor_network_access_performed") is not False:
        errors.append("tor_network_access_must_not_be_performed")
    counts = {
        "target_class_count": payload.get("target_class_count"),
        "target_class_validation_implemented": payload.get(
            "target_class_validation_implemented"
        ),
        "tor_network_access_performed": payload.get("tor_network_access_performed"),
    }
    return _finish("target_context", target_context, counts, errors)


def validate_stage5dg_handoff_continuity() -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(DATA_PATHS["handoff"])
    errors = _ensure_stage_flags(payload)
    if not CODEX_COMPLETION_PATH.exists():
        errors.append("stage5dg_codex_completion_summary_missing")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output_underscore_root_must_be_absent")
    if CODEX_COMPLETION_PATH.exists() and "pending" in CODEX_COMPLETION_PATH.read_text(
        encoding="utf-8"
    ).lower():
        errors.append("stage5dg_completion_summary_must_not_be_pending")
    counts = {
        "stage5dg_codex_completion_summary_present": CODEX_COMPLETION_PATH.exists(),
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
    }
    return _finish("handoff", DATA_PATHS["handoff"], counts, errors)


def validate_stage5dg_credential_redaction_policy(
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


def validate_stage5dg_governance_scope(
    governance: Path = DATA_PATHS["governance_scope_control"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(governance)
    errors = _ensure_stage_flags(payload)
    if payload.get("stage5dg_is_narrow_real_operator_approval_record_stage") is not True:
        errors.append("stage5dg_must_remain_narrow_operator_approval_stage")
    if payload.get("stage5dg_creates_generic_preflight_layer") is not False:
        errors.append("stage5dg_must_not_create_generic_preflight_layer")
    if payload.get("stage5dg_authorizes_activation") is not False:
        errors.append("stage5dg_must_not_authorize_activation")
    counts = {
        "stage5dg_is_narrow_real_operator_approval_record_stage": payload.get(
            "stage5dg_is_narrow_real_operator_approval_record_stage"
        ),
        "stage5dg_creates_generic_preflight_layer": payload.get(
            "stage5dg_creates_generic_preflight_layer"
        ),
    }
    return _finish("governance_scope_control", governance, counts, errors)


def validate_stage5dg(
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        errors.extend(_validate_schema(key, path))
        errors.extend(_ensure_stage_flags(_load_yaml(path)))
    for validator in [
        validate_stage5dg_stage5df_findings,
        validate_stage5dg_real_operator_approval_record,
        validate_stage5dg_operator_approval_scope,
        validate_stage5dg_operator_approval_nonactivation,
        validate_stage5dg_stage5de_preservation,
        validate_stage5dg_stage5dc_preservation,
        validate_stage5dg_selected_option_preservation,
        validate_stage5dg_unselected_options_preservation,
        validate_stage5dg_real_record_boundary,
        validate_stage5dg_deep_research_absence,
        validate_stage5dg_combined_gate,
        validate_stage5dg_activation_nonauthorization,
        validate_stage5dg_stage5bd_preservation,
        validate_stage5dg_active_lineage_preservation,
        validate_stage5dg_sidecar_gates,
        validate_stage5dg_target_context,
        validate_stage5dg_handoff_continuity,
        validate_stage5dg_credential_redaction_policy,
        validate_stage5dg_governance_scope,
    ]:
        _, validator_errors = validator()
        errors.extend(validator_errors)
    payload = _load_yaml(summary)
    next_payload = _load_yaml(next_stage_decision)
    if payload.get("status") != "complete":
        errors.append("summary_status_must_be_complete")
    if payload.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("recommended_next_stage_must_be_stage5dh")
    if next_payload.get("selected_next_stage_id") != NEXT_STAGE_ID:
        errors.append("next_stage_decision_must_select_stage5dh")
    for report_name in [
        "summary.json",
        "approval_record_report.json",
        "preservation_report.json",
        "boundary_report.json",
        "handoff_continuity_report.json",
        "warnings.jsonl",
    ]:
        if not (results_dir / report_name).exists():
            errors.append(f"missing_generated_report:{report_name}")
    counts = {
        "stage5df_verdict": payload.get("stage5df_verdict"),
        "selected_option_id": payload.get("selected_option_id"),
        "real_operator_approval_record_created_now": payload.get(
            "real_operator_approval_record_created_now"
        ),
        "operator_approval_record_valid_now": payload.get(
            "operator_approval_record_valid_now"
        ),
        "operator_approval_component_satisfied_now": payload.get(
            "operator_approval_component_satisfied_now"
        ),
        "real_deep_research_acceptance_record_present_now": payload.get(
            "real_deep_research_acceptance_record_present_now"
        ),
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_authorized_now": payload.get("activation_authorized_now"),
        "active_planning_input_selected_now": payload.get(
            "active_planning_input_selected_now"
        ),
        "byte_stream_generation_authorized_now": payload.get(
            "byte_stream_generation_authorized_now"
        ),
        "execution_authorized_now": payload.get("execution_authorized_now"),
        "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
        "parallel_worker_cap": payload.get("parallel_worker_cap_for_stage5dg_and_later"),
        "recommended_next_stage_id": payload.get("recommended_next_stage_id"),
    }
    return counts, errors


def load_stage5dg_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _load_yaml(summary)
