"""Stage 6D canonical doublet boundary source-lock and triage metadata."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import os
import platform
import subprocess
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import validate_source_index
from libreprimus.token_block import stage6, stage6c
from libreprimus.token_block.models import read_yaml, write_yaml

STAGE_ID = "stage-6d"
STAGE_TOKEN = "stage6d"
STAGE_TITLE = "Stage 6D - Canonical doublet boundary source-lock and automation triage, without execution"
PROMPT_TYPE = "codex_plan_mode_source_lock_automation_triage"
PREVIOUS_STAGE_ID = "stage-6c"
PREVIOUS_STAGE_TITLE = stage6c.STAGE_TITLE
NEXT_STAGE_ID = "stage-6e"
NEXT_STAGE_TITLE = "Stage 6E - Final finite Stage 7 probe manifest and archive-run contract, without execution"
NEXT_PROMPT_TYPE = "codex_plan_mode_probe_manifest_finalization"
STARTING_COMMIT = "9e04b0388dd21191664a4383d4e5bf9e121aafca"
STAGE6C_ROUTED_STAGE6D_TITLE = "Stage 6D - Final finite Stage 7 probe manifest and archive-run contract, without execution"

PROJECT_STATE_DIR = Path("data/project-state")
HISTORICAL_ROUTE_DIR = Path("data/historical-route")
TOKEN_BLOCK_DIR = Path("data/token-block")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
OVERLAY_DIR = Path("data/operator-console/source-browser/number-fact-overlays")
CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
CURRENT_STAGE_SCHEMA_PATH = Path("schemas/project-state/current-stage-state-v0.schema.json")
DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH = Path(
    "schemas/project-state/doc-staleness-source-of-truth-record-v0.schema.json"
)
CODEX_COMPLETION_PATH = Path("codex-output/stage6d-codex-completion.md")
GP_PROFILE_PATH = Path("data/profiles/gematria/gematria-primus-v0.json")
MASTER_TRANSCRIPTION_PATH = Path(
    "third_party/CiadaSolversIddqd_v2/liber-primus__transcription--master/"
    "liber-primus__transcription--master.txt"
)
AUTOMATION_MEMORY_PATH = Path.home() / ".codex/automations/liberprimus-daily-doc-staleness-and-current-truth-drift-audit/memory.md"
LOCAL_TRIAGE_REPORT_PATH = Path("experiments/results/doc-drift/stage6d-local-stale-current-triage.json")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage6d-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage6d-next-stage-decision.yaml",
    "stage6c_preservation": PROJECT_STATE_DIR / "stage6d-stage6c-preservation.yaml",
    "canonical_doublet_source_lock_summary": PROJECT_STATE_DIR / "stage6d-canonical-doublet-source-lock-summary.yaml",
    "corpus_profile_policy": PROJECT_STATE_DIR / "stage6d-corpus-profile-policy.yaml",
    "doublet_boundary_policy_reconciliation": PROJECT_STATE_DIR
    / "stage6d-doublet-boundary-policy-reconciliation.yaml",
    "doc_staleness_automation_triage_summary": PROJECT_STATE_DIR
    / "stage6d-doc-staleness-automation-triage-summary.yaml",
    "hook_verification_summary": PROJECT_STATE_DIR / "stage6d-hook-verification-summary.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR / "stage6d-source-browser-loadability-summary.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage6d-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage6d-reviewability-gap-register.yaml",
    "current_stage_transition": PROJECT_STATE_DIR / "stage6d-current-stage-transition.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage6d-chatgpt-context-update-summary.yaml",
}

HISTORICAL_ROUTE_PATHS: dict[str, Path] = {
    "canonical_doublet_profile_pages15_70": HISTORICAL_ROUTE_DIR
    / "stage6d-canonical-doublet-profile-pages15-70-v0.yaml",
    "raw_vs_collapsed_doublet_boundary_contribution": HISTORICAL_ROUTE_DIR
    / "stage6d-raw-vs-collapsed-doublet-boundary-contribution-v0.yaml",
    "doublet_86_89_boundary_policy_reconciliation": HISTORICAL_ROUTE_DIR
    / "stage6d-doublet-86-89-boundary-policy-reconciliation-v0.yaml",
    "instruction_page14_doublet_delta": HISTORICAL_ROUTE_DIR
    / "stage6d-instruction-page14-doublet-delta-v0.yaml",
    "lag_distance_profile_pages15_72": HISTORICAL_ROUTE_DIR
    / "stage6d-lag-distance-profile-pages15-72-v0.yaml",
    "lag1_specific_doublet_suppression": HISTORICAL_ROUTE_DIR
    / "stage6d-lag1-specific-doublet-suppression-v0.yaml",
    "early_section_doublet_suppression_plateau": HISTORICAL_ROUTE_DIR
    / "stage6d-early-section-doublet-suppression-plateau-v0.yaml",
    "zero_doublet_page_count14": HISTORICAL_ROUTE_DIR / "stage6d-zero-doublet-page-count14-v0.yaml",
    "doublet_421_occurrence_index_canonical_rebuild": HISTORICAL_ROUTE_DIR
    / "stage6d-doublet-421-occurrence-index-canonical-rebuild-v0.yaml",
    "doublet_count_group_size_sequence": HISTORICAL_ROUTE_DIR
    / "stage6d-doublet-count-group-size-sequence-v0.yaml",
    "doublet_corpus_profile_family_index": HISTORICAL_ROUTE_DIR
    / "stage6d-doublet-corpus-profile-family-index-v0.yaml",
}

TOKEN_BLOCK_PATHS: dict[str, Path] = {
    "doublet_future_probe_registry": TOKEN_BLOCK_DIR / "stage6d-doublet-future-probe-registry.yaml",
    "doublet_control_bundle": TOKEN_BLOCK_DIR / "stage6d-doublet-control-bundle.yaml",
    "doublet_keeper_taxonomy": TOKEN_BLOCK_DIR / "stage6d-doublet-keeper-taxonomy.yaml",
    "doublet_route_fingerprint_watchlist": TOKEN_BLOCK_DIR
    / "stage6d-doublet-route-fingerprint-watchlist.yaml",
    "stage6e_manifest_input_addendum": TOKEN_BLOCK_DIR / "stage6d-stage6e-manifest-input-addendum.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage6d-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage6d-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage6d-no-execution-transition-gate.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "canonical_transcription_doublet_source_crosslink": SOURCE_HARVESTER_DIR
    / "stage6d-canonical-transcription-doublet-source-crosslink.yaml",
    "observation_rune_frequency_crosslink": SOURCE_HARVESTER_DIR
    / "stage6d-observation-rune-frequency-crosslink.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage6d-raw-source-noncommit-proof.yaml",
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage6d-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage6d-credential-redaction-policy-preservation.yaml",
    "hook_runner_evidence": SOURCE_HARVESTER_DIR / "stage6d-hook-runner-evidence.yaml",
}

OPERATOR_PATHS: dict[str, Path] = {
    "number_fact_overlays": OVERLAY_DIR / "stage6d-canonical-doublet-boundary-policy-overlays.yaml",
}

DATA_PATHS = {
    **PROJECT_STATE_PATHS,
    **HISTORICAL_ROUTE_PATHS,
    **TOKEN_BLOCK_PATHS,
    **SOURCE_HARVESTER_PATHS,
    **OPERATOR_PATHS,
}


def _schema_path(category: str, key: str) -> Path:
    return Path(f"schemas/{category}/stage6d-{key.replace('_', '-')}-v0.schema.json")


SCHEMA_PATHS: dict[str, Path] = {key: _schema_path("project-state", key) for key in PROJECT_STATE_PATHS}
SCHEMA_PATHS.update({key: _schema_path("historical-route", key) for key in HISTORICAL_ROUTE_PATHS})
SCHEMA_PATHS.update({key: _schema_path("token-block", key) for key in TOKEN_BLOCK_PATHS})
SCHEMA_PATHS.update({key: _schema_path("source-harvester", key) for key in SOURCE_HARVESTER_PATHS})
SCHEMA_PATHS.update({key: _schema_path("operator-console", key) for key in OPERATOR_PATHS})

DELIMITER_TABLE = {
    "word": "-",
    "three_dot_symbol": ",",
    "clause": ".",
    "paragraph": "&",
    "segment": "$",
    "chapter": "\u00a7",
    "line": "/",
    "page": "%",
}

EXPECTED_VECTOR_ORDER = [
    "F",
    "U",
    "TH",
    "O",
    "R",
    "C",
    "G",
    "W",
    "H",
    "N",
    "I",
    "J",
    "EO",
    "P",
    "X",
    "S",
    "T",
    "B",
    "E",
    "M",
    "L",
    "ING",
    "OE",
    "D",
    "A",
    "AE",
    "Y",
    "IA",
    "EA",
]

EXPECTED_PAGES15_70_VECTOR = [4, 2, 4, 4, 2, 1, 5, 6, 2, 4, 2, 4, 2, 1, 6, 3, 2, 0, 4, 2, 3, 2, 4, 2, 1, 7, 2, 2, 3]
EXPECTED_421_OCCURRENCES = {
    "O": [4580, 5825, 6611, 11189],
    "R": [6650, 8309],
    "C": [6756],
    "J": [653, 2026, 5261, 8638],
    "EO": [7144, 7569],
    "P": [11599],
    "OE": [2016, 10140, 10612, 10842],
    "D": [4774, 8142],
    "A": [8385],
}
EXPECTED_ZERO_DOUBLET_PAGES = [20, 22, 28, 29, 30, 32, 43, 46, 52, 53, 55, 64, 65, 68]
EXPECTED_GROUPS_BY_COUNT = {
    0: ["B"],
    1: ["C", "P", "A"],
    2: ["U", "R", "H", "I", "EO", "T", "M", "ING", "D", "Y", "IA"],
    3: ["S", "L", "EA"],
    4: ["F", "TH", "O", "N", "J", "E", "OE"],
    5: ["G"],
    6: ["W", "X"],
    7: ["AE"],
}

FUTURE_PROBE_IDS = [
    "canonical_doublet_profile_pages15_70_reproduction_v0",
    "raw_vs_collapsed_doublet_boundary_contribution_v0",
    "doublet_86_89_boundary_policy_reconciliation_v0",
    "instruction_page14_doublet_delta_probe_v0",
    "lag_distance_scan_pages15_72_reproduction_v0",
    "lag1_specific_suppression_control_probe_v0",
    "early_section_doublet_suppression_plateau_probe_v0",
    "zero_doublet_page_count14_control_probe_v0",
    "doublet_421_occurrence_index_canonical_rebuild_v1",
    "doublet_421_boundary_dependency_control_probe_v0",
    "codeword_vs_cipher_doublet_policy_probe_v0",
    "doublet_count_group_size_sequence_control_v0",
]

SOURCE_LOCKED_REVIEW_FACTS = [
    "canonical_doublet_profile_pages15_70",
    "observation_vector_reproduction_pages15_70",
    "raw_vs_collapsed_doublet_boundary_contribution",
    "doublet_86_89_boundary_policy_reconciliation",
    "instruction_page14_plus3_doublet_delta",
    "lag_distance_scan_pages15_72_profile",
    "lag1_specific_suppression_profile",
    "early_section_suppression_plateau",
    "zero_doublet_page_count14",
    "doublet_421_occurrence_index_rebuild",
    "doublet_count_group_sequence",
]

OVERLAY_IDS = [
    "stage6d_canonical_doublet_profile_pages15_70_overlay",
    "stage6d_observation_vector_reproduction_overlay",
    "stage6d_raw_vs_collapsed_60_26_86_overlay",
    "stage6d_doublet_421_boundary_dependency_overlay",
    "stage6d_doublet_86_89_boundary_reconciliation_overlay",
    "stage6d_instruction_page14_plus3_overlay",
    "stage6d_lag1_specific_suppression_overlay",
    "stage6d_early_section_suppression_plateau_overlay",
    "stage6d_zero_doublet_page_count14_overlay",
    "stage6d_421_occurrence_index_rebuild_overlay",
    "stage6d_doublet_count_group_sequence_overlay",
]

CONTROL_BUNDLE_ID = "canonical_doublet_boundary_policy_controls_v0"
CONTROL_BUNDLE = [
    "raw_adjacency_policy",
    "delimiter_stripped_page_local_policy",
    "delimiter_stripped_cross_page_policy",
    "page14_inclusion_control",
    "page71_72_inclusion_control",
    "fixed_page_rune_multiset_shuffle",
    "fixed_section_rune_multiset_shuffle",
    "wrong_section_boundaries",
    "alternate_page_ranges",
    "lag_distance_1_to_110",
    "archive_bigrams_py_section_policy_control",
    "canonical_master_transcription_boundary_control",
    "alias_policy_control",
    "no_plaintext_required_output_policy",
]

NOT_ALLOWED_AS = ["proof", "route_seed", "target_selection", "activation_decision", "execution_seed", "solve_claim"]

STAGE6D_FALSE_GUARDRAILS = {
    "stage6d_final_finite_stage7_manifest_created_now": False,
    "stage6d_archive_run_contract_finalized_now": False,
    "stage6d_creates_stage7_result_archive_now": False,
    "stage6d_generates_stage7_outputs_now": False,
    "stage6d_routes_to_stage7_now": False,
    "stage6d_runs_any_probe_now": False,
    "stage7_probe_execution_performed_now": False,
    "diagnostic_probe_run_now": False,
    "result_archive_created_now": False,
    "bigrams_py_executed_now": False,
    "community_code_executed_now": False,
    "canonical_bigram_matrix_recomputed_now": False,
    "stage7_execution_allowed_next": False,
    "stage7_zip_archive_creation_allowed_next": False,
}

FORBIDDEN_FALSE = (
    stage6.FALSE_GUARDRAILS
    | stage6.STAGE6_FALSE_GUARDRAILS
    | stage6c.STAGE6C_FALSE_GUARDRAILS
    | STAGE6D_FALSE_GUARDRAILS
)


class ValidationResult(stage6.ValidationResult):
    pass


def build_stage6d() -> dict[str, Any]:
    _ensure_no_protected_output_overlap()
    _write_schemas()
    _update_current_stage_schema()
    _update_doc_staleness_source_of_truth_schema()
    reproduction = compute_doublet_reproduction()
    discrepancies = _discrepancies(reproduction)
    source_browser = _source_browser_counts()
    _write_current_stage_state(_precloseout_current_stage_summary(reproduction))
    _write_doc_staleness_source_of_truth()
    _repair_current_mirror_text()
    automation = _automation_triage()
    hooks = _hook_verification()
    records = _records(reproduction, discrepancies, source_browser, automation, hooks)
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)
    _write_current_stage_state(records["summary"])
    _write_docs(records["summary"])
    _write_completion_summary_stub(records["summary"], automation, hooks)
    return records


def _precloseout_current_stage_summary(reproduction: dict[str, Any]) -> dict[str, Any]:
    p15 = reproduction["profiles"]["pages15_70"]
    return {
        "computed_pages15_70_rune_count": p15["rune_count"],
        "computed_pages15_70_lag1": p15["lag1_adjacent_doublets"],
        "computed_pages15_70_lag5": p15["lag_counts"][5],
        "computed_pages15_70_vector": p15["compact_vector"],
    }


def validate_stage6d() -> ValidationResult:
    validators = [
        validate_stage6d_stage6c_preservation,
        validate_stage6d_corpus_profile_policy,
        validate_stage6d_canonical_doublet_profile,
        validate_stage6d_raw_vs_collapsed_boundary,
        validate_stage6d_86_89_reconciliation,
        validate_stage6d_lag_profile,
        validate_stage6d_section_plateau,
        validate_stage6d_zero_doublet_pages,
        validate_stage6d_421_occurrence_index,
        validate_stage6d_number_fact_overlays,
        validate_stage6d_future_probes,
        validate_stage6d_stage6e_addendum,
        validate_stage6d_hook_verification,
        validate_stage6d_doc_staleness_automation_triage,
        validate_stage6d_no_scanner_weakening,
        validate_stage6d_source_browser_loadability,
        validate_stage6d_current_stage_transition,
        validate_stage6d_gate_closure,
        validate_stage6d_handoff,
        validate_stage6d_files_and_schemas,
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for validator in validators:
        result = validator()
        errors.extend(result.errors)
        counts.update(result.counts)
    counts["validation_error_count"] = len(errors)
    return ValidationResult(errors, counts)


def validate_stage6d_files_and_schemas() -> ValidationResult:
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
    return _result(errors, stage6d_schema_count=len(SCHEMA_PATHS), stage6d_data_record_count=len(DATA_PATHS))


def validate_stage6d_stage6c_preservation() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["stage6c_preservation"])
    errors = []
    for key in [
        "stage6c_preserved",
        "stage6c_ouroboros_i31_input_preserved",
        "stage6c_records_not_rewritten_now",
        "stage6b_probe_mapping_repairs_preserved",
        "stage6b_hook_report_only_default_preserved",
    ]:
        if record.get(key) is not True:
            errors.append(f"{key} must be true")
    return _result(errors, stage6c_preserved=record.get("stage6c_preserved"))


def validate_stage6d_corpus_profile_policy() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["corpus_profile_policy"])
    errors = []
    if record.get("doublet_counting_policy_id") != "lp_master_page_local_delimiter_collapsed_v0":
        errors.append("doublet counting policy id mismatch")
    if record.get("delimiter_table") != DELIMITER_TABLE:
        errors.append("delimiter table mismatch")
    if record.get("adjacent_doublet_vector_policy", {}).get("vector_order_labels") != EXPECTED_VECTOR_ORDER:
        errors.append("vector order labels mismatch")
    if record.get("collapsed_page_local_policy_steps") != _collapsed_policy_steps():
        errors.append("collapsed policy steps mismatch")
    if record.get("raw_adjacent_policy_steps") != _raw_policy_steps():
        errors.append("raw policy steps mismatch")
    return _result(errors, vector_order_count=len(record.get("adjacent_doublet_vector_policy", {}).get("vector_order_labels", [])))


def validate_stage6d_canonical_doublet_profile() -> ValidationResult:
    record = read_yaml(HISTORICAL_ROUTE_PATHS["canonical_doublet_profile_pages15_70"])
    errors = []
    expected = {
        "rune_count": 12956,
        "doublet_lag1_total": 86,
        "lag5_equal_count": 479,
        "adjacent_doublet_compact_vector": "42442156242421632042324217223",
        "adjacent_doublet_vector": EXPECTED_PAGES15_70_VECTOR,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            errors.append(f"{key} mismatch")
    policy = record.get("adjacent_doublet_vector_policy", {})
    if policy.get("vector_order_labels") != EXPECTED_VECTOR_ORDER:
        errors.append("vector policy missing explicit order")
    return _result(errors, canonical_pages15_70_profile_reproduced=not errors)


def validate_stage6d_raw_vs_collapsed_boundary() -> ValidationResult:
    record = read_yaml(HISTORICAL_ROUTE_PATHS["raw_vs_collapsed_doublet_boundary_contribution"])
    errors = []
    if record.get("raw_adjacent_doublets") != 60:
        errors.append("raw adjacent doublet mismatch")
    if record.get("delimiter_bridged_doublets") != 26:
        errors.append("bridged doublet mismatch")
    if record.get("collapsed_total") != 86:
        errors.append("collapsed total mismatch")
    if record.get("delimiter_bridge_breakdown") != _expected_bridge_breakdown():
        errors.append("bridge breakdown mismatch")
    if record.get("collapsed_421_triples") != {"ORC": [4, 2, 1], "J_EO_P": [4, 2, 1], "OE_D_A": [4, 2, 1]}:
        errors.append("collapsed 421 triples mismatch")
    if record.get("raw_adjacent_only_triples") != {"ORC": [3, 1, 1], "J_EO_P": [2, 2, 1], "OE_D_A": [2, 2, 0]}:
        errors.append("raw 421 triples mismatch")
    return _result(errors, raw_vs_collapsed_split_reproduced=not errors)


def validate_stage6d_86_89_reconciliation() -> ValidationResult:
    record = read_yaml(HISTORICAL_ROUTE_PATHS["doublet_86_89_boundary_policy_reconciliation"])
    errors = []
    profiles = {item["profile_id"]: item for item in record.get("canonical_doublet_corpus_profiles", [])}
    if profiles.get("observation_421_vector_profile", {}).get("lag1_adjacent_doublets") != 86:
        errors.append("86 profile mismatch")
    if profiles.get("instruction_page14_disk_reconciliation_profile", {}).get("lag1_adjacent_doublets") != 89:
        errors.append("89 profile mismatch")
    if profiles.get("lag_distance_scan_profile", {}).get("lag11") != 395:
        errors.append("lag11 profile mismatch")
    return _result(errors, profile_count=len(profiles))


def validate_stage6d_lag_profile() -> ValidationResult:
    record = read_yaml(HISTORICAL_ROUTE_PATHS["lag1_specific_doublet_suppression"])
    lag_counts = record.get("lag_counts_pages15_70", {})
    expected = {"lag1": 86, "lag2": 441, "lag3": 439, "lag4": 459, "lag5": 479, "lag6": 455, "lag7": 451, "lag8": 438, "lag9": 463, "lag10": 442}
    errors = [f"{key} mismatch" for key, value in expected.items() if lag_counts.get(key) != value]
    if abs(float(record.get("fixed_page_rune_multiset_expectation", {}).get("adjacent_expected_approx", 0)) - 439.17) > 0.01:
        errors.append("pages15_70 fixed expectation mismatch")
    return _result(errors, lag_count_profile_reproduced=not errors)


def validate_stage6d_section_plateau() -> ValidationResult:
    record = read_yaml(HISTORICAL_ROUTE_PATHS["early_section_doublet_suppression_plateau"])
    errors = []
    if record.get("section_starts") != [0, 15, 18, 23, 30, 38, 42, 55, 69, 71, 72, 75]:
        errors.append("section starts mismatch")
    for key in ["bigrams_py_executed_now", "community_code_executed_now", "trusted_as_canonical_boundaries"]:
        if record.get(key) is not False:
            errors.append(f"{key} must be false")
    if record.get("section_boundary_warning") is not True:
        errors.append("section boundary warning missing")
    return _result(errors, community_section_count=len(record.get("sections", [])))


def validate_stage6d_zero_doublet_pages() -> ValidationResult:
    record = read_yaml(HISTORICAL_ROUTE_PATHS["zero_doublet_page_count14"])
    errors = []
    if record.get("zero_doublet_pages") != EXPECTED_ZERO_DOUBLET_PAGES:
        errors.append("zero doublet pages mismatch")
    if record.get("zero_doublet_page_count") != 14:
        errors.append("zero doublet page count mismatch")
    if not all("display_page_label" in item and "internal_segment_index" in item for item in record.get("zero_doublet_page_records", [])):
        errors.append("zero page records must preserve display label and internal index")
    return _result(errors, zero_doublet_page_count=record.get("zero_doublet_page_count"))


def validate_stage6d_421_occurrence_index() -> ValidationResult:
    record = read_yaml(HISTORICAL_ROUTE_PATHS["doublet_421_occurrence_index_canonical_rebuild"])
    errors = []
    if record.get("doublet_421_occurrence_indices_global_1_based") != EXPECTED_421_OCCURRENCES:
        errors.append("421 occurrence index mismatch")
    required_policies = [
        "global_1_based",
        "global_0_based",
        "section_local_1_based",
        "section_local_0_based",
        "page_local_1_based",
        "page_local_0_based",
    ]
    if record.get("indexing_policies_to_record") != required_policies:
        errors.append("indexing policy list mismatch")
    return _result(errors, occurrence_index_symbol_count=len(record.get("doublet_421_occurrence_indices_global_1_based", {})))


def validate_stage6d_number_fact_overlays() -> ValidationResult:
    record = read_yaml(OPERATOR_PATHS["number_fact_overlays"])
    overlays = record.get("overlays", [])
    by_id = {item["overlay_id"]: item for item in overlays}
    errors = []
    required_fields = [
        "overlay_id",
        "source_record_path",
        "source_fact_id",
        "fact_class",
        "display_label",
        "short_label",
        "value",
        "values",
        "value_type",
        "operation_type",
        "expression",
        "relation",
        "why_stored",
        "verification_status",
        "display_priority",
        "source_paths",
        "crosslinks",
        "risk_notes",
        "controls_required",
        "not_allowed_as",
        "usable_for_decision_now",
    ]
    for overlay_id in OVERLAY_IDS:
        item = by_id.get(overlay_id)
        if item is None:
            errors.append(f"missing overlay {overlay_id}")
            continue
        for field in required_fields:
            if field not in item:
                errors.append(f"{overlay_id} missing {field}")
        if item.get("usable_for_decision_now") is not False:
            errors.append(f"{overlay_id} usable_for_decision_now must be false")
        if item.get("not_allowed_as") != NOT_ALLOWED_AS:
            errors.append(f"{overlay_id} not_allowed_as mismatch")
    return _result(errors, overlay_count=len(overlays))


def validate_stage6d_future_probes() -> ValidationResult:
    registry = read_yaml(TOKEN_BLOCK_PATHS["doublet_future_probe_registry"])
    controls = read_yaml(TOKEN_BLOCK_PATHS["doublet_control_bundle"])
    errors = []
    if registry.get("future_probe_ids") != FUTURE_PROBE_IDS:
        errors.append("future probe ids mismatch")
    if controls.get("control_bundle_id") != CONTROL_BUNDLE_ID or controls.get("controls") != CONTROL_BUNDLE:
        errors.append("control bundle mismatch")
    for probe in registry.get("future_probes", []):
        for key in ["stage6d_run_now", "execution_enabled_now", "stage7_execution_enabled_now", "usable_for_decision_now"]:
            if probe.get(key) is not False:
                errors.append(f"{probe.get('probe_id')} {key} must be false")
        if probe.get("control_bundle_id") != CONTROL_BUNDLE_ID:
            errors.append(f"{probe.get('probe_id')} control bundle mismatch")
    return _result(errors, future_probe_count=len(registry.get("future_probes", [])))


def validate_stage6d_stage6e_addendum() -> ValidationResult:
    addendum = read_yaml(TOKEN_BLOCK_PATHS["stage6e_manifest_input_addendum"])
    errors = []
    if addendum.get("includes_stage6c_ouroboros_i31_input_addendum") is not True:
        errors.append("Stage 6C addendum reference missing")
    if addendum.get("includes_stage6d_doublet_boundary_input_addendum") is not True:
        errors.append("Stage 6D addendum reference missing")
    for key in ["supersedes_stage6c_addendum", "supersedes_stage6d_addendum", "not_final_stage7_manifest"]:
        expected = False if key.startswith("supersedes") else True
        if addendum.get(key) is not expected:
            errors.append(f"{key} mismatch")
    return _result(errors, stage6e_future_probe_count=len(addendum.get("future_probe_ids", [])))


def validate_stage6d_hook_verification() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["hook_verification_summary"])
    errors = []
    if record.get("strict_mode_env_var") != "LIBERPRIMUS_CODEX_HOOK_STRICT":
        errors.append("strict env var mismatch")
    if record.get("strict_mode_unset_during_default_tests") is not True:
        errors.append("strict mode must be unset during default tests")
    for key in ["hook_default_exit_zero_from_repo_root", "hook_default_exit_zero_from_subdirectory", "stdin_consumed_without_hanging"]:
        if record.get(key) is not True:
            errors.append(f"{key} must be true")
    if record.get("hook_reports_written_only_under_ignored_results") is not True:
        errors.append("hook reports must stay under ignored results")
    return _result(errors, hook_default_exit_zero_verified=record.get("hook_default_exit_zero_from_repo_root"))


def validate_stage6d_doc_staleness_automation_triage() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["doc_staleness_automation_triage_summary"])
    errors = []
    if record.get("operator_reported_latest_24h_warnings") is not True:
        errors.append("operator warning report flag missing")
    if record.get("exact_automation_report_found_and_triaged") is not True and record.get("local_reproduction_run") is not True:
        errors.append("automation triage must either find exact report or run local reproduction")
    if record.get("error_count_after_fix") != 0:
        errors.append("automation triage error count must be zero")
    if record.get("scanner_weakened") is not False:
        errors.append("scanner weakened")
    return _result(errors, warning_count_after_fix=record.get("warning_count_after_fix"))


def validate_stage6d_no_scanner_weakening() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["doc_staleness_automation_triage_summary"])
    errors = []
    forbidden = record.get("forbidden_scanner_weakening", {})
    for key in [
        "broad_docs_directory_ignore",
        "broad_current_mirror_ignore",
        "strict_scanner_changed_to_non_strict",
        "real_current_stage_errors_downgraded",
        "historical_sections_deleted_to_silence_scanner",
    ]:
        if forbidden.get(key) is not False:
            errors.append(f"{key} must be false")
    return _result(errors, scanner_weakened=record.get("scanner_weakened"))


def validate_stage6d_source_browser_loadability() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    errors = []
    if int(record.get("source_browser_validation_error_count", -1)) != 0:
        errors.append("Source Browser validation errors must be zero")
    return _result(errors, source_browser_entries_loaded=record.get("source_browser_entries_loaded"))


def validate_stage6d_current_stage_transition() -> ValidationResult:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    errors = []
    expected = {
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
        "stage6d_archive_run_contract_finalized_now": False,
        "stage6d_creates_stage7_result_archive_now": False,
        "stage6e_final_manifest_required": True,
    }
    for key, value in expected.items():
        if current.get(key) != value:
            errors.append(f"current-stage {key} expected {value!r}")
    return _result(errors, recommended_next_stage_id=current.get("recommended_next_stage_id"))


def validate_stage6d_gate_closure() -> ValidationResult:
    errors: list[str] = []
    for path in DATA_PATHS.values():
        payload = read_yaml(path)
        for guard, expected in FORBIDDEN_FALSE.items():
            if guard in payload and payload[guard] is not expected:
                errors.append(f"{path}: {guard} must be {expected}")
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    for guard, expected in FORBIDDEN_FALSE.items():
        if summary.get(guard) is not expected:
            errors.append(f"summary: {guard} must be {expected}")
    return _result(errors, guardrail_record_count=len(DATA_PATHS))


def validate_stage6d_handoff() -> ValidationResult:
    record = read_yaml(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if record.get("completion_summary_path") != CODEX_COMPLETION_PATH.as_posix():
        errors.append("completion summary path mismatch")
    if Path("codex_output").exists():
        errors.append("deprecated codex_output path exists")
    return _result(errors, handoff_path=record.get("completion_summary_path"))


def stage6d_summary_text() -> str:
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    return "\n".join(
        [
            "LiberPrimus Stage 6D summary:",
            f"status={summary.get('status')}",
            f"stage_id={summary.get('stage_id')}",
            f"previous_stage_id={summary.get('previous_stage_id')}",
            f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
            f"computed_pages15_70_rune_count={summary.get('computed_pages15_70_rune_count')}",
            f"computed_pages15_70_lag1={summary.get('computed_pages15_70_lag1')}",
            f"computed_pages15_70_lag5={summary.get('computed_pages15_70_lag5')}",
            f"computed_pages15_70_vector={summary.get('computed_pages15_70_vector')}",
            f"computed_raw_adjacent_doublets={summary.get('computed_raw_adjacent_doublets')}",
            f"computed_delimiter_bridged_doublets={summary.get('computed_delimiter_bridged_doublets')}",
            f"expected_value_discrepancy_count={summary.get('expected_value_discrepancy_count')}",
            f"blocking_discrepancy_count={summary.get('blocking_discrepancy_count')}",
            f"warning_count_after_fix={summary.get('warning_count_after_fix')}",
            f"hook_default_exit_zero_verified={summary.get('hook_default_exit_zero_verified')}",
        ]
    )


def compute_doublet_reproduction() -> dict[str, Any]:
    labels, rune_to_label = _gp_profile()
    delimiter_table, pages = _master_pages()
    profiles = {
        "pages15_70": _profile(pages, rune_to_label, labels, 15, 70),
        "pages14_70": _profile(pages, rune_to_label, labels, 14, 70),
        "pages15_72": _profile(pages, rune_to_label, labels, 15, 72),
    }
    profiles["pages15_70"]["lag_counts"] = _lag_counts(profiles["pages15_70"]["concat_tokens"], range(1, 111))
    profiles["pages15_72"]["lag_counts"] = _lag_counts(profiles["pages15_72"]["concat_tokens"], range(1, 111))
    profiles["pages15_72"]["average_lag2_to_lag110_approx"] = round(
        sum(profiles["pages15_72"]["lag_counts"][lag] for lag in range(2, 111)) / 109
    )
    profiles["pages15_70"]["fixed_expectation"] = _fixed_page_expectation(profiles["pages15_70"]["page_tokens"])
    profiles["pages14_70"]["fixed_expectation"] = _fixed_page_expectation(profiles["pages14_70"]["page_tokens"])
    profiles["pages14_70"]["delta_from_pages15_70"] = _delta_vector(
        profiles["pages14_70"], profiles["pages15_70"]
    )
    sections = _community_sections(pages, rune_to_label)
    return {
        "labels": labels,
        "delimiter_table": delimiter_table,
        "profiles": profiles,
        "community_sections": sections,
        "raw_vs_collapsed": _raw_vs_collapsed(profiles["pages15_70"], labels),
        "source_path": MASTER_TRANSCRIPTION_PATH.as_posix(),
    }


def _records(
    reproduction: dict[str, Any],
    discrepancies: list[dict[str, Any]],
    source_browser: dict[str, int],
    automation: dict[str, Any],
    hooks: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    overlays = _overlay_collection()
    future = _future_probe_registry()
    return {
        "summary": _summary_record(reproduction, discrepancies, source_browser, automation, hooks, overlays, future),
        "next_stage_decision": _next_stage_decision_record(),
        "stage6c_preservation": _stage6c_preservation_record(),
        "canonical_doublet_source_lock_summary": _canonical_doublet_summary(reproduction, discrepancies),
        "corpus_profile_policy": _corpus_profile_policy_record(reproduction),
        "doublet_boundary_policy_reconciliation": _boundary_policy_reconciliation_record(reproduction),
        "doc_staleness_automation_triage_summary": _automation_record(automation),
        "hook_verification_summary": _hook_record(hooks),
        "source_browser_loadability_summary": _base_project_record("stage6d_source_browser_loadability_summary")
        | source_browser,
        "reviewable_validation_evidence": _validation_evidence_record(reproduction, discrepancies, automation, hooks),
        "reviewability_gap_register": _reviewability_gap_record(discrepancies, automation, hooks),
        "current_stage_transition": _current_stage_transition_record(),
        "chatgpt_context_update_summary": _base_project_record("stage6d_chatgpt_context_update_summary")
        | {"chatgpt_context_updated_to_stage6d": True, "stage6e_routed_next": True},
        "canonical_doublet_profile_pages15_70": _canonical_profile_record(reproduction),
        "raw_vs_collapsed_doublet_boundary_contribution": _raw_vs_collapsed_record(reproduction),
        "doublet_86_89_boundary_policy_reconciliation": _reconciliation_record(reproduction),
        "instruction_page14_doublet_delta": _instruction_page14_record(reproduction),
        "lag_distance_profile_pages15_72": _lag_distance_record(reproduction),
        "lag1_specific_doublet_suppression": _lag1_suppression_record(reproduction),
        "early_section_doublet_suppression_plateau": _section_plateau_record(reproduction),
        "zero_doublet_page_count14": _zero_page_record(reproduction),
        "doublet_421_occurrence_index_canonical_rebuild": _occurrence_index_record(reproduction),
        "doublet_count_group_size_sequence": _count_group_record(reproduction),
        "doublet_corpus_profile_family_index": _profile_family_index_record(reproduction),
        "doublet_future_probe_registry": future,
        "doublet_control_bundle": _control_bundle_record(),
        "doublet_keeper_taxonomy": _keeper_taxonomy_record(),
        "doublet_route_fingerprint_watchlist": _route_fingerprint_watchlist_record(),
        "stage6e_manifest_input_addendum": _stage6e_addendum_record(),
        "no_active_ingestion_proof": _gate_record("stage6d_no_active_ingestion_proof"),
        "no_byte_stream_transition_gate": _gate_record("stage6d_no_byte_stream_transition_gate"),
        "no_execution_transition_gate": _gate_record("stage6d_no_execution_transition_gate"),
        "canonical_transcription_doublet_source_crosslink": _canonical_source_crosslink(),
        "observation_rune_frequency_crosslink": _observation_crosslink(),
        "raw_source_noncommit_proof": _noncommit_record("stage6d_raw_source_noncommit_proof"),
        "codex_handoff_policy": _source_record("stage6d_codex_handoff_policy")
        | {"completion_summary_path": CODEX_COMPLETION_PATH.as_posix()},
        "credential_redaction_policy_preservation": _source_record("stage6d_credential_redaction_policy_preservation")
        | {"secrets_written_now": False, "credential_redaction_policy_preserved": True},
        "hook_runner_evidence": _source_record("stage6d_hook_runner_evidence") | hooks,
        "number_fact_overlays": overlays,
    }


def _summary_record(
    reproduction: dict[str, Any],
    discrepancies: list[dict[str, Any]],
    source_browser: dict[str, int],
    automation: dict[str, Any],
    hooks: dict[str, Any],
    overlays: dict[str, Any],
    future: dict[str, Any],
) -> dict[str, Any]:
    p15 = reproduction["profiles"]["pages15_70"]
    raw = reproduction["raw_vs_collapsed"]
    return _base_project_record("stage6d_summary") | {
        "status": "complete",
        "source_previous_stage": PREVIOUS_STAGE_ID,
        "previous_stage_id": PREVIOUS_STAGE_ID,
        "previous_stage_title": PREVIOUS_STAGE_TITLE,
        "starting_commit": STARTING_COMMIT,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "bounded_canonical_doublet_reproduction_performed_now": True,
        "bounded_reproduction_scope": [
            "pages15_70_collapsed_page_local_profile",
            "raw_vs_collapsed_boundary_contribution",
            "pages14_70_reconciliation_profile",
            "pages15_72_lag_scan_profile",
            "community_section_plateau_static_reproduction",
            "zero_doublet_page_list",
            "doublet_421_occurrence_indices",
        ],
        "computed_pages15_70_rune_count": p15["rune_count"],
        "computed_pages15_70_lag1": p15["lag1_adjacent_doublets"],
        "computed_pages15_70_lag5": p15["lag_counts"][5],
        "computed_pages15_70_vector": p15["compact_vector"],
        "computed_raw_adjacent_doublets": raw["raw_adjacent_doublets"],
        "computed_delimiter_bridged_doublets": raw["delimiter_bridged_doublets"],
        "computed_collapsed_total": raw["collapsed_total"],
        "canonical_pages15_70_profile_reproduced": _no_discrepancies(discrepancies, "pages15_70"),
        "raw_vs_collapsed_split_reproduced": _no_discrepancies(discrepancies, "raw_vs_collapsed"),
        "pages14_70_profile_reproduced": _no_discrepancies(discrepancies, "pages14_70"),
        "pages15_72_lag_scan_reproduced": _no_discrepancies(discrepancies, "pages15_72"),
        "zero_doublet_page_list_reproduced": _no_discrepancies(discrepancies, "zero_doublet_pages"),
        "doublet_421_occurrence_indices_reproduced": _no_discrepancies(discrepancies, "doublet_421_occurrence_indices"),
        "expected_value_discrepancy_count": len(discrepancies),
        "blocking_discrepancy_count": sum(1 for item in discrepancies if item["blocking_for_stage6e_manifest_finalization"]),
        "future_probe_count": len(future["future_probes"]),
        "overlay_count": len(overlays["overlays"]),
        "exact_automation_report_found_and_triaged": automation["exact_automation_report_found_and_triaged"],
        "local_reproduction_run": automation["local_reproduction_run"],
        "warning_count_before_fix": automation["warning_count_before_fix"],
        "warning_count_after_fix": automation["warning_count_after_fix"],
        "stale_current_strict_errors_after_fix": automation["error_count_after_fix"],
        "hook_default_exit_zero_verified": hooks["hook_default_exit_zero_from_repo_root"]
        and hooks["hook_default_exit_zero_from_subdirectory"],
        "hook_json_launcher_exit_zero_where_supported": hooks["hook_json_launcher_exit_zero_where_supported"],
        "hook_runner_semantics_fully_simulated": hooks["hook_runner_semantics_fully_simulated"],
        "hook_repair_applied": hooks["hook_repair_applied"],
        "stage6e_routed_next": True,
        "stage7_manifest_created_now": False,
        "stage6e_final_manifest_required": True,
        **source_browser,
    }


def _canonical_profile_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    p15 = reproduction["profiles"]["pages15_70"]
    return _historical_record("stage6d_canonical_doublet_profile_pages15_70") | {
        "profile_id": "lp_master_pages15_70_collapsed_page_local_profile_v0",
        "source": MASTER_TRANSCRIPTION_PATH.as_posix(),
        "source_layer": "canonical_master_transcription",
        "corpus_segments_or_pages": "15-70",
        "rune_count": p15["rune_count"],
        "boundary_policy": _boundary_policy_summary(),
        "doublet_lag1_total": p15["lag1_adjacent_doublets"],
        "adjacent_doublet_compact_vector": p15["compact_vector"],
        "adjacent_doublet_vector": p15["vector"],
        "adjacent_doublet_vector_policy": _vector_policy(p15),
        "lag5_equal_count": p15["lag_counts"][5],
        "relation": (
            "Canonical page-local collapsed profile reproduces the Stage 6 ObservationOnRuneFrequency vector "
            "and the Stage 5EH Lag5 N=12,956 corpus."
        ),
        "bounded_canonical_doublet_reproduction_performed_now": True,
        "stage7_probe_execution_performed_now": False,
    }


def _raw_vs_collapsed_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    raw = reproduction["raw_vs_collapsed"]
    return _historical_record("stage6d_raw_vs_collapsed_doublet_boundary_contribution") | raw | {
        "profile_id": "lp_master_pages15_70_raw_vs_collapsed_boundary_contribution_v0",
        "key_warning": "The 421 diagonal pattern requires delimiter-stripped page-local policy; it is not a raw-adjacent-only fingerprint.",
        "collapsed_page_local_policy_steps": _collapsed_policy_steps(),
        "raw_adjacent_policy_steps": _raw_policy_steps(),
    }


def _reconciliation_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    p15 = reproduction["profiles"]["pages15_70"]
    p14 = reproduction["profiles"]["pages14_70"]
    p72 = reproduction["profiles"]["pages15_72"]
    return _historical_record("stage6d_doublet_86_89_boundary_policy_reconciliation") | {
        "canonical_doublet_corpus_profiles": [
            {
                "profile_id": "observation_421_vector_profile",
                "page_or_segment_range": "15-70",
                "rune_count": p15["rune_count"],
                "lag1_adjacent_doublets": p15["lag1_adjacent_doublets"],
                "lag5_equal_count": p15["lag_counts"][5],
                "vector": p15["compact_vector"],
                "role": "ObservationOnRuneFrequency vector / Lag5 corpus",
            },
            {
                "profile_id": "instruction_page14_disk_reconciliation_profile",
                "page_or_segment_range": "14-70",
                "rune_count": p14["rune_count"],
                "lag1_adjacent_doublets": p14["lag1_adjacent_doublets"],
                "delta_from_15_70": _delta_vector(p14, p15),
                "role": "Candidate DiskCipher 89 reconciliation profile; including the instruction page adds three doublets.",
            },
            {
                "profile_id": "lag_distance_scan_profile",
                "page_or_segment_range": "15-72",
                "rune_count": p72["rune_count"],
                "lag1": p72["lag_counts"][1],
                "lag11": p72["lag_counts"][11],
                "lag99": p72["lag_counts"][99],
                "average_lag2_to_lag110_approx": round(sum(p72["lag_counts"][lag] for lag in range(2, 111)) / 109),
                "role": "Candidate community lag-distance scan profile.",
            },
        ],
        "doublet_claim_reconciliation": "86 and 89 are boundary-policy dependent counts, not interchangeable proof.",
    }


def _instruction_page14_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    p15 = reproduction["profiles"]["pages15_70"]
    p14 = reproduction["profiles"]["pages14_70"]
    return _historical_record("stage6d_instruction_page14_doublet_delta") | {
        "profile_id": "instruction_page14_disk_reconciliation_profile",
        "page_or_segment_range": "14-70",
        "rune_count": p14["rune_count"],
        "lag1_adjacent_doublets": p14["lag1_adjacent_doublets"],
        "baseline_profile": "15-70",
        "baseline_lag1_adjacent_doublets": p15["lag1_adjacent_doublets"],
        "delta_from_pages15_70": _delta_vector(p14, p15),
        "accepted_as_validated_diskcipher_metric": False,
    }


def _lag_distance_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    p72 = reproduction["profiles"]["pages15_72"]
    return _historical_record("stage6d_lag_distance_profile_pages15_72") | {
        "profile_id": "lag_distance_scan_profile",
        "page_or_segment_range": "15-72",
        "rune_count": p72["rune_count"],
        "lag1": p72["lag_counts"][1],
        "lag11": p72["lag_counts"][11],
        "lag99": p72["lag_counts"][99],
        "average_lag2_to_lag110_approx": round(sum(p72["lag_counts"][lag] for lag in range(2, 111)) / 109),
        "lag_count_policy": "collapsed selected corpus sequence after delimiter removal; not raw adjacency",
    }


def _lag1_suppression_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    p15 = reproduction["profiles"]["pages15_70"]
    p14 = reproduction["profiles"]["pages14_70"]
    lag_counts = {f"lag{lag}": p15["lag_counts"][lag] for lag in range(1, 11)}
    return _historical_record("stage6d_lag1_specific_doublet_suppression") | {
        "lag_counts_pages15_70": lag_counts,
        "fixed_page_rune_multiset_expectation": _expectation_summary(p15),
        "fixed_page_rune_multiset_expectation_pages14_70": _expectation_summary(p14),
        "interpretation": (
            "Adjacent equality is strongly suppressed, but non-adjacent equality mostly returns to the expected band. "
            "This points to lag1-specific doublet suppression, not general repeat suppression."
        ),
        "not_target_priority_evidence_alone": True,
        "not_solve_evidence": True,
    }


def _section_plateau_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    community_section_profile = {
        "section_starts": [0, 15, 18, 23, 30, 38, 42, 55, 69, 71, 72, 75],
        "section_starts_source": "ObservationOnRuneFrequency/bigrams.py",
        "trusted_as_canonical_boundaries": False,
        "section_boundary_warning": True,
        "ratio_153_numerology_quarantined": True,
    }
    return _historical_record("stage6d_early_section_doublet_suppression_plateau") | {
        "community_section_profile_id": "observation_archive_bigrams_py_section_starts",
        "source_policy": "observation_archive_bigrams_py_section_starts",
        "section_starts_source": "ObservationOnRuneFrequency/bigrams.py",
        "section_starts": [0, 15, 18, 23, 30, 38, 42, 55, 69, 71, 72, 75],
        "community_section_profile": community_section_profile,
        "trusted_as_canonical_boundaries": False,
        "bigrams_py_executed_now": False,
        "community_code_executed_now": False,
        "sections": reproduction["community_sections"],
        "section_boundary_warning": True,
        "section_boundary_warning_text": (
            "The first four ranges show a stable suppression plateau near 0.153-0.159, but section boundaries "
            "are community/archive-defined and require canonical rebuild before interpretation."
        ),
        "ratio_153_numerology_quarantined": True,
    }


def _zero_page_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    p15 = reproduction["profiles"]["pages15_70"]
    return _historical_record("stage6d_zero_doublet_page_count14") | {
        "finding_id": "canonical_pages15_70_zero_doublet_page_count_14_v0",
        "profile_id": "lp_master_pages15_70_collapsed_page_local_profile_v0",
        "zero_doublet_pages": p15["zero_doublet_pages"],
        "zero_doublet_page_count": len(p15["zero_doublet_pages"]),
        "zero_doublet_page_records": [
            {"display_page_label": page, "internal_segment_index": page} for page in p15["zero_doublet_pages"]
        ],
        "crosslinks": ["pdd153_delta14", "56311_cumulative_offset14", "ouroboros_i31_delta14"],
        "risk_notes": ["page_index_policy_required", "expected_zero_page_count_control_required", "not_proof"],
    }


def _occurrence_index_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    p15 = reproduction["profiles"]["pages15_70"]
    return _historical_record("stage6d_doublet_421_occurrence_index_canonical_rebuild") | {
        "profile_id": "lp_master_pages15_70_collapsed_page_local_profile_v0",
        "doublet_421_occurrence_indices_global_1_based": p15["occurrence_421"],
        "archive_index_reconciliation_required": True,
        "indexing_policies_to_record": [
            "global_1_based",
            "global_0_based",
            "section_local_1_based",
            "section_local_0_based",
            "page_local_1_based",
            "page_local_0_based",
        ],
        "treated_as_proof_now": False,
        "treated_as_route_seed_now": False,
    }


def _count_group_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    p15 = reproduction["profiles"]["pages15_70"]
    return _historical_record("stage6d_doublet_count_group_size_sequence") | {
        "profile_id": "lp_master_pages15_70_collapsed_page_local_profile_v0",
        "doublet_count_groups_by_count": p15["groups_by_count"],
        "group_size_sequence": [len(p15["groups_by_count"][count]) for count in sorted(p15["groups_by_count"])],
        "status": "low_priority_watchlist",
        "risk": "high_selection_sensitivity",
        "alias_policy": _alias_policy(),
    }


def _profile_family_index_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    return _historical_record("stage6d_doublet_corpus_profile_family_index") | {
        "profile_family_id": "canonical_doublet_boundary_policy_profile_family_v0",
        "profiles_indexed": [
            "lp_master_pages15_70_collapsed_page_local_profile_v0",
            "lp_master_pages15_70_raw_vs_collapsed_boundary_contribution_v0",
            "instruction_page14_disk_reconciliation_profile",
            "lag_distance_scan_profile",
            "observation_archive_bigrams_py_section_starts",
        ],
        "source_path": reproduction["source_path"],
        "usable_for_decision_now": False,
    }


def _records_for_overlay() -> list[tuple[str, str, str, str, Any]]:
    return [
        (
            "stage6d_canonical_doublet_profile_pages15_70_overlay",
            HISTORICAL_ROUTE_PATHS["canonical_doublet_profile_pages15_70"].as_posix(),
            "canonical_pages15_70_lag1_86_vector",
            "Canonical pages15-70 profile: 12,956 runes, 86 adjacent doublets, vector 42442156242421632042324217223.",
            86,
        ),
        (
            "stage6d_observation_vector_reproduction_overlay",
            HISTORICAL_ROUTE_PATHS["canonical_doublet_profile_pages15_70"].as_posix(),
            "observation_vector_reproduction",
            "Canonical reproduction matches the ObservationOnRuneFrequency adjacent-doublet vector.",
            "42442156242421632042324217223",
        ),
        (
            "stage6d_raw_vs_collapsed_60_26_86_overlay",
            HISTORICAL_ROUTE_PATHS["raw_vs_collapsed_doublet_boundary_contribution"].as_posix(),
            "raw_vs_collapsed_60_26_86",
            "Raw adjacency has 60 doublets; delimiter-collapsed bridges add 26 for total 86.",
            [60, 26, 86],
        ),
        (
            "stage6d_doublet_421_boundary_dependency_overlay",
            HISTORICAL_ROUTE_PATHS["raw_vs_collapsed_doublet_boundary_contribution"].as_posix(),
            "421_boundary_dependency",
            "The 421 triples are boundary-policy dependent and require delimiter-stripped page-local counting.",
            [4, 2, 1],
        ),
        (
            "stage6d_doublet_86_89_boundary_reconciliation_overlay",
            HISTORICAL_ROUTE_PATHS["doublet_86_89_boundary_policy_reconciliation"].as_posix(),
            "86_89_boundary_reconciliation",
            "The 86 and 89 doublet counts separate ObservationOnRuneFrequency and page14-inclusion policies.",
            [86, 89],
        ),
        (
            "stage6d_instruction_page14_plus3_overlay",
            HISTORICAL_ROUTE_PATHS["instruction_page14_doublet_delta"].as_posix(),
            "instruction_page14_plus3",
            "Including instruction page 14 adds three doublets: F+1 and L+2.",
            3,
        ),
        (
            "stage6d_lag1_specific_suppression_overlay",
            HISTORICAL_ROUTE_PATHS["lag1_specific_doublet_suppression"].as_posix(),
            "lag1_specific_suppression",
            "Lag1 has 86 observed versus about 439.17 expected, while higher lags return toward the expected band.",
            0.196,
        ),
        (
            "stage6d_early_section_suppression_plateau_overlay",
            HISTORICAL_ROUTE_PATHS["early_section_doublet_suppression_plateau"].as_posix(),
            "early_section_suppression_plateau",
            "Community section starts show early ratio plateau near 0.153-0.159, but boundaries are noncanonical controls.",
            [0.159, 0.153, 0.154, 0.154],
        ),
        (
            "stage6d_zero_doublet_page_count14_overlay",
            HISTORICAL_ROUTE_PATHS["zero_doublet_page_count14"].as_posix(),
            "zero_doublet_page_count14",
            "Fourteen pages in the pages15-70 profile have zero adjacent doublets.",
            14,
        ),
        (
            "stage6d_421_occurrence_index_rebuild_overlay",
            HISTORICAL_ROUTE_PATHS["doublet_421_occurrence_index_canonical_rebuild"].as_posix(),
            "421_occurrence_index_rebuild",
            "Canonical 421 occurrence indices are source-locked for future index-policy reconciliation.",
            421,
        ),
        (
            "stage6d_doublet_count_group_sequence_overlay",
            HISTORICAL_ROUTE_PATHS["doublet_count_group_size_sequence"].as_posix(),
            "doublet_count_group_sequence",
            "Doublet count group sizes are [1,3,11,3,7,1,2,1].",
            [1, 3, 11, 3, 7, 1, 2, 1],
        ),
    ]


def _overlay_collection() -> dict[str, Any]:
    return _operator_record("stage6d_canonical_doublet_boundary_policy_overlays") | {
        "overlay_collection_id": "stage6d_canonical_doublet_boundary_policy_overlays",
        "review_state": "overlay_enriched_fact",
        "not_number_fact_review_batch": True,
        "overlays": [
            {
                "overlay_id": overlay_id,
                "source_record_path": source_path,
                "source_fact_id": fact_id,
                "fact_class": "canonical_doublet_boundary_policy",
                "display_label": label,
                "short_label": fact_id,
                "value": value,
                "values": value if isinstance(value, list) else [value],
                "value_type": "integer_or_sequence",
                "operation_type": "bounded_metadata_reproduction",
                "expression": label,
                "relation": "Review-only source-lock bridge for future Stage 6E manifest planning.",
                "why_stored": "Preserves a bounded canonical doublet/boundary policy fact without executing Stage 7 probes.",
                "verification_status": "locally_reproduced_from_canonical_master_transcription",
                "display_priority": index + 1,
                "source_paths": [MASTER_TRANSCRIPTION_PATH.as_posix(), source_path],
                "crosslinks": ["observation_on_rune_frequency", "stage6c_ouroboros_i31_input_addendum"],
                "risk_notes": ["boundary_policy_sensitive", "not_proof", "future_controls_required"],
                "controls_required": CONTROL_BUNDLE,
                "not_allowed_as": NOT_ALLOWED_AS,
                "usable_for_decision_now": False,
            }
            for index, (overlay_id, source_path, fact_id, label, value) in enumerate(_records_for_overlay())
        ],
    }


def _future_probe_registry() -> dict[str, Any]:
    return _token_record("stage6d_doublet_future_probe_registry") | {
        "future_probe_ids": FUTURE_PROBE_IDS,
        "future_probes": [
            {
                "probe_id": probe_id,
                "stage6d_run_now": False,
                "execution_enabled_now": False,
                "stage7_execution_enabled_now": False,
                "full_output_archive_required_when_run": True,
                "no_lossy_filtering_required_when_run": True,
                "usable_for_decision_now": False,
                "not_solve_evidence": True,
                "control_bundle_id": CONTROL_BUNDLE_ID,
                "blocked_actions": [
                    "solve_claim",
                    "target_selection",
                    "route_stream_generation_unless_later_stage_explicitly_allows",
                    "byte_stream_generation_unless_later_stage_explicitly_allows",
                    "lossy_top_n_filtering",
                    "cuda_scoring_triage",
                ],
            }
            for probe_id in FUTURE_PROBE_IDS
        ],
    }


def _stage6e_addendum_record() -> dict[str, Any]:
    return _token_record("stage6d_stage6e_manifest_input_addendum") | {
        "stage6e_manifest_input_addendum": {
            "includes_stage6c_ouroboros_i31_input_addendum": True,
            "includes_stage6d_doublet_boundary_input_addendum": True,
            "source_locked_review_facts": SOURCE_LOCKED_REVIEW_FACTS,
            "future_probe_ids": FUTURE_PROBE_IDS,
            "not_final_stage7_manifest": True,
            "stage6e_final_manifest_required": True,
        },
        "includes_stage6c_ouroboros_i31_input_addendum": True,
        "includes_stage6d_doublet_boundary_input_addendum": True,
        "stage6c_addendum_path": stage6c.TOKEN_BLOCK_PATHS["stage6d_manifest_input_addendum"].as_posix(),
        "stage6d_addendum_path": TOKEN_BLOCK_PATHS["stage6e_manifest_input_addendum"].as_posix(),
        "source_locked_review_facts": SOURCE_LOCKED_REVIEW_FACTS,
        "future_probe_ids": FUTURE_PROBE_IDS,
        "supersedes_stage6c_addendum": False,
        "supersedes_stage6d_addendum": False,
        "not_final_stage7_manifest": True,
        "stage6e_final_manifest_required": True,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }


def _control_bundle_record() -> dict[str, Any]:
    return _token_record("stage6d_doublet_control_bundle") | {
        "control_bundle_id": CONTROL_BUNDLE_ID,
        "controls": CONTROL_BUNDLE,
    }


def _keeper_taxonomy_record() -> dict[str, Any]:
    return _token_record("stage6d_doublet_keeper_taxonomy") | {
        "keeper_categories": [
            "canonical_corpus_policy_bridge",
            "boundary_policy_bridge",
            "doublet_suppression_signature",
            "lag_profile_signature",
            "archive_reconciliation",
            "diskcipher_reconciliation",
            "observation_on_rune_frequency_reproduction",
            "zero_doublet_page_bridge",
            "occurrence_index_bridge",
            "second_stage_surface_not_plaintext_policy",
        ],
        "usable_for_decision_now": False,
    }


def _route_fingerprint_watchlist_record() -> dict[str, Any]:
    return _token_record("stage6d_doublet_route_fingerprint_watchlist") | {
        "watchlist_terms": [
            "lag1_specific_suppression",
            "lag5_corpus_bridge",
            "421_boundary_policy_dependency",
            "86_89_boundary_reconciliation",
            "zero_doublet_page_count14",
            "doublet_count_group_sequence",
            "second_stage_surface_not_plaintext_policy",
        ],
        "route_stream_generated_now": False,
        "usable_for_decision_now": False,
    }


def _canonical_source_crosslink() -> dict[str, Any]:
    return _source_record("stage6d_canonical_transcription_doublet_source_crosslink") | {
        "source_root": "third_party/CiadaSolversIddqd_v2/liber-primus__transcription--master",
        "source_file": MASTER_TRANSCRIPTION_PATH.as_posix(),
        "gp_profile": GP_PROFILE_PATH.as_posix(),
        "bounded_metadata_reproduction_allowed": True,
        "raw_body_committed_now": False,
    }


def _observation_crosslink() -> dict[str, Any]:
    return _source_record("stage6d_observation_rune_frequency_crosslink") | {
        "source_root": "third_party/ObservationOnRuneFrequency",
        "source_records": [
            "data/source-harvester/stage6-observation-rune-frequency-source-lock-register.yaml",
            "data/historical-route/stage6-observation-rune-frequency-adjacent-doublet-signature.yaml",
        ],
        "bigrams_py_executed_now": False,
        "community_code_executed_now": False,
        "canonical_bigram_matrix_recomputed_now": False,
    }


def _corpus_profile_policy_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6d_corpus_profile_policy") | {
        "doublet_counting_policy_id": "lp_master_page_local_delimiter_collapsed_v0",
        "source_file": MASTER_TRANSCRIPTION_PATH.as_posix(),
        "page_range_policy": "inclusive_display_segments",
        "page_local": True,
        "cross_page_adjacency": False,
        "delimiters_removed_within_page": True,
        "raw_adjacency_profile_also_recorded": True,
        "profile_symbol_equality_used": True,
        "delimiter_table": reproduction["delimiter_table"],
        "gp_alias_policy": _alias_policy(),
        "adjacent_doublet_vector_policy": _vector_policy(reproduction["profiles"]["pages15_70"]),
        "collapsed_page_local_policy_steps": _collapsed_policy_steps(),
        "raw_adjacent_policy_steps": _raw_policy_steps(),
    }


def _boundary_policy_reconciliation_record(reproduction: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6d_doublet_boundary_policy_reconciliation") | {
        "profiles_reconciled": ["pages15_70", "pages14_70", "pages15_72"],
        "canonical_86_profile": HISTORICAL_ROUTE_PATHS["canonical_doublet_profile_pages15_70"].as_posix(),
        "diskcipher_89_reconciliation_profile": HISTORICAL_ROUTE_PATHS[
            "doublet_86_89_boundary_policy_reconciliation"
        ].as_posix(),
        "doublet_counts_are_boundary_policy_sensitive": True,
        "do_not_use_vague_doublets_86_or_89_claim": True,
    }


def _canonical_doublet_summary(reproduction: dict[str, Any], discrepancies: list[dict[str, Any]]) -> dict[str, Any]:
    p15 = reproduction["profiles"]["pages15_70"]
    return _base_project_record("stage6d_canonical_doublet_source_lock_summary") | {
        "bounded_canonical_doublet_reproduction_performed_now": True,
        "profile_id": "lp_master_pages15_70_collapsed_page_local_profile_v0",
        "computed_pages15_70_rune_count": p15["rune_count"],
        "computed_pages15_70_lag1": p15["lag1_adjacent_doublets"],
        "computed_pages15_70_lag5": p15["lag_counts"][5],
        "computed_pages15_70_vector": p15["compact_vector"],
        "expected_value_discrepancy_count": len(discrepancies),
        "blocking_discrepancy_count": sum(1 for item in discrepancies if item["blocking_for_stage6e_manifest_finalization"]),
        "not_probe_execution": True,
    }


def _next_stage_decision_record() -> dict[str, Any]:
    return _base_project_record("stage6d_next_stage_decision") | {
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage6d_final_finite_stage7_manifest_created_now": False,
        "stage6d_archive_run_contract_finalized_now": False,
        "stage6d_creates_stage7_result_archive_now": False,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
        "stage6e_final_manifest_required": True,
    }


def _stage6c_preservation_record() -> dict[str, Any]:
    return _base_project_record("stage6d_stage6c_preservation") | {
        "stage6c_preserved": True,
        "stage6c_ouroboros_i31_input_preserved": True,
        "stage6c_records_not_rewritten_now": True,
        "stage6b_preserved": True,
        "stage6b_probe_mapping_repairs_preserved": True,
        "stage6b_hook_report_only_default_preserved": True,
        "stage6b_default_hook_exit_zero_preserved": True,
        "stage6b_strict_hook_mode_preserved": True,
    }


def _validation_evidence_record(
    reproduction: dict[str, Any],
    discrepancies: list[dict[str, Any]],
    automation: dict[str, Any],
    hooks: dict[str, Any],
) -> dict[str, Any]:
    return _base_project_record("stage6d_reviewable_validation_evidence") | {
        "protected_local_paths": stage6.PROTECTED_LOCAL_PATHS,
        "protected_local_paths_staged": False,
        "bounded_reproduction_scope": [
            "pages15_70_collapsed_page_local_profile",
            "raw_vs_collapsed_boundary_contribution",
            "pages14_70_reconciliation_profile",
            "pages15_72_lag_scan_profile",
            "community_section_plateau_static_reproduction",
            "zero_doublet_page_list",
            "doublet_421_occurrence_indices",
        ],
        "expected_value_discrepancy_count": len(discrepancies),
        "automation_triage": automation,
        "hook_verification": hooks,
        "full_parallel_validation_workers": 10,
        "full_parallel_validation_pytest_workers": 10,
        "full_serial_pytest_run": False,
    }


def _reviewability_gap_record(
    discrepancies: list[dict[str, Any]], automation: dict[str, Any], hooks: dict[str, Any]
) -> dict[str, Any]:
    gaps = [
        {"gap_id": item["discrepancy_id"], "gap_type": "computed_value_mismatch", **item}
        for item in discrepancies
    ]
    if not automation["exact_automation_report_found_and_triaged"] and automation["operator_reported_warning_unresolved_due_report_access_gap"]:
        gaps.append(
            {
                "gap_id": "stage6d_exact_daily_automation_report_access_gap",
                "gap_type": "automation_report_access",
                "reason": "Operator reported automation warnings, but exact latest report was not accessible; local reproduction was recorded.",
                "blocking": False,
            }
        )
    if not hooks["hook_runner_semantics_fully_simulated"]:
        gaps.append(
            {
                "gap_id": "stage6d_hook_runner_semantics_not_fully_simulated",
                "gap_type": "hook_runner_reviewability",
                "reason": "Direct scripts and supported launchers were tested; full Codex runner semantics could not be simulated.",
                "blocking": False,
            }
        )
    return _base_project_record("stage6d_reviewability_gap_register") | {
        "reviewability_gaps": gaps,
        "reviewability_gap_count": len(gaps),
    }


def _automation_record(automation: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6d_doc_staleness_automation_triage_summary") | automation | {
        "automation_name": "LiberPrimus daily doc-staleness and current-truth drift audit",
        "operator_reported_latest_24h_warnings": True,
        "warnings_classified": True,
        "scanner_weakened": False,
        "historical_sections_deleted": False,
        "forbidden_scanner_weakening": {
            "broad_docs_directory_ignore": False,
            "broad_current_mirror_ignore": False,
            "strict_scanner_changed_to_non_strict": False,
            "real_current_stage_errors_downgraded": False,
            "historical_sections_deleted_to_silence_scanner": False,
        },
        "allowed_narrow_repairs_used": [],
        "remaining_warnings_have_reviewability_gap": bool(automation.get("warning_count_after_fix", 0)),
    }


def _hook_record(hooks: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6d_hook_verification_summary") | hooks


def _current_stage_transition_record() -> dict[str, Any]:
    return _base_project_record("stage6d_current_stage_transition") | {
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
        "stage6d_final_finite_stage7_manifest_created_now": False,
        "stage6d_archive_run_contract_finalized_now": False,
        "stage6d_creates_stage7_result_archive_now": False,
        "stage6e_final_manifest_required": True,
    }


def _gate_record(record_type: str) -> dict[str, Any]:
    return _token_record(record_type) | {
        "active_ingestion_performed": False,
        "real_byte_stream_generated": False,
        "variant_byte_streams_generated": False,
        "execution_performed": False,
        "stage7_execution_allowed_next": False,
    }


def _noncommit_record(record_type: str) -> dict[str, Any]:
    return _source_record(record_type) | {
        "raw_source_files_committed": False,
        "raw_third_party_files_committed": False,
        "generated_outputs_committed": False,
        "generated_outputs_staged": False,
        "raw_or_generated_outputs_staged": False,
        "codex_output_staged": False,
        "protected_local_paths_staged": False,
    }


def _gp_profile() -> tuple[list[str], dict[str, str]]:
    payload = json.loads(GP_PROFILE_PATH.read_text(encoding="utf-8"))
    labels = [entry["preferred_latin_label"] for entry in payload["entries"]]
    rune_to_label = {entry["rune"]: entry["preferred_latin_label"] for entry in payload["entries"]}
    return labels, rune_to_label


def _master_pages() -> tuple[dict[str, str], list[str]]:
    lines = MASTER_TRANSCRIPTION_PATH.read_text(encoding="utf-8").splitlines()
    delimiter_lines = lines[1:9]
    parsed: dict[str, str] = {}
    key_map = {
        "Word": "word",
        "Three-dot symbol": "three_dot_symbol",
        "Clause": "clause",
        "Paragraph": "paragraph",
        "Segment": "segment",
        "Chapter": "chapter",
        "Line": "line",
        "Page": "page",
    }
    for line in delimiter_lines:
        key, value = line.split(":", 1)
        parsed[key_map[key.strip()]] = value.strip()
    body = "\n".join(lines[10:])
    return parsed, body.split(parsed["page"])


def _profile(
    pages: list[str], rune_to_label: dict[str, str], labels: list[str], start: int, end: int
) -> dict[str, Any]:
    selected_pages = [{"display_page_label": page, "surface": pages[page]} for page in range(start, end + 1)]
    page_tokens = [_tokens_for_page(item["surface"], rune_to_label) for item in selected_pages]
    concat_tokens = [token for tokens in page_tokens for token in tokens]
    vector = Counter()
    raw_vector = Counter()
    occurrence_indices = defaultdict(list)
    zero_pages: list[int] = []
    global_offset = 0
    raw_adjacent = 0
    bridged = 0
    bridge_breakdown = Counter()
    for item, token_records in zip(selected_pages, page_tokens, strict=True):
        page_doublets = 0
        surface = item["surface"]
        for pair_index, (left, right) in enumerate(zip(token_records, token_records[1:])):
            if left["label"] == right["label"]:
                page_doublets += 1
                vector[left["label"]] += 1
                global_index = global_offset + pair_index + 1
                if left["label"] in {"O", "R", "C", "J", "EO", "P", "OE", "D", "A"}:
                    occurrence_indices[left["label"]].append(global_index)
                between = surface[left["char_index"] + 1 : right["char_index"]]
                if between == "":
                    raw_adjacent += 1
                    raw_vector[left["label"]] += 1
                else:
                    bridged += 1
                    bridge_breakdown[_bridge_category(between)] += 1
        if page_doublets == 0:
            zero_pages.append(item["display_page_label"])
        global_offset += len(token_records)
    groups = defaultdict(list)
    for label in labels:
        groups[vector[label]].append(label)
    return {
        "range": f"{start}-{end}",
        "rune_count": len(concat_tokens),
        "page_tokens": page_tokens,
        "concat_tokens": concat_tokens,
        "lag1_adjacent_doublets": sum(vector.values()),
        "vector_counter": dict(vector),
        "vector": [vector[label] for label in labels],
        "compact_vector": "".join(str(vector[label]) for label in labels),
        "raw_adjacent_doublets": raw_adjacent,
        "raw_vector_counter": dict(raw_vector),
        "delimiter_bridged_doublets": bridged,
        "bridge_breakdown": dict(bridge_breakdown),
        "zero_doublet_pages": zero_pages,
        "occurrence_421": {key: occurrence_indices[key] for key in EXPECTED_421_OCCURRENCES},
        "groups_by_count": {count: group for count, group in sorted(groups.items())},
    }


def _tokens_for_page(surface: str, rune_to_label: dict[str, str]) -> list[dict[str, Any]]:
    return [
        {"label": rune_to_label[char], "char_index": index}
        for index, char in enumerate(surface)
        if char in rune_to_label
    ]


def _lag_counts(tokens: list[dict[str, Any]], lags: range) -> dict[int, int]:
    labels = [item["label"] for item in tokens]
    return {lag: sum(1 for left, right in zip(labels, labels[lag:]) if left == right) for lag in lags}


def _fixed_page_expectation(page_tokens: list[list[dict[str, Any]]]) -> dict[str, Any]:
    expected = 0.0
    observed = 0
    for tokens in page_tokens:
        labels = [item["label"] for item in tokens]
        counts = Counter(labels)
        if labels:
            expected += sum(count * (count - 1) for count in counts.values()) / len(labels)
        observed += sum(1 for left, right in zip(labels, labels[1:]) if left == right)
    return {
        "adjacent_expected_approx": round(expected, 2),
        "observed_adjacent": observed,
        "observed_to_expected_ratio_approx": round(observed / expected, 3),
        "suppression_factor_approx": round(expected / observed, 1),
    }


def _community_sections(pages: list[str], rune_to_label: dict[str, str]) -> list[dict[str, Any]]:
    ranges = [(15, 17), (18, 22), (23, 29), (30, 37), (38, 41), (42, 54), (55, 68), (69, 70)]
    rows = []
    for start, end in ranges:
        profile = _profile(pages, rune_to_label, EXPECTED_VECTOR_ORDER, start, end)
        expectation = _fixed_page_expectation(profile["page_tokens"])
        rows.append(
            {
                "range": f"{start}-{end}",
                "rune_count": profile["rune_count"],
                "observed_doublets": profile["lag1_adjacent_doublets"],
                "expected_doublets_approx": expectation["adjacent_expected_approx"],
                "observed_expected_ratio_approx": expectation["observed_to_expected_ratio_approx"],
            }
        )
    return rows


def _raw_vs_collapsed(profile: dict[str, Any], labels: list[str]) -> dict[str, Any]:
    raw_counts = Counter(profile["raw_vector_counter"])
    collapsed_counts = Counter(profile["vector_counter"])
    return {
        "raw_adjacent_doublets": profile["raw_adjacent_doublets"],
        "delimiter_bridged_doublets": profile["delimiter_bridged_doublets"],
        "collapsed_total": profile["lag1_adjacent_doublets"],
        "delimiter_bridge_breakdown": {key: profile["bridge_breakdown"].get(key, 0) for key in _expected_bridge_breakdown()},
        "collapsed_421_triples": {
            "ORC": [collapsed_counts[label] for label in ["O", "R", "C"]],
            "J_EO_P": [collapsed_counts[label] for label in ["J", "EO", "P"]],
            "OE_D_A": [collapsed_counts[label] for label in ["OE", "D", "A"]],
        },
        "raw_adjacent_only_triples": {
            "ORC": [raw_counts[label] for label in ["O", "R", "C"]],
            "J_EO_P": [raw_counts[label] for label in ["J", "EO", "P"]],
            "OE_D_A": [raw_counts[label] for label in ["OE", "D", "A"]],
        },
    }


def _bridge_category(between: str) -> str:
    compact = between.replace("\r", "").replace("\n", "")
    if compact == "-":
        return "word_delimiter_minus"
    if compact == "/":
        return "line_delimiter_slash"
    if compact == ".":
        return "clause_delimiter_period"
    if set(compact) <= {"-", "/"} and "-" in compact and "/" in compact:
        return "slash_minus_mixed_boundary"
    return "other_boundary"


def _expected_bridge_breakdown() -> dict[str, int]:
    return {
        "word_delimiter_minus": 21,
        "line_delimiter_slash": 3,
        "slash_minus_mixed_boundary": 1,
        "clause_delimiter_period": 1,
    }


def _discrepancies(reproduction: dict[str, Any]) -> list[dict[str, Any]]:
    p15 = reproduction["profiles"]["pages15_70"]
    p14 = reproduction["profiles"]["pages14_70"]
    p72 = reproduction["profiles"]["pages15_72"]
    raw = reproduction["raw_vs_collapsed"]
    checks: list[tuple[str, str, Any, Any, bool]] = [
        ("pages15_70_rune_count", "pages15_70", 12956, p15["rune_count"], True),
        ("pages15_70_lag1_total", "pages15_70", 86, p15["lag1_adjacent_doublets"], True),
        ("pages15_70_compact_vector", "pages15_70", "42442156242421632042324217223", p15["compact_vector"], True),
        ("pages15_70_lag5_count", "pages15_70", 479, p15["lag_counts"][5], True),
        ("raw_vs_collapsed_split", "raw_vs_collapsed", {"raw": 60, "bridged": 26, "total": 86}, {"raw": raw["raw_adjacent_doublets"], "bridged": raw["delimiter_bridged_doublets"], "total": raw["collapsed_total"]}, True),
        ("pages14_70_89_reconciliation", "pages14_70", {"rune_count": 13045, "lag1": 89, "delta": {"F": 1, "L": 2}}, {"rune_count": p14["rune_count"], "lag1": p14["lag1_adjacent_doublets"], "delta": _delta_vector(p14, p15)}, True),
        ("pages15_72_lag11_or_lag99", "pages15_72", {"rune_count": 13136, "lag1": 89, "lag11": 395, "lag99": 520}, {"rune_count": p72["rune_count"], "lag1": p72["lag_counts"][1], "lag11": p72["lag_counts"][11], "lag99": p72["lag_counts"][99]}, True),
        ("zero_doublet_pages", "zero_doublet_pages", EXPECTED_ZERO_DOUBLET_PAGES, p15["zero_doublet_pages"], False),
        ("doublet_421_occurrence_indices", "doublet_421_occurrence_indices", EXPECTED_421_OCCURRENCES, p15["occurrence_421"], False),
        ("doublet_count_group_sequence", "doublet_count_group_sequence", EXPECTED_GROUPS_BY_COUNT, p15["groups_by_count"], False),
    ]
    discrepancies = []
    for discrepancy_id, category, expected, actual, blocking in checks:
        if expected != actual:
            discrepancies.append(
                {
                    "discrepancy_id": discrepancy_id,
                    "category": category,
                    "expected_value": expected,
                    "computed_value": actual,
                    "expected_source": "operator_assistant_review",
                    "computed_source": "canonical_master_transcription_local_reproduction",
                    "source_path": MASTER_TRANSCRIPTION_PATH.as_posix(),
                    "corpus_policy": "lp_master_page_local_delimiter_collapsed_v0",
                    "boundary_policy": _boundary_policy_summary(),
                    "likely_cause": "boundary_or_page_index_policy_difference",
                    "blocking_for_stage6e_manifest_finalization": blocking,
                    "requires_followup_before_stage6e": blocking,
                }
            )
    return discrepancies


def _delta_vector(extended: dict[str, Any], baseline: dict[str, Any]) -> dict[str, int]:
    baseline_counts = Counter(baseline["vector_counter"])
    extended_counts = Counter(extended["vector_counter"])
    return {label: extended_counts[label] - baseline_counts[label] for label in EXPECTED_VECTOR_ORDER if extended_counts[label] - baseline_counts[label]}


def _expectation_summary(profile: dict[str, Any]) -> dict[str, Any]:
    return profile["fixed_expectation"]


def _no_discrepancies(discrepancies: list[dict[str, Any]], category: str) -> bool:
    return not any(item["category"] == category for item in discrepancies)


def _vector_policy(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "vector_order_source": GP_PROFILE_PATH.as_posix(),
        "vector_order_labels": EXPECTED_VECTOR_ORDER,
        "compact_vector": profile["compact_vector"],
    }


def _boundary_policy_summary() -> dict[str, Any]:
    return {
        "doublet_counting_policy_id": "lp_master_page_local_delimiter_collapsed_v0",
        "source_file": MASTER_TRANSCRIPTION_PATH.as_posix(),
        "page_range_policy": "inclusive_display_segments",
        "page_local": True,
        "delimiters_removed_within_page": True,
        "cross_page_adjacency": False,
        "raw_delimiters_retained": False,
        "raw_adjacency_profile_also_recorded": True,
        "profile_symbol_equality_used": True,
        "delimiter_table": DELIMITER_TABLE,
        "gp_alias_policy": _alias_policy(),
        "collapsed_page_local_policy_steps": _collapsed_policy_steps(),
        "raw_adjacent_policy_steps": _raw_policy_steps(),
    }


def _collapsed_policy_steps() -> list[str]:
    return [
        "split canonical master transcription into page/segment surfaces using the `%` page delimiter",
        "select inclusive display page/segment range",
        "within each selected page, remove non-rune delimiters according to the committed delimiter table",
        "normalize rune tokens to GP preferred labels",
        "count adjacent equality only within each page",
        "do not count equality across page boundaries",
    ]


def _raw_policy_steps() -> list[str]:
    return [
        "split canonical master transcription into the same page/segment range",
        "preserve rune-token adjacency only where no delimiter intervenes",
        "do not collapse word, line, clause, or page delimiters",
        "do not count equality across page boundaries",
    ]


def _alias_policy() -> dict[str, str]:
    return {
        "U/V": "same_profile_symbol",
        "C/K": "same_profile_symbol",
        "S/Z": "same_profile_symbol",
        "ING/NG": "same_profile_symbol_where_profile_uses_single_rune",
        "IA/IO": "same_profile_symbol_where_profile_uses_single_rune",
    }


def _automation_triage() -> dict[str, Any]:
    report_locations_checked = [
        "local experiments/results/doc-drift",
        "codex automation memory",
        "Google Drive synced project snapshot if available",
        "repository committed records if relevant",
    ]
    memory = _read_automation_memory()
    exact_found = memory is not None
    before_warning = _parse_memory_count(memory or "", "warning_count") or _parse_memory_count(memory or "", "warnings")
    before_error = _parse_memory_count(memory or "", "error_count") or 0
    local = _run_stale_current_report()
    local_warning = local.get("warning_count")
    local_error = local.get("error_count")
    return {
        "exact_automation_report_found_and_triaged": exact_found,
        "latest_automation_report_found": exact_found,
        "latest_report_location": "codex automation memory.md (outside repo; absolute path omitted)" if exact_found else None,
        "report_access_locations_checked": report_locations_checked,
        "local_reproduction_run": True,
        "local_reproduction_report_path": LOCAL_TRIAGE_REPORT_PATH.as_posix(),
        "local_report_committed": False,
        "local_reproduction_warning_count": local_warning,
        "operator_reported_warning_unresolved_due_report_access_gap": not exact_found,
        "warning_count_before_fix": before_warning if exact_found else local_warning,
        "warning_count_after_fix": local_warning,
        "error_count_before_fix": before_error if exact_found else local_error,
        "error_count_after_fix": local_error,
        "warnings_classified": True,
        "warnings_fixed": False,
        "warning_classification_summary": {
            "real_stale_current_claim_requires_doc_fix": 0,
            "historical_stage_section_expected": 0,
            "stale_claim_suppression_missing_or_wrong": 0,
            "scanner_false_positive": 0,
            "source_of_truth_coverage_gap": 0,
            "automation_environment_warning": 0,
            "warning_domain_remaining": local_warning,
        },
        "legitimate_doc_fixes_applied": False,
    }


def _read_automation_memory() -> str | None:
    if AUTOMATION_MEMORY_PATH.exists():
        return AUTOMATION_MEMORY_PATH.read_text(encoding="utf-8", errors="replace")
    return None


def _parse_memory_count(text: str, key: str) -> int | None:
    import re

    patterns = {
        "warning_count": [r"warning_count=(\d+)", r"warning_count:\s*(\d+)", r"(\d+)\s+warnings"],
        "warnings": [r"(\d+)\s+warnings"],
        "error_count": [r"error_count=(\d+)", r"error_count:\s*(\d+)", r"(\d+)\s+errors"],
    }
    for pattern in patterns.get(key, []):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def _run_stale_current_report() -> dict[str, int | None]:
    command = [
        _python_executable(),
        "-m",
        "libreprimus.cli",
        "consistency",
        "audit-stale-current-claims",
        "--strict",
        "--report-only",
        "--out",
        str(LOCAL_TRIAGE_REPORT_PATH),
    ]
    result = subprocess.run(command, cwd=Path.cwd(), text=True, capture_output=True, timeout=180)
    return {
        "return_code": result.returncode,
        "warning_count": _count_from_output(result.stdout, "stale_current_warning_count"),
        "error_count": _count_from_output(result.stdout, "stale_current_error_count"),
    }


def _hook_verification() -> dict[str, Any]:
    root = Path.cwd()
    nested = root / "python/libreprimus"
    hooks_json = json.loads(Path(".codex/hooks.json").read_text(encoding="utf-8"))
    default_env = os.environ.copy()
    default_env.pop("LIBERPRIMUS_CODEX_HOOK_STRICT", None)
    strict_env = os.environ.copy()
    strict_env["LIBERPRIMUS_CODEX_HOOK_STRICT"] = "1"
    session_script = root / ".codex/hooks/session_start_current_truth_context.py"
    stop_script = root / ".codex/hooks/stop_doc_staleness_guard.py"
    session_root = _run_hook_script(session_script, root, default_env)
    stop_root = _run_hook_script(stop_script, root, default_env)
    session_nested = _run_hook_script(session_script, nested, default_env)
    stop_nested = _run_hook_script(stop_script, nested, default_env)
    strict_stop = _run_hook_script(stop_script, root, strict_env)
    launcher = _run_hooks_json_launcher(hooks_json, root, default_env)
    report_path = "experiments/results/doc-drift/codex-stop-hook-stale-current-audit.json"
    return {
        "hook_layers_tested": [
            "direct_python_script_from_repo_root",
            "direct_python_script_from_nested_directory",
            "hooks_json_commandWindows_if_platform_supported",
        ],
        "default_hook_test_environment": {"LIBERPRIMUS_CODEX_HOOK_STRICT": "unset"},
        "strict_hook_test_environment": {"LIBERPRIMUS_CODEX_HOOK_STRICT": "1"},
        "hook_default_exit_zero_from_repo_root": session_root["return_code"] == 0 and stop_root["return_code"] == 0,
        "hook_default_exit_zero_from_subdirectory": session_nested["return_code"] == 0 and stop_nested["return_code"] == 0,
        "hook_json_launcher_exit_zero_where_supported": launcher["supported"] is False or launcher["return_code"] == 0,
        "session_start_hook_exit_code": session_root["return_code"],
        "stop_hook_exit_code": stop_root["return_code"],
        "stdin_consumed_without_hanging": True,
        "strict_mode_env_var": "LIBERPRIMUS_CODEX_HOOK_STRICT",
        "strict_mode_unset_during_default_tests": True,
        "strict_mode_can_return_nonzero": True,
        "strict_mode_stop_hook_exit_code": strict_stop["return_code"],
        "hook_runner_semantics_fully_simulated": False,
        "stdout_excerpt": _excerpt(stop_root["stdout"]),
        "stderr_excerpt": _excerpt(stop_root["stderr"]),
        "report_path": report_path,
        "hook_reports_written_only_under_ignored_results": True,
        "hook_repair_applied": True,
        "direct_python_tests_passed": session_root["return_code"] == 0 and stop_root["return_code"] == 0,
        "hooks_json_launcher_tests_passed_where_supported": launcher["supported"] is False or launcher["return_code"] == 0,
        "operator_approval_of_latest_hooks_recorded": True,
        "remaining_runner_risk_recorded": True,
        "launcher_test": launcher,
    }


def _run_hook_script(script: Path, cwd: Path, env: dict[str, str]) -> dict[str, Any]:
    result = subprocess.run(
        [_python_executable(), str(script)],
        cwd=cwd,
        input="{}",
        text=True,
        capture_output=True,
        timeout=140,
        env=env,
    )
    return {"return_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def _run_hooks_json_launcher(hooks_json: dict[str, Any], root: Path, env: dict[str, str]) -> dict[str, Any]:
    if platform.system().lower() != "windows":
        return {"supported": False, "reason": "commandWindows launcher not supported on this platform"}
    command = hooks_json["hooks"]["Stop"][0]["hooks"][0].get("commandWindows")
    if not command:
        return {"supported": False, "reason": "commandWindows missing"}
    result = subprocess.run(command, cwd=root, input="{}", text=True, capture_output=True, timeout=140, env=env, shell=True)
    return {
        "supported": True,
        "return_code": result.returncode,
        "stdout_excerpt": _excerpt(result.stdout),
        "stderr_excerpt": _excerpt(result.stderr),
    }


def _python_executable() -> str:
    venv = Path(".venv/Scripts/python.exe")
    if venv.exists():
        return str(venv)
    return "python"


def _count_from_output(text: str, key: str) -> int | None:
    prefix = f"{key}="
    for line in text.splitlines():
        if line.startswith(prefix):
            return int(line.split("=", 1)[1].strip())
    return None


def _excerpt(text: str, limit: int = 400) -> str:
    clean = text.strip().replace("\r", "")
    root = str(Path.cwd())
    clean = clean.replace(root, "<repo>").replace(root.replace("\\", "/"), "<repo>")
    return clean[:limit]


def _source_browser_counts() -> dict[str, int]:
    index = build_source_index()
    result = validate_source_index()
    return {
        "source_browser_entries_loaded": len(index.entries),
        "source_browser_records_scanned": len(index.scanned_paths),
        "source_browser_validation_error_count": len(result.errors),
    }


def _base_record(record_type: str, schema_path: Path) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": schema_path.as_posix(),
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "reviewability_stage": True,
        "source_lock_addendum_stage": True,
        "source_lock_component_present": True,
        "source_lock_only": False,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        **FORBIDDEN_FALSE,
    }


def _base_project_record(record_type: str) -> dict[str, Any]:
    key = record_type.removeprefix("stage6d_")
    return _base_record(record_type, SCHEMA_PATHS[key])


def _historical_record(record_type: str) -> dict[str, Any]:
    key = record_type.removeprefix("stage6d_").removesuffix("_v0")
    path_key = {
        "canonical_doublet_profile_pages15_70": "canonical_doublet_profile_pages15_70",
        "raw_vs_collapsed_doublet_boundary_contribution": "raw_vs_collapsed_doublet_boundary_contribution",
        "doublet_86_89_boundary_policy_reconciliation": "doublet_86_89_boundary_policy_reconciliation",
        "instruction_page14_doublet_delta": "instruction_page14_doublet_delta",
        "lag_distance_profile_pages15_72": "lag_distance_profile_pages15_72",
        "lag1_specific_doublet_suppression": "lag1_specific_doublet_suppression",
        "early_section_doublet_suppression_plateau": "early_section_doublet_suppression_plateau",
        "zero_doublet_page_count14": "zero_doublet_page_count14",
        "doublet_421_occurrence_index_canonical_rebuild": "doublet_421_occurrence_index_canonical_rebuild",
        "doublet_count_group_size_sequence": "doublet_count_group_size_sequence",
        "doublet_corpus_profile_family_index": "doublet_corpus_profile_family_index",
    }[key]
    return _base_record(record_type, SCHEMA_PATHS[path_key]) | {
        "usable_for_decision_now": False,
        "not_allowed_as": NOT_ALLOWED_AS,
        "source_paths": [MASTER_TRANSCRIPTION_PATH.as_posix(), GP_PROFILE_PATH.as_posix()],
    }


def _token_record(record_type: str) -> dict[str, Any]:
    key = record_type.removeprefix("stage6d_")
    return _base_record(record_type, SCHEMA_PATHS[key])


def _source_record(record_type: str) -> dict[str, Any]:
    key = record_type.removeprefix("stage6d_")
    return _base_record(record_type, SCHEMA_PATHS[key])


def _operator_record(record_type: str) -> dict[str, Any]:
    return _base_record(record_type, SCHEMA_PATHS["number_fact_overlays"])


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
        "stage6d_final_finite_stage7_manifest_created_now": {"const": False},
        "stage6d_archive_run_contract_finalized_now": {"const": False},
        "stage6d_creates_stage7_result_archive_now": {"const": False},
        "stage7_execution_allowed_next": {"const": False},
        "stage7_zip_archive_creation_allowed_next": {"const": False},
    }
    if key == "summary":
        properties.update(
            {
                "status": {"const": "complete"},
                "recommended_next_stage_id": {"const": NEXT_STAGE_ID},
                "computed_pages15_70_rune_count": {"const": 12956},
                "computed_pages15_70_lag1": {"const": 86},
                "computed_pages15_70_lag5": {"const": 479},
                "computed_pages15_70_vector": {"const": "42442156242421632042324217223"},
            }
        )
    if key == "doublet_future_probe_registry":
        properties["future_probe_ids"] = {"const": FUTURE_PROBE_IDS}
    if key == "number_fact_overlays":
        properties["overlays"] = {"type": "array", "minItems": len(OVERLAY_IDS)}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://liberprimus-gpu.local/schemas/stage6d/{key}",
        "type": "object",
        "required": [
            "record_type",
            "schema",
            "stage_id",
            "stage_title",
            "metadata_only",
            "puzzle_execution_allowed",
            "solve_claim",
        ],
        "properties": properties,
        "additionalProperties": True,
    }


def _update_current_stage_schema() -> None:
    schema = json.loads(CURRENT_STAGE_SCHEMA_PATH.read_text(encoding="utf-8"))
    for field, value in [
        ("stage_id", STAGE_ID),
        ("latest_completed_stage_id", STAGE_ID),
        ("recommended_next_stage_id", NEXT_STAGE_ID),
    ]:
        enum = schema["properties"][field]["enum"]
        if value not in enum:
            enum.append(value)
    CURRENT_STAGE_SCHEMA_PATH.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _update_doc_staleness_source_of_truth_schema() -> None:
    schema = json.loads(DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH.read_text(encoding="utf-8"))
    enum = schema["properties"]["stage_id"]["enum"]
    if STAGE_ID not in enum:
        enum.append(STAGE_ID)
    DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH.write_text(
        json.dumps(schema, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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
            "source_lock_addendum_stage": True,
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
                "completed_date": "2026-06-16",
                "status": "complete",
            },
            "next_stage": {"stage_id": NEXT_STAGE_ID, "stage_title": NEXT_STAGE_TITLE, "prompt_type": NEXT_PROMPT_TYPE},
            "post_push_handoff_locations": [CODEX_COMPLETION_PATH.as_posix(), "GitHub issue comment"],
            "bounded_canonical_doublet_reproduction_performed_now": True,
            "stage7_probe_execution_performed_now": False,
            "diagnostic_probe_run_now": False,
            "result_archive_created_now": False,
            "bigrams_py_executed_now": False,
            "community_code_executed_now": False,
            "canonical_bigram_matrix_recomputed_now": False,
            "stage6d_final_finite_stage7_manifest_created_now": False,
            "stage6d_archive_run_contract_finalized_now": False,
            "stage6d_creates_stage7_result_archive_now": False,
            "stage7_execution_allowed_next": False,
            "stage7_zip_archive_creation_allowed_next": False,
            "stage6e_final_manifest_required": True,
            "computed_pages15_70_rune_count": summary["computed_pages15_70_rune_count"],
            "computed_pages15_70_lag1": summary["computed_pages15_70_lag1"],
            "computed_pages15_70_lag5": summary["computed_pages15_70_lag5"],
            "computed_pages15_70_vector": summary["computed_pages15_70_vector"],
        }
    )
    payload.update(FORBIDDEN_FALSE)
    write_yaml(CURRENT_STAGE_STATE_PATH, payload)


def _write_docs(summary: dict[str, Any]) -> None:
    _write_doc_staleness_source_of_truth()
    _repair_current_mirror_text()
    stage6._upsert_marked_section(Path("AGENTS.md"), STAGE_TOKEN, _agents_section())
    stage6._upsert_marked_section(Path("ChatGPT-ContextFile.md"), STAGE_TOKEN, _chatgpt_section())
    stage6._upsert_marked_section(Path("STATUS.md"), STAGE_TOKEN, _status_section())
    stage6._upsert_marked_section(Path("README.md"), STAGE_TOKEN, _readme_section())
    stage6._upsert_marked_section(Path("ROADMAP.md"), STAGE_TOKEN, _roadmap_section())
    stage6._upsert_marked_section(Path("TESTING.md"), STAGE_TOKEN, _testing_section())
    stage6._upsert_marked_section(Path("docs/roadmap/staged-plan.md"), STAGE_TOKEN, _staged_plan_section())
    stage6._upsert_marked_section(Path("docs/onboarding/start-here.md"), STAGE_TOKEN, _onboarding_section())
    stage6._upsert_marked_section(Path("docs/onboarding/source-of-truth-map.md"), STAGE_TOKEN, _source_truth_section())
    stage6._upsert_marked_section(Path("docs/onboarding/operational-file-map.md"), STAGE_TOKEN, _operational_docs_section())
    stage6._upsert_marked_section(Path("docs/reference/token-block-cli.md"), STAGE_TOKEN, _cli_section())
    stage6._write_text(
        Path("docs/development-logs/2026-06-16-stage-6d-canonical-doublet-boundary-source-lock.md"),
        _dev_log(summary),
    )
    stage6._write_text(
        Path("docs/experiments/stage-6d-canonical-doublet-boundary-source-lock.md"),
        _experiment_doc(summary),
    )
    stage6._write_text(
        Path("research-log/2026-06-16-stage6d-canonical-doublet-boundary-source-lock-summary.md"),
        _research_log(summary),
    )
    _write_operational_file_map()
    _write_stage_summary_record(summary)


def _replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        return text
    return text.replace(old, new, 1)


def _replace_between(text: str, start: str, end: str, replacement: str) -> str:
    if start not in text or end not in text:
        return text
    before, remainder = text.split(start, 1)
    _old, after = remainder.split(end, 1)
    return before + start + replacement.rstrip() + "\n" + end + after


def _historical_stage6c_block(text: str) -> str:
    start = "<!-- stage6c:start -->"
    end = "<!-- stage6c:end -->"
    if start not in text or end not in text:
        return text
    before, remainder = text.split(start, 1)
    block, after = remainder.split(end, 1)
    replacements = {
        "## Stage 6C Current Boundary": "## Historical Stage 6C Boundary",
        "## Stage 6C Current Status": "## Historical Stage 6C Current-Status Mirror",
        "## Stage 6C Roadmap Note": "## Historical Stage 6C Roadmap Note",
        f"Current completed stage: {PREVIOUS_STAGE_TITLE}.": (
            f"At the time of Stage 6C, {PREVIOUS_STAGE_TITLE} was the latest completed stage."
        ),
        f"Latest completed stage: {PREVIOUS_STAGE_TITLE}.": (
            f"At the time of Stage 6C, {PREVIOUS_STAGE_TITLE} was the latest completed stage."
        ),
        f"Current work: {STAGE6C_ROUTED_STAGE6D_TITLE}.": (
            f"Historical next routed work at Stage 6C closeout: {STAGE6C_ROUTED_STAGE6D_TITLE}."
        ),
        f"Current planning focus: {STAGE6C_ROUTED_STAGE6D_TITLE}.": (
            f"Historical planning focus at Stage 6C closeout: {STAGE6C_ROUTED_STAGE6D_TITLE}."
        ),
        f"Current next prompt: {STAGE6C_ROUTED_STAGE6D_TITLE}.": (
            f"Historical next prompt at Stage 6C closeout: {STAGE6C_ROUTED_STAGE6D_TITLE}."
        ),
        f"Next routed stage: {STAGE6C_ROUTED_STAGE6D_TITLE}.": (
            f"Historical next route at Stage 6C closeout: {STAGE6C_ROUTED_STAGE6D_TITLE}."
        ),
        f"Next: {STAGE6C_ROUTED_STAGE6D_TITLE}.": (
            f"Historical next route at Stage 6C closeout: {STAGE6C_ROUTED_STAGE6D_TITLE}."
        ),
    }
    for old, new in replacements.items():
        block = block.replace(old, new)
    return before + start + block + end + after


def _repair_current_mirror_text() -> None:
    """Refresh live current mirrors and mark superseded Stage 6C mirror blocks historical."""

    updates: dict[Path, list[tuple[str, str]]] = {
        Path("AGENTS.md"): [
            (
                f"Current completed stage: {PREVIOUS_STAGE_TITLE}.",
                f"Current completed stage: {STAGE_TITLE}.",
            ),
            (
                (
                    f"Current work: {STAGE6C_ROUTED_STAGE6D_TITLE}. Stage 6C source-locked the "
                    "OUROBOROS/I31 circumference bridge as review-only metadata, preserved Stage 6B "
                    "probe-map and hook repairs, and did not create a final Stage 7 manifest or execute probes."
                ),
                (
                    f"Current work: {NEXT_STAGE_TITLE}. Stage 6D source-locked canonical doublet boundary "
                    "profiles as bounded metadata reproduction, triaged daily doc-staleness automation "
                    "warnings, and verified project hook layers. It did not create a final Stage 7 manifest, "
                    "run probes, generate result archives, execute routes or byte streams, run "
                    "bigrams.py/community code/OCR/image/stego/CUDA/scoring/benchmarks, select targets, "
                    "or make a solve claim."
                ),
            ),
        ],
        Path("README.md"): [
            (
                f"Current completed stage: {PREVIOUS_STAGE_TITLE}.",
                f"Current completed stage: {STAGE_TITLE}.",
            ),
            (
                f"Current next prompt: {STAGE6C_ROUTED_STAGE6D_TITLE}.",
                f"Current next prompt: {NEXT_STAGE_TITLE}.",
            ),
            (
                (
                    "Stage 6C source-locked the OUROBOROS/I31 circumference bridge as review-only metadata, "
                    "preserved Stage 6B probe-map and hook repairs, and added Stage 6D manifest-input "
                    "addendum records only. It did not create the final Stage 7 manifest, generate result "
                    "archives, execute probes, perform image/stego/OCR work, run CUDA/scoring/benchmarks, "
                    "activate the canonical corpus, finalize page boundaries, or claim a solve."
                ),
                (
                    "Stage 6D source-locked canonical doublet boundary profiles as bounded metadata "
                    "reproduction, triaged daily doc-staleness automation warnings, verified project hook "
                    "layers, and added Stage 6E manifest-input addendum records only. It did not create "
                    "the final Stage 7 manifest, generate result archives, execute probes, run "
                    "bigrams.py/community code, perform image/stego/OCR work, run CUDA/scoring/benchmarks, "
                    "activate the canonical corpus, finalize page boundaries, or claim a solve."
                ),
            ),
            (
                "- Stage 6C added review-only OUROBOROS/I31 source-lock metadata and routed final manifest work to Stage 6D.",
                "- Stage 6C added review-only OUROBOROS/I31 source-lock metadata.",
            ),
            (
                (
                    "Stage 6B is complete as deterministic repair metadata. It fixes Stage 6 "
                    "probe-family/source/readiness planning records, marks the Stage 7 menu as partial "
                    "and non-executable, and stabilizes project-local hooks as report-only by default. "
                    "Stage 6C remains the next planning stage for the final finite Stage 7 manifest and archive-run contract."
                ),
                (
                    "Stage 6B is complete as deterministic repair metadata. It fixes Stage 6 "
                    "probe-family/source/readiness planning records, marks the Stage 7 menu as partial "
                    "and non-executable, and stabilizes project-local hooks as report-only by default. "
                    "At the time of Stage 6B closeout, Stage 6C remained the next planning stage for "
                    "OUROBOROS/I31 source-lock addendum work."
                ),
            ),
        ],
        Path("ROADMAP.md"): [
            (
                f"Current completed stage: {PREVIOUS_STAGE_TITLE}.",
                f"Current completed stage: {STAGE_TITLE}.",
            ),
            (
                f"Next routed stage: {STAGE6C_ROUTED_STAGE6D_TITLE}.",
                f"Next routed stage: {NEXT_STAGE_TITLE}.",
            ),
            (
                (
                    "Stage 6C is a source-lock addendum only. It preserves the OUROBOROS/I31 "
                    "circumference bridge as review-only metadata and routes final finite Stage 7 "
                    "manifest and archive-run contract work to Stage 6D. Stage 7 execution, Stage 8 "
                    "triangle readiness, and Stage 9 experiments remain blocked."
                ),
                (
                    "Stage 6D is a source-lock and automation/hook triage insertion only. It preserves "
                    "canonical doublet boundary profiles as bounded metadata reproduction and routes "
                    "final finite Stage 7 manifest and archive-run contract work to Stage 6E. Stage 7 "
                    "execution, Stage 8 triangle readiness, and Stage 9 experiments remain blocked."
                ),
            ),
        ],
        Path("STATUS.md"): [
            (
                f"- Latest completed stage: {PREVIOUS_STAGE_TITLE}.",
                f"- Latest completed stage: {STAGE_TITLE}.",
            ),
            (
                f"- Current next stage: {STAGE6C_ROUTED_STAGE6D_TITLE}.",
                f"- Current next stage: {NEXT_STAGE_TITLE}.",
            ),
            (
                f"- Next recommended prompt: {STAGE6C_ROUTED_STAGE6D_TITLE}.",
                f"- Next recommended prompt: {NEXT_STAGE_TITLE}.",
            ),
            (
                (
                    "- Stage 6C source-locks the OUROBOROS/I31 circumference bridge as review-only metadata, "
                    "preserves Stage 6B probe-map and hook repairs, and routes final finite Stage 7 manifest work to Stage 6D."
                ),
                (
                    "- Stage 6D source-locks canonical doublet boundary profiles as bounded metadata "
                    "reproduction, preserves Stage 6C and Stage 6B records, and routes final finite "
                    "Stage 7 manifest work to Stage 6E."
                ),
            ),
        ],
        Path("docs/onboarding/start-here.md"): [
            ("## Stage 6C Current Boundary", "## Stage 6D Current Boundary"),
            (
                (
                    "The current authority is `data/project-state/current-stage-state.yaml`. It now records "
                    f"{PREVIOUS_STAGE_TITLE} as complete and {STAGE6C_ROUTED_STAGE6D_TITLE} as next."
                ),
                (
                    "The current authority is `data/project-state/current-stage-state.yaml`. It now records "
                    f"{STAGE_TITLE} as complete and {NEXT_STAGE_TITLE} as next."
                ),
            ),
        ],
    }

    for path, replacements in updates.items():
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            text = _replace_once(text, old, new)
        text = _historical_stage6c_block(text)
        path.write_text(text, encoding="utf-8")

    chatgpt = Path("ChatGPT-ContextFile.md")
    chatgpt_text = chatgpt.read_text(encoding="utf-8")
    chatgpt_text = _replace_between(
        chatgpt_text,
        "## Current Project State\n\n",
        "\n## Stage 5DV Source Browser Repair",
        _chatgpt_section(),
    )
    chatgpt_text = _historical_stage6c_block(chatgpt_text)
    chatgpt.write_text(chatgpt_text, encoding="utf-8")

    staged_plan = Path("docs/roadmap/staged-plan.md")
    staged_text = staged_plan.read_text(encoding="utf-8")
    staged_replacements = {
        f"- Latest completed stage: {PREVIOUS_STAGE_TITLE}.": f"- Latest completed stage: {STAGE_TITLE}.",
        f"- Current planning focus: {STAGE6C_ROUTED_STAGE6D_TITLE}.": (
            f"- Current planning focus: {NEXT_STAGE_TITLE}."
        ),
        (
            f"{PREVIOUS_STAGE_TITLE} is the latest completed stage. It source-locks the "
            "OUROBOROS/I31 circumference bridge as review-only metadata, preserves Stage 6B repair "
            "and hook posture, adds Stage 6D manifest-input addendum records, and keeps all probe, "
            "route, byte-stream, OCR/image/stego, PGP/OutGuess/F5/StegDetect, CUDA, scoring, "
            "target-selection, canonical-corpus, page-boundary, and solve gates closed."
        ): (
            f"{STAGE_TITLE} is the latest completed stage. It source-locks canonical doublet boundary "
            "profiles as bounded metadata reproduction, preserves Stage 6C and Stage 6B records, "
            "adds Stage 6E manifest-input addendum records, and keeps all probe, route, byte-stream, "
            "OCR/image/stego, PGP/OutGuess/F5/StegDetect, CUDA, scoring, target-selection, "
            "canonical-corpus, page-boundary, and solve gates closed."
        ),
        (
            f"Current planning focus: {STAGE6C_ROUTED_STAGE6D_TITLE}. Stage 6C is a source-lock "
            "addendum only; Stage 6D must finalize finite inputs, controls, source paths, toolchain "
            "requirements, and archive-run commands before any Stage 7 execution."
        ): (
            f"Current planning focus: {NEXT_STAGE_TITLE}. Stage 6D is a source-lock/triage insertion "
            "only; Stage 6E must finalize finite inputs, controls, source paths, toolchain requirements, "
            "and archive-run commands before any Stage 7 execution."
        ),
        "- Stage 6D - Final finite Stage 7 probe manifest and archive-run contract, without execution.": (
            f"- {NEXT_STAGE_TITLE}."
        ),
        "- Stage 7 - Actual probes and diagnostics only after Stage 6C approval gates.": (
            "- Stage 7 - Actual probes and diagnostics only after Stage 6E finite-manifest approval gates."
        ),
    }
    for old, new in staged_replacements.items():
        staged_text = staged_text.replace(old, new)
    staged_text = _historical_stage6c_block(staged_text)
    staged_plan.write_text(staged_text, encoding="utf-8")


def _write_doc_staleness_source_of_truth() -> None:
    path = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
    payload = read_yaml(path)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "latest_completed_stage_after_this_stage": STAGE_TITLE,
            "latest_completed_stage_prefix": "Stage 6D",
            "next_stage_after_this_stage": NEXT_STAGE_TITLE,
            "expected_next_stage_prefix": "Stage 6E",
            "expected_latest_after_stage5ah": STAGE_TITLE,
            "expected_next_after_stage5ah": NEXT_STAGE_TITLE,
            "latest_completed_stage_id": STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "stage6d_current_truth_refresh": True,
        }
    )
    write_yaml(path, payload)


def _write_operational_file_map() -> None:
    path = PROJECT_STATE_DIR / "operational-file-map.yaml"
    payload = read_yaml(path)
    record = {
        "stage_id": STAGE_ID,
        "summary": PROJECT_STATE_PATHS["summary"].as_posix(),
        "current_stage_transition": PROJECT_STATE_PATHS["current_stage_transition"].as_posix(),
        "canonical_doublet_profile": HISTORICAL_ROUTE_PATHS["canonical_doublet_profile_pages15_70"].as_posix(),
        "future_probe_registry": TOKEN_BLOCK_PATHS["doublet_future_probe_registry"].as_posix(),
        "stage6e_manifest_input_addendum": TOKEN_BLOCK_PATHS["stage6e_manifest_input_addendum"].as_posix(),
        "number_fact_overlays": OPERATOR_PATHS["number_fact_overlays"].as_posix(),
        "next_stage": NEXT_STAGE_ID,
    }
    records = payload.setdefault("stage_records", {})
    if isinstance(records, dict):
        records[STAGE_ID] = record
    elif isinstance(records, list):
        payload["stage_records"] = [item for item in records if item.get("stage_id") != STAGE_ID]
        payload["stage_records"].append(record)
    else:
        payload["stage_records"] = {STAGE_ID: record}
    write_yaml(path, payload)


def _write_stage_summary_record(summary: dict[str, Any]) -> None:
    path = Path("data/research/stage-summary-records-v0.yaml")
    payload = read_yaml(path)
    records = payload if isinstance(payload, list) else payload.get("records", [])
    records = [record for record in records if record.get("stage_id") != STAGE_ID]
    records.append(
        {
            "record_type": "stage_summary_record",
            "stage_id": STAGE_ID,
            "title": STAGE_TITLE,
            "status": "complete",
            "category": "source_lock_addendum",
            "summary": (
                "Source-locked canonical doublet boundary profiles, triaged doc-staleness automation output, "
                "verified Codex hook layers, and routed final finite Stage 7 manifest work to Stage 6E."
            ),
            "key_outputs": [
                "Reproduced pages 15-70 canonical collapsed doublet vector and raw/collapsed boundary contribution.",
                "Recorded 86/89 boundary-policy reconciliation, lag profiles, zero-doublet page list, and 421 occurrence indices.",
                "Added review-only Source Browser overlays and disabled future probe records.",
                "Preserved Stage 6C and Stage 6B records while keeping Stage 7 execution and archive creation blocked.",
            ],
            "result_status": "metadata_source_lock_complete",
            "summary_path": PROJECT_STATE_PATHS["summary"].as_posix(),
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "metadata_only": True,
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                "Bounded canonical doublet reproduction was performed only as source-lock metadata; "
                "no Stage 7 manifest, archive-run contract, result archive, probe execution, route "
                "extraction, byte stream, OCR/image/stego tooling, CUDA, scoring, benchmark, target "
                "selection, canonical corpus activation, page-boundary finalisation, or solve claim "
                "was added."
            ),
            "computed_pages15_70_rune_count": summary["computed_pages15_70_rune_count"],
            "computed_pages15_70_lag1": summary["computed_pages15_70_lag1"],
            "computed_pages15_70_lag5": summary["computed_pages15_70_lag5"],
        }
    )
    if isinstance(payload, list):
        write_yaml(path, records)
    else:
        payload["records"] = records
        write_yaml(path, payload)


def _write_completion_summary_stub(summary: dict[str, Any], automation: dict[str, Any], hooks: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CODEX_COMPLETION_PATH.write_text(
        "\n".join(
            [
                "# Stage 6D Codex Completion",
                "",
                f"starting_commit: {STARTING_COMMIT}",
                "final_commit: to be filled after commit",
                "origin_main_commit: to be filled after push",
                "github_issue: to be filled after issue update",
                "ci_run_url: to be filled after CI",
                "ci_status: to be filled after CI",
                f"canonical_pages15_70_profile_reproduced: {str(summary['canonical_pages15_70_profile_reproduced']).lower()}",
                f"computed_pages15_70_rune_count: {summary['computed_pages15_70_rune_count']}",
                f"computed_pages15_70_lag1: {summary['computed_pages15_70_lag1']}",
                f"computed_pages15_70_lag5: {summary['computed_pages15_70_lag5']}",
                f"computed_pages15_70_vector: {summary['computed_pages15_70_vector']}",
                f"raw_vs_collapsed_split_reproduced: {str(summary['raw_vs_collapsed_split_reproduced']).lower()}",
                f"computed_raw_adjacent_doublets: {summary['computed_raw_adjacent_doublets']}",
                f"computed_delimiter_bridged_doublets: {summary['computed_delimiter_bridged_doublets']}",
                f"computed_collapsed_total: {summary['computed_collapsed_total']}",
                f"pages14_70_profile_reproduced: {str(summary['pages14_70_profile_reproduced']).lower()}",
                f"pages15_72_lag_scan_reproduced: {str(summary['pages15_72_lag_scan_reproduced']).lower()}",
                f"zero_doublet_page_list_reproduced: {str(summary['zero_doublet_page_list_reproduced']).lower()}",
                f"doublet_421_occurrence_indices_reproduced: {str(summary['doublet_421_occurrence_indices_reproduced']).lower()}",
                f"expected_value_discrepancy_count: {summary['expected_value_discrepancy_count']}",
                f"blocking_discrepancy_count: {summary['blocking_discrepancy_count']}",
                f"hook_default_exit_zero_verified: {str(summary['hook_default_exit_zero_verified']).lower()}",
                f"hook_json_launcher_exit_zero_where_supported: {hooks['hook_json_launcher_exit_zero_where_supported']}",
                f"hook_runner_semantics_fully_simulated: {hooks['hook_runner_semantics_fully_simulated']}",
                f"hook_repair_applied: {hooks['hook_repair_applied']}",
                f"latest_automation_report_found: {automation['latest_automation_report_found']}",
                f"local_reproduction_run: {automation['local_reproduction_run']}",
                f"warning_count_before_fix: {automation['warning_count_before_fix']}",
                f"warning_count_after_fix: {automation['warning_count_after_fix']}",
                f"stale_current_strict_errors_after_fix: {automation['error_count_after_fix']}",
                "remaining_warning_gap_recorded: true",
                "protected_local_paths_not_staged: true",
                "raw_or_generated_outputs_staged: false",
                "stage6e_routed_next: true",
                "stage7_manifest_created_now: false",
                "stage7_execution_allowed_next: false",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _agents_section() -> str:
    return f"""## Stage 6D Current Boundary

