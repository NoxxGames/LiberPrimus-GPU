"""Stage 5DX number-fact review batch 002 overlays.

This stage adds reviewability metadata only. It enriches Source Browser
NumberFactCards through overlays, preserves historical source-lock records, and
does not authorize target selection, route extraction, byte generation,
execution, CUDA, scoring, or solve claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP

STAGE_ID = "stage-5dx"
STAGE_TITLE = (
    "Stage 5DX - Source-lock number-fact review batch 002, visual/red-heading/"
    "transform bridge enrichment overlays, without execution"
)
PROMPT_TYPE = "codex_metadata_and_operator_console_reviewability_implementation"
SOURCE_PREVIOUS_STAGE_ID = "stage-5dw"
SOURCE_PREVIOUS_STAGE_TITLE = (
    "Stage 5DW - Source-lock number-fact review batch 001, high-signal "
    "enrichment overlays, without execution"
)
SOURCE_PREVIOUS_STAGE_STARTING_COMMIT = "fe8d3d002defe18de0414dc7b14a5a68293094a7"
SOURCE_PREVIOUS_STAGE_FINAL_COMMIT = "8fc6f36878b56cc529fa81b68a291c5cf54ab16d"
SOURCE_PREVIOUS_ISSUE = 158
SOURCE_PREVIOUS_CI_RUN = 27233448832
SOURCE_PREVIOUS_CI_STATUS = "passed"
NEXT_STAGE_ID = "stage-5dy"
NEXT_STAGE_TITLE = "Stage 5DY - Operator/assistant source-lock number-fact review batch 3, without execution"
REVIEW_BATCH_ID = "number_fact_review_batch_002_visual_transform"
REVIEW_BATCH_SELECTION_POLICY = "assistant_operator_high_signal_visual_red_heading_transform_batch"
EXPECTED_REVIEWED_ENTRY_COUNT = 20
EXPECTED_OVERLAY_COUNT = 23
OVERLAY_COLLECTION_PATH = Path(
    "data/operator-console/source-browser/number-fact-overlays/"
    "stage5dx-review-batch-002-visual-transform-overlays.yaml"
)
OVERLAY_SCHEMA_PATH = Path("schemas/operator-console/source-browser-number-fact-enrichment-overlay-v0.schema.json")
CHATGPT_CONTEXT_PATH = Path("ChatGPT-ContextFile.md")

PROJECT_STATE_DIR = Path("data/project-state")
SOURCE_BROWSER_DIR = Path("data/operator-console/source-browser")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
TOKEN_BLOCK_DIR = Path("data/token-block")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5dx-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5dx-next-stage-decision.yaml",
    "stage5dw_preservation": PROJECT_STATE_DIR / "stage5dx-stage5dw-preservation.yaml",
    "source_browser_loadability": PROJECT_STATE_DIR / "stage5dx-source-browser-loadability-summary.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5dx-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5dx-reviewability-gap-register.yaml",
    "scope_control": PROJECT_STATE_DIR / "stage5dx-scope-control.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage5dx-chatgpt-context-update-summary.yaml",
}

SOURCE_BROWSER_PATHS: dict[str, Path] = {
    "review_batch_result": SOURCE_BROWSER_DIR
    / "number-fact-review-batches/stage5dx-review-batch-002-visual-transform-result.yaml",
    "review_batch_entry_status": SOURCE_BROWSER_DIR
    / "number-fact-review-batches/stage5dx-review-batch-002-entry-status.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5dx-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5dx-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5dx-raw-source-noncommit-proof.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "stage5dg_preservation": TOKEN_BLOCK_DIR / "stage5dx-stage5dg-preservation.yaml",
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5dx-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5dx-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5dx-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR / "stage5dx-no-byte-stream-transition-proof.yaml",
    "no_token_block_execution_proof": TOKEN_BLOCK_DIR / "stage5dx-no-token-block-execution-proof.yaml",
}

DATA_PATHS: dict[str, Path] = {}
DATA_PATHS.update(PROJECT_STATE_PATHS)
DATA_PATHS.update(SOURCE_BROWSER_PATHS)
DATA_PATHS.update(SOURCE_HARVESTER_PATHS)
DATA_PATHS.update(TOKEN_PATHS)

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5dx-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5dx-next-stage-decision-v0.schema.json"),
    "stage5dw_preservation": Path("schemas/project-state/stage5dx-stage5dw-preservation-v0.schema.json"),
    "source_browser_loadability": Path(
        "schemas/project-state/stage5dx-source-browser-loadability-summary-v0.schema.json"
    ),
    "reviewable_validation_evidence": Path(
        "schemas/project-state/stage5dx-reviewable-validation-evidence-v0.schema.json"
    ),
    "reviewability_gap_register": Path("schemas/project-state/stage5dx-reviewability-gap-register-v0.schema.json"),
    "scope_control": Path("schemas/project-state/stage5dx-scope-control-v0.schema.json"),
    "chatgpt_context_update_summary": Path(
        "schemas/project-state/stage5dx-chatgpt-context-update-summary-v0.schema.json"
    ),
    "review_batch_result": Path(
        "schemas/operator-console/stage5dx-source-browser-number-fact-review-batch-result-v0.schema.json"
    ),
    "review_batch_entry_status": Path(
        "schemas/operator-console/stage5dx-source-browser-number-fact-entry-status-v0.schema.json"
    ),
    "codex_handoff_policy": Path("schemas/source-harvester/stage5dx-codex-handoff-policy-v0.schema.json"),
    "credential_redaction_policy_preservation": Path(
        "schemas/source-harvester/stage5dx-credential-redaction-policy-preservation-v0.schema.json"
    ),
    "raw_source_noncommit_proof": Path("schemas/source-harvester/stage5dx-raw-source-noncommit-proof-v0.schema.json"),
    "generic_token_block": Path("schemas/token-block/stage5dx-generic-record-v0.schema.json"),
    "no_token_block_execution_proof": Path(
        "schemas/token-block/stage5dx-no-token-block-execution-proof-v0.schema.json"
    ),
}

SCHEMA_BY_DATA_KEY: dict[str, str] = {
    "summary": "summary",
    "next_stage_decision": "next_stage_decision",
    "stage5dw_preservation": "stage5dw_preservation",
    "source_browser_loadability": "source_browser_loadability",
    "reviewable_validation_evidence": "reviewable_validation_evidence",
    "reviewability_gap_register": "reviewability_gap_register",
    "scope_control": "scope_control",
    "chatgpt_context_update_summary": "chatgpt_context_update_summary",
    "review_batch_result": "review_batch_result",
    "review_batch_entry_status": "review_batch_entry_status",
    "codex_handoff_policy": "codex_handoff_policy",
    "credential_redaction_policy_preservation": "credential_redaction_policy_preservation",
    "raw_source_noncommit_proof": "raw_source_noncommit_proof",
    "no_token_block_execution_proof": "no_token_block_execution_proof",
}

SELECTED_SOURCE_RECORD_PATHS = [
    "data/historical-route/stage5du-red-runes-enlightened-mumons-comment-155-551-candidate-v0.yaml",
    "data/historical-route/stage5du-red-runes-prime742-continue-this-candidate-v0.yaml",
    "data/historical-route/stage5du-red-runes-key682-speech-tongue-sentence-candidate-v0.yaml",
    "data/historical-route/stage5du-red-runes-first-two-indices31-mumon-word-position-candidate-v0.yaml",
    "data/historical-route/stage5du-big-gap-red-subset-one-based-sum-229-candidate-v0.yaml",
    "data/historical-route/stage5du-lp-line-gap-metric-73-109-129-candidate-v0.yaml",
    "data/historical-route/stage5du-wing-tree-641-709-prime-index-gap11-candidate-v0.yaml",
    "data/historical-route/stage5du-stardust-phrase-gp2540-threshold254-candidate-v0.yaml",
    "data/historical-route/stage5du-mayfly-star-artifact-72-600-twinprime-gap-candidate-v0.yaml",
    "data/historical-route/stage5du-lp-page-icc-profile-boundary-candidate-v0.yaml",
    "data/historical-route/stage5du-page15-your-truth-crib-pointer-candidate-v0.yaml",
    "data/historical-route/stage5du-divinity-within-491-563-1229-crosslink-v0.yaml",
    "data/historical-route/stage5du-dead-tree-yggdrasil-gp491-bridge-candidate-v0.yaml",
    "data/historical-route/stage5du-page54-55-a-postlude-red-heading-candidate-v1.yaml",
    "data/historical-route/stage5du-mobius-totient-zero-class-gp-alphabet-candidate-v0.yaml",
    "data/historical-route/stage5du-page0-divinity-within-crossroads-gp491-candidate-v0.yaml",
    "data/historical-route/stage5ds-pdd153-56311-ouroboric-cycle-candidate-v0.yaml",
    "data/historical-route/stage5ds-pdd153-ouroboros-167-mod153-offset14-candidate-v0.yaml",
    "data/historical-route/stage5dn-disk-56311-wynn-way-bridge-v1.yaml",
    "data/historical-route/stage5ds-ouroboros-gp-167-music-cycle-candidate-v0.yaml",
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
    "scoring_performed",
    "semantic_image_interpretation_performed",
    "solve_claim",
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

OVERLAY_ROWS: list[dict[str, Any]] = [
    {
        "overlay_id": "stage5dx_red_runes_enlightened_mumons_index155_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[0],
        "source_fact_id": "red_runes_enlightened_mumons_index155",
        "fact_class": "red_runes_gateless_gate_number_facts",
        "display_label": "ENLIGHTENED and MUMON'S COMMENT both have zero-based GP index sum 155",
        "short_label": "ENLIGHTENED = MUMON'S COMMENT = 155 index",
        "value": 155,
        "values": [155],
        "value_type": "gp_sum",
        "operation_type": "symbolic_gp_scan",
        "expression": "ENLIGHTENED zero-based GP index sum = 155; MUMON'S COMMENT zero-based GP index sum = 155",
        "relation": "Links the proposed koan title word ENLIGHTENED to the Mumon commentary layer of The Gateless Gate case.",
        "why_stored": "This is a semantic title-to-commentary bridge, not just a bare number match.",
        "verification_status": "arithmetic_verified_metadata_only",
        "display_priority": "high",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[0], "third_party/RedRunes_Possible_Koan_Connection/messages.txt"],
        "crosslinks": ["red_runes_gateless_gate_koan20_title_candidate_v0", "solved_koan_gp_facts_candidate_v0"],
        "risk_notes": [
            "red_rune_transcription_required",
            "page_index_convention_required",
            "spelling_warning_MUMON_not_MUMMON",
        ],
    },
    {
        "overlay_id": "stage5dx_red_runes_enlightened_mumons_prime551_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[0],
        "source_fact_id": "red_runes_enlightened_mumons_prime551",
        "fact_class": "red_runes_gateless_gate_number_facts",
        "display_label": "ENLIGHTENED and MUMON'S COMMENT both have GP prime sum 551",
        "short_label": "ENLIGHTENED = MUMON'S COMMENT = 551 prime-sum",
        "value": 551,
        "values": [551],
        "value_type": "gp_sum",
        "operation_type": "symbolic_gp_scan",
        "expression": "ENLIGHTENED GP prime sum = 551; MUMON'S COMMENT GP prime sum = 551",
        "relation": "Same semantic bridge as the 155 index-sum fact, but under normal GP prime-value summation.",
        "why_stored": "Dual index/prime equality makes the title-comment bridge easier to review in the Source Browser.",
        "verification_status": "arithmetic_verified_metadata_only",
        "display_priority": "high",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[0], "third_party/RedRunes_Possible_Koan_Connection/messages.txt"],
        "risk_notes": ["selection_bias_control_required", "exact_tokenization_policy_required"],
    },
    {
        "overlay_id": "stage5dx_red_runes_prime742_continue_this_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[1],
        "source_fact_id": "red_runes_prime742_continue_this",
        "fact_class": "red_runes_gateless_gate_number_facts",
        "display_label": "Red-rune GP prime sum 742 matches LET ANOTHER CONTINUE THIS = 742",
        "short_label": "Red-runes = LET ANOTHER CONTINUE THIS = 742",
        "value": 742,
        "values": [742],
        "value_type": "gp_sum",
        "operation_type": "gp_sum",
        "expression": "red-rune GP prime sum = 742; LET ANOTHER CONTINUE THIS GP prime sum = 742",
        "relation": "Links the red-rune string to a partial final-line phrase from The Enlightened Man koan.",
        "why_stored": "The phrase continue this is contextually relevant but the omitted final word POEM must stay visible as a warning.",
        "verification_status": "canonical_source_required",
        "display_priority": "high",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[1], "third_party/RedRunes_Possible_Koan_Connection/messages.txt"],
        "risk_notes": [
            "partial_line_match_warning",
            "omitted_final_word_POEM",
            "red_rune_transcription_required",
            "selection_bias_control_required",
        ],
    },
    {
        "overlay_id": "stage5dx_red_runes_key682_speech_tongue_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[2],
        "source_fact_id": "red_runes_key682_speech_tongue",
        "fact_class": "red_runes_gateless_gate_number_facts",
        "display_label": "Red-to-title key prime sum 682 matches speech/tongue sentence index sum 682",
        "short_label": "Key sum 682 -> speech/tongue sentence 682",
        "value": 682,
        "values": [682],
        "value_type": "gp_sum",
        "operation_type": "sequence_mapping",
        "expression": "Under P=(C+K) mod 29, the derived key indices have GP prime sum 682; the koan speech/tongue sentence has zero-based GP index sum 682.",
        "relation": "Connects the target-derived key stream to an internal koan sentence about speech/tongue, echoing LP voice/body themes.",
        "why_stored": "This is a potentially meaningful internal-koan bridge, but the key is target-derived and therefore overfit-prone.",
        "verification_status": "canonical_source_required",
        "display_priority": "medium",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[2]],
        "crosslinks": ["solved_i_voice_of_circumference_precedent_v0"],
        "risk_notes": ["key_stream_overfit_warning", "target_plaintext_chosen_first", "exact_gp_tokenization_required"],
    },
    {
        "overlay_id": "stage5dx_red_runes_first_two_indices31_mumon_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[3],
        "source_fact_id": "red_runes_first_two_indices31_mumon",
        "fact_class": "red_runes_gateless_gate_number_facts",
        "display_label": "First two red-rune indices 20+11 = 31; word 31 claim points to Mumon's",
        "short_label": "First two red-rune indices = 31 -> Mumon's",
        "value": 31,
        "values": [20, 11, 31],
        "value_type": "word_count",
        "operation_type": "sum",
        "expression": "20 + 11 = 31",
        "relation": "Provides a weak but reviewable pointer from the first red-rune pair to the Mumon commentary layer by word position.",
        "why_stored": "Keeps the exact counting convention visible instead of hiding this as a vague word-position coincidence.",
        "verification_status": "canonical_source_required",
        "display_priority": "low",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[3]],
        "risk_notes": [
            "word_count_policy_required",
            "title_exclusion_policy_required",
            "low_confidence_word_position_bridge",
        ],
    },
    {
        "overlay_id": "stage5dx_big_gap_red_subset_229_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[4],
        "source_fact_id": "big_gap_red_subset_one_based_sum_229",
        "fact_class": "gap_layout_number_facts",
        "display_label": "Big-gap pages with clear red elements have one-based page sum 229",
        "short_label": "Big-gap red subset sum = 229",
        "value": 229,
        "values": [4, 10, 43, 53, 56, 57, 229],
        "value_type": "sum",
        "operation_type": "sum",
        "expression": "one-based pages 5 + 11 + 44 + 54 + 57 + 58 = 229",
        "relation": "Candidate bridge between red visual elements in big-gap pages and the Mayfly 167/229/229/229/104 axis.",
        "why_stored": "Preserves the red-subset relation separately from the broader 16-page big-gap set.",
        "verification_status": "canonical_image_required",
        "display_priority": "medium",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[4], "third_party/BigGapsFoundInLiberPrimus/messages.txt"],
        "crosslinks": ["mayfly_horizontal_axis_167_229_229_229_104_candidate_v0"],
        "risk_notes": [
            "red_threshold_policy_required",
            "selection_bias_control_required",
            "page_indexing_policy_required",
        ],
    },
    {
        "overlay_id": "stage5dx_line_gap_metric_73_109_129_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[5],
        "source_fact_id": "lp_line_gap_metric_73_109_129",
        "fact_class": "gap_layout_number_facts",
        "display_label": "Claimed LP line gaps: regular 73 px, big 109 px, parable 129 px; 109=prime(29)",
        "short_label": "Line gaps 73/109/129; 109=prime(29)",
        "value": 109,
        "values": [73, 109, 36, 129, 56, 29, 31, 37],
        "value_type": "coordinate",
        "operation_type": "source_observation",
        "expression": "regular gap 73; big gap 109; difference 36; parable gap 129; parable difference 56; 109 = prime(29)",
        "relation": "Candidate layout/negative-space metric where the big-gap value 109 corresponds to GP EA and one-indexed prime(29).",
        "why_stored": "Makes the measurement policy, GP-value notes, and correction of the source's I/J claim reviewable.",
        "verification_status": "canonical_image_required",
        "display_priority": "medium",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[5]],
        "risk_notes": [
            "measurement_policy_required",
            "crop_scale_threshold_must_be_declared",
            "source_thread_claim_37_is_i_corrected_to_I_31_J_37",
        ],
    },
    {
        "overlay_id": "stage5dx_wing_tree_641_709_prime_index_gap11_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[6],
        "source_fact_id": "wing_tree_641_709_prime_index_gap11",
        "fact_class": "star_artifact_pixel_number_facts",
        "display_label": "Tree edge offsets 641 and 709 are primes with prime-index gap 11",
        "short_label": "Tree offsets 641/709 -> prime-index gap 11",
        "value": 11,
        "values": [641, 709, 116, 127, 11, 107, 167, 229, 28, 39, 50],
        "value_type": "prime_index",
        "operation_type": "prime_index_lookup",
        "expression": "primepi(641)=116; primepi(709)=127; 127-116=11; prior pattern 107/167/229 has indices 28/39/50 with step 11.",
        "relation": "Links StarArtifacts tree-edge measurement to the 167/229 prime-index axis already present in Mayfly and music/disk context.",
        "why_stored": "This is one of the more constrained pixel-measurement facts in the star-artifact thread.",
        "verification_status": "canonical_image_required",
        "display_priority": "high",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[6], "third_party/StarArtifactsInLPPageImages/messages.txt"],
        "crosslinks": [
            "page32_tree_polar_route_v0",
            "mayfly_horizontal_axis_167_229_229_229_104_candidate_v0",
            "instar_title_761_duration_167_bridge_v1",
        ],
        "risk_notes": [
            "canonical_coordinate_policy_required",
            "exact_image_hash_required",
            "measurement_selection_bias_warning",
        ],
    },
    {
        "overlay_id": "stage5dx_stardust_phrase_2540_threshold254_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[7],
        "source_fact_id": "stardust_phrase_gp2540_threshold254",
        "fact_class": "star_artifact_pixel_number_facts",
        "display_label": "Unverified STARDUST phrase GP sum 2540 = exact threshold 254 x 10",
        "short_label": "STARDUST phrase 2540 = 254x10",
        "value": 2540,
        "values": [2540, 254, 10],
        "value_type": "gp_sum",
        "operation_type": "product",
        "expression": "THE STARDUST FROM WHEN LIFE ENDS WILL SWIRL AGAIN ALONG AND START = 2540; 2540 = 254 * 10",
        "relation": "Candidate bridge between an unverified community decode phrase and the exact RGB/max-channel 254 star-artifact threshold.",
        "why_stored": "The arithmetic is compact and thematically relevant, but the phrase source remains unverified and must stay quarantined from proof/route use.",
        "verification_status": "quarantined_selection_bias",
        "display_priority": "medium",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[7]],
        "risk_notes": [
            "unverified_community_decode_screenshot",
            "not_accepted_plaintext",
            "exact_gp_tokenization_required",
            "selection_bias_control_required",
        ],
    },
    {
        "overlay_id": "stage5dx_mayfly_star_72_600_twinprime_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[8],
        "source_fact_id": "mayfly_star_72_600_twinprime_gap",
        "fact_class": "star_artifact_pixel_number_facts",
        "display_label": "Mayfly star-artifact coordinate gaps 72 and 600 sit between twin primes",
        "short_label": "Mayfly star gaps 72/600 between twin primes",
        "value": 72,
        "values": [72, 71, 73, 600, 599, 601],
        "value_type": "coordinate",
        "operation_type": "source_observation",
        "expression": "72 lies between twin primes 71 and 73; 600 lies between twin primes 599 and 601.",
        "relation": "Candidate visual-coordinate bridge on Mayfly pages, relevant because Mayfly already has strong grid/axis source-locks.",
        "why_stored": "Keeps this low/medium confidence coordinate claim visible with its selection-risk warning.",
        "verification_status": "canonical_image_required",
        "display_priority": "low",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[8]],
        "crosslinks": ["mayfly_instar_grid_analysis_candidate_v1"],
        "risk_notes": ["coordinate_selection_risk", "full_component_register_required", "exact_image_hash_required"],
    },
    {
        "overlay_id": "stage5dx_lp_page_icc_profile_boundary_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[9],
        "source_fact_id": "lp_page_icc_profile_boundary_00_16_17_74",
        "fact_class": "page_image_production_metadata_number_facts",
        "display_label": "LP page ICC boundary claim: pages 00-16 no ICC; pages 17-74 share 2576-byte ICC profile",
        "short_label": "ICC boundary 00-16 vs 17-74; profile length 2576",
        "value": 2576,
        "values": [0, 16, 17, 74, 2576],
        "value_type": "file_size",
        "operation_type": "source_observation",
        "expression": "pages 00-16 have no ICC profile; pages 17-74 share same ICC profile; ICC length claim 2576 bytes.",
        "relation": "Production-boundary metadata that may explain or contextualize visual artefacts without treating them as cipher evidence.",
        "why_stored": "Helps separate visual-production metadata from intended clue claims during future image review.",
        "verification_status": "canonical_image_required",
        "display_priority": "medium",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[9]],
        "risk_notes": ["production_metadata_not_clue_proof", "canonical_image_hash_required"],
    },
    {
        "overlay_id": "stage5dx_page15_instruction_phrase_prime_cluster_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[10],
        "source_fact_id": "page15_instruction_phrase_prime_cluster",
        "fact_class": "page15_internal_instruction_number_facts",
        "display_label": "Page15/internal instruction phrases have prime GP sums 353, 383, 727, 971, 571, 769",
        "short_label": "Instruction phrase GP primes: 353/383/727/971/571/769",
        "value": 353,
        "values": [353, 383, 727, 971, 179, 571, 769, 547],
        "value_type": "gp_sum",
        "operation_type": "symbolic_gp_scan",
        "expression": "FIND YOUR TRUTH=353; FOLLOW YOUR TRUTH=383; KWESTION ALL THINGS=727; DISCOVER TRUTH INSIDE YOURSELF=971 (reverse 179); IMPOSE NOTHING ON OTHERS=571; EXPERIENCE YOUR DEATH=769; ALONG THE WAY=547.",
        "relation": "Internal instruction/crib-pointer phrase cluster, including ALONG THE WAY=547 as a possible music/Interconnectedness bridge.",
        "why_stored": "Consolidates the Page15/internal-instruction GP facts into a reviewable card and preserves the tokenization warning.",
        "verification_status": "arithmetic_verified_metadata_only",
        "display_priority": "medium",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[10], "third_party/CribbingPage15/messages.txt"],
        "crosslinks": [
            "music_transform_grammar_for_cipher_methods_candidate_v1",
            "interconnectedness_547_beats_137_measures_candidate_v0",
        ],
        "risk_notes": [
            "page15_YOUR_TRUTH_standard_token_lengths_4_4_not_clean_4_5",
            "phrase_selection_bias_warning",
        ],
    },
    {
        "overlay_id": "stage5dx_divinity_within_491_563_1229_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[11],
        "source_fact_id": "divinity_within_491_563_1229_crosslink",
        "fact_class": "red_heading_gp491_number_facts",
        "display_label": "DIVINITY WITHIN=491; THE DIVINITY WITHIN=563; FIND THE DIVINITY WITHIN AND EMERGE=1229",
        "short_label": "DIVINITY WITHIN 491/563/1229 crosslink",
        "value": 491,
        "values": [491, 563, 1229],
        "value_type": "gp_sum",
        "operation_type": "symbolic_gp_scan",
        "expression": "DIVINITY WITHIN=491; THE DIVINITY WITHIN=563; FIND THE DIVINITY WITHIN AND EMERGE=1229.",
        "relation": "Crosslinks Page0 red-heading theory, 2016 tree-dimension context, and Instar parable/divinity-emergence music context.",
        "why_stored": "This is a compact cross-family number bridge spanning music, red headings, and 2016 tree context.",
        "verification_status": "arithmetic_verified_metadata_only",
        "display_priority": "high",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[11]],
        "crosslinks": [
            "stage5ds-instar-parable-id3-gp-product-candidate-v1",
            "page0_divinity_within_crossroads_gp491_candidate_v0",
            "2016_message_route_meta_clue_v0",
        ],
        "risk_notes": ["phrase_selection_bias_warning", "symbolic_context_only"],
    },
    {
        "overlay_id": "stage5dx_dead_tree_yggdrasil_491_564_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[12],
        "source_fact_id": "dead_tree_yggdrasil_491_564",
        "fact_class": "red_heading_gp491_number_facts",
        "display_label": "YGGDRASIL = 491, but YGGDRASILL = 564; one-L spelling required for GP491 bridge",
        "short_label": "YGGDRASIL=491; YGGDRASILL=564",
        "value": 491,
        "values": [491, 564],
        "value_type": "gp_sum",
        "operation_type": "gp_sum",
        "expression": "YGGDRASIL=491; YGGDRASILL=564.",
        "relation": "Keeps the spelling-sensitive tree/Yggdrasil bridge explicit for the Page54/55 red-heading GP491 family.",
        "why_stored": "Prevents silent spelling drift from making the GP491 bridge look more robust than it is.",
        "verification_status": "arithmetic_verified_metadata_only",
        "display_priority": "medium",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[12], "third_party/PotentialCrib_RedRunes_Pages_54_55/messages.txt"],
        "risk_notes": ["spelling_sensitive", "subjective_image_label_warning"],
    },
    {
        "overlay_id": "stage5dx_page54_55_a_postlude_structure_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[13],
        "source_fact_id": "page54_55_a_postlude_1_8_structure_491",
        "fact_class": "red_heading_gp491_number_facts",
        "display_label": "Page54/55 red heading has 1/8 structure; proposed A POSTLUDE belongs to GP491 family",
        "short_label": "Page54/55 1/8 -> A POSTLUDE=491",
        "value": 491,
        "values": [1, 8, 491],
        "value_type": "gp_sum",
        "operation_type": "source_observation",
        "expression": "red-heading word count 2 with group lengths 1 and 8; proposed plaintext A POSTLUDE; A POSTLUDE=491 in the GP491 family.",
        "relation": "Links red-heading visible structure to a semantically selected GP491 candidate for the ending/postlude section.",
        "why_stored": "Records the structural 1/8 constraint separately from the broader GP491 family card.",
        "verification_status": "canonical_transcript_required",
        "display_priority": "medium",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[13]],
        "crosslinks": ["red_heading_marginalia_gp491_equivalence_family_v0"],
        "risk_notes": [
            "A_POSTLUDE_not_unique_by_gp_alone",
            "semantic_manual_selection_warning",
            "red_heading_transcription_required",
        ],
    },
    {
        "overlay_id": "stage5dx_mobius_totient_zero_class_14_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[14],
        "source_fact_id": "mobius_totient_zero_class_14_runes",
        "fact_class": "mobius_totient_method_number_facts",
        "display_label": "Mobius/totient zero-class partition contains 14 GP tokens/rune classes",
        "short_label": "mu(phi(p)) zero class = 14 tokens",
        "value": 14,
        "values": [14],
        "value_type": "sequence",
        "operation_type": "source_observation",
        "expression": "For each rune prime p, compute phi(p)=p-1 and mu(p-1); zero class includes TH, C/K, G, W, N, J, EO, S/Z, B, L, D, A, AE, EA.",
        "relation": "Converts the community Mobius/totient method into a reviewable method-fact card without accepting any page0 plaintext.",
        "why_stored": "This is deterministic arithmetic-method context and may bridge visual Mobius references to the arithmetic Mobius function.",
        "verification_status": "canonical_source_required",
        "display_priority": "high",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[14], "third_party/Mobius_totient_first_page_theory/messages.txt"],
        "crosslinks": ["page32_moebius_fibonacci_prime_index_spiral_v1", "disk_p39_row1_math_semantic_cluster_v1"],
        "risk_notes": [
            "proposed_plaintext_not_accepted",
            "community_code_not_executed",
            "deterministic_reimplementation_required_before_experiment",
        ],
    },
    {
        "overlay_id": "stage5dx_page0_divinity_crossroads_491_8_5_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[15],
        "source_fact_id": "page0_divinity_within_crossroads_491_8_5",
        "fact_class": "mobius_totient_method_number_facts",
        "display_label": "Page0 red heading claim: 8/5 groups; DIVINITY WITHIN = A CROSSROADS = 491",
        "short_label": "Page0 8/5; DIVINITY WITHIN=A CROSSROADS=491",
        "value": 491,
        "values": [8, 5, 491],
        "value_type": "gp_sum",
        "operation_type": "gp_sum",
        "expression": "Page0 red-heading group lengths claimed as 8 and 5; proposed plaintext DIVINITY WITHIN; DIVINITY WITHIN=491 and A CROSSROADS=491.",
        "relation": "Links the page0 red-heading theory, GP491 family, and Mobius/totient zero-preservation claim.",
        "why_stored": "Keeps visible structure, GP equivalence, and non-acceptance warnings in one review card.",
        "verification_status": "canonical_transcript_required",
        "display_priority": "high",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[15]],
        "crosslinks": ["divinity_within_491_563_1229_crosslink_v0", "red_heading_marginalia_gp491_equivalence_family_v0"],
        "risk_notes": [
            "red_heading_not_accepted_as_decrypted",
            "zero_class_alignment_claim_requires_control_test",
            "page0_plaintext_not_accepted",
        ],
    },
    {
        "overlay_id": "stage5dx_pdd153_56311_ouroboric_cycle_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[16],
        "source_fact_id": "pdd153_56311_ouroboric_cycle_25_153_612",
        "fact_class": "pdd_153_triangle_number_facts",
        "display_label": "Repeated 56311 has net +25; gcd(25,153)=1; 4-phase closed period = 612",
        "short_label": "56311 cycle: sum25, gcd(25,153)=1, period612",
        "value": 612,
        "values": [5, 6, 3, 11, 25, 153, 1, 4, 612],
        "value_type": "sequence",
        "operation_type": "modulo",
        "expression": "sequence [5,6,3,11] has sum 25; gcd(25,153)=1; phase count 4; closed state period 4*153=612.",
        "relation": "Static ouroboric-cycle property for PDD-153 / 56311 without extracting any route output.",
        "why_stored": "This is the strongest constrained mathematical consequence of the ouroboros/56311 idea.",
        "verification_status": "arithmetic_verified_metadata_only",
        "display_priority": "high",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[16]],
        "crosslinks": ["pdd_153_triangle_56311_wynn_way_route_v1", "disk_56311_wynn_way_bridge_v1"],
        "risk_notes": ["route_extraction_not_performed", "not_an_execution_seed_now"],
    },
    {
        "overlay_id": "stage5dx_pdd153_ouroboros_167_offset14_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[17],
        "source_fact_id": "pdd153_ouroboros_167_minus_153_offset14",
        "fact_class": "pdd_153_triangle_number_facts",
        "display_label": "OUROBOROS GP 167 minus PDD-153 word count gives offset 14",
        "short_label": "OUROBOROS 167 - 153 = 14",
        "value": 14,
        "values": [167, 153, 14],
        "value_type": "difference",
        "operation_type": "difference",
        "expression": "OUROBOROS GP sum 167; PDD body word count 153; 167 - 153 = 14.",
        "relation": "Links the ouroboros symbolic cycle to the PDD-153 surface and the 56311 cumulative offset 14.",
        "why_stored": "Keeps the arithmetic bridge explicit while preserving candidate-only status.",
        "verification_status": "arithmetic_verified_metadata_only",
        "display_priority": "medium",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[17]],
        "crosslinks": ["pdd_153_56311_ouroboric_cycle_candidate_v0", "ouroboros_gp_167_music_cycle_candidate_v0"],
        "risk_notes": ["symbolic_context_not_proof", "route_extraction_not_performed"],
    },
    {
        "overlay_id": "stage5dx_disk_56311_wynn_way_bridge_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[18],
        "source_fact_id": "disk_56311_wynn_way_center41_word52",
        "fact_class": "disk_triangle_bridge_number_facts",
        "display_label": "Disk sequence 56311 from triangle center 41/WYNN reaches word52/WAY via offsets 5/11/14/25",
        "short_label": "56311: center41 WYNN -> word52 WAY",
        "value": 52,
        "values": [5, 6, 3, 11, 41, 46, 52, 55, 66, 5, 11, 14, 25],
        "value_type": "sequence",
        "operation_type": "sequence_mapping",
        "expression": "center word index 41 plus cumulative offsets 5,11,14,25 gives positions 46,52,55,66; position 52 is the word52 WAY-derivation anchor.",
        "relation": "Bridges DiskCipher 56311/WYNN structure into the PDD-153 triangle center and WAY derivation candidate.",
        "why_stored": "This is the strongest DiskCipher-to-triangle numeric bridge and should be reviewable before target-priority planning.",
        "verification_status": "arithmetic_verified_metadata_only",
        "display_priority": "high",
        "source_paths": [SELECTED_SOURCE_RECORD_PATHS[18], "third_party/DiskCipherStuff/message_bodies.txt"],
        "crosslinks": [
            "pdd_153_triangle_56311_wynn_way_route_v1",
            "pdd_153_triangle_way_anchor_route_v1",
            "pdd_153_triangle_word_prime_route_v1",
        ],
        "risk_notes": ["accepted_as_route_false", "no_route_output_generated", "disk_cipher_model_not_validated"],
    },
    {
        "overlay_id": "stage5dx_ouroboros_gp167_music_cycle_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[19],
        "source_fact_id": "ouroboros_gp167_music_cycle",
        "fact_class": "ouroboros_self_reference_number_facts",
        "display_label": "OUROBOROS GP sum = 167, linking cycle/circumference context to Instar 761/167",
        "short_label": "OUROBOROS = 167",
        "value": 167,
        "values": [167, 761],
        "value_type": "gp_sum",
        "operation_type": "symbolic_gp_scan",
        "expression": "OUROBOROS = 167; crosslinked to Instar title/filename 761 and reverse 761 -> 167.",
        "relation": "Symbolic/numeric cycle bridge tying ouroboros, music/Instar, Mayfly/DiskCipher 167, and PDD-153 offset candidates.",
        "why_stored": "Keeps the cycle/self-reference 167 bridge distinct from the more speculative mythology context.",
        "verification_status": "arithmetic_verified_metadata_only",
        "display_priority": "medium",
        "source_paths": [
            SELECTED_SOURCE_RECORD_PATHS[19],
            "data/historical-route/stage5ds-instar-title-761-duration-167-bridge-v1.yaml",
        ],
        "crosslinks": [
            "instar_title_761_duration_167_bridge_v1",
            "pdd_153_ouroboros_167_mod153_offset14_candidate_v0",
            "mayfly_horizontal_axis_167_229_229_229_104_candidate_v0",
        ],
        "risk_notes": ["symbolic_context_not_proof", "not_target_priority_evidence_now"],
    },
    {
        "overlay_id": "stage5dx_red_runes_secondary_fact_cluster_summary_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[2],
        "source_fact_id": "red_runes_secondary_fact_cluster_summary",
        "fact_class": "red_runes_gateless_gate_number_facts",
        "display_label": "RedRunes secondary cluster: 155/551 title-comment, 742 continue-this, 682 speech/tongue, 31 Mumon word-position",
        "short_label": "RedRunes secondary cluster 155/551/742/682/31",
        "value": 682,
        "values": [155, 551, 742, 682, 31],
        "value_type": "sequence",
        "operation_type": "source_observation",
        "expression": "Cluster summary only; see individual overlays for details.",
        "relation": "Compact review chip tying together all Stage 5DX RedRunes secondary facts.",
        "why_stored": "Improves Source Browser scanability without replacing the detailed fact cards.",
        "verification_status": "canonical_source_required",
        "display_priority": "low",
        "source_paths": SELECTED_SOURCE_RECORD_PATHS[0:4],
        "risk_notes": ["summary_card_only", "not_independent_evidence"],
    },
    {
        "overlay_id": "stage5dx_visual_negative_space_fact_cluster_summary_overlay",
        "source_record_path": SELECTED_SOURCE_RECORD_PATHS[6],
        "source_fact_id": "visual_negative_space_fact_cluster_summary",
        "fact_class": "visual_negative_space_number_facts",
        "display_label": "Visual/negative-space cluster: 229 red subset, 73/109/129 gaps, 641/709 tree offsets, 2540 stardust, 72/600 Mayfly, 2576 ICC",
        "short_label": "Visual cluster 229/109/641-709/2540/72-600/2576",
        "value": 229,
        "values": [229, 73, 109, 129, 641, 709, 2540, 72, 600, 2576],
        "value_type": "sequence",
        "operation_type": "source_observation",
        "expression": "Cluster summary only; see individual overlays for details.",
        "relation": "Compact review chip tying together Stage 5DX visual/negative-space observations.",
        "why_stored": "Improves Source Browser scanability while retaining full risk warnings in detailed cards.",
        "verification_status": "canonical_image_required",
        "display_priority": "low",
        "source_paths": SELECTED_SOURCE_RECORD_PATHS[4:10],
        "risk_notes": ["summary_card_only", "not_independent_evidence", "canonical_image_controls_required"],
    },
]


@dataclass(frozen=True)
class Stage5DXValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5dx"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5dx() -> dict[str, dict[str, Any]]:
    _validate_stage5dw_baseline_for_build()
    _write_schemas()
    _write_overlay_collection()
    _update_chatgpt_context()
    records = _build_records()
    _write_records(records)
    _update_stage_summary_records(records["summary"])
    return records


def _validate_stage5dw_baseline_for_build() -> None:
    summary = _load(Path("data/project-state/stage5dw-summary.yaml"))
    expected = {
        "stage_id": "stage-5dw",
        "status": "complete",
        "reviewed_entry_count": 20,
        "overlay_count": 37,
        "overlay_only_fact_cards_supported": True,
        "overlay_only_fact_cards_validated": True,
        "source_browser_validation_error_count": 0,
        "fact_card_count_after_stage5dw": 53,
        "selected_batch_fact_card_count": 46,
        "historical_source_lock_records_rewritten": False,
        "pivot_target_selected_now": False,
        "route_extraction_performed_now": False,
        "real_byte_stream_generated": False,
        "execution_performed": False,
        "solve_claim": False,
        "recommended_next_stage_id": STAGE_ID,
    }
    errors = [
        f"Stage 5DW summary {key} expected {expected_value!r}, found {summary.get(key)!r}"
        for key, expected_value in expected.items()
        if summary.get(key) != expected_value
    ]
    if summary.get("overlay_collection_path") != (
        "data/operator-console/source-browser/number-fact-overlays/"
        "stage5dw-review-batch-001-high-signal-overlays.yaml"
    ):
        errors.append("Stage 5DW overlay_collection_path does not match the expected batch-001 overlay file")
    if errors:
        raise RuntimeError("Stage 5DW baseline is invalid for Stage 5DX: " + "; ".join(errors))


def validate_stage5dx() -> Stage5DXValidationResult:
    checks = [
        validate_stage5dx_review_batch_selection,
        validate_stage5dx_number_fact_overlays,
        validate_stage5dx_overlay_only_support,
        validate_stage5dx_source_browser_loadability,
        validate_stage5dx_stage5dw_preservation,
        validate_stage5dx_stage5dv_preservation,
        validate_stage5dx_stage5du_preservation,
        validate_stage5dx_stage5dg_preservation,
        validate_stage5dx_stage5bd_preservation,
        validate_stage5dx_active_lineage_preservation,
        validate_stage5dx_sidecar_gates,
        validate_stage5dx_handoff_continuity,
        validate_stage5dx_credential_redaction_policy,
        validate_stage5dx_governance_scope,
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
        "number_fact_review_batch_2_performed_now": True,
        "source_lock_entry_batch_review_performed_now": True,
        "reviewed_entry_count": EXPECTED_REVIEWED_ENTRY_COUNT,
        "overlay_count": EXPECTED_OVERLAY_COUNT,
        "overlay_only_fact_cards_supported": True,
        "overlay_only_fact_cards_validated": True,
        "historical_source_lock_records_rewritten": False,
        "number_fact_backfill_performed_now": False,
        "target_priority_decision_created_now": False,
        "pivot_target_selected_now": False,
        "route_extraction_performed_now": False,
        "real_byte_stream_generated": False,
        "execution_performed": False,
        "solve_claim": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"{PROJECT_STATE_PATHS['summary'].as_posix()}: {key} must be {value}")
    errors.extend(_required_false_errors(summary, PROJECT_STATE_PATHS["summary"].as_posix()))
    counts.update(_summary_counts(summary))
    counts["token_block_stage5dx_valid"] = not errors
    return Stage5DXValidationResult(len(errors), counts, errors)


def validate_stage5dx_review_batch_selection() -> Stage5DXValidationResult:
    payload = _load(PROJECT_STATE_PATHS["summary"])
    selected = payload.get("selected_source_record_paths", [])
    errors = []
    if payload.get("review_batch_id") != REVIEW_BATCH_ID:
        errors.append("Stage 5DX review batch id mismatch")
    if payload.get("reviewed_entry_count") != EXPECTED_REVIEWED_ENTRY_COUNT or len(selected) != 20:
        errors.append("Stage 5DX selected batch must contain exactly 20 records")
    if selected != SELECTED_SOURCE_RECORD_PATHS:
        errors.append("Stage 5DX selected source path order/content mismatch")
    missing = [path for path in selected if not Path(path).exists()]
    errors.extend(f"selected source path missing: {path}" for path in missing)
    if payload.get("review_scope") != "selected_20_source_records_only":
        errors.append("Stage 5DX review scope must be selected_20_source_records_only")
    return Stage5DXValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dx_number_fact_overlays() -> Stage5DXValidationResult:
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
    schema = _load(OVERLAY_SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for index, overlay in enumerate(overlays):
        for error in sorted(validator.iter_errors(overlay), key=lambda item: item.path):
            errors.append(f"overlay[{index}] {overlay.get('overlay_id')}: {error.message}")
        for key in ("source_record_path", "source_fact_id", "display_label", "relation", "why_stored"):
            if not overlay.get(key):
                errors.append(f"{overlay.get('overlay_id')}: missing {key}")
        if not overlay.get("verification_status"):
            errors.append(f"{overlay.get('overlay_id')}: missing verification_status")
        if not overlay.get("risk_notes"):
            errors.append(f"{overlay.get('overlay_id')}: missing risk_notes")
        if overlay.get("usable_for_decision_now") is not False:
            errors.append(f"{overlay.get('overlay_id')}: usable_for_decision_now must be false")
        not_allowed = set(overlay.get("not_allowed_as", []))
        for value in OVERLAY_REQUIRED_NOT_ALLOWED:
            if value not in not_allowed:
                errors.append(f"{overlay.get('overlay_id')}: not_allowed_as missing {value}")
    return Stage5DXValidationResult(
        len(errors),
        {
            "overlay_count": len(overlays),
            "reviewed_entry_count": collection.get("reviewed_entry_count"),
            "selected_source_path_count": len(selected),
        },
        errors,
    )


def validate_stage5dx_overlay_only_support() -> Stage5DXValidationResult:
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
        errors.append("Stage 5DX overlays must remain overlay-only review cards")
    return Stage5DXValidationResult(
        len(errors),
        {
            "selected_batch_fact_cards": selected_cards,
            "overlay_only_cards_required_count": overlay_only_cards,
        },
        errors,
    )


def validate_stage5dx_source_browser_loadability() -> Stage5DXValidationResult:
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
    if len(index.entries) < 1529:
        errors.append("Source Browser entry count regressed below Stage 5DW baseline")
    return Stage5DXValidationResult(len(errors), {**result.counts, **path_result.counts, **_summary_counts(payload)}, errors)


def validate_stage5dx_stage5dw_preservation() -> Stage5DXValidationResult:
    payload = _load(PROJECT_STATE_PATHS["stage5dw_preservation"])
    errors = []
    if payload.get("stage5dw_preserved") is not True:
        errors.append("Stage 5DW must be preserved")
    expected = {
        "stage5dw_reviewed_entry_count": 20,
        "stage5dw_overlay_count": 37,
        "stage5dw_source_browser_validation_error_count": 0,
        "stage5dw_historical_source_lock_records_rewritten": False,
        "stage5dw_target_selected": False,
        "stage5dw_route_extracted": False,
        "stage5dw_byte_streams_generated": False,
        "stage5dw_execution_performed": False,
        "stage5dw_solve_claim": False,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            errors.append(f"{key} must be {value}")
    return Stage5DXValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dx_stage5dv_preservation() -> Stage5DXValidationResult:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    errors = []
    if summary.get("stage5dv_path_canonicalization_preserved") is not True:
        errors.append("Stage 5DV path canonicalization repair must be preserved")
    if summary.get("spurious_root_image_paths_after") != 0:
        errors.append("spurious root image paths must remain 0")
    return Stage5DXValidationResult(len(errors), _summary_counts(summary), errors)


def validate_stage5dx_stage5du_preservation() -> Stage5DXValidationResult:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    errors = []
    if summary.get("stage5du_preserved") is not True:
        errors.append("Stage 5DU must be preserved")
    if summary.get("stage5du_thread_image_paths_under_third_party") is not True:
        errors.append("Stage 5DU thread image paths must remain third_party anchored")
    return Stage5DXValidationResult(len(errors), _summary_counts(summary), errors)


def validate_stage5dx_stage5dg_preservation() -> Stage5DXValidationResult:
    payload = _load(TOKEN_PATHS["stage5dg_preservation"])
    errors = []
    if payload.get("stage5dg_operator_approval_record_preserved") is not True:
        errors.append("Stage 5DG operator approval record must be preserved")
    if payload.get("combined_approval_gate_satisfied_now") is not False:
        errors.append("combined approval gate must remain unsatisfied")
    return Stage5DXValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dx_stage5bd_preservation() -> Stage5DXValidationResult:
    payload = _load(TOKEN_PATHS["stage5bd_preservation"])
    errors = []
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    return Stage5DXValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dx_active_lineage_preservation() -> Stage5DXValidationResult:
    payload = _load(TOKEN_PATHS["active_lineage_preservation"])
    errors = []
    if payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage count must remain 8")
    return Stage5DXValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dx_sidecar_gates() -> Stage5DXValidationResult:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for path in (
        TOKEN_PATHS["no_active_ingestion_proof"],
        TOKEN_PATHS["no_byte_stream_transition_proof"],
        TOKEN_PATHS["no_token_block_execution_proof"],
    ):
        payload = _load(path)
        counts[path.stem] = payload.get("gate_status")
        errors.extend(_required_false_errors(payload, path.as_posix()))
        if payload.get("gate_status") != "closed":
            errors.append(f"{path.as_posix()}: gate_status must be closed")
    return Stage5DXValidationResult(len(errors), counts, errors)


def validate_stage5dx_handoff_continuity() -> Stage5DXValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if payload.get("deprecated_codex_output_root_used") is not False or payload.get("codex_output_used") is not False:
        errors.append("deprecated codex_output root must not be used")
    if Path("codex_output").exists():
        errors.append("deprecated codex_output directory is present")
    return Stage5DXValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dx_credential_redaction_policy() -> Stage5DXValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["credential_redaction_policy_preservation"])
    errors = []
    if payload.get("credential_like_remote_count") != 0:
        errors.append("credential-like remote count must be 0")
    if payload.get("raw_source_body_included") is not False:
        errors.append("credential policy must not include raw source bodies")
    return Stage5DXValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dx_governance_scope() -> Stage5DXValidationResult:
    payload = _load(PROJECT_STATE_PATHS["scope_control"])
    errors = _required_false_errors(payload, PROJECT_STATE_PATHS["scope_control"].as_posix())
    if payload.get("source_lock_entry_batch_review_performed_now") is not True:
        errors.append("Stage 5DX must record source_lock_entry_batch_review_performed_now=true")
    if payload.get("number_fact_review_batch_2_performed_now") is not True:
        errors.append("Stage 5DX must record number_fact_review_batch_2_performed_now=true")
    if payload.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("next stage must be Stage 5DY")
    return Stage5DXValidationResult(len(errors), _summary_counts(payload), errors)


def stage5dx_summary_text() -> str:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5DX summary:",
        f"status={summary.get('status')}",
        f"review_batch_id={summary.get('review_batch_id')}",
        f"reviewed_entry_count={summary.get('reviewed_entry_count')}",
        f"overlay_count={summary.get('overlay_count')}",
        f"overlay_only_fact_cards_supported={summary.get('overlay_only_fact_cards_supported')}",
        f"source_browser_entries_loaded={summary.get('source_browser_entries_loaded')}",
        f"source_browser_records_scanned={summary.get('source_browser_records_scanned')}",
        f"fact_card_count_after_stage5dx={summary.get('fact_card_count_after_stage5dx')}",
        f"source_browser_validation_error_count={summary.get('source_browser_validation_error_count')}",
        f"spurious_root_image_paths_after={summary.get('spurious_root_image_paths_after')}",
        f"spurious_root_document_paths_after={summary.get('spurious_root_document_paths_after')}",
        f"duplicate_present_missing_path_pairs_after={summary.get('duplicate_present_missing_path_pairs_after')}",
        f"historical_source_lock_records_rewritten={summary.get('historical_source_lock_records_rewritten')}",
        f"target_selected={summary.get('pivot_target_selected_now')}",
        f"route_extracted={summary.get('route_extraction_performed_now')}",
        f"execution_performed={summary.get('execution_performed')}",
        f"solve_claim={summary.get('solve_claim')}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


def _build_records() -> dict[str, dict[str, Any]]:
    collection = _load_overlay_collection()
    overlays = collection["overlays"]
    all_overlays = load_enrichment_overlays()
    index = build_source_index()
    entry_by_path = {entry.source_record_path: entry for entry in index.entries}
    browser = source_browser_summary(index)
    path_report = path_canonicalization_report(index)
    overlay_only_count = _overlay_only_count(overlays, entry_by_path)
    selected_fact_cards = {
        path: len(normalize_entry_number_facts(entry_by_path[path], all_overlays))
        for path in SELECTED_SOURCE_RECORD_PATHS
        if path in entry_by_path
    }
    fact_card_count_after = sum(len(normalize_entry_number_facts(entry, all_overlays)) for entry in index.entries)
    base = _stage_base()
    false_flags = _false_flags()
    source_browser_validation = validate_source_index()
    stage5dw_summary = _load(Path("data/project-state/stage5dw-summary.yaml"))

    summary = {
        **base,
        **false_flags,
        "record_type": "stage5dx_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "status": "complete",
        "source_previous_stage": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_title": SOURCE_PREVIOUS_STAGE_TITLE,
        "source_previous_stage_starting_commit": SOURCE_PREVIOUS_STAGE_STARTING_COMMIT,
        "source_previous_stage_final_commit": SOURCE_PREVIOUS_STAGE_FINAL_COMMIT,
        "source_previous_issue": SOURCE_PREVIOUS_ISSUE,
        "source_previous_ci_run": SOURCE_PREVIOUS_CI_RUN,
        "source_previous_ci_status": SOURCE_PREVIOUS_CI_STATUS,
        "stage5dw_preserved": True,
        "stage5dv_path_canonicalization_preserved": True,
        "stage5dv_performance_repair_preserved": True,
        "stage5du_preserved": True,
        "stage5dw_overlay_only_support_preserved": True,
        "number_fact_review_batch_2_performed_now": True,
        "source_lock_entry_batch_review_performed_now": True,
        "review_batch_id": REVIEW_BATCH_ID,
        "review_batch_selection_policy": REVIEW_BATCH_SELECTION_POLICY,
        "review_scope": "selected_20_source_records_only",
        "reviewed_entry_count": EXPECTED_REVIEWED_ENTRY_COUNT,
        "selected_source_record_paths": SELECTED_SOURCE_RECORD_PATHS,
        "number_fact_enrichment_overlays_added_now": True,
        "overlay_collection_path": OVERLAY_COLLECTION_PATH.as_posix(),
        "overlay_count": len(overlays),
        "overlay_only_fact_cards_supported": True,
        "overlay_only_fact_cards_validated": True,
        "overlay_only_cards_required_count": overlay_only_count,
        "source_browser_loadability_validated": True,
        "source_browser_entries_loaded": browser["entries_loaded"],
        "source_browser_records_scanned": browser["records_scanned"],
        "source_browser_validation_error_count": len(source_browser_validation.errors),
        "source_browser_warning_count": browser["warnings"],
        "source_browser_missing_paths_after": browser["missing_paths"],
        "missing_paths_retained_as_warnings": True,
        "fact_card_count_after_stage5dx": fact_card_count_after,
        "selected_batch_fact_card_count": sum(selected_fact_cards.values()),
        "spurious_root_image_paths_after": path_report["spurious_root_image_paths"],
        "spurious_root_document_paths_after": path_report["spurious_root_document_paths"],
        "duplicate_present_missing_path_pairs_after": path_report["duplicate_present_missing_path_pairs"],
        "source_root_relative_resolved_paths": path_report["source_root_relative_resolved_paths"],
        "canonical_lp_page_root_alias_present": path_report["canonical_lp_page_root_alias_present"],
        "stage5du_thread_image_paths_under_third_party": path_report["stage5du_thread_image_paths_under_third_party"],
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": 8,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "old_16_worker_default_reintroduced": False,
        "codex_output_used": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": "assistant_or_operator_review_then_codex_overlay_update",
        "selected_next_stage_authorizes_execution": False,
        "selected_next_stage_authorizes_activation": False,
        "selected_next_stage_authorizes_byte_stream_generation": False,
    }

    records: dict[str, dict[str, Any]] = {
        "summary": summary,
        "next_stage_decision": {
            **base,
            **false_flags,
            "record_type": "stage5dx_next_stage_decision",
            "schema": SCHEMA_PATHS["next_stage_decision"].as_posix(),
            "status": "complete",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": "assistant_or_operator_review_then_codex_overlay_update",
            "selected_next_stage_authorizes_execution": False,
            "selected_next_stage_authorizes_activation": False,
            "selected_next_stage_authorizes_byte_stream_generation": False,
        },
        "stage5dw_preservation": {
            **base,
            "record_type": "stage5dx_stage5dw_preservation",
            "schema": SCHEMA_PATHS["stage5dw_preservation"].as_posix(),
            "stage5dw_preserved": True,
            "stage5dw_status": stage5dw_summary.get("status"),
            "stage5dw_reviewed_entry_count": stage5dw_summary.get("reviewed_entry_count"),
            "stage5dw_overlay_count": stage5dw_summary.get("overlay_count"),
            "stage5dw_overlay_only_fact_cards_supported": stage5dw_summary.get("overlay_only_fact_cards_supported"),
            "stage5dw_overlay_only_fact_cards_validated": stage5dw_summary.get("overlay_only_fact_cards_validated"),
            "stage5dw_source_browser_entries_loaded": stage5dw_summary.get("source_browser_entries_loaded"),
            "stage5dw_source_browser_records_scanned": stage5dw_summary.get("source_browser_records_scanned"),
            "stage5dw_source_browser_validation_error_count": stage5dw_summary.get(
                "source_browser_validation_error_count"
            ),
            "stage5dw_fact_card_count_after_stage5dw": stage5dw_summary.get("fact_card_count_after_stage5dw"),
            "stage5dw_selected_batch_fact_card_count": stage5dw_summary.get("selected_batch_fact_card_count"),
            "stage5dw_historical_source_lock_records_rewritten": stage5dw_summary.get(
                "historical_source_lock_records_rewritten"
            ),
            "stage5dw_target_selected": stage5dw_summary.get("pivot_target_selected_now"),
            "stage5dw_route_extracted": stage5dw_summary.get("route_extraction_performed_now"),
            "stage5dw_byte_streams_generated": stage5dw_summary.get("real_byte_stream_generated"),
            "stage5dw_execution_performed": stage5dw_summary.get("execution_performed"),
            "stage5dw_solve_claim": stage5dw_summary.get("solve_claim"),
        },
        "source_browser_loadability": {
            **base,
            "record_type": "stage5dx_source_browser_loadability_summary",
            "schema": SCHEMA_PATHS["source_browser_loadability"].as_posix(),
            "source_browser_entries_loaded": browser["entries_loaded"],
            "source_browser_records_scanned": browser["records_scanned"],
            "source_browser_validation_error_count": len(source_browser_validation.errors),
            "source_browser_warning_count": browser["warnings"],
            "source_browser_missing_paths_after": browser["missing_paths"],
            "missing_paths_retained_as_warnings": True,
            "fact_card_count_after_stage5dx": fact_card_count_after,
            "spurious_root_image_paths_after": path_report["spurious_root_image_paths"],
            "spurious_root_document_paths_after": path_report["spurious_root_document_paths"],
            "duplicate_present_missing_path_pairs_after": path_report["duplicate_present_missing_path_pairs"],
            "source_root_relative_resolved_paths": path_report["source_root_relative_resolved_paths"],
            "stage5dv_path_canonicalization_preserved": True,
            "stage5dw_overlay_only_support_preserved": True,
        },
        "reviewable_validation_evidence": {
            **base,
            "record_type": "stage5dx_reviewable_validation_evidence",
            "schema": SCHEMA_PATHS["reviewable_validation_evidence"].as_posix(),
            "validators": [
                "validate-stage5dx",
                "validate-stage5dx-review-batch-selection",
                "validate-stage5dx-number-fact-overlays",
                "validate-stage5dx-overlay-only-support",
                "validate-stage5dx-source-browser-loadability",
                "source-browser validate-index",
                "source-browser validate-paths",
                "source-browser performance-smoke",
            ],
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
            "old_16_worker_default_reintroduced": False,
        },
        "reviewability_gap_register": {
            **base,
            "record_type": "stage5dx_reviewability_gap_register",
            "schema": SCHEMA_PATHS["reviewability_gap_register"].as_posix(),
            "remaining_gap": "continue_number_fact_review_batches",
            "next_batch_recommended": "number_fact_review_batch_003",
            "overlay_count_deviation": False,
            "target_priority_decision_created_now": False,
        },
        "scope_control": {
            **base,
            **false_flags,
            "record_type": "stage5dx_scope_control",
            "schema": SCHEMA_PATHS["scope_control"].as_posix(),
            "source_lock_entry_batch_review_performed_now": True,
            "number_fact_review_batch_2_performed_now": True,
            "review_scope": "selected_20_source_records_only",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "old_16_worker_default_reintroduced": False,
            "codex_output_used": False,
        },
        "chatgpt_context_update_summary": {
            **base,
            "record_type": "stage5dx_chatgpt_context_update_summary",
            "schema": SCHEMA_PATHS["chatgpt_context_update_summary"].as_posix(),
            "chatgpt_context_updated": _context_contains_stage5dx(),
            "chatgpt_context_path": CHATGPT_CONTEXT_PATH.as_posix(),
            "raw_source_body_included": False,
            "long_prompt_text_included": False,
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
            "number_fact_backfill_performed_now": False,
            "review_scope": "selected_20_source_records_only",
            "review_result_status": "overlay_enrichment_complete",
            "selected_source_record_paths": SELECTED_SOURCE_RECORD_PATHS,
            "overlay_file": OVERLAY_COLLECTION_PATH.as_posix(),
            "facts_added_directly_to_source_records": False,
            "facts_added_as_overlays": True,
        },
        "review_batch_entry_status": {
            **base,
            "record_type": "source_browser_number_fact_review_batch_entry_status",
            "schema": SCHEMA_PATHS["review_batch_entry_status"].as_posix(),
            "review_batch_id": REVIEW_BATCH_ID,
            "entry_count": EXPECTED_REVIEWED_ENTRY_COUNT,
            "entries": [
                {
                    "source_record_path": path,
                    "review_status": "reviewed_overlay_added",
                    "entry_historical_source_lock_rewritten": False,
                    "usable_for_decision_now": False,
                    "not_allowed_as": OVERLAY_REQUIRED_NOT_ALLOWED,
                    "overlay_count": sum(1 for overlay in overlays if overlay.get("source_record_path") == path),
                    "fact_card_count_after_overlay": selected_fact_cards.get(path, 0),
                }
                for path in SELECTED_SOURCE_RECORD_PATHS
            ],
        },
    }
    records.update(_source_harvester_records(base, false_flags))
    records.update(_token_records(base, false_flags))
    return records


def _source_harvester_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "codex_handoff_policy": {
            **base,
            "record_type": "stage5dx_codex_handoff_policy",
            "schema": SCHEMA_PATHS["codex_handoff_policy"].as_posix(),
            "canonical_codex_handoff_root": "codex-output",
            "deprecated_codex_output_root_used": False,
            "codex_output_used": False,
            "completion_summary_path": "codex-output/stage5dx-codex-completion.md",
            "completion_summary_committed": False,
        },
        "credential_redaction_policy_preservation": {
            **base,
            "record_type": "stage5dx_credential_redaction_policy_preservation",
            "schema": SCHEMA_PATHS["credential_redaction_policy_preservation"].as_posix(),
            "credential_like_remote_count": 0,
            "credential_redaction_policy_preserved": True,
            "raw_source_body_included": False,
            "secret_material_committed": False,
        },
        "raw_source_noncommit_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dx_raw_source_noncommit_proof",
            "schema": SCHEMA_PATHS["raw_source_noncommit_proof"].as_posix(),
            "raw_source_body_included": False,
            "raw_source_files_committed": False,
            "raw_third_party_files_committed": False,
            "generated_outputs_committed": False,
        },
    }


def _token_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "stage5dg_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5dx_stage5dg_preservation",
            "stage5dg_operator_approval_record_preserved": True,
            "operator_approval_component_satisfied_preserved": True,
            "deep_research_acceptance_created_now": False,
            "combined_approval_gate_satisfied_now": False,
        },
        "stage5bd_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5dx_stage5bd_preservation",
            "stage5bd_run_plan_id_count": 10,
            "stage5bd_run_plan_ids_preserved": True,
        },
        "active_lineage_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5dx_active_lineage_preservation",
            "active_lineage_record_count": 8,
            "active_lineage_preserved": True,
        },
        "no_active_ingestion_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dx_no_active_ingestion_proof",
            "gate_status": "closed",
            "active_ingestion_performed": False,
        },
        "no_byte_stream_transition_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dx_no_byte_stream_transition_proof",
            "gate_status": "closed",
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "byte_stream_generation_authorized_now": False,
        },
        "no_token_block_execution_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dx_no_token_block_execution_proof",
            "schema": SCHEMA_PATHS["no_token_block_execution_proof"].as_posix(),
            "gate_status": "closed",
            "execution_authorized_now": False,
            "execution_performed": False,
            "token_block_experiment_executed": False,
        },
    }


def _write_records(records: dict[str, dict[str, Any]]) -> None:
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        if key == "summary":
            schema = _object_schema(["record_type", "stage_id", "status", "review_batch_id"])
        elif key == "review_batch_result":
            schema = _object_schema(["record_type", "stage_id", "review_batch_id", "selected_source_record_paths"])
        elif key == "review_batch_entry_status":
            schema = _object_schema(["record_type", "stage_id", "review_batch_id", "entries"])
        else:
            schema = _object_schema(["record_type", "stage_id"])
        write_json(path, schema)


def _write_overlay_collection() -> None:
    write_yaml(OVERLAY_COLLECTION_PATH, _overlay_collection_payload())


def _overlay_collection_payload() -> dict[str, Any]:
    return {
        **_stage_base(),
        "record_type": "source_browser_number_fact_enrichment_overlay_collection",
        "schema": OVERLAY_SCHEMA_PATH.as_posix(),
        "review_batch_id": REVIEW_BATCH_ID,
        "review_batch_selection_policy": REVIEW_BATCH_SELECTION_POLICY,
        "reviewed_entry_count": EXPECTED_REVIEWED_ENTRY_COUNT,
        "overlay_count": EXPECTED_OVERLAY_COUNT,
        "overlay_only_fact_cards_supported_required": True,
        "review_state": "overlay_enriched_fact",
        "historical_source_lock_records_rewritten": False,
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
            "solve_claim": {"const": False},
            "execution_performed": {"const": False},
            "historical_source_lock_records_rewritten": {"const": False},
            "raw_source_files_committed": {"const": False},
            "raw_third_party_files_committed": {"const": False},
            "generated_outputs_committed": {"const": False},
            "target_priority_decision_created_now": {"const": False},
            "pivot_target_selected_now": {"const": False},
            "route_extraction_performed_now": {"const": False},
            "real_byte_stream_generated": {"const": False},
        },
    }


def _validate_required_paths() -> list[str]:
    paths = list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values()) + [OVERLAY_COLLECTION_PATH, OVERLAY_SCHEMA_PATH]
    return [f"required Stage 5DX path missing: {path.as_posix()}" for path in paths if not path.exists()]


def _validate_schemas() -> list[str]:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        schema_key = SCHEMA_BY_DATA_KEY.get(key)
        schema_path = SCHEMA_PATHS.get(schema_key or "") or SCHEMA_PATHS["generic_token_block"]
        if not path.exists() or not schema_path.exists():
            continue
        payload = _load(path)
        schema = _load(schema_path)
        for error in sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda item: item.path):
            errors.append(f"{path.as_posix()}: {error.message}")
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


def _required_false_errors(payload: dict[str, Any], label: str) -> list[str]:
    errors = []
    for key in FALSE_FLAGS:
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


def _context_contains_stage5dx() -> bool:
    if not CHATGPT_CONTEXT_PATH.exists():
        return False
    return "## Stage 5DX - Number-fact review batch 002" in CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8")


def _update_chatgpt_context() -> None:
    marker = "## Stage 5DX - Number-fact review batch 002"
    text = CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8") if CHATGPT_CONTEXT_PATH.exists() else ""
    if marker in text:
        return
    addition = f"""

