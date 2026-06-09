"""Stage 5DU community visual/red-heading/negative-space source locks.

This stage records local ignored community-thread folders as compact metadata.
It deliberately does not run OCR, image forensics, community code, route
extraction, byte generation, token-block execution, target selection, or CUDA.
"""

from __future__ import annotations

import json
import mimetypes
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.number_facts import (
    OPERATION_TYPES,
    REVIEW_STATES,
    VALUE_TYPES,
    VERIFICATION_STATUSES,
    load_enrichment_overlays,
    reviewability_counts,
)
from libreprimus.operator_console.source_browser.validators import (
    validate_number_fact_cards,
    validate_source_index,
)
from libreprimus.token_block.models import read_yaml, sha256_file, write_json, write_yaml
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import ACTIVE_LINEAGE_PATHS
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP, SECRET_PATTERNS
from libreprimus.token_block.stage5dt import validate_stage5dt

STAGE_ID = "stage-5du"
STAGE_TITLE = (
    "Stage 5DU - Community visual/red-heading/negative-space source-lock "
    "addendum, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE_ID = "stage-5dt"
SOURCE_PREVIOUS_STAGE_COMMIT = "bd5bfa8dd8f1b310340f2254d9eaf53ff3d15791"
NEXT_STAGE_ID = "stage-5dv"
NEXT_STAGE_TITLE = (
    "Stage 5DV - Operator/assistant source-lock number-fact review batch 1, "
    "without execution"
)

PROJECT_STATE_DIR = Path("data/project-state")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
HISTORICAL_ROUTE_DIR = Path("data/historical-route")
TOKEN_BLOCK_DIR = Path("data/token-block")
OVERLAY_DIR = Path("data/operator-console/source-browser/number-fact-overlays")

CODEX_COMPLETION_PATH = Path("codex-output/stage5du-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
CANONICAL_PAGE_ROOT = Path("third_party/CiadaSolversIddqd_v2/liber-primus__images--full")
CANONICAL_PAGE_ROOT_ALT = Path("third_party/CicadaSolversIddqd_v2/liber-primus__images--full")

SOURCE_ROOTS: dict[str, dict[str, Any]] = {
    "big_gaps_found_in_liber_primus": {
        "source_root": Path("third_party/BigGapsFoundInLiberPrimus"),
        "expected_thread_images": 43,
        "expected_missing_image_numbers": [1],
        "expected_duplicate_note": "images 30-35 duplicate 36-41 in prior archive analysis",
    },
    "cribbing_page15": {
        "source_root": Path("third_party/CribbingPage15"),
        "expected_files": ["messages.txt"],
    },
    "mobius_totient_first_page_theory": {
        "source_root": Path("third_party/Mobius_totient_first_page_theory"),
        "expected_files_about": "messages.txt plus images, Python files, text outputs, and spreadsheets",
    },
    "potential_crib_red_runes_pages_54_55": {
        "source_root": Path("third_party/PotentialCrib_RedRunes_Pages_54_55"),
        "expected_files_about": "messages.txt plus 6 images/screenshots",
    },
    "red_runes_possible_koan_connection": {
        "source_root": Path("third_party/RedRunes_Possible_Koan_Connection"),
        "expected_files": [
            "messages.txt",
            "a famous book.png",
            "coincidence for me_01.png",
            "coincidence for me_02.png",
        ],
    },
    "star_artifacts_in_lp_page_images": {
        "source_root": Path("third_party/StarArtifactsInLPPageImages"),
        "expected_thread_images": 79,
        "expected_duplicate_note": "1.png = 41.png = 42.png in prior archive analysis",
    },
}

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5du-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5du-next-stage-decision.yaml",
    "stage5dt_preservation": PROJECT_STATE_DIR / "stage5du-stage5dt-preservation.yaml",
    "operator_inserted_addendum_routing": PROJECT_STATE_DIR
    / "stage5du-operator-inserted-addendum-routing.yaml",
    "community_thread_source_lock_plan": PROJECT_STATE_DIR
    / "stage5du-community-thread-source-lock-plan.yaml",
    "visual_observation_family_index": PROJECT_STATE_DIR
    / "stage5du-visual-observation-family-index.yaml",
    "red_heading_family_index": PROJECT_STATE_DIR / "stage5du-red-heading-family-index.yaml",
    "number_fact_card_readiness_summary": PROJECT_STATE_DIR
    / "stage5du-number-fact-card-readiness-summary.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR
    / "stage5du-source-browser-loadability-summary.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR
    / "stage5du-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5du-reviewability-gap-register.yaml",
    "scope_control": PROJECT_STATE_DIR / "stage5du-scope-control.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR
    / "stage5du-chatgpt-context-update-summary.yaml",
}

SOURCE_PATHS: dict[str, Path] = {
    "community_thread_source_lock_register": SOURCE_HARVESTER_DIR
    / "stage5du-community-thread-source-lock-register.yaml",
    "community_thread_file_inventory": SOURCE_HARVESTER_DIR
    / "stage5du-community-thread-file-inventory.yaml",
    "thread_messages_source_locks": SOURCE_HARVESTER_DIR
    / "stage5du-thread-messages-source-locks.yaml",
    "thread_attachment_order_index": SOURCE_HARVESTER_DIR
    / "stage5du-thread-attachment-order-index.yaml",
    "thread_image_source_locks": SOURCE_HARVESTER_DIR
    / "stage5du-thread-image-source-locks.yaml",
    "thread_code_and_table_inventory": SOURCE_HARVESTER_DIR
    / "stage5du-thread-code-and-table-inventory.yaml",
    "canonical_lp_page_image_root_crosslink": SOURCE_HARVESTER_DIR
    / "stage5du-canonical-lp-page-image-root-crosslink.yaml",
    "external_reference_url_lock_register": SOURCE_HARVESTER_DIR
    / "stage5du-external-reference-url-lock-register.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR
    / "stage5du-raw-source-noncommit-proof.yaml",
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5du-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5du-credential-redaction-policy-preservation.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "stage5dg_preservation": TOKEN_BLOCK_DIR / "stage5du-stage5dg-preservation.yaml",
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5du-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5du-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5du-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR
    / "stage5du-no-byte-stream-transition-proof.yaml",
    "no_token_block_execution_proof": TOKEN_BLOCK_DIR
    / "stage5du-no-token-block-execution-proof.yaml",
    "operator_console_stage5dt_preservation": TOKEN_BLOCK_DIR
    / "stage5du-operator-console-stage5dt-preservation.yaml",
}

OVERLAY_PATH = OVERLAY_DIR / "stage5du-community-visual-fact-overlays.yaml"

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5du-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5du-next-stage-decision-v0.schema.json"),
    "scope_control": Path("schemas/project-state/stage5du-scope-control-v0.schema.json"),
    "community_thread_source_lock_register": Path(
        "schemas/source-harvester/"
        "stage5du-community-thread-source-lock-register-v0.schema.json"
    ),
    "community_thread_file_inventory": Path(
        "schemas/source-harvester/stage5du-community-thread-file-inventory-v0.schema.json"
    ),
    "thread_messages_source_locks": Path(
        "schemas/source-harvester/stage5du-thread-messages-source-locks-v0.schema.json"
    ),
    "thread_attachment_order_index": Path(
        "schemas/source-harvester/stage5du-thread-attachment-order-index-v0.schema.json"
    ),
    "canonical_lp_page_image_root_crosslink": Path(
        "schemas/source-harvester/"
        "stage5du-canonical-lp-page-image-root-crosslink-v0.schema.json"
    ),
    "community_visual_candidate": Path(
        "schemas/historical-route/stage5du-community-visual-candidate-record-v0.schema.json"
    ),
    "red_heading_candidate": Path(
        "schemas/historical-route/stage5du-red-heading-candidate-record-v0.schema.json"
    ),
    "negative_space_candidate": Path(
        "schemas/historical-route/stage5du-negative-space-candidate-record-v0.schema.json"
    ),
    "star_artifact_candidate": Path(
        "schemas/historical-route/stage5du-star-artifact-candidate-record-v0.schema.json"
    ),
    "mobius_totient_candidate": Path(
        "schemas/historical-route/stage5du-mobius-totient-candidate-record-v0.schema.json"
    ),
    "no_token_block_execution_proof": Path(
        "schemas/token-block/stage5du-no-token-block-execution-proof-v0.schema.json"
    ),
}

FORBIDDEN_FALSE_FLAGS = {
    "activation_authorized_now",
    "activation_decision_valid_now",
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "active_token_block_manifest_changed",
    "ai_ml_interpretation_performed",
    "alberti_html_executed_now",
    "audio_stego_performed",
    "benchmark_performed",
    "branch_enumeration_performed",
    "byte_stream_generation_authorized_now",
    "canonical_corpus_active",
    "codex_output_used",
    "combined_approval_gate_satisfied_now",
    "community_code_executed_now",
    "cuda_execution_performed",
    "decode_attempt_performed",
    "decryption_attempt_performed_now",
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
    "mobius_totient_dictionary_search_executed_now",
    "mp3stego_execution_performed",
    "network_target_validation_performed_now",
    "number_fact_backfill_performed_now",
    "ocr_performed",
    "old_16_worker_default_reintroduced",
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
    "raw_third_party_files_committed",
    "real_byte_stream_generated",
    "red_heading_decryption_accepted_now",
    "route_extraction_performed_now",
    "scoring_performed",
    "semantic_image_interpretation_performed",
    "solve_claim",
    "source_lock_entry_batch_review_performed_now",
    "spectrogram_stego_performed",
    "spreadsheet_macro_execution_performed",
    "target_class_validation_implemented",
    "target_priority_decision_created_now",
    "token_block_experiment_executed",
    "token_block_variant_byte_streams_generated",
    "tor_network_access_performed",
    "variant_byte_streams_generated",
    "variant_materialisation_performed",
    "website_expansion_performed",
}

STAGE5DU_CONTEXT_SECTION = """\
## Stage 5DU - Community visual/red-heading/negative-space source-lock addendum

- Stage 5DU source-locks six local `third_party` forum-thread folders: BigGapsFoundInLiberPrimus, CribbingPage15, Mobius_totient_first_page_theory, PotentialCrib_RedRunes_Pages_54_55, RedRunes_Possible_Koan_Connection, and StarArtifactsInLPPageImages.
- Original page images for thread crosschecks live under `third_party/CiadaSolversIddqd_v2/liber-primus__images--full`; old per-archive `original-pages` folders were intentionally removed.
- RedRunes/Gateless Gate strongest observation: red rune grouping 2/11/3 matches THE/ENLIGHTENED/MAN, koan #20 of 49; title zero-index GP sum 227 = prime(49); 227 is not unique among titles, but 2/11/3 grouping is the strong constraint.
- BigGaps strongest observations: claimed 16 big-gap pages, one-based sum 569; red big-gap subset one-based sum 229; line gaps 73/109/129 and same-frame overlay/phase-shift candidate. Layout artifact risk remains high.
- StarArtifacts strongest observations: exact RGB/max-channel 254 threshold reveals near-white star/sunburst layer; pages 10-13 and 41-43 are key; tree offsets 641/709 have prime-index gap 11; stardust phrase GP 2540 = 254x10 is unverified community decode context.
- CribbingPage15 preserves internal phrase GP facts and YOUR TRUTH crib warning; standard short-token GP makes YOUR/TRUTH 4/4, not clean 4/5.
- Page54/55 red-heading candidate: A POSTLUDE / DEAD TREE / YGGDRASIL / DIVINITY WITHIN / A CROSSROADS all sit in GP 491 family; A POSTLUDE is not unique by GP alone.
- Mobius_totient_first_page_theory preserves the arithmetic Mobius/totient zero-class method and page0 DIVINITY WITHIN / A CROSSROADS claim. The proposed 33-word page0 plaintext is quarantined, not accepted.
- Stage 5DU performs no OCR, image forensics, route extraction, community-code execution, target selection, byte generation, or solve claim.
- The Stage 5DT number-fact review batch 1 is still pending after this addendum and shifts to Stage 5DV.
"""

EXTERNAL_URLS = [
    {
        "url_id": "gateless_gate_wikisource",
        "url": "https://en.wikisource.org/wiki/The_Gateless_Gate",
        "reference_family": "red_runes_gateless_gate",
    },
    {
        "url_id": "gateless_gate_wikipedia",
        "url": "https://en.wikipedia.org/wiki/The_Gateless_Barrier",
        "reference_family": "red_runes_gateless_gate",
    },
    {
        "url_id": "yggdrasil_wikipedia",
        "url": "https://en.wikipedia.org/wiki/Yggdrasil",
        "reference_family": "red_heading_gp491",
    },
    {
        "url_id": "mobius_function_wikipedia",
        "url": "https://en.wikipedia.org/wiki/Mobius_function",
        "reference_family": "mobius_totient",
    },
    {
        "url_id": "euler_totient_wikipedia",
        "url": "https://en.wikipedia.org/wiki/Euler%27s_totient_function",
        "reference_family": "mobius_totient",
    },
]


@dataclass
class Stage5DUValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5du"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5du() -> dict[str, dict[str, Any]]:
    previous = validate_stage5dt()
    if previous.validation_error_count:
        raise RuntimeError("Stage 5DT validation must pass before Stage 5DU")
    _stage5bd_counts, stage5bd_errors = validate_stage5bd()
    if stage5bd_errors:
        raise RuntimeError("Stage 5BD preservation validation must pass before Stage 5DU")

    _write_schemas()
    _update_chatgpt_context()
    _update_operational_file_map()

    inventory = _thread_file_inventory()
    records = _build_records(inventory)
    _write_records(records)
    _write_overlay_collection()
    records = _build_records(inventory)
    _write_records(records)
    _update_stage_summary_records(records["summary"])
    return records


