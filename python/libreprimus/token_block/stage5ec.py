"""Stage 5EC number-fact review batch 003 overlays.

This stage is reviewability metadata only. It adds Source Browser
NumberFactCard overlays for a selected triangle/Page32/token/music/self-reference
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

STAGE_ID = "stage-5ec"
STAGE_TOKEN = "stage5ec"
STAGE_TITLE = (
    "Stage 5EC - Source-lock number-fact review batch 003, triangle / Page32 / "
    "token-static / music / self-reference enrichment overlays, without execution"
)
PROMPT_TYPE = "assistant_or_operator_review_then_codex_overlay_update"
PREVIOUS_STAGE_ID = "stage-5eb"
PREVIOUS_STAGE_FINAL_COMMIT = "0881db701c3515433360b1772337857cc4acbcd4"
PREVIOUS_STAGE_ISSUE = 163
PREVIOUS_STAGE_CI_RUN = 27340480456
PREVIOUS_STAGE_CI_STATUS = "passed"
NEXT_STAGE_ID = "stage-5ed"
NEXT_STAGE_TITLE = "Stage 5ED - Source-lock number-fact review batch 004, without execution"
REVIEW_BATCH_ID = "number_fact_review_batch_003_triangle_page32_token_music"
REVIEW_BATCH_SELECTION_POLICY = "assistant_operator_triangle_page32_token_music_self_reference_batch"
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
    "number-fact-overlays/stage5ec-review-batch-003-triangle-page32-token-music-overlays.yaml"
)
REVIEW_BATCH_RESULT_PATH = SOURCE_BROWSER_DIR / (
    "number-fact-review-batches/stage5ec-review-batch-003-triangle-page32-token-music-result.yaml"
)

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5ec-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5ec-next-stage-decision.yaml",
    "review_batch_selection": PROJECT_STATE_DIR / "stage5ec-review-batch-selection.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5ec-reviewable-validation-evidence.yaml",
    "scope_control": PROJECT_STATE_DIR / "stage5ec-scope-control.yaml",
    "source_browser_loadability": PROJECT_STATE_DIR / "stage5ec-source-browser-loadability-summary.yaml",
    "stage5eb_preservation": PROJECT_STATE_DIR / "stage5ec-stage5eb-preservation.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage5ec-chatgpt-context-update-summary.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5ec-reviewability-gap-register.yaml",
    "current_stage_state": PROJECT_STATE_DIR / "current-stage-state.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "token_stage5eb_preservation": TOKEN_BLOCK_DIR / "stage5ec-stage5eb-preservation.yaml",
    "stage5dx_preservation": TOKEN_BLOCK_DIR / "stage5ec-stage5dx-preservation.yaml",
    "stage5dw_preservation": TOKEN_BLOCK_DIR / "stage5ec-stage5dw-preservation.yaml",
    "stage5dv_preservation": TOKEN_BLOCK_DIR / "stage5ec-stage5dv-preservation.yaml",
    "stage5du_preservation": TOKEN_BLOCK_DIR / "stage5ec-stage5du-preservation.yaml",
    "stage5dg_preservation": TOKEN_BLOCK_DIR / "stage5ec-stage5dg-preservation.yaml",
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5ec-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5ec-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5ec-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR / "stage5ec-no-byte-stream-transition-proof.yaml",
    "no_execution_transition_proof": TOKEN_BLOCK_DIR / "stage5ec-no-execution-transition-proof.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5ec-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5ec-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5ec-raw-source-noncommit-proof.yaml",
}

DATA_PATHS: dict[str, Path] = {
    **PROJECT_STATE_PATHS,
    "review_batch_result": REVIEW_BATCH_RESULT_PATH,
    **TOKEN_PATHS,
    **SOURCE_HARVESTER_PATHS,
}

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5ec-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5ec-next-stage-decision-v0.schema.json"),
    "review_batch_selection": Path("schemas/project-state/stage5ec-review-batch-selection-v0.schema.json"),
    "reviewable_validation_evidence": Path(
        "schemas/project-state/stage5ec-reviewable-validation-evidence-v0.schema.json"
    ),
    "scope_control": Path("schemas/project-state/stage5ec-scope-control-v0.schema.json"),
    "review_batch_result": Path(
        "schemas/operator-console/stage5ec-source-browser-number-fact-review-batch-result-v0.schema.json"
    ),
    "overlay_collection": Path(
        "schemas/operator-console/stage5ec-source-browser-number-fact-overlay-collection-v0.schema.json"
    ),
}

SCHEMA_BY_DATA_KEY: dict[str, str] = {
    "summary": "summary",
    "next_stage_decision": "next_stage_decision",
    "review_batch_selection": "review_batch_selection",
    "reviewable_validation_evidence": "reviewable_validation_evidence",
    "scope_control": "scope_control",
    "review_batch_result": "review_batch_result",
}

SELECTED_SOURCE_RECORD_PATHS = [
    "data/historical-route/stage5dl-number-triangle-v1-source-lock.yaml",
    "data/historical-route/stage5dl-triangle-way-anchor-source-lock.yaml",
    "data/historical-route/stage5dl-triangle-prime-mask-source-lock.yaml",
    "data/historical-route/stage5dl-triangle-2016-prime-layer-source-lock.yaml",
    "data/historical-route/stage5dl-triangle-fibonacci-prime-index-source-lock.yaml",
    "data/historical-route/stage5dl-triangle-56311-wynn-way-source-lock.yaml",
    "data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml",
    "data/historical-route/stage5ds-token-block-machine-code-static-sanity-candidate-v0.yaml",
    "data/historical-route/stage5ds-token-block-base-neighbor-static-scan-v0.yaml",
    "data/historical-route/stage5ds-interconnectedness-table-canon-29-note-gp-mapping-v1.yaml",
    "data/historical-route/stage5ds-instar-205-beats-prime205-1259-poem-line-v1.yaml",
    "data/historical-route/stage5ds-interconnectedness-guitar-tab-prime-fret-strings-v1.yaml",
    "data/historical-route/stage5ds-interconnectedness-547-beats-137-measures-v0.yaml",
    "data/historical-route/stage5ds-strange-loop-gp463-page32-bridge-candidate-v0.yaml",
    "data/historical-route/stage5ds-self-reference-gp529-square23-candidate-v0.yaml",
    "data/historical-route/stage5ds-self-fulfilling-prophecy-gp841-square29-candidate-v0.yaml",
    "data/historical-route/stage5ds-infinite-loop-gp409-page33-dot-bridge-candidate-v0.yaml",
    "data/historical-route/stage5ds-three-hares-rotational-shared-parts-candidate-v0.yaml",
    "data/historical-route/stage5ds-mobius-ouroboros-one-boundary-transform-candidate-v1.yaml",
    "data/historical-route/stage5ds-token-block-vm-or-table-surface-candidate-v0.yaml",
]

FALSE_FLAGS = {
    "activation_authorized_now",
    "activation_decision_valid_now",
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "active_token_block_manifest_changed",
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

STAGE5EC_OVERLAY_YAML = r"""
- overlay_id: stage5ec_pdd153_triangle_t17_center41_overlay
  source_record_path: data/historical-route/stage5dl-number-triangle-v1-source-lock.yaml
  source_fact_id: pdd153_t17_center41
  fact_class: pdd_153_triangle_number_facts
  display_label: PDD triangle body has 153 words = T17, arranged as 17 rows with center word 41
  short_label: PDD153 = T17; center=41
  value: 153
  values: [153, 17, 41]
  value_type: word_count
  operation_type: source_observation
  expression: 153 = 17*18/2; 17-row triangular surface; center word position claimed as 41.
  relation: Defines the core PDD-153 triangular route surface used by later WAY / 56311 / prime-mask candidates.
  why_stored: This is the base surface fact; without it, later route/offset facts are not reviewable.
  verification_status: canonical_transcript_required
  display_priority: high
  source_paths: [data/historical-route/stage5dl-number-triangle-v1-source-lock.yaml]
  crosslinks: [pdd_153_triangle_word_prime_route_v1, pdd_153_triangle_way_anchor_route_v1]
  risk_notes: [exact_153_word_window_must_be_canonicalized, heading_boundary_policy_required, route_extraction_not_performed]
