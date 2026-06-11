"""Stage 5ED number-fact review batch 004 overlays.

This stage is reviewability metadata only. It adds Source Browser
NumberFactCard overlays for a selected disk/visual-method/route-context
batch, preserves Stage 5EB validation policy, and does not mutate historical
source-lock records or authorize execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.number_facts import (
    load_enrichment_overlays,
    normalize_entry_number_facts,
)
from libreprimus.operator_console.source_browser.validators import (
    path_canonicalization_report,
    source_browser_summary,
    validate_path_canonicalization,
    validate_source_index,
)
from libreprimus.token_block.models import read_yaml, write_json, write_yaml

STAGE_ID = "stage-5ed"
STAGE_TOKEN = "stage5ed"
STAGE_TITLE = (
    "Stage 5ED - Source-lock number-fact review batch 004, disk / visual-method / "
    "route-context enrichment overlays, without execution"
)
PROMPT_TYPE = "assistant_or_operator_review_then_codex_overlay_update"
PREVIOUS_STAGE_ID = "stage-5ec"
PREVIOUS_STAGE_FINAL_COMMIT = "584692e1303b80b75bd759dc79cd69a31bd5f83a"
PREVIOUS_STAGE_ISSUE = 164
PREVIOUS_STAGE_CI_RUN = 27354396743
PREVIOUS_STAGE_CI_STATUS = "passed"
NEXT_STAGE_ID = "stage-5ee"
NEXT_STAGE_TITLE = "Stage 5EE - Source-lock number-fact review batch 005, without execution"
REVIEW_BATCH_ID = "number_fact_review_batch_004_disk_visual_method"
REVIEW_BATCH_SELECTION_POLICY = "assistant_operator_disk_visual_method_route_context_batch"
EXPECTED_REVIEWED_ENTRY_COUNT = 20
EXPECTED_OVERLAY_COUNT = 25
PARALLEL_WORKER_CAP = 10
LOCAL_PARALLEL_DEFAULT_WORKERS = 10
LOCAL_PARALLEL_DEFAULT_PYTEST_WORKERS = 10

PROJECT_STATE_DIR = Path("data/project-state")
TOKEN_BLOCK_DIR = Path("data/token-block")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
SOURCE_BROWSER_DIR = Path("data/operator-console/source-browser")
RESEARCH_DIR = Path("data/research")
CODEX_OUTPUT_DIR = Path("codex-output")
CHATGPT_CONTEXT_PATH = Path("ChatGPT-ContextFile.md")
STAGE_SUMMARY_RECORDS_PATH = RESEARCH_DIR / "stage-summary-records-v0.yaml"
OPERATIONAL_FILE_MAP_PATH = PROJECT_STATE_DIR / "operational-file-map.yaml"
DOC_STALENESS_SOURCE_OF_TRUTH_PATH = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"

OVERLAY_COLLECTION_PATH = SOURCE_BROWSER_DIR / (
    "number-fact-overlays/stage5ed-review-batch-004-disk-visual-method-overlays.yaml"
)
REVIEW_BATCH_RESULT_PATH = SOURCE_BROWSER_DIR / (
    "number-fact-review-batches/stage5ed-review-batch-004-disk-visual-method-result.yaml"
)

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5ed-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5ed-next-stage-decision.yaml",
    "review_batch_selection": PROJECT_STATE_DIR / "stage5ed-review-batch-selection.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5ed-reviewable-validation-evidence.yaml",
    "scope_control": PROJECT_STATE_DIR / "stage5ed-scope-control.yaml",
    "source_browser_loadability": PROJECT_STATE_DIR / "stage5ed-source-browser-loadability-summary.yaml",
    "stage5ec_preservation": PROJECT_STATE_DIR / "stage5ed-stage5ec-preservation.yaml",
    "stage5eb_preservation": PROJECT_STATE_DIR / "stage5ed-stage5eb-preservation.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage5ed-chatgpt-context-update-summary.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5ed-reviewability-gap-register.yaml",
    "current_stage_state": PROJECT_STATE_DIR / "current-stage-state.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "token_stage5eb_preservation": TOKEN_BLOCK_DIR / "stage5ed-stage5eb-preservation.yaml",
    "stage5dx_preservation": TOKEN_BLOCK_DIR / "stage5ed-stage5dx-preservation.yaml",
    "stage5dw_preservation": TOKEN_BLOCK_DIR / "stage5ed-stage5dw-preservation.yaml",
    "stage5dv_preservation": TOKEN_BLOCK_DIR / "stage5ed-stage5dv-preservation.yaml",
    "stage5du_preservation": TOKEN_BLOCK_DIR / "stage5ed-stage5du-preservation.yaml",
    "stage5dg_preservation": TOKEN_BLOCK_DIR / "stage5ed-stage5dg-preservation.yaml",
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5ed-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5ed-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5ed-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR / "stage5ed-no-byte-stream-transition-proof.yaml",
    "no_execution_transition_proof": TOKEN_BLOCK_DIR / "stage5ed-no-execution-transition-proof.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5ed-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5ed-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5ed-raw-source-noncommit-proof.yaml",
}

DATA_PATHS: dict[str, Path] = {
    **PROJECT_STATE_PATHS,
    "review_batch_result": REVIEW_BATCH_RESULT_PATH,
    **TOKEN_PATHS,
    **SOURCE_HARVESTER_PATHS,
}

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5ed-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5ed-next-stage-decision-v0.schema.json"),
    "review_batch_selection": Path("schemas/project-state/stage5ed-review-batch-selection-v0.schema.json"),
    "reviewable_validation_evidence": Path(
        "schemas/project-state/stage5ed-reviewable-validation-evidence-v0.schema.json"
    ),
    "source_browser_loadability": Path("schemas/project-state/stage5ed-source-browser-loadability-summary-v0.schema.json"),
    "scope_control": Path("schemas/project-state/stage5ed-scope-control-v0.schema.json"),
    "chatgpt_context_update_summary": Path(
        "schemas/project-state/stage5ed-chatgpt-context-update-summary-v0.schema.json"
    ),
    "review_batch_result": Path(
        "schemas/operator-console/stage5ed-source-browser-number-fact-review-batch-result-v0.schema.json"
    ),
    "overlay_collection": Path(
        "schemas/operator-console/stage5ed-source-browser-number-fact-overlay-collection-v0.schema.json"
    ),
}

SCHEMA_BY_DATA_KEY: dict[str, str] = {
    "summary": "summary",
    "next_stage_decision": "next_stage_decision",
    "review_batch_selection": "review_batch_selection",
    "reviewable_validation_evidence": "reviewable_validation_evidence",
    "source_browser_loadability": "source_browser_loadability",
    "scope_control": "scope_control",
    "chatgpt_context_update_summary": "chatgpt_context_update_summary",
    "review_batch_result": "review_batch_result",
}

SELECTED_SOURCE_RECORD_PATHS = [
    "data/historical-route/stage5dn-disk-alberti-branch-cipher-candidate-v1.yaml",
    "data/historical-route/stage5dn-disk-p39-row1-math-semantic-cluster-v1.yaml",
    "data/historical-route/stage5dn-disk-rule4-mobius-trip-rotation-bridge-v0.yaml",
    "data/historical-route/stage5dn-disk-doublet-suppression-candidate-v1.yaml",
    "data/historical-route/stage5dn-disk-ruth-root-route-way-wordplay-candidate-v0.yaml",
    "data/historical-route/stage5dn-disk-2015-eclipse-167-temporal-candidate-v0.yaml",
    "data/historical-route/stage5dn-pdd-153-triangle-56311-wynn-way-route-v1.yaml",
    "data/historical-route/stage5dn-solved-i-voice-of-circumference-precedent-v0.yaml",
    "data/historical-route/stage5dn-circumference-single-i-spiral-anchor-crosslink-v0.yaml",
    "data/historical-route/stage5dn-disk-probability-claim-quarantine-v1.yaml",
    "data/historical-route/stage5dm-blake-visual-text-source-family.yaml",
    "data/historical-route/stage5dm-lp-sacred-book-edition-overlay-index.yaml",
    "data/historical-route/stage5dm-solved-magic-square-word-sum-precedent.yaml",
    "data/historical-route/stage5dm-full-lp-page-visual-motif-index.yaml",
    "data/historical-route/stage5dm-lp-doublet-scarcity-feature-candidate.yaml",
    "data/historical-route/stage5di-2016-message-route-meta-clue.yaml",
    "data/historical-route/stage5di-page32-tree-polar-route-candidate.yaml",
    "data/historical-route/stage5dk-page56-dwh-hash-contract.yaml",
    "data/historical-route/stage5di-dinkus-visual-delimiter-candidate.yaml",
    "data/historical-route/stage5di-magic-square-matrix-route-context.yaml",
]

FALSE_FLAGS = {
    "activation_authorized_now",
    "activation_decision_valid_now",
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "active_token_block_manifest_changed",
    "alberti_cipher_execution_performed_now",
    "magic_square_transform_performed_now",
    "new_source_lock_evidence_added_now",
    "page_boundaries_finalized",
    "alberti_html_executed_now",
    "audio_stego_performed",
    "benchmark_performed",
    "branch_enumeration_performed",
    "byte_stream_generation_authorized_now",
    "canonical_corpus_active",
    "combined_approval_gate_satisfied_now",
    "community_code_executed_now",
    "cuda_execution_performed",
    "decode_attempt_performed",
    "decryption_attempt_performed_now",
    "direct_music_substitution_executed",
    "disk_cipher_execution_performed_now",
    "dwh_hash_search_performed",
    "execution_authorized_now",
    "execution_performed",
    "full_cartesian_product_enumerated",
    "generated_outputs_committed",
    "hash_preimage_search_performed",
    "hidden_content_image_forensics_performed",
    "historical_source_lock_records_rewritten",
    "html_tool_executed_now",
    "image_forensics_performed",
    "known_plaintext_attack_performed_now",
    "machine_code_execution_performed_now",
    "mayfly_route_extraction_performed_now",
    "midi_route_extraction_performed_now",
    "mp3stego_execution_performed",
    "music_route_extraction_performed_now",
    "native_code_execution_performed_now",
    "network_target_validation_performed_now",
    "number_fact_backfill_performed_now",
    "ocr_performed",
    "openpuff_execution_performed",
    "operator_readiness_decision_created_now",
    "page0_plaintext_accepted_now",
    "page32_route_extraction_performed_now",
    "page56_hash_preimage_tested_now",
    "page_boundaries_final",
    "pdf_ocr_or_hidden_content_rendering_performed",
    "pivot_target_selected_now",
    "probability_claim_accepted_as_validated",
    "raw_source_files_committed",
    "raw_source_files_mutated_by_gui",
    "raw_third_party_files_committed",
    "real_byte_stream_generated",
    "red_heading_decryption_accepted_now",
    "route_extraction_performed_now",
    "route_stream_generated_now",
    "scoring_performed",
    "semantic_image_interpretation_performed",
    "solve_claim",
    "source_lock_evidence_updated_now",
    "spectrogram_stego_performed",
    "spreadsheet_macro_execution_performed",
    "target_class_validation_implemented",
    "target_priority_decision_created_now",
    "token_block_experiment_executed",
    "token_block_variant_byte_streams_generated",
    "tor_network_access_performed",
    "triangle_route_extraction_performed_now",
    "variant_byte_streams_generated",
    "variant_materialisation_performed",
    "vm_bytecode_execution_performed_now",
    "website_expansion_performed",
}

OVERLAY_REQUIRED_NOT_ALLOWED = ["proof", "route_seed", "execution_seed", "solve_claim"]

STAGE5ED_OVERLAY_YAML = r"""
- overlay_id: stage5ed_disk_alberti_model_components_overlay
  source_record_path: data/historical-route/stage5dn-disk-alberti-branch-cipher-candidate-v1.yaml
  source_fact_id: disk_alberti_model_components
  fact_class: disk_cipher_number_facts
  display_label: DiskCipher candidate has 8 claimed model components including four-rule codebook and 56311
  short_label: 'Disk model: 8 components; 56311'
  value: 8
  values:
  - 8
  - 4
  - 5
  - 6
  - 3
  - 11
  value_type: sequence
  operation_type: source_observation
  expression: Source-lock lists 8 model components; includes four_rule_codebook and sequence_56311.
  relation: Preserves the model surface without executing Alberti branches.
  why_stored: Helps reviewers see that DiskCipher is a many-component candidate and not a single arithmetic fact.
  verification_status: source_author_claim
  display_priority: medium
  source_paths:
  - data/historical-route/stage5dn-disk-alberti-branch-cipher-candidate-v1.yaml
  crosslinks:
  - disk_alberti_branch_cipher_candidate_v1
  - disk_56311_wynn_way_bridge_v1
  risk_notes:
  - high_degrees_of_freedom_warning
  - model_not_validated
  - no_html_execution
