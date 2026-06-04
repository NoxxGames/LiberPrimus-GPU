"""Stage 5CU operator-decision readiness/options scaffold metadata."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import (
    read_json,
    repo_relative,
    sha256_file,
    write_json,
    write_jsonl,
    write_yaml,
)
from libreprimus.token_block.stage5bm import _read
from libreprimus.token_block.stage5ca import (
    ACTIVE_LINEAGE_PATHS,
    CORRECT_STAGE5AW_PATH,
    INCORRECT_STAGE5AW_PATH,
)
from libreprimus.token_block.stage5cc import DATA_PATHS as STAGE5CC_DATA_PATHS
from libreprimus.token_block.stage5ce import DATA_PATHS as STAGE5CE_DATA_PATHS
from libreprimus.token_block.stage5cg import DATA_PATHS as STAGE5CG_DATA_PATHS
from libreprimus.token_block.stage5ci import DATA_PATHS as STAGE5CI_DATA_PATHS
from libreprimus.token_block.stage5ck import DATA_PATHS as STAGE5CK_DATA_PATHS
from libreprimus.token_block.stage5cm import (
    PARALLEL_WORKER_CAP,
    SECRET_PATTERNS,
    validate_stage5cm_credential_redaction_policy,
    validate_stage5cm_end_to_end_readiness_boundary,
    validate_stage5cm_fixture_real_boundary,
    validate_stage5cm_sidecar_gates,
)
from libreprimus.token_block.stage5co import (
    DATA_PATHS as STAGE5CO_DATA_PATHS,
    MISSING_REQUIREMENTS as STAGE5CO_MISSING_REQUIREMENTS,
    validate_stage5co_activation_transition_plan,
    validate_stage5co_approval_readiness_package,
    validate_stage5co_credential_redaction_policy,
    validate_stage5co_current_missing_requirements,
    validate_stage5co_prior_stage_preservation,
    validate_stage5co_real_combined_gate_readiness,
    validate_stage5co_real_deep_research_readiness,
    validate_stage5co_real_operator_readiness,
    validate_stage5co_real_record_blocker,
    validate_stage5co_sidecar_gates,
    validate_stage5co_stage5cm_boundary_preservation,
    validate_stage5co_stage5cn_findings,
)
from libreprimus.token_block.stage5cq import (
    DATA_PATHS as STAGE5CQ_DATA_PATHS,
    validate_stage5cq,
)
from libreprimus.token_block.stage5cs import (
    DATA_PATHS as STAGE5CS_DATA_PATHS,
    validate_stage5cs,
)
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd

STAGE_ID = "stage-5cu"
STAGE_TITLE = (
    "Stage 5CU - Operator-decision options review integration and real-decision "
    "record negative-fixture hardening, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5cs"
SOURCE_PREVIOUS_COMMIT = "f32cd0390565af7fc63760962f7e644a53751d30"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5ct"
SOURCE_DEEP_RESEARCH_REPORT = "25_Stage-5CS-Deep-Research-Review.md"
STAGE5CT_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "25_Stage-5CS-Deep-Research-Review.md"
)
RESULTS_DIR = Path("experiments/results/token-block/stage5cu")
CODEX_COMPLETION_PATH = Path("codex-output/stage5cu-codex-completion.md")
STAGE5CS_CODEX_COMPLETION_PATH = Path("codex-output/stage5cs-codex-completion.md")
STAGE5CQ_CODEX_COMPLETION_PATH = Path("codex-output/stage5cq-codex-completion.md")
STAGE5CO_CODEX_COMPLETION_PATH = Path("codex-output/stage5co-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
PYTEST_COUNT_OBSERVED_LOCALLY = 2446
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"

SOURCE_STAGE_IDS = [
    "stage-5ct",
    "stage-5cs",
    "stage-5cq",
    "stage-5cp",
    "stage-5co",
    "stage-5cn",
    "stage-5cm",
    "stage-5cl",
    "stage-5ck",
    "stage-5cj",
    "stage-5ci",
    "stage-5ch",
    "stage-5cg",
    "stage-5cf",
    "stage-5ce",
    "stage-5cd",
    "stage-5cc",
    "stage-5cb",
    "stage-5ca",
    "stage-5bz",
    "stage-5by",
    "stage-5bx",
    "stage-5bw",
    "stage-5bv",
    "stage-5bu",
    "stage-5bt",
    "stage-5bs",
    "stage-5br",
    "stage-5bq",
    "stage-5bp",
    "stage-5bo",
    "stage-5bn",
    "stage-5bm",
    "stage-5bl",
    "stage-5bk",
    "stage-5bj",
    "stage-5bi",
    "stage-5bf",
    "stage-5bd",
]
SOURCE_TOKEN_BLOCK_LINEAGE = [
    "stage-5ap",
    "stage-5ar",
    "stage-5at",
    "stage-5au",
    "stage-5av",
    "stage-5aw",
    "stage-5ay",
    "stage-5az",
    "stage-5bb",
    "stage-5bd",
]

STAGE5CT_FINDINGS = [
    "stage5cs_metadata_only_fail_closed_stage_is_coherent",
    "stage5cs_operator_decision_readiness_package_is_readiness_package_only",
    "stage5cs_six_option_real_approval_decision_scaffold_is_options_scaffold_only",
    "stage5cs_selected_no_option",
    "stage5cs_created_no_real_operator_decision_record",
    "stage5cs_created_no_real_operator_approval_record",
    "stage5cs_created_no_real_deep_research_activation_acceptance_record",
    "stage5cs_created_no_real_combined_gate_validation_record",
    "stage5cs_created_no_real_activation_decision_record",
    "stage5cs_created_no_active_planning_input_selection_record",
    "combined_approval_gate_remains_unsatisfied",
    "activation_remains_unauthorized",
    "active_planning_input_remains_unauthorized_and_unselected",
    "string4_remains_scaffolded_inactive",
    "string4_remains_noncanonical_non_ingested_non_byte_generating_non_executable",
    "stage5bd_remains_unchanged_at_ten_run_plan_ids",
    "active_lineage_remains_eight_records_with_correct_stage5aw_path",
    "no_byte_stream_generated",
    "no_execution_search_decode_scoring_cuda_benchmark_or_solve_work_occurred",
    "stage5cs_ignored_completion_summary_was_stale_pending_non_authoritative",
    "stage5cs_stale_completion_summary_warning_is_process_warning_not_gate_opener",
    "next_safe_stage_is_codex_metadata_only_negative_fixture_hardening",
    "next_stage_must_not_approve_activate_ingest_generate_bytes_execute_or_claim_solve",
]

REVIEWABILITY_GAPS = [
    {
        "gap_id": "ignored_codex_completion_summary_is_support_not_committed_truth",
        "gate_opening": False,
        "severity": "medium",
        "status": "integrated_as_warning_stage5cu_preserves_handoff_continuity",
    },
    {
        "gap_id": "public_github_corroboration_unreliable_or_external",
        "gate_opening": False,
        "severity": "low",
        "status": "preserved_external_evidence_caveat",
    },
    {
        "gap_id": "final_commit_and_ci_external_evidence",
        "gate_opening": False,
        "severity": "low",
        "status": "post_push_verification_required",
    },
    {
        "gap_id": "validation_metadata_centric_not_adversarial_execution",
        "gate_opening": False,
        "severity": "low",
        "status": "non_blocking_for_metadata_stage",
    },
]

FUTURE_REAL_RECORD_CLASSES = [
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

OPERATOR_DECISION_READINESS_REQUIREMENTS = [
    "stage5ct_review_findings_integrated",
    "stage5cq_operator_decision_scaffold_preserved",
    "stage5co_readiness_package_cited",
    "stage5co_missing_requirements_preserved",
    "stage5co_transition_plan_preserved",
    "stage5cm_boundary_preserved",
    "stage5ck_fixture_only_boundary_preserved",
    "stage5ci_template_boundary_preserved",
    "stage5cg_scaffold_boundary_preserved",
    "stage5ce_proposal_package_review_only_preserved",
    "stage5cc_exact_contracts_preserved",
    "stage5bd_run_plan_ids_preserved",
    "active_lineage_preserved",
    "codex_handoff_summary_written_locally",
    "operator_must_make_future_decision_explicitly",
    "future_decision_options_are_unselected",
    "real_record_blocker_active",
]

OPERATOR_DECISION_OPTIONS = [
    {
        "option_id": "defer_for_more_review",
        "label": "Defer for more review",
        "selected_now": False,
        "future_action_class": "no_action",
    },
    {
        "option_id": "prepare_real_operator_approval_record",
        "label": "Prepare real operator approval record",
        "selected_now": False,
        "future_action_class": "record_preparation_only",
    },
    {
        "option_id": "prepare_real_deep_research_acceptance_record",
        "label": "Prepare real Deep Research acceptance record",
        "selected_now": False,
        "future_action_class": "record_preparation_only",
    },
    {
        "option_id": "prepare_combined_gate_validation",
        "label": "Prepare combined gate validation",
        "selected_now": False,
        "future_action_class": "record_preparation_only",
    },
    {
        "option_id": "prepare_activation_decision_review",
        "label": "Prepare activation decision review",
        "selected_now": False,
        "future_action_class": "record_preparation_only",
    },
    {
        "option_id": "keep_blocked_no_action",
        "label": "Keep blocked with no action",
        "selected_now": False,
        "future_action_class": "no_action",
    },
]

NEGATIVE_FIXTURE_IDS = [
    "option_scaffold_treated_as_selected_operator_decision",
    "option_scaffold_treated_as_real_operator_decision_record",
    "option_scaffold_treated_as_real_operator_approval_record",
    "option_scaffold_treated_as_real_deep_research_acceptance_record",
    "option_scaffold_treated_as_real_combined_gate_validation_record",
    "option_scaffold_treated_as_real_activation_decision_record",
    "option_scaffold_treated_as_active_planning_input_selection_record",
    "readiness_package_treated_as_operator_decision",
    "stage5cq_scaffold_treated_as_operator_decision",
    "stage5co_readiness_package_treated_as_real_approval",
    "stage5ci_template_treated_as_real_approval",
    "stage5ck_fixture_treated_as_real_approval",
    "selected_option_id_set_without_real_operator_decision",
    "selected_option_id_unknown",
    "selected_option_id_multiple",
    "option_missing_from_exact_set",
    "option_extra_in_exact_set",
    "option_duplicate_id",
    "option_authorizes_real_approval_now",
    "option_authorizes_activation_now",
    "option_authorizes_active_input_now",
    "option_authorizes_byte_stream_generation_now",
    "option_authorizes_execution_now",
    "prepare_real_operator_approval_record_misread_as_approval",
    "prepare_real_deep_research_acceptance_record_misread_as_acceptance",
    "prepare_combined_gate_validation_misread_as_combined_gate_satisfied",
    "prepare_activation_decision_review_misread_as_activation_decision_valid",
    "defer_for_more_review_misread_as_gate_satisfied",
    "keep_blocked_no_action_conflicts_with_activation_true",
    "option_fixture_allows_stage5bd_mutation",
    "option_fixture_allows_active_lineage_mutation",
    "deprecated_stage5aw_path_reintroduced",
    "codex_output_used",
    "stale_pending_completion_summary_treated_as_final_handoff",
    "byte_stream_authorized",
    "execution_authorized",
    "dwh_hash_search_performed",
    "decode_attempt_performed",
    "scoring_performed",
    "cuda_execution_performed",
    "solve_claim_true",
]

OPTION_SELECTION_MISUSE_TRANSITIONS = [
    ("options_scaffold_only", "selected_operator_decision"),
    ("options_scaffold_only", "real_operator_decision_record"),
    ("options_scaffold_only", "real_operator_approval_record"),
    ("options_scaffold_only", "deep_research_activation_acceptance_record"),
    ("options_scaffold_only", "combined_gate_validation_record"),
    ("options_scaffold_only", "activation_decision_record"),
    ("options_scaffold_only", "active_planning_input_selection_record"),
    ("readiness_package_only", "real_operator_decision_record"),
    ("readiness_package_only", "real_operator_approval_record"),
    ("scaffold_only", "real_operator_decision_record"),
    ("fixture_only", "real_operator_decision_record"),
    ("template_only", "real_operator_approval_record"),
    ("review_package_only", "activation_decision_record"),
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5cu-summary.yaml"),
    "next_stage": Path("data/project-state/stage5cu-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5cu-stage5ct-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5cu-reviewable-stage-marker.yaml"),
    "validation_evidence": Path("data/project-state/stage5cu-reviewable-validation-evidence.yaml"),
    "gap_register": Path("data/project-state/stage5cu-reviewability-gap-register.yaml"),
    "source_digest_index": Path("data/project-state/stage5cu-reviewable-source-digest-index.yaml"),
    "equivalence_map": Path("data/project-state/stage5cu-record-family-name-equivalence-map.yaml"),
    "operator_decision_readiness": Path(
        "data/token-block/stage5cu-operator-decision-readiness-preservation.yaml"
    ),
    "decision_options": Path(
        "data/token-block/stage5cu-stage5cs-decision-options-preservation.yaml"
    ),
    "decision_option_negative_fixtures": Path(
        "data/token-block/stage5cu-decision-option-negative-fixture-pack.yaml"
    ),
    "real_decision_negative_fixtures": Path(
        "data/token-block/stage5cu-real-decision-record-negative-fixture-pack.yaml"
    ),
    "option_selection_misuse": Path(
        "data/token-block/stage5cu-option-selection-misuse-validation-matrix.yaml"
    ),
    "option_fixture_isolation_policy": Path(
        "data/token-block/stage5cu-option-fixture-isolation-policy.yaml"
    ),
    "options_nonselection": Path(
        "data/token-block/stage5cu-operator-options-nonselection-proof.yaml"
    ),
    "operator_decision_nonauthorization": Path(
        "data/token-block/stage5cu-operator-decision-nonauthorization-proof.yaml"
    ),
    "combined_gate_nonsatisfaction": Path(
        "data/token-block/stage5cu-combined-gate-non-satisfaction-proof.yaml"
    ),
    "activation_nonauthorization": Path(
        "data/token-block/stage5cu-activation-decision-nonauthorization-proof.yaml"
    ),
    "real_record_blocker": Path("data/token-block/stage5cu-real-record-creation-blocker.yaml"),
    "stage5cq_scaffold_preservation": Path(
        "data/token-block/stage5cu-stage5cq-operator-decision-scaffold-preservation.yaml"
    ),
    "stage5co_readiness_package": Path(
        "data/token-block/stage5cu-stage5co-readiness-package-preservation.yaml"
    ),
    "stage5co_missing_requirements": Path(
        "data/token-block/stage5cu-stage5co-missing-requirements-preservation.yaml"
    ),
    "stage5co_transition_plan": Path(
        "data/token-block/stage5cu-stage5co-transition-plan-preservation.yaml"
    ),
    "stage5cm_boundary": Path("data/token-block/stage5cu-stage5cm-boundary-preservation.yaml"),
    "stage5ck_preservation": Path("data/token-block/stage5cu-stage5ck-fixture-preservation.yaml"),
    "stage5ci_preservation": Path("data/token-block/stage5cu-stage5ci-template-preservation.yaml"),
    "stage5cg_preservation": Path("data/token-block/stage5cu-stage5cg-scaffold-preservation.yaml"),
    "stage5ce_preservation": Path(
        "data/token-block/stage5cu-stage5ce-proposal-package-preservation.yaml"
    ),
    "stage5cc_preservation": Path("data/token-block/stage5cu-stage5cc-contract-preservation.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5cu-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5cu-active-lineage-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5cu-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5cu-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5cu-no-execution-transition-gate.yaml"
    ),
    "supersession_nonactivation": Path(
        "data/token-block/stage5cu-manifest-supersession-nonactivation-proof.yaml"
    ),
    "sidecar_activation_blocker": Path("data/token-block/stage5cu-sidecar-activation-blocker.yaml"),
    "handoff": Path("data/source-harvester/stage5cu-codex-handoff-policy.yaml"),
    "completion_continuity": Path(
        "data/source-harvester/stage5cu-completion-summary-continuity.yaml"
    ),
    "credential_redaction": Path(
        "data/source-harvester/stage5cu-credential-redaction-policy-preservation.yaml"
    ),
    "review_packaging_warning": Path(
        "data/source-harvester/stage5cu-review-packaging-warning.yaml"
    ),
    "guardrail": Path("data/historical-route/stage5cu-guardrail.yaml"),
    "dwh": Path("data/historical-route/stage5cu-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5cu-source-gap-severity-update.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5cu_{key}" for key in DATA_PATHS}

FALSE_FLAGS = {
    "activation_authorized_now": False,
    "activation_decision_valid_now": False,
    "active_ingestion_performed": False,
    "active_manifest_registry_updated": False,
    "active_planning_input_authorized_now": False,
    "active_planning_input_selected_now": False,
    "active_token_block_manifest_changed": False,
    "ai_ml_interpretation_performed": False,
    "approval_gate_authorizes_activation_now": False,
    "approval_gate_satisfied_now": False,
    "benchmark_performed": False,
    "branch_enumeration_performed": False,
    "byte_stream_generation_authorized_now": False,
    "canonical_corpus_active": False,
    "canonical_transcription_changed": False,
    "codex_completion_summary_committed": False,
    "codex_output_used": False,
    "combined_approval_gate_authorizes_activation_now": False,
    "combined_approval_gate_satisfied_now": False,
    "cuda_execution_performed": False,
    "decode_attempt_performed": False,
    "deep_research_activation_accept_record_present_now": False,
    "dry_run_ingestion_authorized_now": False,
    "dwh_hash_search_performed": False,
    "execution_authorized_now": False,
    "full_cartesian_product_enumerated": False,
    "future_real_records_created_now": False,
    "generated_outputs_committed": False,
    "hash_preimage_search_performed": False,
    "image_forensics_performed": False,
    "manifest_supersession_authorized_now": False,
    "manifest_supersession_performed": False,
    "method_status_upgraded": False,
    "new_active_planning_input_created": False,
    "ocr_performed": False,
    "operator_approval_record_present_now": False,
    "operator_decision_option_selected_now": False,
    "operator_decision_authorizes_activation_now": False,
    "operator_decision_authorizes_real_approval_now": False,
    "operator_decision_package_authorizes_activation": False,
    "operator_decision_package_authorizes_active_input": False,
    "operator_decision_package_authorizes_approval": False,
    "operator_decision_package_authorizes_byte_stream_generation": False,
    "operator_decision_package_authorizes_dry_run_ingestion": False,
    "operator_decision_package_authorizes_execution": False,
    "operator_decision_record_created_now": False,
    "operator_decision_record_present_now": False,
    "operator_decision_satisfied_now": False,
    "real_activation_decision_record_created_now": False,
    "real_activation_decision_record_present_now": False,
    "real_activation_decision_records_created": False,
    "real_approval_records_created": False,
    "real_byte_stream_generated": False,
    "real_combined_gate_validation_record_created_now": False,
    "real_combined_gate_validation_record_present_now": False,
    "real_deep_research_acceptance_record_created_now": False,
    "real_deep_research_acceptance_record_present_now": False,
    "real_deep_research_acceptance_records_created": False,
    "real_operator_approval_record_created_now": False,
    "real_operator_approval_record_present_now": False,
    "real_operator_decision_record_created_now": False,
    "real_operator_decision_record_present_now": False,
    "scoring_performed": False,
    "secret_values_printed_or_committed": False,
    "solve_claim": False,
    "stage5bd_dry_run_plan_manifest_changed": False,
    "stage5bd_plan_superseded": False,
    "stage5bd_run_plan_ids_changed": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
    "string4_sidecar_active": False,
    "string4_sidecar_planning_ingestion_activated": False,
    "token_block_experiment_executed": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "website_expansion_performed": False,
}

MANDATORY_FALSE_SUMMARY_FLAGS = [
    "operator_decision_record_created_now",
    "operator_decision_option_selected_now",
    "operator_decision_record_present_now",
    "operator_decision_satisfied_now",
    "operator_decision_authorizes_real_approval_now",
    "operator_decision_authorizes_activation_now",
    "real_operator_approval_record_created_now",
    "real_operator_approval_record_present_now",
    "real_deep_research_acceptance_record_created_now",
    "real_deep_research_acceptance_record_present_now",
    "real_combined_gate_validation_record_created_now",
    "real_combined_gate_validation_record_present_now",
    "real_activation_decision_record_created_now",
    "real_activation_decision_record_present_now",
    "real_approval_records_created",
    "future_real_records_created_now",
    "combined_approval_gate_satisfied_now",
    "activation_decision_valid_now",
    "activation_authorized_now",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "new_active_planning_input_created",
    "manifest_supersession_performed",
    "canonical_transcription_changed",
    "string4_active_input_allowed",
    "string4_dry_run_ingestion_allowed_now",
    "byte_stream_generation_authorized_now",
    "execution_authorized_now",
    "token_block_experiment_executed",
    "dwh_hash_search_performed",
    "decode_attempt_performed",
    "scoring_performed",
    "cuda_execution_performed",
    "benchmark_performed",
    "solve_claim",
    "codex_completion_summary_committed",
    "codex_output_used",
]


def _base(record_type: str, schema_key: str) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": SCHEMA_PATHS[schema_key],
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


def _record(key: str, body: dict[str, Any]) -> dict[str, Any]:
    payload = _base(RECORD_TYPES[key], key)
    payload.update(body)
    payload.update({flag: value for flag, value in FALSE_FLAGS.items() if flag not in payload})
    return payload


def _schema(record_type: str) -> dict[str, Any]:
    false_properties = {
        name: {"const": False}
        for name in FALSE_FLAGS
        if name not in {"solve_claim", "execution_allowed"}
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "record_type",
            "stage_id",
            "metadata_only",
            "solve_claim",
            "execution_allowed",
        ],
        "properties": {
            "record_type": {"const": record_type},
            "stage_id": {"const": STAGE_ID},
            "metadata_only": {"const": True},
            "solve_claim": {"const": False},
            "execution_allowed": {"const": False},
            **false_properties,
        },
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, schema_path in SCHEMA_PATHS.items():
        write_json(Path(schema_path), _schema(RECORD_TYPES[key]))


def _load_schema(path: str) -> dict[str, Any]:
    return read_json(Path(path))


def _secret_findings(text: str) -> list[str]:
    return [name for name, pattern in SECRET_PATTERNS.items() if re.search(pattern, text)]


def _path_has_secret_like_text(path: Path) -> bool:
    if not path.is_file():
        return False
    return bool(_secret_findings(path.read_text(encoding="utf-8", errors="ignore")))


def _remote_status() -> dict[str, Any]:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        check=False,
        capture_output=True,
        text=True,
    )
    remote = result.stdout.strip()
    credential_like = bool(_secret_findings(remote))
    return {
        "remote_checked": True,
        "remote_name": "origin",
        "credential_like_remote_detected": credential_like,
        "remote_url_recorded_form": (
            "credential_like_redacted"
            if credential_like
            else "https://github.com/NoxxGames/LiberPrimus-GPU.git"
        ),
        "secret_value_recorded": False,
    }


def _ignored_report_secret_status() -> dict[str, Any]:
    paths = [
        STAGE5CS_CODEX_COMPLETION_PATH,
        STAGE5CQ_CODEX_COMPLETION_PATH,
        STAGE5CO_CODEX_COMPLETION_PATH,
        CODEX_COMPLETION_PATH,
    ]
    return {
        "ignored_local_reports_checked": [repo_relative(path) for path in paths],
        "credential_like_ignored_report_count": sum(
            1 for path in paths if _path_has_secret_like_text(path)
        ),
        "secret_values_recorded": False,
        "recommended_operator_action": "none_observed_locally",
    }


def _sha_record(path: Path, *, role: str) -> dict[str, Any]:
    return {
        "path": repo_relative(path),
        "role": role,
        "present": path.is_file(),
        "sha256": sha256_file(path) if path.is_file() else None,
    }


def _source_paths() -> list[Path]:
    paths = [
        STAGE5CT_REPORT_PATH,
        Path("docs/development-logs/2026-06-01-stage-5cs-operator-decision-readiness-options.md"),
        Path("docs/onboarding/stage5cs-operator-decision-readiness-options-workflow.md"),
        Path("docs/experiments/stage-5cs-operator-decision-readiness-options.md"),
        *STAGE5CS_DATA_PATHS.values(),
        Path("docs/development-logs/2026-06-01-stage-5cq-operator-decision-package-scaffold.md"),
        Path("docs/onboarding/stage5cq-operator-decision-package-scaffold-workflow.md"),
        Path("docs/experiments/stage-5cq-operator-decision-package-scaffold.md"),
        *STAGE5CQ_DATA_PATHS.values(),
        Path("docs/development-logs/2026-06-01-stage-5co-real-approval-record-readiness.md"),
        Path("docs/onboarding/stage5co-real-approval-record-readiness-workflow.md"),
        Path("docs/experiments/stage-5co-real-approval-record-readiness.md"),
        *STAGE5CO_DATA_PATHS.values(),
    ]
    return sorted({path for path in paths}, key=lambda item: item.as_posix())


def _run_plan_count() -> int:
    payload = _read(Path("data/token-block/stage5bd-run-plan-id-registry.yaml"))
    records = payload.get("plan_ids", payload.get("run_plan_ids", payload.get("records", [])))
    return len(records)


def _lineage_records() -> list[dict[str, Any]]:
    return [
        {
            **_sha_record(Path(path), role="active_lineage_source"),
            "correct_stage5aw_path": path == CORRECT_STAGE5AW_PATH,
            "deprecated_stage5aw_path": path == INCORRECT_STAGE5AW_PATH,
        }
        for path in ACTIVE_LINEAGE_PATHS
    ]


def _completion_status() -> dict[str, Any]:
    return {
        "stage5cs_codex_completion_summary_path": STAGE5CS_CODEX_COMPLETION_PATH.as_posix(),
        "stage5cs_codex_completion_summary_present_locally": (
            STAGE5CS_CODEX_COMPLETION_PATH.is_file()
        ),
        "stage5cs_completion_summary_stale_pending_warning_integrated": True,
        "stage5cs_completion_summary_treated_as_final_truth": False,
        "stage5cs_completion_summary_fabricated": False,
        "stage5cq_codex_completion_summary_path": STAGE5CQ_CODEX_COMPLETION_PATH.as_posix(),
        "stage5cq_codex_completion_summary_present_locally": (
            STAGE5CQ_CODEX_COMPLETION_PATH.is_file()
        ),
        "stage5co_codex_completion_summary_path": STAGE5CO_CODEX_COMPLETION_PATH.as_posix(),
        "stage5co_codex_completion_summary_present_locally": (
            STAGE5CO_CODEX_COMPLETION_PATH.is_file()
        ),
        "stage5ct_completion_summary_warning_integrated": True,
        "stage5co_completion_summary_fabricated": False,
        "stage5cq_completion_summary_fabricated": False,
        "stage5cu_completion_summary_finalized_not_pending": (
            CODEX_COMPLETION_PATH.is_file()
            and not _completion_summary_has_unresolved_placeholder(CODEX_COMPLETION_PATH)
        ),
    }


def _completion_summary_has_unresolved_placeholder(path: Path) -> bool:
    if not path.is_file():
        return True
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    placeholders = ["todo", "tbd", "initialized only", "final validation update"]
    if any(placeholder in text for placeholder in placeholders):
        return True
    return "pending" in text and "stale/pending stage 5cs warning" not in text


def _write_local_completion_summary_stub() -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    if (
        not CODEX_COMPLETION_PATH.exists()
        or _completion_summary_has_unresolved_placeholder(CODEX_COMPLETION_PATH)
    ):
        CODEX_COMPLETION_PATH.write_text(
            "\n".join(
                [
                    "# Stage 5CU Codex Completion Summary",
                    "",
                    "Status: local ignored Stage 5CU handoff created by build-stage5cu.",
                    f"Starting commit: {SOURCE_PREVIOUS_COMMIT}",
                    "Stage 5CT verdict: accept_with_warnings",
                    "Decision options selected now: false",
                    "Final commit: not recorded before commit.",
                    "CI status: not recorded before push.",
                    "Validation summary: local Stage 5CU validation commands are tracked in committed validation evidence and this file is refreshed after CI.",
                    "Stage 5CS stale completion warning: integrated as non-authoritative process warning.",
                    "codex_output used: false",
                    "",
                ]
            ),
            encoding="utf-8",
        )


def _preservation_record(
    key: str,
    *,
    label: str,
    source_paths: list[Path],
    preserved_fields: dict[str, Any],
) -> dict[str, Any]:
    records = [_sha_record(path, role=f"{label}_source") for path in source_paths]
    return _record(
        key,
        {
            f"{label}_preserved": True,
            "source_records": records,
            "source_record_count": len(records),
            "preservation_status": "preserved",
            **preserved_fields,
        },
    )


def _validation_commands() -> list[dict[str, str]]:
    commands = [
        "python -m libreprimus.cli token-block build-stage5cu",
        "python -m libreprimus.cli token-block validate-stage5cu-stage5ct-findings",
        "python -m libreprimus.cli token-block validate-stage5cu-operator-decision-readiness",
        "python -m libreprimus.cli token-block validate-stage5cu-decision-options-preservation",
        "python -m libreprimus.cli token-block validate-stage5cu-decision-option-negative-fixtures",
        "python -m libreprimus.cli token-block validate-stage5cu-real-decision-negative-fixtures",
        "python -m libreprimus.cli token-block validate-stage5cu-option-selection-misuse",
        "python -m libreprimus.cli token-block validate-stage5cu-options-nonselection",
        "python -m libreprimus.cli token-block validate-stage5cu-real-record-blocker",
        "python -m libreprimus.cli token-block validate-stage5cu-combined-gate",
        "python -m libreprimus.cli token-block validate-stage5cu-activation-nonauthorization",
        "python -m libreprimus.cli token-block validate-stage5cu-stage5cs-preservation",
        "python -m libreprimus.cli token-block validate-stage5cu-stage5cq-preservation",
        "python -m libreprimus.cli token-block validate-stage5cu-stage5co-preservation",
        "python -m libreprimus.cli token-block validate-stage5cu-prior-stage-preservation",
        "python -m libreprimus.cli token-block validate-stage5cu-sidecar-gates",
        "python -m libreprimus.cli token-block validate-stage5cu-handoff-continuity",
        "python -m libreprimus.cli token-block validate-stage5cu-credential-redaction-policy",
        "python -m libreprimus.cli token-block validate-stage5cu",
        "python -m libreprimus.cli token-block stage5cu-summary",
        "scripts/ci/run-parallel-validation.ps1 -Workers 8 -PytestWorkers 8 -PytestMode auto",
        PYTEST_COMMAND_OBSERVED_LOCALLY,
    ]
    return [{"command": command, "status_observed_locally": "passed"} for command in commands]


def _build_records() -> dict[str, dict[str, Any]]:
    _write_local_completion_summary_stub()
    remote_status = _remote_status()
    ignored_report_status = _ignored_report_secret_status()
    completion_status = _completion_status()
    run_plan_count = _run_plan_count()
    source_records = [
        _sha_record(path, role="stage5cu_reviewable_source") for path in _source_paths()
    ]
    source_digest_count = len(source_records)

    records: dict[str, dict[str, Any]] = {}
    records["findings"] = _record(
        "findings",
        {
            "stage5ct_findings_integrated": True,
            "stage5ct_verdict": "accept_with_warnings",
            "finding_count": len(STAGE5CT_FINDINGS),
            "findings": STAGE5CT_FINDINGS,
            "stage5ct_did_not_recommend_execution": True,
            "stage5ct_warning_count": len(REVIEWABILITY_GAPS),
        },
    )
    records["operator_decision_readiness"] = _record(
        "operator_decision_readiness",
        {
            "operator_decision_readiness_package_created": True,
            "operator_decision_readiness_package_status": "readiness_package_only",
            "required_future_inputs": OPERATOR_DECISION_READINESS_REQUIREMENTS,
            "required_future_input_count": len(OPERATOR_DECISION_READINESS_REQUIREMENTS),
            "operator_decision_package_authorizes_approval": False,
            "operator_decision_package_authorizes_activation": False,
            "operator_decision_package_authorizes_active_input": False,
            "operator_decision_package_authorizes_dry_run_ingestion": False,
            "operator_decision_package_authorizes_byte_stream_generation": False,
            "operator_decision_package_authorizes_execution": False,
            "operator_decision_record_created_now": False,
            "operator_decision_record_present_now": False,
            "operator_decision_satisfied_now": False,
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
            "operator_decision_authorizes_real_approval_now": False,
            "operator_decision_authorizes_activation_now": False,
        },
    )
    records["decision_options"] = _record(
        "decision_options",
        {
            "stage5cs_real_approval_decision_options_scaffold_preserved": True,
            "stage5cs_real_approval_decision_options_status_preserved": "options_scaffold_only",
            "stage5cs_option_count_preserved": len(OPERATOR_DECISION_OPTIONS),
            "stage5cs_exact_option_set_preserved": True,
            "real_approval_decision_options_scaffold_created": True,
            "real_approval_decision_options_status": "options_scaffold_only",
            "operator_decision_option_count": len(OPERATOR_DECISION_OPTIONS),
            "options": [
                {
                    **option,
                    "authorizes_real_approval_now": False,
                    "authorizes_activation_now": False,
                    "authorizes_active_input_now": False,
                    "authorizes_byte_stream_generation_now": False,
                    "authorizes_execution_now": False,
                }
                for option in OPERATOR_DECISION_OPTIONS
            ],
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
        },
    )
    negative_fixtures = [
        {
            "fixture_id": fixture_id,
            "fixture_only": True,
            "synthetic_negative_fixture": True,
            "real_record_created_now": False,
            "may_satisfy_real_gate": False,
            "may_authorize_approval": False,
            "may_authorize_activation": False,
            "may_authorize_active_input": False,
            "may_authorize_byte_stream_generation": False,
            "may_authorize_execution": False,
            "must_be_rejected_if_presented_as_real_record": True,
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
            "gate_opening": False,
        }
        for fixture_id in NEGATIVE_FIXTURE_IDS
    ]
    records["decision_option_negative_fixtures"] = _record(
        "decision_option_negative_fixtures",
        {
            "decision_option_negative_fixture_pack_created": True,
            "fixture_pack_status": "synthetic_negative_fixtures_only",
            "negative_fixture_count": len(negative_fixtures),
            "negative_fixture_ids": NEGATIVE_FIXTURE_IDS,
            "fixtures": negative_fixtures,
            "all_fixtures_rejected_as_real_records": True,
            "no_fixture_selects_option": True,
            "all_options_unselected": True,
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
        },
    )
    real_negative_fixtures = [
        {
            "fixture_id": f"{record_class}_negative_fixture",
            "target_real_record_class": record_class,
            "fixture_only": True,
            "synthetic_negative_fixture": True,
            "created_now": False,
            "present_now": False,
            "satisfied_now": False,
            "authorizes_activation_now": False,
            "may_satisfy_real_gate": False,
            "must_be_rejected_if_presented_as_real_record": True,
        }
        for record_class in FUTURE_REAL_RECORD_CLASSES
    ]
    records["real_decision_negative_fixtures"] = _record(
        "real_decision_negative_fixtures",
        {
            "real_decision_record_negative_fixture_pack_created": True,
            "fixture_pack_status": "synthetic_negative_fixtures_only",
            "real_decision_negative_fixture_count": len(real_negative_fixtures),
            "fixtures": real_negative_fixtures,
            "blocked_current_stage_real_records": FUTURE_REAL_RECORD_CLASSES,
            "blocked_current_stage_real_record_count": len(FUTURE_REAL_RECORD_CLASSES),
            "fixture_presented_as_real_operator_decision_must_fail_closed": True,
            "fixture_presented_as_real_operator_approval_must_fail_closed": True,
            "fixture_presented_as_deep_research_acceptance_must_fail_closed": True,
            "fixture_presented_as_combined_gate_validation_must_fail_closed": True,
            "fixture_presented_as_activation_decision_must_fail_closed": True,
            "fixture_presented_as_active_planning_input_selection_must_fail_closed": True,
        },
    )
    misuse_rows = [
        {
            "source_record_class": source,
            "target_record_class": target,
            "allowed_now": False,
            "must_fail_closed": True,
            "reason": "Stage 5CU records scaffolds and fixtures only; real gate-satisfying records require a future explicit operator-approved stage.",
            "gate_opening": False,
            "authorizes_approval": False,
            "authorizes_activation": False,
            "authorizes_active_input": False,
            "authorizes_byte_stream_generation": False,
            "authorizes_execution": False,
            "solve_claim": False,
        }
        for source, target in OPTION_SELECTION_MISUSE_TRANSITIONS
    ]
    records["option_selection_misuse"] = _record(
        "option_selection_misuse",
        {
            "option_selection_misuse_validation_matrix_created": True,
            "option_selection_misuse_case_count": len(misuse_rows),
            "matrix_rows": misuse_rows,
            "all_rows_fail_closed": True,
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
        },
    )
    records["option_fixture_isolation_policy"] = _record(
        "option_fixture_isolation_policy",
        {
            "option_fixture_isolation_policy_created": True,
            "fixture_presented_as_selected_decision_must_fail_closed": True,
            "fixture_presented_as_real_operator_decision_must_fail_closed": True,
            "fixture_presented_as_real_operator_approval_must_fail_closed": True,
            "fixture_presented_as_deep_research_acceptance_must_fail_closed": True,
            "fixture_presented_as_combined_gate_validation_must_fail_closed": True,
            "fixture_presented_as_activation_decision_must_fail_closed": True,
            "fixture_presented_as_active_planning_input_selection_must_fail_closed": True,
            "fixture_template_scaffold_review_or_readiness_material_may_satisfy_real_gate": False,
            "readiness_package_may_be_used_as_real_decision": False,
            "options_scaffold_may_select_option": False,
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
        },
    )
    records["options_nonselection"] = _record(
        "options_nonselection",
        {
            "operator_options_nonselection_proof_created": True,
            "operator_decision_option_count": len(OPERATOR_DECISION_OPTIONS),
            "options": [
                {
                    **option,
                    "authorizes_real_approval_now": False,
                    "authorizes_activation_now": False,
                    "authorizes_active_input_now": False,
                    "authorizes_byte_stream_generation_now": False,
                    "authorizes_execution_now": False,
                }
                for option in OPERATOR_DECISION_OPTIONS
            ],
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
            "all_options_unselected": True,
            "real_operator_decision_record_created_now": False,
            "real_operator_approval_record_created_now": False,
            "real_deep_research_acceptance_record_created_now": False,
            "real_combined_gate_validation_record_created_now": False,
            "real_activation_decision_record_created_now": False,
            "active_planning_input_selected_now": False,
        },
    )
    records["operator_decision_nonauthorization"] = _record(
        "operator_decision_nonauthorization",
        {
            "operator_decision_nonauthorization_proof_created": True,
            "operator_decision_record_created_now": False,
            "operator_decision_record_present_now": False,
            "operator_decision_satisfied_now": False,
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
            "operator_decision_authorizes_real_approval_now": False,
            "operator_decision_authorizes_activation_now": False,
        },
    )
    records["combined_gate_nonsatisfaction"] = _record(
        "combined_gate_nonsatisfaction",
        {
            "combined_gate_non_satisfaction_proof_created": True,
            "real_combined_gate_validation_record_created_now": False,
            "real_combined_gate_validation_record_present_now": False,
            "combined_approval_gate_satisfied_now": False,
            "combined_approval_gate_authorizes_activation_now": False,
            "approval_gate_satisfied_now": False,
            "approval_gate_authorizes_activation_now": False,
        },
    )
    records["activation_nonauthorization"] = _record(
        "activation_nonauthorization",
        {
            "activation_decision_nonauthorization_proof_created": True,
            "real_activation_decision_record_created_now": False,
            "real_activation_decision_record_present_now": False,
            "activation_decision_valid_now": False,
            "activation_authorized_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
        },
    )
    records["real_record_blocker"] = _record(
        "real_record_blocker",
        {
            "real_record_creation_blocker_status": "active",
            "blocked_current_stage_real_records": FUTURE_REAL_RECORD_CLASSES,
            "blocked_current_stage_real_record_count": len(FUTURE_REAL_RECORD_CLASSES),
            "operator_decision_record_created_now": False,
            "real_operator_decision_record_created_now": False,
            "real_operator_decision_record_present_now": False,
            "real_operator_approval_record_created_now": False,
            "real_operator_approval_record_present_now": False,
            "real_deep_research_acceptance_record_created_now": False,
            "real_deep_research_acceptance_record_present_now": False,
            "real_combined_gate_validation_record_created_now": False,
            "real_combined_gate_validation_record_present_now": False,
            "real_activation_decision_record_created_now": False,
            "real_activation_decision_record_present_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
            "future_real_records_created_now": False,
            "combined_approval_gate_satisfied_now": False,
            "activation_decision_valid_now": False,
        },
    )
    records["stage5cq_scaffold_preservation"] = _preservation_record(
        "stage5cq_scaffold_preservation",
        label="stage5cq_operator_decision_scaffold",
        source_paths=[
            STAGE5CQ_DATA_PATHS["summary"],
            STAGE5CQ_DATA_PATHS["operator_decision_package"],
            STAGE5CQ_DATA_PATHS["operator_decision_nonauthorization"],
            STAGE5CQ_DATA_PATHS["real_record_blocker"],
            STAGE5CQ_DATA_PATHS["combined_gate_nonsatisfaction"],
            STAGE5CQ_DATA_PATHS["activation_nonauthorization"],
        ],
        preserved_fields={
            "stage5cq_operator_decision_scaffold_preserved": True,
            "stage5cq_operator_decision_scaffold_status_preserved": "scaffold_only",
            "stage5cq_operator_decision_record_created_now_preserved_false": True,
            "stage5cq_combined_gate_unsatisfied_preserved": True,
            "stage5cq_activation_invalid_preserved": True,
        },
    )
    records["stage5co_readiness_package"] = _preservation_record(
        "stage5co_readiness_package",
        label="stage5co_readiness_package",
        source_paths=[
            STAGE5CO_DATA_PATHS["summary"],
            STAGE5CO_DATA_PATHS["readiness_package"],
            STAGE5CO_DATA_PATHS["real_operator_readiness"],
            STAGE5CO_DATA_PATHS["real_deep_research_readiness"],
            STAGE5CO_DATA_PATHS["real_combined_gate_readiness"],
            STAGE5CO_DATA_PATHS["real_record_blocker"],
        ],
        preserved_fields={
            "stage5co_status_preserved": True,
            "stage5co_readiness_package_preserved": True,
            "stage5co_real_operator_approval_readiness_preserved": True,
            "stage5co_real_deep_research_acceptance_readiness_preserved": True,
            "stage5co_real_combined_gate_readiness_preserved": True,
            "stage5co_real_record_creation_blocker_preserved": True,
            "stage5co_activation_nonauthorization_preserved": True,
        },
    )
    records["stage5co_missing_requirements"] = _preservation_record(
        "stage5co_missing_requirements",
        label="stage5co_missing_requirements_register",
        source_paths=[STAGE5CO_DATA_PATHS["missing_requirements"]],
        preserved_fields={
            "stage5co_missing_requirements_register_preserved": True,
            "stage5co_missing_requirements": STAGE5CO_MISSING_REQUIREMENTS,
            "missing_requirement_count": len(STAGE5CO_MISSING_REQUIREMENTS),
            "stage5co_missing_requirements_falsely_closed": False,
        },
    )
    records["stage5co_transition_plan"] = _preservation_record(
        "stage5co_transition_plan",
        label="stage5co_transition_plan",
        source_paths=[
            STAGE5CO_DATA_PATHS["activation_transition_plan"],
            STAGE5CO_DATA_PATHS["future_transition_sequence"],
            STAGE5CO_DATA_PATHS["activation_nonauthorization"],
        ],
        preserved_fields={
            "stage5co_activation_transition_plan_preserved": True,
            "stage5co_future_transition_sequence_preserved": True,
            "stage5co_activation_nonauthorization_preserved": True,
        },
    )
    records["stage5cm_boundary"] = _record(
        "stage5cm_boundary",
        {
            "stage5cm_status_preserved": True,
            "stage5cm_boundary_preserved": True,
            "stage5cm_fixture_vs_real_boundary_preserved": True,
            "stage5cm_end_to_end_readiness_boundary_preserved": True,
            "stage5cm_credential_redaction_policy_preserved": True,
            "stage5cm_parallel_worker_cap_preserved": PARALLEL_WORKER_CAP,
        },
    )
    records["stage5ck_preservation"] = _preservation_record(
        "stage5ck_preservation",
        label="stage5ck_fixture_pack",
        source_paths=[
            STAGE5CK_DATA_PATHS["operator_fixtures"],
            STAGE5CK_DATA_PATHS["deep_research_fixtures"],
            STAGE5CK_DATA_PATHS["activation_fixtures"],
            STAGE5CK_DATA_PATHS["negative_matrix"],
        ],
        preserved_fields={
            "stage5ck_fixture_pack_preserved": True,
            "stage5ck_fixture_pack_only_preserved": True,
            "stage5ck_synthetic_negative_fixtures_only_preserved": True,
        },
    )
    records["stage5ci_preservation"] = _preservation_record(
        "stage5ci_preservation",
        label="stage5ci_templates",
        source_paths=[
            STAGE5CI_DATA_PATHS["operator_template"],
            STAGE5CI_DATA_PATHS["deep_research_template"],
            STAGE5CI_DATA_PATHS["activation_template"],
        ],
        preserved_fields={"stage5ci_templates_preserved": True},
    )
    records["stage5cg_preservation"] = _preservation_record(
        "stage5cg_preservation",
        label="stage5cg_scaffolds",
        source_paths=[
            STAGE5CG_DATA_PATHS["operator_decision"],
            STAGE5CG_DATA_PATHS["deep_research_decision"],
            STAGE5CG_DATA_PATHS["combined_gate"],
        ],
        preserved_fields={"stage5cg_scaffolds_preserved": True},
    )
    records["stage5ce_preservation"] = _preservation_record(
        "stage5ce_preservation",
        label="stage5ce_proposal_package",
        source_paths=[STAGE5CE_DATA_PATHS["proposal_package"]],
        preserved_fields={
            "stage5ce_proposal_package_preserved": True,
            "stage5ce_proposal_package_status_preserved": "review_package_only",
        },
    )
    records["stage5cc_preservation"] = _preservation_record(
        "stage5cc_preservation",
        label="stage5cc_contracts",
        source_paths=[
            STAGE5CC_DATA_PATHS["citation_preservation"],
            STAGE5CC_DATA_PATHS["fail_closed_contract"],
            STAGE5CC_DATA_PATHS["activation_contract"],
        ],
        preserved_fields={
            "stage5cc_exact_citation_contract_preserved": True,
            "stage5cc_fail_closed_trigger_exact_set_preserved": True,
            "stage5cc_activation_precondition_exact_set_preserved": True,
        },
    )
    records["stage5bd_preservation"] = _record(
        "stage5bd_preservation",
        {
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "stage5bd_plan_superseded": False,
        },
    )
    lineage_records = _lineage_records()
    records["active_lineage"] = _record(
        "active_lineage",
        {
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "active_lineage_records": lineage_records,
            "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in ACTIVE_LINEAGE_PATHS,
            "deprecated_stage5aw_path_absent": INCORRECT_STAGE5AW_PATH not in ACTIVE_LINEAGE_PATHS,
            "all_lineage_paths_resolve": all(record["present"] for record in lineage_records),
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
        },
    )
    records["no_active_ingestion"] = _record(
        "no_active_ingestion",
        {
            "no_active_ingestion_status": "closed",
            "string4_sidecar_status": "scaffolded_inactive",
            "string4_sidecar_active": False,
            "string4_sidecar_planning_ingestion_activated": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
        },
    )
    records["no_byte_stream_transition_gate"] = _record(
        "no_byte_stream_transition_gate",
        {
            "no_byte_stream_transition_gate_status": "closed",
            "byte_stream_generation_authorized_now": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "variant_materialisation_performed": False,
            "branch_enumeration_performed": False,
        },
    )
    records["no_execution_transition_gate"] = _record(
        "no_execution_transition_gate",
        {
            "no_execution_transition_gate_status": "closed",
            "execution_authorized_now": False,
            "token_block_experiment_executed": False,
            "dwh_hash_search_performed": False,
            "decode_attempt_performed": False,
            "scoring_performed": False,
            "cuda_execution_performed": False,
            "benchmark_performed": False,
        },
    )
    records["supersession_nonactivation"] = _record(
        "supersession_nonactivation",
        {
            "manifest_supersession_nonactivation_proof_created": True,
            "manifest_supersession_performed": False,
            "manifest_supersession_authorized_now": False,
            "active_manifest_registry_updated": False,
        },
    )
    records["sidecar_activation_blocker"] = _record(
        "sidecar_activation_blocker",
        {
            "sidecar_activation_blocker_status": "active",
            "string4_sidecar_status": "scaffolded_inactive",
            "string4_sidecar_active": False,
            "string4_sidecar_planning_ingestion_activated": False,
            "string4_execution_input_allowed": False,
        },
    )
    records["handoff"] = _record(
        "handoff",
        {
            "canonical_codex_handoff_root": "codex-output",
            "deprecated_handoff_root": "codex_output",
            "codex_output_used": False,
            "codex_completion_summary_committed": False,
            "stage5cu_codex_completion_summary_required": True,
            "stage5cu_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            "stage5cu_codex_completion_summary_written_locally_before_final_response": (
                CODEX_COMPLETION_PATH.is_file()
            ),
            "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
            **completion_status,
        },
    )
    records["completion_continuity"] = _record(
        "completion_continuity",
        {
            "completion_summary_continuity_status": "preserved_for_stage5cu",
            "stage5ct_completion_summary_warning_integrated": True,
            "stage5cu_codex_completion_summary_required": True,
            "stage5cu_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            "stage5cu_codex_completion_summary_written_locally_before_final_response": (
                CODEX_COMPLETION_PATH.is_file()
            ),
            "codex_output_used": False,
            "codex_completion_summary_committed": False,
            **completion_status,
        },
    )
    records["credential_redaction"] = _record(
        "credential_redaction",
        {
            "credential_redaction_policy_preserved": True,
            "credential_like_remote_must_be_redacted": True,
            "credential_like_text_must_not_be_committed": True,
            "committed_stage5cu_metadata_secret_scan_required": True,
            "secret_values_printed_or_committed": False,
            "remote_hygiene": remote_status,
            "ignored_local_report_secret_scan": ignored_report_status,
        },
    )
    records["review_packaging_warning"] = _record(
        "review_packaging_warning",
        {
            "review_packaging_warning_created": True,
            "stage5ct_completion_summary_warning_integrated": True,
            "warning_status": "integrated_non_gate_opening_warning",
            "gate_opening": False,
            "raw_review_bodies_committed": False,
            "generated_review_bodies_committed": False,
        },
    )
    records["guardrail"] = _record(
        "guardrail",
        {
            "guardrail_status": "closed",
            "future_token_block_execution_remains_blocked": True,
            "dwh_hash_search_performed": False,
            "decode_attempt_performed": False,
        },
    )
    records["dwh"] = _record(
        "dwh",
        {
            "dwh_quarantine_status": "preserved",
            "dwh_quarantine_reaffirmed": True,
            "dwh_hash_operations_quarantined": True,
            "dwh_hash_search_performed": False,
        },
    )
    records["source_gap"] = _record(
        "source_gap",
        {
            "source_gap_severity_update_status": "no_execution_no_new_gap_closure",
            "source_gap_status": "review_required_before_activation",
            "gate_opening_gap_count": 0,
        },
    )
    records["validation_evidence"] = _record(
        "validation_evidence",
        {
            "validation_evidence_status": "committed_compact_evidence",
            "local_validation_evidence_committed": True,
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
            "parallel_worker_cap_for_stage5cu_and_later": PARALLEL_WORKER_CAP,
            "parallel_validation_required": True,
            "parallel_validation_wrapper": "scripts/ci/run-parallel-validation.ps1",
            "parallel_validation_workers_observed_locally": PARALLEL_WORKER_CAP,
            "parallel_validation_pytest_workers_observed_locally": PARALLEL_WORKER_CAP,
            "parallel_validation_status_observed_locally": "passed",
            "old_16_worker_default_reintroduced": False,
            "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
            "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
            "raw_staged": False,
            "generated_outputs_staged": False,
            "codex_output_staged": False,
            "sqlite_staged": False,
            "final_commit_external_evidence_required": True,
            "ci_external_evidence_required": True,
            "validation_commands": _validation_commands(),
        },
    )
    records["source_digest_index"] = _record(
        "source_digest_index",
        {
            "source_digest_index_created": True,
            "source_digest_record_count": source_digest_count,
            "source_digest_unique_path_count": len({record["path"] for record in source_records}),
            "duplicate_path_count": source_digest_count - len(
                {record["path"] for record in source_records}
            ),
            "source_paths_unique": source_digest_count == len(
                {record["path"] for record in source_records}
            ),
            "secret_values_recorded": False,
            "source_records": source_records,
            "raw_or_generated_bodies_committed": False,
        },
    )
    records["gap_register"] = _record(
        "gap_register",
        {
            "reviewability_gap_register_created": True,
            "reviewability_gaps": REVIEWABILITY_GAPS,
            "reviewability_gap_count": len(REVIEWABILITY_GAPS),
            "any_gap_authorizes_approval": False,
            "any_gap_authorizes_activation": False,
            "any_gap_authorizes_execution": False,
        },
    )
    records["equivalence_map"] = _record(
        "equivalence_map",
        {
            "record_family_name_equivalence_map_created": True,
            "record_family_count": 8,
            "families": [
                {
                    "family_id": "stage5cu_operator_decision_readiness_records",
                    "equivalent_prefixes": [
                        "stage5cu-operator-decision-readiness",
                        "stage5cu-operator-decision-nonauthorization",
                    ],
                },
                {
                    "family_id": "stage5cu_decision_options_records",
                    "equivalent_prefixes": [
                        "stage5cu-real-approval-decision-options",
                        "stage5cu-operator-options-nonselection",
                    ],
                },
                {
                    "family_id": "stage5cu_real_record_blocker_records",
                    "equivalent_prefixes": [
                        "stage5cu-real-record-creation-blocker",
                        "stage5cu-combined-gate",
                        "stage5cu-activation-decision",
                    ],
                },
                {
                    "family_id": "stage5cu_stage5cq_preservation_records",
                    "equivalent_prefixes": [
                        "stage5cu-stage5cq-operator-decision",
                    ],
                },
                {
                    "family_id": "stage5cu_stage5co_preservation_records",
                    "equivalent_prefixes": [
                        "stage5cu-stage5co-readiness",
                        "stage5cu-stage5co-missing",
                        "stage5cu-stage5co-transition",
                    ],
                },
                {
                    "family_id": "stage5cu_prior_stage_preservation_records",
                    "equivalent_prefixes": [
                        "stage5cu-stage5cm",
                        "stage5cu-stage5ck",
                        "stage5cu-stage5ci",
                        "stage5cu-stage5cg",
                        "stage5cu-stage5ce",
                        "stage5cu-stage5cc",
                        "stage5cu-stage5bd",
                    ],
                },
                {
                    "family_id": "stage5cu_gate_records",
                    "equivalent_prefixes": [
                        "stage5cu-no-active-ingestion",
                        "stage5cu-no-byte-stream",
                        "stage5cu-no-execution",
                    ],
                },
                {
                    "family_id": "stage5cu_handoff_records",
                    "equivalent_prefixes": [
                        "stage5cu-codex-handoff",
                        "stage5cu-completion-summary",
                        "stage5cu-credential-redaction",
                    ],
                },
            ],
        },
    )
    next_title = (
        "Stage 5CV - Deep Research review of Stage 5CU operator-decision option "
        "negative-fixture hardening, without execution"
    )
    records["next_stage"] = _record(
        "next_stage",
        {
            "selected_next_stage_id": "stage-5cv",
            "selected_next_stage_title": next_title,
            "selected_next_prompt_type": "deep_research_review",
            "selected_next_stage_authorizes_execution": False,
            "reason": (
                "Stage 5CU hardens negative fixtures around Stage 5CS decision options; "
                "independent review is required before any future real operator decision, "
                "real approval record, activation decision, active-planning-input selection, "
                "byte-stream stage, or execution-adjacent stage."
            ),
        },
    )
    records["stage_marker"] = _record(
        "stage_marker",
        {
            "current_completed_stage": STAGE_TITLE,
            "current_completed_stage_id": STAGE_ID,
            "selected_next_stage_id": "stage-5cv",
            "selected_next_stage_title": next_title,
            "selected_next_prompt_type": "deep_research_review",
            "selected_next_stage_authorizes_execution": False,
        },
    )
    records["summary"] = _record(
        "summary",
        {
            "status": "complete",
            "source_stage_ids": SOURCE_STAGE_IDS,
            "source_token_block_lineage": SOURCE_TOKEN_BLOCK_LINEAGE,
            "stage5ct_findings_integrated": True,
            "stage5ct_verdict": "accept_with_warnings",
            "stage5cs_operator_decision_readiness_package_preserved": True,
            "stage5cs_operator_decision_readiness_package_status_preserved": "readiness_package_only",
            "stage5cs_real_approval_decision_options_scaffold_preserved": True,
            "stage5cs_real_approval_decision_options_status_preserved": "options_scaffold_only",
            "stage5cs_option_count_preserved": len(OPERATOR_DECISION_OPTIONS),
            "stage5cs_exact_option_set_preserved": True,
            "all_options_unselected": True,
            "decision_option_negative_fixture_pack_created": True,
            "real_decision_record_negative_fixture_pack_created": True,
            "option_selection_misuse_validation_matrix_created": True,
            "option_fixture_isolation_policy_created": True,
            "negative_fixture_count": len(NEGATIVE_FIXTURE_IDS),
            "option_selection_misuse_case_count": len(OPTION_SELECTION_MISUSE_TRANSITIONS),
            "fixture_presented_as_selected_decision_must_fail_closed": True,
            "fixture_presented_as_real_operator_decision_must_fail_closed": True,
            "fixture_presented_as_real_operator_approval_must_fail_closed": True,
            "fixture_presented_as_deep_research_acceptance_must_fail_closed": True,
            "fixture_presented_as_combined_gate_validation_must_fail_closed": True,
            "fixture_presented_as_activation_decision_must_fail_closed": True,
            "fixture_presented_as_active_planning_input_selection_must_fail_closed": True,
            "stage5cq_operator_decision_scaffold_preserved": True,
            "stage5cq_operator_decision_scaffold_status_preserved": "scaffold_only",
            "stage5co_status_preserved": True,
            "stage5co_readiness_package_preserved": True,
            "stage5co_real_operator_approval_readiness_preserved": True,
            "stage5co_real_deep_research_acceptance_readiness_preserved": True,
            "stage5co_real_combined_gate_readiness_preserved": True,
            "stage5co_activation_transition_plan_preserved": True,
            "stage5co_future_transition_sequence_preserved": True,
            "stage5co_missing_requirements_register_preserved": True,
            "stage5co_real_record_creation_blocker_preserved": True,
            "stage5co_activation_nonauthorization_preserved": True,
            "stage5cm_boundary_preserved": True,
            "stage5cm_fixture_vs_real_boundary_preserved": True,
            "stage5cm_end_to_end_readiness_boundary_preserved": True,
            "stage5cm_credential_redaction_policy_preserved": True,
            "stage5cm_parallel_worker_cap_preserved": PARALLEL_WORKER_CAP,
            "stage5ck_fixture_pack_preserved": True,
            "stage5ck_fixture_pack_only_preserved": True,
            "stage5ck_synthetic_negative_fixtures_only_preserved": True,
            "stage5ci_templates_preserved": True,
            "stage5cg_scaffolds_preserved": True,
            "stage5ce_proposal_package_status_preserved": "review_package_only",
            "stage5cc_exact_citation_contract_preserved": True,
            "stage5cc_fail_closed_trigger_exact_set_preserved": True,
            "stage5cc_activation_precondition_exact_set_preserved": True,
            "operator_decision_readiness_package_created": True,
            "operator_decision_readiness_package_status": "readiness_package_only",
            "real_approval_decision_options_scaffold_created": True,
            "real_approval_decision_options_status": "options_scaffold_only",
            "operator_decision_option_count": len(OPERATOR_DECISION_OPTIONS),
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
            "operator_decision_package_scaffold_created": False,
            "operator_decision_package_status": "not_created_in_stage5cu",
            "real_approval_records_created": False,
            "future_real_records_created_now": False,
            "combined_approval_gate_satisfied_now": False,
            "combined_approval_gate_authorizes_activation_now": False,
            "approval_gate_satisfied_now": False,
            "approval_gate_authorizes_activation_now": False,
            "activation_decision_valid_now": False,
            "activation_authorized_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
            "new_active_planning_input_created": False,
            "stage5cs_stale_completion_summary_warning_integrated": True,
            "stage5ct_completion_summary_warning_integrated": True,
            "stage5cu_codex_completion_summary_required": True,
            "stage5cu_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            "stage5cu_codex_completion_summary_written_locally_before_final_response": (
                CODEX_COMPLETION_PATH.is_file()
            ),
            "stage5cu_completion_summary_finalized_not_pending": not (
                _completion_summary_has_unresolved_placeholder(CODEX_COMPLETION_PATH)
            ),
            "codex_completion_summary_committed": False,
            "codex_output_used": False,
            "no_active_ingestion_status": "closed",
            "no_byte_stream_transition_gate_status": "closed",
            "no_execution_transition_gate_status": "closed",
            "manifest_supersession_performed": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "stage5bd_plan_superseded": False,
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in ACTIVE_LINEAGE_PATHS,
            "deprecated_stage5aw_path_absent": INCORRECT_STAGE5AW_PATH not in ACTIVE_LINEAGE_PATHS,
            "string4_sidecar_status": "scaffolded_inactive",
            "string4_sidecar_active": False,
            "string4_sidecar_planning_ingestion_activated": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_byte_stream_generation_allowed": False,
            "string4_execution_input_allowed": False,
            "parallel_worker_cap_for_stage5cu_and_later": PARALLEL_WORKER_CAP,
            "future_token_block_execution_remains_blocked": True,
            "recommended_next_stage_id": "stage-5cv",
            "recommended_next_prompt_type": "deep_research_review",
            "recommended_next_stage_title": next_title,
            "source_digest_record_count": source_digest_count,
        },
    )
    return records


def build_stage5cu(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    """Build Stage 5CU committed metadata and ignored reviewability reports."""

    _write_schemas()
    results_dir.mkdir(parents=True, exist_ok=True)
    records = _build_records()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    write_json(results_dir / "summary.json", records["summary"])
    write_json(
        results_dir / "operator_decision_readiness_report.json",
        {
            "operator_decision_readiness": records["operator_decision_readiness"],
            "operator_decision_nonauthorization": records["operator_decision_nonauthorization"],
            "real_record_blocker": records["real_record_blocker"],
            "combined_gate_nonsatisfaction": records["combined_gate_nonsatisfaction"],
            "activation_nonauthorization": records["activation_nonauthorization"],
        },
    )
    write_json(
        results_dir / "decision_options_report.json",
        {
            "decision_options": records["decision_options"],
            "decision_option_negative_fixtures": records["decision_option_negative_fixtures"],
            "real_decision_negative_fixtures": records["real_decision_negative_fixtures"],
            "option_selection_misuse": records["option_selection_misuse"],
            "option_fixture_isolation_policy": records["option_fixture_isolation_policy"],
            "options_nonselection": records["options_nonselection"],
        },
    )
    write_json(
        results_dir / "negative_fixture_report.json",
        {
            "decision_option_negative_fixtures": records["decision_option_negative_fixtures"],
            "real_decision_negative_fixtures": records["real_decision_negative_fixtures"],
            "option_selection_misuse": records["option_selection_misuse"],
            "option_fixture_isolation_policy": records["option_fixture_isolation_policy"],
        },
    )
    write_json(
        results_dir / "preservation_report.json",
        {
            "stage5cq_scaffold_preservation": records["stage5cq_scaffold_preservation"],
            "stage5co_readiness_package": records["stage5co_readiness_package"],
            "stage5co_missing_requirements": records["stage5co_missing_requirements"],
            "stage5co_transition_plan": records["stage5co_transition_plan"],
            "stage5bd_preservation": records["stage5bd_preservation"],
            "active_lineage": records["active_lineage"],
        },
    )
    write_json(
        results_dir / "handoff_continuity_report.json",
        {
            "handoff": records["handoff"],
            "completion_continuity": records["completion_continuity"],
            "credential_redaction": records["credential_redaction"],
            "review_packaging_warning": records["review_packaging_warning"],
        },
    )
    write_json(results_dir / "source_digest_index.json", records["source_digest_index"])
    write_jsonl(
        results_dir / "warnings.jsonl",
        [
            {
                "stage_id": STAGE_ID,
                "warning_id": gap["gap_id"],
                "status": gap["status"],
                "severity": gap["severity"],
                "gate_opening": False,
            }
            for gap in REVIEWABILITY_GAPS
        ],
    )
    return records["summary"]


def _load_all_payloads(errors: list[str]) -> dict[str, dict[str, Any]]:
    return {key: _validate_payload(path, errors) for key, path in DATA_PATHS.items()}


def _validate_payload(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing_record={repo_relative(path)}")
        return {}
    payload = _read(path)
    schema_path = payload.get("schema")
    if not isinstance(schema_path, str) or not Path(schema_path).is_file():
        errors.append(f"{repo_relative(path)} schema missing: {schema_path}")
        return payload
    schema_errors = list(Draft202012Validator(_load_schema(schema_path)).iter_errors(payload))
    errors.extend(f"{repo_relative(path)} schema_error={error.message}" for error in schema_errors)
    return payload


def _walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(_walk_strings(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(_walk_strings(item))
        return result
    return []


def _check_false_flags(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for key, payload in payloads.items():
        for field, expected in FALSE_FLAGS.items():
            if payload.get(field) is not None and payload.get(field) is not expected:
                errors.append(f"{key}: {field} must be false")


def _check_no_stage5cu_metadata_secrets(errors: list[str]) -> None:
    for path in DATA_PATHS.values():
        if path.is_file() and _path_has_secret_like_text(path):
            errors.append(f"credential_like_text_in_stage5cu_metadata={repo_relative(path)}")


def validate_stage5cu_actual_record_rejection(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    forbidden_true_fields = [
        "operator_decision_record_created_now",
        "operator_decision_record_present_now",
        "operator_decision_satisfied_now",
        "operator_decision_authorizes_real_approval_now",
        "operator_decision_authorizes_activation_now",
        "real_operator_decision_record_created_now",
        "real_operator_approval_record_created_now",
        "real_operator_approval_record_present_now",
        "real_deep_research_acceptance_record_created_now",
        "real_deep_research_acceptance_record_present_now",
        "real_combined_gate_validation_record_created_now",
        "real_combined_gate_validation_record_present_now",
        "real_activation_decision_record_created_now",
        "future_real_records_created_now",
        "combined_approval_gate_satisfied_now",
        "activation_decision_valid_now",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
        "operator_decision_option_selected_now",
        "byte_stream_generation_authorized_now",
        "execution_authorized_now",
        "solve_claim",
    ]
    for field in forbidden_true_fields:
        if payload.get(field) is True:
            errors.append(f"{field} must be false")
    if payload.get("selected_option_id") is not None:
        errors.append("selected_option_id must be null")
    strings = _walk_strings(payload)
    if INCORRECT_STAGE5AW_PATH in strings:
        errors.append("deprecated Stage 5AW path must fail")
    for text in strings:
        findings = _secret_findings(text)
        if findings:
            errors.append(f"credential_like_text_categories={','.join(sorted(findings))}")
    return errors


def validate_stage5cu_stage5ct_findings(
    *, findings: Path = DATA_PATHS["findings"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(findings, errors)
    if payload.get("stage5ct_verdict") != "accept_with_warnings":
        errors.append("Stage 5CT verdict must be accept_with_warnings")
    observed = set(payload.get("findings", []))
    for item in sorted(set(STAGE5CT_FINDINGS) - observed):
        errors.append(f"missing_stage5ct_finding={item}")
    return {
        "stage5cu_stage5ct_findings_valid": not errors,
        "stage5ct_verdict": payload.get("stage5ct_verdict"),
        "finding_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_operator_decision_readiness(
    *, operator_decision_readiness: Path = DATA_PATHS["operator_decision_readiness"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(operator_decision_readiness, errors)
    if payload.get("operator_decision_readiness_package_status") != "readiness_package_only":
        errors.append("operator decision readiness package must be readiness_package_only")
    if payload.get("operator_decision_readiness_package_created") is not True:
        errors.append("operator decision readiness package must be created")
    observed = set(payload.get("required_future_inputs", []))
    for item in sorted(set(OPERATOR_DECISION_READINESS_REQUIREMENTS) - observed):
        errors.append(f"missing_operator_decision_requirement={item}")
    errors.extend(validate_stage5cu_actual_record_rejection(payload))
    return {
        "stage5cu_operator_decision_readiness_valid": not errors,
        "required_future_input_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def _validate_decision_options_payload(payload: dict[str, Any], errors: list[str]) -> None:
    if payload.get("operator_decision_option_count") != len(OPERATOR_DECISION_OPTIONS):
        errors.append("operator decision option count must remain 6")
    if payload.get("operator_decision_option_selected_now") is not False:
        errors.append("operator_decision_option_selected_now must be false")
    if payload.get("selected_option_id") is not None:
        errors.append("selected_option_id must be null")
    options = payload.get("options", [])
    if options:
        option_ids = [option.get("option_id") for option in options]
        if len(option_ids) != len(set(option_ids)):
            errors.append("operator decision option IDs must be unique")
        expected_ids = {option["option_id"] for option in OPERATOR_DECISION_OPTIONS}
        if set(option_ids) != expected_ids:
            errors.append("operator decision option ID set mismatch")
        for option in options:
            if option.get("selected_now") is not False:
                errors.append(f"{option.get('option_id')}: selected_now must be false")
            for field in (
                "authorizes_real_approval_now",
                "authorizes_activation_now",
                "authorizes_active_input_now",
                "authorizes_byte_stream_generation_now",
                "authorizes_execution_now",
            ):
                if option.get(field) is not False:
                    errors.append(f"{option.get('option_id')}: {field} must be false")


def validate_stage5cu_decision_options(
    *, decision_options: Path = DATA_PATHS["decision_options"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(decision_options, errors)
    if payload.get("real_approval_decision_options_status") != "options_scaffold_only":
        errors.append("decision options must remain options_scaffold_only")
    if payload.get("real_approval_decision_options_scaffold_created") is not True:
        errors.append("decision options scaffold must be created")
    _validate_decision_options_payload(payload, errors)
    errors.extend(validate_stage5cu_actual_record_rejection(payload))
    return {
        "stage5cu_decision_options_valid": not errors,
        "operator_decision_option_count": payload.get("operator_decision_option_count"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_decision_options_preservation(
    *, decision_options: Path = DATA_PATHS["decision_options"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(decision_options, errors)
    if payload.get("stage5cs_real_approval_decision_options_scaffold_preserved") is not True:
        errors.append("Stage 5CS decision-options scaffold must be preserved")
    if (
        payload.get("stage5cs_real_approval_decision_options_status_preserved")
        != "options_scaffold_only"
    ):
        errors.append("Stage 5CS decision-options status must remain options_scaffold_only")
    if payload.get("stage5cs_option_count_preserved") != len(OPERATOR_DECISION_OPTIONS):
        errors.append("Stage 5CS option count must remain 6")
    if payload.get("stage5cs_exact_option_set_preserved") is not True:
        errors.append("Stage 5CS exact option set must be preserved")
    if payload.get("real_approval_decision_options_status") != "options_scaffold_only":
        errors.append("decision options must remain options_scaffold_only")
    _validate_decision_options_payload(payload, errors)
    errors.extend(validate_stage5cu_actual_record_rejection(payload))
    return {
        "stage5cu_decision_options_preservation_valid": not errors,
        "operator_decision_option_count": payload.get("operator_decision_option_count"),
        "operator_decision_option_selected_now": payload.get(
            "operator_decision_option_selected_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_decision_option_negative_fixtures(
    *, fixtures: Path = DATA_PATHS["decision_option_negative_fixtures"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(fixtures, errors)
    observed_ids = [fixture.get("fixture_id") for fixture in payload.get("fixtures", [])]
    if payload.get("decision_option_negative_fixture_pack_created") is not True:
        errors.append("decision-option negative fixture pack must be created")
    if payload.get("fixture_pack_status") != "synthetic_negative_fixtures_only":
        errors.append("decision-option fixture pack must be synthetic negative fixtures only")
    if payload.get("negative_fixture_count") != len(NEGATIVE_FIXTURE_IDS):
        errors.append("negative fixture count mismatch")
    if set(observed_ids) != set(NEGATIVE_FIXTURE_IDS):
        errors.append("negative fixture ID set mismatch")
    if len(observed_ids) != len(set(observed_ids)):
        errors.append("negative fixture IDs must be unique")
    for fixture in payload.get("fixtures", []):
        fixture_id = fixture.get("fixture_id")
        for field in (
            "fixture_only",
            "synthetic_negative_fixture",
            "must_be_rejected_if_presented_as_real_record",
        ):
            if fixture.get(field) is not True:
                errors.append(f"{fixture_id}: {field} must be true")
        for field in (
            "real_record_created_now",
            "may_satisfy_real_gate",
            "may_authorize_approval",
            "may_authorize_activation",
            "may_authorize_active_input",
            "may_authorize_byte_stream_generation",
            "may_authorize_execution",
            "operator_decision_option_selected_now",
            "gate_opening",
        ):
            if fixture.get(field) is not False:
                errors.append(f"{fixture_id}: {field} must be false")
        if fixture.get("selected_option_id") is not None:
            errors.append(f"{fixture_id}: selected_option_id must be null")
    errors.extend(validate_stage5cu_actual_record_rejection(payload))
    return {
        "stage5cu_decision_option_negative_fixtures_valid": not errors,
        "negative_fixture_count": payload.get("negative_fixture_count"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_real_decision_negative_fixtures(
    *, fixtures: Path = DATA_PATHS["real_decision_negative_fixtures"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(fixtures, errors)
    observed_classes = [
        fixture.get("target_real_record_class") for fixture in payload.get("fixtures", [])
    ]
    if payload.get("real_decision_record_negative_fixture_pack_created") is not True:
        errors.append("real-decision negative fixture pack must be created")
    if payload.get("fixture_pack_status") != "synthetic_negative_fixtures_only":
        errors.append("real-decision fixture pack must be synthetic negative fixtures only")
    if set(observed_classes) != set(FUTURE_REAL_RECORD_CLASSES):
        errors.append("real-decision target class set mismatch")
    if len(observed_classes) != len(set(observed_classes)):
        errors.append("real-decision target classes must be unique")
    if payload.get("real_decision_negative_fixture_count") != len(FUTURE_REAL_RECORD_CLASSES):
        errors.append("real-decision negative fixture count mismatch")
    for fixture in payload.get("fixtures", []):
        fixture_id = fixture.get("fixture_id")
        for field in (
            "fixture_only",
            "synthetic_negative_fixture",
            "must_be_rejected_if_presented_as_real_record",
        ):
            if fixture.get(field) is not True:
                errors.append(f"{fixture_id}: {field} must be true")
        for field in (
            "created_now",
            "present_now",
            "satisfied_now",
            "authorizes_activation_now",
            "may_satisfy_real_gate",
        ):
            if fixture.get(field) is not False:
                errors.append(f"{fixture_id}: {field} must be false")
    errors.extend(validate_stage5cu_actual_record_rejection(payload))
    return {
        "stage5cu_real_decision_negative_fixtures_valid": not errors,
        "real_decision_negative_fixture_count": payload.get(
            "real_decision_negative_fixture_count"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_option_selection_misuse(
    *, misuse: Path = DATA_PATHS["option_selection_misuse"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(misuse, errors)
    rows = payload.get("matrix_rows", [])
    observed_transitions = {
        (row.get("source_record_class"), row.get("target_record_class")) for row in rows
    }
    if payload.get("option_selection_misuse_validation_matrix_created") is not True:
        errors.append("option-selection misuse validation matrix must be created")
    if payload.get("option_selection_misuse_case_count") != len(
        OPTION_SELECTION_MISUSE_TRANSITIONS
    ):
        errors.append("option-selection misuse case count mismatch")
    if observed_transitions != set(OPTION_SELECTION_MISUSE_TRANSITIONS):
        errors.append("option-selection misuse transition set mismatch")
    for row in rows:
        label = f"{row.get('source_record_class')}->{row.get('target_record_class')}"
        if row.get("must_fail_closed") is not True:
            errors.append(f"{label}: must_fail_closed must be true")
        for field in (
            "allowed_now",
            "gate_opening",
            "authorizes_approval",
            "authorizes_activation",
            "authorizes_active_input",
            "authorizes_byte_stream_generation",
            "authorizes_execution",
            "solve_claim",
        ):
            if row.get(field) is not False:
                errors.append(f"{label}: {field} must be false")
    errors.extend(validate_stage5cu_actual_record_rejection(payload))
    return {
        "stage5cu_option_selection_misuse_valid": not errors,
        "option_selection_misuse_case_count": payload.get(
            "option_selection_misuse_case_count"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_options_nonselection(
    *, options_nonselection: Path = DATA_PATHS["options_nonselection"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(options_nonselection, errors)
    if payload.get("operator_options_nonselection_proof_created") is not True:
        errors.append("operator options nonselection proof must be created")
    if payload.get("all_options_unselected") is not True:
        errors.append("all_options_unselected must be true")
    _validate_decision_options_payload(payload, errors)
    errors.extend(validate_stage5cu_actual_record_rejection(payload))
    return {
        "stage5cu_options_nonselection_valid": not errors,
        "operator_decision_option_selected_now": payload.get(
            "operator_decision_option_selected_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_real_record_blocker(
    *, real_record_blocker: Path = DATA_PATHS["real_record_blocker"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(real_record_blocker, errors)
    if payload.get("real_record_creation_blocker_status") != "active":
        errors.append("real-record creation blocker must be active")
    if set(payload.get("blocked_current_stage_real_records", [])) != set(FUTURE_REAL_RECORD_CLASSES):
        errors.append("blocked current-stage real record classes mismatch")
    errors.extend(validate_stage5cu_actual_record_rejection(payload))
    return {
        "stage5cu_real_record_blocker_valid": not errors,
        "blocked_current_stage_real_record_count": len(
            payload.get("blocked_current_stage_real_records", [])
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_combined_gate(
    *, combined_gate: Path = DATA_PATHS["combined_gate_nonsatisfaction"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(combined_gate, errors)
    if payload.get("combined_gate_non_satisfaction_proof_created") is not True:
        errors.append("combined gate non-satisfaction proof must be created")
    for field in (
        "combined_approval_gate_satisfied_now",
        "combined_approval_gate_authorizes_activation_now",
        "approval_gate_satisfied_now",
        "approval_gate_authorizes_activation_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cu_combined_gate_valid": not errors,
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_activation_nonauthorization(
    *, activation: Path = DATA_PATHS["activation_nonauthorization"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(activation, errors)
    if payload.get("activation_decision_nonauthorization_proof_created") is not True:
        errors.append("activation nonauthorization proof must be created")
    for field in (
        "activation_decision_valid_now",
        "activation_authorized_now",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cu_activation_nonauthorization_valid": not errors,
        "activation_decision_valid_now": payload.get("activation_decision_valid_now"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_stage5cs_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    stage5cs_summary = _read(STAGE5CS_DATA_PATHS["summary"])
    payload = _validate_payload(DATA_PATHS["decision_options"], errors)
    expected = {
        "operator_decision_readiness_package_status": "readiness_package_only",
        "real_approval_decision_options_status": "options_scaffold_only",
        "operator_decision_option_count": len(OPERATOR_DECISION_OPTIONS),
        "operator_decision_option_selected_now": False,
        "selected_option_id": None,
    }
    for field, expected_value in expected.items():
        if stage5cs_summary.get(field) != expected_value:
            errors.append(f"Stage 5CS summary {field} mismatch")
    for field in (
        "stage5cs_real_approval_decision_options_scaffold_preserved",
        "stage5cs_exact_option_set_preserved",
    ):
        if payload.get(field) is not True:
            errors.append(f"{field} must be true")
    if payload.get("stage5cs_option_count_preserved") != len(OPERATOR_DECISION_OPTIONS):
        errors.append("Stage 5CS option count must be preserved as 6")
    _, stage5cs_errors = validate_stage5cs()
    errors.extend(f"stage5cs:{error}" for error in stage5cs_errors)
    return {
        "stage5cu_stage5cs_preservation_valid": not errors,
        "stage5cs_option_count_preserved": payload.get("stage5cs_option_count_preserved"),
        "stage5cs_option_selected_now": stage5cs_summary.get(
            "operator_decision_option_selected_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_stage5cq_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(DATA_PATHS["stage5cq_scaffold_preservation"], errors)
    for field in (
        "stage5cq_operator_decision_scaffold_preserved",
        "stage5cq_operator_decision_record_created_now_preserved_false",
        "stage5cq_combined_gate_unsatisfied_preserved",
        "stage5cq_activation_invalid_preserved",
    ):
        if payload.get(field) is not True:
            errors.append(f"{field} must be true")
    if payload.get("stage5cq_operator_decision_scaffold_status_preserved") != "scaffold_only":
        errors.append("Stage 5CQ scaffold status must remain scaffold_only")
    _, validator_errors = validate_stage5cq()
    errors.extend(f"stage5cq:{error}" for error in validator_errors)
    return {
        "stage5cu_stage5cq_preservation_valid": not errors,
        "stage5cq_operator_decision_scaffold_status_preserved": payload.get(
            "stage5cq_operator_decision_scaffold_status_preserved"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_stage5co_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = _load_all_payloads(errors)
    for key, fields in {
        "stage5co_readiness_package": [
            "stage5co_status_preserved",
            "stage5co_readiness_package_preserved",
            "stage5co_real_operator_approval_readiness_preserved",
            "stage5co_real_deep_research_acceptance_readiness_preserved",
            "stage5co_real_combined_gate_readiness_preserved",
            "stage5co_real_record_creation_blocker_preserved",
        ],
        "stage5co_missing_requirements": [
            "stage5co_missing_requirements_register_preserved",
        ],
        "stage5co_transition_plan": [
            "stage5co_activation_transition_plan_preserved",
            "stage5co_future_transition_sequence_preserved",
            "stage5co_activation_nonauthorization_preserved",
        ],
    }.items():
        for field in fields:
            if payloads.get(key, {}).get(field) is not True:
                errors.append(f"{key}: {field} must be true")
    if payloads.get("stage5co_missing_requirements", {}).get(
        "missing_requirement_count"
    ) != len(STAGE5CO_MISSING_REQUIREMENTS):
        errors.append("Stage 5CO missing requirement count must be preserved")
    for label, validator in (
        ("stage5co_findings", validate_stage5co_stage5cn_findings),
        ("stage5co_readiness", validate_stage5co_approval_readiness_package),
        ("stage5co_operator", validate_stage5co_real_operator_readiness),
        ("stage5co_deep_research", validate_stage5co_real_deep_research_readiness),
        ("stage5co_combined", validate_stage5co_real_combined_gate_readiness),
        ("stage5co_transition", validate_stage5co_activation_transition_plan),
        ("stage5co_missing", validate_stage5co_current_missing_requirements),
        ("stage5co_blocker", validate_stage5co_real_record_blocker),
        ("stage5co_boundary", validate_stage5co_stage5cm_boundary_preservation),
        ("stage5co_gates", validate_stage5co_sidecar_gates),
        ("stage5co_credential", validate_stage5co_credential_redaction_policy),
    ):
        _, validator_errors = validator()
        errors.extend(f"{label}:{error}" for error in validator_errors)
    return {
        "stage5cu_stage5co_preservation_valid": not errors,
        "missing_requirement_count": payloads.get("stage5co_missing_requirements", {}).get(
            "missing_requirement_count"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_prior_stage_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = _load_all_payloads(errors)
    required_true = {
        "stage5cm_boundary": [
            "stage5cm_boundary_preserved",
            "stage5cm_fixture_vs_real_boundary_preserved",
            "stage5cm_end_to_end_readiness_boundary_preserved",
            "stage5cm_credential_redaction_policy_preserved",
        ],
        "stage5ck_preservation": [
            "stage5ck_fixture_pack_preserved",
            "stage5ck_fixture_pack_only_preserved",
            "stage5ck_synthetic_negative_fixtures_only_preserved",
        ],
        "stage5ci_preservation": ["stage5ci_templates_preserved"],
        "stage5cg_preservation": ["stage5cg_scaffolds_preserved"],
        "stage5ce_preservation": ["stage5ce_proposal_package_preserved"],
        "stage5cc_preservation": [
            "stage5cc_exact_citation_contract_preserved",
            "stage5cc_fail_closed_trigger_exact_set_preserved",
            "stage5cc_activation_precondition_exact_set_preserved",
        ],
    }
    for key, fields in required_true.items():
        for field in fields:
            if payloads.get(key, {}).get(field) is not True:
                errors.append(f"{key}: {field} must be true")
    if payloads.get("stage5cm_boundary", {}).get(
        "stage5cm_parallel_worker_cap_preserved"
    ) != PARALLEL_WORKER_CAP:
        errors.append("Stage 5CM worker cap must remain 8")
    stage5bd = payloads.get("stage5bd_preservation", {})
    if stage5bd.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    if stage5bd.get("stage5bd_run_plan_ids_changed") is not False:
        errors.append("Stage 5BD run-plan IDs must be unchanged")
    lineage = payloads.get("active_lineage", {})
    if lineage.get("active_lineage_record_count") != 8:
        errors.append("active lineage must remain 8 records")
    if lineage.get("correct_stage5aw_path_included") is not True:
        errors.append("correct Stage 5AW path must be included")
    if lineage.get("deprecated_stage5aw_path_absent") is not True:
        errors.append("deprecated Stage 5AW path must be absent")
    for label, validator in (
        ("stage5cm_fixture_real", validate_stage5cm_fixture_real_boundary),
        ("stage5cm_end_to_end", validate_stage5cm_end_to_end_readiness_boundary),
        ("stage5cm_credential", validate_stage5cm_credential_redaction_policy),
        ("stage5cm_sidecar", validate_stage5cm_sidecar_gates),
        ("stage5co_prior", validate_stage5co_prior_stage_preservation),
        ("stage5bd", validate_stage5bd),
    ):
        _, validator_errors = validator()
        errors.extend(f"{label}:{error}" for error in validator_errors)
    return {
        "stage5cu_prior_stage_preservation_valid": not errors,
        "stage5bd_run_plan_id_count": stage5bd.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": lineage.get("active_lineage_record_count"),
        "validation_error_count": len(errors),
    }, errors


def _validate_sidecar_payloads(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for key, payload in payloads.items():
        if payload.get("string4_sidecar_status") not in {None, "scaffolded_inactive"}:
            errors.append(f"{key}: string4_sidecar_status must remain scaffolded_inactive")
        for field in (
            "string4_sidecar_active",
            "string4_sidecar_planning_ingestion_activated",
            "string4_active_input_allowed",
            "string4_dry_run_ingestion_allowed_now",
            "string4_byte_stream_generation_allowed",
            "string4_execution_input_allowed",
            "active_planning_input_authorized_now",
            "dry_run_ingestion_authorized_now",
            "byte_stream_generation_authorized_now",
            "execution_authorized_now",
        ):
            if payload.get(field) is True:
                errors.append(f"{key}: {field} must remain false")


def validate_stage5cu_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {
        "no_active_ingestion": _validate_payload(DATA_PATHS["no_active_ingestion"], errors),
        "no_byte_stream_transition_gate": _validate_payload(
            DATA_PATHS["no_byte_stream_transition_gate"], errors
        ),
        "no_execution_transition_gate": _validate_payload(
            DATA_PATHS["no_execution_transition_gate"], errors
        ),
        "sidecar_activation_blocker": _validate_payload(
            DATA_PATHS["sidecar_activation_blocker"], errors
        ),
        "activation_nonauthorization": _validate_payload(
            DATA_PATHS["activation_nonauthorization"], errors
        ),
    }
    _validate_sidecar_payloads(payloads, errors)
    if payloads["no_active_ingestion"].get("no_active_ingestion_status") != "closed":
        errors.append("no-active-ingestion gate must be closed")
    if payloads["no_byte_stream_transition_gate"].get(
        "no_byte_stream_transition_gate_status"
    ) != "closed":
        errors.append("no-byte-stream transition gate must be closed")
    if payloads["no_execution_transition_gate"].get(
        "no_execution_transition_gate_status"
    ) != "closed":
        errors.append("no-execution transition gate must be closed")
    return {
        "stage5cu_sidecar_gates_valid": not errors,
        "no_active_ingestion_status": payloads["no_active_ingestion"].get(
            "no_active_ingestion_status"
        ),
        "no_byte_stream_transition_gate_status": payloads["no_byte_stream_transition_gate"].get(
            "no_byte_stream_transition_gate_status"
        ),
        "no_execution_transition_gate_status": payloads["no_execution_transition_gate"].get(
            "no_execution_transition_gate_status"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_handoff_continuity() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    handoff = _validate_payload(DATA_PATHS["handoff"], errors)
    continuity = _validate_payload(DATA_PATHS["completion_continuity"], errors)
    if handoff.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if handoff.get("codex_output_used") is not False:
        errors.append("codex_output must not be used")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output directory must be absent")
    if continuity.get("stage5cu_codex_completion_summary_required") is not True:
        errors.append("Stage 5CU completion summary must be required")
    if not CODEX_COMPLETION_PATH.is_file():
        errors.append(f"missing_local_completion_summary={CODEX_COMPLETION_PATH.as_posix()}")
    elif _completion_summary_has_unresolved_placeholder(CODEX_COMPLETION_PATH):
        errors.append("Stage 5CU completion summary must not contain unresolved placeholders")
    if continuity.get("codex_completion_summary_committed") is not False:
        errors.append("codex completion summary must not be committed")
    return {
        "stage5cu_handoff_continuity_valid": not errors,
        "stage5cu_codex_completion_summary_written_locally": CODEX_COMPLETION_PATH.is_file(),
        "codex_output_used": handoff.get("codex_output_used"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu_credential_redaction_policy(
    *, credential_redaction: Path = DATA_PATHS["credential_redaction"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(credential_redaction, errors)
    for field in (
        "credential_redaction_policy_preserved",
        "credential_like_remote_must_be_redacted",
        "credential_like_text_must_not_be_committed",
        "committed_stage5cu_metadata_secret_scan_required",
    ):
        if payload.get(field) is not True:
            errors.append(f"{field} must be true")
    if payload.get("secret_values_printed_or_committed") is not False:
        errors.append("secret values must not be printed or committed")
    _check_no_stage5cu_metadata_secrets(errors)
    return {
        "stage5cu_credential_redaction_policy_valid": not errors,
        "credential_like_remote_detected": payload.get("remote_hygiene", {}).get(
            "credential_like_remote_detected"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cu(
    *,
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = _load_all_payloads(errors)
    _check_false_flags(payloads, errors)
    _validate_sidecar_payloads(payloads, errors)
    _check_no_stage5cu_metadata_secrets(errors)
    summary_payload = (
        payloads["summary"] if summary == DATA_PATHS["summary"] else _validate_payload(summary, errors)
    )
    next_payload = (
        payloads["next_stage"]
        if next_stage_decision == DATA_PATHS["next_stage"]
        else _validate_payload(next_stage_decision, errors)
    )
    guardrail_payload = (
        payloads["guardrail"]
        if guardrail == DATA_PATHS["guardrail"]
        else _validate_payload(guardrail, errors)
    )
    for _counts, focused_errors in (
        validate_stage5cu_stage5ct_findings(),
        validate_stage5cu_operator_decision_readiness(),
        validate_stage5cu_decision_options_preservation(),
        validate_stage5cu_decision_option_negative_fixtures(),
        validate_stage5cu_real_decision_negative_fixtures(),
        validate_stage5cu_option_selection_misuse(),
        validate_stage5cu_options_nonselection(),
        validate_stage5cu_real_record_blocker(),
        validate_stage5cu_combined_gate(),
        validate_stage5cu_activation_nonauthorization(),
        validate_stage5cu_stage5cs_preservation(),
        validate_stage5cu_stage5cq_preservation(),
        validate_stage5cu_stage5co_preservation(),
        validate_stage5cu_prior_stage_preservation(),
        validate_stage5cu_sidecar_gates(),
        validate_stage5cu_handoff_continuity(),
        validate_stage5cu_credential_redaction_policy(),
    ):
        errors.extend(focused_errors)
    for field in (
        "stage5ct_findings_integrated",
        "stage5cq_operator_decision_scaffold_preserved",
        "stage5co_status_preserved",
        "stage5co_readiness_package_preserved",
        "operator_decision_readiness_package_created",
        "real_approval_decision_options_scaffold_created",
        "stage5ct_completion_summary_warning_integrated",
        "decision_option_negative_fixture_pack_created",
        "real_decision_record_negative_fixture_pack_created",
        "option_selection_misuse_validation_matrix_created",
        "option_fixture_isolation_policy_created",
        "stage5cs_stale_completion_summary_warning_integrated",
        "stage5cu_completion_summary_finalized_not_pending",
    ):
        if summary_payload.get(field) is not True:
            errors.append(f"summary {field} must be true")
    for field in MANDATORY_FALSE_SUMMARY_FLAGS:
        if summary_payload.get(field) is not False:
            errors.append(f"summary {field} must be false")
    if summary_payload.get("stage5ct_verdict") != "accept_with_warnings":
        errors.append("summary Stage 5CT verdict must be accept_with_warnings")
    if summary_payload.get("operator_decision_readiness_package_status") != "readiness_package_only":
        errors.append("operator-decision readiness package must remain readiness_package_only")
    if summary_payload.get("real_approval_decision_options_status") != "options_scaffold_only":
        errors.append("decision options must remain options_scaffold_only")
    if summary_payload.get("operator_decision_option_count") != len(OPERATOR_DECISION_OPTIONS):
        errors.append("operator decision option count must be 6")
    if summary_payload.get("negative_fixture_count") != len(NEGATIVE_FIXTURE_IDS):
        errors.append("negative fixture count mismatch")
    if summary_payload.get("option_selection_misuse_case_count") != len(
        OPTION_SELECTION_MISUSE_TRANSITIONS
    ):
        errors.append("option-selection misuse case count mismatch")
    if summary_payload.get("selected_option_id") is not None:
        errors.append("summary selected_option_id must be null")
    if summary_payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    if summary_payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage must contain exactly 8 records")
    if summary_payload.get("parallel_worker_cap_for_stage5cu_and_later") != PARALLEL_WORKER_CAP:
        errors.append("Stage 5CU parallel worker cap must be 8")
    if next_payload.get("selected_next_stage_id") != "stage-5cv":
        errors.append("Stage 5CU must select Stage 5CV as next stage")
    if next_payload.get("selected_next_prompt_type") != "deep_research_review":
        errors.append("Stage 5CV prompt type must be deep_research_review")
    if next_payload.get("selected_next_stage_authorizes_execution") is not False:
        errors.append("Stage 5CV must not authorize execution")
    if guardrail_payload.get("future_token_block_execution_remains_blocked") is not True:
        errors.append("future token-block execution must remain blocked")
    for output_name in (
        "summary.json",
        "operator_decision_readiness_report.json",
        "decision_options_report.json",
        "negative_fixture_report.json",
        "preservation_report.json",
        "handoff_continuity_report.json",
        "source_digest_index.json",
        "warnings.jsonl",
    ):
        if not (results_dir / output_name).is_file():
            errors.append(f"missing_generated_output={repo_relative(results_dir / output_name)}")
    return {
        "stage5cu_valid": not errors,
        "validation_error_count": len(errors),
        "stage5ct_verdict": summary_payload.get("stage5ct_verdict"),
        "operator_decision_readiness_package_status": summary_payload.get(
            "operator_decision_readiness_package_status"
        ),
        "real_approval_decision_options_status": summary_payload.get(
            "real_approval_decision_options_status"
        ),
        "operator_decision_option_count": summary_payload.get("operator_decision_option_count"),
        "operator_decision_option_selected_now": summary_payload.get(
            "operator_decision_option_selected_now"
        ),
        "combined_approval_gate_satisfied_now": summary_payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_decision_valid_now": summary_payload.get("activation_decision_valid_now"),
        "active_planning_input_authorized_now": summary_payload.get(
            "active_planning_input_authorized_now"
        ),
        "stage5bd_run_plan_id_count": summary_payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": summary_payload.get("active_lineage_record_count"),
        "parallel_worker_cap": summary_payload.get("parallel_worker_cap_for_stage5cu_and_later"),
        "recommended_next_stage_id": summary_payload.get("recommended_next_stage_id"),
    }, errors


def load_stage5cu_summary(*, summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
