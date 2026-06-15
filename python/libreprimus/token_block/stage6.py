"""Stage 6 diagnostic backlog readiness metadata."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.doc_staleness.stale_current_claims import audit_repository
from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import validate_source_index
from libreprimus.token_block.models import read_yaml, write_yaml

STAGE_ID = "stage-6"
STAGE_TOKEN = "stage6"
STAGE_TITLE = (
    "Stage 6 - Diagnostic backlog census, discovery-probe readiness, result-bundle "
    "policy, and Stage 7/8/9 handoff, without execution"
)
PROMPT_TYPE = "codex_plan_mode_probe_diagnostic_readiness"
PREVIOUS_STAGE_ID = "stage-5ei"
PREVIOUS_STAGE_TITLE = "Stage 5EI - Final Stage 5 triangle-transposition and diagnostics transition, without execution"
NEXT_STAGE_ID = "stage-6b"
NEXT_STAGE_TITLE = "Stage 6B - Final finite Stage 7 probe manifest and archive-run contract, without execution"
NEXT_PROMPT_TYPE = "codex_plan_mode_probe_manifest_finalization"

PROJECT_STATE_DIR = Path("data/project-state")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
TOKEN_BLOCK_DIR = Path("data/token-block")
HISTORICAL_ROUTE_DIR = Path("data/historical-route")
OVERLAY_DIR = Path("data/operator-console/source-browser/number-fact-overlays")
RESEARCH_DIR = Path("data/research")
CODEX_OUTPUT_DIR = Path("codex-output")

CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
DOC_STALENESS_SOURCE_OF_TRUTH_PATH = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
OPERATIONAL_FILE_MAP_PATH = PROJECT_STATE_DIR / "operational-file-map.yaml"
STAGE_SUMMARY_RECORDS_PATH = RESEARCH_DIR / "stage-summary-records-v0.yaml"
DEV_LOG_PATH = Path("docs/development-logs/2026-06-14-stage-6-diagnostic-backlog-readiness.md")
RESEARCH_LOG_PATH = Path("research-log/2026-06-14-stage6-next-stage-decision-summary.md")
EXPERIMENT_DOC_PATH = Path("docs/experiments/stage-6-diagnostic-backlog-readiness.md")

PROTECTED_LOCAL_PATHS = [
    "data/project-state/stage5cy-reviewable-source-digest-index.yaml",
    "data/project-state/stage5eg-source-browser-loadability-summary.yaml",
    "data/project-state/stage5eg-summary.yaml",
    "data/token-block/stage5dg-real-operator-approval-record.yaml",
]

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage6-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage6-next-stage-decision.yaml",
    "stage5ei_preservation": PROJECT_STATE_DIR / "stage6-stage5ei-preservation.yaml",
    "stage5eh_probe_manifest_preservation": PROJECT_STATE_DIR
    / "stage6-stage5eh-probe-manifest-preservation.yaml",
    "third_party_source_root_census": PROJECT_STATE_DIR / "stage6-third-party-source-root-census.yaml",
    "source_lock_family_census": PROJECT_STATE_DIR / "stage6-source-lock-family-census.yaml",
    "diagnostic_backlog_census": PROJECT_STATE_DIR / "stage6-diagnostic-backlog-census.yaml",
    "stage7_readiness_classification": PROJECT_STATE_DIR / "stage6-stage7-readiness-classification.yaml",
    "stage7_candidate_menu": PROJECT_STATE_DIR / "stage6-stage7-candidate-menu.yaml",
    "result_bundle_policy": PROJECT_STATE_DIR / "stage6-result-bundle-policy.yaml",
    "no_lossy_filtering_policy": PROJECT_STATE_DIR / "stage6-no-lossy-filtering-policy.yaml",
    "non_cuda_non_scoring_triage_policy": PROJECT_STATE_DIR
    / "stage6-non-cuda-non-scoring-triage-policy.yaml",
    "post_run_analysis_workflow": PROJECT_STATE_DIR / "stage6-post-run-analysis-workflow.yaml",
    "deep_research_archive_review_policy": PROJECT_STATE_DIR
    / "stage6-deep-research-archive-review-policy.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage6-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage6-reviewability-gap-register.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR / "stage6-source-browser-loadability-summary.yaml",
    "current_stage_transition": PROJECT_STATE_DIR / "stage6-current-stage-transition.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage6-chatgpt-context-update-summary.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "source_harvester_third_party_source_root_census": SOURCE_HARVESTER_DIR
    / "stage6-third-party-source-root-census.yaml",
    "observation_rune_frequency_source_lock_register": SOURCE_HARVESTER_DIR
    / "stage6-observation-rune-frequency-source-lock-register.yaml",
    "observation_rune_frequency_file_inventory": SOURCE_HARVESTER_DIR
    / "stage6-observation-rune-frequency-file-inventory.yaml",
    "observation_rune_frequency_attachment_context_map": SOURCE_HARVESTER_DIR
    / "stage6-observation-rune-frequency-attachment-context-map.yaml",
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage6-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage6-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage6-raw-source-noncommit-proof.yaml",
    "third_party_source_noncommit_proof": SOURCE_HARVESTER_DIR
    / "stage6-third-party-source-noncommit-proof.yaml",
}

TOKEN_BLOCK_PATHS: dict[str, Path] = {
    "discovery_probe_manifest_registry": TOKEN_BLOCK_DIR / "stage6-discovery-probe-manifest-registry.yaml",
    "route_fingerprint_taxonomy": TOKEN_BLOCK_DIR / "stage6-route-fingerprint-taxonomy.yaml",
    "null_negative_control_policy": TOKEN_BLOCK_DIR / "stage6-null-negative-control-policy.yaml",
    "bridge_capture_taxonomy": TOKEN_BLOCK_DIR / "stage6-bridge-capture-taxonomy.yaml",
    "keeper_taxonomy": TOKEN_BLOCK_DIR / "stage6-keeper-taxonomy.yaml",
    "stage7_result_bundle_template": TOKEN_BLOCK_DIR / "stage6-stage7-result-bundle-template.yaml",
    "stage7_result_template_registry": TOKEN_BLOCK_DIR / "stage6-stage7-result-template-registry.yaml",
    "stage7_execution_gate_contract": TOKEN_BLOCK_DIR / "stage6-stage7-execution-gate-contract.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage6-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage6-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage6-no-execution-transition-gate.yaml",
}

HISTORICAL_ROUTE_PATHS: dict[str, Path] = {
    "observation_rune_frequency_adjacent_doublet_signature": HISTORICAL_ROUTE_DIR
    / "stage6-observation-rune-frequency-adjacent-doublet-signature.yaml",
    "observation_rune_frequency_421_bridge_candidates": HISTORICAL_ROUTE_DIR
    / "stage6-observation-rune-frequency-421-bridge-candidates.yaml",
    "observation_rune_frequency_disk_lag5_crosslink": HISTORICAL_ROUTE_DIR
    / "stage6-observation-rune-frequency-disk-lag5-crosslink.yaml",
    "observation_rune_frequency_blake_orc_context": HISTORICAL_ROUTE_DIR
    / "stage6-observation-rune-frequency-blake-orc-context.yaml",
    "observation_rune_frequency_probe_readiness": HISTORICAL_ROUTE_DIR
    / "stage6-observation-rune-frequency-probe-readiness.yaml",
    "pdd153_triangle_readiness_deferment": HISTORICAL_ROUTE_DIR
    / "stage6-pdd153-triangle-readiness-deferment.yaml",
    "triangular_transposition_taxonomy_resolution_plan": HISTORICAL_ROUTE_DIR
    / "stage6-triangular-transposition-taxonomy-resolution-plan.yaml",
    "page32_pdd153_cross_surface_control_policy": HISTORICAL_ROUTE_DIR
    / "stage6-page32-pdd153-cross-surface-control-policy.yaml",
    "stage8_triangle_readiness_handoff": HISTORICAL_ROUTE_DIR
    / "stage6-stage8-triangle-readiness-handoff.yaml",
}

OPERATOR_PATHS: dict[str, Path] = {
    "observation_rune_frequency_overlays": OVERLAY_DIR / "stage6-observation-rune-frequency-overlays.yaml"
}

DATA_PATHS: dict[str, Path] = {
    **PROJECT_STATE_PATHS,
    **SOURCE_HARVESTER_PATHS,
    **TOKEN_BLOCK_PATHS,
    **HISTORICAL_ROUTE_PATHS,
    **OPERATOR_PATHS,
}


def _schema_path(category: str, key: str) -> Path:
    return Path(f"schemas/{category}/stage6-{key.replace('_', '-')}-v0.schema.json")


SCHEMA_PATHS: dict[str, Path] = {
    key: _schema_path("project-state", key) for key in PROJECT_STATE_PATHS
}
SCHEMA_PATHS.update({key: _schema_path("source-harvester", key) for key in SOURCE_HARVESTER_PATHS})
SCHEMA_PATHS.update({key: _schema_path("token-block", key) for key in TOKEN_BLOCK_PATHS})
SCHEMA_PATHS.update({key: _schema_path("historical-route", key) for key in HISTORICAL_ROUTE_PATHS})
SCHEMA_PATHS.update(
    {
        "observation_rune_frequency_overlays": Path(
            "schemas/operator-console/stage6-observation-rune-frequency-overlay-collection-v0.schema.json"
        )
    }
)

FALSE_GUARDRAILS: dict[str, bool] = {
    "activation_authorized_now": False,
    "activation_decision_valid_now": False,
    "active_ingestion_performed": False,
    "active_manifest_registry_updated": False,
    "active_planning_input_authorized_now": False,
    "active_planning_input_selected_now": False,
    "active_token_block_manifest_changed": False,
    "alberti_cipher_execution_performed_now": False,
    "alberti_html_executed_now": False,
    "audio_stego_performed": False,
    "benchmark_performed": False,
    "branch_enumeration_performed": False,
    "byte_stream_generation_authorized_now": False,
    "canonical_corpus_active": False,
    "combined_approval_gate_satisfied_now": False,
    "community_code_executed_now": False,
    "cuda_execution_performed": False,
    "cuda_triage_performed": False,
    "decode_attempt_performed": False,
    "decryption_attempt_performed_now": False,
    "diagnostic_execution_performed_now": False,
    "diagnostic_probe_run_now": False,
    "disk_cipher_execution_performed_now": False,
    "dwh_hash_search_performed": False,
    "execution_authorized_now": False,
    "execution_performed": False,
    "f5_extraction_performed_now": False,
    "f5_password_search_performed_now": False,
    "full_cartesian_product_enumerated": False,
    "generated_outputs_committed": False,
    "hash_preimage_search_performed": False,
    "hidden_content_image_forensics_performed": False,
    "historical_source_lock_records_rewritten": False,
    "html_tool_executed_now": False,
    "image_forensics_performed": False,
    "known_plaintext_attack_performed_now": False,
    "lossy_filtering_performed": False,
    "machine_code_execution_performed_now": False,
    "mayfly_route_extraction_performed_now": False,
    "midi_route_extraction_performed_now": False,
    "mp3stego_execution_performed": False,
    "music_route_extraction_performed_now": False,
    "native_code_execution_performed_now": False,
    "network_target_validation_performed_now": False,
    "new_source_lock_evidence_added_as_raw_body": False,
    "number_fact_backfill_performed_now": False,
    "ocr_performed": False,
    "openpuff_execution_performed": False,
    "operator_target_priority_decision_created_now": False,
    "outguess_execution_performed": False,
    "page13_f5_payload_claim_accepted_now": False,
    "page32_route_extraction_performed_now": False,
    "page56_hash_preimage_tested_now": False,
    "page_boundaries_final": False,
    "page_boundaries_finalized": False,
    "pdf_ocr_or_hidden_content_rendering_performed": False,
    "pivot_target_selected_now": False,
    "pgp_private_key_operation_performed": False,
    "pgp_signature_verified_now": False,
    "pgp_verification_performed_now": False,
    "probe_execution_performed_now": False,
    "raw_source_files_committed": False,
    "raw_third_party_files_committed": False,
    "real_byte_stream_generated": False,
    "route_extraction_performed_now": False,
    "route_stream_generated_now": False,
    "scoring_performed": False,
    "scoring_triage_performed": False,
    "semantic_image_interpretation_performed": False,
    "solve_claim": False,
    "spectrogram_stego_performed": False,
    "stegdetect_execution_performed_now": False,
    "stego_tool_execution_performed": False,
    "target_class_validation_implemented": False,
    "target_priority_decision_created_now": False,
    "token_block_experiment_executed": False,
    "token_block_variant_byte_streams_generated": False,
    "tor_network_access_performed": False,
    "triangle_route_extraction_performed_now": False,
    "triangular_transposition_readouts_generated_now": False,
    "triangular_transposition_route_stream_generated_now": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "vm_bytecode_execution_performed_now": False,
    "website_expansion_performed": False,
}

STAGE6_FALSE_GUARDRAILS = {
    "stage6_probe_execution_allowed": False,
    "stage6_probe_execution_performed_now": False,
    "stage6_result_archive_created_now": False,
    "stage6_zip_result_bundle_created_now": False,
    "stage6_runs_bigrams_py_now": False,
    "stage6_recomputes_canonical_bigram_matrix_now": False,
    "stage6_runs_lag5_probe_now": False,
    "stage6_runs_diskcipher_probe_now": False,
    "stage6_runs_music_probe_now": False,
    "stage6_runs_triangle_probe_now": False,
    "stage6_runs_stego_probe_now": False,
    "stage6_selects_stage7_probe_outputs_now": False,
    "stage6_discards_outputs_by_score_now": False,
}

SOURCE_ROOTS = [
    ("ciada_solvers_iddqd_v2", "third_party/CiadaSolversIddqd_v2", "present_local_ignored", "allowed_after_stage6"),
    ("cicada_solvers_iddqd", "third_party/CicadaSolversIddqd", "present_local_ignored", "support_only"),
    ("cicada_music", "third_party/CicadaMusic", "present_local_ignored", "conditional"),
    ("cicada_music_community_theory", "third_party/CicadaMusic/community-theory", "present_local_ignored", "conditional"),
    ("diskcipher_stuff", "third_party/DiskCipherStuff", "present_local_ignored", "conditional"),
    ("lag5_phenomenon", "third_party/Lag5-phenomenon", "present_local_ignored", "allowed_after_stage6"),
    ("observation_on_rune_frequency", "third_party/ObservationOnRuneFrequency", "present_local_ignored", "allowed_after_stage6"),
    ("number_triangle_stuff", "third_party/NumberTriangleStuff", "present_local_ignored", "stage8_triangle_readiness"),
    ("number_facts_collection", "third_party/NumberFactsCollection", "present_local_ignored", "support_only"),
    ("potential_hint_3301_page32", "third_party/PotentialHint-3301-on-Page32", "present_local_ignored", "conditional"),
    ("reddit_stuff", "third_party/RedditStuff", "present_local_ignored", "support_only"),
    ("community_observations", "third_party/CommunityObservations", "present_local_ignored", "support_only"),
    ("star_artifacts_lp_page_images", "third_party/StarArtifactsInLPPageImages", "present_local_ignored", "conditional"),
    ("big_gaps_liber_primus", "third_party/BigGapsFoundInLiberPrimus", "present_local_ignored", "support_only"),
    ("red_runes_koan_connection", "third_party/RedRunes_Possible_Koan_Connection", "present_local_ignored", "support_only"),
    ("potential_crib_red_runes_pages_54_55", "third_party/PotentialCrib_RedRunes_Pages_54_55", "present_local_ignored", "conditional"),
    ("mobius_totient_first_page_theory", "third_party/Mobius_totient_first_page_theory", "present_local_ignored", "support_only"),
    ("cribbing_page15", "third_party/CribbingPage15", "present_local_ignored", "support_only"),
    ("liber_primus_pages", "third_party/LiberPrimusPages", "present_local_ignored", "support_only"),
    ("cicada_archive", "third_party/CicadaArchive", "present_local_ignored", "support_only"),
    ("complete_cicada3301_archive", "third_party/The-Complete-Cicada3301-Archive-main", "present_local_ignored", "support_only"),
    ("interconnected_chapters", "third_party/interconnected-chapters", "present_local_ignored", "support_only"),
    ("stego_positive_controls", "third_party/StegoPositiveControls", "present_local_ignored", "conditional"),
    ("source_snapshots", "third_party/SourceSnapshots", "present_local_ignored", "support_only"),
    ("useful_files_and_ideas", "third_party/UsefulFilesAndIdeas", "present_local_ignored", "support_only"),
]

LARGE_ROOT_IDS = {
    "ciada_solvers_iddqd_v2",
    "cicada_solvers_iddqd",
    "cicada_music",
    "cicada_music_community_theory",
    "diskcipher_stuff",
    "liber_primus_pages",
    "cicada_archive",
    "complete_cicada3301_archive",
    "source_snapshots",
}

DIAGNOSTIC_FAMILIES = [
    "iddqd_v2_canonical_source_root_readiness",
    "outguess_pgp_xor_byte_string_detector_diagnostics",
    "lag5_copy_null_doublet_diagnostics",
    "adjacent_doublet_frequency_signature_421_fibonacci",
    "diskcipher_alberti_doublet_56311_readiness",
    "cicada_music_score_metadata_and_number_diagnostics",
    "page32_numberfacts_pixel_colour_diagnostics",
    "pdd153_page32_triangle_readiness",
    "community_visual_negative_space_red_rune_controls",
    "page54_55_red_number_alignment_readiness",
    "page56_dwh_hash_contract_readiness",
    "token_block_static_primary60_matrix_readiness",
    "ouroboros_self_reference_symbolic_context",
    "fandom_archive_source_crosswalk_readiness",
    "stego_positive_control_toolchain_readiness",
]

STAGE_FAMILY_MAP = {
    "stage-5bk": [
        "iddqd_v2_canonical_source_root_readiness",
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "token_block_static_primary60_matrix_readiness",
    ],
    "stage-5di": [
        "pdd153_page32_triangle_readiness",
        "page56_dwh_hash_contract_readiness",
        "page32_numberfacts_pixel_colour_diagnostics",
        "community_visual_negative_space_red_rune_controls",
    ],
    "stage-5dj": ["cicada_music_score_metadata_and_number_diagnostics"],
    "stage-5dk": ["fandom_archive_source_crosswalk_readiness", "page56_dwh_hash_contract_readiness"],
    "stage-5dl": ["pdd153_page32_triangle_readiness", "diskcipher_alberti_doublet_56311_readiness"],
    "stage-5dm": [
        "pdd153_page32_triangle_readiness",
        "ouroboros_self_reference_symbolic_context",
        "community_visual_negative_space_red_rune_controls",
        "token_block_static_primary60_matrix_readiness",
    ],
    "stage-5dn": ["diskcipher_alberti_doublet_56311_readiness", "pdd153_page32_triangle_readiness"],
    "stage-5do": ["page32_numberfacts_pixel_colour_diagnostics"],
    "stage-5ds": [
        "cicada_music_score_metadata_and_number_diagnostics",
        "ouroboros_self_reference_symbolic_context",
        "token_block_static_primary60_matrix_readiness",
    ],
    "stage-5du": ["community_visual_negative_space_red_rune_controls", "page54_55_red_number_alignment_readiness"],
    "stage-5eh": [
        "lag5_copy_null_doublet_diagnostics",
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "page54_55_red_number_alignment_readiness",
        "stego_positive_control_toolchain_readiness",
    ],
    "stage-5ei": ["pdd153_page32_triangle_readiness", "adjacent_doublet_frequency_signature_421_fibonacci"],
}

STAGE5EH_PROBE_IDS = [
    "lag5_reproduction_probe_candidate_v0",
    "lag5_doublet_suppressed_null_probe_candidate_v0",
    "lag5_page_section_event_overlay_probe_candidate_v0",
    "lag5_token_block_neighborhood_probe_candidate_v0",
    "lag5_pdd153_56311_route_overlay_probe_candidate_v0",
    "lag5_page32_route_stream_fingerprint_probe_candidate_v0",
    "lag5_disk_doublet_suppression_model_constraint_probe_candidate_v0",
    "lag5_negative_space_null_marker_bridge_probe_candidate_v0",
    "outguess_pgp_signature_verification_probe_candidate_v0",
    "outguess_00_01_02_xor_reconstruction_probe_candidate_v0",
    "outguess_03_jpeg_extraction_metadata_probe_candidate_v0",
    "outguess_03_jpeg_human_transcription_verification_probe_candidate_v0",
    "xor_txt_29_symbol_alphabet_classification_probe_candidate_v0",
    "outguess_magic_square_route_mask_probe_candidate_v0",
    "byte_strings_outguess_xor_precedent_comparison_probe_candidate_v0",
    "byte_strings_03_control_key_probe_candidate_v0",
    "byte_strings_16x16_matrix_route_mask_probe_candidate_v0",
    "byte_strings_token_block_matrix_comparison_probe_candidate_v0",
    "page54_55_red_numbered_line_block_transcript_alignment_probe_candidate_v0",
    "lp_pages_stegdetect_baseline_probe_manifest_v0",
    "known_outguessed_pages_stegdetect_comparison_probe_manifest_v0",
    "star_artifact_mod8_dct_residue_probe_manifest_v0",
    "page13_canonical_image_hash_and_detector_reproduction_probe_manifest_v0",
]

OBSERVATION_PROBE_IDS = [
    "observation_on_rune_frequency_attachment_context_reconstruction_v0",
    "adjacent_doublet_diagonal_vector_reproduction_v0",
    "adjacent_doublet_86_89_boundary_reconciliation_v0",
    "diagonal_421_delimiter_alphabet_order_control_v0",
    "lag1_lag5_joint_copy_null_fingerprint_v0",
    "diskcipher_doublet_metric_reimplementation_preflight_v0",
    "doublet_421_numeric_bridge_verification_v0",
    "diagonal_421_blake_orc_control_v0",
    "diagonal_421_occurrence_index_prime_emirp_probe_v0",
    "adjacent_doublet_music_29_note_projection_control_v0",
    "adjacent_doublet_token_block_29_symbol_projection_control_v0",
]

READINESS_CLASSES = [
    "stage7_ready_metadata_only",
    "stage7_ready_deterministic_no_toolchain",
    "stage7_conditional_requires_canonical_transcript_or_boundary",
    "stage7_conditional_requires_toolchain",
    "stage7_conditional_requires_toolchain_and_canonical_image",
    "stage7_conditional_requires_reimplementation_metric_definition",
    "stage7_conditional_requires_canonical_score_or_music_metadata",
    "stage7_conditional_requires_source_and_fixture_boundary",
    "stage7_conditional_requires_canonical_source_boundary",
    "stage7_conditional_requires_canonical_image_or_transcript",
    "stage8_triangle_readiness",
    "stage9_triangle_experiment_deferred",
    "quarantine_background",
]

PROBE_BLOCKED_ACTIONS = [
    "solve_claim",
    "target_selection",
    "route_stream_generation_unless_later_stage_explicitly_allows",
    "byte_stream_generation_unless_later_stage_explicitly_allows",
]


def _probe_classification(
    family_id: str,
    readiness_class: str,
    *,
    source_roots: list[str],
    source_records: list[str] | None = None,
    source_gap_or_stage6c_precondition: str | None = None,
    run_allowed_stage: str = "stage-7",
    triangle_scope_crosslink_only: bool = False,
) -> dict[str, Any]:
    return {
        "family_id": family_id,
        "readiness_class": readiness_class,
        "source_roots": source_roots,
        "source_records": source_records or [],
        "source_gap_or_stage6c_precondition": source_gap_or_stage6c_precondition,
        "run_allowed_stage": run_allowed_stage,
        "triangle_scope_crosslink_only": triangle_scope_crosslink_only,
        "triangle_execution_deferred_to_stage8_stage9": triangle_scope_crosslink_only,
    }


LAG5_SOURCE_RECORDS = [
    "data/source-harvester/stage5eh-lag5-local-source-lock-register.yaml",
    "data/source-harvester/stage5eh-lag5-file-inventory.yaml",
    "data/project-state/stage5eh-diagnostic-probe-manifest-index.yaml",
    "data/token-block/stage5eh-diagnostic-probe-manifest-records.yaml",
]
OUTGUESS_SOURCE_RECORDS = [
    "data/source-harvester/stage5eh-lp-outguessed-source-lock-register.yaml",
    "data/source-harvester/stage5eh-lp-outguessed-pgp-signed-output-inventory.yaml",
    "data/source-harvester/stage5eh-cicada-solvers-iddqd-v2-crosswalk.yaml",
    "data/source-harvester/stage5eh-byte-strings-context-crosswalk.yaml",
    "data/project-state/stage5eh-diagnostic-probe-manifest-index.yaml",
    "data/token-block/stage5eh-diagnostic-probe-manifest-records.yaml",
]
PAGE54_SOURCE_RECORDS = [
    "data/source-harvester/stage5eh-page54-55-red-number-source-crosswalk.yaml",
    "data/project-state/stage5eh-diagnostic-probe-manifest-index.yaml",
    "data/token-block/stage5eh-diagnostic-probe-manifest-records.yaml",
]
STEGO_SOURCE_RECORDS = [
    "data/source-harvester/stage5eh-page13-stegdetect-operator-result-lock.yaml",
    "data/source-harvester/stage5eh-cicada-solvers-iddqd-v2-crosswalk.yaml",
    "data/project-state/stage5eh-diagnostic-probe-manifest-index.yaml",
    "data/token-block/stage5eh-diagnostic-probe-manifest-records.yaml",
]
OBSERVATION_SOURCE_RECORDS = [
    "data/source-harvester/stage6-observation-rune-frequency-source-lock-register.yaml",
    "data/source-harvester/stage6-observation-rune-frequency-file-inventory.yaml",
    "data/source-harvester/stage6-observation-rune-frequency-attachment-context-map.yaml",
    "data/historical-route/stage6-observation-rune-frequency-adjacent-doublet-signature.yaml",
    "data/historical-route/stage6-observation-rune-frequency-421-bridge-candidates.yaml",
    "data/historical-route/stage6-observation-rune-frequency-disk-lag5-crosslink.yaml",
    "data/historical-route/stage6-observation-rune-frequency-blake-orc-context.yaml",
    "data/historical-route/stage6-observation-rune-frequency-probe-readiness.yaml",
]

EXPECTED_PROBE_CLASSIFICATION: dict[str, dict[str, Any]] = {
    "lag5_reproduction_probe_candidate_v0": _probe_classification(
        "lag5_copy_null_doublet_diagnostics",
        "stage7_conditional_requires_canonical_transcript_or_boundary",
        source_roots=["third_party/Lag5-phenomenon"],
        source_records=LAG5_SOURCE_RECORDS,
    ),
    "lag5_doublet_suppressed_null_probe_candidate_v0": _probe_classification(
        "lag5_copy_null_doublet_diagnostics",
        "stage7_conditional_requires_canonical_transcript_or_boundary",
        source_roots=["third_party/Lag5-phenomenon"],
        source_records=LAG5_SOURCE_RECORDS,
    ),
    "lag5_page_section_event_overlay_probe_candidate_v0": _probe_classification(
        "lag5_copy_null_doublet_diagnostics",
        "stage7_conditional_requires_canonical_transcript_or_boundary",
        source_roots=["third_party/Lag5-phenomenon"],
        source_records=LAG5_SOURCE_RECORDS,
    ),
    "lag5_token_block_neighborhood_probe_candidate_v0": _probe_classification(
        "lag5_copy_null_doublet_diagnostics",
        "stage7_conditional_requires_canonical_transcript_or_boundary",
        source_roots=["third_party/Lag5-phenomenon"],
        source_records=LAG5_SOURCE_RECORDS + ["data/token-block/stage5eh-token-block-static-context-preservation.yaml"],
    ),
    "lag5_pdd153_56311_route_overlay_probe_candidate_v0": _probe_classification(
        "lag5_copy_null_doublet_diagnostics",
        "stage8_triangle_readiness",
        source_roots=["third_party/Lag5-phenomenon"],
        source_records=LAG5_SOURCE_RECORDS + ["data/historical-route/stage6-stage8-triangle-readiness-handoff.yaml"],
        run_allowed_stage="stage-8",
        triangle_scope_crosslink_only=True,
    ),
    "lag5_page32_route_stream_fingerprint_probe_candidate_v0": _probe_classification(
        "lag5_copy_null_doublet_diagnostics",
        "stage8_triangle_readiness",
        source_roots=["third_party/Lag5-phenomenon"],
        source_records=LAG5_SOURCE_RECORDS + ["data/historical-route/stage6-stage8-triangle-readiness-handoff.yaml"],
        run_allowed_stage="stage-8",
        triangle_scope_crosslink_only=True,
    ),
    "lag5_disk_doublet_suppression_model_constraint_probe_candidate_v0": _probe_classification(
        "lag5_copy_null_doublet_diagnostics",
        "stage7_conditional_requires_reimplementation_metric_definition",
        source_roots=["third_party/Lag5-phenomenon", "third_party/DiskCipherStuff"],
        source_records=LAG5_SOURCE_RECORDS + ["data/project-state/stage6-source-lock-family-census.yaml"],
    ),
    "lag5_negative_space_null_marker_bridge_probe_candidate_v0": _probe_classification(
        "lag5_copy_null_doublet_diagnostics",
        "stage7_conditional_requires_canonical_transcript_or_boundary",
        source_roots=["third_party/Lag5-phenomenon", "third_party/BigGapsFoundInLiberPrimus"],
        source_records=LAG5_SOURCE_RECORDS + ["data/project-state/stage6-source-lock-family-census.yaml"],
    ),
    "outguess_pgp_signature_verification_probe_candidate_v0": _probe_classification(
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "stage7_conditional_requires_toolchain",
        source_roots=["third_party/CiadaSolversIddqd_v2/lp_outguessed"],
        source_records=OUTGUESS_SOURCE_RECORDS,
    ),
    "outguess_00_01_02_xor_reconstruction_probe_candidate_v0": _probe_classification(
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "stage7_conditional_requires_source_and_fixture_boundary",
        source_roots=["third_party/CiadaSolversIddqd_v2/lp_outguessed"],
        source_records=OUTGUESS_SOURCE_RECORDS,
    ),
    "outguess_03_jpeg_extraction_metadata_probe_candidate_v0": _probe_classification(
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "stage7_conditional_requires_toolchain",
        source_roots=["third_party/CiadaSolversIddqd_v2/lp_outguessed"],
        source_records=OUTGUESS_SOURCE_RECORDS,
    ),
    "outguess_03_jpeg_human_transcription_verification_probe_candidate_v0": _probe_classification(
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "stage7_conditional_requires_canonical_source_boundary",
        source_roots=["third_party/CiadaSolversIddqd_v2/lp_outguessed"],
        source_records=OUTGUESS_SOURCE_RECORDS,
    ),
    "xor_txt_29_symbol_alphabet_classification_probe_candidate_v0": _probe_classification(
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "stage7_ready_deterministic_no_toolchain",
        source_roots=["third_party/CiadaSolversIddqd_v2/lp_outguessed"],
        source_records=OUTGUESS_SOURCE_RECORDS,
        source_gap_or_stage6c_precondition="requires xor.txt source boundary if local file remains absent",
    ),
    "outguess_magic_square_route_mask_probe_candidate_v0": _probe_classification(
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "stage7_conditional_requires_source_and_fixture_boundary",
        source_roots=["third_party/CiadaSolversIddqd_v2/lp_outguessed"],
        source_records=OUTGUESS_SOURCE_RECORDS,
    ),
    "byte_strings_outguess_xor_precedent_comparison_probe_candidate_v0": _probe_classification(
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "stage7_ready_deterministic_no_toolchain",
        source_roots=["third_party/CiadaSolversIddqd_v2/byte-strings"],
        source_records=OUTGUESS_SOURCE_RECORDS,
    ),
    "byte_strings_03_control_key_probe_candidate_v0": _probe_classification(
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "stage7_conditional_requires_canonical_source_boundary",
        source_roots=["third_party/CiadaSolversIddqd_v2/byte-strings"],
        source_records=OUTGUESS_SOURCE_RECORDS,
    ),
    "byte_strings_16x16_matrix_route_mask_probe_candidate_v0": _probe_classification(
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "stage7_ready_deterministic_no_toolchain",
        source_roots=["third_party/CiadaSolversIddqd_v2/byte-strings"],
        source_records=OUTGUESS_SOURCE_RECORDS,
    ),
    "byte_strings_token_block_matrix_comparison_probe_candidate_v0": _probe_classification(
        "outguess_pgp_xor_byte_string_detector_diagnostics",
        "stage7_ready_deterministic_no_toolchain",
        source_roots=["third_party/CiadaSolversIddqd_v2/byte-strings"],
        source_records=OUTGUESS_SOURCE_RECORDS + ["data/project-state/stage6-source-lock-family-census.yaml"],
    ),
    "page54_55_red_numbered_line_block_transcript_alignment_probe_candidate_v0": _probe_classification(
        "page54_55_red_number_alignment_readiness",
        "stage7_conditional_requires_canonical_image_or_transcript",
        source_roots=[
            "third_party/CiadaSolversIddqd_v2/liber-primus__images--full",
            "third_party/CiadaSolversIddqd_v2/liber-primus__transcription--master",
        ],
        source_records=PAGE54_SOURCE_RECORDS,
    ),
    "lp_pages_stegdetect_baseline_probe_manifest_v0": _probe_classification(
        "stego_positive_control_toolchain_readiness",
        "stage7_conditional_requires_toolchain_and_canonical_image",
        source_roots=["third_party/CiadaSolversIddqd_v2/liber-primus__images--full", "third_party/StegoPositiveControls"],
        source_records=STEGO_SOURCE_RECORDS,
    ),
    "known_outguessed_pages_stegdetect_comparison_probe_manifest_v0": _probe_classification(
        "stego_positive_control_toolchain_readiness",
        "stage7_conditional_requires_toolchain_and_canonical_image",
        source_roots=["third_party/CiadaSolversIddqd_v2/liber-primus__images--full", "third_party/StegoPositiveControls"],
        source_records=STEGO_SOURCE_RECORDS,
    ),
    "star_artifact_mod8_dct_residue_probe_manifest_v0": _probe_classification(
        "stego_positive_control_toolchain_readiness",
        "stage7_conditional_requires_toolchain_and_canonical_image",
        source_roots=["third_party/StarArtifactsInLPPageImages", "third_party/CiadaSolversIddqd_v2/liber-primus__images--full"],
        source_records=STEGO_SOURCE_RECORDS,
    ),
    "page13_canonical_image_hash_and_detector_reproduction_probe_manifest_v0": _probe_classification(
        "stego_positive_control_toolchain_readiness",
        "stage7_conditional_requires_toolchain_and_canonical_image",
        source_roots=["third_party/CiadaSolversIddqd_v2/liber-primus__images--full", "third_party/StegoPositiveControls"],
        source_records=STEGO_SOURCE_RECORDS,
    ),
    "observation_on_rune_frequency_attachment_context_reconstruction_v0": _probe_classification(
        "adjacent_doublet_frequency_signature_421_fibonacci",
        "stage7_ready_metadata_only",
        source_roots=["third_party/ObservationOnRuneFrequency"],
        source_records=OBSERVATION_SOURCE_RECORDS,
    ),
    "adjacent_doublet_diagonal_vector_reproduction_v0": _probe_classification(
        "adjacent_doublet_frequency_signature_421_fibonacci",
        "stage7_conditional_requires_canonical_transcript_or_boundary",
        source_roots=["third_party/ObservationOnRuneFrequency"],
        source_records=OBSERVATION_SOURCE_RECORDS,
    ),
    "adjacent_doublet_86_89_boundary_reconciliation_v0": _probe_classification(
        "adjacent_doublet_frequency_signature_421_fibonacci",
        "stage7_conditional_requires_canonical_transcript_or_boundary",
        source_roots=["third_party/ObservationOnRuneFrequency"],
        source_records=OBSERVATION_SOURCE_RECORDS,
    ),
    "diagonal_421_delimiter_alphabet_order_control_v0": _probe_classification(
        "adjacent_doublet_frequency_signature_421_fibonacci",
        "stage7_conditional_requires_canonical_transcript_or_boundary",
        source_roots=["third_party/ObservationOnRuneFrequency"],
        source_records=OBSERVATION_SOURCE_RECORDS,
    ),
    "lag1_lag5_joint_copy_null_fingerprint_v0": _probe_classification(
        "adjacent_doublet_frequency_signature_421_fibonacci",
        "stage7_conditional_requires_canonical_transcript_or_boundary",
        source_roots=["third_party/ObservationOnRuneFrequency", "third_party/Lag5-phenomenon"],
        source_records=OBSERVATION_SOURCE_RECORDS + LAG5_SOURCE_RECORDS,
    ),
    "diskcipher_doublet_metric_reimplementation_preflight_v0": _probe_classification(
        "diskcipher_alberti_doublet_56311_readiness",
        "stage7_conditional_requires_reimplementation_metric_definition",
        source_roots=["third_party/ObservationOnRuneFrequency", "third_party/DiskCipherStuff"],
        source_records=[
            "data/historical-route/stage6-observation-rune-frequency-disk-lag5-crosslink.yaml",
            "data/project-state/stage6-source-lock-family-census.yaml",
        ],
    ),
    "doublet_421_numeric_bridge_verification_v0": _probe_classification(
        "adjacent_doublet_frequency_signature_421_fibonacci",
        "stage7_ready_metadata_only",
        source_roots=["third_party/ObservationOnRuneFrequency"],
        source_records=OBSERVATION_SOURCE_RECORDS,
    ),
    "diagonal_421_blake_orc_control_v0": _probe_classification(
        "adjacent_doublet_frequency_signature_421_fibonacci",
        "stage7_conditional_requires_canonical_transcript_or_boundary",
        source_roots=["third_party/ObservationOnRuneFrequency"],
        source_records=OBSERVATION_SOURCE_RECORDS,
    ),
    "diagonal_421_occurrence_index_prime_emirp_probe_v0": _probe_classification(
        "adjacent_doublet_frequency_signature_421_fibonacci",
        "stage7_conditional_requires_canonical_transcript_or_boundary",
        source_roots=["third_party/ObservationOnRuneFrequency"],
        source_records=OBSERVATION_SOURCE_RECORDS,
    ),
    "adjacent_doublet_music_29_note_projection_control_v0": _probe_classification(
        "cicada_music_score_metadata_and_number_diagnostics",
        "stage7_conditional_requires_canonical_score_or_music_metadata",
        source_roots=["third_party/ObservationOnRuneFrequency", "third_party/CicadaMusic", "third_party/CicadaMusic/community-theory"],
        source_records=["data/project-state/stage6-source-lock-family-census.yaml"],
    ),
    "adjacent_doublet_token_block_29_symbol_projection_control_v0": _probe_classification(
        "token_block_static_primary60_matrix_readiness",
        "stage7_ready_deterministic_no_toolchain",
        source_roots=["third_party/ObservationOnRuneFrequency"],
        source_records=["data/project-state/stage6-source-lock-family-census.yaml"],
        source_gap_or_stage6c_precondition="requires Stage 6C to bind finite token-block projection input set",
    ),
}

OBSERVED_DIAGONAL_VECTOR = [
    4,
    2,
    4,
    4,
    2,
    1,
    5,
    6,
    2,
    4,
    2,
    4,
    2,
    1,
    6,
    3,
    2,
    0,
    4,
    2,
    3,
    2,
    4,
    2,
    1,
    7,
    2,
    2,
    3,
]
OBSERVED_COMPACT_STRING = "42442156242421632042324217223"

ROUTE_FINGERPRINTS = [
    "ic_ioc",
    "doublet_rate",
    "doublet_suppression_profile",
    "lag5_d1_d4_fingerprint",
    "bigram_diagonal_or_copy_signature",
    "ngram_repeat_profile",
    "gp_index_mod29_residue_profile",
    "single_rune_anchor_distribution",
    "way_wynn_word52_geometry_preservation",
    "known_lp_cipher_family_resemblance",
    "typo_variant_and_gp_orthography_normalization_profile",
    "wrong_route_and_shuffled_surface_control_delta",
    "adjacent_doublet_diagonal_vector",
    "repeated_421_delimiter_profile",
    "fibonacci_segment_spacing_profile",
    "alphabet_order_sensitivity_profile",
    "lag1_lag5_copy_null_overlap_profile",
    "section_boundary_doublet_delta_profile",
    "prime_emirp_occurrence_index_profile",
]


@dataclass(frozen=True)
class ValidationResult:
    errors: list[str]
    counts: dict[str, Any]

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def validation_error_count(self) -> int:
        return len(self.errors)

    def to_cli_text(self) -> str:
        lines = [
            f"{key}={str(value).lower() if isinstance(value, bool) else value}"
            for key, value in self.counts.items()
        ]
        lines.extend(f"ERROR {error}" for error in self.errors)
        return "\n".join(lines)


def build_stage6() -> dict[str, Any]:
    _ensure_no_protected_output_overlap()
    _write_current_stage_state({})
    _write_doc_staleness_source_of_truth()
    _repair_current_mirror_text()
    source_browser = _source_browser_counts()
    stale_counts = _stale_counts()
    source_roots = _source_root_records()
    observation_inventory = _observation_file_inventory()
    discovery_records = _discovery_probe_records()
    diagnostic_families = _diagnostic_family_records()
    gaps = _reviewability_gaps(source_roots)

    records: dict[str, Any] = {
        "summary": _summary_record(source_roots, diagnostic_families, discovery_records, gaps, source_browser, stale_counts),
        "next_stage_decision": _base_project_record("stage6_next_stage_decision")
        | {
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
            "stage7_direct_route_selected_now": False,
            "stage6b_required_for_final_finite_manifest": True,
        },
        "stage5ei_preservation": _stage5ei_preservation_record(),
        "stage5eh_probe_manifest_preservation": _stage5eh_preservation_record(),
        "third_party_source_root_census": _source_root_census_record(source_roots),
        "source_lock_family_census": _source_lock_family_census_record(),
        "diagnostic_backlog_census": _diagnostic_backlog_census_record(diagnostic_families),
        "stage7_readiness_classification": _stage7_readiness_classification_record(),
        "stage7_candidate_menu": _stage7_candidate_menu_record(),
        "result_bundle_policy": _result_bundle_policy_record(),
        "no_lossy_filtering_policy": _no_lossy_filtering_policy_record(),
        "non_cuda_non_scoring_triage_policy": _non_cuda_non_scoring_policy_record(),
        "post_run_analysis_workflow": _post_run_workflow_record(),
        "deep_research_archive_review_policy": _deep_research_policy_record(),
        "reviewable_validation_evidence": _validation_evidence_record(stale_counts),
        "reviewability_gap_register": _reviewability_gap_record(gaps),
        "source_browser_loadability_summary": _source_browser_record(source_browser),
        "current_stage_transition": _current_stage_transition_record(),
        "chatgpt_context_update_summary": _chatgpt_context_record(),
        "observation_rune_frequency_source_lock_register": _observation_source_lock_record(observation_inventory),
        "observation_rune_frequency_file_inventory": _observation_file_inventory_record(observation_inventory),
        "observation_rune_frequency_attachment_context_map": _attachment_context_map_record(),
        "codex_handoff_policy": _source_record("stage6_codex_handoff_policy")
        | {"completion_summary_path": "codex-output/stage6-codex-completion.md"},
        "credential_redaction_policy_preservation": _source_record("stage6_credential_redaction_policy_preservation")
        | {"secrets_written_now": False, "credential_redaction_policy_preserved": True},
        "raw_source_noncommit_proof": _noncommit_record("stage6_raw_source_noncommit_proof"),
        "third_party_source_noncommit_proof": _noncommit_record("stage6_third_party_source_noncommit_proof"),
        "source_harvester_third_party_source_root_census": _source_harvester_census_record(source_roots),
        "discovery_probe_manifest_registry": _discovery_probe_registry_record(discovery_records),
        "route_fingerprint_taxonomy": _route_fingerprint_taxonomy_record(),
        "null_negative_control_policy": _null_negative_control_policy_record(),
        "bridge_capture_taxonomy": _bridge_capture_taxonomy_record(),
        "keeper_taxonomy": _keeper_taxonomy_record(),
        "stage7_result_bundle_template": _stage7_result_bundle_template_record(),
        "stage7_result_template_registry": _stage7_result_template_registry_record(),
        "stage7_execution_gate_contract": _gate_record("stage6_stage7_execution_gate_contract"),
        "no_active_ingestion_proof": _gate_record("stage6_no_active_ingestion_proof"),
        "no_byte_stream_transition_gate": _gate_record("stage6_no_byte_stream_transition_gate"),
        "no_execution_transition_gate": _gate_record("stage6_no_execution_transition_gate"),
        "observation_rune_frequency_adjacent_doublet_signature": _adjacent_doublet_record(),
        "observation_rune_frequency_421_bridge_candidates": _bridge_421_record(),
        "observation_rune_frequency_disk_lag5_crosslink": _disk_lag5_record(),
        "observation_rune_frequency_blake_orc_context": _blake_orc_record(),
        "observation_rune_frequency_probe_readiness": _observation_probe_readiness_record(),
        "pdd153_triangle_readiness_deferment": _triangle_boundary_record("stage6_pdd153_triangle_readiness_deferment"),
        "triangular_transposition_taxonomy_resolution_plan": _triangle_taxonomy_record(),
        "page32_pdd153_cross_surface_control_policy": _triangle_boundary_record(
            "stage6_page32_pdd153_cross_surface_control_policy"
        ),
        "stage8_triangle_readiness_handoff": _stage8_handoff_record(),
    }
    records["observation_rune_frequency_overlays"] = _overlay_or_deferment_record()

    _write_schemas()
    for key, path in DATA_PATHS.items():
        write_yaml(path, records[key])
    _write_docs(records["summary"])
    _write_current_stage_state(records["summary"])
    _write_operational_file_map()
    _write_stage_summary_record(records["summary"])
    _write_completion_summary(records["summary"])
    return records


def validate_stage6() -> ValidationResult:
    validators = [
        validate_stage6_files_and_schemas,
        validate_stage6_stage5ei_preservation,
        validate_stage6_stage5eh_probe_preservation,
        validate_stage6_source_root_census,
        validate_stage6_source_lock_family_census,
        validate_stage6_diagnostic_backlog_census,
        validate_stage6_discovery_probe_registry,
        validate_stage6_route_fingerprint_taxonomy,
        validate_stage6_null_negative_controls,
        validate_stage6_bridge_capture_taxonomy,
        validate_stage6_keeper_taxonomy,
        validate_stage6_result_bundle_policy,
        validate_stage6_no_lossy_filtering_policy,
        validate_stage6_non_cuda_non_scoring_policy,
        validate_stage6_observation_rune_frequency,
        validate_stage6_stage7_candidate_menu,
        validate_stage6_stage8_triangle_boundary,
        validate_stage6_source_browser_loadability,
        validate_stage6_gate_closure,
        validate_stage6_handoff,
        validate_stage6_protected_local_state,
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for validator in validators:
        result = validator()
        errors.extend(result.errors)
        counts.update(result.counts)
    counts["validation_error_count"] = len(errors)
    return ValidationResult(errors, counts)


def validate_stage6_files_and_schemas() -> ValidationResult:
    errors: list[str] = []
    for key, data_path in DATA_PATHS.items():
        schema_path = SCHEMA_PATHS[key]
        if not data_path.exists():
            errors.append(f"missing data file: {data_path}")
            continue
        if not schema_path.exists():
            errors.append(f"missing schema file: {schema_path}")
            continue
        schema = read_yaml(schema_path)
        payload = read_yaml(data_path)
        Draft202012Validator.check_schema(schema)
        schema_errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda err: err.path)
        errors.extend(f"{data_path}: {error.message}" for error in schema_errors)
    return _result(errors, schema_count=len(SCHEMA_PATHS), data_record_count=len(DATA_PATHS))


def validate_stage6_stage5ei_preservation() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["stage5ei_preservation"])
    errors = []
    if record.get("previous_stage_id") != "stage-5ei":
        errors.append("Stage 5EI preservation does not cite stage-5ei")
    if not record.get("stage5ei_preserved"):
        errors.append("Stage 5EI preservation flag is false")
    return _result(errors, previous_stage_id=record.get("previous_stage_id"))


def validate_stage6_stage5eh_probe_preservation() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["stage5eh_probe_manifest_preservation"])
    registry = read_yaml(TOKEN_BLOCK_PATHS["discovery_probe_manifest_registry"])
    ids = {entry["diagnostic_id"] for entry in registry["diagnostics"]}
    missing = sorted(set(STAGE5EH_PROBE_IDS) - ids)
    errors = []
    if record.get("stage5eh_probe_manifest_count_preserved") != 23:
        errors.append("Stage 5EH preserved probe count is not 23")
    if missing:
        errors.append(f"Stage 5EH probe IDs missing from Stage 6 registry: {missing}")
    return _result(errors, stage5eh_probe_manifest_count_preserved=record.get("stage5eh_probe_manifest_count_preserved"))


def validate_stage6_source_root_census() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["third_party_source_root_census"])
    roots = record["source_roots"]
    errors = []
    root_ids = {root["root_id"] for root in roots}
    expected = {root_id for root_id, *_ in SOURCE_ROOTS}
    if root_ids != expected:
        errors.append("Stage 6 source-root census does not match required root set")
    obs = next(root for root in roots if root["root_id"] == "observation_on_rune_frequency")
    if not obs["present_locally"]:
        errors.append("ObservationOnRuneFrequency should be present locally in this workspace")
    if obs["sha256_tree_digest_if_present"] is None:
        errors.append("ObservationOnRuneFrequency focused tree digest is missing")
    large_bad = [root["root_id"] for root in roots if root["root_id"] in LARGE_ROOT_IDS and root["bounded_inventory_mode"] != "presence_status_only"]
    if large_bad:
        errors.append(f"large roots were not bounded: {large_bad}")
    return _result(errors, source_root_count=len(roots), observation_root_present=obs["present_locally"])


def validate_stage6_source_lock_family_census() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["source_lock_family_census"])
    stages = {entry["stage_id"] for entry in record["source_lock_stage_families"]}
    errors = []
    if set(STAGE_FAMILY_MAP) - stages:
        errors.append("Source-lock family census is missing required stage mappings")
    return _result(errors, source_lock_stage_family_count=len(stages))


def validate_stage6_diagnostic_backlog_census() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["diagnostic_backlog_census"])
    families = record["diagnostic_families"]
    errors = []
    if {item["family_id"] for item in families} != set(DIAGNOSTIC_FAMILIES):
        errors.append("Diagnostic backlog family set is incomplete")
    if not any(item["family_id"] == "adjacent_doublet_frequency_signature_421_fibonacci" for item in families):
        errors.append("Adjacent-doublet diagnostic family missing")
    return _result(errors, diagnostic_family_count=len(families))


def validate_stage6_discovery_probe_registry() -> ValidationResult:
    registry = read_yaml(TOKEN_BLOCK_PATHS["discovery_probe_manifest_registry"])
    diagnostics = registry["diagnostics"]
    by_id = {entry["diagnostic_id"]: entry for entry in diagnostics}
    ids = set(by_id)
    errors = []
    for required in STAGE5EH_PROBE_IDS + OBSERVATION_PROBE_IDS:
        if required not in ids:
            errors.append(f"missing discovery probe ID: {required}")
            continue
        entry = by_id[required]
        expected = EXPECTED_PROBE_CLASSIFICATION[required]
        if entry.get("family_id") != expected["family_id"]:
            errors.append(f"{required} family mismatch: {entry.get('family_id')} != {expected['family_id']}")
        if entry.get("readiness_class") != expected["readiness_class"]:
            errors.append(
                f"{required} readiness mismatch: {entry.get('readiness_class')} != {expected['readiness_class']}"
            )
        if entry.get("run_allowed_stage") != expected["run_allowed_stage"]:
            errors.append(
                f"{required} run stage mismatch: {entry.get('run_allowed_stage')} != {expected['run_allowed_stage']}"
            )
        if not (entry.get("source_records") or entry.get("source_roots") or entry.get("source_gap_or_stage6c_precondition")):
            errors.append(f"{required} lacks source traceability or explicit Stage 6C precondition")
        for action in PROBE_BLOCKED_ACTIONS:
            if action not in entry.get("blocked_actions", []):
                errors.append(f"{required} missing blocked action: {action}")
        if not entry.get("full_output_archive_required_when_run"):
            errors.append(f"{required} does not require full output archive")
        if not entry.get("not_solve_evidence"):
            errors.append(f"{required} is not marked non-solve evidence")
    bad = [
        entry["diagnostic_id"]
        for entry in diagnostics
        if entry.get("stage6_run_now") or entry.get("execution_enabled_now")
    ]
    if bad:
        errors.append(f"Stage 6 probe registry enabled execution: {bad}")
    return _result(errors, discovery_probe_count=len(diagnostics), observation_probe_count=len(OBSERVATION_PROBE_IDS))


def validate_stage6_route_fingerprint_taxonomy() -> ValidationResult:
    record = read_yaml(TOKEN_BLOCK_PATHS["route_fingerprint_taxonomy"])
    ids = set(record["fingerprint_ids"])
    errors = []
    for required in ROUTE_FINGERPRINTS:
        if required not in ids:
            errors.append(f"missing fingerprint: {required}")
    return _result(errors, route_fingerprint_count=len(ids))


def validate_stage6_null_negative_controls() -> ValidationResult:
    record = read_yaml(TOKEN_BLOCK_PATHS["null_negative_control_policy"])
    required = {"wrong source root", "wrong page/section boundary", "doublet-suppressed null", "alphabet reversal", "known outguessed page positive controls", "bulk NumberFacts multiple-comparison controls"}
    controls = {item["control_id"] for item in record["controls"]}
    errors = [f"missing null/negative control: {item}" for item in sorted(required - controls)]
    return _result(errors, null_negative_control_count=len(controls))


def validate_stage6_bridge_capture_taxonomy() -> ValidationResult:
    record = read_yaml(TOKEN_BLOCK_PATHS["bridge_capture_taxonomy"])
    errors = []
    for value in [29, 41, 421, 842, 56311, 12956]:
        if value not in record["number_bridge_watchlist"]:
            errors.append(f"missing bridge watchlist value {value}")
    if not record.get("watchlist_numbers_are_not_proof"):
        errors.append("Bridge watchlist proof guard is false")
    return _result(errors, number_bridge_watchlist_count=len(record["number_bridge_watchlist"]))


def validate_stage6_keeper_taxonomy() -> ValidationResult:
    record = read_yaml(TOKEN_BLOCK_PATHS["keeper_taxonomy"])
    errors = []
    for entry in record["keeper_categories"]:
        forbidden = set(entry["not_allowed_as"])
        if {"solve_claim", "target_selection", "activation_decision"} - forbidden:
            errors.append(f"keeper category lacks forbidden uses: {entry['category_id']}")
    return _result(errors, keeper_category_count=len(record["keeper_categories"]))


def validate_stage6_result_bundle_policy() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["result_bundle_policy"])
    required_false = ["discard_by_score_allowed", "top_n_only_output_allowed", "cuda_triage_allowed", "scoring_triage_allowed", "generated_outputs_committed", "stage6_creates_result_archive_now"]
    errors = []
    for key in required_false:
        if record.get(key) is not False:
            errors.append(f"result bundle policy must keep {key}=false")
    if not record.get("stage7_zip_archive_required"):
        errors.append("Stage 7 ZIP archive requirement missing")
    return _result(errors, result_bundle_policy_created=True)


def validate_stage6_no_lossy_filtering_policy() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["no_lossy_filtering_policy"])
    errors = []
    if not record.get("lossy_filtering_before_archive_forbidden"):
        errors.append("No-lossy-filtering policy does not forbid lossy filtering")
    for key in ["top_n_only_output_allowed", "score_threshold_discard_allowed", "cuda_triage_allowed", "scoring_triage_allowed", "discard_by_score_allowed"]:
        if record.get(key) is not False:
            errors.append(f"no-lossy policy must keep {key}=false")
    return _result(errors, no_lossy_filtering_policy_created=True)


def validate_stage6_non_cuda_non_scoring_policy() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["non_cuda_non_scoring_triage_policy"])
    errors = []
    if record.get("cuda_triage_allowed") is not False or record.get("scoring_triage_allowed") is not False:
        errors.append("non-CUDA/non-scoring policy allows CUDA or scoring triage")
    return _result(errors, non_cuda_non_scoring_policy_created=True)


def validate_stage6_observation_rune_frequency() -> ValidationResult:
    source = read_yaml(SOURCE_HARVESTER_PATHS["observation_rune_frequency_source_lock_register"])
    adjacent = read_yaml(HISTORICAL_ROUTE_PATHS["observation_rune_frequency_adjacent_doublet_signature"])
    context = read_yaml(SOURCE_HARVESTER_PATHS["observation_rune_frequency_attachment_context_map"])
    errors = []
    false_keys = [
        "bigrams_py_executed_now",
        "community_code_executed_now",
        "canonical_bigram_matrix_recomputed_now",
        "canonical_transcript_reproduction_performed_now",
        "image_ocr_performed_now",
        "image_forensics_performed_now",
        "semantic_image_interpretation_performed_now",
    ]
    for key in false_keys:
        if source.get(key) is not False:
            errors.append(f"Observation source lock must keep {key}=false")
    if adjacent.get("observed_diagonal_doublet_vector") != OBSERVED_DIAGONAL_VECTOR:
        errors.append("Observed diagonal vector differs from required archive-observed candidate")
    if adjacent.get("observed_compact_string") != OBSERVED_COMPACT_STRING:
        errors.append("Observed compact string differs from required value")
    if adjacent.get("observed_diagonal_total") != 86:
        errors.append("Observed diagonal total must be 86")
    for attachment in context["attachments"]:
        if attachment.get("filename_is_page_or_subject_claim") is not False:
            errors.append(f"attachment filename treated as subject claim: {attachment.get('file_name')}")
    return _result(errors, observation_source_root_present=source.get("source_root_present"))


def validate_stage6_stage7_candidate_menu() -> ValidationResult:
    menu = read_yaml(PROJECT_STATE_PATHS["stage7_candidate_menu"])
    errors = []
    if not menu["stage7_candidates"]:
        errors.append("Stage 7 candidate menu is empty")
    if menu.get("candidate_menu_status") != "partial_foundation_only":
        errors.append("Stage 7 candidate menu is not marked partial_foundation_only")
    if not menu.get("not_stage7_execution_manifest"):
        errors.append("Stage 7 candidate menu is not marked as non-execution manifest")
    if not menu.get("stage6c_final_menu_required"):
        errors.append("Stage 7 candidate menu does not require Stage 6C finalization")
    if menu.get("stage7_execution_allowed_from_this_menu"):
        errors.append("Stage 7 candidate menu allows execution")
    if menu.get("stage7_zip_archive_creation_allowed_from_this_menu"):
        errors.append("Stage 7 candidate menu allows ZIP archive creation")
    if any(candidate["stage6_run_now"] for candidate in menu["stage7_candidates"]):
        errors.append("Stage 7 candidate menu contains Stage 6 run-now entry")
    for candidate in menu["stage7_candidates"]:
        expected = EXPECTED_PROBE_CLASSIFICATION.get(candidate["candidate_id"])
        if expected is None:
            errors.append(f"unexpected Stage 7 candidate: {candidate['candidate_id']}")
            continue
        if candidate.get("family_id") != expected["family_id"]:
            errors.append(f"Stage 7 menu family mismatch for {candidate['candidate_id']}")
        if candidate.get("readiness_class") != expected["readiness_class"]:
            errors.append(f"Stage 7 menu readiness mismatch for {candidate['candidate_id']}")
    return _result(errors, stage7_candidate_count=len(menu["stage7_candidates"]))


def validate_stage6_stage8_triangle_boundary() -> ValidationResult:
    handoff = read_yaml(HISTORICAL_ROUTE_PATHS["stage8_triangle_readiness_handoff"])
    errors = []
    required_false = ["stage6_triangle_readout_generation_allowed", "stage6_pdd153_route_extraction_allowed", "stage6_page32_route_extraction_allowed"]
    for key in required_false:
        if handoff.get(key) is not False:
            errors.append(f"Stage 8 boundary must keep {key}=false")
    if not handoff.get("stage8_triangle_readiness_deferred") or not handoff.get("stage9_triangle_experiment_deferred"):
        errors.append("Stage 8/9 triangle deferment flags are not true")
    return _result(errors, stage8_boundary_created=True)


def validate_stage6_source_browser_loadability() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    errors = []
    if record.get("source_browser_validation_error_count") != 0:
        errors.append("Source Browser validation errors are nonzero")
    return _result(errors, source_browser_entries_loaded=record.get("source_browser_entries_loaded"))


def validate_stage6_gate_closure() -> ValidationResult:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        payload = read_yaml(path)
        for guard, expected in {**FALSE_GUARDRAILS, **STAGE6_FALSE_GUARDRAILS}.items():
            if guard in payload and payload[guard] is not expected:
                errors.append(f"{path}: {guard} must be {expected}")
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    for key, expected in {**FALSE_GUARDRAILS, **STAGE6_FALSE_GUARDRAILS}.items():
        if summary.get(key) is not expected:
            errors.append(f"summary: {key} must be {expected}")
    return _result(errors, guardrail_record_count=len(DATA_PATHS))


def validate_stage6_handoff() -> ValidationResult:
    record = read_yaml(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if record.get("completion_summary_path") != "codex-output/stage6-codex-completion.md":
        errors.append("Stage 6 completion summary path is incorrect")
    if Path("codex_output").exists():
        errors.append("deprecated codex_output path exists")
    return _result(errors, handoff_path=record.get("completion_summary_path"))


def validate_stage6_protected_local_state() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["reviewable_validation_evidence"])
    errors = []
    protected = record.get("protected_local_paths", [])
    if protected != PROTECTED_LOCAL_PATHS:
        errors.append("Protected local path list was not preserved exactly")
    if record.get("protected_local_paths_staged") is not False:
        errors.append("Protected local path staged flag must be false")
    return _result(errors, protected_local_path_count=len(protected))


def stage6_summary_text() -> str:
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    return "\n".join(
        [
            "LiberPrimus Stage 6 summary:",
            f"status={summary.get('status')}",
            f"stage_id={summary.get('stage_id')}",
            f"previous_stage_id={summary.get('previous_stage_id')}",
            f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
            f"source_root_count={summary.get('source_root_count')}",
            f"diagnostic_family_count={summary.get('diagnostic_family_count')}",
            f"discovery_probe_count={summary.get('discovery_probe_count')}",
            f"stage5eh_probe_manifest_count_preserved={summary.get('stage5eh_probe_manifest_count_preserved')}",
            f"observation_on_rune_frequency_source_root_present={summary.get('observation_on_rune_frequency_source_root_present')}",
            f"observation_on_rune_frequency_stage6_run_now={summary.get('observation_on_rune_frequency_stage6_run_now')}",
            f"stage6_zip_result_bundle_created_now={summary.get('stage6_zip_result_bundle_created_now')}",
            f"source_browser_validation_error_count={summary.get('source_browser_validation_error_count')}",
            f"stale_current_claim_strict_errors_after_stage6={summary.get('stale_current_claim_strict_errors_after_stage6')}",
            f"full_serial_pytest_run={summary.get('full_serial_pytest_run')}",
        ]
    )


def _result(errors: list[str], **counts: Any) -> ValidationResult:
    return ValidationResult(errors=errors, counts=counts)


def _ensure_no_protected_output_overlap() -> None:
    output_paths = {path.as_posix() for path in DATA_PATHS.values()}
    overlaps = sorted(output_paths.intersection(PROTECTED_LOCAL_PATHS))
    if overlaps:
        raise RuntimeError(f"Stage 6 output paths overlap protected local state: {overlaps}")


def _base_record(record_type: str, schema_path: Path) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": schema_path.as_posix(),
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "reviewability_stage": True,
        "source_lock_only": False,
        "source_lock_component_present": True,
        "probe_diagnostic_readiness_stage": True,
        "number_fact_review_batch_stage": False,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        **FALSE_GUARDRAILS,
        **STAGE6_FALSE_GUARDRAILS,
    }


def _base_project_record(record_type: str) -> dict[str, Any]:
    key = record_type.removeprefix("stage6_")
    return _base_record(record_type, SCHEMA_PATHS[key])


def _source_record(record_type: str) -> dict[str, Any]:
    key = record_type.removeprefix("stage6_")
    return _base_record(record_type, SCHEMA_PATHS[key])


def _token_record(record_type: str) -> dict[str, Any]:
    key = record_type.removeprefix("stage6_")
    return _base_record(record_type, SCHEMA_PATHS[key])


def _historical_record(record_type: str) -> dict[str, Any]:
    key = record_type.removeprefix("stage6_")
    return _base_record(record_type, SCHEMA_PATHS[key])


def _summary_record(
    source_roots: list[dict[str, Any]],
    diagnostic_families: list[dict[str, Any]],
    discovery_records: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    source_browser: dict[str, int],
    stale_counts: dict[str, int],
) -> dict[str, Any]:
    return _base_project_record("stage6_summary") | {
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "previous_stage_id": PREVIOUS_STAGE_ID,
        "previous_stage_title": PREVIOUS_STAGE_TITLE,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage5ei_preserved": True,
        "stage5eh_probe_manifest_preserved": True,
        "stage5eh_probe_manifest_count_preserved": 23,
        "stage5ei_route_diagnostic_policy_preserved": True,
        "stage5ei_route_fingerprint_count_preserved": 12,
        "source_root_count": len(source_roots),
        "diagnostic_family_count": len(diagnostic_families),
        "discovery_probe_count": len(discovery_records),
        "observation_probe_count": len(OBSERVATION_PROBE_IDS),
        "reviewability_gap_count": len(gaps),
        "third_party_source_root_census_created": True,
        "source_lock_family_census_created": True,
        "diagnostic_backlog_census_created": True,
        "discovery_probe_manifest_registry_created": True,
        "route_fingerprint_taxonomy_created": True,
        "null_negative_control_policy_created": True,
        "bridge_capture_taxonomy_created": True,
        "keeper_taxonomy_created": True,
        "stage7_result_bundle_policy_created": True,
        "no_lossy_filtering_policy_created": True,
        "non_cuda_non_scoring_triage_policy_created": True,
        "post_run_analysis_workflow_created": True,
        "deep_research_archive_review_policy_created": True,
        "stage8_triangle_boundary_created": True,
        "observation_on_rune_frequency_source_lock_created": True,
        "observation_on_rune_frequency_source_root_present": _obs_root().exists(),
        "observation_on_rune_frequency_stage7_candidate": True,
        "observation_on_rune_frequency_stage6_run_now": False,
        "observation_on_rune_frequency_target_priority_decision_created_now": False,
        "observation_on_rune_frequency_pivot_selected_now": False,
        "observation_on_rune_frequency_route_seed_now": False,
        "observation_on_rune_frequency_accepted_as_proof_now": False,
        "source_browser_entries_loaded": source_browser["source_browser_entries_loaded"],
        "source_browser_validation_error_count": source_browser["source_browser_validation_error_count"],
        "stale_current_claim_strict_errors_after_stage6": stale_counts["stale_current_error_count"],
        "stale_current_claim_warning_count_after_stage6": stale_counts["stale_current_warning_count"],
        "full_parallel_validation_workers": 10,
        "full_parallel_validation_pytest_workers": 10,
        "full_serial_pytest_run": False,
    }


def _stage5ei_preservation_record() -> dict[str, Any]:
    stage5ei_summary = _read_optional_yaml(PROJECT_STATE_DIR / "stage5ei-summary.yaml")
    return _base_project_record("stage6_stage5ei_preservation") | {
        "previous_stage_id": PREVIOUS_STAGE_ID,
        "stage5ei_preserved": True,
        "stage5ei_summary_path": "data/project-state/stage5ei-summary.yaml",
        "stage5ei_route_diagnostic_policy_preserved": True,
        "stage5ei_route_fingerprint_count_preserved": int(stage5ei_summary.get("route_fingerprint_count", 12)),
        "stage5ei_records_rewritten_now": False,
    }


def _stage5eh_preservation_record() -> dict[str, Any]:
    return _base_project_record("stage6_stage5eh_probe_manifest_preservation") | {
        "stage5eh_probe_manifest_path": "data/token-block/stage5eh-diagnostic-probe-manifest-records.yaml",
        "stage5eh_probe_manifest_preserved": True,
        "stage5eh_probe_manifest_count_preserved": 23,
        "stage5eh_probe_ids_preserved": STAGE5EH_PROBE_IDS,
        "stage5eh_records_rewritten_now": False,
    }


def _source_root_records() -> list[dict[str, Any]]:
    records = []
    for root_id, relative_path, default_status, usage in SOURCE_ROOTS:
        path = Path(relative_path)
        present = path.exists()
        bounded_mode = "focused_expected_file_inventory" if root_id == "observation_on_rune_frequency" else "presence_status_only"
        if root_id in LARGE_ROOT_IDS:
            bounded_mode = "presence_status_only"
        file_count = _cheap_file_count(path) if present and root_id == "observation_on_rune_frequency" else None
        records.append(
            {
                "root_id": root_id,
                "relative_path": relative_path,
                "present_locally": present,
                "source_root_status": default_status if present else "absent_source_gap",
                "bounded_inventory_mode": bounded_mode,
                "raw_files_committed": False,
                "raw_source_mutated_now": False,
                "file_count_if_present": file_count,
                "sha256_tree_digest_if_present": _observation_tree_digest() if root_id == "observation_on_rune_frequency" and present else None,
                "primary_theory_families": _families_for_root(root_id),
                "source_lock_records": _source_lock_records_for_root(root_id),
                "canonical_for_future_probes": True if root_id == "observation_on_rune_frequency" else "support_only",
                "used_for_stage7_inputs": usage if present else "deferred",
                "reviewability_gaps": [] if present else [f"{root_id}_source_root_absent"],
            }
        )
    return records


def _source_root_census_record(source_roots: list[dict[str, Any]]) -> dict[str, Any]:
    return _base_project_record("stage6_third_party_source_root_census") | {
        "bounded_census": True,
        "full_recursive_third_party_hashing_performed": False,
        "focused_hashing_limited_to_observation_on_rune_frequency": True,
        "source_roots": source_roots,
        "source_root_count": len(source_roots),
    }


def _source_harvester_census_record(source_roots: list[dict[str, Any]]) -> dict[str, Any]:
    return _source_record("stage6_source_harvester_third_party_source_root_census") | {
        "bounded_census": True,
        "full_recursive_third_party_hashing_performed": False,
        "focused_hashing_limited_to_observation_on_rune_frequency": True,
        "source_roots": source_roots,
        "source_root_count": len(source_roots),
    }


def _source_lock_family_census_record() -> dict[str, Any]:
    return _base_project_record("stage6_source_lock_family_census") | {
        "source_lock_stage_families": [
            {"stage_id": stage_id, "families": families} for stage_id, families in STAGE_FAMILY_MAP.items()
        ],
        "stage_family_count": len(STAGE_FAMILY_MAP),
    }


def _diagnostic_family_records() -> list[dict[str, Any]]:
    records = []
    for family_id in DIAGNOSTIC_FAMILIES:
        readiness = "stage7_ready_deterministic_no_toolchain"
        if "triangle" in family_id or "pdd153" in family_id:
            readiness = "stage8_triangle_readiness"
        if family_id in {"page56_dwh_hash_contract_readiness", "ouroboros_self_reference_symbolic_context"}:
            readiness = "quarantine_background"
        records.append(
            {
                "family_id": family_id,
                "family_label": family_id.replace("_", " "),
                "source_roots": _roots_for_family(family_id),
                "source_lock_records": _records_for_family(family_id),
                "number_fact_overlay_records": _overlays_for_family(family_id),
                "candidate_records": [],
                "third_party_support": [],
                "source_status": "source_locked_metadata",
                "primary_discovery_value": ["number_bridges", "method_constraints", "control_deltas"],
                "readiness_class": readiness,
                "stage7_candidate": readiness.startswith("stage7"),
                "stage8_candidate": readiness == "stage8_triangle_readiness",
                "stage9_candidate": readiness == "stage9_triangle_experiment_deferred",
                "archive_value_class": ["high_discovery_value", "high_bridge_value", "high_control_value"],
                "expected_output_review_mode": ["full_manual_ai_review", "number_bridge_review", "control_delta_review"],
                "blocked_actions": ["solve_claim", "target_selection", "route_stream_generation"],
                "controls_required": ["wrong source root", "wrong page/section boundary", "rune-frequency-preserving shuffle"],
                "stage6_execution_performed": False,
                "solve_claim": False,
            }
        )
    return records


def _diagnostic_backlog_census_record(families: list[dict[str, Any]]) -> dict[str, Any]:
    return _base_project_record("stage6_diagnostic_backlog_census") | {
        "diagnostic_families": families,
        "diagnostic_family_count": len(families),
    }


def _discovery_probe_records() -> list[dict[str, Any]]:
    return [_probe_record(probe_id) for probe_id in STAGE5EH_PROBE_IDS + OBSERVATION_PROBE_IDS]


def stage6_discovery_probe_records_for_validation() -> list[dict[str, Any]]:
    """Return regenerated Stage 6 discovery records without writing files."""

    return _discovery_probe_records()


def expected_probe_classification_for_validation() -> dict[str, dict[str, Any]]:
    """Return the explicit probe classification table used by Stage 6/6B validators."""

    return EXPECTED_PROBE_CLASSIFICATION


def _probe_record(probe_id: str) -> dict[str, Any]:
    classification = EXPECTED_PROBE_CLASSIFICATION[probe_id]
    return {
        "diagnostic_id": probe_id,
        "family_id": classification["family_id"],
        "readiness_class": classification["readiness_class"],
        "source_records": classification["source_records"],
        "source_roots": classification["source_roots"],
        "source_gap_or_stage6c_precondition": classification["source_gap_or_stage6c_precondition"],
        "run_allowed_stage": classification["run_allowed_stage"],
        "triangle_scope_crosslink_only": classification["triangle_scope_crosslink_only"],
        "triangle_execution_deferred_to_stage8_stage9": classification[
            "triangle_execution_deferred_to_stage8_stage9"
        ],
        "stage6_run_now": False,
        "execution_enabled_now": False,
        "finite_input_set_required": True,
        "full_output_archive_required_when_run": True,
        "discovery_objectives": [
            "confirm_or_reject_known_candidate",
            "search_for_number_bridges",
            "compare_against_nulls_and_controls",
        ],
        "preserve_even_if": [
            "not_plaintext",
            "high_entropy",
            "ciphertext_like",
            "control_stream_like",
            "negative_result",
        ],
        "archive_value_class": ["high_discovery_value", "high_bridge_value", "high_control_value"],
        "blocked_actions": PROBE_BLOCKED_ACTIONS,
        "usable_for_decision_now": False,
        "not_solve_evidence": True,
    }


def _discovery_probe_registry_record(records: list[dict[str, Any]]) -> dict[str, Any]:
    return _token_record("stage6_discovery_probe_manifest_registry") | {
        "diagnostics": records,
        "diagnostic_count": len(records),
        "stage5eh_probe_count_preserved": len(STAGE5EH_PROBE_IDS),
        "observation_on_rune_frequency_probe_count": len(OBSERVATION_PROBE_IDS),
        "all_stage6_run_now_false": True,
        "all_execution_enabled_now_false": True,
    }


def _observation_file_inventory() -> list[dict[str, Any]]:
    root = _obs_root()
    expected = [
        "messages.txt",
        "bigrams.py",
        "cover of LP.jpg",
        "6 and 7.png",
        *[f"proper version{i}.png" for i in range(1, 12)],
    ]
    records = []
    for name in expected:
        path = root / name
        records.append(
            {
                "file_name": name,
                "relative_path": path.as_posix(),
                "present": path.exists(),
                "size_bytes": path.stat().st_size if path.exists() else None,
                "sha256": _sha256(path) if path.exists() else None,
                "metadata_only": True,
            }
        )
    return records


def _observation_source_lock_record(inventory: list[dict[str, Any]]) -> dict[str, Any]:
    return _source_record("stage6_observation_rune_frequency_source_lock_register") | {
        "source_root": "third_party/ObservationOnRuneFrequency",
        "source_root_present": _obs_root().exists(),
        "source_status": "community_observation_archive",
        "evidence_status": "operator_assistant_observed_hypothesis",
        "future_probe_required": True,
        "usable_for_decision_now": False,
        "expected_files": [entry["file_name"] for entry in inventory],
        "file_inventory_count": len(inventory),
        "raw_source_files_committed": False,
        "raw_source_files_mutated": False,
        "community_code_executed_now": False,
        "bigrams_py_executed_now": False,
        "canonical_bigram_matrix_recomputed_now": False,
        "canonical_transcript_reproduction_performed_now": False,
        "image_ocr_performed_now": False,
        "image_forensics_performed_now": False,
        "semantic_image_interpretation_performed_now": False,
    }


def _observation_file_inventory_record(inventory: list[dict[str, Any]]) -> dict[str, Any]:
    return _source_record("stage6_observation_rune_frequency_file_inventory") | {
        "source_root": "third_party/ObservationOnRuneFrequency",
        "focused_hashing_only": True,
        "files": inventory,
        "file_count": len(inventory),
        "tree_digest": _observation_tree_digest() if _obs_root().exists() else None,
    }


def _attachment_context_map_record() -> dict[str, Any]:
    return _source_record("stage6_observation_rune_frequency_attachment_context_map") | {
        "archive_id": "observation_on_rune_frequency",
        "source_root": "third_party/ObservationOnRuneFrequency",
        "filename_policy": "filenames_are_preceding_message_context_anchors",
        "filename_is_subject_claim_by_default": False,
        "attachment_context_fields": [
            "file_name",
            "preceding_message_context",
            "inferred_role",
            "filename_is_context_anchor",
            "filename_is_page_or_subject_claim",
            "risk_notes",
        ],
        "attachments": [
            {
                "file_name": "cover of LP.jpg",
                "preceding_message_context": "first ORC / Blake / Urizen observation ending with cover of LP",
                "inferred_role": "annotated_full_heatmap_for_ORC_421_observation",
                "filename_is_context_anchor": True,
                "filename_is_page_or_subject_claim": False,
                "risk_notes": ["not_automatically_lp_cover_image", "visual_semantics_not_reinterpreted_now"],
            },
            {
                "file_name": "6 and 7.png",
                "preceding_message_context": "grouping followed by 4,5,6 and 7",
                "inferred_role": "annotated_diagonal_segmentation_image_for_421_and_4567_claim",
                "filename_is_context_anchor": True,
                "filename_is_page_or_subject_claim": False,
                "risk_notes": [
                    "not_automatically_pages_6_and_7",
                    "section_boundaries_require_future_canonical_rebuild",
                ],
            },
            {
                "file_name_pattern": "proper version*.png",
                "preceding_message_context": "proper-version heatmap batch from community script output",
                "inferred_role": "per_section_or_per_chapter_heatmap_batch",
                "filename_is_context_anchor": True,
                "filename_is_page_or_subject_claim": False,
                "risk_notes": [
                    "proper_version_sequence_not_canonical_section_mapping",
                    "community_grouping_reported_incorrect",
                    "canonical_section_boundary_rebuild_required",
                ],
            },
        ],
    }


def _adjacent_doublet_record() -> dict[str, Any]:
    return _historical_record("stage6_observation_rune_frequency_adjacent_doublet_signature") | {
        "archive_id": "observation_on_rune_frequency",
        "source_root": "third_party/ObservationOnRuneFrequency",
        "source_status": "community_observation_archive",
        "evidence_status": "operator_assistant_observed_hypothesis",
        "future_probe_required": True,
        "usable_for_decision_now": False,
        "accepted_as_route_now": False,
        "accepted_as_cipher_mechanism_now": False,
        "stage6_recomputed_from_canonical_transcript_now": False,
        "stage6_runs_bigrams_py_now": False,
        "observed_diagonal_doublet_vector": OBSERVED_DIAGONAL_VECTOR,
        "observed_compact_string": OBSERVED_COMPACT_STRING,
        "observed_diagonal_total": sum(OBSERVED_DIAGONAL_VECTOR),
        "repeated_delimiter_candidate": "421",
        "delimiter_rune_triples": ["ORC", "J/EO/P", "OE/D/A"],
        "pre_delimiter_segment_lengths": [3, 5, 8],
        "observed_segment_headers": [4, 5, 6, 7],
        "diskcipher_reconciliation_target": {
            "archive_observed_total": 86,
            "prior_diskcipher_observed_total": 89,
        },
        "primary_status": "future_reproduction_required",
        "risk_notes": [
            "community_observation_not_project_reproduction",
            "alphabet_order_sensitivity_must_be_tested",
            "canonical_transcript_required",
            "no_route_seed",
            "no_solve_claim",
        ],
    }


def _bridge_421_record() -> dict[str, Any]:
    return _historical_record("stage6_observation_rune_frequency_421_bridge_candidates") | {
        "archive_id": "observation_on_rune_frequency",
        "primary_number": 421,
        "candidate_facts": [
            {"claim_id": "421_is_prime", "expression": "421 is prime", "verification_status": "arithmetic_verified_metadata_only"},
            {"claim_id": "421_prime_index_82", "expression": "prime_index_one_based(421) = 82", "verification_status": "arithmetic_verified_metadata_only"},
            {"claim_id": "82_equals_2_times_41", "expression": "82 = 2 * 41", "verification_status": "arithmetic_verified_metadata_only"},
            {"claim_id": "842_equals_2_times_421", "expression": "842 = 2 * 421", "verification_status": "arithmetic_verified_metadata_only"},
            {"claim_id": "842_equals_29_squared_plus_1", "expression": "842 = 29^2 + 1", "verification_status": "arithmetic_verified_metadata_only"},
        ],
        "number_bridge_not_proof": True,
        "future_probe_required": True,
    }


def _disk_lag5_record() -> dict[str, Any]:
    return _historical_record("stage6_observation_rune_frequency_disk_lag5_crosslink") | {
        "archive_id": "observation_on_rune_frequency",
        "adjacent_doublet_vector_sum": 86,
        "stage5ed_diskcipher_observed_doublet_claim": 89,
        "stage5ed_diskcipher_expected_doublet_claim": 448,
        "diskcipher_observed_minus_adjacent_vector_sum": 3,
        "stage5eh_lag5_n_claimed": 12956,
        "stage5eh_lag5_m_sum_claimed": 479,
        "stage5eh_lag5_d_counts_claimed": [29, 15, 14, 28, 19, 15],
        "stage5eh_lag5_d1_d4_sum_claimed": 57,
        "future_probe_ids": [
            "adjacent_doublet_diagonal_vector_reproduction_v0",
            "adjacent_doublet_86_89_boundary_reconciliation_v0",
            "lag1_lag5_joint_copy_null_fingerprint_v0",
            "diskcipher_doublet_metric_reimplementation_preflight_v0",
        ],
        "risk_notes": ["metric_definition_required", "canonical_corpus_required", "boundary_policy_required"],
    }


def _blake_orc_record() -> dict[str, Any]:
    return _historical_record("stage6_observation_rune_frequency_blake_orc_context") | {
        "archive_id": "observation_on_rune_frequency",
        "primary_observation": "first_421_delimiter_rune_triple_spells_ORC_under_latin_labels",
        "rune_triple": ["O", "R", "C"],
        "counts": [4, 2, 1],
        "message_context_mentions_blake_orc_urizen": True,
        "keeper_category": "theme_bridge",
        "stage7_probe_candidate": "diagonal_421_blake_orc_control_v0",
        "risk_notes": ["thematic_link_only", "requires_control_against_all_other_diagonal_trigrams"],
    }


def _observation_probe_readiness_record() -> dict[str, Any]:
    return _historical_record("stage6_observation_rune_frequency_probe_readiness") | {
        "archive_id": "observation_on_rune_frequency",
        "probe_ids": OBSERVATION_PROBE_IDS,
        "probe_count": len(OBSERVATION_PROBE_IDS),
        "all_stage6_run_now_false": True,
        "all_execution_enabled_now_false": True,
        "future_probe_required": True,
    }


def _stage7_readiness_classification_record() -> dict[str, Any]:
    classifications = [
        {
            "candidate_id": probe_id,
            "family_id": classification["family_id"],
            "readiness_class": classification["readiness_class"],
            "reason": "explicit Stage 6B repaired probe classification",
            "source_gap_or_stage6c_precondition": classification["source_gap_or_stage6c_precondition"],
            "blocked_actions": PROBE_BLOCKED_ACTIONS,
        }
        for probe_id, classification in EXPECTED_PROBE_CLASSIFICATION.items()
    ]
    classifications.append(
        {
            "candidate_id": "pdd153_triangular_transposition_readouts",
            "family_id": "pdd153_page32_triangle_readiness",
            "readiness_class": "stage8_triangle_readiness",
            "reason": "triangle-specific execution scope deferred",
            "blocked_actions": ["route_stream_generation", "solve_claim", "target_selection"],
        }
    )
    return _base_project_record("stage6_stage7_readiness_classification") | {
        "readiness_classes": READINESS_CLASSES,
        "classifications": classifications,
    }


def _stage7_candidate_menu_record() -> dict[str, Any]:
    candidates = [
        {
            "candidate_id": probe_id,
            "family_id": EXPECTED_PROBE_CLASSIFICATION[probe_id]["family_id"],
            "readiness_class": EXPECTED_PROBE_CLASSIFICATION[probe_id]["readiness_class"],
            "source_gap_or_stage6c_precondition": EXPECTED_PROBE_CLASSIFICATION[probe_id][
                "source_gap_or_stage6c_precondition"
            ],
            "stage6_run_now": False,
            "execution_enabled_now": False,
            "result_bundle_policy_required": True,
            "controls_required": ["alphabet order controls", "canonical boundary controls"],
            "not_solve_evidence": True,
        }
        for probe_id in OBSERVATION_PROBE_IDS
    ]
    return _base_project_record("stage6_stage7_candidate_menu") | {
        "candidate_menu_status": "partial_foundation_only",
        "stage7_candidate_menu_scope": "observation_on_rune_frequency_only",
        "not_stage7_execution_manifest": True,
        "stage6c_final_menu_required": True,
        "stage7_execution_allowed_from_this_menu": False,
        "stage7_zip_archive_creation_allowed_from_this_menu": False,
        "stage7_candidates": candidates,
        "candidate_count": len(candidates),
        "stage6b_finalization_required": True,
    }


def _result_bundle_policy_record() -> dict[str, Any]:
    return _base_project_record("stage6_result_bundle_policy") | {
        "stage7_zip_archive_required": True,
        "all_bounded_outputs_preserved": True,
        "lossy_filtering_before_archive_forbidden": True,
        "discard_by_score_allowed": False,
        "top_n_only_output_allowed": False,
        "cuda_triage_allowed": False,
        "scoring_triage_allowed": False,
        "generated_outputs_committed": False,
        "full_outputs_local_or_attached_only": True,
        "compact_committed_result_summaries_allowed": True,
        "assistant_archive_analysis_required": True,
        "deep_research_second_pass_recommended": True,
        "stage6_creates_result_archive_now": False,
        "stage7_earliest_archive_creation_stage": True,
        "preferred_ignored_local_stage7_output_path": "experiments/results/stage7-probe-results/<timestamp>/stage7-probe-results.zip",
    }


def _no_lossy_filtering_policy_record() -> dict[str, Any]:
    return _base_project_record("stage6_no_lossy_filtering_policy") | {
        "lossy_filtering_before_archive_forbidden": True,
        "discard_unranked_outputs_before_archive": False,
        "top_n_only_output_allowed": False,
        "score_threshold_discard_allowed": False,
        "cuda_triage_allowed": False,
        "scoring_triage_allowed": False,
        "discard_by_score_allowed": False,
        "full_result_bundle_required": True,
        "post_run_interpretive_review_required": True,
        "assistant_archive_analysis_required_before_deep_research": True,
        "deep_research_archive_review_recommended": True,
        "metrics_are_descriptive_fingerprints_not_final_filters": True,
        "if_expected_output_too_large": [
            "split_probe_into_smaller_finite_batches",
            "reduce_scope_before_execution",
            "archive_batchwise",
            "record_omitted_scope_explicitly",
            "do_not_discard_by_score",
        ],
    }


def _non_cuda_non_scoring_policy_record() -> dict[str, Any]:
    return _base_project_record("stage6_non_cuda_non_scoring_triage_policy") | {
        "cuda_triage_allowed": False,
        "scoring_triage_allowed": False,
        "discard_by_score_allowed": False,
        "metrics_are_descriptive_fingerprints_not_final_filters": True,
    }


def _post_run_workflow_record() -> dict[str, Any]:
    return _base_project_record("stage6_post_run_analysis_workflow") | {
        "stage7_runs_bounded_probes_and_creates_zip": True,
        "operator_uploads_zip_to_assistant_after_stage7": True,
        "assistant_interpretive_archive_review_required": True,
        "assistant_outputs_expected": [
            "assistant-stage7-archive-analysis.md",
            "candidate-bridges.yaml",
            "number-pattern-index.yaml",
            "theme-method-bridge-index.yaml",
            "control-delta-findings.yaml",
            "negative-results-worth-keeping.yaml",
            "followup-probe-candidates.yaml",
            "stage8-triangle-relevance-notes.yaml",
        ],
    }


def _deep_research_policy_record() -> dict[str, Any]:
    return _base_project_record("stage6_deep_research_archive_review_policy") | {
        "deep_research_reviews_zip_and_assistant_analysis_after_assistant": True,
        "codex_integrates_review_outcome_later_as_compact_metadata": True,
        "edits_allowed_in_review_policy_now": False,
    }


def _route_fingerprint_taxonomy_record() -> dict[str, Any]:
    return _token_record("stage6_route_fingerprint_taxonomy") | {
        "plaintext_likeness_required_for_route_interest": False,
        "english_readability_required_for_route_interest": False,
        "high_entropy_output_can_be_interesting": True,
        "ciphertext_like_output_can_be_interesting": True,
        "key_like_output_can_be_interesting": True,
        "control_stream_like_output_can_be_interesting": True,
        "byte_like_output_can_be_interesting": True,
        "null_copy_mask_like_output_can_be_interesting": True,
        "intermediate_surface_output_can_be_interesting": True,
        "intentional_typo_and_orthography_noise_warning": True,
        "gp_orthography_normalization_required_before_language_judgment": True,
        "fingerprint_ids": ROUTE_FINGERPRINTS,
    }


def _null_negative_control_policy_record() -> dict[str, Any]:
    controls = [
        "wrong source root",
        "wrong page image variant",
        "wrong transcript boundary",
        "wrong page/section boundary",
        "wrong PDD center",
        "wrong word52",
        "wrong triangle size",
        "shuffled 153-word surface",
        "unrelated 153-word section",
        "doublet-suppressed null",
        "rune-frequency-preserving shuffle",
        "Markov first-order rune controls",
        "alphabet reversal",
        "alphabet cyclic rotations",
        "alternate rune order controls",
        "sorted-by-frequency order control",
        "all diagonal trigrams control",
        "known outguessed page positive controls",
        "known non-outguessed page negative controls",
        "randomized DiskCipher candidate controls",
        "randomized music beat/measure controls",
        "bulk NumberFacts multiple-comparison controls",
        "image-layout artifact controls",
        "source-author claim vs arithmetic-verified distinction",
        "attachment-filename subject-claim control",
    ]
    return _token_record("stage6_null_negative_control_policy") | {
        "controls": [
            {
                "control_id": control,
                "applies_to_families": DIAGNOSTIC_FAMILIES,
                "required_before_stage7": True,
                "required_before_stage8": "triangle" in control or "PDD" in control,
                "required_before_stage9": "triangle" in control or "PDD" in control,
            }
            for control in controls
        ]
    }


def _bridge_capture_taxonomy_record() -> dict[str, Any]:
    return _token_record("stage6_bridge_capture_taxonomy") | {
        "number_bridge_watchlist": [
            29,
            41,
            52,
            57,
            82,
            86,
            89,
            137,
            153,
            167,
            205,
            401,
            409,
            421,
            412,
            463,
            479,
            529,
            547,
            761,
            842,
            841,
            1033,
            1229,
            1259,
            1433,
            2472,
            3299,
            3301,
            3368,
            56311,
            12956,
        ],
        "watchlist_numbers_are_not_proof": True,
        "watchlist_numbers_do_not_authorize_execution": True,
        "watchlist_numbers_require_source_and_controls": True,
        "theme_families": [
            "way_road_path_direction",
            "wynn_way_ruth_root_route",
            "circle_circumference_spiral_mobius",
            "music_canon_retrograde_inversion",
            "negative_space_gap_null_copy",
            "self_reference_loop_ouroboros_quine",
            "magic_square_matrix_table",
            "pgp_signed_surface",
            "byte_string_surface",
            "triangle_t17_pdd153",
            "blake_orc_urizen_los",
            "doublet_copy_null_delimiter",
        ],
        "method_families": [
            "adjacent_bigram_heatmap",
            "lagged_equality_marker",
            "doublet_suppression_metric",
            "triangular_transposition",
            "fibonacci_prime_index_route",
            "matrix_magic_square_route",
            "music_canon_table_projection",
            "token_block_primary60_projection",
            "signed_surface_verification",
            "stego_positive_control",
            "source_root_crosswalk",
        ],
    }


def _keeper_taxonomy_record() -> dict[str, Any]:
    categories = [
        "direct_reproduction_of_source_locked_fact",
        "control_delta_signal",
        "number_bridge",
        "theme_bridge",
        "method_bridge",
        "source_validation_or_source_gap",
        "negative_control_discriminator",
        "unexpected_surface_resemblance",
        "route_fingerprint_preservation",
        "route_fingerprint_destruction",
        "quarantine_but_preserve",
        "probably_noise_but_documented",
    ]
    return _token_record("stage6_keeper_taxonomy") | {
        "keeper_categories": [
            {
                "category_id": category,
                "not_allowed_as": [
                    "solve_claim",
                    "target_selection",
                    "activation_decision",
                    "execution_seed_without_later_stage",
                    "byte_generation_authorization",
                ],
            }
            for category in categories
        ]
    }


def _stage7_result_bundle_template_record() -> dict[str, Any]:
    return _token_record("stage6_stage7_result_bundle_template") | {
        "template_id": "stage7_probe_result_bundle_layout_v0",
        "zip_layout_template_path": "docs/templates/stage7-probe-result-bundle-layout.md",
        "stage6_creates_result_archive_now": False,
        "required_top_level_entries": [
            "README.md",
            "bundle-manifest.yaml",
            "bundle-hashes.yaml",
            "environment/",
            "source-context/",
            "probes/",
            "controls/",
            "cross-probe-indexes/",
            "generated-review-material/",
            "bundle-closeout.yaml",
        ],
    }


def _stage7_result_template_registry_record() -> dict[str, Any]:
    return _token_record("stage6_stage7_result_template_registry") | {
        "templates": [
            "docs/templates/stage7-probe-result-bundle-layout.md",
            "docs/templates/stage7-assistant-archive-analysis-template.md",
            "docs/templates/stage7-deep-research-archive-review-prompt-template.md",
        ],
        "result_archive_created_now": False,
    }


def _gate_record(record_type: str) -> dict[str, Any]:
    return _token_record(record_type) | {
        "gate_closed": True,
        "execution_enabled_now": False,
        "stage6_run_now": False,
        "requires_later_explicit_authorization": True,
    }


def _triangle_boundary_record(record_type: str) -> dict[str, Any]:
    return _historical_record(record_type) | {
        "stage6_triangle_readiness_inventory_allowed": True,
        "stage6_triangle_readout_generation_allowed": False,
        "stage6_pdd153_route_extraction_allowed": False,
        "stage6_page32_route_extraction_allowed": False,
        "stage8_triangle_readiness_deferred": True,
        "stage9_triangle_experiment_deferred": True,
    }


def _triangle_taxonomy_record() -> dict[str, Any]:
    return _triangle_boundary_record("stage6_triangular_transposition_taxonomy_resolution_plan") | {
        "operator_supplied_claim_22_distinct_triangular_transpositions": True,
        "claim_22_distinct_transpositions_verified_now": False,
        "natural_triangular_readout_family_count_observed_by_assistant": 24,
        "transposition_count_taxonomy_ambiguous": True,
        "taxonomy_resolution_deferred_to_stage8": True,
    }


def _stage8_handoff_record() -> dict[str, Any]:
    return _triangle_boundary_record("stage6_stage8_triangle_readiness_handoff") | {
        "stage8_required_inputs": [
            "pdd153_t17_geometry_candidate_set_v0",
            "pdd153_triangular_transposition_taxonomy",
            "pdd153_pascal_fibonacci_diagonal_context",
            "pdd153_bottom_row_page32_quarantine_bridge",
            "stage6_route_fingerprint_taxonomy",
            "stage6_null_negative_control_policy",
            "stage7_diagnostic_results_if_available",
            "observation_on_rune_frequency_adjacent_doublet_signature_if_validated_by_stage7",
        ],
        "stage8_execution_allowed": False,
        "stage9_earliest_triangle_execution": True,
    }


def _overlay_or_deferment_record() -> dict[str, Any]:
    overlays = [
        {
            "overlay_id": f"stage6_obsfreq_{idx:02d}_{name}",
            "source_record_path": source,
            "fact_class": "stage6_observation_rune_frequency_review_fact",
            "display_label": label,
            "value": value,
            "usable_for_decision_now": False,
            "not_allowed_as": ["proof", "route_seed", "execution_seed", "solve_claim"],
            "verification_status": "archive_observed_future_probe_required",
            "risk_notes": ["community_observation_archive", "no_execution", "no_solve_claim"],
        }
        for idx, (name, source, label, value) in enumerate(
            [
                ("diagonal_vector", HISTORICAL_ROUTE_PATHS["observation_rune_frequency_adjacent_doublet_signature"].as_posix(), "Adjacent-doublet vector 29 counts / sum 86", 86),
                ("421_delimiters", HISTORICAL_ROUTE_PATHS["observation_rune_frequency_adjacent_doublet_signature"].as_posix(), "Three 421 delimiter candidates: ORC / J-EO-P / OE-D-A", 421),
                ("86_89_bridge", HISTORICAL_ROUTE_PATHS["observation_rune_frequency_disk_lag5_crosslink"].as_posix(), "Doublet total 86 vs DiskCipher 89", 3),
                ("lag5_bridge", HISTORICAL_ROUTE_PATHS["observation_rune_frequency_disk_lag5_crosslink"].as_posix(), "Lag1/Lag5 copy-null bridge", 12956),
                ("filename_policy", SOURCE_HARVESTER_PATHS["observation_rune_frequency_attachment_context_map"].as_posix(), "Filenames are Discord context anchors", 2),
            ],
            start=1,
        )
    ]
    return _base_record("stage6_observation_rune_frequency_overlay_collection", SCHEMA_PATHS["observation_rune_frequency_overlays"]) | {
        "review_batch_id": "stage6_observation_rune_frequency_review_only",
        "review_batch_selection_policy": "diagnostic_backlog_source_root_review_not_number_fact_batch",
        "overlay_count": len(overlays),
        "usable_for_decision_now": False,
        "overlays": overlays,
        "overlay_schema_fit": "existing_convention_clean",
    }


def _validation_evidence_record(stale_counts: dict[str, int]) -> dict[str, Any]:
    return _base_project_record("stage6_reviewable_validation_evidence") | {
        "baseline_validation_commands": [
            "token-block validate-stage5ei",
            "token-block stage5ei-summary",
            "consistency audit-stale-current-claims --strict",
            "source-browser validate-index",
            "source-browser validate-paths",
        ],
        "stage6_validation_commands": [
            "token-block build-stage6",
            "token-block validate-stage6",
            "token-block stage6-summary",
            "pytest -q tests/python/test_stage6_*.py",
            "ruff check python/libreprimus tests/python",
            "scripts/ci/run-stage-validation.ps1 -Stage stage6 -Profile full-parallel -Workers 10 -PytestWorkers 10",
        ],
        "stale_current_claim_strict_errors_after_stage6": stale_counts["stale_current_error_count"],
        "protected_local_paths": PROTECTED_LOCAL_PATHS,
        "protected_local_paths_staged": False,
        "full_parallel_workers": 10,
        "full_parallel_pytest_workers": 10,
        "full_serial_pytest_run": False,
    }


def _reviewability_gaps(source_roots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gaps = []
    for root in source_roots:
        for gap in root["reviewability_gaps"]:
            gaps.append({"gap_id": gap, "gap_type": "source_root_absent", "source_root": root["relative_path"]})
    gaps.append(
        {
            "gap_id": "stage6b-final-finite-stage7-manifest-required",
            "gap_type": "stage6b_followup",
            "reason": "Stage 6 creates census and policy foundation; final finite Stage 7 manifest remains routed to Stage 6B.",
        }
    )
    return gaps


def _reviewability_gap_record(gaps: list[dict[str, Any]]) -> dict[str, Any]:
    return _base_project_record("stage6_reviewability_gap_register") | {
        "reviewability_gaps": gaps,
        "reviewability_gap_count": len(gaps),
    }


def _source_browser_record(source_browser: dict[str, int]) -> dict[str, Any]:
    return _base_project_record("stage6_source_browser_loadability_summary") | source_browser


def _current_stage_transition_record() -> dict[str, Any]:
    return _base_project_record("stage6_current_stage_transition") | {
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "latest_completed_stage_id": STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "current_stage_state_updated_to_stage6": True,
    }


def _chatgpt_context_record() -> dict[str, Any]:
    return _base_project_record("stage6_chatgpt_context_update_summary") | {
        "current_stage_context_mentions_stage6": True,
        "recommended_next_stage_mentions_stage6b": True,
        "broad_doc_churn_avoided": True,
    }


def _noncommit_record(record_type: str) -> dict[str, Any]:
    return _source_record(record_type) | {
        "raw_source_files_committed": False,
        "raw_third_party_files_committed": False,
        "generated_outputs_committed": False,
        "codex_output_deprecated_path_used": False,
        "protected_local_paths_staged": False,
    }


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_schema_for(key), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _schema_for(key: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"type": "string"},
        "schema": {"type": "string"},
        "stage_id": {"const": STAGE_ID},
        "stage_title": {"const": STAGE_TITLE},
        "metadata_only": {"const": True},
        "puzzle_execution_allowed": {"const": False},
        "solve_claim": {"const": False},
        "generated_outputs_committed": {"const": False},
        "raw_source_files_committed": {"const": False},
        "raw_third_party_files_committed": {"const": False},
        "route_stream_generated_now": {"const": False},
        "real_byte_stream_generated": {"const": False},
        "cuda_execution_performed": {"const": False},
        "scoring_performed": {"const": False},
        "benchmark_performed": {"const": False},
        "stage6_probe_execution_performed_now": {"const": False},
        "stage6_zip_result_bundle_created_now": {"const": False},
    }
    if key == "summary":
        properties.update(
            {
                "latest_completed_stage_id": {"not": {}},
                "status": {"const": "complete"},
                "stage5eh_probe_manifest_count_preserved": {"const": 23},
                "recommended_next_stage_id": {"const": NEXT_STAGE_ID},
                "observation_on_rune_frequency_stage6_run_now": {"const": False},
            }
        )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://liberprimus-gpu.local/schemas/stage6/{key}",
        "type": "object",
        "required": ["record_type", "schema", "stage_id", "stage_title", "metadata_only", "puzzle_execution_allowed", "solve_claim"],
        "properties": properties,
        "additionalProperties": True,
    }


def _write_docs(summary: dict[str, Any]) -> None:
    _repair_current_mirror_text()
    _upsert_marked_section(Path("AGENTS.md"), STAGE_TOKEN, _agents_section())
    _upsert_marked_section(Path("ChatGPT-ContextFile.md"), STAGE_TOKEN, _chatgpt_section())
    _upsert_marked_section(Path("STATUS.md"), STAGE_TOKEN, _status_section())
    _upsert_marked_section(Path("README.md"), STAGE_TOKEN, _readme_section())
    _upsert_marked_section(Path("ROADMAP.md"), STAGE_TOKEN, _roadmap_section())
    _upsert_marked_section(Path("TESTING.md"), STAGE_TOKEN, _testing_section())
    _upsert_marked_section(Path("docs/roadmap/staged-plan.md"), STAGE_TOKEN, _staged_plan_section())
    _upsert_marked_section(Path("docs/onboarding/start-here.md"), STAGE_TOKEN, _onboarding_section())
    _upsert_marked_section(Path("docs/onboarding/source-of-truth-map.md"), STAGE_TOKEN, _source_truth_section())
    _upsert_marked_section(Path("docs/onboarding/operational-file-map.md"), STAGE_TOKEN, _operational_map_doc_section())
    _upsert_marked_section(Path("docs/reference/token-block-cli.md"), STAGE_TOKEN, _cli_doc_section())
    _write_text(EXPERIMENT_DOC_PATH, _experiment_doc(summary))
    _write_text(Path("docs/templates/stage7-probe-result-bundle-layout.md"), _bundle_layout_template())
    _write_text(Path("docs/templates/stage7-assistant-archive-analysis-template.md"), _assistant_template())
    _write_text(Path("docs/templates/stage7-deep-research-archive-review-prompt-template.md"), _deep_research_template())
    _write_text(DEV_LOG_PATH, _dev_log(summary))
    _write_text(RESEARCH_LOG_PATH, _research_log(summary))


def _repair_current_mirror_text() -> None:
    previous_title = PREVIOUS_STAGE_TITLE
    prior_stage6_title = "Stage 6 - Probe and diagnostic readiness, without execution"
    replacements_by_path = {
        Path("AGENTS.md"): {
            f"Current completed stage: {previous_title}.": f"Current completed stage: {STAGE_TITLE}.",
            f"Current work: {prior_stage6_title}.": f"Current work: {NEXT_STAGE_TITLE}.",
        },
        Path("ChatGPT-ContextFile.md"): {
            "## Stage 5EI Current Boundary": "## Stage 6 Current Boundary",
            f"Latest completed stage: {previous_title}.": f"Latest completed stage: {STAGE_TITLE}.",
            f"Current planning focus: {prior_stage6_title}.": f"Current planning focus: {NEXT_STAGE_TITLE}.",
        },
        Path("README.md"): {
            f"Current completed stage: {previous_title}.": f"Current completed stage: {STAGE_TITLE}.",
            f"Current next prompt: {prior_stage6_title}.": f"Current next prompt: {NEXT_STAGE_TITLE}.",
        },
        Path("ROADMAP.md"): {
            f"Current completed stage: {previous_title}.": f"Current completed stage: {STAGE_TITLE}.",
            f"Next: {prior_stage6_title}.": f"Next: {NEXT_STAGE_TITLE}.",
        },
        Path("STATUS.md"): {
            f"- Latest completed stage: {previous_title}.": f"- Latest completed stage: {STAGE_TITLE}.",
            f"- Current next stage: {prior_stage6_title}.": f"- Current next stage: {NEXT_STAGE_TITLE}.",
            f"- Next recommended prompt: {prior_stage6_title}.": f"- Next recommended prompt: {NEXT_STAGE_TITLE}.",
        },
        Path("docs/onboarding/start-here.md"): {
            "## Stage 5EI Current Boundary": "## Stage 6 Current Boundary",
        },
        Path("docs/roadmap/staged-plan.md"): {
            f"- Latest completed stage: {previous_title}.": f"- Latest completed stage: {STAGE_TITLE}.",
            f"- Current planning focus: {prior_stage6_title}.": f"- Current planning focus: {NEXT_STAGE_TITLE}.",
            f"{previous_title} is the latest completed stage.": f"{STAGE_TITLE} is the latest completed stage.",
            f"Current planning focus: {prior_stage6_title}.": f"Current planning focus: {NEXT_STAGE_TITLE}.",
        },
    }
    for path, replacements in replacements_by_path.items():
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def _write_current_stage_state(summary: dict[str, Any]) -> None:
    payload = read_yaml(CURRENT_STAGE_STATE_PATH)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "stage_title": STAGE_TITLE,
            "prompt_type": PROMPT_TYPE,
            "metadata_only": True,
            "source_lock_only": False,
            "source_lock_component_present": True,
            "probe_diagnostic_readiness_stage": True,
            "puzzle_execution_allowed": False,
            "solve_claim": False,
            "status": "complete",
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "previous_completed_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
            "latest_completed_stage": {
                "stage_id": STAGE_ID,
                "stage_title": STAGE_TITLE,
                "completed_commit": "",
                "completed_date": "2026-06-14",
                "status": "complete",
            },
            "next_stage": {
                "stage_id": NEXT_STAGE_ID,
                "stage_title": NEXT_STAGE_TITLE,
                "prompt_type": NEXT_PROMPT_TYPE,
            },
            "post_push_handoff_locations": [
                "codex-output/stage6-codex-completion.md",
                "GitHub issue comment",
            ],
            "diagnostic_execution_performed_now": False,
            "route_extraction_performed_now": False,
            "route_stream_generated_now": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "stego_tool_execution_performed": False,
            "ocr_performed": False,
            "image_forensics_performed": False,
            "audio_stego_performed": False,
            "cuda_execution_performed": False,
            "scoring_performed": False,
            "benchmark_performed": False,
            "target_priority_decision_created_now": False,
            "pivot_target_selected_now": False,
        }
    )
    payload.update(FALSE_GUARDRAILS)
    payload.update(STAGE6_FALSE_GUARDRAILS)
    write_yaml(CURRENT_STAGE_STATE_PATH, payload)


def _write_doc_staleness_source_of_truth() -> None:
    payload = read_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "latest_completed_stage_after_this_stage": STAGE_TITLE,
            "latest_completed_stage_prefix": "Stage 6",
            "next_stage_after_this_stage": NEXT_STAGE_TITLE,
            "expected_next_stage_prefix": "Stage 6B",
            "latest_previous_stage": PREVIOUS_STAGE_TITLE,
            "expected_latest_after_stage5ah": STAGE_TITLE,
            "expected_next_after_stage5ah": NEXT_STAGE_TITLE,
            "latest_completed_stage_id": STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "stage6_current_truth_refresh": True,
            "current_stage_state_authoritative": True,
            "human_readable_docs_are_mirrors_only": True,
        }
    )
    write_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH, payload)


def _write_operational_file_map() -> None:
    payload = read_yaml(OPERATIONAL_FILE_MAP_PATH)
    payload["stage6_summary_record"] = PROJECT_STATE_PATHS["summary"].as_posix()
    payload["stage6_diagnostic_backlog_census"] = PROJECT_STATE_PATHS["diagnostic_backlog_census"].as_posix()
    payload["stage6_discovery_probe_manifest_registry"] = TOKEN_BLOCK_PATHS["discovery_probe_manifest_registry"].as_posix()
    payload["stage6_observation_rune_frequency_source_lock_register"] = SOURCE_HARVESTER_PATHS[
        "observation_rune_frequency_source_lock_register"
    ].as_posix()
    write_yaml(OPERATIONAL_FILE_MAP_PATH, payload)


def _write_stage_summary_record(summary: dict[str, Any]) -> None:
    payload = read_yaml(STAGE_SUMMARY_RECORDS_PATH)
    entry = {
        "record_type": "stage_summary_record",
        "stage_id": STAGE_ID,
        "title": STAGE_TITLE,
        "status": "complete",
        "category": "metadata_diagnostic_readiness",
        "summary": (
            "Completed metadata-only diagnostic backlog readiness with a bounded source-root census, "
            "future-only discovery probes, no-lossy Stage 7 archive policy, and Stage 8/9 triangle boundaries."
        ),
        "key_outputs": [
            f"Bounded source-root census records: {summary['source_root_count']}.",
            f"Diagnostic families represented: {summary['diagnostic_family_count']}.",
            f"Future discovery probes declared with execution disabled: {summary['discovery_probe_count']}.",
            "ObservationOnRuneFrequency recorded as archive-observed future-probe context only.",
            "Stage 7 archive policy forbids lossy filtering, score discard, top-N-only retention, CUDA triage, and scoring triage.",
            f"Recommended next stage: {NEXT_STAGE_ID}.",
        ],
        "result_status": "metadata_readiness_complete",
        "solve_claim": False,
        "cuda_used": False,
        "raw_outputs_committed": False,
        "generated_outputs_committed": False,
        "notes": (
            "No probes, ZIP archive, Stage 7 outputs, raw third-party commits, generated-output commits, "
            "bigrams.py execution, OCR/image/stego/PGP/OutGuess/F5/StegDetect/CUDA/scoring/benchmarks, "
            "target selection, canonical-corpus activation, page-boundary finalisation, or solve claim."
        ),
        "summary_path": PROJECT_STATE_PATHS["summary"].as_posix(),
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "source_root_count": summary["source_root_count"],
        "diagnostic_family_count": summary["diagnostic_family_count"],
        "discovery_probe_count": summary["discovery_probe_count"],
    }
    if isinstance(payload, list):
        payload = [item for item in payload if not (isinstance(item, dict) and item.get("stage_id") == STAGE_ID)]
        payload.append(entry)
    elif isinstance(payload, dict):
        records = payload.setdefault("records", [])
        records[:] = [item for item in records if not (isinstance(item, dict) and item.get("stage_id") == STAGE_ID)]
        records.append(entry)
    write_yaml(STAGE_SUMMARY_RECORDS_PATH, payload)


def _write_completion_summary(summary: dict[str, Any]) -> None:
    text = f"""# Stage 6 Codex Completion