- overlay_id: stage5ed_disk_p39_row1_term_count_overlay
  source_record_path: data/historical-route/stage5dn-disk-p39-row1-math-semantic-cluster-v1.yaml
  source_fact_id: disk_p39_row1_claimed_term_count
  fact_class: disk_cipher_number_facts
  display_label: Disk p39 row-1 cluster claims 10 terms including EULER, TOTIENT, CIRCUMFERENCE, FISH, WYNN, and PHI
  short_label: Disk p39 row1 = 10 claimed terms
  value: 10
  values:
  - 10
  value_type: sequence
  operation_type: source_observation
  expression: Claimed terms are EULER, LEONHARD, NAPIER, JOHN, TOTIENT, CIRCUMFERENCE, PRIME_NUMBER, FISH, WYNN, PHI.
  relation: Dense source-author semantic cluster linking DiskCipher to known LP math/geometry vocabulary.
  why_stored: This is one of the strongest DiskCipher review hooks, but remains candidate-only.
  verification_status: source_author_claim
  display_priority: high
  source_paths:
  - data/historical-route/stage5dn-disk-p39-row1-math-semantic-cluster-v1.yaml
  crosslinks:
  - disk_alberti_branch_cipher_candidate_v1
  - pdd_153_triangle_word_prime_route_v1
  - solved_i_voice_of_circumference_precedent_v0
  risk_notes:
  - terms_claimed_by_source_author
  - independent_reimplementation_required
  - negative_controls_required
  - accepted_plaintext_false
- overlay_id: stage5ed_disk_p39_row1_lp_relevance_overlay
  source_record_path: data/historical-route/stage5dn-disk-p39-row1-math-semantic-cluster-v1.yaml
  source_fact_id: disk_p39_row1_lp_relevance_cluster
  fact_class: disk_cipher_number_facts
  display_label: 'Disk p39 row-1 cluster links to 5 LP relevance families: prime/totient, circumference, fish/153, WYNN/41,
    and PHI geometry'
  short_label: Disk p39 row1 -> 5 LP relevance links
  value: 5
  values:
  - 5
  - 153
  - 41
  value_type: sequence
  operation_type: source_observation
  expression: Source-lock relevance list includes prime/totient solved wisdom, circumference solved koan, fish/153 triangle,
    WYNN/center41, and PHI geometry.
  relation: Crosswalks the row-1 semantic cluster into the current triangle/Page32/music evidence graph.
  why_stored: Prevents the term cluster from appearing as isolated vocabulary.
  verification_status: operator_assistant_observed
  display_priority: medium
  source_paths:
  - data/historical-route/stage5dn-disk-p39-row1-math-semantic-cluster-v1.yaml
  crosslinks:
  - pdd_153_triangle_word_prime_route_v1
  - page32_moebius_fibonacci_prime_index_spiral_v1
  - music_3301_instar_crab_canon_v0
  risk_notes:
  - semantic_context_not_proof
  - candidate_only
- overlay_id: stage5ed_disk_rule4_mobius_rotation_terms_overlay
  source_record_path: data/historical-route/stage5dn-disk-rule4-mobius-trip-rotation-bridge-v0.yaml
  source_fact_id: disk_rule4_mobius_rotation_terms
  fact_class: disk_cipher_number_facts
  display_label: "Disk Rule-4 M\xF6bius bridge records 5 route-mechanics terms: rotation, flip, loop, step/trip, circumference"
  short_label: 'Rule4 terms: rotation/flip/loop/step/circumference'
  value: 5
  values:
  - 4
  - 5
  value_type: sequence
  operation_type: source_observation
  expression: Rule-4 bridge terms are rotation, flip, loop, step_or_trip, circumference.
  relation: "Conceptual bridge to Page32 M\xF6bius/Fibonacci route mechanics."
  why_stored: The mechanics vocabulary may matter for future route design, but it is not a route itself.
  verification_status: source_author_claim
  display_priority: medium
  source_paths:
  - data/historical-route/stage5dn-disk-rule4-mobius-trip-rotation-bridge-v0.yaml
  crosslinks:
  - page32_moebius_fibonacci_prime_index_spiral_v1
  - disk_alberti_branch_cipher_candidate_v1
  risk_notes:
  - confidence_low_medium
  - route_not_accepted
  - no_execution
- overlay_id: stage5ed_disk_doublet_suppression_448_89_overlay
  source_record_path: data/historical-route/stage5dn-disk-doublet-suppression-candidate-v1.yaml
  source_fact_id: disk_doublet_suppression_448_expected_89_observed
  fact_class: disk_cipher_number_facts
  display_label: Disk doublet-suppression claim compares expected 448 doublets to observed 89, approximately 5x suppression
  short_label: Doublets 448 expected / 89 observed / ~5x
  value: 89
  values:
  - 448
  - 89
  - 5
  value_type: sequence
  operation_type: source_observation
  expression: 'Source claim: expected doublets ~448, observed doublets 89, suppression factor approximately 5x.'
  relation: Possible mechanism-level bridge to LP-wide doublet scarcity.
  why_stored: This is a falsifiable statistical constraint for future DiskCipher/LP mechanism review.
  verification_status: source_author_claim
  display_priority: high
  source_paths:
  - data/historical-route/stage5dn-disk-doublet-suppression-candidate-v1.yaml
  crosslinks:
  - lp_doublet_scarcity_feature_v0
  - lp_doublet_scarcity_feature_v1
  - disk_alberti_branch_cipher_candidate_v1
  risk_notes:
  - accepted_as_validated_false
  - metric_definition_required
  - search_space_audit_required
  - random_controls_required
- overlay_id: stage5ed_disk_doublet_validation_requirements_overlay
  source_record_path: data/historical-route/stage5dn-disk-doublet-suppression-candidate-v1.yaml
  source_fact_id: disk_doublet_validation_requirement_count
  fact_class: disk_cipher_number_facts
  display_label: Disk doublet-suppression record lists 6 future validation requirements before accepting the claim
  short_label: Doublet validation requirements = 6
  value: 6
  values:
  - 6
  value_type: sequence
  operation_type: source_observation
  expression: Requirements include metric definition, canonical corpus, solved/unsolved split, random controls, model controls,
    and trial-count accounting.
  relation: Keeps the statistical claim quarantined until model and corpus controls exist.
  why_stored: Makes the uncertainty reviewable in the Source Browser.
  verification_status: quarantined_selection_bias
  display_priority: medium
  source_paths:
  - data/historical-route/stage5dn-disk-doublet-suppression-candidate-v1.yaml
  crosslinks:
  - disk_probability_claim_quarantine_v1
  risk_notes:
  - future_validation_required
  - no_probability_claim_accepted
- overlay_id: stage5ed_disk_ruth_route_way_wordplay_cluster_overlay
  source_record_path: data/historical-route/stage5dn-disk-ruth-root-route-way-wordplay-candidate-v0.yaml
  source_fact_id: disk_ruth_root_route_way_wordplay_cluster
  fact_class: disk_cipher_number_facts
  display_label: Disk wordplay record links WAY/RUTH/root/route/road/path/direction to 2016 route vocabulary
  short_label: WAY/RUTH/root/route/road/path/direction
  value: 7
  values:
  - 7
  value_type: sequence
  operation_type: source_observation
  expression: 'Semantic cluster has 7 route/devotion terms: WAY, RUTH, root, route, road, path, direction.'
  relation: Weak semantic support for the WAY route surface and 2016 route-meta clue.
  why_stored: Useful as context, but too flexible to use as evidence alone.
  verification_status: operator_assistant_observed
  display_priority: low
  source_paths:
  - data/historical-route/stage5dn-disk-ruth-root-route-way-wordplay-candidate-v0.yaml
  crosslinks:
  - pdd_153_triangle_way_anchor_route_v1
  - 2016_message_route_meta_clue_v0
  - disk_56311_wynn_way_bridge_v1
  risk_notes:
  - flexible_wordplay
  - not_independent_evidence
  - not_route_seed
- overlay_id: stage5ed_disk_2015_eclipse_167_overlay
  source_record_path: data/historical-route/stage5dn-disk-2015-eclipse-167-temporal-candidate-v0.yaml
  source_fact_id: disk_2015_eclipse_167_temporal_candidate
  fact_class: disk_cipher_number_facts
  display_label: Disk 2015 eclipse candidate preserves a low/medium 167-second temporal bridge to 761.MP3
  short_label: 2015 eclipse 167s -> 761.MP3 167s
  value: 167
  values:
  - 2015
  - 167
  - 761
  value_type: sequence
  operation_type: source_observation
  expression: Community/source claim links March 20 2015 eclipse timing around 167 seconds to the 761.MP3 duration family.
  relation: Possible temporal bridge between DiskCipher external-date material and music/Instar 167 context.
  why_stored: Preserves the compact 167 bridge while warning that the external symbolic chain is broad.
  verification_status: canonical_source_required
  display_priority: low
  source_paths:
  - data/historical-route/stage5dn-disk-2015-eclipse-167-temporal-candidate-v0.yaml
  crosslinks:
  - music_3301_instar_crab_canon_v0
  - instar_title_761_duration_167_bridge_v1
  risk_notes:
  - external_fact_not_source_locked_now
  - broad_symbolic_chain
  - accepted_as_cicada_clue_false
  - accepted_route_false