- overlay_id: stage5ec_pdd153_single_rune_positions_overlay
  source_record_path: data/historical-route/stage5dl-number-triangle-v1-source-lock.yaml
  source_fact_id: pdd153_single_rune_positions
  fact_class: pdd_153_triangle_number_facts
  display_label: PDD153 single-rune word positions are 25, 41, 53, 91, and 106
  short_label: PDD single-rune positions 25/41/53/91/106
  value: 41
  values: [25, 41, 53, 91, 106]
  value_type: sequence
  operation_type: source_observation
  expression: Source-lock records single-rune word positions as 25, 41, 53, 91, 106.
  relation: Candidate anchors for bounded route starts/controls, including the center-WYNN position 41.
  why_stored: These are compact anchor positions likely to matter in route design and should be visible as fact cards.
  verification_status: canonical_transcript_required
  display_priority: high
  source_paths: [data/historical-route/stage5dl-number-triangle-v1-source-lock.yaml]
  crosslinks: [pdd_153_triangle_56311_wynn_way_route_v1]
  risk_notes: [canonical_transcription_required, anchor_selection_must_be_controlled]
- overlay_id: stage5ec_pdd153_way_anchor_heading_minus_word52_overlay
  source_record_path: data/historical-route/stage5dl-triangle-way-anchor-source-lock.yaml
  source_fact_id: pdd153_way_anchor_heading_minus_reversed_word52
  fact_class: pdd_153_triangle_number_facts
  display_label: PDD heading values 13/23/2 minus reversed word52 values 6/28/5 produce WAY values 7/24/26
  short_label: PDD heading - reverse(word52) = WAY
  value: 52
  values: [13, 23, 2, 5, 28, 6, 6, 28, 5, 7, 24, 26, 52]
  value_type: sequence
  operation_type: sequence_mapping
  expression: "[13,23,2] - [6,28,5] mod 29 = [7,24,26] = WAY."
  relation: Strong instruction-level partial result for the PDD-153 triangle surface.
  why_stored: This is the cleanest triangle arithmetic result and must remain reviewable without opening route execution.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  source_paths: [data/historical-route/stage5dl-triangle-way-anchor-source-lock.yaml]
  crosslinks: [pdd_153_triangle_word_prime_route_v1, pdd_153_triangle_56311_wynn_way_route_v1]
  risk_notes: [heading_transcription_must_be_P_D_TH_not_EOH_D_TH, exact_word52_transcription_required, accepted_as_plaintext_false, route_extraction_not_performed]
- overlay_id: stage5ec_pdd153_prime_mask_present_missing_overlay
  source_record_path: data/historical-route/stage5dl-triangle-prime-mask-source-lock.yaml
  source_fact_id: pdd153_prime_mask_present_missing_under153
  fact_class: pdd_153_triangle_number_facts
  display_label: PDD153 prime mask records 20 present primes and 16 missing primes under 153
  short_label: "PDD prime mask: 20 present / 16 missing"
  value: 20
  values: [20, 16, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151]
  value_type: sequence
  operation_type: source_observation
  expression: "Present primes under 153: 20 values through 71; missing primes under 153: 16 values from 73 through 151."
  relation: Candidate mask family for distinguishing surface-visible vs absent/negative-space prime positions.
  why_stored: Prime presence/absence is a concrete number layer connected to the triangle surface.
  verification_status: arithmetic_verified_metadata_only
  display_priority: medium
  source_paths: [data/historical-route/stage5dl-triangle-prime-mask-source-lock.yaml]
  crosslinks: [pdd_153_triangle_word_prime_route_v1, lp_negative_space_layout_candidate_family_v0]
  risk_notes: [mask_use_not_authorized_now, prime_position_policy_must_be_predeclared]
- overlay_id: stage5ec_pdd153_2016_prime_layer_overlay
  source_record_path: data/historical-route/stage5dl-triangle-2016-prime-layer-source-lock.yaml
  source_fact_id: pdd153_2016_prime_layer
  fact_class: pdd_153_triangle_number_facts
  display_label: PDD triangle has a 2016-message prime-layer candidate linked to words/map/road/numbers-direction
  short_label: PDD 2016 prime-layer candidate
  value: 2016
  values: [2016, 153]
  value_type: sequence
  operation_type: source_observation
  expression: 2016 message route-meta clue is carried as a prime-layer / route-context candidate over the 153-word triangle.
  relation: Connects PDD-153 route interpretation to the solved/verified 2016 words/map/numbers-direction clue family.
  why_stored: Keeps the 2016 route-meta clue visible as method context rather than treating triangle as standalone numerology.
  verification_status: canonical_source_required
  display_priority: medium
  source_paths: [data/historical-route/stage5dl-triangle-2016-prime-layer-source-lock.yaml]
  crosslinks: [2016_message_route_meta_clue_v0, pdd_153_triangle_word_prime_route_v1]
  risk_notes: [source_context_not_route_execution, no_prime_layer_output_generated]
- overlay_id: stage5ec_pdd153_fibonacci_prime_index_route_overlay
  source_record_path: data/historical-route/stage5dl-triangle-fibonacci-prime-index-source-lock.yaml
  source_fact_id: pdd153_fibonacci_prime_index_route_candidate
  fact_class: pdd_153_triangle_number_facts
  display_label: PDD153 has a Fibonacci-prime-index route candidate for future bounded comparison
  short_label: PDD Fibonacci-prime-index route candidate
  value: 153
  values: [153, 17]
  value_type: sequence
  operation_type: source_observation
  expression: PDD153 source-lock carries Fibonacci-prime-index route family as a future candidate over the 17-row / 153-word surface.
  relation: Bridges PDD153 to Page32's Fibonacci-prime-index spiral family.
  why_stored: This is the triangle-side counterpart to the Page32 Fibonacci-prime-index grid and should be visible in review.
  verification_status: canonical_transcript_required
  display_priority: medium
  source_paths: [data/historical-route/stage5dl-triangle-fibonacci-prime-index-source-lock.yaml]
  crosslinks: [page32_moebius_fibonacci_prime_index_spiral_v1, pdd_153_triangle_word_prime_route_v1]
  risk_notes: [route_stream_not_generated, comparison_only_until_experiment_authorized]