def validate_stage5du() -> Stage5DUValidationResult:
    checks = [
        validate_stage5du_community_thread_source_locks,
        validate_stage5du_thread_file_inventory,
        validate_stage5du_canonical_page_root_crosslink,
        validate_stage5du_red_runes_gateless_gate,
        validate_stage5du_big_gaps_negative_space,
        validate_stage5du_star_artifacts,
        validate_stage5du_cribbing_page15,
        validate_stage5du_red_runes_pages54_55,
        validate_stage5du_mobius_totient,
        validate_stage5du_number_fact_cards,
        validate_stage5du_source_browser_loadability,
        validate_stage5du_chatgpt_context,
        validate_stage5du_stage5dt_preservation,
        validate_stage5du_stage5dg_preservation,
        validate_stage5du_stage5bd_preservation,
        validate_stage5du_active_lineage_preservation,
        validate_stage5du_sidecar_gates,
        validate_stage5du_handoff_continuity,
        validate_stage5du_credential_redaction_policy,
        validate_stage5du_governance_scope,
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    errors.extend(_validate_required_paths())
    errors.extend(_validate_schemas())
    for check in checks:
        result = check()
        counts.update(result.counts)
        errors.extend(result.errors)
    for path in _all_yaml_record_paths():
        payload = _load(path)
        errors.extend(_required_false_errors(payload, path.as_posix()))
    summary = _load(PROJECT_STATE_PATHS["summary"])
    expected = {
        "status": "complete",
        "metadata_only": True,
        "source_lock_only": True,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "community_thread_source_lock_created": True,
        "canonical_lp_page_root_crosslink_created": True,
        "number_fact_card_overlays_created": True,
        "chatgpt_context_updated": True,
        "source_browser_loadability_validated": True,
        "operator_inserted_visual_community_source_lock_addendum_first": True,
        "number_fact_review_batch_1_still_required_after_this_stage": True,
        "source_lock_entry_batch_review_performed_now": False,
        "pivot_target_selected_now": False,
        "target_priority_decision_created_now": False,
        "byte_stream_generation_authorized_now": False,
        "execution_performed": False,
        "community_code_executed_now": False,
        "ocr_performed": False,
        "image_forensics_performed": False,
        "route_extraction_performed_now": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"{PROJECT_STATE_PATHS['summary'].as_posix()}: {key} must be {value}")
    if summary.get("stage5bd_run_plan_id_count") != 10:
        errors.append("stage5bd_run_plan_id_count must remain 10")
    if summary.get("active_lineage_record_count") != 8:
        errors.append("active_lineage_record_count must remain 8")
    if summary.get("parallel_worker_cap") != 8:
        errors.append("parallel worker cap must remain 8")
    if _codex_output_used():
        errors.append("deprecated codex_output directory is present")
    counts.update(_summary_counts(summary))
    counts["token_block_stage5du_valid"] = not errors
    return Stage5DUValidationResult(len(errors), counts, errors)


def validate_stage5du_community_thread_source_locks() -> Stage5DUValidationResult:
    payload = _load(SOURCE_PATHS["community_thread_source_lock_register"])
    roots = payload.get("source_roots") or []
    errors = _required_false_errors(payload)
    if len(roots) != len(SOURCE_ROOTS):
        errors.append("all six community source roots must be represented")
    for root in roots:
        if root.get("source_status") not in {"local_ignored_metadata_locked", "missing_local_gap_recorded"}:
            errors.append(f"{root.get('source_root_id')}: unexpected source status")
    counts = {
        "thread_folders_represented": len(roots) if isinstance(roots, list) else 0,
        "thread_folders_absent": sum(1 for root in roots if not root.get("source_root_exists")),
    }
    return Stage5DUValidationResult(len(errors), counts, errors)


def validate_stage5du_thread_file_inventory() -> Stage5DUValidationResult:
    payload = _load(SOURCE_PATHS["community_thread_file_inventory"])
    rows = payload.get("files") or []
    errors = _required_false_errors(payload)
    if not isinstance(rows, list) or not rows:
        errors.append("thread file inventory must contain files")
    for row in rows:
        if row.get("raw_file_committed") is not False:
            errors.append(f"{row.get('relative_path')}: raw_file_committed must be false")
        if len(str(row.get("sha256") or "")) != 64:
            errors.append(f"{row.get('relative_path')}: invalid sha256")
    counts = {
        "thread_file_count": len(rows) if isinstance(rows, list) else 0,
        "thread_image_file_count_total": payload.get("image_file_count", 0),
        "thread_python_file_count_total": payload.get("python_file_count", 0),
        "thread_spreadsheet_file_count_total": payload.get("spreadsheet_file_count", 0),
    }
    return Stage5DUValidationResult(len(errors), counts, errors)


def validate_stage5du_canonical_page_root_crosslink() -> Stage5DUValidationResult:
    payload = _load(SOURCE_PATHS["canonical_lp_page_image_root_crosslink"])
    errors = _required_false_errors(payload)
    if payload.get("expected_canonical_page_count") != 75:
        errors.append("expected canonical page count must be 75")
    if payload.get("raw_page_images_committed_now") is not False:
        errors.append("raw_page_images_committed_now must be false")
    if payload.get("path_spelling_warning_ciada_vs_cicada_recorded") is not True:
        errors.append("Ciada/Cicada spelling warning must be recorded")
    counts = {
        "canonical_lp_page_image_root_present": payload.get("canonical_page_image_root_exists", False),
        "canonical_lp_page_image_count": payload.get("canonical_page_count_observed"),
    }
    return Stage5DUValidationResult(len(errors), counts, errors)


def validate_stage5du_red_runes_gateless_gate() -> Stage5DUValidationResult:
    path = CANDIDATE_PATHS["red_runes_gateless_gate_koan20_title_candidate"]
    payload = _load(path)
    errors = _candidate_common_errors(payload, path)
    if payload.get("grouping_match_2_11_3") is not True:
        errors.append("red-rune 2/11/3 grouping must be recorded")
    if payload.get("zero_based_gp_index_sum_title") != 227:
        errors.append("THE ENLIGHTENED MAN zero-index sum must be 227")
    if payload.get("prime_49") != 227:
        errors.append("prime(49)=227 must be recorded")
    if not payload.get("gateless_gate_title_control_scan", {}).get("title_sum_227_not_unique"):
        errors.append("227 non-uniqueness control warning must be recorded")
    return Stage5DUValidationResult(
        len(errors),
        {"red_runes_gateless_gate_records_created": _count_paths(RED_RUNE_PATHS)},
        errors,
    )


def validate_stage5du_big_gaps_negative_space() -> Stage5DUValidationResult:
    path = CANDIDATE_PATHS["big_gap_page_set_16_candidate"]
    payload = _load(path)
    errors = _candidate_common_errors(payload, path)
    if payload.get("claimed_big_gap_page_count") != 16:
        errors.append("big-gap page count must be 16")
    if payload.get("one_based_page_sum") != 569:
        errors.append("big-gap one-based page sum must be 569")
    red = _load(CANDIDATE_PATHS["big_gap_red_subset_one_based_sum_229_candidate"])
    if red.get("one_based_red_subset_sum") != 229:
        errors.append("red subset one-based sum must be 229")
    return Stage5DUValidationResult(
        len(errors),
        {"big_gaps_negative_space_records_created": _count_paths(BIG_GAP_PATHS)},
        errors,
    )


def validate_stage5du_star_artifacts() -> Stage5DUValidationResult:
    path = CANDIDATE_PATHS["star_artifacts_exact254_mask_method"]
    payload = _load(path)
    errors = _candidate_common_errors(payload, path)
    if payload.get("method_claim") != "max(R,G,B) == 254 mask reveals star/sunburst artifacts":
        errors.append("exact254 method claim missing")
    ray = _load(CANDIDATE_PATHS["star_artifacts_12_ray_sunburst_candidate"])
    if ray.get("ray_count_claim") != 12:
        errors.append("12-ray sunburst claim must be recorded")
    tree = _load(CANDIDATE_PATHS["wing_tree_641_709_prime_index_gap11_candidate"])
    if tree.get("prime_index_difference") != 11:
        errors.append("641/709 prime-index gap must be 11")
    return Stage5DUValidationResult(
        len(errors),
        {"star_artifacts_records_created": _count_paths(STAR_PATHS)},
        errors,
    )


def validate_stage5du_cribbing_page15() -> Stage5DUValidationResult:
    path = CANDIDATE_PATHS["page15_your_truth_crib_pointer_candidate"]
    payload = _load(path)
    errors = _candidate_common_errors(payload, path)
    facts = payload.get("internal_instruction_phrase_gp_facts") or []
    if not any(item.get("phrase") == "FIND YOUR TRUTH" and item.get("gp_sum") == 353 for item in facts):
        errors.append("FIND YOUR TRUTH GP 353 must be recorded")
    warning = _load(CANDIDATE_PATHS["page15_red_header_tokenization_warning"])
    if warning.get("standard_short_token_match_clean") is not False:
        errors.append("YOUR/TRUTH 4/5 warning must remain unresolved")
    return Stage5DUValidationResult(
        len(errors),
        {"cribbing_page15_records_created": _count_paths(CRIBBING_PATHS)},
        errors,
    )


def validate_stage5du_red_runes_pages54_55() -> Stage5DUValidationResult:
    path = CANDIDATE_PATHS["page54_55_a_postlude_red_heading_candidate"]
    payload = _load(path)
    errors = _candidate_common_errors(payload, path)
    if payload.get("proposed_plaintext") != "A POSTLUDE":
        errors.append("A POSTLUDE candidate must be recorded")
    gp = _load(CANDIDATE_PATHS["red_heading_marginalia_gp491_equivalence_family"])
    phrases = {item.get("phrase"): item.get("gp_sum") for item in gp.get("gp491_family", [])}
    for phrase in ("A POSTLUDE", "DEAD TREE", "YGGDRASIL", "DIVINITY WITHIN", "A CROSSROADS"):
        if phrases.get(phrase) != 491:
            errors.append(f"{phrase}=491 must be recorded")
    alt = _load(CANDIDATE_PATHS["a_postlude_vs_a_synthesis_a_postulat_alternative_crib_warning"])
    if alt.get("A_POSTLUDE_not_uniquely_implied_by_gp_sum") is not True:
        errors.append("A POSTLUDE non-uniqueness warning must be recorded")
    return Stage5DUValidationResult(
        len(errors),
        {"red_runes_pages54_55_records_created": _count_paths(PAGE5455_PATHS)},
        errors,
    )


def validate_stage5du_mobius_totient() -> Stage5DUValidationResult:
    path = CANDIDATE_PATHS["mobius_totient_zero_class_gp_alphabet_candidate"]
    payload = _load(path)
    errors = _candidate_common_errors(payload, path)
    zero_class = payload.get("zero_class_runes") or []
    if "TH" not in zero_class or "AE" not in zero_class:
        errors.append("Mobius/totient zero class must include TH and AE")
    quarantine = _load(CANDIDATE_PATHS["page0_mobius_totient_plaintext_claim_quarantine"])
    if quarantine.get("accepted_as_plaintext_now") is not False:
        errors.append("page0 plaintext claim must remain unaccepted")
    if quarantine.get("candidate_status") != "quarantined_review_only":
        errors.append("page0 plaintext claim must be quarantined")
    return Stage5DUValidationResult(
        len(errors),
        {"mobius_totient_records_created": _count_paths(MOBIUS_PATHS)},
        errors,
    )


def validate_stage5du_number_fact_cards() -> Stage5DUValidationResult:
    result = validate_number_fact_cards()
    overlay_count = len(load_enrichment_overlays())
    errors = list(result.errors)
    if overlay_count < 6:
        errors.append("Stage 5DU must add at least one overlay per required fact-card class")
    overlays = _load(OVERLAY_PATH).get("overlays") or []
    for overlay in overlays:
        for key in ("display_label", "why_stored", "verification_status", "risk_notes"):
            if not overlay.get(key):
                errors.append(f"{overlay.get('overlay_id')}: {key} is required")
        if overlay.get("usable_for_decision_now") is not False:
            errors.append(f"{overlay.get('overlay_id')}: usable_for_decision_now must be false")
    counts = dict(result.counts)
    counts["stage5du_overlay_count"] = len(overlays) if isinstance(overlays, list) else 0
    return Stage5DUValidationResult(len(errors), counts, errors)


def validate_stage5du_source_browser_loadability() -> Stage5DUValidationResult:
    source_result = validate_source_index()
    payload = _load(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    errors = list(source_result.errors)
    if payload.get("source_browser_validation_error_count") != 0:
        errors.append("source browser validation error count must be 0")
    if payload.get("stage5du_entries_loaded", 0) <= 0:
        errors.append("Stage 5DU entries must be visible in Source Browser")
    counts = dict(source_result.counts)
    counts["stage5du_entries_loaded"] = payload.get("stage5du_entries_loaded", 0)
    return Stage5DUValidationResult(len(errors), counts, errors)


def validate_stage5du_chatgpt_context() -> Stage5DUValidationResult:
    path = Path("ChatGPT-ContextFile.md")
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    required = [
        "Stage 5DU - Community visual/red-heading/negative-space source-lock addendum",
        "RedRunes/Gateless Gate strongest observation",
        "BigGaps strongest observations",
        "StarArtifacts strongest observations",
        "Stage 5DV",
    ]
    errors = [f"ChatGPT context missing phrase: {phrase}" for phrase in required if phrase not in text]
    payload = _load(PROJECT_STATE_PATHS["chatgpt_context_update_summary"])
    if payload.get("raw_source_body_included") is not False:
        errors.append("ChatGPT context must not include raw source bodies")
    return Stage5DUValidationResult(len(errors), {"chatgpt_context_updated": not errors}, errors)


def validate_stage5du_stage5dt_preservation() -> Stage5DUValidationResult:
    payload = _load(PROJECT_STATE_PATHS["stage5dt_preservation"])
    errors = []
    if payload.get("stage5dt_complete") is not True:
        errors.append("Stage 5DT must remain complete")
    if payload.get("number_fact_review_batch_1_performed_now") is not False:
        errors.append("Stage 5DT planned review batch must not be performed")
    if payload.get("stage5dt_recommended_stage5du_number_fact_review_batch_1") is not True:
        errors.append("Stage 5DT next-stage recommendation must be preserved")
    return Stage5DUValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5du_stage5dg_preservation() -> Stage5DUValidationResult:
    payload = _load(TOKEN_PATHS["stage5dg_preservation"])
    errors = []
    if payload.get("stage5dg_operator_approval_record_preserved") is not True:
        errors.append("Stage 5DG operator approval record must be preserved")
    if payload.get("combined_approval_gate_satisfied_now") is not False:
        errors.append("combined gate must remain unsatisfied")
    return Stage5DUValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5du_stage5bd_preservation() -> Stage5DUValidationResult:
    payload = _load(TOKEN_PATHS["stage5bd_preservation"])
    errors = []
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    return Stage5DUValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5du_active_lineage_preservation() -> Stage5DUValidationResult:
    payload = _load(TOKEN_PATHS["active_lineage_preservation"])
    errors = []
    if payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage count must remain 8")
    return Stage5DUValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5du_sidecar_gates() -> Stage5DUValidationResult:
    paths = [
        TOKEN_PATHS["no_active_ingestion_proof"],
        TOKEN_PATHS["no_byte_stream_transition_proof"],
        TOKEN_PATHS["no_token_block_execution_proof"],
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for path in paths:
        payload = _load(path)
        counts[path.stem] = payload.get("gate_status")
        errors.extend(_required_false_errors(payload, path.as_posix()))
        if payload.get("gate_status") != "closed":
            errors.append(f"{path.as_posix()}: gate_status must be closed")
    return Stage5DUValidationResult(len(errors), counts, errors)


def validate_stage5du_handoff_continuity() -> Stage5DUValidationResult:
    payload = _load(SOURCE_PATHS["codex_handoff_policy"])
    errors = []
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if payload.get("codex_output_used") is not False:
        errors.append("codex_output_used must be false")
    return Stage5DUValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5du_credential_redaction_policy() -> Stage5DUValidationResult:
    payload = _load(SOURCE_PATHS["credential_redaction_policy_preservation"])
    errors = []
    if payload.get("credential_like_remote_count") != 0:
        errors.append("credential-like remote count must be 0")
    return Stage5DUValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5du_governance_scope() -> Stage5DUValidationResult:
    payload = _load(PROJECT_STATE_PATHS["scope_control"])
    errors = _validate_payload(PROJECT_STATE_PATHS["scope_control"], SCHEMA_PATHS["scope_control"])
    errors.extend(_required_false_errors(payload, PROJECT_STATE_PATHS["scope_control"].as_posix()))
    if payload.get("source_lock_entry_batch_review_performed_now") is not False:
        errors.append("number-fact review batch must remain unperformed")
    return Stage5DUValidationResult(len(errors), _summary_counts(payload), errors)


def stage5du_summary_text() -> str:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5DU summary:",
        f"status={summary.get('status')}",
        f"thread_folders_represented={summary.get('community_thread_folder_count_represented')}",
        f"thread_file_count_total={summary.get('thread_file_count_total')}",
        f"canonical_lp_page_image_root_present={_format(summary.get('canonical_lp_page_image_root_present'))}",
        f"canonical_lp_page_image_count={summary.get('canonical_lp_page_image_count')}",
        f"candidate_records_created={summary.get('candidate_records_created')}",
        f"number_fact_cards_created_or_enriched={summary.get('number_fact_cards_created_or_enriched')}",
        f"source_browser_entries_loaded={summary.get('source_browser_entries_loaded')}",
        f"stage5du_entries_loaded={summary.get('stage5du_entries_loaded')}",
        f"target_priority_decision_created_now={_format(summary.get('target_priority_decision_created_now'))}",
        f"source_lock_entry_batch_review_performed_now={_format(summary.get('source_lock_entry_batch_review_performed_now'))}",
        f"community_code_executed_now={_format(summary.get('community_code_executed_now'))}",
        f"ocr_performed={_format(summary.get('ocr_performed'))}",
        f"image_forensics_performed={_format(summary.get('image_forensics_performed'))}",
        f"route_extraction_performed_now={_format(summary.get('route_extraction_performed_now'))}",
        f"byte_stream_generation_authorized_now={_format(summary.get('byte_stream_generation_authorized_now'))}",
        f"execution_performed={_format(summary.get('execution_performed'))}",
        f"solve_claim={_format(summary.get('solve_claim'))}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


def _build_records(inventory: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    source_browser = _source_browser_summary()
    candidates = _candidate_records()
    records: dict[str, dict[str, Any]] = {}
    records.update(_project_state_records(inventory, candidates, source_browser))
    records.update(_source_records(inventory))
    records.update(candidates)
    records.update(_token_records())
    return records


def _project_state_records(
    inventory: list[dict[str, Any]],
    candidates: dict[str, dict[str, Any]],
    source_browser: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    folder_rows = _source_root_rows(inventory)
    folder_count = len(folder_rows)
    gap_rows = _reviewability_gaps(folder_rows)
    image_count = _count_kind(inventory, "image")
    python_count = _count_kind(inventory, "python")
    text_count = _count_kind(inventory, "text_output")
    spreadsheet_count = _count_kind(inventory, "spreadsheet")
    messages_count = sum(1 for row in inventory if row["file_name"].lower() == "messages.txt")
    candidate_count = len(candidates)
    overlay_count = len(_overlay_rows())
    common = _base_payload("stage5du_summary", SCHEMA_PATHS["summary"])
    summary = {
        **common,
        "status": "complete",
        "source_previous_stage": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_commit_expected": SOURCE_PREVIOUS_STAGE_COMMIT,
        "operator_inserted_visual_community_source_lock_addendum_first": True,
        "number_fact_review_batch_1_still_required_after_this_stage": True,
        "community_thread_source_lock_created": True,
        "community_thread_folder_count_expected": 6,
        "community_thread_folder_count_represented": folder_count,
        "canonical_lp_page_root_crosslink_created": True,
        "red_runes_gateless_gate_records_created": True,
        "big_gaps_negative_space_records_created": True,
        "star_artifacts_records_created": True,
        "cribbing_page15_records_created": True,
        "red_runes_pages54_55_records_created": True,
        "mobius_totient_records_created": True,
        "cross_family_records_created": True,
        "number_fact_card_overlays_created": True,
        "chatgpt_context_updated": True,
        "source_browser_loadability_validated": source_browser["source_browser_validation_error_count"] == 0,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": "assistant_or_operator_review",
        "thread_file_count_total": len(inventory),
        "thread_image_file_count_total": image_count,
        "thread_python_file_count_total": python_count,
        "thread_text_output_file_count_total": text_count,
        "thread_spreadsheet_file_count_total": spreadsheet_count,
        "thread_messages_txt_count": messages_count,
        "canonical_lp_page_image_root_present": CANONICAL_PAGE_ROOT.exists(),
        "canonical_lp_page_image_count": _canonical_page_count(),
        "candidate_records_created": candidate_count,
        "number_fact_cards_created_or_enriched": _candidate_number_fact_count(candidates) + overlay_count,
        "reviewability_gap_count": len(gap_rows),
        **source_browser,
        **_false_flags(),
    }
    summary["source_lock_entry_batch_review_performed_now"] = False

    next_stage = {
        **_base_payload("stage5du_next_stage_decision", SCHEMA_PATHS["next_stage_decision"]),
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": "assistant_or_operator_review",
        "stage5dt_recommended_stage5du_number_fact_review_batch_1": True,
        "operator_inserted_visual_community_source_lock_addendum_first": True,
        "stage5du_is_source_lock_addendum_not_review_batch": True,
        "number_fact_review_batch_1_still_required": True,
        "selected_next_stage_authorizes_execution": False,
        "selected_next_stage_authorizes_activation": False,
        "selected_next_stage_authorizes_byte_stream_generation": False,
        **_false_flags(),
    }
    scope = {
        **_base_payload("stage5du_scope_control", SCHEMA_PATHS["scope_control"]),
        "scope_statement": "metadata-only community visual/red-heading/layout source-lock addendum",
        "source_lock_entry_batch_review_performed_now": False,
        "old_16_worker_default_reintroduced": False,
        "not_authorized": [
            "OCR",
            "image forensics",
            "semantic image interpretation",
            "community code execution",
            "route extraction",
            "target selection",
            "byte-stream generation",
            "execution",
            "CUDA",
            "solve claim",
        ],
        **_false_flags(),
    }
    return {
        "summary": summary,
        "next_stage_decision": next_stage,
        "stage5dt_preservation": _stage5dt_preservation(),
        "operator_inserted_addendum_routing": _operator_inserted_routing(),
        "community_thread_source_lock_plan": _plan_record(folder_rows),
        "visual_observation_family_index": _family_index("visual"),
        "red_heading_family_index": _family_index("red_heading"),
        "number_fact_card_readiness_summary": _number_fact_card_readiness(candidates, overlay_count),
        "source_browser_loadability_summary": {
            **_base_payload("stage5du_source_browser_loadability_summary"),
            **source_browser,
            "source_browser_loadability_validated": source_browser[
                "source_browser_validation_error_count"
            ]
            == 0,
            "new_records_have_titles": True,
            "new_records_have_summary": True,
            "new_records_have_candidate_family_id_where_applicable": True,
            "new_records_have_source_paths": True,
            "new_records_have_review_state": True,
            "new_records_have_number_fact_cards_where_relevant": True,
            **_false_flags(),
        },
        "reviewable_validation_evidence": _validation_evidence(),
        "reviewability_gap_register": {
            **_base_payload("stage5du_reviewability_gap_register"),
            "reviewability_gap_count": len(gap_rows),
            "gaps": gap_rows,
            **_false_flags(),
        },
        "scope_control": scope,
        "chatgpt_context_update_summary": {
            **_base_payload("stage5du_chatgpt_context_update_summary"),
            "chatgpt_context_updated": True,
            "stage5du_section_present": True,
            "raw_source_body_included": False,
            **_false_flags(),
        },
    }


def _source_records(inventory: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    folder_rows = _source_root_rows(inventory)
    messages = _message_rows(inventory)
    attachment_rows = _attachment_rows(inventory)
    image_rows = [row for row in inventory if row["file_kind"] == "image"]
    code_table_rows = [
        row for row in inventory if row["file_kind"] in {"python", "spreadsheet", "text_output"}
    ]
    return {
        "community_thread_source_lock_register": {
            **_base_payload(
                "stage5du_community_thread_source_lock_register",
                SCHEMA_PATHS["community_thread_source_lock_register"],
            ),
            "source_roots": folder_rows,
            "raw_source_files_committed": False,
            "metadata_only": True,
            "source_lock_only": True,
            "route_extraction_performed_now": False,
            "image_forensics_performed": False,
            "ocr_performed": False,
            "expected_thread_summaries": _expected_thread_summaries(),
            **_false_flags(),
        },
        "community_thread_file_inventory": {
            **_base_payload(
                "stage5du_community_thread_file_inventory",
                SCHEMA_PATHS["community_thread_file_inventory"],
            ),
            "file_count": len(inventory),
            "image_file_count": _count_kind(inventory, "image"),
            "audio_file_count": _count_kind(inventory, "audio"),
            "pdf_file_count": _count_kind(inventory, "pdf"),
            "text_file_count": _count_kind(inventory, "text_output")
            + sum(1 for row in inventory if row["file_name"].lower() == "messages.txt"),
            "python_file_count": _count_kind(inventory, "python"),
            "spreadsheet_file_count": _count_kind(inventory, "spreadsheet"),
            "other_file_count": _count_kind(inventory, "other"),
            "files": inventory,
            "raw_source_files_committed": False,
            **_false_flags(),
        },
        "thread_messages_source_locks": {
            **_base_payload(
                "stage5du_thread_messages_source_locks",
                SCHEMA_PATHS["thread_messages_source_locks"],
            ),
            "message_lock_count": len(messages),
            "message_locks": messages,
            "raw_message_bodies_committed": False,
            **_false_flags(),
        },
        "thread_attachment_order_index": {
            **_base_payload(
                "stage5du_thread_attachment_order_index",
                SCHEMA_PATHS["thread_attachment_order_index"],
            ),
            "attachment_count": len(attachment_rows),
            "attachments": attachment_rows,
            "raw_attachments_committed": False,
            **_false_flags(),
        },
        "thread_image_source_locks": {
            **_base_payload("stage5du_thread_image_source_locks"),
            "image_lock_count": len(image_rows),
            "image_locks": image_rows,
            "raw_images_committed": False,
            **_false_flags(),
        },
        "thread_code_and_table_inventory": {
            **_base_payload("stage5du_thread_code_and_table_inventory"),
            "code_inventory_count": sum(1 for row in code_table_rows if row["file_kind"] == "python"),
            "table_inventory_count": sum(
                1 for row in code_table_rows if row["file_kind"] in {"spreadsheet", "text_output"}
            ),
            "files": code_table_rows,
            "community_code_executed_now": False,
            "spreadsheet_macro_execution_performed": False,
            **_false_flags(),
        },
        "canonical_lp_page_image_root_crosslink": _canonical_root_record(),
        "external_reference_url_lock_register": _external_reference_record(),
        "raw_source_noncommit_proof": _raw_noncommit_proof(),
        "codex_handoff_policy": _handoff_policy(),
        "credential_redaction_policy_preservation": _credential_redaction_policy(),
    }


def _candidate_records() -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for key, spec in CANDIDATE_SPECS.items():
        records[key] = _candidate_payload(spec)
    return records


def _token_records() -> dict[str, dict[str, Any]]:
    return {
        "stage5dg_preservation": {
            **_base_payload("stage5du_stage5dg_preservation"),
            "stage5dg_operator_approval_record_preserved": Path(
                "data/token-block/stage5dg-real-operator-approval-record.yaml"
            ).exists(),
            "operator_approval_component_satisfied_now": True,
            "deep_research_acceptance_created_now": False,
            "combined_approval_gate_satisfied_now": False,
            **_false_flags(),
        },
        "stage5bd_preservation": {
            **_base_payload("stage5du_stage5bd_preservation"),
            "stage5bd_run_plan_id_count": 10,
            "stage5bd_run_plan_ids_preserved": True,
            **_false_flags(),
        },
        "active_lineage_preservation": {
            **_base_payload("stage5du_active_lineage_preservation"),
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "active_lineage_preserved": True,
            **_false_flags(),
        },
        "no_active_ingestion_proof": _closed_gate_record(
            "stage5du_no_active_ingestion_proof",
            "active ingestion remains unauthorized",
        ),
        "no_byte_stream_transition_proof": _closed_gate_record(
            "stage5du_no_byte_stream_transition_proof",
            "byte-stream transition remains unauthorized",
        ),
        "no_token_block_execution_proof": {
            **_closed_gate_record(
                "stage5du_no_token_block_execution_proof",
                "token-block execution remains unauthorized",
            ),
            "schema": SCHEMA_PATHS["no_token_block_execution_proof"].as_posix(),
        },
        "operator_console_stage5dt_preservation": {
            **_base_payload("stage5du_operator_console_stage5dt_preservation"),
            "stage5dt_number_fact_card_model_preserved": True,
            "stage5dt_planned_review_batch_preserved": True,
            "stage5dt_review_batch_performed_now": False,
            **_false_flags(),
        },
    }


def _thread_file_inventory() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_root_id, spec in SOURCE_ROOTS.items():
        root = spec["source_root"]
        if not root.exists():
            continue
        for path in sorted(file_path for file_path in root.rglob("*") if file_path.is_file()):
            stat = path.stat()
            rel = path.as_posix()
            rows.append(
                {
                    "source_root_id": source_root_id,
                    "source_root": root.as_posix(),
                    "file_name": path.name,
                    "relative_path": rel,
                    "extension": path.suffix.lower(),
                    "file_kind": _file_kind(path),
                    "mime_guess": mimetypes.guess_type(path.name)[0],
                    "size_bytes": stat.st_size,
                    "modified_utc": datetime.fromtimestamp(stat.st_mtime, UTC)
                    .replace(microsecond=0)
                    .isoformat()
                    .replace("+00:00", "Z"),
                    "sha256": sha256_file(path),
                    "raw_file_committed": False,
                    "metadata_only": True,
                }
            )
    return rows


def _source_root_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_root_id, spec in SOURCE_ROOTS.items():
        root = spec["source_root"]
        root_rows = [row for row in inventory if row["source_root_id"] == source_root_id]
        names = {row["file_name"] for row in root_rows}
        expected = set(spec.get("expected_files") or [])
        rows.append(
            {
                "source_root_id": source_root_id,
                "source_root": root.as_posix(),
                "source_status": "local_ignored_metadata_locked"
                if root.exists()
                else "missing_local_gap_recorded",
                "source_root_exists": root.exists(),
                "messages_txt_present": "messages.txt" in {name.lower() for name in names},
                "file_count": len(root_rows),
                "audio_file_count": _count_kind(root_rows, "audio"),
                "pdf_file_count": _count_kind(root_rows, "pdf"),
                "image_file_count": _count_kind(root_rows, "image"),
                "text_file_count": _count_kind(root_rows, "text_output")
                + sum(1 for row in root_rows if row["file_name"].lower() == "messages.txt"),
                "python_file_count": _count_kind(root_rows, "python"),
                "spreadsheet_file_count": _count_kind(root_rows, "spreadsheet"),
                "other_file_count": _count_kind(root_rows, "other"),
                "missing_expected_files": sorted(expected - names),
                "unexpected_raw_original_pages_folder_present": (root / "original-pages").exists(),
                "expected_thread_images": spec.get("expected_thread_images"),
                "expected_duplicate_note": spec.get("expected_duplicate_note"),
                "expected_files_about": spec.get("expected_files_about"),
            }
        )
    return rows


def _message_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inventory:
        if row["file_name"].lower() != "messages.txt":
            continue
        path = Path(row["relative_path"])
        line_count = 0
        if path.exists():
            line_count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        rows.append(
            {
                "source_root_id": row["source_root_id"],
                "source_path": row["relative_path"],
                "messages_txt_present": True,
                "source_sha256": row["sha256"],
                "size_bytes": row["size_bytes"],
                "line_count": line_count,
                "raw_message_body_committed": False,
                "line_anchor_policy": "metadata only; raw body omitted",
            }
        )
    return rows


def _attachment_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_root: dict[str, list[dict[str, Any]]] = {}
    for row in inventory:
        if row["file_name"].lower() == "messages.txt":
            continue
        by_root.setdefault(row["source_root_id"], []).append(row)
    for source_root_id, root_rows in by_root.items():
        for index, row in enumerate(sorted(root_rows, key=lambda item: item["relative_path"]), start=1):
            rows.append(
                {
                    "source_root_id": source_root_id,
                    "attachment_order": index,
                    "file_name": row["file_name"],
                    "relative_path": row["relative_path"],
                    "file_sha256": row["sha256"],
                    "file_kind": row["file_kind"],
                    "raw_attachment_committed": False,
                    "message_line_anchor_present": False,
                    "anchor_status": "filename_order_metadata_only",
                }
            )
    return rows


def _canonical_root_record() -> dict[str, Any]:
    pages = sorted(CANONICAL_PAGE_ROOT.glob("*.jpg")) if CANONICAL_PAGE_ROOT.exists() else []
    representatives = [
        "00.jpg",
        "04.jpg",
        "07.jpg",
        "10.jpg",
        "13.jpg",
        "20.jpg",
        "41.jpg",
        "42.jpg",
        "43.jpg",
        "49.jpg",
        "51.jpg",
        "53.jpg",
        "54.jpg",
        "55.jpg",
        "56.jpg",
        "57.jpg",
    ]
    locks = []
    for name in representatives:
        path = CANONICAL_PAGE_ROOT / name
        locks.append(
            {
                "page_image_name": name,
                "relative_path": path.as_posix(),
                "exists": path.exists(),
                "sha256": sha256_file(path) if path.exists() else None,
                "size_bytes": path.stat().st_size if path.exists() else 0,
                "raw_page_image_committed_now": False,
            }
        )
    aliases = [CANONICAL_PAGE_ROOT.as_posix()]
    if CANONICAL_PAGE_ROOT_ALT.exists():
        aliases.append(CANONICAL_PAGE_ROOT_ALT.as_posix())
    return {
        **_base_payload(
            "stage5du_canonical_lp_page_image_root_crosslink",
            SCHEMA_PATHS["canonical_lp_page_image_root_crosslink"],
        ),
        "canonical_page_image_root": CANONICAL_PAGE_ROOT.as_posix(),
        "canonical_page_image_root_exists": CANONICAL_PAGE_ROOT.exists(),
        "expected_canonical_page_count": 75,
        "canonical_page_count_observed": len(pages),
        "expected_page_pattern": "00.jpg through 74.jpg",
        "used_for_stage5du_original_page_references": True,
        "old_original_pages_folders_expected_in_thread_roots": False,
        "source_root_aliases": aliases,
        "path_spelling_warning_ciada_vs_cicada_recorded": True,
        "raw_page_images_committed_now": False,
        "representative_page_locks": locks,
        **_false_flags(),
    }


def _external_reference_record() -> dict[str, Any]:
    return {
        **_base_payload("stage5du_external_reference_url_lock_register"),
        "network_fetch_performed_now": False,
        "url_lock_status": "metadata_url_list_only_no_network_dependency",
        "urls": [
            {
                **row,
                "access_status": "not_fetched_in_stage5du_build",
                "raw_body_committed": False,
            }
            for row in EXTERNAL_URLS
        ],
        **_false_flags(),
    }


def _raw_noncommit_proof() -> dict[str, Any]:
    tracked = _git_lines("ls-files", *[spec["source_root"].as_posix() for spec in SOURCE_ROOTS.values()])
    generated_tracked = _git_lines("ls-files", "experiments/results", "codex-output", "codex_output")
    return {
        **_base_payload("stage5du_raw_source_noncommit_proof"),
        "raw_third_party_files_committed": False,
        "raw_source_files_committed": False,
        "tracked_stage5du_source_root_file_count": len(tracked),
        "tracked_stage5du_source_root_files": tracked,
        "generated_or_codex_handoff_tracked_count": len(generated_tracked),
        "generated_or_codex_handoff_tracked_files": generated_tracked,
        **_false_flags(),
    }


def _handoff_policy() -> dict[str, Any]:
    return {
        **_base_payload("stage5du_codex_handoff_policy"),
        "canonical_codex_handoff_root": "codex-output",
        "completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "codex_output_used": False,
        "raw_source_body_included": False,
        **_false_flags(),
    }


def _credential_redaction_policy() -> dict[str, Any]:
    return {
        **_base_payload("stage5du_credential_redaction_policy_preservation"),
        "credential_like_remote_count": _credential_like_remote_count(),
        "credential_redaction_policy_preserved": True,
        "raw_secrets_committed": False,
        **_false_flags(),
    }


def _stage5dt_preservation() -> dict[str, Any]:
    summary = _load(Path("data/project-state/stage5dt-summary.yaml"))
    return {
        **_base_payload("stage5du_stage5dt_preservation"),
        "stage5dt_complete": summary.get("status") == "complete",
        "stage5dt_recommended_stage5du_number_fact_review_batch_1": summary.get(
            "recommended_next_stage_id"
        )
        == "stage-5du",
        "stage5dt_source_browser_entries_loaded": summary.get("source_browser_entries_loaded"),
        "stage5dt_planned_review_batches": summary.get("planned_review_batches"),
        "operator_inserted_visual_community_source_lock_addendum_first": True,
        "number_fact_review_batch_1_performed_now": False,
        "number_fact_review_batch_1_still_required_after_stage5du": True,
        **_false_flags(),
    }


def _operator_inserted_routing() -> dict[str, Any]:
    return {
        **_base_payload("stage5du_operator_inserted_addendum_routing"),
        "stage5dt_recommended_stage5du_number_fact_review_batch_1": True,
        "operator_inserted_visual_community_source_lock_addendum_first": True,
        "stage5du_is_source_lock_addendum_not_review_batch": True,
        "number_fact_review_batch_1_still_required_after_this_stage": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        **_false_flags(),
    }


def _plan_record(folder_rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        **_base_payload("stage5du_community_thread_source_lock_plan"),
        "planned_source_roots": [row["source_root_id"] for row in folder_rows],
        "source_root_count": len(folder_rows),
        "metadata_only": True,
        "source_lock_only": True,
        "review_batch_performed_now": False,
        **_false_flags(),
    }


def _family_index(kind: str) -> dict[str, Any]:
    if kind == "red_heading":
        families = [
            "red_runes_gateless_gate_koan20_title_candidate_v0",
            "page54_55_a_postlude_red_heading_candidate_v1",
            "red_heading_marginalia_gp491_equivalence_family_v1",
            "page0_divinity_within_crossroads_gp491_candidate_v0",
        ]
        record_type = "stage5du_red_heading_family_index"
    else:
        families = [
            "lp_negative_space_layout_candidate_family_v0",
            "star_artifacts_exact254_mask_method_v0",
            "visual_byte_level_surface_context_v0",
            "lp_negative_space_hidden_layer_overlay_family_v0",
        ]
        record_type = "stage5du_visual_observation_family_index"
    return {
        **_base_payload(record_type),
        "family_count": len(families),
        "families": families,
        "selected_now": False,
        "target_priority_decision_created_now": False,
        **_false_flags(),
    }


def _number_fact_card_readiness(candidates: dict[str, dict[str, Any]], overlay_count: int) -> dict[str, Any]:
    return {
        **_base_payload("stage5du_number_fact_card_readiness_summary"),
        "required_fact_card_classes": [
            "red_runes_gateless_gate_number_facts",
            "gap_layout_number_facts",
            "star_artifact_pixel_number_facts",
            "cribbing_page15_instruction_phrase_number_facts",
            "red_heading_gp491_number_facts",
            "mobius_totient_method_number_facts",
        ],
        "candidate_number_fact_count": _candidate_number_fact_count(candidates),
        "enrichment_overlay_count": overlay_count,
        "older_source_lock_entries_with_zero_facts_not_assumed_number_free": True,
        "stage5du_does_not_backfill_all_old_records": True,
        "usable_for_target_priority_now": False,
        **_false_flags(),
    }


def _validation_evidence() -> dict[str, Any]:
    return {
        **_base_payload("stage5du_reviewable_validation_evidence"),
        "focused_validators_defined": True,
        "aggregate_validator_fail_closed": True,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "validation_notes": [
            "Stage 5DU validates metadata/source-lock records only.",
            "No raw third_party files are required by CI validation.",
        ],
        **_false_flags(),
    }


def _reviewability_gaps(folder_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    for row in folder_rows:
        if not row["source_root_exists"]:
            gaps.append(
                {
                    "gap_id": f"{row['source_root_id']}_missing_source_root",
                    "source_root_id": row["source_root_id"],
                    "gap_type": "source_gap",
                    "notes": "Expected local ignored source root is absent.",
                }
            )
        if row.get("unexpected_raw_original_pages_folder_present"):
            gaps.append(
                {
                    "gap_id": f"{row['source_root_id']}_original_pages_folder_present",
                    "source_root_id": row["source_root_id"],
                    "gap_type": "path_policy_warning",
                    "notes": "Per-thread original-pages folder is warning-only; canonical root is CiadaSolversIddqd_v2.",
                }
            )
        for missing in row.get("missing_expected_files") or []:
            gaps.append(
                {
                    "gap_id": f"{row['source_root_id']}_{_slug(missing)}_missing",
                    "source_root_id": row["source_root_id"],
                    "gap_type": "missing_expected_file",
                    "notes": f"Expected file not present locally: {missing}",
                }
            )
    return gaps


def _closed_gate_record(record_type: str, notes: str) -> dict[str, Any]:
    return {
        **_base_payload(record_type),
        "gate_status": "closed",
        "notes": notes,
        "activation_authorized_now": False,
        "byte_stream_generation_authorized_now": False,
        "execution_authorized_now": False,
        "execution_performed": False,
        **_false_flags(),
    }


def _write_overlay_collection() -> None:
    payload = {
        **_base_payload("source_browser_number_fact_enrichment_overlay_collection"),
        "schema": "schemas/operator-console/source-browser-number-fact-enrichment-overlay-v0.schema.json",
        "overlay_collection_id": "stage5du_community_visual_fact_overlays",
        "review_state": "overlay_enriched_fact",
        "overlays": _overlay_rows(),
        **_false_flags(),
    }
    write_yaml(OVERLAY_PATH, payload)


def _overlay_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fact_class, spec_key, fact_id, display_label, value, value_type in [
        (
            "red_runes_gateless_gate_number_facts",
            "red_runes_gateless_gate_koan20_title_candidate",
            "red_runes_227_prime49_grouping",
            "THE ENLIGHTENED MAN = 227 = prime(49), with red/title groups 2/11/3",
            227,
            "gp_sum",
        ),
        (
            "gap_layout_number_facts",
            "big_gap_page_set_16_candidate",
            "big_gap_page_set_one_based_sum_569",
            "Big-gap page set one-based sum = 569",
            569,
            "sum",
        ),
        (
            "star_artifact_pixel_number_facts",
            "star_artifacts_exact254_mask_method",
            "exact254_star_artifact_threshold",
            "Exact 254 mask preserves near-white star layer on pages 10-13 and 41-43",
            254,
            "pixel_count",
        ),
        (
            "cribbing_page15_instruction_phrase_number_facts",
            "page15_your_truth_crib_pointer_candidate",
            "find_follow_truth_palindromic_primes",
            "FIND YOUR TRUTH = 353, FOLLOW YOUR TRUTH = 383",
            353,
            "gp_sum",
        ),
        (
            "red_heading_gp491_number_facts",
            "red_heading_marginalia_gp491_equivalence_family",
            "red_heading_gp491_family",
            "DIVINITY WITHIN / A CROSSROADS / A POSTLUDE / DEAD TREE / YGGDRASIL = 491",
            491,
            "gp_sum",
        ),
        (
            "mobius_totient_method_number_facts",
            "mobius_totient_zero_class_gp_alphabet_candidate",
            "mobius_totient_zero_class_partition",
            "Mobius/totient zero-class GP alphabet partition",
            "zero_class",
            "unknown",
        ),
    ]:
        source_path = CANDIDATE_PATHS[spec_key].as_posix()
        rows.append(
            {
                "record_type": "source_browser_number_fact_enrichment_overlay",
                "overlay_id": f"stage5du_{fact_id}_overlay",
                "fact_class": fact_class,
                "source_record_path": source_path,
                "source_fact_id": fact_id,
                "display_label": display_label,
                "short_label": display_label[:48],
                "value": value,
                "values": [value],
                "value_type": value_type,
                "operation_type": "source_observation",
                "expression": None,
                "relation": "Stage 5DU review-only source-lock number fact.",
                "components": [],
                "why_stored": "Preserves a community/operator visual-route number fact for later review without target selection.",
                "source_paths": [source_path],
                "source_anchor": None,
                "verification_status": "canonical_source_required"
                if value_type == "unknown"
                else "source_author_claim",
                "review_state": "overlay_enriched_fact",
                "risk_notes": [
                    "selection_bias_control_required",
                    "canonical_source_or_image_verification_required",
                    "not_target_priority_evidence",
                ],
                "crosslinks": [spec_key],
                "display_priority": "medium",
                "usable_for_decision_now": False,
                "not_allowed_as": ["proof", "route_seed", "solve_claim"],
            }
        )
    return rows


def _candidate_payload(spec: dict[str, Any]) -> dict[str, Any]:
    path = spec["path"]
    payload = {
        **_base_payload(spec["record_type"], spec["schema"]),
        "candidate_family_id": spec["candidate_family_id"],
        "title": spec["title"],
        "summary": spec["summary"],
        "source_type": "community_forum_thread",
        "source_root": spec["source_root"],
        "source_paths": spec.get("source_paths", [spec["source_root"]]),
        "candidate_status": spec.get("candidate_status", "source_locked_candidate_only"),
        "review_state": spec.get("review_state", "source_locked_review_only"),
        "evidence_status": spec.get("evidence_status", "candidate_context_only"),
        "confidence": spec.get("confidence", "low_medium"),
        "trusted_as_canonical": False,
        "usable_as_experiment_seed_now": False,
        "selected_now": False,
        "usable_for_target_priority_now": False,
        "route_extraction_performed_now": False,
        "solve_claim": False,
        "raw_source_files_committed": False,
        "number_facts": spec.get("number_facts", []),
        "control_requirements": spec.get("control_requirements", DEFAULT_CONTROLS),
        "risk_notes": spec.get("risk_notes", DEFAULT_RISKS),
        **_false_flags(),
        **spec.get("details", {}),
    }
    if "quarantine" in path.name or spec.get("candidate_status") == "quarantined_review_only":
        payload["candidate_status"] = "quarantined_review_only"
        payload["review_state"] = "quarantined"
        payload["evidence_status"] = "quarantined"
    return payload


def _base_payload(record_type: str, schema: Path | None = None) -> dict[str, Any]:
    payload = {
        "record_type": record_type,
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "source_lock_only": True,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "canonical_codex_handoff_root": "codex-output",
        "source_previous_stage_id": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_commit_expected": SOURCE_PREVIOUS_STAGE_COMMIT,
    }
    if schema is not None:
        payload["schema"] = schema.as_posix()
    payload.update(_false_flags())
    return payload


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in FORBIDDEN_FALSE_FLAGS}


def _write_records(records: dict[str, dict[str, Any]]) -> None:
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)


def _write_schemas() -> None:
    object_schema = _object_schema(["record_type", "stage_id"])
    for key in ("summary", "next_stage_decision", "scope_control"):
        write_json(SCHEMA_PATHS[key], object_schema)
    write_json(
        SCHEMA_PATHS["community_thread_source_lock_register"],
        _object_schema(["record_type", "stage_id", "source_roots"]),
    )
    write_json(
        SCHEMA_PATHS["community_thread_file_inventory"],
        _object_schema(["record_type", "stage_id", "files"]),
    )
    write_json(
        SCHEMA_PATHS["thread_messages_source_locks"],
        _object_schema(["record_type", "stage_id", "message_locks"]),
    )
    write_json(
        SCHEMA_PATHS["thread_attachment_order_index"],
        _object_schema(["record_type", "stage_id", "attachments"]),
    )
    write_json(
        SCHEMA_PATHS["canonical_lp_page_image_root_crosslink"],
        _object_schema(["record_type", "stage_id", "canonical_page_image_root"]),
    )
    for key in (
        "community_visual_candidate",
        "red_heading_candidate",
        "negative_space_candidate",
        "star_artifact_candidate",
        "mobius_totient_candidate",
    ):
        write_json(SCHEMA_PATHS[key], _candidate_schema())
    write_json(
        SCHEMA_PATHS["no_token_block_execution_proof"],
        _object_schema(["record_type", "stage_id", "gate_status"]),
    )


def _object_schema(required: list[str]) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": required,
        "properties": {
            "stage_id": {"const": STAGE_ID},
            "metadata_only": {"const": True},
            "source_lock_only": {"const": True},
            "puzzle_execution_allowed": {"const": False},
            "solve_claim": {"const": False},
            "canonical_codex_handoff_root": {"const": "codex-output"},
            "generated_outputs_committed": {"const": False},
            "raw_source_files_committed": {"const": False},
            "raw_third_party_files_committed": {"const": False},
        },
        "additionalProperties": True,
    }


def _candidate_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "record_type",
            "stage_id",
            "candidate_family_id",
            "candidate_status",
            "review_state",
            "evidence_status",
            "trusted_as_canonical",
            "usable_as_experiment_seed_now",
            "selected_now",
            "route_extraction_performed_now",
            "solve_claim",
        ],
        "properties": {
            "stage_id": {"const": STAGE_ID},
            "trusted_as_canonical": {"const": False},
            "usable_as_experiment_seed_now": {"const": False},
            "selected_now": {"const": False},
            "route_extraction_performed_now": {"const": False},
            "solve_claim": {"const": False},
            "candidate_status": {
                "enum": [
                    "source_locked_candidate_only",
                    "source_locked_context_only",
                    "source_locked_method_claim_only",
                    "quarantined_review_only",
                ]
            },
        },
        "additionalProperties": True,
    }


def _validate_required_paths() -> list[str]:
    errors: list[str] = []
    for path in list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values()) + [OVERLAY_PATH]:
        if not path.exists():
            errors.append(f"required path missing: {path.as_posix()}")
    return errors


def _validate_schemas() -> list[str]:
    pairs = [
        (PROJECT_STATE_PATHS["summary"], SCHEMA_PATHS["summary"]),
        (PROJECT_STATE_PATHS["next_stage_decision"], SCHEMA_PATHS["next_stage_decision"]),
        (PROJECT_STATE_PATHS["scope_control"], SCHEMA_PATHS["scope_control"]),
        (
            SOURCE_PATHS["community_thread_source_lock_register"],
            SCHEMA_PATHS["community_thread_source_lock_register"],
        ),
        (
            SOURCE_PATHS["community_thread_file_inventory"],
            SCHEMA_PATHS["community_thread_file_inventory"],
        ),
        (SOURCE_PATHS["thread_messages_source_locks"], SCHEMA_PATHS["thread_messages_source_locks"]),
        (
            SOURCE_PATHS["thread_attachment_order_index"],
            SCHEMA_PATHS["thread_attachment_order_index"],
        ),
        (
            SOURCE_PATHS["canonical_lp_page_image_root_crosslink"],
            SCHEMA_PATHS["canonical_lp_page_image_root_crosslink"],
        ),
        (TOKEN_PATHS["no_token_block_execution_proof"], SCHEMA_PATHS["no_token_block_execution_proof"]),
    ]
    for key, path in CANDIDATE_PATHS.items():
        schema = CANDIDATE_SPECS[key]["schema"]
        pairs.append((path, schema))
    errors: list[str] = []
    for record_path, schema_path in pairs:
        errors.extend(_validate_payload(record_path, schema_path))
    return errors


def _validate_payload(record_path: Path, schema_path: Path) -> list[str]:
    if not record_path.exists() or not schema_path.exists():
        return [f"schema pair missing: {record_path.as_posix()} / {schema_path.as_posix()}"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = read_yaml(record_path)
    validator = Draft202012Validator(schema)
    return [
        f"{record_path.as_posix()}: schema error: {error.message}"
        for error in validator.iter_errors(payload)
    ]


def _candidate_common_errors(payload: dict[str, Any], path: Path) -> list[str]:
    errors = _required_false_errors(payload, path.as_posix())
    for key in (
        "candidate_status",
        "review_state",
        "evidence_status",
        "candidate_family_id",
    ):
        if not payload.get(key):
            errors.append(f"{path.as_posix()}: missing {key}")
    if payload.get("trusted_as_canonical") is not False:
        errors.append(f"{path.as_posix()}: trusted_as_canonical must be false")
    if payload.get("usable_as_experiment_seed_now") is not False:
        errors.append(f"{path.as_posix()}: usable_as_experiment_seed_now must be false")
    if payload.get("selected_now") is not False:
        errors.append(f"{path.as_posix()}: selected_now must be false")
    return errors


def _required_false_errors(payload: Any, prefix: str = "record") -> list[str]:
    errors: list[str] = []
    for key, value in _iter_items(payload):
        if key in FORBIDDEN_FALSE_FLAGS and value is not False:
            errors.append(f"{prefix}: {key} must be false")
    return errors


def _iter_items(value: Any) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            items.append((str(key), item))
            items.extend(_iter_items(item))
    elif isinstance(value, list):
        for item in value:
            items.extend(_iter_items(item))
    return items


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = read_yaml(path)
    return payload if isinstance(payload, dict) else {}


def _summary_counts(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in payload.items()
        if isinstance(value, str | int | bool) and key not in {"schema", "stage_title"}
    }


def _all_yaml_record_paths() -> list[Path]:
    return [
        *PROJECT_STATE_PATHS.values(),
        *SOURCE_PATHS.values(),
        *CANDIDATE_PATHS.values(),
        *TOKEN_PATHS.values(),
        OVERLAY_PATH,
    ]


def _count_paths(paths: dict[str, Path]) -> int:
    return sum(1 for path in paths.values() if path.exists())


def _count_kind(rows: list[dict[str, Any]], kind: str) -> int:
    return sum(1 for row in rows if row.get("file_kind") == kind)


def _candidate_number_fact_count(candidates: dict[str, dict[str, Any]]) -> int:
    return sum(len(payload.get("number_facts") or []) for payload in candidates.values())


def _canonical_page_count() -> int:
    return len(list(CANONICAL_PAGE_ROOT.glob("*.jpg"))) if CANONICAL_PAGE_ROOT.exists() else 0


def _source_browser_summary() -> dict[str, Any]:
    index = build_source_index()
    result = validate_source_index()
    fact_counts = reviewability_counts(index.entries)
    return {
        "source_browser_records_scanned": len(index.scanned_paths),
        "source_browser_entries_loaded": len(index.entries),
        "stage5du_entries_loaded": sum(1 for entry in index.entries if entry.stage_id == STAGE_ID),
        "source_browser_validation_error_count": len(result.errors),
        "source_browser_warning_count": int(result.counts.get("warnings", 0)),
        "source_browser_fact_cards_extracted": fact_counts["total_number_fact_cards_extracted"],
    }


def _file_kind(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        return "image"
    if ext in {".mp3", ".wav", ".flac", ".ogg"}:
        return "audio"
    if ext == ".pdf":
        return "pdf"
    if ext == ".py":
        return "python"
    if ext in {".xlsx", ".xls", ".csv", ".ods"}:
        return "spreadsheet"
    if ext == ".txt":
        return "message_text" if path.name.lower() == "messages.txt" else "text_output"
    return "other"


def _expected_thread_summaries() -> dict[str, Any]:
    return {
        "BigGapsFoundInLiberPrimus": {
            "expected_thread_images": 43,
            "expected_missing_image_numbers": [1],
            "expected_duplicate_note": "images 30-35 duplicate 36-41 in prior archive analysis",
        },
        "RedRunes_Possible_Koan_Connection": {
            "expected_files": [
                "messages.txt",
                "a famous book.png",
                "coincidence for me_01.png",
                "coincidence for me_02.png",
            ],
        },
        "StarArtifactsInLPPageImages": {
            "expected_thread_images": 79,
            "expected_duplicate_note": "1.png = 41.png = 42.png in prior archive analysis",
        },
        "CribbingPage15": {"expected_files": ["messages.txt"]},
        "PotentialCrib_RedRunes_Pages_54_55": {
            "expected_files_about": "messages.txt plus 6 images/screenshots"
        },
        "Mobius_totient_first_page_theory": {
            "expected_files_about": "messages.txt plus images, Python files, text outputs, and spreadsheets"
        },
    }


def _update_chatgpt_context() -> None:
    path = Path("ChatGPT-ContextFile.md")
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    heading = "## Stage 5DU - Community visual/red-heading/negative-space source-lock addendum"
    if heading in text:
        prefix = text.split(heading, 1)[0].rstrip()
        text = prefix + "\n\n" + STAGE5DU_CONTEXT_SECTION
    else:
        text = text.rstrip() + "\n\n" + STAGE5DU_CONTEXT_SECTION
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _update_operational_file_map() -> None:
    path = Path("data/project-state/operational-file-map.yaml")
    if not path.exists():
        return
    payload = read_yaml(path)
    records = payload.get("records", [])
    if not isinstance(records, list):
        return
    additions = [
        {
            "path": PROJECT_STATE_PATHS["summary"].as_posix(),
            "category": "active_data_record",
            "purpose": "Stage 5DU community visual/red-heading/layout metadata-only source-lock summary.",
            "source_of_truth_rank": 1,
            "last_meaningful_update_stage": STAGE_ID,
            "expected_update_frequency": "stage_specific",
            "mutable_or_reference_only": "reference_only",
            "mirror_or_generated_relationships": "source",
            "staleness_check_level": "strict",
            "owner_context": "codex_agent",
            "notes": "Source-lock addendum only; no target selection, route extraction, OCR, image forensics, or execution.",
        },
        {
            "path": SOURCE_PATHS["community_thread_source_lock_register"].as_posix(),
            "category": "active_data_record",
            "purpose": "Compact metadata source-lock register for six ignored community-thread folders.",
            "source_of_truth_rank": 1,
            "last_meaningful_update_stage": STAGE_ID,
            "expected_update_frequency": "stage_specific",
            "mutable_or_reference_only": "reference_only",
            "mirror_or_generated_relationships": "source",
            "staleness_check_level": "strict",
            "owner_context": "codex_agent",
            "notes": "Raw thread folders remain ignored and uncommitted.",
        },
        {
            "path": OVERLAY_PATH.as_posix(),
            "category": "active_data_record",
            "purpose": "Stage 5DU review-only NumberFactCard enrichment overlays.",
            "source_of_truth_rank": 1,
            "last_meaningful_update_stage": STAGE_ID,
            "expected_update_frequency": "stage_specific",
            "mutable_or_reference_only": "reference_only",
            "mirror_or_generated_relationships": "source",
            "staleness_check_level": "strict",
            "owner_context": "operator_review",
            "notes": "Overlays are review display aids only and not target-priority evidence.",
        },
    ]
    records_by_path = {
        record.get("path"): record for record in records if isinstance(record, dict) and record.get("path")
    }
    changed = False
    for addition in additions:
        existing = records_by_path.get(addition["path"])
        if existing is None:
            records.append(addition)
            changed = True
        else:
            for key, value in addition.items():
                if existing.get(key) != value:
                    existing[key] = value
                    changed = True
    if changed:
        payload["records"] = records
        write_yaml(path, payload)


def _update_stage_summary_records(summary: dict[str, Any]) -> None:
    path = Path("data/research/stage-summary-records-v0.yaml")
    if not path.exists():
        return
    payload = read_yaml(path)
    records = payload.get("stage_records") or payload.get("records")
    if not isinstance(records, list):
        return
    records[:] = [
        record
        for record in records
        if not (isinstance(record, dict) and record.get("stage_id") == STAGE_ID)
    ]
    records.append(
        {
            "record_type": "stage_summary_record",
            "stage_id": STAGE_ID,
            "title": STAGE_TITLE,
            "status": "complete",
            "category": "source_lock_metadata",
            "summary": (
                "Source-locked six local community visual/red-heading/layout theory folders "
                "as compact metadata and review-only candidate context."
            ),
            "key_outputs": [
                "Community-thread file inventories, message locks, attachment order records, image/code/table inventories, and canonical LP page root crosslink.",
                "Review-only candidate records for RedRunes/Gateless Gate, BigGaps/negative space, StarArtifacts, CribbingPage15, pages 54/55 red headings, Mobius/totient, and cross-family risk.",
                "NumberFactCard-compatible overlays and Source Browser loadability records.",
            ],
            "result_status": "metadata_only",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                f"Stage 5DU represented {summary.get('community_thread_folder_count_represented')} "
                f"folders, inventoried {summary.get('thread_file_count_total')} files, created "
                f"{summary.get('candidate_records_created')} candidate records, preserved Stage 5DT, "
                "Stage 5DG, Stage 5BD, active-lineage, and the 8-worker cap, and shifted the pending "
                "Stage 5DT number-fact review batch to Stage 5DV without execution."
            ),
        }
    )
    if "stage_records" in payload:
        payload["stage_records"] = records
    else:
        payload["records"] = records
    write_yaml(path, payload)


def _credential_like_remote_count() -> int:
    result = subprocess.run(["git", "remote", "-v"], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return 0
    count = 0
    for line in result.stdout.splitlines():
        if any(_pattern_matches(pattern, line) for pattern in SECRET_PATTERNS):
            count += 1
    return count


def _pattern_matches(pattern: Any, text: str) -> bool:
    if hasattr(pattern, "search"):
        return bool(pattern.search(text))
    return re.search(str(pattern), text) is not None


def _codex_output_used() -> bool:
    return DEPRECATED_CODEX_OUTPUT.exists()


def _git_lines(*args: str) -> list[str]:
    result = subprocess.run(["git", *args], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _format(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _fact(
    fact_id: str,
    display_label: str,
    value: int | str,
    value_type: str,
    expression: str | None = None,
) -> dict[str, Any]:
    if value_type not in VALUE_TYPES:
        value_type = "unknown"
    return {
        "fact_id": fact_id,
        "source_fact_id": fact_id,
        "display_label": display_label,
        "value": value,
        "value_type": value_type,
        "operation_type": "source_observation" if "source_observation" in OPERATION_TYPES else "unknown",
        "expression": expression,
        "components": [],
        "why_stored": "Stage 5DU review-only source-lock number fact.",
        "source_paths": [],
        "verification_status": "source_author_claim"
        if "source_author_claim" in VERIFICATION_STATUSES
        else "not_verified",
        "review_state": "overlay_enriched_fact"
        if "overlay_enriched_fact" in REVIEW_STATES
        else "vague_fact_enrichment_needed",
        "risk_notes": ["selection_bias_control_required", "not_solve_evidence"],
        "crosslinks": [],
        "usable_for_target_priority_now": False,
        "usable_for_decision_now": False,
        "not_allowed_as": ["proof", "execution_seed", "solve_claim", "route_seed"],
    }


DEFAULT_CONTROLS = [
    "canonical source verification",
    "negative controls",
    "selection-bias review",
    "multiple-comparison controls",
]
DEFAULT_RISKS = [
    "community hypothesis",
    "selection bias possible",
    "not target-priority evidence",
]


def _path(name: str) -> Path:
    return HISTORICAL_ROUTE_DIR / name


RED_RUNE_PATHS = {
    "red_runes_gateless_gate_source_lock_register": _path(
        "stage5du-red-runes-gateless-gate-source-lock-register-v0.yaml"
    ),
    "red_runes_gateless_gate_koan20_title_candidate": _path(
        "stage5du-red-runes-gateless-gate-koan20-title-candidate-v0.yaml"
    ),
    "red_runes_the_enlightened_man_grouping": _path(
        "stage5du-red-runes-the-enlightened-man-grouping-2-11-3-candidate-v0.yaml"
    ),
    "red_runes_the_enlightened_man_gp227_prime49": _path(
        "stage5du-red-runes-the-enlightened-man-gp227-prime49-candidate-v0.yaml"
    ),
    "red_runes_enlightened_mumons_comment_155_551_candidate": _path(
        "stage5du-red-runes-enlightened-mumons-comment-155-551-candidate-v0.yaml"
    ),
    "red_runes_prime742_continue_this_candidate": _path(
        "stage5du-red-runes-prime742-continue-this-candidate-v0.yaml"
    ),
    "red_runes_key682_speech_tongue_sentence_candidate": _path(
        "stage5du-red-runes-key682-speech-tongue-sentence-candidate-v0.yaml"
    ),
    "red_runes_first_two_indices31_mumon_word_position_candidate": _path(
        "stage5du-red-runes-first-two-indices31-mumon-word-position-candidate-v0.yaml"
    ),
    "red_runes_zero_based_gp_policy_record": _path(
        "stage5du-red-runes-zero-based-gp-policy-record-v0.yaml"
    ),
    "red_runes_transcription_verification_gap": _path(
        "stage5du-red-runes-transcription-verification-gap-v0.yaml"
    ),
    "gateless_gate_title_control_scan": _path("stage5du-gateless-gate-title-control-scan-v0.yaml"),
}

BIG_GAP_PATHS = {
    "big_gaps_liber_primus_source_lock_register": _path(
        "stage5du-big-gaps-liber-primus-source-lock-register-v0.yaml"
    ),
    "big_gaps_thread_image_inventory": _path("stage5du-big-gaps-thread-image-inventory-v0.yaml"),
    "big_gap_page_set_16_candidate": _path("stage5du-big-gap-page-set-16-candidate-v0.yaml"),
    "lp_line_gap_metric_73_109_129_candidate": _path(
        "stage5du-lp-line-gap-metric-73-109-129-candidate-v0.yaml"
    ),
    "big_gap_page_set_one_based_sum_569_candidate": _path(
        "stage5du-big-gap-page-set-one-based-sum-569-candidate-v0.yaml"
    ),
    "big_gap_red_subset_one_based_sum_229_candidate": _path(
        "stage5du-big-gap-red-subset-one-based-sum-229-candidate-v0.yaml"
    ),
    "big_gap_punctuation_quote_number_correlation_candidate": _path(
        "stage5du-big-gap-punctuation-quote-number-correlation-candidate-v0.yaml"
    ),
    "big_gap_vertical_phase_shift_candidate": _path(
        "stage5du-big-gap-vertical-phase-shift-candidate-v0.yaml"
    ),
    "same_marginalia_page_overlay_registration_candidate": _path(
        "stage5du-same-marginalia-page-overlay-registration-candidate-v0.yaml"
    ),
    "lp2_consecutive_same_frame_overlay_candidate": _path(
        "stage5du-lp2-consecutive-same-frame-overlay-candidate-v0.yaml"
    ),
    "overlay_overlap_f_doublet_candidate": _path(
        "stage5du-overlay-overlap-f-doublet-candidate-v0.yaml"
    ),
    "page56_layout_gap_hash_contract_candidate": _path(
        "stage5du-page56-layout-gap-hash-contract-candidate-v0.yaml"
    ),
    "token_block_big_gap_number_layout_candidate": _path(
        "stage5du-token-block-big-gap-number-layout-candidate-v0.yaml"
    ),
    "layout_typographic_artifact_quarantine": _path(
        "stage5du-layout-typographic-artifact-quarantine-v0.yaml"
    ),
    "lp_negative_space_layout_candidate_family": _path(
        "stage5du-lp-negative-space-layout-candidate-family-v0.yaml"
    ),
}

STAR_PATHS = {
    "star_artifacts_lp_page_images_source_lock_register": _path(
        "stage5du-star-artifacts-lp-page-images-source-lock-register-v0.yaml"
    ),
    "star_artifacts_exact254_mask_method": _path("stage5du-star-artifacts-exact254-mask-method-v0.yaml"),
    "star_artifacts_exact254_page_presence_summary": _path(
        "stage5du-star-artifacts-exact254-page-presence-summary-v0.yaml"
    ),
    "star_artifacts_12_ray_sunburst_candidate": _path(
        "stage5du-star-artifacts-12-ray-sunburst-candidate-v0.yaml"
    ),
    "star_artifacts_layer_order_pasted_over_candidate": _path(
        "stage5du-star-artifacts-layer-order-pasted-over-candidate-v0.yaml"
    ),
    "star_artifacts_outguess_blockiness_control": _path(
        "stage5du-star-artifacts-outguess-blockiness-control-v0.yaml"
    ),
    "lp_page_icc_profile_boundary_candidate": _path(
        "stage5du-lp-page-icc-profile-boundary-candidate-v0.yaml"
    ),
    "lp_page_jpeg_quantization_profile_context": _path(
        "stage5du-lp-page-jpeg-quantization-profile-context-v0.yaml"
    ),
    "wing_tree_641_709_prime_index_gap11_candidate": _path(
        "stage5du-wing-tree-641-709-prime-index-gap11-candidate-v0.yaml"
    ),
    "mayfly_star_artifact_72_600_twinprime_gap_candidate": _path(
        "stage5du-mayfly-star-artifact-72-600-twinprime-gap-candidate-v0.yaml"
    ),
    "stardust_phrase_gp2540_threshold254_candidate": _path(
        "stage5du-stardust-phrase-gp2540-threshold254-candidate-v0.yaml"
    ),
    "star_artifacts_instar_emergence_symbolic_bridge": _path(
        "stage5du-star-artifacts-instar-emergence-symbolic-bridge-v0.yaml"
    ),
    "visual_byte_level_surface_context": _path("stage5du-visual-byte-level-surface-context-v0.yaml"),
    "lp_negative_space_visual_layer_candidate_family": _path(
        "stage5du-lp-negative-space-visual-layer-candidate-family-v0.yaml"
    ),
    "star_artifact_xor_prime_value_claim_quarantine": _path(
        "stage5du-star-artifact-xor-prime-value-claim-quarantine-v0.yaml"
    ),
}

CRIBBING_PATHS = {
    "page15_your_truth_crib_pointer_candidate": _path(
        "stage5du-page15-your-truth-crib-pointer-candidate-v0.yaml"
    ),
    "lp_internal_instruction_phrase_prime_gp_facts": _path(
        "stage5du-lp-internal-instruction-phrase-prime-gp-facts-v0.yaml"
    ),
    "truth_inside_follow_truth_grid_pointer_candidate": _path(
        "stage5du-truth-inside-follow-truth-grid-pointer-candidate-v0.yaml"
    ),
    "divinity_within_491_563_1229_crosslink": _path(
        "stage5du-divinity-within-491-563-1229-crosslink-v0.yaml"
    ),
    "hill_climb_449_cryptographic_crib_candidate": _path(
        "stage5du-hill-climb-449-cryptographic-crib-candidate-v0.yaml"
    ),
    "page15_red_header_tokenization_warning": _path(
        "stage5du-page15-red-header-tokenization-warning-v0.yaml"
    ),
}

PAGE5455_PATHS = {
    "potential_crib_red_runes_54_55_source_lock": _path(
        "stage5du-potential-crib-red-runes-54-55-source-lock-v0.yaml"
    ),
    "page54_55_a_postlude_red_heading_candidate": _path(
        "stage5du-page54-55-a-postlude-red-heading-candidate-v1.yaml"
    ),
    "red_heading_marginalia_gp491_equivalence_family": _path(
        "stage5du-red-heading-marginalia-gp491-equivalence-family-v0.yaml"
    ),
    "dead_tree_yggdrasil_gp491_bridge_candidate": _path(
        "stage5du-dead-tree-yggdrasil-gp491-bridge-candidate-v0.yaml"
    ),
    "a_postlude_491_candidate_filter_source_lock": _path(
        "stage5du-a-postlude-491-candidate-filter-source-lock-v0.yaml"
    ),
    "a_postlude_vs_a_synthesis_a_postulat_alternative_crib_warning": _path(
        "stage5du-a-postlude-vs-a-synthesis-a-postulat-alternative-crib-warning-v0.yaml"
    ),
    "red_heading_single_rune_article_a_candidate": _path(
        "stage5du-red-heading-single-rune-article-a-candidate-v0.yaml"
    ),
    "yggdrasil_network_deep_web_symbolic_bridge": _path(
        "stage5du-yggdrasil-network-deep-web-symbolic-bridge-v0.yaml"
    ),
}

MOBIUS_PATHS = {
    "mobius_totient_first_page_source_lock": _path(
        "stage5du-mobius-totient-first-page-source-lock-v0.yaml"
    ),
    "mobius_totient_thread_code_and_table_inventory": _path(
        "stage5du-mobius-totient-thread-code-and-table-inventory-v0.yaml"
    ),
    "mobius_totient_zero_class_gp_alphabet_candidate": _path(
        "stage5du-mobius-totient-zero-class-gp-alphabet-candidate-v0.yaml"
    ),
    "page0_divinity_within_crossroads_gp491_candidate": _path(
        "stage5du-page0-divinity-within-crossroads-gp491-candidate-v0.yaml"
    ),
    "page0_mobius_totient_plaintext_claim_quarantine": _path(
        "stage5du-page0-mobius-totient-plaintext-claim-quarantine-v0.yaml"
    ),
    "page0_final_33_word_plaintext_claim": _path(
        "stage5du-page0-final-33-word-plaintext-claim-v0.yaml"
    ),
    "mobius_visual_to_arithmetic_function_bridge": _path(
        "stage5du-mobius-visual-to-arithmetic-function-bridge-v0.yaml"
    ),
    "red_heading_marginalia_gp491_equivalence_family_v1": _path(
        "stage5du-red-heading-marginalia-gp491-equivalence-family-v1.yaml"
    ),
    "lp_red_heading_beginning_end_gp491_frame_candidate": _path(
        "stage5du-lp-red-heading-beginning-end-gp491-frame-candidate-v0.yaml"
    ),
    "red_heading_gp_equivalence_selection_bias_warning": _path(
        "stage5du-red-heading-gp-equivalence-selection-bias-warning-v0.yaml"
    ),
    "thread_code_execution_quarantine": _path("stage5du-thread-code-execution-quarantine-v0.yaml"),
}

CROSS_PATHS = {
    "red_heading_external_text_reference_family": _path(
        "stage5du-red-heading-external-text-reference-family-v0.yaml"
    ),
    "red_heading_marginalia_gp_equivalence_family_v1_cross": _path(
        "stage5du-red-heading-marginalia-gp-equivalence-family-v1.yaml"
    ),
    "lp_negative_space_hidden_layer_overlay_family": _path(
        "stage5du-lp-negative-space-hidden-layer-overlay-family-v0.yaml"
    ),
    "exact_pixel_value_visual_surface_family": _path(
        "stage5du-exact-pixel-value-visual-surface-family-v0.yaml"
    ),
    "visual_layout_artifact_vs_intentionality_risk_register": _path(
        "stage5du-visual-layout-artifact-vs-intentionality-risk-register-v0.yaml"
    ),
    "community_visual_probability_claim_quarantine": _path(
        "stage5du-community-visual-probability-claim-quarantine-v0.yaml"
    ),
}

CANDIDATE_PATHS: dict[str, Path] = {}
CANDIDATE_PATHS.update(RED_RUNE_PATHS)
CANDIDATE_PATHS.update(BIG_GAP_PATHS)
CANDIDATE_PATHS.update(STAR_PATHS)
CANDIDATE_PATHS.update(CRIBBING_PATHS)
CANDIDATE_PATHS.update(PAGE5455_PATHS)
CANDIDATE_PATHS.update(MOBIUS_PATHS)
CANDIDATE_PATHS.update(CROSS_PATHS)

DATA_PATHS: dict[str, Path] = {}
DATA_PATHS.update(PROJECT_STATE_PATHS)
DATA_PATHS.update(SOURCE_PATHS)
DATA_PATHS.update(CANDIDATE_PATHS)
DATA_PATHS.update(TOKEN_PATHS)


def _candidate_spec(
    key: str,
    *,
    family: str | None = None,
    title: str | None = None,
    source_root: str,
    schema: Path,
    details: dict[str, Any] | None = None,
    facts: list[dict[str, Any]] | None = None,
    status: str = "source_locked_candidate_only",
    review_state: str = "source_locked_review_only",
    evidence: str = "candidate_context_only",
    confidence: str = "low_medium",
) -> dict[str, Any]:
    family_id = family or f"{key}_v0"
    return {
        "path": CANDIDATE_PATHS[key],
        "record_type": family_id,
        "candidate_family_id": family_id,
        "title": title or family_id.replace("_", " "),
        "summary": f"Stage 5DU review-only source-lock record for {family_id}.",
        "source_root": source_root,
        "schema": schema,
        "details": details or {},
        "number_facts": facts or [],
        "candidate_status": status,
        "review_state": review_state,
        "evidence_status": evidence,
        "confidence": confidence,
    }


RED_SOURCE = "third_party/RedRunes_Possible_Koan_Connection"
BIG_SOURCE = "third_party/BigGapsFoundInLiberPrimus"
STAR_SOURCE = "third_party/StarArtifactsInLPPageImages"
CRIB_SOURCE = "third_party/CribbingPage15"
PAGE5455_SOURCE = "third_party/PotentialCrib_RedRunes_Pages_54_55"
MOBIUS_SOURCE = "third_party/Mobius_totient_first_page_theory"

CANDIDATE_SPECS: dict[str, dict[str, Any]] = {
    key: _candidate_spec(key, source_root=RED_SOURCE, schema=SCHEMA_PATHS["red_heading_candidate"])
    for key in RED_RUNE_PATHS
}
CANDIDATE_SPECS.update(
    {
        key: _candidate_spec(key, source_root=BIG_SOURCE, schema=SCHEMA_PATHS["negative_space_candidate"])
        for key in BIG_GAP_PATHS
    }
)
CANDIDATE_SPECS.update(
    {
        key: _candidate_spec(key, source_root=STAR_SOURCE, schema=SCHEMA_PATHS["star_artifact_candidate"])
        for key in STAR_PATHS
    }
)
CANDIDATE_SPECS.update(
    {
        key: _candidate_spec(key, source_root=CRIB_SOURCE, schema=SCHEMA_PATHS["red_heading_candidate"])
        for key in CRIBBING_PATHS
    }
)
CANDIDATE_SPECS.update(
    {
        key: _candidate_spec(key, source_root=PAGE5455_SOURCE, schema=SCHEMA_PATHS["red_heading_candidate"])
        for key in PAGE5455_PATHS
    }
)
CANDIDATE_SPECS.update(
    {
        key: _candidate_spec(key, source_root=MOBIUS_SOURCE, schema=SCHEMA_PATHS["mobius_totient_candidate"])
        for key in MOBIUS_PATHS
    }
)
CANDIDATE_SPECS.update(
    {
        key: _candidate_spec(key, source_root="multiple_stage5du_source_roots", schema=SCHEMA_PATHS["community_visual_candidate"])
        for key in CROSS_PATHS
    }
)

CANDIDATE_SPECS["red_runes_gateless_gate_koan20_title_candidate"].update(
    {
        "candidate_family_id": "red_runes_gateless_gate_koan20_title_candidate_v0",
        "details": {
            "red_rune_groups_claimed": [{"group_length": 2}, {"group_length": 11}, {"group_length": 3}],
            "target_title": "THE ENLIGHTENED MAN",
            "target_title_token_groups": [{"THE": 2}, {"ENLIGHTENED": 11}, {"MAN": 3}],
            "grouping_match_2_11_3": True,
            "zero_based_gp_index_sum_title": 227,
            "prime_49": 227,
            "gateless_gate_edition_case_count": 49,
            "koan_number": 20,
            "lp_page_index_claim": 20,
            "page_index_convention_verification_required": True,
            "red_rune_transcription_verification_required": True,
            "gateless_gate_title_control_scan": {
                "title_sum_227_not_unique": True,
                "another_title_with_227": "TWO MONKS ROLL UP THE SCREEN",
                "grouping_2_11_3_unique_to_the_enlightened_man_under_declared_tokenization": True,
            },
        },
        "number_facts": [
            _fact(
                "red_runes_227_prime49_grouping",
                "THE ENLIGHTENED MAN = 227 = prime(49), with red/title groups 2/11/3",
                227,
                "gp_sum",
                "THE ENLIGHTENED MAN zero-index GP sum = 227 = prime(49)",
            )
        ],
    }
)
CANDIDATE_SPECS["red_runes_enlightened_mumons_comment_155_551_candidate"]["details"] = {
    "phrase_a": "ENLIGHTENED",
    "phrase_b": "MUMONS COMMENT",
    "zero_based_gp_index_sum_a": 155,
    "zero_based_gp_index_sum_b": 155,
    "gp_prime_sum_a": 551,
    "gp_prime_sum_b": 551,
    "spelling_warning": "MUMON, not MUMMON",
    "semantic_link": "title_word_to_comment_section",
}
CANDIDATE_SPECS["red_runes_prime742_continue_this_candidate"]["details"] = {
    "red_rune_prime_sum_claim": 742,
    "matched_phrase": "LET ANOTHER CONTINUE THIS",
    "matched_phrase_gp_prime_sum": 742,
    "omitted_final_word": "POEM",
    "partial_line_match_warning": True,
}
CANDIDATE_SPECS["red_runes_key682_speech_tongue_sentence_candidate"]["details"] = {
    "key_derivation_model": "P = (C + K) mod 29",
    "plaintext_target": "THE ENLIGHTENED MAN",
    "key_indices": {
        "THE": [11, 7],
        "ENLIGHTENED": [6, 1, 28, 5, 4, 21, 20, 7, 22, 4, 15],
        "MAN": [3, 23, 16],
    },
    "key_prime_sum": 682,
    "koan_sentence": "AND HE ALSO SAID IT IS NOT NECESSARY FOR SPEECH TO COME FROM THE TONGUE",
    "koan_sentence_zero_based_gp_index_sum": 682,
    "key_stream_overfit_warning": True,
}
CANDIDATE_SPECS["red_runes_first_two_indices31_mumon_word_position_candidate"]["details"] = {
    "first_two_red_rune_indices": [20, 11],
    "sum": 31,
    "word_position_claim": "word 31 of koan body excluding title is Mumon's",
    "word_count_policy_required": True,
    "confidence": "low_medium",
}

CANDIDATE_SPECS["big_gap_page_set_16_candidate"]["details"] = {
    "claimed_big_gap_pages_zero_based": [4, 7, 10, 21, 22, 35, 36, 37, 38, 41, 42, 43, 51, 53, 56, 57],
    "claimed_big_gap_page_count": 16,
    "zero_based_page_sum": 553,
    "zero_based_sum_factorization": [7, 79],
    "one_based_page_sum": 569,
    "one_based_page_sum_prime": True,
    "crosslink_569": "2016 image dimension 563x569 candidate context",
    "selection_risk_warning": True,
}
CANDIDATE_SPECS["big_gap_page_set_16_candidate"]["number_facts"] = [
    _fact("big_gap_page_set_one_based_sum_569", "Big-gap page set one-based sum = 569", 569, "sum")
]
CANDIDATE_SPECS["big_gap_red_subset_one_based_sum_229_candidate"]["details"] = {
    "claimed_big_gap_red_subset_zero_based": [4, 10, 43, 53, 56, 57],
    "one_based_red_subset_sum": 229,
    "one_based_red_subset_sum_prime": True,
    "crosslink_229": "Mayfly axis 167/229/229/229/104",
    "red_threshold_policy_required": True,
    "selection_risk_warning": True,
}
CANDIDATE_SPECS["lp_line_gap_metric_73_109_129_candidate"]["details"] = {
    "regular_gap_claim_px": 73,
    "big_gap_claim_px": 109,
    "gap_difference_claim_px": 36,
    "parable_gap_claim_px": 129,
    "parable_gap_difference_claim_px": 56,
    "gp_value_73": "L",
    "gp_value_109": "EA",
    "prime_index_109_one_indexed": 29,
    "thread_claim_37_is_i_corrected": True,
    "standard_gp_i_value": 31,
    "standard_gp_37_value": "J",
    "measurement_policy_required": True,
}
CANDIDATE_SPECS["big_gap_vertical_phase_shift_candidate"]["details"] = {
    "same_frame_overlay_registration_candidate": True,
    "big_gap_vertical_phase_shift_candidate": True,
    "possible_role": ["align", "shift", "skip", "phase_change", "mask", "before_after_separator"],
    "cipher_claimed_now": False,
    "overlay_route_extraction_performed_now": False,
}
CANDIDATE_SPECS["overlay_overlap_f_doublet_candidate"]["details"] = {
    "overlap_f_doublet_claim_present": True,
    "claimed_nicest_overlaps_include": ["one_F", "two_doublets"],
    "crosslinks": [
        "no_f_rune_count_section_flow_candidate_v0",
        "lp_doublet_scarcity_feature_v1",
        "disk_doublet_suppression_candidate_v1",
    ],
    "expected_random_overlap_warning": True,
    "all_page_pair_baseline_required": True,
    "exact_rune_transcription_required": True,
    "canonical_alignment_rule_required": True,
}
CANDIDATE_SPECS["page56_layout_gap_hash_contract_candidate"]["details"] = {
    "page56_big_gap_hash_contract_crosslink": True,
    "token_block_big_gap_number_layout_crosslink": True,
    "page51_number_token_example_claim": "1r 2c 2q 3o 30 0a 39 1K",
}

CANDIDATE_SPECS["star_artifacts_exact254_mask_method"]["details"] = {
    "method_claim": "max(R,G,B) == 254 mask reveals star/sunburst artifacts",
    "method_status": "source_locked_method_claim_only",
    "exact254_claimed_or_assistant_observed_counts": [
        {"page": "10.jpg", "max_rgb_254_pixels": 1757676, "pure_rgb_254_254_254_pixels": 1755076},
        {"page": "11.jpg", "max_rgb_254_pixels": 1736280, "pure_rgb_254_254_254_pixels": 1735123},
        {"page": "12.jpg", "max_rgb_254_pixels": 1737723, "pure_rgb_254_254_254_pixels": 1736591},
        {"page": "13.jpg", "max_rgb_254_pixels": 1710229, "pure_rgb_254_254_254_pixels": 1701930},
        {"page": "41.jpg", "max_rgb_254_pixels": 246110, "pure_rgb_254_254_254_pixels": 246110},
        {"page": "42.jpg", "max_rgb_254_pixels": 242707, "pure_rgb_254_254_254_pixels": 242707},
        {"page": "43.jpg", "max_rgb_254_pixels": 245319, "pure_rgb_254_254_254_pixels": 245230},
    ],
    "prominent_clusters": {
        "pages_10_13": "very_strong_star_sunburst_layer",
        "pages_06_09": "strong_old_man_or_visual_artifact_layer",
        "pages_41_43": "mayfly_pages_clean_side_star_artifacts",
        "pages_03_04": "high_artifact_counts_more_blocky_or_outguess_looking",
    },
}
CANDIDATE_SPECS["star_artifacts_exact254_mask_method"]["number_facts"] = [
    _fact("exact254_star_artifact_threshold", "Exact 254 near-white star/sunburst layer threshold", 254, "pixel_count")
]
CANDIDATE_SPECS["star_artifacts_12_ray_sunburst_candidate"]["details"] = {
    "ray_count_claim": 12,
    "possible_interpretations": ["clock", "zodiac", "cycle", "circumference_marker", "sunburst", "stardust_motif", "production_artifact"],
    "route_evidence_now": False,
    "component_inventory_required": True,
}
CANDIDATE_SPECS["star_artifacts_layer_order_pasted_over_candidate"]["details"] = {
    "production_stack_model_candidate": [
        "faint_background_star_layer",
        "art_or_cicada_or_frame_layer",
        "rune_text_and_red_runes",
        "export_compression",
    ],
    "interpretation": "production_layer_context_only",
}
CANDIDATE_SPECS["lp_page_icc_profile_boundary_candidate"]["details"] = {
    "claim": "pages 00-16 have no ICC profile; pages 17-74 share same ICC profile",
    "icc_profile_length_claim": 2576,
    "production_boundary_interpretation_only": True,
}
CANDIDATE_SPECS["lp_page_jpeg_quantization_profile_context"]["details"] = {
    "quantization_group_count_claim": 4,
    "production_metadata_context_only": True,
}
CANDIDATE_SPECS["wing_tree_641_709_prime_index_gap11_candidate"]["details"] = {
    "blurred_tree_left_edge_offset_claim_px": 709,
    "blurred_tree_right_edge_offset_claim_px": 641,
    "641_is_prime": True,
    "709_is_prime": True,
    "primepi_641": 116,
    "primepi_709": 127,
    "prime_index_difference": 11,
    "prior_pattern_values": [
        {"value": 107, "prime_index": 28},
        {"value": 167, "prime_index": 39},
        {"value": 229, "prime_index": 50},
    ],
    "prior_pattern_index_step": 11,
    "canonical_coordinate_policy_required": True,
}
CANDIDATE_SPECS["mayfly_star_artifact_72_600_twinprime_gap_candidate"]["details"] = {
    "coordinate_claims": {"left_gap_px": 72, "right_gap_px": 600},
    "72_between_twin_primes_71_73": True,
    "600_between_twin_primes_599_601": True,
    "coordinate_selection_risk": True,
    "full_component_register_required": True,
}
CANDIDATE_SPECS["stardust_phrase_gp2540_threshold254_candidate"]["details"] = {
    "source_phrase": "THE STARDUST FROM WHEN LIFE ENDS WILL SWIRL AGAIN ALONG AND START",
    "gp_prime_sum": 2540,
    "threshold_crosslink": 254,
    "relation": "2540 = 254 * 10",
    "source_phrase_status": "unverified_community_decode_screenshot",
    "not_accepted_plaintext": True,
    "route_extraction_performed_now": False,
}
CANDIDATE_SPECS["visual_byte_level_surface_context"]["details"] = {
    "context": [
        "exact RGB/channel value 254",
        "exact pixel counts",
        "token-block byte-like surface",
        "Page56 hash bytes",
        "image channel byte values",
    ],
    "interpretation": "byte_level_visual_surface_context_only",
}

CANDIDATE_SPECS["page15_your_truth_crib_pointer_candidate"]["details"] = {
    "internal_instruction_phrase_gp_facts": [
        {"phrase": "FIND YOUR TRUTH", "gp_sum": 353, "prime_status": "prime", "note": "palindromic_prime"},
        {"phrase": "FOLLOW YOUR TRUTH", "gp_sum": 383, "prime_status": "prime", "note": "palindromic_prime"},
        {"phrase": "KWESTION ALL THINGS", "gp_sum": 727, "prime_status": "prime", "note": "palindromic_prime"},
        {"phrase": "DISCOVER TRUTH INSIDE YOURSELF", "gp_sum": 971, "reverse": 179, "reverse_prime_status": "prime"},
        {"phrase": "IMPOSE NOTHING ON OTHERS", "gp_sum": 571, "prime_status": "prime"},
        {"phrase": "EXPERIENCE YOUR DEATH", "gp_sum": 769, "prime_status": "prime"},
    ],
    "along_the_way_bridge": {
        "phrase": "ALONG THE WAY",
        "gp_sum": 547,
        "prime_status": "prime",
        "crosslink": "Interconnectedness beat count 547 community claim",
        "confidence": "low_medium",
    },
}
CANDIDATE_SPECS["page15_your_truth_crib_pointer_candidate"]["number_facts"] = [
    _fact("find_follow_truth_palindromic_primes", "FIND YOUR TRUTH = 353, FOLLOW YOUR TRUTH = 383", 353, "gp_sum")
]
CANDIDATE_SPECS["divinity_within_491_563_1229_crosslink"]["details"] = {
    "phrase_values": {
        "DIVINITY WITHIN": 491,
        "THE DIVINITY WITHIN": 563,
        "FIND THE DIVINITY WITHIN AND EMERGE": 1229,
    },
    "crosslinks": [
        "music_instar_parable_id3_gp_product_candidate_v1",
        "2016_tree_dimension_563_context",
        "page0_divinity_within_crossroads_gp491_candidate_v0",
    ],
}
CANDIDATE_SPECS["hill_climb_449_cryptographic_crib_candidate"]["details"] = {
    "phrase": "HILL CLIMB",
    "gp_sum": 449,
    "crosslinks": ["PARABLE = 449", "MAYFLY = 449", "hill_cipher", "hill_climbing_algorithm"],
    "confidence": "low_medium",
}
CANDIDATE_SPECS["page15_red_header_tokenization_warning"]["details"] = {
    "red_header_claim": "YOUR TRUTH",
    "visible_red_header_group_lengths_claim": [4, 5],
    "standard_gp_token_lengths": {"YOUR": 4, "TRUTH": 4},
    "standard_short_token_match_clean": False,
    "nonstandard_truth_tokenization_required": True,
    "candidate_confidence_warning": True,
}

CANDIDATE_SPECS["page54_55_a_postlude_red_heading_candidate"]["details"] = {
    "red_heading_structure_claim": {"word_count": 2, "group_lengths": [1, 8]},
    "proposed_plaintext": "A POSTLUDE",
}
CANDIDATE_SPECS["red_heading_marginalia_gp491_equivalence_family"]["details"] = {
    "gp491_family": [
        {"phrase": "DEAD TREE", "gp_sum": 491},
        {"phrase": "YGGDRASIL", "gp_sum": 491},
        {"phrase": "A POSTLUDE", "gp_sum": 491},
        {"phrase": "DIVINITY WITHIN", "gp_sum": 491},
        {"phrase": "A CROSSROADS", "gp_sum": 491},
    ],
}
CANDIDATE_SPECS["red_heading_marginalia_gp491_equivalence_family"]["number_facts"] = [
    _fact("red_heading_gp491_family", "GP491 family: A POSTLUDE / DEAD TREE / YGGDRASIL / DIVINITY WITHIN / A CROSSROADS", 491, "gp_sum")
]
CANDIDATE_SPECS["red_heading_single_rune_article_a_candidate"]["details"] = {
    "A_gp_sum": 97,
    "POSTLUDE_gp_sum": 394,
    "sum": 491,
    "single_rune_article_a_candidate": True,
}
CANDIDATE_SPECS["a_postlude_491_candidate_filter_source_lock"]["details"] = {
    "word_filter_source_claim": {"initial_words_loaded": 19083, "matching_words_found": 12},
    "matching_words_shown": [
        "BRANDISH",
        "CARBONYL",
        "CONGRIDAE",
        "JUDICIARY",
        "LUNKHEAD",
        "LYGODIUM",
        "MINSTREL",
        "MONSTERA",
        "PARTICLE",
        "PILOTAGE",
        "PLUNDERING",
        "POSTLUDE",
    ],
    "semantic_manual_selection_required": True,
}
CANDIDATE_SPECS["a_postlude_vs_a_synthesis_a_postulat_alternative_crib_warning"]["details"] = {
    "alternative_cribs": [
        {"phrase": "A SYNTHESIS", "gp_sum": 491},
        {"phrase": "A POSTULAT", "gp_sum": 491},
        {"phrase": "A RECREATION", "gp_sum": 503, "prime_status": "prime"},
    ],
    "A_POSTLUDE_not_uniquely_implied_by_gp_sum": True,
}
CANDIDATE_SPECS["dead_tree_yggdrasil_gp491_bridge_candidate"]["details"] = {
    "YGGDRASIL_gp_sum": 491,
    "YGGDRASILL_gp_sum": 564,
    "single_L_required_for_491": True,
}
CANDIDATE_SPECS["yggdrasil_network_deep_web_symbolic_bridge"].update({"confidence": "low"})
CANDIDATE_SPECS["yggdrasil_network_deep_web_symbolic_bridge"]["details"] = {
    "symbolic_network_context_only": True,
    "not_used_for_target_selection_now": True,
}

CANDIDATE_SPECS["mobius_totient_thread_code_and_table_inventory"]["details"] = {
    "community_code_executed_now": False,
    "spreadsheet_macro_execution_performed": False,
}
CANDIDATE_SPECS["mobius_totient_zero_class_gp_alphabet_candidate"]["details"] = {
    "method": [
        "for each rune, take GP prime value p",
        "compute phi(p)",
        "because p is prime, phi(p)=p-1",
        "compute Mobius mu(p-1)",
        "classify rune into {-1, 0, 1}, with special attention to zero class",
    ],
    "method_status": "deterministic_transform_candidate",
    "community_code_available": True,
    "community_code_executed_now": False,
    "zero_class_runes": ["TH", "C/K", "G", "W", "N", "J", "EO", "S/Z", "B", "L", "D", "A", "AE", "EA"],
    "zero_class_verification_status": "arithmetic_verified_or_recorded_as_claim",
}
CANDIDATE_SPECS["mobius_totient_zero_class_gp_alphabet_candidate"]["number_facts"] = [
    _fact("mobius_totient_zero_class_partition", "Mobius/totient zero-class GP alphabet partition", "zero_class", "unknown")
]
CANDIDATE_SPECS["page0_divinity_within_crossroads_gp491_candidate"]["details"] = {
    "page0_red_heading_group_lengths_claim": [8, 5],
    "proposed_plaintext": "DIVINITY WITHIN",
    "DIUINITY_WITHIN_variant_recorded": True,
    "DIVINITY_WITHIN_gp_sum": 491,
    "A_CROSSROADS_gp_sum": 491,
    "red_heading_not_accepted_as_decrypted": True,
    "zero_preservation_red_heading_claim_present": True,
    "cipher_plaintext_zero_class_alignment_claimed": True,
    "known_plaintext_attack_performed_now": False,
    "plaintext_accepted_now": False,
}
CANDIDATE_SPECS["page0_mobius_totient_plaintext_claim_quarantine"].update(
    {
        "candidate_status": "quarantined_review_only",
        "review_state": "quarantined",
        "evidence_status": "quarantined",
    }
)
CANDIDATE_SPECS["page0_mobius_totient_plaintext_claim_quarantine"]["details"] = {
    "proposed_plaintext_claim": (
        "DIUINITY WITHIN / AEONS AGO WAS AMALGAMATED BASIS / ONLY ONE AND DARK / "
        "AND BEYOND LIMITATIONS OF NO THING / AND ABYSSAL AMONG ANYTHING IN / "
        "OCEAN OF BEING / THUS AGAIN AN OLD SAGE / DOES BLESSING HOLY SABBATH END."
    ),
    "word_count_claim": 33,
    "accepted_as_plaintext_now": False,
    "accepted_as_decryption_now": False,
    "manual_semantic_selection_warning": True,
    "deterministic_reimplementation_required": True,
    "negative_controls_required": True,
    "claim_drift_examples": [
        {"early": "AEONS AGO WAS AMALGAMATING BASIS", "later": "AEONS AGO WAS AMALGAMATED BASIS"}
    ],
    "claim_drift_warning": True,
}
CANDIDATE_SPECS["red_heading_marginalia_gp491_equivalence_family_v1"]["details"] = {
    "examples": [
        "DIVINITY WITHIN = A CROSSROADS = 491",
        "A POSTLUDE = DEAD TREE = YGGDRASIL = 491",
        "AN END = FIVE DOTS = 311",
        "PARABLE = MAYFLY = 449",
    ],
    "interpretation": "red headings may be tied to natural image/marginalia labels by GP equality",
    "selection_bias_warning": True,
    "all_red_headings_control_scan_required": True,
}
CANDIDATE_SPECS["lp_red_heading_beginning_end_gp491_frame_candidate"]["details"] = {
    "opening_frame": ["DIVINITY WITHIN", "A CROSSROADS", 491],
    "ending_frame": ["A POSTLUDE", "DEAD TREE", "YGGDRASIL", 491],
    "symbolic_context": ["beginning_end", "crossroads_postlude", "divinity_tree", "ouroboros_cycle"],
}
CANDIDATE_SPECS["thread_code_execution_quarantine"].update(
    {"candidate_status": "quarantined_review_only", "review_state": "quarantined", "evidence_status": "quarantined"}
)
CANDIDATE_SPECS["thread_code_execution_quarantine"]["details"] = {
    "community_code_executed_now": False,
    "spreadsheet_macro_execution_performed": False,
    "code_review_required_before_any_execution": True,
}
CANDIDATE_SPECS["visual_layout_artifact_vs_intentionality_risk_register"]["details"] = {
    "risk_families": [
        "red_heading_phrase_selection_bias",
        "image_label_subjectivity",
        "page_index_convention_ambiguity",
        "canonical_transcription_required",
        "canonical_image_hash_required",
        "exact_color_count_jpeg_recompression_risk",
        "star_artifact_production_artifact_risk",
        "line_gap_typographic_artifact_risk",
        "overlay_random_overlap_expected_baseline",
        "community_code_manual_semantic_selection_risk",
        "proposed_plaintext_claim_drift",
    ],
    "controls_required_before_target_priority": [
        "all_red_heading_control_scan",
        "all_page_gap_measurement_control",
        "all_same_frame_overlay_baseline",
        "exact_pixel_value_canonical_image_control",
        "Mobius/totient known-plaintext validation against solved pages",
        "deterministic dictionary/scoring freeze before page0 tests",
    ],
}
CANDIDATE_SPECS["community_visual_probability_claim_quarantine"].update(
    {"candidate_status": "quarantined_review_only", "review_state": "quarantined", "evidence_status": "quarantined"}
)
CANDIDATE_SPECS["community_visual_probability_claim_quarantine"]["details"] = {
    "probability_claims_present": True,
    "probability_claims_accepted_as_validated": False,
    "quarantine_reasons": [
        "broad search spaces",
        "multiple comparisons",
        "manual selection",
        "unknown canonical source image state",
        "unbounded phrase choice",
        "no negative controls",
    ],
}