- stage: {STAGE_TITLE}
- starting commit: b69282192f45e74ea72a3c335f52c450adc07a2c
- final commit: recorded after commit
- origin/main commit: recorded after push
- issue: recorded after GitHub issue update
- CI: recorded after GitHub Actions completes
- no probes were run: true
- no ZIP archive was created: true
- no Stage 7 outputs were generated: true
- no raw third-party files were committed: true
- no generated outputs were committed: true
- bigrams.py was not executed: true
- ObservationOnRuneFrequency status: archive-observed future-probe context only
- recommended next stage: {NEXT_STAGE_TITLE}
- source roots in bounded census: {summary['source_root_count']}
- diagnostic families: {summary['diagnostic_family_count']}
- discovery probes: {summary['discovery_probe_count']}
- protected local YAML modifications were not staged or changed by Stage 6: to be verified at closeout
- untracked generated outputs were left ignored and untouched: true
"""
    _write_text(CODEX_OUTPUT_DIR / "stage6-codex-completion.md", text)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _upsert_marked_section(path: Path, token: str, body: str) -> None:
    start = f"<!-- {token}:start -->"
    end = f"<!-- {token}:end -->"
    section = f"{start}\n{body.rstrip()}\n{end}\n"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if start in text and end in text:
        before = text.split(start, 1)[0]
        after = text.split(end, 1)[1]
        path.write_text(before + section + after.lstrip("\n"), encoding="utf-8")
    else:
        path.write_text(text.rstrip() + "\n\n" + section, encoding="utf-8")


def _agents_section() -> str:
    return f"""## Stage 6 Current Boundary