- overlay_id: stage5ec_pdd153_stage5dl_56311_wynn_way_overlay
  source_record_path: data/historical-route/stage5dl-triangle-56311-wynn-way-source-lock.yaml
  source_fact_id: pdd153_stage5dl_56311_center41_word52
  fact_class: pdd_153_triangle_number_facts
  display_label: Stage 5DL records 56311 from center word 41/WYNN to word52/WAY anchor
  short_label: Stage5DL 56311 center41 -> word52
  value: 52
  values: [5, 6, 3, 11, 41, 46, 52, 55, 66, 5, 11, 14, 25]
  value_type: sequence
  operation_type: sequence_mapping
  expression: Center 41 plus cumulative offsets 5,11,14,25 gives 46,52,55,66; word52 is WAY anchor.
  relation: Direct Stage 5DL triangle-side version of the later DiskCipher/WYNN/WAY bridge.
  why_stored: Prevents the 56311 relation from appearing only as a DiskCipher support fact.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  source_paths: [data/historical-route/stage5dl-triangle-56311-wynn-way-source-lock.yaml]
  crosslinks: [disk_56311_wynn_way_bridge_v1, pdd_153_triangle_way_anchor_route_v1]
  risk_notes: [route_extraction_not_performed, no_route_stream_generated]
- overlay_id: stage5ec_page32_grid_spiral_values_overlay
  source_record_path: data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml
  source_fact_id: page32_grid_spiral_values
  fact_class: page32_moebius_number_facts
  display_label: Page32 4x4 grid spiral starts 3299 and reaches 2472 after 12 cells
  short_label: Page32 spiral 3299 -> 2472
  value: 3299
  values: [3299, 3298, 3296, 3294, 3288, 3278, 3258, 3222, 3152, 3038, 2838, 2472, 1820, 708, 1206, 4516]
  value_type: sequence
  operation_type: matrix_grid_match
  expression: "Spiral route values: 3299,3298,3296,3294,3288,3278,3258,3222,3152,3038,2838,2472,1820,708,1206,4516."
  relation: Core Page32 Moebius/Fibonacci-prime grid surface; red-header facts select 3299 and 2472 in related records.
  why_stored: This is the Page32 numeric route surface itself and needs a fact-card display independent of red-header overlays.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  source_paths: [data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml]
  crosslinks: [page32_red_header_progressive_gp_sum_2472_v1, page32_red_header_cumulative_index_463_3299_candidate_v1]
  risk_notes: [route_extraction_not_performed, red_header_selected_segment_not_executed]