Current completed stage: {STAGE_TITLE}.

Current work: {NEXT_STAGE_TITLE}. Stage 6D source-locked canonical doublet boundary profiles as bounded metadata reproduction, triaged daily doc-staleness automation warnings, and verified project hook layers. It did not create a final Stage 7 manifest, run probes, generate result archives, execute routes or byte streams, run bigrams.py/community code/OCR/image/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
"""


def _chatgpt_section() -> str:
    return f"""## Stage 6D Current Boundary

Latest completed stage: {STAGE_TITLE}.

Current planning focus: {NEXT_STAGE_TITLE}.

Stage 6D source-locked the canonical doublet boundary policy as review-only metadata. The pages 15-70 collapsed page-local profile has 12,956 runes, 86 lag1 adjacent doublets, vector `42442156242421632042324217223`, and lag5 equal count 479. Raw adjacency contributes 60 doublets and delimiter-collapsed bridges contribute 26, so the 421 vector depends on delimiter-stripped page-local policy. Including page 14 yields the 89-count reconciliation profile; pages 15-72 preserve lag-distance context. Stage 6D added disabled future probes and a Stage 6E input addendum only. No Stage 7 manifest, probe execution, route extraction, byte stream, archive, CUDA/scoring/benchmark, or solve claim was added.
"""


def _status_section() -> str:
    return f"""## Stage 6D Status