Current completed stage: {STAGE_TITLE}.

Current work: {NEXT_STAGE_TITLE}. Stage 6 is diagnostic-backlog and archive-policy metadata only. It records bounded source-root census, future discovery probes, no-lossy Stage 7 archive policy, and Stage 8/9 triangle boundaries. It does not execute probes, generate route or byte streams, run OCR/image/stego/PGP/OutGuess/F5/StegDetect/CUDA/scoring/benchmarks, select targets, activate the canonical corpus, finalize page boundaries, or claim a solve.
"""


def _chatgpt_section() -> str:
    return f"""## Stage 6 Current Boundary

Latest completed stage: {STAGE_TITLE}.

Current planning focus: {NEXT_STAGE_TITLE}.

Stage 6 created the diagnostic backlog census and Stage 7 archive-policy foundation without execution. ObservationOnRuneFrequency is recorded as archive-observed future-probe context only, not canonical transcript truth.
"""


def _status_section() -> str:
    return f"""## Stage 6 Status

- Latest completed stage: {STAGE_TITLE}.
- Current next stage: {NEXT_STAGE_TITLE}.
- Stage 6 preserves Stage 5EI and Stage 5EH, records a bounded source-root census, maps diagnostic families, adds future-only discovery probes, and defines Stage 7 result-bundle policy.
- No probes ran, no ZIP result archive was created, and no raw third-party or generated outputs are committed.
"""


def _readme_section() -> str:
    return """## Stage 6 Readiness Snapshot