- overlay_id: stage5ec_page32_prime_indices_fibonacci_increments_overlay
  source_record_path: data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml
  source_fact_id: page32_prime_indices_fibonacci_increments
  fact_class: page32_moebius_number_facts
  display_label: Page32 prime-index sequence 1/2/3/4/6/.../988 has Fibonacci-like increments
  short_label: Page32 prime-index Fibonacci increments
  value: 988
  values: [1, 2, 3, 4, 6, 9, 14, 22, 35, 56, 90, 145, 234, 378, 611, 988, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
  value_type: sequence
  operation_type: prime_index_lookup
  expression: Prime-index sequence has increments +1,+1,+1,+2,+3,+5,+8,+13,+21,+34,+55,+89,+144,+233,+377.
  relation: Encodes the Fibonacci-prime-index rule behind the Page32 grid values.
  why_stored: Operators need to see the generating sequence, not just the final 4x4 numbers.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  source_paths: [data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml]
  crosslinks: [page32_fibonacci_mod29_prime_palindrome_candidate_v0, pdd_153_triangle_fibonacci_prime_index_route_v1]
  risk_notes: [prime_index_convention_must_be_declared, not_a_direct_plaintext_route]
- overlay_id: stage5ec_page32_mod153_bridge_overlay
  source_record_path: data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml
  source_fact_id: page32_prime_index_and_value_mod153_bridge
  fact_class: page32_moebius_number_facts
  display_label: Page32 prime-index/value sequences have mod-153 projections for PDD comparison
  short_label: Page32 mod153 bridge vectors
  value: 153
  values: [1, 2, 3, 4, 6, 9, 14, 22, 35, 56, 90, 145, 81, 72, 152, 70, 86, 85, 83, 81, 75, 65, 45, 9, 92, 131, 84, 24, 137, 96, 135, 79]
  value_type: modular_residue
  operation_type: modulo
  expression: Prime-index mod153 vector and grid-value mod153 vector are carried as future-only PDD comparison context.
  relation: Potential bridge between Page32 route scheduler and the PDD153 triangle surface.
  why_stored: Makes the Page32/PDD cross-surface design note visible without generating any route output.
  verification_status: arithmetic_verified_metadata_only
  display_priority: medium
  source_paths: [data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml]
  crosslinks: [pdd_153_triangle_word_prime_route_v1, page32_red_header_anchored_3299_to_2472_route_candidate]
  risk_notes: [future_comparison_only, no_pdd_route_stream_generated]
- overlay_id: stage5ec_token_block_primary60_byte_surface_overlay
  source_record_path: data/historical-route/stage5ds-token-block-machine-code-static-sanity-candidate-v0.yaml
  source_fact_id: token_block_primary60_byte_surface
  fact_class: token_block_static_number_facts
  display_label: Token-block primary60 surface is 32x8 = 256 tokens with 161 unique values
  short_label: Token-block 32x8=256; unique=161
  value: 256
  values: [32, 8, 256, 161, 60, 0, 255]
  value_type: sequence
  operation_type: base_conversion
  expression: 32 rows * 8 columns = 256 tokens; primary60 maps 00->0 and 4F->255; unique token/byte count = 161.
  relation: Defines the token-block as a byte-like data surface rather than literal hex.
  why_stored: This is the core token-block static fact needed for future review.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  source_paths: [data/historical-route/stage5ds-token-block-machine-code-static-sanity-candidate-v0.yaml, data/token-block/stage5ap-token-block-canonical-transcription.yaml]
  crosslinks: [token_block_matrix_context_v0]
  risk_notes: [byte_stream_generation_not_authorized, variant_enumeration_not_performed, not_hex_key_claim]
- overlay_id: stage5ec_token_block_x86_lret_out_sanity_overlay
  source_record_path: data/historical-route/stage5ds-token-block-machine-code-static-sanity-candidate-v0.yaml
  source_fact_id: token_block_x86_lret_out_sanity
  fact_class: token_block_static_number_facts
  display_label: Primary60 row-major bytes begin with CB E7; x86 interpretation starts lret/out and likely faults
  short_label: "x86 sanity: starts CB E7 = lret/out"
  value: cbe7
  values: [cb, e7, cbe7a7ba61ed7eb75cf99cdef704b7d4]
  value_type: sequence
  operation_type: source_observation
  expression: First bytes cbe7a7ba61ed7eb75cf99cdef704b7d4; x86/x86-64 offset-0 interpretation starts with lret then privileged I/O-like behavior.
  relation: Static sanity check lowering native-machine-code likelihood while leaving VM/table interpretation open.
  why_stored: Prevents future reviewers from re-litigating native-code execution from byte 0 without a new architecture clue.
  verification_status: operator_assistant_observed
  display_priority: medium
  source_paths: [data/historical-route/stage5ds-token-block-machine-code-static-sanity-candidate-v0.yaml]
  crosslinks: [token_block_vm_or_table_surface_candidate_v0]
  risk_notes: [native_code_execution_not_performed, disassembly_shape_not_solve_evidence, architecture_unspecified]
- overlay_id: stage5ec_token_block_base_neighbor_scan_overlay
  source_record_path: data/historical-route/stage5ds-token-block-base-neighbor-static-scan-v0.yaml
  source_fact_id: token_block_base58_64_neighbor_scan
  fact_class: token_block_static_number_facts
  display_label: Base60 is clean; base58/base59 invalid; base61-64 overflow byte range without wrapping
  short_label: "Base scan: 58/59 invalid, 60 clean, 61-64 overflow"
  value: 60
  values: [58, 59, 60, 61, 62, 63, 64]
  value_type: sequence
  operation_type: base_conversion
  expression: base58/base59 invalid due suffix x index 59; base60 clean; base61-base64 require overflow/modulo wrapping.
  relation: Constrains token-block byte interpretation to primary60 unless a source-backed wrap rule appears.
  why_stored: Base choice is a critical future experiment variable and should be visible in the Source Browser.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  source_paths: [data/historical-route/stage5ds-token-block-base-neighbor-static-scan-v0.yaml]
  crosslinks: [token_block_machine_code_static_sanity_candidate_v0]
  risk_notes: [wrap_rules_not_authorized, byte_stream_generation_not_authorized]
- overlay_id: stage5ec_token_block_vm_table_surface_review_overlay
  source_record_path: data/historical-route/stage5ds-token-block-vm-or-table-surface-candidate-v0.yaml
  source_fact_id: token_block_vm_table_surface_review
  fact_class: token_block_static_number_facts
  display_label: Token-block is more likely VM/table/key-schedule surface than native CPU code
  short_label: Token-block VM/table surface candidate
  value: 256
  values: [32, 8, 256, 161]
  value_type: sequence
  operation_type: source_observation
  expression: 32x8 / 256-token / 161-unique surface is interpreted as VM/table/key-schedule candidate, not accepted native code.
  relation: Preserves the current static role hypothesis for the token block.
  why_stored: Useful review context even though it is not a direct arithmetic proof.
  verification_status: operator_assistant_observed
  display_priority: medium
  source_paths: [data/historical-route/stage5ds-token-block-vm-or-table-surface-candidate-v0.yaml]
  crosslinks: [token_block_matrix_context_v0]
  risk_notes: [conceptual_role_hypothesis_only, no_vm_instruction_set_source_locked, no_execution]
- overlay_id: stage5ec_interconnectedness_table_canon_29_note_overlay
  source_record_path: data/historical-route/stage5ds-interconnectedness-table-canon-29-note-gp-mapping-v1.yaml
  source_fact_id: interconnectedness_table_canon_29_note_mapping
  fact_class: music_number_facts
  display_label: Interconnectedness table/canon claim has 29-note inventory matching GP alphabet size
  short_label: Interconnectedness table canon -> 29 notes
  value: 29
  values: [19, 29]
  value_type: sequence
  operation_type: source_observation
  expression: Community theory claims original unique-note count 19 and table-canon unique-note count 29.
  relation: Music-side bridge to the 29-token GP alphabet, with direct pitch substitution quarantined.
  why_stored: The 29-note claim is the most reviewable numeric piece of the table/canon mapping candidate.
  verification_status: canonical_source_required
  display_priority: medium
  source_paths: [data/historical-route/stage5ds-interconnectedness-table-canon-29-note-gp-mapping-v1.yaml, third_party/CicadaMusic/community-theory/messages.txt]
  crosslinks: [music_transform_grammar_for_cipher_methods_candidate_v1]
  risk_notes: [canonical_musicxml_or_midi_required, note_inventory_policy_required, direct_pitch_substitution_low_value_warning]
- overlay_id: stage5ec_instar_205_prime205_1259_overlay
  source_record_path: data/historical-route/stage5ds-instar-205-beats-prime205-1259-poem-line-v1.yaml
  source_fact_id: instar_205_prime205_1259
  fact_class: music_number_facts
  display_label: Instar beat-count claim 205 maps by prime(205)=1259 to the first parable line GP sum
  short_label: Instar 205 beats -> prime(205)=1259
  value: 1259
  values: [205, 1259]
  value_type: prime_index
  operation_type: prime_index_lookup
  expression: prime(205)=1259; LIKE THE INSTAR TUNNELING TO THE SURFACE has GP sum 1259.
  relation: Links community beat-count claim to the first Instar parable GP line.
  why_stored: Compact music-number bridge, but beat count needs canonical transcription verification.
  verification_status: canonical_source_required
  display_priority: medium
  source_paths: [data/historical-route/stage5ds-instar-205-beats-prime205-1259-poem-line-v1.yaml]
  crosslinks: [instar_parable_id3_gp_product_candidate_v1]
  risk_notes: [beat_count_not_verified_now, canonical_audio_or_score_required, route_extraction_not_performed]
- overlay_id: stage5ec_interconnectedness_guitar_tab_prime_strings_overlay
  source_record_path: data/historical-route/stage5ds-interconnectedness-guitar-tab-prime-fret-strings-v1.yaml
  source_fact_id: interconnectedness_guitar_tab_prime_fret_strings
  fact_class: music_number_facts
  display_label: Interconnectedness guitar-tab thread lists multiple prime fret-number strings and 32023=31x1033
  short_label: Guitar-tab prime strings; 32023=31x1033
  value: 32023
  values: [355330003553333, 37302523, 230032303, 53033303, 230303, 333032303, 300323, 252323, 32303, 353, 32023, 31, 1033]
  value_type: sequence
  operation_type: factorization
  expression: Several fret strings are prime; nonprime 32023 factors as 31 * 1033.
  relation: Music/thread arithmetic candidate linked to 1033/3301 number family.
  why_stored: Preserves a concrete table/string arithmetic family while warning about tab-boundary dependence.
  verification_status: arithmetic_verified_metadata_only
  display_priority: medium
  source_paths: [data/historical-route/stage5ds-interconnectedness-guitar-tab-prime-fret-strings-v1.yaml, third_party/CicadaMusic/community-theory/messages.txt]
  crosslinks: [prime_index_bridge_761_167_464_1033_3301_candidate_v0]
  risk_notes: [canonical_tab_required, bar_boundary_policy_required, string_order_policy_required, source_selection_bias_warning]
- overlay_id: stage5ec_interconnectedness_547_137_overlay
  source_record_path: data/historical-route/stage5ds-interconnectedness-547-beats-137-measures-v0.yaml
  source_fact_id: interconnectedness_547_beats_137_measures
  fact_class: music_number_facts
  display_label: Interconnectedness community claim records 547 beats and 137 measures
  short_label: Interconnectedness 547 beats / 137 measures
  value: 547
  values: [547, 137]
  value_type: sequence
  operation_type: source_observation
  expression: Community theory claims Interconnectedness beat count 547 and 137-measure structure.
  relation: Potential bridge to ALONG THE WAY=547 and route/canon timing context.
  why_stored: Keeps the 547/137 timing claim visible but clearly unverified.
  verification_status: canonical_source_required
  display_priority: low
  source_paths: [data/historical-route/stage5ds-interconnectedness-547-beats-137-measures-v0.yaml]
  crosslinks: [music_transform_grammar_for_cipher_methods_candidate_v1, page15_internal_instruction_number_facts]
  risk_notes: [beat_measure_count_requires_canonical_score, low_confidence_until_transcription]
- overlay_id: stage5ec_strange_loop_463_page32_overlay
  source_record_path: data/historical-route/stage5ds-strange-loop-gp463-page32-bridge-candidate-v0.yaml
  source_fact_id: strange_loop_gp463_page32_bridge
  fact_class: ouroboros_self_reference_number_facts
  display_label: STRANGE LOOP has GP sum 463, linking self-reference context to Page32 463->3299
  short_label: STRANGE LOOP=463 -> Page32 463/3299
  value: 463
  values: [463, 3299]
  value_type: gp_sum
  operation_type: symbolic_gp_scan
  expression: STRANGE LOOP = 463; Page32 red-header cumulative-index bridge uses 463 -> prime(463)=3299.
  relation: Self-reference vocabulary lands on the Page32 463/3299 number bridge.
  why_stored: This is the strongest Ouroboros-see-also arithmetic crosslink to an existing Page32 fact.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  source_paths: [data/historical-route/stage5ds-strange-loop-gp463-page32-bridge-candidate-v0.yaml]
  crosslinks: [page32_red_header_cumulative_index_463_3299_candidate_v1]
  risk_notes: [symbolic_context_not_proof, phrase_selection_bias_warning]
- overlay_id: stage5ec_self_reference_529_square23_overlay
  source_record_path: data/historical-route/stage5ds-self-reference-gp529-square23-candidate-v0.yaml
  source_fact_id: self_reference_gp529_square23
  fact_class: ouroboros_self_reference_number_facts
  display_label: SELF REFERENCE has GP sum 529 = 23^2
  short_label: SELF REFERENCE=529=23^2
  value: 529
  values: [529, 23, 23]
  value_type: gp_sum
  operation_type: factorization
  expression: SELF REFERENCE = 529 = 23 * 23.
  relation: Contextual self-reference / quine / ouroboros vocabulary linked to GP square structure.
  why_stored: Useful context for fixed-point/route-output-as-instruction hypotheses, but not proof.
  verification_status: arithmetic_verified_metadata_only
  display_priority: medium
  source_paths: [data/historical-route/stage5ds-self-reference-gp529-square23-candidate-v0.yaml]
  crosslinks: [quine_fixed_point_self_reproduction_candidate_v0, solved_i_voice_of_circumference_precedent_v0]
  risk_notes: [symbolic_context_only, phrase_selection_bias_warning]
- overlay_id: stage5ec_self_fulfilling_prophecy_841_square29_overlay
  source_record_path: data/historical-route/stage5ds-self-fulfilling-prophecy-gp841-square29-candidate-v0.yaml
  source_fact_id: self_fulfilling_prophecy_gp841_square29
  fact_class: ouroboros_self_reference_number_facts
  display_label: SELF FULFILLING PROPHECY has GP sum 841 = 29^2
  short_label: SELF FULFILLING PROPHECY=841=29^2
  value: 841
  values: [841, 29, 29]
  value_type: gp_sum
  operation_type: factorization
  expression: SELF FULFILLING PROPHECY = 841 = 29 * 29.
  relation: Self-producing / fixed-point vocabulary lands on the full GP alphabet square.
  why_stored: Elegant symbolic arithmetic, but must stay quarantined from priority decisions unless independently constrained.
  verification_status: arithmetic_verified_metadata_only
  display_priority: medium
  source_paths: [data/historical-route/stage5ds-self-fulfilling-prophecy-gp841-square29-candidate-v0.yaml]
  crosslinks: [quine_fixed_point_self_reproduction_candidate_v0]
  risk_notes: [phrase_selection_bias_warning, symbolic_context_not_execution_seed]
- overlay_id: stage5ec_infinite_loop_409_page33_dot_overlay
  source_record_path: data/historical-route/stage5ds-infinite-loop-gp409-page33-dot-bridge-candidate-v0.yaml
  source_fact_id: infinite_loop_gp409_page33_dot_bridge
  fact_class: ouroboros_self_reference_number_facts
  display_label: INFINITE LOOP has GP sum 409, crosslinked to Page33 dot-distance candidate
  short_label: INFINITE LOOP=409
  value: 409
  values: [409]
  value_type: gp_sum
  operation_type: symbolic_gp_scan
  expression: INFINITE LOOP = 409 under GP; crosslinked to Page33 three-dot geometry/distance candidate.
  relation: Loop vocabulary attaches to an already-source-locked dot/geometry number.
  why_stored: Preserves a compact loop/dot bridge while keeping mythology/context from driving experiments.
  verification_status: arithmetic_verified_metadata_only
  display_priority: low
  source_paths: [data/historical-route/stage5ds-infinite-loop-gp409-page33-dot-bridge-candidate-v0.yaml]
  crosslinks: [page33_three_dot_emirp_area_block_candidate_v0]
  risk_notes: [symbolic_context_only, not_target_priority_evidence_now]
- overlay_id: stage5ec_three_hares_401_rotational_overlay
  source_record_path: data/historical-route/stage5ds-three-hares-rotational-shared-parts-candidate-v0.yaml
  source_fact_id: three_hares_gp401_rotational_shared_parts
  fact_class: ouroboros_self_reference_number_facts
  display_label: THREE HARES has GP sum 401 and carries a 3-fold rotational/shared-parts motif
  short_label: THREE HARES=401; 3-fold motif
  value: 401
  values: [401, 3]
  value_type: gp_sum
  operation_type: symbolic_gp_scan
  expression: THREE HARES = 401; motif has threefold rotational/shared-component structure.
  relation: Contextual bridge to dot/threefold/rotation motifs, not a route rule.
  why_stored: Low-priority but useful symbolic/topological context for rotational sharing.
  verification_status: arithmetic_verified_metadata_only
  display_priority: low
  source_paths: [data/historical-route/stage5ds-three-hares-rotational-shared-parts-candidate-v0.yaml]
  crosslinks: [lp_dot_marker_geometry_family_v1]
  risk_notes: [symbolic_context_only, low_priority]
- overlay_id: stage5ec_mobius_strip_423_one_boundary_overlay
  source_record_path: data/historical-route/stage5ds-mobius-ouroboros-one-boundary-transform-candidate-v1.yaml
  source_fact_id: mobius_strip_gp423_one_boundary
  fact_class: ouroboros_self_reference_number_facts
  display_label: MOBIUS STRIP has GP sum 423 and one-boundary / half-twist transform context
  short_label: MOBIUS STRIP=423; one boundary
  value: 423
  values: [423, 1, 2]
  value_type: gp_sum
  operation_type: symbolic_gp_scan
  expression: MOBIUS STRIP = 423; concept supplies one boundary and half-twist route vocabulary.
  relation: Bridges Page32 visual Moebius, DiskCipher flip/rotation, and PDD closed-cycle route grammar.
  why_stored: The numeric GP fact is secondary; the one-boundary/half-twist transform context is the real review value.
  verification_status: arithmetic_verified_metadata_only
  display_priority: medium
  source_paths: [data/historical-route/stage5ds-mobius-ouroboros-one-boundary-transform-candidate-v1.yaml]
  crosslinks: [page32_moebius_fibonacci_prime_index_spiral_v1, disk_rule4_mobius_trip_rotation_bridge_v0, pdd_153_56311_ouroboric_cycle_candidate_v0]
  risk_notes: [symbolic_context_not_route_proof, no_mobius_route_executed]
- overlay_id: stage5ec_batch003_triangle_page32_token_music_cluster_summary_overlay
  source_record_path: data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml
  source_fact_id: batch003_triangle_page32_token_music_cluster_summary
  fact_class: batch_summary_number_facts
  display_label: "Batch 003 cluster: PDD153/T17, WAY, 56311, Page32 spiral, token-block 256/161, music 29/205/547, self-reference squares"
  short_label: "Batch003: PDD153/Page32/token/music/self-ref"
  value: 153
  values: [153, 17, 41, 52, 56311, 3299, 2472, 256, 161, 29, 205, 547, 529, 841]
  value_type: sequence
  operation_type: source_observation
  expression: Cluster summary only; see individual overlays for details.
  relation: Compact review chip tying together Stage 5EC's selected source-lock entries.
  why_stored: Improves scanability without replacing detailed fact cards.
  verification_status: reviewed_none_found
  display_priority: low
  source_paths: [data/historical-route/stage5dl-number-triangle-v1-source-lock.yaml, data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml, data/historical-route/stage5ds-token-block-machine-code-static-sanity-candidate-v0.yaml, data/historical-route/stage5ds-interconnectedness-table-canon-29-note-gp-mapping-v1.yaml]
  risk_notes: [summary_card_only, not_independent_evidence]
"""

OVERLAY_ROWS: list[dict[str, Any]] = yaml.safe_load(STAGE5EC_OVERLAY_YAML)


@dataclass
class Stage5ECValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5ec"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5ec() -> dict[str, dict[str, Any]]:
    _write_schemas()
    _write_overlay_collection()
    records = _build_records()
    _write_records(records)
    _update_chatgpt_context()
    _update_stage_summary_records(records["summary"])
    _update_doc_staleness_source_of_truth()
    _update_operational_file_map()
    _write_codex_completion(records["summary"])
    return records


def validate_stage5ec() -> Stage5ECValidationResult:
    checks = [
        validate_stage5ec_review_batch_selection,
        validate_stage5ec_number_fact_overlays,
        validate_stage5ec_overlay_only_support,
        validate_stage5ec_source_browser_loadability,
        validate_stage5ec_stage5eb_preservation,
        validate_stage5ec_stage5dx_preservation,
        validate_stage5ec_stage5dw_preservation,
        validate_stage5ec_stage5dv_preservation,
        validate_stage5ec_stage5du_preservation,
        validate_stage5ec_stage5dg_preservation,
        validate_stage5ec_stage5bd_preservation,
        validate_stage5ec_active_lineage_preservation,
        validate_stage5ec_sidecar_gates,
        validate_stage5ec_handoff_continuity,
        validate_stage5ec_credential_redaction_policy,
        validate_stage5ec_governance_scope,
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
    counts["token_block_stage5ec_valid"] = not errors
    return Stage5ECValidationResult(len(errors), counts, errors)


def validate_stage5ec_review_batch_selection() -> Stage5ECValidationResult:
    payload = _load(PROJECT_STATE_PATHS["review_batch_selection"])
    selected = payload.get("selected_source_record_paths", [])
    errors = []
    if payload.get("review_batch_id") != REVIEW_BATCH_ID:
        errors.append("Stage 5EC review batch id mismatch")
    if payload.get("reviewed_entry_count") != EXPECTED_REVIEWED_ENTRY_COUNT or len(selected) != 20:
        errors.append("Stage 5EC selected batch must contain exactly 20 records")
    if selected != SELECTED_SOURCE_RECORD_PATHS:
        errors.append("Stage 5EC selected source path order/content mismatch")
    errors.extend(f"selected source path missing: {path}" for path in selected if not Path(path).exists())
    if payload.get("review_scope") != "selected_20_source_records_only":
        errors.append("Stage 5EC review scope must be selected_20_source_records_only")
    return Stage5ECValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ec_number_fact_overlays() -> Stage5ECValidationResult:
    collection = _load_overlay_collection()
    overlays = collection.get("overlays", [])
    errors = []
    if collection.get("record_type") != "source_browser_number_fact_enrichment_overlay_collection":
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
    return Stage5ECValidationResult(
        len(errors),
        {
            "overlay_count": len(overlays),
            "reviewed_entry_count": collection.get("reviewed_entry_count"),
            "selected_source_path_count": len(selected),
        },
        errors,
    )


def validate_stage5ec_overlay_only_support() -> Stage5ECValidationResult:
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
        errors.append("Stage 5EC overlays must remain overlay-only review cards")
    return Stage5ECValidationResult(
        len(errors),
        {
            "selected_batch_fact_cards": selected_cards,
            "overlay_only_cards_required_count": overlay_only_cards,
        },
        errors,
    )


def validate_stage5ec_source_browser_loadability() -> Stage5ECValidationResult:
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
    return Stage5ECValidationResult(len(errors), {**result.counts, **path_result.counts, **_summary_counts(payload)}, errors)


def validate_stage5ec_stage5eb_preservation() -> Stage5ECValidationResult:
    payload = _load(PROJECT_STATE_PATHS["stage5eb_preservation"])
    errors = _expect(
        payload,
        {
            "stage5eb_preserved": True,
            "stage5eb_status": "complete",
            "stage5eb_issue": PREVIOUS_STAGE_ISSUE,
            "stage5eb_ci_status": PREVIOUS_STAGE_CI_STATUS,
            "stage5eb_local_parallel_default_workers": 10,
            "stage5eb_local_parallel_default_pytest_workers": 10,
            "full_serial_pytest_required_for_normal_stage_completion": False,
        },
    )
    return Stage5ECValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ec_stage5dx_preservation() -> Stage5ECValidationResult:
    return _validate_token_preservation("stage5dx_preservation", "stage-5dx")


def validate_stage5ec_stage5dw_preservation() -> Stage5ECValidationResult:
    return _validate_token_preservation("stage5dw_preservation", "stage-5dw")


def validate_stage5ec_stage5dv_preservation() -> Stage5ECValidationResult:
    return _validate_token_preservation("stage5dv_preservation", "stage-5dv")


def validate_stage5ec_stage5du_preservation() -> Stage5ECValidationResult:
    return _validate_token_preservation("stage5du_preservation", "stage-5du")


def validate_stage5ec_stage5dg_preservation() -> Stage5ECValidationResult:
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
    return Stage5ECValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ec_stage5bd_preservation() -> Stage5ECValidationResult:
    payload = _load(TOKEN_PATHS["stage5bd_preservation"])
    errors = _expect(payload, {"source_stage_id": "stage-5bd", "stage5bd_run_plan_id_count": 10, "preserved": True})
    return Stage5ECValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ec_active_lineage_preservation() -> Stage5ECValidationResult:
    payload = _load(TOKEN_PATHS["active_lineage_preservation"])
    errors = _expect(payload, {"active_lineage_record_count": 8, "preserved": True})
    return Stage5ECValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ec_sidecar_gates() -> Stage5ECValidationResult:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for key in ("no_active_ingestion_proof", "no_byte_stream_transition_proof", "no_execution_transition_proof"):
        payload = _load(TOKEN_PATHS[key])
        counts[key] = payload.get("gate_status")
        errors.extend(_required_false_errors(payload, TOKEN_PATHS[key].as_posix()))
        if payload.get("gate_status") != "closed":
            errors.append(f"{TOKEN_PATHS[key].as_posix()}: gate_status must be closed")
    return Stage5ECValidationResult(len(errors), counts, errors)


def validate_stage5ec_handoff_continuity() -> Stage5ECValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if payload.get("deprecated_codex_output_root_used") is not False or payload.get("codex_output_used") is not False:
        errors.append("deprecated codex_output root must not be used")
    if Path("codex_output").exists():
        errors.append("deprecated codex_output directory is present")
    return Stage5ECValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ec_credential_redaction_policy() -> Stage5ECValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["credential_redaction_policy_preservation"])
    errors = []
    if payload.get("credential_like_remote_count") != 0:
        errors.append("credential-like remote count must be 0")
    if payload.get("raw_source_body_included") is not False:
        errors.append("credential policy must not include raw source bodies")
    return Stage5ECValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ec_governance_scope() -> Stage5ECValidationResult:
    payload = _load(PROJECT_STATE_PATHS["scope_control"])
    errors = _required_false_errors(payload, PROJECT_STATE_PATHS["scope_control"].as_posix(), allow_true_batch_flags=True)
    if payload.get("source_lock_entry_batch_review_performed_now") is not True:
        errors.append("Stage 5EC must record source_lock_entry_batch_review_performed_now=true")
    if payload.get("assistant_or_operator_number_fact_batch_performed_now") is not True:
        errors.append("Stage 5EC must record assistant_or_operator_number_fact_batch_performed_now=true")
    if payload.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("next stage must be Stage 5ED")
    return Stage5ECValidationResult(len(errors), _summary_counts(payload), errors)


def stage5ec_summary_text() -> str:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5EC summary:",
        f"status={summary.get('status')}",
        f"review_batch_id={summary.get('review_batch_id')}",
        f"reviewed_entry_count={summary.get('reviewed_entry_count')}",
        f"overlay_count={summary.get('overlay_count')}",
        f"overlay_only_fact_cards_supported={summary.get('overlay_only_fact_cards_supported')}",
        f"source_browser_entries_loaded={summary.get('source_browser_entries_loaded')}",
        f"source_browser_records_scanned={summary.get('source_browser_records_scanned')}",
        f"fact_card_count_after_stage5ec={summary.get('fact_card_count_after_stage5ec')}",
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
    base = _stage_base()
    false_flags = _false_flags()

    summary = {
        **base,
        **false_flags,
        "record_type": "stage5ec_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "source_previous_stage_final_commit": PREVIOUS_STAGE_FINAL_COMMIT,
        "source_previous_issue": PREVIOUS_STAGE_ISSUE,
        "source_previous_ci_run": PREVIOUS_STAGE_CI_RUN,
        "source_previous_ci_status": PREVIOUS_STAGE_CI_STATUS,
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
        "fact_card_count_after_stage5ec": fact_card_count_after,
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
            "record_type": "stage5ec_reviewable_validation_evidence",
            "schema": SCHEMA_PATHS["reviewable_validation_evidence"].as_posix(),
            "validators": [
                "validate-stage5ec",
                "validate-stage5ec-review-batch-selection",
                "validate-stage5ec-number-fact-overlays",
                "validate-stage5ec-overlay-only-support",
                "validate-stage5ec-source-browser-loadability",
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
            "record_type": "stage5ec_scope_control",
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
            "record_type": "stage5ec_source_browser_loadability_summary",
            "source_browser_entries_loaded": browser["entries_loaded"],
            "source_browser_records_scanned": browser["records_scanned"],
            "source_browser_validation_error_count": len(source_browser_validation.errors),
            "source_browser_warning_count": browser["warnings"],
            "source_browser_missing_paths_after": browser["missing_paths"],
            "missing_paths_retained_as_warnings": True,
            "fact_card_count_after_stage5ec": fact_card_count_after,
            "spurious_root_image_paths_after": path_report["spurious_root_image_paths"],
            "spurious_root_document_paths_after": path_report["spurious_root_document_paths"],
            "duplicate_present_missing_path_pairs_after": path_report["duplicate_present_missing_path_pairs"],
            "source_root_relative_resolved_paths": path_report["source_root_relative_resolved_paths"],
        },
        "stage5eb_preservation": _stage5eb_preservation_record(base, false_flags, stage5eb),
        "chatgpt_context_update_summary": {
            **base,
            "record_type": "stage5ec_chatgpt_context_update_summary",
            "chatgpt_context_updated": _context_contains_stage5ec(),
            "chatgpt_context_path": CHATGPT_CONTEXT_PATH.as_posix(),
            "durable_facts_added": _context_contains_stage5ec(),
            "raw_source_body_included": False,
            "long_prompt_text_included": False,
        },
        "reviewability_gap_register": {
            **base,
            "record_type": "stage5ec_reviewability_gap_register",
            "remaining_gap": "continue_number_fact_review_batches",
            "next_batch_recommended": "number_fact_review_batch_004",
            "lag5_phenomenon_source_locked_by_stage5ec": False,
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
            "post_push_handoff_locations": ["codex-output/stage5ec-codex-completion.md", "GitHub issue comment"],
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
        "record_type": "stage5ec_next_stage_decision",
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
        "record_type": "stage5ec_review_batch_selection",
        "schema": SCHEMA_PATHS["review_batch_selection"].as_posix(),
        "review_batch_id": REVIEW_BATCH_ID,
        "review_batch_selection_policy": REVIEW_BATCH_SELECTION_POLICY,
        "review_scope": "selected_20_source_records_only",
        "reviewed_entry_count": EXPECTED_REVIEWED_ENTRY_COUNT,
        "selected_source_record_paths": SELECTED_SOURCE_RECORD_PATHS,
        "selection_clusters": ["pdd153_triangle", "page32_moebius", "token_block_static", "music", "self_reference"],
        "historical_source_lock_records_rewritten": False,
        "source_lock_evidence_updated_now": False,
    }


def _stage5eb_preservation_record(
    base: dict[str, Any], false_flags: dict[str, bool], stage5eb: dict[str, Any]
) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5ec_stage5eb_preservation",
        "stage5eb_preserved": True,
        "stage5eb_status": stage5eb.get("status", "complete"),
        "stage5eb_issue": PREVIOUS_STAGE_ISSUE,
        "stage5eb_ci_status": PREVIOUS_STAGE_CI_STATUS,
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
            "record_type": "stage5ec_codex_handoff_policy",
            "canonical_codex_handoff_root": "codex-output",
            "deprecated_codex_output_root_used": False,
            "codex_output_used": False,
            "completion_summary_path": "codex-output/stage5ec-codex-completion.md",
            "completion_summary_committed": False,
        },
        "credential_redaction_policy_preservation": {
            **base,
            "record_type": "stage5ec_credential_redaction_policy_preservation",
            "credential_like_remote_count": 0,
            "credential_redaction_policy_preserved": True,
            "raw_source_body_included": False,
            "secret_material_committed": False,
        },
        "raw_source_noncommit_proof": {
            **base,
            **false_flags,
            "record_type": "stage5ec_raw_source_noncommit_proof",
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
            "record_type": f"stage5ec_{key}",
            "source_stage_id": source_stage,
            "preserved": True,
            "rewritten": False,
            "superseded_now": False,
            "notes": "Stage 5EC records preservation only; it does not mutate historical inputs.",
        }
    records["stage5dg_preservation"] = {
        **base,
        **false_flags,
        "record_type": "stage5ec_stage5dg_preservation",
        "source_stage_id": "stage-5dg",
        "preserved": True,
        "operator_approval_component_satisfied_preserved": True,
        "deep_research_acceptance_created_now": False,
        "combined_approval_gate_satisfied_now": False,
    }
    records["stage5bd_preservation"] = {
        **base,
        **false_flags,
        "record_type": "stage5ec_stage5bd_preservation",
        "source_stage_id": "stage-5bd",
        "preserved": True,
        "stage5bd_run_plan_id_count": 10,
        "stage5bd_run_plan_ids_preserved": True,
    }
    records["active_lineage_preservation"] = {
        **base,
        **false_flags,
        "record_type": "stage5ec_active_lineage_preservation",
        "active_lineage_record_count": 8,
        "preserved": True,
        "active_lineage_preserved": True,
    }
    records["no_active_ingestion_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ec_no_active_ingestion_proof",
        "gate_status": "closed",
        "active_ingestion_performed": False,
    }
    records["no_byte_stream_transition_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ec_no_byte_stream_transition_proof",
        "gate_status": "closed",
        "real_byte_stream_generated": False,
        "variant_byte_streams_generated": False,
        "byte_stream_generation_authorized_now": False,
    }
    records["no_execution_transition_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ec_no_execution_transition_proof",
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
        "record_type": "source_browser_number_fact_enrichment_overlay_collection",
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
            "record_type": {"const": "source_browser_number_fact_enrichment_overlay_collection"},
            "review_batch_id": {"const": REVIEW_BATCH_ID},
            "overlays": {"type": "array", "minItems": EXPECTED_OVERLAY_COUNT, "maxItems": EXPECTED_OVERLAY_COUNT},
        }
    )
    return schema


def _validate_required_paths() -> list[str]:
    paths = list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values()) + [OVERLAY_COLLECTION_PATH]
    return [f"required Stage 5EC path missing: {path.as_posix()}" for path in paths if not path.exists()]


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


def _validate_token_preservation(path_key: str, source_stage_id: str) -> Stage5ECValidationResult:
    payload = _load(TOKEN_PATHS[path_key])
    errors = _expect(payload, {"source_stage_id": source_stage_id, "preserved": True, "rewritten": False})
    return Stage5ECValidationResult(len(errors), _summary_counts(payload), errors)


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


def _context_contains_stage5ec() -> bool:
    if not CHATGPT_CONTEXT_PATH.exists():
        return False
    return "## Stage 5EC - Number-fact review batch 003" in CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8")


def _update_chatgpt_context() -> None:
    marker = "## Stage 5EC - Number-fact review batch 003"
    text = CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8") if CHATGPT_CONTEXT_PATH.exists() else ""
    if marker in text:
        return
    addition = f"""

{marker}

- Stage 5EC reviewed 20 selected triangle/Page32/token-static/music/self-reference source-lock entries and added 25 NumberFactCard overlays only.
- Stage 5EC did not rewrite historical source-lock records, add new source-lock evidence, select a target, generate byte streams, run routes, execute tools, or make a solve claim.
- Durable batch facts: PDD153/T17/center41, PDD single-rune positions 25/41/53/91/106, heading minus reversed word52 = WAY, 56311 center41->word52, Page32 3299->2472 spiral, Page32 Fibonacci-prime-index increments, token-block 32x8=256 with 161 unique primary60 values, base60 clean while neighboring bases are blocked, music 29/205/547, STRANGE LOOP=463, SELF REFERENCE=529=23^2, SELF FULFILLING PROPHECY=841=29^2, and INFINITE LOOP=409.
- Stage 5EB validation policy remains active: local/full-parallel validation uses 10 workers / 10 pytest workers, and full serial pytest is not part of normal completion.
- The lag5 phenomenon remains not source-locked by Stage 5EC and is only a future lead.
- Stage 5ED should continue number-fact review batch 004 unless a blocking Source Browser issue appears.
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
                "Added review-only NumberFactCard overlays for the third selected 20-entry "
                "source-lock number-fact review batch."
            ),
            "key_outputs": [
                "Stage 5EC triangle/Page32/token/music overlay collection with 25 review-only facts.",
                "Stage 5EC review-batch, preservation, loadability, scope, and validation records.",
                "Stage 5ED selected as the next number-fact review batch.",
            ],
            "result_status": "reviewability_overlays_only",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                f"Reviewed entries={summary.get('reviewed_entry_count')}, overlays={summary.get('overlay_count')}, "
                f"fact_cards_after={summary.get('fact_card_count_after_stage5ec')}. Historical source locks were not rewritten."
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
    payload["latest_completed_stage_prefix"] = "Stage 5EC"
    payload["next_stage_after_this_stage"] = NEXT_STAGE_TITLE
    payload["expected_next_stage_prefix"] = "Stage 5ED"
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
    text = f"""# Stage 5EC Codex Completion

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
    (CODEX_OUTPUT_DIR / "stage5ec-codex-completion.md").write_text(text, encoding="utf-8")