- overlay_id: stage5ed_stage5dn_pdd153_56311_wynn_way_route_overlay
  source_record_path: data/historical-route/stage5dn-pdd-153-triangle-56311-wynn-way-route-v1.yaml
  source_fact_id: stage5dn_pdd153_56311_wynn_way_route
  fact_class: pdd_153_triangle_number_facts
  display_label: Stage 5DN PDD153 bridge records center word 41/WYNN and word52 reached by 56311
  short_label: Stage5DN PDD153 41/WYNN -> 52/WAY
  value: 52
  values:
  - 41
  - 52
  - 5
  - 6
  - 3
  - 11
  value_type: sequence
  operation_type: sequence_mapping
  expression: PDD153 center word index 41 is WYNN; word52 is reached by 56311-from-center bridge and preserves the WAY derivation
    candidate.
  relation: Triangle-side counterpart to the DiskCipher 56311/WYNN/WAY support layer.
  why_stored: Ensures the Stage 5DN bridge is visible separately from Stage 5DL/5EC triangle cards.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  source_paths:
  - data/historical-route/stage5dn-pdd-153-triangle-56311-wynn-way-route-v1.yaml
  crosslinks:
  - disk_56311_wynn_way_bridge_v1
  - pdd_153_triangle_56311_wynn_way_route_v1
  risk_notes:
  - route_extraction_not_performed
  - accepted_route_false
- overlay_id: stage5ed_solved_i_voice_circumference_precedent_overlay
  source_record_path: data/historical-route/stage5dn-solved-i-voice-of-circumference-precedent-v0.yaml
  source_fact_id: solved_i_voice_circumference_single_i
  fact_class: solved_koan_number_facts
  display_label: Solved koan 0.4.0 contains single-letter I and the quote THE I IS THE VOICE OF THE CIRCUMFERENCE
  short_label: 'Solved 0.4.0: I + CIRCUMFERENCE'
  value: 1
  values:
  - 1
  - 4
  - 0
  value_type: sequence
  operation_type: source_observation
  expression: Source section 0.4.0 includes a single-letter I token and the solved quote THE I IS THE VOICE OF THE CIRCUMFERENCE.
  relation: Solved precedent for single-letter / circumference / voice-self context.
  why_stored: Supports review of single-rune/single-letter anchor hypotheses without claiming I maps to WYNN.
  verification_status: verified_against_committed_source
  display_priority: high
  source_paths:
  - data/historical-route/stage5dn-solved-i-voice-of-circumference-precedent-v0.yaml
  crosslinks:
  - circumference_single_i_spiral_anchor_crosslink_v0
  - blake_urizen_los_reason_circumference_v0
  - pdd_153_triangle_word_prime_route_v1
  risk_notes:
  - not_claiming_i_equals_center_w
  - not_claiming_direct_mapping_between_i_and_wynn
- overlay_id: stage5ed_circumference_single_i_spiral_anchor_overlay
  source_record_path: data/historical-route/stage5dn-circumference-single-i-spiral-anchor-crosslink-v0.yaml
  source_fact_id: circumference_single_i_spiral_anchor_crosslink
  fact_class: solved_koan_number_facts
  display_label: Circumference crosslink records five triangle single-rune anchors and center word 41/WYNN without claiming
    I=WYNN
  short_label: Circumference / I / anchors 25/41/53/91/106
  value: 41
  values:
  - 25
  - 41
  - 53
  - 91
  - 106
  value_type: sequence
  operation_type: source_observation
  expression: Source facts include triangle single-rune anchors 25,41,53,91,106 and center word 41 WYNN, plus solved I/circumference
    context.
  relation: "Cross-family context linking solved I, PDD anchors, Page32 M\xF6bius, DiskCipher circles, and music circumference."
  why_stored: Makes the non-mapping warning visible alongside the numeric anchor list.
  verification_status: operator_assistant_observed
  display_priority: medium
  source_paths:
  - data/historical-route/stage5dn-circumference-single-i-spiral-anchor-crosslink-v0.yaml
  crosslinks:
  - solved_i_voice_of_circumference_precedent_v0
  - pdd_153_triangle_word_prime_route_v1
  - page32_moebius_fibonacci_prime_index_spiral_v1
  risk_notes:
  - not_a_mapping_claim
  - not_claiming_i_equals_wynn
  - not_claiming_i_equals_triangle_center
- overlay_id: stage5ed_disk_probability_quarantine_requirements_overlay
  source_record_path: data/historical-route/stage5dn-disk-probability-claim-quarantine-v1.yaml
  source_fact_id: disk_probability_quarantine_requirements
  fact_class: disk_cipher_number_facts
  display_label: Disk probability claims are quarantined due to 5 risk classes and 5 future-control requirements
  short_label: 'Disk probability quarantine: 5 risks / 5 requirements'
  value: 5
  values:
  - 5
  - 5
  value_type: sequence
  operation_type: source_observation
  expression: 'Quarantine lists 5 risk reasons and 5 future requirements: formal model, deterministic reimplementation, trial
    accounting, negative controls, blind randomized testing.'
  relation: Keeps p-value/probability claims from influencing target decisions prematurely.
  why_stored: Prevents impressive probability claims from appearing validated in the UI.
  verification_status: quarantined_selection_bias
  display_priority: quarantine
  source_paths:
  - data/historical-route/stage5dn-disk-probability-claim-quarantine-v1.yaml
  crosslinks:
  - disk_doublet_suppression_candidate_v1
  - disk_alberti_branch_cipher_candidate_v1
  risk_notes:
  - probability_claim_accepted_as_validated_false
  - many_degrees_of_freedom
  - selection_bias
- overlay_id: stage5ed_blake_seven_subfamilies_overlay
  source_record_path: data/historical-route/stage5dm-blake-visual-text-source-family.yaml
  source_fact_id: blake_visual_text_seven_subfamilies
  fact_class: blake_visual_text_number_facts
  display_label: Blake visual-text source family records seven source-context subfamilies
  short_label: Blake source family = 7 subfamilies
  value: 7
  values:
  - 7
  value_type: sequence
  operation_type: source_observation
  expression: Source-lock records 7 Blake subfamilies including Marriage, Tyger, Innocence/Experience, Ancient of Days/Newton,
    Urizen/Los, body/soul, and Human Abstract.
  relation: Context layer for circumference, perception, body/self, geometry, contraries, symmetry, and tree/mind themes.
  why_stored: Makes Blake context reviewable without treating it as a cipher key.
  verification_status: source_author_claim
  display_priority: medium
  source_paths:
  - data/historical-route/stage5dm-blake-visual-text-source-family.yaml
  crosslinks:
  - blake_urizen_los_reason_circumference_v0
  - solved_i_voice_of_circumference_precedent_v0
  - page32_tree_polar_route_v0
  risk_notes:
  - thematic_links_only
  - cipher_key_claimed_false
  - decode_authorized_now_false
- overlay_id: stage5ed_sacred_book_overlay_inventory_overlay
  source_record_path: data/historical-route/stage5dm-lp-sacred-book-edition-overlay-index.yaml
  source_fact_id: sacred_book_overlay_inventory_15_files
  fact_class: visual_source_number_facts
  display_label: LP Sacred Book overlay index has 15 expected overlay images, all present, used as alignment aids only
  short_label: Sacred Book overlays = 15 present
  value: 15
  values:
  - 15
  - 700
  - 1050
  value_type: sequence
  operation_type: source_observation
  expression: File inventory count and expected filename count are 15; early page overlay dimensions include 700x1050.
  relation: Human alignment aids for source review, not primary sources and not OCR evidence.
  why_stored: Helps review image/source availability while preserving primary-source hierarchy.
  verification_status: verified_against_committed_source
  display_priority: low
  source_paths:
  - data/historical-route/stage5dm-lp-sacred-book-edition-overlay-index.yaml
  crosslinks:
  - lp_sacred_book_edition_overlay_v0
  risk_notes:
  - overlay_images_are_not_primary_source
  - raw_overlay_images_not_committed
  - ocr_or_ai_interpretation_false
- overlay_id: stage5ed_solved_magic_square_1033_overlay
  source_record_path: data/historical-route/stage5dm-solved-magic-square-word-sum-precedent.yaml
  source_fact_id: solved_magic_square_row_sum_1033
  fact_class: magic_square_number_facts
  display_label: Solved magic-square precedent has magic constant 1033 with worked row sum 272+138+341+131+151=1033
  short_label: Magic square constant 1033
  value: 1033
  values:
  - 272
  - 138
  - 341
  - 131
  - 151
  - 1033
  value_type: sum
  operation_type: sum
  expression: 272 + 138 + 341 + 131 + 151 = 1033.
  relation: Solved LP precedent for word-number interchange and matrix-like route objects.
  why_stored: Strong support context for future triangle/Page32/matrix word-sum tests.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  source_paths:
  - data/historical-route/stage5dm-solved-magic-square-word-sum-precedent.yaml
  crosslinks:
  - pdd_153_triangle_word_prime_route_v1
  - magic_square_matrix_route_context_v0
  risk_notes:
  - future_only
  - broad_magic_square_search_not_performed
  - no_experiment_authorized
- overlay_id: stage5ed_full_lp_visual_motif_14_sections_overlay
  source_record_path: data/historical-route/stage5dm-full-lp-page-visual-motif-index.yaml
  source_fact_id: full_lp_visual_motif_index_14_sections
  fact_class: visual_source_number_facts
  display_label: Full LP visual motif index records 14 section-level motif groups
  short_label: Visual motif index = 14 sections
  value: 14
  values:
  - 14
  value_type: sequence
  operation_type: source_observation
  expression: Source-lock records 14 section-level visual motif groups across LP page ranges.
  relation: Review map for visual/route candidate families such as PDD153, Page32 tree/polar, Blake, and quote-dialogue.
  why_stored: Useful UI context; not image classification or decode evidence.
  verification_status: operator_assistant_observed
  display_priority: medium
  source_paths:
  - data/historical-route/stage5dm-full-lp-page-visual-motif-index.yaml
  crosslinks:
  - full_lp_page_visual_motif_index_v0
  - page32_tree_polar_route_v0
  - pdd_153_triangle_word_prime_route_v1
  risk_notes:
  - motif_tags_are_review_metadata
  - no_image_forensics
  - no_visual_matching
- overlay_id: stage5ed_stage5dm_doublet_metric_family_overlay
  source_record_path: data/historical-route/stage5dm-lp-doublet-scarcity-feature-candidate.yaml
  source_fact_id: stage5dm_doublet_metric_family
  fact_class: doublet_statistical_number_facts
  display_label: Stage 5DM doublet-scarcity candidate defines seven future metrics but computes no statistics
  short_label: Doublet metrics = 7 planned / computed=false
  value: 7
  values:
  - 7
  value_type: sequence
  operation_type: source_observation
  expression: Candidate metrics include adjacent identical count/rate, within-word, cross-word, repeated bigram, repeated
    word, solved-vs-unsolved, and section z-score.
  relation: Review-only statistical feature family later linked to Stage 5DN doublet-suppression claims.
  why_stored: Prevents metric-design records from looking empty in the Source Browser.
  verification_status: operator_assistant_observed
  display_priority: medium
  source_paths:
  - data/historical-route/stage5dm-lp-doublet-scarcity-feature-candidate.yaml
  crosslinks:
  - disk_doublet_suppression_candidate_v1
  - lp_doublet_scarcity_feature_v1
  risk_notes:
  - statistics_computed_now_false
  - corpus_wide_experiment_false
  - metric_predeclaration_required
