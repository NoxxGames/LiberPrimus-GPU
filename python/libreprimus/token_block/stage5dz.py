"""Stage 5DZ triangle/Page32 bounded findings source-lock records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import (
    validate_path_canonicalization,
    validate_source_index,
)
from libreprimus.token_block.models import read_yaml, write_json, write_yaml

STAGE_ID = "stage-5dz"
STAGE_TITLE = (
    "Stage 5DZ - Triangle/Page32 bounded-solve findings source-lock and "
    "enriched review records, without execution"
)
PROMPT_TYPE = "codex_metadata_and_operator_console_reviewability_implementation"
PREVIOUS_STAGE_ID = "stage-5dy"
PREVIOUS_STAGE_TITLE = (
    "Stage 5DY - Validation performance, parallel-test discipline, stage-isolation, "
    "and non-mutating validator repair, without execution"
)
PREVIOUS_STARTING_COMMIT = "eb93bc8d4367464908645c95677fe6a26427e2af"
PREVIOUS_FINAL_COMMIT = "da0a6439c7fda70feac98bd8b7ef9118e680bac7"
PREVIOUS_ISSUE = 160
PREVIOUS_CI_RUN = 27271767355
PREVIOUS_CI_STATUS = "passed"
NEXT_STAGE_ID = "stage-5ea"
NEXT_STAGE_TITLE = "Stage 5EA - Operator/assistant source-lock number-fact review batch 3, without execution"
NEXT_PROMPT_TYPE = "assistant_or_operator_review_then_codex_overlay_update"
REVIEW_BATCH_ID = "triangle_page32_bounded_findings_source_lock_enrichment"
REVIEW_BATCH_KIND = "inserted_bounded_findings_source_lock_addendum"
EXPECTED_OVERLAY_COUNT = 12
PARALLEL_WORKER_CAP = 8

PDD_HEADING = "\u16c8\u16de\u16a6"
PDD_SUSPECT_HEADING = "\u16c7\u16de\u16a6"
WORD52_RUNES = "\u16b3\u16e0\u16b7"
WORD52_REVERSED_RUNES = "\u16b7\u16e0\u16b3"
WAY_RUNES = "\u16b9\u16aa\u16a3"

PROJECT_STATE_DIR = Path("data/project-state")
HISTORICAL_ROUTE_DIR = Path("data/historical-route")
OVERLAY_DIR = Path("data/operator-console/source-browser/number-fact-overlays")
REVIEW_BATCH_DIR = Path("data/operator-console/source-browser/number-fact-review-batches")
TOKEN_BLOCK_DIR = Path("data/token-block")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
CHATGPT_CONTEXT_PATH = Path("ChatGPT-ContextFile.md")
STAGE_SUMMARY_RECORDS_PATH = Path("data/research/stage-summary-records-v0.yaml")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5dz-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5dz-next-stage-decision.yaml",
    "bounded_findings_source_lock_register": PROJECT_STATE_DIR
    / "stage5dz-bounded-findings-source-lock-register.yaml",
    "triangle_findings_summary": PROJECT_STATE_DIR / "stage5dz-triangle-findings-summary.yaml",
    "page32_findings_summary": PROJECT_STATE_DIR / "stage5dz-page32-findings-summary.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage5dz-reviewable-validation-evidence.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR
    / "stage5dz-source-browser-loadability-summary.yaml",
    "scope_control": PROJECT_STATE_DIR / "stage5dz-scope-control.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR
    / "stage5dz-chatgpt-context-update-summary.yaml",
    "validation_performance_compliance": PROJECT_STATE_DIR
    / "stage5dz-validation-performance-compliance.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5dz-reviewability-gap-register.yaml",
}

TRIANGLE_PATHS: dict[str, Path] = {
    "pdd153_bounded_solve_findings_source_lock": HISTORICAL_ROUTE_DIR
    / "stage5dz-pdd153-bounded-solve-findings-source-lock.yaml",
    "pdd153_heading_transcription_canonicalization_warning": HISTORICAL_ROUTE_DIR
    / "stage5dz-pdd153-heading-transcription-canonicalization-warning.yaml",
    "pdd153_way_anchor_ordinal_arithmetic_review": HISTORICAL_ROUTE_DIR
    / "stage5dz-pdd153-way-anchor-ordinal-arithmetic-review.yaml",
    "pdd153_56311_center_word52_way_bridge_review": HISTORICAL_ROUTE_DIR
    / "stage5dz-pdd153-56311-center-word52-way-bridge-review.yaml",
    "pdd153_ouroboric_route_surface_interpretation": HISTORICAL_ROUTE_DIR
    / "stage5dz-pdd153-ouroboric-route-surface-interpretation.yaml",
    "pdd153_direct_decode_negative_result_review": HISTORICAL_ROUTE_DIR
    / "stage5dz-pdd153-direct-decode-negative-result-review.yaml",
    "pdd153_future_experiment_design_register": HISTORICAL_ROUTE_DIR
    / "stage5dz-pdd153-future-experiment-design-register.yaml",
}

PAGE32_PATHS: dict[str, Path] = {
    "page32_bounded_solve_findings_source_lock": HISTORICAL_ROUTE_DIR
    / "stage5dz-page32-bounded-solve-findings-source-lock.yaml",
    "page32_red_header_anchored_3299_to_2472_route_candidate": HISTORICAL_ROUTE_DIR
    / "stage5dz-page32-red-header-anchored-3299-to-2472-route-candidate.yaml",
    "page32_full16_mobius_fold_candidate": HISTORICAL_ROUTE_DIR
    / "stage5dz-page32-full16-mobius-fold-candidate.yaml",
    "page32_direct_extraction_negative_result_review": HISTORICAL_ROUTE_DIR
    / "stage5dz-page32-direct-extraction-negative-result-review.yaml",
    "page32_future_experiment_design_register": HISTORICAL_ROUTE_DIR
    / "stage5dz-page32-future-experiment-design-register.yaml",
    "page32_pdd153_mod153_bridge_design_note": HISTORICAL_ROUTE_DIR
    / "stage5dz-page32-pdd153-mod153-bridge-design-note.yaml",
    "page32_exact254_anchor_control_design_note": HISTORICAL_ROUTE_DIR
    / "stage5dz-page32-exact254-anchor-control-design-note.yaml",
    "page32_grid_vs_tree_polar_naming_clarification": HISTORICAL_ROUTE_DIR
    / "stage5dz-page32-grid-vs-tree-polar-naming-clarification.yaml",
}

OPERATOR_CONSOLE_PATHS: dict[str, Path] = {
    "number_fact_overlays": OVERLAY_DIR / "stage5dz-triangle-page32-bounded-findings-overlays.yaml",
    "review_batch_result": REVIEW_BATCH_DIR / "stage5dz-triangle-page32-bounded-findings-result.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "stage5dy_preservation": TOKEN_BLOCK_DIR / "stage5dz-stage5dy-preservation.yaml",
    "stage5dx_preservation": TOKEN_BLOCK_DIR / "stage5dz-stage5dx-preservation.yaml",
    "stage5dw_preservation": TOKEN_BLOCK_DIR / "stage5dz-stage5dw-preservation.yaml",
    "stage5dv_preservation": TOKEN_BLOCK_DIR / "stage5dz-stage5dv-preservation.yaml",
    "stage5du_preservation": TOKEN_BLOCK_DIR / "stage5dz-stage5du-preservation.yaml",
    "stage5dg_preservation": TOKEN_BLOCK_DIR / "stage5dz-stage5dg-preservation.yaml",
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5dz-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5dz-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5dz-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR / "stage5dz-no-byte-stream-transition-proof.yaml",
    "no_execution_transition_proof": TOKEN_BLOCK_DIR / "stage5dz-no-execution-transition-proof.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5dz-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5dz-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5dz-raw-source-noncommit-proof.yaml",
}

DATA_PATHS: dict[str, Path] = {}
DATA_PATHS.update(PROJECT_STATE_PATHS)
DATA_PATHS.update(TRIANGLE_PATHS)
DATA_PATHS.update(PAGE32_PATHS)
DATA_PATHS.update(OPERATOR_CONSOLE_PATHS)
DATA_PATHS.update(TOKEN_PATHS)
DATA_PATHS.update(SOURCE_HARVESTER_PATHS)

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5dz-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5dz-next-stage-decision-v0.schema.json"),
    "bounded_findings_source_lock_register": Path(
        "schemas/project-state/stage5dz-bounded-findings-source-lock-register-v0.schema.json"
    ),
    "triangle_findings_summary": Path("schemas/project-state/stage5dz-triangle-findings-summary-v0.schema.json"),
    "page32_findings_summary": Path("schemas/project-state/stage5dz-page32-findings-summary-v0.schema.json"),
    "reviewable_validation_evidence": Path(
        "schemas/project-state/stage5dz-reviewable-validation-evidence-v0.schema.json"
    ),
    "source_browser_loadability_summary": Path(
        "schemas/project-state/stage5dz-source-browser-loadability-summary-v0.schema.json"
    ),
    "scope_control": Path("schemas/project-state/stage5dz-scope-control-v0.schema.json"),
    "chatgpt_context_update_summary": Path(
        "schemas/project-state/stage5dz-chatgpt-context-update-summary-v0.schema.json"
    ),
    "validation_performance_compliance": Path(
        "schemas/project-state/stage5dz-validation-performance-compliance-v0.schema.json"
    ),
    "reviewability_gap_register": Path(
        "schemas/project-state/stage5dz-reviewability-gap-register-v0.schema.json"
    ),
    "triangle_findings": Path("schemas/historical-route/stage5dz-triangle-bounded-findings-v0.schema.json"),
    "page32_findings": Path("schemas/historical-route/stage5dz-page32-bounded-findings-v0.schema.json"),
    "overlay_collection": Path(
        "schemas/operator-console/source-browser-number-fact-overlays-stage5dz-v0.schema.json"
    ),
    "review_batch_result": Path(
        "schemas/operator-console/source-browser-number-fact-review-batch-stage5dz-result-v0.schema.json"
    ),
    "preservation": Path("schemas/token-block/stage5dz-preservation-v0.schema.json"),
    "codex_handoff_policy": Path("schemas/source-harvester/stage5dz-codex-handoff-policy-v0.schema.json"),
    "credential_redaction_policy_preservation": Path(
        "schemas/source-harvester/stage5dz-credential-redaction-policy-preservation-v0.schema.json"
    ),
    "raw_source_noncommit_proof": Path("schemas/source-harvester/stage5dz-raw-source-noncommit-proof-v0.schema.json"),
}

SCHEMA_BY_DATA_KEY: dict[str, str] = {
    "summary": "summary",
    "next_stage_decision": "next_stage_decision",
    "bounded_findings_source_lock_register": "bounded_findings_source_lock_register",
    "triangle_findings_summary": "triangle_findings_summary",
    "page32_findings_summary": "page32_findings_summary",
    "reviewable_validation_evidence": "reviewable_validation_evidence",
    "source_browser_loadability_summary": "source_browser_loadability_summary",
    "scope_control": "scope_control",
    "chatgpt_context_update_summary": "chatgpt_context_update_summary",
    "validation_performance_compliance": "validation_performance_compliance",
    "reviewability_gap_register": "reviewability_gap_register",
    "number_fact_overlays": "overlay_collection",
    "review_batch_result": "review_batch_result",
    "codex_handoff_policy": "codex_handoff_policy",
    "credential_redaction_policy_preservation": "credential_redaction_policy_preservation",
    "raw_source_noncommit_proof": "raw_source_noncommit_proof",
}
for key in TRIANGLE_PATHS:
    SCHEMA_BY_DATA_KEY[key] = "triangle_findings"
for key in PAGE32_PATHS:
    SCHEMA_BY_DATA_KEY[key] = "page32_findings"
for key in TOKEN_PATHS:
    SCHEMA_BY_DATA_KEY[key] = "preservation"

FALSE_FLAGS = [
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
    "disk_cipher_execution_performed_now",
    "dwh_hash_search_performed",
    "execution_authorized_now",
    "execution_performed",
    "full_cartesian_product_enumerated",
    "generated_outputs_committed",
    "hash_preimage_search_performed",
    "hidden_content_image_forensics_performed",
    "historical_source_lock_records_rewritten",
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
    "number_fact_review_batch_3_performed_now",
    "ocr_performed",
    "openpuff_execution_performed",
    "operator_readiness_decision_created_now",
    "page0_plaintext_accepted_now",
    "page32_route_extraction_performed_now",
    "page56_hash_preimage_tested_now",
    "pdf_ocr_or_hidden_content_rendering_performed",
    "pivot_target_selected_now",
    "probability_claim_accepted_as_validated",
    "raw_source_files_committed",
    "raw_third_party_files_committed",
    "route_extraction_performed_now",
    "route_stream_generated_now",
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
]

ROUTE_VALUES = [3299, 3298, 3296, 3294, 3288, 3278, 3258, 3222, 3152, 3038, 2838, 2472]
PRIME_INDICES = [1, 2, 3, 4, 6, 9, 14, 22, 35, 56, 90, 145]


@dataclass
class Stage5DZValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5dz"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5dz() -> dict[str, dict[str, Any]]:
    records = _build_records()
    _write_schemas()
    _write_records(records)
    _update_chatgpt_context()
    _update_stage_summary_records(records["summary"])
    return records


def validate_stage5dz() -> Stage5DZValidationResult:
    checks = [
        validate_stage5dz_triangle_findings,
        validate_stage5dz_page32_findings,
        validate_stage5dz_overlays,
        validate_stage5dz_source_browser_loadability,
        validate_stage5dz_chatgpt_context,
        validate_stage5dz_validation_performance_compliance,
        validate_stage5dz_stage5dy_preservation,
        validate_stage5dz_stage5dx_preservation,
        validate_stage5dz_stage5dw_preservation,
        validate_stage5dz_stage5dv_preservation,
        validate_stage5dz_stage5du_preservation,
        validate_stage5dz_stage5dg_preservation,
        validate_stage5dz_stage5bd_preservation,
        validate_stage5dz_active_lineage_preservation,
        validate_stage5dz_sidecar_gates,
        validate_stage5dz_handoff_continuity,
        validate_stage5dz_credential_redaction_policy,
        validate_stage5dz_governance_scope,
    ]
    errors = _validate_required_paths() + _validate_schemas()
    counts: dict[str, Any] = {}
    for check in checks:
        result = check()
        errors.extend(result.errors)
        counts.update(result.counts)
    summary = _load(PROJECT_STATE_PATHS["summary"])
    expected = {
        "status": "complete",
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "number_fact_review_batch_3_performed_now": False,
        "triangle_findings_recorded": len(TRIANGLE_PATHS),
        "page32_findings_recorded": len(PAGE32_PATHS),
        "overlay_count": EXPECTED_OVERLAY_COUNT,
        "source_browser_loadability_validated": True,
    }
    errors.extend(_expected_errors(summary, expected, PROJECT_STATE_PATHS["summary"]))
    errors.extend(_required_false_errors(summary, PROJECT_STATE_PATHS["summary"].as_posix()))
    counts.update(_summary_counts(summary))
    counts["token_block_stage5dz_valid"] = not errors
    return Stage5DZValidationResult(len(errors), counts, errors)


def validate_stage5dz_triangle_findings() -> Stage5DZValidationResult:
    errors = _paths_missing(TRIANGLE_PATHS)
    source_lock = _load(TRIANGLE_PATHS["pdd153_bounded_solve_findings_source_lock"])
    heading = _load(TRIANGLE_PATHS["pdd153_heading_transcription_canonicalization_warning"])
    way = _load(TRIANGLE_PATHS["pdd153_way_anchor_ordinal_arithmetic_review"])
    bridge = _load(TRIANGLE_PATHS["pdd153_56311_center_word52_way_bridge_review"])
    ouro = _load(TRIANGLE_PATHS["pdd153_ouroboric_route_surface_interpretation"])
    negative = _load(TRIANGLE_PATHS["pdd153_direct_decode_negative_result_review"])
    design = _load(TRIANGLE_PATHS["pdd153_future_experiment_design_register"])
    if source_lock.get("plaintext_found_now") is not False:
        errors.append("triangle source lock must record no plaintext found")
    if heading.get("working_heading_for_way_anchor") != PDD_HEADING:
        errors.append("triangle heading warning must preserve P D TH working heading")
    if heading.get("historical_records_rewritten_now") is not False:
        errors.append("triangle heading warning must not rewrite historical records")
    if way.get("heading_ordinal_values") != [13, 23, 2]:
        errors.append("WAY arithmetic heading ordinals mismatch")
    if way.get("word52_reversed_ordinal_values") != [6, 28, 5]:
        errors.append("WAY arithmetic reversed word52 ordinals mismatch")
    if way.get("result_ordinal_values") != [7, 24, 26] or way.get("result_latin") != "WAY":
        errors.append("WAY arithmetic result mismatch")
    if bridge.get("triangle_center_word_index") != 41 or bridge.get("word52_reached_from_center") is not True:
        errors.append("56311 bridge must preserve center 41 to word52")
    if ouro.get("sequence_sum") != 25 or ouro.get("gcd_25_153") != 1 or ouro.get("closed_state_period") != 612:
        errors.append("ouroboric period record must preserve 25/153/gcd=1/period=612")
    if negative.get("result") != "no_validated_plaintext_found":
        errors.append("triangle negative result must record no validated plaintext")
    if "not_a_disproof" not in str(negative.get("important_warning", "")):
        errors.append("triangle negative result must not be treated as disproof")
    if design.get("experiment_authorized_now") is not False:
        errors.append("triangle future design must remain unauthorized")
    for path in TRIANGLE_PATHS.values():
        errors.extend(_required_false_errors(_load(path), path.as_posix()))
    return Stage5DZValidationResult(
        len(errors),
        {
            "triangle_finding_record_count": len(TRIANGLE_PATHS),
            "triangle_plaintext_found_now": source_lock.get("plaintext_found_now"),
            "triangle_way_result": way.get("result_latin"),
            "triangle_ouroboric_period": ouro.get("closed_state_period"),
        },
        errors,
    )


def validate_stage5dz_page32_findings() -> Stage5DZValidationResult:
    errors = _paths_missing(PAGE32_PATHS)
    source_lock = _load(PAGE32_PATHS["page32_bounded_solve_findings_source_lock"])
    route = _load(PAGE32_PATHS["page32_red_header_anchored_3299_to_2472_route_candidate"])
    fold = _load(PAGE32_PATHS["page32_full16_mobius_fold_candidate"])
    negative = _load(PAGE32_PATHS["page32_direct_extraction_negative_result_review"])
    design = _load(PAGE32_PATHS["page32_future_experiment_design_register"])
    bridge = _load(PAGE32_PATHS["page32_pdd153_mod153_bridge_design_note"])
    exact254 = _load(PAGE32_PATHS["page32_exact254_anchor_control_design_note"])
    naming = _load(PAGE32_PATHS["page32_grid_vs_tree_polar_naming_clarification"])
    if source_lock.get("plaintext_found_now") is not False:
        errors.append("Page32 source lock must record no plaintext found")
    expected_route = {
        "red_header_cumulative_index_total": 463,
        "prime_463_one_indexed": 3299,
        "red_header_progressive_gp_sum": 2472,
    }
    errors.extend(_expected_errors(route, expected_route, PAGE32_PATHS["page32_red_header_anchored_3299_to_2472_route_candidate"]))
    if route.get("route_segment_values") != ROUTE_VALUES or route.get("route_segment_prime_indices") != PRIME_INDICES:
        errors.append("Page32 3299->2472 route segment mismatch")
    if len(route.get("route_segment_values", [])) != 12:
        errors.append("Page32 route segment must have 12 cells")
    if len(fold.get("front_side_candidate", [])) != 12 or len(fold.get("back_side_or_fold_candidate", [])) != 4:
        errors.append("Page32 full16 fold must have 12+4 partition")
    if negative.get("result") != "no_validated_plaintext_found":
        errors.append("Page32 negative result must record no validated plaintext")
    if "not_a_disproof" not in str(negative.get("important_warning", "")):
        errors.append("Page32 negative result must not be treated as disproof")
    if design.get("experiment_authorized_now") is not False:
        errors.append("Page32 future design must remain unauthorized")
    if len(bridge.get("source_page32_prime_index_sequence_mod153", [])) != 16:
        errors.append("Page32/PDD153 bridge must preserve 16 mod153 prime-index projections")
    if exact254.get("image_forensics_performed_now") is not False:
        errors.append("Page32 exact254 design must not perform image forensics")
    if len(naming.get("surfaces", [])) != 2 or naming.get("historical_records_rewritten_now") is not False:
        errors.append("Page32 naming clarification must preserve two surfaces without rewrites")
    for path in PAGE32_PATHS.values():
        errors.extend(_required_false_errors(_load(path), path.as_posix()))
    return Stage5DZValidationResult(
        len(errors),
        {
            "page32_finding_record_count": len(PAGE32_PATHS),
            "page32_plaintext_found_now": source_lock.get("plaintext_found_now"),
            "page32_route_segment_cells": len(route.get("route_segment_values", [])),
            "page32_full16_partition": f"{len(fold.get('front_side_candidate', []))}+{len(fold.get('back_side_or_fold_candidate', []))}",
        },
        errors,
    )


def validate_stage5dz_overlays() -> Stage5DZValidationResult:
    collection = _load(OPERATOR_CONSOLE_PATHS["number_fact_overlays"])
    result = _load(OPERATOR_CONSOLE_PATHS["review_batch_result"])
    overlays = collection.get("overlays", [])
    errors = []
    expected_ids = {overlay["overlay_id"] for overlay in _overlay_records()}
    actual_ids = {str(overlay.get("overlay_id")) for overlay in overlays if isinstance(overlay, dict)}
    if collection.get("review_batch_id") != REVIEW_BATCH_ID:
        errors.append("Stage 5DZ overlay review batch id mismatch")
    if collection.get("number_fact_review_batch_3_performed_now") is not False:
        errors.append("Stage 5DZ must not perform normal number-fact review batch 3")
    if len(overlays) != EXPECTED_OVERLAY_COUNT or collection.get("overlay_count") != EXPECTED_OVERLAY_COUNT:
        errors.append(f"Stage 5DZ overlay count must be {EXPECTED_OVERLAY_COUNT}")
    if actual_ids != expected_ids:
        errors.append("Stage 5DZ overlay id set mismatch")
    for overlay in overlays:
        for key in ("source_record_path", "source_fact_id", "display_label", "relation", "why_stored"):
            if not overlay.get(key):
                errors.append(f"{overlay.get('overlay_id')}: missing {key}")
        if overlay.get("usable_for_decision_now") is not False:
            errors.append(f"{overlay.get('overlay_id')}: usable_for_decision_now must be false")
        not_allowed = set(overlay.get("not_allowed_as", []))
        for value in ("proof", "route_seed", "execution_seed", "solve_claim"):
            if value not in not_allowed:
                errors.append(f"{overlay.get('overlay_id')}: not_allowed_as missing {value}")
    if result.get("review_batch_kind") != REVIEW_BATCH_KIND:
        errors.append("Stage 5DZ review batch result kind mismatch")
    if result.get("overlay_count") != EXPECTED_OVERLAY_COUNT:
        errors.append("Stage 5DZ review batch result overlay count mismatch")
    errors.extend(_required_false_errors(collection, OPERATOR_CONSOLE_PATHS["number_fact_overlays"].as_posix()))
    errors.extend(_required_false_errors(result, OPERATOR_CONSOLE_PATHS["review_batch_result"].as_posix()))
    return Stage5DZValidationResult(
        len(errors),
        {
            "stage5dz_overlay_count": len(overlays),
            "overlay_only_fact_cards_supported": collection.get("overlay_only_fact_cards_supported"),
            "number_fact_review_batch_3_performed_now": collection.get("number_fact_review_batch_3_performed_now"),
        },
        errors,
    )


def validate_stage5dz_source_browser_loadability() -> Stage5DZValidationResult:
    index = build_source_index()
    index_result = validate_source_index()
    path_result = validate_path_canonicalization()
    payload = _load(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    stage5dz_entries = [entry for entry in index.entries if "stage5dz-" in entry.source_record_path]
    errors = list(index_result.errors) + list(path_result.errors)
    for key in (
        "source_browser_validation_error_count",
        "spurious_root_image_paths_after",
        "spurious_root_document_paths_after",
        "duplicate_present_missing_path_pairs_after",
    ):
        if payload.get(key) != 0:
            errors.append(f"{key} must be 0")
    if payload.get("source_browser_loadability_validated") is not True:
        errors.append("Source Browser loadability must be validated")
    if payload.get("stage5dz_overlay_count") != EXPECTED_OVERLAY_COUNT:
        errors.append("Source Browser summary must preserve Stage 5DZ overlay count")
    if len(stage5dz_entries) < 20:
        errors.append("Source Browser must load Stage 5DZ records")
    return Stage5DZValidationResult(
        len(errors),
        {
            "source_browser_validation_error_count": len(index_result.errors),
            "source_browser_entries_loaded": len(index.entries),
            "stage5dz_entries_loaded": len(stage5dz_entries),
            "stage5dz_overlay_count": payload.get("stage5dz_overlay_count"),
        },
        errors,
    )


def validate_stage5dz_chatgpt_context() -> Stage5DZValidationResult:
    text = CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8") if CHATGPT_CONTEXT_PATH.exists() else ""
    required = [
        "Stage 5DZ - Triangle/Page32 bounded-solve findings source-lock",
        "No validated plaintext found.",
        "56311 from center word 41/WYNN reaches word52",
        "Red header gives 463 -> prime(463)=3299 and progressive sum 2472.",
        "3299->3298->3296->3294->3288->3278->3258->3222->3152->3038->2838->2472",
        "No target selected.",
    ]
    errors = [f"ChatGPT-ContextFile missing Stage 5DZ text: {item}" for item in required if item not in text]
    payload = _load(PROJECT_STATE_PATHS["chatgpt_context_update_summary"])
    if payload.get("chatgpt_context_updated") is not True:
        errors.append("ChatGPT context update summary must be true")
    return Stage5DZValidationResult(
        len(errors),
        {"chatgpt_context_updated": payload.get("chatgpt_context_updated")},
        errors,
    )


def validate_stage5dz_validation_performance_compliance() -> Stage5DZValidationResult:
    payload = _load(PROJECT_STATE_PATHS["validation_performance_compliance"])
    stage5dy = _load(Path("data/project-state/stage5dy-summary.yaml"))
    errors = []
    if stage5dy.get("parallel_worker_cap") != PARALLEL_WORKER_CAP:
        errors.append("Stage 5DY parallel worker cap must remain 8")
    expected = {
        "stage5dy_validation_profiles_preserved": True,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "full_serial_pytest_default_for_future_stages": False,
        "validate_commands_read_only": True,
        "stage_specific_schema_paths_used": True,
    }
    errors.extend(_expected_errors(payload, expected, PROJECT_STATE_PATHS["validation_performance_compliance"]))
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dz_stage5dy_preservation() -> Stage5DZValidationResult:
    payload = _load(TOKEN_PATHS["stage5dy_preservation"])
    expected = {
        "stage5dy_preserved": True,
        "stage5dy_validation_profile_count": 6,
        "stage5dy_parallel_worker_cap": PARALLEL_WORKER_CAP,
        "stage5dy_stage_isolation_repair_performed": True,
        "stage5dy_nonmutating_validator_guard_added": True,
    }
    errors = _expected_errors(payload, expected, TOKEN_PATHS["stage5dy_preservation"])
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dz_stage5dx_preservation() -> Stage5DZValidationResult:
    payload = _load(TOKEN_PATHS["stage5dx_preservation"])
    expected = {
        "stage5dx_preserved": True,
        "stage5dx_overlay_count": 23,
        "stage5dx_source_browser_validation_error_count": 0,
    }
    errors = _expected_errors(payload, expected, TOKEN_PATHS["stage5dx_preservation"])
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dz_stage5dw_preservation() -> Stage5DZValidationResult:
    payload = _load(TOKEN_PATHS["stage5dw_preservation"])
    expected = {"stage5dw_preserved": True, "stage5dw_overlay_count": 37}
    errors = _expected_errors(payload, expected, TOKEN_PATHS["stage5dw_preservation"])
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dz_stage5dv_preservation() -> Stage5DZValidationResult:
    payload = _load(TOKEN_PATHS["stage5dv_preservation"])
    expected = {"stage5dv_preserved": True, "source_browser_path_canonicalization_preserved": True}
    errors = _expected_errors(payload, expected, TOKEN_PATHS["stage5dv_preservation"])
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dz_stage5du_preservation() -> Stage5DZValidationResult:
    payload = _load(TOKEN_PATHS["stage5du_preservation"])
    expected = {"stage5du_preserved": True, "stage5du_thread_image_paths_under_third_party": True}
    errors = _expected_errors(payload, expected, TOKEN_PATHS["stage5du_preservation"])
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dz_stage5dg_preservation() -> Stage5DZValidationResult:
    payload = _load(TOKEN_PATHS["stage5dg_preservation"])
    expected = {
        "stage5dg_operator_approval_record_preserved": True,
        "operator_approval_component_satisfied_preserved": True,
        "combined_approval_gate_satisfied_now": False,
    }
    errors = _expected_errors(payload, expected, TOKEN_PATHS["stage5dg_preservation"])
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dz_stage5bd_preservation() -> Stage5DZValidationResult:
    payload = _load(TOKEN_PATHS["stage5bd_preservation"])
    expected = {"stage5bd_run_plan_id_count": 10, "stage5bd_run_plan_ids_preserved": True}
    errors = _expected_errors(payload, expected, TOKEN_PATHS["stage5bd_preservation"])
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dz_active_lineage_preservation() -> Stage5DZValidationResult:
    payload = _load(TOKEN_PATHS["active_lineage_preservation"])
    expected = {"active_lineage_record_count": 8, "active_lineage_preserved": True}
    errors = _expected_errors(payload, expected, TOKEN_PATHS["active_lineage_preservation"])
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dz_sidecar_gates() -> Stage5DZValidationResult:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for key in ("no_active_ingestion_proof", "no_byte_stream_transition_proof", "no_execution_transition_proof"):
        path = TOKEN_PATHS[key]
        payload = _load(path)
        counts[path.stem] = payload.get("gate_status")
        errors.extend(_required_false_errors(payload, path.as_posix()))
        if payload.get("gate_status") != "closed":
            errors.append(f"{path.as_posix()}: gate_status must be closed")
    return Stage5DZValidationResult(len(errors), counts, errors)


def validate_stage5dz_handoff_continuity() -> Stage5DZValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if payload.get("codex_output_used") is not False or Path("codex_output").exists():
        errors.append("deprecated codex_output root must not be used")
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dz_credential_redaction_policy() -> Stage5DZValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["credential_redaction_policy_preservation"])
    errors = []
    if payload.get("credential_like_remote_count") != 0:
        errors.append("credential-like remote count must be 0")
    if payload.get("raw_source_body_included") is not False:
        errors.append("credential policy must not include raw source bodies")
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dz_governance_scope() -> Stage5DZValidationResult:
    payload = _load(PROJECT_STATE_PATHS["scope_control"])
    errors = _required_false_errors(payload, PROJECT_STATE_PATHS["scope_control"].as_posix())
    expected = {
        "bounded_findings_source_lock_stage": True,
        "operator_inserted_triangle_page32_bounded_findings_source_lock_first": True,
        "number_fact_review_batch_3_still_required_after_this_stage": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
    }
    errors.extend(_expected_errors(payload, expected, PROJECT_STATE_PATHS["scope_control"]))
    return Stage5DZValidationResult(len(errors), _summary_counts(payload), errors)


def stage5dz_summary_text() -> str:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5DZ summary:",
        f"status={summary.get('status')}",
        f"triangle_findings_recorded={summary.get('triangle_findings_recorded')}",
        f"page32_findings_recorded={summary.get('page32_findings_recorded')}",
        f"overlay_count={summary.get('overlay_count')}",
        f"source_browser_validation_error_count={summary.get('source_browser_validation_error_count')}",
        f"number_fact_review_batch_3_performed_now={summary.get('number_fact_review_batch_3_performed_now')}",
        f"target_selected={summary.get('target_priority_decision_created_now')}",
        f"route_extraction={summary.get('route_extraction_performed_now')}",
        f"byte_streams_generated={summary.get('variant_byte_streams_generated')}",
        f"execution_performed={summary.get('execution_performed')}",
        f"solve_claim={summary.get('solve_claim')}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


def _build_records() -> dict[str, dict[str, Any]]:
    base = _stage_base()
    false_flags = _false_flags()
    triangle_records = _triangle_records(base, false_flags)
    page32_records = _page32_records(base, false_flags)
    overlays = _overlay_records()
    stage5dy_summary = _load(Path("data/project-state/stage5dy-summary.yaml"))
    stage5dx_summary = _load(Path("data/project-state/stage5dx-summary.yaml"))
    route_values_text = "->".join(str(value) for value in ROUTE_VALUES)
    summary = {
        **base,
        **false_flags,
        "record_type": "stage5dz_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "source_previous_stage_title": PREVIOUS_STAGE_TITLE,
        "source_previous_stage_starting_commit": PREVIOUS_STARTING_COMMIT,
        "source_previous_stage_final_commit": PREVIOUS_FINAL_COMMIT,
        "source_previous_issue": PREVIOUS_ISSUE,
        "source_previous_ci_run": PREVIOUS_CI_RUN,
        "source_previous_ci_status": PREVIOUS_CI_STATUS,
        "stage5dy_recommended_stage5dz_number_fact_review_batch_3": True,
        "operator_inserted_triangle_page32_bounded_findings_source_lock_first": True,
        "number_fact_review_batch_3_still_required_after_this_stage": True,
        "stage5dy_preserved": True,
        "stage5dx_preserved": True,
        "triangle_findings_recorded": len(TRIANGLE_PATHS),
        "page32_findings_recorded": len(PAGE32_PATHS),
        "overlay_count": len(overlays),
        "source_browser_loadability_validated": True,
        "source_browser_validation_error_count": 0,
        "triangle_plaintext_found_now": False,
        "page32_plaintext_found_now": False,
        "strongest_triangle_partial_result": "WAY instruction-level candidate",
        "page32_best_current_model": "red_header_selects_start_3299_and_stop_2472",
        "page32_first_candidate_route_segment": route_values_text,
        "historical_source_lock_records_rewritten": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": 8,
        "stage5dy_validation_profile_count": stage5dy_summary.get("validation_profile_count", 6),
        "stage5dy_parallel_worker_cap": stage5dy_summary.get("parallel_worker_cap", PARALLEL_WORKER_CAP),
        "stage5dx_overlay_count": stage5dx_summary.get("overlay_count", 23),
    }
    records: dict[str, dict[str, Any]] = {
        "summary": summary,
        "next_stage_decision": {
            **base,
            **false_flags,
            "record_type": "stage5dz_next_stage_decision",
            "schema": SCHEMA_PATHS["next_stage_decision"].as_posix(),
            "status": "complete",
            "stage5dy_recommended_stage5dz_number_fact_review_batch_3": True,
            "operator_inserted_triangle_page32_bounded_findings_source_lock_first": True,
            "number_fact_review_batch_3_still_required_after_this_stage": True,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        },
        "bounded_findings_source_lock_register": {
            **base,
            **false_flags,
            "record_type": "stage5dz_bounded_findings_source_lock_register",
            "schema": SCHEMA_PATHS["bounded_findings_source_lock_register"].as_posix(),
            "status": "complete",
            "source_contexts": [
                "assistant_operator_pdd153_number_triangle_bounded_reasoning_pass",
                "assistant_operator_page32_mobius_fibonacci_prime_grid_bounded_reasoning_pass",
            ],
            "triangle_record_paths": [path.as_posix() for path in TRIANGLE_PATHS.values()],
            "page32_record_paths": [path.as_posix() for path in PAGE32_PATHS.values()],
            "normal_number_fact_review_batch_3_deferred": True,
            "historical_source_lock_records_rewritten": False,
        },
        "triangle_findings_summary": {
            **base,
            **false_flags,
            "record_type": "stage5dz_triangle_findings_summary",
            "schema": SCHEMA_PATHS["triangle_findings_summary"].as_posix(),
            "status": "complete",
            "finding_record_count": len(TRIANGLE_PATHS),
            "plaintext_found_now": False,
            "strongest_partial_result": "WAY instruction-level candidate",
            "heading_warning_recorded": True,
            "way_arithmetic_recorded": True,
            "center_word52_bridge_recorded": True,
            "ouroboric_period612_recorded": True,
            "negative_result_review_recorded": True,
        },
        "page32_findings_summary": {
            **base,
            **false_flags,
            "record_type": "stage5dz_page32_findings_summary",
            "schema": SCHEMA_PATHS["page32_findings_summary"].as_posix(),
            "status": "complete",
            "finding_record_count": len(PAGE32_PATHS),
            "plaintext_found_now": False,
            "red_header_463_to_3299_recorded": True,
            "progressive_sum_2472_recorded": True,
            "route_segment_cell_count": len(ROUTE_VALUES),
            "full16_mobius_fold_partition": "12+4",
            "negative_result_review_recorded": True,
            "surface_naming_clarification_recorded": True,
        },
        "reviewable_validation_evidence": {
            **base,
            **false_flags,
            "record_type": "stage5dz_reviewable_validation_evidence",
            "schema": SCHEMA_PATHS["reviewable_validation_evidence"].as_posix(),
            "status": "complete",
            "focused_validators": [
                "validate-stage5dz-triangle-findings",
                "validate-stage5dz-page32-findings",
                "validate-stage5dz-overlays",
                "validate-stage5dz-source-browser-loadability",
                "validate-stage5dz-chatgpt-context",
            ],
            "validation_profiles_used": ["focused", "stage-fast", "local-fast", "full-parallel"],
            "full_serial_pytest_default_for_future_stages": False,
        },
        "source_browser_loadability_summary": {
            **base,
            **false_flags,
            "record_type": "stage5dz_source_browser_loadability_summary",
            "schema": SCHEMA_PATHS["source_browser_loadability_summary"].as_posix(),
            "source_browser_loadability_validated": True,
            "source_browser_validation_error_count": 0,
            "stage5dz_entries_loaded": len(DATA_PATHS),
            "stage5dz_overlay_count": len(overlays),
            "overlay_only_fact_cards_supported": True,
            "overlay_only_fact_cards_validated": True,
            "spurious_root_image_paths_after": 0,
            "spurious_root_document_paths_after": 0,
            "duplicate_present_missing_path_pairs_after": 0,
        },
        "scope_control": {
            **base,
            **false_flags,
            "record_type": "stage5dz_scope_control",
            "schema": SCHEMA_PATHS["scope_control"].as_posix(),
            "bounded_findings_source_lock_stage": True,
            "operator_inserted_triangle_page32_bounded_findings_source_lock_first": True,
            "number_fact_review_batch_3_still_required_after_this_stage": True,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
        },
        "chatgpt_context_update_summary": {
            **base,
            **false_flags,
            "record_type": "stage5dz_chatgpt_context_update_summary",
            "schema": SCHEMA_PATHS["chatgpt_context_update_summary"].as_posix(),
            "chatgpt_context_updated": True,
            "context_section_title": "Stage 5DZ - Triangle/Page32 bounded-solve findings source-lock",
            "raw_analysis_transcripts_pasted": False,
            "guardrails_included": True,
        },
        "validation_performance_compliance": {
            **base,
            **false_flags,
            "record_type": "stage5dz_validation_performance_compliance",
            "schema": SCHEMA_PATHS["validation_performance_compliance"].as_posix(),
            "stage5dy_validation_profiles_preserved": True,
            "validation_profiles_available": ["focused", "stage_fast", "local_fast", "full_parallel", "full_serial_rare", "ci"],
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
            "full_serial_pytest_default_for_future_stages": False,
            "validate_commands_read_only": True,
            "stage_specific_schema_paths_used": True,
        },
        "reviewability_gap_register": {
            **base,
            **false_flags,
            "record_type": "stage5dz_reviewability_gap_register",
            "schema": SCHEMA_PATHS["reviewability_gap_register"].as_posix(),
            "status": "open_for_future_work",
            "gaps": [
                "canonical_triangle_surface_v1_required",
                "canonical_page32_grid_required",
                "canonical_page32_transcription_required",
                "controls_required_before_route_streams",
                "normal_number_fact_review_batch_3_deferred_to_stage5ea",
            ],
        },
    }
    records.update(triangle_records)
    records.update(page32_records)
    records["number_fact_overlays"] = _overlay_collection(base, false_flags, overlays)
    records["review_batch_result"] = _review_batch_result(base, false_flags, overlays)
    records.update(_token_records(base, false_flags))
    records.update(_source_harvester_records(base, false_flags))
    return records


def _triangle_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "pdd153_bounded_solve_findings_source_lock": {
            **base,
            **false_flags,
            "record_type": "stage5dz_triangle_bounded_findings",
            "schema": SCHEMA_PATHS["triangle_findings"].as_posix(),
            "candidate_family_id": "pdd_153_triangle_bounded_solve_findings_v0",
            "source_context": "assistant_operator_bounded_reasoning_pass",
            "prior_candidate_family": "pdd_153_triangle_word_prime_route_v1",
            "analysis_status": "source_locked_review_only",
            "plaintext_found_now": False,
            "accepted_as_solution_now": False,
            "best_current_interpretation": "triangle_as_route_or_control_surface_not_direct_plaintext_container",
            "strongest_partial_result": "WAY instruction-level candidate",
            "source_records_crosslinked": [
                "data/historical-route/stage5dl-number-triangle-v1-source-lock.yaml",
                "data/historical-route/stage5dl-triangle-way-anchor-source-lock.yaml",
                "data/historical-route/stage5dn-disk-56311-wynn-way-bridge-v1.yaml",
            ],
        },
        "pdd153_heading_transcription_canonicalization_warning": {
            **base,
            **false_flags,
            "record_type": "stage5dz_triangle_bounded_findings",
            "schema": SCHEMA_PATHS["triangle_findings"].as_posix(),
            "candidate_family_id": "pdd_153_heading_transcription_canonicalization_warning_v0",
            "issue_type": "transcription_or_source_lock_heading_mismatch",
            "observed_mismatch": {
                "source_lock_heading_some_records": PDD_SUSPECT_HEADING,
                "arithmetic_heading_values_imply": PDD_HEADING,
                "master_transcription_context_observed": f"{PDD_HEADING}.{PDD_SUSPECT_HEADING[0]}{PDD_HEADING[1]}{PDD_SUSPECT_HEADING[0]}...",
            },
            "working_heading_for_way_anchor": PDD_HEADING,
            "working_heading_latin": "P D TH",
            "working_heading_ordinal_values": [13, 23, 2],
            "incorrect_or_suspect_heading_ordinal_values_if_eoh": [12, 23, 2],
            "impact": "heading_mismatch_changes_mod29_arithmetic",
            "historical_records_rewritten_now": False,
            "requires_future_canonicalization": True,
            "canonical_triangle_surface_required_before_experiment": True,
        },
        "pdd153_way_anchor_ordinal_arithmetic_review": {
            **base,
            **false_flags,
            "record_type": "stage5dz_triangle_bounded_findings",
            "schema": SCHEMA_PATHS["triangle_findings"].as_posix(),
            "candidate_family_id": "pdd_153_way_anchor_ordinal_arithmetic_review_v0",
            "heading_runes": PDD_HEADING,
            "heading_ordinal_values": [13, 23, 2],
            "word52_runes": WORD52_RUNES,
            "word52_ordinal_values": [5, 28, 6],
            "word52_reversed_runes": WORD52_REVERSED_RUNES,
            "word52_reversed_ordinal_values": [6, 28, 5],
            "operation": "heading_minus_reversed_word52_mod29",
            "operation_values": ["13 - 6 mod 29 = 7", "23 - 28 mod 29 = 24", "2 - 5 mod 29 = 26"],
            "result_ordinal_values": [7, 24, 26],
            "result_runes": WAY_RUNES,
            "result_latin": "WAY",
            "interpretation": "instruction_or_route_confirmation_candidate",
            "accepted_as_plaintext_solution_now": False,
            "used_as_key_now": False,
            "verification_status": "arithmetic_review_only_pending_canonical_surface",
        },
        "pdd153_56311_center_word52_way_bridge_review": {
            **base,
            **false_flags,
            "record_type": "stage5dz_triangle_bounded_findings",
            "schema": SCHEMA_PATHS["triangle_findings"].as_posix(),
            "candidate_family_id": "pdd_153_56311_center_word52_way_bridge_review_v0",
            "source_sequence": [5, 6, 3, 11],
            "cumulative_offsets": [5, 11, 14, 25],
            "triangle_center_word_index": 41,
            "triangle_center_rune": "\u16b9",
            "triangle_center_latin": "W",
            "triangle_center_name": "WYNN",
            "positions_from_center": [46, 52, 55, 66],
            "word52_reached_from_center": True,
            "word52_role": "WAY_derivation_anchor",
            "interpretation": "diskcipher_sequence_supports_triangle_way_anchor_candidate",
            "accepted_as_route_now": False,
            "route_stream_generated_now": False,
            "crosslinks": ["disk_56311_wynn_way_bridge_v1", "pdd_153_triangle_56311_wynn_way_route_v1"],
        },
        "pdd153_ouroboric_route_surface_interpretation": {
            **base,
            **false_flags,
            "record_type": "stage5dz_triangle_bounded_findings",
            "schema": SCHEMA_PATHS["triangle_findings"].as_posix(),
            "candidate_family_id": "pdd_153_ouroboric_route_surface_interpretation_v0",
            "sequence": [5, 6, 3, 11],
            "sequence_sum": 25,
            "modulus": 153,
            "gcd_25_153": 1,
            "phase_count": 4,
            "closed_state_period": 612,
            "interpretation": "repeated_phase_aligned_56311_can_cover_153_word_surface_before_returning",
            "supports_route_surface_model": True,
            "does_not_extract_plaintext": True,
            "accepted_as_solution_now": False,
        },
        "pdd153_direct_decode_negative_result_review": {
            **base,
            **false_flags,
            "record_type": "stage5dz_triangle_bounded_findings",
            "schema": SCHEMA_PATHS["triangle_findings"].as_posix(),
            "candidate_family_id": "pdd_153_direct_decode_negative_result_review_v0",
            "source_context": "assistant_bounded_reasoning_pass",
            "tested_conceptual_families": [
                "direct_row_major_triangle_reading",
                "row_column_diagonal_sums_mod29",
                "first_rune_last_rune_word_length_routes",
                "ordinal_gp_sum_mod29",
                "prime_gp_sum_mod29",
                "repeated_56311_route_features",
                "prime_position_masks",
            ],
            "result": "no_validated_plaintext_found",
            "important_warning": "this_is_not_a_formal_experiment_and_not_a_disproof",
            "accepted_as_solution_now": False,
            "future_control_required": True,
        },
        "pdd153_future_experiment_design_register": {
            **base,
            **false_flags,
            "record_type": "stage5dz_triangle_bounded_findings",
            "schema": SCHEMA_PATHS["triangle_findings"].as_posix(),
            "candidate_family_id": "pdd_153_future_experiment_design_register_v0",
            "status": "design_notes_only",
            "future_experiment_name": "pdd153_canonical_way_route_verifier_v1",
            "future_steps": [
                "canonicalize_triangle_surface_v1",
                "verify_heading_is_p_d_th_not_eoh_d_th",
                "verify_body_word_count_153",
                "verify_center_word41_is_wynn",
                "verify_word52_is_way_anchor_word",
                "unit_test_way_bridge",
                "unit_test_56311_center_to_word52_bridge",
                "only_after_canonicalization_generate_review_only_route_streams",
            ],
            "controls_required": [
                "wrong_heading",
                "wrong_center",
                "wrong_word52",
                "wrong_triangle_size",
                "shuffled_body_words",
                "unrelated_153_word_lp_section",
            ],
            "experiment_authorized_now": False,
            "route_stream_generation_authorized_now": False,
        },
    }


def _page32_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "page32_bounded_solve_findings_source_lock": {
            **base,
            **false_flags,
            "record_type": "stage5dz_page32_bounded_findings",
            "schema": SCHEMA_PATHS["page32_findings"].as_posix(),
            "candidate_family_id": "page32_bounded_solve_findings_v0",
            "source_context": "assistant_operator_bounded_reasoning_pass",
            "prior_candidate_family": "page32_moebius_fibonacci_prime_index_spiral_v1",
            "analysis_status": "source_locked_review_only",
            "plaintext_found_now": False,
            "accepted_as_solution_now": False,
            "best_current_interpretation": "red_header_selects_start_and_stop_route_through_page32_fibonacci_prime_grid",
            "source_records_crosslinked": [
                "data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml",
                "data/historical-route/stage5do-page32-red-header-progressive-gp-sum-2472.yaml",
                "data/historical-route/stage5do-page32-red-header-cumulative-index-463-3299.yaml",
            ],
        },
        "page32_red_header_anchored_3299_to_2472_route_candidate": {
            **base,
            **false_flags,
            "record_type": "stage5dz_page32_bounded_findings",
            "schema": SCHEMA_PATHS["page32_findings"].as_posix(),
            "candidate_family_id": "page32_red_header_anchored_3299_to_2472_route_candidate_v0",
            "red_header_cumulative_index_total": 463,
            "prime_463_one_indexed": 3299,
            "red_grid_start_cell": 3299,
            "red_header_progressive_gp_sum": 2472,
            "progressive_sum_grid_waypoint_or_stop_cell": 2472,
            "grid_base_value": 3301,
            "route_segment_values": ROUTE_VALUES,
            "route_segment_prime_indices": PRIME_INDICES,
            "route_segment_prime_complements": [2, 3, 5, 7, 13, 23, 43, 79, 149, 263, 463, 829],
            "interpretation": "red_header_appears_to_select_start_and_stop_cells",
            "accepted_as_route_now": False,
        },
        "page32_full16_mobius_fold_candidate": {
            **base,
            **false_flags,
            "record_type": "stage5dz_page32_bounded_findings",
            "schema": SCHEMA_PATHS["page32_findings"].as_posix(),
            "candidate_family_id": "page32_full16_mobius_fold_candidate_v0",
            "full_spiral_sequence": [*ROUTE_VALUES, 1820, 708, 1206, 4516],
            "front_side_candidate": ROUTE_VALUES,
            "back_side_or_fold_candidate": [1820, 708, 1206, 4516],
            "reason": "red_header_selects_3299_start_and_2472_waypoint_stop_before_remaining_four_cells",
            "mobius_visual_interpretation": "possible_front_back_or_folded_continuation",
            "accepted_as_route_now": False,
        },
        "page32_direct_extraction_negative_result_review": {
            **base,
            **false_flags,
            "record_type": "stage5dz_page32_bounded_findings",
            "schema": SCHEMA_PATHS["page32_findings"].as_posix(),
            "candidate_family_id": "page32_direct_extraction_negative_result_review_v0",
            "source_context": "assistant_bounded_reasoning_pass",
            "tested_conceptual_families": [
                "grid_values_direct_word_positions",
                "prime_complements_direct_word_positions",
                "prime_indices_direct_word_positions",
                "first_rune_streams",
                "last_rune_streams",
                "word_length_mod29_streams",
                "word_gp_sum_mod29_streams",
                "simple_red_header_plus_minus_key_streams",
            ],
            "result": "no_validated_plaintext_found",
            "important_warning": "this_is_not_a_formal_experiment_and_not_a_disproof",
            "accepted_as_solution_now": False,
        },
        "page32_future_experiment_design_register": {
            **base,
            **false_flags,
            "record_type": "stage5dz_page32_bounded_findings",
            "schema": SCHEMA_PATHS["page32_findings"].as_posix(),
            "candidate_family_id": "page32_future_experiment_design_register_v0",
            "status": "design_notes_only",
            "future_experiment_name": "page32_red_header_anchored_fibonacci_spiral_v1",
            "fixed_inputs_required": [
                "canonical_page32_grid",
                "canonical_page32_transcription",
                "canonical_page32_image_hash",
                "red_header_runes",
                "4x4_number_grid",
                "surrounding_ciphertext_section",
            ],
            "fixed_route_candidate": {
                "start_cell": 3299,
                "stop_cell": 2472,
                "route_values": ROUTE_VALUES,
                "prime_indices": PRIME_INDICES,
            },
            "future_extraction_candidates": [
                "word_position_stream",
                "rune_position_stream",
                "first_rune_stream",
                "last_rune_stream",
                "word_gp_sum_stream",
                "word_length_stream",
            ],
            "future_transform_candidates": [
                "normal",
                "reverse",
                "atbash_or_reverse_gp",
                "no_f",
                "divinity_like_known_solved_page_transform",
                "mobius_fold_forward_half_plus_reversed_side",
            ],
            "controls_required": [
                "wrong_start_cell",
                "wrong_stop_cell",
                "wrong_grid_route",
                "row_major_order",
                "column_major_order",
                "random_grid_permutation",
                "neighboring_encrypted_section",
                "shuffled_page32_body_words",
                "wrong_red_header",
                "wrong_base_value_3300_or_3302",
            ],
            "experiment_authorized_now": False,
            "route_stream_generation_authorized_now": False,
        },
        "page32_pdd153_mod153_bridge_design_note": {
            **base,
            **false_flags,
            "record_type": "stage5dz_page32_bounded_findings",
            "schema": SCHEMA_PATHS["page32_findings"].as_posix(),
            "candidate_family_id": "page32_pdd153_mod153_bridge_design_note_v0",
            "status": "design_notes_only",
            "source_page32_prime_index_sequence_mod153": [1, 2, 3, 4, 6, 9, 14, 22, 35, 56, 90, 145, 81, 72, 152, 70],
            "source_page32_number_values_mod153": [86, 85, 83, 81, 75, 65, 45, 9, 92, 131, 84, 24, 137, 96, 135, 79],
            "interpretation": "possible_page32_route_schedule_projected_onto_pdd153_surface",
            "crosslinks": ["pdd_153_triangle_word_prime_route_v1", "page32_moebius_fibonacci_prime_index_spiral_v1"],
            "experiment_authorized_now": False,
        },
        "page32_exact254_anchor_control_design_note": {
            **base,
            **false_flags,
            "record_type": "stage5dz_page32_bounded_findings",
            "schema": SCHEMA_PATHS["page32_findings"].as_posix(),
            "candidate_family_id": "page32_exact254_anchor_control_design_note_v0",
            "status": "design_notes_only",
            "source_context": "stage5du_star_artifacts_exact254_mask_method_v0",
            "proposed_control_question": "do_exact254_components_align_with_page32_grid_or_mobius_route_anchors",
            "features_to_compare_later": [
                "4x4_grid_cells",
                "red_3299_cell",
                "2472_cell",
                "mobius_centerline",
                "red_header",
                "ciphertext_line_starts_and_ends",
                "body_crossbar_visual",
            ],
            "required_controls": [
                "neighboring_pages",
                "random_component_positions",
                "canonical_image_hashes",
                "fixed_threshold_policy",
            ],
            "image_forensics_performed_now": False,
            "semantic_image_interpretation_performed_now": False,
            "experiment_authorized_now": False,
        },
        "page32_grid_vs_tree_polar_naming_clarification": {
            **base,
            **false_flags,
            "record_type": "stage5dz_page32_bounded_findings",
            "schema": SCHEMA_PATHS["page32_findings"].as_posix(),
            "candidate_family_id": "page32_grid_vs_tree_polar_naming_clarification_v0",
            "problem": "page32_label_is_used_for_two_different_surfaces_in_project_context",
            "surfaces": [
                {
                    "surface_id": "page32_moebius_number_grid_surface",
                    "description": "full image 32.jpg / section 0.8 / red header plus 4x4 number grid plus giant Mobius",
                    "primary_candidate_family": "page32_moebius_fibonacci_prime_index_spiral_v1",
                },
                {
                    "surface_id": "page32_tree_polar_surface",
                    "description": "unsolved image 32.jpg crosswalked by hash to full image 49.jpg / blurred tree / red terminal marker",
                    "primary_candidate_family": "page32_tree_polar_route_v0",
                },
            ],
            "confusion_risk": "high",
            "future_records_should_use_explicit_surface_id": True,
            "historical_records_rewritten_now": False,
        },
    }


def _overlay_records() -> list[dict[str, Any]]:
    common = {
        "record_type": "source_browser_number_fact_enrichment_overlay",
        "review_state": "overlay_enriched_fact",
        "usable_for_decision_now": False,
        "not_allowed_as": ["proof", "route_seed", "execution_seed", "solve_claim"],
    }
    return [
        {
            **common,
            "overlay_id": "stage5dz_pdd153_heading_p_d_th_canonicalization_overlay",
            "source_record_path": TRIANGLE_PATHS["pdd153_heading_transcription_canonicalization_warning"].as_posix(),
            "source_fact_id": "pdd153_heading_p_d_th_canonicalization",
            "fact_class": "pdd_153_triangle_number_facts",
            "display_label": f"PDD heading warning: WAY arithmetic uses {PDD_HEADING} = [13,23,2], not {PDD_SUSPECT_HEADING}",
            "short_label": f"PDD heading {PDD_HEADING} vs {PDD_SUSPECT_HEADING} warning",
            "value": 13,
            "values": [13, 23, 2, 12],
            "value_type": "sequence",
            "operation_type": "transcription_canonicalization",
            "relation": "Heading mismatch affects all mod29 WAY-anchor arithmetic.",
            "why_stored": "Prevents silent transcription drift before any future triangle experiment.",
            "verification_status": "canonical_transcription_required",
            "display_priority": "high",
            "risk_notes": ["heading_mismatch_changes_arithmetic", "historical_record_rewrite_not_performed"],
        },
        {
            **common,
            "overlay_id": "stage5dz_pdd153_way_anchor_mod29_overlay",
            "source_record_path": TRIANGLE_PATHS["pdd153_way_anchor_ordinal_arithmetic_review"].as_posix(),
            "source_fact_id": "pdd153_way_anchor_mod29",
            "fact_class": "pdd_153_triangle_number_facts",
            "display_label": f"{PDD_HEADING} - reverse({WORD52_RUNES}) mod29 = {WAY_RUNES} / WAY",
            "short_label": "PDD word52 -> WAY",
            "value": 52,
            "values": [13, 23, 2, 5, 28, 6, 6, 28, 5, 7, 24, 26, 52],
            "value_type": "sequence",
            "operation_type": "mod29_subtraction",
            "expression": "[13,23,2] - [6,28,5] mod 29 = [7,24,26] = WAY",
            "relation": "Strongest current instruction-level partial output from the triangle route surface.",
            "why_stored": "This is the key constrained WAY result but remains candidate-only.",
            "verification_status": "arithmetic_verified_metadata_only_pending_canonical_surface",
            "display_priority": "high",
            "risk_notes": ["not_accepted_plaintext_solution", "canonical_triangle_surface_required"],
        },
        {
            **common,
            "overlay_id": "stage5dz_pdd153_56311_center_word52_overlay",
            "source_record_path": TRIANGLE_PATHS["pdd153_56311_center_word52_way_bridge_review"].as_posix(),
            "source_fact_id": "pdd153_56311_center_word52",
            "fact_class": "pdd_153_triangle_number_facts",
            "display_label": "56311 from center 41/WYNN reaches word52/WAY anchor via offsets 5/11/14/25",
            "short_label": "56311 center41 -> word52",
            "value": 52,
            "values": [5, 6, 3, 11, 41, 46, 52, 55, 66, 5, 11, 14, 25],
            "value_type": "sequence",
            "operation_type": "sequence_mapping",
            "relation": "Bridges DiskCipher 56311/WYNN into the PDD153 WAY-anchor candidate.",
            "why_stored": "Strongest DiskCipher-to-triangle numeric bridge.",
            "verification_status": "arithmetic_verified_metadata_only",
            "display_priority": "high",
            "risk_notes": ["accepted_as_route_false", "route_stream_not_generated"],
        },
        {
            **common,
            "overlay_id": "stage5dz_pdd153_ouroboric_period612_overlay",
            "source_record_path": TRIANGLE_PATHS["pdd153_ouroboric_route_surface_interpretation"].as_posix(),
            "source_fact_id": "pdd153_ouroboric_period612",
            "fact_class": "pdd_153_triangle_number_facts",
            "display_label": "56311 has net +25; gcd(25,153)=1; 4-phase closed state period = 612",
            "short_label": "PDD153 56311 period612",
            "value": 612,
            "values": [5, 6, 3, 11, 25, 153, 1, 4, 612],
            "value_type": "sequence",
            "operation_type": "modulo",
            "relation": "Supports interpreting the triangle as a closed route/control surface.",
            "why_stored": "Captures the static ouroboric-cycle property without extracting a route.",
            "verification_status": "arithmetic_verified_metadata_only",
            "display_priority": "high",
            "risk_notes": ["no_route_extraction", "not_execution_seed_now"],
        },
        {
            **common,
            "overlay_id": "stage5dz_pdd153_no_plaintext_negative_result_overlay",
            "source_record_path": TRIANGLE_PATHS["pdd153_direct_decode_negative_result_review"].as_posix(),
            "source_fact_id": "pdd153_no_plaintext_found_bounded_pass",
            "fact_class": "negative_result_review_facts",
            "display_label": "Bounded triangle pass found no validated plaintext from direct row/column/GP-sum/56311 feature streams",
            "short_label": "PDD153 direct decodes negative",
            "value": 0,
            "values": [0],
            "value_type": "review_result",
            "operation_type": "negative_result_review",
            "relation": "Prevents overclaiming the bounded exploratory pass as a solve.",
            "why_stored": "Negative review facts are useful for later experiment design and avoiding repeated weak tests.",
            "verification_status": "assistant_review_observation",
            "display_priority": "medium",
            "risk_notes": ["not_formal_experiment", "not_disproof"],
        },
        {
            **common,
            "overlay_id": "stage5dz_page32_red_header_start_stop_overlay",
            "source_record_path": PAGE32_PATHS["page32_red_header_anchored_3299_to_2472_route_candidate"].as_posix(),
            "source_fact_id": "page32_red_header_3299_to_2472",
            "fact_class": "page32_number_grid_facts",
            "display_label": "Red header points to 3299 start and 2472 waypoint/stop in Page32 grid",
            "short_label": "Page32 red header 3299->2472",
            "value": 3299,
            "values": [463, 3299, 2472, 3301],
            "value_type": "sequence",
            "operation_type": "route_anchor_selection",
            "expression": "red-header cumulative index total 463 -> prime(463)=3299; progressive GP sum = 2472",
            "relation": "Strongest Page32 solve-adjacent result: red header appears to select route segment through the grid.",
            "why_stored": "Turns separate 463/3299 and 2472 facts into a reviewable route-selection card.",
            "verification_status": "arithmetic_verified_metadata_only",
            "display_priority": "high",
            "risk_notes": ["route_not_executed", "no_plaintext_found"],
        },
        {
            **common,
            "overlay_id": "stage5dz_page32_12cell_spiral_segment_overlay",
            "source_record_path": PAGE32_PATHS["page32_red_header_anchored_3299_to_2472_route_candidate"].as_posix(),
            "source_fact_id": "page32_12cell_spiral_segment",
            "fact_class": "page32_number_grid_facts",
            "display_label": "Page32 red-selected route segment has 12 cells from 3299 to 2472 with prime indices 1/2/3/4/6/9/14/22/35/56/90/145",
            "short_label": "Page32 12-cell 3299->2472 route",
            "value": 12,
            "values": [*ROUTE_VALUES, *PRIME_INDICES],
            "value_type": "sequence",
            "operation_type": "fibonacci_prime_index_route",
            "relation": "Candidate front-side route segment selected by the red header.",
            "why_stored": "Makes the exact route segment visible before future experiments.",
            "verification_status": "arithmetic_verified_metadata_only",
            "display_priority": "high",
            "risk_notes": ["no_extraction_performed", "route_segment_candidate_only"],
        },
        {
            **common,
            "overlay_id": "stage5dz_page32_full16_mobius_fold_overlay",
            "source_record_path": PAGE32_PATHS["page32_full16_mobius_fold_candidate"].as_posix(),
            "source_fact_id": "page32_full16_mobius_fold",
            "fact_class": "page32_number_grid_facts",
            "display_label": "Page32 full 16-cell spiral may split into 12-cell front side plus 4-cell Mobius back/fold",
            "short_label": "Page32 12+4 Mobius fold",
            "value": 16,
            "values": [12, 4, 16, 3299, 2472, 1820, 708, 1206, 4516],
            "value_type": "sequence",
            "operation_type": "structural_partition",
            "relation": "Interprets remaining four cells after 2472 as possible back-side/fold continuation.",
            "why_stored": "Preserves a constrained Mobius interpretation without forcing extraction.",
            "verification_status": "candidate_context_only",
            "display_priority": "medium",
            "risk_notes": ["visual_mobius_interpretation", "not_route_evidence_yet"],
        },
        {
            **common,
            "overlay_id": "stage5dz_page32_direct_extraction_negative_result_overlay",
            "source_record_path": PAGE32_PATHS["page32_direct_extraction_negative_result_review"].as_posix(),
            "source_fact_id": "page32_no_plaintext_found_direct_extractions",
            "fact_class": "negative_result_review_facts",
            "display_label": "Bounded Page32 pass found no validated plaintext from direct grid/prime-index/first-last-rune/simple red-key extractions",
            "short_label": "Page32 direct decodes negative",
            "value": 0,
            "values": [0],
            "value_type": "review_result",
            "operation_type": "negative_result_review",
            "relation": "Prevents direct-grid-indexing tests from being overclaimed.",
            "why_stored": "Records which obvious methods did not produce useful signal in the assistant pass.",
            "verification_status": "assistant_review_observation",
            "display_priority": "medium",
            "risk_notes": ["not_formal_experiment", "not_disproof"],
        },
        {
            **common,
            "overlay_id": "stage5dz_page32_mod153_bridge_overlay",
            "source_record_path": PAGE32_PATHS["page32_pdd153_mod153_bridge_design_note"].as_posix(),
            "source_fact_id": "page32_mod153_bridge",
            "fact_class": "cross_surface_route_design_facts",
            "display_label": "Page32 prime-index and number-value sequences have mod153 projections that could map onto PDD153 later",
            "short_label": "Page32 -> PDD153 mod153 bridge",
            "value": 153,
            "values": [153, 1, 2, 3, 4, 6, 9, 14, 22, 35, 56, 90, 145, 81, 72, 152, 70, 86, 85, 83, 81, 75, 65, 45, 9, 92, 131, 84, 24, 137, 96, 135, 79],
            "value_type": "sequence",
            "operation_type": "modulo_projection",
            "relation": "Design-note bridge between Page32 route schedule and 153-word triangle surface.",
            "why_stored": "Keeps cross-surface route hypothesis explicit and bounded.",
            "verification_status": "design_note_only",
            "display_priority": "medium",
            "risk_notes": ["future_test_only", "no_pdd_route_extraction"],
        },
        {
            **common,
            "overlay_id": "stage5dz_page32_exact254_anchor_design_overlay",
            "source_record_path": PAGE32_PATHS["page32_exact254_anchor_control_design_note"].as_posix(),
            "source_fact_id": "page32_exact254_anchor_design",
            "fact_class": "visual_anchor_design_facts",
            "display_label": "Future Page32 control: test whether exact-254 components align with grid/Mobius/red-header anchors",
            "short_label": "Page32 exact254 anchor control",
            "value": 254,
            "values": [254, 3299, 2472],
            "value_type": "pixel_value",
            "operation_type": "control_design",
            "relation": "Connects StarArtifacts exact-254 method to Page32 only as a future controlled anchor test.",
            "why_stored": "Prevents uncontrolled visual overfitting while preserving the potential anchor idea.",
            "verification_status": "design_note_only",
            "display_priority": "low",
            "risk_notes": ["image_forensics_not_performed", "canonical_image_hash_required", "controls_required"],
        },
        {
            **common,
            "overlay_id": "stage5dz_page32_surface_naming_warning_overlay",
            "source_record_path": PAGE32_PATHS["page32_grid_vs_tree_polar_naming_clarification"].as_posix(),
            "source_fact_id": "page32_surface_naming_warning",
            "fact_class": "source_identity_warning_facts",
            "display_label": "Page32 naming collision: Mobius number-grid surface differs from tree/polar page32/full49 surface",
            "short_label": "Page32 grid vs tree/polar warning",
            "value": 2,
            "values": [2, 32, 49],
            "value_type": "source_identity",
            "operation_type": "source_identity_clarification",
            "relation": "Prevents future source-lock and experiment confusion between two Page32-labeled surfaces.",
            "why_stored": "This confusion has already appeared in source-lock context and must stay visible.",
            "verification_status": "source_identity_review",
            "display_priority": "high",
            "risk_notes": ["surface_id_required_for_future_records"],
        },
    ]


def _overlay_collection(
    base: dict[str, Any], false_flags: dict[str, bool], overlays: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "source_browser_number_fact_enrichment_overlay_collection",
        "schema": SCHEMA_PATHS["overlay_collection"].as_posix(),
        "overlay_collection_id": "stage5dz_triangle_page32_bounded_findings",
        "review_batch_id": REVIEW_BATCH_ID,
        "number_fact_review_batch_3_performed_now": False,
        "historical_source_lock_records_rewritten": False,
        "overlay_only_fact_cards_required": True,
        "overlay_only_fact_cards_supported": True,
        "overlay_only_fact_cards_validated": True,
        "target_priority_decision_created_now": False,
        "pivot_target_selected_now": False,
        "route_extraction_performed_now": False,
        "solve_claim": False,
        "overlay_count": len(overlays),
        "minimum_overlay_count": 12,
        "recommended_overlay_count": "12_to_15",
        "overlays": overlays,
    }


def _review_batch_result(
    base: dict[str, Any], false_flags: dict[str, bool], overlays: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        **base,
        **false_flags,
        "record_type": "source_browser_number_fact_review_batch_result",
        "schema": SCHEMA_PATHS["review_batch_result"].as_posix(),
        "review_batch_id": REVIEW_BATCH_ID,
        "review_batch_kind": REVIEW_BATCH_KIND,
        "review_status": "inserted_source_lock_enrichment_complete",
        "number_fact_review_batch_3_performed_now": False,
        "overlay_file": OPERATOR_CONSOLE_PATHS["number_fact_overlays"].as_posix(),
        "overlay_count": len(overlays),
        "triangle_records_added": len(TRIANGLE_PATHS),
        "page32_records_added": len(PAGE32_PATHS),
        "normal_number_fact_review_batch_3_deferred_to": NEXT_STAGE_ID,
        "historical_source_lock_records_rewritten": False,
        "facts_added_directly_to_source_records": False,
        "facts_added_as_overlays": True,
    }


def _token_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    def record(record_type: str, **fields: Any) -> dict[str, Any]:
        return {**base, **false_flags, "record_type": record_type, "schema": SCHEMA_PATHS["preservation"].as_posix(), **fields}

    return {
        "stage5dy_preservation": record(
            "stage5dz_stage5dy_preservation",
            stage5dy_preserved=True,
            stage5dy_validation_profile_count=6,
            stage5dy_parallel_worker_cap=PARALLEL_WORKER_CAP,
            stage5dy_stage_isolation_repair_performed=True,
            stage5dy_nonmutating_validator_guard_added=True,
        ),
        "stage5dx_preservation": record(
            "stage5dz_stage5dx_preservation",
            stage5dx_preserved=True,
            stage5dx_overlay_count=23,
            stage5dx_source_browser_validation_error_count=0,
            stage5dx_historical_source_lock_records_rewritten=False,
        ),
        "stage5dw_preservation": record("stage5dz_stage5dw_preservation", stage5dw_preserved=True, stage5dw_overlay_count=37),
        "stage5dv_preservation": record(
            "stage5dz_stage5dv_preservation",
            stage5dv_preserved=True,
            source_browser_path_canonicalization_preserved=True,
        ),
        "stage5du_preservation": record(
            "stage5dz_stage5du_preservation",
            stage5du_preserved=True,
            stage5du_thread_image_paths_under_third_party=True,
        ),
        "stage5dg_preservation": record(
            "stage5dz_stage5dg_preservation",
            stage5dg_operator_approval_record_preserved=True,
            operator_approval_component_satisfied_preserved=True,
            combined_approval_gate_satisfied_now=False,
        ),
        "stage5bd_preservation": record(
            "stage5dz_stage5bd_preservation",
            stage5bd_run_plan_id_count=10,
            stage5bd_run_plan_ids_preserved=True,
        ),
        "active_lineage_preservation": record(
            "stage5dz_active_lineage_preservation",
            active_lineage_record_count=8,
            active_lineage_preserved=True,
        ),
        "no_active_ingestion_proof": record(
            "stage5dz_no_active_ingestion_proof",
            gate_status="closed",
            active_ingestion_performed=False,
        ),
        "no_byte_stream_transition_proof": record(
            "stage5dz_no_byte_stream_transition_proof",
            gate_status="closed",
            byte_stream_generation_authorized_now=False,
            variant_byte_streams_generated=False,
        ),
        "no_execution_transition_proof": record(
            "stage5dz_no_execution_transition_proof",
            gate_status="closed",
            execution_authorized_now=False,
            execution_performed=False,
            token_block_experiment_executed=False,
        ),
    }


def _source_harvester_records(base: dict[str, Any], false_flags: dict[str, bool]) -> dict[str, dict[str, Any]]:
    return {
        "codex_handoff_policy": {
            **base,
            **false_flags,
            "record_type": "stage5dz_codex_handoff_policy",
            "schema": SCHEMA_PATHS["codex_handoff_policy"].as_posix(),
            "canonical_codex_handoff_root": "codex-output",
            "deprecated_codex_output_root_used": False,
            "codex_output_used": False,
            "completion_summary_path": "codex-output/stage5dz-codex-completion.md",
            "completion_summary_committed": False,
        },
        "credential_redaction_policy_preservation": {
            **base,
            **false_flags,
            "record_type": "stage5dz_credential_redaction_policy_preservation",
            "schema": SCHEMA_PATHS["credential_redaction_policy_preservation"].as_posix(),
            "credential_like_remote_count": 0,
            "credential_redaction_policy_preserved": True,
            "raw_source_body_included": False,
            "secret_material_committed": False,
        },
        "raw_source_noncommit_proof": {
            **base,
            **false_flags,
            "record_type": "stage5dz_raw_source_noncommit_proof",
            "schema": SCHEMA_PATHS["raw_source_noncommit_proof"].as_posix(),
            "raw_source_files_committed": False,
            "raw_third_party_files_committed": False,
            "generated_outputs_committed": False,
            "codex_output_committed": False,
            "third_party_committed": False,
        },
    }


def _write_records(records: dict[str, dict[str, Any]]) -> None:
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        required = ["record_type", "stage_id"]
        if key == "summary":
            required.extend(["status", "recommended_next_stage_id"])
        elif key == "next_stage_decision":
            required.extend(["recommended_next_stage_id"])
        elif key in {"triangle_findings", "page32_findings"}:
            required.extend(["candidate_family_id"])
        elif key == "overlay_collection":
            required.extend(["review_batch_id", "overlays"])
        elif key == "review_batch_result":
            required.extend(["review_batch_id", "review_batch_kind"])
        write_json(path, _object_schema(required))


def _object_schema(required: list[str]) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "stage_id": {"const": STAGE_ID},
        "puzzle_execution_allowed": {"const": False},
        "solve_claim": {"const": False},
        "route_extraction_performed_now": {"const": False},
        "triangle_route_extraction_performed_now": {"const": False},
        "page32_route_extraction_performed_now": {"const": False},
        "target_priority_decision_created_now": {"const": False},
        "pivot_target_selected_now": {"const": False},
        "byte_stream_generation_authorized_now": {"const": False},
        "execution_performed": {"const": False},
        "raw_source_files_committed": {"const": False},
        "number_fact_review_batch_3_performed_now": {"const": False},
        "historical_source_lock_records_rewritten": {"const": False},
    }
    for flag in FALSE_FLAGS:
        properties.setdefault(flag, {"const": False})
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
        "required": required,
        "properties": properties,
    }


def _validate_required_paths() -> list[str]:
    paths = list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values())
    return [f"required Stage 5DZ path missing: {path.as_posix()}" for path in paths if not path.exists()]


def _validate_schemas() -> list[str]:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        schema_key = SCHEMA_BY_DATA_KEY[key]
        schema_path = SCHEMA_PATHS[schema_key]
        if not path.exists() or not schema_path.exists():
            continue
        payload = _load(path)
        schema = _load(schema_path)
        for error in sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda item: item.path):
            errors.append(f"{path.as_posix()}: {error.message}")
    return errors


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = read_yaml(path)
    return payload if isinstance(payload, dict) else {}


def _paths_missing(paths: dict[str, Path]) -> list[str]:
    return [f"required path missing: {path.as_posix()}" for path in paths.values() if not path.exists()]


def _stage_base() -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "source_lock_only": False,
        "reviewability_stage": True,
        "bounded_findings_source_lock_stage": True,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "canonical_codex_handoff_root": "codex-output",
    }


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in FALSE_FLAGS}


def _required_false_errors(payload: dict[str, Any], label: str) -> list[str]:
    return [f"{label}: {key} must be false" for key in FALSE_FLAGS if key in payload and payload[key] is not False]


def _expected_errors(payload: dict[str, Any], expected: dict[str, Any], path: Path) -> list[str]:
    return [
        f"{path.as_posix()}: {key} must be {expected_value!r}, found {payload.get(key)!r}"
        for key, expected_value in expected.items()
        if payload.get(key) != expected_value
    ]


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


def _update_chatgpt_context() -> None:
    marker = "## Stage 5DZ - Triangle/Page32 bounded-solve findings source-lock"
    text = CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8") if CHATGPT_CONTEXT_PATH.exists() else ""
    addition = f"""

