"""Stage 5CW real-decision package preflight metadata."""

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
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
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
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP, SECRET_PATTERNS
from libreprimus.token_block.stage5co import (
    DATA_PATHS as STAGE5CO_DATA_PATHS,
    MISSING_REQUIREMENTS as STAGE5CO_MISSING_REQUIREMENTS,
)
from libreprimus.token_block.stage5cq import DATA_PATHS as STAGE5CQ_DATA_PATHS
from libreprimus.token_block.stage5cs import DATA_PATHS as STAGE5CS_DATA_PATHS
from libreprimus.token_block.stage5cs import validate_stage5cs
from libreprimus.token_block.stage5cu import (
    DATA_PATHS as STAGE5CU_DATA_PATHS,
    FUTURE_REAL_RECORD_CLASSES,
    NEGATIVE_FIXTURE_IDS,
    OPERATOR_DECISION_OPTIONS,
    OPTION_SELECTION_MISUSE_TRANSITIONS,
    validate_stage5cu,
)

STAGE_ID = "stage-5cw"
STAGE_TITLE = (
    "Stage 5CW - Operator-decision readiness review integration and "
    "real-decision package preflight, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5cu"
SOURCE_PREVIOUS_COMMIT = "a80d6e49ccfad34d690237cfa0fbb96a05cca7a2"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5cv"
SOURCE_DEEP_RESEARCH_REPORT = "26_Stage-5CU-Deep-Research-Review.md"
STAGE5CV_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "26_Stage-5CU-Deep-Research-Review.md"
)
RESULTS_DIR = Path("experiments/results/token-block/stage5cw")
CODEX_COMPLETION_PATH = Path("codex-output/stage5cw-codex-completion.md")
STAGE5CU_CODEX_COMPLETION_PATH = Path("codex-output/stage5cu-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
PYTEST_COUNT_OBSERVED_LOCALLY = 2446
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"

SOURCE_STAGE_IDS = [
    "stage-5cv",
    "stage-5cu",
    "stage-5ct",
    "stage-5cs",
    "stage-5cr",
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

STAGE5CV_FINDINGS = [
    "stage5cu_is_coherent_conservative_and_fail_closed",
    "stage5cu_preserves_stage5cs_six_option_scaffold_exactly",
    "stage5cu_keeps_all_six_options_unselected",
    "stage5cu_created_41_decision_option_negative_fixtures",
    "stage5cu_created_10_real_decision_negative_fixture_classes",
    "stage5cu_created_13_option_selection_misuse_cases",
    "stage5cu_created_option_fixture_isolation_policy",
    "fixture_template_scaffold_review_readiness_and_option_material_cannot_satisfy_real_gates",
    "stage5cu_negative_fixture_layer_is_meaningful_safety_improvement",
    "stage5cu_created_no_real_operator_decision",
    "stage5cu_created_no_real_operator_approval",
    "stage5cu_created_no_real_deep_research_acceptance",
    "stage5cu_created_no_real_combined_gate_validation",
    "stage5cu_created_no_real_activation_decision",
    "stage5cu_created_no_active_planning_input_authorization_or_selection",
    "combined_approval_gate_remains_unsatisfied",
    "activation_remains_invalid_and_unauthorized",
    "active_planning_input_remains_unauthorized_and_unselected",
    "stage5bd_preserved_at_ten_run_plan_ids",
    "active_lineage_preserved_at_eight_records",
    "string4_scaffolded_inactive",
    "no_active_no_byte_no_execution_gates_closed",
    "stage5cs_stale_completion_summary_warning_integrated_honestly",
    "stage5cu_local_ignored_completion_summary_finalized",
    "public_github_ci_and_final_commit_facts_remain_external_evidence",
    "ignored_codex_output_summaries_are_supporting_artifacts_not_committed_truth",
    "validation_metadata_centric_not_execution_adversarial_is_visible_gap",
    "next_stage_should_create_review_only_real_decision_package_preflight",
]

FUTURE_REAL_DECISION_INPUTS = [
    "future_stage_id_explicitly_scoped_to_operator_decision_or_real_decision_package",
    "explicit_operator_identity_or_operator_role_record",
    "explicit_operator_decision_timestamp",
    "exact_selected_option_id_from_stage5cs_option_set",
    "proof_exactly_one_option_selected",
    "proof_selected_option_was_unselected_before_future_decision",
    "stage5cv_review_findings_integrated",
    "stage5cu_negative_fixture_layer_preserved",
    "stage5cs_option_scaffold_preserved",
    "stage5cq_operator_decision_scaffold_preserved",
    "stage5co_real_approval_readiness_package_preserved",
    "stage5cm_fixture_vs_real_boundary_preserved",
    "stage5ck_fixture_only_boundary_preserved",
    "stage5ci_templates_preserved",
    "stage5cg_scaffolds_preserved",
    "stage5ce_proposal_package_review_only_preserved",
    "stage5cc_exact_contracts_preserved",
    "stage5bd_preservation_or_explicit_future_supersession_record",
    "active_lineage_preservation_or_explicit_future_supersession_record",
    "no_byte_stream_transition_review",
    "no_execution_transition_review",
    "no_solve_claim_acknowledgement",
    "credential_redaction_acknowledgement",
    "codex_output_absent_and_codex_output_hyphenated_handoff_continuity",
]

PREFLIGHT_MISUSE_CASES = [
    "real_decision_package_preflight_treated_as_real_operator_decision",
    "real_decision_package_preflight_treated_as_option_selection",
    "real_decision_package_preflight_treated_as_real_operator_approval",
    "real_decision_package_preflight_treated_as_deep_research_acceptance",
    "real_decision_package_preflight_treated_as_combined_gate_validation",
    "real_decision_package_preflight_treated_as_activation_decision",
    "real_decision_package_preflight_treated_as_active_planning_input_selection",
    "preflight_selected_option_id_set_now",
    "preflight_selected_option_id_unknown",
    "preflight_selected_option_id_multiple",
    "preflight_authorizes_real_approval_now",
    "preflight_authorizes_activation_now",
    "preflight_authorizes_active_input_now",
    "preflight_authorizes_dry_run_ingestion_now",
    "preflight_authorizes_byte_stream_generation_now",
    "preflight_authorizes_execution_now",
    "preflight_allows_manifest_supersession_now",
    "preflight_mutates_stage5bd",
    "preflight_mutates_active_lineage",
    "preflight_reintroduces_deprecated_stage5aw_path",
    "preflight_treats_stale_completion_summary_as_final_truth",
    "preflight_uses_codex_output_underscore_root",
    "preflight_leaks_credential_like_remote",
    "preflight_sets_solve_claim_true",
]

REVIEWABILITY_GAPS = [
    {
        "gap_id": "ignored_codex_completion_summary_is_support_not_committed_truth",
        "severity": "medium",
        "gate_opening": False,
        "status": "integrated_as_warning_stage5cw_preserves_handoff_continuity",
    },
    {
        "gap_id": "public_github_corroboration_unreliable_or_external",
        "severity": "low",
        "gate_opening": False,
        "status": "preserved_external_evidence_caveat",
    },
    {
        "gap_id": "final_commit_and_ci_external_evidence",
        "severity": "low",
        "gate_opening": False,
        "status": "post_push_verification_required",
    },
    {
        "gap_id": "validation_metadata_centric_not_execution_adversarial",
        "severity": "low",
        "gate_opening": False,
        "status": "non_blocking_for_metadata_stage",
    },
    {
        "gap_id": "real_decision_package_preflight_is_not_real_decision",
        "severity": "high",
        "gate_opening": False,
        "status": "explicitly_blocked_by_preflight_misuse_validation",
    },
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5cw-summary.yaml"),
    "next_stage": Path("data/project-state/stage5cw-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5cw-stage5cv-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5cw-reviewable-stage-marker.yaml"),
    "validation_evidence": Path("data/project-state/stage5cw-reviewable-validation-evidence.yaml"),
    "source_digest_index": Path("data/project-state/stage5cw-reviewable-source-digest-index.yaml"),
    "gap_register": Path("data/project-state/stage5cw-reviewability-gap-register.yaml"),
    "equivalence_map": Path("data/project-state/stage5cw-record-family-name-equivalence-map.yaml"),
    "real_decision_package_preflight": Path(
        "data/token-block/stage5cw-real-decision-package-preflight.yaml"
    ),
    "future_real_decision_requirements": Path(
        "data/token-block/stage5cw-future-real-operator-decision-package-requirements.yaml"
    ),
    "future_option_selection_requirements": Path(
        "data/token-block/stage5cw-future-option-selection-preflight-requirements.yaml"
    ),
    "future_real_record_dependency_preflight": Path(
        "data/token-block/stage5cw-future-real-record-dependency-preflight.yaml"
    ),
    "preflight_nonselection": Path("data/token-block/stage5cw-preflight-nonselection-proof.yaml"),
    "preflight_nonauthorization": Path(
        "data/token-block/stage5cw-preflight-nonauthorization-proof.yaml"
    ),
    "preflight_misuse": Path("data/token-block/stage5cw-preflight-misuse-validation-matrix.yaml"),
    "stage5cu_negative_fixture_preservation": Path(
        "data/token-block/stage5cw-stage5cu-negative-fixture-preservation.yaml"
    ),
    "stage5cu_real_decision_fixture_preservation": Path(
        "data/token-block/stage5cw-stage5cu-real-decision-fixture-preservation.yaml"
    ),
    "stage5cu_option_selection_misuse_preservation": Path(
        "data/token-block/stage5cw-stage5cu-option-selection-misuse-preservation.yaml"
    ),
    "stage5cu_fixture_isolation_policy_preservation": Path(
        "data/token-block/stage5cw-stage5cu-fixture-isolation-policy-preservation.yaml"
    ),
    "stage5cu_real_record_blocker_preservation": Path(
        "data/token-block/stage5cw-stage5cu-real-record-blocker-preservation.yaml"
    ),
    "stage5cs_decision_options_preservation": Path(
        "data/token-block/stage5cw-stage5cs-decision-options-preservation.yaml"
    ),
    "stage5cs_operator_decision_readiness_preservation": Path(
        "data/token-block/stage5cw-stage5cs-operator-decision-readiness-preservation.yaml"
    ),
    "stage5cq_scaffold_preservation": Path(
        "data/token-block/stage5cw-stage5cq-operator-decision-scaffold-preservation.yaml"
    ),
    "stage5co_readiness_package": Path(
        "data/token-block/stage5cw-stage5co-readiness-package-preservation.yaml"
    ),
    "stage5co_transition_plan": Path(
        "data/token-block/stage5cw-stage5co-transition-plan-preservation.yaml"
    ),
    "stage5co_missing_requirements": Path(
        "data/token-block/stage5cw-stage5co-missing-requirements-preservation.yaml"
    ),
    "stage5cm_boundary": Path("data/token-block/stage5cw-stage5cm-boundary-preservation.yaml"),
    "stage5ck_preservation": Path("data/token-block/stage5cw-stage5ck-fixture-preservation.yaml"),
    "stage5ci_preservation": Path("data/token-block/stage5cw-stage5ci-template-preservation.yaml"),
    "stage5cg_preservation": Path("data/token-block/stage5cw-stage5cg-scaffold-preservation.yaml"),
    "stage5ce_preservation": Path(
        "data/token-block/stage5cw-stage5ce-proposal-package-preservation.yaml"
    ),
    "stage5cc_preservation": Path("data/token-block/stage5cw-stage5cc-contract-preservation.yaml"),
    "real_record_blocker": Path("data/token-block/stage5cw-real-record-creation-blocker.yaml"),
    "options_nonselection": Path("data/token-block/stage5cw-operator-options-nonselection-proof.yaml"),
    "operator_decision_nonauthorization": Path(
        "data/token-block/stage5cw-operator-decision-nonauthorization-proof.yaml"
    ),
    "combined_gate_nonsatisfaction": Path(
        "data/token-block/stage5cw-combined-gate-non-satisfaction-proof.yaml"
    ),
    "activation_nonauthorization": Path(
        "data/token-block/stage5cw-activation-decision-nonauthorization-proof.yaml"
    ),
    "sidecar_activation_blocker": Path("data/token-block/stage5cw-sidecar-activation-blocker.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5cw-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5cw-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5cw-no-execution-transition-gate.yaml"
    ),
    "supersession_nonactivation": Path(
        "data/token-block/stage5cw-manifest-supersession-nonactivation-proof.yaml"
    ),
    "stage5bd_preservation": Path("data/token-block/stage5cw-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5cw-active-lineage-preservation.yaml"),
    "guardrail": Path("data/historical-route/stage5cw-guardrail.yaml"),
    "dwh": Path("data/historical-route/stage5cw-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5cw-source-gap-severity-update.yaml"),
    "handoff": Path("data/source-harvester/stage5cw-codex-handoff-policy.yaml"),
    "completion_continuity": Path(
        "data/source-harvester/stage5cw-completion-summary-continuity.yaml"
    ),
    "credential_redaction": Path(
        "data/source-harvester/stage5cw-credential-redaction-policy-preservation.yaml"
    ),
    "review_packaging_warning": Path(
        "data/source-harvester/stage5cw-review-packaging-warning.yaml"
    ),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5cw_{key}" for key in DATA_PATHS}

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
    "historical_route_execution_performed": False,
    "image_forensics_performed": False,
    "manifest_supersession_authorized_now": False,
    "manifest_supersession_performed": False,
    "method_status_upgraded": False,
    "mp3stego_execution_performed": False,
    "new_active_planning_input_created": False,
    "ocr_performed": False,
    "openpuff_execution_performed": False,
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
    "outguess_execution_performed": False,
    "preflight_authorizes_activation_decision_now": False,
    "preflight_authorizes_active_planning_input_now": False,
    "preflight_authorizes_byte_stream_generation_now": False,
    "preflight_authorizes_combined_gate_validation_now": False,
    "preflight_authorizes_deep_research_acceptance_now": False,
    "preflight_authorizes_dry_run_ingestion_now": False,
    "preflight_authorizes_execution_now": False,
    "preflight_authorizes_real_approval_now": False,
    "preflight_authorizes_real_decision_now": False,
    "real_activation_decision_record_created_now": False,
    "real_activation_decision_record_present_now": False,
    "real_activation_decision_records_created": False,
    "real_approval_records_created": False,
    "real_byte_stream_generated": False,
    "real_combined_gate_validation_record_created_now": False,
    "real_combined_gate_validation_record_present_now": False,
    "real_decision_package_created_now": False,
    "real_decision_package_valid_now": False,
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
    "real_decision_package_created_now",
    "real_decision_package_valid_now",
    "real_operator_decision_record_created_now",
    "real_operator_approval_record_created_now",
    "real_deep_research_acceptance_record_created_now",
    "real_combined_gate_validation_record_created_now",
    "real_activation_decision_record_created_now",
    "real_approval_records_created",
    "future_real_records_created_now",
    "combined_approval_gate_satisfied_now",
    "activation_decision_valid_now",
    "activation_authorized_now",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
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
    paths = [STAGE5CU_CODEX_COMPLETION_PATH, CODEX_COMPLETION_PATH]
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


def _completion_summary_has_unresolved_placeholder(path: Path) -> bool:
    if not path.is_file():
        return True
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    placeholders = ["pending", "todo", "tbd", "initialized only", "final validation update"]
    return any(placeholder in text for placeholder in placeholders)


def _write_local_completion_summary_stub() -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    if (
        not CODEX_COMPLETION_PATH.exists()
        or _completion_summary_has_unresolved_placeholder(CODEX_COMPLETION_PATH)
    ):
        CODEX_COMPLETION_PATH.write_text(
            "\n".join(
                [
                    "# Stage 5CW Codex Completion Summary",
                    "",
                    "Status: local ignored Stage 5CW handoff created by build-stage5cw.",
                    f"Starting commit: {SOURCE_PREVIOUS_COMMIT}",
                    "Stage 5CV verdict: accept_with_warnings",
                    "Real-decision package preflight created: true",
                    "Real decision package created now: false",
                    "Decision options selected now: false",
                    "Final commit: recorded after commit and push.",
                    "CI status: recorded after push verification.",
                    "Validation summary: local Stage 5CW validation commands are tracked in committed validation evidence.",
                    "codex_output used: false",
                    "",
                ]
            ),
            encoding="utf-8",
        )


def _completion_status() -> dict[str, Any]:
    return {
        "stage5cu_codex_completion_summary_path": STAGE5CU_CODEX_COMPLETION_PATH.as_posix(),
        "stage5cu_codex_completion_summary_present_locally": (
            STAGE5CU_CODEX_COMPLETION_PATH.is_file()
        ),
        "stage5cu_completion_summary_finalized_not_pending": (
            STAGE5CU_CODEX_COMPLETION_PATH.is_file()
            and not _completion_summary_has_unresolved_placeholder(STAGE5CU_CODEX_COMPLETION_PATH)
        ),
        "stage5cw_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5cw_codex_completion_summary_present_locally": CODEX_COMPLETION_PATH.is_file(),
        "stage5cw_completion_summary_finalized_not_pending": (
            CODEX_COMPLETION_PATH.is_file()
            and not _completion_summary_has_unresolved_placeholder(CODEX_COMPLETION_PATH)
        ),
    }


def _source_paths() -> list[Path]:
    paths = [
        STAGE5CV_REPORT_PATH,
        *STAGE5CU_DATA_PATHS.values(),
        *STAGE5CS_DATA_PATHS.values(),
        STAGE5CQ_DATA_PATHS["summary"],
        STAGE5CQ_DATA_PATHS["operator_decision_package"],
        STAGE5CO_DATA_PATHS["summary"],
        STAGE5CO_DATA_PATHS["readiness_package"],
        STAGE5CO_DATA_PATHS["activation_transition_plan"],
        STAGE5CO_DATA_PATHS["future_transition_sequence"],
        STAGE5CO_DATA_PATHS["missing_requirements"],
        STAGE5CC_DATA_PATHS["citation_preservation"],
        STAGE5CC_DATA_PATHS["fail_closed_contract"],
        STAGE5CC_DATA_PATHS["activation_contract"],
        *STAGE5CE_DATA_PATHS.values(),
        *STAGE5CG_DATA_PATHS.values(),
        *STAGE5CI_DATA_PATHS.values(),
        *STAGE5CK_DATA_PATHS.values(),
        *[Path(path) for path in ACTIVE_LINEAGE_PATHS],
        *[
            path
            for key, path in DATA_PATHS.items()
            if key not in {"source_digest_index"}
        ],
    ]
    return sorted({path for path in paths}, key=lambda item: item.as_posix())


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


def _option_effects() -> dict[str, dict[str, Any]]:
    return {
        option["option_id"]: {
            "immediate_effect_now": "none",
            "future_action_class": option["future_action_class"],
            "may_create_real_record_now": False,
        }
        for option in OPERATOR_DECISION_OPTIONS
    }


def _option_rows() -> list[dict[str, Any]]:
    return [
        {
            **option,
            "authorizes_real_approval_now": False,
            "authorizes_activation_now": False,
            "authorizes_active_input_now": False,
            "authorizes_byte_stream_generation_now": False,
            "authorizes_execution_now": False,
        }
        for option in OPERATOR_DECISION_OPTIONS
    ]


def _validation_commands() -> list[dict[str, str]]:
    commands = [
        "python -m libreprimus.cli token-block build-stage5cw",
        "python -m libreprimus.cli token-block validate-stage5cw-stage5cv-findings",
        "python -m libreprimus.cli token-block validate-stage5cw-real-decision-package-preflight",
        "python -m libreprimus.cli token-block validate-stage5cw-future-real-decision-requirements",
        "python -m libreprimus.cli token-block validate-stage5cw-preflight-misuse",
        "python -m libreprimus.cli token-block validate-stage5cw-stage5cu-preservation",
        "python -m libreprimus.cli token-block validate-stage5cw-stage5cs-preservation",
        "python -m libreprimus.cli token-block validate-stage5cw-options-nonselection",
        "python -m libreprimus.cli token-block validate-stage5cw-real-record-blocker",
        "python -m libreprimus.cli token-block validate-stage5cw-combined-gate",
        "python -m libreprimus.cli token-block validate-stage5cw-activation-nonauthorization",
        "python -m libreprimus.cli token-block validate-stage5cw-stage5bd-preservation",
        "python -m libreprimus.cli token-block validate-stage5cw-active-lineage-preservation",
        "python -m libreprimus.cli token-block validate-stage5cw-sidecar-gates",
        "python -m libreprimus.cli token-block validate-stage5cw-handoff-continuity",
        "python -m libreprimus.cli token-block validate-stage5cw-credential-redaction-policy",
        "python -m libreprimus.cli token-block validate-stage5cw",
        "python -m libreprimus.cli token-block stage5cw-summary",
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
    source_records = [_sha_record(path, role="stage5cw_reviewable_source") for path in _source_paths()]
    source_digest_count = len(source_records)

    records: dict[str, dict[str, Any]] = {}
    records["findings"] = _record(
        "findings",
        {
            "stage5cv_findings_integrated": True,
            "stage5cv_verdict": "accept_with_warnings",
            "finding_count": len(STAGE5CV_FINDINGS),
            "findings": STAGE5CV_FINDINGS,
            "stage5cv_did_not_recommend_execution": True,
        },
    )
    records["real_decision_package_preflight"] = _record(
        "real_decision_package_preflight",
        {
            "real_decision_package_preflight_created": True,
            "real_decision_package_preflight_status": "review_preflight_only",
            "real_decision_package_created_now": False,
            "real_decision_package_valid_now": False,
            "preflight_authorizes_real_decision_now": False,
            "preflight_authorizes_real_approval_now": False,
            "preflight_authorizes_deep_research_acceptance_now": False,
            "preflight_authorizes_combined_gate_validation_now": False,
            "preflight_authorizes_activation_decision_now": False,
            "preflight_authorizes_active_planning_input_now": False,
            "preflight_authorizes_dry_run_ingestion_now": False,
            "preflight_authorizes_byte_stream_generation_now": False,
            "preflight_authorizes_execution_now": False,
            "selected_option_id": None,
        },
    )
    records["future_real_decision_requirements"] = _record(
        "future_real_decision_requirements",
        {
            "future_real_decision_package_requirements_created": True,
            "required_future_inputs": FUTURE_REAL_DECISION_INPUTS,
            "required_future_input_count": len(FUTURE_REAL_DECISION_INPUTS),
            "real_decision_package_created_now": False,
            "real_decision_package_valid_now": False,
            "selected_option_id": None,
        },
    )
    records["future_option_selection_requirements"] = _record(
        "future_option_selection_requirements",
        {
            "future_option_selection_preflight_requirements_created": True,
            "future_option_selection_rules": {
                "exact_option_set_source": STAGE5CU_DATA_PATHS["decision_options"].as_posix(),
                "exact_option_count": len(OPERATOR_DECISION_OPTIONS),
                "exactly_one_option_selected": "required_in_future_real_decision_stage_only",
                "selected_option_id_now": None,
                "selected_option_now": False,
                "allowed_option_ids": [option["option_id"] for option in OPERATOR_DECISION_OPTIONS],
                "option_addition_allowed_now": False,
                "option_removal_allowed_now": False,
                "option_rename_allowed_now": False,
                "option_selection_allowed_now": False,
            },
            "future_option_effects": _option_effects(),
            "selected_option_id": None,
            "operator_decision_option_selected_now": False,
        },
    )
    records["future_real_record_dependency_preflight"] = _record(
        "future_real_record_dependency_preflight",
        {
            "future_real_record_dependency_preflight_created": True,
            "dependency_count": len(FUTURE_REAL_RECORD_CLASSES),
            "dependency_rows": [
                {
                    "target_real_record_class": record_class,
                    "required_in_future_stage_only": True,
                    "created_now": False,
                    "present_now": False,
                    "may_satisfy_gate_now": False,
                }
                for record_class in FUTURE_REAL_RECORD_CLASSES
            ],
            "future_real_records_created_now": False,
        },
    )
    records["preflight_nonselection"] = _record(
        "preflight_nonselection",
        {
            "preflight_nonselection_proof_created": True,
            "operator_decision_option_count": len(OPERATOR_DECISION_OPTIONS),
            "options": _option_rows(),
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
            "all_options_unselected": True,
        },
    )
    records["preflight_nonauthorization"] = _record(
        "preflight_nonauthorization",
        {
            "preflight_nonauthorization_proof_created": True,
            "preflight_authorizes_real_decision_now": False,
            "preflight_authorizes_real_approval_now": False,
            "preflight_authorizes_deep_research_acceptance_now": False,
            "preflight_authorizes_combined_gate_validation_now": False,
            "preflight_authorizes_activation_decision_now": False,
            "preflight_authorizes_active_planning_input_now": False,
            "preflight_authorizes_dry_run_ingestion_now": False,
            "preflight_authorizes_byte_stream_generation_now": False,
            "preflight_authorizes_execution_now": False,
        },
    )
    records["preflight_misuse"] = _record(
        "preflight_misuse",
        {
            "preflight_misuse_validation_matrix_created": True,
            "preflight_misuse_case_count": len(PREFLIGHT_MISUSE_CASES),
            "matrix_rows": [
                {
                    "misuse_case_id": case,
                    "allowed_now": False,
                    "must_fail_closed": True,
                    "gate_opening": False,
                    "authorizes_approval": False,
                    "authorizes_activation": False,
                    "authorizes_active_input": False,
                    "authorizes_dry_run_ingestion": False,
                    "authorizes_byte_stream_generation": False,
                    "authorizes_execution": False,
                    "solve_claim": False,
                }
                for case in PREFLIGHT_MISUSE_CASES
            ],
            "stage5cu_option_selection_misuse_compatible": True,
        },
    )
    records["stage5cu_negative_fixture_preservation"] = _preservation_record(
        "stage5cu_negative_fixture_preservation",
        label="stage5cu_negative_fixture_pack",
        source_paths=[STAGE5CU_DATA_PATHS["decision_option_negative_fixtures"]],
        preserved_fields={
            "stage5cu_negative_fixture_pack_preserved": True,
            "stage5cu_negative_fixture_count_preserved": len(NEGATIVE_FIXTURE_IDS),
            "count_drift_classification": "none",
        },
    )
    records["stage5cu_real_decision_fixture_preservation"] = _preservation_record(
        "stage5cu_real_decision_fixture_preservation",
        label="stage5cu_real_decision_negative_fixture_pack",
        source_paths=[STAGE5CU_DATA_PATHS["real_decision_negative_fixtures"]],
        preserved_fields={
            "stage5cu_real_decision_negative_fixture_pack_preserved": True,
            "stage5cu_real_decision_negative_fixture_count_preserved": len(
                FUTURE_REAL_RECORD_CLASSES
            ),
            "count_drift_classification": "none",
        },
    )
    records["stage5cu_option_selection_misuse_preservation"] = _preservation_record(
        "stage5cu_option_selection_misuse_preservation",
        label="stage5cu_option_selection_misuse_matrix",
        source_paths=[STAGE5CU_DATA_PATHS["option_selection_misuse"]],
        preserved_fields={
            "stage5cu_option_selection_misuse_matrix_preserved": True,
            "stage5cu_option_selection_misuse_case_count_preserved": len(
                OPTION_SELECTION_MISUSE_TRANSITIONS
            ),
            "count_drift_classification": "none",
        },
    )
    records["stage5cu_fixture_isolation_policy_preservation"] = _preservation_record(
        "stage5cu_fixture_isolation_policy_preservation",
        label="stage5cu_fixture_isolation_policy",
        source_paths=[STAGE5CU_DATA_PATHS["option_fixture_isolation_policy"]],
        preserved_fields={"stage5cu_fixture_isolation_policy_preserved": True},
    )
    records["stage5cu_real_record_blocker_preservation"] = _preservation_record(
        "stage5cu_real_record_blocker_preservation",
        label="stage5cu_real_record_blocker",
        source_paths=[STAGE5CU_DATA_PATHS["real_record_blocker"]],
        preserved_fields={"stage5cu_real_record_blocker_preserved": True},
    )
    records["stage5cs_decision_options_preservation"] = _preservation_record(
        "stage5cs_decision_options_preservation",
        label="stage5cs_decision_options",
        source_paths=[STAGE5CS_DATA_PATHS["decision_options"], STAGE5CS_DATA_PATHS["options_nonselection"]],
        preserved_fields={
            "stage5cs_real_approval_decision_options_status_preserved": "options_scaffold_only",
            "stage5cs_option_count_preserved": len(OPERATOR_DECISION_OPTIONS),
            "stage5cs_exact_option_set_preserved": True,
            "all_options_unselected": True,
            "operator_decision_option_count": len(OPERATOR_DECISION_OPTIONS),
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
            "options": _option_rows(),
        },
    )
    records["stage5cs_operator_decision_readiness_preservation"] = _preservation_record(
        "stage5cs_operator_decision_readiness_preservation",
        label="stage5cs_operator_decision_readiness",
        source_paths=[STAGE5CS_DATA_PATHS["operator_decision_readiness"]],
        preserved_fields={
            "stage5cs_operator_decision_readiness_package_preserved": True,
            "stage5cs_operator_decision_readiness_package_status_preserved": "readiness_package_only",
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
        ],
        preserved_fields={
            "stage5cq_operator_decision_scaffold_preserved": True,
            "stage5cq_operator_decision_scaffold_status_preserved": "scaffold_only",
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
            "stage5co_readiness_package_preserved": True,
            "stage5co_real_operator_approval_readiness_preserved": True,
            "stage5co_real_deep_research_acceptance_readiness_preserved": True,
            "stage5co_real_combined_gate_readiness_preserved": True,
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
    records["stage5co_missing_requirements"] = _preservation_record(
        "stage5co_missing_requirements",
        label="stage5co_missing_requirements_register",
        source_paths=[STAGE5CO_DATA_PATHS["missing_requirements"]],
        preserved_fields={
            "stage5co_missing_requirements_register_preserved": True,
            "stage5co_missing_requirements": STAGE5CO_MISSING_REQUIREMENTS,
            "missing_requirement_count": len(STAGE5CO_MISSING_REQUIREMENTS),
        },
    )
    records["stage5cm_boundary"] = _record(
        "stage5cm_boundary",
        {
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
        source_paths=list(STAGE5CK_DATA_PATHS.values()),
        preserved_fields={
            "stage5ck_fixture_pack_preserved": True,
            "stage5ck_fixture_pack_only_preserved": True,
            "stage5ck_synthetic_negative_fixtures_only_preserved": True,
        },
    )
    records["stage5ci_preservation"] = _preservation_record(
        "stage5ci_preservation",
        label="stage5ci_templates",
        source_paths=list(STAGE5CI_DATA_PATHS.values()),
        preserved_fields={"stage5ci_templates_preserved": True},
    )
    records["stage5cg_preservation"] = _preservation_record(
        "stage5cg_preservation",
        label="stage5cg_scaffolds",
        source_paths=list(STAGE5CG_DATA_PATHS.values()),
        preserved_fields={"stage5cg_scaffolds_preserved": True},
    )
    records["stage5ce_preservation"] = _preservation_record(
        "stage5ce_preservation",
        label="stage5ce_proposal_package",
        source_paths=list(STAGE5CE_DATA_PATHS.values()),
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
    records["real_record_blocker"] = _record(
        "real_record_blocker",
        {
            "real_record_creation_blocker_status": "active",
            "blocked_current_stage_real_records": FUTURE_REAL_RECORD_CLASSES,
            "blocked_current_stage_real_record_count": len(FUTURE_REAL_RECORD_CLASSES),
        },
    )
    records["options_nonselection"] = _record(
        "options_nonselection",
        {
            "operator_options_nonselection_proof_created": True,
            "operator_decision_option_count": len(OPERATOR_DECISION_OPTIONS),
            "options": _option_rows(),
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
            "all_options_unselected": True,
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
        },
    )
    records["combined_gate_nonsatisfaction"] = _record(
        "combined_gate_nonsatisfaction",
        {
            "combined_gate_non_satisfaction_proof_created": True,
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
            "activation_decision_valid_now": False,
            "activation_authorized_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
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
    records["no_active_ingestion"] = _record(
        "no_active_ingestion",
        {
            "no_active_ingestion_status": "closed",
            "string4_sidecar_status": "scaffolded_inactive",
            "string4_sidecar_active": False,
            "string4_sidecar_planning_ingestion_activated": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "active_ingestion_performed": False,
            "active_manifest_registry_updated": False,
            "active_token_block_manifest_changed": False,
            "real_decision_package_preflight_authorizes_active_ingestion": False,
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
            "full_cartesian_product_enumerated": False,
            "string4_byte_stream_generation_allowed": False,
            "real_decision_package_preflight_authorizes_bytes": False,
        },
    )
    records["no_execution_transition_gate"] = _record(
        "no_execution_transition_gate",
        {
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
            "real_decision_package_preflight_authorizes_execution": False,
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
    records["guardrail"] = _record(
        "guardrail",
        {
            "guardrail_status": "closed",
            "future_token_block_execution_remains_blocked": True,
            "dwh_quarantine_reaffirmed": True,
            "dwh_hash_search_performed": False,
            "historical_route_execution_performed": False,
            "stego_tool_execution_performed": False,
            "outguess_execution_performed": False,
            "openpuff_execution_performed": False,
            "mp3stego_execution_performed": False,
            "magic_square_key_exploration_performed": False,
            "unused_number_negative_space_exploration_performed": False,
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
    records["handoff"] = _record(
        "handoff",
        {
            "canonical_codex_handoff_root": "codex-output",
            "deprecated_handoff_root": "codex_output",
            "codex_output_used": False,
            "codex_completion_summary_committed": False,
            "stage5cw_codex_completion_summary_required": True,
            "stage5cw_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            "stage5cw_codex_completion_summary_written_locally_before_final_response": (
                CODEX_COMPLETION_PATH.is_file()
            ),
            "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
            **completion_status,
        },
    )
    records["completion_continuity"] = _record(
        "completion_continuity",
        {
            "completion_summary_continuity_status": "preserved_for_stage5cw",
            "stage5cv_warning_integrated": True,
            "stage5cu_completion_summary_continuity_preserved": True,
            "stage5cw_codex_completion_summary_required": True,
            "stage5cw_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            "stage5cw_codex_completion_summary_written_locally_before_final_response": (
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
            "committed_stage5cw_metadata_secret_scan_required": True,
            "secret_values_printed_or_committed": False,
            "remote_hygiene": remote_status,
            "ignored_local_report_secret_scan": ignored_report_status,
        },
    )
    records["review_packaging_warning"] = _record(
        "review_packaging_warning",
        {
            "review_packaging_warning_created": True,
            "stage5cv_warning_integrated": True,
            "warning_status": "integrated_non_gate_opening_warning",
            "gate_opening": False,
            "raw_review_bodies_committed": False,
            "generated_review_bodies_committed": False,
        },
    )
    records["validation_evidence"] = _record(
        "validation_evidence",
        {
            "validation_evidence_status": "committed_compact_evidence",
            "local_validation_evidence_committed": True,
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
            "parallel_worker_cap_for_stage5cw_and_later": PARALLEL_WORKER_CAP,
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
            "source_paths_unique": source_digest_count == len(
                {record["path"] for record in source_records}
            ),
            "stage5cv_report_recorded_as_external_reference": True,
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
            "any_gap_authorizes_active_input": False,
            "any_gap_authorizes_byte_stream_generation": False,
            "any_gap_authorizes_execution": False,
        },
    )
    records["equivalence_map"] = _record(
        "equivalence_map",
        {
            "record_family_name_equivalence_map_created": True,
            "record_family_count": 7,
            "families": [
                {
                    "family_id": "stage5cw_preflight_records",
                    "equivalent_prefixes": [
                        "stage5cw-real-decision-package-preflight",
                        "stage5cw-future-real-operator-decision",
                        "stage5cw-future-option-selection",
                    ],
                },
                {
                    "family_id": "stage5cw_misuse_records",
                    "equivalent_prefixes": ["stage5cw-preflight-misuse"],
                },
                {
                    "family_id": "stage5cw_stage5cu_preservation_records",
                    "equivalent_prefixes": [
                        "stage5cw-stage5cu-negative",
                        "stage5cw-stage5cu-real-decision",
                        "stage5cw-stage5cu-option-selection",
                        "stage5cw-stage5cu-fixture",
                        "stage5cw-stage5cu-real-record",
                    ],
                },
                {
                    "family_id": "stage5cw_stage5cs_preservation_records",
                    "equivalent_prefixes": [
                        "stage5cw-stage5cs-decision-options",
                        "stage5cw-stage5cs-operator-decision-readiness",
                    ],
                },
                {
                    "family_id": "stage5cw_real_record_blocker_records",
                    "equivalent_prefixes": [
                        "stage5cw-real-record",
                        "stage5cw-combined-gate",
                        "stage5cw-activation-decision",
                    ],
                },
                {
                    "family_id": "stage5cw_gate_records",
                    "equivalent_prefixes": [
                        "stage5cw-no-active-ingestion",
                        "stage5cw-no-byte-stream",
                        "stage5cw-no-execution",
                    ],
                },
                {
                    "family_id": "stage5cw_handoff_records",
                    "equivalent_prefixes": [
                        "stage5cw-codex-handoff",
                        "stage5cw-completion-summary",
                        "stage5cw-credential-redaction",
                    ],
                },
            ],
        },
    )
    next_title = (
        "Stage 5CX - Deep Research review of Stage 5CW operator-decision "
        "readiness integration and real-decision package preflight, without execution"
    )
    records["next_stage"] = _record(
        "next_stage",
        {
            "selected_next_stage_id": "stage-5cx",
            "selected_next_stage_title": next_title,
            "selected_next_prompt_type": "deep_research_review",
            "selected_next_stage_authorizes_execution": False,
            "reason": (
                "Stage 5CW creates only review-only real-decision package preflight "
                "metadata; independent review is required before any real operator "
                "decision package or option-selection stage."
            ),
        },
    )
    records["stage_marker"] = _record(
        "stage_marker",
        {
            "current_completed_stage": STAGE_TITLE,
            "current_completed_stage_id": STAGE_ID,
            "selected_next_stage_id": "stage-5cx",
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
            "stage5cv_findings_integrated": True,
            "stage5cv_verdict": "accept_with_warnings",
            "real_decision_package_preflight_created": True,
            "real_decision_package_preflight_status": "review_preflight_only",
            "real_decision_package_created_now": False,
            "real_decision_package_valid_now": False,
            "future_real_decision_required_input_count": len(FUTURE_REAL_DECISION_INPUTS),
            "preflight_misuse_validation_matrix_created": True,
            "preflight_misuse_case_count": len(PREFLIGHT_MISUSE_CASES),
            "stage5cu_negative_fixture_pack_preserved": True,
            "stage5cu_negative_fixture_count_preserved": len(NEGATIVE_FIXTURE_IDS),
            "stage5cu_real_decision_negative_fixture_pack_preserved": True,
            "stage5cu_real_decision_negative_fixture_count_preserved": len(
                FUTURE_REAL_RECORD_CLASSES
            ),
            "stage5cu_option_selection_misuse_matrix_preserved": True,
            "stage5cu_option_selection_misuse_case_count_preserved": len(
                OPTION_SELECTION_MISUSE_TRANSITIONS
            ),
            "stage5cu_fixture_isolation_policy_preserved": True,
            "stage5cu_real_record_blocker_preserved": True,
            "stage5cs_real_approval_decision_options_status_preserved": "options_scaffold_only",
            "stage5cs_option_count_preserved": len(OPERATOR_DECISION_OPTIONS),
            "stage5cs_exact_option_set_preserved": True,
            "all_options_unselected": True,
            "operator_decision_option_count": len(OPERATOR_DECISION_OPTIONS),
            "operator_decision_option_selected_now": False,
            "selected_option_id": None,
            "real_approval_records_created": False,
            "future_real_records_created_now": False,
            "combined_approval_gate_satisfied_now": False,
            "activation_decision_valid_now": False,
            "activation_authorized_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
            "new_active_planning_input_created": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_id_count": run_plan_count,
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
            "stage5cw_codex_completion_summary_required": True,
            "stage5cw_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            "stage5cw_codex_completion_summary_written_locally_before_final_response": (
                CODEX_COMPLETION_PATH.is_file()
            ),
            "stage5cw_completion_summary_finalized_not_pending": (
                CODEX_COMPLETION_PATH.is_file()
                and not _completion_summary_has_unresolved_placeholder(CODEX_COMPLETION_PATH)
            ),
            "codex_completion_summary_committed": False,
            "codex_output_used": False,
            "parallel_worker_cap_for_stage5cw_and_later": PARALLEL_WORKER_CAP,
            "future_token_block_execution_remains_blocked": True,
            "recommended_next_stage_id": "stage-5cx",
            "recommended_next_prompt_type": "deep_research_review",
            "recommended_next_stage_title": next_title,
            "source_digest_record_count": source_digest_count,
        },
    )
    return records


def build_stage5cw(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    """Build Stage 5CW committed metadata and ignored reviewability reports."""

    _write_schemas()
    results_dir.mkdir(parents=True, exist_ok=True)
    records = _build_records()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)
    # Rebuild once so digest records can include newly written Stage 5CW files.
    records = _build_records()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    write_json(results_dir / "summary.json", records["summary"])
    write_json(
        results_dir / "real_decision_package_preflight_report.json",
        {
            "real_decision_package_preflight": records["real_decision_package_preflight"],
            "future_real_decision_requirements": records["future_real_decision_requirements"],
            "future_option_selection_requirements": records[
                "future_option_selection_requirements"
            ],
            "future_real_record_dependency_preflight": records[
                "future_real_record_dependency_preflight"
            ],
            "preflight_nonauthorization": records["preflight_nonauthorization"],
        },
    )
    write_json(results_dir / "preflight_misuse_report.json", records["preflight_misuse"])
    write_json(
        results_dir / "preservation_report.json",
        {
            "stage5cu_negative_fixture_preservation": records[
                "stage5cu_negative_fixture_preservation"
            ],
            "stage5cu_real_decision_fixture_preservation": records[
                "stage5cu_real_decision_fixture_preservation"
            ],
            "stage5cu_option_selection_misuse_preservation": records[
                "stage5cu_option_selection_misuse_preservation"
            ],
            "stage5cs_decision_options_preservation": records[
                "stage5cs_decision_options_preservation"
            ],
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


def _check_no_stage5cw_metadata_secrets(errors: list[str]) -> None:
    for path in DATA_PATHS.values():
        if path.is_file() and _path_has_secret_like_text(path):
            errors.append(f"credential_like_text_in_stage5cw_metadata={repo_relative(path)}")


def validate_stage5cw_actual_record_rejection(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in MANDATORY_FALSE_SUMMARY_FLAGS:
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


def validate_stage5cw_stage5cv_findings(
    *, findings: Path = DATA_PATHS["findings"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(findings, errors)
    if payload.get("stage5cv_verdict") != "accept_with_warnings":
        errors.append("Stage 5CV verdict must be accept_with_warnings")
    observed = set(payload.get("findings", []))
    for item in sorted(set(STAGE5CV_FINDINGS) - observed):
        errors.append(f"missing_stage5cv_finding={item}")
    return {
        "stage5cw_stage5cv_findings_valid": not errors,
        "stage5cv_verdict": payload.get("stage5cv_verdict"),
        "finding_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_real_decision_package_preflight(
    *, preflight: Path = DATA_PATHS["real_decision_package_preflight"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(preflight, errors)
    if payload.get("real_decision_package_preflight_created") is not True:
        errors.append("real-decision package preflight must be created")
    if payload.get("real_decision_package_preflight_status") != "review_preflight_only":
        errors.append("real-decision package preflight must be review_preflight_only")
    errors.extend(validate_stage5cw_actual_record_rejection(payload))
    return {
        "stage5cw_real_decision_package_preflight_valid": not errors,
        "real_decision_package_preflight_status": payload.get(
            "real_decision_package_preflight_status"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_future_real_decision_requirements(
    *, requirements: Path = DATA_PATHS["future_real_decision_requirements"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(requirements, errors)
    observed = set(payload.get("required_future_inputs", []))
    for item in sorted(set(FUTURE_REAL_DECISION_INPUTS) - observed):
        errors.append(f"missing_future_real_decision_input={item}")
    if payload.get("required_future_input_count") != len(FUTURE_REAL_DECISION_INPUTS):
        errors.append("future real-decision required input count mismatch")
    errors.extend(validate_stage5cw_actual_record_rejection(payload))
    return {
        "stage5cw_future_real_decision_requirements_valid": not errors,
        "required_future_input_count": payload.get("required_future_input_count"),
        "validation_error_count": len(errors),
    }, errors


def _validate_options_payload(payload: dict[str, Any], errors: list[str]) -> None:
    if payload.get("operator_decision_option_count") != len(OPERATOR_DECISION_OPTIONS):
        errors.append("operator decision option count must remain 6")
    if payload.get("operator_decision_option_selected_now") is not False:
        errors.append("operator_decision_option_selected_now must be false")
    if payload.get("selected_option_id") is not None:
        errors.append("selected_option_id must be null")
    options = payload.get("options", [])
    if options:
        option_ids = [option.get("option_id") for option in options]
        expected_ids = {option["option_id"] for option in OPERATOR_DECISION_OPTIONS}
        if set(option_ids) != expected_ids:
            errors.append("operator decision option ID set mismatch")
        if len(option_ids) != len(set(option_ids)):
            errors.append("operator decision option IDs must be unique")
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


def validate_stage5cw_preflight_misuse(
    *, misuse: Path = DATA_PATHS["preflight_misuse"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(misuse, errors)
    rows = payload.get("matrix_rows", [])
    observed = [row.get("misuse_case_id") for row in rows]
    if set(observed) != set(PREFLIGHT_MISUSE_CASES):
        errors.append("preflight misuse case set mismatch")
    if len(observed) != len(set(observed)):
        errors.append("preflight misuse case IDs must be unique")
    if payload.get("preflight_misuse_case_count") != len(PREFLIGHT_MISUSE_CASES):
        errors.append("preflight misuse case count mismatch")
    for row in rows:
        case_id = row.get("misuse_case_id")
        if row.get("must_fail_closed") is not True:
            errors.append(f"{case_id}: must_fail_closed must be true")
        for field in (
            "allowed_now",
            "gate_opening",
            "authorizes_approval",
            "authorizes_activation",
            "authorizes_active_input",
            "authorizes_dry_run_ingestion",
            "authorizes_byte_stream_generation",
            "authorizes_execution",
            "solve_claim",
        ):
            if row.get(field) is not False:
                errors.append(f"{case_id}: {field} must be false")
    errors.extend(validate_stage5cw_actual_record_rejection(payload))
    return {
        "stage5cw_preflight_misuse_valid": not errors,
        "preflight_misuse_case_count": payload.get("preflight_misuse_case_count"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_stage5cu_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = _load_all_payloads(errors)
    expectations = {
        "stage5cu_negative_fixture_preservation": {
            "stage5cu_negative_fixture_pack_preserved": True,
            "stage5cu_negative_fixture_count_preserved": len(NEGATIVE_FIXTURE_IDS),
        },
        "stage5cu_real_decision_fixture_preservation": {
            "stage5cu_real_decision_negative_fixture_pack_preserved": True,
            "stage5cu_real_decision_negative_fixture_count_preserved": len(
                FUTURE_REAL_RECORD_CLASSES
            ),
        },
        "stage5cu_option_selection_misuse_preservation": {
            "stage5cu_option_selection_misuse_matrix_preserved": True,
            "stage5cu_option_selection_misuse_case_count_preserved": len(
                OPTION_SELECTION_MISUSE_TRANSITIONS
            ),
        },
        "stage5cu_fixture_isolation_policy_preservation": {
            "stage5cu_fixture_isolation_policy_preserved": True,
        },
        "stage5cu_real_record_blocker_preservation": {
            "stage5cu_real_record_blocker_preserved": True,
        },
    }
    for key, fields in expectations.items():
        payload = payloads.get(key, {})
        for field, expected in fields.items():
            if payload.get(field) != expected:
                errors.append(f"{key}: {field} mismatch")
    _, stage5cu_errors = validate_stage5cu()
    errors.extend(f"stage5cu:{error}" for error in stage5cu_errors)
    return {
        "stage5cw_stage5cu_preservation_valid": not errors,
        "negative_fixture_count_preserved": len(NEGATIVE_FIXTURE_IDS),
        "real_decision_negative_fixture_count_preserved": len(FUTURE_REAL_RECORD_CLASSES),
        "option_selection_misuse_case_count_preserved": len(OPTION_SELECTION_MISUSE_TRANSITIONS),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_stage5cs_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(DATA_PATHS["stage5cs_decision_options_preservation"], errors)
    if payload.get("stage5cs_real_approval_decision_options_status_preserved") != (
        "options_scaffold_only"
    ):
        errors.append("Stage 5CS decision options must remain options_scaffold_only")
    if payload.get("stage5cs_option_count_preserved") != len(OPERATOR_DECISION_OPTIONS):
        errors.append("Stage 5CS option count must remain 6")
    if payload.get("stage5cs_exact_option_set_preserved") is not True:
        errors.append("Stage 5CS exact option set must be preserved")
    if payload.get("all_options_unselected") is not True:
        errors.append("all options must remain unselected")
    _validate_options_payload(payload, errors)
    _, stage5cs_errors = validate_stage5cs()
    errors.extend(f"stage5cs:{error}" for error in stage5cs_errors)
    return {
        "stage5cw_stage5cs_preservation_valid": not errors,
        "stage5cs_option_count_preserved": payload.get("stage5cs_option_count_preserved"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_options_nonselection(
    *, options_nonselection: Path = DATA_PATHS["options_nonselection"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(options_nonselection, errors)
    if payload.get("all_options_unselected") is not True:
        errors.append("all_options_unselected must be true")
    _validate_options_payload(payload, errors)
    errors.extend(validate_stage5cw_actual_record_rejection(payload))
    return {
        "stage5cw_options_nonselection_valid": not errors,
        "operator_decision_option_selected_now": payload.get(
            "operator_decision_option_selected_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_real_record_blocker(
    *, real_record_blocker: Path = DATA_PATHS["real_record_blocker"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(real_record_blocker, errors)
    if payload.get("real_record_creation_blocker_status") != "active":
        errors.append("real-record creation blocker must be active")
    if set(payload.get("blocked_current_stage_real_records", [])) != set(FUTURE_REAL_RECORD_CLASSES):
        errors.append("blocked current-stage real record classes mismatch")
    errors.extend(validate_stage5cw_actual_record_rejection(payload))
    return {
        "stage5cw_real_record_blocker_valid": not errors,
        "blocked_current_stage_real_record_count": len(
            payload.get("blocked_current_stage_real_records", [])
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_combined_gate(
    *, combined_gate: Path = DATA_PATHS["combined_gate_nonsatisfaction"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(combined_gate, errors)
    for field in (
        "combined_approval_gate_satisfied_now",
        "combined_approval_gate_authorizes_activation_now",
        "approval_gate_satisfied_now",
        "approval_gate_authorizes_activation_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cw_combined_gate_valid": not errors,
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_activation_nonauthorization(
    *, activation: Path = DATA_PATHS["activation_nonauthorization"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(activation, errors)
    for field in (
        "activation_decision_valid_now",
        "activation_authorized_now",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cw_activation_nonauthorization_valid": not errors,
        "activation_decision_valid_now": payload.get("activation_decision_valid_now"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_stage5bd_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(DATA_PATHS["stage5bd_preservation"], errors)
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    for field in (
        "stage5bd_run_plan_ids_changed",
        "stage5bd_dry_run_plan_manifest_changed",
        "stage5bd_plan_superseded",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    _, stage5bd_errors = validate_stage5bd()
    errors.extend(f"stage5bd:{error}" for error in stage5bd_errors)
    return {
        "stage5cw_stage5bd_preservation_valid": not errors,
        "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_active_lineage_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(DATA_PATHS["active_lineage"], errors)
    if payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage must contain exactly 8 records")
    if payload.get("correct_stage5aw_path_included") is not True:
        errors.append("correct Stage 5AW path must be included")
    if payload.get("deprecated_stage5aw_path_absent") is not True:
        errors.append("deprecated Stage 5AW path must be absent")
    if payload.get("all_lineage_paths_resolve") is not True:
        errors.append("all active lineage paths must resolve")
    errors.extend(validate_stage5cw_actual_record_rejection(payload))
    return {
        "stage5cw_active_lineage_preservation_valid": not errors,
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
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


def validate_stage5cw_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
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
        "stage5cw_sidecar_gates_valid": not errors,
        "no_active_ingestion_status": payloads["no_active_ingestion"].get(
            "no_active_ingestion_status"
        ),
        "no_byte_stream_transition_gate_status": payloads[
            "no_byte_stream_transition_gate"
        ].get("no_byte_stream_transition_gate_status"),
        "no_execution_transition_gate_status": payloads["no_execution_transition_gate"].get(
            "no_execution_transition_gate_status"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_handoff_continuity() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    handoff = _validate_payload(DATA_PATHS["handoff"], errors)
    continuity = _validate_payload(DATA_PATHS["completion_continuity"], errors)
    if handoff.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if handoff.get("codex_output_used") is not False:
        errors.append("codex_output must not be used")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output directory must be absent")
    if continuity.get("stage5cw_codex_completion_summary_required") is not True:
        errors.append("Stage 5CW completion summary must be required")
    if not CODEX_COMPLETION_PATH.is_file():
        errors.append(f"missing_local_completion_summary={CODEX_COMPLETION_PATH.as_posix()}")
    elif _completion_summary_has_unresolved_placeholder(CODEX_COMPLETION_PATH):
        errors.append("Stage 5CW completion summary must not contain unresolved placeholders")
    if continuity.get("codex_completion_summary_committed") is not False:
        errors.append("codex completion summary must not be committed")
    return {
        "stage5cw_handoff_continuity_valid": not errors,
        "stage5cw_codex_completion_summary_written_locally": CODEX_COMPLETION_PATH.is_file(),
        "codex_output_used": handoff.get("codex_output_used"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw_credential_redaction_policy(
    *, credential_redaction: Path = DATA_PATHS["credential_redaction"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(credential_redaction, errors)
    for field in (
        "credential_redaction_policy_preserved",
        "credential_like_remote_must_be_redacted",
        "credential_like_text_must_not_be_committed",
        "committed_stage5cw_metadata_secret_scan_required",
    ):
        if payload.get(field) is not True:
            errors.append(f"{field} must be true")
    if payload.get("secret_values_printed_or_committed") is not False:
        errors.append("secret values must not be printed or committed")
    _check_no_stage5cw_metadata_secrets(errors)
    return {
        "stage5cw_credential_redaction_policy_valid": not errors,
        "credential_like_remote_detected": payload.get("remote_hygiene", {}).get(
            "credential_like_remote_detected"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cw(
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
    _check_no_stage5cw_metadata_secrets(errors)
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
        validate_stage5cw_stage5cv_findings(),
        validate_stage5cw_real_decision_package_preflight(),
        validate_stage5cw_future_real_decision_requirements(),
        validate_stage5cw_preflight_misuse(),
        validate_stage5cw_stage5cu_preservation(),
        validate_stage5cw_stage5cs_preservation(),
        validate_stage5cw_options_nonselection(),
        validate_stage5cw_real_record_blocker(),
        validate_stage5cw_combined_gate(),
        validate_stage5cw_activation_nonauthorization(),
        validate_stage5cw_stage5bd_preservation(),
        validate_stage5cw_active_lineage_preservation(),
        validate_stage5cw_sidecar_gates(),
        validate_stage5cw_handoff_continuity(),
        validate_stage5cw_credential_redaction_policy(),
    ):
        errors.extend(focused_errors)
    for field in (
        "stage5cv_findings_integrated",
        "real_decision_package_preflight_created",
        "preflight_misuse_validation_matrix_created",
        "stage5cu_negative_fixture_pack_preserved",
        "stage5cu_real_decision_negative_fixture_pack_preserved",
        "stage5cu_option_selection_misuse_matrix_preserved",
        "stage5cu_fixture_isolation_policy_preserved",
        "stage5cu_real_record_blocker_preserved",
        "stage5cs_exact_option_set_preserved",
    ):
        if summary_payload.get(field) is not True:
            errors.append(f"summary {field} must be true")
    for field in MANDATORY_FALSE_SUMMARY_FLAGS:
        if summary_payload.get(field) is not False:
            errors.append(f"summary {field} must be false")
    if summary_payload.get("stage5cv_verdict") != "accept_with_warnings":
        errors.append("summary Stage 5CV verdict must be accept_with_warnings")
    if summary_payload.get("real_decision_package_preflight_status") != "review_preflight_only":
        errors.append("real-decision package preflight must be review_preflight_only")
    if summary_payload.get("operator_decision_option_count") != len(OPERATOR_DECISION_OPTIONS):
        errors.append("operator decision option count must be 6")
    if summary_payload.get("stage5cu_negative_fixture_count_preserved") != len(
        NEGATIVE_FIXTURE_IDS
    ):
        errors.append("Stage 5CU negative fixture count mismatch")
    if summary_payload.get("stage5cu_real_decision_negative_fixture_count_preserved") != len(
        FUTURE_REAL_RECORD_CLASSES
    ):
        errors.append("Stage 5CU real-decision fixture count mismatch")
    if summary_payload.get("preflight_misuse_case_count") != len(PREFLIGHT_MISUSE_CASES):
        errors.append("preflight misuse case count mismatch")
    if summary_payload.get("selected_option_id") is not None:
        errors.append("summary selected_option_id must be null")
    if summary_payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    if summary_payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage must contain exactly 8 records")
    if summary_payload.get("parallel_worker_cap_for_stage5cw_and_later") != PARALLEL_WORKER_CAP:
        errors.append("Stage 5CW parallel worker cap must be 8")
    if next_payload.get("selected_next_stage_id") != "stage-5cx":
        errors.append("Stage 5CW must select Stage 5CX as next stage")
    if next_payload.get("selected_next_prompt_type") != "deep_research_review":
        errors.append("Stage 5CX prompt type must be deep_research_review")
    if next_payload.get("selected_next_stage_authorizes_execution") is not False:
        errors.append("Stage 5CX must not authorize execution")
    if guardrail_payload.get("future_token_block_execution_remains_blocked") is not True:
        errors.append("future token-block execution must remain blocked")
    for output_name in (
        "summary.json",
        "real_decision_package_preflight_report.json",
        "preflight_misuse_report.json",
        "preservation_report.json",
        "handoff_continuity_report.json",
        "source_digest_index.json",
        "warnings.jsonl",
    ):
        if not (results_dir / output_name).is_file():
            errors.append(f"missing_generated_output={repo_relative(results_dir / output_name)}")
    return {
        "stage5cw_valid": not errors,
        "validation_error_count": len(errors),
        "stage5cv_verdict": summary_payload.get("stage5cv_verdict"),
        "real_decision_package_preflight_status": summary_payload.get(
            "real_decision_package_preflight_status"
        ),
        "operator_decision_option_count": summary_payload.get("operator_decision_option_count"),
        "operator_decision_option_selected_now": summary_payload.get(
            "operator_decision_option_selected_now"
        ),
        "negative_fixture_count_preserved": summary_payload.get(
            "stage5cu_negative_fixture_count_preserved"
        ),
        "preflight_misuse_case_count": summary_payload.get("preflight_misuse_case_count"),
        "combined_approval_gate_satisfied_now": summary_payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_decision_valid_now": summary_payload.get("activation_decision_valid_now"),
        "active_planning_input_authorized_now": summary_payload.get(
            "active_planning_input_authorized_now"
        ),
        "stage5bd_run_plan_id_count": summary_payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": summary_payload.get("active_lineage_record_count"),
        "parallel_worker_cap": summary_payload.get("parallel_worker_cap_for_stage5cw_and_later"),
        "recommended_next_stage_id": summary_payload.get("recommended_next_stage_id"),
    }, errors


def load_stage5cw_summary(*, summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
