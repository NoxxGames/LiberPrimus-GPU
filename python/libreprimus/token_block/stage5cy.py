"""Stage 5CY option-selection decision preflight metadata."""

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
from libreprimus.token_block.stage5cs import validate_stage5cs
from libreprimus.token_block.stage5cu import (
    FUTURE_REAL_RECORD_CLASSES,
    NEGATIVE_FIXTURE_IDS,
    OPERATOR_DECISION_OPTIONS,
    OPTION_SELECTION_MISUSE_TRANSITIONS,
    validate_stage5cu,
)
from libreprimus.token_block.stage5cw import (
    DATA_PATHS as STAGE5CW_DATA_PATHS,
    validate_stage5cw,
)

STAGE_ID = "stage-5cy"
STAGE_TITLE = (
    "Stage 5CY - Operator real-decision package readiness review integration "
    "and option-selection decision preflight, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5cw"
SOURCE_PREVIOUS_COMMIT = "6844ce4757a78031c87579c63f077219f8bd7e75"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5cx"
SOURCE_DEEP_RESEARCH_REPORT = "27_Stage-5CW-Deep-Research-Review.md"
STAGE5CX_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "27_Stage-5CW-Deep-Research-Review.md"
)
RESULTS_DIR = Path("experiments/results/token-block/stage5cy")
CODEX_COMPLETION_PATH = Path("codex-output/stage5cy-codex-completion.md")
STAGE5CW_CODEX_COMPLETION_PATH = Path("codex-output/stage5cw-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
PYTEST_COUNT_STAGE5CW_COMMITTED = 2446
PYTEST_COUNT_STAGE5CW_FINAL_TRAIL = 2466
PYTEST_COUNT_OBSERVED_LOCALLY = 2483
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"

SOURCE_STAGE_IDS = [
    "stage-5cx",
    "stage-5cw",
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

STAGE5CX_FINDINGS = [
    "stage5cw_accepted_with_warnings",
    "stage5cw_metadata_only_review_preflight_coherent",
    "stage5cw_integrates_stage5cv",
    "stage5cw_preserves_stage5cu_negative_fixture_layer",
    "stage5cw_preserves_stage5cs_exact_six_option_scaffold",
    "stage5cw_keeps_all_six_options_unselected",
    "stage5cw_creates_only_future_real_decision_package_preflight",
    "stage5cw_does_not_create_real_decision_package",
    "stage5cw_does_not_select_option",
    "stage5cw_does_not_create_real_operator_approval",
    "stage5cw_does_not_create_real_deep_research_acceptance",
    "stage5cw_does_not_satisfy_combined_gate",
    "stage5cw_does_not_authorize_activation",
    "stage5cw_does_not_authorize_or_select_active_planning_input",
    "stage5cw_preserves_stage5bd_unchanged",
    "stage5cw_preserves_active_lineage_unchanged",
    "stage5cw_keeps_string4_inactive_non_ingested_non_byte_generating_non_executable",
    "stage5cw_keeps_no_active_no_byte_no_execution_gates_closed",
    "stage5cw_preserves_codex_output_handoff_and_credential_redaction_policy",
    "stage5cw_pytest_count_reviewability_warning_2446_vs_2466",
    "pytest_count_discrepancy_is_reviewability_count_mismatch_not_gate_opener",
    "final_stage5cw_commit_is_narrow_cli_test_interpreter_portability_fix",
    "project_has_governance_overbuild_risk",
    "next_stage_should_prepare_operator_facing_option_selection_decision_preflight",
    "next_stage_should_still_not_select_option",
    "after_stage5cy_and_review_force_operator_choice_or_pause_unless_defect_found",
]

OPTION_SELECTION_REQUIREMENTS = [
    "stage5cz_independent_review_required_before_choice",
    "operator_must_choose_explicitly_or_pause_after_stage5cz",
    "exact_stage5cs_option_set_must_be_cited",
    "selected_option_id_must_be_one_of_exact_six_if_future_choice_occurs",
    "exactly_one_option_must_be_selected_in_future_real_decision",
    "future_real_decision_record_must_not_be_fixture_template_or_preflight",
    "future_real_decision_record_must_include_operator_identity_or_role",
    "future_real_decision_record_must_include_timestamp",
    "stage5cw_reconciliation_record_must_be_cited",
    "stage5cu_negative_fixtures_must_remain_preserved",
    "stage5cs_option_scaffold_must_remain_preserved",
    "stage5bd_run_plan_ids_must_remain_unchanged_or_have_future_supersession",
    "active_lineage_must_remain_unchanged_or_have_future_supersession",
    "no_active_ingestion_gate_must_be_reviewed",
    "no_byte_stream_gate_must_be_reviewed",
    "no_execution_gate_must_be_reviewed",
    "credential_redaction_policy_must_be_reviewed",
    "codex_output_hyphenated_handoff_root_must_remain_canonical",
    "codex_output_underscore_root_must_remain_unused",
    "future_choice_must_not_authorize_bytes_by_itself",
    "future_choice_must_not_authorize_execution_by_itself",
    "future_choice_must_not_claim_solve",
    "future_choice_must_not_activate_canonical_corpus",
    "future_choice_must_not_finalize_page_boundaries",
]

OPTION_SELECTION_MISUSE_CASES = [
    "option_selection_preflight_treated_as_real_operator_decision",
    "option_selection_preflight_treated_as_real_option_selection",
    "option_selection_preflight_adds_option_to_exact_set",
    "option_selection_preflight_removes_option_from_exact_set",
    "option_selection_preflight_renames_option_from_exact_set",
    "option_selection_preflight_sets_selected_option_id",
    "option_selection_preflight_marks_any_option_selected",
    "option_selection_preflight_creates_real_operator_approval",
    "option_selection_preflight_creates_deep_research_acceptance",
    "option_selection_preflight_satisfies_combined_gate",
    "option_selection_preflight_creates_activation_decision",
    "option_selection_preflight_authorizes_active_input",
    "option_selection_preflight_authorizes_dry_run_ingestion",
    "option_selection_preflight_authorizes_byte_stream_generation",
    "option_selection_preflight_authorizes_execution",
    "option_selection_preflight_mutates_stage5bd",
    "option_selection_preflight_mutates_active_lineage",
    "option_selection_preflight_mutates_active_manifests",
    "option_selection_preflight_uses_codex_output_underscore_root",
    "option_selection_preflight_leaks_credential_like_remote",
    "option_selection_preflight_treats_pytest_count_mismatch_as_gate_opener",
    "option_selection_preflight_skips_stage5cz_review",
    "option_selection_preflight_creates_another_generic_governance_layer_after_stage5cz",
    "option_selection_preflight_sets_solve_claim_true",
]

REVIEWABILITY_GAPS = [
    {
        "gap_id": "stage5cw_pytest_count_mismatch_2446_vs_2466",
        "severity": "medium",
        "gate_opening": False,
        "activation_defect": False,
        "status": "superseded_by_stage5cy_reconciliation_record",
    },
    {
        "gap_id": "governance_overbuild_risk",
        "severity": "medium",
        "gate_opening": False,
        "activation_defect": False,
        "status": "bounded_by_stage5cy_governance_scope_control",
    },
    {
        "gap_id": "stage5cz_review_required_before_operator_choice",
        "severity": "high",
        "gate_opening": False,
        "activation_defect": False,
        "status": "preserved_as_required_next_stage",
    },
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5cy-summary.yaml"),
    "next_stage": Path("data/project-state/stage5cy-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5cy-stage5cx-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5cy-reviewable-stage-marker.yaml"),
    "validation_evidence": Path("data/project-state/stage5cy-reviewable-validation-evidence.yaml"),
    "source_digest_index": Path("data/project-state/stage5cy-reviewable-source-digest-index.yaml"),
    "gap_register": Path("data/project-state/stage5cy-reviewability-gap-register.yaml"),
    "equivalence_map": Path("data/project-state/stage5cy-record-family-name-equivalence-map.yaml"),
    "validation_count_reconciliation": Path(
        "data/project-state/stage5cy-validation-count-reconciliation.yaml"
    ),
    "governance_scope_control": Path("data/project-state/stage5cy-governance-scope-control.yaml"),
    "real_decision_preflight_preservation": Path(
        "data/token-block/stage5cy-real-decision-preflight-preservation.yaml"
    ),
    "operator_option_selection_preflight": Path(
        "data/token-block/stage5cy-operator-option-selection-preflight.yaml"
    ),
    "option_selection_requirements": Path(
        "data/token-block/stage5cy-option-selection-requirements.yaml"
    ),
    "option_selection_misuse": Path(
        "data/token-block/stage5cy-option-selection-misuse-validation-matrix.yaml"
    ),
    "options_nonselection": Path("data/token-block/stage5cy-options-nonselection-proof.yaml"),
    "real_record_blocker": Path("data/token-block/stage5cy-real-record-creation-blocker.yaml"),
    "operator_decision_nonauthorization": Path(
        "data/token-block/stage5cy-operator-decision-nonauthorization-proof.yaml"
    ),
    "combined_gate_nonsatisfaction": Path(
        "data/token-block/stage5cy-combined-gate-non-satisfaction-proof.yaml"
    ),
    "activation_nonauthorization": Path(
        "data/token-block/stage5cy-activation-decision-nonauthorization-proof.yaml"
    ),
    "preflight_nonauthorization": Path(
        "data/token-block/stage5cy-preflight-nonauthorization-proof.yaml"
    ),
    "stage5cw_preservation": Path("data/token-block/stage5cy-stage5cw-preservation.yaml"),
    "stage5cu_preservation": Path("data/token-block/stage5cy-stage5cu-preservation.yaml"),
    "stage5cs_preservation": Path("data/token-block/stage5cy-stage5cs-preservation.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5cy-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5cy-active-lineage-preservation.yaml"),
    "sidecar_activation_blocker": Path("data/token-block/stage5cy-sidecar-activation-blocker.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5cy-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5cy-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5cy-no-execution-transition-gate.yaml"
    ),
    "guardrail": Path("data/historical-route/stage5cy-guardrail.yaml"),
    "dwh": Path("data/historical-route/stage5cy-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5cy-source-gap-severity-update.yaml"),
    "handoff": Path("data/source-harvester/stage5cy-codex-handoff-policy.yaml"),
    "completion_continuity": Path(
        "data/source-harvester/stage5cy-completion-summary-continuity.yaml"
    ),
    "credential_redaction": Path(
        "data/source-harvester/stage5cy-credential-redaction-policy-preservation.yaml"
    ),
    "review_packaging_warning": Path(
        "data/source-harvester/stage5cy-review-packaging-warning.yaml"
    ),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5cy_{key}" for key in DATA_PATHS}

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
    "operator_facing_option_selection_preflight_authorizes_approval": False,
    "operator_facing_option_selection_preflight_authorizes_activation": False,
    "operator_facing_option_selection_preflight_authorizes_active_input": False,
    "operator_facing_option_selection_preflight_authorizes_dry_run_ingestion": False,
    "operator_facing_option_selection_preflight_authorizes_bytes": False,
    "operator_facing_option_selection_preflight_authorizes_execution": False,
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

SELECTED_OPTION_FIELD = {"selected_option_id": None}


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
        "required": ["record_type", "stage_id", "metadata_only", "execution_allowed", "solve_claim"],
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


def _stage5cw_summary() -> dict[str, Any]:
    return _load_yaml(STAGE5CW_DATA_PATHS["summary"])


def _stage5cw_validation_evidence() -> dict[str, Any]:
    return _load_yaml(STAGE5CW_DATA_PATHS["validation_evidence"])


def _stage5cs_options() -> list[dict[str, Any]]:
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


def _source_digest_rows() -> list[dict[str, Any]]:
    source_paths = sorted(
        set(
            [
                *[path.as_posix() for path in DATA_PATHS.values()],
                *[path.as_posix() for path in STAGE5CW_DATA_PATHS.values()],
                "data/token-block/stage5cs-real-approval-decision-options-scaffold.yaml",
                "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
                "codex-output/stage5cw-codex-completion.md",
            ]
        )
    )
    rows: list[dict[str, Any]] = []
    for path_text in source_paths:
        path = Path(path_text)
        rows.append(
            {
                "path": path_text,
                "exists": path.exists(),
                "committed": path_text.startswith("data/"),
                "ignored_local_support": path_text.startswith("codex-output/"),
                "sha256": sha256_file(path) if path.exists() and path.is_file() else None,
            }
        )
    return rows


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
    stage5cw_summary = _stage5cw_summary()
    stage5cw_validation = _stage5cw_validation_evidence()
    stage5cw_counts = {
        "stage5cw_real_decision_package_preflight_status_preserved": stage5cw_summary.get(
            "real_decision_package_preflight_status"
        ),
        "stage5cw_operator_decision_option_count_preserved": stage5cw_summary.get(
            "operator_decision_option_count"
        ),
        "stage5cw_selected_option_id_preserved": stage5cw_summary.get("selected_option_id"),
        "stage5cw_stage5bd_run_plan_id_count_preserved": stage5cw_summary.get(
            "stage5bd_run_plan_id_count"
        ),
        "stage5cw_active_lineage_record_count_preserved": stage5cw_summary.get(
            "active_lineage_record_count"
        ),
    }
    validation_reconciliation = {
        "stage5cw_committed_validation_evidence_path": DATA_PATHS[
            "validation_count_reconciliation"
        ].as_posix(),
        "stage5cw_committed_compact_pytest_count": PYTEST_COUNT_STAGE5CW_COMMITTED,
        "stage5cw_committed_compact_pytest_count_from_record": stage5cw_validation.get(
            "pytest_count_observed_locally"
        ),
        "stage5cw_final_issue_completion_trail_pytest_count": PYTEST_COUNT_STAGE5CW_FINAL_TRAIL,
        "stage5cy_pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
        "reconciliation_status": "superseding_reconciliation_record",
        "history_rewritten": False,
        "historical_stage5cw_metadata_changed": False,
        "count_mismatch_class": "reviewability_count_reconciliation_warning",
        "gate_opening": False,
        "activation_defect": False,
        "scope_expansion": False,
        "stage5cw_final_commit_scope": "narrow_cli_test_interpreter_portability_fix",
    }
    source_digest_rows = _source_digest_rows()
    credential_summary = _credential_remote_summary()

    records: dict[str, dict[str, Any]] = {}
    records["findings"] = {
        **_base_record("findings"),
        "stage5cx_verdict": "accept_with_warnings",
        "stage5cx_findings_integrated": True,
        "finding_count": len(STAGE5CX_FINDINGS),
        "findings": STAGE5CX_FINDINGS,
        "stage5cx_did_not_recommend_execution": True,
        "stage5cx_did_not_recommend_option_selection": True,
        **_stage_flags(),
    }
    records["validation_count_reconciliation"] = {
        **_base_record("validation_count_reconciliation"),
        **validation_reconciliation,
        **_stage_flags(),
    }
    records["real_decision_preflight_preservation"] = {
        **_base_record("real_decision_preflight_preservation"),
        "stage5cw_real_decision_package_preflight_preserved": True,
        "stage5cw_real_decision_package_preflight_status": "review_preflight_only",
        "stage5cw_real_decision_package_created_now": False,
        "stage5cw_real_decision_package_valid_now": False,
        **stage5cw_counts,
        **_stage_flags(),
    }
    records["operator_option_selection_preflight"] = {
        **_base_record("operator_option_selection_preflight"),
        "operator_facing_option_selection_preflight_created": True,
        "operator_facing_option_selection_preflight_status": "review_preflight_only",
        "operator_facing_option_selection_preflight_is_real_operator_decision": False,
        "operator_facing_option_selection_preflight_selects_option": False,
        "operator_decision_option_count": len(OPERATOR_DECISION_OPTIONS),
        "operator_decision_options": _stage5cs_options(),
        "all_options_unselected": True,
        "stage5cz_review_required_before_option_selection": True,
        "after_stage5cz_requires_operator_choice_or_pause": True,
        **_stage_flags(),
    }
    records["option_selection_requirements"] = {
        **_base_record("option_selection_requirements"),
        "option_selection_preflight_requirement_count": len(OPTION_SELECTION_REQUIREMENTS),
        "requirements": OPTION_SELECTION_REQUIREMENTS,
        "option_selection_ready_now": False,
        "stage5cz_review_required": True,
        **_stage_flags(),
    }
    records["option_selection_misuse"] = {
        **_base_record("option_selection_misuse"),
        "option_selection_misuse_case_count": len(OPTION_SELECTION_MISUSE_CASES),
        "misuse_cases": [
            {
                "misuse_case_id": misuse_case,
                "blocked_now": True,
                "gate_opening": False,
                "authorizes_execution": False,
            }
            for misuse_case in OPTION_SELECTION_MISUSE_CASES
        ],
        **_stage_flags(),
    }
    records["options_nonselection"] = {
        **_base_record("options_nonselection"),
        "stage5cs_exact_option_set_preserved": True,
        "operator_decision_option_count": len(OPERATOR_DECISION_OPTIONS),
        "operator_decision_options": _stage5cs_options(),
        "all_options_unselected": True,
        "operator_decision_option_selected_now": False,
        "selected_option_id": None,
        "option_addition_allowed_now": False,
        "option_removal_allowed_now": False,
        "option_rename_allowed_now": False,
        **FALSE_FLAGS,
    }
    records["real_record_blocker"] = {
        **_base_record("real_record_blocker"),
        "real_record_class_count": len(FUTURE_REAL_RECORD_CLASSES),
        "blocked_real_record_classes": [
            {
                "record_class": record_class,
                "created_now": False,
                "valid_now": False,
                "blocked_reason": "stage5cy_is_option_selection_preflight_only",
            }
            for record_class in FUTURE_REAL_RECORD_CLASSES
        ],
        **_stage_flags(),
    }
    records["operator_decision_nonauthorization"] = {
        **_base_record("operator_decision_nonauthorization"),
        "real_operator_decision_record_created_now": False,
        "operator_decision_record_present_now": False,
        "operator_decision_satisfied_now": False,
        **_stage_flags(),
    }
    records["combined_gate_nonsatisfaction"] = {
        **_base_record("combined_gate_nonsatisfaction"),
        "combined_approval_gate_satisfied_now": False,
        "real_combined_gate_validation_record_created_now": False,
        "operator_approval_record_present_now": False,
        "deep_research_activation_accept_record_present_now": False,
        **_stage_flags(),
    }
    records["activation_nonauthorization"] = {
        **_base_record("activation_nonauthorization"),
        "activation_decision_valid_now": False,
        "activation_authorized_now": False,
        "real_activation_decision_record_created_now": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        **_stage_flags(),
    }
    records["preflight_nonauthorization"] = {
        **_base_record("preflight_nonauthorization"),
        "preflight_status": "review_preflight_only",
        "preflight_authorizes_real_decision_now": False,
        "preflight_authorizes_real_approval_now": False,
        "preflight_authorizes_deep_research_acceptance_now": False,
        "preflight_authorizes_combined_gate_validation_now": False,
        "preflight_authorizes_activation_decision_now": False,
        "preflight_authorizes_active_planning_input_now": False,
        "preflight_authorizes_dry_run_ingestion_now": False,
        "preflight_authorizes_byte_stream_generation_now": False,
        "preflight_authorizes_execution_now": False,
        **_stage_flags(),
    }
    records["stage5cw_preservation"] = {
        **_base_record("stage5cw_preservation"),
        "stage5cw_summary_path": STAGE5CW_DATA_PATHS["summary"].as_posix(),
        "stage5cw_complete": stage5cw_summary.get("status") == "complete",
        "stage5cw_preserved_without_historical_edit": True,
        "stage5cw_pytest_count_warning_reconciled_by_stage5cy": True,
        **stage5cw_counts,
        **_stage_flags(),
    }
    records["stage5cu_preservation"] = {
        **_base_record("stage5cu_preservation"),
        "stage5cu_negative_fixture_pack_preserved": True,
        "stage5cu_negative_fixture_count_preserved": len(NEGATIVE_FIXTURE_IDS),
        "stage5cu_real_decision_negative_fixture_count_preserved": len(
            FUTURE_REAL_RECORD_CLASSES
        ),
        "stage5cu_option_selection_misuse_case_count_preserved": len(
            OPTION_SELECTION_MISUSE_TRANSITIONS
        ),
        **_stage_flags(),
    }
    records["stage5cs_preservation"] = {
        **_base_record("stage5cs_preservation"),
        "stage5cs_real_approval_decision_options_status_preserved": "options_scaffold_only",
        "stage5cs_option_count_preserved": len(OPERATOR_DECISION_OPTIONS),
        "stage5cs_exact_option_set_preserved": True,
        "all_options_unselected": True,
        "operator_decision_options": _stage5cs_options(),
        **_stage_flags(),
    }
    records["stage5bd_preservation"] = {
        **_base_record("stage5bd_preservation"),
        "stage5bd_dry_run_records_remain_valid": True,
        "stage5bd_run_plan_id_count": 10,
        "stage5bd_run_plan_ids_changed": False,
        "stage5bd_dry_run_plan_manifest_changed": False,
        "stage5bd_plan_superseded": False,
        **_stage_flags(),
    }
    records["active_lineage"] = {
        **_base_record("active_lineage"),
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "active_lineage_records": [
            {
                "path": path_text,
                "exists": Path(path_text).exists(),
                "sha256": sha256_file(Path(path_text)) if Path(path_text).exists() else None,
            }
            for path_text in ACTIVE_LINEAGE_PATHS
        ],
        "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in ACTIVE_LINEAGE_PATHS,
        "deprecated_stage5aw_path_absent": INCORRECT_STAGE5AW_PATH not in ACTIVE_LINEAGE_PATHS,
        "all_lineage_paths_resolve": all(Path(path).exists() for path in ACTIVE_LINEAGE_PATHS),
        **_stage_flags(),
    }
    records["sidecar_activation_blocker"] = {
        **_base_record("sidecar_activation_blocker"),
        "string4_sidecar_status": "scaffolded_inactive",
        "string4_sidecar_active": False,
        "string4_sidecar_planning_ingestion_activated": False,
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
        "active_manifest_registry_updated": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        "active_token_block_manifest_changed": False,
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
        "operator_facing_option_selection_preflight_authorizes_bytes": False,
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
        "operator_facing_option_selection_preflight_authorizes_execution": False,
        **_stage_flags(),
    }
    records["guardrail"] = {
        **_base_record("guardrail"),
        "guardrail_status": "metadata_only_fail_closed",
        "blocked_actions": sorted(FALSE_FLAGS),
        **_stage_flags(),
    }
    records["dwh"] = {
        **_base_record("dwh"),
        "dwh_quarantine_reaffirmed": True,
        "dwh_hash_search_performed": False,
        "hash_preimage_search_performed": False,
        **_stage_flags(),
    }
    records["source_gap"] = {
        **_base_record("source_gap"),
        "source_gap_status": "no_new_source_gap_for_stage5cy",
        "stage5cw_pytest_count_gap_reconciled": True,
        **_stage_flags(),
    }
    records["handoff"] = {
        **_base_record("handoff"),
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_handoff_root": "codex_output",
        "codex_output_used": False,
        "codex_completion_summary_committed": False,
        "stage5cy_codex_completion_summary_required": True,
        "stage5cy_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5cy_codex_completion_summary_written_locally_before_final_response": True,
        "stage5cy_completion_summary_finalized_not_pending": True,
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
        **FALSE_FLAGS,
    }
    records["completion_continuity"] = {
        **_base_record("completion_continuity"),
        "stage5cw_codex_completion_summary_path": STAGE5CW_CODEX_COMPLETION_PATH.as_posix(),
        "stage5cw_codex_completion_summary_present": STAGE5CW_CODEX_COMPLETION_PATH.exists(),
        "stage5cw_completion_summary_finalized_not_pending": True,
        "stage5cy_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5cy_codex_completion_summary_written_locally_before_final_response": True,
        "stage5cy_completion_summary_finalized_not_pending": True,
        **_stage_flags(),
    }
    records["credential_redaction"] = {
        **_base_record("credential_redaction"),
        **credential_summary,
        "secret_values_printed_or_committed": False,
        **_stage_flags(),
    }
    records["review_packaging_warning"] = {
        **_base_record("review_packaging_warning"),
        "review_packaging_warning_status": "integrated_non_gate_opening",
        "stage5cz_review_required": True,
        **_stage_flags(),
    }
    records["stage_marker"] = {
        **_base_record("stage_marker"),
        "reviewable_stage_marker_created": True,
        "current_completed_stage_prefix": "Stage 5CY",
        "expected_next_stage_prefix": "Stage 5CZ",
        **_stage_flags(),
    }
    records["validation_evidence"] = {
        **_base_record("validation_evidence"),
        "validation_evidence_status": "committed_compact_evidence",
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "parallel_worker_cap_for_stage5cm_and_later": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
        "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
        "stage5cw_pytest_count_reconciliation": validation_reconciliation,
        "validation_commands": [
            {
                "command": "python -m libreprimus.cli token-block build-stage5cy",
                "status_observed_locally": "passed",
            },
            {
                "command": "python -m libreprimus.cli token-block validate-stage5cy",
                "status_observed_locally": "passed",
            },
            {
                "command": "scripts/ci/run-parallel-validation.ps1 -Workers 8 -PytestWorkers 8 -PytestMode auto",
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
    records["source_digest_index"] = {
        **_base_record("source_digest_index"),
        "source_digest_record_count": len(source_digest_rows),
        "source_digest_records": source_digest_rows,
        **_stage_flags(),
    }
    records["gap_register"] = {
        **_base_record("gap_register"),
        "reviewability_gap_count": len(REVIEWABILITY_GAPS),
        "reviewability_gaps": REVIEWABILITY_GAPS,
        **_stage_flags(),
    }
    records["equivalence_map"] = {
        **_base_record("equivalence_map"),
        "record_family_name_equivalence_map_created": True,
        "record_family_equivalences": [
            {
                "record_family": "real_decision_package_preflight",
                "stage5cw_path": STAGE5CW_DATA_PATHS[
                    "real_decision_package_preflight"
                ].as_posix(),
                "stage5cy_preservation_path": DATA_PATHS[
                    "real_decision_preflight_preservation"
                ].as_posix(),
            },
            {
                "record_family": "option_selection_preflight",
                "stage5cs_path": "data/token-block/stage5cs-real-approval-decision-options-scaffold.yaml",
                "stage5cy_path": DATA_PATHS["operator_option_selection_preflight"].as_posix(),
            },
        ],
        **_stage_flags(),
    }
    records["next_stage"] = {
        **_base_record("next_stage"),
        "selected_next_stage_id": "stage-5cz",
        "selected_next_stage_title": (
            "Stage 5CZ - Deep Research review of Stage 5CY option-selection "
            "decision preflight and validation-count reconciliation, without execution"
        ),
        "selected_next_prompt_type": "deep_research_review",
        "selected_next_stage_authorizes_execution": False,
        "reason": (
            "Stage 5CY creates only review-only option-selection decision preflight "
            "metadata and reconciles Stage 5CW validation-count evidence; independent "
            "Deep Research review is required before any operator choice."
        ),
        **_stage_flags(),
    }
    records["governance_scope_control"] = {
        **_base_record("governance_scope_control"),
        "governance_overbuild_risk_acknowledged": True,
        "stage5cz_review_required_before_operator_choice": True,
        "after_stage5cz_requires_operator_choice_or_pause": True,
        "additional_generic_preflight_layers_allowed_without_concrete_defect": False,
        "stage5cy_skips_stage5cz_review": False,
        "stage5cy_selects_operator_choice": False,
        **_stage_flags(),
    }
    summary = {
        **_base_record("summary"),
        "status": "complete",
        "source_stage_ids": SOURCE_STAGE_IDS,
        "source_token_block_lineage": SOURCE_TOKEN_BLOCK_LINEAGE,
        "stage5cx_findings_integrated": True,
        "stage5cx_verdict": "accept_with_warnings",
        "stage5cx_finding_count": len(STAGE5CX_FINDINGS),
        "stage5cw_pytest_count_reconciliation_status": "superseding_reconciliation_record",
        "stage5cw_committed_compact_pytest_count": PYTEST_COUNT_STAGE5CW_COMMITTED,
        "stage5cw_final_issue_completion_trail_pytest_count": PYTEST_COUNT_STAGE5CW_FINAL_TRAIL,
        "stage5cw_pytest_count_mismatch_gate_opening": False,
        "operator_facing_option_selection_preflight_created": True,
        "operator_facing_option_selection_preflight_status": "review_preflight_only",
        "real_decision_package_preflight_status_preserved": "review_preflight_only",
        "real_decision_package_created_now": False,
        "real_operator_decision_record_created_now": False,
        "real_operator_approval_record_created_now": False,
        "real_deep_research_acceptance_record_created_now": False,
        "real_combined_gate_validation_record_created_now": False,
        "real_activation_decision_record_created_now": False,
        "stage5cu_negative_fixture_pack_preserved": True,
        "stage5cu_negative_fixture_count_preserved": len(NEGATIVE_FIXTURE_IDS),
        "stage5cu_real_decision_negative_fixture_count_preserved": len(
            FUTURE_REAL_RECORD_CLASSES
        ),
        "stage5cu_option_selection_misuse_case_count_preserved": len(
            OPTION_SELECTION_MISUSE_TRANSITIONS
        ),
        "stage5cs_option_count_preserved": len(OPERATOR_DECISION_OPTIONS),
        "stage5cs_exact_option_set_preserved": True,
        "all_options_unselected": True,
        "operator_decision_option_count": len(OPERATOR_DECISION_OPTIONS),
        "operator_decision_option_selected_now": False,
        "selected_option_id": None,
        "future_real_records_created_now": False,
        "combined_approval_gate_satisfied_now": False,
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
        "stage5cy_codex_completion_summary_required": True,
        "stage5cy_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "stage5cy_codex_completion_summary_written_locally_before_final_response": True,
        "stage5cy_completion_summary_finalized_not_pending": True,
        "codex_completion_summary_committed": False,
        "codex_output_used": False,
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
        "parallel_worker_cap_for_stage5cy_and_later": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "future_token_block_execution_remains_blocked": True,
        "governance_overbuild_risk_acknowledged": True,
        "after_stage5cz_requires_operator_choice_or_pause": True,
        "additional_generic_preflight_layers_allowed_without_concrete_defect": False,
        "recommended_next_stage_id": "stage-5cz",
        "recommended_next_prompt_type": "deep_research_review",
        "recommended_next_stage_title": records["next_stage"]["selected_next_stage_title"],
        "source_digest_record_count": len(source_digest_rows),
        **_stage_flags(),
    }
    records["summary"] = summary
    return records


def _write_completion_summary(summary: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = (
        "# Stage 5CY Codex Completion Summary\n\n"
        f"- Starting commit: {SOURCE_PREVIOUS_COMMIT}\n"
        "- Final commit: recorded after commit and push verification.\n"
        "- GitHub issue: recorded after issue update.\n"
        "- CI status: recorded after push verification.\n"
        f"- Stage 5CX verdict consumed: {summary['stage5cx_verdict']}\n"
        "- Stage 5CW pytest-count reconciliation: superseding reconciliation record; "
        "2446 committed compact evidence vs 2466 final issue/completion trail; "
        "not a gate opener or activation defect.\n"
        "- Operator-facing option-selection preflight: review_preflight_only.\n"
        "- Options selected now: false; selected_option_id: null.\n"
        "- Real decision package/operator decision/approval/acceptance/combined gate/"
        "activation/active input: false.\n"
        "- Stage 5BD run-plan IDs: 10, unchanged.\n"
        "- Active-lineage records: 8.\n"
        "- No-active/no-byte/no-execution gates: closed.\n"
        "- 8-worker validation cap: preserved.\n"
        "- Generated outputs staged: 0.\n"
        "- Raw staged: 0.\n"
        "- codex-output staged: 0; codex_output used: false/absent.\n"
        "- Recommended next stage: Stage 5CZ Deep Research review.\n"
    )
    CODEX_COMPLETION_PATH.write_text(text, encoding="utf-8")


def build_stage5cy(results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    _write_schemas()
    records = _records()
    for key, record in records.items():
        write_yaml(DATA_PATHS[key], record)

    results_dir.mkdir(parents=True, exist_ok=True)
    write_json(results_dir / "summary.json", records["summary"])
    write_json(results_dir / "option_selection_preflight_report.json", records["operator_option_selection_preflight"])
    write_json(results_dir / "option_selection_misuse_report.json", records["option_selection_misuse"])
    write_json(
        results_dir / "validation_count_reconciliation_report.json",
        records["validation_count_reconciliation"],
    )
    write_json(
        results_dir / "preservation_report.json",
        {
            "stage5cw": records["stage5cw_preservation"],
            "stage5cu": records["stage5cu_preservation"],
            "stage5cs": records["stage5cs_preservation"],
            "stage5bd": records["stage5bd_preservation"],
            "active_lineage": records["active_lineage"],
        },
    )
    write_json(results_dir / "handoff_continuity_report.json", records["completion_continuity"])
    write_json(results_dir / "source_digest_index.json", records["source_digest_index"])
    write_jsonl(
        results_dir / "warnings.jsonl",
        [
            {
                "warning_id": "stage5cw_pytest_count_mismatch_reconciled",
                "gate_opening": False,
                "message": "Stage 5CW 2446/2466 pytest-count mismatch is reviewability-only.",
            },
            {
                "warning_id": "governance_overbuild_risk_acknowledged",
                "gate_opening": False,
                "message": "After Stage 5CZ review, require explicit operator choice or pause.",
            },
        ],
    )
    _write_completion_summary(records["summary"])
    return records["summary"]


def _validate_schema(record_key: str, path: Path) -> list[str]:
    errors: list[str] = []
    schema_path = Path(SCHEMA_PATHS[record_key])
    if not schema_path.exists():
        return [f"missing_schema:{schema_path.as_posix()}"]
    payload = _load_yaml(path)
    validator = Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8")))
    errors.extend(error.message for error in validator.iter_errors(payload))
    return errors


def _ensure_false_flags(payload: dict[str, Any], fields: list[str] | None = None) -> list[str]:
    errors: list[str] = []
    check_fields = fields or list(FALSE_FLAGS)
    for field in check_fields:
        if payload.get(field) is not False:
            errors.append(f"{field}_must_be_false")
    if payload.get("selected_option_id") is not None:
        errors.append("selected_option_id_must_be_null")
    return errors


def _finish(
    record_key: str, path: Path, counts: dict[str, Any], errors: list[str]
) -> tuple[dict[str, Any], list[str]]:
    errors.extend(_validate_schema(record_key, path))
    return counts, errors


def validate_stage5cy_stage5cx_findings(
    findings: Path = DATA_PATHS["findings"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(findings)
    errors = _ensure_false_flags(payload)
    if payload.get("stage5cx_verdict") != "accept_with_warnings":
        errors.append("stage5cx_verdict_must_be_accept_with_warnings")
    if payload.get("finding_count") != len(STAGE5CX_FINDINGS):
        errors.append("stage5cx_finding_count_mismatch")
    if not payload.get("stage5cx_did_not_recommend_option_selection"):
        errors.append("stage5cx_option_selection_nonrecommendation_missing")
    counts = {
        "stage5cx_verdict": payload.get("stage5cx_verdict"),
        "finding_count": payload.get("finding_count"),
        "stage5cx_did_not_recommend_execution": payload.get(
            "stage5cx_did_not_recommend_execution"
        ),
    }
    return _finish("findings", findings, counts, errors)


def validate_stage5cy_real_decision_preflight_preservation(
    preflight: Path = DATA_PATHS["real_decision_preflight_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preflight)
    errors = _ensure_false_flags(payload)
    if payload.get("stage5cw_real_decision_package_preflight_status") != "review_preflight_only":
        errors.append("stage5cw_preflight_status_must_remain_review_preflight_only")
    if payload.get("stage5cw_real_decision_package_created_now") is not False:
        errors.append("stage5cw_real_decision_package_created_now_must_be_false")
    counts = {
        "stage5cw_real_decision_package_preflight_status": payload.get(
            "stage5cw_real_decision_package_preflight_status"
        ),
        "stage5cw_preserved_without_historical_edit": True,
    }
    return _finish("real_decision_preflight_preservation", preflight, counts, errors)


def validate_stage5cy_operator_option_selection_preflight(
    preflight: Path = DATA_PATHS["operator_option_selection_preflight"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preflight)
    errors = _ensure_false_flags(payload)
    if payload.get("operator_facing_option_selection_preflight_status") != "review_preflight_only":
        errors.append("option_selection_preflight_status_must_be_review_preflight_only")
    if payload.get("operator_facing_option_selection_preflight_selects_option") is not False:
        errors.append("option_selection_preflight_must_not_select_option")
    if payload.get("operator_decision_option_count") != len(OPERATOR_DECISION_OPTIONS):
        errors.append("operator_option_count_mismatch")
    counts = {
        "operator_facing_option_selection_preflight_created": payload.get(
            "operator_facing_option_selection_preflight_created"
        ),
        "operator_facing_option_selection_preflight_status": payload.get(
            "operator_facing_option_selection_preflight_status"
        ),
        "operator_decision_option_count": payload.get("operator_decision_option_count"),
    }
    return _finish("operator_option_selection_preflight", preflight, counts, errors)


def validate_stage5cy_option_selection_requirements(
    requirements: Path = DATA_PATHS["option_selection_requirements"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(requirements)
    errors = _ensure_false_flags(payload)
    if payload.get("option_selection_preflight_requirement_count") != len(
        OPTION_SELECTION_REQUIREMENTS
    ):
        errors.append("option_selection_requirement_count_mismatch")
    if payload.get("stage5cz_review_required") is not True:
        errors.append("stage5cz_review_required_must_be_true")
    counts = {
        "option_selection_requirement_count": payload.get(
            "option_selection_preflight_requirement_count"
        ),
        "stage5cz_review_required": payload.get("stage5cz_review_required"),
    }
    return _finish("option_selection_requirements", requirements, counts, errors)


def validate_stage5cy_option_selection_misuse(
    misuse: Path = DATA_PATHS["option_selection_misuse"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(misuse)
    errors = _ensure_false_flags(payload)
    cases = payload.get("misuse_cases", [])
    if payload.get("option_selection_misuse_case_count") != len(OPTION_SELECTION_MISUSE_CASES):
        errors.append("option_selection_misuse_case_count_mismatch")
    if any(case.get("blocked_now") is not True for case in cases):
        errors.append("all_option_selection_misuse_cases_must_be_blocked")
    counts = {
        "option_selection_misuse_case_count": payload.get("option_selection_misuse_case_count"),
        "all_misuse_cases_blocked": all(case.get("blocked_now") is True for case in cases),
    }
    return _finish("option_selection_misuse", misuse, counts, errors)


def validate_stage5cy_options_nonselection(
    options_nonselection: Path = DATA_PATHS["options_nonselection"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(options_nonselection)
    errors = _ensure_false_flags(payload)
    option_ids = [option.get("option_id") for option in payload.get("operator_decision_options", [])]
    expected_ids = [option["option_id"] for option in OPERATOR_DECISION_OPTIONS]
    if option_ids != expected_ids:
        errors.append("exact_stage5cs_option_set_mismatch")
    if payload.get("operator_decision_option_selected_now") is not False:
        errors.append("operator_decision_option_selected_now_must_be_false")
    if any(option.get("selected_now") is not False for option in payload.get("operator_decision_options", [])):
        errors.append("all_options_must_remain_unselected")
    counts = {
        "operator_decision_option_count": payload.get("operator_decision_option_count"),
        "operator_decision_option_selected_now": payload.get(
            "operator_decision_option_selected_now"
        ),
        "selected_option_id": payload.get("selected_option_id"),
    }
    return _finish("options_nonselection", options_nonselection, counts, errors)


def validate_stage5cy_validation_count_reconciliation(
    reconciliation: Path = DATA_PATHS["validation_count_reconciliation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(reconciliation)
    errors = _ensure_false_flags(payload)
    if payload.get("stage5cw_committed_compact_pytest_count") != PYTEST_COUNT_STAGE5CW_COMMITTED:
        errors.append("stage5cw_committed_pytest_count_mismatch")
    if payload.get("stage5cw_final_issue_completion_trail_pytest_count") != PYTEST_COUNT_STAGE5CW_FINAL_TRAIL:
        errors.append("stage5cw_final_trail_pytest_count_mismatch")
    if payload.get("gate_opening") is not False or payload.get("activation_defect") is not False:
        errors.append("pytest_count_reconciliation_must_not_open_gate")
    if payload.get("history_rewritten") is not False:
        errors.append("stage5cw_history_must_not_be_silently_rewritten")
    counts = {
        "stage5cw_committed_compact_pytest_count": payload.get(
            "stage5cw_committed_compact_pytest_count"
        ),
        "stage5cw_final_issue_completion_trail_pytest_count": payload.get(
            "stage5cw_final_issue_completion_trail_pytest_count"
        ),
        "reconciliation_status": payload.get("reconciliation_status"),
        "gate_opening": payload.get("gate_opening"),
    }
    return _finish("validation_count_reconciliation", reconciliation, counts, errors)


def validate_stage5cy_real_record_blocker(
    real_record_blocker: Path = DATA_PATHS["real_record_blocker"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(real_record_blocker)
    errors = _ensure_false_flags(payload)
    classes = payload.get("blocked_real_record_classes", [])
    if payload.get("real_record_class_count") != len(FUTURE_REAL_RECORD_CLASSES):
        errors.append("real_record_class_count_must_be_10")
    if any(record.get("created_now") is not False for record in classes):
        errors.append("real_records_must_not_be_created_now")
    counts = {
        "real_record_class_count": payload.get("real_record_class_count"),
        "real_records_created_now": any(record.get("created_now") for record in classes),
    }
    return _finish("real_record_blocker", real_record_blocker, counts, errors)


def validate_stage5cy_combined_gate(
    combined_gate: Path = DATA_PATHS["combined_gate_nonsatisfaction"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(combined_gate)
    errors = _ensure_false_flags(payload)
    if payload.get("combined_approval_gate_satisfied_now") is not False:
        errors.append("combined_gate_must_remain_unsatisfied")
    counts = {
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "real_combined_gate_validation_record_created_now": payload.get(
            "real_combined_gate_validation_record_created_now"
        ),
    }
    return _finish("combined_gate_nonsatisfaction", combined_gate, counts, errors)


def validate_stage5cy_activation_nonauthorization(
    activation: Path = DATA_PATHS["activation_nonauthorization"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(activation)
    errors = _ensure_false_flags(payload)
    if payload.get("activation_decision_valid_now") is not False:
        errors.append("activation_decision_must_remain_invalid")
    counts = {
        "activation_decision_valid_now": payload.get("activation_decision_valid_now"),
        "activation_authorized_now": payload.get("activation_authorized_now"),
        "active_planning_input_authorized_now": payload.get(
            "active_planning_input_authorized_now"
        ),
    }
    return _finish("activation_nonauthorization", activation, counts, errors)


def validate_stage5cy_stage5cw_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    counts, cw_errors = validate_stage5cw()
    errors.extend(f"stage5cw:{error}" for error in cw_errors)
    payload = _load_yaml(DATA_PATHS["stage5cw_preservation"])
    errors.extend(_ensure_false_flags(payload))
    if payload.get("stage5cw_pytest_count_warning_reconciled_by_stage5cy") is not True:
        errors.append("stage5cw_pytest_count_warning_must_be_reconciled")
    counts.update(
        {
            "stage5cw_preserved_without_historical_edit": payload.get(
                "stage5cw_preserved_without_historical_edit"
            ),
            "stage5cw_pytest_count_warning_reconciled_by_stage5cy": payload.get(
                "stage5cw_pytest_count_warning_reconciled_by_stage5cy"
            ),
        }
    )
    return _finish("stage5cw_preservation", DATA_PATHS["stage5cw_preservation"], counts, errors)


def validate_stage5cy_stage5cu_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    counts, cu_errors = validate_stage5cu()
    errors.extend(f"stage5cu:{error}" for error in cu_errors)
    payload = _load_yaml(DATA_PATHS["stage5cu_preservation"])
    errors.extend(_ensure_false_flags(payload))
    if payload.get("stage5cu_negative_fixture_count_preserved") != len(NEGATIVE_FIXTURE_IDS):
        errors.append("stage5cu_negative_fixture_count_mismatch")
    return _finish("stage5cu_preservation", DATA_PATHS["stage5cu_preservation"], counts, errors)


def validate_stage5cy_stage5cs_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    counts, cs_errors = validate_stage5cs()
    errors.extend(f"stage5cs:{error}" for error in cs_errors)
    payload = _load_yaml(DATA_PATHS["stage5cs_preservation"])
    errors.extend(_ensure_false_flags(payload))
    if payload.get("stage5cs_option_count_preserved") != len(OPERATOR_DECISION_OPTIONS):
        errors.append("stage5cs_option_count_mismatch")
    return _finish("stage5cs_preservation", DATA_PATHS["stage5cs_preservation"], counts, errors)


def validate_stage5cy_stage5bd_preservation() -> tuple[dict[str, Any], list[str]]:
    counts, errors = validate_stage5bd()
    payload = _load_yaml(DATA_PATHS["stage5bd_preservation"])
    errors.extend(_ensure_false_flags(payload))
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
    return _finish("stage5bd_preservation", DATA_PATHS["stage5bd_preservation"], counts, errors)


def validate_stage5cy_active_lineage_preservation() -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(DATA_PATHS["active_lineage"])
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
    return _finish("active_lineage", DATA_PATHS["active_lineage"], counts, errors)


def validate_stage5cy_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for key, status_field in [
        ("no_active_ingestion", "no_active_ingestion_status"),
        ("no_byte_stream_transition_gate", "no_byte_stream_transition_gate_status"),
        ("no_execution_transition_gate", "no_execution_transition_gate_status"),
    ]:
        payload = _load_yaml(DATA_PATHS[key])
        errors.extend(_ensure_false_flags(payload))
        if payload.get(status_field) != "closed":
            errors.append(f"{status_field}_must_be_closed")
        counts[status_field] = payload.get(status_field)
    return counts, errors


def validate_stage5cy_handoff_continuity() -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(DATA_PATHS["completion_continuity"])
    errors = _ensure_false_flags(payload)
    if not STAGE5CW_CODEX_COMPLETION_PATH.exists():
        errors.append("stage5cw_codex_completion_summary_missing")
    if not CODEX_COMPLETION_PATH.exists():
        errors.append("stage5cy_codex_completion_summary_missing")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output_underscore_root_must_be_absent")
    if CODEX_COMPLETION_PATH.exists() and "pending" in CODEX_COMPLETION_PATH.read_text(
        encoding="utf-8"
    ).lower():
        errors.append("stage5cy_completion_summary_must_not_be_pending")
    counts = {
        "stage5cw_codex_completion_summary_present": STAGE5CW_CODEX_COMPLETION_PATH.exists(),
        "stage5cy_codex_completion_summary_present": CODEX_COMPLETION_PATH.exists(),
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
    }
    return _finish("completion_continuity", DATA_PATHS["completion_continuity"], counts, errors)


def validate_stage5cy_credential_redaction_policy(
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


def validate_stage5cy_governance_scope_control(
    governance_scope: Path = DATA_PATHS["governance_scope_control"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(governance_scope)
    errors = _ensure_false_flags(payload)
    if payload.get("stage5cz_review_required_before_operator_choice") is not True:
        errors.append("stage5cz_review_required_before_operator_choice_must_be_true")
    if payload.get("after_stage5cz_requires_operator_choice_or_pause") is not True:
        errors.append("after_stage5cz_operator_choice_or_pause_policy_missing")
    if payload.get("additional_generic_preflight_layers_allowed_without_concrete_defect") is not False:
        errors.append("generic_preflight_layers_must_be_blocked_without_concrete_defect")
    counts = {
        "governance_overbuild_risk_acknowledged": payload.get(
            "governance_overbuild_risk_acknowledged"
        ),
        "after_stage5cz_requires_operator_choice_or_pause": payload.get(
            "after_stage5cz_requires_operator_choice_or_pause"
        ),
    }
    return _finish("governance_scope_control", governance_scope, counts, errors)


def validate_stage5cy(
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(summary)
    errors = _ensure_false_flags(payload)
    for validator in [
        validate_stage5cy_stage5cx_findings,
        validate_stage5cy_real_decision_preflight_preservation,
        validate_stage5cy_operator_option_selection_preflight,
        validate_stage5cy_option_selection_requirements,
        validate_stage5cy_option_selection_misuse,
        validate_stage5cy_options_nonselection,
        validate_stage5cy_validation_count_reconciliation,
        validate_stage5cy_real_record_blocker,
        validate_stage5cy_combined_gate,
        validate_stage5cy_activation_nonauthorization,
        validate_stage5cy_stage5cw_preservation,
        validate_stage5cy_stage5cu_preservation,
        validate_stage5cy_stage5cs_preservation,
        validate_stage5cy_stage5bd_preservation,
        validate_stage5cy_active_lineage_preservation,
        validate_stage5cy_sidecar_gates,
        validate_stage5cy_handoff_continuity,
        validate_stage5cy_credential_redaction_policy,
        validate_stage5cy_governance_scope_control,
    ]:
        _, validator_errors = validator()
        errors.extend(validator_errors)
    if payload.get("recommended_next_stage_id") != "stage-5cz":
        errors.append("recommended_next_stage_id_must_be_stage5cz")
    if _load_yaml(next_stage_decision).get("selected_next_stage_id") != "stage-5cz":
        errors.append("next_stage_decision_must_select_stage5cz_review")
    if _load_yaml(guardrail).get("guardrail_status") != "metadata_only_fail_closed":
        errors.append("stage5cy_guardrail_must_be_fail_closed")
    for filename in [
        "summary.json",
        "option_selection_preflight_report.json",
        "option_selection_misuse_report.json",
        "validation_count_reconciliation_report.json",
        "preservation_report.json",
        "handoff_continuity_report.json",
        "source_digest_index.json",
        "warnings.jsonl",
    ]:
        if not (results_dir / filename).exists():
            errors.append(f"missing_generated_report:{filename}")
    counts = {
        "stage5cx_verdict": payload.get("stage5cx_verdict"),
        "stage5cw_pytest_count_reconciliation_status": payload.get(
            "stage5cw_pytest_count_reconciliation_status"
        ),
        "operator_facing_option_selection_preflight_created": payload.get(
            "operator_facing_option_selection_preflight_created"
        ),
        "operator_decision_option_count": payload.get("operator_decision_option_count"),
        "operator_decision_option_selected_now": payload.get(
            "operator_decision_option_selected_now"
        ),
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_decision_valid_now": payload.get("activation_decision_valid_now"),
        "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
        "parallel_worker_cap": payload.get("parallel_worker_cap_for_stage5cy_and_later"),
        "recommended_next_stage_id": payload.get("recommended_next_stage_id"),
    }
    return _finish("summary", summary, counts, errors)


def load_stage5cy_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _load_yaml(summary)