- overlay_id: stage5ed_2016_message_563_569_route_terms_overlay
  source_record_path: data/historical-route/stage5di-2016-message-route-meta-clue.yaml
  source_fact_id: message_2016_563_569_five_route_terms
  fact_class: historical_message_number_facts
  display_label: 2016 message source-lock records claimed oak-tree dimensions 563x569 and five route terms
  short_label: 2016 message 563x569 + 5 route terms
  value: 563
  values:
  - 563
  - 569
  - 5
  value_type: sequence
  operation_type: source_observation
  expression: Image dimensions claimed as 563x569; route terms present are path, way, map, road, direction.
  relation: Route-meta clue for word/number/layout methods; crosslinks to PDD, Page32, Page56, and music route context.
  why_stored: This is a compact source-locked description of the route grammar we keep referencing.
  verification_status: canonical_source_required
  display_priority: high
  source_paths:
  - data/historical-route/stage5di-2016-message-route-meta-clue.yaml
  crosslinks:
  - pdd_153_triangle_word_prime_route_v1
  - page32_tree_polar_route_v0
  - page56_dwh_hash_target_contract_v0
  risk_notes:
  - pgp_signature_not_reverified_stage5di
  - source_claim_not_route_execution
- overlay_id: stage5ed_page32_tree_polar_crosswalk_overlay
  source_record_path: data/historical-route/stage5di-page32-tree-polar-route-candidate.yaml
  source_fact_id: page32_tree_polar_unsolved32_full49_hash_crosswalk
  fact_class: page32_tree_polar_number_facts
  display_label: Page32 tree/polar record crosswalks unsolved 32.jpg and full 49.jpg by same file size/hash
  short_label: 'page32 tree: unsolved32 = full49'
  value: 32
  values:
  - 32
  - 49
  - 362637
  value_type: sequence
  operation_type: source_observation
  expression: Unsolved image 32.jpg and full image 49.jpg both have file size 362637 bytes and the same SHA-256 in the source-lock.
  relation: Prevents naming/indexing confusion between unsolved-page 32 and full-page 49 route surfaces.
  why_stored: Critical page-numbering crosswalk for future Page32/tree/polar review.
  verification_status: verified_against_committed_source
  display_priority: high
  source_paths:
  - data/historical-route/stage5di-page32-tree-polar-route-candidate.yaml
  crosslinks:
  - page32_tree_polar_route_v0
  - message_2016_route_meta_clue_v0
  risk_notes:
  - route_model_candidates_future_only
  - no_polar_extraction
  - page_numbering_convention_required
- overlay_id: stage5ed_page56_hash_contract_128_64_512_overlay
  source_record_path: data/historical-route/stage5dk-page56-dwh-hash-contract.yaml
  source_fact_id: page56_hash_contract_128_64_512
  fact_class: page56_hash_number_facts
  display_label: Page56 hash contract has 128 hex characters = 64 bytes = 512 bits; algorithm/preimage unknown
  short_label: Page56 hash 128 hex / 64 bytes / 512 bits
  value: 512
  values:
  - 128
  - 64
  - 512
  value_type: hash_length
  operation_type: source_observation
  expression: Page56 hash length is 128 hex characters, 64 bytes, 512 bits; algorithm not selected and preimage not searched.
  relation: Target-contract context for final route outputs; not an immediate experiment.
  why_stored: Important final-target constraint visible in review.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  source_paths:
  - data/historical-route/stage5dk-page56-dwh-hash-contract.yaml
  crosslinks:
  - page56_dwh_hash_target_contract_v0
  - token_block_matrix_context_v0
  - page32_tree_polar_route_v0
  - pdd_153_triangle_word_prime_route_v1
  risk_notes:
  - page56_hash_algorithm_selected_now_false
  - hash_preimage_search_performed_false
  - target_class_validation_false
  - not_onion_address
- overlay_id: stage5ed_page56_hash_algorithm_candidate_set_overlay
  source_record_path: data/historical-route/stage5dk-page56-dwh-hash-contract.yaml
  source_fact_id: page56_hash_algorithm_candidate_set_7
  fact_class: page56_hash_number_facts
  display_label: Page56 hash-contract record lists seven possible 512-bit hash algorithm classes but selects none
  short_label: Page56 algorithm candidates = 7 / selected=false
  value: 7
  values:
  - 7
  - 128
  - 64
  - 512
  value_type: sequence
  operation_type: source_observation
  expression: Candidate algorithms are SHA-512, SHA3-512, BLAKE-512, BLAKE2b-512, Whirlpool, Skein-512, unknown/custom 512-bit
    hash.
  relation: Prevents false algorithm assumptions from creeping into target planning.
  why_stored: Useful for final-target review without enabling preimage search.
  verification_status: source_author_claim
  display_priority: medium
  source_paths:
  - data/historical-route/stage5dk-page56-dwh-hash-contract.yaml
  crosslinks:
  - page56_dwh_hash_target_contract_v0
  risk_notes:
  - algorithm_known_false
  - preimage_known_false
  - no_search
- overlay_id: stage5ed_dinkus_two_pages_three_dots_overlay
  source_record_path: data/historical-route/stage5di-dinkus-visual-delimiter-candidate.yaml
  source_fact_id: dinkus_two_pages_three_dots
  fact_class: visual_source_number_facts
  display_label: 'Dinkus candidate records three-dot horizontal separators on two pages: 50.jpg and 56.jpg'
  short_label: 'Dinkus candidate: 3 dots on 2 pages'
  value: 3
  values:
  - 3
  - 2
  - 50
  - 56
  value_type: sequence
  operation_type: source_observation
  expression: Observed feature is three black dots in horizontal separator form on operator-attached 50.jpg and 56.jpg.
  relation: Low/medium visual delimiter candidate relevant to section boundary review and Page56 context.
  why_stored: Makes the observation visible without turning uneven spacing into a cipher claim.
  verification_status: operator_assistant_observed
  display_priority: low
  source_paths:
  - data/historical-route/stage5di-dinkus-visual-delimiter-candidate.yaml
  crosslinks:
  - page56_dwh_hash_target_contract_v0
  - lp_negative_space_layout_candidate_family_v0
  risk_notes:
  - measurement_performed_now_false
  - uneven_spacing_cipher_claimed_now_false
  - visual_marker_only
- overlay_id: stage5ed_magic_square_matrix_context_terms_overlay
  source_record_path: data/historical-route/stage5di-magic-square-matrix-route-context.yaml
  source_fact_id: magic_square_matrix_context_four_terms
  fact_class: magic_square_number_facts
  display_label: 'Magic-square matrix context preserves four route-method terms: magic_square, matrix_route, gf_matrix, layout_transform'
  short_label: Magic-square context = 4 method terms
  value: 4
  values:
  - 4
  value_type: sequence
  operation_type: source_observation
  expression: Route context terms are magic_square, matrix_route, gf_matrix, and layout_transform.
  relation: Context layer for solved magic-square precedent and future bounded matrix-method tests.
  why_stored: Keeps matrix/GF discussion source-locked without executing transforms.
  verification_status: operator_assistant_observed
  display_priority: medium
  source_paths:
  - data/historical-route/stage5di-magic-square-matrix-route-context.yaml
  crosslinks:
  - solved_magic_square_word_sum_precedent_v0
  - token_block_matrix_context_v0
  risk_notes:
  - magic_square_transform_performed_now_false
  - route_extraction_false
  - future_bounded_candidate_only
- overlay_id: stage5ed_disk_support_cluster_summary_overlay
  source_record_path: data/historical-route/stage5dn-disk-p39-row1-math-semantic-cluster-v1.yaml
  source_fact_id: disk_support_cluster_summary
  fact_class: disk_cipher_number_facts
  display_label: 'Disk support cluster summary: 56311, WYNN/41, p39 ten-term cluster, doublet 448/89, 167 temporal bridge'
  short_label: Disk support cluster 56311/WYNN/p39/doublets/167
  value: 56311
  values:
  - 56311
  - 41
  - 52
  - 10
  - 448
  - 89
  - 167
  value_type: sequence
  operation_type: source_observation
  expression: Summary card only; detailed cards cover the individual DiskCipher facts.
  relation: Compact review chip tying together the Stage 5ED DiskCipher support-layer overlays.
  why_stored: Improves Source Browser scanability while preserving detailed cards and risk notes.
  verification_status: operator_assistant_observed
  display_priority: low
  source_paths:
  - data/historical-route/stage5dn-disk-p39-row1-math-semantic-cluster-v1.yaml
  - data/historical-route/stage5dn-disk-doublet-suppression-candidate-v1.yaml
  - data/historical-route/stage5dn-disk-2015-eclipse-167-temporal-candidate-v0.yaml
  risk_notes:
  - summary_card_only
  - not_independent_evidence
  - no_route_execution
- overlay_id: stage5ed_visual_method_cluster_summary_overlay
  source_record_path: data/historical-route/stage5dm-solved-magic-square-word-sum-precedent.yaml
  source_fact_id: visual_method_context_cluster_summary
  fact_class: visual_method_number_facts
  display_label: 'Visual/method context summary: Blake 7, Sacred overlays 15, magic-square 1033, motif sections 14, Page56
    512-bit hash'
  short_label: Visual/method 7/15/1033/14/512
  value: 1033
  values:
  - 7
  - 15
  - 1033
  - 14
  - 512
  value_type: sequence
  operation_type: source_observation
  expression: Summary card only; detailed cards cover Blake, Sacred Book overlays, magic-square precedent, LP motif index,
    and Page56 hash contract.
  relation: Compact review chip tying together non-Disk method/context overlays in Stage 5ED.
  why_stored: Improves Source Browser scanability without creating a new evidence claim.
  verification_status: operator_assistant_observed
  display_priority: low
  source_paths:
  - data/historical-route/stage5dm-blake-visual-text-source-family.yaml
  - data/historical-route/stage5dm-lp-sacred-book-edition-overlay-index.yaml
  - data/historical-route/stage5dm-solved-magic-square-word-sum-precedent.yaml
  - data/historical-route/stage5dm-full-lp-page-visual-motif-index.yaml
  - data/historical-route/stage5dk-page56-dwh-hash-contract.yaml
  risk_notes:
  - summary_card_only
  - no_visual_matching
  - no_hash_search
