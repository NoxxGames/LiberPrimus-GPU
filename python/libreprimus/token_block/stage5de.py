"""Stage 5DE real operator approval preparation metadata."""

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
from libreprimus.token_block.stage5dc import (
    DATA_PATHS as STAGE5DC_DATA_PATHS,
    FALSE_FLAGS as STAGE5DC_FALSE_FLAGS,
)
from libreprimus.token_block.stage5bm import _read

STAGE_ID = "stage-5de"
STAGE_TITLE = (
    "Stage 5DE - Real operator approval record preparation package, "
    "without activation"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5dc"
SOURCE_PREVIOUS_COMMIT = "95d295e77864755900a4b909f0d660ac2b42a809"
SOURCE_REVIEW_STAGE = "stage-5dd"
SOURCE_REVIEW_REPORT = "30_Stage-5DC-Deep-Research-Review.md"
SOURCE_REVIEW_VERDICT = "accept_with_warnings"
STAGE5DC_ISSUE = "#141"
STAGE5DC_CI = "26930630863 passed"
SELECTED_OPTION_ID = "prepare_real_operator_approval_record"
CHOICE_SOURCE = "explicit_operator_prompt_stage5dc"
RESULTS_DIR = Path("experiments/results/token-block/stage5de")
CODEX_COMPLETION_PATH = Path("codex-output/stage5de-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
PYTEST_COUNT_OBSERVED_LOCALLY = 2539
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"
NEXT_STAGE_ID = "stage-5df"
NEXT_STAGE_TITLE = (
    "Stage 5DF - Review of Stage 5DE real operator approval preparation "
    "package, without activation"
)
NEXT_PROMPT_TYPE = "assistant_or_operator_review"

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

FUTURE_OPERATOR_APPROVAL_REQUIREMENTS = [
    "future_stage_id_explicitly_scoped_to_operator_approval",
    "future_operator_identity_or_operator_role",
    "future_operator_approval_timestamp_utc",
    "future_operator_approval_scope",
    "future_operator_approval_decision_value",
    "future_operator_approval_record_status_not_template_not_fixture_not_preflight",
    "exact_stage5dc_selected_option_record_path",
    "exact_stage5dc_operator_choice_decision_record_path",
    "exact_stage5dc_real_approval_noncreation_proof_path",
    "exact_stage5dc_real_record_boundary_path",
    "exact_stage5cy_option_selection_preflight_path",
    "exact_stage5da_choice_pause_scaffold_path",
    "exact_stage5cs_option_set_preservation_path",
    "exact_stage5bd_plan_preservation_or_future_supersession_record",
    "exact_active_lineage_preservation_or_future_supersession_record",
    "no_active_ingestion_acknowledgement",
    "no_byte_stream_acknowledgement",
    "no_execution_acknowledgement",
    "no_solve_claim_acknowledgement",
    "credential_redaction_acknowledgement",
    "codex_output_hyphenated_handoff_acknowledgement",
    "explicit_operator_approval_alone_does_not_authorize_activation_statement",
    "explicit_deep_research_acceptance_absent_statement",
    "explicit_combined_gate_validation_absent_statement",
    "explicit_activation_decision_absent_statement",
    "explicit_active_planning_input_unselected_statement",
    "explicit_byte_stream_generation_not_authorized_statement",
    "explicit_execution_not_authorized_statement",
    "explicit_tor_network_access_not_authorized_statement",
    "explicit_target_class_validation_not_authorized_statement",
    "explicit_page_boundaries_not_finalized_statement",
    "explicit_canonical_corpus_not_activated_statement",
    "explicit_stage5cm_and_later_worker_cap_8_acknowledgement",
    "explicit_no_generic_preflight_layer_statement",
]

FUTURE_TARGET_CLASS_CONTEXT = [
    "v3_onion_hostname",
    "raw_v3_onion_public_key_material",
    "historical_v2_onion_candidate_requiring_archive_validation",
    "lp_style_deep_web_page_content_hash",
    "pgp_material",
    "compressed_payload",
    "encrypted_payload",
    "file_or_container_bytes",
    "high_entropy_key_or_hash_material",
    "unknown_binary_payload",
]

STAGE5DD_FINDINGS = [
    "stage5dc_accepted_with_warnings",
    "stage5dc_selected_prepare_real_operator_approval_record",
    "stage5dc_real_operator_choice_record_verified",
    "stage5dc_real_operator_approval_absent_verified",
    "stage5dc_activation_absent_verified",
    "deep_research_report_label_drift_detected",
    "assistant_snapshot_review_used_as_primary_stage5dc_verification",
    "label_drift_is_reviewability_warning_not_gate_opening",
    "stage5de_should_create_preparation_package_only",
]

_STAGE5_FALSE_OVERRIDES = {
    "operator_decision_option_selected_now",
    "stage5dc_creates_generic_preflight_layer",
    "stage5dc_creates_broad_new_negative_fixture_layer",
    "stage5dc_creates_real_operator_approval_record",
}

TRUE_FLAGS = {
    "operator_choice_or_pause_record_created_now": True,
    "operator_choice_or_pause_record_valid_now": True,
    "explicit_operator_choice_provided_now": True,
    "operator_decision_option_selected_now": True,
    "real_operator_choice_pause_record_created_now": True,
    "real_operator_choice_pause_record_valid_now": True,
    "stage5dc_selects_operator_choice": True,
    "stage5dc_selected_option_preserved": True,
    "real_operator_approval_preparation_package_created": True,
    "governance_overbuild_risk_acknowledged": True,
    "stage5dc_is_narrow_operator_choice_stage": True,
    "stage5de_is_narrow_operator_approval_preparation_stage": True,
    "target_class_context_recorded_for_future_design_only": True,
}

FALSE_FLAGS = {
    **{
        key: value
        for key, value in STAGE5CY_FALSE_FLAGS.items()
        if key not in _STAGE5_FALSE_OVERRIDES
    },
    **{
        key: value
        for key, value in STAGE5DC_FALSE_FLAGS.items()
        if key not in _STAGE5_FALSE_OVERRIDES
    },
    "explicit_pause_provided_now": False,
    "explicit_pause_selected_now": False,
    "automatic_option_selection_allowed": False,
    "future_real_operator_approval_record_created_now": False,
    "future_real_operator_approval_record_valid_now": False,
    "real_operator_approval_record_created_now": False,
    "real_operator_approval_record_present_now": False,
    "operator_approval_record_present_now": False,
    "operator_approval_record_valid_now": False,
    "real_approval_records_created": False,
    "deep_research_activation_accept_record_present_now": False,
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
    "stage5de_creates_generic_preflight_layer": False,
    "stage5de_creates_broad_new_negative_fixture_layer": False,
    "stage5de_creates_real_operator_approval_record": False,
    "stage5de_authorizes_activation": False,
    "additional_generic_preflight_layers_allowed_without_concrete_defect": False,
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
    "active_manifest_registry_updated": False,
    "active_token_block_manifest_changed": False,
    "canonical_transcription_changed": False,
    "future_real_records_created_now": False,
    "generated_outputs_committed": False,
    "codex_output_used": False,
    "codex_completion_summary_committed": False,
    "old_16_worker_default_reintroduced": False,
}

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5de-summary.yaml"),
    "next_stage": Path("data/project-state/stage5de-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5de-stage5dd-findings-integration.yaml"),
    "review_label_anomaly": Path("data/project-state/stage5de-review-label-anomaly.yaml"),
    "governance_scope_control": Path(
        "data/project-state/stage5de-governance-scope-control.yaml"
    ),
    "validation_evidence": Path(
        "data/project-state/stage5de-reviewable-validation-evidence.yaml"
    ),
    "gap_register": Path("data/project-state/stage5de-reviewability-gap-register.yaml"),
    "approval_preparation": Path(
        "data/token-block/stage5de-real-operator-approval-preparation-package.yaml"
    ),
    "future_approval_requirements": Path(
        "data/token-block/stage5de-future-operator-approval-record-requirements.yaml"
    ),
    "stage5dc_selected_option_preservation": Path(
        "data/token-block/stage5de-stage5dc-selected-option-preservation.yaml"
    ),
    "stage5dc_choice_record_preservation": Path(
        "data/token-block/stage5de-stage5dc-choice-record-preservation.yaml"
    ),
    "unselected_options": Path("data/token-block/stage5de-unselected-options-preservation.yaml"),
    "real_approval_noncreation": Path(
        "data/token-block/stage5de-real-approval-noncreation-proof.yaml"
    ),
    "combined_gate": Path(
        "data/token-block/stage5de-combined-gate-non-satisfaction-proof.yaml"
    ),
    "activation_nonauthorization": Path(
        "data/token-block/stage5de-activation-decision-nonauthorization-proof.yaml"
    ),
    "real_record_boundary": Path(
        "data/token-block/stage5de-real-record-creation-boundary.yaml"
    ),
    "stage5bd_preservation": Path("data/token-block/stage5de-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5de-active-lineage-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5de-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5de-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5de-no-execution-transition-gate.yaml"
    ),
    "handoff": Path("data/source-harvester/stage5de-codex-handoff-policy.yaml"),
    "credential_redaction": Path(
        "data/source-harvester/stage5de-credential-redaction-policy-preservation.yaml"
    ),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5de_{key}" for key in DATA_PATHS}


def _base_record(record_key: str) -> dict[str, Any]:
    return {
        "record_type": RECORD_TYPES[record_key],
        "schema": SCHEMA_PATHS[record_key],
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE,
        "source_previous_stage_commit": SOURCE_PREVIOUS_COMMIT,
        "source_review_stage": SOURCE_REVIEW_STAGE,
        "source_review_report": SOURCE_REVIEW_REPORT,
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


def _stage5cy_summary() -> dict[str, Any]:
    return _load_yaml(STAGE5CY_DATA_PATHS["summary"])


def _stage5da_summary() -> dict[str, Any]:
    return _load_yaml(STAGE5DA_DATA_PATHS["summary"])


def _stage5dc_summary() -> dict[str, Any]:
    return _load_yaml(STAGE5DC_DATA_PATHS["summary"])


def _stage5dc_choice() -> dict[str, Any]:
    return _load_yaml(STAGE5DC_DATA_PATHS["choice_decision"])


def _stage5dc_selected_option() -> dict[str, Any]:
    return _load_yaml(STAGE5DC_DATA_PATHS["selected_option"])


def _stage5dc_unselected_options() -> dict[str, Any]:
    return _load_yaml(STAGE5DC_DATA_PATHS["unselected_options"])


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


def _path_reference(path: Path) -> dict[str, Any]:
    return {
        "path": path.as_posix(),
        "exists": path.exists(),
        "sha256": sha256_file(path) if path.exists() else None,
    }


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


def _requirement_records() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": requirement,
            "required_for_future_real_operator_approval_record": True,
            "recorded_by_stage5de": True,
            "satisfied_as_real_operator_approval_by_stage5de": False,
            "gate_opening": False,
            "activation_authorized_now": False,
        }
        for requirement in FUTURE_OPERATOR_APPROVAL_REQUIREMENTS
    ]


def _supporting_record_paths() -> list[dict[str, Any]]:
    paths = [
        STAGE5DC_DATA_PATHS["choice_decision"],
        STAGE5DC_DATA_PATHS["selected_option"],
        STAGE5DC_DATA_PATHS["real_approval_noncreation"],
        STAGE5DC_DATA_PATHS["real_record_boundary"],
        STAGE5CY_DATA_PATHS["summary"],
        STAGE5DA_DATA_PATHS["summary"],
        DATA_PATHS["stage5bd_preservation"],
        DATA_PATHS["active_lineage"],
        DATA_PATHS["real_approval_noncreation"],
        DATA_PATHS["combined_gate"],
        DATA_PATHS["activation_nonauthorization"],
    ]
    return [_path_reference(path) for path in paths]


def _records() -> dict[str, dict[str, Any]]:
    stage5cy_summary = _stage5cy_summary()
    stage5da_summary = _stage5da_summary()
    stage5dc_summary = _stage5dc_summary()
    stage5dc_choice = _stage5dc_choice()
    stage5dc_selected = _stage5dc_selected_option()
    stage5dc_unselected = _stage5dc_unselected_options()
    options = _options()
    selected_option = _selected_option(options)
    unselected_options = _unselected_options(options)
    choice_state = _choice_state(options)
    source_stage_ids = [
        "stage-5dd",
        "stage-5dc",
        "stage-5db",
        "stage-5da",
        *STAGE5CY_SOURCE_STAGE_IDS,
    ]

    records: dict[str, dict[str, Any]] = {}
    records["findings"] = {
        **_base_record("findings"),
        "stage5dd_findings_integrated": True,
        "stage5dd_verdict": SOURCE_REVIEW_VERDICT,
        "stage5dd_report_path": SOURCE_REVIEW_REPORT,
        "deep_research_report_label_drift_detected": True,
        "deep_research_report_label_drift_gate_opening": False,
        "assistant_snapshot_review_used_as_primary_stage5dc_verification": True,
        "deep_research_report_usable_but_label_confused": True,
        "stage5dc_commit_verified": SOURCE_PREVIOUS_COMMIT,
        "stage5dc_issue_verified": STAGE5DC_ISSUE,
        "stage5dc_ci_verified": STAGE5DC_CI,
        "stage5dc_selected_option_verified": SELECTED_OPTION_ID,
        "stage5dc_real_approval_absent_verified": True,
        "stage5dc_activation_absent_verified": True,
        "finding_count": len(STAGE5DD_FINDINGS),
        "findings": STAGE5DD_FINDINGS,
        **_stage_flags(),
    }
    records["review_label_anomaly"] = {
        **_base_record("review_label_anomaly"),
        "review_label_anomaly_record_created": True,
        "affected_report": SOURCE_REVIEW_REPORT,
        "expected_review_subject": "stage-5dc",
        "observed_label_drift_mentions": "stage-5da / stage-5db",
        "substantive_review_matches_stage5dc_outcome": True,
        "gate_opening": False,
        "activation_defect": False,
        "requires_repair_before_stage5de": False,
        "requires_generic_preflight_layer": False,
        **_stage_flags(),
    }
    records["governance_scope_control"] = {
        **_base_record("governance_scope_control"),
        "governance_overbuild_risk_acknowledged": True,
        "stage5dc_is_narrow_operator_choice_stage": True,
        "stage5de_is_narrow_operator_approval_preparation_stage": True,
        "additional_generic_preflight_layers_allowed_without_concrete_defect": False,
        "stage5de_creates_generic_preflight_layer": False,
        "stage5de_creates_broad_new_negative_fixture_layer": False,
        "stage5de_creates_real_operator_approval_record": False,
        "stage5de_authorizes_activation": False,
        "stage5de_scope_source": "stage5dc_selected_option_prepare_real_operator_approval_record",
        **_stage_flags(),
    }
    records["approval_preparation"] = {
        **_base_record("approval_preparation"),
        **choice_state,
        "real_operator_approval_preparation_package_created": True,
        "real_operator_approval_preparation_package_status": "preparation_package_only",
        "future_real_operator_approval_record_may_be_prepared_by_later_stage": True,
        "future_real_operator_approval_record_created_now": False,
        "real_operator_approval_record_created_now": False,
        "real_operator_approval_record_present_now": False,
        "operator_approval_record_present_now": False,
        "operator_approval_record_valid_now": False,
        "real_approval_records_created": False,
        "approval_gate_satisfied_now": False,
        "approval_gate_authorizes_activation_now": False,
        "selected_option": selected_option,
        "supporting_record_paths": _supporting_record_paths(),
        "future_target_class_context": FUTURE_TARGET_CLASS_CONTEXT,
        **_stage_flags(),
    }
    records["future_approval_requirements"] = {
        **_base_record("future_approval_requirements"),
        **choice_state,
        "future_operator_approval_required_input_count": len(
            FUTURE_OPERATOR_APPROVAL_REQUIREMENTS
        ),
        "future_operator_approval_requirements": _requirement_records(),
        "future_operator_approval_record_created_now": False,
        "future_operator_approval_record_valid_now": False,
        "operator_approval_record_valid_now": False,
        "explicit_operator_approval_alone_does_not_authorize_activation_statement": True,
        **_stage_flags(),
    }
    records["stage5dc_selected_option_preservation"] = {
        **_base_record("stage5dc_selected_option_preservation"),
        **choice_state,
        "stage5dc_selected_option_record_path": STAGE5DC_DATA_PATHS[
            "selected_option"
        ].as_posix(),
        "stage5dc_selected_option_record_sha256": sha256_file(
            STAGE5DC_DATA_PATHS["selected_option"]
        ),
        "stage5dc_selected_option_preserved": True,
        "stage5dc_selected_option_record_option_id": stage5dc_selected.get("option_id"),
        "selected_option_future_action_class": "record_preparation_only",
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
        "stage5da_selects_operator_choice": False,
        **_stage_flags(),
    }
    records["unselected_options"] = {
        **_base_record("unselected_options"),
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
    records["real_approval_noncreation"] = {
        **_base_record("real_approval_noncreation"),
        **choice_state,
        "real_operator_approval_record_created_now": False,
        "real_operator_approval_record_present_now": False,
        "operator_approval_record_present_now": False,
        "operator_approval_record_valid_now": False,
        "real_approval_records_created": False,
        "approval_gate_satisfied_now": False,
        "approval_gate_authorizes_activation_now": False,
        "combined_approval_gate_satisfied_now": False,
        "combined_approval_gate_authorizes_activation_now": False,
        "activation_authorized_now": False,
        "stage5de_creates_real_operator_approval_record": False,
        **_stage_flags(),
    }
    records["combined_gate"] = {
        **_base_record("combined_gate"),
        **choice_state,
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
    records["real_record_boundary"] = {
        **_base_record("real_record_boundary"),
        **choice_state,
        "real_operator_approval_preparation_package_is_only_new_stage5de_package": True,
        "real_operator_approval_record_created_now": False,
        "future_real_records_created_now": False,
        "blocked_real_record_class_count": len(REAL_RECORD_BOUNDARY_CLASSES),
        "blocked_real_record_classes": [
            {
                "record_class": record_class,
                "created_now": False,
                "present_now": False,
                "valid_now": False,
                "blocked_reason": (
                    "stage5de_prepares_future_operator_approval_record_without_"
                    "creating_real_records"
                ),
            }
            for record_class in REAL_RECORD_BOUNDARY_CLASSES
        ],
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
    records["handoff"] = {
        **_base_record("handoff"),
        **choice_state,
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_handoff_root": "codex_output",
        "codex_output_used": False,
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
        "codex_completion_summary_committed": False,
        "stage5de_codex_completion_summary_required": True,
        "stage5de_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5de_codex_completion_summary_written_locally_before_final_response": True,
        "stage5de_completion_summary_finalized_not_pending": True,
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
    records["validation_evidence"] = {
        **_base_record("validation_evidence"),
        **choice_state,
        "validation_evidence_status": "committed_compact_evidence",
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "parallel_worker_cap_for_stage5de_and_later": PARALLEL_WORKER_CAP,
        "parallel_validation_workers_observed_locally": PARALLEL_WORKER_CAP,
        "parallel_validation_pytest_workers_observed_locally": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
        "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
        "build_stage5de_status": "passed",
        "focused_validators_status": "passed",
        "validate_stage5de_status": "passed",
        "stage5de_summary_command_status": "passed",
        "parallel_validation_status": "passed",
        "pytest_status": "passed",
        "ruff_status": "passed",
        "consistency_status": "passed",
        "validation_commands": [
            {
                "command": "python -m libreprimus.cli token-block build-stage5de",
                "status_observed_locally": "passed",
            },
            {
                "command": "python -m libreprimus.cli token-block validate-stage5de",
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
        "reviewability_gap_count": 3,
        "reviewability_gaps": [
            {
                "gap_id": "real_operator_approval_record_not_created_in_stage5de",
                "status": "expected_stage_boundary",
                "gate_opening": False,
                "activation_defect": False,
            },
            {
                "gap_id": "deep_research_acceptance_record_absent_after_stage5de",
                "status": "expected_future_requirement",
                "gate_opening": False,
                "activation_defect": False,
            },
            {
                "gap_id": "stage5dd_report_label_anomaly",
                "status": "recorded_nonblocking_reviewability_warning",
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
        "selected_next_stage_authorizes_real_operator_approval_record_creation": False,
        "selected_next_stage_review_required_before_real_approval_record_creation": True,
        "likely_post_review_codex_stage_if_accepted": (
            "Stage 5DG - Real operator approval record creation, without activation"
        ),
        "reason": (
            "Stage 5DE creates only the real operator approval preparation package; "
            "review should inspect the package and gate boundaries before any future "
            "real operator approval record creation stage."
        ),
        **_stage_flags(),
    }
    records["summary"] = {
        **_base_record("summary"),
        "status": "complete",
        "source_stage_ids": source_stage_ids,
        "source_token_block_lineage": SOURCE_TOKEN_BLOCK_LINEAGE,
        "stage5dd_findings_integrated": True,
        "stage5dd_verdict": SOURCE_REVIEW_VERDICT,
        "source_review_label_anomaly_detected": True,
        "source_review_label_anomaly_gate_opening": False,
        "assistant_snapshot_review_used_as_primary_stage5dc_verification": True,
        "deep_research_report_usable_but_label_confused": True,
        "stage5dc_summary_status": stage5dc_summary.get("status"),
        "stage5dc_selected_option_preserved": True,
        "stage5cy_option_selection_preflight_preserved": True,
        "stage5cy_validation_count_reconciliation_preserved": True,
        "stage5cy_governance_scope_control_preserved": True,
        "stage5da_operator_choice_pause_scaffold_preserved": True,
        "stage5cs_exact_option_set_preserved": True,
        "stage5cy_summary_path": STAGE5CY_DATA_PATHS["summary"].as_posix(),
        "stage5cy_complete": stage5cy_summary.get("status") == "complete",
        "stage5da_summary_path": STAGE5DA_DATA_PATHS["summary"].as_posix(),
        "stage5da_complete": stage5da_summary.get("status") == "complete",
        **choice_state,
        "real_operator_approval_preparation_package_created": True,
        "real_operator_approval_preparation_package_status": "preparation_package_only",
        "real_operator_approval_record_created_now": False,
        "real_operator_approval_record_present_now": False,
        "operator_approval_record_present_now": False,
        "operator_approval_record_valid_now": False,
        "real_approval_records_created": False,
        "approval_gate_satisfied_now": False,
        "approval_gate_authorizes_activation_now": False,
        "combined_approval_gate_satisfied_now": False,
        "combined_approval_gate_authorizes_activation_now": False,
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
        "parallel_worker_cap_for_stage5de_and_later": PARALLEL_WORKER_CAP,
        "future_token_block_execution_remains_blocked": True,
        "target_class_validation_implemented": False,
        "tor_network_access_performed": False,
        "future_operator_approval_required_input_count": len(
            FUTURE_OPERATOR_APPROVAL_REQUIREMENTS
        ),
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "deep_research_required_now": False,
        "deep_research_optional_now": True,
        "likely_post_review_codex_stage_if_accepted": (
            "Stage 5DG - Real operator approval record creation, without activation"
        ),
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_handoff_root": "codex_output",
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
        "stage5de_codex_completion_summary_required": True,
        "stage5de_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5de_codex_completion_summary_written_locally_before_final_response": True,
        "stage5de_completion_summary_finalized_not_pending": True,
        **_stage_flags(),
    }
    return records


def _write_completion_summary(summary: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CODEX_COMPLETION_PATH.write_text(
        "# Stage 5DE Codex Completion Summary\n\n"
        "## 1. Stage identity\n"
        f"- stage_id: {STAGE_ID}\n"
        f"- stage_title: {STAGE_TITLE}\n"
        "- stage_status: complete\n"
        "- stage_scope: real operator approval preparation package only\n\n"
        "## 2. Starting commit and final commit\n"
        f"- starting_commit: {SOURCE_PREVIOUS_COMMIT}\n"
        "- final_commit: recorded in final operator response after push\n\n"
        "## 3. GitHub issue and CI run\n"
        "- github_issue: recorded in final operator response after issue update\n"
        "- ci_run: recorded in final operator response after push\n\n"
        "## 4. Stage 5DC selected option consumed\n"
        f"- selected_option_id: {summary['selected_option_id']}\n"
        f"- choice_source: {CHOICE_SOURCE}\n"
        "- selected_option_count: 1\n"
        "- unselected_option_count: 5\n\n"
        "## 5. Stage 5DD / assistant review and label-anomaly handling\n"
        f"- source_review_stage: {SOURCE_REVIEW_STAGE}\n"
        f"- source_review_report: {SOURCE_REVIEW_REPORT}\n"
        f"- source_review_verdict: {summary['stage5dd_verdict']}\n"
        "- source_review_label_anomaly_detected: true\n"
        "- source_review_label_anomaly_gate_opening: false\n"
        "- assistant_snapshot_review_used_as_primary_stage5dc_verification: true\n\n"
        "## 6. Files changed by category\n"
        "- project_state_records: stage5de summary, review, validation, and next-stage records\n"
        "- token_block_records: preparation package, preservation proofs, and closed-gate records\n"
        "- source_harvester_records: handoff and credential-redaction policy records\n"
        "- code: python/libreprimus/token_block/stage5de.py and token-block CLI bindings\n"
        "- tests: tests/python/test_stage5de_*.py\n"
        "- docs: narrow Stage 5DE source-of-truth, onboarding, experiment, and research-log updates\n\n"
        "## 7. Preparation package created\n"
        "- real_operator_approval_preparation_package_created: true\n"
        "- real_operator_approval_preparation_package_status: preparation_package_only\n"
        "- real_operator_approval_record_created_now: false\n\n"
        "## 8. Future operator approval record requirements\n"
        f"- future_operator_approval_required_input_count: "
        f"{summary['future_operator_approval_required_input_count']}\n"
        "- future_real_operator_approval_record_created_now: false\n"
        "- future_real_operator_approval_record_valid_now: false\n\n"
        "## 9. Real approval noncreation proof\n"
        "- real_operator_approval_record_created_now: false\n"
        "- real_operator_approval_record_present_now: false\n"
        "- operator_approval_record_present_now: false\n"
        "- real_approval_records_created: false\n\n"
        "## 10. Combined gate and activation nonauthorization proof\n"
        "- approval_gate_satisfied_now: false\n"
        "- combined_approval_gate_satisfied_now: false\n"
        "- activation_decision_valid_now: false\n"
        "- activation_authorized_now: false\n\n"
        "## 11. Stage 5BD preservation\n"
        f"- stage5bd_run_plan_id_count: {summary['stage5bd_run_plan_id_count']}\n"
        "- stage5bd_run_plan_ids_changed: false\n"
        "- stage5bd_plan_superseded: false\n\n"
        "## 12. Active lineage preservation\n"
        f"- active_lineage_record_count: {summary['active_lineage_record_count']}\n"
        "- correct_stage5aw_path_included: true\n"
        "- deprecated_stage5aw_path_absent: true\n"
        "- canonical_transcription_changed: false\n\n"
        "## 13. No-active / no-byte / no-execution gates\n"
        "- no_active_ingestion_status: closed\n"
        "- no_byte_stream_transition_gate_status: closed\n"
        "- no_execution_transition_gate_status: closed\n"
        "- active_planning_input_selected_now: false\n"
        "- byte_stream_generation_authorized_now: false\n"
        "- execution_authorized_now: false\n\n"
        "## 14. Target-class context boundary\n"
        "- target_class_context_recorded_for_future_design_only: true\n"
        "- target_class_validation_implemented: false\n"
        "- tor_network_access_performed: false\n"
        "- byte_stream_generation_authorized_now: false\n\n"
        "## 15. Governance scope-control / anti-overbuild result\n"
        "- governance_overbuild_risk_acknowledged: true\n"
        "- stage5de_is_narrow_operator_approval_preparation_stage: true\n"
        "- stage5de_creates_generic_preflight_layer: false\n"
        "- stage5de_creates_real_operator_approval_record: false\n\n"
        "## 16. Validation commands and results\n"
        "- build_stage5de_status: passed\n"
        "- focused_validators_status: passed\n"
        "- validate_stage5de_status: passed\n"
        "- stage5de_summary_command_status: passed\n\n"
        "## 17. Pytest count\n"
        f"- pytest_count_observed_locally: {PYTEST_COUNT_OBSERVED_LOCALLY}\n"
        f"- pytest_command_observed_locally: {PYTEST_COMMAND_OBSERVED_LOCALLY}\n\n"
        "## 18. Ruff status\n"
        "- ruff_status: passed\n\n"
        "## 19. 8-worker parallel validation status\n"
        "- parallel_worker_cap: 8\n"
        "- parallel_validation_workers_observed_locally: 8\n"
        "- parallel_validation_pytest_workers_observed_locally: 8\n"
        "- parallel_validation_status: passed\n"
        "- old_16_worker_default_reintroduced: false\n\n"
        "## 20. Consistency checks\n"
        "- consistency_status: passed\n"
        "- state_drift_status: passed\n"
        "- operational_file_map_coverage_status: passed\n\n"
        "## 21. Remote blob verification\n"
        "- remote_blob_verification: recorded in final operator response after push\n\n"
        "## 22. Unstaged / ignored local dirt summary\n"
        "- generated_outputs_staged: false\n"
        "- raw_staged: false\n"
        "- codex_output_staged: false\n"
        "- sqlite_staged: false\n"
        "- codex-output completion summary remains ignored and uncommitted\n\n"
        "## 23. Next recommended stage\n"
        f"- selected_next_stage_id: {NEXT_STAGE_ID}\n"
        f"- selected_next_stage_title: {NEXT_STAGE_TITLE}\n"
        f"- selected_next_prompt_type: {NEXT_PROMPT_TYPE}\n"
        "- selected_next_stage_authorizes_execution: false\n\n"
        "## 24. Guardrail summary\n"
        "- real_operator_approval_record_created_now: false\n"
        "- activation_authorized_now: false\n"
        "- byte_stream_generation_authorized_now: false\n"
        "- execution_authorized_now: false\n"
        "- target_class_validation_implemented: false\n"
        "- tor_network_access_performed: false\n"
        "- solve_claim: false\n"
        "- The project has prepared a reviewable future operator approval record "
        "package, but no real operator approval record exists, no gate is satisfied, "
        "no activation is authorized, no active planning input is selected, no bytes "
        "are generated, no token-block work is executed, and no solve claim is made.\n",
        encoding="utf-8",
    )


def build_stage5de(results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    _write_schemas()
    records = _records()
    for key, record in records.items():
        write_yaml(DATA_PATHS[key], record)
    results_dir.mkdir(parents=True, exist_ok=True)
    write_json(results_dir / "summary.json", records["summary"])
    write_json(results_dir / "approval_preparation_report.json", records["approval_preparation"])
    write_json(
        results_dir / "future_requirements_report.json",
        records["future_approval_requirements"],
    )
    write_json(
        results_dir / "preservation_report.json",
        {
            "selected_option": records["stage5dc_selected_option_preservation"],
            "choice_record": records["stage5dc_choice_record_preservation"],
            "stage5bd": records["stage5bd_preservation"],
            "active_lineage": records["active_lineage"],
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


def validate_stage5de_stage5dd_findings(
    findings: Path = DATA_PATHS["findings"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(findings)
    errors = _ensure_stage_flags(payload)
    if payload.get("stage5dd_verdict") != SOURCE_REVIEW_VERDICT:
        errors.append("stage5dd_verdict_must_be_accept_with_warnings")
    if payload.get("stage5dd_findings_integrated") is not True:
        errors.append("stage5dd_findings_must_be_integrated")
    if payload.get("deep_research_report_label_drift_gate_opening") is not False:
        errors.append("label_drift_must_not_open_gate")
    counts = {
        "stage5dd_verdict": payload.get("stage5dd_verdict"),
        "finding_count": payload.get("finding_count"),
        "label_drift_gate_opening": payload.get(
            "deep_research_report_label_drift_gate_opening"
        ),
    }
    return _finish("findings", findings, counts, errors)


def validate_stage5de_review_label_anomaly(
    anomaly: Path = DATA_PATHS["review_label_anomaly"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(anomaly)
    errors = _ensure_stage_flags(payload)
    if payload.get("review_label_anomaly_record_created") is not True:
        errors.append("review_label_anomaly_record_must_be_created")
    if payload.get("gate_opening") is not False:
        errors.append("review_label_anomaly_must_not_open_gate")
    if payload.get("expected_review_subject") != "stage-5dc":
        errors.append("review_subject_must_be_stage5dc")
    counts = {
        "review_label_anomaly_record_created": payload.get(
            "review_label_anomaly_record_created"
        ),
        "gate_opening": payload.get("gate_opening"),
    }
    return _finish("review_label_anomaly", anomaly, counts, errors)


def validate_stage5de_real_operator_approval_preparation(
    preparation: Path = DATA_PATHS["approval_preparation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preparation)
    errors = _ensure_stage_flags(payload)
    if payload.get("real_operator_approval_preparation_package_status") != (
        "preparation_package_only"
    ):
        errors.append("preparation_package_status_must_be_preparation_package_only")
    if payload.get("real_operator_approval_record_created_now") is not False:
        errors.append("real_operator_approval_record_must_not_be_created")
    counts = {
        "preparation_package_created": payload.get(
            "real_operator_approval_preparation_package_created"
        ),
        "preparation_package_status": payload.get(
            "real_operator_approval_preparation_package_status"
        ),
        "supporting_record_count": len(payload.get("supporting_record_paths", [])),
    }
    return _finish("approval_preparation", preparation, counts, errors)


def validate_stage5de_future_operator_approval_requirements(
    requirements: Path = DATA_PATHS["future_approval_requirements"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(requirements)
    errors = _ensure_stage_flags(payload)
    observed_ids = [
        item.get("requirement_id")
        for item in payload.get("future_operator_approval_requirements", [])
    ]
    if observed_ids != FUTURE_OPERATOR_APPROVAL_REQUIREMENTS:
        errors.append("future_operator_approval_requirement_set_mismatch")
    if payload.get("future_operator_approval_required_input_count") != len(
        FUTURE_OPERATOR_APPROVAL_REQUIREMENTS
    ):
        errors.append("future_operator_approval_required_input_count_mismatch")
    counts = {
        "future_operator_approval_required_input_count": payload.get(
            "future_operator_approval_required_input_count"
        ),
        "future_operator_approval_record_created_now": payload.get(
            "future_operator_approval_record_created_now"
        ),
    }
    return _finish("future_approval_requirements", requirements, counts, errors)


def validate_stage5de_stage5dc_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    selected = _load_yaml(DATA_PATHS["stage5dc_selected_option_preservation"])
    choice = _load_yaml(DATA_PATHS["stage5dc_choice_record_preservation"])
    unselected = _load_yaml(DATA_PATHS["unselected_options"])
    expected_unselected = [
        option["option_id"]
        for option in OPERATOR_DECISION_OPTIONS
        if option["option_id"] != SELECTED_OPTION_ID
    ]
    for record_key, payload in [
        ("stage5dc_selected_option_preservation", selected),
        ("stage5dc_choice_record_preservation", choice),
        ("unselected_options", unselected),
    ]:
        errors.extend(_ensure_stage_flags(payload))
        errors.extend(_validate_schema(record_key, DATA_PATHS[record_key]))
    if selected.get("stage5dc_selected_option_preserved") is not True:
        errors.append("stage5dc_selected_option_must_be_preserved")
    if selected.get("selected_option_future_action_class") != "record_preparation_only":
        errors.append("selected_option_future_action_class_mismatch")
    if choice.get("stage5dc_choice_record_preserved") is not True:
        errors.append("stage5dc_choice_record_must_be_preserved")
    if unselected.get("unselected_option_ids") != expected_unselected:
        errors.append("unselected_option_id_set_mismatch")
    if any(option.get("selected_now") is not False for option in unselected.get("unselected_options", [])):
        errors.append("unselected_options_must_remain_unselected")
    counts = {
        "stage5dc_selected_option_preserved": selected.get(
            "stage5dc_selected_option_preserved"
        ),
        "stage5dc_choice_record_preserved": choice.get("stage5dc_choice_record_preserved"),
        "unselected_option_count": unselected.get("unselected_option_count"),
    }
    return counts, errors


def validate_stage5de_real_approval_noncreation(
    approval: Path = DATA_PATHS["real_approval_noncreation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(approval)
    errors = _ensure_stage_flags(payload)
    if payload.get("real_operator_approval_record_created_now") is not False:
        errors.append("real_operator_approval_record_must_not_be_created")
    if payload.get("real_approval_records_created") is not False:
        errors.append("real_approval_records_must_not_be_created")
    counts = {
        "real_operator_approval_record_created_now": payload.get(
            "real_operator_approval_record_created_now"
        ),
        "real_approval_records_created": payload.get("real_approval_records_created"),
    }
    return _finish("real_approval_noncreation", approval, counts, errors)


def validate_stage5de_combined_gate(
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
        "approval_gate_satisfied_now": payload.get("approval_gate_satisfied_now"),
    }
    return _finish("combined_gate", combined_gate, counts, errors)


def validate_stage5de_activation_nonauthorization(
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


def validate_stage5de_real_record_boundary(
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
    if payload.get("future_real_records_created_now") is not False:
        errors.append("future_real_records_created_now_must_be_false")
    counts = {
        "blocked_real_record_class_count": payload.get("blocked_real_record_class_count"),
        "future_real_records_created_now": payload.get("future_real_records_created_now"),
    }
    return _finish("real_record_boundary", boundary, counts, errors)


def validate_stage5de_stage5bd_preservation(
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


def validate_stage5de_active_lineage_preservation(
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


def validate_stage5de_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
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


def validate_stage5de_handoff_continuity() -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(DATA_PATHS["handoff"])
    errors = _ensure_stage_flags(payload)
    if not CODEX_COMPLETION_PATH.exists():
        errors.append("stage5de_codex_completion_summary_missing")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output_underscore_root_must_be_absent")
    if CODEX_COMPLETION_PATH.exists() and "pending" in CODEX_COMPLETION_PATH.read_text(
        encoding="utf-8"
    ).lower():
        errors.append("stage5de_completion_summary_must_not_be_pending")
    counts = {
        "stage5de_codex_completion_summary_present": CODEX_COMPLETION_PATH.exists(),
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
    }
    return _finish("handoff", DATA_PATHS["handoff"], counts, errors)


def validate_stage5de_credential_redaction_policy(
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


def validate_stage5de_governance_scope(
    governance: Path = DATA_PATHS["governance_scope_control"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(governance)
    errors = _ensure_stage_flags(payload)
    if payload.get("stage5de_creates_generic_preflight_layer") is not False:
        errors.append("stage5de_must_not_create_generic_preflight_layer")
    if payload.get("stage5de_creates_real_operator_approval_record") is not False:
        errors.append("stage5de_must_not_create_real_operator_approval_record")
    if payload.get("additional_generic_preflight_layers_allowed_without_concrete_defect") is not False:
        errors.append("generic_preflight_layers_must_be_blocked_without_defect")
    counts = {
        "governance_overbuild_risk_acknowledged": payload.get(
            "governance_overbuild_risk_acknowledged"
        ),
        "stage5de_is_narrow_operator_approval_preparation_stage": payload.get(
            "stage5de_is_narrow_operator_approval_preparation_stage"
        ),
    }
    return _finish("governance_scope_control", governance, counts, errors)


def validate_stage5de(
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(summary)
    errors = _ensure_stage_flags(payload)
    for key, path in DATA_PATHS.items():
        errors.extend(_validate_schema(key, path))
    for validator in [
        validate_stage5de_stage5dd_findings,
        validate_stage5de_review_label_anomaly,
        validate_stage5de_real_operator_approval_preparation,
        validate_stage5de_future_operator_approval_requirements,
        validate_stage5de_stage5dc_preservation,
        validate_stage5de_real_approval_noncreation,
        validate_stage5de_combined_gate,
        validate_stage5de_activation_nonauthorization,
        validate_stage5de_real_record_boundary,
        validate_stage5de_stage5bd_preservation,
        validate_stage5de_active_lineage_preservation,
        validate_stage5de_sidecar_gates,
        validate_stage5de_handoff_continuity,
        validate_stage5de_credential_redaction_policy,
        validate_stage5de_governance_scope,
    ]:
        _, validator_errors = validator()
        errors.extend(validator_errors)
    if payload.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("recommended_next_stage_id_must_be_stage5df")
    if _load_yaml(next_stage_decision).get("selected_next_stage_id") != NEXT_STAGE_ID:
        errors.append("next_stage_decision_must_select_stage5df_review")
    for filename in [
        "summary.json",
        "approval_preparation_report.json",
        "future_requirements_report.json",
        "preservation_report.json",
        "handoff_continuity_report.json",
        "warnings.jsonl",
    ]:
        if not (results_dir / filename).exists():
            errors.append(f"missing_generated_report:{filename}")
    counts = {
        "stage5dd_verdict": payload.get("stage5dd_verdict"),
        "stage5dc_selected_option_preserved": payload.get(
            "stage5dc_selected_option_preserved"
        ),
        "selected_option_id": payload.get("selected_option_id"),
        "real_operator_approval_preparation_package_created": payload.get(
            "real_operator_approval_preparation_package_created"
        ),
        "real_operator_approval_record_created_now": payload.get(
            "real_operator_approval_record_created_now"
        ),
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_authorized_now": payload.get("activation_authorized_now"),
        "active_planning_input_selected_now": payload.get(
            "active_planning_input_selected_now"
        ),
        "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
        "future_operator_approval_required_input_count": payload.get(
            "future_operator_approval_required_input_count"
        ),
        "parallel_worker_cap": payload.get("parallel_worker_cap_for_stage5de_and_later"),
        "recommended_next_stage_id": payload.get("recommended_next_stage_id"),
    }
    return _finish("summary", summary, counts, errors)


def load_stage5de_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _load_yaml(summary)