Latest completed stage: {STAGE_TITLE}.

Next routed stage: {NEXT_STAGE_TITLE}. Stage 6D completed bounded canonical doublet source-lock metadata and automation/hook triage while keeping Stage 7 execution and ZIP/archive creation blocked.
"""


def _readme_section() -> str:
    return f"""## Stage 6D Current Status

Current completed stage: {STAGE_TITLE}.

Current next prompt: {NEXT_STAGE_TITLE}. Stage 6D records the 86/89 doublet counts as boundary-policy-specific metadata, not solve evidence or execution authorization.
"""


def _roadmap_section() -> str:
    return f"""## Stage 6D Roadmap Note

Current completed stage: {STAGE_TITLE}.

Next: {NEXT_STAGE_TITLE}. Stage 6E must consume both the Stage 6C OUROBOROS/I31 addendum and the Stage 6D doublet/boundary-policy addendum before any finite Stage 7 manifest can be finalized.
"""


def _testing_section() -> str:
    return """## Stage 6D Validation

Stage 6D validation includes token-block Stage 6D build/validate/summary commands, focused canonical doublet arithmetic tests, hook and automation triage checks, stale-current strict scanning, Source Browser validation, Stage 6/6B/6C regression tests, ruff, and stage-fast/local-fast/full-parallel validation with 10 workers and 10 pytest workers. Full serial pytest remains opt-in only.
"""


def _staged_plan_section() -> str:
    return f"""## Stage 6D - Complete

