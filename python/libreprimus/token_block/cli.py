"""Typer CLI for Stage 5AP token-block source-lock records."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .alphabets import build_alphabet_registry
from .case_policy import build_case_policy
from .coordinates import build_coordinate_records
from .coordinate_validation import validate_coordinate_payload
from .dwh_context import build_dwh_context
from .mapping import build_mapping_preflight
from .models import (
    ALPHABET_PATH,
    COORDINATE_PATH,
    DWH_CONTEXT_PATH,
    IMAGE_PROVENANCE_PATH,
    MAPPING_PATH,
    NEXT_STAGE_DECISION_PATH,
    NULL_CONTROL_PATH,
    RESEARCH_SUMMARY_PATH,
    RESULTS_DIR,
    SOURCE_LOCK_PATH,
    SUMMARY_PATH,
    STAGE5AR_CASE_AMBIGUITIES_PATH,
    STAGE5AR_CASE_POLICY_PATH,
    STAGE5AR_COORDINATE_VALIDATION_PATH,
    STAGE5AR_DWH_CONTEXT_PATH,
    STAGE5AR_GUARDRAIL_PATH,
    STAGE5AR_IMAGE_VARIANTS_PATH,
    STAGE5AR_NEXT_STAGE_DECISION_PATH,
    STAGE5AR_NULL_CONTROL_UPDATE_PATH,
    STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH,
    STAGE5AR_PAGE_SPLIT_POLICY_PATH,
    STAGE5AR_PAGE_SPLIT_RECORDS_PATH,
    STAGE5AR_PIXEL_COORDINATE_POLICY_PATH,
    STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH,
    STAGE5AR_RESULTS_DIR,
    STAGE5AR_SOURCE_LOCK_UPDATE_PATH,
    STAGE5AR_SUMMARY_PATH,
    STAGE5AT_CANONICAL_CHALLENGE_SET_PATH,
    STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH,
    STAGE5AT_CASE_REVIEW_POLICY_PATH,
    STAGE5AT_CROP_MANIFEST_PATH,
    STAGE5AT_DECISION_TEMPLATE_PATH,
    STAGE5AT_DOC_DRIFT_PATH,
    STAGE5AT_DWH_CASE_CONTEXT_PATH,
    STAGE5AT_GUARDRAIL_PATH,
    STAGE5AT_NEXT_STAGE_DECISION_PATH,
    STAGE5AT_NULL_CONTROL_UPDATE_PATH,
    STAGE5AT_PACK_MANIFEST_PATH,
    STAGE5AT_RESULTS_DIR,
    STAGE5AT_REVIEW_PACK_ROOT,
    STAGE5AT_SUMMARY_PATH,
    STAGE5AT_VARIANT_REPAIR_PATH,
    STAGE5AU_CANONICAL_CHALLENGES_V2_PATH,
    STAGE5AU_CASE_CHALLENGES_V2_PATH,
    STAGE5AU_CROP_GEOMETRY_POLICY_PATH,
    STAGE5AU_CROP_QUALITY_PATH,
    STAGE5AU_DECISION_TEMPLATE_PATH,
    STAGE5AU_DWH_CONTEXT_PATH,
    STAGE5AU_GUARDRAIL_PATH,
    STAGE5AU_NEXT_STAGE_DECISION_PATH,
    STAGE5AU_NULL_CONTROL_UPDATE_PATH,
    STAGE5AU_PACK_MANIFEST_PATH,
    STAGE5AU_RESULTS_DIR,
    STAGE5AU_REVIEW_PACK_ROOT,
    STAGE5AU_SUMMARY_PATH,
    STAGE5AU_UI_COVERAGE_PATH,
    STAGE5AU_USABILITY_AUDIT_PATH,
    STAGE5AV_BRANCH_MANIFEST_PATH,
    STAGE5AV_CANONICAL_UPDATE_PATH,
    STAGE5AV_CONFIRMED_TOKENS_PATH,
    STAGE5AV_DECISION_FILE_INGEST_PATH,
    STAGE5AV_DECISION_FILE_VALIDATION_PATH,
    STAGE5AV_DWH_CONTEXT_PATH,
    STAGE5AV_GUARDRAIL_PATH,
    STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH,
    STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH,
    STAGE5AV_NEXT_STAGE_DECISION_PATH,
    STAGE5AV_NULL_CONTROL_UPDATE_PATH,
    STAGE5AV_PRIMARY60_IMPACT_PATH,
    STAGE5AV_RESULTS_DIR,
    STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH,
    STAGE5AV_SUMMARY_PATH,
    STAGE5AV_UNRESOLVED_VARIANTS_PATH,
    STAGE5AW_CANONICAL_UPDATE_PATH,
    STAGE5AW_DECISION_PARSER_AUDIT_PATH,
    STAGE5AW_DWH_CONTEXT_PATH,
    STAGE5AW_GUARDRAIL_PATH,
    STAGE5AW_MALFORMED_FRAGMENTS_PATH,
    STAGE5AW_NEXT_STAGE_DECISION_PATH,
    STAGE5AW_NULL_CONTROL_UPDATE_PATH,
    STAGE5AW_PARSER_POLICY_PATH,
    STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH,
    STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH,
    STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH,
    STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
    STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    STAGE5AW_RESULTS_DIR,
    STAGE5AW_SUMMARY_PATH,
    STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH,
    STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    STAGE5AY_BRANCH_COUNT_BUDGET_PATH,
    STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH,
    STAGE5AY_DWH_PREFLIGHT_CONTEXT_PATH,
    STAGE5AY_EXECUTION_GATES_PATH,
    STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH,
    STAGE5AY_GUARDRAIL_PATH,
    STAGE5AY_NEXT_STAGE_DECISION_PATH,
    STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH,
    STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH,
    STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH,
    STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH,
    STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH,
    STAGE5AY_RESULTS_DIR,
    STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH,
    STAGE5AY_SUMMARY_PATH,
    STAGE5AZ_DEEP_RESEARCH_READINESS_PATH,
    STAGE5AZ_DWH_MANIFEST_INTEGRITY_CONTEXT_PATH,
    STAGE5AZ_FAMILY_ID_UNIQUENESS_AUDIT_PATH,
    STAGE5AZ_FAMILY_TAXONOMY_MEMBERSHIP_POLICY_PATH,
    STAGE5AZ_GUARDRAIL_PATH,
    STAGE5AZ_MANIFEST_REFERENCE_AUDIT_PATH,
    STAGE5AZ_NEXT_STAGE_DECISION_PATH,
    STAGE5AZ_PREFLIGHT_MANIFEST_INTEGRITY_AUDIT_PATH,
    STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH,
    STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH,
    STAGE5AZ_REPAIRED_PREFLIGHT_DESIGN_POLICY_PATH,
    STAGE5AZ_RESULTS_DIR,
    STAGE5AZ_SUMMARY_PATH,
    STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    STAGE5BB_BRANCH_COUNTER_SUMMARY_PATH,
    STAGE5BB_BRANCH_ELIGIBILITY_REFERENCE_VALIDATION_PATH,
    STAGE5BB_DRY_RUN_PLAN_PREVIEW_PATH,
    STAGE5BB_DWH_RUNNER_CONTEXT_PATH,
    STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH,
    STAGE5BB_EXECUTION_GATE_VALIDATION_PATH,
    STAGE5BB_FAMILY_ENUMERATION_SUMMARY_PATH,
    STAGE5BB_FIXTURE_RESULT_SCHEMA_RECORDS_PATH,
    STAGE5BB_GUARDRAIL_PATH,
    STAGE5BB_LEGACY_POINTER_AUDIT_PATH,
    STAGE5BB_LOADER_SCAFFOLD_POLICY_PATH,
    STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH,
    STAGE5BB_MANIFEST_REFERENCE_VALIDATION_PATH,
    STAGE5BB_NEXT_STAGE_DECISION_PATH,
    STAGE5BB_NO_EXECUTION_PROOF_PATH,
    STAGE5BB_RESULT_SCHEMA_FIXTURE_POLICY_PATH,
    STAGE5BB_RESULTS_DIR,
    STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH,
    STAGE5BB_SUMMARY_PATH,
    STAGE5BB_VALIDATION_EVIDENCE_INDEX_PATH,
    STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH,
    STAGE5BD_ARCHIVE_MARKER_POLICY_PATH,
    STAGE5BD_ARCHIVE_REVIEW_MARKER_PATH,
    STAGE5BD_BRANCH_FAMILY_PLAN_COUNTERS_PATH,
    STAGE5BD_CONTROL_FAMILY_PLAN_COUNTERS_PATH,
    STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH,
    STAGE5BD_DRY_RUN_POLICY_PATH,
    STAGE5BD_DRY_RUN_REPORT_SCHEMA_PATH,
    STAGE5BD_DWH_DRY_RUN_CONTEXT_PATH,
    STAGE5BD_EXECUTION_GATE_DRY_RUN_VALIDATION_PATH,
    STAGE5BD_FIXTURE_DRY_RUN_RECORDS_PATH,
    STAGE5BD_FIXTURE_RESULT_EXAMPLE_POLICY_PATH,
    STAGE5BD_FUTURE_RESULT_PATH_POLICY_PATH,
    STAGE5BD_FUTURE_RESULT_PATH_VALIDATION_PATH,
    STAGE5BD_GUARDRAIL_PATH,
    STAGE5BD_NEXT_STAGE_DECISION_PATH,
    STAGE5BD_NO_BYTE_STREAM_PROOF_PATH,
    STAGE5BD_NULL_CONTROL_PLAN_COUNTERS_PATH,
    STAGE5BD_RESULTS_DIR,
    STAGE5BD_RUN_PLAN_ID_POLICY_PATH,
    STAGE5BD_RUN_PLAN_ID_REGISTRY_PATH,
    STAGE5BD_STAGE5BB_VALIDATION_EVIDENCE_CONSOLIDATION_PATH,
    STAGE5BD_SUMMARY_PATH,
    TRANSCRIPTION_PATH,
    read_yaml,
)
from .null_controls import build_null_control_plan
from .original_images import build_original_image_source_lock
from .page_split import build_page_split
from .pixel_coordinates import build_pixel_coordinates
from .provenance import build_source_lock
from .stage5ap import build_next_stage_decision, build_research_summary, build_summary
from .stage5ar import build_stage5ar_summary, build_stage5ar_updates, validate_stage5ar
from .stage5at import (
    build_case_challenge_sets,
    build_case_review_policy,
    build_doc_drift_repair_summary,
    build_dwh_case_context,
    build_null_control_case_update,
    build_review_pack,
    build_stage5at_summary,
    validate_stage5at,
)
from .stage5au import (
    audit_stage5at_review_pack_usability,
    build_crop_geometry_policy,
    build_review_pack_v2,
    build_stage5au_dwh_review_pack_context,
    build_stage5au_null_control_update,
    build_stage5au_summary,
    validate_stage5au,
)
from .stage5av import (
    build_stage5av_decision_records,
    build_stage5av_summary,
    build_stage5av_updates,
    build_stage5av_variant_branch_manifest,
    ingest_stage5av_decisions,
    validate_stage5av,
)
from .stage5aw import (
    audit_stage5aw_decision_parser,
    build_stage5aw_repaired_branch_manifest,
    build_stage5aw_summary,
    build_stage5aw_updates,
    repair_stage5aw_decision_variants,
    validate_stage5aw,
)
from .stage5ay import (
    build_stage5ay_control_manifests,
    build_stage5ay_execution_gates,
    build_stage5ay_preflight_design,
    build_stage5ay_summary,
    validate_stage5ay,
)
from .stage5az import (
    audit_stage5az_preflight_manifests,
    build_stage5az_readiness,
    build_stage5az_summary,
    repair_stage5az_variant_family_manifest,
    validate_stage5az,
)
from .stage5bb import (
    audit_stage5bb_legacy_pointers,
    build_stage5bb_active_manifest_registry,
    build_stage5bb_dry_run_preview,
    build_stage5bb_fixture_result_schema_records,
    build_stage5bb_runner_scaffold,
    build_stage5bb_summary,
    validate_stage5bb,
    validate_stage5bb_execution_gates,
    validate_stage5bb_manifest_references,
)
from .preflight_runner.stage5bd import (
    build_stage5bd_archive_marker,
    build_stage5bd_dry_run_plan,
    build_stage5bd_dry_run_policy,
    build_stage5bd_fixture_dry_run_records,
    build_stage5bd_future_result_path_validation,
    build_stage5bd_plan_counters,
    build_stage5bd_summary,
    build_stage5bd_validation_evidence,
    validate_stage5bd,
    validate_stage5bd_execution_gates,
)
from .stage5bm import (
    DATA_PATHS as STAGE5BM_DATA_PATHS,
    HISTORICAL_RESULTS_DIR as STAGE5BM_HISTORICAL_RESULTS_DIR,
    RESULTS_DIR as STAGE5BM_RESULTS_DIR,
    build_stage5bm_string4_reconciliation,
    stage5bm_summary,
    validate_stage5bm,
)
from .stage5bn import (
    DATA_PATHS as STAGE5BN_DATA_PATHS,
    RESULTS_DIR as STAGE5BN_RESULTS_DIR,
    build_stage5bn_summary_records,
    build_stage5bn_unsupported_position_review,
    load_stage5bn_summary,
    validate_stage5bn,
)
from .stage5bo import (
    DATA_PATHS as STAGE5BO_DATA_PATHS,
    ORIGINAL_TEMPLATE_PATH as STAGE5BO_ORIGINAL_TEMPLATE_PATH,
    RESULTS_DIR as STAGE5BO_RESULTS_DIR,
    build_stage5bo_decision_template_errata,
    load_stage5bo_summary,
    validate_stage5bo,
)
from .stage5bq import (
    DATA_PATHS as STAGE5BQ_DATA_PATHS,
    RESULTS_DIR as STAGE5BQ_RESULTS_DIR,
    STAGE5BD_ACTIVE_LOCK_PATH as STAGE5BQ_STAGE5BD_ACTIVE_LOCK_PATH,
    STAGE5BD_DRY_RUN_PLAN_PATH as STAGE5BQ_STAGE5BD_DRY_RUN_PLAN_PATH,
    STAGE5BD_RUN_PLAN_REGISTRY_PATH as STAGE5BQ_STAGE5BD_RUN_PLAN_REGISTRY_PATH,
    STAGE5BD_SUMMARY_PATH as STAGE5BQ_STAGE5BD_SUMMARY_PATH,
    STAGE5BO_BRANCH_MEMBERSHIP_PATH as STAGE5BQ_STAGE5BO_BRANCH_MEMBERSHIP_PATH,
    STAGE5BO_OPTION_UNIVERSE_PATH as STAGE5BQ_STAGE5BO_OPTION_UNIVERSE_PATH,
    STAGE5BO_PLANNING_CONSTRAINT_PATH as STAGE5BQ_STAGE5BO_PLANNING_CONSTRAINT_PATH,
    STAGE5BO_SOURCE_GAP_CLOSURE_PATH as STAGE5BQ_STAGE5BO_SOURCE_GAP_CLOSURE_PATH,
    STAGE5BO_SUMMARY_PATH as STAGE5BQ_STAGE5BO_SUMMARY_PATH,
    build_stage5bq_planning_integration,
    load_stage5bq_summary,
    validate_stage5bq,
)
from .stage5bs import (
    DATA_PATHS as STAGE5BS_DATA_PATHS,
    RESULTS_DIR as STAGE5BS_RESULTS_DIR,
    STAGE5BD_DRY_RUN_PLAN_PATH as STAGE5BS_STAGE5BD_DRY_RUN_PLAN_PATH,
    STAGE5BD_RUN_PLAN_REGISTRY_PATH as STAGE5BS_STAGE5BD_RUN_PLAN_REGISTRY_PATH,
    STAGE5BO_BRANCH_MEMBERSHIP_PATH as STAGE5BS_STAGE5BO_BRANCH_MEMBERSHIP_PATH,
    STAGE5BO_OPTION_UNIVERSE_PATH as STAGE5BS_STAGE5BO_OPTION_UNIVERSE_PATH,
    STAGE5BO_SOURCE_GAP_CLOSURE_PATH as STAGE5BS_STAGE5BO_SOURCE_GAP_CLOSURE_PATH,
    STAGE5BQ_CONSTRAINT_PATH as STAGE5BS_STAGE5BQ_CONSTRAINT_PATH,
    STAGE5BQ_CONTEXT_PATH as STAGE5BS_STAGE5BQ_CONTEXT_PATH,
    STAGE5BQ_NEXT_STAGE_PATH as STAGE5BS_STAGE5BQ_NEXT_STAGE_PATH,
    STAGE5BQ_NO_ACTIVE_INGESTION_PATH as STAGE5BS_STAGE5BQ_NO_ACTIVE_INGESTION_PATH,
    STAGE5BQ_REQUIREMENTS_PATH as STAGE5BS_STAGE5BQ_REQUIREMENTS_PATH,
    STAGE5BQ_SUMMARY_PATH as STAGE5BS_STAGE5BQ_SUMMARY_PATH,
    STAGE5BR_REPORT_PATH as STAGE5BS_STAGE5BR_REPORT_PATH,
    build_stage5bs_planning_ingestion_gate,
    load_stage5bs_summary,
    validate_stage5bs,
)
from .stage5bu import (
    DATA_PATHS as STAGE5BU_DATA_PATHS,
    RESULTS_DIR as STAGE5BU_RESULTS_DIR,
    STAGE5BS_ACTIVE_PRESERVATION_PATH as STAGE5BU_STAGE5BS_ACTIVE_PRESERVATION_PATH,
    STAGE5BT_REPORT_PATH as STAGE5BU_STAGE5BT_REPORT_PATH,
    build_stage5bu_lineage_path_repair,
    build_stage5bu_reviewability_records,
    load_stage5bu_summary,
    validate_stage5bu,
    validate_stage5bu_lineage_paths,
)
from .stage5bw import (
    DATA_PATHS as STAGE5BW_DATA_PATHS,
    RESULTS_DIR as STAGE5BW_RESULTS_DIR,
    build_stage5bw,
    load_stage5bw_summary,
    validate_stage5bw,
)
from .stage5by import (
    DATA_PATHS as STAGE5BY_DATA_PATHS,
    RESULTS_DIR as STAGE5BY_RESULTS_DIR,
    build_stage5by,
    load_stage5by_summary,
    validate_stage5by,
    validate_stage5by_sidecar_gates,
    validate_stage5by_source_digest_uniqueness,
)
from .stage5ca import (
    DATA_PATHS as STAGE5CA_DATA_PATHS,
    RESULTS_DIR as STAGE5CA_RESULTS_DIR,
    build_stage5ca,
    load_stage5ca_summary,
    validate_stage5ca,
    validate_stage5ca_activation_preconditions,
    validate_stage5ca_citation_contract,
    validate_stage5ca_fail_closed_triggers,
    validate_stage5ca_manifest_supersession_contract,
    validate_stage5ca_sidecar_gates,
)
from .stage5cc import (
    DATA_PATHS as STAGE5CC_DATA_PATHS,
    RESULTS_DIR as STAGE5CC_RESULTS_DIR,
    build_stage5cc,
    load_stage5cc_summary,
    validate_stage5cc,
    validate_stage5cc_activation_preconditions,
    validate_stage5cc_active_planning_input_preflight,
    validate_stage5cc_citation_contract,
    validate_stage5cc_fail_closed_triggers,
    validate_stage5cc_no_byte_stream_transition_gate,
    validate_stage5cc_no_execution_transition_gate,
    validate_stage5cc_sidecar_gates,
)
from .stage5ce import (
    DATA_PATHS as STAGE5CE_DATA_PATHS,
    RESULTS_DIR as STAGE5CE_RESULTS_DIR,
    build_stage5ce,
    load_stage5ce_summary,
    validate_stage5ce,
    validate_stage5ce_approval_gate,
    validate_stage5ce_citation_negative_tests,
    validate_stage5ce_no_byte_stream_transition_gate,
    validate_stage5ce_no_execution_transition_gate,
    validate_stage5ce_proposal_package,
)
from .stage5cg import (
    DATA_PATHS as STAGE5CG_DATA_PATHS,
    RESULTS_DIR as STAGE5CG_RESULTS_DIR,
    build_stage5cg,
    load_stage5cg_summary,
    validate_stage5cg,
    validate_stage5cg_active_planning_input_decision_scaffold,
    validate_stage5cg_combined_approval_gate,
    validate_stage5cg_deep_research_decision_scaffold,
    validate_stage5cg_no_byte_stream_transition_gate,
    validate_stage5cg_no_execution_transition_gate,
    validate_stage5cg_operator_decision_scaffold,
    validate_stage5cg_sidecar_gates,
    validate_stage5cg_stage5ce_wording_review,
)
from .stage5ci import (
    DATA_PATHS as STAGE5CI_DATA_PATHS,
    RESULTS_DIR as STAGE5CI_RESULTS_DIR,
    build_stage5ci,
    load_stage5ci_summary,
    validate_stage5ci,
    validate_stage5ci_activation_decision_template,
    validate_stage5ci_combined_approval_gate,
    validate_stage5ci_deep_research_acceptance_template,
    validate_stage5ci_negative_validation_contract,
    validate_stage5ci_operator_approval_template,
    validate_stage5ci_sidecar_gates,
)
from .stage5ck import (
    DATA_PATHS as STAGE5CK_DATA_PATHS,
    RESULTS_DIR as STAGE5CK_RESULTS_DIR,
    build_stage5ck,
    load_stage5ck_summary,
    validate_stage5ck,
    validate_stage5ck_activation_decision_fixtures,
    validate_stage5ck_deep_research_fixtures,
    validate_stage5ck_negative_validation_matrix,
    validate_stage5ck_operator_fixtures,
    validate_stage5ck_review_package,
    validate_stage5ck_sidecar_gates,
)
from .stage5cm import (
    DATA_PATHS as STAGE5CM_DATA_PATHS,
    RESULTS_DIR as STAGE5CM_RESULTS_DIR,
    build_stage5cm,
    load_stage5cm_summary,
    validate_stage5cm,
    validate_stage5cm_activation_decision_gate,
    validate_stage5cm_approval_readiness_boundary,
    validate_stage5cm_credential_redaction_policy,
    validate_stage5cm_end_to_end_readiness_boundary,
    validate_stage5cm_fixture_real_boundary,
    validate_stage5cm_real_approval_readiness,
    validate_stage5cm_sidecar_gates,
)
from .stage5co import (
    DATA_PATHS as STAGE5CO_DATA_PATHS,
    RESULTS_DIR as STAGE5CO_RESULTS_DIR,
    build_stage5co,
    load_stage5co_summary,
    validate_stage5co,
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
from .stage5cq import (
    DATA_PATHS as STAGE5CQ_DATA_PATHS,
    RESULTS_DIR as STAGE5CQ_RESULTS_DIR,
    build_stage5cq,
    load_stage5cq_summary,
    validate_stage5cq,
    validate_stage5cq_activation_nonauthorization,
    validate_stage5cq_combined_gate,
    validate_stage5cq_credential_redaction_policy,
    validate_stage5cq_handoff_restoration,
    validate_stage5cq_operator_decision_package,
    validate_stage5cq_prior_stage_preservation,
    validate_stage5cq_real_record_blocker,
    validate_stage5cq_sidecar_gates,
    validate_stage5cq_stage5co_preservation,
    validate_stage5cq_stage5cp_findings,
)
from .stage5cs import (
    DATA_PATHS as STAGE5CS_DATA_PATHS,
    RESULTS_DIR as STAGE5CS_RESULTS_DIR,
    build_stage5cs,
    load_stage5cs_summary,
    validate_stage5cs,
    validate_stage5cs_activation_nonauthorization,
    validate_stage5cs_combined_gate,
    validate_stage5cs_credential_redaction_policy,
    validate_stage5cs_decision_options,
    validate_stage5cs_handoff_continuity,
    validate_stage5cs_operator_decision_readiness,
    validate_stage5cs_options_nonselection,
    validate_stage5cs_prior_stage_preservation,
    validate_stage5cs_real_record_blocker,
    validate_stage5cs_sidecar_gates,
    validate_stage5cs_stage5co_preservation,
    validate_stage5cs_stage5cq_preservation,
    validate_stage5cs_stage5cr_findings,
)
from .stage5cu import (
    DATA_PATHS as STAGE5CU_DATA_PATHS,
    RESULTS_DIR as STAGE5CU_RESULTS_DIR,
    build_stage5cu,
    load_stage5cu_summary,
    validate_stage5cu,
    validate_stage5cu_activation_nonauthorization,
    validate_stage5cu_combined_gate,
    validate_stage5cu_credential_redaction_policy,
    validate_stage5cu_decision_option_negative_fixtures,
    validate_stage5cu_decision_options_preservation,
    validate_stage5cu_handoff_continuity,
    validate_stage5cu_operator_decision_readiness,
    validate_stage5cu_option_selection_misuse,
    validate_stage5cu_options_nonselection,
    validate_stage5cu_prior_stage_preservation,
    validate_stage5cu_real_decision_negative_fixtures,
    validate_stage5cu_real_record_blocker,
    validate_stage5cu_sidecar_gates,
    validate_stage5cu_stage5co_preservation,
    validate_stage5cu_stage5cq_preservation,
    validate_stage5cu_stage5cs_preservation,
    validate_stage5cu_stage5ct_findings,
)
from .stage5cw import (
    DATA_PATHS as STAGE5CW_DATA_PATHS,
    RESULTS_DIR as STAGE5CW_RESULTS_DIR,
    build_stage5cw,
    load_stage5cw_summary,
    validate_stage5cw,
    validate_stage5cw_activation_nonauthorization,
    validate_stage5cw_active_lineage_preservation,
    validate_stage5cw_combined_gate,
    validate_stage5cw_credential_redaction_policy,
    validate_stage5cw_future_real_decision_requirements,
    validate_stage5cw_handoff_continuity,
    validate_stage5cw_options_nonselection,
    validate_stage5cw_preflight_misuse,
    validate_stage5cw_real_decision_package_preflight,
    validate_stage5cw_real_record_blocker,
    validate_stage5cw_sidecar_gates,
    validate_stage5cw_stage5bd_preservation,
    validate_stage5cw_stage5cs_preservation,
    validate_stage5cw_stage5cu_preservation,
    validate_stage5cw_stage5cv_findings,
)
from .stage5cy import (
    DATA_PATHS as STAGE5CY_DATA_PATHS,
    RESULTS_DIR as STAGE5CY_RESULTS_DIR,
    build_stage5cy,
    load_stage5cy_summary,
    validate_stage5cy,
    validate_stage5cy_activation_nonauthorization,
    validate_stage5cy_active_lineage_preservation,
    validate_stage5cy_combined_gate,
    validate_stage5cy_credential_redaction_policy,
    validate_stage5cy_governance_scope_control,
    validate_stage5cy_handoff_continuity,
    validate_stage5cy_operator_option_selection_preflight,
    validate_stage5cy_option_selection_misuse,
    validate_stage5cy_option_selection_requirements,
    validate_stage5cy_options_nonselection,
    validate_stage5cy_real_decision_preflight_preservation,
    validate_stage5cy_real_record_blocker,
    validate_stage5cy_sidecar_gates,
    validate_stage5cy_stage5bd_preservation,
    validate_stage5cy_stage5cs_preservation,
    validate_stage5cy_stage5cu_preservation,
    validate_stage5cy_stage5cw_preservation,
    validate_stage5cy_stage5cx_findings,
    validate_stage5cy_validation_count_reconciliation,
)
from .transcription import build_transcription
from .validation import validate_stage5ap
from .variant_classifier import build_variant_classifier_repair_summary

console = Console()
app = typer.Typer(help="Stage 5AP page 49-51 token-block commands.", no_args_is_help=True)


@app.command("build-stage5ap-source-lock")
def build_stage5ap_source_lock_command(
    search_roots: list[Path] | None = typer.Option(None),
    results_dir: Path = typer.Option(RESULTS_DIR),
    out_source_lock: Path = typer.Option(SOURCE_LOCK_PATH),
    out_image_provenance: Path = typer.Option(IMAGE_PROVENANCE_PATH),
) -> None:
    roots = search_roots or [Path("third_party/LiberPrimusPages"), Path("data"), Path("research-inputs"), Path("website-export")]
    source, provenance = build_source_lock(
        search_roots=roots,
        out_source_lock=out_source_lock,
        out_image_provenance=out_image_provenance,
        results_dir=results_dir,
    )
    console.print(f"source_locked_page_image_count={source['source_locked_page_image_count']}")
    console.print(f"page_image_provenance_records={provenance['page_image_record_count']}")


@app.command("build-stage5ap-transcription")
def build_stage5ap_transcription_command(
    out: Path = typer.Option(TRANSCRIPTION_PATH),
    coordinates_out: Path = typer.Option(COORDINATE_PATH),
    results_dir: Path = typer.Option(RESULTS_DIR),
) -> None:
    record = build_transcription(out=out, results_dir=results_dir)
    coords = build_coordinate_records(transcription=out, out=coordinates_out, results_dir=results_dir)
    console.print(f"token_count={record['token_count']}")
    console.print(f"coordinate_record_count={coords['coordinate_record_count']}")


@app.command("build-stage5ap-alphabet-registry")
def build_stage5ap_alphabet_registry_command(
    transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    out: Path = typer.Option(ALPHABET_PATH),
) -> None:
    record = build_alphabet_registry(transcription=transcription, out=out)
    console.print(f"primary_alphabet_length={record['primary_alphabet_length']}")
    console.print(f"observed_suffix_count={record['observed_suffix_count']}")


@app.command("build-stage5ap-mapping-preflight")
def build_stage5ap_mapping_preflight_command(
    transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    out: Path = typer.Option(MAPPING_PATH),
    results_dir: Path = typer.Option(RESULTS_DIR),
) -> None:
    record = build_mapping_preflight(
        transcription=transcription,
        alphabet_registry=alphabet_registry,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"value_min={record['value_min']}")
    console.print(f"value_max={record['value_max']}")


@app.command("build-stage5ap-null-control-plan")
def build_stage5ap_null_control_plan_command(out: Path = typer.Option(NULL_CONTROL_PATH)) -> None:
    record = build_null_control_plan(out=out)
    console.print(f"null_control_count={record['null_control_count']}")


@app.command("build-stage5ap-dwh-context")
def build_stage5ap_dwh_context_command(out: Path = typer.Option(DWH_CONTEXT_PATH)) -> None:
    record = build_dwh_context(out=out)
    console.print(f"context_status={record['context_status']}")


@app.command("build-stage5ap-summary")
def build_stage5ap_summary_command(
    source_lock: Path = typer.Option(SOURCE_LOCK_PATH),
    image_provenance: Path = typer.Option(IMAGE_PROVENANCE_PATH),
    transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    coordinates: Path = typer.Option(COORDINATE_PATH),
    alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    mapping_preflight: Path = typer.Option(MAPPING_PATH),
    null_control_plan: Path = typer.Option(NULL_CONTROL_PATH),
    dwh_context: Path = typer.Option(DWH_CONTEXT_PATH),
    outguess_toolchain: Path = typer.Option("data/stego/stage5ap-outguess-toolchain-readiness.yaml"),
    outguess_matrix: Path = typer.Option("data/stego/stage5ap-outguess-positive-control-matrix.yaml"),
    outguess_historical: Path = typer.Option("data/stego/stage5ap-outguess-historical-fixture-readiness.yaml"),
    outguess_guardrail: Path = typer.Option("data/stego/stage5ap-outguess-guardrail.yaml"),
    research_summary_out: Path = typer.Option(RESEARCH_SUMMARY_PATH),
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(RESULTS_DIR),
) -> None:
    build_research_summary(
        source_lock=source_lock,
        transcription=transcription,
        alphabet_registry=alphabet_registry,
        mapping_preflight=mapping_preflight,
        dwh_context=dwh_context,
        out=research_summary_out,
    )
    decision = build_next_stage_decision(
        source_lock=source_lock,
        transcription=transcription,
        mapping_preflight=mapping_preflight,
        out=next_stage_decision_out,
    )
    summary = build_summary(
        source_lock=source_lock,
        image_provenance=image_provenance,
        transcription=transcription,
        coordinates=coordinates,
        alphabet_registry=alphabet_registry,
        mapping_preflight=mapping_preflight,
        null_control_plan=null_control_plan,
        dwh_context=dwh_context,
        outguess_toolchain=outguess_toolchain,
        outguess_matrix=outguess_matrix,
        outguess_historical=outguess_historical,
        outguess_guardrail=outguess_guardrail,
        research_summary=research_summary_out,
        next_stage_decision=next_stage_decision_out,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"deep_research_next_ready={str(decision['deep_research_next_ready']).lower()}")
    console.print(f"token_count={summary['token_count']}")


@app.command("validate-stage5ap")
def validate_stage5ap_command(
    source_lock: Path = typer.Option(SOURCE_LOCK_PATH),
    image_provenance: Path = typer.Option(IMAGE_PROVENANCE_PATH),
    transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    coordinates: Path = typer.Option(COORDINATE_PATH),
    alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    mapping_preflight: Path = typer.Option(MAPPING_PATH),
    null_control_plan: Path = typer.Option(NULL_CONTROL_PATH),
    dwh_context: Path = typer.Option(DWH_CONTEXT_PATH),
    research_summary: Path = typer.Option(RESEARCH_SUMMARY_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path | None = typer.Option(None),
    outguess_toolchain: Path | None = typer.Option(None),
    outguess_policy: Path | None = typer.Option(None),
    outguess_matrix: Path | None = typer.Option(None),
    outguess_historical: Path | None = typer.Option(None),
    outguess_guardrail: Path | None = typer.Option(None),
) -> None:
    _ = (results_dir, outguess_toolchain, outguess_policy, outguess_matrix, outguess_historical, outguess_guardrail)
    counts, errors = validate_stage5ap(
        source_lock=source_lock,
        image_provenance=image_provenance,
        transcription=transcription,
        coordinates=coordinates,
        alphabet_registry=alphabet_registry,
        mapping_preflight=mapping_preflight,
        null_control_plan=null_control_plan,
        dwh_context=dwh_context,
        research_summary=research_summary,
        next_stage_decision=next_stage_decision,
        summary=summary,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ap_valid=true")


@app.command("build-stage5ar-original-image-source-lock")
def build_stage5ar_original_image_source_lock_command(
    search_roots: list[Path] = typer.Option(
        [Path("third_party"), Path("research-inputs"), Path("website-export"), Path("data")]
    ),
    stage5ap_image_provenance: Path = typer.Option(IMAGE_PROVENANCE_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    out_variants: Path = typer.Option(STAGE5AR_IMAGE_VARIANTS_PATH),
) -> None:
    source, variants = build_original_image_source_lock(
        search_roots=search_roots,
        stage5ap_image_provenance=stage5ap_image_provenance,
        results_dir=results_dir,
        out_source_lock=out_source_lock,
        out_variants=out_variants,
    )
    console.print(f"selected_original_image_count={source['selected_original_image_count']}")
    console.print(f"variant_record_count={variants['variant_record_count']}")


@app.command("classify-stage5ar-image-variants")
def classify_stage5ar_image_variants_command(
    search_roots: list[Path] = typer.Option(
        [Path("third_party"), Path("research-inputs"), Path("website-export"), Path("data")]
    ),
    stage5ap_image_provenance: Path = typer.Option(IMAGE_PROVENANCE_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    out_variants: Path = typer.Option(STAGE5AR_IMAGE_VARIANTS_PATH),
) -> None:
    source, variants = build_original_image_source_lock(
        search_roots=search_roots,
        stage5ap_image_provenance=stage5ap_image_provenance,
        results_dir=results_dir,
        out_source_lock=out_source_lock,
        out_variants=out_variants,
    )
    console.print(f"selected_original_image_count={source['selected_original_image_count']}")
    console.print(f"variant_record_count={variants['variant_record_count']}")


@app.command("build-stage5ar-page-split")
def build_stage5ar_page_split_command(
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    original_image_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out_policy: Path = typer.Option(STAGE5AR_PAGE_SPLIT_POLICY_PATH),
    out_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
) -> None:
    policy, records = build_page_split(
        stage5ap_transcription=stage5ap_transcription,
        original_image_source_lock=original_image_source_lock,
        results_dir=results_dir,
        out_policy=out_policy,
        out_records=out_records,
    )
    console.print(f"page_split_status={policy['page_split_status']}")
    console.print(f"row_count_sum={records['row_count_sum']}")


@app.command("build-stage5ar-pixel-coordinates")
def build_stage5ar_pixel_coordinates_command(
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    stage5ap_logical_coordinates: Path = typer.Option(COORDINATE_PATH),
    original_image_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    page_split_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out_policy: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_POLICY_PATH),
    out_records: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
) -> None:
    policy, records = build_pixel_coordinates(
        stage5ap_transcription=stage5ap_transcription,
        stage5ap_logical_coordinates=stage5ap_logical_coordinates,
        original_image_source_lock=original_image_source_lock,
        page_split_records=page_split_records,
        results_dir=results_dir,
        out_policy=out_policy,
        out_records=out_records,
    )
    console.print(f"coordinate_method={policy['coordinate_method']}")
    console.print(f"token_coordinate_record_count={records['coordinate_record_count']}")


@app.command("build-stage5ar-case-policy")
def build_stage5ar_case_policy_command(
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    pixel_coordinate_records: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    out_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
) -> None:
    policy, ambiguities = build_case_policy(
        stage5ap_transcription=stage5ap_transcription,
        pixel_coordinate_records=pixel_coordinate_records,
        results_dir=results_dir,
        out_policy=out_policy,
        out_ambiguities=out_ambiguities,
    )
    console.print(f"ambiguity_record_count={ambiguities['ambiguity_record_count']}")
    console.print(f"unresolved_ambiguity_class_count={policy['unresolved_ambiguity_class_count']}")


@app.command("validate-stage5ar-coordinates")
def validate_stage5ar_coordinates_command(
    original_image_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    page_split_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
    pixel_coordinate_policy: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_POLICY_PATH),
    pixel_coordinate_records: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    case_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    case_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
    out: Path = typer.Option(STAGE5AR_COORDINATE_VALIDATION_PATH),
) -> None:
    record = validate_coordinate_payload(
        original_image_source_lock=original_image_source_lock,
        page_split_records=page_split_records,
        pixel_coordinate_policy=pixel_coordinate_policy,
        pixel_coordinate_records=pixel_coordinate_records,
        case_policy=case_policy,
        case_ambiguities=case_ambiguities,
        results_dir=results_dir,
        out=out,
    )
    console.print(f"coordinate_validation_status={record['coordinate_validation_status']}")
    console.print(f"validation_error_count={record['validation_error_count']}")
    if record["validation_error_count"]:
        raise typer.Exit(1)


@app.command("build-stage5ar-updates")
def build_stage5ar_updates_command(
    stage5ap_source_lock: Path = typer.Option(SOURCE_LOCK_PATH),
    stage5ap_null_control_plan: Path = typer.Option(NULL_CONTROL_PATH),
    coordinate_validation: Path = typer.Option(STAGE5AR_COORDINATE_VALIDATION_PATH),
    case_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    page_split_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
    out_source_lock_update: Path = typer.Option(STAGE5AR_SOURCE_LOCK_UPDATE_PATH),
    out_null_control_update: Path = typer.Option(STAGE5AR_NULL_CONTROL_UPDATE_PATH),
    out_dwh_context: Path = typer.Option(STAGE5AR_DWH_CONTEXT_PATH),
) -> None:
    source_update, null_update, dwh = build_stage5ar_updates(
        stage5ap_source_lock=stage5ap_source_lock,
        stage5ap_null_control_plan=stage5ap_null_control_plan,
        coordinate_validation=coordinate_validation,
        case_policy=case_policy,
        page_split_records=page_split_records,
        out_source_lock_update=out_source_lock_update,
        out_null_control_update=out_null_control_update,
        out_dwh_context=out_dwh_context,
    )
    console.print(f"updated_source_lock_status={source_update['updated_source_lock_status']}")
    console.print(f"coordinate_specific_controls_created={str(null_update['coordinate_specific_controls_created']).lower()}")
    console.print(f"dwh_defined={str(dwh['dwh_defined']).lower()}")


@app.command("build-stage5ar-summary")
def build_stage5ar_summary_command(
    original_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    variants: Path = typer.Option(STAGE5AR_IMAGE_VARIANTS_PATH),
    page_split_policy: Path = typer.Option(STAGE5AR_PAGE_SPLIT_POLICY_PATH),
    page_split_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
    pixel_coordinate_policy: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_POLICY_PATH),
    pixel_coordinate_records: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    case_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    case_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
    coordinate_validation: Path = typer.Option(STAGE5AR_COORDINATE_VALIDATION_PATH),
    source_lock_update: Path = typer.Option(STAGE5AR_SOURCE_LOCK_UPDATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AR_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AR_DWH_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5AR_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AR_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AR_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AR_RESULTS_DIR),
) -> None:
    _, next_stage, summary = build_stage5ar_summary(
        original_source_lock=original_source_lock,
        variants=variants,
        page_split_policy=page_split_policy,
        page_split_records=page_split_records,
        pixel_coordinate_policy=pixel_coordinate_policy,
        pixel_coordinate_records=pixel_coordinate_records,
        case_policy=case_policy,
        case_ambiguities=case_ambiguities,
        coordinate_validation=coordinate_validation,
        source_lock_update=source_lock_update,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
        results_dir=results_dir,
    )
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"token_pixel_coordinate_record_count={summary['token_pixel_coordinate_record_count']}")


@app.command("validate-stage5ar")
def validate_stage5ar_command(
    original_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    variants: Path = typer.Option(STAGE5AR_IMAGE_VARIANTS_PATH),
    page_split_policy: Path = typer.Option(STAGE5AR_PAGE_SPLIT_POLICY_PATH),
    page_split_records: Path = typer.Option(STAGE5AR_PAGE_SPLIT_RECORDS_PATH),
    pixel_coordinate_policy: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_POLICY_PATH),
    pixel_coordinate_records: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    case_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    case_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
    coordinate_validation: Path = typer.Option(STAGE5AR_COORDINATE_VALIDATION_PATH),
    source_lock_update: Path = typer.Option(STAGE5AR_SOURCE_LOCK_UPDATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AR_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AR_DWH_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AR_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AR_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AR_SUMMARY_PATH),
    results_dir: Path | None = typer.Option(None),
) -> None:
    _ = results_dir
    counts, errors = validate_stage5ar(
        original_source_lock=original_source_lock,
        variants=variants,
        page_split_policy=page_split_policy,
        page_split_records=page_split_records,
        pixel_coordinate_policy=pixel_coordinate_policy,
        pixel_coordinate_records=pixel_coordinate_records,
        case_policy=case_policy,
        case_ambiguities=case_ambiguities,
        coordinate_validation=coordinate_validation,
        source_lock_update=source_lock_update,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ar_valid=true")


@app.command("repair-stage5at-variant-classifier")
def repair_stage5at_variant_classifier_command(
    stage5ar_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    stage5ar_variants: Path = typer.Option(STAGE5AR_IMAGE_VARIANTS_PATH),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out: Path = typer.Option(STAGE5AT_VARIANT_REPAIR_PATH),
) -> None:
    summary = build_variant_classifier_repair_summary(
        stage5ar_source_lock=stage5ar_source_lock,
        stage5ar_variants=stage5ar_variants,
        results_dir=results_dir,
        out=out,
    )
    console.print(f"variant_classifier_repaired={str(summary['variant_classifier_repaired']).lower()}")
    console.print(f"unmodified_path_bug_test_passed={str(summary['unmodified_path_bug_test_passed']).lower()}")


@app.command("build-stage5at-case-review-policy")
def build_stage5at_case_review_policy_command(
    stage5ar_case_policy: Path = typer.Option(STAGE5AR_CASE_POLICY_PATH),
    stage5ar_case_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    out: Path = typer.Option(STAGE5AT_CASE_REVIEW_POLICY_PATH),
) -> None:
    policy = build_case_review_policy(
        stage5ar_case_policy=stage5ar_case_policy,
        stage5ar_case_ambiguities=stage5ar_case_ambiguities,
        stage5ap_transcription=stage5ap_transcription,
        out=out,
    )
    console.print(f"active_ambiguity_class_count={policy['active_ambiguity_class_count']}")
    console.print(f"active_classes_match_stage5ar_data={str(policy['active_classes_match_stage5ar_data']).lower()}")


@app.command("build-stage5at-case-challenge-set")
def build_stage5at_case_challenge_set_command(
    stage5ar_case_ambiguities: Path = typer.Option(STAGE5AR_CASE_AMBIGUITIES_PATH),
    stage5ar_pixel_coordinates: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    stage5ap_alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out_case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    out_canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
) -> None:
    case_payload, canonical_payload = build_case_challenge_sets(
        stage5ar_case_ambiguities=stage5ar_case_ambiguities,
        stage5ar_pixel_coordinates=stage5ar_pixel_coordinates,
        stage5ap_transcription=stage5ap_transcription,
        stage5ap_alphabet_registry=stage5ap_alphabet_registry,
        results_dir=results_dir,
        out_case_challenges=out_case_challenges,
        out_canonical_challenges=out_canonical_challenges,
    )
    console.print(f"case_review_challenge_count={case_payload['challenge_count']}")
    console.print(f"canonical_transcription_challenge_count={canonical_payload['challenge_count']}")


@app.command("build-stage5at-decision-template")
def build_stage5at_decision_template_command(
    stage5ar_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    stage5ar_pixel_coordinates: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    out_root: Path = typer.Option(STAGE5AT_REVIEW_PACK_ROOT),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out_crop_manifest: Path = typer.Option(STAGE5AT_CROP_MANIFEST_PATH),
    out_decision_template: Path = typer.Option(STAGE5AT_DECISION_TEMPLATE_PATH),
    out_pack_manifest: Path = typer.Option(STAGE5AT_PACK_MANIFEST_PATH),
) -> None:
    _, decision_template, _ = build_review_pack(
        stage5ar_source_lock=stage5ar_source_lock,
        stage5ar_pixel_coordinates=stage5ar_pixel_coordinates,
        case_challenges=case_challenges,
        canonical_challenges=canonical_challenges,
        out_root=out_root,
        results_dir=results_dir,
        out_crop_manifest=out_crop_manifest,
        out_decision_template=out_decision_template,
        out_pack_manifest=out_pack_manifest,
    )
    console.print(f"decision_template_records={decision_template['decision_count']}")
    console.print("template_status=empty_unfilled")


@app.command("build-stage5at-review-pack")
def build_stage5at_review_pack_command(
    stage5ar_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    stage5ar_pixel_coordinates: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    out_root: Path = typer.Option(STAGE5AT_REVIEW_PACK_ROOT),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out_crop_manifest: Path = typer.Option(STAGE5AT_CROP_MANIFEST_PATH),
    out_decision_template: Path = typer.Option(STAGE5AT_DECISION_TEMPLATE_PATH),
    out_pack_manifest: Path = typer.Option(STAGE5AT_PACK_MANIFEST_PATH),
) -> None:
    crop_manifest, _, pack_manifest = build_review_pack(
        stage5ar_source_lock=stage5ar_source_lock,
        stage5ar_pixel_coordinates=stage5ar_pixel_coordinates,
        case_challenges=case_challenges,
        canonical_challenges=canonical_challenges,
        out_root=out_root,
        results_dir=results_dir,
        out_crop_manifest=out_crop_manifest,
        out_decision_template=out_decision_template,
        out_pack_manifest=out_pack_manifest,
    )
    console.print(f"generated_crop_count={crop_manifest['crop_count']}")
    console.print(f"review_pack_zip_path={pack_manifest['review_pack_zip_path']}")


@app.command("build-stage5at-null-control-update")
def build_stage5at_null_control_update_command(
    stage5ar_null_control_update: Path = typer.Option(STAGE5AR_NULL_CONTROL_UPDATE_PATH),
    case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    out: Path = typer.Option(STAGE5AT_NULL_CONTROL_UPDATE_PATH),
) -> None:
    payload = build_null_control_case_update(
        stage5ar_null_control_update=stage5ar_null_control_update,
        case_challenges=case_challenges,
        out=out,
    )
    console.print(f"case_decision_controls_added={str(payload['case_decision_controls_added']).lower()}")
    console.print(f"value_sensitivity_controls_added={str(payload['value_sensitivity_controls_added']).lower()}")


@app.command("build-stage5at-dwh-case-context")
def build_stage5at_dwh_case_context_command(out: Path = typer.Option(STAGE5AT_DWH_CASE_CONTEXT_PATH)) -> None:
    payload = build_dwh_case_context(out=out)
    console.print(f"dwh_defined={str(payload['dwh_defined']).lower()}")
    console.print(f"hash_search_performed={str(payload['hash_search_performed']).lower()}")


@app.command("build-stage5at-summary")
def build_stage5at_summary_command(
    case_review_policy: Path = typer.Option(STAGE5AT_CASE_REVIEW_POLICY_PATH),
    case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    crop_manifest: Path = typer.Option(STAGE5AT_CROP_MANIFEST_PATH),
    decision_template: Path = typer.Option(STAGE5AT_DECISION_TEMPLATE_PATH),
    pack_manifest: Path = typer.Option(STAGE5AT_PACK_MANIFEST_PATH),
    variant_repair: Path = typer.Option(STAGE5AT_VARIANT_REPAIR_PATH),
    doc_drift_summary: Path = typer.Option(STAGE5AT_DOC_DRIFT_PATH),
    null_control_update: Path = typer.Option(STAGE5AT_NULL_CONTROL_UPDATE_PATH),
    dwh_case_context: Path = typer.Option(STAGE5AT_DWH_CASE_CONTEXT_PATH),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out_guardrail: Path = typer.Option(STAGE5AT_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AT_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AT_SUMMARY_PATH),
) -> None:
    guardrail, next_stage, summary = build_stage5at_summary(
        case_review_policy=case_review_policy,
        case_challenges=case_challenges,
        canonical_challenges=canonical_challenges,
        crop_manifest=crop_manifest,
        decision_template=decision_template,
        pack_manifest=pack_manifest,
        variant_repair=variant_repair,
        doc_drift_summary=doc_drift_summary,
        null_control_update=null_control_update,
        dwh_case_context=dwh_case_context,
        results_dir=results_dir,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
    )
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"case_review_challenge_count={summary['case_review_challenge_count']}")
    console.print(f"automatic_case_resolution_performed={str(guardrail['automatic_case_resolution_performed']).lower()}")


@app.command("build-stage5at-doc-drift-summary")
def build_stage5at_doc_drift_summary_command(
    case_review_policy: Path = typer.Option(STAGE5AT_CASE_REVIEW_POLICY_PATH),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
    out: Path = typer.Option(STAGE5AT_DOC_DRIFT_PATH),
) -> None:
    payload = build_doc_drift_repair_summary(case_review_policy=case_review_policy, results_dir=results_dir, out=out)
    console.print(f"doc_drift_repaired={str(payload['doc_drift_repaired']).lower()}")
    console.print(f"doc_drift_active_classes_match_data={str(payload['doc_drift_active_classes_match_data']).lower()}")


@app.command("validate-stage5at")
def validate_stage5at_command(
    case_review_policy: Path = typer.Option(STAGE5AT_CASE_REVIEW_POLICY_PATH),
    case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    crop_manifest: Path = typer.Option(STAGE5AT_CROP_MANIFEST_PATH),
    decision_template: Path = typer.Option(STAGE5AT_DECISION_TEMPLATE_PATH),
    pack_manifest: Path = typer.Option(STAGE5AT_PACK_MANIFEST_PATH),
    variant_repair: Path = typer.Option(STAGE5AT_VARIANT_REPAIR_PATH),
    doc_drift_summary: Path = typer.Option(STAGE5AT_DOC_DRIFT_PATH),
    null_control_update: Path = typer.Option(STAGE5AT_NULL_CONTROL_UPDATE_PATH),
    dwh_case_context: Path = typer.Option(STAGE5AT_DWH_CASE_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AT_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AT_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AT_SUMMARY_PATH),
    review_pack_root: Path = typer.Option(STAGE5AT_REVIEW_PACK_ROOT),
    results_dir: Path = typer.Option(STAGE5AT_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5at(
        case_review_policy=case_review_policy,
        case_challenges=case_challenges,
        canonical_challenges=canonical_challenges,
        crop_manifest=crop_manifest,
        decision_template=decision_template,
        pack_manifest=pack_manifest,
        variant_repair=variant_repair,
        doc_drift_summary=doc_drift_summary,
        null_control_update=null_control_update,
        dwh_case_context=dwh_case_context,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
        review_pack_root=review_pack_root,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5at_valid=true")


@app.command("audit-stage5at-review-pack-usability")
def audit_stage5at_review_pack_usability_command(
    stage5at_review_pack_root: Path = typer.Option(STAGE5AT_REVIEW_PACK_ROOT),
    stage5at_pack_manifest: Path = typer.Option(STAGE5AT_PACK_MANIFEST_PATH),
    stage5at_case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    stage5at_canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    results_dir: Path = typer.Option(STAGE5AU_RESULTS_DIR),
    out: Path = typer.Option(STAGE5AU_USABILITY_AUDIT_PATH),
) -> None:
    payload = audit_stage5at_review_pack_usability(
        stage5at_review_pack_root=stage5at_review_pack_root,
        stage5at_pack_manifest=stage5at_pack_manifest,
        stage5at_case_challenges=stage5at_case_challenges,
        stage5at_canonical_challenges=stage5at_canonical_challenges,
        results_dir=results_dir,
        out=out,
    )
    console.print(f"stage5at_pack_exists={str(payload['stage5at_pack_exists']).lower()}")
    console.print(f"stage5at_html_case_card_count={payload['stage5at_html_case_card_count']}")
    console.print(f"stage5at_manual_review_usable={str(payload['stage5at_manual_review_usable']).lower()}")
    console.print(f"repair_required={str(payload['repair_required']).lower()}")


@app.command("build-stage5au-crop-geometry-policy")
def build_stage5au_crop_geometry_policy_command(
    stage5ar_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    stage5ar_pixel_coordinates: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    out: Path = typer.Option(STAGE5AU_CROP_GEOMETRY_POLICY_PATH),
) -> None:
    payload = build_crop_geometry_policy(
        stage5ar_source_lock=stage5ar_source_lock,
        stage5ar_pixel_coordinates=stage5ar_pixel_coordinates,
        out=out,
    )
    console.print(f"source_original_images_only={str(payload['source_original_images_only']).lower()}")
    console.print(f"crop_type_count={len(payload['crop_types'])}")


@app.command("build-stage5au-review-pack-v2")
def build_stage5au_review_pack_v2_command(
    stage5ar_source_lock: Path = typer.Option(STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH),
    stage5ar_pixel_coordinates: Path = typer.Option(STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH),
    stage5at_case_challenges: Path = typer.Option(STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH),
    stage5at_canonical_challenges: Path = typer.Option(STAGE5AT_CANONICAL_CHALLENGE_SET_PATH),
    crop_geometry_policy: Path = typer.Option(STAGE5AU_CROP_GEOMETRY_POLICY_PATH),
    out_root: Path = typer.Option(STAGE5AU_REVIEW_PACK_ROOT),
    results_dir: Path = typer.Option(STAGE5AU_RESULTS_DIR),
    out_crop_quality: Path = typer.Option(STAGE5AU_CROP_QUALITY_PATH),
    out_case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    out_canonical_challenges_v2: Path = typer.Option(STAGE5AU_CANONICAL_CHALLENGES_V2_PATH),
    out_pack_manifest: Path = typer.Option(STAGE5AU_PACK_MANIFEST_PATH),
    out_ui_coverage: Path = typer.Option(STAGE5AU_UI_COVERAGE_PATH),
    out_decision_template: Path = typer.Option(STAGE5AU_DECISION_TEMPLATE_PATH),
) -> None:
    quality, cases, canonical, pack, ui = build_review_pack_v2(
        stage5ar_source_lock=stage5ar_source_lock,
        stage5ar_pixel_coordinates=stage5ar_pixel_coordinates,
        stage5at_case_challenges=stage5at_case_challenges,
        stage5at_canonical_challenges=stage5at_canonical_challenges,
        crop_geometry_policy=crop_geometry_policy,
        out_root=out_root,
        results_dir=results_dir,
        out_crop_quality=out_crop_quality,
        out_case_challenges_v2=out_case_challenges_v2,
        out_canonical_challenges_v2=out_canonical_challenges_v2,
        out_pack_manifest=out_pack_manifest,
        out_ui_coverage=out_ui_coverage,
        out_decision_template=out_decision_template,
    )
    console.print(f"case_challenges_rendered={cases['challenge_count']}")
    console.print(f"canonical_challenges_rendered={canonical['challenge_count']}")
    console.print(f"generated_crop_count={pack['generated_crop_count']}")
    console.print(f"overlay_count={quality['overlay_count']}")
    console.print(f"all_case_challenges_visible={str(ui['all_203_case_challenges_visible_or_linked']).lower()}")


@app.command("validate-stage5au-review-pack-v2")
def validate_stage5au_review_pack_v2_command(
    ui_coverage: Path = typer.Option(STAGE5AU_UI_COVERAGE_PATH),
    pack_manifest: Path = typer.Option(STAGE5AU_PACK_MANIFEST_PATH),
) -> None:
    ui = read_yaml(ui_coverage)
    pack = read_yaml(pack_manifest)
    console.print(f"case_challenges_rendered={ui['case_challenges_rendered']}")
    console.print(f"canonical_challenges_rendered={ui['canonical_challenges_rendered']}")
    console.print(f"review_pack_v2_zip_path={pack['review_pack_v2_zip_path']}")
    if not ui.get("manual_review_usable"):
        raise typer.Exit(1)
    console.print("token_block_stage5au_review_pack_v2_valid=true")


@app.command("build-stage5au-null-control-update")
def build_stage5au_null_control_update_command(
    stage5at_null_control_update: Path = typer.Option(STAGE5AT_NULL_CONTROL_UPDATE_PATH),
    case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    crop_quality: Path = typer.Option(STAGE5AU_CROP_QUALITY_PATH),
    out: Path = typer.Option(STAGE5AU_NULL_CONTROL_UPDATE_PATH),
) -> None:
    payload = build_stage5au_null_control_update(
        stage5at_null_control_update=stage5at_null_control_update,
        case_challenges_v2=case_challenges_v2,
        crop_quality=crop_quality,
        out=out,
    )
    console.print(f"review_pack_v2_null_controls_added={str(payload['review_pack_v2_null_controls_added']).lower()}")


@app.command("build-stage5au-dwh-review-pack-context")
def build_stage5au_dwh_review_pack_context_command(out: Path = typer.Option(STAGE5AU_DWH_CONTEXT_PATH)) -> None:
    payload = build_stage5au_dwh_review_pack_context(out=out)
    console.print(f"dwh_expansion={payload['dwh_expansion']}")
    console.print(f"hash_search_performed={str(payload['hash_search_performed']).lower()}")


@app.command("build-stage5au-summary")
def build_stage5au_summary_command(
    usability_audit: Path = typer.Option(STAGE5AU_USABILITY_AUDIT_PATH),
    crop_geometry_policy: Path = typer.Option(STAGE5AU_CROP_GEOMETRY_POLICY_PATH),
    crop_quality: Path = typer.Option(STAGE5AU_CROP_QUALITY_PATH),
    case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    canonical_challenges_v2: Path = typer.Option(STAGE5AU_CANONICAL_CHALLENGES_V2_PATH),
    pack_manifest: Path = typer.Option(STAGE5AU_PACK_MANIFEST_PATH),
    ui_coverage: Path = typer.Option(STAGE5AU_UI_COVERAGE_PATH),
    decision_template_v2: Path = typer.Option(STAGE5AU_DECISION_TEMPLATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AU_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AU_DWH_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5AU_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AU_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AU_SUMMARY_PATH),
) -> None:
    guard, next_stage, summary = build_stage5au_summary(
        usability_audit=usability_audit,
        crop_geometry_policy=crop_geometry_policy,
        crop_quality=crop_quality,
        case_challenges_v2=case_challenges_v2,
        canonical_challenges_v2=canonical_challenges_v2,
        pack_manifest=pack_manifest,
        ui_coverage=ui_coverage,
        decision_template_v2=decision_template_v2,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
    )
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"review_pack_v2_zip_sha256={summary['review_pack_v2_zip_sha256']}")
    console.print(f"automatic_case_resolution_performed={str(guard['automatic_case_resolution_performed']).lower()}")


@app.command("validate-stage5au")
def validate_stage5au_command(
    usability_audit: Path = typer.Option(STAGE5AU_USABILITY_AUDIT_PATH),
    crop_geometry_policy: Path = typer.Option(STAGE5AU_CROP_GEOMETRY_POLICY_PATH),
    crop_quality: Path = typer.Option(STAGE5AU_CROP_QUALITY_PATH),
    case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    canonical_challenges_v2: Path = typer.Option(STAGE5AU_CANONICAL_CHALLENGES_V2_PATH),
    pack_manifest: Path = typer.Option(STAGE5AU_PACK_MANIFEST_PATH),
    ui_coverage: Path = typer.Option(STAGE5AU_UI_COVERAGE_PATH),
    decision_template_v2: Path = typer.Option(STAGE5AU_DECISION_TEMPLATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AU_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AU_DWH_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AU_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AU_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AU_SUMMARY_PATH),
    review_pack_root: Path = typer.Option(STAGE5AU_REVIEW_PACK_ROOT),
    results_dir: Path = typer.Option(STAGE5AU_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5au(
        usability_audit=usability_audit,
        crop_geometry_policy=crop_geometry_policy,
        crop_quality=crop_quality,
        case_challenges_v2=case_challenges_v2,
        canonical_challenges_v2=canonical_challenges_v2,
        pack_manifest=pack_manifest,
        ui_coverage=ui_coverage,
        decision_template_v2=decision_template_v2,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
        review_pack_root=review_pack_root,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5au_valid=true")


@app.command("ingest-stage5av-decisions")
def ingest_stage5av_decisions_command(
    decision_file: Path = typer.Option(STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH),
    case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    canonical_challenges_v2: Path = typer.Option(STAGE5AU_CANONICAL_CHALLENGES_V2_PATH),
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    results_dir: Path = typer.Option(STAGE5AV_RESULTS_DIR),
    out_ingest: Path = typer.Option(STAGE5AV_DECISION_FILE_INGEST_PATH),
    out_validation: Path = typer.Option(STAGE5AV_DECISION_FILE_VALIDATION_PATH),
) -> None:
    ingest, validation = ingest_stage5av_decisions(
        decision_file=decision_file,
        case_challenges_v2=case_challenges_v2,
        canonical_challenges_v2=canonical_challenges_v2,
        stage5ap_transcription=stage5ap_transcription,
        results_dir=results_dir,
        out_ingest=out_ingest,
        out_validation=out_validation,
    )
    console.print(f"decision_file_found={str(ingest['decision_file_found']).lower()}")
    console.print(f"decision_record_count={ingest['decision_record_count']}")
    for decision, count in validation.get("decision_counts", {}).items():
        console.print(f"{decision}_count={count}")
    if validation.get("validation_error_count"):
        raise typer.Exit(1)


@app.command("validate-stage5av-decisions")
def validate_stage5av_decisions_command(
    validation: Path = typer.Option(STAGE5AV_DECISION_FILE_VALIDATION_PATH),
) -> None:
    payload = read_yaml(validation)
    console.print(f"valid_for_stage5av_integration={str(payload['valid_for_stage5av_integration']).lower()}")
    console.print(f"validation_error_count={payload['validation_error_count']}")
    console.print(f"validation_warning_count={payload['validation_warning_count']}")
    if payload.get("validation_error_count"):
        raise typer.Exit(1)


@app.command("build-stage5av-decision-records")
def build_stage5av_decision_records_command(
    decision_file: Path = typer.Option(STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH),
    validation: Path = typer.Option(STAGE5AV_DECISION_FILE_VALIDATION_PATH),
    case_challenges_v2: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    stage5ap_alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    results_dir: Path = typer.Option(STAGE5AV_RESULTS_DIR),
    out_decisions: Path = typer.Option(STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH),
    out_confirmed: Path = typer.Option(STAGE5AV_CONFIRMED_TOKENS_PATH),
    out_unresolved: Path = typer.Option(STAGE5AV_UNRESOLVED_VARIANTS_PATH),
    out_extras: Path = typer.Option(STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH),
) -> None:
    decisions, confirmed, unresolved, extras = build_stage5av_decision_records(
        decision_file=decision_file,
        validation=validation,
        case_challenges_v2=case_challenges_v2,
        stage5ap_alphabet_registry=stage5ap_alphabet_registry,
        results_dir=results_dir,
        out_decisions=out_decisions,
        out_confirmed=out_confirmed,
        out_unresolved=out_unresolved,
        out_extras=out_extras,
    )
    console.print(f"decision_record_count={decisions['decision_record_count']}")
    console.print(f"confirmed_token_count={confirmed['confirmed_token_count']}")
    console.print(f"unresolved_token_variant_count={unresolved['unresolved_token_variant_count']}")
    console.print(f"reviewer_extra_possible_token_count={extras['reviewer_extra_possible_token_count']}")


@app.command("build-stage5av-variant-branch-manifest")
def build_stage5av_variant_branch_manifest_command(
    decision_records: Path = typer.Option(STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH),
    unresolved_variants: Path = typer.Option(STAGE5AV_UNRESOLVED_VARIANTS_PATH),
    reviewer_extras: Path = typer.Option(STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH),
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    stage5ap_mapping_preflight: Path = typer.Option(MAPPING_PATH),
    results_dir: Path = typer.Option(STAGE5AV_RESULTS_DIR),
    out_impact: Path = typer.Option(STAGE5AV_PRIMARY60_IMPACT_PATH),
    out_branch_manifest: Path = typer.Option(STAGE5AV_BRANCH_MANIFEST_PATH),
) -> None:
    impact, manifest = build_stage5av_variant_branch_manifest(
        decision_records=decision_records,
        unresolved_variants=unresolved_variants,
        reviewer_extras=reviewer_extras,
        stage5ap_transcription=stage5ap_transcription,
        stage5ap_mapping_preflight=stage5ap_mapping_preflight,
        results_dir=results_dir,
        out_impact=out_impact,
        out_branch_manifest=out_branch_manifest,
    )
    console.print(f"branch_count_upper_bound_log10={impact['branch_count_upper_bound_log10']}")
    console.print(f"use_compact_branch_manifest={str(manifest['use_compact_branch_manifest']).lower()}")
    console.print(f"full_cartesian_product_enumerated={str(manifest['full_cartesian_product_enumerated']).lower()}")


@app.command("build-stage5av-updates")
def build_stage5av_updates_command(
    decision_records: Path = typer.Option(STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH),
    unresolved_variants: Path = typer.Option(STAGE5AV_UNRESOLVED_VARIANTS_PATH),
    impact_summary: Path = typer.Option(STAGE5AV_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AV_BRANCH_MANIFEST_PATH),
    out_canonical_update: Path = typer.Option(STAGE5AV_CANONICAL_UPDATE_PATH),
    out_null_control_update: Path = typer.Option(STAGE5AV_NULL_CONTROL_UPDATE_PATH),
    out_dwh_context: Path = typer.Option(STAGE5AV_DWH_CONTEXT_PATH),
) -> None:
    canonical, null_update, dwh = build_stage5av_updates(
        decision_records=decision_records,
        unresolved_variants=unresolved_variants,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        out_canonical_update=out_canonical_update,
        out_null_control_update=out_null_control_update,
        out_dwh_context=out_dwh_context,
    )
    console.print(f"canonical_transcription_changed={str(canonical['canonical_transcription_changed']).lower()}")
    console.print(f"null_controls_updated={str(null_update['baseline_current_control_preserved']).lower()}")
    console.print(f"dwh_defined={str(dwh['dwh_defined']).lower()}")


@app.command("build-stage5av-summary")
def build_stage5av_summary_command(
    ingest: Path = typer.Option(STAGE5AV_DECISION_FILE_INGEST_PATH),
    validation: Path = typer.Option(STAGE5AV_DECISION_FILE_VALIDATION_PATH),
    decision_records: Path = typer.Option(STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH),
    confirmed: Path = typer.Option(STAGE5AV_CONFIRMED_TOKENS_PATH),
    unresolved_variants: Path = typer.Option(STAGE5AV_UNRESOLVED_VARIANTS_PATH),
    reviewer_extras: Path = typer.Option(STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH),
    impact_summary: Path = typer.Option(STAGE5AV_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AV_BRANCH_MANIFEST_PATH),
    canonical_update: Path = typer.Option(STAGE5AV_CANONICAL_UPDATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AV_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AV_DWH_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5AV_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AV_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AV_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AV_RESULTS_DIR),
) -> None:
    guard, next_stage, summary = build_stage5av_summary(
        ingest=ingest,
        validation=validation,
        decision_records=decision_records,
        confirmed=confirmed,
        unresolved_variants=unresolved_variants,
        reviewer_extras=reviewer_extras,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        canonical_update=canonical_update,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
        results_dir=results_dir,
    )
    console.print(f"automatic_case_resolution_performed={str(guard['automatic_case_resolution_performed']).lower()}")
    console.print(f"next_stage={next_stage['next_stage_selected']}")
    console.print(f"decision_record_count={summary['decision_record_count']}")


@app.command("validate-stage5av")
def validate_stage5av_command(
    ingest: Path = typer.Option(STAGE5AV_DECISION_FILE_INGEST_PATH),
    validation: Path = typer.Option(STAGE5AV_DECISION_FILE_VALIDATION_PATH),
    decision_records: Path = typer.Option(STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH),
    confirmed: Path = typer.Option(STAGE5AV_CONFIRMED_TOKENS_PATH),
    unresolved_variants: Path = typer.Option(STAGE5AV_UNRESOLVED_VARIANTS_PATH),
    reviewer_extras: Path = typer.Option(STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH),
    impact_summary: Path = typer.Option(STAGE5AV_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AV_BRANCH_MANIFEST_PATH),
    canonical_update: Path = typer.Option(STAGE5AV_CANONICAL_UPDATE_PATH),
    null_control_update: Path = typer.Option(STAGE5AV_NULL_CONTROL_UPDATE_PATH),
    dwh_context: Path = typer.Option(STAGE5AV_DWH_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AV_GUARDRAIL_PATH),
    next_stage: Path = typer.Option(STAGE5AV_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AV_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AV_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5av(
        ingest=ingest,
        validation=validation,
        decision_records=decision_records,
        confirmed=confirmed,
        unresolved_variants=unresolved_variants,
        reviewer_extras=reviewer_extras,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        canonical_update=canonical_update,
        null_control_update=null_control_update,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage=next_stage,
        summary=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5av_valid=true")


@app.command("audit-stage5aw-decision-parser")
def audit_stage5aw_decision_parser_command(
    decision_file: Path = typer.Option(STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH),
    stage5av_extras: Path = typer.Option(STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH),
    stage5av_branch_manifest: Path = typer.Option(STAGE5AV_BRANCH_MANIFEST_PATH),
    results_dir: Path = typer.Option(STAGE5AW_RESULTS_DIR),
    out_audit: Path = typer.Option(STAGE5AW_DECISION_PARSER_AUDIT_PATH),
    out_policy: Path = typer.Option(STAGE5AW_PARSER_POLICY_PATH),
) -> None:
    audit, policy = audit_stage5aw_decision_parser(
        decision_file=decision_file,
        stage5av_extras=stage5av_extras,
        stage5av_branch_manifest=stage5av_branch_manifest,
        results_dir=results_dir,
        out_audit=out_audit,
        out_policy=out_policy,
    )
    console.print(f"stage5av_malformed_reviewer_extra_count={audit['stage5av_malformed_reviewer_extra_count']}")
    console.print(f"parser_policy_status={policy['policy_status']}")


@app.command("repair-stage5aw-decision-variants")
def repair_stage5aw_decision_variants_command(
    decision_file: Path = typer.Option(STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH),
    stage5au_case_challenges: Path = typer.Option(STAGE5AU_CASE_CHALLENGES_V2_PATH),
    stage5ap_alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    parser_policy: Path = typer.Option(STAGE5AW_PARSER_POLICY_PATH),
    results_dir: Path = typer.Option(STAGE5AW_RESULTS_DIR),
    out_decisions: Path = typer.Option(STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH),
    out_unresolved: Path = typer.Option(
        STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
        "--out-unresolved-variants",
        "--out-unresolved",
    ),
    out_extras: Path = typer.Option(
        STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
        "--out-reviewer-extras",
        "--out-extras",
    ),
    out_malformed: Path = typer.Option(STAGE5AW_MALFORMED_FRAGMENTS_PATH),
) -> None:
    decisions, unresolved, extras, malformed = repair_stage5aw_decision_variants(
        decision_file=decision_file,
        stage5au_case_challenges=stage5au_case_challenges,
        stage5ap_alphabet_registry=stage5ap_alphabet_registry,
        parser_policy=parser_policy,
        results_dir=results_dir,
        out_decisions=out_decisions,
        out_unresolved=out_unresolved,
        out_extras=out_extras,
        out_malformed=out_malformed,
    )
    console.print(f"repaired_decision_record_count={decisions['decision_record_count']}")
    console.print(f"repaired_unresolved_variant_count={unresolved['unresolved_token_variant_count']}")
    console.print(f"repaired_reviewer_extra_possible_token_count={extras['repaired_reviewer_extra_possible_token_count']}")
    console.print(f"malformed_possible_token_fragment_count={malformed['malformed_possible_token_fragment_count']}")


@app.command("build-stage5aw-repaired-branch-manifest")
def build_stage5aw_repaired_branch_manifest_command(
    repaired_decisions: Path = typer.Option(STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH),
    repaired_unresolved: Path = typer.Option(
        STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
        "--repaired-unresolved-variants",
        "--repaired-unresolved",
    ),
    repaired_extras: Path = typer.Option(
        STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
        "--repaired-reviewer-extras",
        "--repaired-extras",
    ),
    malformed_fragments: Path = typer.Option(STAGE5AW_MALFORMED_FRAGMENTS_PATH),
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    stage5ap_mapping_preflight: Path = typer.Option(MAPPING_PATH),
    results_dir: Path = typer.Option(STAGE5AW_RESULTS_DIR),
    out_impact: Path = typer.Option(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH),
    out_branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
) -> None:
    impact, manifest = build_stage5aw_repaired_branch_manifest(
        repaired_decisions=repaired_decisions,
        repaired_unresolved=repaired_unresolved,
        repaired_extras=repaired_extras,
        malformed_fragments=malformed_fragments,
        stage5ap_transcription=stage5ap_transcription,
        stage5ap_mapping_preflight=stage5ap_mapping_preflight,
        results_dir=results_dir,
        out_impact=out_impact,
        out_branch_manifest=out_branch_manifest,
    )
    console.print(f"primary60_mappable_option_count={impact['primary60_mappable_option_count']}")
    console.print(f"primary60_unmappable_option_count={impact['primary60_unmappable_option_count']}")
    console.print(f"branch_count_upper_bound_product={manifest['branch_count_upper_bound_product']}")


@app.command("build-stage5aw-updates")
def build_stage5aw_updates_command(
    repaired_unresolved: Path = typer.Option(
        STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
        "--repaired-unresolved-variants",
        "--repaired-unresolved",
    ),
    impact_summary: Path = typer.Option(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
    out_canonical_update: Path = typer.Option(STAGE5AW_CANONICAL_UPDATE_PATH),
    out_null_control: Path = typer.Option(
        STAGE5AW_NULL_CONTROL_UPDATE_PATH,
        "--out-null-control-update",
        "--out-null-control",
    ),
    out_dwh_context: Path = typer.Option(STAGE5AW_DWH_CONTEXT_PATH),
) -> None:
    canonical, null_control, dwh = build_stage5aw_updates(
        repaired_unresolved=repaired_unresolved,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        out_canonical_update=out_canonical_update,
        out_null_control=out_null_control,
        out_dwh_context=out_dwh_context,
    )
    console.print(f"canonical_transcription_changed={str(canonical['canonical_transcription_changed']).lower()}")
    console.print(f"future_preflight_must_use_stage5aw_repaired_manifest={str(null_control['future_preflight_must_use_stage5aw_repaired_manifest']).lower()}")
    console.print(f"dwh_defined={str(dwh['dwh_defined']).lower()}")


@app.command("build-stage5aw-summary")
def build_stage5aw_summary_command(
    audit: Path = typer.Option(STAGE5AW_DECISION_PARSER_AUDIT_PATH),
    policy: Path = typer.Option(STAGE5AW_PARSER_POLICY_PATH),
    repaired_decisions: Path = typer.Option(STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH),
    repaired_unresolved: Path = typer.Option(
        STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
        "--repaired-unresolved-variants",
        "--repaired-unresolved",
    ),
    repaired_extras: Path = typer.Option(
        STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
        "--repaired-reviewer-extras",
        "--repaired-extras",
    ),
    malformed_fragments: Path = typer.Option(STAGE5AW_MALFORMED_FRAGMENTS_PATH),
    impact_summary: Path = typer.Option(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
    canonical_update: Path = typer.Option(STAGE5AW_CANONICAL_UPDATE_PATH),
    null_control: Path = typer.Option(
        STAGE5AW_NULL_CONTROL_UPDATE_PATH,
        "--null-control-update",
        "--null-control",
    ),
    dwh_context: Path = typer.Option(STAGE5AW_DWH_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5AW_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AW_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AW_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AW_RESULTS_DIR),
) -> None:
    guard, next_stage, summary = build_stage5aw_summary(
        audit=audit,
        policy=policy,
        repaired_decisions=repaired_decisions,
        repaired_unresolved=repaired_unresolved,
        repaired_extras=repaired_extras,
        malformed_fragments=malformed_fragments,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        canonical_update=canonical_update,
        null_control=null_control,
        dwh_context=dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
        results_dir=results_dir,
    )
    console.print(f"parser_repair_only={str(guard['parser_repair_only']).lower()}")
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"stage5aw_repaired_reviewer_extra_possible_token_count={summary['stage5aw_repaired_reviewer_extra_possible_token_count']}")


@app.command("validate-stage5aw")
def validate_stage5aw_command(
    audit: Path = typer.Option(STAGE5AW_DECISION_PARSER_AUDIT_PATH),
    policy: Path = typer.Option(STAGE5AW_PARSER_POLICY_PATH),
    repaired_decisions: Path = typer.Option(STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH),
    repaired_unresolved: Path = typer.Option(
        STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
        "--repaired-unresolved-variants",
        "--repaired-unresolved",
    ),
    repaired_extras: Path = typer.Option(
        STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
        "--repaired-reviewer-extras",
        "--repaired-extras",
    ),
    malformed_fragments: Path = typer.Option(STAGE5AW_MALFORMED_FRAGMENTS_PATH),
    impact_summary: Path = typer.Option(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH),
    branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
    canonical_update: Path = typer.Option(STAGE5AW_CANONICAL_UPDATE_PATH),
    null_control: Path = typer.Option(
        STAGE5AW_NULL_CONTROL_UPDATE_PATH,
        "--null-control-update",
        "--null-control",
    ),
    dwh_context: Path = typer.Option(STAGE5AW_DWH_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AW_GUARDRAIL_PATH),
    next_stage: Path = typer.Option(STAGE5AW_NEXT_STAGE_DECISION_PATH, "--next-stage-decision", "--next-stage"),
    summary: Path = typer.Option(STAGE5AW_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AW_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5aw(
        audit=audit,
        policy=policy,
        repaired_decisions=repaired_decisions,
        repaired_unresolved=repaired_unresolved,
        repaired_extras=repaired_extras,
        malformed_fragments=malformed_fragments,
        impact_summary=impact_summary,
        branch_manifest=branch_manifest,
        canonical_update=canonical_update,
        null_control=null_control,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage=next_stage,
        summary=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5aw_valid=true")


@app.command("build-stage5ay-preflight-design")
def build_stage5ay_preflight_design_command(
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    stage5ap_alphabet_registry: Path = typer.Option(ALPHABET_PATH),
    stage5ap_mapping_preflight: Path = typer.Option(MAPPING_PATH),
    stage5ar_coordinate_validation: Path = typer.Option(STAGE5AR_COORDINATE_VALIDATION_PATH),
    stage5aw_branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
    stage5aw_impact_summary: Path = typer.Option(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH),
    stage5aw_null_control: Path = typer.Option(STAGE5AW_NULL_CONTROL_UPDATE_PATH),
    stage5ax_run_summary: Path = typer.Option("data/ci/stage5ax-parallel-validation-run-summary.yaml"),
    results_dir: Path = typer.Option(STAGE5AY_RESULTS_DIR),
    out_source_inputs: Path = typer.Option(STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH),
    out_policy: Path = typer.Option(STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH),
    out_branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    out_branch_budget: Path = typer.Option(STAGE5AY_BRANCH_COUNT_BUDGET_PATH),
) -> None:
    source_inputs, policy, eligibility, budget = build_stage5ay_preflight_design(
        stage5ap_transcription=stage5ap_transcription,
        stage5ap_alphabet_registry=stage5ap_alphabet_registry,
        stage5ap_mapping_preflight=stage5ap_mapping_preflight,
        stage5ar_coordinate_validation=stage5ar_coordinate_validation,
        stage5aw_branch_manifest=stage5aw_branch_manifest,
        stage5aw_impact_summary=stage5aw_impact_summary,
        stage5aw_null_control=stage5aw_null_control,
        stage5ax_run_summary=stage5ax_run_summary,
        results_dir=results_dir,
        out_source_inputs=out_source_inputs,
        out_policy=out_policy,
        out_branch_eligibility=out_branch_eligibility,
        out_branch_budget=out_branch_budget,
    )
    console.print(f"source_input_record_count={source_inputs['source_record_count']}")
    console.print(f"branch_eligibility_option_record_count={eligibility['option_record_count']}")
    console.print(f"branch_upper_bound_product={budget['branch_count_upper_bound_product']}")
    console.print(f"stage5aw_repaired_branch_manifest_used={str(policy['stage5aw_repaired_branch_manifest_used']).lower()}")


@app.command("build-stage5ay-control-manifests")
def build_stage5ay_control_manifests_command(
    preflight_policy: Path = typer.Option(STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH),
    branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    stage5ap_null_control: Path = typer.Option(NULL_CONTROL_PATH),
    stage5aw_null_control: Path = typer.Option(STAGE5AW_NULL_CONTROL_UPDATE_PATH),
    results_dir: Path = typer.Option(STAGE5AY_RESULTS_DIR),
    out_variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    out_null_control_family: Path = typer.Option(STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH),
    out_alphabet_control: Path = typer.Option(STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH),
    out_reading_order: Path = typer.Option(STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH),
    out_page_split: Path = typer.Option(STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH),
    out_source_control: Path = typer.Option(STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH),
) -> None:
    variant, null_control, alphabet, reading, page_split, source = build_stage5ay_control_manifests(
        preflight_policy=preflight_policy,
        branch_eligibility=branch_eligibility,
        stage5ap_null_control=stage5ap_null_control,
        stage5aw_null_control=stage5aw_null_control,
        results_dir=results_dir,
        out_variant_family=out_variant_family,
        out_null_control_family=out_null_control_family,
        out_alphabet_control=out_alphabet_control,
        out_reading_order=out_reading_order,
        out_page_split=out_page_split,
        out_source_control=out_source_control,
    )
    control_count = (
        len(null_control["families"])
        + len(alphabet["families"])
        + len(reading["families"])
        + len(page_split["families"])
        + len(source["families"])
    )
    console.print(f"variant_family_count={variant['family_count']}")
    console.print(f"control_family_count={control_count}")
    console.print("controls_executed=false")


@app.command("build-stage5ay-execution-gates")
def build_stage5ay_execution_gates_command(
    source_inputs: Path = typer.Option(STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH),
    branch_budget: Path = typer.Option(STAGE5AY_BRANCH_COUNT_BUDGET_PATH),
    variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    null_control_family: Path = typer.Option(STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH),
    results_dir: Path = typer.Option(STAGE5AY_RESULTS_DIR),
    out_result_schema_preview: Path = typer.Option(STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH),
    out_execution_gates: Path = typer.Option(STAGE5AY_EXECUTION_GATES_PATH),
    out_dwh_context: Path = typer.Option(STAGE5AY_DWH_PREFLIGHT_CONTEXT_PATH),
) -> None:
    result_schema, gates, dwh = build_stage5ay_execution_gates(
        source_inputs=source_inputs,
        branch_budget=branch_budget,
        variant_family=variant_family,
        null_control_family=null_control_family,
        results_dir=results_dir,
        out_result_schema_preview=out_result_schema_preview,
        out_execution_gates=out_execution_gates,
        out_dwh_context=out_dwh_context,
    )
    console.print(f"execution_gate_count={len(gates['gates'])}")
    console.print(f"dwh_operational_status={dwh['dwh_operational_status']}")
    console.print(f"future_result_schema_preview_only={str(result_schema['future_result_schema_preview_only']).lower()}")


@app.command("build-stage5ay-summary")
def build_stage5ay_summary_command(
    source_inputs: Path = typer.Option(STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH),
    policy: Path = typer.Option(STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH),
    branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    null_control_family: Path = typer.Option(STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH),
    alphabet_control: Path = typer.Option(STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH),
    reading_order: Path = typer.Option(STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH),
    page_split: Path = typer.Option(STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH),
    source_control: Path = typer.Option(STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH),
    branch_budget: Path = typer.Option(STAGE5AY_BRANCH_COUNT_BUDGET_PATH),
    result_schema_preview: Path = typer.Option(STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH),
    execution_gates: Path = typer.Option(STAGE5AY_EXECUTION_GATES_PATH),
    dwh_context: Path = typer.Option(STAGE5AY_DWH_PREFLIGHT_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5AY_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AY_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AY_SUMMARY_PATH),
) -> None:
    _guardrail, next_stage, summary = build_stage5ay_summary(
        source_inputs=source_inputs,
        policy=policy,
        branch_eligibility=branch_eligibility,
        variant_family=variant_family,
        null_control_family=null_control_family,
        alphabet_control=alphabet_control,
        reading_order=reading_order,
        page_split=page_split,
        source_control=source_control,
        branch_budget=branch_budget,
        result_schema_preview=result_schema_preview,
        execution_gates=execution_gates,
        dwh_context=dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
    )
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"manifest_family_count={summary['manifest_family_count']}")
    console.print(f"token_experiments_executed={str(summary['token_experiments_executed']).lower()}")


@app.command("validate-stage5ay")
def validate_stage5ay_command(
    source_inputs: Path = typer.Option(STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH),
    policy: Path = typer.Option(STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH),
    branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    null_control_family: Path = typer.Option(STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH),
    alphabet_control: Path = typer.Option(STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH),
    reading_order: Path = typer.Option(STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH),
    page_split: Path = typer.Option(STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH),
    source_control: Path = typer.Option(STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH),
    branch_budget: Path = typer.Option(STAGE5AY_BRANCH_COUNT_BUDGET_PATH),
    result_schema_preview: Path = typer.Option(STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH),
    execution_gates: Path = typer.Option(STAGE5AY_EXECUTION_GATES_PATH),
    dwh_context: Path = typer.Option(STAGE5AY_DWH_PREFLIGHT_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AY_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AY_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AY_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AY_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5ay(
        source_inputs=source_inputs,
        policy=policy,
        branch_eligibility=branch_eligibility,
        variant_family=variant_family,
        null_control_family=null_control_family,
        alphabet_control=alphabet_control,
        reading_order=reading_order,
        page_split=page_split,
        source_control=source_control,
        branch_budget=branch_budget,
        result_schema_preview=result_schema_preview,
        execution_gates=execution_gates,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ay_valid=true")


@app.command("audit-stage5az-preflight-manifests")
def audit_stage5az_preflight_manifests_command(
    stage5ay_summary: Path = typer.Option(STAGE5AY_SUMMARY_PATH),
    stage5ay_source_inputs: Path = typer.Option(STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH),
    stage5ay_policy: Path = typer.Option(STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH),
    stage5ay_variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    stage5ay_null_control_family: Path = typer.Option(STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH),
    stage5ay_alphabet_control: Path = typer.Option(STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH),
    stage5ay_reading_order: Path = typer.Option(STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH),
    stage5ay_page_split: Path = typer.Option(STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH),
    stage5ay_source_control: Path = typer.Option(STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH),
    stage5ay_branch_budget: Path = typer.Option(STAGE5AY_BRANCH_COUNT_BUDGET_PATH),
    stage5ay_result_schema_preview: Path = typer.Option(STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH),
    stage5ay_execution_gates: Path = typer.Option(STAGE5AY_EXECUTION_GATES_PATH),
    stage5ay_dwh_context: Path = typer.Option(STAGE5AY_DWH_PREFLIGHT_CONTEXT_PATH),
    stage5ay_guardrail: Path = typer.Option(STAGE5AY_GUARDRAIL_PATH),
    stage5aw_branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
    results_dir: Path = typer.Option(STAGE5AZ_RESULTS_DIR),
    out_integrity_audit: Path = typer.Option(STAGE5AZ_PREFLIGHT_MANIFEST_INTEGRITY_AUDIT_PATH),
    out_family_id_audit: Path = typer.Option(STAGE5AZ_FAMILY_ID_UNIQUENESS_AUDIT_PATH),
    out_reference_audit: Path = typer.Option(STAGE5AZ_MANIFEST_REFERENCE_AUDIT_PATH),
    out_taxonomy_policy: Path = typer.Option(STAGE5AZ_FAMILY_TAXONOMY_MEMBERSHIP_POLICY_PATH),
) -> None:
    integrity, family_audit, reference, taxonomy = audit_stage5az_preflight_manifests(
        stage5ay_summary=stage5ay_summary,
        stage5ay_source_inputs=stage5ay_source_inputs,
        stage5ay_policy=stage5ay_policy,
        stage5ay_variant_family=stage5ay_variant_family,
        stage5ay_null_control_family=stage5ay_null_control_family,
        stage5ay_alphabet_control=stage5ay_alphabet_control,
        stage5ay_reading_order=stage5ay_reading_order,
        stage5ay_page_split=stage5ay_page_split,
        stage5ay_source_control=stage5ay_source_control,
        stage5ay_branch_budget=stage5ay_branch_budget,
        stage5ay_result_schema_preview=stage5ay_result_schema_preview,
        stage5ay_execution_gates=stage5ay_execution_gates,
        stage5ay_dwh_context=stage5ay_dwh_context,
        stage5ay_guardrail=stage5ay_guardrail,
        stage5aw_branch_manifest=stage5aw_branch_manifest,
        results_dir=results_dir,
        out_integrity_audit=out_integrity_audit,
        out_family_id_audit=out_family_id_audit,
        out_reference_audit=out_reference_audit,
        out_taxonomy_policy=out_taxonomy_policy,
    )
    console.print(f"manifest_count_checked={integrity['manifest_count_checked']}")
    console.print(
        f"duplicate_family_id_count_before_repair={family_audit['duplicate_family_id_count_before_repair']}"
    )
    console.print(f"known_duplicate_family_id_found={family_audit['known_duplicate_family_id_found']}")
    console.print(f"stage5aw_repaired_branch_manifest_used={reference['stage5aw_repaired_branch_manifest_used']}")
    console.print(f"taxonomy_multi_membership_family_count={len(taxonomy['multi_membership_family_ids'])}")


@app.command("repair-stage5az-variant-family-manifest")
def repair_stage5az_variant_family_manifest_command(
    stage5ay_policy: Path = typer.Option(STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH),
    stage5ay_variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    stage5ay_branch_budget: Path = typer.Option(STAGE5AY_BRANCH_COUNT_BUDGET_PATH),
    stage5ay_execution_gates: Path = typer.Option(STAGE5AY_EXECUTION_GATES_PATH),
    taxonomy_policy: Path = typer.Option(STAGE5AZ_FAMILY_TAXONOMY_MEMBERSHIP_POLICY_PATH),
    family_id_audit: Path = typer.Option(STAGE5AZ_FAMILY_ID_UNIQUENESS_AUDIT_PATH),
    results_dir: Path = typer.Option(STAGE5AZ_RESULTS_DIR),
    out_repaired_policy: Path = typer.Option(STAGE5AZ_REPAIRED_PREFLIGHT_DESIGN_POLICY_PATH),
    out_repaired_variant_family: Path = typer.Option(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    out_repaired_branch_budget: Path = typer.Option(STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH),
    out_repaired_execution_gates: Path = typer.Option(STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH),
) -> None:
    _policy, variant, budget, gates = repair_stage5az_variant_family_manifest(
        stage5ay_policy=stage5ay_policy,
        stage5ay_variant_family=stage5ay_variant_family,
        stage5ay_branch_budget=stage5ay_branch_budget,
        stage5ay_execution_gates=stage5ay_execution_gates,
        taxonomy_policy=taxonomy_policy,
        family_id_audit=family_id_audit,
        results_dir=results_dir,
        out_repaired_policy=out_repaired_policy,
        out_repaired_variant_family=out_repaired_variant_family,
        out_repaired_branch_budget=out_repaired_branch_budget,
        out_repaired_execution_gates=out_repaired_execution_gates,
    )
    console.print(f"repaired_unique_family_count={variant['unique_family_count']}")
    console.print(f"taxonomy_membership_count={variant['taxonomy_membership_count']}")
    console.print(f"branch_budget_changed={budget['branch_budget_changed']}")
    console.print(f"execution_gate_count={len(gates['gates'])}")


@app.command("build-stage5az-readiness")
def build_stage5az_readiness_command(
    integrity_audit: Path = typer.Option(STAGE5AZ_PREFLIGHT_MANIFEST_INTEGRITY_AUDIT_PATH),
    family_id_audit: Path = typer.Option(STAGE5AZ_FAMILY_ID_UNIQUENESS_AUDIT_PATH),
    reference_audit: Path = typer.Option(STAGE5AZ_MANIFEST_REFERENCE_AUDIT_PATH),
    repaired_policy: Path = typer.Option(STAGE5AZ_REPAIRED_PREFLIGHT_DESIGN_POLICY_PATH),
    repaired_variant_family: Path = typer.Option(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    repaired_branch_budget: Path = typer.Option(STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH),
    repaired_execution_gates: Path = typer.Option(STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH),
    stage5ay_dwh_context: Path = typer.Option(STAGE5AY_DWH_PREFLIGHT_CONTEXT_PATH),
    out_readiness: Path = typer.Option(STAGE5AZ_DEEP_RESEARCH_READINESS_PATH),
    out_dwh_context: Path = typer.Option(STAGE5AZ_DWH_MANIFEST_INTEGRITY_CONTEXT_PATH),
) -> None:
    readiness, dwh = build_stage5az_readiness(
        integrity_audit=integrity_audit,
        family_id_audit=family_id_audit,
        reference_audit=reference_audit,
        repaired_policy=repaired_policy,
        repaired_variant_family=repaired_variant_family,
        repaired_branch_budget=repaired_branch_budget,
        repaired_execution_gates=repaired_execution_gates,
        stage5ay_dwh_context=stage5ay_dwh_context,
        out_readiness=out_readiness,
        out_dwh_context=out_dwh_context,
    )
    console.print(f"deep_research_readiness={readiness['deep_research_readiness']}")
    console.print(f"dwh_operational_status={dwh['dwh_operational_status']}")


@app.command("build-stage5az-summary")
def build_stage5az_summary_command(
    integrity_audit: Path = typer.Option(STAGE5AZ_PREFLIGHT_MANIFEST_INTEGRITY_AUDIT_PATH),
    family_id_audit: Path = typer.Option(STAGE5AZ_FAMILY_ID_UNIQUENESS_AUDIT_PATH),
    reference_audit: Path = typer.Option(STAGE5AZ_MANIFEST_REFERENCE_AUDIT_PATH),
    taxonomy_policy: Path = typer.Option(STAGE5AZ_FAMILY_TAXONOMY_MEMBERSHIP_POLICY_PATH),
    repaired_policy: Path = typer.Option(STAGE5AZ_REPAIRED_PREFLIGHT_DESIGN_POLICY_PATH),
    repaired_variant_family: Path = typer.Option(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    repaired_branch_budget: Path = typer.Option(STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH),
    repaired_execution_gates: Path = typer.Option(STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH),
    readiness: Path = typer.Option(STAGE5AZ_DEEP_RESEARCH_READINESS_PATH),
    dwh_context: Path = typer.Option(STAGE5AZ_DWH_MANIFEST_INTEGRITY_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5AZ_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5AZ_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5AZ_SUMMARY_PATH),
) -> None:
    guardrail, next_stage, summary = build_stage5az_summary(
        integrity_audit=integrity_audit,
        family_id_audit=family_id_audit,
        reference_audit=reference_audit,
        taxonomy_policy=taxonomy_policy,
        repaired_policy=repaired_policy,
        repaired_variant_family=repaired_variant_family,
        repaired_branch_budget=repaired_branch_budget,
        repaired_execution_gates=repaired_execution_gates,
        readiness=readiness,
        dwh_context=dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
    )
    console.print(f"stage5az_guardrail_status={guardrail['status']}")
    console.print(f"selected_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"repaired_unique_family_count={summary['repaired_unique_family_count']}")


@app.command("validate-stage5az")
def validate_stage5az_command(
    integrity_audit: Path = typer.Option(STAGE5AZ_PREFLIGHT_MANIFEST_INTEGRITY_AUDIT_PATH),
    family_id_audit: Path = typer.Option(STAGE5AZ_FAMILY_ID_UNIQUENESS_AUDIT_PATH),
    reference_audit: Path = typer.Option(STAGE5AZ_MANIFEST_REFERENCE_AUDIT_PATH),
    taxonomy_policy: Path = typer.Option(STAGE5AZ_FAMILY_TAXONOMY_MEMBERSHIP_POLICY_PATH),
    repaired_policy: Path = typer.Option(STAGE5AZ_REPAIRED_PREFLIGHT_DESIGN_POLICY_PATH),
    repaired_variant_family: Path = typer.Option(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    repaired_branch_budget: Path = typer.Option(STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH),
    repaired_execution_gates: Path = typer.Option(STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH),
    readiness: Path = typer.Option(STAGE5AZ_DEEP_RESEARCH_READINESS_PATH),
    dwh_context: Path = typer.Option(STAGE5AZ_DWH_MANIFEST_INTEGRITY_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5AZ_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5AZ_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5AZ_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5AZ_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5az(
        integrity_audit=integrity_audit,
        family_id_audit=family_id_audit,
        reference_audit=reference_audit,
        taxonomy_policy=taxonomy_policy,
        repaired_policy=repaired_policy,
        repaired_variant_family=repaired_variant_family,
        repaired_branch_budget=repaired_branch_budget,
        repaired_execution_gates=repaired_execution_gates,
        readiness=readiness,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5az_valid=true")


@app.command("build-stage5bb-active-manifest-registry")
def build_stage5bb_active_manifest_registry_command(
    stage5az_summary: Path = typer.Option(STAGE5AZ_SUMMARY_PATH),
    stage5az_readiness: Path = typer.Option(STAGE5AZ_DEEP_RESEARCH_READINESS_PATH),
    stage5aw_branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
    stage5aw_impact_summary: Path = typer.Option(STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH),
    stage5aw_unresolved: Path = typer.Option(STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH),
    stage5aw_extras: Path = typer.Option(STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH),
    stage5ay_source_inputs: Path = typer.Option(STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH),
    stage5ay_branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    stage5az_policy: Path = typer.Option(STAGE5AZ_REPAIRED_PREFLIGHT_DESIGN_POLICY_PATH),
    stage5az_variant_family: Path = typer.Option(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    stage5az_branch_budget: Path = typer.Option(STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH),
    stage5az_execution_gates: Path = typer.Option(STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH),
    stage5az_dwh_context: Path = typer.Option(STAGE5AZ_DWH_MANIFEST_INTEGRITY_CONTEXT_PATH),
    stage5ay_null_control_family: Path = typer.Option(STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH),
    stage5ay_alphabet_control: Path = typer.Option(STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH),
    stage5ay_reading_order_control: Path = typer.Option(STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH),
    stage5ay_page_split_control: Path = typer.Option(STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH),
    stage5ay_source_control: Path = typer.Option(STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH),
    stage5ay_result_schema_preview: Path = typer.Option(STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH),
    inactive_stage5av_branch_manifest: Path = typer.Option(STAGE5AV_BRANCH_MANIFEST_PATH),
    inactive_stage5ay_variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    results_dir: Path = typer.Option(STAGE5BB_RESULTS_DIR),
    out_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    out_precedence_policy: Path = typer.Option(STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH),
) -> None:
    registry, policy = build_stage5bb_active_manifest_registry(
        stage5az_summary=stage5az_summary,
        stage5az_readiness=stage5az_readiness,
        stage5aw_branch_manifest=stage5aw_branch_manifest,
        stage5aw_impact_summary=stage5aw_impact_summary,
        stage5aw_unresolved=stage5aw_unresolved,
        stage5aw_extras=stage5aw_extras,
        stage5ay_source_inputs=stage5ay_source_inputs,
        stage5ay_branch_eligibility=stage5ay_branch_eligibility,
        stage5az_policy=stage5az_policy,
        stage5az_variant_family=stage5az_variant_family,
        stage5az_branch_budget=stage5az_branch_budget,
        stage5az_execution_gates=stage5az_execution_gates,
        stage5az_dwh_context=stage5az_dwh_context,
        stage5ay_null_control_family=stage5ay_null_control_family,
        stage5ay_alphabet_control=stage5ay_alphabet_control,
        stage5ay_reading_order_control=stage5ay_reading_order_control,
        stage5ay_page_split_control=stage5ay_page_split_control,
        stage5ay_source_control=stage5ay_source_control,
        stage5ay_result_schema_preview=stage5ay_result_schema_preview,
        inactive_stage5av_branch_manifest=inactive_stage5av_branch_manifest,
        inactive_stage5ay_variant_family=inactive_stage5ay_variant_family,
        results_dir=results_dir,
        out_registry=out_registry,
        out_precedence_policy=out_precedence_policy,
    )
    console.print(f"active_manifest_role_count={registry['active_manifest_role_count']}")
    console.print(f"all_active_paths_resolve={registry['all_active_paths_resolve']}")
    console.print(f"stale_active_load_allowed={registry['stale_active_load_allowed']}")
    console.print(f"precedence_policy_status={policy['policy_status']}")


@app.command("audit-stage5bb-legacy-pointers")
def audit_stage5bb_legacy_pointers_command(
    active_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    precedence_policy: Path = typer.Option(STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH),
    stage5az_execution_gates: Path = typer.Option(STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH),
    stage5ay_variant_family: Path = typer.Option(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    stage5az_variant_family: Path = typer.Option(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    results_dir: Path = typer.Option(STAGE5BB_RESULTS_DIR),
    out: Path = typer.Option(STAGE5BB_LEGACY_POINTER_AUDIT_PATH),
) -> None:
    audit = audit_stage5bb_legacy_pointers(
        active_registry=active_registry,
        precedence_policy=precedence_policy,
        stage5az_execution_gates=stage5az_execution_gates,
        stage5ay_variant_family=stage5ay_variant_family,
        stage5az_variant_family=stage5az_variant_family,
        results_dir=results_dir,
        out=out,
    )
    console.print(f"legacy_pointer_count={audit['legacy_pointer_count']}")
    console.print(f"audit_status={audit['audit_status']}")
    console.print(f"stale_active_load_allowed={audit['stale_active_load_allowed']}")


@app.command("validate-stage5bb-manifest-references")
def validate_stage5bb_manifest_references_command(
    active_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    precedence_policy: Path = typer.Option(STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH),
    legacy_pointer_audit: Path = typer.Option(STAGE5BB_LEGACY_POINTER_AUDIT_PATH),
    results_dir: Path = typer.Option(STAGE5BB_RESULTS_DIR),
    out_reference_validation: Path = typer.Option(STAGE5BB_MANIFEST_REFERENCE_VALIDATION_PATH),
    out_branch_eligibility_validation: Path = typer.Option(STAGE5BB_BRANCH_ELIGIBILITY_REFERENCE_VALIDATION_PATH),
) -> None:
    reference, branch = validate_stage5bb_manifest_references(
        active_registry=active_registry,
        precedence_policy=precedence_policy,
        legacy_pointer_audit=legacy_pointer_audit,
        results_dir=results_dir,
        out_reference_validation=out_reference_validation,
        out_branch_eligibility_validation=out_branch_eligibility_validation,
    )
    console.print(f"all_manifest_references_resolve={reference['all_manifest_references_resolve']}")
    console.print(f"inactive_manifest_used_as_active_count={reference['inactive_manifest_used_as_active_count']}")
    console.print(f"branch_eligibility_policy_validated={branch['branch_eligibility_policy_validated']}")
    console.print(f"option_record_count={branch['option_record_count']}")


@app.command("build-stage5bb-runner-scaffold")
def build_stage5bb_runner_scaffold_command(
    active_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    reference_validation: Path = typer.Option(STAGE5BB_MANIFEST_REFERENCE_VALIDATION_PATH),
    branch_eligibility_validation: Path = typer.Option(STAGE5BB_BRANCH_ELIGIBILITY_REFERENCE_VALIDATION_PATH),
    stage5az_execution_gates: Path = typer.Option(STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH),
    results_dir: Path = typer.Option(STAGE5BB_RESULTS_DIR),
    out_loader_policy: Path = typer.Option(STAGE5BB_LOADER_SCAFFOLD_POLICY_PATH),
    out_runner_manifest: Path = typer.Option(STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH),
    out_gate_policy: Path = typer.Option(STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH),
) -> None:
    loader, runner, gate = build_stage5bb_runner_scaffold(
        active_registry=active_registry,
        reference_validation=reference_validation,
        branch_eligibility_validation=branch_eligibility_validation,
        stage5az_execution_gates=stage5az_execution_gates,
        results_dir=results_dir,
        out_loader_policy=out_loader_policy,
        out_runner_manifest=out_runner_manifest,
        out_gate_policy=out_gate_policy,
    )
    console.print(f"loader_refuses_inactive={loader['refuse_inactive_paths_as_active_inputs']}")
    console.print(f"runner_scaffold_created={runner['runner_scaffold_created']}")
    console.print(f"runner_execution_created={runner['runner_execution_created']}")
    console.print(f"gate_count={gate['gate_count']}")


@app.command("build-stage5bb-dry-run-preview")
def build_stage5bb_dry_run_preview_command(
    active_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    runner_manifest: Path = typer.Option(STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH),
    gate_policy: Path = typer.Option(STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH),
    results_dir: Path = typer.Option(STAGE5BB_RESULTS_DIR),
    out_dry_run_preview: Path = typer.Option(STAGE5BB_DRY_RUN_PLAN_PREVIEW_PATH),
    out_branch_counter: Path = typer.Option(STAGE5BB_BRANCH_COUNTER_SUMMARY_PATH),
    out_family_summary: Path = typer.Option(STAGE5BB_FAMILY_ENUMERATION_SUMMARY_PATH),
) -> None:
    preview, branch, family = build_stage5bb_dry_run_preview(
        active_registry=active_registry,
        runner_manifest=runner_manifest,
        gate_policy=gate_policy,
        results_dir=results_dir,
        out_dry_run_preview=out_dry_run_preview,
        out_branch_counter=out_branch_counter,
        out_family_summary=out_family_summary,
    )
    console.print(f"dry_run_preview_created={preview['dry_run_preview_created']}")
    console.print(f"branch_upper_bound_product={branch['branch_upper_bound_product']}")
    console.print(f"unique_variant_family_count={family['unique_variant_family_count']}")
    console.print(f"taxonomy_membership_count={family['taxonomy_membership_count']}")


@app.command("validate-stage5bb-execution-gates")
def validate_stage5bb_execution_gates_command(
    active_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    runner_manifest: Path = typer.Option(STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH),
    dry_run_preview: Path = typer.Option(STAGE5BB_DRY_RUN_PLAN_PREVIEW_PATH),
    stage5az_execution_gates: Path = typer.Option(STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH),
    gate_policy: Path = typer.Option(STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH),
    results_dir: Path = typer.Option(STAGE5BB_RESULTS_DIR),
    out_gate_validation: Path = typer.Option(STAGE5BB_EXECUTION_GATE_VALIDATION_PATH),
    out_no_execution_proof: Path = typer.Option(STAGE5BB_NO_EXECUTION_PROOF_PATH),
) -> None:
    gate, proof = validate_stage5bb_execution_gates(
        active_registry=active_registry,
        runner_manifest=runner_manifest,
        dry_run_preview=dry_run_preview,
        stage5az_execution_gates=stage5az_execution_gates,
        gate_policy=gate_policy,
        results_dir=results_dir,
        out_gate_validation=out_gate_validation,
        out_no_execution_proof=out_no_execution_proof,
    )
    console.print(f"gate_enforcer_blocks_execution={gate['gate_enforcer_blocks_execution']}")
    console.print(f"real_token_block_byte_streams_generated={proof['real_token_block_byte_streams_generated']}")
    console.print(f"hash_search_performed={proof['hash_search_performed']}")


@app.command("build-stage5bb-fixture-result-schema-records")
def build_stage5bb_fixture_result_schema_records_command(
    active_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    runner_manifest: Path = typer.Option(STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH),
    results_dir: Path = typer.Option(STAGE5BB_RESULTS_DIR),
    out_policy: Path = typer.Option(STAGE5BB_RESULT_SCHEMA_FIXTURE_POLICY_PATH),
    out_records: Path = typer.Option(STAGE5BB_FIXTURE_RESULT_SCHEMA_RECORDS_PATH),
) -> None:
    policy, records = build_stage5bb_fixture_result_schema_records(
        active_registry=active_registry,
        runner_manifest=runner_manifest,
        results_dir=results_dir,
        out_policy=out_policy,
        out_records=out_records,
    )
    console.print(f"fixture_result_schema_writer_allowed={policy['fixture_result_schema_writer_allowed']}")
    console.print(f"fixture_record_count={records['fixture_record_count']}")
    console.print(f"fixture_data_not_derived_from_liber_primus={policy['fixture_data_not_derived_from_liber_primus']}")


@app.command("build-stage5bb-summary")
def build_stage5bb_summary_command(
    active_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    precedence_policy: Path = typer.Option(STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH),
    legacy_pointer_audit: Path = typer.Option(STAGE5BB_LEGACY_POINTER_AUDIT_PATH),
    reference_validation: Path = typer.Option(STAGE5BB_MANIFEST_REFERENCE_VALIDATION_PATH),
    branch_eligibility_validation: Path = typer.Option(STAGE5BB_BRANCH_ELIGIBILITY_REFERENCE_VALIDATION_PATH),
    loader_policy: Path = typer.Option(STAGE5BB_LOADER_SCAFFOLD_POLICY_PATH),
    runner_manifest: Path = typer.Option(STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH),
    dry_run_preview: Path = typer.Option(STAGE5BB_DRY_RUN_PLAN_PREVIEW_PATH),
    branch_counter: Path = typer.Option(STAGE5BB_BRANCH_COUNTER_SUMMARY_PATH),
    family_summary: Path = typer.Option(STAGE5BB_FAMILY_ENUMERATION_SUMMARY_PATH),
    gate_policy: Path = typer.Option(STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH),
    gate_validation: Path = typer.Option(STAGE5BB_EXECUTION_GATE_VALIDATION_PATH),
    fixture_policy: Path = typer.Option(STAGE5BB_RESULT_SCHEMA_FIXTURE_POLICY_PATH),
    fixture_records: Path = typer.Option(STAGE5BB_FIXTURE_RESULT_SCHEMA_RECORDS_PATH),
    no_execution_proof: Path = typer.Option(STAGE5BB_NO_EXECUTION_PROOF_PATH),
    out_validation_evidence: Path = typer.Option(STAGE5BB_VALIDATION_EVIDENCE_INDEX_PATH),
    out_dwh_context: Path = typer.Option(STAGE5BB_DWH_RUNNER_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5BB_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5BB_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5BB_SUMMARY_PATH),
) -> None:
    evidence, dwh, _guardrail, summary = build_stage5bb_summary(
        active_registry=active_registry,
        precedence_policy=precedence_policy,
        legacy_pointer_audit=legacy_pointer_audit,
        reference_validation=reference_validation,
        branch_eligibility_validation=branch_eligibility_validation,
        loader_policy=loader_policy,
        runner_manifest=runner_manifest,
        dry_run_preview=dry_run_preview,
        branch_counter=branch_counter,
        family_summary=family_summary,
        gate_policy=gate_policy,
        gate_validation=gate_validation,
        fixture_policy=fixture_policy,
        fixture_records=fixture_records,
        no_execution_proof=no_execution_proof,
        out_validation_evidence=out_validation_evidence,
        out_dwh_context=out_dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
    )
    console.print(f"validation_evidence_index_created={evidence['validation_evidence_index_created']}")
    console.print(f"dwh_operational_status={dwh['dwh_operational_status']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")


@app.command("validate-stage5bb")
def validate_stage5bb_command(
    active_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    precedence_policy: Path = typer.Option(STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH),
    legacy_pointer_audit: Path = typer.Option(STAGE5BB_LEGACY_POINTER_AUDIT_PATH),
    reference_validation: Path = typer.Option(STAGE5BB_MANIFEST_REFERENCE_VALIDATION_PATH),
    branch_eligibility_validation: Path = typer.Option(STAGE5BB_BRANCH_ELIGIBILITY_REFERENCE_VALIDATION_PATH),
    loader_policy: Path = typer.Option(STAGE5BB_LOADER_SCAFFOLD_POLICY_PATH),
    runner_manifest: Path = typer.Option(STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH),
    dry_run_preview: Path = typer.Option(STAGE5BB_DRY_RUN_PLAN_PREVIEW_PATH),
    branch_counter: Path = typer.Option(STAGE5BB_BRANCH_COUNTER_SUMMARY_PATH),
    family_summary: Path = typer.Option(STAGE5BB_FAMILY_ENUMERATION_SUMMARY_PATH),
    gate_policy: Path = typer.Option(STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH),
    gate_validation: Path = typer.Option(STAGE5BB_EXECUTION_GATE_VALIDATION_PATH),
    fixture_policy: Path = typer.Option(STAGE5BB_RESULT_SCHEMA_FIXTURE_POLICY_PATH),
    fixture_records: Path = typer.Option(STAGE5BB_FIXTURE_RESULT_SCHEMA_RECORDS_PATH),
    validation_evidence: Path = typer.Option(STAGE5BB_VALIDATION_EVIDENCE_INDEX_PATH),
    no_execution_proof: Path = typer.Option(STAGE5BB_NO_EXECUTION_PROOF_PATH),
    dwh_context: Path = typer.Option(STAGE5BB_DWH_RUNNER_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5BB_GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(STAGE5BB_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5BB_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5BB_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5bb(
        active_registry=active_registry,
        precedence_policy=precedence_policy,
        legacy_pointer_audit=legacy_pointer_audit,
        reference_validation=reference_validation,
        branch_eligibility_validation=branch_eligibility_validation,
        loader_policy=loader_policy,
        runner_manifest=runner_manifest,
        dry_run_preview=dry_run_preview,
        branch_counter=branch_counter,
        family_summary=family_summary,
        gate_policy=gate_policy,
        gate_validation=gate_validation,
        fixture_policy=fixture_policy,
        fixture_records=fixture_records,
        validation_evidence=validation_evidence,
        no_execution_proof=no_execution_proof,
        dwh_context=dwh_context,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5bb_valid=true")


@app.command("build-stage5bd-dry-run-policy")
def build_stage5bd_dry_run_policy_command(
    stage5bb_summary: Path = typer.Option(STAGE5BB_SUMMARY_PATH),
    stage5bc_review_note: str = typer.Option("Stage 5BC approved no-execution dry-run implementation"),
    stage5bb_active_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    stage5bb_precedence_policy: Path = typer.Option(STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH),
    stage5bb_no_execution_proof: Path = typer.Option(STAGE5BB_NO_EXECUTION_PROOF_PATH),
    stage5bb_guardrail: Path = typer.Option(STAGE5BB_GUARDRAIL_PATH),
    results_dir: Path = typer.Option(STAGE5BD_RESULTS_DIR),
    out_policy: Path = typer.Option(STAGE5BD_DRY_RUN_POLICY_PATH),
    out_active_lock: Path = typer.Option(STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH),
) -> None:
    policy, lock = build_stage5bd_dry_run_policy(
        stage5bb_summary=stage5bb_summary,
        stage5bc_review_note=stage5bc_review_note,
        stage5bb_active_registry=stage5bb_active_registry,
        stage5bb_precedence_policy=stage5bb_precedence_policy,
        stage5bb_no_execution_proof=stage5bb_no_execution_proof,
        stage5bb_guardrail=stage5bb_guardrail,
        results_dir=results_dir,
        out_policy=out_policy,
        out_active_lock=out_active_lock,
    )
    console.print(f"dry_run_policy_status={policy['status']}")
    console.print(f"active_branch_manifest={lock['active_branch_manifest']}")
    console.print(f"real_execution_authorised={policy['real_execution_authorised']}")


@app.command("build-stage5bd-active-manifest-lock")
def build_stage5bd_active_manifest_lock_command(
    stage5bb_summary: Path = typer.Option(STAGE5BB_SUMMARY_PATH),
    stage5bb_active_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    stage5bb_precedence_policy: Path = typer.Option(STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH),
    stage5bb_no_execution_proof: Path = typer.Option(STAGE5BB_NO_EXECUTION_PROOF_PATH),
    stage5bb_guardrail: Path = typer.Option(STAGE5BB_GUARDRAIL_PATH),
    results_dir: Path = typer.Option(STAGE5BD_RESULTS_DIR),
    out_policy: Path = typer.Option(STAGE5BD_DRY_RUN_POLICY_PATH),
    out_active_lock: Path = typer.Option(STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH),
) -> None:
    _policy, lock = build_stage5bd_dry_run_policy(
        stage5bb_summary=stage5bb_summary,
        stage5bb_active_registry=stage5bb_active_registry,
        stage5bb_precedence_policy=stage5bb_precedence_policy,
        stage5bb_no_execution_proof=stage5bb_no_execution_proof,
        stage5bb_guardrail=stage5bb_guardrail,
        results_dir=results_dir,
        out_policy=out_policy,
        out_active_lock=out_active_lock,
    )
    console.print(f"active_manifest_lock_status={lock['status']}")
    console.print(f"all_active_paths_resolve={lock['all_active_paths_resolve']}")


@app.command("build-stage5bd-dry-run-plan")
def build_stage5bd_dry_run_plan_command(
    dry_run_policy: Path = typer.Option(STAGE5BD_DRY_RUN_POLICY_PATH),
    active_lock: Path = typer.Option(STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH),
    active_registry: Path = typer.Option(STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH),
    variant_family: Path = typer.Option(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    branch_budget: Path = typer.Option(STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH),
    branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    execution_gates: Path = typer.Option(STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH),
    results_dir: Path = typer.Option(STAGE5BD_RESULTS_DIR),
    out_id_policy: Path = typer.Option(STAGE5BD_RUN_PLAN_ID_POLICY_PATH),
    out_plan: Path = typer.Option(STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH),
    out_id_registry: Path = typer.Option(STAGE5BD_RUN_PLAN_ID_REGISTRY_PATH),
) -> None:
    _id_policy, plan, registry = build_stage5bd_dry_run_plan(
        dry_run_policy=dry_run_policy,
        active_lock=active_lock,
        active_registry=active_registry,
        variant_family=variant_family,
        branch_budget=branch_budget,
        branch_eligibility=branch_eligibility,
        execution_gates=execution_gates,
        results_dir=results_dir,
        out_id_policy=out_id_policy,
        out_plan=out_plan,
        out_id_registry=out_id_registry,
    )
    console.print(f"dry_run_plan_created={plan['dry_run_plan_created']}")
    console.print(f"run_plan_id_count={registry['run_plan_id_count']}")
    console.print(f"real_byte_streams_generated={plan['real_byte_streams_generated']}")


@app.command("build-stage5bd-future-result-path-validation")
def build_stage5bd_future_result_path_validation_command(
    dry_run_plan: Path = typer.Option(STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH),
    active_lock: Path = typer.Option(STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH),
    results_dir: Path = typer.Option(STAGE5BD_RESULTS_DIR),
    out_policy: Path = typer.Option(STAGE5BD_FUTURE_RESULT_PATH_POLICY_PATH),
    out_validation: Path = typer.Option(STAGE5BD_FUTURE_RESULT_PATH_VALIDATION_PATH),
) -> None:
    _policy, validation = build_stage5bd_future_result_path_validation(
        dry_run_plan=dry_run_plan,
        active_lock=active_lock,
        results_dir=results_dir,
        out_policy=out_policy,
        out_validation=out_validation,
    )
    console.print(f"future_result_paths_validated={validation['future_result_paths_validated']}")
    console.print(f"future_result_paths_written={validation['future_result_paths_written']}")
    console.print(f"blocked_path_count={validation['blocked_path_count']}")


@app.command("build-stage5bd-plan-counters")
def build_stage5bd_plan_counters_command(
    dry_run_plan: Path = typer.Option(STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH),
    variant_family: Path = typer.Option(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
    null_control_family: Path = typer.Option(STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH),
    alphabet_control: Path = typer.Option(STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH),
    reading_order_control: Path = typer.Option(STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH),
    page_split_control: Path = typer.Option(STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH),
    source_control: Path = typer.Option(STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH),
    branch_budget: Path = typer.Option(STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH),
    results_dir: Path = typer.Option(STAGE5BD_RESULTS_DIR),
    out_branch_family_counters: Path = typer.Option(STAGE5BD_BRANCH_FAMILY_PLAN_COUNTERS_PATH),
    out_null_control_counters: Path = typer.Option(STAGE5BD_NULL_CONTROL_PLAN_COUNTERS_PATH),
    out_control_family_counters: Path = typer.Option(STAGE5BD_CONTROL_FAMILY_PLAN_COUNTERS_PATH),
) -> None:
    branch, null, control = build_stage5bd_plan_counters(
        dry_run_plan=dry_run_plan,
        variant_family=variant_family,
        null_control_family=null_control_family,
        alphabet_control=alphabet_control,
        reading_order_control=reading_order_control,
        page_split_control=page_split_control,
        source_control=source_control,
        branch_budget=branch_budget,
        results_dir=results_dir,
        out_branch_family_counters=out_branch_family_counters,
        out_null_control_counters=out_null_control_counters,
        out_control_family_counters=out_control_family_counters,
    )
    console.print(f"variant_family_count={branch['variant_family_count']}")
    console.print(f"null_control_family_count={null['null_control_family_count']}")
    console.print(f"dry_run_plan_family_count={control['dry_run_plan_family_count']}")


@app.command("build-stage5bd-fixture-dry-run-records")
def build_stage5bd_fixture_dry_run_records_command(
    dry_run_plan: Path = typer.Option(STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH),
    results_dir: Path = typer.Option(STAGE5BD_RESULTS_DIR),
    out_schema: Path = typer.Option(STAGE5BD_DRY_RUN_REPORT_SCHEMA_PATH),
    out_policy: Path = typer.Option(STAGE5BD_FIXTURE_RESULT_EXAMPLE_POLICY_PATH),
    out_records: Path = typer.Option(STAGE5BD_FIXTURE_DRY_RUN_RECORDS_PATH),
) -> None:
    _schema, policy, records = build_stage5bd_fixture_dry_run_records(
        dry_run_plan=dry_run_plan,
        results_dir=results_dir,
        out_schema=out_schema,
        out_policy=out_policy,
        out_records=out_records,
    )
    console.print(f"fixture_result_examples_allowed={policy['fixture_result_examples_allowed']}")
    console.print(f"fixture_record_count={records['fixture_record_count']}")
    console.print(f"real_token_block_data_used={policy['real_token_block_data_used']}")


@app.command("validate-stage5bd-execution-gates")
def validate_stage5bd_execution_gates_command(
    dry_run_policy: Path = typer.Option(STAGE5BD_DRY_RUN_POLICY_PATH),
    dry_run_plan: Path = typer.Option(STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH),
    active_lock: Path = typer.Option(STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH),
    stage5bb_gate_policy: Path = typer.Option(STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH),
    stage5bb_gate_validation: Path = typer.Option(STAGE5BB_EXECUTION_GATE_VALIDATION_PATH),
    stage5az_execution_gates: Path = typer.Option(STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH),
    results_dir: Path = typer.Option(STAGE5BD_RESULTS_DIR),
    out_validation: Path = typer.Option(STAGE5BD_EXECUTION_GATE_DRY_RUN_VALIDATION_PATH),
    out_proof: Path = typer.Option(STAGE5BD_NO_BYTE_STREAM_PROOF_PATH),
) -> None:
    validation, proof = validate_stage5bd_execution_gates(
        dry_run_policy=dry_run_policy,
        dry_run_plan=dry_run_plan,
        active_lock=active_lock,
        stage5bb_gate_policy=stage5bb_gate_policy,
        stage5bb_gate_validation=stage5bb_gate_validation,
        stage5az_execution_gates=stage5az_execution_gates,
        results_dir=results_dir,
        out_validation=out_validation,
        out_proof=out_proof,
    )
    console.print(f"gate_enforcer_blocks_execution={validation['gate_enforcer_blocks_execution']}")
    console.print(f"real_token_block_byte_streams_generated={proof['real_token_block_byte_streams_generated']}")
    console.print(f"hash_search_performed={proof['hash_search_performed']}")


@app.command("build-stage5bd-validation-evidence")
def build_stage5bd_validation_evidence_command(
    stage5bb_validation_evidence: Path = typer.Option(STAGE5BB_VALIDATION_EVIDENCE_INDEX_PATH),
    stage5bb_development_log: Path = typer.Option("docs/development-logs/2026-05-26-stage-5bb-preflight-runner-scaffold.md"),
    stage5bb_summary: Path = typer.Option(STAGE5BB_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5BD_RESULTS_DIR),
    out: Path = typer.Option(STAGE5BD_STAGE5BB_VALIDATION_EVIDENCE_CONSOLIDATION_PATH),
) -> None:
    record = build_stage5bd_validation_evidence(
        stage5bb_validation_evidence=stage5bb_validation_evidence,
        stage5bb_development_log=stage5bb_development_log,
        stage5bb_summary=stage5bb_summary,
        results_dir=results_dir,
        out=out,
    )
    console.print(f"stage5bb_validation_evidence_placeholders_found={record['stage5bb_validation_evidence_placeholders_found']}")
    console.print(f"consolidated_validation_status={record['consolidated_validation_status']}")
    console.print(f"stage5bb_historical_file_mutated={record['stage5bb_historical_file_mutated']}")


@app.command("build-stage5bd-archive-marker")
def build_stage5bd_archive_marker_command(
    dry_run_policy: Path = typer.Option(STAGE5BD_DRY_RUN_POLICY_PATH),
    dry_run_plan: Path = typer.Option(STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH),
    summary_output_path: Path = typer.Option(STAGE5BD_ARCHIVE_REVIEW_MARKER_PATH),
    policy_output_path: Path = typer.Option(STAGE5BD_ARCHIVE_MARKER_POLICY_PATH),
    results_dir: Path = typer.Option(STAGE5BD_RESULTS_DIR),
) -> None:
    policy, marker = build_stage5bd_archive_marker(
        dry_run_policy=dry_run_policy,
        dry_run_plan=dry_run_plan,
        summary_output_path=summary_output_path,
        policy_output_path=policy_output_path,
        results_dir=results_dir,
    )
    console.print(f"archive_marker_policy_status={policy['status']}")
    console.print(f"current_commit_detected={marker['current_commit_detected']}")
    console.print("archive_marker_files_created=true")


@app.command("build-stage5bd-summary")
def build_stage5bd_summary_command(
    dry_run_policy: Path = typer.Option(STAGE5BD_DRY_RUN_POLICY_PATH),
    active_lock: Path = typer.Option(STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH),
    id_policy: Path = typer.Option(STAGE5BD_RUN_PLAN_ID_POLICY_PATH),
    dry_run_plan: Path = typer.Option(STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH),
    id_registry: Path = typer.Option(STAGE5BD_RUN_PLAN_ID_REGISTRY_PATH),
    future_result_policy: Path = typer.Option(STAGE5BD_FUTURE_RESULT_PATH_POLICY_PATH),
    future_result_validation: Path = typer.Option(STAGE5BD_FUTURE_RESULT_PATH_VALIDATION_PATH),
    branch_family_counters: Path = typer.Option(STAGE5BD_BRANCH_FAMILY_PLAN_COUNTERS_PATH),
    null_control_counters: Path = typer.Option(STAGE5BD_NULL_CONTROL_PLAN_COUNTERS_PATH),
    control_family_counters: Path = typer.Option(STAGE5BD_CONTROL_FAMILY_PLAN_COUNTERS_PATH),
    dry_run_report_schema: Path = typer.Option(STAGE5BD_DRY_RUN_REPORT_SCHEMA_PATH),
    fixture_policy: Path = typer.Option(STAGE5BD_FIXTURE_RESULT_EXAMPLE_POLICY_PATH),
    fixture_records: Path = typer.Option(STAGE5BD_FIXTURE_DRY_RUN_RECORDS_PATH),
    gate_validation: Path = typer.Option(STAGE5BD_EXECUTION_GATE_DRY_RUN_VALIDATION_PATH),
    no_byte_proof: Path = typer.Option(STAGE5BD_NO_BYTE_STREAM_PROOF_PATH),
    validation_evidence: Path = typer.Option(STAGE5BD_STAGE5BB_VALIDATION_EVIDENCE_CONSOLIDATION_PATH),
    archive_marker_policy: Path = typer.Option(STAGE5BD_ARCHIVE_MARKER_POLICY_PATH),
    archive_review_marker: Path = typer.Option(STAGE5BD_ARCHIVE_REVIEW_MARKER_PATH),
    out_dwh_context: Path = typer.Option(STAGE5BD_DWH_DRY_RUN_CONTEXT_PATH),
    out_guardrail: Path = typer.Option(STAGE5BD_GUARDRAIL_PATH),
    out_next_stage: Path = typer.Option(STAGE5BD_NEXT_STAGE_DECISION_PATH),
    out_summary: Path = typer.Option(STAGE5BD_SUMMARY_PATH),
) -> None:
    dwh, _guardrail, next_stage, summary = build_stage5bd_summary(
        dry_run_policy=dry_run_policy,
        active_lock=active_lock,
        id_policy=id_policy,
        dry_run_plan=dry_run_plan,
        id_registry=id_registry,
        future_result_policy=future_result_policy,
        future_result_validation=future_result_validation,
        branch_family_counters=branch_family_counters,
        null_control_counters=null_control_counters,
        control_family_counters=control_family_counters,
        dry_run_report_schema=dry_run_report_schema,
        fixture_policy=fixture_policy,
        fixture_records=fixture_records,
        gate_validation=gate_validation,
        no_byte_proof=no_byte_proof,
        validation_evidence=validation_evidence,
        archive_marker_policy=archive_marker_policy,
        archive_review_marker=archive_review_marker,
        out_dwh_context=out_dwh_context,
        out_guardrail=out_guardrail,
        out_next_stage=out_next_stage,
        out_summary=out_summary,
    )
    console.print(f"dwh_operational_status={dwh['dwh_operational_status']}")
    console.print(f"recommended_next_stage_title={next_stage['selected_next_stage_title']}")
    console.print(f"run_plan_id_count={summary['run_plan_id_count']}")


@app.command("validate-stage5bd")
def validate_stage5bd_command(
    dry_run_policy: Path = typer.Option(STAGE5BD_DRY_RUN_POLICY_PATH),
    active_lock: Path = typer.Option(STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH),
    id_policy: Path = typer.Option(STAGE5BD_RUN_PLAN_ID_POLICY_PATH),
    dry_run_plan: Path = typer.Option(STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH),
    id_registry: Path = typer.Option(STAGE5BD_RUN_PLAN_ID_REGISTRY_PATH),
    future_result_policy: Path = typer.Option(STAGE5BD_FUTURE_RESULT_PATH_POLICY_PATH),
    future_result_validation: Path = typer.Option(STAGE5BD_FUTURE_RESULT_PATH_VALIDATION_PATH),
    branch_family_counters: Path = typer.Option(STAGE5BD_BRANCH_FAMILY_PLAN_COUNTERS_PATH),
    null_control_counters: Path = typer.Option(STAGE5BD_NULL_CONTROL_PLAN_COUNTERS_PATH),
    control_family_counters: Path = typer.Option(STAGE5BD_CONTROL_FAMILY_PLAN_COUNTERS_PATH),
    dry_run_report_schema: Path = typer.Option(STAGE5BD_DRY_RUN_REPORT_SCHEMA_PATH),
    fixture_policy: Path = typer.Option(STAGE5BD_FIXTURE_RESULT_EXAMPLE_POLICY_PATH),
    fixture_records: Path = typer.Option(STAGE5BD_FIXTURE_DRY_RUN_RECORDS_PATH),
    gate_validation: Path = typer.Option(STAGE5BD_EXECUTION_GATE_DRY_RUN_VALIDATION_PATH),
    no_byte_proof: Path = typer.Option(STAGE5BD_NO_BYTE_STREAM_PROOF_PATH),
    validation_evidence: Path = typer.Option(STAGE5BD_STAGE5BB_VALIDATION_EVIDENCE_CONSOLIDATION_PATH),
    archive_marker_policy: Path = typer.Option(STAGE5BD_ARCHIVE_MARKER_POLICY_PATH),
    dwh_context: Path = typer.Option(STAGE5BD_DWH_DRY_RUN_CONTEXT_PATH),
    guardrail: Path = typer.Option(STAGE5BD_GUARDRAIL_PATH),
    archive_review_marker: Path = typer.Option(STAGE5BD_ARCHIVE_REVIEW_MARKER_PATH),
    next_stage_decision: Path = typer.Option(STAGE5BD_NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(STAGE5BD_SUMMARY_PATH),
    results_dir: Path = typer.Option(STAGE5BD_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5bd(
        dry_run_policy=dry_run_policy,
        active_lock=active_lock,
        id_policy=id_policy,
        dry_run_plan=dry_run_plan,
        id_registry=id_registry,
        future_result_policy=future_result_policy,
        future_result_validation=future_result_validation,
        branch_family_counters=branch_family_counters,
        null_control_counters=null_control_counters,
        control_family_counters=control_family_counters,
        dry_run_report_schema=dry_run_report_schema,
        fixture_policy=fixture_policy,
        fixture_records=fixture_records,
        gate_validation=gate_validation,
        no_byte_proof=no_byte_proof,
        validation_evidence=validation_evidence,
        archive_marker_policy=archive_marker_policy,
        dwh_context=dwh_context,
        guardrail=guardrail,
        archive_review_marker=archive_review_marker,
        next_stage_decision=next_stage_decision,
        summary=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5bd_valid=true")


@app.command("build-stage5bm-string4-reconciliation")
def build_stage5bm_string4_reconciliation_command(
    results_dir: Path = typer.Option(STAGE5BM_RESULTS_DIR),
    historical_results_dir: Path = typer.Option(STAGE5BM_HISTORICAL_RESULTS_DIR),
) -> None:
    summary = build_stage5bm_string4_reconciliation(
        results_dir=results_dir,
        historical_results_dir=historical_results_dir,
    )
    console.print(f"string4_branch_membership_status={summary['string4_branch_membership_status']}")
    console.print(f"string4_canonical_match_count={summary['string4_canonical_match_count']}")
    console.print(f"string4_stage5aw_supported_noncanonical_count={summary['string4_stage5aw_supported_noncanonical_count']}")
    console.print(f"string4_unsupported_position_count={summary['string4_unsupported_position_count']}")
    console.print(f"future_token_block_execution_remains_blocked={summary['future_token_block_execution_remains_blocked']}")


@app.command("validate-stage5bm-string4-reconciliation")
def validate_stage5bm_string4_reconciliation_command(
    results_dir: Path = typer.Option(STAGE5BM_RESULTS_DIR),
    summary: Path = typer.Option(STAGE5BM_DATA_PATHS["summary"]),
) -> None:
    counts, errors = validate_stage5bm(results_dir=results_dir, summary=summary)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5bm_string4_reconciliation_valid=true")


@app.command("stage5bm-summary")
def stage5bm_summary_command(
    summary: Path = typer.Option(STAGE5BM_DATA_PATHS["summary"]),
) -> None:
    payload = stage5bm_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"string4_branch_membership_status={payload.get('string4_branch_membership_status')}")
    console.print(f"string4_canonical_match_count={payload.get('string4_canonical_match_count')}")
    console.print(f"string4_stage5aw_supported_noncanonical_count={payload.get('string4_stage5aw_supported_noncanonical_count')}")
    console.print(f"string4_unsupported_position_count={payload.get('string4_unsupported_position_count')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("validate-stage5bm")
def validate_stage5bm_command(
    results_dir: Path = typer.Option(STAGE5BM_RESULTS_DIR),
    summary: Path = typer.Option(STAGE5BM_DATA_PATHS["summary"]),
) -> None:
    counts, errors = validate_stage5bm(results_dir=results_dir, summary=summary)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5bm_valid=true")


@app.command("build-stage5bn-unsupported-position-review")
def build_stage5bn_unsupported_position_review_command(
    stage5bm_summary: Path = typer.Option(STAGE5BM_DATA_PATHS["summary"]),
    stage5bm_branch_membership: Path = typer.Option(STAGE5BM_DATA_PATHS["branch_membership"]),
    stage5bm_mismatch_analysis: Path = typer.Option(STAGE5BM_DATA_PATHS["mismatch_analysis"]),
    stage5bm_source_gap: Path = typer.Option(STAGE5BM_DATA_PATHS["gap_update"]),
    stage5bm_planning_constraint: Path = typer.Option(STAGE5BM_DATA_PATHS["planning_constraint"]),
    stage5ap_transcription: Path = typer.Option(TRANSCRIPTION_PATH),
    stage5ap_coordinates: Path = typer.Option(COORDINATE_PATH),
    stage5aw_unresolved: Path = typer.Option(STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH),
    stage5aw_extras: Path = typer.Option(STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH),
    stage5aw_parser_audit: Path = typer.Option(STAGE5AW_DECISION_PARSER_AUDIT_PATH),
    stage5aw_parser_policy: Path = typer.Option(STAGE5AW_PARSER_POLICY_PATH),
    stage5ay_branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    stage5bi_spreadsheet_lock: Path = typer.Option(Path("data/source-harvester/stage5bi-local-spreadsheet-source-lock.yaml")),
    local_spreadsheet: Path = typer.Option(Path("third_party/3N_3p_Bases_49-51.jpg.xlsx")),
    local_iddqd_v2_root: Path = typer.Option(Path("third_party/CiadaSolversIddqd_v2")),
    local_historical_archive: Path = typer.Option(Path("third_party/CicadaSolversIddqd")),
    human_review_pack_root: Path = typer.Option(Path("human-review-packs/stage5bn/string4-unsupported-position")),
    results_dir: Path = typer.Option(STAGE5BN_RESULTS_DIR),
    out_target: Path = typer.Option(STAGE5BN_DATA_PATHS["target"]),
    out_option_gap_audit: Path = typer.Option(STAGE5BN_DATA_PATHS["option_gap_audit"]),
    out_spreadsheet_audit: Path = typer.Option(STAGE5BN_DATA_PATHS["spreadsheet_audit"]),
    out_coordinate_context: Path = typer.Option(STAGE5BN_DATA_PATHS["coordinate_context"]),
    out_source_evidence: Path = typer.Option(STAGE5BN_DATA_PATHS["source_evidence"]),
    out_human_review_pack_manifest: Path = typer.Option(STAGE5BN_DATA_PATHS["human_review_pack_manifest"]),
    out_proposed_addendum: Path = typer.Option(STAGE5BN_DATA_PATHS["proposed_addendum"]),
    out_gap_closure: Path = typer.Option(STAGE5BN_DATA_PATHS["gap_closure"]),
    out_planning_constraint_update: Path = typer.Option(STAGE5BN_DATA_PATHS["planning_constraint_update"]),
    out_lineage: Path = typer.Option(STAGE5BN_DATA_PATHS["lineage"]),
) -> None:
    summary = build_stage5bn_unsupported_position_review(
        stage5bm_summary=stage5bm_summary,
        stage5bm_branch_membership=stage5bm_branch_membership,
        stage5bm_mismatch_analysis=stage5bm_mismatch_analysis,
        stage5bm_source_gap=stage5bm_source_gap,
        stage5bm_planning_constraint=stage5bm_planning_constraint,
        stage5ap_transcription=stage5ap_transcription,
        stage5ap_coordinates=stage5ap_coordinates,
        stage5aw_unresolved=stage5aw_unresolved,
        stage5aw_extras=stage5aw_extras,
        stage5aw_parser_audit=stage5aw_parser_audit,
        stage5aw_parser_policy=stage5aw_parser_policy,
        stage5ay_branch_eligibility=stage5ay_branch_eligibility,
        stage5bi_spreadsheet_lock=stage5bi_spreadsheet_lock,
        local_spreadsheet=local_spreadsheet,
        local_iddqd_v2_root=local_iddqd_v2_root,
        local_historical_archive=local_historical_archive,
        human_review_pack_root=human_review_pack_root,
        results_dir=results_dir,
        out_target=out_target,
        out_option_gap_audit=out_option_gap_audit,
        out_spreadsheet_audit=out_spreadsheet_audit,
        out_coordinate_context=out_coordinate_context,
        out_source_evidence=out_source_evidence,
        out_human_review_pack_manifest=out_human_review_pack_manifest,
        out_proposed_addendum=out_proposed_addendum,
        out_gap_closure=out_gap_closure,
        out_planning_constraint_update=out_planning_constraint_update,
        out_lineage=out_lineage,
    )
    console.print(f"target_token_index_0_based={summary['target_token_index_0_based']}")
    console.print(f"stage5aw_supports_0l={str(summary['stage5aw_supports_0l']).lower()}")
    console.print(f"spreadsheet_target_cell_identified={str(summary['spreadsheet_target_cell_identified']).lower()}")
    console.print(f"spreadsheet_supports_0l={str(summary['spreadsheet_supports_0l']).lower()}")
    console.print(f"unsupported_position_closure_status={summary['unsupported_position_closure_status']}")
    console.print(f"proposed_option_addendum_status={summary['proposed_option_addendum_status']}")
    console.print(f"human_review_required={str(summary['human_review_required']).lower()}")
    console.print(f"future_token_block_execution_remains_blocked={str(summary['future_token_block_execution_remains_blocked']).lower()}")


@app.command("stage5bn-summary")
def stage5bn_summary_command(
    target: Path = typer.Option(STAGE5BN_DATA_PATHS["target"]),
    option_gap_audit: Path = typer.Option(STAGE5BN_DATA_PATHS["option_gap_audit"]),
    spreadsheet_audit: Path = typer.Option(STAGE5BN_DATA_PATHS["spreadsheet_audit"]),
    coordinate_context: Path = typer.Option(STAGE5BN_DATA_PATHS["coordinate_context"]),
    source_evidence: Path = typer.Option(STAGE5BN_DATA_PATHS["source_evidence"]),
    human_review_pack_manifest: Path = typer.Option(STAGE5BN_DATA_PATHS["human_review_pack_manifest"]),
    proposed_addendum: Path = typer.Option(STAGE5BN_DATA_PATHS["proposed_addendum"]),
    gap_closure: Path = typer.Option(STAGE5BN_DATA_PATHS["gap_closure"]),
    planning_constraint_update: Path = typer.Option(STAGE5BN_DATA_PATHS["planning_constraint_update"]),
    lineage: Path = typer.Option(STAGE5BN_DATA_PATHS["lineage"]),
    stage5bm_gap_update: Path = typer.Option(STAGE5BM_DATA_PATHS["gap_update"]),
    results_dir: Path = typer.Option(STAGE5BN_RESULTS_DIR),
    out_gap_severity: Path = typer.Option(STAGE5BN_DATA_PATHS["gap_severity"]),
    out_dwh_quarantine: Path = typer.Option(STAGE5BN_DATA_PATHS["dwh_quarantine"]),
    out_guardrail: Path = typer.Option(STAGE5BN_DATA_PATHS["guardrail"]),
    out_codex_handoff: Path = typer.Option(STAGE5BN_DATA_PATHS["codex_handoff"]),
    out_summary: Path = typer.Option(STAGE5BN_DATA_PATHS["summary"]),
    out_next_stage: Path = typer.Option(STAGE5BN_DATA_PATHS["next_stage"]),
) -> None:
    payload = build_stage5bn_summary_records(
        target=target,
        option_gap_audit=option_gap_audit,
        spreadsheet_audit=spreadsheet_audit,
        coordinate_context=coordinate_context,
        source_evidence=source_evidence,
        human_review_pack_manifest=human_review_pack_manifest,
        proposed_addendum=proposed_addendum,
        gap_closure=gap_closure,
        planning_constraint_update=planning_constraint_update,
        lineage=lineage,
        stage5bm_gap_update=stage5bm_gap_update,
        results_dir=results_dir,
        out_gap_severity=out_gap_severity,
        out_dwh_quarantine=out_dwh_quarantine,
        out_guardrail=out_guardrail,
        out_codex_handoff=out_codex_handoff,
        out_summary=out_summary,
        out_next_stage=out_next_stage,
    )
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"target_token_index_0_based={payload.get('target_token_index_0_based')}")
    console.print(f"unsupported_position_closure_status={payload.get('unsupported_position_closure_status')}")
    console.print(f"spreadsheet_supports_0l={str(payload.get('spreadsheet_supports_0l')).lower()}")
    console.print(f"human_review_required={str(payload.get('human_review_required')).lower()}")
    console.print(f"proposed_option_addendum_status={payload.get('proposed_option_addendum_status')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("validate-stage5bn")
def validate_stage5bn_command(
    target: Path = typer.Option(STAGE5BN_DATA_PATHS["target"]),
    option_gap_audit: Path = typer.Option(STAGE5BN_DATA_PATHS["option_gap_audit"]),
    spreadsheet_audit: Path = typer.Option(STAGE5BN_DATA_PATHS["spreadsheet_audit"]),
    coordinate_context: Path = typer.Option(STAGE5BN_DATA_PATHS["coordinate_context"]),
    source_evidence: Path = typer.Option(STAGE5BN_DATA_PATHS["source_evidence"]),
    human_review_pack_manifest: Path = typer.Option(STAGE5BN_DATA_PATHS["human_review_pack_manifest"]),
    proposed_addendum: Path = typer.Option(STAGE5BN_DATA_PATHS["proposed_addendum"]),
    gap_closure: Path = typer.Option(STAGE5BN_DATA_PATHS["gap_closure"]),
    planning_constraint_update: Path = typer.Option(STAGE5BN_DATA_PATHS["planning_constraint_update"]),
    lineage: Path = typer.Option(STAGE5BN_DATA_PATHS["lineage"]),
    gap_severity: Path = typer.Option(STAGE5BN_DATA_PATHS["gap_severity"]),
    dwh_quarantine: Path = typer.Option(STAGE5BN_DATA_PATHS["dwh_quarantine"]),
    guardrail: Path = typer.Option(STAGE5BN_DATA_PATHS["guardrail"]),
    codex_handoff: Path = typer.Option(STAGE5BN_DATA_PATHS["codex_handoff"]),
    summary: Path = typer.Option(STAGE5BN_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5BN_DATA_PATHS["next_stage"]),
    results_dir: Path = typer.Option(STAGE5BN_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5bn(
        target=target,
        option_gap_audit=option_gap_audit,
        spreadsheet_audit=spreadsheet_audit,
        coordinate_context=coordinate_context,
        source_evidence=source_evidence,
        human_review_pack_manifest=human_review_pack_manifest,
        proposed_addendum=proposed_addendum,
        gap_closure=gap_closure,
        planning_constraint_update=planning_constraint_update,
        lineage=lineage,
        gap_severity=gap_severity,
        dwh_quarantine=dwh_quarantine,
        guardrail=guardrail,
        codex_handoff=codex_handoff,
        summary=summary,
        next_stage_decision=next_stage_decision,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5bn_valid=true")


@app.command("show-stage5bn-summary")
def show_stage5bn_summary_command(
    summary: Path = typer.Option(STAGE5BN_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5bn_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"unsupported_position_closure_status={payload.get('unsupported_position_closure_status')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5bo-decision-template-errata")
def build_stage5bo_decision_template_errata_command(
    original_template: Path = typer.Option(STAGE5BO_ORIGINAL_TEMPLATE_PATH),
    corrected_template: Path = typer.Option(
        Path("human-review-packs/stage5au/token-case-review-v2/decision-template-corrected.yaml")
    ),
    stage5bn_summary: Path = typer.Option(STAGE5BN_DATA_PATHS["summary"]),
    stage5bn_addendum: Path = typer.Option(STAGE5BN_DATA_PATHS["proposed_addendum"]),
    stage5bm_branch_membership: Path = typer.Option(STAGE5BM_DATA_PATHS["branch_membership"]),
    stage5aw_branch_manifest: Path = typer.Option(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
    stage5ay_branch_eligibility: Path = typer.Option(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
    results_dir: Path = typer.Option(STAGE5BO_RESULTS_DIR),
    out_source_lock: Path = typer.Option(STAGE5BO_DATA_PATHS["source_lock"]),
    out_errata: Path = typer.Option(STAGE5BO_DATA_PATHS["errata"]),
    out_impact: Path = typer.Option(STAGE5BO_DATA_PATHS["impact"]),
    out_universe: Path = typer.Option(STAGE5BO_DATA_PATHS["universe"]),
    out_string4: Path = typer.Option(STAGE5BO_DATA_PATHS["string4"]),
    out_addendum_integration: Path = typer.Option(STAGE5BO_DATA_PATHS["addendum"]),
    out_gap_closure: Path = typer.Option(STAGE5BO_DATA_PATHS["gap_closure"]),
    out_planning_constraint: Path = typer.Option(STAGE5BO_DATA_PATHS["planning_constraint"]),
    out_lineage: Path = typer.Option(STAGE5BO_DATA_PATHS["lineage"]),
    out_future_impact: Path = typer.Option(STAGE5BO_DATA_PATHS["future_impact"]),
    out_source_gap_severity: Path = typer.Option(STAGE5BO_DATA_PATHS["gap_severity"]),
    out_dwh: Path = typer.Option(STAGE5BO_DATA_PATHS["dwh"]),
    out_guardrail: Path = typer.Option(STAGE5BO_DATA_PATHS["guardrail"]),
    out_handoff: Path = typer.Option(STAGE5BO_DATA_PATHS["handoff"]),
    out_summary: Path = typer.Option(STAGE5BO_DATA_PATHS["summary"]),
    out_next_stage: Path = typer.Option(STAGE5BO_DATA_PATHS["next_stage"]),
) -> None:
    payload = build_stage5bo_decision_template_errata(
        original_template=original_template,
        corrected_template=corrected_template,
        stage5bn_summary=stage5bn_summary,
        stage5bn_addendum=stage5bn_addendum,
        stage5bm_branch_membership=stage5bm_branch_membership,
        stage5aw_branch_manifest=stage5aw_branch_manifest,
        stage5ay_branch_eligibility=stage5ay_branch_eligibility,
        results_dir=results_dir,
        out_source_lock=out_source_lock,
        out_errata=out_errata,
        out_impact=out_impact,
        out_universe=out_universe,
        out_string4=out_string4,
        out_addendum_integration=out_addendum_integration,
        out_gap_closure=out_gap_closure,
        out_planning_constraint=out_planning_constraint,
        out_lineage=out_lineage,
        out_future_impact=out_future_impact,
        out_source_gap_severity=out_source_gap_severity,
        out_dwh=out_dwh,
        out_guardrail=out_guardrail,
        out_handoff=out_handoff,
        out_summary=out_summary,
        out_next_stage=out_next_stage,
    )
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"original_decision_template_found={str(payload.get('original_decision_template_found')).lower()}")
    console.print(f"corrected_decision_template_found={str(payload.get('corrected_decision_template_found')).lower()}")
    console.print(f"token_case_errata_record_count={payload.get('token_case_errata_record_count')}")
    console.print(f"case_199_operator_errata_found={str(payload.get('case_199_operator_errata_found')).lower()}")
    console.print(f"case_198_operator_errata_found={str(payload.get('case_198_operator_errata_found')).lower()}")
    console.print(
        "string4_branch_membership_status_after_errata="
        f"{payload.get('string4_branch_membership_status_after_errata')}"
    )
    console.print(
        "string4_unsupported_position_count_after_errata="
        f"{payload.get('string4_unsupported_position_count_after_errata')}"
    )
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )


@app.command("validate-stage5bo")
def validate_stage5bo_command(
    source_lock: Path = typer.Option(STAGE5BO_DATA_PATHS["source_lock"]),
    errata: Path = typer.Option(STAGE5BO_DATA_PATHS["errata"]),
    impact: Path = typer.Option(STAGE5BO_DATA_PATHS["impact"]),
    universe: Path = typer.Option(STAGE5BO_DATA_PATHS["universe"]),
    string4: Path = typer.Option(STAGE5BO_DATA_PATHS["string4"]),
    addendum: Path = typer.Option(STAGE5BO_DATA_PATHS["addendum"]),
    gap_closure: Path = typer.Option(STAGE5BO_DATA_PATHS["gap_closure"]),
    planning_constraint: Path = typer.Option(STAGE5BO_DATA_PATHS["planning_constraint"]),
    lineage: Path = typer.Option(STAGE5BO_DATA_PATHS["lineage"]),
    future_impact: Path = typer.Option(STAGE5BO_DATA_PATHS["future_impact"]),
    gap_severity: Path = typer.Option(STAGE5BO_DATA_PATHS["gap_severity"]),
    dwh: Path = typer.Option(STAGE5BO_DATA_PATHS["dwh"]),
    guardrail: Path = typer.Option(STAGE5BO_DATA_PATHS["guardrail"]),
    handoff: Path = typer.Option(STAGE5BO_DATA_PATHS["handoff"]),
    summary: Path = typer.Option(STAGE5BO_DATA_PATHS["summary"]),
    next_stage: Path = typer.Option(STAGE5BO_DATA_PATHS["next_stage"]),
    results_dir: Path = typer.Option(STAGE5BO_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5bo(
        source_lock=source_lock,
        errata=errata,
        impact=impact,
        universe=universe,
        string4=string4,
        addendum=addendum,
        gap_closure=gap_closure,
        planning_constraint=planning_constraint,
        lineage=lineage,
        future_impact=future_impact,
        gap_severity=gap_severity,
        dwh=dwh,
        guardrail=guardrail,
        handoff=handoff,
        summary=summary,
        next_stage=next_stage,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5bo_valid=true")


@app.command("stage5bo-summary")
def stage5bo_summary_command(
    summary: Path = typer.Option(STAGE5BO_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5bo_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"token_case_errata_record_count={payload.get('token_case_errata_record_count')}")
    console.print(f"case_199_operator_errata_found={str(payload.get('case_199_operator_errata_found')).lower()}")
    console.print(f"case_198_operator_errata_found={str(payload.get('case_198_operator_errata_found')).lower()}")
    console.print(
        "string4_branch_membership_status_after_errata="
        f"{payload.get('string4_branch_membership_status_after_errata')}"
    )
    console.print(
        "stage5bn_addendum_integrated_as_inactive="
        f"{str(payload.get('stage5bn_addendum_integrated_as_inactive')).lower()}"
    )
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5bq-planning-integration")
def build_stage5bq_planning_integration_command(
    stage5bo_summary: Path = typer.Option(STAGE5BQ_STAGE5BO_SUMMARY_PATH),
    stage5bo_branch_membership: Path = typer.Option(STAGE5BQ_STAGE5BO_BRANCH_MEMBERSHIP_PATH),
    stage5bo_option_universe: Path = typer.Option(STAGE5BQ_STAGE5BO_OPTION_UNIVERSE_PATH),
    stage5bo_source_gap_closure: Path = typer.Option(STAGE5BQ_STAGE5BO_SOURCE_GAP_CLOSURE_PATH),
    stage5bo_planning_constraint: Path = typer.Option(STAGE5BQ_STAGE5BO_PLANNING_CONSTRAINT_PATH),
    stage5bd_summary: Path = typer.Option(STAGE5BQ_STAGE5BD_SUMMARY_PATH),
    stage5bd_active_lock: Path = typer.Option(STAGE5BQ_STAGE5BD_ACTIVE_LOCK_PATH),
    stage5bd_dry_run_plan: Path = typer.Option(STAGE5BQ_STAGE5BD_DRY_RUN_PLAN_PATH),
    stage5bd_run_plan_registry: Path = typer.Option(STAGE5BQ_STAGE5BD_RUN_PLAN_REGISTRY_PATH),
    results_dir: Path = typer.Option(STAGE5BQ_RESULTS_DIR),
    out_findings: Path = typer.Option(STAGE5BQ_DATA_PATHS["findings"]),
    out_review_packaging_warning: Path = typer.Option(STAGE5BQ_DATA_PATHS["review_packaging_warning"]),
    out_string4_context: Path = typer.Option(STAGE5BQ_DATA_PATHS["string4_context"]),
    out_sidecar_status: Path = typer.Option(STAGE5BQ_DATA_PATHS["sidecar_status"]),
    out_dry_run_constraint: Path = typer.Option(STAGE5BQ_DATA_PATHS["dry_run_constraint"]),
    out_no_active_ingestion: Path = typer.Option(STAGE5BQ_DATA_PATHS["no_active_ingestion"]),
    out_future_requirements: Path = typer.Option(STAGE5BQ_DATA_PATHS["future_requirements"]),
    out_active_preservation: Path = typer.Option(STAGE5BQ_DATA_PATHS["active_preservation"]),
    out_stage5bd_preservation: Path = typer.Option(STAGE5BQ_DATA_PATHS["stage5bd_preservation"]),
    out_future_impact: Path = typer.Option(STAGE5BQ_DATA_PATHS["future_impact"]),
    out_source_gap: Path = typer.Option(STAGE5BQ_DATA_PATHS["source_gap"]),
    out_dwh: Path = typer.Option(STAGE5BQ_DATA_PATHS["dwh"]),
    out_guardrail: Path = typer.Option(STAGE5BQ_DATA_PATHS["guardrail"]),
    out_handoff: Path = typer.Option(STAGE5BQ_DATA_PATHS["handoff"]),
    out_summary: Path = typer.Option(STAGE5BQ_DATA_PATHS["summary"]),
    out_next_stage: Path = typer.Option(STAGE5BQ_DATA_PATHS["next_stage"]),
) -> None:
    payload = build_stage5bq_planning_integration(
        stage5bo_summary=stage5bo_summary,
        stage5bo_branch_membership=stage5bo_branch_membership,
        stage5bo_option_universe=stage5bo_option_universe,
        stage5bo_source_gap_closure=stage5bo_source_gap_closure,
        stage5bo_planning_constraint=stage5bo_planning_constraint,
        stage5bd_summary=stage5bd_summary,
        stage5bd_active_lock=stage5bd_active_lock,
        stage5bd_dry_run_plan=stage5bd_dry_run_plan,
        stage5bd_run_plan_registry=stage5bd_run_plan_registry,
        results_dir=results_dir,
        out_findings=out_findings,
        out_review_packaging_warning=out_review_packaging_warning,
        out_string4_context=out_string4_context,
        out_sidecar_status=out_sidecar_status,
        out_dry_run_constraint=out_dry_run_constraint,
        out_no_active_ingestion=out_no_active_ingestion,
        out_future_requirements=out_future_requirements,
        out_active_preservation=out_active_preservation,
        out_stage5bd_preservation=out_stage5bd_preservation,
        out_future_impact=out_future_impact,
        out_source_gap=out_source_gap,
        out_dwh=out_dwh,
        out_guardrail=out_guardrail,
        out_handoff=out_handoff,
        out_summary=out_summary,
        out_next_stage=out_next_stage,
    )
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"stage5bp_verdict={payload.get('stage5bp_verdict')}")
    console.print(
        "string4_branch_membership_status_after_errata="
        f"{payload.get('string4_branch_membership_status_after_errata')}"
    )
    console.print(f"string4_planning_context_status={payload.get('string4_planning_context_status')}")
    console.print(f"string4_active_input_allowed={str(payload.get('string4_active_input_allowed')).lower()}")
    console.print(
        "string4_dry_run_ingestion_allowed_now="
        f"{str(payload.get('string4_dry_run_ingestion_allowed_now')).lower()}"
    )
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )


@app.command("validate-stage5bq")
def validate_stage5bq_command(
    findings: Path = typer.Option(STAGE5BQ_DATA_PATHS["findings"]),
    string4_context: Path = typer.Option(STAGE5BQ_DATA_PATHS["string4_context"]),
    sidecar_status: Path = typer.Option(STAGE5BQ_DATA_PATHS["sidecar_status"]),
    dry_run_constraint: Path = typer.Option(STAGE5BQ_DATA_PATHS["dry_run_constraint"]),
    no_active_ingestion: Path = typer.Option(STAGE5BQ_DATA_PATHS["no_active_ingestion"]),
    future_requirements: Path = typer.Option(STAGE5BQ_DATA_PATHS["future_requirements"]),
    active_preservation: Path = typer.Option(STAGE5BQ_DATA_PATHS["active_preservation"]),
    stage5bd_preservation: Path = typer.Option(STAGE5BQ_DATA_PATHS["stage5bd_preservation"]),
    future_impact: Path = typer.Option(STAGE5BQ_DATA_PATHS["future_impact"]),
    source_gap: Path = typer.Option(STAGE5BQ_DATA_PATHS["source_gap"]),
    dwh: Path = typer.Option(STAGE5BQ_DATA_PATHS["dwh"]),
    guardrail: Path = typer.Option(STAGE5BQ_DATA_PATHS["guardrail"]),
    handoff: Path = typer.Option(STAGE5BQ_DATA_PATHS["handoff"]),
    summary: Path = typer.Option(STAGE5BQ_DATA_PATHS["summary"]),
    next_stage: Path = typer.Option(STAGE5BQ_DATA_PATHS["next_stage"]),
    review_packaging_warning: Path = typer.Option(STAGE5BQ_DATA_PATHS["review_packaging_warning"]),
    results_dir: Path = typer.Option(STAGE5BQ_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5bq(
        findings=findings,
        string4_context=string4_context,
        sidecar_status=sidecar_status,
        dry_run_constraint=dry_run_constraint,
        no_active_ingestion=no_active_ingestion,
        future_requirements=future_requirements,
        active_preservation=active_preservation,
        stage5bd_preservation=stage5bd_preservation,
        future_impact=future_impact,
        source_gap=source_gap,
        dwh=dwh,
        guardrail=guardrail,
        handoff=handoff,
        summary=summary,
        next_stage=next_stage,
        review_packaging_warning=review_packaging_warning,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5bq_valid=true")


@app.command("stage5bq-summary")
def stage5bq_summary_command(
    summary: Path = typer.Option(STAGE5BQ_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5bq_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5bp_verdict={payload.get('stage5bp_verdict')}")
    console.print(
        "string4_branch_membership_status_after_errata="
        f"{payload.get('string4_branch_membership_status_after_errata')}"
    )
    console.print(f"string4_planning_context_status={payload.get('string4_planning_context_status')}")
    console.print(f"string4_active_input_allowed={str(payload.get('string4_active_input_allowed')).lower()}")
    console.print(
        "string4_dry_run_ingestion_allowed_now="
        f"{str(payload.get('string4_dry_run_ingestion_allowed_now')).lower()}"
    )
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5bs-planning-ingestion-gate")
def build_stage5bs_planning_ingestion_gate_command(
    stage5bq_summary: Path = typer.Option(STAGE5BS_STAGE5BQ_SUMMARY_PATH),
    stage5bq_next_stage: Path = typer.Option(STAGE5BS_STAGE5BQ_NEXT_STAGE_PATH),
    stage5bq_context: Path = typer.Option(STAGE5BS_STAGE5BQ_CONTEXT_PATH),
    stage5bq_constraint: Path = typer.Option(STAGE5BS_STAGE5BQ_CONSTRAINT_PATH),
    stage5bq_no_active_ingestion: Path = typer.Option(STAGE5BS_STAGE5BQ_NO_ACTIVE_INGESTION_PATH),
    stage5bq_requirements: Path = typer.Option(STAGE5BS_STAGE5BQ_REQUIREMENTS_PATH),
    stage5bo_branch_membership: Path = typer.Option(STAGE5BS_STAGE5BO_BRANCH_MEMBERSHIP_PATH),
    stage5bo_option_universe: Path = typer.Option(STAGE5BS_STAGE5BO_OPTION_UNIVERSE_PATH),
    stage5bo_source_gap_closure: Path = typer.Option(STAGE5BS_STAGE5BO_SOURCE_GAP_CLOSURE_PATH),
    stage5bd_dry_run_plan: Path = typer.Option(STAGE5BS_STAGE5BD_DRY_RUN_PLAN_PATH),
    stage5bd_run_plan_registry: Path = typer.Option(STAGE5BS_STAGE5BD_RUN_PLAN_REGISTRY_PATH),
    stage5br_report: Path = typer.Option(STAGE5BS_STAGE5BR_REPORT_PATH),
    results_dir: Path = typer.Option(STAGE5BS_RESULTS_DIR),
) -> None:
    payload = build_stage5bs_planning_ingestion_gate(
        stage5bq_summary=stage5bq_summary,
        stage5bq_next_stage=stage5bq_next_stage,
        stage5bq_context=stage5bq_context,
        stage5bq_constraint=stage5bq_constraint,
        stage5bq_no_active_ingestion=stage5bq_no_active_ingestion,
        stage5bq_requirements=stage5bq_requirements,
        stage5bo_branch_membership=stage5bo_branch_membership,
        stage5bo_option_universe=stage5bo_option_universe,
        stage5bo_source_gap_closure=stage5bo_source_gap_closure,
        stage5bd_dry_run_plan=stage5bd_dry_run_plan,
        stage5bd_run_plan_registry=stage5bd_run_plan_registry,
        stage5br_report=stage5br_report,
        results_dir=results_dir,
    )
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"stage5br_verdict={payload.get('stage5br_verdict')}")
    console.print(
        "string4_branch_membership_status_after_errata="
        f"{payload.get('string4_branch_membership_status_after_errata')}"
    )
    console.print(f"string4_planning_context_status={payload.get('string4_planning_context_status')}")
    console.print(
        "string4_planning_ingestion_gate_status="
        f"{payload.get('string4_planning_ingestion_gate_status')}"
    )
    console.print(
        "string4_active_input_allowed="
        f"{str(payload.get('string4_active_input_allowed')).lower()}"
    )
    console.print(
        "string4_dry_run_ingestion_allowed_now="
        f"{str(payload.get('string4_dry_run_ingestion_allowed_now')).lower()}"
    )
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )


@app.command("validate-stage5bs")
def validate_stage5bs_command(
    summary: Path = typer.Option(STAGE5BS_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5BS_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5BS_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5BS_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5bs(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5bs_valid=true")


@app.command("stage5bs-summary")
def stage5bs_summary_command(
    summary: Path = typer.Option(STAGE5BS_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5bs_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5br_verdict={payload.get('stage5br_verdict')}")
    console.print(
        "string4_branch_membership_status_after_errata="
        f"{payload.get('string4_branch_membership_status_after_errata')}"
    )
    console.print(f"string4_planning_context_status={payload.get('string4_planning_context_status')}")
    console.print(
        "string4_planning_ingestion_gate_status="
        f"{payload.get('string4_planning_ingestion_gate_status')}"
    )
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5bu-lineage-path-repair")
def build_stage5bu_lineage_path_repair_command(
    active_preservation: Path = typer.Option(STAGE5BU_STAGE5BS_ACTIVE_PRESERVATION_PATH),
    results_dir: Path = typer.Option(STAGE5BU_RESULTS_DIR),
) -> None:
    payload = build_stage5bu_lineage_path_repair(
        active_preservation=active_preservation,
        results_dir=results_dir,
    )
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"lineage_path_repair_written={str(payload.get('lineage_path_repair_written')).lower()}")
    console.print(f"path_replacement_count={payload.get('path_replacement_count')}")
    console.print(f"lineage_path_validation_status={payload.get('lineage_path_validation_status')}")
    console.print(f"lineage_record_count={payload.get('lineage_record_count')}")


@app.command("validate-stage5bu-lineage-paths")
def validate_stage5bu_lineage_paths_command(
    lineage_erratum: Path = typer.Option(STAGE5BU_DATA_PATHS["lineage_erratum"]),
    active_repair: Path = typer.Option(STAGE5BU_DATA_PATHS["active_repair"]),
    lineage_digest: Path = typer.Option(STAGE5BU_DATA_PATHS["lineage_digest"]),
    lineage_validation: Path = typer.Option(STAGE5BU_DATA_PATHS["lineage_validation"]),
    active_preservation: Path = typer.Option(STAGE5BU_STAGE5BS_ACTIVE_PRESERVATION_PATH),
) -> None:
    counts, errors = validate_stage5bu_lineage_paths(
        lineage_erratum=lineage_erratum,
        active_repair=active_repair,
        lineage_digest=lineage_digest,
        lineage_validation=lineage_validation,
        active_preservation=active_preservation,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5bu_lineage_paths_valid=true")


@app.command("build-stage5bu-reviewability-records")
def build_stage5bu_reviewability_records_command(
    results_dir: Path = typer.Option(STAGE5BU_RESULTS_DIR),
    stage5bt_report: Path = typer.Option(STAGE5BU_STAGE5BT_REPORT_PATH),
) -> None:
    payload = build_stage5bu_reviewability_records(
        results_dir=results_dir,
        stage5bt_report=stage5bt_report,
    )
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5bt_verdict={payload.get('stage5bt_verdict')}")
    console.print(
        "lineage_path_resolution_validation_status="
        f"{payload.get('lineage_path_resolution_validation_status')}"
    )
    console.print(f"lineage_record_count={payload.get('lineage_record_count')}")
    console.print(f"source_digest_record_count={payload.get('source_digest_record_count')}")


@app.command("validate-stage5bu")
def validate_stage5bu_command(
    summary: Path = typer.Option(STAGE5BU_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5BU_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5BU_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5BU_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5bu(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5bu_valid=true")


@app.command("stage5bu-summary")
def stage5bu_summary_command(
    summary: Path = typer.Option(STAGE5BU_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5bu_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5bt_verdict={payload.get('stage5bt_verdict')}")
    console.print(
        "lineage_path_resolution_validation_status="
        f"{payload.get('lineage_path_resolution_validation_status')}"
    )
    console.print(f"stage5bs_validator_hardened={str(payload.get('stage5bs_validator_hardened')).lower()}")
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5bw")
def build_stage5bw_command(
    results_dir: Path = typer.Option(STAGE5BW_RESULTS_DIR),
) -> None:
    payload = build_stage5bw(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5bv_verdict={payload.get('stage5bv_verdict')}")
    console.print(
        "string4_sidecar_planning_ingestion_proposed="
        f"{str(payload.get('string4_sidecar_planning_ingestion_proposed')).lower()}"
    )
    console.print(
        "string4_sidecar_planning_ingestion_activated="
        f"{str(payload.get('string4_sidecar_planning_ingestion_activated')).lower()}"
    )
    console.print(
        "manifest_supersession_performed="
        f"{str(payload.get('manifest_supersession_performed')).lower()}"
    )
    console.print(f"active_lineage_record_count={payload.get('active_lineage_record_count')}")
    console.print(f"stage5bd_run_plan_id_count={payload.get('stage5bd_run_plan_id_count')}")


@app.command("validate-stage5bw")
def validate_stage5bw_command(
    summary: Path = typer.Option(STAGE5BW_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5BW_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5BW_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5BW_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5bw(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5bw_valid=true")


@app.command("stage5bw-summary")
def stage5bw_summary_command(
    summary: Path = typer.Option(STAGE5BW_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5bw_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5bv_verdict={payload.get('stage5bv_verdict')}")
    console.print(
        "string4_sidecar_planning_ingestion_proposed="
        f"{str(payload.get('string4_sidecar_planning_ingestion_proposed')).lower()}"
    )
    console.print(
        "manifest_supersession_performed="
        f"{str(payload.get('manifest_supersession_performed')).lower()}"
    )
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5by")
def build_stage5by_command(
    results_dir: Path = typer.Option(STAGE5BY_RESULTS_DIR),
) -> None:
    payload = build_stage5by(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5bx_verdict={payload.get('stage5bx_verdict')}")
    console.print(
        "stage5bw_source_digest_duplicates_reviewed="
        f"{str(payload.get('stage5bw_source_digest_duplicates_reviewed')).lower()}"
    )
    console.print(f"stage5bw_source_digest_row_count={payload.get('stage5bw_source_digest_row_count')}")
    console.print(
        "stage5bw_source_digest_unique_path_count="
        f"{payload.get('stage5bw_source_digest_unique_path_count')}"
    )
    console.print(
        "inactive_sidecar_scaffold_created="
        f"{str(payload.get('string4_inactive_sidecar_planning_manifest_scaffold_created')).lower()}"
    )
    console.print(
        "no_execution_sidecar_created="
        f"{str(payload.get('string4_no_execution_planning_ingestion_sidecar_created')).lower()}"
    )
    console.print(
        "manifest_supersession_performed="
        f"{str(payload.get('manifest_supersession_performed')).lower()}"
    )


@app.command("validate-stage5by-source-digest-uniqueness")
def validate_stage5by_source_digest_uniqueness_command() -> None:
    counts, errors = validate_stage5by_source_digest_uniqueness()
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5by_source_digest_uniqueness_valid=true")


@app.command("validate-stage5by-sidecar-gates")
def validate_stage5by_sidecar_gates_command() -> None:
    counts, errors = validate_stage5by_sidecar_gates()
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5by_sidecar_gates_valid=true")


@app.command("validate-stage5by")
def validate_stage5by_command(
    summary: Path = typer.Option(STAGE5BY_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5BY_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5BY_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5BY_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5by(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5by_valid=true")


@app.command("stage5by-summary")
def stage5by_summary_command(
    summary: Path = typer.Option(STAGE5BY_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5by_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5bx_verdict={payload.get('stage5bx_verdict')}")
    console.print(
        "stage5bw_source_digest_duplicates_reviewed="
        f"{str(payload.get('stage5bw_source_digest_duplicates_reviewed')).lower()}"
    )
    console.print(
        "record_family_equivalence_map_created="
        f"{str(payload.get('record_family_name_equivalence_map_created')).lower()}"
    )
    console.print(
        "inactive_sidecar_scaffold_created="
        f"{str(payload.get('string4_inactive_sidecar_planning_manifest_scaffold_created')).lower()}"
    )
    console.print(
        "no_execution_sidecar_created="
        f"{str(payload.get('string4_no_execution_planning_ingestion_sidecar_created')).lower()}"
    )
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5ca")
def build_stage5ca_command(
    results_dir: Path = typer.Option(STAGE5CA_RESULTS_DIR),
) -> None:
    payload = build_stage5ca(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5bz_verdict={payload.get('stage5bz_verdict')}")
    console.print(
        "future_runner_exact_citation_contract_created="
        f"{str(payload.get('future_runner_exact_citation_contract_created')).lower()}"
    )
    console.print(
        "fail_closed_trigger_contract_created="
        f"{str(payload.get('fail_closed_trigger_contract_created')).lower()}"
    )
    console.print(
        "activation_precondition_contract_created="
        f"{str(payload.get('activation_precondition_contract_created')).lower()}"
    )
    console.print(
        "manifest_supersession_preflight_contract_created="
        f"{str(payload.get('manifest_supersession_preflight_contract_created')).lower()}"
    )
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )


@app.command("validate-stage5ca-citation-contract")
def validate_stage5ca_citation_contract_command(
    citation_contract: Path = typer.Option(STAGE5CA_DATA_PATHS["citation_contract"]),
) -> None:
    counts, errors = validate_stage5ca_citation_contract(citation_contract=citation_contract)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ca_citation_contract_valid=true")


@app.command("validate-stage5ca-fail-closed-triggers")
def validate_stage5ca_fail_closed_triggers_command(
    trigger_contract: Path = typer.Option(STAGE5CA_DATA_PATHS["fail_closed_contract"]),
) -> None:
    counts, errors = validate_stage5ca_fail_closed_triggers(trigger_contract=trigger_contract)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ca_fail_closed_triggers_valid=true")


@app.command("validate-stage5ca-activation-preconditions")
def validate_stage5ca_activation_preconditions_command(
    activation_contract: Path = typer.Option(STAGE5CA_DATA_PATHS["activation_contract"]),
) -> None:
    counts, errors = validate_stage5ca_activation_preconditions(
        activation_contract=activation_contract
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ca_activation_preconditions_valid=true")


@app.command("validate-stage5ca-manifest-supersession-contract")
def validate_stage5ca_manifest_supersession_contract_command(
    supersession_contract: Path = typer.Option(STAGE5CA_DATA_PATHS["supersession_contract"]),
) -> None:
    counts, errors = validate_stage5ca_manifest_supersession_contract(
        supersession_contract=supersession_contract
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ca_manifest_supersession_contract_valid=true")


@app.command("validate-stage5ca-sidecar-gates")
def validate_stage5ca_sidecar_gates_command() -> None:
    counts, errors = validate_stage5ca_sidecar_gates()
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ca_sidecar_gates_valid=true")


@app.command("validate-stage5ca")
def validate_stage5ca_command(
    summary: Path = typer.Option(STAGE5CA_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CA_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CA_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CA_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5ca(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ca_valid=true")


@app.command("stage5ca-summary")
def stage5ca_summary_command(
    summary: Path = typer.Option(STAGE5CA_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5ca_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5bz_verdict={payload.get('stage5bz_verdict')}")
    console.print(
        "future_runner_exact_citation_contract_created="
        f"{str(payload.get('future_runner_exact_citation_contract_created')).lower()}"
    )
    console.print(
        "fail_closed_trigger_contract_created="
        f"{str(payload.get('fail_closed_trigger_contract_created')).lower()}"
    )
    console.print(
        "activation_precondition_contract_created="
        f"{str(payload.get('activation_precondition_contract_created')).lower()}"
    )
    console.print(
        "manifest_supersession_preflight_contract_created="
        f"{str(payload.get('manifest_supersession_preflight_contract_created')).lower()}"
    )
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5cc")
def build_stage5cc_command(
    results_dir: Path = typer.Option(STAGE5CC_RESULTS_DIR),
) -> None:
    payload = build_stage5cc(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cb_verdict={payload.get('stage5cb_verdict')}")
    console.print(
        "stage5ca_exact_citation_contract_preserved="
        f"{str(payload.get('stage5ca_exact_citation_contract_preserved')).lower()}"
    )
    console.print(
        "fail_closed_trigger_exact_set_hardened="
        f"{str(payload.get('fail_closed_trigger_exact_set_hardened')).lower()}"
    )
    console.print(
        "activation_precondition_exact_set_hardened="
        f"{str(payload.get('activation_precondition_exact_set_hardened')).lower()}"
    )
    console.print(
        "active_planning_input_proposal_preflight_created="
        f"{str(payload.get('active_planning_input_proposal_preflight_created')).lower()}"
    )
    console.print(
        "no_byte_stream_transition_gate_status="
        f"{payload.get('no_byte_stream_transition_gate_status')}"
    )
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )


@app.command("validate-stage5cc-citation-contract")
def validate_stage5cc_citation_contract_command(
    citation_contract: Path = typer.Option(STAGE5CC_DATA_PATHS["citation_preservation"]),
) -> None:
    counts, errors = validate_stage5cc_citation_contract(citation_contract=citation_contract)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cc_citation_contract_valid=true")


@app.command("validate-stage5cc-fail-closed-triggers")
def validate_stage5cc_fail_closed_triggers_command(
    trigger_contract: Path = typer.Option(STAGE5CC_DATA_PATHS["fail_closed_contract"]),
) -> None:
    counts, errors = validate_stage5cc_fail_closed_triggers(trigger_contract=trigger_contract)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cc_fail_closed_triggers_valid=true")


@app.command("validate-stage5cc-activation-preconditions")
def validate_stage5cc_activation_preconditions_command(
    activation_contract: Path = typer.Option(STAGE5CC_DATA_PATHS["activation_contract"]),
) -> None:
    counts, errors = validate_stage5cc_activation_preconditions(
        activation_contract=activation_contract
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cc_activation_preconditions_valid=true")


@app.command("validate-stage5cc-active-planning-input-preflight")
def validate_stage5cc_active_planning_input_preflight_command(
    preflight: Path = typer.Option(STAGE5CC_DATA_PATHS["active_planning_preflight"]),
) -> None:
    counts, errors = validate_stage5cc_active_planning_input_preflight(preflight=preflight)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cc_active_planning_input_preflight_valid=true")


@app.command("validate-stage5cc-no-byte-stream-transition-gate")
def validate_stage5cc_no_byte_stream_transition_gate_command(
    gate: Path = typer.Option(STAGE5CC_DATA_PATHS["no_byte_stream_transition_gate"]),
) -> None:
    counts, errors = validate_stage5cc_no_byte_stream_transition_gate(gate=gate)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cc_no_byte_stream_transition_gate_valid=true")


@app.command("validate-stage5cc-no-execution-transition-gate")
def validate_stage5cc_no_execution_transition_gate_command(
    gate: Path = typer.Option(STAGE5CC_DATA_PATHS["no_execution_transition_gate"]),
) -> None:
    counts, errors = validate_stage5cc_no_execution_transition_gate(gate=gate)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cc_no_execution_transition_gate_valid=true")


@app.command("validate-stage5cc-sidecar-gates")
def validate_stage5cc_sidecar_gates_command() -> None:
    counts, errors = validate_stage5cc_sidecar_gates()
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cc_sidecar_gates_valid=true")


@app.command("validate-stage5cc")
def validate_stage5cc_command(
    summary: Path = typer.Option(STAGE5CC_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CC_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CC_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CC_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5cc(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cc_valid=true")


@app.command("stage5cc-summary")
def stage5cc_summary_command(
    summary: Path = typer.Option(STAGE5CC_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5cc_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cb_verdict={payload.get('stage5cb_verdict')}")
    console.print(
        "stage5ca_exact_citation_contract_preserved="
        f"{str(payload.get('stage5ca_exact_citation_contract_preserved')).lower()}"
    )
    console.print(
        "fail_closed_trigger_exact_set_hardened="
        f"{str(payload.get('fail_closed_trigger_exact_set_hardened')).lower()}"
    )
    console.print(
        "activation_precondition_exact_set_hardened="
        f"{str(payload.get('activation_precondition_exact_set_hardened')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(
        "no_byte_stream_transition_gate_status="
        f"{payload.get('no_byte_stream_transition_gate_status')}"
    )
    console.print(
        "no_execution_transition_gate_status="
        f"{payload.get('no_execution_transition_gate_status')}"
    )
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5ce")
def build_stage5ce_command(
    results_dir: Path = typer.Option(STAGE5CE_RESULTS_DIR),
) -> None:
    payload = build_stage5ce(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cd_verdict={payload.get('stage5cd_verdict')}")
    console.print(
        "active_planning_input_proposal_package_status="
        f"{payload.get('active_planning_input_proposal_package_status')}"
    )
    console.print(
        "approval_gate_satisfied_now="
        f"{str(payload.get('approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "no_byte_stream_transition_gate_status="
        f"{payload.get('no_byte_stream_transition_gate_status')}"
    )
    console.print(
        "no_execution_transition_gate_status="
        f"{payload.get('no_execution_transition_gate_status')}"
    )
    console.print(
        "future_token_block_execution_remains_blocked="
        f"{str(payload.get('future_token_block_execution_remains_blocked')).lower()}"
    )


@app.command("validate-stage5ce-proposal-package")
def validate_stage5ce_proposal_package_command(
    proposal_package: Path = typer.Option(STAGE5CE_DATA_PATHS["proposal_package"]),
) -> None:
    counts, errors = validate_stage5ce_proposal_package(proposal_package=proposal_package)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ce_proposal_package_valid=true")


@app.command("validate-stage5ce-approval-gate")
def validate_stage5ce_approval_gate_command(
    combined_gate: Path = typer.Option(STAGE5CE_DATA_PATHS["combined_gate"]),
) -> None:
    counts, errors = validate_stage5ce_approval_gate(combined_gate=combined_gate)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ce_approval_gate_valid=true")


@app.command("validate-stage5ce-citation-negative-tests")
def validate_stage5ce_citation_negative_tests_command(
    citation_set: Path = typer.Option(STAGE5CE_DATA_PATHS["citation_set"]),
) -> None:
    counts, errors = validate_stage5ce_citation_negative_tests(citation_set=citation_set)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ce_citation_negative_tests_valid=true")


@app.command("validate-stage5ce-no-byte-stream-transition-gate")
def validate_stage5ce_no_byte_stream_transition_gate_command(
    gate: Path = typer.Option(STAGE5CE_DATA_PATHS["no_byte_stream_transition_gate"]),
) -> None:
    counts, errors = validate_stage5ce_no_byte_stream_transition_gate(gate=gate)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ce_no_byte_stream_transition_gate_valid=true")


@app.command("validate-stage5ce-no-execution-transition-gate")
def validate_stage5ce_no_execution_transition_gate_command(
    gate: Path = typer.Option(STAGE5CE_DATA_PATHS["no_execution_transition_gate"]),
) -> None:
    counts, errors = validate_stage5ce_no_execution_transition_gate(gate=gate)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ce_no_execution_transition_gate_valid=true")


@app.command("validate-stage5ce")
def validate_stage5ce_command(
    summary: Path = typer.Option(STAGE5CE_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CE_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CE_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CE_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5ce(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ce_valid=true")


@app.command("stage5ce-summary")
def stage5ce_summary_command(
    summary: Path = typer.Option(STAGE5CE_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5ce_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cd_verdict={payload.get('stage5cd_verdict')}")
    console.print(
        "active_planning_input_proposal_package_status="
        f"{payload.get('active_planning_input_proposal_package_status')}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(
        "approval_gate_satisfied_now="
        f"{str(payload.get('approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "no_byte_stream_transition_gate_status="
        f"{payload.get('no_byte_stream_transition_gate_status')}"
    )
    console.print(
        "no_execution_transition_gate_status="
        f"{payload.get('no_execution_transition_gate_status')}"
    )
    console.print(
        "pytest_count_observed_locally="
        f"{payload.get('pytest_count_observed_locally')}"
    )
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5cg")
def build_stage5cg_command(
    results_dir: Path = typer.Option(STAGE5CG_RESULTS_DIR),
) -> None:
    payload = build_stage5cg(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cf_verdict={payload.get('stage5cf_verdict')}")
    console.print(
        "operator_approval_decision_scaffold_created="
        f"{str(payload.get('operator_approval_decision_scaffold_created')).lower()}"
    )
    console.print(
        "deep_research_acceptance_decision_scaffold_created="
        f"{str(payload.get('deep_research_acceptance_decision_scaffold_created')).lower()}"
    )
    console.print(
        "approval_gate_satisfied_now="
        f"{str(payload.get('approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")


@app.command("validate-stage5cg-operator-decision-scaffold")
def validate_stage5cg_operator_decision_scaffold_command(
    operator_decision: Path = typer.Option(STAGE5CG_DATA_PATHS["operator_decision"]),
) -> None:
    counts, errors = validate_stage5cg_operator_decision_scaffold(
        operator_decision=operator_decision
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cg_operator_decision_scaffold_valid=true")


@app.command("validate-stage5cg-deep-research-decision-scaffold")
def validate_stage5cg_deep_research_decision_scaffold_command(
    deep_research_decision: Path = typer.Option(
        STAGE5CG_DATA_PATHS["deep_research_decision"]
    ),
) -> None:
    counts, errors = validate_stage5cg_deep_research_decision_scaffold(
        deep_research_decision=deep_research_decision
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cg_deep_research_decision_scaffold_valid=true")


@app.command("validate-stage5cg-combined-approval-gate")
def validate_stage5cg_combined_approval_gate_command(
    combined_gate: Path = typer.Option(STAGE5CG_DATA_PATHS["combined_gate"]),
) -> None:
    counts, errors = validate_stage5cg_combined_approval_gate(combined_gate=combined_gate)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cg_combined_approval_gate_valid=true")


@app.command("validate-stage5cg-active-planning-input-decision-scaffold")
def validate_stage5cg_active_planning_input_decision_scaffold_command(
    active_planning_decision: Path = typer.Option(
        STAGE5CG_DATA_PATHS["active_planning_decision"]
    ),
) -> None:
    counts, errors = validate_stage5cg_active_planning_input_decision_scaffold(
        active_planning_decision=active_planning_decision
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cg_active_planning_input_decision_scaffold_valid=true")


@app.command("validate-stage5cg-stage5ce-wording-review")
def validate_stage5cg_stage5ce_wording_review_command(
    wording_review: Path = typer.Option(STAGE5CG_DATA_PATHS["wording_review"]),
) -> None:
    counts, errors = validate_stage5cg_stage5ce_wording_review(
        wording_review=wording_review
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cg_stage5ce_wording_review_valid=true")


@app.command("validate-stage5cg-no-byte-stream-transition-gate")
def validate_stage5cg_no_byte_stream_transition_gate_command(
    gate: Path = typer.Option(STAGE5CG_DATA_PATHS["no_byte_stream_transition_gate"]),
) -> None:
    counts, errors = validate_stage5cg_no_byte_stream_transition_gate(gate=gate)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cg_no_byte_stream_transition_gate_valid=true")


@app.command("validate-stage5cg-no-execution-transition-gate")
def validate_stage5cg_no_execution_transition_gate_command(
    gate: Path = typer.Option(STAGE5CG_DATA_PATHS["no_execution_transition_gate"]),
) -> None:
    counts, errors = validate_stage5cg_no_execution_transition_gate(gate=gate)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cg_no_execution_transition_gate_valid=true")


@app.command("validate-stage5cg-sidecar-gates")
def validate_stage5cg_sidecar_gates_command() -> None:
    counts, errors = validate_stage5cg_sidecar_gates()
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cg_sidecar_gates_valid=true")


@app.command("validate-stage5cg")
def validate_stage5cg_command(
    summary: Path = typer.Option(STAGE5CG_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CG_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CG_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CG_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5cg(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cg_valid=true")


@app.command("stage5cg-summary")
def stage5cg_summary_command(
    summary: Path = typer.Option(STAGE5CG_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5cg_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cf_verdict={payload.get('stage5cf_verdict')}")
    console.print(
        "operator_approval_decision_scaffold_created="
        f"{str(payload.get('operator_approval_decision_scaffold_created')).lower()}"
    )
    console.print(
        "deep_research_acceptance_decision_scaffold_created="
        f"{str(payload.get('deep_research_acceptance_decision_scaffold_created')).lower()}"
    )
    console.print(
        "approval_gate_satisfied_now="
        f"{str(payload.get('approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(
        "string4_active_input_allowed="
        f"{str(payload.get('string4_active_input_allowed')).lower()}"
    )
    console.print(
        "stage5ce_wording_blemish_disposition="
        f"{payload.get('stage5ce_wording_blemish_disposition')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5ci")
def build_stage5ci_command(
    results_dir: Path = typer.Option(STAGE5CI_RESULTS_DIR),
) -> None:
    payload = build_stage5ci(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(
        "operator_approval_record_template_hardened="
        f"{str(payload.get('operator_approval_record_template_hardened')).lower()}"
    )
    console.print(
        "deep_research_acceptance_record_template_hardened="
        f"{str(payload.get('deep_research_acceptance_record_template_hardened')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")


@app.command("validate-stage5ci-operator-approval-template")
def validate_stage5ci_operator_approval_template_command(
    operator_template: Path = typer.Option(STAGE5CI_DATA_PATHS["operator_template"]),
) -> None:
    counts, errors = validate_stage5ci_operator_approval_template(
        operator_template=operator_template
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ci_operator_approval_template_valid=true")


@app.command("validate-stage5ci-deep-research-acceptance-template")
def validate_stage5ci_deep_research_acceptance_template_command(
    deep_research_template: Path = typer.Option(STAGE5CI_DATA_PATHS["deep_research_template"]),
) -> None:
    counts, errors = validate_stage5ci_deep_research_acceptance_template(
        deep_research_template=deep_research_template
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ci_deep_research_acceptance_template_valid=true")


@app.command("validate-stage5ci-combined-approval-gate")
def validate_stage5ci_combined_approval_gate_command(
    combined_gate: Path = typer.Option(STAGE5CI_DATA_PATHS["combined_gate"]),
) -> None:
    counts, errors = validate_stage5ci_combined_approval_gate(combined_gate=combined_gate)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ci_combined_approval_gate_valid=true")


@app.command("validate-stage5ci-activation-decision-template")
def validate_stage5ci_activation_decision_template_command(
    activation_template: Path = typer.Option(STAGE5CI_DATA_PATHS["activation_template"]),
) -> None:
    counts, errors = validate_stage5ci_activation_decision_template(
        activation_template=activation_template
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ci_activation_decision_template_valid=true")


@app.command("validate-stage5ci-negative-validation-contract")
def validate_stage5ci_negative_validation_contract_command(
    negative_contract: Path = typer.Option(STAGE5CI_DATA_PATHS["negative_contract"]),
) -> None:
    counts, errors = validate_stage5ci_negative_validation_contract(
        negative_contract=negative_contract
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ci_negative_validation_contract_valid=true")


@app.command("validate-stage5ci-sidecar-gates")
def validate_stage5ci_sidecar_gates_command() -> None:
    counts, errors = validate_stage5ci_sidecar_gates()
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ci_sidecar_gates_valid=true")


@app.command("validate-stage5ci")
def validate_stage5ci_command(
    summary: Path = typer.Option(STAGE5CI_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CI_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CI_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CI_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5ci(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ci_valid=true")


@app.command("stage5ci-summary")
def stage5ci_summary_command(
    summary: Path = typer.Option(STAGE5CI_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5ci_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5ch_verdict={payload.get('stage5ch_verdict')}")
    console.print(
        "operator_approval_record_template_hardened="
        f"{str(payload.get('operator_approval_record_template_hardened')).lower()}"
    )
    console.print(
        "deep_research_acceptance_record_template_hardened="
        f"{str(payload.get('deep_research_acceptance_record_template_hardened')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(
        "stage5bd_run_plan_id_count="
        f"{payload.get('stage5bd_run_plan_id_count')}"
    )
    console.print(
        "active_lineage_record_count="
        f"{payload.get('active_lineage_record_count')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5ck")
def build_stage5ck_command(
    results_dir: Path = typer.Option(STAGE5CK_RESULTS_DIR),
) -> None:
    payload = build_stage5ck(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"fixture_pack_created={str(payload.get('fixture_pack_created')).lower()}")
    console.print(f"fixture_pack_only={str(payload.get('fixture_pack_only')).lower()}")
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )


@app.command("validate-stage5ck-operator-fixtures")
def validate_stage5ck_operator_fixtures_command(
    operator_fixtures: Path = typer.Option(STAGE5CK_DATA_PATHS["operator_fixtures"]),
) -> None:
    counts, errors = validate_stage5ck_operator_fixtures(operator_fixtures=operator_fixtures)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ck_operator_fixtures_valid=true")


@app.command("validate-stage5ck-deep-research-fixtures")
def validate_stage5ck_deep_research_fixtures_command(
    deep_research_fixtures: Path = typer.Option(STAGE5CK_DATA_PATHS["deep_research_fixtures"]),
) -> None:
    counts, errors = validate_stage5ck_deep_research_fixtures(
        deep_research_fixtures=deep_research_fixtures
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ck_deep_research_fixtures_valid=true")


@app.command("validate-stage5ck-activation-decision-fixtures")
def validate_stage5ck_activation_decision_fixtures_command(
    activation_fixtures: Path = typer.Option(STAGE5CK_DATA_PATHS["activation_fixtures"]),
) -> None:
    counts, errors = validate_stage5ck_activation_decision_fixtures(
        activation_fixtures=activation_fixtures
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ck_activation_decision_fixtures_valid=true")


@app.command("validate-stage5ck-negative-validation-matrix")
def validate_stage5ck_negative_validation_matrix_command(
    negative_matrix: Path = typer.Option(STAGE5CK_DATA_PATHS["negative_matrix"]),
) -> None:
    counts, errors = validate_stage5ck_negative_validation_matrix(negative_matrix=negative_matrix)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ck_negative_validation_matrix_valid=true")


@app.command("validate-stage5ck-review-package")
def validate_stage5ck_review_package_command(
    review_package: Path = typer.Option(STAGE5CK_DATA_PATHS["review_package"]),
) -> None:
    counts, errors = validate_stage5ck_review_package(review_package=review_package)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ck_review_package_valid=true")


@app.command("validate-stage5ck-sidecar-gates")
def validate_stage5ck_sidecar_gates_command() -> None:
    counts, errors = validate_stage5ck_sidecar_gates()
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ck_sidecar_gates_valid=true")


@app.command("validate-stage5ck")
def validate_stage5ck_command(
    summary: Path = typer.Option(STAGE5CK_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CK_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CK_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CK_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5ck(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5ck_valid=true")


@app.command("stage5ck-summary")
def stage5ck_summary_command(
    summary: Path = typer.Option(STAGE5CK_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5ck_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cj_verdict={payload.get('stage5cj_verdict')}")
    console.print(f"fixture_pack_created={str(payload.get('fixture_pack_created')).lower()}")
    console.print(f"fixture_pack_only={str(payload.get('fixture_pack_only')).lower()}")
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(
        "stage5bd_run_plan_id_count="
        f"{payload.get('stage5bd_run_plan_id_count')}"
    )
    console.print(
        "active_lineage_record_count="
        f"{payload.get('active_lineage_record_count')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5cm")
def build_stage5cm_command(
    results_dir: Path = typer.Option(STAGE5CM_RESULTS_DIR),
) -> None:
    payload = build_stage5cm(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cl_verdict={payload.get('stage5cl_verdict')}")
    console.print(
        "approval_record_readiness_boundary_created="
        f"{str(payload.get('approval_record_readiness_boundary_created')).lower()}"
    )
    console.print(
        "fixture_vs_real_record_boundary_hardened="
        f"{str(payload.get('fixture_vs_real_record_boundary_hardened')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "parallel_worker_cap_for_stage5cm_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cm_and_later')}"
    )


@app.command("validate-stage5cm-approval-readiness-boundary")
def validate_stage5cm_approval_readiness_boundary_command(
    approval_readiness_boundary: Path = typer.Option(
        STAGE5CM_DATA_PATHS["approval_readiness_boundary"]
    ),
) -> None:
    counts, errors = validate_stage5cm_approval_readiness_boundary(
        approval_readiness_boundary=approval_readiness_boundary
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cm_approval_readiness_boundary_valid=true")


@app.command("validate-stage5cm-fixture-real-boundary")
def validate_stage5cm_fixture_real_boundary_command(
    fixture_real_boundary: Path = typer.Option(STAGE5CM_DATA_PATHS["fixture_real_boundary"]),
) -> None:
    counts, errors = validate_stage5cm_fixture_real_boundary(
        fixture_real_boundary=fixture_real_boundary
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cm_fixture_real_boundary_valid=true")


@app.command("validate-stage5cm-end-to-end-readiness-boundary")
def validate_stage5cm_end_to_end_readiness_boundary_command(
    end_to_end_boundary: Path = typer.Option(STAGE5CM_DATA_PATHS["end_to_end_boundary"]),
) -> None:
    counts, errors = validate_stage5cm_end_to_end_readiness_boundary(
        end_to_end_boundary=end_to_end_boundary
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cm_end_to_end_readiness_boundary_valid=true")


@app.command("validate-stage5cm-real-approval-readiness")
def validate_stage5cm_real_approval_readiness_command(
    real_approval_readiness: Path = typer.Option(STAGE5CM_DATA_PATHS["real_approval_readiness"]),
) -> None:
    counts, errors = validate_stage5cm_real_approval_readiness(
        real_approval_readiness=real_approval_readiness
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cm_real_approval_readiness_valid=true")


@app.command("validate-stage5cm-activation-decision-gate")
def validate_stage5cm_activation_decision_gate_command(
    activation_gate: Path = typer.Option(STAGE5CM_DATA_PATHS["activation_gate"]),
) -> None:
    counts, errors = validate_stage5cm_activation_decision_gate(activation_gate=activation_gate)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cm_activation_decision_gate_valid=true")


@app.command("validate-stage5cm-credential-redaction-policy")
def validate_stage5cm_credential_redaction_policy_command(
    credential_redaction: Path = typer.Option(STAGE5CM_DATA_PATHS["credential_redaction"]),
) -> None:
    counts, errors = validate_stage5cm_credential_redaction_policy(
        credential_redaction=credential_redaction
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cm_credential_redaction_policy_valid=true")


@app.command("validate-stage5cm-sidecar-gates")
def validate_stage5cm_sidecar_gates_command() -> None:
    counts, errors = validate_stage5cm_sidecar_gates()
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cm_sidecar_gates_valid=true")


@app.command("validate-stage5cm")
def validate_stage5cm_command(
    summary: Path = typer.Option(STAGE5CM_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CM_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CM_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CM_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5cm(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5cm_valid=true")


@app.command("stage5cm-summary")
def stage5cm_summary_command(
    summary: Path = typer.Option(STAGE5CM_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5cm_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cl_verdict={payload.get('stage5cl_verdict')}")
    console.print(
        "approval_record_readiness_boundary_created="
        f"{str(payload.get('approval_record_readiness_boundary_created')).lower()}"
    )
    console.print(
        "fixture_vs_real_record_boundary_hardened="
        f"{str(payload.get('fixture_vs_real_record_boundary_hardened')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(
        "stage5bd_run_plan_id_count="
        f"{payload.get('stage5bd_run_plan_id_count')}"
    )
    console.print(
        "active_lineage_record_count="
        f"{payload.get('active_lineage_record_count')}"
    )
    console.print(
        "parallel_worker_cap_for_stage5cm_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cm_and_later')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


@app.command("build-stage5co")
def build_stage5co_command(
    results_dir: Path = typer.Option(STAGE5CO_RESULTS_DIR),
) -> None:
    payload = build_stage5co(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cn_verdict={payload.get('stage5cn_verdict')}")
    console.print(
        "real_approval_record_readiness_package_created="
        f"{str(payload.get('real_approval_record_readiness_package_created')).lower()}"
    )
    console.print(
        "activation_decision_transition_plan_created="
        f"{str(payload.get('activation_decision_transition_plan_created')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "parallel_worker_cap_for_stage5co_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5co_and_later')}"
    )


@app.command("validate-stage5co-stage5cn-findings")
def validate_stage5co_stage5cn_findings_command(
    findings: Path = typer.Option(STAGE5CO_DATA_PATHS["findings"]),
) -> None:
    counts, errors = validate_stage5co_stage5cn_findings(findings=findings)
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_stage5cn_findings_valid=true")


@app.command("validate-stage5co-approval-readiness-package")
def validate_stage5co_approval_readiness_package_command(
    readiness_package: Path = typer.Option(STAGE5CO_DATA_PATHS["readiness_package"]),
) -> None:
    counts, errors = validate_stage5co_approval_readiness_package(
        readiness_package=readiness_package
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_approval_readiness_package_valid=true")


@app.command("validate-stage5co-real-operator-readiness")
def validate_stage5co_real_operator_readiness_command(
    real_operator_readiness: Path = typer.Option(STAGE5CO_DATA_PATHS["real_operator_readiness"]),
) -> None:
    counts, errors = validate_stage5co_real_operator_readiness(
        real_operator_readiness=real_operator_readiness
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_real_operator_readiness_valid=true")


@app.command("validate-stage5co-real-deep-research-readiness")
def validate_stage5co_real_deep_research_readiness_command(
    real_deep_research_readiness: Path = typer.Option(
        STAGE5CO_DATA_PATHS["real_deep_research_readiness"]
    ),
) -> None:
    counts, errors = validate_stage5co_real_deep_research_readiness(
        real_deep_research_readiness=real_deep_research_readiness
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_real_deep_research_readiness_valid=true")


@app.command("validate-stage5co-real-combined-gate-readiness")
def validate_stage5co_real_combined_gate_readiness_command(
    real_combined_gate_readiness: Path = typer.Option(
        STAGE5CO_DATA_PATHS["real_combined_gate_readiness"]
    ),
) -> None:
    counts, errors = validate_stage5co_real_combined_gate_readiness(
        real_combined_gate_readiness=real_combined_gate_readiness
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_real_combined_gate_readiness_valid=true")


@app.command("validate-stage5co-activation-transition-plan")
def validate_stage5co_activation_transition_plan_command(
    activation_transition_plan: Path = typer.Option(
        STAGE5CO_DATA_PATHS["activation_transition_plan"]
    ),
) -> None:
    counts, errors = validate_stage5co_activation_transition_plan(
        activation_transition_plan=activation_transition_plan
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_activation_transition_plan_valid=true")


@app.command("validate-stage5co-current-missing-requirements")
def validate_stage5co_current_missing_requirements_command(
    missing_requirements: Path = typer.Option(STAGE5CO_DATA_PATHS["missing_requirements"]),
) -> None:
    counts, errors = validate_stage5co_current_missing_requirements(
        missing_requirements=missing_requirements
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_current_missing_requirements_valid=true")


@app.command("validate-stage5co-real-record-blocker")
def validate_stage5co_real_record_blocker_command(
    real_record_blocker: Path = typer.Option(STAGE5CO_DATA_PATHS["real_record_blocker"]),
) -> None:
    counts, errors = validate_stage5co_real_record_blocker(
        real_record_blocker=real_record_blocker
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_real_record_blocker_valid=true")


@app.command("validate-stage5co-stage5cm-boundary-preservation")
def validate_stage5co_stage5cm_boundary_preservation_command(
    stage5cm_boundary: Path = typer.Option(STAGE5CO_DATA_PATHS["stage5cm_boundary"]),
) -> None:
    counts, errors = validate_stage5co_stage5cm_boundary_preservation(
        stage5cm_boundary=stage5cm_boundary
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_stage5cm_boundary_preservation_valid=true")


@app.command("validate-stage5co-prior-stage-preservation")
def validate_stage5co_prior_stage_preservation_command() -> None:
    counts, errors = validate_stage5co_prior_stage_preservation()
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_prior_stage_preservation_valid=true")


@app.command("validate-stage5co-sidecar-gates")
def validate_stage5co_sidecar_gates_command() -> None:
    counts, errors = validate_stage5co_sidecar_gates()
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_sidecar_gates_valid=true")


@app.command("validate-stage5co-credential-redaction-policy")
def validate_stage5co_credential_redaction_policy_command(
    credential_redaction: Path = typer.Option(STAGE5CO_DATA_PATHS["credential_redaction"]),
) -> None:
    counts, errors = validate_stage5co_credential_redaction_policy(
        credential_redaction=credential_redaction
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_credential_redaction_policy_valid=true")


@app.command("validate-stage5co")
def validate_stage5co_command(
    summary: Path = typer.Option(STAGE5CO_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CO_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CO_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CO_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5co(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print("token_block_stage5co_valid=true")


@app.command("stage5co-summary")
def stage5co_summary_command(
    summary: Path = typer.Option(STAGE5CO_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5co_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cn_verdict={payload.get('stage5cn_verdict')}")
    console.print(
        "real_approval_record_readiness_package_created="
        f"{str(payload.get('real_approval_record_readiness_package_created')).lower()}"
    )
    console.print(
        "activation_decision_transition_plan_created="
        f"{str(payload.get('activation_decision_transition_plan_created')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(
        "stage5bd_run_plan_id_count="
        f"{payload.get('stage5bd_run_plan_id_count')}"
    )
    console.print(
        "active_lineage_record_count="
        f"{payload.get('active_lineage_record_count')}"
    )
    console.print(
        "parallel_worker_cap_for_stage5co_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5co_and_later')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


def _print_stage5cq_counts(counts: dict[str, object], errors: list[str], success_line: str) -> None:
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print(success_line)


@app.command("build-stage5cq")
def build_stage5cq_command(
    results_dir: Path = typer.Option(STAGE5CQ_RESULTS_DIR),
) -> None:
    payload = build_stage5cq(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cp_verdict={payload.get('stage5cp_verdict')}")
    console.print(
        "operator_decision_package_status="
        f"{payload.get('operator_decision_package_status')}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "parallel_worker_cap_for_stage5cq_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cq_and_later')}"
    )


@app.command("validate-stage5cq-stage5cp-findings")
def validate_stage5cq_stage5cp_findings_command(
    findings: Path = typer.Option(STAGE5CQ_DATA_PATHS["findings"]),
) -> None:
    counts, errors = validate_stage5cq_stage5cp_findings(findings=findings)
    _print_stage5cq_counts(
        counts, errors, "token_block_stage5cq_stage5cp_findings_valid=true"
    )


@app.command("validate-stage5cq-operator-decision-package")
def validate_stage5cq_operator_decision_package_command(
    operator_decision_package: Path = typer.Option(
        STAGE5CQ_DATA_PATHS["operator_decision_package"]
    ),
) -> None:
    counts, errors = validate_stage5cq_operator_decision_package(
        operator_decision_package=operator_decision_package
    )
    _print_stage5cq_counts(
        counts, errors, "token_block_stage5cq_operator_decision_package_valid=true"
    )


@app.command("validate-stage5cq-real-record-blocker")
def validate_stage5cq_real_record_blocker_command(
    real_record_blocker: Path = typer.Option(STAGE5CQ_DATA_PATHS["real_record_blocker"]),
) -> None:
    counts, errors = validate_stage5cq_real_record_blocker(real_record_blocker=real_record_blocker)
    _print_stage5cq_counts(
        counts, errors, "token_block_stage5cq_real_record_blocker_valid=true"
    )


@app.command("validate-stage5cq-combined-gate")
def validate_stage5cq_combined_gate_command(
    combined_gate: Path = typer.Option(STAGE5CQ_DATA_PATHS["combined_gate_nonsatisfaction"]),
) -> None:
    counts, errors = validate_stage5cq_combined_gate(combined_gate=combined_gate)
    _print_stage5cq_counts(counts, errors, "token_block_stage5cq_combined_gate_valid=true")


@app.command("validate-stage5cq-activation-nonauthorization")
def validate_stage5cq_activation_nonauthorization_command(
    activation: Path = typer.Option(STAGE5CQ_DATA_PATHS["activation_nonauthorization"]),
) -> None:
    counts, errors = validate_stage5cq_activation_nonauthorization(activation=activation)
    _print_stage5cq_counts(
        counts, errors, "token_block_stage5cq_activation_nonauthorization_valid=true"
    )


@app.command("validate-stage5cq-stage5co-preservation")
def validate_stage5cq_stage5co_preservation_command() -> None:
    counts, errors = validate_stage5cq_stage5co_preservation()
    _print_stage5cq_counts(
        counts, errors, "token_block_stage5cq_stage5co_preservation_valid=true"
    )


@app.command("validate-stage5cq-prior-stage-preservation")
def validate_stage5cq_prior_stage_preservation_command() -> None:
    counts, errors = validate_stage5cq_prior_stage_preservation()
    _print_stage5cq_counts(
        counts, errors, "token_block_stage5cq_prior_stage_preservation_valid=true"
    )


@app.command("validate-stage5cq-sidecar-gates")
def validate_stage5cq_sidecar_gates_command() -> None:
    counts, errors = validate_stage5cq_sidecar_gates()
    _print_stage5cq_counts(counts, errors, "token_block_stage5cq_sidecar_gates_valid=true")


@app.command("validate-stage5cq-handoff-restoration")
def validate_stage5cq_handoff_restoration_command() -> None:
    counts, errors = validate_stage5cq_handoff_restoration()
    _print_stage5cq_counts(
        counts, errors, "token_block_stage5cq_handoff_restoration_valid=true"
    )


@app.command("validate-stage5cq-credential-redaction-policy")
def validate_stage5cq_credential_redaction_policy_command(
    credential_redaction: Path = typer.Option(STAGE5CQ_DATA_PATHS["credential_redaction"]),
) -> None:
    counts, errors = validate_stage5cq_credential_redaction_policy(
        credential_redaction=credential_redaction
    )
    _print_stage5cq_counts(
        counts, errors, "token_block_stage5cq_credential_redaction_policy_valid=true"
    )


@app.command("validate-stage5cq")
def validate_stage5cq_command(
    summary: Path = typer.Option(STAGE5CQ_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CQ_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CQ_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CQ_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5cq(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    _print_stage5cq_counts(counts, errors, "token_block_stage5cq_valid=true")


@app.command("stage5cq-summary")
def stage5cq_summary_command(
    summary: Path = typer.Option(STAGE5CQ_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5cq_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cp_verdict={payload.get('stage5cp_verdict')}")
    console.print(
        "operator_decision_package_status="
        f"{payload.get('operator_decision_package_status')}"
    )
    console.print(
        "real_approval_records_created="
        f"{str(payload.get('real_approval_records_created')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(
        "stage5bd_run_plan_id_count="
        f"{payload.get('stage5bd_run_plan_id_count')}"
    )
    console.print(
        "active_lineage_record_count="
        f"{payload.get('active_lineage_record_count')}"
    )
    console.print(
        "parallel_worker_cap_for_stage5cq_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cq_and_later')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


def _print_stage5cs_counts(counts: dict[str, object], errors: list[str], success_line: str) -> None:
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print(success_line)


@app.command("build-stage5cs")
def build_stage5cs_command(
    results_dir: Path = typer.Option(STAGE5CS_RESULTS_DIR),
) -> None:
    payload = build_stage5cs(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cr_verdict={payload.get('stage5cr_verdict')}")
    console.print(
        "operator_decision_readiness_package_status="
        f"{payload.get('operator_decision_readiness_package_status')}"
    )
    console.print(
        "real_approval_decision_options_status="
        f"{payload.get('real_approval_decision_options_status')}"
    )
    console.print(f"operator_decision_option_count={payload.get('operator_decision_option_count')}")
    console.print(
        "operator_decision_option_selected_now="
        f"{str(payload.get('operator_decision_option_selected_now')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "parallel_worker_cap_for_stage5cs_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cs_and_later')}"
    )


@app.command("validate-stage5cs-stage5cr-findings")
def validate_stage5cs_stage5cr_findings_command(
    findings: Path = typer.Option(STAGE5CS_DATA_PATHS["findings"]),
) -> None:
    counts, errors = validate_stage5cs_stage5cr_findings(findings=findings)
    _print_stage5cs_counts(counts, errors, "token_block_stage5cs_stage5cr_findings_valid=true")


@app.command("validate-stage5cs-operator-decision-readiness")
def validate_stage5cs_operator_decision_readiness_command(
    operator_decision_readiness: Path = typer.Option(
        STAGE5CS_DATA_PATHS["operator_decision_readiness"]
    ),
) -> None:
    counts, errors = validate_stage5cs_operator_decision_readiness(
        operator_decision_readiness=operator_decision_readiness
    )
    _print_stage5cs_counts(
        counts, errors, "token_block_stage5cs_operator_decision_readiness_valid=true"
    )


@app.command("validate-stage5cs-decision-options")
def validate_stage5cs_decision_options_command(
    decision_options: Path = typer.Option(STAGE5CS_DATA_PATHS["decision_options"]),
) -> None:
    counts, errors = validate_stage5cs_decision_options(decision_options=decision_options)
    _print_stage5cs_counts(counts, errors, "token_block_stage5cs_decision_options_valid=true")


@app.command("validate-stage5cs-options-nonselection")
def validate_stage5cs_options_nonselection_command(
    options_nonselection: Path = typer.Option(STAGE5CS_DATA_PATHS["options_nonselection"]),
) -> None:
    counts, errors = validate_stage5cs_options_nonselection(
        options_nonselection=options_nonselection
    )
    _print_stage5cs_counts(
        counts, errors, "token_block_stage5cs_options_nonselection_valid=true"
    )


@app.command("validate-stage5cs-real-record-blocker")
def validate_stage5cs_real_record_blocker_command(
    real_record_blocker: Path = typer.Option(STAGE5CS_DATA_PATHS["real_record_blocker"]),
) -> None:
    counts, errors = validate_stage5cs_real_record_blocker(real_record_blocker=real_record_blocker)
    _print_stage5cs_counts(counts, errors, "token_block_stage5cs_real_record_blocker_valid=true")


@app.command("validate-stage5cs-combined-gate")
def validate_stage5cs_combined_gate_command(
    combined_gate: Path = typer.Option(STAGE5CS_DATA_PATHS["combined_gate_nonsatisfaction"]),
) -> None:
    counts, errors = validate_stage5cs_combined_gate(combined_gate=combined_gate)
    _print_stage5cs_counts(counts, errors, "token_block_stage5cs_combined_gate_valid=true")


@app.command("validate-stage5cs-activation-nonauthorization")
def validate_stage5cs_activation_nonauthorization_command(
    activation: Path = typer.Option(STAGE5CS_DATA_PATHS["activation_nonauthorization"]),
) -> None:
    counts, errors = validate_stage5cs_activation_nonauthorization(activation=activation)
    _print_stage5cs_counts(
        counts, errors, "token_block_stage5cs_activation_nonauthorization_valid=true"
    )


@app.command("validate-stage5cs-stage5cq-preservation")
def validate_stage5cs_stage5cq_preservation_command() -> None:
    counts, errors = validate_stage5cs_stage5cq_preservation()
    _print_stage5cs_counts(counts, errors, "token_block_stage5cs_stage5cq_preservation_valid=true")


@app.command("validate-stage5cs-stage5co-preservation")
def validate_stage5cs_stage5co_preservation_command() -> None:
    counts, errors = validate_stage5cs_stage5co_preservation()
    _print_stage5cs_counts(counts, errors, "token_block_stage5cs_stage5co_preservation_valid=true")


@app.command("validate-stage5cs-prior-stage-preservation")
def validate_stage5cs_prior_stage_preservation_command() -> None:
    counts, errors = validate_stage5cs_prior_stage_preservation()
    _print_stage5cs_counts(
        counts, errors, "token_block_stage5cs_prior_stage_preservation_valid=true"
    )


@app.command("validate-stage5cs-sidecar-gates")
def validate_stage5cs_sidecar_gates_command() -> None:
    counts, errors = validate_stage5cs_sidecar_gates()
    _print_stage5cs_counts(counts, errors, "token_block_stage5cs_sidecar_gates_valid=true")


@app.command("validate-stage5cs-handoff-continuity")
def validate_stage5cs_handoff_continuity_command() -> None:
    counts, errors = validate_stage5cs_handoff_continuity()
    _print_stage5cs_counts(counts, errors, "token_block_stage5cs_handoff_continuity_valid=true")


@app.command("validate-stage5cs-credential-redaction-policy")
def validate_stage5cs_credential_redaction_policy_command(
    credential_redaction: Path = typer.Option(STAGE5CS_DATA_PATHS["credential_redaction"]),
) -> None:
    counts, errors = validate_stage5cs_credential_redaction_policy(
        credential_redaction=credential_redaction
    )
    _print_stage5cs_counts(
        counts, errors, "token_block_stage5cs_credential_redaction_policy_valid=true"
    )


@app.command("validate-stage5cs")
def validate_stage5cs_command(
    summary: Path = typer.Option(STAGE5CS_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CS_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CS_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CS_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5cs(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    _print_stage5cs_counts(counts, errors, "token_block_stage5cs_valid=true")


@app.command("stage5cs-summary")
def stage5cs_summary_command(
    summary: Path = typer.Option(STAGE5CS_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5cs_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cr_verdict={payload.get('stage5cr_verdict')}")
    console.print(
        "operator_decision_readiness_package_status="
        f"{payload.get('operator_decision_readiness_package_status')}"
    )
    console.print(
        "real_approval_decision_options_status="
        f"{payload.get('real_approval_decision_options_status')}"
    )
    console.print(f"operator_decision_option_count={payload.get('operator_decision_option_count')}")
    console.print(
        "operator_decision_option_selected_now="
        f"{str(payload.get('operator_decision_option_selected_now')).lower()}"
    )
    console.print(
        "real_approval_records_created="
        f"{str(payload.get('real_approval_records_created')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(f"stage5bd_run_plan_id_count={payload.get('stage5bd_run_plan_id_count')}")
    console.print(f"active_lineage_record_count={payload.get('active_lineage_record_count')}")
    console.print(
        "parallel_worker_cap_for_stage5cs_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cs_and_later')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")
    console.print(f"recommended_next_prompt_type={payload.get('recommended_next_prompt_type')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


def _print_stage5cu_counts(counts: dict[str, object], errors: list[str], success_line: str) -> None:
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"ERROR {error}")
    if errors:
        raise typer.Exit(1)
    console.print(success_line)


@app.command("build-stage5cu")
def build_stage5cu_command(
    results_dir: Path = typer.Option(STAGE5CU_RESULTS_DIR),
) -> None:
    payload = build_stage5cu(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5ct_verdict={payload.get('stage5ct_verdict')}")
    console.print(
        "operator_decision_readiness_package_status="
        f"{payload.get('operator_decision_readiness_package_status')}"
    )
    console.print(
        "real_approval_decision_options_status="
        f"{payload.get('real_approval_decision_options_status')}"
    )
    console.print(f"operator_decision_option_count={payload.get('operator_decision_option_count')}")
    console.print(
        "operator_decision_option_selected_now="
        f"{str(payload.get('operator_decision_option_selected_now')).lower()}"
    )
    console.print(f"negative_fixture_count={payload.get('negative_fixture_count')}")
    console.print(
        "option_selection_misuse_case_count="
        f"{payload.get('option_selection_misuse_case_count')}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "parallel_worker_cap_for_stage5cu_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cu_and_later')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")


@app.command("validate-stage5cu-stage5ct-findings")
def validate_stage5cu_stage5ct_findings_command(
    findings: Path = typer.Option(STAGE5CU_DATA_PATHS["findings"]),
) -> None:
    counts, errors = validate_stage5cu_stage5ct_findings(findings=findings)
    _print_stage5cu_counts(counts, errors, "token_block_stage5cu_stage5ct_findings_valid=true")


@app.command("validate-stage5cu-operator-decision-readiness")
def validate_stage5cu_operator_decision_readiness_command(
    operator_decision_readiness: Path = typer.Option(
        STAGE5CU_DATA_PATHS["operator_decision_readiness"]
    ),
) -> None:
    counts, errors = validate_stage5cu_operator_decision_readiness(
        operator_decision_readiness=operator_decision_readiness
    )
    _print_stage5cu_counts(
        counts, errors, "token_block_stage5cu_operator_decision_readiness_valid=true"
    )


@app.command("validate-stage5cu-decision-options-preservation")
def validate_stage5cu_decision_options_preservation_command(
    decision_options: Path = typer.Option(STAGE5CU_DATA_PATHS["decision_options"]),
) -> None:
    counts, errors = validate_stage5cu_decision_options_preservation(
        decision_options=decision_options
    )
    _print_stage5cu_counts(
        counts, errors, "token_block_stage5cu_decision_options_preservation_valid=true"
    )


@app.command("validate-stage5cu-decision-option-negative-fixtures")
def validate_stage5cu_decision_option_negative_fixtures_command(
    fixtures: Path = typer.Option(STAGE5CU_DATA_PATHS["decision_option_negative_fixtures"]),
) -> None:
    counts, errors = validate_stage5cu_decision_option_negative_fixtures(fixtures=fixtures)
    _print_stage5cu_counts(
        counts, errors, "token_block_stage5cu_decision_option_negative_fixtures_valid=true"
    )


@app.command("validate-stage5cu-real-decision-negative-fixtures")
def validate_stage5cu_real_decision_negative_fixtures_command(
    fixtures: Path = typer.Option(STAGE5CU_DATA_PATHS["real_decision_negative_fixtures"]),
) -> None:
    counts, errors = validate_stage5cu_real_decision_negative_fixtures(fixtures=fixtures)
    _print_stage5cu_counts(
        counts, errors, "token_block_stage5cu_real_decision_negative_fixtures_valid=true"
    )


@app.command("validate-stage5cu-option-selection-misuse")
def validate_stage5cu_option_selection_misuse_command(
    misuse: Path = typer.Option(STAGE5CU_DATA_PATHS["option_selection_misuse"]),
) -> None:
    counts, errors = validate_stage5cu_option_selection_misuse(misuse=misuse)
    _print_stage5cu_counts(
        counts, errors, "token_block_stage5cu_option_selection_misuse_valid=true"
    )


@app.command("validate-stage5cu-options-nonselection")
def validate_stage5cu_options_nonselection_command(
    options_nonselection: Path = typer.Option(STAGE5CU_DATA_PATHS["options_nonselection"]),
) -> None:
    counts, errors = validate_stage5cu_options_nonselection(
        options_nonselection=options_nonselection
    )
    _print_stage5cu_counts(
        counts, errors, "token_block_stage5cu_options_nonselection_valid=true"
    )


@app.command("validate-stage5cu-real-record-blocker")
def validate_stage5cu_real_record_blocker_command(
    real_record_blocker: Path = typer.Option(STAGE5CU_DATA_PATHS["real_record_blocker"]),
) -> None:
    counts, errors = validate_stage5cu_real_record_blocker(real_record_blocker=real_record_blocker)
    _print_stage5cu_counts(counts, errors, "token_block_stage5cu_real_record_blocker_valid=true")


@app.command("validate-stage5cu-combined-gate")
def validate_stage5cu_combined_gate_command(
    combined_gate: Path = typer.Option(STAGE5CU_DATA_PATHS["combined_gate_nonsatisfaction"]),
) -> None:
    counts, errors = validate_stage5cu_combined_gate(combined_gate=combined_gate)
    _print_stage5cu_counts(counts, errors, "token_block_stage5cu_combined_gate_valid=true")


@app.command("validate-stage5cu-activation-nonauthorization")
def validate_stage5cu_activation_nonauthorization_command(
    activation: Path = typer.Option(STAGE5CU_DATA_PATHS["activation_nonauthorization"]),
) -> None:
    counts, errors = validate_stage5cu_activation_nonauthorization(activation=activation)
    _print_stage5cu_counts(
        counts, errors, "token_block_stage5cu_activation_nonauthorization_valid=true"
    )


@app.command("validate-stage5cu-stage5cs-preservation")
def validate_stage5cu_stage5cs_preservation_command() -> None:
    counts, errors = validate_stage5cu_stage5cs_preservation()
    _print_stage5cu_counts(counts, errors, "token_block_stage5cu_stage5cs_preservation_valid=true")


@app.command("validate-stage5cu-stage5cq-preservation")
def validate_stage5cu_stage5cq_preservation_command() -> None:
    counts, errors = validate_stage5cu_stage5cq_preservation()
    _print_stage5cu_counts(counts, errors, "token_block_stage5cu_stage5cq_preservation_valid=true")


@app.command("validate-stage5cu-stage5co-preservation")
def validate_stage5cu_stage5co_preservation_command() -> None:
    counts, errors = validate_stage5cu_stage5co_preservation()
    _print_stage5cu_counts(counts, errors, "token_block_stage5cu_stage5co_preservation_valid=true")


@app.command("validate-stage5cu-prior-stage-preservation")
def validate_stage5cu_prior_stage_preservation_command() -> None:
    counts, errors = validate_stage5cu_prior_stage_preservation()
    _print_stage5cu_counts(
        counts, errors, "token_block_stage5cu_prior_stage_preservation_valid=true"
    )


@app.command("validate-stage5cu-sidecar-gates")
def validate_stage5cu_sidecar_gates_command() -> None:
    counts, errors = validate_stage5cu_sidecar_gates()
    _print_stage5cu_counts(counts, errors, "token_block_stage5cu_sidecar_gates_valid=true")


@app.command("validate-stage5cu-handoff-continuity")
def validate_stage5cu_handoff_continuity_command() -> None:
    counts, errors = validate_stage5cu_handoff_continuity()
    _print_stage5cu_counts(counts, errors, "token_block_stage5cu_handoff_continuity_valid=true")


@app.command("validate-stage5cu-credential-redaction-policy")
def validate_stage5cu_credential_redaction_policy_command(
    credential_redaction: Path = typer.Option(STAGE5CU_DATA_PATHS["credential_redaction"]),
) -> None:
    counts, errors = validate_stage5cu_credential_redaction_policy(
        credential_redaction=credential_redaction
    )
    _print_stage5cu_counts(
        counts, errors, "token_block_stage5cu_credential_redaction_policy_valid=true"
    )


@app.command("validate-stage5cu")
def validate_stage5cu_command(
    summary: Path = typer.Option(STAGE5CU_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CU_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CU_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CU_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5cu(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    _print_stage5cu_counts(counts, errors, "token_block_stage5cu_valid=true")


@app.command("stage5cu-summary")
def stage5cu_summary_command(
    summary: Path = typer.Option(STAGE5CU_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5cu_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5ct_verdict={payload.get('stage5ct_verdict')}")
    console.print(
        "operator_decision_readiness_package_status="
        f"{payload.get('operator_decision_readiness_package_status')}"
    )
    console.print(
        "real_approval_decision_options_status="
        f"{payload.get('real_approval_decision_options_status')}"
    )
    console.print(f"operator_decision_option_count={payload.get('operator_decision_option_count')}")
    console.print(
        "operator_decision_option_selected_now="
        f"{str(payload.get('operator_decision_option_selected_now')).lower()}"
    )
    console.print(f"negative_fixture_count={payload.get('negative_fixture_count')}")
    console.print(
        "option_selection_misuse_case_count="
        f"{payload.get('option_selection_misuse_case_count')}"
    )
    console.print(
        "real_operator_decision_record_created_now="
        f"{str(payload.get('real_operator_decision_record_created_now')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(f"stage5bd_run_plan_id_count={payload.get('stage5bd_run_plan_id_count')}")
    console.print(f"active_lineage_record_count={payload.get('active_lineage_record_count')}")
    console.print(
        "stage5cu_completion_summary_finalized_not_pending="
        f"{str(payload.get('stage5cu_completion_summary_finalized_not_pending')).lower()}"
    )
    console.print(
        "parallel_worker_cap_for_stage5cu_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cu_and_later')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")
    console.print(f"recommended_next_prompt_type={payload.get('recommended_next_prompt_type')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


def _print_stage5cw_counts(counts: dict[str, object], errors: list[str], success_line: str) -> None:
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"error={error}")
    if errors:
        raise typer.Exit(1)
    console.print(success_line)


@app.command("build-stage5cw")
def build_stage5cw_command(
    results_dir: Path = typer.Option(STAGE5CW_RESULTS_DIR),
) -> None:
    payload = build_stage5cw(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cv_verdict={payload.get('stage5cv_verdict')}")
    console.print(
        "real_decision_package_preflight_status="
        f"{payload.get('real_decision_package_preflight_status')}"
    )
    console.print(f"operator_decision_option_count={payload.get('operator_decision_option_count')}")
    console.print(
        "operator_decision_option_selected_now="
        f"{str(payload.get('operator_decision_option_selected_now')).lower()}"
    )
    console.print(
        "stage5cu_negative_fixture_count_preserved="
        f"{payload.get('stage5cu_negative_fixture_count_preserved')}"
    )
    console.print(f"preflight_misuse_case_count={payload.get('preflight_misuse_case_count')}")
    console.print(f"stage5bd_run_plan_id_count={payload.get('stage5bd_run_plan_id_count')}")
    console.print(f"active_lineage_record_count={payload.get('active_lineage_record_count')}")
    console.print(
        "parallel_worker_cap_for_stage5cw_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cw_and_later')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")


@app.command("validate-stage5cw-stage5cv-findings")
def validate_stage5cw_stage5cv_findings_command(
    findings: Path = typer.Option(STAGE5CW_DATA_PATHS["findings"]),
) -> None:
    counts, errors = validate_stage5cw_stage5cv_findings(findings=findings)
    _print_stage5cw_counts(counts, errors, "token_block_stage5cw_stage5cv_findings_valid=true")


@app.command("validate-stage5cw-real-decision-package-preflight")
def validate_stage5cw_real_decision_package_preflight_command(
    preflight: Path = typer.Option(STAGE5CW_DATA_PATHS["real_decision_package_preflight"]),
) -> None:
    counts, errors = validate_stage5cw_real_decision_package_preflight(preflight=preflight)
    _print_stage5cw_counts(
        counts, errors, "token_block_stage5cw_real_decision_package_preflight_valid=true"
    )


@app.command("validate-stage5cw-future-real-decision-requirements")
def validate_stage5cw_future_real_decision_requirements_command(
    requirements: Path = typer.Option(STAGE5CW_DATA_PATHS["future_real_decision_requirements"]),
) -> None:
    counts, errors = validate_stage5cw_future_real_decision_requirements(
        requirements=requirements
    )
    _print_stage5cw_counts(
        counts, errors, "token_block_stage5cw_future_real_decision_requirements_valid=true"
    )


@app.command("validate-stage5cw-preflight-misuse")
def validate_stage5cw_preflight_misuse_command(
    misuse: Path = typer.Option(STAGE5CW_DATA_PATHS["preflight_misuse"]),
) -> None:
    counts, errors = validate_stage5cw_preflight_misuse(misuse=misuse)
    _print_stage5cw_counts(counts, errors, "token_block_stage5cw_preflight_misuse_valid=true")


@app.command("validate-stage5cw-stage5cu-preservation")
def validate_stage5cw_stage5cu_preservation_command() -> None:
    counts, errors = validate_stage5cw_stage5cu_preservation()
    _print_stage5cw_counts(
        counts, errors, "token_block_stage5cw_stage5cu_preservation_valid=true"
    )


@app.command("validate-stage5cw-stage5cs-preservation")
def validate_stage5cw_stage5cs_preservation_command() -> None:
    counts, errors = validate_stage5cw_stage5cs_preservation()
    _print_stage5cw_counts(
        counts, errors, "token_block_stage5cw_stage5cs_preservation_valid=true"
    )


@app.command("validate-stage5cw-options-nonselection")
def validate_stage5cw_options_nonselection_command(
    options_nonselection: Path = typer.Option(STAGE5CW_DATA_PATHS["options_nonselection"]),
) -> None:
    counts, errors = validate_stage5cw_options_nonselection(
        options_nonselection=options_nonselection
    )
    _print_stage5cw_counts(counts, errors, "token_block_stage5cw_options_nonselection_valid=true")


@app.command("validate-stage5cw-real-record-blocker")
def validate_stage5cw_real_record_blocker_command(
    real_record_blocker: Path = typer.Option(STAGE5CW_DATA_PATHS["real_record_blocker"]),
) -> None:
    counts, errors = validate_stage5cw_real_record_blocker(real_record_blocker=real_record_blocker)
    _print_stage5cw_counts(counts, errors, "token_block_stage5cw_real_record_blocker_valid=true")


@app.command("validate-stage5cw-combined-gate")
def validate_stage5cw_combined_gate_command(
    combined_gate: Path = typer.Option(STAGE5CW_DATA_PATHS["combined_gate_nonsatisfaction"]),
) -> None:
    counts, errors = validate_stage5cw_combined_gate(combined_gate=combined_gate)
    _print_stage5cw_counts(counts, errors, "token_block_stage5cw_combined_gate_valid=true")


@app.command("validate-stage5cw-activation-nonauthorization")
def validate_stage5cw_activation_nonauthorization_command(
    activation: Path = typer.Option(STAGE5CW_DATA_PATHS["activation_nonauthorization"]),
) -> None:
    counts, errors = validate_stage5cw_activation_nonauthorization(activation=activation)
    _print_stage5cw_counts(
        counts, errors, "token_block_stage5cw_activation_nonauthorization_valid=true"
    )


@app.command("validate-stage5cw-stage5bd-preservation")
def validate_stage5cw_stage5bd_preservation_command() -> None:
    counts, errors = validate_stage5cw_stage5bd_preservation()
    _print_stage5cw_counts(
        counts, errors, "token_block_stage5cw_stage5bd_preservation_valid=true"
    )


@app.command("validate-stage5cw-active-lineage-preservation")
def validate_stage5cw_active_lineage_preservation_command() -> None:
    counts, errors = validate_stage5cw_active_lineage_preservation()
    _print_stage5cw_counts(
        counts, errors, "token_block_stage5cw_active_lineage_preservation_valid=true"
    )


@app.command("validate-stage5cw-sidecar-gates")
def validate_stage5cw_sidecar_gates_command() -> None:
    counts, errors = validate_stage5cw_sidecar_gates()
    _print_stage5cw_counts(counts, errors, "token_block_stage5cw_sidecar_gates_valid=true")


@app.command("validate-stage5cw-handoff-continuity")
def validate_stage5cw_handoff_continuity_command() -> None:
    counts, errors = validate_stage5cw_handoff_continuity()
    _print_stage5cw_counts(counts, errors, "token_block_stage5cw_handoff_continuity_valid=true")


@app.command("validate-stage5cw-credential-redaction-policy")
def validate_stage5cw_credential_redaction_policy_command(
    credential_redaction: Path = typer.Option(STAGE5CW_DATA_PATHS["credential_redaction"]),
) -> None:
    counts, errors = validate_stage5cw_credential_redaction_policy(
        credential_redaction=credential_redaction
    )
    _print_stage5cw_counts(
        counts, errors, "token_block_stage5cw_credential_redaction_policy_valid=true"
    )


@app.command("validate-stage5cw")
def validate_stage5cw_command(
    summary: Path = typer.Option(STAGE5CW_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CW_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CW_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CW_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5cw(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    _print_stage5cw_counts(counts, errors, "token_block_stage5cw_valid=true")


@app.command("stage5cw-summary")
def stage5cw_summary_command(
    summary: Path = typer.Option(STAGE5CW_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5cw_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cv_verdict={payload.get('stage5cv_verdict')}")
    console.print(
        "real_decision_package_preflight_status="
        f"{payload.get('real_decision_package_preflight_status')}"
    )
    console.print(f"operator_decision_option_count={payload.get('operator_decision_option_count')}")
    console.print(
        "operator_decision_option_selected_now="
        f"{str(payload.get('operator_decision_option_selected_now')).lower()}"
    )
    console.print(
        "stage5cu_negative_fixture_count_preserved="
        f"{payload.get('stage5cu_negative_fixture_count_preserved')}"
    )
    console.print(
        "stage5cu_real_decision_negative_fixture_count_preserved="
        f"{payload.get('stage5cu_real_decision_negative_fixture_count_preserved')}"
    )
    console.print(f"preflight_misuse_case_count={payload.get('preflight_misuse_case_count')}")
    console.print(
        "real_operator_decision_record_created_now="
        f"{str(payload.get('real_operator_decision_record_created_now')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(f"stage5bd_run_plan_id_count={payload.get('stage5bd_run_plan_id_count')}")
    console.print(f"active_lineage_record_count={payload.get('active_lineage_record_count')}")
    console.print(
        "stage5cw_completion_summary_finalized_not_pending="
        f"{str(payload.get('stage5cw_completion_summary_finalized_not_pending')).lower()}"
    )
    console.print(
        "parallel_worker_cap_for_stage5cw_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cw_and_later')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")
    console.print(f"recommended_next_prompt_type={payload.get('recommended_next_prompt_type')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


def _print_stage5cy_counts(counts: dict[str, object], errors: list[str], success_line: str) -> None:
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(f"error={error}")
    if errors:
        raise typer.Exit(1)
    console.print(success_line)


@app.command("build-stage5cy")
def build_stage5cy_command(
    results_dir: Path = typer.Option(STAGE5CY_RESULTS_DIR),
) -> None:
    payload = build_stage5cy(results_dir=results_dir)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cx_verdict={payload.get('stage5cx_verdict')}")
    console.print(
        "stage5cw_pytest_count_reconciliation_status="
        f"{payload.get('stage5cw_pytest_count_reconciliation_status')}"
    )
    console.print(
        "operator_facing_option_selection_preflight_status="
        f"{payload.get('operator_facing_option_selection_preflight_status')}"
    )
    console.print(f"operator_decision_option_count={payload.get('operator_decision_option_count')}")
    console.print(
        "operator_decision_option_selected_now="
        f"{str(payload.get('operator_decision_option_selected_now')).lower()}"
    )
    console.print(f"stage5bd_run_plan_id_count={payload.get('stage5bd_run_plan_id_count')}")
    console.print(f"active_lineage_record_count={payload.get('active_lineage_record_count')}")
    console.print(
        "parallel_worker_cap_for_stage5cy_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cy_and_later')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")


@app.command("validate-stage5cy-stage5cx-findings")
def validate_stage5cy_stage5cx_findings_command(
    findings: Path = typer.Option(STAGE5CY_DATA_PATHS["findings"]),
) -> None:
    counts, errors = validate_stage5cy_stage5cx_findings(findings=findings)
    _print_stage5cy_counts(counts, errors, "token_block_stage5cy_stage5cx_findings_valid=true")


@app.command("validate-stage5cy-real-decision-preflight-preservation")
def validate_stage5cy_real_decision_preflight_preservation_command(
    preflight: Path = typer.Option(STAGE5CY_DATA_PATHS["real_decision_preflight_preservation"]),
) -> None:
    counts, errors = validate_stage5cy_real_decision_preflight_preservation(
        preflight=preflight
    )
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_real_decision_preflight_preservation_valid=true"
    )


@app.command("validate-stage5cy-operator-option-selection-preflight")
def validate_stage5cy_operator_option_selection_preflight_command(
    preflight: Path = typer.Option(STAGE5CY_DATA_PATHS["operator_option_selection_preflight"]),
) -> None:
    counts, errors = validate_stage5cy_operator_option_selection_preflight(
        preflight=preflight
    )
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_operator_option_selection_preflight_valid=true"
    )


@app.command("validate-stage5cy-option-selection-requirements")
def validate_stage5cy_option_selection_requirements_command(
    requirements: Path = typer.Option(STAGE5CY_DATA_PATHS["option_selection_requirements"]),
) -> None:
    counts, errors = validate_stage5cy_option_selection_requirements(requirements=requirements)
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_option_selection_requirements_valid=true"
    )


@app.command("validate-stage5cy-option-selection-misuse")
def validate_stage5cy_option_selection_misuse_command(
    misuse: Path = typer.Option(STAGE5CY_DATA_PATHS["option_selection_misuse"]),
) -> None:
    counts, errors = validate_stage5cy_option_selection_misuse(misuse=misuse)
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_option_selection_misuse_valid=true"
    )


@app.command("validate-stage5cy-options-nonselection")
def validate_stage5cy_options_nonselection_command(
    options_nonselection: Path = typer.Option(STAGE5CY_DATA_PATHS["options_nonselection"]),
) -> None:
    counts, errors = validate_stage5cy_options_nonselection(
        options_nonselection=options_nonselection
    )
    _print_stage5cy_counts(counts, errors, "token_block_stage5cy_options_nonselection_valid=true")


@app.command("validate-stage5cy-validation-count-reconciliation")
def validate_stage5cy_validation_count_reconciliation_command(
    reconciliation: Path = typer.Option(STAGE5CY_DATA_PATHS["validation_count_reconciliation"]),
) -> None:
    counts, errors = validate_stage5cy_validation_count_reconciliation(
        reconciliation=reconciliation
    )
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_validation_count_reconciliation_valid=true"
    )


@app.command("validate-stage5cy-real-record-blocker")
def validate_stage5cy_real_record_blocker_command(
    real_record_blocker: Path = typer.Option(STAGE5CY_DATA_PATHS["real_record_blocker"]),
) -> None:
    counts, errors = validate_stage5cy_real_record_blocker(
        real_record_blocker=real_record_blocker
    )
    _print_stage5cy_counts(counts, errors, "token_block_stage5cy_real_record_blocker_valid=true")


@app.command("validate-stage5cy-combined-gate")
def validate_stage5cy_combined_gate_command(
    combined_gate: Path = typer.Option(STAGE5CY_DATA_PATHS["combined_gate_nonsatisfaction"]),
) -> None:
    counts, errors = validate_stage5cy_combined_gate(combined_gate=combined_gate)
    _print_stage5cy_counts(counts, errors, "token_block_stage5cy_combined_gate_valid=true")


@app.command("validate-stage5cy-activation-nonauthorization")
def validate_stage5cy_activation_nonauthorization_command(
    activation: Path = typer.Option(STAGE5CY_DATA_PATHS["activation_nonauthorization"]),
) -> None:
    counts, errors = validate_stage5cy_activation_nonauthorization(activation=activation)
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_activation_nonauthorization_valid=true"
    )


@app.command("validate-stage5cy-stage5cw-preservation")
def validate_stage5cy_stage5cw_preservation_command() -> None:
    counts, errors = validate_stage5cy_stage5cw_preservation()
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_stage5cw_preservation_valid=true"
    )


@app.command("validate-stage5cy-stage5cu-preservation")
def validate_stage5cy_stage5cu_preservation_command() -> None:
    counts, errors = validate_stage5cy_stage5cu_preservation()
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_stage5cu_preservation_valid=true"
    )


@app.command("validate-stage5cy-stage5cs-preservation")
def validate_stage5cy_stage5cs_preservation_command() -> None:
    counts, errors = validate_stage5cy_stage5cs_preservation()
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_stage5cs_preservation_valid=true"
    )


@app.command("validate-stage5cy-stage5bd-preservation")
def validate_stage5cy_stage5bd_preservation_command() -> None:
    counts, errors = validate_stage5cy_stage5bd_preservation()
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_stage5bd_preservation_valid=true"
    )


@app.command("validate-stage5cy-active-lineage-preservation")
def validate_stage5cy_active_lineage_preservation_command() -> None:
    counts, errors = validate_stage5cy_active_lineage_preservation()
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_active_lineage_preservation_valid=true"
    )


@app.command("validate-stage5cy-sidecar-gates")
def validate_stage5cy_sidecar_gates_command() -> None:
    counts, errors = validate_stage5cy_sidecar_gates()
    _print_stage5cy_counts(counts, errors, "token_block_stage5cy_sidecar_gates_valid=true")


@app.command("validate-stage5cy-handoff-continuity")
def validate_stage5cy_handoff_continuity_command() -> None:
    counts, errors = validate_stage5cy_handoff_continuity()
    _print_stage5cy_counts(counts, errors, "token_block_stage5cy_handoff_continuity_valid=true")


@app.command("validate-stage5cy-credential-redaction-policy")
def validate_stage5cy_credential_redaction_policy_command(
    credential_redaction: Path = typer.Option(STAGE5CY_DATA_PATHS["credential_redaction"]),
) -> None:
    counts, errors = validate_stage5cy_credential_redaction_policy(
        credential_redaction=credential_redaction
    )
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_credential_redaction_policy_valid=true"
    )


@app.command("validate-stage5cy-governance-scope-control")
def validate_stage5cy_governance_scope_control_command(
    governance_scope: Path = typer.Option(STAGE5CY_DATA_PATHS["governance_scope_control"]),
) -> None:
    counts, errors = validate_stage5cy_governance_scope_control(governance_scope=governance_scope)
    _print_stage5cy_counts(
        counts, errors, "token_block_stage5cy_governance_scope_control_valid=true"
    )


@app.command("validate-stage5cy")
def validate_stage5cy_command(
    summary: Path = typer.Option(STAGE5CY_DATA_PATHS["summary"]),
    next_stage_decision: Path = typer.Option(STAGE5CY_DATA_PATHS["next_stage"]),
    guardrail: Path = typer.Option(STAGE5CY_DATA_PATHS["guardrail"]),
    results_dir: Path = typer.Option(STAGE5CY_RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5cy(
        summary=summary,
        next_stage_decision=next_stage_decision,
        guardrail=guardrail,
        results_dir=results_dir,
    )
    _print_stage5cy_counts(counts, errors, "token_block_stage5cy_valid=true")


@app.command("stage5cy-summary")
def stage5cy_summary_command(
    summary: Path = typer.Option(STAGE5CY_DATA_PATHS["summary"]),
) -> None:
    payload = load_stage5cy_summary(summary=summary)
    console.print(f"stage_id={payload.get('stage_id')}")
    console.print(f"status={payload.get('status')}")
    console.print(f"stage5cx_verdict={payload.get('stage5cx_verdict')}")
    console.print(
        "stage5cw_pytest_count_reconciliation_status="
        f"{payload.get('stage5cw_pytest_count_reconciliation_status')}"
    )
    console.print(
        "operator_facing_option_selection_preflight_status="
        f"{payload.get('operator_facing_option_selection_preflight_status')}"
    )
    console.print(f"operator_decision_option_count={payload.get('operator_decision_option_count')}")
    console.print(
        "operator_decision_option_selected_now="
        f"{str(payload.get('operator_decision_option_selected_now')).lower()}"
    )
    console.print(f"selected_option_id={payload.get('selected_option_id')}")
    console.print(
        "real_operator_decision_record_created_now="
        f"{str(payload.get('real_operator_decision_record_created_now')).lower()}"
    )
    console.print(
        "combined_approval_gate_satisfied_now="
        f"{str(payload.get('combined_approval_gate_satisfied_now')).lower()}"
    )
    console.print(
        "activation_decision_valid_now="
        f"{str(payload.get('activation_decision_valid_now')).lower()}"
    )
    console.print(
        "active_planning_input_authorized_now="
        f"{str(payload.get('active_planning_input_authorized_now')).lower()}"
    )
    console.print(f"stage5bd_run_plan_id_count={payload.get('stage5bd_run_plan_id_count')}")
    console.print(f"active_lineage_record_count={payload.get('active_lineage_record_count')}")
    console.print(
        "parallel_worker_cap_for_stage5cy_and_later="
        f"{payload.get('parallel_worker_cap_for_stage5cy_and_later')}"
    )
    console.print(f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}")
    console.print(f"recommended_next_prompt_type={payload.get('recommended_next_prompt_type')}")
    console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="token-block")