Stage 6 is complete as metadata-only diagnostic readiness. The project now has a bounded source-root census, diagnostic-backlog census, future discovery-probe registry, bridge/keeper taxonomies, no-lossy Stage 7 archive policy, and Stage 8/9 triangle boundaries. The next routed stage is Stage 6B, not execution.
"""


def _roadmap_section() -> str:
    return """## Stage 6 Roadmap Update

Stage 6 completed the diagnostic backlog readiness foundation without execution. Stage 6B should finalize the finite Stage 7 probe manifest and archive-run contract. Stage 7 remains the earliest bounded diagnostic execution stage after Stage 6B, Stage 8 remains triangle readiness, and Stage 9 remains earliest bounded triangle experiments.
"""


def _testing_section() -> str:
    return """## Stage 6 Validation Policy

Stage 6 uses focused validators first, then stale-current scanner strict mode, Source Browser validation, focused Stage 6 pytest files, ruff, stage-fast, local-fast, and one full-parallel run with Workers=10 and PytestWorkers=10. Full serial pytest remains opt-in only and is not required for normal closeout.
"""


def _staged_plan_section() -> str:
    return f"""## Stage 6 - Diagnostic Backlog Readiness

{STAGE_TITLE} is the latest completed stage. It is metadata-only and creates a bounded source-root census, diagnostic-backlog census, discovery-probe registry, bridge/keeper taxonomy, no-lossy Stage 7 archive policy, and Stage 8/9 triangle boundary handoff.

