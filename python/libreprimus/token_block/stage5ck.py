"""Stage 5CK approval fixture-pack metadata."""

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
from libreprimus.token_block.stage5ci import (
    DATA_PATHS as STAGE5CI_DATA_PATHS,
    RESULTS_DIR as STAGE5CI_RESULTS_DIR,
    validate_stage5ci,
)

STAGE_ID = "stage-5ck"
STAGE_TITLE = (
    "Stage 5CK - Approval-record validation fixture pack and activation-decision "
    "review package, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5ci"
SOURCE_PREVIOUS_COMMIT = "654098c8de63d9e5dc94618d2b89020299fc4a36"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5cj"
SOURCE_DEEP_RESEARCH_REPORT = "20_Stage-5CI-Deep-Research-Review.md"
STAGE5CJ_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "20_Stage-5CI-Deep-Research-Review.md"
)
RESULTS_DIR = Path("experiments/results/token-block/stage5ck")
CODEX_COMPLETION_PATH = Path("codex-output/stage5ck-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

PYTEST_COUNT_OBSERVED_LOCALLY = 2327
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"

STAGE5CJ_FINDINGS = [
    "stage5ci_coherent_metadata_only_hardening_stage",
    "stage5ci_hardens_future_operator_approval_template",
    "stage5ci_hardens_future_deep_research_activation_acceptance_template",
    "stage5ci_hardens_combined_approval_gate_validation_surface",
    "stage5ci_hardens_activation_decision_template",
    "stage5ci_hardens_negative_validation_contract",
    "stage5ci_keeps_approval_activation_active_input_byte_manifest_and_execution_paths_closed",
    "string4_remains_inactive_noncanonical_sidecar_context",
    "stage5bd_remains_unchanged_at_ten_run_plan_ids",
    "active_lineage_remains_eight_records",
    "no_byte_execution_dwh_decode_stego_scoring_cuda_benchmark_or_solve_authorized",
    "warnings_are_reviewability_and_packaging_warnings_not_gate_openers",
    "attached_zip_not_pristine_checkout",
    "public_github_corroboration_not_reliable_in_stage5cj_session",
    "final_commit_and_ci_remain_external_evidence_items",
    "negative_validation_coverage_split_is_acceptable_but_needs_fixture_packaging",
    "stage5ci_safe_to_build_on",
    "next_safe_stage_is_fixture_pack_and_activation_decision_review_package",
]

STAGE5CJ_WARNINGS = {
    "attached_zip_not_pristine_checkout": "preserved_as_packaging_warning_not_gate_opener",
    "public_github_corroboration_unreliable": "recorded_as_external_evidence_caveat",
    "final_commit_and_ci_external": "kept_as_post_push_external_evidence",
    "negative_validation_split_across_tests": "closed_by_fixture_pack_reviewability",
}

OPERATOR_FIXTURE_CASES = [
    "missing_required_field",
    "template_only_misread_attempt",
    "approval_decision_present_but_no_activation_authorization",
    "byte_stream_authorized_invalid",
    "execution_authorized_invalid",
    "stage5bd_preservation_missing_invalid",
    "active_lineage_preservation_missing_invalid",
    "solve_claim_true_invalid",
]

DEEP_RESEARCH_FIXTURE_CASES = [
    "missing_required_field",
    "template_only_misread_attempt",
    "acceptance_decision_present_but_no_activation_acceptance",
    "byte_stream_authorized_invalid",
    "execution_authorized_invalid",
    "warnings_disposition_missing_invalid",
    "stage5bd_preservation_missing_invalid",
    "solve_claim_true_invalid",
]

ACTIVATION_DECISION_FIXTURE_CASES = [
    "missing_operator_approval_path",
    "missing_deep_research_acceptance_path",
    "combined_gate_unsatisfied_invalid",
    "active_planning_input_selected_without_approval_invalid",
    "string4_status_active_invalid",
    "byte_stream_authorized_invalid",
    "execution_authorized_invalid",
    "manifest_supersession_authorized_now_invalid",
    "stage5bd_supersession_missing_invalid",
    "solve_claim_true_invalid",
]

NEGATIVE_MATRIX_CLASSES = [
    *OPERATOR_FIXTURE_CASES,
    *DEEP_RESEARCH_FIXTURE_CASES,
    *ACTIVATION_DECISION_FIXTURE_CASES,
    "fixture_record_passed_as_actual_operator_approval",
    "fixture_record_passed_as_actual_deep_research_acceptance",
    "fixture_record_passed_as_actual_activation_decision",
]

REVIEW_CHECKLIST = [
    "Stage 5CI templates still present and valid.",
    "Stage 5CK fixtures reviewed.",
    "Operator approval record is real, not fixture.",
    "Deep Research acceptance record is real, not fixture.",
    "Combined gate validation proves both approvals are present.",
    "Activation decision references exact Stage 5CE proposal package.",
    "Activation decision references exact Stage 5CG combined gate scaffold.",
    "Activation decision references exact Stage 5CI template versions.",
    "Activation decision references exact Stage 5CK fixture review package if required.",
    "Stage 5BD preservation or explicit future supersession is present.",
    "Active-lineage preservation or explicit future supersession is present.",
    "No-byte-stream transition gate remains closed until a separate byte stage.",
    "No-execution transition gate remains closed until a separate execution stage.",
    "Manifest supersession is explicit if selected; otherwise false.",
    "No solve claim is made.",
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5ck-summary.yaml"),
    "next_stage": Path("data/project-state/stage5ck-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5ck-stage5cj-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5ck-reviewable-stage-marker.yaml"),
    "validation_evidence": Path("data/project-state/stage5ck-reviewable-validation-evidence.yaml"),
    "source_digest_index": Path("data/project-state/stage5ck-reviewable-source-digest-index.yaml"),
    "gap_register": Path("data/project-state/stage5ck-reviewability-gap-register.yaml"),
    "equivalence_map": Path("data/project-state/stage5ck-record-family-name-equivalence-map.yaml"),
    "stage5ci_preservation": Path("data/token-block/stage5ck-stage5ci-template-preservation.yaml"),
    "stage5cg_preservation": Path("data/token-block/stage5ck-stage5cg-scaffold-preservation.yaml"),
    "stage5ce_preservation": Path("data/token-block/stage5ck-stage5ce-proposal-package-preservation.yaml"),
    "stage5cc_preservation": Path("data/token-block/stage5ck-stage5cc-contract-preservation.yaml"),
    "fixture_isolation": Path("data/token-block/stage5ck-fixture-isolation-policy.yaml"),
    "operator_fixtures": Path("data/token-block/stage5ck-operator-approval-fixture-pack.yaml"),
    "deep_research_fixtures": Path("data/token-block/stage5ck-deep-research-acceptance-fixture-pack.yaml"),
    "activation_fixtures": Path("data/token-block/stage5ck-activation-decision-fixture-pack.yaml"),
    "negative_matrix": Path("data/token-block/stage5ck-approval-fixture-negative-validation-matrix.yaml"),
    "review_package": Path("data/token-block/stage5ck-activation-decision-review-package.yaml"),
    "approval_fixture_non_satisfaction": Path(
        "data/token-block/stage5ck-approval-fixture-non-satisfaction-proof.yaml"
    ),
    "combined_gate_non_satisfaction": Path(
        "data/token-block/stage5ck-combined-gate-non-satisfaction-proof.yaml"
    ),
    "activation_invalid": Path("data/token-block/stage5ck-activation-decision-invalid-now-proof.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5ck-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path("data/token-block/stage5ck-no-byte-stream-transition-gate.yaml"),
    "no_execution_transition_gate": Path("data/token-block/stage5ck-no-execution-transition-gate.yaml"),
    "supersession_nonactivation": Path(
        "data/token-block/stage5ck-manifest-supersession-nonactivation-proof.yaml"
    ),
    "stage5bd_preservation": Path("data/token-block/stage5ck-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5ck-active-lineage-preservation.yaml"),
    "sidecar_activation_blocker": Path("data/token-block/stage5ck-sidecar-activation-blocker.yaml"),
    "future_impact": Path("data/token-block/stage5ck-future-dry-run-planning-impact.yaml"),
    "guardrail": Path("data/historical-route/stage5ck-guardrail.yaml"),
    "dwh": Path("data/historical-route/stage5ck-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5ck-source-gap-severity-update.yaml"),
    "handoff": Path("data/source-harvester/stage5ck-codex-handoff-policy.yaml"),
    "review_packaging_warning": Path("data/source-harvester/stage5ck-review-packaging-warning.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}

RECORD_TYPES = {key: f"stage5ck_{key}" for key in DATA_PATHS}

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

FIXTURE_KEYS = {
    "fixture_isolation",
    "operator_fixtures",
    "deep_research_fixtures",
    "activation_fixtures",
    "negative_matrix",
    "review_package",
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


def _schema(record_type: str, *, fixture_record: bool) -> dict[str, Any]:
    false_properties = {
        name: {"const": False}
        for name in FALSE_FLAGS
        if name not in {"solve_claim", "execution_allowed"}
    }
    properties: dict[str, Any] = {
        "record_type": {"const": record_type},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "solve_claim": {"const": False},
        "execution_allowed": {"const": False},
        **false_properties,
    }
    if fixture_record:
        properties.update(
            {
                "fixture_pack_only": {"const": True},
                "fixtures_may_satisfy_real_gate": {"const": False},
                "fixtures_may_authorize_activation": {"const": False},
                "fixtures_may_authorize_execution": {"const": False},
            }
        )
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
        "properties": properties,
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, schema_path in SCHEMA_PATHS.items():
        path = Path(schema_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                _schema(RECORD_TYPES[key], fixture_record=key in FIXTURE_KEYS),
                indent=2,
                sort_keys=True,
            )
            + "\n",
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
        STAGE5CJ_REPORT_PATH.as_posix(),
        *[path.as_posix() for path in STAGE5CI_DATA_PATHS.values()],
        "data/project-state/stage5cg-summary.yaml",
        "data/project-state/stage5ce-summary.yaml",
        "data/project-state/stage5cc-summary.yaml",
        "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
        "data/token-block/stage5bd-run-plan-id-registry.yaml",
        "README.md",
        "STATUS.md",
        "AGENTS.md",
        "ROADMAP.md",
        "TESTING.md",
        "RESULTS_SCHEMA.md",
        "EXPERIMENTS.md",
        "CIPHER_CATALOG.md",
        "docs/roadmap/staged-plan.md",
        "docs/onboarding/start-here.md",
        "docs/onboarding/source-of-truth-map.md",
        "docs/onboarding/operational-file-map.md",
        "docs/onboarding/codex-navigation-map.md",
        "docs/onboarding/deep-research-handoff-map.md",
        "docs/reference/token-block-cli.md",
    ]
    paths.extend(ACTIVE_LINEAGE_PATHS)
    return sorted(dict.fromkeys(paths))


def _validation_commands() -> list[dict[str, Any]]:
    commands = [
        "python -m libreprimus.cli token-block build-stage5ck",
        "python -m libreprimus.cli token-block validate-stage5ck-operator-fixtures",
        "python -m libreprimus.cli token-block validate-stage5ck-deep-research-fixtures",
        "python -m libreprimus.cli token-block validate-stage5ck-activation-decision-fixtures",
        "python -m libreprimus.cli token-block validate-stage5ck-negative-validation-matrix",
        "python -m libreprimus.cli token-block validate-stage5ck-review-package",
        "python -m libreprimus.cli token-block validate-stage5ck-sidecar-gates",
        "python -m libreprimus.cli token-block validate-stage5ck",
        "python -m libreprimus.cli token-block stage5ck-summary",
        "python -m libreprimus.cli token-block validate-stage5ci",
        "python -m libreprimus.cli token-block validate-stage5cg",
        "python -m libreprimus.cli token-block validate-stage5ce",
        "python -m libreprimus.cli token-block validate-stage5cc",
        "python -m libreprimus.cli token-block validate-stage5ca",
        "python -m libreprimus.cli token-block validate-stage5bd --results-dir experiments/results/token-block/stage5bd",
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


def _fixture(fixture_id: str, case: str, *, family: str) -> dict[str, Any]:
    return {
        "fixture_id": fixture_id,
        "fixture_family": family,
        "fixture_case": case,
        "fixture_only": True,
        "fixture_mode_required": True,
        "actual_approval_record": False,
        "actual_operator_approval_record": False,
        "actual_acceptance_record": False,
        "actual_deep_research_acceptance_record": False,
        "actual_activation_decision_record": False,
        "may_satisfy_real_gate": False,
        "may_authorize_activation": False,
        "may_authorize_active_input": False,
        "may_authorize_byte_streams": False,
        "may_authorize_execution": False,
        "expected_fixture_validation_status": "valid_fixture_invalid_actual_record",
    }


def _fixture_pack(
    key: str,
    cases: list[str],
    *,
    family: str,
    created_field: str,
    satisfy_field: str,
    actual_field: str,
) -> dict[str, Any]:
    fixtures = [
        _fixture(f"{STAGE_ID}-{family}-{case}", case, family=family)
        for case in cases
    ]
    return _record(
        key,
        {
            "fixture_pack_created": True,
            "fixture_pack_only": True,
            "synthetic_negative_fixtures_only": True,
            "fixture_records_created": True,
            created_field: True,
            actual_field: False,
            satisfy_field: False,
            "real_approval_records_created": False,
            "real_activation_records_created": False,
            "fixtures_may_satisfy_real_gate": False,
            "fixtures_may_authorize_activation": False,
            "fixtures_may_authorize_execution": False,
            "fixture_cases": cases,
            "fixture_records": fixtures,
            "fixture_record_count": len(fixtures),
        },
    )


def _non_satisfaction_body(run_plan_count: int) -> dict[str, Any]:
    return {
        "operator_approval_record_present_now": False,
        "deep_research_activation_accept_record_present_now": False,
        "combined_approval_gate_satisfied_now": False,
        "combined_approval_gate_authorizes_activation_now": False,
        "activation_decision_valid_now": False,
        "activation_authorized_now": False,
        "active_planning_input_authorized_now": False,
        "active_planning_input_selected_now": False,
        "new_active_planning_input_created": False,
        "string4_sidecar_status": "scaffolded_inactive",
        "string4_active_input_allowed": False,
        "string4_dry_run_ingestion_allowed_now": False,
        "string4_byte_stream_generation_allowed": False,
        "string4_execution_input_allowed": False,
        "manifest_supersession_performed": False,
        "stage5bd_run_plan_id_count": run_plan_count,
        "stage5bd_run_plan_ids_changed": False,
        "token_block_experiment_executed": False,
        "solve_claim": False,
    }


def _build_records(source_records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    run_plan_count = _run_plan_count()
    stage5ci_summary = _read(STAGE5CI_DATA_PATHS["summary"])
    active_lineage_records = [_sha_record(Path(path), role="stage5ck_active_lineage") for path in ACTIVE_LINEAGE_PATHS]
    source_unique_count = len({record["path"] for record in source_records})
    source_digest_count = int(stage5ci_summary.get("source_digest_record_count", 0))
    common_proof = _non_satisfaction_body(run_plan_count)

    records: dict[str, dict[str, Any]] = {
        "findings": _record(
            "findings",
            {
                "stage5cj_findings_integrated": True,
                "stage5cj_verdict": "accept_with_warnings",
                "findings": STAGE5CJ_FINDINGS,
                "warnings": STAGE5CJ_WARNINGS,
                "warnings_gate_opening": False,
                "stage5ci_safe_to_build_on": True,
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
                "stage5cj_report_present": STAGE5CJ_REPORT_PATH.is_file(),
            },
        ),
        "gap_register": _record(
            "gap_register",
            {
                "reviewability_gap_status": "warnings_preserved_non_gate_opening",
                "gaps": [
                    {
                        "gap_id": "attached_zip_not_pristine_checkout",
                        "severity": "warning",
                        "gate_opener": False,
                        "disposition": "preserved_from_stage5cj",
                    },
                    {
                        "gap_id": "public_github_corroboration_unreliable",
                        "severity": "warning",
                        "gate_opener": False,
                        "disposition": "external_evidence_caveat_preserved",
                    },
                    {
                        "gap_id": "final_commit_and_ci_external_evidence",
                        "severity": "expected_external_evidence",
                        "gate_opener": False,
                        "disposition": "post_push_verification_required",
                    },
                    {
                        "gap_id": "negative_validation_split_across_tests",
                        "severity": "warning",
                        "gate_opener": False,
                        "disposition": "closed_by_fixture_packaging",
                    },
                ],
                "gate_opening_gap_count": 0,
            },
        ),
        "equivalence_map": _record(
            "equivalence_map",
            {
                "record_family_equivalence_status": "explicit",
                "equivalence_families": [
                    {
                        "family_id": "stage5ci_template_family",
                        "paths": [
                            STAGE5CI_DATA_PATHS["operator_template"].as_posix(),
                            STAGE5CI_DATA_PATHS["deep_research_template"].as_posix(),
                            STAGE5CI_DATA_PATHS["combined_gate"].as_posix(),
                            STAGE5CI_DATA_PATHS["activation_template"].as_posix(),
                            STAGE5CI_DATA_PATHS["negative_contract"].as_posix(),
                        ],
                    },
                    {
                        "family_id": "stage5ck_fixture_pack_family",
                        "paths": [
                            DATA_PATHS["operator_fixtures"].as_posix(),
                            DATA_PATHS["deep_research_fixtures"].as_posix(),
                            DATA_PATHS["activation_fixtures"].as_posix(),
                            DATA_PATHS["negative_matrix"].as_posix(),
                            DATA_PATHS["review_package"].as_posix(),
                        ],
                    },
                ],
            },
        ),
        "stage5ci_preservation": _record(
            "stage5ci_preservation",
            {
                "stage5ci_status_preserved": True,
                "stage5ci_operator_approval_template_preserved": True,
                "stage5ci_deep_research_acceptance_template_preserved": True,
                "stage5ci_combined_approval_gate_validation_preserved": True,
                "stage5ci_activation_decision_template_preserved": True,
                "stage5ci_negative_validation_contract_preserved": True,
                "stage5ci_summary_sha256": sha256_file(STAGE5CI_DATA_PATHS["summary"]),
                "stage5ci_source_digest_record_count_preserved": source_digest_count,
            },
        ),
        "stage5cg_preservation": _record(
            "stage5cg_preservation",
            {
                "stage5cg_scaffolds_preserved": True,
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
        "fixture_isolation": _record(
            "fixture_isolation",
            {
                "fixture_pack_created": True,
                "fixture_pack_only": True,
                "fixture_isolation_policy_status": "active",
                "synthetic_negative_fixtures_only": True,
                "fixture_records_created": True,
                "real_approval_records_created": False,
                "real_deep_research_acceptance_records_created": False,
                "real_activation_decision_records_created": False,
                "fixtures_may_satisfy_real_gate": False,
                "fixtures_may_authorize_activation": False,
                "fixtures_may_authorize_execution": False,
                "fixtures_must_be_rejected_as_actual_records": True,
            },
        ),
        "operator_fixtures": _fixture_pack(
            "operator_fixtures",
            OPERATOR_FIXTURE_CASES,
            family="operator-approval",
            created_field="operator_approval_fixture_records_created",
            satisfy_field="operator_approval_fixture_records_satisfy_approval",
            actual_field="actual_operator_approval_records_created",
        ),
        "deep_research_fixtures": _fixture_pack(
            "deep_research_fixtures",
            DEEP_RESEARCH_FIXTURE_CASES,
            family="deep-research-acceptance",
            created_field="deep_research_acceptance_fixture_records_created",
            satisfy_field="deep_research_acceptance_fixture_records_satisfy_acceptance",
            actual_field="actual_deep_research_acceptance_records_created",
        ),
        "activation_fixtures": _fixture_pack(
            "activation_fixtures",
            ACTIVATION_DECISION_FIXTURE_CASES,
            family="activation-decision",
            created_field="activation_decision_fixture_records_created",
            satisfy_field="activation_decision_fixture_records_valid_now",
            actual_field="actual_activation_decision_records_created",
        ),
        "negative_matrix": _record(
            "negative_matrix",
            {
                "fixture_pack_created": True,
                "fixture_pack_only": True,
                "synthetic_negative_fixtures_only": True,
                "negative_validation_matrix_status": "active",
                "negative_validation_classes": sorted(set(NEGATIVE_MATRIX_CLASSES)),
                "negative_validation_class_count": len(set(NEGATIVE_MATRIX_CLASSES)),
                "fixtures_may_satisfy_real_gate": False,
                "fixtures_may_authorize_activation": False,
                "fixtures_may_authorize_execution": False,
                "fixture_records_rejected_as_actual_records": True,
                "real_approval_records_created": False,
                "real_activation_records_created": False,
            },
        ),
        "review_package": _record(
            "review_package",
            {
                "activation_decision_review_package_created": True,
                "activation_decision_review_package_status": "review_package_only",
                "activation_decision_review_package_authorizes_activation": False,
                "activation_decision_review_package_authorizes_active_input": False,
                "activation_decision_review_package_authorizes_dry_run_ingestion": False,
                "activation_decision_review_package_authorizes_byte_stream_generation": False,
                "activation_decision_review_package_authorizes_execution": False,
                "fixture_pack_only": True,
                "fixtures_may_satisfy_real_gate": False,
                "fixtures_may_authorize_activation": False,
                "fixtures_may_authorize_execution": False,
                "review_checklist": REVIEW_CHECKLIST,
                "review_checklist_count": len(REVIEW_CHECKLIST),
            },
        ),
        "approval_fixture_non_satisfaction": _record(
            "approval_fixture_non_satisfaction",
            {
                "approval_fixture_non_satisfaction_proof_status": "closed",
                "fixture_records_created": True,
                "fixture_records_satisfy_approval": False,
                **common_proof,
            },
        ),
        "combined_gate_non_satisfaction": _record(
            "combined_gate_non_satisfaction",
            {
                "combined_gate_non_satisfaction_proof_status": "closed",
                **common_proof,
            },
        ),
        "activation_invalid": _record(
            "activation_invalid",
            {
                "activation_decision_invalid_now_proof_status": "closed",
                "activation_decision_fixture_records_valid_now": False,
                **common_proof,
            },
        ),
        "no_active_ingestion": _record(
            "no_active_ingestion",
            {
                "no_active_ingestion_proof_status": "closed",
                **common_proof,
            },
        ),
        "no_byte_stream_transition_gate": _record(
            "no_byte_stream_transition_gate",
            {
                "no_byte_stream_transition_gate_status": "closed",
                "blocked_actions": BLOCKED_BYTE_STREAM_ACTIONS,
                **common_proof,
            },
        ),
        "no_execution_transition_gate": _record(
            "no_execution_transition_gate",
            {
                "no_execution_transition_gate_status": "closed",
                **common_proof,
            },
        ),
        "supersession_nonactivation": _record(
            "supersession_nonactivation",
            {
                "manifest_supersession_preflight_status": "carried_forward_unperformed",
                "manifest_supersession_performed": False,
                "manifest_supersession_authorized_now": False,
                "active_manifest_registry_updated": False,
                **common_proof,
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
                "string4_added_to_stage5bd_run_plan_ids": False,
                "string4_added_to_active_dry_run_inputs": False,
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
                "raw_or_generated_body_committed": False,
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
                "source_gap_updates": sorted(STAGE5CJ_WARNINGS),
                "gate_opener": False,
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
                "selected_next_stage_id": "stage-5cl",
                "selected_next_stage_title": (
                    "Stage 5CL - Deep Research review of Stage 5CK approval-record "
                    "validation fixture pack and activation-decision review package, "
                    "without execution"
                ),
                "selected_next_prompt_type": "deep_research_review",
                "selected_next_stage_authorizes_execution": False,
                "selected_next_stage_reason": (
                    "Stage 5CK creates fixture-only validation records and an "
                    "activation-decision review package; independent Deep Research "
                    "review is required before any future approval-record validation "
                    "package or activation-decision readiness scaffold."
                ),
            },
        ),
    }

    summary_body = {
        "status": "complete",
        "stage5cj_findings_integrated": True,
        "stage5cj_verdict": "accept_with_warnings",
        "stage5ci_status_preserved": True,
        "stage5ci_operator_approval_template_preserved": True,
        "stage5ci_deep_research_acceptance_template_preserved": True,
        "stage5ci_combined_approval_gate_validation_preserved": True,
        "stage5ci_activation_decision_template_preserved": True,
        "stage5ci_negative_validation_contract_preserved": True,
        "fixture_pack_created": True,
        "fixture_pack_only": True,
        "synthetic_negative_fixtures_only": True,
        "real_approval_records_created": False,
        "real_deep_research_acceptance_records_created": False,
        "real_activation_decision_records_created": False,
        "operator_approval_fixture_pack_created": True,
        "operator_approval_fixture_records_created": True,
        "operator_approval_fixture_records_satisfy_approval": False,
        "operator_approval_record_created_now": False,
        "operator_approval_record_present_now": False,
        "operator_approval_satisfied_now": False,
        "operator_approval_authorizes_activation_now": False,
        "deep_research_acceptance_fixture_pack_created": True,
        "deep_research_acceptance_fixture_records_created": True,
        "deep_research_acceptance_fixture_records_satisfy_acceptance": False,
        "deep_research_activation_accept_record_created_now": False,
        "deep_research_activation_accept_record_present_now": False,
        "deep_research_activation_accept_satisfied_now": False,
        "deep_research_acceptance_authorizes_activation_now": False,
        "activation_decision_fixture_pack_created": True,
        "activation_decision_fixture_records_created": True,
        "activation_decision_fixture_records_valid_now": False,
        "active_planning_input_decision_record_created_now": False,
        "activation_decision_valid_now": False,
        "activation_authorized_now": False,
        "combined_approval_gate_fixture_validation_created": True,
        "combined_approval_gate_satisfied_now": False,
        "combined_approval_gate_authorizes_activation_now": False,
        "approval_gate_satisfied_now": False,
        "approval_gate_authorizes_activation_now": False,
        "activation_decision_review_package_created": True,
        "activation_decision_review_package_status": "review_package_only",
        "activation_decision_review_package_authorizes_activation": False,
        "stage5ce_proposal_package_status_preserved": "review_package_only",
        "stage5cg_scaffolds_preserved": True,
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
        "operator_fixture_case_count": len(OPERATOR_FIXTURE_CASES),
        "deep_research_fixture_case_count": len(DEEP_RESEARCH_FIXTURE_CASES),
        "activation_decision_fixture_case_count": len(ACTIVATION_DECISION_FIXTURE_CASES),
        "negative_validation_class_count": len(set(NEGATIVE_MATRIX_CLASSES)),
        "source_digest_record_count": len(source_records),
        "source_digest_unique_path_count": source_unique_count,
        "stage5ci_source_digest_record_count_preserved": source_digest_count,
        "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
        "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
        "recommended_next_stage_id": "stage-5cl",
        "recommended_next_stage_title": records["next_stage"]["selected_next_stage_title"],
    }
    summary_body.update(FALSE_FLAGS)
    records["summary"] = _record("summary", summary_body, include_false_flags=False)
    return records


def build_stage5ck(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    """Build Stage 5CK committed metadata and ignored fixture reports."""

    _write_schemas()
    results_dir.mkdir(parents=True, exist_ok=True)
    source_records = [_sha_record(Path(path), role="stage5ck_reviewable_source") for path in _source_paths()]
    records = _build_records(source_records)
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    write_json(results_dir / "summary.json", records["summary"])
    write_json(
        results_dir / "fixture_pack_report.json",
        {
            "operator_fixtures": records["operator_fixtures"],
            "deep_research_fixtures": records["deep_research_fixtures"],
            "activation_fixtures": records["activation_fixtures"],
        },
    )
    write_json(results_dir / "activation_decision_review_package.json", records["review_package"])
    write_json(results_dir / "combined_gate_validation.json", records["combined_gate_non_satisfaction"])
    write_json(results_dir / "negative_validation_matrix.json", records["negative_matrix"])
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


def _check_fixture_common(payload: dict[str, Any], errors: list[str], *, label: str) -> None:
    for field in (
        "fixture_pack_created",
        "fixture_pack_only",
        "synthetic_negative_fixtures_only",
        "fixture_records_created",
    ):
        if payload.get(field) is not True:
            errors.append(f"{label} {field} must be true")
    for field in (
        "real_approval_records_created",
        "real_activation_records_created",
        "fixtures_may_satisfy_real_gate",
        "fixtures_may_authorize_activation",
        "fixtures_may_authorize_execution",
    ):
        if payload.get(field) is not False:
            errors.append(f"{label} {field} must be false")
    for fixture in payload.get("fixture_records", []):
        for field in (
            "fixture_only",
            "fixture_mode_required",
        ):
            if fixture.get(field) is not True:
                errors.append(f"{label} fixture {fixture.get('fixture_id')} {field} must be true")
        for field in (
            "actual_approval_record",
            "actual_operator_approval_record",
            "actual_acceptance_record",
            "actual_deep_research_acceptance_record",
            "actual_activation_decision_record",
            "may_satisfy_real_gate",
            "may_authorize_activation",
            "may_authorize_active_input",
            "may_authorize_byte_streams",
            "may_authorize_execution",
        ):
            if fixture.get(field) is not False:
                errors.append(f"{label} fixture {fixture.get('fixture_id')} {field} must be false")


def _check_fixture_cases(
    payload: dict[str, Any],
    expected_cases: list[str],
    errors: list[str],
    *,
    label: str,
) -> None:
    observed = [str(case) for case in payload.get("fixture_cases", [])]
    missing = sorted(set(expected_cases) - set(observed))
    errors.extend(f"{label} missing_fixture_case={case}" for case in missing)
    fixture_cases = [str(fixture.get("fixture_case")) for fixture in payload.get("fixture_records", [])]
    missing_records = sorted(set(expected_cases) - set(fixture_cases))
    errors.extend(f"{label} missing_fixture_record_case={case}" for case in missing_records)


def validate_stage5ck_actual_record_rejection(payload: dict[str, Any]) -> list[str]:
    """Return errors proving a fixture/template cannot be treated as a real record."""

    errors: list[str] = []
    if payload.get("fixture_only") is True or payload.get("fixture_pack_only") is True:
        errors.append("fixture record cannot be accepted as an actual approval or activation record")
    if payload.get("template_only") is True:
        errors.append("template record cannot be accepted as an actual approval or activation record")
    for field in (
        "may_satisfy_real_gate",
        "may_authorize_activation",
        "may_authorize_active_input",
        "may_authorize_byte_streams",
        "may_authorize_execution",
    ):
        if payload.get(field) is True:
            errors.append(f"{field} must not be true for actual-record validation")
    return errors


def validate_stage5ck_operator_fixtures(
    *, operator_fixtures: Path = DATA_PATHS["operator_fixtures"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(operator_fixtures, errors)
    _check_fixture_common(payload, errors, label="operator_fixtures")
    _check_fixture_cases(payload, OPERATOR_FIXTURE_CASES, errors, label="operator_fixtures")
    if payload.get("actual_operator_approval_records_created") is not False:
        errors.append("operator fixtures must not create actual approval records")
    if payload.get("operator_approval_fixture_records_satisfy_approval") is not False:
        errors.append("operator fixtures must not satisfy approval")
    for fixture in payload.get("fixture_records", []):
        if not validate_stage5ck_actual_record_rejection(fixture):
            errors.append(f"fixture accepted as actual record: {fixture.get('fixture_id')}")
    return {
        "stage5ck_operator_fixtures_valid": not errors,
        "fixture_record_count": len(payload.get("fixture_records", [])),
        "operator_approval_fixture_records_satisfy_approval": payload.get(
            "operator_approval_fixture_records_satisfy_approval"
        ),
        "actual_operator_approval_records_created": payload.get(
            "actual_operator_approval_records_created"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5ck_deep_research_fixtures(
    *, deep_research_fixtures: Path = DATA_PATHS["deep_research_fixtures"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(deep_research_fixtures, errors)
    _check_fixture_common(payload, errors, label="deep_research_fixtures")
    _check_fixture_cases(payload, DEEP_RESEARCH_FIXTURE_CASES, errors, label="deep_research_fixtures")
    if payload.get("actual_deep_research_acceptance_records_created") is not False:
        errors.append("Deep Research fixtures must not create actual acceptance records")
    if payload.get("deep_research_acceptance_fixture_records_satisfy_acceptance") is not False:
        errors.append("Deep Research fixtures must not satisfy acceptance")
    for fixture in payload.get("fixture_records", []):
        if not validate_stage5ck_actual_record_rejection(fixture):
            errors.append(f"fixture accepted as actual record: {fixture.get('fixture_id')}")
    return {
        "stage5ck_deep_research_fixtures_valid": not errors,
        "fixture_record_count": len(payload.get("fixture_records", [])),
        "deep_research_acceptance_fixture_records_satisfy_acceptance": payload.get(
            "deep_research_acceptance_fixture_records_satisfy_acceptance"
        ),
        "actual_deep_research_acceptance_records_created": payload.get(
            "actual_deep_research_acceptance_records_created"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5ck_activation_decision_fixtures(
    *, activation_fixtures: Path = DATA_PATHS["activation_fixtures"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(activation_fixtures, errors)
    _check_fixture_common(payload, errors, label="activation_fixtures")
    _check_fixture_cases(payload, ACTIVATION_DECISION_FIXTURE_CASES, errors, label="activation_fixtures")
    if payload.get("actual_activation_decision_records_created") is not False:
        errors.append("activation fixtures must not create actual activation decisions")
    if payload.get("activation_decision_fixture_records_valid_now") is not False:
        errors.append("activation fixtures must be invalid as current activation decisions")
    for fixture in payload.get("fixture_records", []):
        if not validate_stage5ck_actual_record_rejection(fixture):
            errors.append(f"fixture accepted as actual record: {fixture.get('fixture_id')}")
    return {
        "stage5ck_activation_decision_fixtures_valid": not errors,
        "fixture_record_count": len(payload.get("fixture_records", [])),
        "activation_decision_fixture_records_valid_now": payload.get(
            "activation_decision_fixture_records_valid_now"
        ),
        "actual_activation_decision_records_created": payload.get(
            "actual_activation_decision_records_created"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5ck_negative_validation_matrix(
    *, negative_matrix: Path = DATA_PATHS["negative_matrix"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(negative_matrix, errors)
    expected = set(NEGATIVE_MATRIX_CLASSES)
    observed = set(payload.get("negative_validation_classes", []))
    for item in sorted(expected - observed):
        errors.append(f"missing_negative_validation_class={item}")
    if payload.get("fixture_records_rejected_as_actual_records") is not True:
        errors.append("negative matrix must reject fixture records as actual records")
    for field in (
        "fixtures_may_satisfy_real_gate",
        "fixtures_may_authorize_activation",
        "fixtures_may_authorize_execution",
        "real_approval_records_created",
        "real_activation_records_created",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5ck_negative_validation_matrix_valid": not errors,
        "negative_validation_class_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5ck_review_package(
    *, review_package: Path = DATA_PATHS["review_package"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(review_package, errors)
    if payload.get("activation_decision_review_package_created") is not True:
        errors.append("activation-decision review package must be created")
    if payload.get("activation_decision_review_package_status") != "review_package_only":
        errors.append("activation-decision review package must be review_package_only")
    for field in (
        "activation_decision_review_package_authorizes_activation",
        "activation_decision_review_package_authorizes_active_input",
        "activation_decision_review_package_authorizes_dry_run_ingestion",
        "activation_decision_review_package_authorizes_byte_stream_generation",
        "activation_decision_review_package_authorizes_execution",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    if len(payload.get("review_checklist", [])) < len(REVIEW_CHECKLIST):
        errors.append("review checklist is incomplete")
    return {
        "stage5ck_review_package_valid": not errors,
        "activation_decision_review_package_status": payload.get(
            "activation_decision_review_package_status"
        ),
        "activation_decision_review_package_authorizes_activation": payload.get(
            "activation_decision_review_package_authorizes_activation"
        ),
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


def validate_stage5ck_sidecar_gates(
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
        "stage5ck_sidecar_gates_valid": not errors,
        "string4_sidecar_status": payloads["no_active_ingestion"].get("string4_sidecar_status"),
        "no_byte_stream_transition_gate_status": payloads["no_byte_stream_transition_gate"].get(
            "no_byte_stream_transition_gate_status"
        ),
        "no_execution_transition_gate_status": payloads["no_execution_transition_gate"].get(
            "no_execution_transition_gate_status"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5ck(
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
        validate_stage5ck_operator_fixtures(),
        validate_stage5ck_deep_research_fixtures(),
        validate_stage5ck_activation_decision_fixtures(),
        validate_stage5ck_negative_validation_matrix(),
        validate_stage5ck_review_package(),
        validate_stage5ck_sidecar_gates(),
    ):
        errors.extend(focused_errors)

    for label, validator in (
        ("stage5ci", lambda: validate_stage5ci(results_dir=STAGE5CI_RESULTS_DIR)),
        ("stage5cg", lambda: validate_stage5cg(results_dir=STAGE5CG_RESULTS_DIR)),
        ("stage5ce", lambda: validate_stage5ce(results_dir=STAGE5CE_RESULTS_DIR)),
        ("stage5ca_citation", validate_stage5ca_citation_contract),
        ("stage5cc_triggers", validate_stage5cc_fail_closed_triggers),
        ("stage5cc_preconditions", validate_stage5cc_activation_preconditions),
        ("stage5cc", validate_stage5cc),
    ):
        _, validator_errors = validator()
        errors.extend(f"{label}:{error}" for error in validator_errors)

    if summary_payload.get("stage5cj_verdict") != "accept_with_warnings":
        errors.append("Stage 5CJ verdict must be accept_with_warnings")
    for key in (
        "fixture_pack_created",
        "operator_approval_fixture_pack_created",
        "deep_research_acceptance_fixture_pack_created",
        "activation_decision_fixture_pack_created",
        "activation_decision_review_package_created",
    ):
        if summary_payload.get(key) is not True:
            errors.append(f"summary {key} must be true")
    for key in (
        "real_approval_records_created",
        "real_deep_research_acceptance_records_created",
        "real_activation_decision_records_created",
        "operator_approval_fixture_records_satisfy_approval",
        "deep_research_acceptance_fixture_records_satisfy_acceptance",
        "activation_decision_fixture_records_valid_now",
        "combined_approval_gate_satisfied_now",
        "activation_decision_valid_now",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
    ):
        if summary_payload.get(key) is not False:
            errors.append(f"summary {key} must be false")
    if summary_payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    if summary_payload.get("active_lineage_record_count") != 8:
        errors.append("active-lineage record count must remain 8")
    if next_payload.get("selected_next_stage_id") != "stage-5cl":
        errors.append("Stage 5CK must select Stage 5CL as next stage")
    if next_payload.get("selected_next_stage_authorizes_execution") is not False:
        errors.append("Stage 5CL must not authorize execution")
    if guardrail_payload.get("future_token_block_execution_remains_blocked") is not True:
        errors.append("future token-block execution must remain blocked")

    digest_paths = [record.get("path") for record in payloads["source_digest_index"].get("source_records", [])]
    duplicate_paths = [path for path, count in Counter(digest_paths).items() if count > 1]
    errors.extend(f"stage5ck_duplicate_source_digest_path={path}" for path in duplicate_paths)

    gap_ids = {gap.get("gap_id") for gap in payloads["gap_register"].get("gaps", [])}
    for required_gap in {
        "attached_zip_not_pristine_checkout",
        "public_github_corroboration_unreliable",
        "final_commit_and_ci_external_evidence",
        "negative_validation_split_across_tests",
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
        errors.append("Stage 5CK must use codex-output as handoff root")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output directory must be absent/unused")

    generated_summary_present = (results_dir / "summary.json").is_file()
    return {
        "stage5ck_valid": not errors,
        "validation_error_count": len(errors),
        "stage5cj_verdict": summary_payload.get("stage5cj_verdict"),
        "fixture_pack_created": summary_payload.get("fixture_pack_created"),
        "fixture_pack_only": summary_payload.get("fixture_pack_only"),
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


def load_stage5ck_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    """Load the Stage 5CK summary."""

    return _read(summary)