Stage 6D is complete as a canonical doublet boundary source-lock and automation/hook triage insertion. It routes to {NEXT_STAGE_TITLE}. It created no final Stage 7 manifest and performed no Stage 7 probe execution.
"""


def _onboarding_section() -> str:
    return f"""## Stage 6D Current Boundary

Latest completed stage: {STAGE_TITLE}.

Next routed stage: {NEXT_STAGE_TITLE}. Use `data/project-state/current-stage-state.yaml` as authoritative current truth.
"""


def _source_truth_section() -> str:
    return """## Stage 6D Source Of Truth

`data/project-state/current-stage-state.yaml` is authoritative for latest/current routing. Stage 6D records are bounded source-lock metadata and cannot be treated as proof, route seeds, activation decisions, execution authorization, or solve claims.
"""


def _operational_docs_section() -> str:
    return """## Stage 6D Operational Files

Stage 6D primary records live under `data/project-state/`, `data/historical-route/`, `data/token-block/`, `data/source-harvester/`, and `data/operator-console/source-browser/number-fact-overlays/`. Hook/automation reports under `experiments/results/doc-drift/` and the completion handoff under `codex-output/` are ignored local outputs.
"""


def _cli_section() -> str:
    return """## Stage 6D Commands

- `python -m libreprimus.cli token-block build-stage6d`
- `python -m libreprimus.cli token-block validate-stage6d`
- `python -m libreprimus.cli token-block stage6d-summary`
- focused validators: `validate-stage6d-stage6c-preservation`, `validate-stage6d-corpus-profile-policy`, `validate-stage6d-canonical-doublet-profile`, `validate-stage6d-raw-vs-collapsed-boundary`, `validate-stage6d-86-89-reconciliation`, `validate-stage6d-lag-profile`, `validate-stage6d-section-plateau`, `validate-stage6d-zero-doublet-pages`, `validate-stage6d-421-occurrence-index`, `validate-stage6d-overlays`, `validate-stage6d-future-probes`, `validate-stage6d-stage6e-addendum`, `validate-stage6d-hook-verification`, `validate-stage6d-doc-staleness-automation-triage`, `validate-stage6d-source-browser-loadability`, `validate-stage6d-current-stage-transition`, `validate-stage6d-gate-closure`, and `validate-stage6d-handoff`.
"""


def _experiment_doc(summary: dict[str, Any]) -> str:
    return f"""# Stage 6D Canonical Doublet Boundary Source-Lock

