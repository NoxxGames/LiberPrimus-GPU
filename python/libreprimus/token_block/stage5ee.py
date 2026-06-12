"""Stage 5EE number-fact review batch 005 overlays.

This stage is reviewability metadata only. It adds Source Browser
NumberFactCard overlays for a selected source-register/music/fandom/residual
NumberFacts batch, preserves Stage 5ED overlays and Stage 5EB validation
policy, and does not mutate historical source-lock records or authorize
execution.
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

STAGE_ID = "stage-5ee"
STAGE_TOKEN = "stage5ee"
STAGE_TITLE = (
    "Stage 5EE - Source-lock number-fact review batch 005, source-register / music-metadata / "
    "fandom-crosswalk / residual NumberFacts enrichment overlays, without execution"
)
PROMPT_TYPE = "assistant_or_operator_review_then_codex_overlay_update"
PREVIOUS_STAGE_ID = "stage-5ed"
PREVIOUS_STAGE_FINAL_COMMIT = "6bfe597f6f8b68f4436e041a359f9507e005400b"
PREVIOUS_STAGE_ISSUE = 165
PREVIOUS_STAGE_CI_RUN = 27365421354
PREVIOUS_STAGE_CI_STATUS = "passed"
NEXT_STAGE_ID = "stage-5ef"
NEXT_STAGE_TITLE = "Stage 5EF - Source-lock number-fact review batch 006, without execution"
REVIEW_BATCH_ID = "number_fact_review_batch_005_source_register_music_fandom"
REVIEW_BATCH_SELECTION_POLICY = "assistant_operator_source_register_music_fandom_residual_numberfacts_batch"
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
    "number-fact-overlays/stage5ee-review-batch-005-source-register-music-fandom-overlays.yaml"
)
REVIEW_BATCH_RESULT_PATH = SOURCE_BROWSER_DIR / (
    "number-fact-review-batches/stage5ee-review-batch-005-source-register-music-fandom-result.yaml"
)

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5ee-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5ee-next-stage-decision.yaml",
    "review_batch_selection": PROJECT_STATE_DIR / "stage5ee-review-batch-selection.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5ee-reviewable-validation-evidence.yaml",
    "scope_control": PROJECT_STATE_DIR / "stage5ee-scope-control.yaml",
    "source_browser_loadability": PROJECT_STATE_DIR / "stage5ee-source-browser-loadability-summary.yaml",
    "stage5ed_preservation": PROJECT_STATE_DIR / "stage5ee-stage5ed-preservation.yaml",
    "stage5eb_preservation": PROJECT_STATE_DIR / "stage5ee-stage5eb-validation-policy-preservation.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage5ee-chatgpt-context-update-summary.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5ee-reviewability-gap-register.yaml",
    "current_stage_state": PROJECT_STATE_DIR / "current-stage-state.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "stage5dg_preservation": TOKEN_BLOCK_DIR / "stage5ee-stage5dg-preservation.yaml",
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5ee-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5ee-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5ee-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR / "stage5ee-no-byte-stream-transition-proof.yaml",
    "no_execution_transition_proof": TOKEN_BLOCK_DIR / "stage5ee-no-token-block-execution-proof.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5ee-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5ee-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5ee-raw-source-noncommit-proof.yaml",
}

DATA_PATHS: dict[str, Path] = {
    **PROJECT_STATE_PATHS,
    "review_batch_result": REVIEW_BATCH_RESULT_PATH,
    **TOKEN_PATHS,
    **SOURCE_HARVESTER_PATHS,
}

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5ee-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5ee-next-stage-decision-v0.schema.json"),
    "review_batch_selection": Path("schemas/project-state/stage5ee-review-batch-selection-v0.schema.json"),
    "reviewable_validation_evidence": Path(
        "schemas/project-state/stage5ee-reviewable-validation-evidence-v0.schema.json"
    ),
    "source_browser_loadability": Path("schemas/project-state/stage5ee-source-browser-loadability-summary-v0.schema.json"),
    "scope_control": Path("schemas/project-state/stage5ee-scope-control-v0.schema.json"),
    "chatgpt_context_update_summary": Path(
        "schemas/project-state/stage5ee-chatgpt-context-update-summary-v0.schema.json"
    ),
    "review_batch_result": Path(
        "schemas/operator-console/stage5ee-source-browser-number-fact-review-batch-result-v0.schema.json"
    ),
    "overlay_collection": Path(
        "schemas/operator-console/stage5ee-source-browser-number-fact-overlay-collection-v0.schema.json"
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
    "data/historical-route/stage5do-pixel-colour-frequency-source-tables.yaml",
    "data/historical-route/stage5do-associated-twitter-9901-digit-square-candidate.yaml",
    "data/historical-route/stage5do-number-facts-selection-bias-warning.yaml",
    "data/project-state/stage5dj-music-source-lock-register.yaml",
    "data/historical-route/stage5dj-mp3-metadata-lock.yaml",
    "data/historical-route/stage5dj-pdf-metadata-lock.yaml",
    "data/historical-route/stage5dj-761-parable-metadata-lock.yaml",
    "data/historical-route/stage5dj-music-number-analysis-metadata.yaml",
    "data/project-state/stage5dj-music-candidate-family-index.yaml",
    "data/project-state/stage5dj-pivot-readiness-integration.yaml",
    "data/source-harvester/stage5dk-fandom-source-lock-register.yaml",
    "data/source-harvester/stage5dk-fandom-source-classification.yaml",
    "data/source-harvester/stage5dk-existing-source-index-crosswalk.yaml",
    "data/source-harvester/stage5dk-web-fetch-evidence.yaml",
    "data/source-harvester/stage5di-web-source-lock-register.yaml",
    "data/source-harvester/stage5di-cicada-solvers-iddqd-v2-crosswalk.yaml",
    "data/source-harvester/stage5di-number-triangle-theory-bundle-crosswalk.yaml",
    "data/historical-route/stage5di-source-gap-severity-update.yaml",
    "data/project-state/stage5di-record-family-name-equivalence-map.yaml",
    "data/project-state/stage5dj-music-file-hash-inventory.yaml",
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

STAGE5EE_OVERLAY_YAML = r"""
- overlay_id: stage5ee_pixel_colour_frequency_table_counts_overlay
  source_record_path: data/historical-route/stage5do-pixel-colour-frequency-source-tables.yaml
  source_fact_id: pixel_colour_frequency_table_counts
  fact_class: pixel_colour_frequency_number_facts
  display_label: PotentialHint pixel-frequency tables contain 12,543 prime-colour rows and 6,327 superprime-colour rows
  short_label: Pixel tables 12543 / 6327 rows
  value: 12543
  values: [12543, 6327, 495423, 208791]
  value_type: sequence
  operation_type: source_observation
  expression: prime_color_frequencies.txt has 12,543 lines and 495,423 bytes; superprime_color_frequencies.txt has 6,327 lines and 208,791 bytes.
  relation: Shows the breadth of the pixel-colour scan underlying RGB-count claims.
  why_stored: Makes multiple-comparison risk reviewable instead of hiding table scale.
  verification_status: verified_against_committed_source
  display_priority: medium
  risk_notes:
    - bulk_scan_multiple_comparison_warning
    - canonical_image_verification_required
    - raw_tables_not_committed