Next: {NEXT_STAGE_TITLE}.
"""


def _onboarding_section() -> str:
    return f"""## Stage 6 Current Boundary

Use `data/project-state/current-stage-state.yaml` as the authoritative latest/next-stage truth. It records {STAGE_TITLE} as complete and {NEXT_STAGE_TITLE} as next. Stage 6 did not run diagnostics or publish generated outputs.
"""


def _source_truth_section() -> str:
    return f"""## Stage 6 Source-Of-Truth Update

- Latest completed stage: {STAGE_TITLE}.
- Next routed stage: {NEXT_STAGE_TITLE}.
- Stage 6 records ObservationOnRuneFrequency as community-observation archive context only; canonical transcript reproduction is future Stage 7 work.
"""


def _operational_map_doc_section() -> str:
    return """## Stage 6 Operational Map Update

Stage 6 records live under `data/project-state/stage6-*`, `data/source-harvester/stage6-*`, `data/token-block/stage6-*`, and `data/historical-route/stage6-*`. Generated completion handoff remains ignored under `codex-output/stage6-codex-completion.md`.
"""


def _cli_doc_section() -> str:
    return """## Stage 6 Token-Block Commands

Stage 6 token-block commands: `build-stage6`, `validate-stage6`, `stage6-summary`, and focused validators for preservation, source-root census, source-lock family census, diagnostic backlog, discovery probes, route fingerprints, controls, bridge/keeper taxonomy, result-bundle policy, no-lossy filtering, non-CUDA/non-scoring policy, ObservationOnRuneFrequency, Stage 7 menu, Stage 8 triangle boundary, Source Browser loadability, gate closure, and handoff.
"""


def _experiment_doc(summary: dict[str, Any]) -> str:
    return f"""# Stage 6 Diagnostic Backlog Readiness

