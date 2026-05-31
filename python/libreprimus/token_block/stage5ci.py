"""Stage 5CI approval-record template hardening metadata."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import repo_relative, sha256_file, write_json, write_yaml
from libreprimus.token_block.stage5bm import _read
from libreprimus.token_block.stage5ca import (
    ACTIVE_LINEAGE_PATHS,
    CORRECT_STAGE5AW_PATH,
    INCORRECT_STAGE5AW_PATH,
    REQUIRED_ACTIVATION_PRECONDITIONS,
    REQUIRED_CITATION_PATHS,
    REQUIRED_FAIL_CLOSED_TRIGGERS,
    validate_stage5ca_citation_contract,
)
from libreprimus.token_block.stage5cc import (
    BLOCKED_BYTE_STREAM_ACTIONS,
    validate_stage5cc,
    validate_stage5cc_activation_preconditions,
    validate_stage5cc_fail_closed_triggers,
)
from libreprimus.token_block.stage5ce import (
    DATA_PATHS as STAGE5CE_DATA_PATHS,
    RESULTS_DIR as STAGE5CE_RESULTS_DIR,
    validate_stage5ce,
)
from libreprimus.token_block.stage5cg import (
    DATA_PATHS as STAGE5CG_DATA_PATHS,
    RESULTS_DIR as STAGE5CG_RESULTS_DIR,
    validate_stage5cg,
)

STAGE_ID = "stage-5ci"
STAGE_TITLE = (
    "Stage 5CI - Operator/Deep Research approval-record template hardening and "
    "activation-decision validation preflight, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5cg"
SOURCE_PREVIOUS_COMMIT = "43b4f923e780350de24f421e99265c1d14eb6217"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5ch"
SOURCE_DEEP_RESEARCH_REPORT = "19_Stage-5CG-Deep-Research-Review.md"
STAGE5CH_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "19_Stage-5CG-Deep-Research-Review.md"
)
RESULTS_DIR = Path("experiments/results/token-block/stage5ci")
CODEX_COMPLETION_PATH = Path("codex-output/stage5ci-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

# Updated after the final local pytest run in this stage.
PYTEST_COUNT_OBSERVED_LOCALLY = 2305
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"

STAGE5CH_FINDINGS = [
    "stage5cg_coherent_metadata_only_no_execution_stage",
    "stage5cg_safely_integrates_stage5cf_accept_with_warnings_review",
    "stage5cg_creates_operator_approval_decision_scaffold",
    "stage5cg_creates_deep_research_acceptance_decision_scaffold",
    "stage5cg_creates_combined_approval_gate_scaffold",
    "stage5cg_creates_active_planning_input_decision_record_scaffold",
    "stage5cg_creates_approval_gate_non_satisfaction_proof",
    "stage5cg_does_not_create_operator_approval_record",
    "stage5cg_does_not_create_deep_research_activation_acceptance_record",
    "stage5cg_does_not_satisfy_approval_gate",
    "stage5cg_does_not_authorize_activation",
    "stage5cg_does_not_authorize_or_select_active_planning_input",
    "stage5cg_does_not_create_new_active_planning_input",
    "stage5cg_preserves_stage5ce_proposal_package_as_review_package_only",
    "stage5cg_preserves_stage5ce_operator_deep_research_gate_design",
    "stage5cg_preserves_stage5cc_exact_contracts",
    "stage5cg_preserves_stage5bd_run_plan_ids_and_dry_run_records",
    "stage5cg_preserves_eight_active_lineage_records_and_correct_stage5aw_path",
    "stage5cg_keeps_no_byte_stream_and_no_execution_gates_closed",
    "stage5cg_records_stage5ce_wording_blemish_as_non_gate_opening",
    "stage5cg_remains_safe_to_build_on",
    "remaining_warnings_are_reviewability_validation_polish_not_gate_opening",
]

STAGE5CH_WARNING_ACTIONS = {
    "warning_1_public_github_corroboration_unavailable_or_stale": [
        "preserve_external_evidence_caveat",
        "keep_reviewable_metadata_committed",
        "do_not_attempt_final_commit_self_embedding",
    ],
    "warning_2_attached_zip_not_pristine": [
        "preserve_packaging_warning",
        "keep_raw_generated_uncommitted",
        "record_packaging_dirt_does_not_authorize_activation",
    ],
    "warning_3_active_planning_input_decision_scaffold_minimalist": [
        "harden_active_planning_input_activation_decision_template",
        "harden_activation_decision_validator_surface",
        "require_exact_references_to_stage5ce_and_stage5cg_metadata",
        "require_no_byte_and_no_execution_acknowledgements",
        "require_stage5bd_preservation_or_explicit_future_supersession",
        "require_active_lineage_preservation_or_explicit_future_supersession",
        "keep_current_stage_authorizes_activation_false",
    ],
}

OPERATOR_TEMPLATE_REQUIRED_FIELDS = [
    "record_type",
    "stage_id",
    "operator_identity_or_handle",
    "approval_scope",
    "approval_decision",
    "approval_timestamp_utc",
    "stage5ce_proposal_package_path",
    "stage5cg_operator_scaffold_path",
    "stage5ci_template_version",
    "no_byte_stream_acknowledgement",
    "no_execution_acknowledgement",
    "stage5bd_preservation_acknowledgement",
    "active_lineage_preservation_acknowledgement",
    "manifest_supersession_statement",
    "solve_claim_false_acknowledgement",
]

DEEP_RESEARCH_TEMPLATE_REQUIRED_FIELDS = [
    "record_type",
    "stage_id",
    "deep_research_review_id",
    "acceptance_decision",
    "acceptance_timestamp_utc",
    "stage5ce_proposal_package_path",
    "stage5cg_deep_research_scaffold_path",
    "stage5ci_template_version",
    "review_scope",
    "warnings_disposition",
    "no_byte_stream_acknowledgement",
    "no_execution_acknowledgement",
    "stage5bd_preservation_acknowledgement",
    "active_lineage_preservation_acknowledgement",
    "solve_claim_false_acknowledgement",
]

ACTIVATION_DECISION_TEMPLATE_REQUIRED_FIELDS = [
    "record_type",
    "stage_id",
    "activation_decision_id",
    "operator_approval_record_path",
    "deep_research_acceptance_record_path",
    "combined_gate_validation_path",
    "stage5ce_proposal_package_path",
    "stage5cg_combined_gate_scaffold_path",
    "stage5ci_template_version",
    "active_planning_input_candidate_path",
    "selected_active_planning_input",
    "string4_status",
    "no_byte_stream_acknowledgement",
    "no_execution_acknowledgement",
    "stage5bd_preservation_or_supersession_statement",
    "active_lineage_preservation_or_supersession_statement",
    "manifest_supersession_statement",
    "solve_claim_false_acknowledgement",
]

NEGATIVE_FAILURE_CLASSES = [
    "missing_operator_approval_record",
    "missing_deep_research_acceptance_record",
    "template_misread_as_approval",
    "byte_stream_authorized",
    "execution_authorized",
    "dry_run_ingestion_authorized",
    "manifest_supersession_authorized",
    "deprecated_stage5aw_path_present",
    "codex_output_used",
    "solve_claim_true",
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5ci-summary.yaml"),
    "next_stage": Path("data/project-state/stage5ci-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5ci-stage5ch-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5ci-reviewable-stage-marker.yaml"),
    "validation_evidence": Path(
        "data/project-state/stage5ci-reviewable-validation-evidence.yaml"
    ),
    "source_digest_index": Path(
        "data/project-state/stage5ci-reviewable-source-digest-index.yaml"
    ),
    "gap_register": Path("data/project-state/stage5ci-reviewability-gap-register.yaml"),
    "equivalence_map": Path(
        "data/project-state/stage5ci-record-family-name-equivalence-map.yaml"
    ),
    "operator_template": Path("data/token-block/stage5ci-operator-approval-record-template.yaml"),
    "operator_validation": Path(
        "data/token-block/stage5ci-operator-approval-template-validation-requirements.yaml"
    ),
    "deep_research_template": Path(
        "data/token-block/stage5ci-deep-research-acceptance-record-template.yaml"
    ),
    "deep_research_validation": Path(
        "data/token-block/stage5ci-deep-research-acceptance-template-validation-requirements.yaml"
    ),
    "combined_gate": Path(
        "data/token-block/stage5ci-combined-approval-gate-validation-preflight.yaml"
    ),
    "approval_non_satisfaction": Path(
        "data/token-block/stage5ci-combined-approval-gate-non-satisfaction-proof.yaml"
    ),
    "activation_template": Path(
        "data/token-block/stage5ci-active-planning-input-activation-decision-template.yaml"
    ),
    "activation_validation": Path(
        "data/token-block/stage5ci-activation-decision-validation-requirements.yaml"
    ),
    "field_contract": Path(
        "data/token-block/stage5ci-decision-record-field-completeness-contract.yaml"
    ),
    "negative_contract": Path(
        "data/token-block/stage5ci-approval-record-negative-validation-contract.yaml"
    ),
    "stage5cg_preservation": Path("data/token-block/stage5ci-stage5cg-scaffold-preservation.yaml"),
    "stage5ce_preservation": Path(
        "data/token-block/stage5ci-stage5ce-proposal-package-preservation.yaml"
    ),
    "stage5cc_preservation": Path("data/token-block/stage5ci-stage5cc-contract-preservation.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5ci-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5ci-active-lineage-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5ci-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5ci-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5ci-no-execution-transition-gate.yaml"
    ),
    "supersession_nonactivation": Path(
        "data/token-block/stage5ci-manifest-supersession-nonactivation-proof.yaml"
    ),
    "sidecar_activation_blocker": Path("data/token-block/stage5ci-sidecar-activation-blocker.yaml"),
    "future_impact": Path("data/token-block/stage5ci-future-dry-run-planning-impact.yaml"),
    "dwh": Path("data/historical-route/stage5ci-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5ci-source-gap-severity-update.yaml"),
    "guardrail": Path("data/historical-route/stage5ci-guardrail.yaml"),
    "handoff": Path("data/source-harvester/stage5ci-codex-handoff-policy.yaml"),
    "review_packaging_warning": Path("data/source-harvester/stage5ci-review-packaging-warning.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}

RECORD_TYPES = {key: f"stage5ci_{key}" for key in DATA_PATHS}
RECORD_TYPES.update(
    {
        "operator_template": "stage5ci_operator_approval_record_template",
        "operator_validation": "stage5ci_operator_approval_template_validation_requirements",
        "deep_research_template": "stage5ci_deep_research_acceptance_record_template",
        "deep_research_validation": (
            "stage5ci_deep_research_acceptance_template_validation_requirements"
        ),
        "combined_gate": "stage5ci_combined_approval_gate_validation_preflight",
        "approval_non_satisfaction": "stage5ci_combined_approval_gate_non_satisfaction_proof",
        "activation_template": "stage5ci_active_planning_input_activation_decision_template",
        "activation_validation": "stage5ci_activation_decision_validation_requirements",
        "field_contract": "stage5ci_decision_record_field_completeness_contract",
        "negative_contract": "stage5ci_approval_record_negative_validation_contract",
        "no_byte_stream_transition_gate": "stage5ci_no_byte_stream_transition_gate",
        "no_execution_transition_gate": "stage5ci_no_execution_transition_gate",
    }
)

FALSE_FLAGS = {
    "activation_authorized_now": False,
    "activation_decision_valid_now": False,
    "active_ingestion_performed": False,
    "active_manifest_registry_updated": False,
    "active_planning_input_authorized_now": False,
    "active_planning_input_decision_record_created_now": False,
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
    "deep_research_acceptance_authorizes_activation_now": False,
    "deep_research_activation_accept_record_created_now": False,
    "deep_research_activation_accept_record_present_now": False,
    "deep_research_activation_accept_satisfied_now": False,
    "dry_run_ingestion_authorized_now": False,
    "dwh_hash_search_performed": False,
    "execution_allowed": False,
    "execution_authorized_now": False,
    "final_commit_self_embedded": False,
    "full_cartesian_product_enumerated": False,
    "generated_byte_streams_committed": False,
    "generated_outputs_committed": False,
    "hash_preimage_search_performed": False,
    "image_forensics_performed": False,
    "llm_vision_token_reading_performed": False,
    "manifest_supersession_authorized_now": False,
    "manifest_supersession_performed": False,
    "method_status_upgraded": False,
    "new_active_planning_input_created": False,
    "ocr_performed": False,
    "operator_approval_authorizes_activation_now": False,
    "operator_approval_record_created_now": False,
    "operator_approval_record_present_now": False,
    "operator_approval_satisfied_now": False,
    "page_boundaries_final": False,
    "pgp_network_verification_performed": False,
    "raw_archive_files_committed": False,
    "raw_fandom_files_committed": False,
    "raw_human_review_pack_committed": False,
    "real_byte_stream_generated": False,
    "scoring_performed": False,
    "solve_claim": False,
    "spreadsheet_file_committed": False,
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
    "template_bodies_committed": False,
    "template_misread_as_approval": False,
    "token_block_experiment_executed": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "website_expansion_performed": False,
}


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
    }


def _record(key: str, body: dict[str, Any], *, include_false_flags: bool = True) -> dict[str, Any]:
    payload = _base(RECORD_TYPES[key], key)
    payload.update(body)
    if include_false_flags:
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
        path = Path(schema_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(_schema(RECORD_TYPES[key]), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def _sha_record(path: Path, *, role: str) -> dict[str, Any]:
    return {
        "path": repo_relative(path),
        "role": role,
        "present": path.is_file(),
        "sha256": sha256_file(path) if path.is_file() else None,
        "size_bytes": path.stat().st_size if path.is_file() else None,
        "raw_or_generated_body_committed": False,
    }


def _run_plan_count() -> int:
    payload = _read(Path("data/token-block/stage5bd-run-plan-id-registry.yaml"))
    return int(payload.get("run_plan_id_count") or len(payload.get("plan_ids", [])))


def _source_paths() -> list[str]:
    paths = [
        str(STAGE5CH_REPORT_PATH),
        "data/project-state/stage5cg-summary.yaml",
        "data/project-state/stage5cg-next-stage-decision.yaml",
        "data/token-block/stage5cg-operator-approval-decision-scaffold.yaml",
        "data/token-block/stage5cg-deep-research-acceptance-decision-scaffold.yaml",
        "data/token-block/stage5cg-combined-approval-decision-gate-scaffold.yaml",
        "data/token-block/stage5cg-active-planning-input-decision-record-scaffold.yaml",
        "data/token-block/stage5cg-approval-gate-non-satisfaction-proof.yaml",
        "data/token-block/stage5cg-stage5ce-proposal-package-preservation.yaml",
        "data/token-block/stage5cg-stage5ce-gate-design-preservation.yaml",
        "data/token-block/stage5cg-stage5cc-contract-preservation.yaml",
        "data/token-block/stage5cg-stage5bd-plan-preservation.yaml",
        "data/token-block/stage5cg-active-lineage-preservation.yaml",
        "data/token-block/stage5cg-no-byte-stream-transition-gate.yaml",
        "data/token-block/stage5cg-no-execution-transition-gate.yaml",
        "data/project-state/stage5ce-summary.yaml",
        "data/token-block/stage5ce-active-planning-input-proposal-package.yaml",
        "data/token-block/stage5ce-operator-deep-research-combined-gate-contract.yaml",
        "data/project-state/stage5cc-summary.yaml",
        "data/token-block/stage5cc-future-runner-citation-contract-preservation.yaml",
        "data/token-block/stage5cc-fail-closed-trigger-exact-set-contract.yaml",
        "data/token-block/stage5cc-activation-precondition-exact-set-contract.yaml",
        "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
        "data/token-block/stage5bd-run-plan-id-registry.yaml",
        "data/token-block/stage5bd-active-manifest-lock.yaml",
        "README.md",
        "STATUS.md",
        "AGENTS.md",
        "ROADMAP.md",
        "TESTING.md",
        "RESULTS_SCHEMA.md",
        "EXPERIMENTS.md",
        "docs/roadmap/staged-plan.md",
        "docs/onboarding/start-here.md",
        "docs/onboarding/source-of-truth-map.md",
        "docs/onboarding/operational-file-map.md",
        "docs/onboarding/codex-navigation-map.md",
        "docs/onboarding/deep-research-handoff-map.md",
        "docs/onboarding/token-block-preflight-dry-run-workflow.md",
        "docs/reference/token-block-cli.md",
        *ACTIVE_LINEAGE_PATHS,
        *REQUIRED_CITATION_PATHS,
    ]
    return list(dict.fromkeys(paths))


def _validation_commands() -> list[dict[str, Any]]:
    commands = [
        "python -m libreprimus.cli token-block build-stage5ci",
        "python -m libreprimus.cli token-block validate-stage5ci-operator-approval-template",
        "python -m libreprimus.cli token-block validate-stage5ci-deep-research-acceptance-template",
        "python -m libreprimus.cli token-block validate-stage5ci-combined-approval-gate",
        "python -m libreprimus.cli token-block validate-stage5ci-activation-decision-template",
        "python -m libreprimus.cli token-block validate-stage5ci-negative-validation-contract",
        "python -m libreprimus.cli token-block validate-stage5ci-sidecar-gates",
        "python -m libreprimus.cli token-block validate-stage5ci",
        "python -m libreprimus.cli token-block stage5ci-summary",
        "python -m libreprimus.cli token-block validate-stage5cg",
        "python -m libreprimus.cli token-block validate-stage5ce",
        "python -m libreprimus.cli token-block validate-stage5cc",
        "python -m libreprimus.cli token-block validate-stage5ca",
        "python -m libreprimus.cli parallel-validation validate-stage5ax",
        ".\\scripts\\ci\\run-parallel-validation.ps1 -Workers 16 -PytestWorkers 16 -PytestMode auto",
        "python -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md",
        "python -m libreprimus.cli consistency check-state-drift",
        "python -m libreprimus.cli consistency check-all --allow-warnings",
        "python -m libreprimus.cli smoke",
        "python -m ruff check python/libreprimus tests/python",
        "python -m pytest -q tests/python",
        ".\\scripts\\ci\\run-consistency-checks.ps1",
    ]
    return [{"command": command, "safe_to_parallelize": False} for command in commands]


def _build_records(source_records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    stage5cg_summary = _read(STAGE5CG_DATA_PATHS["summary"])
    stage5ce_summary = _read(STAGE5CE_DATA_PATHS["summary"])
    run_plan_count = _run_plan_count()
    active_lineage_records = [_sha_record(Path(path), role="stage5ci_active_lineage") for path in ACTIVE_LINEAGE_PATHS]
    source_unique_count = len({record["path"] for record in source_records})
    gap_records = [
        {
            "gap_id": "public_github_issue_ci_external_or_unavailable",
            "severity": "warning",
            "gate_opener": False,
            "disposition": "external_evidence_caveat_preserved",
        },
        {
            "gap_id": "attached_zip_not_pristine_checkout",
            "severity": "warning",
            "gate_opener": False,
            "disposition": "packaging_warning_recorded_raw_generated_uncommitted",
        },
        {
            "gap_id": "active_planning_input_scaffold_minimalist",
            "severity": "warning",
            "gate_opener": False,
            "disposition": "closed_by_stage5ci_template_hardening",
        },
        {
            "gap_id": "final_commit_self_embedding",
            "severity": "expected_external_evidence",
            "gate_opener": False,
            "disposition": "impossible_by_design_external_evidence_required",
        },
    ]

    records: dict[str, dict[str, Any]] = {
        "findings": _record(
            "findings",
            {
                "stage5ch_findings_integrated": True,
                "stage5ch_verdict": "accept_with_warnings",
                "findings": STAGE5CH_FINDINGS,
                "warning_actions": STAGE5CH_WARNING_ACTIONS,
                "stage5cg_remains_safe_to_build_on": True,
                "warnings_gate_opening": False,
            },
        ),
        "stage_marker": _record(
            "stage_marker",
            {
                "status": "complete",
                "reviewable_stage_marker_status": "active",
                "reviewable_stage_id": STAGE_ID,
                "metadata_only": True,
                "reviewable_commit_self_embedding_expected": False,
            },
        ),
        "validation_evidence": _record(
            "validation_evidence",
            {
                "validation_evidence_status": "planned_and_recorded",
                "validation_commands": _validation_commands(),
                "parallel_validation_required": True,
                "parallel_validation_wrapper": "scripts/ci/run-parallel-validation.ps1",
                "parallel_validation_status_observed_locally": "passed",
                "parallel_validation_pytest_mode_observed_locally": "xdist",
                "bash_wrapper_status": "wsl_present_without_installed_distribution",
                "unsafe_operations_kept_serial": True,
                "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
                "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
            },
        ),
        "source_digest_index": _record(
            "source_digest_index",
            {
                "source_digest_status": "reviewable_metadata_index",
                "source_records": source_records,
                "source_digest_record_count": len(source_records),
                "source_digest_unique_path_count": source_unique_count,
                "stage5ch_report_present": STAGE5CH_REPORT_PATH.is_file(),
            },
        ),
        "gap_register": _record(
            "gap_register",
            {
                "reviewability_gap_status": "warnings_preserved_non_gate_opening",
                "gaps": gap_records,
                "gap_count": len(gap_records),
                "gate_opening_gap_count": 0,
            },
        ),
        "equivalence_map": _record(
            "equivalence_map",
            {
                "record_family_equivalence_status": "explicit",
                "equivalence_families": [
                    {
                        "family_id": "stage5cg_approval_scaffold_family",
                        "paths": [
                            "data/token-block/stage5cg-operator-approval-decision-scaffold.yaml",
                            "data/token-block/stage5cg-deep-research-acceptance-decision-scaffold.yaml",
                            "data/token-block/stage5cg-combined-approval-decision-gate-scaffold.yaml",
                            "data/token-block/stage5cg-active-planning-input-decision-record-scaffold.yaml",
                        ],
                    },
                    {
                        "family_id": "stage5ci_approval_template_family",
                        "paths": [
                            DATA_PATHS["operator_template"].as_posix(),
                            DATA_PATHS["deep_research_template"].as_posix(),
                            DATA_PATHS["combined_gate"].as_posix(),
                            DATA_PATHS["activation_template"].as_posix(),
                        ],
                    },
                ],
            },
        ),
        "operator_template": _record(
            "operator_template",
            {
                "template_id": "stage5ci-future-operator-approval-record-template-v0",
                "template_only": True,
                "actual_operator_approval_record": False,
                "operator_approval_record_template_hardened": True,
                "template_required_fields": OPERATOR_TEMPLATE_REQUIRED_FIELDS,
                "future_record_must_cite": [
                    "data/token-block/stage5ce-active-planning-input-proposal-package.yaml",
                    "data/token-block/stage5cg-operator-approval-decision-scaffold.yaml",
                    DATA_PATHS["operator_validation"].as_posix(),
                ],
                "approval_effect_now": "none",
            },
        ),
        "operator_validation": _record(
            "operator_validation",
            {
                "operator_approval_template_validation_hardened": True,
                "template_required_fields": OPERATOR_TEMPLATE_REQUIRED_FIELDS,
                "must_reject_if_template_only_is_false": True,
                "must_reject_if_actual_approval_record_created_now": True,
                "must_reject_if_approval_satisfies_gate_now": True,
                "must_reject_if_activation_authorized_now": True,
            },
        ),
        "deep_research_template": _record(
            "deep_research_template",
            {
                "template_id": "stage5ci-future-deep-research-acceptance-record-template-v0",
                "template_only": True,
                "actual_deep_research_acceptance_record": False,
                "deep_research_acceptance_record_template_hardened": True,
                "template_required_fields": DEEP_RESEARCH_TEMPLATE_REQUIRED_FIELDS,
                "future_record_must_cite": [
                    "data/token-block/stage5ce-active-planning-input-proposal-package.yaml",
                    "data/token-block/stage5cg-deep-research-acceptance-decision-scaffold.yaml",
                    DATA_PATHS["deep_research_validation"].as_posix(),
                ],
                "approval_effect_now": "none",
            },
        ),
        "deep_research_validation": _record(
            "deep_research_validation",
            {
                "deep_research_acceptance_template_validation_hardened": True,
                "template_required_fields": DEEP_RESEARCH_TEMPLATE_REQUIRED_FIELDS,
                "must_reject_if_template_only_is_false": True,
                "must_reject_if_actual_acceptance_record_created_now": True,
                "must_reject_if_acceptance_satisfies_gate_now": True,
                "must_reject_if_activation_authorized_now": True,
            },
        ),
        "combined_gate": _record(
            "combined_gate",
            {
                "combined_approval_gate_validation_hardened": True,
                "operator_approval_required": True,
                "deep_research_acceptance_required": True,
                "required_approval_record_types": [
                    "future_operator_approval_record",
                    "future_deep_research_activation_acceptance_record",
                ],
                "operator_approval_record_present_now": False,
                "deep_research_activation_accept_record_present_now": False,
                "combined_approval_gate_satisfied_now": False,
                "combined_approval_gate_authorizes_activation_now": False,
                "approval_gate_satisfied_now": False,
                "approval_gate_authorizes_activation_now": False,
                "activation_authorized_now": False,
            },
        ),
        "approval_non_satisfaction": _record(
            "approval_non_satisfaction",
            {
                "approval_gate_non_satisfaction_proof_status": "closed",
                "operator_approval_record_present_now": False,
                "deep_research_activation_accept_record_present_now": False,
                "missing_record_count": 2,
                "approval_gate_satisfied_now": False,
                "activation_authorized_now": False,
            },
        ),
        "activation_template": _record(
            "activation_template",
            {
                "template_id": "stage5ci-future-active-planning-input-activation-decision-template-v0",
                "template_only": True,
                "active_planning_input_activation_decision_template_hardened": True,
                "template_required_fields": ACTIVATION_DECISION_TEMPLATE_REQUIRED_FIELDS,
                "requires_exact_references_to_stage5ce_and_stage5cg_metadata": True,
                "requires_no_byte_and_no_execution_acknowledgements": True,
                "requires_stage5bd_preservation_or_explicit_future_supersession": True,
                "requires_active_lineage_preservation_or_explicit_future_supersession": True,
                "active_planning_input_decision_record_created_now": False,
                "activation_decision_valid_now": False,
                "active_planning_input_authorized_now": False,
                "active_planning_input_selected_now": False,
            },
        ),
        "activation_validation": _record(
            "activation_validation",
            {
                "activation_decision_validator_surface_hardened": True,
                "template_required_fields": ACTIVATION_DECISION_TEMPLATE_REQUIRED_FIELDS,
                "must_reject_without_operator_approval": True,
                "must_reject_without_deep_research_acceptance": True,
                "must_reject_if_byte_stream_authorized": True,
                "must_reject_if_execution_authorized": True,
                "must_reject_if_manifest_supersession_authorized_now": True,
            },
        ),
        "field_contract": _record(
            "field_contract",
            {
                "decision_record_field_completeness_contract_status": "hardened",
                "operator_template_required_field_count": len(OPERATOR_TEMPLATE_REQUIRED_FIELDS),
                "deep_research_template_required_field_count": len(
                    DEEP_RESEARCH_TEMPLATE_REQUIRED_FIELDS
                ),
                "activation_decision_template_required_field_count": len(
                    ACTIVATION_DECISION_TEMPLATE_REQUIRED_FIELDS
                ),
                "operator_template_required_fields": OPERATOR_TEMPLATE_REQUIRED_FIELDS,
                "deep_research_template_required_fields": DEEP_RESEARCH_TEMPLATE_REQUIRED_FIELDS,
                "activation_decision_template_required_fields": ACTIVATION_DECISION_TEMPLATE_REQUIRED_FIELDS,
            },
        ),
        "negative_contract": _record(
            "negative_contract",
            {
                "negative_validation_contract_status": "active",
                "failure_classes": NEGATIVE_FAILURE_CLASSES,
                "failure_class_count": len(NEGATIVE_FAILURE_CLASSES),
                "synthetic_negative_fixtures_only": True,
                "real_approval_records_created": False,
            },
        ),
        "stage5cg_preservation": _record(
            "stage5cg_preservation",
            {
                "stage5cg_status_preserved": True,
                "stage5cg_operator_approval_scaffold_preserved": True,
                "stage5cg_deep_research_acceptance_scaffold_preserved": True,
                "stage5cg_combined_approval_gate_scaffold_preserved": True,
                "stage5cg_active_planning_input_decision_scaffold_preserved": True,
                "stage5cg_approval_gate_satisfied_now": False,
                "stage5cg_activation_authorized_now": False,
                "stage5cg_summary_sha256": sha256_file(STAGE5CG_DATA_PATHS["summary"]),
            },
        ),
        "stage5ce_preservation": _record(
            "stage5ce_preservation",
            {
                "stage5ce_proposal_package_status_preserved": "review_package_only",
                "stage5ce_proposal_package_preserved": True,
                "stage5ce_operator_deep_research_gate_design_preserved": True,
                "stage5ce_summary_sha256": sha256_file(STAGE5CE_DATA_PATHS["summary"]),
                "stage5ce_source_digest_record_count_preserved": int(
                    stage5ce_summary.get("source_digest_record_count", 0)
                ),
            },
        ),
        "stage5cc_preservation": _record(
            "stage5cc_preservation",
            {
                "stage5cc_exact_citation_contract_preserved": True,
                "stage5cc_fail_closed_trigger_exact_set_preserved": True,
                "stage5cc_activation_precondition_exact_set_preserved": True,
                "required_citation_count": len(REQUIRED_CITATION_PATHS),
                "required_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
                "required_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
            },
        ),
        "stage5bd_preservation": _record(
            "stage5bd_preservation",
            {
                "stage5bd_dry_run_records_remain_valid": True,
                "stage5bd_run_plan_id_count": run_plan_count,
                "stage5bd_run_plan_ids_changed": False,
                "stage5bd_dry_run_plan_manifest_changed": False,
                "stage5bd_plan_superseded": False,
            },
        ),
        "active_lineage": _record(
            "active_lineage",
            {
                "active_lineage_preservation_status": "preserved_unchanged",
                "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
                "correct_stage5aw_path_included": True,
                "deprecated_stage5aw_path_absent": True,
                "lineage_records": active_lineage_records,
                "all_lineage_paths_resolve": all(record["present"] for record in active_lineage_records),
            },
        ),
        "no_active_ingestion": _record(
            "no_active_ingestion",
            {
                "no_active_ingestion_proof_status": "closed",
                "string4_sidecar_status": "scaffolded_inactive",
                "string4_active_input_allowed": False,
                "string4_dry_run_ingestion_allowed_now": False,
                "active_planning_input_authorized_now": False,
            },
        ),
        "no_byte_stream_transition_gate": _record(
            "no_byte_stream_transition_gate",
            {
                "no_byte_stream_transition_gate_status": "closed",
                "blocked_actions": BLOCKED_BYTE_STREAM_ACTIONS,
                "byte_stream_generation_authorized_now": False,
                "real_byte_stream_generated": False,
                "variant_byte_streams_generated": False,
            },
        ),
        "no_execution_transition_gate": _record(
            "no_execution_transition_gate",
            {
                "no_execution_transition_gate_status": "closed",
                "execution_authorized_now": False,
                "token_block_experiment_executed": False,
                "dwh_hash_search_performed": False,
                "scoring_performed": False,
                "cuda_execution_performed": False,
            },
        ),
        "supersession_nonactivation": _record(
            "supersession_nonactivation",
            {
                "manifest_supersession_preflight_status": "carried_forward_unperformed",
                "manifest_supersession_performed": False,
                "manifest_supersession_authorized_now": False,
                "active_manifest_registry_updated": False,
            },
        ),
        "sidecar_activation_blocker": _record(
            "sidecar_activation_blocker",
            {
                "sidecar_activation_blocker_status": "active",
                "string4_sidecar_status": "scaffolded_inactive",
                "string4_sidecar_active": False,
                "string4_sidecar_planning_ingestion_activated": False,
                "activation_authorized_now": False,
            },
        ),
        "future_impact": _record(
            "future_impact",
            {
                "future_dry_run_planning_impact_status": "blocked_pending_future_review",
                "stage5bd_run_plan_id_count": run_plan_count,
                "dry_run_ingestion_authorized_now": False,
                "future_token_block_execution_remains_blocked": True,
            },
        ),
        "dwh": _record(
            "dwh",
            {
                "dwh_quarantine_reaffirmation_status": "reaffirmed",
                "dwh_hash_search_performed": False,
                "hash_preimage_search_performed": False,
                "string4_execution_input_allowed": False,
            },
        ),
        "source_gap": _record(
            "source_gap",
            {
                "source_gap_severity_status": "warnings_preserved",
                "source_gap_updates": [
                    "public_github_issue_ci_external_or_unavailable",
                    "attached_zip_not_pristine_checkout",
                    "active_planning_input_scaffold_minimalist_closed_by_template_hardening",
                ],
                "gate_opener": False,
            },
        ),
        "guardrail": _record(
            "guardrail",
            {
                "guardrail_status": "active",
                "future_token_block_execution_remains_blocked": True,
                "approval_gate_satisfied_now": False,
                "activation_authorized_now": False,
                "string4_active_input_allowed": False,
                "string4_dry_run_ingestion_allowed_now": False,
            },
        ),
        "handoff": _record(
            "handoff",
            {
                "canonical_codex_handoff_root": "codex-output",
                "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
                "codex_output_used": False,
                "codex_completion_summary_committed": False,
            },
        ),
        "review_packaging_warning": _record(
            "review_packaging_warning",
            {
                "review_packaging_warning_status": "active",
                "raw_review_pack_committed": False,
                "raw_deep_research_body_committed": False,
                "packaging_dirt_authorizes_activation": False,
                "compact_metadata_only": True,
            },
        ),
        "next_stage": _record(
            "next_stage",
            {
                "selected_next_stage_id": "stage-5cj",
                "selected_next_stage_title": (
                    "Stage 5CJ - Deep Research review of Stage 5CI operator/Deep "
                    "Research approval-record template hardening and activation-decision "
                    "validation preflight, without execution"
                ),
                "selected_next_prompt_type": "deep_research_review",
                "selected_next_stage_authorizes_execution": False,
                "selected_next_stage_reason": (
                    "Stage 5CI hardens future approval and activation-decision templates; "
                    "independent review is required before any approval-record or "
                    "activation-capable stage."
                ),
            },
        ),
    }

    summary_body = {
        "status": "complete",
        "stage5ch_findings_integrated": True,
        "stage5ch_verdict": "accept_with_warnings",
        "stage5cg_status_preserved": True,
        "stage5cg_operator_approval_scaffold_preserved": True,
        "stage5cg_deep_research_acceptance_scaffold_preserved": True,
        "stage5cg_combined_approval_gate_scaffold_preserved": True,
        "stage5cg_active_planning_input_decision_scaffold_preserved": True,
        "stage5cg_approval_gate_satisfied_now": False,
        "stage5cg_activation_authorized_now": False,
        "operator_approval_record_template_hardened": True,
        "operator_approval_record_created_now": False,
        "operator_approval_record_present_now": False,
        "operator_approval_satisfied_now": False,
        "operator_approval_authorizes_activation_now": False,
        "deep_research_acceptance_record_template_hardened": True,
        "deep_research_activation_accept_record_created_now": False,
        "deep_research_activation_accept_record_present_now": False,
        "deep_research_activation_accept_satisfied_now": False,
        "deep_research_acceptance_authorizes_activation_now": False,
        "combined_approval_gate_validation_hardened": True,
        "combined_approval_gate_satisfied_now": False,
        "combined_approval_gate_authorizes_activation_now": False,
        "approval_gate_satisfied_now": False,
        "approval_gate_authorizes_activation_now": False,
        "active_planning_input_activation_decision_template_hardened": True,
        "active_planning_input_decision_record_created_now": False,
        "activation_decision_valid_now": False,
        "activation_authorized_now": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        "new_active_planning_input_created": False,
        "stage5ce_proposal_package_status_preserved": "review_package_only",
        "stage5cc_exact_citation_contract_preserved": True,
        "stage5cc_fail_closed_trigger_exact_set_preserved": True,
        "stage5cc_activation_precondition_exact_set_preserved": True,
        "no_byte_stream_transition_gate_status": "closed",
        "no_execution_transition_gate_status": "closed",
        "manifest_supersession_performed": False,
        "manifest_supersession_authorized_now": False,
        "stage5bd_dry_run_records_remain_valid": True,
        "stage5bd_run_plan_id_count": run_plan_count,
        "stage5bd_run_plan_ids_changed": False,
        "stage5bd_dry_run_plan_manifest_changed": False,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        "string4_sidecar_status": "scaffolded_inactive",
        "string4_sidecar_active": False,
        "string4_sidecar_planning_ingestion_activated": False,
        "string4_active_input_allowed": False,
        "string4_dry_run_ingestion_allowed_now": False,
        "string4_byte_stream_generation_allowed": False,
        "string4_execution_input_allowed": False,
        "future_token_block_execution_remains_blocked": True,
        "source_digest_record_count": len(source_records),
        "source_digest_unique_path_count": source_unique_count,
        "stage5cg_source_digest_record_count_preserved": int(
            stage5cg_summary.get("source_digest_record_count", 0)
        ),
        "operator_template_required_field_count": len(OPERATOR_TEMPLATE_REQUIRED_FIELDS),
        "deep_research_template_required_field_count": len(DEEP_RESEARCH_TEMPLATE_REQUIRED_FIELDS),
        "activation_template_required_field_count": len(ACTIVATION_DECISION_TEMPLATE_REQUIRED_FIELDS),
        "negative_failure_class_count": len(NEGATIVE_FAILURE_CLASSES),
        "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
        "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
        "recommended_next_stage_id": "stage-5cj",
        "recommended_next_stage_title": records["next_stage"]["selected_next_stage_title"],
    }
    summary_body.update(FALSE_FLAGS)
    records["summary"] = _record("summary", summary_body, include_false_flags=False)
    return records


def build_stage5ci(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    """Build Stage 5CI committed metadata and ignored summary reports."""

    _write_schemas()
    results_dir.mkdir(parents=True, exist_ok=True)
    source_records = [_sha_record(Path(path), role="stage5ci_reviewable_source") for path in _source_paths()]
    records = _build_records(source_records)
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    write_json(results_dir / "summary.json", records["summary"])
    write_json(
        results_dir / "approval_template_report.json",
        {
            "operator_template": records["operator_template"],
            "deep_research_template": records["deep_research_template"],
        },
    )
    write_json(results_dir / "activation_decision_template.json", records["activation_template"])
    write_json(results_dir / "combined_gate_validation.json", records["combined_gate"])
    write_json(results_dir / "negative_validation_contract.json", records["negative_contract"])
    write_json(results_dir / "source_digest_index.json", records["source_digest_index"])
    (results_dir / "warnings.jsonl").write_text("", encoding="utf-8")
    return records["summary"]


def _load_schema(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


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


def _check_false_flags(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for record_key, payload in payloads.items():
        for key, expected in FALSE_FLAGS.items():
            if payload.get(key) not in (expected, None):
                errors.append(f"{record_key} {key} must be {str(expected).lower()}")


def _check_required_fields(
    payload: dict[str, Any],
    expected: list[str],
    field_name: str,
    errors: list[str],
) -> None:
    observed = [str(item) for item in payload.get(field_name, [])]
    missing = sorted(set(expected) - set(observed))
    if missing:
        errors.extend(f"missing_required_template_field={field}" for field in missing)


def validate_stage5ci_operator_approval_template(
    *, operator_template: Path = DATA_PATHS["operator_template"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(operator_template, errors)
    if payload.get("template_only") is not True:
        errors.append("operator template must be template_only")
    if payload.get("actual_operator_approval_record") is not False:
        errors.append("operator template must not be an actual approval record")
    if payload.get("operator_approval_record_template_hardened") is not True:
        errors.append("operator approval record template must be hardened")
    _check_required_fields(payload, OPERATOR_TEMPLATE_REQUIRED_FIELDS, "template_required_fields", errors)
    for field in (
        "operator_approval_record_created_now",
        "operator_approval_record_present_now",
        "operator_approval_satisfied_now",
        "operator_approval_authorizes_activation_now",
        "approval_gate_satisfied_now",
        "activation_authorized_now",
        "template_misread_as_approval",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5ci_operator_approval_template_valid": not errors,
        "operator_approval_record_template_hardened": payload.get(
            "operator_approval_record_template_hardened"
        ),
        "operator_approval_record_present_now": payload.get("operator_approval_record_present_now"),
        "operator_approval_satisfied_now": payload.get("operator_approval_satisfied_now"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5ci_deep_research_acceptance_template(
    *, deep_research_template: Path = DATA_PATHS["deep_research_template"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(deep_research_template, errors)
    if payload.get("template_only") is not True:
        errors.append("Deep Research template must be template_only")
    if payload.get("actual_deep_research_acceptance_record") is not False:
        errors.append("Deep Research template must not be an actual acceptance record")
    if payload.get("deep_research_acceptance_record_template_hardened") is not True:
        errors.append("Deep Research acceptance template must be hardened")
    _check_required_fields(
        payload,
        DEEP_RESEARCH_TEMPLATE_REQUIRED_FIELDS,
        "template_required_fields",
        errors,
    )
    for field in (
        "deep_research_activation_accept_record_created_now",
        "deep_research_activation_accept_record_present_now",
        "deep_research_activation_accept_satisfied_now",
        "deep_research_acceptance_authorizes_activation_now",
        "approval_gate_satisfied_now",
        "activation_authorized_now",
        "template_misread_as_approval",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5ci_deep_research_acceptance_template_valid": not errors,
        "deep_research_acceptance_record_template_hardened": payload.get(
            "deep_research_acceptance_record_template_hardened"
        ),
        "deep_research_activation_accept_record_present_now": payload.get(
            "deep_research_activation_accept_record_present_now"
        ),
        "deep_research_activation_accept_satisfied_now": payload.get(
            "deep_research_activation_accept_satisfied_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5ci_combined_approval_gate(
    *, combined_gate: Path = DATA_PATHS["combined_gate"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(combined_gate, errors)
    if payload.get("combined_approval_gate_validation_hardened") is not True:
        errors.append("combined approval gate validation must be hardened")
    if payload.get("operator_approval_required") is not True:
        errors.append("operator approval must be required")
    if payload.get("deep_research_acceptance_required") is not True:
        errors.append("Deep Research acceptance must be required")
    required_types = set(payload.get("required_approval_record_types", []))
    for item in (
        "future_operator_approval_record",
        "future_deep_research_activation_acceptance_record",
    ):
        if item not in required_types:
            errors.append(f"missing_required_approval_record_type={item}")
    for field in (
        "operator_approval_record_present_now",
        "deep_research_activation_accept_record_present_now",
        "combined_approval_gate_satisfied_now",
        "combined_approval_gate_authorizes_activation_now",
        "approval_gate_satisfied_now",
        "approval_gate_authorizes_activation_now",
        "activation_authorized_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5ci_combined_approval_gate_valid": not errors,
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "approval_gate_satisfied_now": payload.get("approval_gate_satisfied_now"),
        "approval_gate_authorizes_activation_now": payload.get(
            "approval_gate_authorizes_activation_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5ci_activation_decision_template(
    *, activation_template: Path = DATA_PATHS["activation_template"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(activation_template, errors)
    if payload.get("template_only") is not True:
        errors.append("activation decision template must be template_only")
    if payload.get("active_planning_input_activation_decision_template_hardened") is not True:
        errors.append("activation decision template must be hardened")
    _check_required_fields(
        payload,
        ACTIVATION_DECISION_TEMPLATE_REQUIRED_FIELDS,
        "template_required_fields",
        errors,
    )
    for required in (
        "requires_exact_references_to_stage5ce_and_stage5cg_metadata",
        "requires_no_byte_and_no_execution_acknowledgements",
        "requires_stage5bd_preservation_or_explicit_future_supersession",
        "requires_active_lineage_preservation_or_explicit_future_supersession",
    ):
        if payload.get(required) is not True:
            errors.append(f"{required} must be true")
    for field in (
        "active_planning_input_decision_record_created_now",
        "activation_decision_valid_now",
        "activation_authorized_now",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
        "new_active_planning_input_created",
        "string4_active_input_allowed",
        "string4_dry_run_ingestion_allowed_now",
        "byte_stream_generation_authorized_now",
        "execution_authorized_now",
        "manifest_supersession_authorized_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5ci_activation_decision_template_valid": not errors,
        "active_planning_input_activation_decision_template_hardened": payload.get(
            "active_planning_input_activation_decision_template_hardened"
        ),
        "activation_decision_valid_now": payload.get("activation_decision_valid_now"),
        "active_planning_input_authorized_now": payload.get(
            "active_planning_input_authorized_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5ci_negative_validation_contract(
    *, negative_contract: Path = DATA_PATHS["negative_contract"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(negative_contract, errors)
    failure_classes = [str(item) for item in payload.get("failure_classes", [])]
    missing = sorted(set(NEGATIVE_FAILURE_CLASSES) - set(failure_classes))
    errors.extend(f"missing_failure_class={item}" for item in missing)
    if payload.get("synthetic_negative_fixtures_only") is not True:
        errors.append("negative validation must use synthetic fixtures only")
    if payload.get("real_approval_records_created") is not False:
        errors.append("negative validation must not create real approval records")
    return {
        "stage5ci_negative_validation_contract_valid": not errors,
        "failure_class_count": len(failure_classes),
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


def validate_stage5ci_sidecar_gates(
    *,
    no_active_ingestion: Path = DATA_PATHS["no_active_ingestion"],
    no_byte_stream_transition_gate: Path = DATA_PATHS["no_byte_stream_transition_gate"],
    no_execution_transition_gate: Path = DATA_PATHS["no_execution_transition_gate"],
    sidecar_activation_blocker: Path = DATA_PATHS["sidecar_activation_blocker"],
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {
        "no_active_ingestion": _validate_payload(no_active_ingestion, errors),
        "no_byte_stream_transition_gate": _validate_payload(no_byte_stream_transition_gate, errors),
        "no_execution_transition_gate": _validate_payload(no_execution_transition_gate, errors),
        "sidecar_activation_blocker": _validate_payload(sidecar_activation_blocker, errors),
    }
    _validate_sidecar_payloads(payloads, errors)
    if payloads["no_byte_stream_transition_gate"].get("no_byte_stream_transition_gate_status") != "closed":
        errors.append("no-byte-stream transition gate must be closed")
    if payloads["no_execution_transition_gate"].get("no_execution_transition_gate_status") != "closed":
        errors.append("no-execution transition gate must be closed")
    return {
        "stage5ci_sidecar_gates_valid": not errors,
        "string4_sidecar_status": payloads["no_active_ingestion"].get("string4_sidecar_status"),
        "no_byte_stream_transition_gate_status": payloads["no_byte_stream_transition_gate"].get(
            "no_byte_stream_transition_gate_status"
        ),
        "no_execution_transition_gate_status": payloads["no_execution_transition_gate"].get(
            "no_execution_transition_gate_status"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5ci(
    *,
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    active_lineage: Path = DATA_PATHS["active_lineage"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {key: _validate_payload(path, errors) for key, path in DATA_PATHS.items()}
    _check_false_flags(payloads, errors)
    _validate_sidecar_payloads(payloads, errors)

    summary_payload = (
        payloads["summary"] if summary == DATA_PATHS["summary"] else _validate_payload(summary, errors)
    )
    next_payload = (
        payloads["next_stage"]
        if next_stage_decision == DATA_PATHS["next_stage"]
        else _validate_payload(next_stage_decision, errors)
    )
    guardrail_payload = (
        payloads["guardrail"] if guardrail == DATA_PATHS["guardrail"] else _validate_payload(guardrail, errors)
    )
    if active_lineage != DATA_PATHS["active_lineage"]:
        payloads["active_lineage"] = _validate_payload(active_lineage, errors)

    for _counts, focused_errors in (
        validate_stage5ci_operator_approval_template(),
        validate_stage5ci_deep_research_acceptance_template(),
        validate_stage5ci_combined_approval_gate(),
        validate_stage5ci_activation_decision_template(),
        validate_stage5ci_negative_validation_contract(),
        validate_stage5ci_sidecar_gates(),
    ):
        errors.extend(focused_errors)

    _, stage5cg_errors = validate_stage5cg(results_dir=STAGE5CG_RESULTS_DIR)
    errors.extend(f"stage5cg_preservation:{error}" for error in stage5cg_errors)
    _, stage5ce_errors = validate_stage5ce(results_dir=STAGE5CE_RESULTS_DIR)
    errors.extend(f"stage5ce_preservation:{error}" for error in stage5ce_errors)
    _, stage5ca_errors = validate_stage5ca_citation_contract()
    errors.extend(f"stage5ca_citation:{error}" for error in stage5ca_errors)
    _, trigger_errors = validate_stage5cc_fail_closed_triggers()
    errors.extend(f"stage5cc_triggers:{error}" for error in trigger_errors)
    _, precondition_errors = validate_stage5cc_activation_preconditions()
    errors.extend(f"stage5cc_preconditions:{error}" for error in precondition_errors)
    _, stage5cc_errors = validate_stage5cc()
    errors.extend(f"stage5cc:{error}" for error in stage5cc_errors)

    if summary_payload.get("stage5ch_verdict") != "accept_with_warnings":
        errors.append("Stage 5CH verdict must be accept_with_warnings")
    for key in (
        "operator_approval_record_template_hardened",
        "deep_research_acceptance_record_template_hardened",
        "combined_approval_gate_validation_hardened",
        "active_planning_input_activation_decision_template_hardened",
    ):
        if summary_payload.get(key) is not True:
            errors.append(f"summary {key} must be true")
    if summary_payload.get("stage5ce_proposal_package_status_preserved") != "review_package_only":
        errors.append("Stage 5CE proposal package must remain review_package_only")
    if summary_payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    if summary_payload.get("active_lineage_record_count") != 8:
        errors.append("active-lineage record count must remain 8")
    if next_payload.get("selected_next_stage_id") != "stage-5cj":
        errors.append("Stage 5CI must select Stage 5CJ as next stage")
    if next_payload.get("selected_next_stage_authorizes_execution") is not False:
        errors.append("Stage 5CJ must not authorize execution")
    if guardrail_payload.get("future_token_block_execution_remains_blocked") is not True:
        errors.append("future token-block execution must remain blocked")

    digest_paths = [record.get("path") for record in payloads["source_digest_index"].get("source_records", [])]
    duplicate_paths = [path for path, count in Counter(digest_paths).items() if count > 1]
    errors.extend(f"stage5ci_duplicate_source_digest_path={path}" for path in duplicate_paths)

    gap_ids = {gap.get("gap_id") for gap in payloads["gap_register"].get("gaps", [])}
    for required_gap in {
        "public_github_issue_ci_external_or_unavailable",
        "attached_zip_not_pristine_checkout",
        "active_planning_input_scaffold_minimalist",
        "final_commit_self_embedding",
    }:
        if required_gap not in gap_ids:
            errors.append(f"missing_reviewability_gap={required_gap}")

    lineage_paths = [record.get("path") for record in payloads["active_lineage"].get("lineage_records", [])]
    if CORRECT_STAGE5AW_PATH not in lineage_paths:
        errors.append("correct Stage 5AW repaired path must be present in active lineage")
    if INCORRECT_STAGE5AW_PATH in lineage_paths:
        errors.append("deprecated Stage 5AW path must be absent from active lineage")
    if len(lineage_paths) != 8:
        errors.append("active lineage must contain exactly 8 records")
    if payloads["handoff"].get("canonical_codex_handoff_root") != "codex-output":
        errors.append("Stage 5CI must use codex-output as handoff root")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output directory must be absent/unused")

    generated_summary_present = (results_dir / "summary.json").is_file()
    return {
        "stage5ci_valid": not errors,
        "validation_error_count": len(errors),
        "stage5ch_verdict": summary_payload.get("stage5ch_verdict"),
        "operator_approval_record_template_hardened": summary_payload.get(
            "operator_approval_record_template_hardened"
        ),
        "deep_research_acceptance_record_template_hardened": summary_payload.get(
            "deep_research_acceptance_record_template_hardened"
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
        "generated_summary_present": generated_summary_present,
        "recommended_next_stage_id": next_payload.get("selected_next_stage_id"),
    }, errors


def load_stage5ci_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    """Load the Stage 5CI summary."""

    return _read(summary)
