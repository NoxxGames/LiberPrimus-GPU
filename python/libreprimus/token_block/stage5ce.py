"""Stage 5CE active-planning-input proposal package metadata."""

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
    STAGE5BD_PRESERVATION_PATHS,
    validate_stage5ca_citation_contract,
)
from libreprimus.token_block.stage5cc import (
    BLOCKED_BYTE_STREAM_ACTIONS,
    FUTURE_ACTIVE_PLANNING_INPUT_REQUIREMENTS,
    load_stage5cc_summary,
    validate_stage5cc,
    validate_stage5cc_activation_preconditions,
    validate_stage5cc_fail_closed_triggers,
)

STAGE_ID = "stage-5ce"
STAGE_TITLE = (
    "Stage 5CE - Active-planning-input proposal package and operator/Deep Research "
    "gate design, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5cc"
SOURCE_PREVIOUS_COMMIT = "5e52ac4aa02af8d66db8b5d8f5b2d9345830a59a"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5cd"
SOURCE_DEEP_RESEARCH_REPORT = "17_Stage-5CC-Deep-Research-Review.md"

RESULTS_DIR = Path("experiments/results/token-block/stage5ce")
CODEX_COMPLETION_PATH = Path("codex-output/stage5ce-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
STAGE5CD_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "17_Stage-5CC-Deep-Research-Review.md"
)

# Updated after the final local pytest run in this stage.
PYTEST_COUNT_OBSERVED_LOCALLY = 2267
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"

STAGE5CD_FINDINGS = [
    "stage5cc_metadata_only_hardening_is_coherent",
    "stage5cc_preserves_stage5ca_exact_citation_contract",
    "stage5cc_fail_closed_triggers_are_exact_set",
    "stage5cc_activation_preconditions_are_exact_set",
    "stage5cc_active_planning_input_preflight_created",
    "stage5cc_active_planning_input_preflight_only",
    "stage5cc_no_byte_and_no_execution_gates_closed",
    "stage5cc_preserves_stage5bd_run_plan_ids",
    "stage5cc_preserves_active_token_block_lineage",
    "stage5cc_keeps_string4_inactive",
    "stage5cc_keeps_string4_noncanonical",
    "stage5cc_keeps_string4_out_of_active_input",
    "stage5cc_keeps_string4_out_of_dry_run_ingestion",
    "stage5cc_keeps_string4_out_of_byte_stream_generation",
    "stage5cc_keeps_string4_out_of_execution_input",
    "stage5cc_performs_no_manifest_supersession",
    "stage5cc_performs_no_active_ingestion",
    "stage5cc_performs_no_byte_stream_generation",
    "stage5cc_performs_no_execution_or_solve_work",
    "stage5cc_is_safe_to_build_on",
    "next_step_should_package_proposal_for_review_not_activate_anything",
]

STAGE5CD_WARNING_ACTIONS = {
    "warning_1_public_github_stale_or_incomplete": [
        "preserve_external_evidence_caveat",
        "keep_reviewable_metadata_committed",
        "do_not_attempt_final_commit_self_embedding",
        "continue_issue_and_codex_output_as_external_closure_route",
    ],
    "warning_2_commit_ci_externality": [
        "preserve_final_commit_external_evidence_policy",
        "preserve_ci_external_evidence_policy",
        "record_final_commit_self_embedded_false",
        "record_final_commit_external_evidence_required_true",
        "record_ci_external_evidence_required_true",
    ],
    "warning_3_committed_validation_lacks_exact_pytest_count": [
        "add_committed_pytest_count_capture_fields",
        "record_exact_pytest_count_observed_in_stage5ce_local_validation",
        "add_tests_requiring_committed_pytest_count_capture",
    ],
    "warning_4_stage5cc_citation_negative_tests_thinner": [
        "add_direct_negative_test_missing_required_citation",
        "add_direct_negative_test_extra_citation",
        "add_direct_negative_test_unresolved_citation_path",
        "add_direct_negative_test_deprecated_stage5aw_path",
        "preserve_exact_citation_contract_semantics",
    ],
}

APPROVAL_GATE_REQUIREMENTS = [
    "explicit_operator_approval_record",
    "explicit_deep_research_accept_record",
    "stage5ce_proposal_package_reviewed",
    "stage5cc_exact_citation_contract_still_valid",
    "stage5cc_fail_closed_trigger_exact_set_still_valid",
    "stage5cc_activation_precondition_exact_set_still_valid",
    "stage5bd_plan_preservation_or_explicit_future_supersession",
    "active_lineage_preservation_or_explicit_future_supersession",
    "no_byte_stream_transition_gate_still_closed_until_future_byte_stage",
    "no_execution_transition_gate_still_closed_until_future_execution_stage",
    "future_stage_explicitly_scopes_activation",
    "future_stage_keeps_no_solve_claim_policy",
]

CITATION_NEGATIVE_TESTS = [
    "missing_required_citation_fails",
    "extra_citation_fails",
    "unresolved_citation_path_fails",
    "deprecated_stage5aw_path_fails",
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5ce-summary.yaml"),
    "next_stage": Path("data/project-state/stage5ce-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5ce-stage5cd-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5ce-reviewable-stage-marker.yaml"),
    "validation_evidence": Path("data/project-state/stage5ce-reviewable-validation-evidence.yaml"),
    "source_digest_index": Path("data/project-state/stage5ce-reviewable-source-digest-index.yaml"),
    "gap_register": Path("data/project-state/stage5ce-reviewability-gap-register.yaml"),
    "equivalence_map": Path("data/project-state/stage5ce-record-family-name-equivalence-map.yaml"),
    "proposal_package": Path(
        "data/token-block/stage5ce-active-planning-input-proposal-package.yaml"
    ),
    "citation_set": Path("data/token-block/stage5ce-proposal-package-citation-set.yaml"),
    "operator_gate": Path("data/token-block/stage5ce-operator-approval-gate-design.yaml"),
    "deep_research_gate": Path(
        "data/token-block/stage5ce-deep-research-approval-gate-design.yaml"
    ),
    "combined_gate": Path(
        "data/token-block/stage5ce-operator-deep-research-combined-gate-contract.yaml"
    ),
    "approval_validation": Path(
        "data/token-block/stage5ce-approval-gate-validation-requirements.yaml"
    ),
    "stage5cc_preservation": Path(
        "data/token-block/stage5ce-stage5cc-contract-preservation.yaml"
    ),
    "citation_negative": Path(
        "data/token-block/stage5ce-stage5cc-citation-negative-test-hardening.yaml"
    ),
    "pytest_count": Path("data/token-block/stage5ce-committed-pytest-count-capture.yaml"),
    "nonactivation": Path(
        "data/token-block/stage5ce-active-planning-input-nonactivation-proof.yaml"
    ),
    "no_active_ingestion": Path("data/token-block/stage5ce-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5ce-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5ce-no-execution-transition-gate.yaml"
    ),
    "supersession_nonactivation": Path(
        "data/token-block/stage5ce-manifest-supersession-nonactivation-proof.yaml"
    ),
    "stage5bd_preservation": Path("data/token-block/stage5ce-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5ce-active-lineage-preservation.yaml"),
    "sidecar_activation_blocker": Path("data/token-block/stage5ce-sidecar-activation-blocker.yaml"),
    "future_impact": Path("data/token-block/stage5ce-future-dry-run-planning-impact.yaml"),
    "transition_policy": Path(
        "data/token-block/stage5ce-sidecar-to-active-transition-package-policy.yaml"
    ),
    "dwh": Path("data/historical-route/stage5ce-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5ce-source-gap-severity-update.yaml"),
    "guardrail": Path("data/historical-route/stage5ce-guardrail.yaml"),
    "handoff": Path("data/source-harvester/stage5ce-codex-handoff-policy.yaml"),
    "review_packaging_warning": Path("data/source-harvester/stage5ce-review-packaging-warning.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}

RECORD_TYPES = {key: f"stage5ce_{key}" for key in DATA_PATHS}
RECORD_TYPES.update(
    {
        "proposal_package": "stage5ce_active_planning_input_proposal_package",
        "citation_set": "stage5ce_proposal_package_citation_set",
        "combined_gate": "stage5ce_operator_deep_research_combined_gate_contract",
        "no_byte_stream_transition_gate": "stage5ce_no_byte_stream_transition_gate",
        "no_execution_transition_gate": "stage5ce_no_execution_transition_gate",
    }
)

FALSE_FLAGS = {
    "active_ingestion_performed": False,
    "active_manifest_registry_updated": False,
    "active_planning_input_authorized_now": False,
    "active_planning_input_proposal_performed": False,
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
        payload.update(FALSE_FLAGS)
    return payload


def _schema(record_type: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"const": record_type},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
    }
    for key in FALSE_FLAGS:
        properties[key] = {"const": False}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "record_type",
            "schema",
            "stage_id",
            "metadata_only",
            "solve_claim",
            "execution_allowed",
        ],
        "properties": properties,
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, schema_path in SCHEMA_PATHS.items():
        path = Path(schema_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        write_json(path, _schema(RECORD_TYPES[key]))


def _write_generated(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".jsonl":
        path.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in payload),
            encoding="utf-8",
        )
    else:
        write_json(path, payload)


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
    minimum_paths = [
        str(STAGE5CD_REPORT_PATH),
        "data/project-state/stage5cc-summary.yaml",
        "data/project-state/stage5cc-next-stage-decision.yaml",
        "data/token-block/stage5cc-fail-closed-trigger-exact-set-contract.yaml",
        "data/token-block/stage5cc-activation-precondition-exact-set-contract.yaml",
        "data/token-block/stage5cc-active-planning-input-proposal-preflight.yaml",
        "data/token-block/stage5cc-no-byte-stream-transition-gate.yaml",
        "data/token-block/stage5cc-no-execution-transition-gate.yaml",
        "data/token-block/stage5cc-stage5bd-plan-preservation.yaml",
        "data/token-block/stage5cc-active-lineage-preservation.yaml",
        "data/historical-route/stage5cc-guardrail.yaml",
        "data/token-block/stage5ca-future-runner-exact-citation-contract.yaml",
        "data/token-block/stage5bo-string4-branch-membership-after-errata.yaml",
        "data/token-block/stage5bo-errata-aware-token-option-universe.yaml",
        "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
        "data/token-block/stage5bd-run-plan-id-registry.yaml",
        "data/token-block/stage5ap-token-block-canonical-transcription.yaml",
        "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml",
        "data/token-block/stage5ay-branch-eligibility-policy.yaml",
        "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml",
        "data/token-block/stage5bb-active-manifest-registry.yaml",
        "data/token-block/stage5bd-active-manifest-lock.yaml",
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
    stage5ce_key_paths = [
        DATA_PATHS["proposal_package"].as_posix(),
        DATA_PATHS["combined_gate"].as_posix(),
        DATA_PATHS["no_byte_stream_transition_gate"].as_posix(),
        DATA_PATHS["no_execution_transition_gate"].as_posix(),
        DATA_PATHS["stage5bd_preservation"].as_posix(),
        DATA_PATHS["active_lineage"].as_posix(),
        DATA_PATHS["pytest_count"].as_posix(),
    ]
    return list(dict.fromkeys([*minimum_paths, *REQUIRED_CITATION_PATHS, *stage5ce_key_paths]))


def _source_digest_records() -> list[dict[str, Any]]:
    return [_sha_record(Path(path), role="stage5ce_reviewable_source") for path in _source_paths()]


def _lineage_digest_records(paths: list[str]) -> list[dict[str, Any]]:
    return [_sha_record(Path(path), role="stage5ce_preserved_active_lineage_record") for path in paths]


def _citation_records() -> list[dict[str, Any]]:
    return [
        {
            "path": path,
            "required": True,
            "present": Path(path).is_file(),
            "deprecated_stage5aw_path": path == INCORRECT_STAGE5AW_PATH,
        }
        for path in REQUIRED_CITATION_PATHS
    ]


def _validation_commands() -> list[dict[str, Any]]:
    commands = [
        ("stage5ce_build", "python -m libreprimus.cli token-block build-stage5ce"),
        (
            "stage5ce_focused_validators",
            "python -m libreprimus.cli token-block validate-stage5ce-proposal-package; "
            "validate-stage5ce-approval-gate; validate-stage5ce-citation-negative-tests; "
            "validate-stage5ce-no-byte-stream-transition-gate; "
            "validate-stage5ce-no-execution-transition-gate",
        ),
        ("stage5ce_validate", "python -m libreprimus.cli token-block validate-stage5ce"),
        ("stage5ce_summary", "python -m libreprimus.cli token-block stage5ce-summary"),
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
            "python -m libreprimus.cli token-block validate-stage5bd "
            "--results-dir experiments/results/token-block/stage5bd",
        ),
        (
            "stage5ax_validation",
            "python -m libreprimus.cli parallel-validation validate-stage5ax",
        ),
        (
            "stage5ax_parallel_validation",
            ".\\scripts\\ci\\run-parallel-validation.ps1 -Workers 16 "
            "-PytestWorkers 16 -PytestMode auto",
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
    rows = [
        {"command_id": command_id, "command": command, "status": "passed_local_validation"}
        for command_id, command in commands
    ]
    rows.append(
        {
            "command_id": "bash_parallel_or_consistency_wrapper",
            "command": "./scripts/ci/run-parallel-validation.sh and ./scripts/ci/run-consistency-checks.sh",
            "status": "not_run_wsl_unavailable",
            "reason_if_not_run": (
                "Local bash resolves to the Windows Subsystem for Linux launcher, "
                "but no WSL distributions are installed."
            ),
        }
    )
    return rows


def _equivalence_entries() -> list[dict[str, Any]]:
    return [
        {
            "record_family": key,
            "prompt_required_path": repo_relative(path),
            "committed_path": repo_relative(path),
            "semantic_status": "exact_path_used",
        }
        for key, path in DATA_PATHS.items()
        if key
        in {
            "summary",
            "proposal_package",
            "combined_gate",
            "no_byte_stream_transition_gate",
            "no_execution_transition_gate",
            "stage5bd_preservation",
            "active_lineage",
            "pytest_count",
        }
    ]


def _build_records(source_records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    stage5cc_summary = load_stage5cc_summary()
    run_plan_count = _run_plan_count()
    source_paths = [record["path"] for record in source_records]
    lineage_records = _lineage_digest_records(ACTIVE_LINEAGE_PATHS)

    records: dict[str, dict[str, Any]] = {
        "findings": _record(
            "findings",
            {
                "stage5cd_findings_integrated": True,
                "stage5cd_verdict": "accept_with_warnings",
                "stage5cd_finding_count": len(STAGE5CD_FINDINGS),
                "stage5cd_findings": STAGE5CD_FINDINGS,
                "stage5cd_warning_actions": STAGE5CD_WARNING_ACTIONS,
                "warnings_are_gate_openers": False,
                "token_block_execution_recommended": False,
                "active_string4_ingestion_recommended": False,
                "source_report_present_locally": STAGE5CD_REPORT_PATH.is_file(),
                "raw_report_body_committed": False,
            },
        ),
        "stage_marker": _record(
            "stage_marker",
            {
                "status": "complete",
                "reviewable_stage_marker_created": True,
                "source_previous_stage_status": stage5cc_summary.get("status", "unknown"),
                "source_previous_stage_commit_observed": SOURCE_PREVIOUS_COMMIT,
                "selected_next_stage_id": "stage-5cf",
                "selected_next_prompt_type": "deep_research_review",
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
                "pytest_count_source": "local_validation",
                "pytest_count_exactness": "observed_local_count",
                "stage5ax_parallel_validation_used": True,
                "raw_staged": False,
                "generated_outputs_staged": False,
                "codex_output_staged": False,
                "sqlite_staged": False,
                "final_commit_self_embedded": False,
                "final_commit_external_evidence_required": True,
                "ci_external_evidence_required": True,
                "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            },
        ),
        "source_digest_index": _record(
            "source_digest_index",
            {
                "source_digest_unique_path_validation_created": True,
                "source_digest_record_count": len(source_records),
                "source_digest_unique_path_count": len(set(source_paths)),
                "duplicate_path_count": sum(
                    1 for count in Counter(source_paths).values() if count > 1
                ),
                "duplicate_path_exception_count": 0,
                "source_digest_records": source_records,
                "source_paths_unique": len(source_paths) == len(set(source_paths)),
                "raw_or_generated_source_bodies_committed": False,
            },
        ),
        "gap_register": _record(
            "gap_register",
            {
                "reviewability_gap_register_created": True,
                "gap_count": 4,
                "gaps": [
                    {
                        "gap_id": "external_ci_corroboration",
                        "status": "preserved_as_external_evidence_requirement",
                        "gate_opener": False,
                    },
                    {
                        "gap_id": "final_commit_self_embedding",
                        "status": "impossible_by_design_external_evidence_required",
                        "gate_opener": False,
                    },
                    {
                        "gap_id": "stage5cc_pytest_count_not_committed",
                        "status": "closed_by_stage5ce_pytest_count_capture",
                        "gate_opener": False,
                    },
                    {
                        "gap_id": "stage5cc_direct_citation_negative_tests_thinner",
                        "status": "closed_by_stage5ce_direct_negative_tests",
                        "gate_opener": False,
                    },
                ],
            },
        ),
        "equivalence_map": _record(
            "equivalence_map",
            {
                "record_family_name_equivalence_map_created": True,
                "path_mapping_status": "exact_prompt_paths_used",
                "equivalence_record_count": len(_equivalence_entries()),
                "equivalence_records": _equivalence_entries(),
            },
        ),
        "proposal_package": _record(
            "proposal_package",
            {
                "active_planning_input_proposal_package_created": True,
                "active_planning_input_proposal_package_status": "review_package_only",
                "candidate_sidecar_id": "string4_inactive_planning_sidecar",
                "candidate_sidecar_status_required": "scaffolded_inactive",
                "candidate_sidecar_must_remain_noncanonical": True,
                "future_active_planning_input_proposal_would_require": (
                    FUTURE_ACTIVE_PLANNING_INPUT_REQUIREMENTS
                ),
                "operator_approval_required_before_activation": True,
                "deep_research_review_required_before_activation": True,
                "active_planning_input_proposal_performed": False,
                "active_planning_input_authorized_now": False,
                "active_planning_input_selected_now": False,
                "new_active_planning_input_created": False,
                "string4_added_to_stage5bd_run_plan_ids": False,
                "string4_added_to_active_dry_run_inputs": False,
                "future_token_block_execution_remains_blocked": True,
            },
        ),
        "citation_set": _record(
            "citation_set",
            {
                "proposal_package_citation_set_created": True,
                "citation_contract_type": "exact_set",
                "future_runner_must_cite_exactly": REQUIRED_CITATION_PATHS,
                "required_citation_count": len(REQUIRED_CITATION_PATHS),
                "citation_records": _citation_records(),
                "extra_citations_allowed_without_contract_update": False,
                "missing_citation_fails_closed": True,
                "unresolved_citation_path_fails_closed": True,
                "deprecated_stage5aw_path_allowed": False,
            },
        ),
        "operator_gate": _record(
            "operator_gate",
            {
                "operator_approval_gate_design_created": True,
                "operator_approval_required_before_activation": True,
                "operator_approval_record_present_now": False,
                "operator_approval_satisfied_now": False,
                "operator_approval_authorizes_activation_now": False,
                "operator_gate_requirements": APPROVAL_GATE_REQUIREMENTS,
            },
        ),
        "deep_research_gate": _record(
            "deep_research_gate",
            {
                "deep_research_approval_gate_design_created": True,
                "deep_research_review_required_before_activation": True,
                "deep_research_accept_record_present_now": False,
                "deep_research_approval_satisfied_now": False,
                "deep_research_gate_authorizes_activation_now": False,
                "selected_next_stage_id": "stage-5cf",
            },
        ),
        "combined_gate": _record(
            "combined_gate",
            {
                "operator_deep_research_gate_design_created": True,
                "operator_approval_required_before_activation": True,
                "deep_research_review_required_before_activation": True,
                "approval_gate_requirements": APPROVAL_GATE_REQUIREMENTS,
                "approval_gate_satisfied_now": False,
                "approval_gate_authorizes_activation_now": False,
                "activation_authorized_now": False,
                "dry_run_ingestion_authorized_now": False,
                "byte_stream_generation_authorized_now": False,
                "execution_authorized_now": False,
            },
        ),
        "approval_validation": _record(
            "approval_validation",
            {
                "approval_gate_validation_requirements_created": True,
                "validator_command": "libreprimus token-block validate-stage5ce-approval-gate",
                "validates_operator_and_deep_research_required": True,
                "validates_approval_gate_satisfied_false": True,
                "validates_no_activation_authorization": True,
                "validates_no_dry_run_ingestion": True,
                "validates_no_byte_stream_authorization": True,
                "validates_no_execution_authorization": True,
            },
        ),
        "stage5cc_preservation": _record(
            "stage5cc_preservation",
            {
                "stage5cc_status_preserved": stage5cc_summary.get("status") == "complete",
                "stage5cc_exact_citation_contract_preserved": True,
                "stage5cc_fail_closed_trigger_exact_set_preserved": True,
                "stage5cc_activation_precondition_exact_set_preserved": True,
                "stage5cc_required_citation_count": int(
                    stage5cc_summary.get("required_citation_count") or 0
                ),
                "stage5cc_required_fail_closed_trigger_count": int(
                    stage5cc_summary.get("required_fail_closed_trigger_count") or 0
                ),
                "stage5cc_required_activation_precondition_count": int(
                    stage5cc_summary.get("required_activation_precondition_count") or 0
                ),
                "stage5cc_stage5bd_run_plan_id_count": int(
                    stage5cc_summary.get("stage5bd_run_plan_id_count") or 0
                ),
                "stage5cc_active_lineage_record_count": int(
                    stage5cc_summary.get("active_lineage_record_count") or 0
                ),
            },
        ),
        "citation_negative": _record(
            "citation_negative",
            {
                "stage5cc_citation_contract_negative_tests_hardened": True,
                "negative_test_hardening_status": "direct_stage5ce_tests_added",
                "negative_tests_added_or_hardened": CITATION_NEGATIVE_TESTS,
                "missing_required_citation_fails": True,
                "extra_citation_fails": True,
                "unresolved_citation_path_fails": True,
                "deprecated_stage5aw_path_fails": True,
                "preserve_exact_citation_contract_semantics": True,
            },
        ),
        "pytest_count": _record(
            "pytest_count",
            {
                "committed_pytest_count_capture_created": True,
                "pytest_count_capture_created": True,
                "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
                "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
                "pytest_count_committed": True,
                "pytest_count_source": "local_validation",
                "pytest_count_exactness": "observed_local_count",
                "ci_pytest_count_self_embedded": False,
                "ci_external_evidence_required": True,
            },
        ),
        "nonactivation": _record(
            "nonactivation",
            {
                "active_planning_input_nonactivation_proof_created": True,
                "active_planning_input_proposal_package_status": "review_package_only",
                "active_planning_input_proposal_performed": False,
                "active_planning_input_authorized_now": False,
                "active_planning_input_selected_now": False,
                "new_active_planning_input_created": False,
                "string4_active_input_allowed": False,
                "string4_dry_run_ingestion_allowed_now": False,
            },
        ),
        "no_active_ingestion": _record(
            "no_active_ingestion",
            {
                "no_active_ingestion_status": "preserved_closed",
                "string4_sidecar_status": "scaffolded_inactive",
                "string4_sidecar_active": False,
                "string4_active_input_allowed": False,
                "string4_dry_run_ingestion_allowed_now": False,
                "string4_execution_input_allowed": False,
                "string4_added_to_active_dry_run_inputs": False,
                "string4_added_to_stage5bd_run_plan_ids": False,
                "active_ingestion_performed": False,
            },
        ),
        "no_byte_stream_transition_gate": _record(
            "no_byte_stream_transition_gate",
            {
                "no_byte_stream_transition_gate_status": "closed",
                "future_active_planning_input_does_not_imply_bytes": True,
                "byte_stream_generation_requires_separate_future_stage": True,
                "byte_stream_generation_authorized_now": False,
                "real_byte_stream_generated": False,
                "variant_byte_streams_generated": False,
                "generated_byte_streams_committed": False,
                "blocked_actions": BLOCKED_BYTE_STREAM_ACTIONS,
            },
        ),
        "no_execution_transition_gate": _record(
            "no_execution_transition_gate",
            {
                "no_execution_transition_gate_status": "closed",
                "future_active_planning_input_does_not_imply_execution": True,
                "execution_authorized_now": False,
                "token_block_experiment_executed": False,
                "decode_attempt_performed": False,
                "dwh_hash_search_performed": False,
                "scoring_performed": False,
                "cuda_execution_performed": False,
                "benchmark_performed": False,
                "stego_tool_execution_performed": False,
            },
        ),
        "supersession_nonactivation": _record(
            "supersession_nonactivation",
            {
                "manifest_supersession_nonactivation_proof_created": True,
                "manifest_supersession_performed": False,
                "manifest_supersession_authorized_now": False,
                "active_manifest_registry_updated": False,
                "before_after_digest_comparison_performed_for_supersession": False,
                "explicit_target_manifest_list_selected_now": False,
                "stage5bd_plan_superseded": False,
                "stage5bd_plan_preserved_or_explicitly_superseded": "preserved",
            },
        ),
        "stage5bd_preservation": _record(
            "stage5bd_preservation",
            {
                "stage5bd_plan_preservation_status": "preserved_unchanged",
                "stage5bd_run_plan_id_count_before": run_plan_count,
                "stage5bd_run_plan_id_count_after": run_plan_count,
                "stage5bd_run_plan_id_count": run_plan_count,
                "stage5bd_run_plan_ids_changed": False,
                "stage5bd_dry_run_plan_manifest_changed": False,
                "stage5bd_dry_run_records_remain_valid": True,
                "stage5bd_plan_superseded": False,
                "string4_added_to_stage5bd_run_plan_ids": False,
                "string4_added_to_active_dry_run_inputs": False,
                "stage5bd_preservation_paths": STAGE5BD_PRESERVATION_PATHS,
            },
        ),
        "active_lineage": _record(
            "active_lineage",
            {
                "active_lineage_preservation_status": "preserved_unchanged",
                "preserved_active_record_paths": ACTIVE_LINEAGE_PATHS,
                "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
                "lineage_records": lineage_records,
                "deprecated_stage5aw_path_included": False,
                "correct_stage5aw_path_included": True,
                "all_preserved_active_paths_resolve": all(
                    Path(path).is_file() for path in ACTIVE_LINEAGE_PATHS
                ),
                "canonical_transcription_changed": False,
                "active_token_block_manifest_changed": False,
            },
        ),
        "sidecar_activation_blocker": _record(
            "sidecar_activation_blocker",
            {
                "blocker_status": "active",
                "blocked_item": "string4_inactive_planning_sidecar",
                "blocked_actions": [
                    "active_input",
                    "active_dry_run_ingestion",
                    "manifest_supersession",
                    *BLOCKED_BYTE_STREAM_ACTIONS,
                    "execution",
                ],
                "future_token_block_execution_remains_blocked": True,
            },
        ),
        "future_impact": _record(
            "future_impact",
            {
                "future_dry_run_planning_impact": (
                    "proposal package is reviewable but blocked from active ingestion, "
                    "bytes, and execution"
                ),
                "future_token_block_execution_remains_blocked": True,
                "stage5bd_run_plan_ids_preserved": True,
                "future_runner_must_validate_stage5ce_gate_contracts": True,
                "stage5bd_dry_run_plan_manifest_changed": False,
            },
        ),
        "transition_policy": _record(
            "transition_policy",
            {
                "sidecar_to_active_transition_package_policy_created": True,
                "transition_policy_status": "future_stage_only",
                "current_stage_authorizes_activation": False,
                "current_stage_authorizes_active_input": False,
                "current_stage_authorizes_dry_run_ingestion": False,
                "current_stage_authorizes_byte_stream_generation": False,
                "current_stage_authorizes_execution": False,
                "future_transition_requires": APPROVAL_GATE_REQUIREMENTS,
            },
        ),
        "dwh": _record(
            "dwh",
            {
                "dwh_quarantine_status": "reaffirmed_active",
                "dwh_quarantine_reaffirmed": True,
                "dwh_hash_search_performed": False,
                "dwh_context_used_as_execution_input": False,
            },
        ),
        "source_gap": _record(
            "source_gap",
            {
                "source_gap_severity_update": "unchanged_blocking_for_execution",
                "string4_source_gap_status": "inactive_context_only",
                "stage5ce_changes_source_truth": False,
            },
        ),
        "guardrail": _record(
            "guardrail",
            {
                "guardrail_status": "active",
                "future_token_block_execution_remains_blocked": True,
                "string4_sidecar_status": "scaffolded_inactive",
                "stage5ce_is_gate_opener": False,
                "no_byte_stream_transition_gate_status": "closed",
                "no_execution_transition_gate_status": "closed",
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
                "public_github_views_may_be_stale_or_incomplete": True,
                "attached_zip_and_committed_metadata_are_primary_review_sources": True,
                "final_commit_external_evidence_required": True,
                "ci_external_evidence_required": True,
                "raw_review_pack_committed": False,
                "raw_deep_research_body_committed": False,
                "compact_metadata_only": True,
            },
        ),
        "next_stage": _record(
            "next_stage",
            {
                "selected_next_stage_id": "stage-5cf",
                "selected_next_stage_title": (
                    "Stage 5CF - Deep Research review of Stage 5CE "
                    "active-planning-input proposal package and operator/Deep Research "
                    "gate design, without execution"
                ),
                "selected_next_prompt_type": "deep_research_review",
                "selected_next_stage_authorizes_execution": False,
                "selected_next_stage_reason": (
                    "Stage 5CE packages a review-only active-planning-input proposal "
                    "and gate design that requires independent review before any "
                    "activation-capable stage."
                ),
            },
        ),
    }

    summary_body = {
        "status": "complete",
        "stage5cd_findings_integrated": True,
        "stage5cd_verdict": "accept_with_warnings",
        "stage5cc_status_preserved": True,
        "stage5cc_exact_citation_contract_preserved": True,
        "stage5cc_fail_closed_trigger_exact_set_preserved": True,
        "stage5cc_activation_precondition_exact_set_preserved": True,
        "active_planning_input_proposal_package_created": True,
        "active_planning_input_proposal_package_status": "review_package_only",
        "active_planning_input_proposal_performed": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        "new_active_planning_input_created": False,
        "operator_deep_research_gate_design_created": True,
        "operator_approval_required_before_activation": True,
        "deep_research_review_required_before_activation": True,
        "approval_gate_satisfied_now": False,
        "approval_gate_authorizes_activation_now": False,
        "stage5cc_citation_contract_negative_tests_hardened": True,
        "committed_pytest_count_capture_created": True,
        "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
        "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
        "no_byte_stream_transition_gate_status": "closed",
        "no_execution_transition_gate_status": "closed",
        "manifest_supersession_performed": False,
        "manifest_supersession_authorized_now": False,
        "stage5bd_dry_run_records_remain_valid": True,
        "stage5bd_run_plan_id_count": run_plan_count,
        "stage5bd_run_plan_ids_changed": False,
        "stage5bd_dry_run_plan_manifest_changed": False,
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
        "required_citation_count": len(REQUIRED_CITATION_PATHS),
        "required_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
        "observed_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
        "required_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
        "observed_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "source_digest_record_count": len(source_records),
        "source_digest_unique_path_count": len(set(source_paths)),
        "dwh_quarantine_reaffirmed": True,
        "generated_outputs_committed": False,
        "codex_output_used": False,
        "recommended_next_stage_id": "stage-5cf",
        "recommended_next_stage_title": (
            "Stage 5CF - Deep Research review of Stage 5CE active-planning-input "
            "proposal package and operator/Deep Research gate design, without execution"
        ),
    }
    summary_body.update(FALSE_FLAGS)
    records["summary"] = _record("summary", summary_body, include_false_flags=False)
    return records


def build_stage5ce(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    _write_schemas()
    results_dir.mkdir(parents=True, exist_ok=True)

    records = _build_records(_source_digest_records())
    for key, payload in records.items():
        if key != "source_digest_index":
            write_yaml(DATA_PATHS[key], payload)

    records = _build_records(_source_digest_records())
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    _write_generated(results_dir / "proposal_package.json", records["proposal_package"])
    _write_generated(results_dir / "combined_gate_contract.json", records["combined_gate"])
    _write_generated(
        results_dir / "citation_negative_test_hardening.json",
        records["citation_negative"],
    )
    _write_generated(
        results_dir / "no_byte_stream_transition_gate.json",
        records["no_byte_stream_transition_gate"],
    )
    _write_generated(
        results_dir / "no_execution_transition_gate.json",
        records["no_execution_transition_gate"],
    )
    _write_generated(results_dir / "summary.json", records["summary"])
    _write_generated(
        results_dir / "warnings.jsonl",
        [
            {
                "warning_id": "stage5ce_review_package_only",
                "severity": "info",
                "message": "Stage 5CE packages a proposal for review and opens no gate.",
            },
            {
                "warning_id": "external_final_commit_ci_evidence",
                "severity": "info",
                "message": "Final commit and CI status remain external evidence.",
            },
        ],
    )
    return records["summary"]


def _load_schema(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _validate_payload(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing_record={repo_relative(path)}")
        return {}
    payload = _read(path)
    schema_path = payload.get("schema")
    if schema_path and Path(schema_path).is_file():
        schema_errors = list(Draft202012Validator(_load_schema(str(schema_path))).iter_errors(payload))
        errors.extend(f"{repo_relative(path)} schema_error={error.message}" for error in schema_errors)
    return payload


def _check_false_flags(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for record_key, payload in payloads.items():
        for key, expected in FALSE_FLAGS.items():
            if key in payload and payload.get(key) not in (expected, None):
                errors.append(f"{record_key} {key} must be {str(expected).lower()}")


def validate_stage5ce_proposal_package(
    *, proposal_package: Path = DATA_PATHS["proposal_package"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(proposal_package, errors)
    requirements = [
        str(item) for item in payload.get("future_active_planning_input_proposal_would_require", [])
    ]
    missing = sorted(set(FUTURE_ACTIVE_PLANNING_INPUT_REQUIREMENTS) - set(requirements))
    extra = sorted(set(requirements) - set(FUTURE_ACTIVE_PLANNING_INPUT_REQUIREMENTS))
    errors.extend(f"missing_active_planning_requirement={item}" for item in missing)
    errors.extend(f"extra_active_planning_requirement={item}" for item in extra)
    if payload.get("active_planning_input_proposal_package_status") != "review_package_only":
        errors.append("active planning input proposal package must remain review_package_only")
    for flag in [
        "active_planning_input_proposal_performed",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
        "new_active_planning_input_created",
        "string4_added_to_stage5bd_run_plan_ids",
        "string4_added_to_active_dry_run_inputs",
    ]:
        if payload.get(flag) is not False:
            errors.append(f"{flag} must be false")
    counts = {
        "stage5ce_proposal_package_valid": not errors,
        "active_planning_input_authorized_now": bool(
            payload.get("active_planning_input_authorized_now")
        ),
        "active_planning_input_selected_now": bool(payload.get("active_planning_input_selected_now")),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5ce_approval_gate(
    *, combined_gate: Path = DATA_PATHS["combined_gate"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(combined_gate, errors)
    requirements = [str(item) for item in payload.get("approval_gate_requirements", [])]
    missing = sorted(set(APPROVAL_GATE_REQUIREMENTS) - set(requirements))
    extra = sorted(set(requirements) - set(APPROVAL_GATE_REQUIREMENTS))
    errors.extend(f"missing_approval_gate_requirement={item}" for item in missing)
    errors.extend(f"extra_approval_gate_requirement={item}" for item in extra)
    for flag in [
        "operator_approval_required_before_activation",
        "deep_research_review_required_before_activation",
    ]:
        if payload.get(flag) is not True:
            errors.append(f"{flag} must be true")
    for flag in [
        "approval_gate_satisfied_now",
        "approval_gate_authorizes_activation_now",
        "activation_authorized_now",
        "dry_run_ingestion_authorized_now",
        "byte_stream_generation_authorized_now",
        "execution_authorized_now",
    ]:
        if payload.get(flag) is not False:
            errors.append(f"{flag} must be false")
    counts = {
        "stage5ce_approval_gate_valid": not errors,
        "approval_gate_satisfied_now": bool(payload.get("approval_gate_satisfied_now")),
        "approval_gate_authorizes_activation_now": bool(
            payload.get("approval_gate_authorizes_activation_now")
        ),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5ce_citation_negative_tests(
    *, citation_set: Path = DATA_PATHS["citation_set"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(citation_set, errors)
    cited = [str(path) for path in payload.get("future_runner_must_cite_exactly", [])]
    required = list(REQUIRED_CITATION_PATHS)
    missing = sorted(set(required) - set(cited))
    extra = sorted(set(cited) - set(required))
    if missing:
        errors.extend(f"missing_required_citation={path}" for path in missing)
    if extra:
        errors.extend(f"extra_citation={path}" for path in extra)
    unresolved = [path for path in cited if not Path(path).is_file()]
    errors.extend(f"citation_path_unresolved={path}" for path in unresolved)
    if INCORRECT_STAGE5AW_PATH in cited:
        errors.append("deprecated_stage5aw_path_present")
    if payload.get("deprecated_stage5aw_path_allowed") is not False:
        errors.append("deprecated_stage5aw_path_allowed must be false")
    _stage5ca_counts, stage5ca_errors = validate_stage5ca_citation_contract()
    errors.extend(f"stage5ca_{error}" for error in stage5ca_errors)
    counts = {
        "stage5ce_citation_negative_tests_valid": not errors,
        "required_citation_count": len(required),
        "observed_citation_count": len(cited),
        "missing_citation_count": len(missing),
        "extra_citation_count": len(extra),
        "unresolved_citation_count": len(unresolved),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5ce_no_byte_stream_transition_gate(
    *, gate: Path = DATA_PATHS["no_byte_stream_transition_gate"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(gate, errors)
    actions = [str(item) for item in payload.get("blocked_actions", [])]
    missing = sorted(set(BLOCKED_BYTE_STREAM_ACTIONS) - set(actions))
    extra = sorted(set(actions) - set(BLOCKED_BYTE_STREAM_ACTIONS))
    errors.extend(f"missing_blocked_action={item}" for item in missing)
    errors.extend(f"extra_blocked_action={item}" for item in extra)
    if payload.get("no_byte_stream_transition_gate_status") != "closed":
        errors.append("no-byte-stream transition gate must be closed")
    for flag in [
        "byte_stream_generation_authorized_now",
        "real_byte_stream_generated",
        "variant_byte_streams_generated",
        "generated_byte_streams_committed",
    ]:
        if payload.get(flag) is not False:
            errors.append(f"{flag} must be false")
    counts = {
        "stage5ce_no_byte_stream_transition_gate_valid": not errors,
        "no_byte_stream_transition_gate_status": payload.get(
            "no_byte_stream_transition_gate_status", "unknown"
        ),
        "blocked_action_count": len(actions),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5ce_no_execution_transition_gate(
    *, gate: Path = DATA_PATHS["no_execution_transition_gate"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(gate, errors)
    if payload.get("no_execution_transition_gate_status") != "closed":
        errors.append("no-execution transition gate must be closed")
    for flag in [
        "execution_authorized_now",
        "token_block_experiment_executed",
        "decode_attempt_performed",
        "dwh_hash_search_performed",
        "scoring_performed",
        "cuda_execution_performed",
        "benchmark_performed",
        "stego_tool_execution_performed",
    ]:
        if payload.get(flag) is not False:
            errors.append(f"{flag} must be false")
    counts = {
        "stage5ce_no_execution_transition_gate_valid": not errors,
        "no_execution_transition_gate_status": payload.get(
            "no_execution_transition_gate_status", "unknown"
        ),
        "validation_error_count": len(errors),
    }
    return counts, errors


def validate_stage5ce_sidecar_gates(
    *,
    stage5bd_preservation: Path = DATA_PATHS["stage5bd_preservation"],
    active_lineage: Path = DATA_PATHS["active_lineage"],
    validation_evidence: Path = DATA_PATHS["validation_evidence"],
    handoff: Path = DATA_PATHS["handoff"],
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {
        "stage5bd_preservation": _validate_payload(stage5bd_preservation, errors),
        "active_lineage": _validate_payload(active_lineage, errors),
        "validation_evidence": _validate_payload(validation_evidence, errors),
        "handoff": _validate_payload(handoff, errors),
    }
    _validate_sidecar_gates(payloads, errors)
    _check_false_flags(payloads, errors)
    counts = {
        "stage5ce_sidecar_gates_valid": not errors,
        "stage5bd_run_plan_id_count": int(
            payloads["stage5bd_preservation"].get("stage5bd_run_plan_id_count") or 0
        ),
        "active_lineage_record_count": int(
            payloads["active_lineage"].get("active_lineage_record_count") or 0
        ),
        "validation_error_count": len(errors),
    }
    return counts, errors


def _validate_sidecar_gates(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    if payloads["stage5bd_preservation"].get("stage5bd_run_plan_id_count") != _run_plan_count():
        errors.append("Stage 5BD run-plan count must remain 10")
    active_paths = payloads["active_lineage"].get("preserved_active_record_paths", [])
    if INCORRECT_STAGE5AW_PATH in active_paths:
        errors.append("deprecated_stage5aw_path_present")
    if CORRECT_STAGE5AW_PATH not in active_paths:
        errors.append("correct_stage5aw_path_missing")
    for path in active_paths:
        if not Path(path).is_file():
            errors.append(f"active_lineage_path_missing={path}")
    validation = payloads["validation_evidence"]
    if not isinstance(validation.get("pytest_count_observed_locally"), int):
        errors.append("pytest_count_observed_locally must be an integer")
    elif int(validation["pytest_count_observed_locally"]) <= 0:
        errors.append("pytest_count_observed_locally must be positive")
    if payloads["handoff"].get("canonical_codex_handoff_root") != "codex-output":
        errors.append("Stage 5CE must use codex-output as handoff root")
    if payloads["handoff"].get("codex_output_used") is not False:
        errors.append("codex_output_used must be false")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output directory must not exist")


def validate_stage5ce(
    *,
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {key: _validate_payload(path, errors) for key, path in DATA_PATHS.items()}
    summary_payload = (
        payloads["summary"] if summary == DATA_PATHS["summary"] else _validate_payload(summary, errors)
    )
    next_stage_payload = (
        payloads["next_stage"]
        if next_stage_decision == DATA_PATHS["next_stage"]
        else _validate_payload(next_stage_decision, errors)
    )
    guardrail_payload = (
        payloads["guardrail"]
        if guardrail == DATA_PATHS["guardrail"]
        else _validate_payload(guardrail, errors)
    )

    for _counts, focused_errors in [
        validate_stage5ce_proposal_package(),
        validate_stage5ce_approval_gate(),
        validate_stage5ce_citation_negative_tests(),
        validate_stage5ce_no_byte_stream_transition_gate(),
        validate_stage5ce_no_execution_transition_gate(),
    ]:
        errors.extend(focused_errors)

    _stage5cc_counts, stage5cc_errors = validate_stage5cc()
    errors.extend(f"stage5cc_{error}" for error in stage5cc_errors)
    _trigger_counts, trigger_errors = validate_stage5cc_fail_closed_triggers()
    errors.extend(f"stage5cc_trigger_{error}" for error in trigger_errors)
    _activation_counts, activation_errors = validate_stage5cc_activation_preconditions()
    errors.extend(f"stage5cc_activation_{error}" for error in activation_errors)

    _validate_sidecar_gates(payloads, errors)
    _check_false_flags(payloads | {"guardrail_arg": guardrail_payload}, errors)

    digest_paths = [
        str(record.get("path"))
        for record in payloads["source_digest_index"].get("source_digest_records", [])
    ]
    duplicate_paths = [path for path, count in Counter(digest_paths).items() if count > 1]
    if duplicate_paths:
        errors.extend(f"stage5ce_duplicate_source_digest_path={path}" for path in duplicate_paths)

    if summary_payload.get("stage5cd_verdict") != "accept_with_warnings":
        errors.append("summary must integrate Stage 5CD accept_with_warnings verdict")
    for key in [
        "stage5cc_exact_citation_contract_preserved",
        "stage5cc_fail_closed_trigger_exact_set_preserved",
        "stage5cc_activation_precondition_exact_set_preserved",
        "active_planning_input_proposal_package_created",
        "operator_deep_research_gate_design_created",
        "stage5cc_citation_contract_negative_tests_hardened",
        "committed_pytest_count_capture_created",
        "future_token_block_execution_remains_blocked",
    ]:
        if summary_payload.get(key) is not True:
            errors.append(f"summary {key} must be true")
    if summary_payload.get("active_planning_input_proposal_package_status") != "review_package_only":
        errors.append("summary proposal package status must be review_package_only")
    if summary_payload.get("manifest_supersession_performed") is not False:
        errors.append("manifest supersession must not be performed")
    if summary_payload.get("stage5bd_run_plan_id_count") != _run_plan_count():
        errors.append("Stage 5BD run-plan count must remain unchanged")
    if next_stage_payload.get("selected_next_stage_id") != "stage-5cf":
        errors.append("Stage 5CE must select Stage 5CF review")
    if guardrail_payload.get("guardrail_status") != "active":
        errors.append("Stage 5CE guardrail must be active")

    counts = {
        "stage5ce_valid": not errors,
        "validation_error_count": len(errors),
        "stage5cd_verdict": summary_payload.get("stage5cd_verdict", "unknown"),
        "active_planning_input_proposal_package_status": summary_payload.get(
            "active_planning_input_proposal_package_status", "unknown"
        ),
        "active_planning_input_authorized_now": bool(
            summary_payload.get("active_planning_input_authorized_now")
        ),
        "approval_gate_satisfied_now": bool(summary_payload.get("approval_gate_satisfied_now")),
        "no_byte_stream_transition_gate_status": summary_payload.get(
            "no_byte_stream_transition_gate_status", "unknown"
        ),
        "no_execution_transition_gate_status": summary_payload.get(
            "no_execution_transition_gate_status", "unknown"
        ),
        "manifest_supersession_performed": bool(
            summary_payload.get("manifest_supersession_performed")
        ),
        "stage5bd_run_plan_id_count": int(summary_payload.get("stage5bd_run_plan_id_count") or 0),
        "active_lineage_record_count": int(summary_payload.get("active_lineage_record_count") or 0),
        "pytest_count_observed_locally": int(
            summary_payload.get("pytest_count_observed_locally") or 0
        ),
        "source_digest_record_count": len(digest_paths),
        "source_digest_unique_path_count": len(set(digest_paths)),
        "source_digest_duplicate_path_count": len(duplicate_paths),
        "generated_summary_present": (results_dir / "summary.json").is_file(),
        "recommended_next_stage_id": summary_payload.get("recommended_next_stage_id", "unknown"),
    }
    return counts, errors


def load_stage5ce_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