Stage 6 is a metadata-only readiness foundation. It creates a bounded source-root census across {summary['source_root_count']} roots, maps {summary['diagnostic_family_count']} diagnostic families, and records {summary['discovery_probe_count']} future discovery probes with execution disabled.

ObservationOnRuneFrequency is recorded as archive-observed future-probe context only. `bigrams.py` was not executed and canonical transcript reproduction remains future work.
"""


def _bundle_layout_template() -> str:
    return """# Stage 7 Probe Result Bundle Layout

Future Stage 7 ZIP archives must preserve all bounded outputs before interpretation. Required top-level entries: `README.md`, `bundle-manifest.yaml`, `bundle-hashes.yaml`, `environment/`, `source-context/`, `probes/`, `controls/`, `cross-probe-indexes/`, `generated-review-material/`, and `bundle-closeout.yaml`.

Do not discard by score, use top-N-only retention, or commit generated result archives.
"""


def _assistant_template() -> str:
    return """# Stage 7 Assistant Archive Analysis Template

Review the complete archive for number bridges, theme bridges, method bridges, control deltas, negative results worth keeping, source-validation gaps, and follow-up probes. Do not claim a solve or treat readable English as the only interesting output.
"""


def _deep_research_template() -> str:
    return """# Stage 7 Deep Research Archive Review Prompt Template