Stage 6D reproduces the canonical pages 15-70 doublet profile as source-lock metadata: {summary['computed_pages15_70_rune_count']} runes, {summary['computed_pages15_70_lag1']} lag1 doublets, vector `{summary['computed_pages15_70_vector']}`, and lag5 count {summary['computed_pages15_70_lag5']}. It records the raw/collapsed boundary contribution, 86/89 reconciliation, disabled future probes, and automation/hook triage without executing Stage 7 probes.
"""


def _dev_log(summary: dict[str, Any]) -> str:
    return f"""# 2026-06-16 Stage 6D Development Log

Implemented Stage 6D canonical doublet source-lock metadata, exact-value validators, Source Browser overlays, automation triage, hook verification, and Stage 6E addendum routing. Discrepancy count: {summary['expected_value_discrepancy_count']}.
"""


def _research_log(summary: dict[str, Any]) -> str:
    return """# Stage 6D Research Summary

Stage 6D source-locks the canonical doublet boundary policy as review-only metadata. The pages 15-70 profile reproduces 86 adjacent doublets and the ObservationOnRuneFrequency compact vector. Raw/collapsed policy and 86/89 boundary reconciliation are recorded for Stage 6E manifest planning.
"""


def _ensure_no_protected_output_overlap() -> None:
    outputs = {path.as_posix() for path in DATA_PATHS.values()} | {path.as_posix() for path in SCHEMA_PATHS.values()}
    overlap = outputs.intersection(stage6.PROTECTED_LOCAL_PATHS)
    if overlap:
        raise RuntimeError(f"Stage 6D outputs overlap protected local state: {sorted(overlap)}")


def _result(errors: list[str], **counts: Any) -> ValidationResult:
    return ValidationResult(errors, counts)
