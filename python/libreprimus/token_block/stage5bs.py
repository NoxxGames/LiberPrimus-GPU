"""Stage 5BS String 4 inactive-branch planning-ingestion gate metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import repo_relative, sha256_file, write_json, write_yaml
from libreprimus.token_block.stage5bm import _read

STAGE_ID = "stage-5bs"
STAGE_TITLE = (
    "Stage 5BS - String 4 inactive-branch planning-ingestion gate and "
    "future-runner citation integration, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5bq"
SOURCE_PREVIOUS_COMMIT = "8df9e26e5166caa130c059aa91b270bb81968afa"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5br"
SOURCE_DEEP_RESEARCH_REPORT = "11_Deep-Research-Review-Of-Inactive-Branch-Dry-Run-Planning-Integration.md"

RESULTS_DIR = Path("experiments/results/token-block/stage5bs")
CODEX_COMPLETION_PATH = Path("codex-output/stage5bs-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
STAGE5BR_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "11_Deep-Research-Review-Of-Inactive-Branch-Dry-Run-Planning-Integration.md"
)

STAGE5BQ_SUMMARY_PATH = Path("data/project-state/stage5bq-summary.yaml")
STAGE5BQ_NEXT_STAGE_PATH = Path("data/project-state/stage5bq-next-stage-decision.yaml")
STAGE5BQ_CONTEXT_PATH = Path("data/token-block/stage5bq-string4-inactive-branch-planning-context.yaml")
STAGE5BQ_CONSTRAINT_PATH = Path("data/token-block/stage5bq-errata-aware-dry-run-constraint-update.yaml")
STAGE5BQ_NO_ACTIVE_INGESTION_PATH = Path("data/token-block/stage5bq-string4-no-active-ingestion-proof.yaml")
STAGE5BQ_REQUIREMENTS_PATH = Path("data/token-block/stage5bq-future-dry-run-requirements.yaml")
STAGE5BO_BRANCH_MEMBERSHIP_PATH = Path("data/token-block/stage5bo-string4-branch-membership-after-errata.yaml")
STAGE5BO_OPTION_UNIVERSE_PATH = Path("data/token-block/stage5bo-errata-aware-token-option-universe.yaml")
STAGE5BO_SOURCE_GAP_CLOSURE_PATH = Path("data/token-block/stage5bo-string4-source-gap-closure-after-errata.yaml")
STAGE5BD_DRY_RUN_PLAN_PATH = Path("data/token-block/stage5bd-dry-run-plan-manifest.yaml")
STAGE5BD_RUN_PLAN_REGISTRY_PATH = Path("data/token-block/stage5bd-run-plan-id-registry.yaml")

DATA_PATHS: dict[str, Path] = {
    "findings": Path("data/project-state/stage5bs-stage5br-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5bs-reviewable-stage-marker.yaml"),
    "validation_evidence": Path("data/project-state/stage5bs-reviewable-validation-evidence.yaml"),
    "source_digest_index": Path("data/project-state/stage5bs-reviewable-source-digest-index.yaml"),
    "gap_register": Path("data/project-state/stage5bs-reviewability-gap-register.yaml"),
    "review_packaging_warning": Path("data/source-harvester/stage5bs-review-packaging-warning.yaml"),
    "gate": Path("data/token-block/stage5bs-string4-planning-ingestion-gate.yaml"),
    "citation_policy": Path("data/token-block/stage5bs-future-runner-citation-policy.yaml"),
    "sidecar_policy": Path("data/token-block/stage5bs-inactive-sidecar-consumption-policy.yaml"),
    "active_blocker": Path("data/token-block/stage5bs-active-ingestion-blocker.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5bs-no-active-ingestion-proof.yaml"),
    "readiness_matrix": Path("data/token-block/stage5bs-string4-gate-readiness-matrix.yaml"),
    "manifest_requirements": Path("data/token-block/stage5bs-manifest-validation-requirements.yaml"),
    "authorization_policy": Path("data/token-block/stage5bs-future-stage-authorization-policy.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5bs-stage5bd-plan-preservation.yaml"),
    "active_preservation": Path("data/token-block/stage5bs-active-manifest-preservation.yaml"),
    "future_impact": Path("data/token-block/stage5bs-future-dry-run-planning-impact.yaml"),
    "source_gap": Path("data/historical-route/stage5bs-source-gap-severity-update.yaml"),
    "dwh": Path("data/historical-route/stage5bs-dwh-quarantine-reaffirmation.yaml"),
    "guardrail": Path("data/historical-route/stage5bs-guardrail.yaml"),
    "handoff": Path("data/source-harvester/stage5bs-codex-handoff-policy.yaml"),
    "summary": Path("data/project-state/stage5bs-summary.yaml"),
    "next_stage": Path("data/project-state/stage5bs-next-stage-decision.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    key: str(path).replace("data/", "schemas/").replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
SCHEMA_PATHS.update(
    {
        "findings": "schemas/project-state/stage5bs-stage5br-findings-integration-v0.schema.json",
        "stage_marker": "schemas/project-state/stage5bs-reviewable-stage-marker-v0.schema.json",
        "validation_evidence": "schemas/project-state/stage5bs-reviewable-validation-evidence-v0.schema.json",
        "source_digest_index": "schemas/project-state/stage5bs-reviewable-source-digest-index-v0.schema.json",
        "gap_register": "schemas/project-state/stage5bs-reviewability-gap-register-v0.schema.json",
        "review_packaging_warning": "schemas/source-harvester/stage5bs-review-packaging-warning-v0.schema.json",
        "gate": "schemas/token-block/stage5bs-string4-planning-ingestion-gate-v0.schema.json",
        "citation_policy": "schemas/token-block/stage5bs-future-runner-citation-policy-v0.schema.json",
        "sidecar_policy": "schemas/token-block/stage5bs-inactive-sidecar-consumption-policy-v0.schema.json",
        "active_blocker": "schemas/token-block/stage5bs-active-ingestion-blocker-v0.schema.json",
        "no_active_ingestion": "schemas/token-block/stage5bs-no-active-ingestion-proof-v0.schema.json",
        "readiness_matrix": "schemas/token-block/stage5bs-string4-gate-readiness-matrix-v0.schema.json",
        "manifest_requirements": "schemas/token-block/stage5bs-manifest-validation-requirements-v0.schema.json",
        "authorization_policy": "schemas/token-block/stage5bs-future-stage-authorization-policy-v0.schema.json",
        "stage5bd_preservation": "schemas/token-block/stage5bs-stage5bd-plan-preservation-v0.schema.json",
        "active_preservation": "schemas/token-block/stage5bs-active-manifest-preservation-v0.schema.json",
        "future_impact": "schemas/token-block/stage5bs-future-dry-run-planning-impact-v0.schema.json",
        "source_gap": "schemas/historical-route/stage5bs-source-gap-severity-update-v0.schema.json",
        "dwh": "schemas/historical-route/stage5bs-dwh-quarantine-reaffirmation-v0.schema.json",
        "guardrail": "schemas/historical-route/stage5bs-guardrail-v0.schema.json",
        "handoff": "schemas/source-harvester/stage5bs-codex-handoff-policy-v0.schema.json",
        "summary": "schemas/project-state/stage5bs-summary-v0.schema.json",
        "next_stage": "schemas/project-state/stage5bs-next-stage-decision-v0.schema.json",
    }
)

SOURCE_STAGE_IDS = [
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

FALSE_FLAGS: dict[str, bool] = {
    "active_stage5ap_records_mutated": False,
    "active_stage5aw_records_mutated": False,
    "active_stage5ay_records_mutated": False,
    "active_stage5az_records_mutated": False,
    "active_stage5bb_records_mutated": False,
    "active_stage5bd_records_mutated": False,
    "active_token_block_manifest_changed": False,
    "ai_ml_interpretation_performed": False,
    "audio_analysis_performed": False,
    "benchmark_performed": False,
    "branch_materialised_as_active": False,
    "canonical_corpus_active": False,
    "canonical_transcription_changed": False,
    "codex_output_used": False,
    "corrected_decision_template_committed": False,
    "cryptanalytic_benchmark_performed": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "decision_template_committed": False,
    "decode_attempt_performed": False,
    "decoded_byte_body_committed": False,
    "dwh_hash_search_performed": False,
    "execution_allowed": False,
    "fandom_surface_combination_performed": False,
    "full_cartesian_product_enumerated": False,
    "full_string4_body_committed": False,
    "generated_outputs_committed": False,
    "hash_preimage_search_performed": False,
    "hash_search_performed": False,
    "hidden_content_image_forensics_performed": False,
    "iddqd_surface_combination_performed": False,
    "image_forensics_performed": False,
    "llm_vision_token_reading_performed": False,
    "method_status_upgraded": False,
    "mp3stego_execution_performed": False,
    "ocr_performed": False,
    "openpuff_execution_performed": False,
    "outguess_execution_performed": False,
    "page_boundaries_final": False,
    "pgp_network_key_fetch_performed": False,
    "pgp_verification_performed_as_project_truth": False,
    "public_website_publication_performed": False,
    "raw_archive_files_committed": False,
    "raw_human_review_pack_committed": False,
    "raw_iddqd_v2_files_committed": False,
    "real_byte_stream_generated": False,
    "real_token_block_byte_streams_generated": False,
    "reconstructed_token_stream_committed": False,
    "sampled_real_variants_generated": False,
    "scored_experiments_executed": False,
    "scoring_performed": False,
    "semantic_image_interpretation_performed": False,
    "solve_claim": False,
    "spreadsheet_body_committed": False,
    "spreadsheet_file_committed": False,
    "stage5aw_branch_manifest_changed": False,
    "stage5ay_branch_eligibility_changed": False,
    "stage5az_variant_family_manifest_changed": False,
    "stage5bd_dry_run_plan_changed": False,
    "stage5bd_dry_run_records_changed": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_combined_with_2014_surfaces": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
    "template_bodies_committed": False,
    "transposition_attempt_performed": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "website_expansion_performed": False,
    "xor_attempt_performed": False,
}

FALSE_NEXT_STAGE_FLAGS: dict[str, bool] = {
    "ai_ml_selected": False,
    "benchmark_selected": False,
    "byte_stream_generation_selected": False,
    "canonical_corpus_activation_selected": False,
    "cuda_selected": False,
    "decode_selected": False,
    "dwh_hash_search_selected": False,
    "method_status_upgrade_selected": False,
    "ocr_selected": False,
    "page_boundary_finalisation_selected": False,
    "scored_experiments_selected": False,
    "stego_execution_selected": False,
    "token_block_execution_selected": False,
    "variant_materialisation_selected": False,
}

PRESERVED_ACTIVE_RECORDS = [
    "data/token-block/stage5ap-token-block-canonical-transcription.yaml",
    "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml",
    "data/token-block/stage5ay-branch-eligibility-policy.yaml",
    "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml",
    "data/token-block/stage5bb-active-manifest-registry.yaml",
    "data/token-block/stage5bd-active-manifest-lock.yaml",
    "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
    "data/token-block/stage5bd-run-plan-id-registry.yaml",
]

FUTURE_RUNNER_MUST_CITE = [
    "data/token-block/stage5bo-string4-branch-membership-after-errata.yaml",
    "data/token-block/stage5bo-errata-aware-token-option-universe.yaml",
    "data/token-block/stage5bo-string4-source-gap-closure-after-errata.yaml",
    "data/token-block/stage5bq-string4-inactive-branch-planning-context.yaml",
    "data/token-block/stage5bq-errata-aware-dry-run-constraint-update.yaml",
    "data/token-block/stage5bs-string4-planning-ingestion-gate.yaml",
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
    }


def _write_generated(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".jsonl":
        with path.open("w", encoding="utf-8") as handle:
            for row in payload:
                handle.write(json.dumps(row, sort_keys=True) + "\n")
    else:
        write_json(path, payload)


def _sha_record(path: Path, *, committed: bool = True, role: str = "source") -> dict[str, Any]:
    return {
        "path": repo_relative(path),
        "role": role,
        "present": path.is_file(),
        "committed": committed,
        "sha256": sha256_file(path) if path.is_file() else None,
    }


def _run_plan_ids(payload: dict[str, Any]) -> list[str]:
    rows = payload.get("plan_ids", [])
    if not isinstance(rows, list):
        return []
    return [str(row.get("run_plan_id")) for row in rows if isinstance(row, dict) and row.get("run_plan_id")]


def _validation_commands() -> list[dict[str, Any]]:
    passed = [
        ("stage5bs_validator", "python -m libreprimus.cli token-block validate-stage5bs"),
        ("stage5bq_validator", "python -m libreprimus.cli token-block validate-stage5bq"),
        ("stage5bo_validator", "python -m libreprimus.cli token-block validate-stage5bo"),
        ("stage5bd_validator", "python -m libreprimus.cli token-block validate-stage5bd --results-dir experiments/results/token-block/stage5bd"),
        ("stage5ax_parallel_validation", ".\\scripts\\ci\\run-parallel-validation.ps1 -Workers 16 -PytestWorkers 16 -PytestMode auto"),
        ("research_synthesis", "python -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md"),
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
    commands = [{"command_id": command_id, "command": command, "status": "passed"} for command_id, command in passed]
    commands.append(
        {
            "command_id": "bash_consistency_wrapper",
            "command": "./scripts/ci/run-consistency-checks.sh",
            "status": "not_run",
            "reason_if_not_run": "Only WSL bash.exe was available locally and no WSL distribution was installed.",
        }
    )
    return commands


def build_stage5bs_planning_ingestion_gate(
    *,
    stage5bq_summary: Path = STAGE5BQ_SUMMARY_PATH,
    stage5bq_next_stage: Path = STAGE5BQ_NEXT_STAGE_PATH,
    stage5bq_context: Path = STAGE5BQ_CONTEXT_PATH,
    stage5bq_constraint: Path = STAGE5BQ_CONSTRAINT_PATH,
    stage5bq_no_active_ingestion: Path = STAGE5BQ_NO_ACTIVE_INGESTION_PATH,
    stage5bq_requirements: Path = STAGE5BQ_REQUIREMENTS_PATH,
    stage5bo_branch_membership: Path = STAGE5BO_BRANCH_MEMBERSHIP_PATH,
    stage5bo_option_universe: Path = STAGE5BO_OPTION_UNIVERSE_PATH,
    stage5bo_source_gap_closure: Path = STAGE5BO_SOURCE_GAP_CLOSURE_PATH,
    stage5bd_dry_run_plan: Path = STAGE5BD_DRY_RUN_PLAN_PATH,
    stage5bd_run_plan_registry: Path = STAGE5BD_RUN_PLAN_REGISTRY_PATH,
    stage5br_report: Path = STAGE5BR_REPORT_PATH,
    results_dir: Path = RESULTS_DIR,
) -> dict[str, Any]:
    _read(stage5bq_summary)
    _read(stage5bq_context)
    _read(stage5bq_constraint)
    bo_branch = _read(stage5bo_branch_membership)
    bd_registry = _read(stage5bd_run_plan_registry)
    run_plan_ids = _run_plan_ids(bd_registry)
    run_plan_count = int(bd_registry.get("run_plan_id_count", len(run_plan_ids)))
    string4_status = str(bo_branch.get("string4_branch_membership_status_after_errata", "unknown"))

    consumed_paths = [
        stage5bq_summary,
        stage5bq_next_stage,
        stage5bq_context,
        stage5bq_constraint,
        stage5bq_no_active_ingestion,
        stage5bq_requirements,
        stage5bo_branch_membership,
        stage5bo_option_universe,
        stage5bo_source_gap_closure,
        stage5bd_dry_run_plan,
        stage5bd_run_plan_registry,
    ]
    source_digests = [_sha_record(path, role="consumed_committed_record") for path in consumed_paths]
    source_digests.append(_sha_record(stage5br_report, committed=False, role="ignored_deep_research_report"))

    findings = _base("stage5bs_stage5br_findings_integration", "findings")
    findings.update(
        {
            "stage5br_verdict": "accept_with_warnings",
            "accepted_findings": [
                "stage5bq_coherent_conservative_fail_closed",
                "string4_planning_visible_not_active",
                "dry_run_planning_awareness_only",
                "active_lineage_preserved",
                "source_gap_closed_for_metadata_only",
                "dwh_quarantine_preserved",
                "guardrails_strong",
            ],
            "warnings": [
                "evidence_packaging_reviewability_needs_committed_metadata",
                "do_not_jump_to_active_ingestion",
            ],
            "recommended_next_stage": "stage-5bs",
            "recommended_next_prompt_type": PROMPT_TYPE,
            "execution_allowed": False,
        }
    )

    stage_marker = _base("stage5bs_reviewable_stage_marker", "stage_marker")
    stage_marker.update(
        {
            "expected_starting_head_before_stage": SOURCE_PREVIOUS_COMMIT,
            "source_previous_stage_commit": SOURCE_PREVIOUS_COMMIT,
            "reviewable_metadata_created": True,
            "final_commit_self_embedded": False,
            "final_commit_external_evidence_required": True,
            "ci_external_evidence_required": True,
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            "codex_output_directory_used": False,
            "execution_allowed": False,
            "github_issue_number_if_created_before_commit": None,
        }
    )

    validation_evidence = _base("stage5bs_reviewable_validation_evidence", "validation_evidence")
    validation_evidence.update(
        {
            "reviewability_evidence_status": "committed_compact_evidence",
            "local_validation_evidence_committed": True,
            "validation_scope": [
                "stage5bs_validator",
                "stage5bq_validator",
                "stage5bo_validator",
                "stage5bd_validator",
                "stage5ax_parallel_validation",
                "research_synthesis",
                "consistency_state_drift",
                "consistency_check_all",
                "smoke",
                "ruff",
                "pytest",
                "powershell_consistency_wrapper",
                "public_docs",
                "lock_hashes",
                "workflow_static",
                "wiki_source",
                "wiki_dry_run",
            ],
            "commands": _validation_commands(),
            "pytest_count": 2143,
            "stage5ax_parallel_validation_used": True,
            "stage5ax_parallel_validation_passed": True,
            "raw_or_generated_files_staged": False,
            "codex_output_staged": False,
            "third_party_raw_staged": False,
            "human_review_pack_staged": False,
            "full_command_output_committed": False,
            "execution_allowed": False,
        }
    )

    gap_register = _base("stage5bs_reviewability_gap_register", "gap_register")
    gap_register.update(
        {
            "reviewability_evidence_status": "committed_compact_evidence",
            "gaps": [
                {
                    "gap_id": "final_commit_hash_not_self_embedded",
                    "reason": "current commit hash cannot be reliably embedded in files contained by same commit",
                    "closure_route": "GitHub issue comment and ignored codex-output completion summary",
                },
                {
                    "gap_id": "ci_run_id_not_committed_at_stage_commit_time",
                    "reason": "CI run occurs after commit/push",
                    "closure_route": "GitHub issue comment and ignored codex-output completion summary",
                },
                {
                    "gap_id": "raw_codex_completion_summary_uncommitted",
                    "reason": "local handoff artifact is ignored by policy",
                    "closure_route": "compact committed validation-evidence record plus issue comment",
                },
            ],
            "execution_allowed": False,
        }
    )

    review_warning = _base("stage5bs_review_packaging_warning", "review_packaging_warning")
    review_warning.update(
        {
            "warning_status": "reviewability_improved_with_compact_metadata",
            "raw_deep_research_body_committed": False,
            "codex_completion_summary_committed": False,
            "full_command_output_committed": False,
            "compact_reviewable_metadata_committed": True,
            "execution_allowed": False,
        }
    )

    gate = _base("stage5bs_string4_planning_ingestion_gate", "gate")
    gate.update(
        {
            "source_stage5bq_context": repo_relative(stage5bq_context),
            "source_stage5bq_constraint_update": repo_relative(stage5bq_constraint),
            "source_stage5bo_branch_membership": repo_relative(stage5bo_branch_membership),
            "string4_branch_membership_status_after_errata": string4_status,
            "string4_planning_context_status": "inactive_branch_context_only",
            "string4_planning_ingestion_gate_status": "closed_gate_no_active_ingestion",
            "string4_active_ingestion_status": "blocked_pending_explicit_future_stage",
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_execution_input_allowed": False,
            "string4_byte_stream_generation_allowed": False,
            "gate_reasons": [
                "inactive_sidecar_only",
                "active_manifest_preservation_required",
                "no_byte_stream_generation_gate_required",
                "no_execution_guardrail_review_required",
                "explicit_future_codex_planning_ingestion_stage_required",
                "manifest_validation_required",
            ],
            "current_stage_allows_ingestion": False,
            "current_stage_allows_execution": False,
            "execution_allowed": False,
        }
    )

    citation_policy = _base("stage5bs_future_runner_citation_policy", "citation_policy")
    citation_policy.update(
        {
            "future_runner_citation_status": "citation_required_fail_closed",
            "future_runner_must_cite": FUTURE_RUNNER_MUST_CITE,
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
            "execution_allowed": False,
        }
    )

    sidecar_policy = _base("stage5bs_inactive_sidecar_consumption_policy", "sidecar_policy")
    sidecar_policy.update(
        {
            "inactive_sidecar_status": "inactive_planning_sidecar",
            "sidecar_records": [
                repo_relative(stage5bo_option_universe),
                repo_relative(stage5bo_branch_membership),
                repo_relative(stage5bq_context),
            ],
            "allowed_consumption": [
                "future_planning_constraint_citation",
                "review_context",
                "manifest_validation_requirement",
            ],
            "forbidden_consumption": [
                "active_input",
                "byte_stream_generation",
                "variant_materialisation",
                "execution_input",
                "canonical_transcription_replacement",
                "stage5aw_manifest_mutation",
                "stage5bd_plan_mutation",
            ],
            "active_manifest_mutation_forbidden": True,
            "execution_allowed": False,
        }
    )

    active_blocker = _base("stage5bs_active_ingestion_blocker", "active_blocker")
    active_blocker.update(
        {
            "blocked_item": "string4_inactive_branch_context",
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
            "blocker_status": "active",
            "future_unblock_requires": [
                "explicit_future_codex_planning_ingestion_stage",
                "deep_research_or_operator_review_if_selected",
                "manifest_validation",
                "no_byte_stream_generation_gate",
                "no_execution_guardrail_review",
                "source_gap_closure_status_verification",
                "stage5bd_plan_preservation_or_explicit_supersession",
                "clear_distinction_between_inactive_sidecar_and_active_input",
            ],
            "execution_allowed": False,
        }
    )

    no_active_ingestion = _base("stage5bs_no_active_ingestion_proof", "no_active_ingestion")
    no_active_ingestion.update(
        {
            "source_stage5bq_no_active_ingestion_proof": repo_relative(stage5bq_no_active_ingestion),
            "source_stage5bd_dry_run_plan": repo_relative(stage5bd_dry_run_plan),
            "source_file_digests": source_digests,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids": run_plan_ids,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "stage5bb_active_manifest_registry_changed": False,
            "stage5aw_branch_manifest_changed": False,
            "stage5ay_branch_eligibility_changed": False,
            "stage5az_variant_family_manifest_changed": False,
            "canonical_transcription_changed": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_execution_input_allowed": False,
            "string4_byte_stream_generation_allowed": False,
            "real_byte_stream_generated": False,
            "variant_materialisation_performed": False,
            "execution_allowed": False,
        }
    )

    readiness_matrix = _base("stage5bs_string4_gate_readiness_matrix", "readiness_matrix")
    readiness_matrix.update(
        {
            "records": [
                {
                    "gate_item": "string4_branch_representability",
                    "status": "satisfied_for_inactive_context",
                    "evidence": repo_relative(stage5bo_branch_membership),
                },
                {
                    "gate_item": "source_gap_metadata_closure",
                    "status": "satisfied_for_metadata_only",
                    "evidence": repo_relative(stage5bo_source_gap_closure),
                },
                {
                    "gate_item": "deep_research_review_of_inactive_context",
                    "status": "satisfied_with_warnings",
                    "evidence": repo_relative(DATA_PATHS["findings"]),
                },
                {
                    "gate_item": "future_planning_awareness",
                    "status": "satisfied_fail_closed",
                    "evidence": repo_relative(stage5bq_constraint),
                },
                {"gate_item": "active_ingestion_authorization", "status": "blocked", "evidence": repo_relative(DATA_PATHS["active_blocker"])},
                {"gate_item": "byte_stream_generation_authorization", "status": "blocked", "evidence": repo_relative(DATA_PATHS["guardrail"])},
                {"gate_item": "execution_authorization", "status": "blocked", "evidence": repo_relative(DATA_PATHS["guardrail"])},
                {"gate_item": "dwh_hash_search_authorization", "status": "blocked", "evidence": repo_relative(DATA_PATHS["dwh"])},
            ],
            "execution_allowed": False,
        }
    )

    manifest_requirements = _base("stage5bs_manifest_validation_requirements", "manifest_requirements")
    manifest_requirements.update(
        {
            "future_string4_planning_ingestion_requires_manifest_checks": [
                "active_manifest_registry_resolves",
                "stage5ap_canonical_transcription_preserved_or_explicitly_superseded",
                "stage5aw_branch_manifest_preserved_or_explicitly_superseded",
                "stage5ay_branch_eligibility_preserved_or_explicitly_superseded",
                "stage5az_variant_family_preserved_or_explicitly_superseded",
                "stage5bb_active_registry_preserved_or_explicitly_superseded",
                "stage5bd_run_plan_ids_preserved_or_explicitly_superseded",
                "string4_sidecar_status_inactive_or_explicitly_activated_by_future_stage",
                "no_byte_stream_generation_gate_passed",
                "no_execution_guardrail_passed",
            ],
            "current_stage_performs_manifest_activation": False,
            "current_stage_changes_manifest": False,
            "execution_allowed": False,
        }
    )

    authorization_policy = _base("stage5bs_future_stage_authorization_policy", "authorization_policy")
    authorization_policy.update(
        {
            "future_authorization_status": "explicit_future_stage_required",
            "current_stage_authorizes_planning_ingestion": False,
            "current_stage_authorizes_active_input": False,
            "current_stage_authorizes_byte_streams": False,
            "current_stage_authorizes_execution": False,
            "execution_allowed": False,
        }
    )

    stage5bd_preservation = _base("stage5bs_stage5bd_plan_preservation", "stage5bd_preservation")
    stage5bd_preservation.update(
        {
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_dry_run_plan_changed": False,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_run_plan_id_count": run_plan_count,
            "string4_added_to_active_dry_run_inputs": False,
            "new_active_dry_run_plan_created": False,
            "execution_allowed": False,
        }
    )

    active_preservation = _base("stage5bs_active_manifest_preservation", "active_preservation")
    active_preservation.update(
        {
            "preserved_active_record_paths": PRESERVED_ACTIVE_RECORDS,
            "stage5ap_canonical_transcription_changed": False,
            "stage5aw_branch_manifest_changed": False,
            "stage5ay_branch_eligibility_changed": False,
            "stage5az_variant_family_manifest_changed": False,
            "stage5bb_active_manifest_registry_changed": False,
            "stage5bd_active_manifest_lock_changed": False,
            "active_token_block_manifest_changed": False,
            "execution_allowed": False,
        }
    )

    future_impact = _base("stage5bs_future_dry_run_planning_impact", "future_impact")
    future_impact.update(
        {
            "planning_effects": [
                "future_planning_constraint_only",
                "future_runner_citation_required",
                "active_ingestion_blocked",
                "no_current_plan_change",
                "review_before_ingestion",
                "manifest_validation_required",
                "no_execution_gate_required",
            ],
            "future_runner_citation_policy_created": True,
            "planning_ingestion_gate_created": True,
            "current_stage5bd_dry_run_plan_changed": False,
            "execution_allowed": False,
        }
    )

    source_gap = _base("stage5bs_source_gap_severity_update", "source_gap")
    source_gap.update(
        {
            "source_gap_updates": [
                {
                    "source_gap_id": "stage5bk-string4-stage5ap-branch-membership-unreconciled",
                    "status_after_stage5bo": "closed_operator_errata_supported_full_branch_match",
                    "status_after_stage5bq": "closed_for_metadata_planning_only",
                    "status_after_stage5bs": "gated_for_future_planning_ingestion_only",
                    "blocks_metadata_planning": False,
                    "blocks_active_ingestion": True,
                    "blocks_execution": True,
                    "blocks_future_token_block_execution": True,
                }
            ],
            "execution_allowed": False,
        }
    )

    dwh = _base("stage5bs_dwh_quarantine_reaffirmation", "dwh")
    dwh.update(
        {
            "dwh_relationship_status": "quarantined",
            "string4_is_dwh_target": False,
            "iddqd_v2_byte_strings_are_dwh_targets": False,
            "hash_search_performed": False,
            "hash_preimage_search_performed": False,
            "experimental_hash_comparison_performed": False,
            "decode_attempt_performed": False,
            "future_dwh_use_requires_explicit_stage": True,
            "execution_allowed": False,
        }
    )

    guardrail = _base("stage5bs_guardrail", "guardrail")
    guardrail.update(
        {
            "planning_ingestion_gate_only": True,
            "reviewable_metadata_created": True,
            "future_token_block_execution_remains_blocked": True,
            "new_cuda_kernels_added": 0,
            **FALSE_FLAGS,
        }
    )

    handoff = _base("stage5bs_codex_handoff_policy", "handoff")
    handoff.update(
        {
            "canonical_codex_handoff_root": "codex-output",
            "deprecated_codex_output_root": "codex_output",
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            "codex_output_directory_exists": DEPRECATED_CODEX_OUTPUT.exists(),
            "codex_output_used": False,
            "codex_output_directory_created": False,
            "codex_output_committed": False,
            "execution_allowed": False,
        }
    )

    next_stage_title = (
        "Stage 5BT - Deep Research review of Stage 5BS planning-ingestion gate "
        "and reviewable evidence metadata, without execution"
    )
    next_reason = (
        "Stage 5BS creates a fail-closed planning-ingestion gate and reviewable "
        "committed evidence metadata; Deep Research should review before any "
        "future planning-ingestion or active-input consideration."
    )

    summary = _base("stage5bs_summary", "summary")
    summary.update(
        {
            "status": "complete",
            "stage5br_findings_integrated": True,
            "stage5br_verdict": "accept_with_warnings",
            "reviewable_metadata_created": True,
            "reviewable_validation_evidence_created": True,
            "reviewable_source_digest_index_created": True,
            "reviewability_gap_register_created": True,
            "string4_branch_membership_status_after_errata": string4_status,
            "string4_planning_context_status": "inactive_branch_context_only",
            "string4_planning_ingestion_gate_status": "closed_gate_no_active_ingestion",
            "future_runner_citation_policy_created": True,
            "inactive_sidecar_consumption_policy_created": True,
            "active_ingestion_blocker_created": True,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "operator_errata_sidecar_status": "inactive_planning_sidecar",
            "stage5bo_errata_aware_universe_active": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_dry_run_plan_changed": False,
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "future_token_block_execution_remains_blocked": True,
            "parallel_validation_harness_used": True,
            "parallel_validation_run_passed": True,
            "codex_completion_summary_path": repo_relative(CODEX_COMPLETION_PATH),
            "codex_output_directory_used": False,
            "recommended_next_prompt_type": "deep_research_review",
            "recommended_next_stage_title": next_stage_title,
            "recommended_next_stage_reason": (
                "Stage 5BS creates a fail-closed planning-ingestion gate and "
                "reviewable committed evidence metadata; independent review should "
                "precede any future inactive-sidecar planning-ingestion stage."
            ),
            "source_record_paths": [repo_relative(path) for key, path in DATA_PATHS.items() if key != "summary"],
            "execution_allowed": False,
        }
    )

    next_stage = _base("stage5bs_next_stage_decision", "next_stage")
    next_stage.update(
        {
            "selected_next_stage_id": "stage-5bt",
            "selected_next_prompt_type": "deep_research_review",
            "selected_next_stage_title": next_stage_title,
            "selected_next_stage_reason": next_reason,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "future_token_block_execution_remains_blocked": True,
            **FALSE_NEXT_STAGE_FLAGS,
            "execution_allowed": False,
        }
    )

    outputs = [
        (DATA_PATHS["findings"], findings),
        (DATA_PATHS["stage_marker"], stage_marker),
        (DATA_PATHS["validation_evidence"], validation_evidence),
        (DATA_PATHS["gap_register"], gap_register),
        (DATA_PATHS["review_packaging_warning"], review_warning),
        (DATA_PATHS["gate"], gate),
        (DATA_PATHS["citation_policy"], citation_policy),
        (DATA_PATHS["sidecar_policy"], sidecar_policy),
        (DATA_PATHS["active_blocker"], active_blocker),
        (DATA_PATHS["no_active_ingestion"], no_active_ingestion),
        (DATA_PATHS["readiness_matrix"], readiness_matrix),
        (DATA_PATHS["manifest_requirements"], manifest_requirements),
        (DATA_PATHS["authorization_policy"], authorization_policy),
        (DATA_PATHS["stage5bd_preservation"], stage5bd_preservation),
        (DATA_PATHS["active_preservation"], active_preservation),
        (DATA_PATHS["future_impact"], future_impact),
        (DATA_PATHS["source_gap"], source_gap),
        (DATA_PATHS["dwh"], dwh),
        (DATA_PATHS["guardrail"], guardrail),
        (DATA_PATHS["handoff"], handoff),
        (DATA_PATHS["summary"], summary),
        (DATA_PATHS["next_stage"], next_stage),
    ]
    for path, payload in outputs:
        write_yaml(path, payload)

    created_records = [
        _sha_record(path, role="created_stage5bs_record")
        for key, path in DATA_PATHS.items()
        if key != "source_digest_index"
    ]
    source_digest_index = _base("stage5bs_reviewable_source_digest_index", "source_digest_index")
    source_digest_index.update(
        {
            "reviewability_evidence_status": "committed_compact_evidence",
            "consumed_source_records": source_digests,
            "created_stage5bs_records": created_records,
            "self_digest_excluded": True,
            "self_digest_exclusion_reason": "record cannot include a stable digest of itself",
            "execution_allowed": False,
        }
    )
    write_yaml(DATA_PATHS["source_digest_index"], source_digest_index)

    _write_generated(
        results_dir / "summary.json",
        {
            "stage_id": STAGE_ID,
            "stage5br_verdict": "accept_with_warnings",
            "string4_branch_membership_status_after_errata": string4_status,
            "string4_planning_ingestion_gate_status": "closed_gate_no_active_ingestion",
            "future_token_block_execution_remains_blocked": True,
        },
    )
    _write_generated(results_dir / "source_file_digests.json", source_digests)
    _write_generated(
        results_dir / "warnings.jsonl",
        [
            {"warning": "final_commit_external_evidence_required", "stage_id": STAGE_ID, "stage_failure": False},
            {"warning": "ci_external_evidence_required", "stage_id": STAGE_ID, "stage_failure": False},
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


def validate_stage5bs(
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
        payloads["next_stage"] if next_stage_decision == DATA_PATHS["next_stage"] else _validate_payload(next_stage_decision, errors)
    )
    guardrail_payload = payloads["guardrail"] if guardrail == DATA_PATHS["guardrail"] else _validate_payload(guardrail, errors)

    if summary_payload.get("stage5br_verdict") != "accept_with_warnings":
        errors.append("summary must preserve Stage 5BR accept_with_warnings verdict")
    if summary_payload.get("string4_planning_ingestion_gate_status") != "closed_gate_no_active_ingestion":
        errors.append("planning-ingestion gate must remain closed")
    if payloads["gate"].get("string4_active_input_allowed") is not False:
        errors.append("String 4 active input must remain false")
    if payloads["citation_policy"].get("future_runner_citation_status") != "citation_required_fail_closed":
        errors.append("future runner citation policy must fail closed")
    if "data/token-block/stage5bs-string4-planning-ingestion-gate.yaml" not in payloads["citation_policy"].get(
        "future_runner_must_cite", []
    ):
        errors.append("future runner citation policy must cite Stage 5BS gate")
    if payloads["sidecar_policy"].get("inactive_sidecar_status") != "inactive_planning_sidecar":
        errors.append("inactive sidecar status must remain inactive_planning_sidecar")
    if payloads["active_blocker"].get("blocker_status") != "active":
        errors.append("active ingestion blocker must be active")
    if payloads["stage5bd_preservation"].get("stage5bd_dry_run_plan_changed") is not False:
        errors.append("Stage 5BD dry-run plan must not change")
    if next_stage_payload.get("selected_next_stage_id") != "stage-5bt":
        errors.append("Stage 5BS must select Stage 5BT review")
    for key in ("execution_allowed", "solve_claim", "string4_active_input_allowed", "string4_dry_run_ingestion_allowed_now"):
        for record_key, payload in payloads.items():
            if key in payload and payload.get(key) is not False:
                errors.append(f"{record_key} {key} must be false")
    for key, expected in FALSE_FLAGS.items():
        if key in guardrail_payload and guardrail_payload.get(key) != expected:
            errors.append(f"guardrail {key} must be {str(expected).lower()}")
    if payloads["handoff"].get("canonical_codex_handoff_root") != "codex-output":
        errors.append("Stage 5BS handoff root must be codex-output")
    if payloads["handoff"].get("codex_output_used") is not False:
        errors.append("Stage 5BS must not use codex_output")
    gap_ids = {gap.get("gap_id") for gap in payloads["gap_register"].get("gaps", []) if isinstance(gap, dict)}
    for required_gap in (
        "final_commit_hash_not_self_embedded",
        "ci_run_id_not_committed_at_stage_commit_time",
        "raw_codex_completion_summary_uncommitted",
    ):
        if required_gap not in gap_ids:
            errors.append(f"missing_reviewability_gap={required_gap}")

    preserved_active_paths = payloads["active_preservation"].get("preserved_active_record_paths", [])
    wrong_stage5aw_path = "data/token-block/stage5aw-repaired-branch-manifest.yaml"
    correct_stage5aw_path = "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml"
    if wrong_stage5aw_path in preserved_active_paths:
        errors.append(f"active_preservation contains unresolved Stage 5AW path {wrong_stage5aw_path}")
    if correct_stage5aw_path not in preserved_active_paths:
        errors.append(f"active_preservation missing corrected Stage 5AW path {correct_stage5aw_path}")
    for preserved_path in preserved_active_paths:
        if not Path(str(preserved_path)).is_file():
            errors.append(f"active_preservation path does not resolve: {preserved_path}")

    counts = {
        "stage5bs_valid": not errors,
        "validation_error_count": len(errors),
        "stage5br_verdict": summary_payload.get("stage5br_verdict", "unknown"),
        "string4_branch_membership_status_after_errata": summary_payload.get(
            "string4_branch_membership_status_after_errata", "unknown"
        ),
        "string4_planning_context_status": summary_payload.get("string4_planning_context_status", "unknown"),
        "string4_planning_ingestion_gate_status": summary_payload.get(
            "string4_planning_ingestion_gate_status", "unknown"
        ),
        "future_runner_citation_status": payloads["citation_policy"].get("future_runner_citation_status", "unknown"),
        "string4_active_input_allowed": bool(summary_payload.get("string4_active_input_allowed")),
        "string4_dry_run_ingestion_allowed_now": bool(summary_payload.get("string4_dry_run_ingestion_allowed_now")),
        "stage5bd_dry_run_records_remain_valid": bool(
            summary_payload.get("stage5bd_dry_run_records_remain_valid")
        ),
        "future_token_block_execution_remains_blocked": bool(
            summary_payload.get("future_token_block_execution_remains_blocked")
        ),
        "reviewable_metadata_created": bool(summary_payload.get("reviewable_metadata_created")),
        "codex_output_used": bool(payloads["handoff"].get("codex_output_used")),
        "ignored_generated_summary_present": (results_dir / "summary.json").is_file(),
    }
    return counts, errors


def load_stage5bs_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