Review the Stage 7 archive and assistant analysis as evidence-indexed research material. Do not edit files, run probes, discard outputs by score, or claim a solve.
"""


def _dev_log(summary: dict[str, Any]) -> str:
    return f"""# Stage 6 Development Log

Implemented Stage 6 diagnostic backlog readiness metadata. Source roots: {summary['source_root_count']}; diagnostic families: {summary['diagnostic_family_count']}; future probes: {summary['discovery_probe_count']}. Guardrails remain closed.
"""


def _research_log(summary: dict[str, Any]) -> str:
    return f"""# Stage 6 Next-Stage Decision Summary

Stage 6 recommends {NEXT_STAGE_ID}: {NEXT_STAGE_TITLE}. Stage 6 is a foundation/census stage and does not directly authorize Stage 7 execution.
"""


def _source_browser_counts() -> dict[str, int]:
    index = build_source_index()
    result = validate_source_index()
    return {
        "source_browser_entries_loaded": len(index.entries),
        "source_browser_records_scanned": len(index.scanned_paths),
        "source_browser_validation_error_count": len(result.errors),
    }


def _stale_counts() -> dict[str, int]:
    report = audit_repository()
    return {
        "stale_current_error_count": report.error_count,
        "stale_current_warning_count": report.warning_count,
    }


def _read_optional_yaml(path: Path) -> dict[str, Any]:
    if path.exists():
        data = read_yaml(path)
        if isinstance(data, dict):
            return data
    return {}


def _obs_root() -> Path:
    return Path("third_party/ObservationOnRuneFrequency")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _observation_tree_digest() -> str | None:
    root = _obs_root()
    if not root.exists():
        return None
    digest = hashlib.sha256()
    for item in sorted(path for path in root.iterdir() if path.is_file()):
        digest.update(item.name.encode("utf-8"))
        digest.update(_sha256(item).encode("ascii"))
    return digest.hexdigest()


def _cheap_file_count(path: Path) -> int | None:
    if not path.exists():
        return None
    return sum(1 for item in path.iterdir() if item.is_file())


def _families_for_root(root_id: str) -> list[str]:
    mapping = {
        "observation_on_rune_frequency": ["adjacent_doublet_frequency_signature_421_fibonacci"],
        "lag5_phenomenon": ["lag5_copy_null_doublet_diagnostics"],
        "diskcipher_stuff": ["diskcipher_alberti_doublet_56311_readiness"],
        "cicada_music": ["cicada_music_score_metadata_and_number_diagnostics"],
        "ciada_solvers_iddqd_v2": ["iddqd_v2_canonical_source_root_readiness"],
    }
    return mapping.get(root_id, ["source_validation"])


def _source_lock_records_for_root(root_id: str) -> list[str]:
    if root_id == "observation_on_rune_frequency":
        return [SOURCE_HARVESTER_PATHS["observation_rune_frequency_source_lock_register"].as_posix()]
    return []


def _roots_for_family(family_id: str) -> list[str]:
    roots = []
    for root_id, relative_path, *_ in SOURCE_ROOTS:
        if family_id in _families_for_root(root_id):
            roots.append(relative_path)
    return roots


def _records_for_family(family_id: str) -> list[str]:
    if family_id == "adjacent_doublet_frequency_signature_421_fibonacci":
        return [
            HISTORICAL_ROUTE_PATHS["observation_rune_frequency_adjacent_doublet_signature"].as_posix(),
            HISTORICAL_ROUTE_PATHS["observation_rune_frequency_421_bridge_candidates"].as_posix(),
        ]
    return []


def _overlays_for_family(family_id: str) -> list[str]:
    if family_id == "adjacent_doublet_frequency_signature_421_fibonacci":
        return [OPERATOR_PATHS["observation_rune_frequency_overlays"].as_posix()]
    return []
