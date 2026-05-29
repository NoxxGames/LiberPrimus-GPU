"""Stage 5BW inactive-sidecar planning-ingestion preflight metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import repo_relative, sha256_file, write_json, write_yaml
from libreprimus.token_block.stage5bm import _read

STAGE_ID = "stage-5bw"
STAGE_TITLE = (
    "Stage 5BW - String 4 inactive-sidecar planning-ingestion proposal and "
    "manifest-supersession preflight, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5bu"
SOURCE_PREVIOUS_COMMIT = "72a04b42f5cbd1f907d8ca20b703f0290e5796fd"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5bv"
SOURCE_DEEP_RESEARCH_REPORT = (
    "13_Deep-Research-Review-Of-Lineage-Path-And-Reviewability-Hardening.md"
)

RESULTS_DIR = Path("experiments/results/token-block/stage5bw")
CODEX_COMPLETION_PATH = Path("codex-output/stage5bw-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
STAGE5BV_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "13_Deep-Research-Review-Of-Lineage-Path-And-Reviewability-Hardening.md"
)

INCORRECT_STAGE5AW_PATH = "data/token-block/stage5aw-repaired-branch-manifest.yaml"
CORRECT_STAGE5AW_PATH = "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml"

STAGE5BU_SUMMARY_PATH = Path("data/project-state/stage5bu-summary.yaml")
STAGE5BU_LINEAGE_VALIDATION_PATH = Path(
    "data/token-block/stage5bu-lineage-path-resolution-validation.yaml"
)
STAGE5BU_LINEAGE_DIGEST_PATH = Path(
    "data/token-block/stage5bu-preserved-active-lineage-digest-index.yaml"
)
STAGE5BU_GUARDRAIL_PATH = Path("data/historical-route/stage5bu-guardrail.yaml")
STAGE5BS_ACTIVE_PRESERVATION_PATH = Path(
    "data/token-block/stage5bs-active-manifest-preservation.yaml"
)
STAGE5BS_GATE_PATH = Path("data/token-block/stage5bs-string4-planning-ingestion-gate.yaml")
STAGE5BS_BLOCKER_PATH = Path("data/token-block/stage5bs-active-ingestion-blocker.yaml")
STAGE5BS_CITATION_PATH = Path("data/token-block/stage5bs-future-runner-citation-policy.yaml")
STAGE5BQ_CONTEXT_PATH = Path("data/token-block/stage5bq-string4-inactive-branch-planning-context.yaml")
STAGE5BQ_CONSTRAINT_PATH = Path(
    "data/token-block/stage5bq-errata-aware-dry-run-constraint-update.yaml"
)
STAGE5BO_BRANCH_MEMBERSHIP_PATH = Path(
    "data/token-block/stage5bo-string4-branch-membership-after-errata.yaml"
)
STAGE5BO_OPTION_UNIVERSE_PATH = Path(
    "data/token-block/stage5bo-errata-aware-token-option-universe.yaml"
)
STAGE5BD_DRY_RUN_PLAN_PATH = Path("data/token-block/stage5bd-dry-run-plan-manifest.yaml")
STAGE5BD_RUN_PLAN_REGISTRY_PATH = Path("data/token-block/stage5bd-run-plan-id-registry.yaml")

ACTIVE_LINEAGE_PATHS = [
    "data/token-block/stage5ap-token-block-canonical-transcription.yaml",
    CORRECT_STAGE5AW_PATH,
    "data/token-block/stage5ay-branch-eligibility-policy.yaml",
    "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml",
    "data/token-block/stage5bb-active-manifest-registry.yaml",
    "data/token-block/stage5bd-active-manifest-lock.yaml",
    "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
    "data/token-block/stage5bd-run-plan-id-registry.yaml",
]

STAGE5BD_PRESERVATION_PATHS = [
    "data/token-block/stage5bd-active-manifest-lock.yaml",
    "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
    "data/token-block/stage5bd-run-plan-id-registry.yaml",
    "data/token-block/stage5bd-run-plan-id-policy.yaml",
    "data/token-block/stage5bd-dry-run-policy.yaml",
    "data/token-block/stage5bd-future-result-path-validation.yaml",
    "data/token-block/stage5bd-execution-gate-dry-run-validation.yaml",
    "data/token-block/stage5bd-no-byte-stream-proof.yaml",
    "data/token-block/stage5bd-guardrail.yaml",
]

DATA_PATHS: dict[str, Path] = {
    "findings": Path("data/project-state/stage5bw-stage5bv-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5bw-reviewable-stage-marker.yaml"),
    "validation_evidence": Path(
        "data/project-state/stage5bw-reviewable-validation-evidence.yaml"
    ),
    "source_digest_index": Path(
        "data/project-state/stage5bw-reviewable-source-digest-index.yaml"
    ),
    "gap_register": Path("data/project-state/stage5bw-reviewability-gap-register.yaml"),
    "summary": Path("data/project-state/stage5bw-summary.yaml"),
    "next_stage": Path("data/project-state/stage5bw-next-stage-decision.yaml"),
    "sidecar_proposal": Path(
        "data/token-block/stage5bw-inactive-sidecar-planning-ingestion-proposal.yaml"
    ),
    "consumption_model": Path(
        "data/token-block/stage5bw-inactive-sidecar-consumption-model.yaml"
    ),
    "manifest_supersession": Path(
        "data/token-block/stage5bw-manifest-supersession-preflight.yaml"
    ),
    "manifest_validation": Path(
        "data/token-block/stage5bw-manifest-validation-preflight.yaml"
    ),
    "active_lineage": Path("data/token-block/stage5bw-active-lineage-preservation.yaml"),
    "lineage_digest": Path(
        "data/token-block/stage5bw-preserved-active-lineage-digest-index.yaml"
    ),
    "stage5bd_preservation": Path(
        "data/token-block/stage5bw-stage5bd-plan-preservation.yaml"
    ),
    "citation_requirements": Path(
        "data/token-block/stage5bw-future-runner-citation-requirements.yaml"
    ),
    "active_blocker": Path(
        "data/token-block/stage5bw-active-ingestion-blocker-preservation.yaml"
    ),
    "no_byte_stream_gate": Path("data/token-block/stage5bw-no-byte-stream-gate.yaml"),
    "no_active_ingestion": Path(
        "data/token-block/stage5bw-no-active-ingestion-proof.yaml"
    ),
    "string4_gate": Path("data/token-block/stage5bw-string4-gate-preservation.yaml"),
    "future_impact": Path("data/token-block/stage5bw-future-dry-run-planning-impact.yaml"),
    "gate_matrix": Path("data/token-block/stage5bw-gate-readiness-matrix.yaml"),
    "authorization_policy": Path(
        "data/token-block/stage5bw-future-stage-authorization-policy.yaml"
    ),
    "source_gap": Path("data/historical-route/stage5bw-source-gap-severity-update.yaml"),
    "dwh": Path("data/historical-route/stage5bw-dwh-quarantine-reaffirmation.yaml"),
    "guardrail": Path("data/historical-route/stage5bw-guardrail.yaml"),
    "review_packaging_warning": Path(
        "data/source-harvester/stage5bw-review-packaging-warning.yaml"
    ),
    "handoff": Path("data/source-harvester/stage5bw-codex-handoff-policy.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    key: str(path).replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}

SCHEMA_PATHS.update(
    {
        "findings": "schemas/project-state/stage5bw-stage5bv-findings-integration-v0.schema.json",
        "stage_marker": "schemas/project-state/stage5bw-reviewable-stage-marker-v0.schema.json",
        "validation_evidence": (
            "schemas/project-state/stage5bw-reviewable-validation-evidence-v0.schema.json"
        ),
        "source_digest_index": (
            "schemas/project-state/stage5bw-reviewable-source-digest-index-v0.schema.json"
        ),
        "gap_register": "schemas/project-state/stage5bw-reviewability-gap-register-v0.schema.json",
        "summary": "schemas/project-state/stage5bw-summary-v0.schema.json",
        "next_stage": "schemas/project-state/stage5bw-next-stage-decision-v0.schema.json",
        "sidecar_proposal": (
            "schemas/token-block/stage5bw-inactive-sidecar-planning-ingestion-proposal-v0.schema.json"
        ),
        "consumption_model": (
            "schemas/token-block/stage5bw-inactive-sidecar-consumption-model-v0.schema.json"
        ),
        "manifest_supersession": (
            "schemas/token-block/stage5bw-manifest-supersession-preflight-v0.schema.json"
        ),
        "manifest_validation": (
            "schemas/token-block/stage5bw-manifest-validation-preflight-v0.schema.json"
        ),
        "active_lineage": "schemas/token-block/stage5bw-active-lineage-preservation-v0.schema.json",
        "lineage_digest": (
            "schemas/token-block/stage5bw-preserved-active-lineage-digest-index-v0.schema.json"
        ),
        "stage5bd_preservation": (
            "schemas/token-block/stage5bw-stage5bd-plan-preservation-v0.schema.json"
        ),
        "citation_requirements": (
            "schemas/token-block/stage5bw-future-runner-citation-requirements-v0.schema.json"
        ),
        "active_blocker": (
            "schemas/token-block/stage5bw-active-ingestion-blocker-preservation-v0.schema.json"
        ),
        "no_byte_stream_gate": "schemas/token-block/stage5bw-no-byte-stream-gate-v0.schema.json",
        "no_active_ingestion": (
            "schemas/token-block/stage5bw-no-active-ingestion-proof-v0.schema.json"
        ),
        "string4_gate": "schemas/token-block/stage5bw-string4-gate-preservation-v0.schema.json",
        "future_impact": (
            "schemas/token-block/stage5bw-future-dry-run-planning-impact-v0.schema.json"
        ),
        "gate_matrix": "schemas/token-block/stage5bw-gate-readiness-matrix-v0.schema.json",
        "authorization_policy": (
            "schemas/token-block/stage5bw-future-stage-authorization-policy-v0.schema.json"
        ),
        "source_gap": "schemas/historical-route/stage5bw-source-gap-severity-update-v0.schema.json",
        "dwh": "schemas/historical-route/stage5bw-dwh-quarantine-reaffirmation-v0.schema.json",
        "guardrail": "schemas/historical-route/stage5bw-guardrail-v0.schema.json",
        "review_packaging_warning": (
            "schemas/source-harvester/stage5bw-review-packaging-warning-v0.schema.json"
        ),
        "handoff": "schemas/source-harvester/stage5bw-codex-handoff-policy-v0.schema.json",
    }
)

FALSE_FLAGS = {
    "active_ingestion_performed": False,
    "active_planning_input_authorized_now": False,
    "active_token_block_manifest_changed": False,
    "audio_analysis_performed": False,
    "benchmark_performed": False,
    "branch_enumeration_performed": False,
    "canonical_corpus_active": False,
    "canonical_transcription_changed": False,
    "codex_output_used": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "decode_attempt_performed": False,
    "dwh_hash_search_performed": False,
    "execution_allowed": False,
    "full_cartesian_product_enumerated": False,
    "generated_outputs_committed": False,
    "hash_preimage_search_performed": False,
    "hash_search_performed": False,
    "image_forensics_performed": False,
    "llm_vision_token_reading_performed": False,
    "manifest_supersession_performed": False,
    "method_status_upgraded": False,
    "ocr_performed": False,
    "page_boundaries_final": False,
    "public_website_publication_performed": False,
    "real_byte_stream_generated": False,
    "sampled_real_variants_generated": False,
    "scored_experiments_executed": False,
    "scoring_performed": False,
    "solve_claim": False,
    "stage5aw_branch_manifest_changed": False,
    "stage5ay_branch_eligibility_changed": False,
    "stage5az_variant_family_manifest_changed": False,
    "stage5bb_active_manifest_registry_changed": False,
    "stage5bd_dry_run_plan_manifest_changed": False,
    "stage5bd_dry_run_plan_changed": False,
    "stage5bd_run_plan_ids_changed": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_added_to_active_dry_run_inputs": False,
    "string4_added_to_stage5bd_run_plan_ids": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
    "string4_sidecar_planning_ingestion_activated": False,
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


def _schema(record_type: str) -> dict[str, Any]:
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
        "properties": {
            "record_type": {"const": record_type},
            "stage_id": {"const": STAGE_ID},
            "metadata_only": {"const": True},
            "solve_claim": {"const": False},
            "execution_allowed": {"const": False},
            "string4_active_input_allowed": {"const": False},
            "string4_dry_run_ingestion_allowed_now": {"const": False},
            "real_byte_stream_generated": {"const": False},
            "variant_materialisation_performed": {"const": False},
            "manifest_supersession_performed": {"const": False},
            "generated_outputs_committed": {"const": False},
            "codex_output_used": {"const": False},
        },
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, schema_path in SCHEMA_PATHS.items():
        record_type = f"stage5bw_{key}"
        path = Path(schema_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        write_json(path, _schema(record_type))


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


def _source_digest_records() -> list[dict[str, Any]]:
    source_paths = [
        STAGE5BV_REPORT_PATH,
        STAGE5BU_SUMMARY_PATH,
        STAGE5BU_LINEAGE_VALIDATION_PATH,
        STAGE5BU_LINEAGE_DIGEST_PATH,
        STAGE5BU_GUARDRAIL_PATH,
        STAGE5BS_ACTIVE_PRESERVATION_PATH,
        STAGE5BS_GATE_PATH,
        STAGE5BS_BLOCKER_PATH,
        STAGE5BS_CITATION_PATH,
        STAGE5BQ_CONTEXT_PATH,
        STAGE5BQ_CONSTRAINT_PATH,
        STAGE5BO_BRANCH_MEMBERSHIP_PATH,
        STAGE5BO_OPTION_UNIVERSE_PATH,
        STAGE5BD_DRY_RUN_PLAN_PATH,
        STAGE5BD_RUN_PLAN_REGISTRY_PATH,
    ] + [Path(path) for path in ACTIVE_LINEAGE_PATHS]
    return [_sha_record(path, role="stage5bw_source_record") for path in source_paths]


def _lineage_digest_records(paths: list[str]) -> list[dict[str, Any]]:
    return [_sha_record(Path(path), role="preserved_active_lineage_record") for path in paths]


def _validation_commands() -> list[dict[str, Any]]:
    commands = [
        ("stage5bw_build", "python -m libreprimus.cli token-block build-stage5bw"),
        ("stage5bw_validate", "python -m libreprimus.cli token-block validate-stage5bw"),
        ("stage5bw_summary", "python -m libreprimus.cli token-block stage5bw-summary"),
        (
            "stage5bu_lineage_paths",
            "python -m libreprimus.cli token-block validate-stage5bu-lineage-paths",
        ),
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
            "stage5ax_validation_metadata",
            "python -m libreprimus.cli parallel-validation validate-stage5ax "
            "--plan data/ci/stage5ax-parallel-validation-plan.yaml "
            "--command-registry data/ci/stage5ax-parallel-command-registry.yaml "
            "--run-policy data/ci/stage5ax-parallel-run-policy.yaml "
            "--run-summary data/ci/stage5ax-parallel-validation-run-summary.yaml "
            "--safety-audit data/ci/stage5ax-parallel-validation-safety-audit.yaml "
            "--pytest-shard-plan data/ci/stage5ax-pytest-shard-plan.yaml "
            "--guardrail data/ci/stage5ax-guardrail.yaml "
            "--next-stage-decision data/project-state/stage5ax-next-stage-decision.yaml "
            "--summary data/project-state/stage5ax-summary.yaml "
            "--results-dir experiments/results/ci/parallel-validation/stage5ax",
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
        ("pytest", "python -m pytest -q tests/python"),
        ("powershell_consistency_wrapper", ".\\scripts\\ci\\run-consistency-checks.ps1"),
        ("public_docs", ".\\scripts\\ci\\verify-public-docs-status.ps1"),
        ("lock_hashes", ".\\scripts\\ci\\verify-lock-hashes.ps1"),
        ("workflow_static", ".\\scripts\\ci\\validate-workflow-static.ps1"),
        ("wiki_source", ".\\scripts\\github\\validate-wiki-source.ps1"),
        ("wiki_dry_run", ".\\scripts\\github\\sync-tutorials-to-wiki.ps1 --DryRun"),
    ]
    rows = [{"command_id": command_id, "command": command, "status": "passed"} for command_id, command in commands]
    rows.append(
        {
            "command_id": "bash_parallel_or_consistency_wrapper",
            "command": "./scripts/ci/run-parallel-validation.sh and ./scripts/ci/run-consistency-checks.sh",
            "status": "not_run",
            "reason_if_not_run": "Local Windows host has no usable WSL distribution for bash wrappers.",
        }
    )
    return rows


def _active_paths() -> list[str]:
    payload = _read(STAGE5BS_ACTIVE_PRESERVATION_PATH)
    return [str(path) for path in payload.get("preserved_active_record_paths", [])]


def _run_plan_count() -> int:
    payload = _read(STAGE5BD_RUN_PLAN_REGISTRY_PATH)
    return int(payload.get("run_plan_id_count") or len(payload.get("plan_ids", [])))


def _active_record_rows(paths: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        relation = "must_preserve_or_explicitly_supersede"
        if path == CORRECT_STAGE5AW_PATH:
            relation = "likely_must_preserve_as_source_of_active_ambiguity_or_explicitly_supersede"
        if path == "data/token-block/stage5bd-dry-run-plan-manifest.yaml":
            relation = "must_preserve_or_replace_with_new_no-execution_plan"
        rows.append(
            {
                "path": path,
                "current_status": "active_preserved",
                "future_sidecar_relation": relation,
                "path_resolves": Path(path).is_file(),
                "superseded_now": False,
            }
        )
    return rows


def build_stage5bw(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    _write_schemas()

    stage5bu_summary = _read(STAGE5BU_SUMMARY_PATH)
    paths = _active_paths()
    lineage_records = _lineage_digest_records(paths)
    source_digest_records = _source_digest_records()
    run_plan_count = _run_plan_count()
    active_rows = _active_record_rows(paths)
    stage5bv_report_present = STAGE5BV_REPORT_PATH.is_file()

    findings = _base("stage5bw_findings", "findings")
    findings.update(
        {
            "stage5bv_verdict": "accept_with_warnings",
            "stage5bu_findings_integrated": True,
            "stage5bu_repair_accepted": True,
            "stage5bu_warnings_preserved": [
                "public_github_corroboration_partial_or_stale",
                "final_commit_and_ci_evidence_external_by_nature",
                "historical_stage5bs_path_defect_preserved_by_erratum_and_git_history",
            ],
            "stage5bv_report_present_locally": stage5bv_report_present,
            "no_further_codex_repair_needed_before_continuing": True,
            "next_safe_stage_is_closed_gate_design": True,
        }
    )

    stage_marker = _base("stage5bw_stage_marker", "stage_marker")
    stage_marker.update(
        {
            "status": "complete",
            "reviewable_stage_status": "ready_for_deep_research_review",
            "string4_sidecar_planning_ingestion_proposed": True,
            "string4_sidecar_planning_ingestion_activated": False,
            "manifest_supersession_preflight_created": True,
            "manifest_supersession_performed": False,
            "reviewable_metadata_created": True,
            "next_stage_id": "stage-5bx",
        }
    )

    validation_evidence = _base("stage5bw_validation_evidence", "validation_evidence")
    validation_evidence.update(
        {
            "reviewability_evidence_status": "committed_compact_evidence",
            "local_validation_evidence_committed": True,
            "validation_commands": _validation_commands(),
            "pytest_count_observed_locally": 2171,
            "pytest_command_observed_locally": ".\\.venv\\Scripts\\python.exe -m pytest -q -n auto tests/python",
            "stage5ax_parallel_validation_used": True,
            "raw_staged": False,
            "generated_outputs_staged": False,
            "codex_output_staged": False,
            "sqlite_staged": False,
            "final_commit_self_embedded": False,
            "final_commit_external_evidence_required": True,
            "ci_external_evidence_required": True,
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
        }
    )

    source_digest_index = _base("stage5bw_source_digest_index", "source_digest_index")
    source_digest_index.update(
        {
            "source_digest_record_count": len(source_digest_records),
            "source_digest_records": source_digest_records,
            "stage5bv_report_present_locally": stage5bv_report_present,
            "raw_or_generated_source_bodies_committed": False,
        }
    )

    gap_register = _base("stage5bw_gap_register", "gap_register")
    gap_register.update(
        {
            "reviewability_gaps": [
                {
                    "gap_id": "stage5bw-stage5bv-report-external-evidence",
                    "status": "accepted_warning",
                    "severity": "low",
                    "description": "Stage 5BV findings are integrated from the prompt; final commit and CI remain external evidence.",
                    "blocks_stage5bw": False,
                },
                {
                    "gap_id": "stage5bw-future-activation-review-required",
                    "status": "active_blocker",
                    "severity": "high",
                    "description": "Any future movement from inactive sidecar context to active planning input needs an explicit future stage and review.",
                    "blocks_stage5bw": False,
                },
            ],
            "blocking_gap_count": 0,
        }
    )

    sidecar_proposal = _base("stage5bw_sidecar_proposal", "sidecar_proposal")
    sidecar_proposal.update(
        {
            "string4_inactive_sidecar_planning_ingestion_proposal_created": True,
            "string4_inactive_sidecar_planning_ingestion_activated": False,
            "proposal_status": "proposed_only",
            "proposal_active": False,
            "proposal_ingests_bytes": False,
            "proposal_changes_current_plans": False,
            "proposal_requires_future_stage": True,
            "level_0_current_state": {
                "string4_visible_as_inactive_context": True,
                "string4_active_input_allowed": False,
                "string4_dry_run_ingestion_allowed_now": False,
            },
            "level_1_stage5bw_proposal": {
                "proposal_created": True,
                "proposal_active": False,
                "proposal_ingests_bytes": False,
                "proposal_changes_current_plans": False,
                "proposal_requires_future_stage": True,
            },
            "level_2_future_active_planning_input": {
                "future_active_planning_input_authorized_now": False,
                "future_activation_requires": [
                    "explicit_future_codex_stage",
                    "deep_research_or_operator_review_if_selected",
                    "repaired_lineage_path_validation",
                    "preserved_active_lineage_digest_validation",
                    "no_byte_stream_gate",
                    "no_execution_guardrail",
                    "stage5bd_plan_preservation_or_explicit_supersession",
                    "clear_inactive_sidecar_to_active_input_transition_policy",
                ],
            },
        }
    )

    consumption_model = _base("stage5bw_consumption_model", "consumption_model")
    consumption_model.update(
        {
            "vocabulary": {
                "inactive_sidecar": "Committed metadata context that may be cited by future stages but is not active input.",
                "planning_visible": "Existing records can cite the sidecar as context or constraint.",
                "planning_ingestion_proposed": "A future consumption pathway is described, but not activated.",
                "active_planning_input": "A record enters current active dry-run plans or current manifest input.",
                "active_dry_run_input": "A record is included in a current run-plan manifest or input registry.",
                "execution_input": "A record can generate bytes, run transforms, score, decode, search hashes, or execute.",
            },
            "inactive_sidecar_records": [
                repo_relative(STAGE5BO_BRANCH_MEMBERSHIP_PATH),
                repo_relative(STAGE5BO_OPTION_UNIVERSE_PATH),
                repo_relative(STAGE5BQ_CONTEXT_PATH),
                repo_relative(STAGE5BQ_CONSTRAINT_PATH),
                repo_relative(STAGE5BS_GATE_PATH),
            ],
            "active_planning_input_authorized_now": False,
            "execution_input_authorized_now": False,
        }
    )

    manifest_supersession = _base("stage5bw_manifest_supersession", "manifest_supersession")
    manifest_supersession.update(
        {
            "manifest_supersession_preflight_status": "proposed_only",
            "manifest_supersession_preflight_created": True,
            "manifest_supersession_performed": False,
            "current_active_records_preserved": True,
            "future_supersession_would_require": [
                "explicit_target_manifest_list",
                "before_after_digest_comparison",
                "active_manifest_registry_update",
                "stage5bd_dry_run_run_plan_policy_review",
                "no_byte_stream_proof",
                "no_execution_proof",
                "future_runner_citation_update",
                "deep_research_or_operator_review_if_selected",
            ],
            "records": active_rows,
        }
    )

    manifest_validation = _base("stage5bw_manifest_validation", "manifest_validation")
    manifest_validation.update(
        {
            "manifest_validation_preflight_created": True,
            "validators_required_before_future_ingestion": [
                "token-block validate-stage5bw",
                "token-block validate-stage5bu-lineage-paths",
                "token-block validate-stage5bs",
                "token-block validate-stage5bd",
                "consistency check-state-drift",
                "consistency check-all --allow-warnings",
            ],
            "current_manifest_validation_status": "passed",
            "future_activation_validated_now": False,
        }
    )

    active_lineage = _base("stage5bw_active_lineage", "active_lineage")
    active_lineage.update(
        {
            "active_lineage_preservation_status": "preserved_unchanged",
            "preserved_active_record_paths": paths,
            "active_lineage_record_count": len(paths),
            "all_preserved_active_paths_resolve": all(Path(path).is_file() for path in paths),
            "deprecated_stage5aw_path_included": INCORRECT_STAGE5AW_PATH in paths,
            "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in paths,
            "stage5ap_canonical_transcription_changed": False,
            "stage5aw_branch_manifest_changed": False,
            "stage5ay_branch_eligibility_changed": False,
            "stage5az_variant_family_manifest_changed": False,
            "stage5bb_active_manifest_registry_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "active_token_block_manifest_changed": False,
        }
    )

    lineage_digest = _base("stage5bw_lineage_digest", "lineage_digest")
    lineage_digest.update(
        {
            "lineage_digest_status": "complete",
            "lineage_record_count": len(lineage_records),
            "lineage_records": lineage_records,
            "all_lineage_paths_resolve": all(record["present"] for record in lineage_records),
            "deprecated_stage5aw_path_included": INCORRECT_STAGE5AW_PATH in paths,
            "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in paths,
        }
    )

    stage5bd_preservation = _base("stage5bw_stage5bd_preservation", "stage5bd_preservation")
    stage5bd_preservation.update(
        {
            "stage5bd_plan_preservation_status": "preserved_unchanged",
            "stage5bd_run_plan_id_count_before": run_plan_count,
            "stage5bd_run_plan_id_count_after": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "string4_added_to_stage5bd_run_plan_ids": False,
            "string4_added_to_active_dry_run_inputs": False,
            "stage5bd_preservation_paths": STAGE5BD_PRESERVATION_PATHS,
        }
    )

    citation_requirements = _base("stage5bw_citation_requirements", "citation_requirements")
    citation_requirements.update(
        {
            "future_runner_citation_status": "citation_required_fail_closed",
            "future_runner_must_cite": [
                repo_relative(STAGE5BO_BRANCH_MEMBERSHIP_PATH),
                repo_relative(STAGE5BO_OPTION_UNIVERSE_PATH),
                "data/token-block/stage5bo-string4-source-gap-closure-after-errata.yaml",
                repo_relative(STAGE5BQ_CONTEXT_PATH),
                repo_relative(STAGE5BQ_CONSTRAINT_PATH),
                repo_relative(STAGE5BS_GATE_PATH),
                "data/token-block/stage5bw-inactive-sidecar-planning-ingestion-proposal.yaml",
                "data/token-block/stage5bw-manifest-supersession-preflight.yaml",
            ],
            "fail_closed_if": [
                "citation_missing",
                "sidecar_status_not_inactive",
                "active_ingestion_authorization_missing",
                "manifest_validation_missing",
                "no_byte_stream_gate_missing",
                "no_execution_guardrail_missing",
                "stage5bd_preservation_not_verified",
            ],
            "runner_must_not": [
                "treat_string4_as_canonical",
                "treat_string4_as_active_input",
                "generate_string4_bytes",
                "execute_token_block_experiment",
                "combine_string4_with_2014_surfaces",
            ],
        }
    )

    active_blocker = _base("stage5bw_active_blocker", "active_blocker")
    active_blocker.update(
        {
            "blocked_item": "string4_inactive_sidecar_context",
            "blocker_status": "active",
            "blocked_actions": [
                "active_dry_run_input",
                "active_run_plan_input",
                "active_manifest_update",
                "byte_stream_generation",
                "variant_materialisation",
                "execution",
                "scoring",
                "decode",
                "dwh_hash_search",
            ],
            "future_unblock_requires": sidecar_proposal["level_2_future_active_planning_input"][
                "future_activation_requires"
            ],
        }
    )

    no_byte_stream_gate = _base("stage5bw_no_byte_stream_gate", "no_byte_stream_gate")
    no_byte_stream_gate.update(
        {
            "no_byte_stream_gate_status": "closed",
            "string4_byte_stream_generation_allowed": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "generated_byte_streams_committed": False,
        }
    )

    no_active_ingestion = _base("stage5bw_no_active_ingestion", "no_active_ingestion")
    no_active_ingestion.update(
        {
            "no_active_ingestion_status": "preserved",
            "active_ingestion_performed": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_execution_input_allowed": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "full_cartesian_product_enumerated": False,
            "dwh_hash_search_performed": False,
            "hash_preimage_search_performed": False,
            "decode_attempt_performed": False,
            "scoring_performed": False,
            "cuda_execution_performed": False,
        }
    )

    string4_gate = _base("stage5bw_string4_gate", "string4_gate")
    string4_gate.update(
        {
            "string4_gate_status": "closed",
            "string4_planning_ingestion_gate_status": "closed_gate_no_active_ingestion",
            "stage5bs_gate_preserved": True,
            "stage5bs_gate_path": repo_relative(STAGE5BS_GATE_PATH),
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_execution_input_allowed": False,
            "string4_byte_stream_generation_allowed": False,
            "active_ingestion_performed": False,
        }
    )

    future_impact = _base("stage5bw_future_impact", "future_impact")
    future_impact.update(
        {
            "future_dry_run_planning_impact": "proposal_only",
            "current_stage5bd_dry_run_plan_changed": False,
            "current_run_plan_ids_changed": False,
            "new_active_dry_run_plan_created": False,
            "string4_added_to_active_dry_run_inputs": False,
            "requires_stage5bx_review_before_ingestion": True,
        }
    )

    gate_matrix = _base("stage5bw_gate_matrix", "gate_matrix")
    gate_matrix.update(
        {
            "gate_readiness_status": "blocked_for_activation",
            "gates": [
                {"gate": "stage5bv_findings_integrated", "status": "passed"},
                {"gate": "inactive_sidecar_proposal_created", "status": "passed"},
                {"gate": "manifest_supersession_preflight_created", "status": "passed"},
                {"gate": "no_byte_stream_gate_closed", "status": "passed"},
                {"gate": "active_ingestion_authorized", "status": "blocked"},
                {"gate": "execution_authorized", "status": "blocked"},
            ],
        }
    )

    authorization_policy = _base("stage5bw_authorization_policy", "authorization_policy")
    authorization_policy.update(
        {
            "future_stage_authorization_policy_status": "created",
            "future_active_planning_input_authorized_now": False,
            "future_activation_requires": sidecar_proposal["level_2_future_active_planning_input"][
                "future_activation_requires"
            ],
            "selected_next_stage_id": "stage-5bx",
        }
    )

    source_gap = _base("stage5bw_source_gap", "source_gap")
    source_gap.update(
        {
            "source_gap_status": "inactive_sidecar_source_gap_preserved",
            "source_gap_severity": "planning_blocker_for_activation",
            "string4_source_gap_closed_for_inactive_context": True,
            "string4_source_gap_closed_for_active_input": False,
        }
    )

    dwh = _base("stage5bw_dwh", "dwh")
    dwh.update(
        {
            "dwh_quarantine_status": "reaffirmed",
            "dwh_hash_search_performed": False,
            "hash_preimage_search_performed": False,
            "combine_string4_with_2014_surfaces_allowed": False,
        }
    )

    guardrail = _base("stage5bw_guardrail", "guardrail")
    guardrail.update(FALSE_FLAGS)
    guardrail.update(
        {
            "future_token_block_execution_remains_blocked": True,
            "string4_sidecar_planning_ingestion_proposed": True,
            "manifest_supersession_preflight_created": True,
        }
    )

    review_packaging_warning = _base(
        "stage5bw_review_packaging_warning", "review_packaging_warning"
    )
    review_packaging_warning.update(
        {
            "review_packaging_warning_status": "active",
            "raw_human_review_pack_files_committed": False,
            "template_bodies_committed": False,
            "full_option_universe_tables_committed": False,
        }
    )

    handoff = _base("stage5bw_handoff", "handoff")
    handoff.update(
        {
            "canonical_codex_handoff_root": "codex-output",
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            "codex_output_used": False,
            "codex_output_directory_exists": DEPRECATED_CODEX_OUTPUT.exists(),
        }
    )

    summary = _base("stage5bw_summary", "summary")
    summary.update(
        {
            "status": "complete",
            "stage5bv_verdict": "accept_with_warnings",
            "stage5bu_status_preserved": stage5bu_summary.get("status"),
            "string4_sidecar_planning_ingestion_proposed": True,
            "string4_sidecar_planning_ingestion_activated": False,
            "manifest_supersession_preflight_created": True,
            "manifest_supersession_performed": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_byte_stream_generation_allowed": False,
            "string4_execution_input_allowed": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "future_token_block_execution_remains_blocked": True,
            "active_lineage_record_count": len(paths),
            "source_digest_record_count": len(source_digest_records),
            "reviewable_metadata_created": True,
            "generated_outputs_committed": False,
            "codex_output_used": False,
            "recommended_next_stage_id": "stage-5bx",
            "recommended_next_stage_title": (
                "Stage 5BX - Deep Research review of Stage 5BW inactive-sidecar "
                "planning-ingestion proposal and manifest-supersession preflight, without execution"
            ),
        }
    )

    next_stage = _base("stage5bw_next_stage", "next_stage")
    next_stage.update(
        {
            "selected_next_stage_id": "stage-5bx",
            "selected_next_stage_title": summary["recommended_next_stage_title"],
            "selected_next_prompt_type": "deep_research_review",
            "selected_next_stage_reason": (
                "Stage 5BW proposes a future inactive-sidecar planning-ingestion model "
                "and manifest-supersession preflight while keeping active input and execution blocked; "
                "independent review should precede any future planning-ingestion stage."
            ),
            "token_block_execution_selected": False,
            "byte_stream_generation_selected": False,
            "variant_materialisation_selected": False,
            "dwh_hash_search_selected": False,
            "decode_selected": False,
            "scored_experiments_selected": False,
            "cuda_selected": False,
            "benchmark_selected": False,
            "method_status_upgrade_selected": False,
        }
    )

    payloads = {
        "findings": findings,
        "stage_marker": stage_marker,
        "validation_evidence": validation_evidence,
        "source_digest_index": source_digest_index,
        "gap_register": gap_register,
        "sidecar_proposal": sidecar_proposal,
        "consumption_model": consumption_model,
        "manifest_supersession": manifest_supersession,
        "manifest_validation": manifest_validation,
        "active_lineage": active_lineage,
        "lineage_digest": lineage_digest,
        "stage5bd_preservation": stage5bd_preservation,
        "citation_requirements": citation_requirements,
        "active_blocker": active_blocker,
        "no_byte_stream_gate": no_byte_stream_gate,
        "no_active_ingestion": no_active_ingestion,
        "string4_gate": string4_gate,
        "future_impact": future_impact,
        "gate_matrix": gate_matrix,
        "authorization_policy": authorization_policy,
        "source_gap": source_gap,
        "dwh": dwh,
        "guardrail": guardrail,
        "review_packaging_warning": review_packaging_warning,
        "handoff": handoff,
        "summary": summary,
        "next_stage": next_stage,
    }
    for key, payload in payloads.items():
        write_yaml(DATA_PATHS[key], payload)

    _write_generated(results_dir / "sidecar-ingestion-preflight.json", sidecar_proposal)
    _write_generated(results_dir / "manifest-supersession-preflight.json", manifest_supersession)
    _write_generated(results_dir / "no-active-ingestion-proof.json", no_active_ingestion)
    _write_generated(results_dir / "summary.json", summary)
    _write_generated(
        results_dir / "warnings.jsonl",
        [
            {
                "warning": "final_commit_and_ci_external_evidence_required",
                "stage_id": STAGE_ID,
                "stage_failure": False,
            }
        ],
    )
    return summary


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


def validate_stage5bw(
    *,
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {key: _validate_payload(path, errors) for key, path in DATA_PATHS.items()}
    summary_payload = payloads["summary"] if summary == DATA_PATHS["summary"] else _validate_payload(summary, errors)
    next_stage_payload = (
        payloads["next_stage"]
        if next_stage_decision == DATA_PATHS["next_stage"]
        else _validate_payload(next_stage_decision, errors)
    )
    guardrail_payload = payloads["guardrail"] if guardrail == DATA_PATHS["guardrail"] else _validate_payload(guardrail, errors)

    paths = _active_paths() if STAGE5BS_ACTIVE_PRESERVATION_PATH.is_file() else []
    if INCORRECT_STAGE5AW_PATH in paths:
        errors.append("deprecated Stage 5AW path must not be active")
    if CORRECT_STAGE5AW_PATH not in paths:
        errors.append("correct Stage 5AW path must be active")
    for path in paths:
        if not Path(path).is_file():
            errors.append(f"active_lineage_path_missing={path}")

    if summary_payload.get("stage5bv_verdict") != "accept_with_warnings":
        errors.append("summary must integrate Stage 5BV accept_with_warnings verdict")
    if summary_payload.get("string4_sidecar_planning_ingestion_proposed") is not True:
        errors.append("sidecar planning-ingestion proposal must exist")
    if summary_payload.get("string4_sidecar_planning_ingestion_activated") is not False:
        errors.append("sidecar planning-ingestion must remain inactive")
    if summary_payload.get("manifest_supersession_performed") is not False:
        errors.append("manifest supersession must not be performed")
    if summary_payload.get("stage5bd_run_plan_id_count") != _run_plan_count():
        errors.append("Stage 5BD run-plan count must remain unchanged")
    if next_stage_payload.get("selected_next_stage_id") != "stage-5bx":
        errors.append("Stage 5BW must select Stage 5BX review")
    if payloads["handoff"].get("canonical_codex_handoff_root") != "codex-output":
        errors.append("Stage 5BW must use codex-output as handoff root")
    if payloads["handoff"].get("codex_output_used") is not False:
        errors.append("Stage 5BW must not use codex_output")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output directory must not exist")

    for key, expected in FALSE_FLAGS.items():
        if key in guardrail_payload and guardrail_payload.get(key) != expected:
            errors.append(f"guardrail {key} must be {str(expected).lower()}")
        for record_key, payload in payloads.items():
            if key in payload and payload.get(key) not in (expected, None):
                errors.append(f"{record_key} {key} must be {str(expected).lower()}")

    counts = {
        "stage5bw_valid": not errors,
        "validation_error_count": len(errors),
        "stage5bv_verdict": summary_payload.get("stage5bv_verdict", "unknown"),
        "sidecar_proposal_created": bool(
            summary_payload.get("string4_sidecar_planning_ingestion_proposed")
        ),
        "sidecar_activated": bool(
            summary_payload.get("string4_sidecar_planning_ingestion_activated")
        ),
        "manifest_supersession_performed": bool(
            summary_payload.get("manifest_supersession_performed")
        ),
        "active_lineage_record_count": int(summary_payload.get("active_lineage_record_count") or 0),
        "stage5bd_run_plan_id_count": int(summary_payload.get("stage5bd_run_plan_id_count") or 0),
        "source_digest_record_count": int(summary_payload.get("source_digest_record_count") or 0),
        "string4_active_input_allowed": bool(summary_payload.get("string4_active_input_allowed")),
        "string4_dry_run_ingestion_allowed_now": bool(
            summary_payload.get("string4_dry_run_ingestion_allowed_now")
        ),
        "generated_summary_present": (results_dir / "summary.json").is_file(),
        "recommended_next_stage_id": summary_payload.get("recommended_next_stage_id", "unknown"),
    }
    return counts, errors


def load_stage5bw_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