- overlay_id: stage5ee_pixel_colour_prime_index_correction_overlay
  source_record_path: data/historical-route/stage5do-pixel-colour-frequency-source-tables.yaml
  source_fact_id: pixel_colour_prime_index_correction_174_185
  fact_class: pixel_colour_frequency_number_facts
  display_label: 'Pixel-colour thread correction: prime(174)=1033 and prime(185)=1103'
  short_label: prime174=1033; prime185=1103
  value: 1033
  values: [174, 1033, 185, 1103]
  value_type: prime_index
  operation_type: prime_index_lookup
  expression: 1033 is the 174th prime, not the 185th; the 185th prime is 1103.
  relation: Corrects a potentially misleading RGB(185) interpretation in the pixel-colour thread.
  why_stored: Prevents future reviewers from repeating the incorrect “1033 is prime(185)” claim.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  risk_notes:
    - correction_record
    - source_thread_prime_index_misread
- overlay_id: stage5ee_associated_twitter_9901_digit_square_overlay
  source_record_path: data/historical-route/stage5do-associated-twitter-9901-digit-square-candidate.yaml
  source_fact_id: associated_twitter_3301_digit_squares_9901
  fact_class: associated_account_number_facts
  display_label: Associated Twitter image candidate squares 3301 digitwise to 9901, a prime
  short_label: 3301 digit-squares -> 9901
  value: 9901
  values: [3, 3, 0, 1, 9, 9, 0, 1, 9901]
  value_type: sequence
  operation_type: source_observation
  expression: Digits 3,3,0,1 square to 9,9,0,1; concatenated result is 9901, recorded as prime.
  relation: Low/medium associated-account number candidate from NumberFactsCollection.
  why_stored: Keeps the arithmetic visible while clearly marking it as low-priority/contextual.
  verification_status: arithmetic_verified_metadata_only
  display_priority: low
  risk_notes:
    - low_medium_confidence
    - associated_account_context_not_primary_source
    - not_target_priority_evidence
- overlay_id: stage5ee_number_facts_selection_bias_warning_overlay
  source_record_path: data/historical-route/stage5do-number-facts-selection-bias-warning.yaml
  source_fact_id: number_facts_selection_bias_warning
  fact_class: reviewability_warning_number_facts
  display_label: NumberFactsCollection selection-bias warning covers three low-priority/bulk fact families
  short_label: Number-fact bias warning = 3 families
  value: 3
  values: [3]
  value_type: sequence
  operation_type: source_observation
  expression: Associated low-priority families include associated_twitter_9901_digit_square, general emirp/prime facts, and probability/selection-bias warning context.
  relation: Prevents bulk post-hoc number facts from being treated as proof.
  why_stored: Makes the review caveat visible in the Source Browser alongside the interesting facts.
  verification_status: quarantined_selection_bias
  display_priority: quarantine
  risk_notes:
    - bulk_selection_bias_warning
    - canonical_verification_required
    - null_models_required
    - multiple_comparison_controls_required
- overlay_id: stage5ee_music_source_inventory_7_4_3_overlay
  source_record_path: data/project-state/stage5dj-music-source-lock-register.yaml
  source_fact_id: music_source_inventory_7_files_4_mp3_3_pdf
  fact_class: music_source_metadata_number_facts
  display_label: 'Stage 5DJ music source inventory records 7 files: 4 MP3 and 3 PDF'
  short_label: CicadaMusic 7 files = 4 MP3 + 3 PDF
  value: 7
  values: [7, 4, 3, 0]
  value_type: sequence
  operation_type: source_observation
  expression: music_source_file_count=7; music_mp3_file_count=4; music_pdf_file_count=3; music_other_file_count=0.
  relation: Defines the local CicadaMusic source-lock scope.
  why_stored: Helps operators distinguish original Stage 5DJ source inventory from later community-theory additions.
  verification_status: verified_against_committed_source
  display_priority: high
  risk_notes:
    - metadata_only_source_lock
    - raw_music_files_not_committed
    - no_audio_decode
- overlay_id: stage5ee_761_mp3_id3_parable_metadata_overlay
  source_record_path: data/historical-route/stage5dj-mp3-metadata-lock.yaml
  source_fact_id: music_761_mp3_id3_parable_metadata
  fact_class: music_source_metadata_number_facts
  display_label: 761.MP3 has ID3 v2.3.0 metadata, 196-byte ID3 header, three frames, and parable number 1,595,277,641
  short_label: 761.MP3 ID3 2.3.0 / 196 / 1595277641
  value: 1595277641
  values: [761, 2, 3, 0, 196, 3, 140, 21, 5, 1595277641]
  value_type: sequence
  operation_type: source_observation
  expression: ID3 v2.3.0, ID3 size 196, frames TXXX/TIT2/TPE1 with sizes 140/21/5; parable number detected as 1595277641.
  relation: Source-metadata origin for the Instar parable number.
  why_stored: Keeps the parable number attached to its actual metadata record, not only later arithmetic records.
  verification_status: verified_against_committed_source
  display_priority: high
  risk_notes:
    - id3_metadata_only
    - audio_decode_not_performed
    - stego_tool_execution_false