"""

OVERLAY_ROWS: list[dict[str, Any]] = yaml.safe_load(STAGE5ED_OVERLAY_YAML)


@dataclass
class Stage5EDValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5ed"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5ed() -> dict[str, dict[str, Any]]:
    _write_schemas()
    _write_overlay_collection()
    _update_chatgpt_context()
    records = _build_records()
    _write_records(records)
    _update_stage_summary_records(records["summary"])
    _update_doc_staleness_source_of_truth()
    _update_operational_file_map()
    _write_codex_completion(records["summary"])
    return records


def validate_stage5ed() -> Stage5EDValidationResult:
    checks = [
        validate_stage5ed_review_batch_selection,
        validate_stage5ed_number_fact_overlays,
        validate_stage5ed_overlay_only_support,
        validate_stage5ed_source_browser_loadability,
        validate_stage5ed_stage5ec_preservation,
        validate_stage5ed_stage5eb_validation_policy,
        validate_stage5ed_stage5dx_preservation,
        validate_stage5ed_stage5dw_preservation,
        validate_stage5ed_stage5dv_preservation,
        validate_stage5ed_stage5du_preservation,
        validate_stage5ed_stage5dg_preservation,
        validate_stage5ed_stage5bd_preservation,
        validate_stage5ed_active_lineage_preservation,
        validate_stage5ed_sidecar_gates,
        validate_stage5ed_handoff_continuity,
        validate_stage5ed_credential_redaction_policy,
        validate_stage5ed_governance_scope,
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    errors.extend(_validate_required_paths())
    errors.extend(_validate_schemas())
    for check in checks:
        result = check()
        counts.update(result.counts)
        errors.extend(result.errors)
    summary = _load(PROJECT_STATE_PATHS["summary"])
    expected = {
        "status": "complete",
        "stage5ec_preserved": True,
        "assistant_or_operator_number_fact_batch_performed_now": True,
        "source_lock_entry_batch_review_performed_now": True,
        "reviewed_entry_count": EXPECTED_REVIEWED_ENTRY_COUNT,
        "overlay_count": EXPECTED_OVERLAY_COUNT,
        "overlay_only_fact_cards_supported": True,
        "historical_source_lock_records_rewritten": False,
        "source_lock_evidence_updated_now": False,
        "number_fact_backfill_performed_now": False,
        "target_priority_decision_created_now": False,
        "pivot_target_selected_now": False,
        "route_extraction_performed_now": False,
        "real_byte_stream_generated": False,
        "execution_performed": False,
        "solve_claim": False,
        "local_parallel_default_workers": LOCAL_PARALLEL_DEFAULT_WORKERS,
        "local_parallel_default_pytest_workers": LOCAL_PARALLEL_DEFAULT_PYTEST_WORKERS,
        "full_serial_pytest_required_for_normal_stage_completion": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"{PROJECT_STATE_PATHS['summary'].as_posix()}: {key} must be {value}")
    errors.extend(_required_false_errors(summary, PROJECT_STATE_PATHS["summary"].as_posix(), allow_true_batch_flags=True))
    counts.update(_summary_counts(summary))
    counts["token_block_stage5ed_valid"] = not errors
    return Stage5EDValidationResult(len(errors), counts, errors)


def validate_stage5ed_review_batch_selection() -> Stage5EDValidationResult:
    payload = _load(PROJECT_STATE_PATHS["review_batch_selection"])
    selected = payload.get("selected_source_record_paths", [])
    errors = []
    if payload.get("review_batch_id") != REVIEW_BATCH_ID:
        errors.append("Stage 5ED review batch id mismatch")
    if payload.get("reviewed_entry_count") != EXPECTED_REVIEWED_ENTRY_COUNT or len(selected) != 20:
        errors.append("Stage 5ED selected batch must contain exactly 20 records")
    if selected != SELECTED_SOURCE_RECORD_PATHS:
        errors.append("Stage 5ED selected source path order/content mismatch")
    errors.extend(f"selected source path missing: {path}" for path in selected if not Path(path).exists())
    if payload.get("review_scope") != "selected_20_source_records_only":
        errors.append("Stage 5ED review scope must be selected_20_source_records_only")
    return Stage5EDValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ed_number_fact_overlays() -> Stage5EDValidationResult:
    collection = _load_overlay_collection()
    overlays = collection.get("overlays", [])
    errors = []
    if collection.get("record_type") != "stage5ed_source_browser_number_fact_enrichment_overlay_collection":
        errors.append("overlay collection record_type mismatch")
    if collection.get("stage_id") != STAGE_ID:
        errors.append("overlay collection stage_id mismatch")
    if collection.get("reviewed_entry_count") != EXPECTED_REVIEWED_ENTRY_COUNT:
        errors.append("overlay collection reviewed entry count must be 20")
    if collection.get("overlay_count") != EXPECTED_OVERLAY_COUNT or len(overlays) != EXPECTED_OVERLAY_COUNT:
        errors.append(f"expected {EXPECTED_OVERLAY_COUNT} overlays, got {len(overlays)}")
    if collection.get("selected_source_record_paths") != SELECTED_SOURCE_RECORD_PATHS:
        errors.append("overlay collection selected source path mismatch")
    selected = set(collection.get("selected_source_record_paths", []))
    overlay_paths = {str(overlay.get("source_record_path") or "") for overlay in overlays}
    errors.extend(f"selected source has no overlay: {path}" for path in sorted(selected - overlay_paths))
    schema = _load(Path("schemas/operator-console/source-browser-number-fact-enrichment-overlay-v0.schema.json"))
    validator = Draft202012Validator(schema)
    ids: set[str] = set()
    for index, overlay in enumerate(overlays):
        overlay_id = str(overlay.get("overlay_id") or "")
        if overlay_id in ids:
            errors.append(f"duplicate overlay_id: {overlay_id}")
        ids.add(overlay_id)
        for error in sorted(validator.iter_errors(overlay), key=lambda item: item.path):
            errors.append(f"overlay[{index}] {overlay_id}: {error.message}")
        for key in ("source_record_path", "source_fact_id", "display_label", "relation", "why_stored"):
            if not overlay.get(key):
                errors.append(f"{overlay_id}: missing {key}")
        if not overlay.get("verification_status"):
            errors.append(f"{overlay_id}: missing verification_status")
        if not overlay.get("risk_notes"):
            errors.append(f"{overlay_id}: missing risk_notes")
        if overlay.get("usable_for_decision_now") is not False:
            errors.append(f"{overlay_id}: usable_for_decision_now must be false")
        not_allowed = set(overlay.get("not_allowed_as", []))
        for value in OVERLAY_REQUIRED_NOT_ALLOWED:
            if value not in not_allowed:
                errors.append(f"{overlay_id}: not_allowed_as missing {value}")
    return Stage5EDValidationResult(
        len(errors),
        {
            "overlay_count": len(overlays),
            "reviewed_entry_count": collection.get("reviewed_entry_count"),
            "selected_source_path_count": len(selected),
        },
        errors,
    )


def validate_stage5ed_overlay_only_support() -> Stage5EDValidationResult:
    index = build_source_index()
    entry_by_path = {entry.source_record_path: entry for entry in index.entries}
    overlays = _load_overlay_collection().get("overlays", [])
    selected_cards = 0
    overlay_only_cards = 0
    errors = []
    for path in SELECTED_SOURCE_RECORD_PATHS:
        entry = entry_by_path.get(path)
        if entry is None:
            errors.append(f"selected entry not loaded: {path}")
            continue
        cards = normalize_entry_number_facts(entry, overlays)
        if not cards:
            errors.append(f"selected entry has no normalized fact cards after overlays: {path}")
        selected_cards += len(cards)
        raw_ids = {_raw_fact_id(fact) for fact in entry.number_facts}
        overlay_only_cards += sum(
            1
            for overlay in overlays
            if overlay.get("source_record_path") == path and str(overlay.get("source_fact_id") or "") not in raw_ids
        )
    if overlay_only_cards < EXPECTED_OVERLAY_COUNT:
        errors.append("Stage 5ED overlays must remain overlay-only review cards")
    return Stage5EDValidationResult(
        len(errors),
        {
            "selected_batch_fact_cards": selected_cards,
            "overlay_only_cards_required_count": overlay_only_cards,
        },
        errors,
    )


def validate_stage5ed_source_browser_loadability() -> Stage5EDValidationResult:
    index = build_source_index()
    result = validate_source_index()
    path_result = validate_path_canonicalization()
    payload = _load(PROJECT_STATE_PATHS["source_browser_loadability"])
    errors = list(result.errors) + list(path_result.errors)
    for key in (
        "source_browser_validation_error_count",
        "spurious_root_image_paths_after",
        "spurious_root_document_paths_after",
        "duplicate_present_missing_path_pairs_after",
    ):
        if payload.get(key) != 0:
            errors.append(f"{key} must be 0")
    if len(index.entries) < 1658:
        errors.append("Source Browser entry count regressed below Stage 5EB baseline")
    return Stage5EDValidationResult(len(errors), {**result.counts, **path_result.counts, **_summary_counts(payload)}, errors)


def validate_stage5ed_stage5ec_preservation() -> Stage5EDValidationResult:
    payload = _load(PROJECT_STATE_PATHS["stage5ec_preservation"])
    errors = _expect(
        payload,
        {
            "stage5ec_preserved": True,
            "stage5ec_status": "complete",
            "stage5ec_reviewed_entry_count": 20,
            "stage5ec_overlay_count": 25,
            "stage5ec_source_browser_validation_error_count": 0,
            "historical_source_lock_records_rewritten": False,
            "source_lock_evidence_updated_now": False,
        },
    )
    return Stage5EDValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ed_stage5eb_validation_policy() -> Stage5EDValidationResult:
    payload = _load(PROJECT_STATE_PATHS["stage5eb_preservation"])
    errors = _expect(
        payload,
        {
            "stage5eb_preserved": True,
            "stage5eb_status": "complete",
            "stage5eb_local_parallel_default_workers": 10,
            "stage5eb_local_parallel_default_pytest_workers": 10,
            "stage5eb_maximum_supported_workers": 10,
            "stage5eb_maximum_supported_pytest_workers": 10,
            "full_serial_pytest_required_for_normal_stage_completion": False,
        },
    )
    return Stage5EDValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ed_stage5eb_preservation() -> Stage5EDValidationResult:
    return validate_stage5ed_stage5eb_validation_policy()


def validate_stage5ed_stage5dx_preservation() -> Stage5EDValidationResult:
    return _validate_token_preservation("stage5dx_preservation", "stage-5dx")


def validate_stage5ed_stage5dw_preservation() -> Stage5EDValidationResult:
    return _validate_token_preservation("stage5dw_preservation", "stage-5dw")


def validate_stage5ed_stage5dv_preservation() -> Stage5EDValidationResult:
    return _validate_token_preservation("stage5dv_preservation", "stage-5dv")


def validate_stage5ed_stage5du_preservation() -> Stage5EDValidationResult:
    return _validate_token_preservation("stage5du_preservation", "stage-5du")


def validate_stage5ed_stage5dg_preservation() -> Stage5EDValidationResult:
    payload = _load(TOKEN_PATHS["stage5dg_preservation"])
    errors = _expect(
        payload,
        {
            "source_stage_id": "stage-5dg",
            "preserved": True,
            "operator_approval_component_satisfied_preserved": True,
            "combined_approval_gate_satisfied_now": False,
        },
    )
    return Stage5EDValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ed_stage5bd_preservation() -> Stage5EDValidationResult:
    payload = _load(TOKEN_PATHS["stage5bd_preservation"])
    errors = _expect(payload, {"source_stage_id": "stage-5bd", "stage5bd_run_plan_id_count": 10, "preserved": True})
    return Stage5EDValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ed_active_lineage_preservation() -> Stage5EDValidationResult:
    payload = _load(TOKEN_PATHS["active_lineage_preservation"])
    errors = _expect(payload, {"active_lineage_record_count": 8, "preserved": True})
    return Stage5EDValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ed_sidecar_gates() -> Stage5EDValidationResult:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for key in ("no_active_ingestion_proof", "no_byte_stream_transition_proof", "no_execution_transition_proof"):
        payload = _load(TOKEN_PATHS[key])
        counts[key] = payload.get("gate_status")
        errors.extend(_required_false_errors(payload, TOKEN_PATHS[key].as_posix()))
        if payload.get("gate_status") != "closed":
            errors.append(f"{TOKEN_PATHS[key].as_posix()}: gate_status must be closed")
    return Stage5EDValidationResult(len(errors), counts, errors)


def validate_stage5ed_handoff_continuity() -> Stage5EDValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if payload.get("deprecated_codex_output_root_used") is not False or payload.get("codex_output_used") is not False:
        errors.append("deprecated codex_output root must not be used")
    if Path("codex_output").exists():
        errors.append("deprecated codex_output directory is present")
    return Stage5EDValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ed_credential_redaction_policy() -> Stage5EDValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["credential_redaction_policy_preservation"])
    errors = []
    if payload.get("credential_like_remote_count") != 0:
        errors.append("credential-like remote count must be 0")
    if payload.get("raw_source_body_included") is not False:
        errors.append("credential policy must not include raw source bodies")
    return Stage5EDValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ed_governance_scope() -> Stage5EDValidationResult:
    payload = _load(PROJECT_STATE_PATHS["scope_control"])
    errors = _required_false_errors(payload, PROJECT_STATE_PATHS["scope_control"].as_posix(), allow_true_batch_flags=True)
    if payload.get("source_lock_entry_batch_review_performed_now") is not True:
        errors.append("Stage 5ED must record source_lock_entry_batch_review_performed_now=true")
    if payload.get("assistant_or_operator_number_fact_batch_performed_now") is not True:
        errors.append("Stage 5ED must record assistant_or_operator_number_fact_batch_performed_now=true")
    if payload.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("next stage must be Stage 5EE")
    return Stage5EDValidationResult(len(errors), _summary_counts(payload), errors)


def stage5ed_summary_text() -> str:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5ED summary:",
        f"status={summary.get('status')}",
        f"review_batch_id={summary.get('review_batch_id')}",
        f"reviewed_entry_count={summary.get('reviewed_entry_count')}",
        f"overlay_count={summary.get('overlay_count')}",
        f"overlay_only_fact_cards_supported={summary.get('overlay_only_fact_cards_supported')}",
        f"source_browser_entries_loaded={summary.get('source_browser_entries_loaded')}",
        f"source_browser_records_scanned={summary.get('source_browser_records_scanned')}",
        f"fact_card_count_after_stage5ed={summary.get('fact_card_count_after_stage5ed')}",
        f"source_browser_validation_error_count={summary.get('source_browser_validation_error_count')}",
        f"historical_source_lock_records_rewritten={summary.get('historical_source_lock_records_rewritten')}",
        f"source_lock_evidence_updated_now={summary.get('source_lock_evidence_updated_now')}",
        f"target_selected={summary.get('pivot_target_selected_now')}",
        f"route_extracted={summary.get('route_extraction_performed_now')}",
        f"execution_performed={summary.get('execution_performed')}",
        f"solve_claim={summary.get('solve_claim')}",
        f"local_parallel_default_workers={summary.get('local_parallel_default_workers')}",
        f"local_parallel_default_pytest_workers={summary.get('local_parallel_default_pytest_workers')}",
        f"full_serial_pytest_required_for_normal_stage_completion={summary.get('full_serial_pytest_required_for_normal_stage_completion')}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


def _build_records() -> dict[str, dict[str, Any]]:
    overlays = _load_overlay_collection()["overlays"]
    all_overlays = load_enrichment_overlays()
    index = build_source_index()
    entry_by_path = {entry.source_record_path: entry for entry in index.entries}
    browser = source_browser_summary(index)
    path_report = path_canonicalization_report(index)
    source_browser_validation = validate_source_index()
    selected_fact_cards = {
        path: len(normalize_entry_number_facts(entry_by_path[path], all_overlays))
        for path in SELECTED_SOURCE_RECORD_PATHS
        if path in entry_by_path
    }
    fact_card_count_after = sum(len(normalize_entry_number_facts(entry, all_overlays)) for entry in index.entries)
    overlay_only_count = _overlay_only_count(overlays, entry_by_path)
    stage5eb = _load(PROJECT_STATE_DIR / "stage5eb-summary.yaml")
    stage5ec = _load(PROJECT_STATE_DIR / "stage5ec-summary.yaml")
    base = _stage_base()
    false_flags = _false_flags()

    summary = {
        **base,
        **false_flags,
        "record_type": "stage5ed_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "source_previous_stage_final_commit": PREVIOUS_STAGE_FINAL_COMMIT,
        "source_previous_issue": PREVIOUS_STAGE_ISSUE,
        "source_previous_ci_run": PREVIOUS_STAGE_CI_RUN,
        "source_previous_ci_status": PREVIOUS_STAGE_CI_STATUS,
        "stage5ec_preserved": True,
        "stage5ec_status": stage5ec.get("status", "complete"),
        "stage5ec_review_batch_id": stage5ec.get("review_batch_id"),
        "stage5ec_reviewed_entry_count": stage5ec.get("reviewed_entry_count", 20),
        "stage5ec_overlay_count": stage5ec.get("overlay_count", 25),
        "stage5ec_fact_card_count_after_stage5ec": stage5ec.get("fact_card_count_after_stage5ec", 117),
        "stage5ec_source_browser_validation_error_count": stage5ec.get("source_browser_validation_error_count", 0),
        "stage5eb_preserved": True,
        "stage5eb_local_parallel_default_workers": stage5eb.get("local_parallel_default_workers", 10),
        "stage5eb_local_parallel_default_pytest_workers": stage5eb.get("local_parallel_default_pytest_workers", 10),
        "stage5eb_full_serial_pytest_default": stage5eb.get("full_serial_pytest_default_for_future_stages", False),
        "assistant_or_operator_number_fact_batch_performed_now": True,
        "source_lock_entry_batch_review_performed_now": True,
        "new_number_fact_overlays_added_now": True,
        "review_batch_id": REVIEW_BATCH_ID,
        "review_batch_selection_policy": REVIEW_BATCH_SELECTION_POLICY,
        "review_scope": "selected_20_source_records_only",
        "reviewed_entry_count": EXPECTED_REVIEWED_ENTRY_COUNT,
        "selected_source_record_paths": SELECTED_SOURCE_RECORD_PATHS,
        "number_fact_enrichment_overlays_added_now": True,
        "overlay_collection_path": OVERLAY_COLLECTION_PATH.as_posix(),
        "review_batch_result_path": REVIEW_BATCH_RESULT_PATH.as_posix(),
        "overlay_count": len(overlays),
        "overlay_only_fact_cards_supported": True,
        "overlay_only_fact_cards_validated": True,
        "overlay_only_cards_required_count": overlay_only_count,
        "facts_added_directly_to_source_records": False,
        "facts_added_as_overlays": True,
        "source_browser_loadability_validated": True,
        "source_browser_entries_loaded": browser["entries_loaded"],
        "source_browser_records_scanned": browser["records_scanned"],
        "source_browser_validation_error_count": len(source_browser_validation.errors),
        "source_browser_warning_count": browser["warnings"],
        "source_browser_missing_paths_after": browser["missing_paths"],
        "missing_paths_retained_as_warnings": True,
        "fact_card_count_after_stage5ed": fact_card_count_after,
        "selected_batch_fact_card_count": sum(selected_fact_cards.values()),
        "spurious_root_image_paths_after": path_report["spurious_root_image_paths"],
        "spurious_root_document_paths_after": path_report["spurious_root_document_paths"],
        "duplicate_present_missing_path_pairs_after": path_report["duplicate_present_missing_path_pairs"],
        "source_root_relative_resolved_paths": path_report["source_root_relative_resolved_paths"],
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": 8,
        "local_parallel_default_workers": LOCAL_PARALLEL_DEFAULT_WORKERS,
        "local_parallel_default_pytest_workers": LOCAL_PARALLEL_DEFAULT_PYTEST_WORKERS,
        "maximum_supported_workers": PARALLEL_WORKER_CAP,
        "maximum_supported_pytest_workers": PARALLEL_WORKER_CAP,
        "full_serial_pytest_default_for_future_stages": False,
        "full_serial_pytest_required_for_normal_stage_completion": False,
        "full_serial_pytest_allowed_only_when_explicitly_requested": True,
        "full_parallel_is_normal_final_local_profile": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": PROMPT_TYPE,
        "selected_next_stage_authorizes_execution": False,
        "selected_next_stage_authorizes_activation": False,
        "selected_next_stage_authorizes_byte_stream_generation": False,
    }
    records: dict[str, dict[str, Any]] = {
        "summary": summary,
        "next_stage_decision": _next_stage_record(base, false_flags),
        "review_batch_selection": _review_batch_selection_record(base, false_flags),
        "reviewable_validation_evidence": {
            **base,
            "record_type": "stage5ed_reviewable_validation_evidence",
            "schema": SCHEMA_PATHS["reviewable_validation_evidence"].as_posix(),
            "validators": [
                "validate-stage5ed",
                "validate-stage5ed-review-batch-selection",
                "validate-stage5ed-number-fact-overlays",
                "validate-stage5ed-overlay-only-support",
                "validate-stage5ed-source-browser-loadability",
                "source-browser validate-index",
                "source-browser validate-paths",
            ],
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
            "full_parallel_is_normal_final_local_profile": True,
            "full_serial_pytest_required_for_normal_stage_completion": False,
        },
        "scope_control": {
            **base,
            **false_flags,
            "record_type": "stage5ed_scope_control",
            "schema": SCHEMA_PATHS["scope_control"].as_posix(),
            "source_lock_entry_batch_review_performed_now": True,
            "assistant_or_operator_number_fact_batch_performed_now": True,
            "new_number_fact_overlays_added_now": True,
            "review_scope": "selected_20_source_records_only",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "codex_output_used": False,
        },
        "source_browser_loadability": {
            **base,
            "record_type": "stage5ed_source_browser_loadability_summary",
            "source_browser_entries_loaded": browser["entries_loaded"],
            "source_browser_records_scanned": browser["records_scanned"],
            "source_browser_validation_error_count": len(source_browser_validation.errors),
            "source_browser_warning_count": browser["warnings"],
            "source_browser_missing_paths_after": browser["missing_paths"],
            "missing_paths_retained_as_warnings": True,
            "fact_card_count_after_stage5ed": fact_card_count_after,
            "spurious_root_image_paths_after": path_report["spurious_root_image_paths"],
            "spurious_root_document_paths_after": path_report["spurious_root_document_paths"],
            "duplicate_present_missing_path_pairs_after": path_report["duplicate_present_missing_path_pairs"],
            "source_root_relative_resolved_paths": path_report["source_root_relative_resolved_paths"],
        },
        "stage5ec_preservation": _stage5ec_preservation_record(base, false_flags, stage5ec),
        "stage5eb_preservation": _stage5eb_preservation_record(base, false_flags, stage5eb),
        "chatgpt_context_update_summary": {
            **base,
            "record_type": "stage5ed_chatgpt_context_update_summary",
            "chatgpt_context_updated": _context_contains_stage5ed(),
            "chatgpt_context_path": CHATGPT_CONTEXT_PATH.as_posix(),
            "durable_facts_added": _context_contains_stage5ed(),
            "raw_source_body_included": False,
            "long_prompt_text_included": False,
        },
        "reviewability_gap_register": {
            **base,
            "record_type": "stage5ed_reviewability_gap_register",
            "remaining_gap": "continue_number_fact_review_batches",
            "next_batch_recommended": "number_fact_review_batch_005",
            "lag5_phenomenon_source_locked_by_stage5ed": False,
            "overlay_count_deviation": False,
            "target_priority_decision_created_now": False,
        },
        "current_stage_state": {
            **base,
            **false_flags,
            "record_type": "current_stage_state",
            "schema": "schemas/project-state/current-stage-state-v0.schema.json",
            "status": "complete",
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "latest_completed_stage_commit_recording_policy": "external_post_push_handoff",
            "latest_completed_stage_ci_status_recording_policy": "external_post_push_handoff",
            "latest_completed_stage_commit_in_committed_registry": "not_applicable_self_referential",
            "latest_completed_stage_ci_status_in_committed_registry": "not_applicable_pre_push",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": PROMPT_TYPE,
            "stage_registry_is_source_of_truth": True,
            "historical_tests_must_not_require_latest_stage": True,
            "current_stage_registry_is_committed_pre_push_state": True,
            "self_referential_commit_hash_not_required_in_committed_registry": True,
            "final_commit_and_ci_recorded_externally": True,
            "post_push_handoff_required": True,
            "post_push_handoff_locations": ["codex-output/stage5ed-codex-completion.md", "GitHub issue comment"],
        },
        "review_batch_result": {
            **base,
            "record_type": "source_browser_number_fact_review_batch_result",
            "schema": SCHEMA_PATHS["review_batch_result"].as_posix(),
            "review_batch_id": REVIEW_BATCH_ID,
            "review_batch_selection_policy": REVIEW_BATCH_SELECTION_POLICY,
            "reviewed_entry_count": EXPECTED_REVIEWED_ENTRY_COUNT,
            "overlay_count": len(overlays),
            "overlays_added_now": True,
            "historical_source_lock_records_rewritten": False,
            "source_lock_evidence_updated_now": False,
            "number_fact_backfill_performed_now": False,
            "review_scope": "selected_20_source_records_only",
            "review_result_status": "overlay_enrichment_complete",
            "selected_source_record_paths": SELECTED_SOURCE_RECORD_PATHS,
            "overlay_file": OVERLAY_COLLECTION_PATH.as_posix(),
            "facts_added_directly_to_source_records": False,
            "facts_added_as_overlays": True,
        },
    }
    records.update(_source_harvester_records(base, false_flags))
    records.update(_token_records(base, false_flags))
    return records


def _next_stage_record(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5ed_next_stage_decision",
        "schema": SCHEMA_PATHS["next_stage_decision"].as_posix(),
        "status": "complete",
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": PROMPT_TYPE,
        "selected_next_stage_authorizes_execution": False,
        "selected_next_stage_authorizes_activation": False,
        "selected_next_stage_authorizes_byte_stream_generation": False,
    }


def _review_batch_selection_record(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5ed_review_batch_selection",
        "schema": SCHEMA_PATHS["review_batch_selection"].as_posix(),
        "review_batch_id": REVIEW_BATCH_ID,
        "review_batch_selection_policy": REVIEW_BATCH_SELECTION_POLICY,
        "review_scope": "selected_20_source_records_only",
        "reviewed_entry_count": EXPECTED_REVIEWED_ENTRY_COUNT,
        "selected_source_record_paths": SELECTED_SOURCE_RECORD_PATHS,
        "selection_clusters": ["disk_cipher", "visual_method", "route_context", "page56_hash", "magic_square"],
        "historical_source_lock_records_rewritten": False,
        "source_lock_evidence_updated_now": False,
    }


def _stage5ec_preservation_record(
    base: dict[str, Any], false_flags: dict[str, bool], stage5ec: dict[str, Any]
) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5ed_stage5ec_preservation",
        "stage5ec_preserved": True,
        "stage5ec_status": stage5ec.get("status", "complete"),
        "stage5ec_review_batch_id": stage5ec.get("review_batch_id"),
        "stage5ec_reviewed_entry_count": stage5ec.get("reviewed_entry_count", 20),
        "stage5ec_overlay_count": stage5ec.get("overlay_count", 25),
        "stage5ec_fact_card_count_after_stage5ec": stage5ec.get("fact_card_count_after_stage5ec", 117),
        "stage5ec_source_browser_validation_error_count": stage5ec.get("source_browser_validation_error_count", 0),
        "historical_source_lock_records_rewritten": False,
        "source_lock_evidence_updated_now": False,
        "facts_added_directly_to_source_records": False,
    }


def _stage5eb_preservation_record(
    base: dict[str, Any], false_flags: dict[str, bool], stage5eb: dict[str, Any]
) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5ed_stage5eb_preservation",
        "stage5eb_preserved": True,
        "stage5eb_status": stage5eb.get("status", "complete"),
        "stage5eb_issue": stage5eb.get("stage5ea_issue"),
        "stage5eb_ci_status": stage5eb.get("stage5ea_ci_status"),
        "stage5eb_local_parallel_default_workers": stage5eb.get("local_parallel_default_workers", 10),
        "stage5eb_local_parallel_default_pytest_workers": stage5eb.get("local_parallel_default_pytest_workers", 10),
        "stage5eb_maximum_supported_workers": stage5eb.get("maximum_supported_workers", 10),
        "stage5eb_maximum_supported_pytest_workers": stage5eb.get("maximum_supported_pytest_workers", 10),
        "full_serial_pytest_default_for_future_stages": False,
        "full_serial_pytest_required_for_normal_stage_completion": False,
        "full_serial_pytest_allowed_only_when_explicitly_requested": True,
        "source_browser_overlay_cache_reuse_validated": True,
    }


def _source_harvester_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "codex_handoff_policy": {
            **base,
            "record_type": "stage5ed_codex_handoff_policy",
            "canonical_codex_handoff_root": "codex-output",
            "deprecated_codex_output_root_used": False,
            "codex_output_used": False,
            "completion_summary_path": "codex-output/stage5ed-codex-completion.md",
            "completion_summary_committed": False,
        },
        "credential_redaction_policy_preservation": {
            **base,
            "record_type": "stage5ed_credential_redaction_policy_preservation",
            "credential_like_remote_count": 0,
            "credential_redaction_policy_preserved": True,
            "raw_source_body_included": False,
            "secret_material_committed": False,
        },
        "raw_source_noncommit_proof": {
            **base,
            **false_flags,
            "record_type": "stage5ed_raw_source_noncommit_proof",
            "raw_source_body_included": False,
            "raw_source_files_committed": False,
            "raw_third_party_files_committed": False,
            "generated_outputs_committed": False,
        },
    }


def _token_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for key, source_stage in (
        ("token_stage5eb_preservation", "stage-5eb"),
        ("stage5dx_preservation", "stage-5dx"),
        ("stage5dw_preservation", "stage-5dw"),
        ("stage5dv_preservation", "stage-5dv"),
        ("stage5du_preservation", "stage-5du"),
    ):
        records[key] = {
            **base,
            **false_flags,
            "record_type": f"stage5ed_{key}",
            "source_stage_id": source_stage,
            "preserved": True,
            "rewritten": False,
            "superseded_now": False,
            "notes": "Stage 5ED records preservation only; it does not mutate historical inputs.",
        }
    records["stage5dg_preservation"] = {
        **base,
        **false_flags,
        "record_type": "stage5ed_stage5dg_preservation",
        "source_stage_id": "stage-5dg",
        "preserved": True,
        "operator_approval_component_satisfied_preserved": True,
        "deep_research_acceptance_created_now": False,
        "combined_approval_gate_satisfied_now": False,
    }
    records["stage5bd_preservation"] = {
        **base,
        **false_flags,
        "record_type": "stage5ed_stage5bd_preservation",
        "source_stage_id": "stage-5bd",
        "preserved": True,
        "stage5bd_run_plan_id_count": 10,
        "stage5bd_run_plan_ids_preserved": True,
    }
    records["active_lineage_preservation"] = {
        **base,
        **false_flags,
        "record_type": "stage5ed_active_lineage_preservation",
        "active_lineage_record_count": 8,
        "preserved": True,
        "active_lineage_preserved": True,
    }
    records["no_active_ingestion_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ed_no_active_ingestion_proof",
        "gate_status": "closed",
        "active_ingestion_performed": False,
    }
    records["no_byte_stream_transition_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ed_no_byte_stream_transition_proof",
        "gate_status": "closed",
        "real_byte_stream_generated": False,
        "variant_byte_streams_generated": False,
        "byte_stream_generation_authorized_now": False,
    }
    records["no_execution_transition_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ed_no_execution_transition_proof",
        "gate_status": "closed",
        "execution_authorized_now": False,
        "execution_performed": False,
        "token_block_experiment_executed": False,
    }
    return records


def _write_records(records: dict[str, dict[str, Any]]) -> None:
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        if key == "summary":
            required = ["record_type", "stage_id", "status", "review_batch_id", "overlay_count"]
            schema = _object_schema(required)
        elif key == "overlay_collection":
            schema = _overlay_collection_schema()
        elif key == "review_batch_result":
            schema = _object_schema(["record_type", "stage_id", "review_batch_id", "selected_source_record_paths"])
        else:
            schema = _object_schema(["record_type", "stage_id"])
        write_json(path, schema)


def _write_overlay_collection() -> None:
    write_yaml(OVERLAY_COLLECTION_PATH, _overlay_collection_payload())


def _overlay_collection_payload() -> dict[str, Any]:
    return {
        **_stage_base(),
        "record_type": "stage5ed_source_browser_number_fact_enrichment_overlay_collection",
        "schema": SCHEMA_PATHS["overlay_collection"].as_posix(),
        "review_batch_id": REVIEW_BATCH_ID,
        "review_batch_selection_policy": REVIEW_BATCH_SELECTION_POLICY,
        "reviewed_entry_count": EXPECTED_REVIEWED_ENTRY_COUNT,
        "overlay_count": EXPECTED_OVERLAY_COUNT,
        "overlay_only_fact_cards_supported_required": True,
        "review_state": "overlay_enriched_fact",
        "historical_source_lock_records_rewritten": False,
        "source_lock_evidence_updated_now": False,
        "raw_source_files_committed": False,
        "target_priority_decision_created_now": False,
        "pivot_target_selected_now": False,
        "execution_performed": False,
        "selected_source_record_paths": SELECTED_SOURCE_RECORD_PATHS,
        "overlays": [_overlay_with_defaults(overlay) for overlay in OVERLAY_ROWS],
    }


def _overlay_with_defaults(overlay: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "source_browser_number_fact_enrichment_overlay",
        "review_state": "overlay_enriched_fact",
        "usable_for_decision_now": False,
        "not_allowed_as": OVERLAY_REQUIRED_NOT_ALLOWED,
        **overlay,
    }


def _object_schema(required: list[str]) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
        "required": required,
        "properties": {
            "stage_id": {"const": STAGE_ID},
            "metadata_only": {"const": True},
            "puzzle_execution_allowed": {"const": False},
            "solve_claim": {"const": False},
            "historical_source_lock_records_rewritten": {"const": False},
            "source_lock_evidence_updated_now": {"const": False},
            "raw_source_files_committed": {"const": False},
            "raw_third_party_files_committed": {"const": False},
            "generated_outputs_committed": {"const": False},
            "target_priority_decision_created_now": {"const": False},
            "pivot_target_selected_now": {"const": False},
            "route_extraction_performed_now": {"const": False},
            "real_byte_stream_generated": {"const": False},
            "execution_performed": {"const": False},
            "reviewed_entry_count": {"const": EXPECTED_REVIEWED_ENTRY_COUNT},
            "overlay_count": {"const": EXPECTED_OVERLAY_COUNT},
        },
    }


def _overlay_collection_schema() -> dict[str, Any]:
    schema = _object_schema(["record_type", "stage_id", "review_batch_id", "overlays", "overlay_count"])
    schema["properties"].update(
        {
            "record_type": {"const": "stage5ed_source_browser_number_fact_enrichment_overlay_collection"},
            "review_batch_id": {"const": REVIEW_BATCH_ID},
            "overlays": {"type": "array", "minItems": EXPECTED_OVERLAY_COUNT, "maxItems": EXPECTED_OVERLAY_COUNT},
        }
    )
    return schema


def _validate_required_paths() -> list[str]:
    paths = list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values()) + [OVERLAY_COLLECTION_PATH]
    return [f"required Stage 5ED path missing: {path.as_posix()}" for path in paths if not path.exists()]


def _validate_schemas() -> list[str]:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        schema_key = SCHEMA_BY_DATA_KEY.get(key)
        if not schema_key:
            continue
        schema_path = SCHEMA_PATHS[schema_key]
        if not path.exists() or not schema_path.exists():
            continue
        payload = _load(path)
        schema = _load(schema_path)
        for error in sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda item: item.path):
            errors.append(f"{path.as_posix()}: {error.message}")
    if OVERLAY_COLLECTION_PATH.exists() and SCHEMA_PATHS["overlay_collection"].exists():
        payload = _load(OVERLAY_COLLECTION_PATH)
        schema = _load(SCHEMA_PATHS["overlay_collection"])
        for error in sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda item: item.path):
            errors.append(f"{OVERLAY_COLLECTION_PATH.as_posix()}: {error.message}")
    return errors


def _load(path: Path) -> dict[str, Any]:
    payload = read_yaml(path)
    return payload if isinstance(payload, dict) else {}


def _load_overlay_collection() -> dict[str, Any]:
    payload = _load(OVERLAY_COLLECTION_PATH)
    overlays = payload.get("overlays")
    if not isinstance(overlays, list):
        payload["overlays"] = []
    return payload


def _stage_base() -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "source_lock_only": False,
        "reviewability_stage": True,
        "number_fact_review_batch_stage": True,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "canonical_codex_handoff_root": "codex-output",
    }


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in FALSE_FLAGS}


def _required_false_errors(
    payload: dict[str, Any],
    label: str,
    *,
    allow_true_batch_flags: bool = False,
) -> list[str]:
    allowed = (
        {"assistant_or_operator_number_fact_batch_performed_now", "source_lock_entry_batch_review_performed_now"}
        if allow_true_batch_flags
        else set()
    )
    errors = []
    for key in FALSE_FLAGS:
        if key in allowed:
            continue
        if key in payload and payload[key] is not False:
            errors.append(f"{label}: {key} must be false")
    return errors


def _overlay_only_count(overlays: list[dict[str, Any]], entry_by_path: dict[str, Any]) -> int:
    count = 0
    for overlay in overlays:
        entry = entry_by_path.get(str(overlay.get("source_record_path") or ""))
        if entry is None:
            continue
        raw_ids = {_raw_fact_id(fact) for fact in entry.number_facts}
        if str(overlay.get("source_fact_id") or "") not in raw_ids:
            count += 1
    return count


def _raw_fact_id(raw_fact: dict[str, Any]) -> str:
    for key in ("source_fact_id", "fact_id", "claim_id", "id"):
        value = raw_fact.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def _validate_token_preservation(path_key: str, source_stage_id: str) -> Stage5EDValidationResult:
    payload = _load(TOKEN_PATHS[path_key])
    errors = _expect(payload, {"source_stage_id": source_stage_id, "preserved": True, "rewritten": False})
    return Stage5EDValidationResult(len(errors), _summary_counts(payload), errors)


def _expect(payload: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    return [f"{key} must be {value!r}" for key, value in expected.items() if payload.get(key) != value]


def _summary_counts(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in payload.items()
        if isinstance(value, str | int | float | bool) or value is None
    }


def _format(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _context_contains_stage5ed() -> bool:
    if not CHATGPT_CONTEXT_PATH.exists():
        return False
    return "## Stage 5ED - Number-fact review batch 004" in CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8")


def _update_chatgpt_context() -> None:
    marker = "## Stage 5ED - Number-fact review batch 004"
    text = CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8") if CHATGPT_CONTEXT_PATH.exists() else ""
    legacy_marker = "## Stage 5ED - Number-fact review batch 003"
    if legacy_marker in text:
        text = text.replace(legacy_marker, marker)
        text = text.replace("- Stage 5ED remains the next fact-review batch.", "- Stage 5EE remains the next fact-review batch.")
        CHATGPT_CONTEXT_PATH.write_text(text, encoding="utf-8")
    if marker in text:
        return
    addition = f"""