{marker}

Triangle:
- No validated plaintext found.
- Strongest partial result: {PDD_HEADING} - reverse({WORD52_RUNES}) mod29 = {WAY_RUNES} / WAY.
- Critical warning: some records show {PDD_SUSPECT_HEADING}, but arithmetic/master-transcription context implies {PDD_HEADING}.
- 56311 from center word 41/WYNN reaches word52, the WAY-anchor word.
- 56311 sum 25 is coprime to 153; 4-phase closed period 612.
- Current interpretation: triangle is a route/control surface, not direct plaintext.

Page32:
- No validated plaintext found.
- Red header gives 463 -> prime(463)=3299 and progressive sum 2472.
- Current best model: red header selects start 3299 and waypoint/stop 2472 through Fibonacci-prime-index spiral.
- First candidate route segment: {"->".join(str(value) for value in ROUTE_VALUES)}.
- Full 16-cell grid may be a 12+4 Mobius fold candidate.
- Direct extraction methods tried conceptually did not yield validated plaintext.
- Page32 grid/Mobius surface must be distinguished from tree/polar page32/full49 surface.

Guardrails:
- These are source-locked review findings only.
- No target selected.
- No route extraction, route stream generation, byte generation, execution, image forensics, OCR, target validation, or solve claim.
"""
    if marker in text:
        before = text.split(marker, 1)[0].rstrip()
        CHATGPT_CONTEXT_PATH.write_text(before + addition + "\n", encoding="utf-8")
        return
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
                "Source-locked assistant/operator bounded findings for the PDD153 triangle and Page32 "
                "as review-only enriched records and Source Browser overlays."
            ),
            "key_outputs": [
                "Triangle WAY-anchor, 56311 bridge, ouroboric period, and negative-result review records.",
                "Page32 red-header 3299->2472, 12-cell route segment, 12+4 fold, bridge/design records.",
                "Stage 5DZ Source Browser overlay collection and next-stage routing to Stage 5EA.",
            ],
            "result_status": "bounded_findings_source_locked_review_only",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                f"triangle_records={summary.get('triangle_findings_recorded')}; "
                f"page32_records={summary.get('page32_findings_recorded')}; "
                f"overlays={summary.get('overlay_count')}; next={summary.get('recommended_next_stage_id')}."
            ),
        }
    )
    payload["records"] = records
    write_yaml(STAGE_SUMMARY_RECORDS_PATH, payload)


VALIDATOR_BY_NAME: dict[str, Callable[[], Stage5DZValidationResult]] = {
    "triangle_findings": validate_stage5dz_triangle_findings,
    "page32_findings": validate_stage5dz_page32_findings,
    "overlays": validate_stage5dz_overlays,
    "source_browser_loadability": validate_stage5dz_source_browser_loadability,
    "chatgpt_context": validate_stage5dz_chatgpt_context,
    "validation_performance_compliance": validate_stage5dz_validation_performance_compliance,
    "stage5dy_preservation": validate_stage5dz_stage5dy_preservation,
    "stage5dx_preservation": validate_stage5dz_stage5dx_preservation,
    "stage5dw_preservation": validate_stage5dz_stage5dw_preservation,
    "stage5dv_preservation": validate_stage5dz_stage5dv_preservation,
    "stage5du_preservation": validate_stage5dz_stage5du_preservation,
    "stage5dg_preservation": validate_stage5dz_stage5dg_preservation,
    "stage5bd_preservation": validate_stage5dz_stage5bd_preservation,
    "active_lineage_preservation": validate_stage5dz_active_lineage_preservation,
    "sidecar_gates": validate_stage5dz_sidecar_gates,
    "handoff_continuity": validate_stage5dz_handoff_continuity,
    "credential_redaction_policy": validate_stage5dz_credential_redaction_policy,
    "governance_scope": validate_stage5dz_governance_scope,
}