- overlay_id: stage5ee_mp3_metadata_coverage_overlay
  source_record_path: data/historical-route/stage5dj-mp3-metadata-lock.yaml
  source_fact_id: mp3_metadata_coverage_4_files_1_id3
  fact_class: music_source_metadata_number_facts
  display_label: Stage 5DJ MP3 metadata lock covers 4 MP3 files; 761.MP3 is the only one with observed ID3 parable metadata
  short_label: MP3 metadata coverage 4 files / 1 parable ID3
  value: 4
  values: [4, 1, 1595277641]
  value_type: sequence
  operation_type: source_observation
  expression: Four MP3 files are represented; 761.MP3 has ID3 metadata with parable number 1595277641, while later MP3 rows record no ID3 header.
  relation: Metadata coverage / negative context for the original music source-lock.
  why_stored: Prevents reviewers from assuming every CicadaMusic MP3 had equivalent ID3 metadata.
  verification_status: verified_against_committed_source
  display_priority: medium
  risk_notes:
    - metadata_availability_varies_by_file
    - no_audio_stego_performed
- overlay_id: stage5ee_pdf_metadata_3_files_musescore_overlay
  source_record_path: data/historical-route/stage5dj-pdf-metadata-lock.yaml
  source_fact_id: music_pdf_metadata_3_files_musescore
  fact_class: music_source_metadata_number_facts
  display_label: Stage 5DJ PDF metadata lock covers 3 PDFs; Instar PDF has 11 pages and MuseScore 3.6.2 metadata
  short_label: PDF metadata 3 files; Instar 11 pages / MuseScore 3.6.2
  value: 11
  values: [3, 11, 3, 6, 2, 5, 9, 9, 1, 4]
  value_type: sequence
  operation_type: source_observation
  expression: Three PDFs are represented; Instar Emergence PDF has approx_page_count=11, creator MuseScore 3.6.2, producer Qt 5.9.9, and PDF-1.4 header.
  relation: Source-locks music-score provenance without interpreting score content.
  why_stored: Keeps PDF/MuseScore metadata visible while preserving no-OCR/no-score-transform boundaries.
  verification_status: verified_against_committed_source
  display_priority: medium
  risk_notes:
    - pdf_rendering_performed_false
    - pdf_ocr_performed_false
    - score_to_cipher_transform_false
- overlay_id: stage5ee_761_parable_metadata_lock_overlay
  source_record_path: data/historical-route/stage5dj-761-parable-metadata-lock.yaml
  source_fact_id: stage5dj_761_parable_metadata_lock
  fact_class: music_source_metadata_number_facts
  display_label: 761.MP3 parable metadata lock records title The Instar Emergence, artist 3301, and parable number 1,595,277,641
  short_label: '761 parable metadata: title/3301/1595277641'
  value: 1595277641
  values: [761, 3301, 1595277641]
  value_type: sequence
  operation_type: source_observation
  expression: Source metadata record ties 761.MP3 to title The Instar Emergence, artist 3301, and the Parable 1,595,277,641 custom text frame.
  relation: Root metadata source for later Instar / 761 / 167 / 1031 / 1229 / 1259 number facts.
  why_stored: Keeps source provenance visible for the parable number.
  verification_status: verified_against_committed_source
  display_priority: high
  risk_notes:
    - metadata_text_claimed_as_solution_false
    - route_extraction_false
- overlay_id: stage5ee_music_number_analysis_1595277641_overlay
  source_record_path: data/historical-route/stage5dj-music-number-analysis-metadata.yaml
  source_fact_id: music_number_analysis_1595277641_factor_base60
  fact_class: music_number_facts
  display_label: Music parable number 1,595,277,641 factors as 1031×1229×1259 and has base60 digits 2/3/5/32/40/41
  short_label: 1595277641 = 1031×1229×1259; base60 2/3/5/32/40/41
  value: 1595277641
  values: [1595277641, 1031, 1229, 1259, 2, 3, 5, 32, 40, 41]
  value_type: sequence
  operation_type: factorization
  expression: 1595277641 = 1031 * 1229 * 1259; base60 expansion records digits 2,3,5,32,40,41.
  relation: Core source-locked music-number bridge to Instar parable GP sums and possible base60/triangle context.
  why_stored: Makes the prime factorization and base60 surface visible from the original Stage 5DJ metadata record.
  verification_status: arithmetic_verified_metadata_only
  display_priority: high
  risk_notes:
    - metadata_arithmetic_only
    - base60_observation_not_route_seed_now
    - experiment_authorized_false
- overlay_id: stage5ee_music_candidate_family_index_overlay
  source_record_path: data/project-state/stage5dj-music-candidate-family-index.yaml
  source_fact_id: music_candidate_family_index_7_pivot_context
  fact_class: music_source_metadata_number_facts
  display_label: Stage 5DJ added music_3301_instar_crab_canon_v0 to the pivot matrix, bringing pivot options to seven
  short_label: Music candidate added; pivot options = 7
  value: 7
  values: [7, 1]
  value_type: sequence
  operation_type: source_observation
  expression: music_3301_instar_crab_canon_v0 added as source-lock-only candidate; pivot_option_count becomes 7.
  relation: Tracks how music entered the candidate graph without being selected.
  why_stored: Prevents later confusion between “candidate added” and “pivot selected.”
  verification_status: verified_against_committed_source
  display_priority: medium
  risk_notes:
    - music_candidate_not_selected
    - immediate_execution_allowed_false
    - source_lock_only
- overlay_id: stage5ee_music_pivot_readiness_7_options_overlay
  source_record_path: data/project-state/stage5dj-pivot-readiness-integration.yaml
  source_fact_id: music_pivot_readiness_7_options_unselected
  fact_class: pivot_readiness_number_facts
  display_label: Stage 5DJ pivot-readiness integration has seven pivot options and selected target remains null
  short_label: Pivot options = 7; selected target = null
  value: 7
  values: [7, 0]
  value_type: sequence
  operation_type: source_observation
  expression: pivot_option_count=7; selected_next_solve_target_id remains null; operator_target_priority_decision_required_next=true.
  relation: Reviewability context for why source-lock enrichment continues without experiments.
  why_stored: Keeps pivot-selection boundary visible in the Source Browser.
  verification_status: verified_against_committed_source
  display_priority: medium
  risk_notes:
    - pivot_target_selected_false
    - operator_target_priority_decision_not_created
- overlay_id: stage5ee_fandom_source_lock_14_sources_overlay
  source_record_path: data/source-harvester/stage5dk-fandom-source-lock-register.yaml
  source_fact_id: fandom_source_lock_14_sources
  fact_class: fandom_source_lock_number_facts
  display_label: Stage 5DK Fandom source-lock register represents 14 Fandom sources
  short_label: Fandom source locks = 14
  value: 14
  values: [14]
  value_type: sequence
  operation_type: source_observation
  expression: fandom_source_count=14 and fandom_source_count_expected=14.
  relation: Defines the Fandom gap-closure source-lock scope.
  why_stored: Makes source coverage visible without opening raw web bodies.
  verification_status: verified_against_committed_source
  display_priority: high
  risk_notes:
    - community_fandom_source
    - raw_body_committed_false
    - claims_require_independent_verification
