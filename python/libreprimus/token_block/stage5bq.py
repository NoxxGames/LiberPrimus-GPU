"""Stage 5BQ inactive String 4 branch dry-run planning metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import repo_relative, sha256_file, write_json, write_yaml
from libreprimus.token_block.stage5bm import _read

STAGE_ID = "stage-5bq"
STAGE_TITLE = (
    "Stage 5BQ - Operator-errata-aware String 4 inactive-branch dry-run "
    "planning integration, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5bo"
SOURCE_PREVIOUS_COMMIT = "f4fcb94a6f43f5733491725e643eebea98a2d26b"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5bp"
SOURCE_DEEP_RESEARCH_REPORT = "10_LiberPrimus-GPU-Stage-5BP-Deep-Research-Review.md"

RESULTS_DIR = Path("experiments/results/token-block/stage5bq")
CODEX_COMPLETION_PATH = Path("codex-output/stage5bq-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

STAGE5BO_SUMMARY_PATH = Path("data/project-state/stage5bo-summary.yaml")
STAGE5BO_BRANCH_MEMBERSHIP_PATH = Path("data/token-block/stage5bo-string4-branch-membership-after-errata.yaml")
STAGE5BO_OPTION_UNIVERSE_PATH = Path("data/token-block/stage5bo-errata-aware-token-option-universe.yaml")
STAGE5BO_SOURCE_GAP_CLOSURE_PATH = Path("data/token-block/stage5bo-string4-source-gap-closure-after-errata.yaml")
STAGE5BO_PLANNING_CONSTRAINT_PATH = Path("data/token-block/stage5bo-string4-planning-constraint-update.yaml")
STAGE5BD_SUMMARY_PATH = Path("data/project-state/stage5bd-summary.yaml")
STAGE5BD_ACTIVE_LOCK_PATH = Path("data/token-block/stage5bd-active-manifest-lock.yaml")
STAGE5BD_DRY_RUN_PLAN_PATH = Path("data/token-block/stage5bd-dry-run-plan-manifest.yaml")
STAGE5BD_RUN_PLAN_REGISTRY_PATH = Path("data/token-block/stage5bd-run-plan-id-registry.yaml")

DATA_PATHS: dict[str, Path] = {
    "findings": Path("data/project-state/stage5bq-stage5bp-findings-integration.yaml"),
    "review_packaging_warning": Path("data/source-harvester/stage5bq-review-packaging-warning.yaml"),
    "string4_context": Path("data/token-block/stage5bq-string4-inactive-branch-planning-context.yaml"),
    "sidecar_status": Path("data/token-block/stage5bq-operator-errata-sidecar-status.yaml"),
    "dry_run_constraint": Path("data/token-block/stage5bq-errata-aware-dry-run-constraint-update.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5bq-string4-no-active-ingestion-proof.yaml"),
    "future_requirements": Path("data/token-block/stage5bq-future-dry-run-requirements.yaml"),
    "active_preservation": Path("data/token-block/stage5bq-active-manifest-preservation.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5bq-stage5bd-dry-run-lineage-preservation.yaml"),
    "future_impact": Path("data/token-block/stage5bq-future-dry-run-planning-impact.yaml"),
    "source_gap": Path("data/historical-route/stage5bq-source-gap-severity-update.yaml"),
    "dwh": Path("data/historical-route/stage5bq-dwh-quarantine-reaffirmation.yaml"),
    "guardrail": Path("data/historical-route/stage5bq-guardrail.yaml"),
    "handoff": Path("data/source-harvester/stage5bq-codex-handoff-policy.yaml"),
    "summary": Path("data/project-state/stage5bq-summary.yaml"),
    "next_stage": Path("data/project-state/stage5bq-next-stage-decision.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    "findings": "schemas/project-state/stage5bq-stage5bp-findings-integration-v0.schema.json",
    "review_packaging_warning": "schemas/source-harvester/stage5bq-review-packaging-warning-v0.schema.json",
    "string4_context": "schemas/token-block/stage5bq-string4-inactive-branch-planning-context-v0.schema.json",
    "sidecar_status": "schemas/token-block/stage5bq-operator-errata-sidecar-status-v0.schema.json",
    "dry_run_constraint": "schemas/token-block/stage5bq-errata-aware-dry-run-constraint-update-v0.schema.json",
    "no_active_ingestion": "schemas/token-block/stage5bq-string4-no-active-ingestion-proof-v0.schema.json",
    "future_requirements": "schemas/token-block/stage5bq-future-dry-run-requirements-v0.schema.json",
    "active_preservation": "schemas/token-block/stage5bq-active-manifest-preservation-v0.schema.json",
    "stage5bd_preservation": "schemas/token-block/stage5bq-stage5bd-dry-run-lineage-preservation-v0.schema.json",
    "future_impact": "schemas/token-block/stage5bq-future-dry-run-planning-impact-v0.schema.json",
    "source_gap": "schemas/historical-route/stage5bq-source-gap-severity-update-v0.schema.json",
    "dwh": "schemas/historical-route/stage5bq-dwh-quarantine-reaffirmation-v0.schema.json",
    "guardrail": "schemas/historical-route/stage5bq-guardrail-v0.schema.json",
    "handoff": "schemas/source-harvester/stage5bq-codex-handoff-policy-v0.schema.json",
    "summary": "schemas/project-state/stage5bq-summary-v0.schema.json",
    "next_stage": "schemas/project-state/stage5bq-next-stage-decision-v0.schema.json",
}

SOURCE_RECORD_PATHS = [repo_relative(path) for path in DATA_PATHS.values() if path.name not in {"stage5bq-summary.yaml"}]

FALSE_FLAGS: dict[str, bool] = {
    "active_stage5aw_records_mutated": False,
    "active_stage5ay_records_mutated": False,
    "active_stage5az_records_mutated": False,
    "active_stage5bd_records_mutated": False,
    "active_token_block_manifest_changed": False,
    "ai_ml_interpretation_performed": False,
    "audio_analysis_performed": False,
    "benchmark_performed": False,
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
    "iddqd_surface_combination_performed": False,
    "image_forensics_performed": False,
    "llm_vision_token_reading_performed": False,
    "method_status_upgraded": False,
    "mp3stego_execution_performed": False,
    "ocr_performed": False,
    "openpuff_execution_performed": False,
    "outguess_execution_performed": False,
    "page_boundaries_final": False,
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
    "stage5bd_dry_run_records_changed": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_branch_materialised_as_active": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_combined_with_2014_surfaces": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
    "template_bodies_committed": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "website_expansion_performed": False,
    "xor_attempt_performed": False,
    "transposition_attempt_performed": False,
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


def _sha_record(path: Path) -> dict[str, Any]:
    return {
        "path": repo_relative(path),
        "present": path.is_file(),
        "sha256": sha256_file(path) if path.is_file() else None,
    }


def build_stage5bq_planning_integration(
    *,
    stage5bo_summary: Path = STAGE5BO_SUMMARY_PATH,
    stage5bo_branch_membership: Path = STAGE5BO_BRANCH_MEMBERSHIP_PATH,
    stage5bo_option_universe: Path = STAGE5BO_OPTION_UNIVERSE_PATH,
    stage5bo_source_gap_closure: Path = STAGE5BO_SOURCE_GAP_CLOSURE_PATH,
    stage5bo_planning_constraint: Path = STAGE5BO_PLANNING_CONSTRAINT_PATH,
    stage5bd_summary: Path = STAGE5BD_SUMMARY_PATH,
    stage5bd_active_lock: Path = STAGE5BD_ACTIVE_LOCK_PATH,
    stage5bd_dry_run_plan: Path = STAGE5BD_DRY_RUN_PLAN_PATH,
    stage5bd_run_plan_registry: Path = STAGE5BD_RUN_PLAN_REGISTRY_PATH,
    results_dir: Path = RESULTS_DIR,
    out_findings: Path = DATA_PATHS["findings"],
    out_review_packaging_warning: Path = DATA_PATHS["review_packaging_warning"],
    out_string4_context: Path = DATA_PATHS["string4_context"],
    out_sidecar_status: Path = DATA_PATHS["sidecar_status"],
    out_dry_run_constraint: Path = DATA_PATHS["dry_run_constraint"],
    out_no_active_ingestion: Path = DATA_PATHS["no_active_ingestion"],
    out_future_requirements: Path = DATA_PATHS["future_requirements"],
    out_active_preservation: Path = DATA_PATHS["active_preservation"],
    out_stage5bd_preservation: Path = DATA_PATHS["stage5bd_preservation"],
    out_future_impact: Path = DATA_PATHS["future_impact"],
    out_source_gap: Path = DATA_PATHS["source_gap"],
    out_dwh: Path = DATA_PATHS["dwh"],
    out_guardrail: Path = DATA_PATHS["guardrail"],
    out_handoff: Path = DATA_PATHS["handoff"],
    out_summary: Path = DATA_PATHS["summary"],
    out_next_stage: Path = DATA_PATHS["next_stage"],
) -> dict[str, Any]:
    bo_summary = _read(stage5bo_summary)
    bo_branch = _read(stage5bo_branch_membership)
    bo_gap = _read(stage5bo_source_gap_closure)
    bd_summary = _read(stage5bd_summary)
    bd_run_registry = _read(stage5bd_run_plan_registry)

    source_files = {
        "stage5bo_summary": _sha_record(stage5bo_summary),
        "stage5bo_branch_membership": _sha_record(stage5bo_branch_membership),
        "stage5bo_option_universe": _sha_record(stage5bo_option_universe),
        "stage5bo_source_gap_closure": _sha_record(stage5bo_source_gap_closure),
        "stage5bo_planning_constraint": _sha_record(stage5bo_planning_constraint),
        "stage5bd_summary": _sha_record(stage5bd_summary),
        "stage5bd_active_lock": _sha_record(stage5bd_active_lock),
        "stage5bd_dry_run_plan": _sha_record(stage5bd_dry_run_plan),
        "stage5bd_run_plan_registry": _sha_record(stage5bd_run_plan_registry),
    }

    string4_status = str(bo_branch.get("string4_branch_membership_status_after_errata"))
    canonical_count = int(bo_branch.get("canonical_match_count", 0))
    stage5aw_noncanonical = int(bo_branch.get("stage5aw_supported_noncanonical_count", 0))
    operator_errata_noncanonical = int(bo_branch.get("operator_errata_supported_noncanonical_count", 0))
    unsupported_count = int(bo_branch.get("unsupported_position_count", 0))
    parser_inconclusive_count = int(bo_branch.get("parser_inconclusive_position_count", 0))
    run_plan_count = int(bd_run_registry.get("run_plan_id_count", 0))

    findings = _base("stage5bq_stage5bp_findings_integration", "findings")
    findings.update(
        {
            "stage5bp_verdict": "accept_with_warnings",
            "stage5bp_primary_conclusion": (
                "stage5bo_operator_errata_integration_coherent_but_string4_must_remain_inactive"
            ),
            "stage5bp_warnings": [
                "review_packaging_warning",
                "errata_classification_coarse_use_explicit_deltas",
                "do_not_ingest_string4_aggressively",
            ],
            "stage5bp_findings_integrated": [
                "string4_full_branch_match_in_inactive_errata_aware_universe",
                "active_records_unchanged",
                "source_gap_closed_metadata_only",
                "dry_run_ingestion_still_blocked",
                "execution_still_blocked",
            ],
            "stage5bp_recommended_next_stage": "stage-5bq",
            "execution_selected": False,
        }
    )

    review_warning = _base("stage5bq_review_packaging_warning", "review_packaging_warning")
    review_warning.update(
        {
            "zip_review_sufficient": True,
            "exact_final_commit_pin_missing_from_review_zip": True,
            "ignored_template_bodies_absent_from_review_zip": True,
            "ignored_spreadsheet_absent_from_review_zip": True,
            "ignored_codex_output_absent_from_review_zip": True,
            "warning_is_stage_failure": False,
            "recommended_future_resolution": [
                "include_archive_or_commit_marker_in_future_review_zips",
                "include_compact_local_source_root_marker_metadata_where_ignored_trees_are_omitted",
                "keep_raw_ignored_bodies_uncommitted",
            ],
            "execution_allowed": False,
        }
    )

    string4_context = _base("stage5bq_string4_inactive_branch_planning_context", "string4_context")
    string4_context.update(
        {
            "source_stage5bo_branch_membership": repo_relative(stage5bo_branch_membership),
            "source_stage5bo_option_universe": repo_relative(stage5bo_option_universe),
            "source_stage5bo_source_gap_closure": repo_relative(stage5bo_source_gap_closure),
            "string4_position_count_checked": int(bo_branch.get("string4_position_count_checked", 256)),
            "string4_branch_membership_status_after_errata": string4_status,
            "canonical_match_count": canonical_count,
            "stage5aw_supported_noncanonical_count": stage5aw_noncanonical,
            "operator_errata_supported_noncanonical_count": operator_errata_noncanonical,
            "unsupported_position_count": unsupported_count,
            "parser_inconclusive_position_count": parser_inconclusive_count,
            "string4_planning_context_status": "inactive_branch_context_only",
            "string4_active_input_allowed": False,
            "string4_execution_input_allowed": False,
            "string4_byte_stream_generation_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_active_ingestion_status": "blocked_pending_explicit_future_stage",
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "execution_allowed": False,
        }
    )

    sidecar = _base("stage5bq_operator_errata_sidecar_status", "sidecar_status")
    sidecar.update(
        {
            "source_errata_record": "data/token-block/stage5bo-token-case-human-review-errata.yaml",
            "source_errata_aware_universe": repo_relative(stage5bo_option_universe),
            "operator_errata_record_count": int(bo_summary.get("token_case_errata_record_count", 0)),
            "case_199_closes_string4_branch_blocker": bool(bo_summary.get("case_199_operator_errata_found")),
            "case_198_recorded": bool(bo_summary.get("case_198_operator_errata_found")),
            "operator_errata_sidecar_status": [
                "inactive_planning_sidecar",
                "citable_for_future_planning",
                "active_manifest_mutation_forbidden",
            ],
            "active_stage5aw_records_mutated": False,
            "active_stage5ay_records_mutated": False,
            "active_stage5az_records_mutated": False,
            "active_stage5bd_records_mutated": False,
            "future_stages_must_use_explicit_token_deltas_not_coarse_classification": True,
            "template_bodies_committed": False,
            "execution_allowed": False,
        }
    )

    dry_run_constraint = _base("stage5bq_errata_aware_dry_run_constraint_update", "dry_run_constraint")
    dry_run_constraint.update(
        {
            "source_stage5bd_dry_run_plan": repo_relative(stage5bd_dry_run_plan),
            "source_stage5bd_active_manifest_lock": repo_relative(stage5bd_active_lock),
            "source_stage5bo_branch_membership": repo_relative(stage5bo_branch_membership),
            "dry_run_planning_effects": [
                "future_planning_constraint_only",
                "future_runner_citation_required",
                "active_ingestion_blocked",
                "no_current_plan_change",
                "review_before_ingestion",
            ],
            "future_runner_must_cite": [
                repo_relative(stage5bo_branch_membership),
                repo_relative(stage5bo_option_universe),
                repo_relative(out_string4_context),
            ],
            "current_stage5bd_dry_run_plan_changed": False,
            "current_run_plan_ids_changed": False,
            "new_active_dry_run_plan_created": False,
            "string4_added_to_active_dry_run_inputs": False,
            "string4_active_input_allowed": False,
            "execution_allowed": False,
        }
    )

    no_active_ingestion = _base("stage5bq_string4_no_active_ingestion_proof", "no_active_ingestion")
    no_active_ingestion.update(
        {
            "source_stage5bo_branch_membership": repo_relative(stage5bo_branch_membership),
            "source_stage5bd_dry_run_plan": repo_relative(stage5bd_dry_run_plan),
            "proof_scope": "committed_metadata_only",
            "source_file_digests": source_files,
            "stage5bd_run_plan_id_count": run_plan_count,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "string4_execution_input_allowed": False,
            "string4_byte_stream_generation_allowed": False,
            "stage5bo_errata_aware_universe_active": False,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "stage5bb_active_manifest_registry_changed": False,
            "stage5aw_branch_manifest_changed": False,
            "stage5ay_branch_eligibility_changed": False,
            "stage5az_variant_family_manifest_changed": False,
            "canonical_transcription_changed": False,
            "real_byte_stream_generated": False,
            "variant_materialisation_performed": False,
            "execution_allowed": False,
        }
    )

    future_requirements = _base("stage5bq_future_dry_run_requirements", "future_requirements")
    future_requirements.update(
        {
            "future_string4_dry_run_ingestion_requires": [
                "explicit_future_codex_no_execution_planning_ingestion_stage",
                "deep_research_or_operator_review_of_stage5bq_if_selected_by_next_stage",
                "manifest_validation",
                "active_manifest_preservation_or_explicit_supersession_policy",
                "no_byte_stream_generation_gate",
                "no_execution_guardrail_review",
                "source_gap_closure_status_verification",
                "clear_distinction_between_inactive_sidecar_and_active_input",
            ],
            "future_string4_execution_requires": [
                "not_authorised_by_stage5bq",
                "separate_execution_stage_prompt",
                "expected_outputs_or_null_controls_where_relevant",
                "explicit_hash_decode_stego_cuda_scope_if_ever_selected",
                "solve_claim_policy",
            ],
            "current_stage_allows_ingestion": False,
            "current_stage_allows_execution": False,
            "execution_allowed": False,
        }
    )

    active_preservation = _base("stage5bq_active_manifest_preservation", "active_preservation")
    active_preservation.update(
        {
            "preserved_records": {
                "stage5ap_canonical_transcription": "data/token-block/stage5ap-token-block-canonical-transcription.yaml",
                "stage5aw_branch_manifest": "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml",
                "stage5ay_branch_eligibility": "data/token-block/stage5ay-branch-eligibility-policy.yaml",
                "stage5az_variant_family_manifest": "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml",
                "stage5bb_active_manifest_registry": "data/token-block/stage5bb-active-manifest-registry.yaml",
                "stage5bd_active_manifest_lock": repo_relative(stage5bd_active_lock),
            },
            "canonical_transcription_changed": False,
            "stage5aw_branch_manifest_changed": False,
            "stage5ay_branch_eligibility_changed": False,
            "stage5az_variant_family_manifest_changed": False,
            "stage5bb_active_manifest_registry_changed": False,
            "stage5bd_active_manifest_lock_changed": False,
            "active_token_block_manifest_changed": False,
            "string4_branch_materialised_as_active": False,
            "execution_allowed": False,
        }
    )

    stage5bd_preservation = _base("stage5bq_stage5bd_dry_run_lineage_preservation", "stage5bd_preservation")
    stage5bd_preservation.update(
        {
            "source_stage5bd_summary": repo_relative(stage5bd_summary),
            "source_stage5bd_dry_run_plan": repo_relative(stage5bd_dry_run_plan),
            "source_stage5bd_run_plan_registry": repo_relative(stage5bd_run_plan_registry),
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_dry_run_records_changed": False,
            "run_plan_ids_changed": False,
            "new_run_plan_ids_created": False,
            "string4_added_to_dry_run_plan_inputs": False,
            "dry_run_plan_ids_remain_metadata_only": True,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_previous_recommended_next_stage": bd_summary.get("recommended_next_stage_title"),
            "real_byte_stream_generated": False,
            "variant_materialisation_performed": False,
            "execution_allowed": False,
        }
    )

    future_impact = _base("stage5bq_future_dry_run_planning_impact", "future_impact")
    future_impact.update(
        {
            "source_stage5bo_future_dry_run_planning_impact": "data/token-block/stage5bo-future-dry-run-planning-impact.yaml",
            "source_stage5bp_review": SOURCE_DEEP_RESEARCH_REPORT,
            "new_constraints_for_future_dry_run": [
                "string4_full_branch_match_is_inactive_planning_context_only",
                "operator_errata_sidecar_is_citable_but_not_active",
                "future_planning_must_use_explicit_token_deltas_not_coarse_errata_labels",
                "current_stage5bd_run_plans_remain_unchanged",
                "active_string4_ingestion_requires_future_explicit_stage",
                "no_byte_stream_generation_or_execution_is_authorised",
            ],
            "future_runner_must_cite_stage5bq_constraints": True,
            "execution_gate_default": "blocked",
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "real_byte_stream_generated": False,
            "hash_search_performed": False,
            "decode_attempt_performed": False,
            "scoring_performed": False,
            "execution_allowed": False,
        }
    )

    source_gap = _base("stage5bq_source_gap_severity_update", "source_gap")
    source_gap.update(
        {
            "source_stage5bo_gap_update": "data/historical-route/stage5bo-source-gap-severity-update.yaml",
            "source_stage5bo_closure": repo_relative(stage5bo_source_gap_closure),
            "source_gap_update_count": 1,
            "records": [
                {
                    "source_gap_id": "stage5bk-string4-stage5ap-branch-membership-unreconciled",
                    "source_gap_origin": "stage-5bm",
                    "affected_family": "token_block_page49_51_context",
                    "status_after_stage5bo": bo_gap.get(
                        "closure_status_after_errata", "closed_operator_errata_supported_full_branch_match"
                    ),
                    "status_after_stage5bq": "closed_for_metadata_planning_only",
                    "blocks_metadata_planning": False,
                    "blocks_string4_ingestion_or_active_use": True,
                    "blocks_future_token_block_execution": True,
                    "recommended_resolution": [
                        "Preserve as metadata-only errata closure.",
                        "Keep String 4 inactive until a future explicit no-execution planning-ingestion stage.",
                        "Require guardrail and manifest validation before any future ingestion.",
                    ],
                    "execution_allowed": False,
                }
            ],
            "execution_allowed": False,
        }
    )

    dwh = _base("stage5bq_dwh_quarantine_reaffirmation", "dwh")
    dwh.update(
        {
            "source_stage5bk_dwh_quarantine": "data/historical-route/stage5bk-dwh-quarantine-reaffirmation.yaml",
            "source_stage5bo_dwh_quarantine": "data/historical-route/stage5bo-dwh-quarantine-reaffirmation.yaml",
            "DWH_relationship_remains_quarantined": True,
            "iddqd_v2_byte_strings_are_not_dwh_targets": True,
            "string4_is_not_dwh_target": True,
            "hash_search_performed": False,
            "hash_preimage_search_performed": False,
            "hash_comparison_performed_as_experiment": False,
            "decode_attempt_performed": False,
            "execution_allowed": False,
        }
    )

    guardrail = _base("stage5bq_guardrail", "guardrail")
    guardrail.update(
        {
            "operator_errata_dry_run_planning_integration_only": True,
            "future_token_block_execution_remains_blocked": True,
            "new_cuda_kernels_added": 0,
            **FALSE_FLAGS,
        }
    )

    handoff = _base("stage5bq_codex_handoff_policy", "handoff")
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
        "Stage 5BR - Deep Research review of Stage 5BQ inactive-branch dry-run "
        "planning integration, without execution"
    )
    next_reason = (
        "Stage 5BQ creates fail-closed future dry-run planning awareness for String 4; "
        "Deep Research should review before any future planning-ingestion stage."
    )

    summary = _base("stage5bq_summary", "summary")
    summary.update(
        {
            "status": "complete",
            "stage5bp_findings_integrated": True,
            "stage5bp_verdict": "accept_with_warnings",
            "string4_branch_membership_status_after_errata": string4_status,
            "string4_planning_context_status": "inactive_branch_context_only",
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "operator_errata_sidecar_status": "inactive_planning_sidecar",
            "stage5bo_errata_aware_universe_active": False,
            "future_dry_run_planning_constraint_created": True,
            "stage5bd_dry_run_records_remain_valid": True,
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
                "Stage 5BQ makes future dry-run planning aware of String 4 inactive "
                "branch context while preserving all active-ingestion and execution "
                "blocks; independent review should precede any future planning-ingestion stage."
            ),
            "source_record_paths": SOURCE_RECORD_PATHS,
            "execution_allowed": False,
        }
    )

    next_stage = _base("stage5bq_next_stage_decision", "next_stage")
    next_stage.update(
        {
            "selected_next_stage_id": "stage-5br",
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
        (out_findings, findings),
        (out_review_packaging_warning, review_warning),
        (out_string4_context, string4_context),
        (out_sidecar_status, sidecar),
        (out_dry_run_constraint, dry_run_constraint),
        (out_no_active_ingestion, no_active_ingestion),
        (out_future_requirements, future_requirements),
        (out_active_preservation, active_preservation),
        (out_stage5bd_preservation, stage5bd_preservation),
        (out_future_impact, future_impact),
        (out_source_gap, source_gap),
        (out_dwh, dwh),
        (out_guardrail, guardrail),
        (out_handoff, handoff),
        (out_summary, summary),
        (out_next_stage, next_stage),
    ]
    for path, payload in outputs:
        write_yaml(path, payload)

    _write_generated(
        results_dir / "summary.json",
        {
            "stage_id": STAGE_ID,
            "stage5bp_verdict": "accept_with_warnings",
            "string4_branch_membership_status_after_errata": string4_status,
            "string4_planning_context_status": "inactive_branch_context_only",
            "future_token_block_execution_remains_blocked": True,
        },
    )
    _write_generated(results_dir / "source_file_digests.json", source_files)
    _write_generated(
        results_dir / "warnings.jsonl",
        [
            {
                "warning": "review_packaging_warning",
                "stage_id": STAGE_ID,
                "stage_failure": False,
            },
            {
                "warning": "errata_classification_coarse_use_explicit_deltas",
                "stage_id": STAGE_ID,
                "stage_failure": False,
            },
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


def validate_stage5bq(
    *,
    findings: Path = DATA_PATHS["findings"],
    string4_context: Path = DATA_PATHS["string4_context"],
    sidecar_status: Path = DATA_PATHS["sidecar_status"],
    dry_run_constraint: Path = DATA_PATHS["dry_run_constraint"],
    no_active_ingestion: Path = DATA_PATHS["no_active_ingestion"],
    future_requirements: Path = DATA_PATHS["future_requirements"],
    active_preservation: Path = DATA_PATHS["active_preservation"],
    stage5bd_preservation: Path = DATA_PATHS["stage5bd_preservation"],
    future_impact: Path = DATA_PATHS["future_impact"],
    source_gap: Path = DATA_PATHS["source_gap"],
    dwh: Path = DATA_PATHS["dwh"],
    guardrail: Path = DATA_PATHS["guardrail"],
    handoff: Path = DATA_PATHS["handoff"],
    summary: Path = DATA_PATHS["summary"],
    next_stage: Path = DATA_PATHS["next_stage"],
    review_packaging_warning: Path = DATA_PATHS["review_packaging_warning"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {
        "findings": _validate_payload(findings, errors),
        "review_packaging_warning": _validate_payload(review_packaging_warning, errors),
        "string4_context": _validate_payload(string4_context, errors),
        "sidecar_status": _validate_payload(sidecar_status, errors),
        "dry_run_constraint": _validate_payload(dry_run_constraint, errors),
        "no_active_ingestion": _validate_payload(no_active_ingestion, errors),
        "future_requirements": _validate_payload(future_requirements, errors),
        "active_preservation": _validate_payload(active_preservation, errors),
        "stage5bd_preservation": _validate_payload(stage5bd_preservation, errors),
        "future_impact": _validate_payload(future_impact, errors),
        "source_gap": _validate_payload(source_gap, errors),
        "dwh": _validate_payload(dwh, errors),
        "guardrail": _validate_payload(guardrail, errors),
        "handoff": _validate_payload(handoff, errors),
        "summary": _validate_payload(summary, errors),
        "next_stage": _validate_payload(next_stage, errors),
    }
    context = payloads["string4_context"]
    guardrail_payload = payloads["guardrail"]
    summary_payload = payloads["summary"]
    next_stage_payload = payloads["next_stage"]
    if context.get("string4_branch_membership_status_after_errata") != "full_branch_match":
        errors.append("String 4 must remain full_branch_match only as inactive context")
    for key in (
        "string4_active_input_allowed",
        "string4_dry_run_ingestion_allowed_now",
        "string4_execution_input_allowed",
        "string4_byte_stream_generation_allowed",
        "execution_allowed",
        "solve_claim",
    ):
        for record_key, payload in payloads.items():
            if key in payload and payload.get(key) is not False:
                errors.append(f"{record_key} {key} must be false")
    for key, expected in FALSE_FLAGS.items():
        if key in guardrail_payload and guardrail_payload.get(key) != expected:
            errors.append(f"guardrail {key} must be {str(expected).lower()}")
    if summary_payload.get("stage5bp_verdict") != "accept_with_warnings":
        errors.append("summary must preserve Stage 5BP accept_with_warnings verdict")
    if summary_payload.get("string4_planning_context_status") != "inactive_branch_context_only":
        errors.append("summary must mark String 4 as inactive planning context only")
    if summary_payload.get("stage5bd_dry_run_records_remain_valid") is not True:
        errors.append("Stage 5BD dry-run records must remain valid")
    if next_stage_payload.get("selected_next_prompt_type") != "deep_research_review":
        errors.append("Stage 5BQ must select a Deep Research review next")
    if next_stage_payload.get("token_block_execution_selected") is not False:
        errors.append("Stage 5BQ next stage must not select token-block execution")
    if payloads["handoff"].get("canonical_codex_handoff_root") != "codex-output":
        errors.append("Stage 5BQ handoff root must be codex-output")
    if payloads["handoff"].get("codex_output_used") is not False:
        errors.append("Stage 5BQ must not use codex_output")

    counts = {
        "stage5bq_valid": not errors,
        "validation_error_count": len(errors),
        "stage5bp_verdict": summary_payload.get("stage5bp_verdict", "unknown"),
        "string4_branch_membership_status_after_errata": context.get(
            "string4_branch_membership_status_after_errata", "unknown"
        ),
        "string4_planning_context_status": summary_payload.get("string4_planning_context_status", "unknown"),
        "string4_active_input_allowed": bool(context.get("string4_active_input_allowed")),
        "string4_dry_run_ingestion_allowed_now": bool(context.get("string4_dry_run_ingestion_allowed_now")),
        "stage5bd_dry_run_records_remain_valid": bool(
            summary_payload.get("stage5bd_dry_run_records_remain_valid")
        ),
        "future_token_block_execution_remains_blocked": bool(
            summary_payload.get("future_token_block_execution_remains_blocked")
        ),
        "codex_output_used": bool(payloads["handoff"].get("codex_output_used")),
        "ignored_generated_summary_present": (results_dir / "summary.json").is_file(),
    }
    return counts, errors


def load_stage5bq_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