{marker}

- Stage 5DX enriched 20 selected visual/red-heading/transform source-lock entries using NumberFactCard overlays only.
- Stage 5DX did not rewrite historical source locks, select a target, run routes, generate bytes, execute code, run OCR/image forensics, or make solve claims.
- RedRunes secondary facts preserved: ENLIGHTENED/MUMON'S COMMENT 155/551, red prime-sum 742, key/speech-tongue 682, first-two-rune sum 31.
- BigGaps/StarArtifacts facts preserved: red-subset sum 229, gap metrics 73/109/129 with 109=prime(29), tree offsets 641/709 with prime-index gap 11, stardust phrase 2540=254*10, Mayfly 72/600 twin-prime gaps, ICC boundary pages 00-16 vs 17-74 with 2576-byte profile claim.
- Red-heading/Mobius facts preserved: Page15 instruction phrase primes, DIVINITY WITHIN 491/563/1229 crosslink, YGGDRASIL spelling 491/564 warning, A POSTLUDE 1/8 structure, Mobius/totient zero-class 14-token partition, page0 DIVINITY WITHIN/A CROSSROADS 491.
- PDD/Disk/Ouroboros facts preserved: 56311 net +25 over modulus 153, gcd(25,153)=1, 4-phase period 612; OUROBOROS 167 minus 153 gives offset 14; Disk 56311 from center 41/WYNN reaches word52/WAY.
- Stage 5DY should continue number-fact review batch 003 unless a blocking Source Browser issue appears.
"""
    CHATGPT_CONTEXT_PATH.write_text(text.rstrip() + addition + "\n", encoding="utf-8")


def _update_stage_summary_records(summary: dict[str, Any]) -> None:
    path = Path("data/research/stage-summary-records-v0.yaml")
    payload = read_yaml(path)
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
                "Added review-only NumberFactCard overlays for the second 20-entry source-lock "
                "number-fact review batch."
            ),
            "key_outputs": [
                "Stage 5DX visual/red-heading/transform overlay collection with 23 review-only facts.",
                "Stage 5DX records, validators, docs, tests, and handoff summary.",
                "Stage 5DY selected as the next number-fact review batch.",
            ],
            "result_status": "reviewability_overlays_only",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                f"Reviewed entries={summary.get('reviewed_entry_count')}, overlays={summary.get('overlay_count')}, "
                f"fact_cards_after={summary.get('fact_card_count_after_stage5dx')}. Historical source locks were not rewritten."
            ),
        }
    )
    payload["records"] = records
    write_yaml(path, payload)