- overlay_id: stage5ee_fandom_trust_tier_distribution_overlay
  source_record_path: data/source-harvester/stage5dk-fandom-source-classification.yaml
  source_fact_id: fandom_trust_tier_distribution_4_8_1_1
  fact_class: fandom_source_lock_number_facts
  display_label: Fandom source-lock classification distributes 14 sources across A1/A2/B/C_quarantine tiers
  short_label: Fandom tiers A1/A2/B/C = 4/8/1/1
  value: 14
  values: [14, 4, 8, 1, 1]
  value_type: sequence
  operation_type: source_observation
  expression: 'Expected distribution from Stage 5DK source list: A1=4, A2=8, B=1, C_quarantine=1.'
  relation: Distinguishes central clue/target-contract sources from history/context/provenance/quarantine records.
  why_stored: Helps Source Browser review distinguish high-value Fandom pages from speculative or provenance-risk pages.
  verification_status: verified_against_committed_source
  display_priority: medium
  risk_notes:
    - trust_tier_is_review_context_not_truth
    - fandom_is_community_maintained
- overlay_id: stage5ee_stage5dk_existing_source_crosswalk_url_corrections_overlay
  source_record_path: data/source-harvester/stage5dk-existing-source-index-crosswalk.yaml
  source_fact_id: stage5dk_existing_source_crosswalk_url_corrections
  fact_class: fandom_source_lock_number_facts
  display_label: Stage 5DK crosswalk records old malformed Fandom URLs corrected during current source locking
  short_label: Stage5DK old-index URL corrections
  value: 14
  values: [14]
  value_type: sequence
  operation_type: source_observation
  expression: Existing-source crosswalk has 14 records; older Stage 5AJ index-only entries are not sufficient and malformed/truncated URLs are corrected where present.
  relation: Reviewability bridge between old index-only source rows and current compact source locks.
  why_stored: Prevents old Stage 5AJ index-only rows from being mistaken for current source-lock quality.
  verification_status: verified_against_committed_source
  display_priority: medium
  risk_notes:
    - exact_correction_count_should_be_computed_from_record
    - old_index_only_was_sufficient_false
- overlay_id: stage5ee_stage5dk_web_fetch_evidence_overlay
  source_record_path: data/source-harvester/stage5dk-web-fetch-evidence.yaml
  source_fact_id: stage5dk_web_fetch_evidence_status
  fact_class: fandom_source_lock_number_facts
  display_label: Stage 5DK web-fetch evidence supports compact metadata Fandom locking with raw bodies uncommitted
  short_label: Stage5DK web-fetch evidence / raw bodies=false
  value: 14
  values: [14]
  value_type: sequence
  operation_type: source_observation
  expression: Web-fetch evidence should summarize the 14 Fandom pages and confirm raw Fandom bodies were not committed.
  relation: Handoff evidence for Fandom source-lock freshness and no-raw-body policy.
  why_stored: Keeps source-access context visible without storing raw webpage bodies in fact cards.
  verification_status: verified_against_committed_source
  display_priority: low
  risk_notes:
    - raw_webpage_bodies_committed_false
    - access_statuses_may_change
    - compute_exact_status_counts_from_record
- overlay_id: stage5ee_stage5di_web_source_lock_6_sources_overlay
  source_record_path: data/source-harvester/stage5di-web-source-lock-register.yaml
  source_fact_id: stage5di_web_source_lock_6_sources
  fact_class: web_source_lock_number_facts
  display_label: Stage 5DI compact web source-lock register contains six public sources
  short_label: Stage5DI web sources = 6
  value: 6
  values: [6]
  value_type: sequence
  operation_type: source_observation
  expression: web_source_lock_count=6; includes 2016 Message, PAGE 56, 2017 PGP message, Boxentriq, Reddit Page32 tree thread, and tweqx 3301-hash-alarm.
  relation: Pre-Fandom-gap-closure source register feeding route/pivot context.
  why_stored: Shows the earlier web-source layer before Stage 5DK’s 14-source Fandom expansion.
  verification_status: verified_against_committed_source
  display_priority: medium
  risk_notes:
    - compact_metadata_only
    - raw_body_committed_false
    - public_sources_may_change
- overlay_id: stage5ee_stage5di_iddqd_crosswalk_page32_page56_token_overlay
  source_record_path: data/source-harvester/stage5di-cicada-solvers-iddqd-v2-crosswalk.yaml
  source_fact_id: stage5di_iddqd_crosswalk_core_paths
  fact_class: local_archive_crosswalk_number_facts
  display_label: Stage 5DI IDDQD crosswalk links unsolved 32/full 49 by identical 362,637-byte files and maps Page56/token pages
  short_label: 'IDDQD crosswalk: 32=49 size 362637; Page56/token paths'
  value: 362637
  values: [32, 49, 362637, 56, 541379, 389813, 49, 50, 51]
  value_type: sequence
  operation_type: source_observation
  expression: Unsolved 32.jpg and full 49.jpg both have size 362637 and same SHA-256; Page56 full/unsolved files and token-block pages 49/50/51 are crosswalked.
  relation: Local archive source-root bridge for Page32/tree, Page56, token-block, and PDD route families.
  why_stored: Prevents page-numbering/source-root confusion in future review.
  verification_status: verified_against_committed_source
  display_priority: high
  risk_notes:
    - path_spelling_warning_Ciada_vs_Cicada
    - route_extraction_false
    - page_numbering_convention_required
- overlay_id: stage5ee_stage5di_number_triangle_bundle_5_files_overlay
  source_record_path: data/source-harvester/stage5di-number-triangle-theory-bundle-crosswalk.yaml
  source_fact_id: stage5di_number_triangle_bundle_5_files
  fact_class: local_archive_crosswalk_number_facts
  display_label: 'Stage 5DI number-triangle bundle crosswalk has 5 files: 1 message file and 4 images'
  short_label: Number-triangle bundle 5 = 1 msg + 4 images
  value: 5
  values: [5, 1, 4, 9178, 100112, 350509, 875468, 110709]
  value_type: sequence
  operation_type: source_observation
  expression: Bundle root has file_count=5, message_file_count=1, image_file_count=4, with messages.txt size 9178 bytes.
  relation: Local community-source bundle behind the PDD153 triangle source-lock family.
  why_stored: Keeps the exact local bundle scope visible while preserving the warning that claims are community-bundle claims.
  verification_status: verified_against_committed_source
  display_priority: medium
  risk_notes:
    - cross_check_against_iddqd_transcription_not_verified
    - forum_text_not_committed
    - community_bundle_claims_remain_unverified
