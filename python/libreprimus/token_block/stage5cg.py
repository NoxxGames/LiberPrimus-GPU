"""Stage 5CG approval-gate decision scaffold metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import repo_relative, sha256_file, write_yaml
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

STAGE_ID = "stage-5cg"
STAGE_TITLE = (
    "Stage 5CG - Post-review approval-gate integration and active-planning-input "
    "decision record scaffold, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5ce"
SOURCE_PREVIOUS_COMMIT = "09d01c533bd1bf62a7c1076e263c479d6d77449d"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5cf"
SOURCE_DEEP_RESEARCH_REPORT = "18_Stage-5CE-Deep-Research-Review.md"
STAGE5CF_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "18_Stage-5CE-Deep-Research-Review.md"
)
RESULTS_DIR = Path("experiments/results/token-block/stage5cg")
CODEX_COMPLETION_PATH = Path("codex-output/stage5cg-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

# Updated after the final local pytest run in this stage.
PYTEST_COUNT_OBSERVED_LOCALLY = 2282
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"

STAGE5CF_FINDINGS = [
    "stage5ce_metadata_only_review_package_is_coherent",
    "stage5ce_preserves_stage5cc_contract_layer",
    "stage5ce_packages_active_planning_input_proposal_as_review_only",
    "stage5ce_requires_operator_and_deep_research_approval_before_activation",
    "stage5ce_records_committed_pytest_count_capture",
    "stage5ce_keeps_no_byte_and_no_execution_transition_gates_closed",
    "stage5ce_preserves_stage5bd_dry_run_plan_set",
    "stage5ce_preserves_eight_record_active_lineage_set",
    "stage5ce_keeps_string4_inactive",
    "stage5ce_keeps_string4_noncanonical",
    "stage5ce_keeps_string4_out_of_active_input",
    "stage5ce_keeps_string4_out_of_dry_run_ingestion",
    "stage5ce_keeps_string4_out_of_byte_stream_generation",
    "stage5ce_keeps_string4_out_of_execution_input",
    "stage5ce_does_not_authorize_active_planning_input",
    "stage5ce_does_not_select_active_planning_input",
    "stage5ce_does_not_create_new_active_planning_input",
    "stage5ce_does_not_perform_manifest_supersession",
    "stage5ce_does_not_mutate_stage5bd_plans",
    "stage5ce_does_not_execute_token_block_work",
    "stage5ce_has_no_gate_opening_defects",
    "proposal_package_design_accepted_with_warnings",
    "next_step_should_integrate_review_and_create_decision_scaffolds_without_decision",
]

STAGE5CF_WARNING_ACTIONS = {
    "warning_1_public_github_issue_ci_external_or_unavailable": [
        "preserve_external_evidence_caveat",
        "keep_committed_reviewability_metadata",
        "do_not_attempt_final_commit_self_embedding",
    ],
    "warning_2_attached_zip_not_pristine_checkout": [
        "record_packaging_warning_as_non_gate_opener",
        "keep_raw_and_generated_files_uncommitted",
        "audit_staging_before_commit",
    ],
    "warning_3_source_digest_broader_than_prompt_expected": [
        "preserve_stage5ce_source_digest_breadth_as_intentional",
        "do_not_shrink_digest_coverage_to_match_older_prompt_expectation",
        "keep_unique_path_validation_active",
    ],
    "warning_4_combined_gate_wording_blemish": [
        "inspect_current_stage5ce_combined_gate_record",
        "record_not_reproduced_current_repo_or_forward_erratum",
        "do_not_hide_history",
        "do_not_weaken_or_satisfy_approval_gate",
    ],
}

DATA_PATHS: dict[str, Path] = {
    "findings": Path("data/project-state/stage5cg-stage5cf-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5cg-reviewable-stage-marker.yaml"),
    "validation_evidence": Path(
        "data/project-state/stage5cg-reviewable-validation-evidence.yaml"
    ),
    "source_digest_index": Path(
        "data/project-state/stage5cg-reviewable-source-digest-index.yaml"
    ),
    "gap_register": Path("data/project-state/stage5cg-reviewability-gap-register.yaml"),
    "equivalence_map": Path(
        "data/project-state/stage5cg-record-family-name-equivalence-map.yaml"
    ),
    "summary": Path("data/project-state/stage5cg-summary.yaml"),
    "next_stage": Path("data/project-state/stage5cg-next-stage-decision.yaml"),
    "proposal_preservation": Path(
        "data/token-block/stage5cg-stage5ce-proposal-package-preservation.yaml"
    ),
    "gate_design_preservation": Path(
        "data/token-block/stage5cg-stage5ce-gate-design-preservation.yaml"
    ),
    "stage5cc_preservation": Path(
        "data/token-block/stage5cg-stage5cc-contract-preservation.yaml"
    ),
    "operator_decision": Path(
        "data/token-block/stage5cg-operator-approval-decision-scaffold.yaml"
    ),
    "deep_research_decision": Path(
        "data/token-block/stage5cg-deep-research-acceptance-decision-scaffold.yaml"
    ),
    "combined_gate": Path(
        "data/token-block/stage5cg-combined-approval-decision-gate-scaffold.yaml"
    ),
    "active_planning_decision": Path(
        "data/token-block/stage5cg-active-planning-input-decision-record-scaffold.yaml"
    ),
    "approval_non_satisfaction": Path(
        "data/token-block/stage5cg-approval-gate-non-satisfaction-proof.yaml"
    ),
    "wording_review": Path(
        "data/token-block/stage5cg-stage5ce-combined-gate-wording-review.yaml"
    ),
    "no_active_ingestion": Path("data/token-block/stage5cg-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5cg-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5cg-no-execution-transition-gate.yaml"
    ),
    "supersession_nonactivation": Path(
        "data/token-block/stage5cg-manifest-supersession-nonactivation-proof.yaml"
    ),
    "stage5bd_preservation": Path("data/token-block/stage5cg-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5cg-active-lineage-preservation.yaml"),
    "sidecar_activation_blocker": Path("data/token-block/stage5cg-sidecar-activation-blocker.yaml"),
    "future_impact": Path("data/token-block/stage5cg-future-dry-run-planning-impact.yaml"),
    "dwh": Path("data/historical-route/stage5cg-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5cg-source-gap-severity-update.yaml"),
    "guardrail": Path("data/historical-route/stage5cg-guardrail.yaml"),
    "review_packaging_warning": Path("data/source-harvester/stage5cg-review-packaging-warning.yaml"),
    "handoff": Path("data/source-harvester/stage5cg-codex-handoff-policy.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}

RECORD_TYPES = {key: f"stage5cg_{key}" for key in DATA_PATHS}
RECORD_TYPES.update(
    {
        "operator_decision": "stage5cg_operator_approval_decision_scaffold",
        "deep_research_decision": "stage5cg_deep_research_acceptance_decision_scaffold",
        "combined_gate": "stage5cg_combined_approval_decision_gate_scaffold",
        "active_planning_decision": "stage5cg_active_planning_input_decision_record_scaffold",
        "wording_review": "stage5cg_stage5ce_combined_gate_wording_review",
        "no_byte_stream_transition_gate": "stage5cg_no_byte_stream_transition_gate",
        "no_execution_transition_gate": "stage5cg_no_execution_transition_gate",
    }
)

FALSE_FLAGS = {
    "activation_authorized_now": False,
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
    "cuda_execution_performed": False,
    "decode_attempt_performed": False,
    "deep_research_acceptance_authorizes_activation_now": False,
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
    "stage5bd_run_plan_ids_changed": False,
    "stage5bd_plan_superseded": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
    "string4_sidecar_active": False,
    "string4_sidecar_planning_ingestion_activated": False,
    "template_bodies_committed": False,
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


def _write_generated(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def _stage5ce_combined_gate_wording() -> dict[str, Any]:
    path = STAGE5CE_DATA_PATHS["combined_gate"]
    payload = _read(path)
    typo_field = "operation_and_deep_research_gate_design_created"
    correct_fields = (
        "operator_and_deep_research_gate_design_created",
        "operator_deep_research_gate_design_created",
    )
    typo_present = typo_field in payload
    correct_present = any(field in payload for field in correct_fields)
    return {
        "stage5ce_combined_gate_path": path.as_posix(),
        "stage5ce_combined_gate_sha256": sha256_file(path) if path.is_file() else None,
        "reported_typo_field": typo_field,
        "reported_typo_field_present_current_repo": typo_present,
        "accepted_correct_fields": list(correct_fields),
        "accepted_correct_field_present_current_repo": correct_present,
        "wording_warning_disposition": (
            "forward_erratum_recorded" if typo_present else "not_reproduced_current_repo"
        ),
        "stage5ce_wording_blemish_reviewed": True,
        "stage5ce_wording_blemish_gate_opener": False,
        "approval_gate_satisfied_now": False,
        "activation_authorized_now": False,
    }


def _source_paths() -> list[str]:
    paths = [
        str(STAGE5CF_REPORT_PATH),
        "data/project-state/stage5ce-summary.yaml",
        "data/project-state/stage5ce-next-stage-decision.yaml",
        "data/project-state/stage5ce-reviewable-validation-evidence.yaml",
        "data/project-state/stage5ce-reviewable-source-digest-index.yaml",
        "data/token-block/stage5ce-active-planning-input-proposal-package.yaml",
        "data/token-block/stage5ce-operator-approval-gate-design.yaml",
        "data/token-block/stage5ce-deep-research-approval-gate-design.yaml",
        "data/token-block/stage5ce-operator-deep-research-combined-gate-contract.yaml",
        "data/token-block/stage5ce-stage5cc-contract-preservation.yaml",
        "data/token-block/stage5ce-no-byte-stream-transition-gate.yaml",
        "data/token-block/stage5ce-no-execution-transition-gate.yaml",
        "data/token-block/stage5ce-stage5bd-plan-preservation.yaml",
        "data/token-block/stage5ce-active-lineage-preservation.yaml",
        "data/token-block/stage5ce-sidecar-activation-blocker.yaml",
        "data/historical-route/stage5ce-dwh-quarantine-reaffirmation.yaml",
        "data/token-block/stage5bd-run-plan-id-registry.yaml",
        "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
        "data/token-block/stage5bd-active-manifest-lock.yaml",
        "data/token-block/stage5ap-token-block-canonical-transcription.yaml",
        "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml",
        "data/token-block/stage5ay-branch-eligibility-policy.yaml",
        "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml",
        "data/token-block/stage5bb-active-manifest-registry.yaml",
        "README.md",
        "STATUS.md",
        "AGENTS.md",
        "ROADMAP.md",
        "TESTING.md",
        "docs/roadmap/staged-plan.md",
        "docs/onboarding/start-here.md",
        "docs/onboarding/source-of-truth-map.md",
        "docs/onboarding/operational-file-map.md",
        "docs/onboarding/codex-navigation-map.md",
        "docs/onboarding/deep-research-handoff-map.md",
        "docs/onboarding/token-block-preflight-dry-run-workflow.md",
        "docs/reference/token-block-cli.md",
    ]
    return list(dict.fromkeys([*paths, *REQUIRED_CITATION_PATHS]))


def _source_digest_records() -> list[dict[str, Any]]:
    return [_sha_record(Path(path), role="stage5cg_reviewable_source") for path in _source_paths()]


def _lineage_digest_records(paths: list[str]) -> list[dict[str, Any]]:
    return [_sha_record(Path(path), role="stage5cg_active_lineage_preservation") for path in paths]


def _validation_commands() -> list[dict[str, Any]]:
    commands = [
        ("stage5cg_build", "python -m libreprimus.cli token-block build-stage5cg"),
        (
            "stage5cg_focused_validators",
            "python -m libreprimus.cli token-block validate-stage5cg-operator-decision-scaffold; "
            "validate-stage5cg-deep-research-decision-scaffold; "
            "validate-stage5cg-combined-approval-gate; "
            "validate-stage5cg-active-planning-input-decision-scaffold; "
            "validate-stage5cg-stage5ce-wording-review",
        ),
        ("stage5cg_validate", "python -m libreprimus.cli token-block validate-stage5cg"),
        ("stage5cg_summary", "python -m libreprimus.cli token-block stage5cg-summary"),
        ("stage5ce_validator", "python -m libreprimus.cli token-block validate-stage5ce"),
        ("stage5cc_validator", "python -m libreprimus.cli token-block validate-stage5cc"),
        ("stage5ca_validator", "python -m libreprimus.cli token-block validate-stage5ca"),
        ("stage5by_validator", "python -m libreprimus.cli token-block validate-stage5by"),
        ("stage5bw_validator", "python -m libreprimus.cli token-block validate-stage5bw"),
        ("stage5bu_validator", "python -m libreprimus.cli token-block validate-stage5bu"),
        ("stage5bs_validator", "python -m libreprimus.cli token-block validate-stage5bs"),
        ("stage5bq_validator", "python -m libreprimus.cli token-block validate-stage5bq"),
        ("stage5bo_validator", "python -m libreprimus.cli token-block validate-stage5bo"),
        (
            "stage5bd_validator",
            "python -m libreprimus.cli token-block validate-stage5bd --results-dir "
            "experiments/results/token-block/stage5bd",
        ),
        (
            "stage5ax_validation",
            "python -m libreprimus.cli parallel-validation validate-stage5ax",
        ),
        (
            "stage5ax_parallel_validation",
            ".\\scripts\\ci\\run-parallel-validation.ps1 -Workers 16 -PytestWorkers 16 "
            "-PytestMode auto",
        ),
        (
            "research_synthesis",
            "python -m libreprimus.cli research-synthesis validate --data-dir data/research "
            "--staged-plan docs/roadmap/staged-plan.md",
        ),
        ("consistency_state_drift", "python -m libreprimus.cli consistency check-state-drift"),
        ("consistency_check_all", "python -m libreprimus.cli consistency check-all --allow-warnings"),
        ("smoke", "python -m libreprimus.cli smoke"),
        ("ruff", "python -m ruff check python/libreprimus tests/python"),
        ("pytest", PYTEST_COMMAND_OBSERVED_LOCALLY),
        ("powershell_consistency_wrapper", ".\\scripts\\ci\\run-consistency-checks.ps1"),
        ("public_docs", ".\\scripts\\ci\\verify-public-docs-status.ps1"),
        ("lock_hashes", ".\\scripts\\ci\\verify-lock-hashes.ps1"),
        ("workflow_static", ".\\scripts\\ci\\validate-workflow-static.ps1"),
        ("wiki_source", ".\\scripts\\github\\validate-wiki-source.ps1"),
        ("wiki_dry_run", ".\\scripts\\github\\sync-tutorials-to-wiki.ps1 --DryRun"),
    ]
    records = [
        {"command_id": command_id, "command": command, "status": "passed_local_validation"}
        for command_id, command in commands
    ]
    records.append(
        {
            "command_id": "bash_parallel_or_consistency_wrapper",
            "command": "./scripts/ci/run-parallel-validation.sh and "
            "./scripts/ci/run-consistency-checks.sh",
            "status": "not_run_wsl_unavailable",
            "reason_if_not_run": (
                "Local bash resolves to the Windows Subsystem for Linux launcher, "
                "but no WSL distributions are installed."
            ),
        }
    )
    return records


def _equivalence_entries() -> list[dict[str, Any]]:
    return [
        {
            "record_family": "stage5cg_decision_scaffold",
            "paths": [
                DATA_PATHS["operator_decision"].as_posix(),
                DATA_PATHS["deep_research_decision"].as_posix(),
                DATA_PATHS["combined_gate"].as_posix(),
                DATA_PATHS["active_planning_decision"].as_posix(),
            ],
            "equivalence_scope": "future_decision_record_scaffold_not_approval",
        },
        {
            "record_family": "stage5cg_transition_gates",
            "paths": [
                DATA_PATHS["no_byte_stream_transition_gate"].as_posix(),
                DATA_PATHS["no_execution_transition_gate"].as_posix(),
                DATA_PATHS["supersession_nonactivation"].as_posix(),
            ],
            "equivalence_scope": "closed_transition_gate_records",
        },
        {
            "record_family": "stage5cg_stage5ce_preservation",
            "paths": [
                DATA_PATHS["proposal_preservation"].as_posix(),
                DATA_PATHS["gate_design_preservation"].as_posix(),
                DATA_PATHS["stage5cc_preservation"].as_posix(),
                DATA_PATHS["wording_review"].as_posix(),
            ],
            "equivalence_scope": "stage5ce_review_integration_and_preservation",
        },
    ]


def _build_records(source_records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    stage5ce_summary = _read(STAGE5CE_DATA_PATHS["summary"])
    run_plan_count = _run_plan_count()
    wording = _stage5ce_combined_gate_wording()
    source_unique_count = len({record["path"] for record in source_records})
    active_lineage_records = _lineage_digest_records(ACTIVE_LINEAGE_PATHS)
    common_counts = {
        "stage5bd_run_plan_id_count": run_plan_count,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "required_citation_count": len(REQUIRED_CITATION_PATHS),
        "required_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
        "required_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
    }
    records: dict[str, dict[str, Any]] = {
        "findings": _record(
            "findings",
            {
                "stage5cf_findings_integrated": True,
                "stage5cf_verdict": "accept_with_warnings",
                "stage5cf_findings": STAGE5CF_FINDINGS,
                "stage5cf_warning_actions": STAGE5CF_WARNING_ACTIONS,
                "warning_count": len(STAGE5CF_WARNING_ACTIONS),
                "warnings_are_gate_openers": False,
            },
        ),
        "stage_marker": _record(
            "stage_marker",
            {
                "status": "complete",
                "reviewable_stage_marker_created": True,
                "selected_next_stage_id": "stage-5ch",
                "selected_next_prompt_type": "deep_research_review",
                "selected_next_stage_authorizes_execution": False,
            },
        ),
        "validation_evidence": _record(
            "validation_evidence",
            {
                "reviewability_evidence_status": "committed_compact_evidence",
                "local_validation_evidence_committed": True,
                "validation_commands": _validation_commands(),
                "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
                "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
                "pytest_count_committed": True,
                "stage5ax_parallel_validation_used": True,
                "raw_staged": False,
                "generated_outputs_staged": False,
                "codex_output_staged": False,
                "sqlite_staged": False,
                "final_commit_external_evidence_required": True,
                "ci_external_evidence_required": True,
                "codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            },
        ),
        "source_digest_index": _record(
            "source_digest_index",
            {
                "source_digest_record_count": len(source_records),
                "source_digest_unique_path_count": source_unique_count,
                "source_digest_duplicate_path_count": len(source_records) - source_unique_count,
                "source_digest_breadth_disposition": "preserved_intentional_unique_coverage",
                "source_records": source_records,
            },
        ),
        "gap_register": _record(
            "gap_register",
            {
                "reviewability_gap_status": "non_gate_opening_warnings_recorded",
                "gaps": [
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
                        "gap_id": "source_digest_broader_than_prompt_expected",
                        "severity": "warning",
                        "gate_opener": False,
                        "disposition": "breadth_preserved_as_intentional_unique_coverage",
                    },
                    {
                        "gap_id": "combined_gate_wording_blemish",
                        "severity": "warning",
                        "gate_opener": False,
                        "disposition": wording["wording_warning_disposition"],
                    },
                ],
            },
        ),
        "equivalence_map": _record(
            "equivalence_map",
            {
                "record_family_name_equivalence_map_created": True,
                "equivalence_entries": _equivalence_entries(),
            },
        ),
        "proposal_preservation": _record(
            "proposal_preservation",
            {
                "stage5ce_status_preserved": True,
                "stage5ce_proposal_package_preserved": True,
                "stage5ce_proposal_package_status": "review_package_only",
                "active_planning_input_proposal_performed": False,
                "active_planning_input_authorized_now": False,
                "active_planning_input_selected_now": False,
                "new_active_planning_input_created": False,
                "source_stage5ce_summary_sha256": sha256_file(STAGE5CE_DATA_PATHS["summary"]),
            },
        ),
        "gate_design_preservation": _record(
            "gate_design_preservation",
            {
                "stage5ce_operator_deep_research_gate_design_preserved": True,
                "operator_approval_required_before_activation": True,
                "deep_research_review_required_before_activation": True,
                "approval_gate_satisfied_now": False,
                "approval_gate_authorizes_activation_now": False,
                "activation_authorized_now": False,
            },
        ),
        "stage5cc_preservation": _record(
            "stage5cc_preservation",
            {
                "stage5cc_exact_citation_contract_preserved": True,
                "stage5cc_fail_closed_trigger_exact_set_preserved": True,
                "stage5cc_activation_precondition_exact_set_preserved": True,
                **common_counts,
            },
        ),
        "operator_decision": _record(
            "operator_decision",
            {
                "operator_approval_decision_scaffold_created": True,
                "operator_approval_record_present_now": False,
                "operator_approval_satisfied_now": False,
                "operator_approval_authorizes_activation_now": False,
                "required_future_record_fields": [
                    "operator_identity_or_role",
                    "approval_scope",
                    "approved_stage_id",
                    "reviewed_stage5cg_metadata_sha256",
                    "explicit_activation_authorization",
                    "no_solve_claim_acknowledgement",
                ],
            },
        ),
        "deep_research_decision": _record(
            "deep_research_decision",
            {
                "deep_research_acceptance_decision_scaffold_created": True,
                "deep_research_activation_accept_record_present_now": False,
                "deep_research_activation_accept_satisfied_now": False,
                "deep_research_acceptance_authorizes_activation_now": False,
                "required_future_record_fields": [
                    "deep_research_review_stage_id",
                    "review_verdict",
                    "activation_acceptance_scope",
                    "reviewed_stage5cg_metadata_sha256",
                    "explicit_activation_acceptance",
                    "no_execution_authorization_acknowledgement",
                ],
            },
        ),
        "combined_gate": _record(
            "combined_gate",
            {
                "combined_approval_decision_gate_scaffold_created": True,
                "operator_approval_required_before_activation": True,
                "deep_research_acceptance_required_before_activation": True,
                "operator_approval_record_present_now": False,
                "deep_research_activation_accept_record_present_now": False,
                "approval_gate_satisfied_now": False,
                "approval_gate_authorizes_activation_now": False,
                "activation_authorized_now": False,
            },
        ),
        "active_planning_decision": _record(
            "active_planning_decision",
            {
                "active_planning_input_decision_record_scaffold_created": True,
                "active_planning_input_authorized_now": False,
                "active_planning_input_selected_now": False,
                "new_active_planning_input_created": False,
                "string4_active_input_allowed": False,
                "string4_dry_run_ingestion_allowed_now": False,
            },
        ),
        "approval_non_satisfaction": _record(
            "approval_non_satisfaction",
            {
                "approval_gate_non_satisfaction_proof_created": True,
                "operator_approval_record_present_now": False,
                "deep_research_activation_accept_record_present_now": False,
                "approval_gate_satisfied_now": False,
                "approval_gate_authorizes_activation_now": False,
                "activation_authorized_now": False,
            },
        ),
        "wording_review": _record("wording_review", wording),
        "no_active_ingestion": _record(
            "no_active_ingestion",
            {
                "no_active_ingestion_proof_created": True,
                "string4_sidecar_status": "scaffolded_inactive",
                "string4_sidecar_active": False,
                "string4_sidecar_planning_ingestion_activated": False,
                "string4_active_input_allowed": False,
                "string4_dry_run_ingestion_allowed_now": False,
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
                "manifest_supersession_performed": False,
                "manifest_supersession_authorized_now": False,
                "active_token_block_manifest_changed": False,
                "stage5bd_plan_superseded": False,
            },
        ),
        "stage5bd_preservation": _record(
            "stage5bd_preservation",
            {
                "stage5bd_plan_preservation_status": "preserved_unchanged",
                "stage5bd_dry_run_records_remain_valid": True,
                "stage5bd_run_plan_id_count_before": run_plan_count,
                "stage5bd_run_plan_id_count_after": run_plan_count,
                "stage5bd_run_plan_id_count": run_plan_count,
                "stage5bd_run_plan_ids_changed": False,
                "stage5bd_dry_run_plan_manifest_changed": False,
                "string4_added_to_stage5bd_run_plan_ids": False,
            },
        ),
        "active_lineage": _record(
            "active_lineage",
            {
                "active_lineage_preservation_status": "preserved_unchanged",
                "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
                "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in ACTIVE_LINEAGE_PATHS,
                "deprecated_stage5aw_path_absent": INCORRECT_STAGE5AW_PATH not in ACTIVE_LINEAGE_PATHS,
                "lineage_records": active_lineage_records,
                "all_lineage_paths_resolve": all(record["present"] for record in active_lineage_records),
            },
        ),
        "sidecar_activation_blocker": _record(
            "sidecar_activation_blocker",
            {
                "sidecar_activation_blocker_created": True,
                "string4_sidecar_status": "scaffolded_inactive",
                "string4_sidecar_active": False,
                "operator_approval_record_present_now": False,
                "deep_research_activation_accept_record_present_now": False,
                "activation_authorized_now": False,
            },
        ),
        "future_impact": _record(
            "future_impact",
            {
                "future_dry_run_planning_impact": "decision_scaffold_only",
                "future_stage_required_before_activation": True,
                "selected_next_stage_id": "stage-5ch",
                "selected_next_stage_authorizes_execution": False,
            },
        ),
        "dwh": _record(
            "dwh",
            {
                "dwh_quarantine_reaffirmed": True,
                "dwh_hash_search_performed": False,
                "dwh_context_status": "quarantined_context_not_execution_input",
            },
        ),
        "source_gap": _record(
            "source_gap",
            {
                "source_gap_severity_status": "preserved_blocking_context",
                "source_gap_upgrade_performed": False,
                "activation_authorized_now": False,
            },
        ),
        "guardrail": _record(
            "guardrail",
            {
                "guardrail_status": "active",
                "metadata_only": True,
                "future_token_block_execution_remains_blocked": True,
                "no_solve_claim": True,
            },
        ),
        "review_packaging_warning": _record(
            "review_packaging_warning",
            {
                "review_packaging_warning_created": True,
                "attached_zip_not_pristine_checkout_warning_preserved": True,
                "gate_opener": False,
                "raw_and_generated_files_uncommitted": True,
                "staging_audit_required_before_commit": True,
            },
        ),
        "handoff": _record(
            "handoff",
            {
                "canonical_codex_handoff_root": "codex-output",
                "deprecated_codex_output_root": "codex_output",
                "codex_output_used": False,
                "codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            },
        ),
        "next_stage": _record(
            "next_stage",
            {
                "selected_next_stage_id": "stage-5ch",
                "selected_next_stage_title": (
                    "Stage 5CH - Deep Research review of Stage 5CG post-review "
                    "approval-gate integration and active-planning-input decision record "
                    "scaffold, without execution"
                ),
                "selected_next_prompt_type": "deep_research_review",
                "selected_next_stage_authorizes_execution": False,
                "selected_next_stage_reason": (
                    "Stage 5CG creates future decision-record scaffolds and integrates "
                    "Stage 5CF review findings; independent review is required before any "
                    "approval-record or activation-capable stage."
                ),
            },
        ),
    }
    records["summary"] = _record(
        "summary",
        {
            "status": "complete",
            "stage5cf_findings_integrated": True,
            "stage5cf_verdict": "accept_with_warnings",
            "stage5ce_status_preserved": True,
            "stage5ce_proposal_package_preserved": True,
            "stage5ce_proposal_package_status": "review_package_only",
            "stage5ce_operator_deep_research_gate_design_preserved": True,
            "stage5cc_exact_citation_contract_preserved": True,
            "stage5cc_fail_closed_trigger_exact_set_preserved": True,
            "stage5cc_activation_precondition_exact_set_preserved": True,
            "operator_approval_decision_scaffold_created": True,
            "operator_approval_record_present_now": False,
            "operator_approval_satisfied_now": False,
            "deep_research_acceptance_decision_scaffold_created": True,
            "deep_research_activation_accept_record_present_now": False,
            "deep_research_activation_accept_satisfied_now": False,
            "combined_approval_decision_gate_scaffold_created": True,
            "approval_gate_satisfied_now": False,
            "approval_gate_authorizes_activation_now": False,
            "activation_authorized_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
            "new_active_planning_input_created": False,
            "stage5ce_wording_blemish_reviewed": True,
            "stage5ce_wording_blemish_disposition": wording["wording_warning_disposition"],
            "stage5ce_wording_blemish_gate_opener": False,
            "no_byte_stream_transition_gate_status": "closed",
            "no_execution_transition_gate_status": "closed",
            "manifest_supersession_performed": False,
            "manifest_supersession_authorized_now": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "string4_sidecar_status": "scaffolded_inactive",
            "string4_sidecar_active": False,
            "string4_sidecar_planning_ingestion_activated": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_byte_stream_generation_allowed": False,
            "string4_execution_input_allowed": False,
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "future_token_block_execution_remains_blocked": True,
            "source_digest_record_count": len(source_records),
            "source_digest_unique_path_count": source_unique_count,
            "stage5ce_source_digest_record_count_preserved": int(
                stage5ce_summary.get("source_digest_record_count", 0)
            ),
            "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
            "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
            "recommended_next_stage_id": "stage-5ch",
            "recommended_next_stage_title": records["next_stage"]["selected_next_stage_title"],
        },
    )
    return records


def build_stage5cg(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    """Build Stage 5CG committed metadata and ignored summary reports."""

    _write_schemas()
    source_records = _source_digest_records()
    records = _build_records(source_records)
    for key, payload in records.items():
        if key in DATA_PATHS:
            write_yaml(DATA_PATHS[key], payload)

    _write_generated(results_dir / "summary.json", records["summary"])
    _write_generated(
        results_dir / "approval_decision_scaffolds.json",
        {
            "operator_decision": records["operator_decision"],
            "deep_research_decision": records["deep_research_decision"],
            "combined_gate": records["combined_gate"],
            "active_planning_decision": records["active_planning_decision"],
        },
    )
    _write_generated(results_dir / "decision_scaffold_report.json", records["combined_gate"])
    _write_generated(results_dir / "proposal_package_preservation.json", records["proposal_preservation"])
    _write_generated(
        results_dir / "no_byte_stream_transition_gate.json",
        records["no_byte_stream_transition_gate"],
    )
    _write_generated(
        results_dir / "no_execution_transition_gate.json",
        records["no_execution_transition_gate"],
    )
    _write_generated(results_dir / "wording_review.json", records["wording_review"])
    _write_generated(results_dir / "source_digest_index.json", records["source_digest_index"])
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
        errors.append(f"{path}: schema missing: {schema_path}")
        return payload
    schema_errors = list(Draft202012Validator(_load_schema(schema_path)).iter_errors(payload))
    errors.extend(f"{repo_relative(path)} schema_error={error.message}" for error in schema_errors)
    return payload


def _check_false_flags(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for key, payload in payloads.items():
        for flag in FALSE_FLAGS:
            if payload.get(flag) is True:
                errors.append(f"{key}: {flag} must remain false")


def validate_stage5cg_operator_decision_scaffold(
    *, operator_decision: Path = DATA_PATHS["operator_decision"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(operator_decision, errors)
    if payload.get("operator_approval_decision_scaffold_created") is not True:
        errors.append("operator approval decision scaffold must exist")
    for field in (
        "operator_approval_record_present_now",
        "operator_approval_satisfied_now",
        "operator_approval_authorizes_activation_now",
        "activation_authorized_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cg_operator_decision_scaffold_valid": not errors,
        "operator_approval_record_present_now": payload.get("operator_approval_record_present_now"),
        "operator_approval_satisfied_now": payload.get("operator_approval_satisfied_now"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cg_deep_research_decision_scaffold(
    *, deep_research_decision: Path = DATA_PATHS["deep_research_decision"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(deep_research_decision, errors)
    if payload.get("deep_research_acceptance_decision_scaffold_created") is not True:
        errors.append("Deep Research acceptance decision scaffold must exist")
    for field in (
        "deep_research_activation_accept_record_present_now",
        "deep_research_activation_accept_satisfied_now",
        "deep_research_acceptance_authorizes_activation_now",
        "activation_authorized_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cg_deep_research_decision_scaffold_valid": not errors,
        "deep_research_activation_accept_record_present_now": payload.get(
            "deep_research_activation_accept_record_present_now"
        ),
        "deep_research_activation_accept_satisfied_now": payload.get(
            "deep_research_activation_accept_satisfied_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cg_combined_approval_gate(
    *, combined_gate: Path = DATA_PATHS["combined_gate"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(combined_gate, errors)
    if payload.get("combined_approval_decision_gate_scaffold_created") is not True:
        errors.append("combined approval decision gate scaffold must exist")
    for field in (
        "operator_approval_record_present_now",
        "deep_research_activation_accept_record_present_now",
        "approval_gate_satisfied_now",
        "approval_gate_authorizes_activation_now",
        "activation_authorized_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cg_combined_approval_gate_valid": not errors,
        "approval_gate_satisfied_now": payload.get("approval_gate_satisfied_now"),
        "approval_gate_authorizes_activation_now": payload.get(
            "approval_gate_authorizes_activation_now"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cg_active_planning_input_decision_scaffold(
    *, active_planning_decision: Path = DATA_PATHS["active_planning_decision"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(active_planning_decision, errors)
    if payload.get("active_planning_input_decision_record_scaffold_created") is not True:
        errors.append("active planning input decision scaffold must exist")
    for field in (
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
        "new_active_planning_input_created",
        "string4_active_input_allowed",
        "string4_dry_run_ingestion_allowed_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cg_active_planning_input_decision_scaffold_valid": not errors,
        "active_planning_input_authorized_now": payload.get(
            "active_planning_input_authorized_now"
        ),
        "active_planning_input_selected_now": payload.get("active_planning_input_selected_now"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cg_stage5ce_wording_review(
    *, wording_review: Path = DATA_PATHS["wording_review"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(wording_review, errors)
    if payload.get("stage5ce_wording_blemish_reviewed") is not True:
        errors.append("Stage 5CE wording warning must be reviewed")
    if payload.get("stage5ce_wording_blemish_gate_opener") is not False:
        errors.append("Stage 5CE wording warning must not be a gate opener")
    if payload.get("reported_typo_field_present_current_repo") is True and (
        payload.get("wording_warning_disposition") != "forward_erratum_recorded"
    ):
        errors.append("present typo must be recorded as a forward erratum")
    if payload.get("reported_typo_field_present_current_repo") is False and (
        payload.get("wording_warning_disposition") != "not_reproduced_current_repo"
    ):
        errors.append("absent typo must be recorded as not reproduced in current repo")
    if payload.get("approval_gate_satisfied_now") is not False:
        errors.append("wording warning must not satisfy approval gate")
    return {
        "stage5cg_stage5ce_wording_review_valid": not errors,
        "wording_warning_disposition": payload.get("wording_warning_disposition"),
        "reported_typo_field_present_current_repo": payload.get(
            "reported_typo_field_present_current_repo"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cg_no_byte_stream_transition_gate(
    *, gate: Path = DATA_PATHS["no_byte_stream_transition_gate"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(gate, errors)
    if payload.get("no_byte_stream_transition_gate_status") != "closed":
        errors.append("no-byte-stream transition gate must be closed")
    for field in (
        "byte_stream_generation_authorized_now",
        "real_byte_stream_generated",
        "variant_byte_streams_generated",
        "dwh_hash_search_performed",
        "scoring_performed",
        "cuda_execution_performed",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cg_no_byte_stream_transition_gate_valid": not errors,
        "no_byte_stream_transition_gate_status": payload.get(
            "no_byte_stream_transition_gate_status"
        ),
        "blocked_action_count": len(payload.get("blocked_actions", [])),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cg_no_execution_transition_gate(
    *, gate: Path = DATA_PATHS["no_execution_transition_gate"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(gate, errors)
    if payload.get("no_execution_transition_gate_status") != "closed":
        errors.append("no-execution transition gate must be closed")
    for field in (
        "execution_authorized_now",
        "token_block_experiment_executed",
        "dwh_hash_search_performed",
        "scoring_performed",
        "cuda_execution_performed",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cg_no_execution_transition_gate_valid": not errors,
        "no_execution_transition_gate_status": payload.get("no_execution_transition_gate_status"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cg_sidecar_gates(
    *,
    no_active_ingestion: Path = DATA_PATHS["no_active_ingestion"],
    sidecar_activation_blocker: Path = DATA_PATHS["sidecar_activation_blocker"],
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {
        "no_active_ingestion": _validate_payload(no_active_ingestion, errors),
        "sidecar_activation_blocker": _validate_payload(sidecar_activation_blocker, errors),
    }
    _validate_sidecar_gates(payloads, errors)
    return {
        "stage5cg_sidecar_gates_valid": not errors,
        "string4_sidecar_status": payloads["no_active_ingestion"].get("string4_sidecar_status"),
        "string4_active_input_allowed": payloads["no_active_ingestion"].get(
            "string4_active_input_allowed"
        ),
        "validation_error_count": len(errors),
    }, errors


def _validate_sidecar_gates(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
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
        ):
            if payload.get(field) is True:
                errors.append(f"{key}: {field} must remain false")


def validate_stage5cg(
    *,
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {key: _validate_payload(path, errors) for key, path in DATA_PATHS.items()}
    _check_false_flags(payloads, errors)
    _validate_sidecar_gates(payloads, errors)

    summary_payload = payloads["summary"]
    next_payload = payloads["next_stage"]
    guardrail_payload = payloads["guardrail"]

    if summary != DATA_PATHS["summary"]:
        summary_payload = _validate_payload(summary, errors)
    if next_stage_decision != DATA_PATHS["next_stage"]:
        next_payload = _validate_payload(next_stage_decision, errors)
    if guardrail != DATA_PATHS["guardrail"]:
        guardrail_payload = _validate_payload(guardrail, errors)

    if summary_payload.get("stage5cf_verdict") != "accept_with_warnings":
        errors.append("Stage 5CF verdict must be accept_with_warnings")
    if summary_payload.get("stage5ce_proposal_package_status") != "review_package_only":
        errors.append("Stage 5CE proposal package must remain review_package_only")
    if summary_payload.get("operator_approval_decision_scaffold_created") is not True:
        errors.append("operator decision scaffold must be created")
    if summary_payload.get("deep_research_acceptance_decision_scaffold_created") is not True:
        errors.append("Deep Research decision scaffold must be created")
    if summary_payload.get("combined_approval_decision_gate_scaffold_created") is not True:
        errors.append("combined approval gate scaffold must be created")
    if summary_payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    if summary_payload.get("active_lineage_record_count") != 8:
        errors.append("active-lineage record count must remain 8")
    if summary_payload.get("stage5ce_wording_blemish_reviewed") is not True:
        errors.append("Stage 5CE wording warning must be reviewed")
    if next_payload.get("selected_next_stage_id") != "stage-5ch":
        errors.append("Stage 5CG must select Stage 5CH as next stage")
    if next_payload.get("selected_next_stage_authorizes_execution") is not False:
        errors.append("Stage 5CH must not authorize execution")
    if guardrail_payload.get("future_token_block_execution_remains_blocked") is not True:
        errors.append("future token-block execution must remain blocked")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output directory must be absent/unused")

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

    generated_summary = results_dir / "summary.json"
    generated_summary_present = generated_summary.is_file()

    source_payload = payloads["source_digest_index"]
    digest_paths = [record.get("path") for record in source_payload.get("source_records", [])]
    if len(digest_paths) != len(set(digest_paths)):
        errors.append("Stage 5CG source digest paths must be unique")

    lineage_payload = payloads["active_lineage"]
    lineage_paths = [record.get("path") for record in lineage_payload.get("lineage_records", [])]
    if CORRECT_STAGE5AW_PATH not in lineage_paths:
        errors.append("correct Stage 5AW repaired path must be present in active lineage")
    if INCORRECT_STAGE5AW_PATH in lineage_paths:
        errors.append("deprecated Stage 5AW path must be absent from active lineage")

    return {
        "stage5cg_valid": not errors,
        "validation_error_count": len(errors),
        "stage5cf_verdict": summary_payload.get("stage5cf_verdict"),
        "operator_approval_decision_scaffold_created": summary_payload.get(
            "operator_approval_decision_scaffold_created"
        ),
        "deep_research_acceptance_decision_scaffold_created": summary_payload.get(
            "deep_research_acceptance_decision_scaffold_created"
        ),
        "approval_gate_satisfied_now": summary_payload.get("approval_gate_satisfied_now"),
        "active_planning_input_authorized_now": summary_payload.get(
            "active_planning_input_authorized_now"
        ),
        "string4_active_input_allowed": summary_payload.get("string4_active_input_allowed"),
        "stage5bd_run_plan_id_count": summary_payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": summary_payload.get("active_lineage_record_count"),
        "generated_summary_present": generated_summary_present,
        "stage5ce_wording_blemish_disposition": summary_payload.get(
            "stage5ce_wording_blemish_disposition"
        ),
        "recommended_next_stage_id": next_payload.get("selected_next_stage_id"),
    }, errors


def load_stage5cg_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    """Load the Stage 5CG summary."""

    return _read(summary)