{marker}

- Stage 5ED reviewed 20 selected DiskCipher/visual-method/route-context source-lock entries and added 25 NumberFactCard overlays only.
- Stage 5ED did not rewrite historical source-lock records, add new source-lock evidence, select a target, generate byte streams, run routes, execute tools, or make a solve claim.
- Durable batch facts: DiskCipher 8-component model, p39 ten-term semantic cluster, doublet 448/89 suppression claim, 167 temporal bridge, Stage 5DN PDD153 56311/WYNN/WAY bridge, solved I/circumference context, Blake seven-subfamily context, 15 Sacred Book overlays, magic-square 1033 precedent, 14 visual motif sections, Page32/full-page hash crosswalk, Page56 128-hex/512-bit hash contract, and dinkus/matrix route-context facts.
- Stage 5EB validation policy remains active: local/full-parallel validation uses 10 workers / 10 pytest workers, and full serial pytest is not part of normal completion.
- The lag5 phenomenon remains not source-locked by Stage 5ED and is only a future lead.
- Stage 5EE should continue number-fact review batch 005 unless a blocking Source Browser issue appears.
"""
    CHATGPT_CONTEXT_PATH.write_text(text.rstrip() + addition + "\n", encoding="utf-8")


def _update_stage_summary_records(summary: dict[str, Any]) -> None:
    payload = read_yaml(STAGE_SUMMARY_RECORDS_PATH)
    if isinstance(payload, dict):
        records = payload.get("records", [])
    else:
        payload = {
            "record_set_id": "stage-summary-records-v0",
            "schema": "schemas/research/stage-summary-record-v0.schema.json",
            "records": [],
        }
        records = []
    if not isinstance(records, list):
        records = []
    records = [record for record in records if not (isinstance(record, dict) and record.get("stage_id") == STAGE_ID)]
    records.append(
        {
            "record_type": "stage_summary_record",
            "stage_id": STAGE_ID,
            "title": STAGE_TITLE,
            "status": "complete",
            "category": "operator_console_reviewability",
            "summary": (
                "Added review-only NumberFactCard overlays for the fourth selected 20-entry "
                "source-lock number-fact review batch."
            ),
            "key_outputs": [
                "Stage 5ED DiskCipher/visual-method/route-context overlay collection with 25 review-only facts.",
                "Stage 5ED review-batch, preservation, loadability, scope, and validation records.",
                "Stage 5EE selected as the next number-fact review batch.",
            ],
            "result_status": "reviewability_overlays_only",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                f"Reviewed entries={summary.get('reviewed_entry_count')}, overlays={summary.get('overlay_count')}, "
                f"fact_cards_after={summary.get('fact_card_count_after_stage5ed')}. Historical source locks were not rewritten."
            ),
        }
    )
    payload["records"] = records
    write_yaml(STAGE_SUMMARY_RECORDS_PATH, payload)


def _update_doc_staleness_source_of_truth() -> None:
    payload = read_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH)
    if not isinstance(payload, dict):
        return
    payload["latest_completed_stage_after_this_stage"] = STAGE_TITLE
    payload["latest_completed_stage_prefix"] = "Stage 5ED"
    payload["next_stage_after_this_stage"] = NEXT_STAGE_TITLE
    payload["expected_next_stage_prefix"] = "Stage 5EE"
    payload["expected_latest_after_stage5ah"] = STAGE_TITLE
    payload["expected_next_after_stage5ah"] = NEXT_STAGE_TITLE
    write_yaml(DOC_STALENESS_SOURCE_OF_TRUTH_PATH, payload)


def _update_operational_file_map() -> None:
    payload = read_yaml(OPERATIONAL_FILE_MAP_PATH)
    if not isinstance(payload, dict):
        return
    records = payload.get("records")
    if not isinstance(records, list):
        return
    strict_paths = {
        "README.md",
        "STATUS.md",
        "ROADMAP.md",
        "AGENTS.md",
        "TESTING.md",
        "ChatGPT-ContextFile.md",
        "docs/roadmap/staged-plan.md",
        "docs/onboarding/start-here.md",
        "docs/onboarding/source-of-truth-map.md",
        "docs/onboarding/operational-file-map.md",
        "docs/reference/token-block-cli.md",
        "docs/operator-console/source-browser-v0.md",
        "data/project-state/current-stage-state.yaml",
    }
    for record in records:
        if isinstance(record, dict) and record.get("path") in strict_paths:
            record["last_meaningful_update_stage"] = STAGE_ID
    write_yaml(OPERATIONAL_FILE_MAP_PATH, payload)


def _write_codex_completion(summary: dict[str, Any]) -> None:
    CODEX_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    text = f"""# Stage 5ED Codex Completion

- stage_id: {STAGE_ID}
- stage_title: {STAGE_TITLE}
- starting_commit: {PREVIOUS_STAGE_FINAL_COMMIT}
- reviewed_entries: {summary.get('reviewed_entry_count')}
- overlays: {summary.get('overlay_count')}
- source_browser_validation_errors: {summary.get('source_browser_validation_error_count')}
- local_parallel_default_workers: {summary.get('local_parallel_default_workers')}
- local_parallel_default_pytest_workers: {summary.get('local_parallel_default_pytest_workers')}
- full_serial_pytest_required_for_normal_stage_completion: false
- historical_source_lock_records_rewritten: false
- source_lock_evidence_updated_now: false
- target_selected: false
- route_extraction_performed_now: false
- real_byte_stream_generated: false
- execution_performed: false
- cuda_execution_performed: false
- solve_claim: false
- recommended_next_stage_id: {NEXT_STAGE_ID}
"""
    (CODEX_OUTPUT_DIR / "stage5ed-codex-completion.md").write_text(text, encoding="utf-8")