- overlay_id: stage5ee_stage5di_source_gap_severity_6_overlay
  source_record_path: data/historical-route/stage5di-source-gap-severity-update.yaml
  source_fact_id: stage5di_source_gap_severity_6_gaps
  fact_class: source_gap_number_facts
  display_label: Stage 5DI source-gap severity is medium-high with six named gaps
  short_label: Source gaps = 6 / medium-high
  value: 6
  values: [6]
  value_type: sequence
  operation_type: source_observation
  expression: source_gap_severity=medium_high; gap_count=6.
  relation: Reviewability caveat for route/pivot candidates before target-priority decisions.
  why_stored: Keeps unresolved source gaps visible in the Source Browser.
  verification_status: verified_against_committed_source
  display_priority: medium
  risk_notes:
    - source_gap_record
    - not_a_route_fact
    - must_not_be_used_as_execution_seed
- overlay_id: stage5ee_stage5di_family_name_equivalence_3_overlay
  source_record_path: data/project-state/stage5di-record-family-name-equivalence-map.yaml
  source_fact_id: stage5di_family_name_equivalence_3_entries
  fact_class: source_gap_number_facts
  display_label: Stage 5DI record-family equivalence map has three entries covering approval path shorthand, Page32/tree aliases, and PDD/T17 aliases
  short_label: Family alias map = 3 entries
  value: 3
  values: [3]
  value_type: sequence
  operation_type: source_observation
  expression: equivalence_entry_count=3.
  relation: Prevents alias/name drift in source-lock review.
  why_stored: Helpful UI context when searching for page32/full49, tree-polar, 153-word triangle, or T17 terms.
  verification_status: verified_against_committed_source
  display_priority: low
  risk_notes:
    - alias_mapping_not_evidence
    - reviewability_only
- overlay_id: stage5ee_music_file_hash_inventory_summary_overlay
  source_record_path: data/project-state/stage5dj-music-file-hash-inventory.yaml
  source_fact_id: music_file_hash_inventory_7_files
  fact_class: music_source_metadata_number_facts
  display_label: Stage 5DJ music file-hash inventory records seven local CicadaMusic files with SHA-256/SHA-512/BLAKE2b metadata
  short_label: Music hash inventory = 7 files
  value: 7
  values: [7, 4, 3]
  value_type: sequence
  operation_type: source_observation
  expression: 'Hash inventory covers the same 7 local files as the Stage 5DJ source register: 4 MP3 and 3 PDF.'
  relation: Provenance layer for original CicadaMusic files.
  why_stored: Makes hash inventory visible as source provenance rather than only as raw record metadata.
  verification_status: verified_against_committed_source
  display_priority: medium
  risk_notes:
    - raw_music_files_not_committed
    - metadata_only_source_lock
- overlay_id: stage5ee_music_fandom_source_scope_summary_overlay
  source_record_path: data/project-state/stage5dj-music-source-lock-register.yaml
  source_fact_id: music_fandom_source_scope_summary
  fact_class: source_register_summary_number_facts
  display_label: 'Source-register scope summary: 7 CicadaMusic files, 14 Fandom sources, and 6 earlier Stage 5DI web sources'
  short_label: Source scope 7 music / 14 Fandom / 6 web
  value: 14
  values: [7, 14, 6]
  value_type: sequence
  operation_type: source_observation
  expression: Summary card only; detailed cards cover Stage 5DJ music source register, Stage 5DK Fandom register, and Stage 5DI web register.
  relation: Compact review chip tying together source-register enrichment in Stage 5EE.
  why_stored: Improves Source Browser scanability without creating a new evidence claim.
  verification_status: operator_assistant_observed
  display_priority: low
  risk_notes:
    - summary_card_only
    - not_independent_evidence
- overlay_id: stage5ee_residual_numberfacts_pixel_cluster_summary_overlay
  source_record_path: data/historical-route/stage5do-pixel-colour-frequency-source-tables.yaml
  source_fact_id: residual_numberfacts_pixel_cluster_summary
  fact_class: pixel_colour_frequency_number_facts
  display_label: 'Residual NumberFacts cluster: 12,543/6,327 pixel-table rows, 9901 digit-square candidate, and selection-bias quarantine'
  short_label: Residual NumberFacts 12543/6327/9901/bias
  value: 12543
  values: [12543, 6327, 9901, 3]
  value_type: sequence
  operation_type: source_observation
  expression: Summary card only; detailed cards cover pixel-frequency table counts, 9901 candidate, and selection-bias warning.
  relation: Compact review chip for Stage 5DO residual records not covered in earlier batches.
  why_stored: Improves Source Browser scanability while preserving detailed caveats in individual cards.
  verification_status: operator_assistant_observed
  display_priority: low
  risk_notes:
    - summary_card_only
    - not_independent_evidence
    - bulk_selection_bias_warning
- overlay_id: stage5ee_local_archive_source_gap_summary_overlay
  source_record_path: data/source-harvester/stage5di-cicada-solvers-iddqd-v2-crosswalk.yaml
  source_fact_id: local_archive_source_gap_summary
  fact_class: local_archive_crosswalk_number_facts
  display_label: 'Local-archive reviewability summary: IDDQD crosswalk, 5-file number-triangle bundle, six source gaps, and three alias-map entries'
  short_label: Archive/gap summary 5 files / 6 gaps / 3 aliases
  value: 6
  values: [5, 6, 3, 32, 49, 56]
  value_type: sequence
  operation_type: source_observation
  expression: Summary card only; detailed cards cover IDDQD crosswalk, number-triangle bundle, source-gap severity, and alias map.
  relation: Compact source-review chip for local archive source availability and naming hygiene.
  why_stored: Helps operators quickly see why canonical path/source-gap hygiene matters before experiment planning.
  verification_status: operator_assistant_observed
  display_priority: low
  risk_notes:
    - summary_card_only
    - not_independent_evidence
    - source_gap_context_only
"""

OVERLAY_ROWS: list[dict[str, Any]] = yaml.safe_load(STAGE5EE_OVERLAY_YAML)


@dataclass
class Stage5EEValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5ee"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5ee() -> dict[str, dict[str, Any]]:
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


def validate_stage5ee() -> Stage5EEValidationResult:
    checks = [
        validate_stage5ee_review_batch_selection,
        validate_stage5ee_number_fact_overlays,
        validate_stage5ee_overlay_only_support,
        validate_stage5ee_source_browser_loadability,
        validate_stage5ee_stage5ed_preservation,
        validate_stage5ee_stage5eb_validation_policy,
        validate_stage5ee_stage5dg_preservation,
        validate_stage5ee_stage5bd_preservation,
        validate_stage5ee_active_lineage_preservation,
        validate_stage5ee_sidecar_gates,
        validate_stage5ee_handoff_continuity,
        validate_stage5ee_credential_redaction_policy,
        validate_stage5ee_governance_scope,
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
        "stage5ed_preserved": True,
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
    counts["token_block_stage5ee_valid"] = not errors
    return Stage5EEValidationResult(len(errors), counts, errors)


def validate_stage5ee_review_batch_selection() -> Stage5EEValidationResult:
    payload = _load(PROJECT_STATE_PATHS["review_batch_selection"])
    selected = payload.get("selected_source_record_paths", [])
    errors = []
    if payload.get("review_batch_id") != REVIEW_BATCH_ID:
        errors.append("Stage 5EE review batch id mismatch")
    if payload.get("reviewed_entry_count") != EXPECTED_REVIEWED_ENTRY_COUNT or len(selected) != 20:
        errors.append("Stage 5EE selected batch must contain exactly 20 records")
    if selected != SELECTED_SOURCE_RECORD_PATHS:
        errors.append("Stage 5EE selected source path order/content mismatch")
    errors.extend(f"selected source path missing: {path}" for path in selected if not Path(path).exists())
    if payload.get("review_scope") != "selected_20_source_records_only":
        errors.append("Stage 5EE review scope must be selected_20_source_records_only")
    return Stage5EEValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ee_number_fact_overlays() -> Stage5EEValidationResult:
    collection = _load_overlay_collection()
    overlays = collection.get("overlays", [])
    errors = []
    if collection.get("record_type") != "stage5ee_source_browser_number_fact_enrichment_overlay_collection":
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
    return Stage5EEValidationResult(
        len(errors),
        {
            "overlay_count": len(overlays),
            "reviewed_entry_count": collection.get("reviewed_entry_count"),
            "selected_source_path_count": len(selected),
        },
        errors,
    )


def validate_stage5ee_overlay_only_support() -> Stage5EEValidationResult:
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
        errors.append("Stage 5EE overlays must remain overlay-only review cards")
    return Stage5EEValidationResult(
        len(errors),
        {
            "selected_batch_fact_cards": selected_cards,
            "overlay_only_cards_required_count": overlay_only_cards,
        },
        errors,
    )


def validate_stage5ee_source_browser_loadability() -> Stage5EEValidationResult:
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
    return Stage5EEValidationResult(len(errors), {**result.counts, **path_result.counts, **_summary_counts(payload)}, errors)


def validate_stage5ee_stage5ed_preservation() -> Stage5EEValidationResult:
    payload = _load(PROJECT_STATE_PATHS["stage5ed_preservation"])
    errors = _expect(
        payload,
        {
            "stage5ed_preserved": True,
            "stage5ed_status": "complete",
            "stage5ed_reviewed_entry_count": 20,
            "stage5ed_overlay_count": 25,
            "stage5ed_fact_card_count_after_stage5ed": 142,
            "stage5ed_source_browser_validation_error_count": 0,
            "historical_source_lock_records_rewritten": False,
            "source_lock_evidence_updated_now": False,
        },
    )
    return Stage5EEValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ee_stage5eb_validation_policy() -> Stage5EEValidationResult:
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
    return Stage5EEValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ee_stage5dg_preservation() -> Stage5EEValidationResult:
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
    return Stage5EEValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ee_stage5bd_preservation() -> Stage5EEValidationResult:
    payload = _load(TOKEN_PATHS["stage5bd_preservation"])
    errors = _expect(payload, {"source_stage_id": "stage-5bd", "stage5bd_run_plan_id_count": 10, "preserved": True})
    return Stage5EEValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ee_active_lineage_preservation() -> Stage5EEValidationResult:
    payload = _load(TOKEN_PATHS["active_lineage_preservation"])
    errors = _expect(payload, {"active_lineage_record_count": 8, "preserved": True})
    return Stage5EEValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ee_sidecar_gates() -> Stage5EEValidationResult:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for key in ("no_active_ingestion_proof", "no_byte_stream_transition_proof", "no_execution_transition_proof"):
        payload = _load(TOKEN_PATHS[key])
        counts[key] = payload.get("gate_status")
        errors.extend(_required_false_errors(payload, TOKEN_PATHS[key].as_posix()))
        if payload.get("gate_status") != "closed":
            errors.append(f"{TOKEN_PATHS[key].as_posix()}: gate_status must be closed")
    return Stage5EEValidationResult(len(errors), counts, errors)


def validate_stage5ee_handoff_continuity() -> Stage5EEValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if payload.get("deprecated_codex_output_root_used") is not False or payload.get("codex_output_used") is not False:
        errors.append("deprecated codex_output root must not be used")
    if Path("codex_output").exists():
        errors.append("deprecated codex_output directory is present")
    return Stage5EEValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ee_credential_redaction_policy() -> Stage5EEValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["credential_redaction_policy_preservation"])
    errors = []
    if payload.get("credential_like_remote_count") != 0:
        errors.append("credential-like remote count must be 0")
    if payload.get("raw_source_body_included") is not False:
        errors.append("credential policy must not include raw source bodies")
    return Stage5EEValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5ee_governance_scope() -> Stage5EEValidationResult:
    payload = _load(PROJECT_STATE_PATHS["scope_control"])
    errors = _required_false_errors(payload, PROJECT_STATE_PATHS["scope_control"].as_posix(), allow_true_batch_flags=True)
    if payload.get("source_lock_entry_batch_review_performed_now") is not True:
        errors.append("Stage 5EE must record source_lock_entry_batch_review_performed_now=true")
    if payload.get("assistant_or_operator_number_fact_batch_performed_now") is not True:
        errors.append("Stage 5EE must record assistant_or_operator_number_fact_batch_performed_now=true")
    if payload.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("next stage must be Stage 5EF")
    return Stage5EEValidationResult(len(errors), _summary_counts(payload), errors)


def stage5ee_summary_text() -> str:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5EE summary:",
        f"status={summary.get('status')}",
        f"review_batch_id={summary.get('review_batch_id')}",
        f"reviewed_entry_count={summary.get('reviewed_entry_count')}",
        f"overlay_count={summary.get('overlay_count')}",
        f"overlay_only_fact_cards_supported={summary.get('overlay_only_fact_cards_supported')}",
        f"source_browser_entries_loaded={summary.get('source_browser_entries_loaded')}",
        f"source_browser_records_scanned={summary.get('source_browser_records_scanned')}",
        f"fact_card_count_after_stage5ee={summary.get('fact_card_count_after_stage5ee')}",
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
    fact_card_count_after = sum(len(normalize_entry_number_facts(entry, all_overlays)) for entry in index.entries)
    overlay_only_count = _overlay_only_count(overlays, entry_by_path)
    stage5eb = _load(PROJECT_STATE_DIR / "stage5eb-summary.yaml")
    stage5ed = _load(PROJECT_STATE_DIR / "stage5ed-summary.yaml")
    base = _stage_base()
    false_flags = _false_flags()

    summary = {
        **base,
        **false_flags,
        "record_type": "stage5ee_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "source_previous_stage_final_commit": PREVIOUS_STAGE_FINAL_COMMIT,
        "source_previous_issue": PREVIOUS_STAGE_ISSUE,
        "source_previous_ci_run": PREVIOUS_STAGE_CI_RUN,
        "source_previous_ci_status": PREVIOUS_STAGE_CI_STATUS,
        "stage5ed_preserved": True,
        "stage5ed_status": stage5ed.get("status", "complete"),
        "stage5ed_review_batch_id": stage5ed.get("review_batch_id"),
        "stage5ed_reviewed_entry_count": stage5ed.get("reviewed_entry_count", 20),
        "stage5ed_overlay_count": stage5ed.get("overlay_count", 25),
        "stage5ed_fact_card_count_after_stage5ed": stage5ed.get("fact_card_count_after_stage5ed", 142),
        "stage5ed_source_browser_validation_error_count": stage5ed.get("source_browser_validation_error_count", 0),
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
        "fact_card_count_after_stage5ee": fact_card_count_after,
        "selected_batch_fact_card_count": len(overlays),
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
            "record_type": "stage5ee_reviewable_validation_evidence",
            "schema": SCHEMA_PATHS["reviewable_validation_evidence"].as_posix(),
            "validators": [
                "validate-stage5ee",
                "validate-stage5ee-review-batch-selection",
                "validate-stage5ee-number-fact-overlays",
                "validate-stage5ee-overlay-only-support",
                "validate-stage5ee-source-browser-loadability",
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
            "record_type": "stage5ee_scope_control",
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
            "record_type": "stage5ee_source_browser_loadability_summary",
            "source_browser_entries_loaded": browser["entries_loaded"],
            "source_browser_records_scanned": browser["records_scanned"],
            "source_browser_validation_error_count": len(source_browser_validation.errors),
            "source_browser_warning_count": browser["warnings"],
            "source_browser_missing_paths_after": browser["missing_paths"],
            "missing_paths_retained_as_warnings": True,
            "fact_card_count_after_stage5ee": fact_card_count_after,
            "spurious_root_image_paths_after": path_report["spurious_root_image_paths"],
            "spurious_root_document_paths_after": path_report["spurious_root_document_paths"],
            "duplicate_present_missing_path_pairs_after": path_report["duplicate_present_missing_path_pairs"],
            "source_root_relative_resolved_paths": path_report["source_root_relative_resolved_paths"],
        },
        "stage5ed_preservation": _stage5ed_preservation_record(base, false_flags, stage5ed),
        "stage5eb_preservation": _stage5eb_preservation_record(base, false_flags, stage5eb),
        "chatgpt_context_update_summary": {
            **base,
            "record_type": "stage5ee_chatgpt_context_update_summary",
            "chatgpt_context_updated": _context_contains_stage5ee(),
            "chatgpt_context_path": CHATGPT_CONTEXT_PATH.as_posix(),
            "durable_facts_added": _context_contains_stage5ee(),
            "raw_source_body_included": False,
            "long_prompt_text_included": False,
        },
        "reviewability_gap_register": {
            **base,
            "record_type": "stage5ee_reviewability_gap_register",
            "remaining_gap": "continue_number_fact_review_batches",
            "next_batch_recommended": "number_fact_review_batch_006",
            "lag5_phenomenon_source_locked_by_stage5ee": False,
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
            "post_push_handoff_locations": ["codex-output/stage5ee-codex-completion.md", "GitHub issue comment"],
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
        "record_type": "stage5ee_next_stage_decision",
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
        "record_type": "stage5ee_review_batch_selection",
        "schema": SCHEMA_PATHS["review_batch_selection"].as_posix(),
        "review_batch_id": REVIEW_BATCH_ID,
        "review_batch_selection_policy": REVIEW_BATCH_SELECTION_POLICY,
        "review_scope": "selected_20_source_records_only",
        "reviewed_entry_count": EXPECTED_REVIEWED_ENTRY_COUNT,
        "selected_source_record_paths": SELECTED_SOURCE_RECORD_PATHS,
        "selection_clusters": ["source_register", "music_metadata", "fandom_crosswalk", "residual_numberfacts"],
        "historical_source_lock_records_rewritten": False,
        "source_lock_evidence_updated_now": False,
    }


def _stage5ed_preservation_record(
    base: dict[str, Any], false_flags: dict[str, bool], stage5ed: dict[str, Any]
) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "stage5ee_stage5ed_preservation",
        "stage5ed_preserved": True,
        "stage5ed_status": stage5ed.get("status", "complete"),
        "stage5ed_review_batch_id": stage5ed.get("review_batch_id"),
        "stage5ed_reviewed_entry_count": stage5ed.get("reviewed_entry_count", 20),
        "stage5ed_overlay_count": stage5ed.get("overlay_count", 25),
        "stage5ed_fact_card_count_after_stage5ed": stage5ed.get("fact_card_count_after_stage5ed", 142),
        "stage5ed_source_browser_validation_error_count": stage5ed.get("source_browser_validation_error_count", 0),
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
        "record_type": "stage5ee_stage5eb_validation_policy_preservation",
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
            "record_type": "stage5ee_codex_handoff_policy",
            "canonical_codex_handoff_root": "codex-output",
            "deprecated_codex_output_root_used": False,
            "codex_output_used": False,
            "completion_summary_path": "codex-output/stage5ee-codex-completion.md",
            "completion_summary_committed": False,
        },
        "credential_redaction_policy_preservation": {
            **base,
            "record_type": "stage5ee_credential_redaction_policy_preservation",
            "credential_like_remote_count": 0,
            "credential_redaction_policy_preserved": True,
            "raw_source_body_included": False,
            "secret_material_committed": False,
        },
        "raw_source_noncommit_proof": {
            **base,
            **false_flags,
            "record_type": "stage5ee_raw_source_noncommit_proof",
            "raw_source_body_included": False,
            "raw_source_files_committed": False,
            "raw_third_party_files_committed": False,
            "generated_outputs_committed": False,
        },
    }


def _token_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    records["stage5dg_preservation"] = {
        **base,
        **false_flags,
        "record_type": "stage5ee_stage5dg_preservation",
        "source_stage_id": "stage-5dg",
        "preserved": True,
        "operator_approval_component_satisfied_preserved": True,
        "deep_research_acceptance_created_now": False,
        "combined_approval_gate_satisfied_now": False,
    }
    records["stage5bd_preservation"] = {
        **base,
        **false_flags,
        "record_type": "stage5ee_stage5bd_preservation",
        "source_stage_id": "stage-5bd",
        "preserved": True,
        "stage5bd_run_plan_id_count": 10,
        "stage5bd_run_plan_ids_preserved": True,
    }
    records["active_lineage_preservation"] = {
        **base,
        **false_flags,
        "record_type": "stage5ee_active_lineage_preservation",
        "active_lineage_record_count": 8,
        "preserved": True,
        "active_lineage_preserved": True,
    }
    records["no_active_ingestion_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ee_no_active_ingestion_proof",
        "gate_status": "closed",
        "active_ingestion_performed": False,
    }
    records["no_byte_stream_transition_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ee_no_byte_stream_transition_proof",
        "gate_status": "closed",
        "real_byte_stream_generated": False,
        "variant_byte_streams_generated": False,
        "byte_stream_generation_authorized_now": False,
    }
    records["no_execution_transition_proof"] = {
        **base,
        **false_flags,
        "record_type": "stage5ee_no_token_block_execution_proof",
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
        "record_type": "stage5ee_source_browser_number_fact_enrichment_overlay_collection",
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
            "record_type": {"const": "stage5ee_source_browser_number_fact_enrichment_overlay_collection"},
            "review_batch_id": {"const": REVIEW_BATCH_ID},
            "overlays": {"type": "array", "minItems": EXPECTED_OVERLAY_COUNT, "maxItems": EXPECTED_OVERLAY_COUNT},
        }
    )
    return schema


def _validate_required_paths() -> list[str]:
    paths = list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values()) + [OVERLAY_COLLECTION_PATH]
    return [f"required Stage 5EE path missing: {path.as_posix()}" for path in paths if not path.exists()]


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


def _validate_token_preservation(path_key: str, source_stage_id: str) -> Stage5EEValidationResult:
    payload = _load(TOKEN_PATHS[path_key])
    errors = _expect(payload, {"source_stage_id": source_stage_id, "preserved": True, "rewritten": False})
    return Stage5EEValidationResult(len(errors), _summary_counts(payload), errors)


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


def _context_contains_stage5ee() -> bool:
    if not CHATGPT_CONTEXT_PATH.exists():
        return False
    return "## Stage 5EE - Number-fact review batch 005" in CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8")


def _update_chatgpt_context() -> None:
    marker = "## Stage 5EE - Number-fact review batch 005"
    text = CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8") if CHATGPT_CONTEXT_PATH.exists() else ""
    if marker in text:
        return
    addition = f"""

{marker}

- Stage 5EE reviewed 20 selected source-register/music/fandom/residual NumberFacts source-lock entries and added 25 NumberFactCard overlays only.
- Stage 5EE did not rewrite historical source-lock records, add new source-lock evidence, select a target, generate byte streams, run routes, execute tools, or make a solve claim.
- Residual Stage 5DO facts now visible: pixel-table counts 12543/6327, 9901 digit-square candidate, and selection-bias quarantine.
- Original Stage 5DJ source metadata now visible: 7 music files, 4 MP3, 3 PDF, 761.MP3 ID3 v2.3.0 size 196, parable number 1595277641, and music factor/base60 facts.
- Stage 5DK Fandom source metadata now visible: 14 Fandom sources, trust-tier distribution, old index/canonical URL crosswalks, and raw body noncommit.
- Stage 5DI crosswalk metadata now visible: 6 web sources, IDDQD source-root crosswalk, number-triangle 5-file bundle, 6 source gaps, and 3 alias-map entries.
- Stage 5EB validation policy remains active: local/full-parallel validation uses 10 workers / 10 pytest workers, and full serial pytest is not part of normal completion.
- Stage 5EF should continue number-fact review batch 006 unless a blocking Source Browser issue appears.
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
                "Added review-only NumberFactCard overlays for the fifth selected 20-entry "
                "source-lock number-fact review batch."
            ),
            "key_outputs": [
                "Stage 5EE source-register/music/fandom/residual NumberFacts overlay collection with 25 review-only facts.",
                "Stage 5EE review-batch, preservation, loadability, scope, and validation records.",
                "Stage 5EF selected as the next number-fact review batch.",
            ],
            "result_status": "reviewability_overlays_only",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                f"Reviewed entries={summary.get('reviewed_entry_count')}, overlays={summary.get('overlay_count')}, "
                f"fact_cards_after={summary.get('fact_card_count_after_stage5ee')}. Historical source locks were not rewritten."
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
    payload["latest_completed_stage_prefix"] = "Stage 5EE"
    payload["next_stage_after_this_stage"] = NEXT_STAGE_TITLE
    payload["expected_next_stage_prefix"] = "Stage 5EF"
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
    text = f"""# Stage 5EE Codex Completion

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
    (CODEX_OUTPUT_DIR / "stage5ee-codex-completion.md").write_text(text, encoding="utf-8")
