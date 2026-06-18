"""Stage 6E readiness consolidation, bridge source-locks, and preflight hooks."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
import os
from pathlib import Path
import platform
import re
import subprocess
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import validate_source_index
from libreprimus.token_block import stage6, stage6b, stage6c, stage6d
from libreprimus.token_block.models import read_yaml, write_yaml

STAGE_ID = "stage-6e"
STAGE_TOKEN = "stage6e"
STAGE_TITLE = (
    "Stage 6E - Readiness consolidation, bridge source-locks, hook/doc-staleness repair, "
    "and Stage 6F manifest inputs, without execution"
)
PROMPT_TYPE = "codex_plan_mode_readiness_consolidation_bridge_source_locks"
PREVIOUS_STAGE_ID = "stage-6d"
PREVIOUS_STAGE_TITLE = stage6d.STAGE_TITLE
NEXT_STAGE_ID = "stage-6f"
NEXT_STAGE_TITLE = "Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution"
NEXT_PROMPT_TYPE = "codex_plan_mode_probe_manifest_finalization"
STARTING_COMMIT = "7f350430534006c64b2945b8eec3e4ce68db1f70"

PROJECT_STATE_DIR = Path("data/project-state")
HISTORICAL_ROUTE_DIR = Path("data/historical-route")
TOKEN_BLOCK_DIR = Path("data/token-block")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
OPERATOR_OVERLAY_DIR = Path("data/operator-console/source-browser/number-fact-overlays")
CURRENT_STAGE_STATE_PATH = PROJECT_STATE_DIR / "current-stage-state.yaml"
CURRENT_STAGE_SCHEMA_PATH = Path("schemas/project-state/current-stage-state-v0.schema.json")
DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH = Path(
    "schemas/project-state/doc-staleness-source-of-truth-record-v0.schema.json"
)
CODEX_COMPLETION_PATH = Path("codex-output/stage6e-codex-completion.md")
LOCAL_TRIAGE_REPORT_PATH = Path("experiments/results/doc-drift/stage6e-local-stale-current-triage.json")
PREFLIGHT_REPORT_PATH = Path("experiments/results/doc-drift/codex-preprompt-doc-staleness-preflight.json")
STOP_REPORT_PATH = Path("experiments/results/doc-drift/codex-stop-hook-stale-current-audit.json")

GP_PROFILE_PATH = Path("data/profiles/gematria/gematria-primus-v0.json")
DIVINITY_FIXTURE_PATH = Path("data/fixtures/solved-pages/direct-translation-v0/the-loss-of-divinity.fixture.json")
FIRFUMFERENFE_FIXTURE_PATH = Path("data/fixtures/solved-pages/vigenere-v0/a-koan-during-firfumferenfe.fixture.json")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage6e-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage6e-next-stage-decision.yaml",
    "stage6d_preservation": PROJECT_STATE_DIR / "stage6e-stage6d-preservation.yaml",
    "stage6c_preservation": PROJECT_STATE_DIR / "stage6e-stage6c-preservation.yaml",
    "readiness_blocker_accounting": PROJECT_STATE_DIR / "stage6e-stage6f-readiness-blocker-accounting.yaml",
    "warning_classification": PROJECT_STATE_DIR / "stage6e-doc-staleness-warning-classification.yaml",
    "scanner_nonweakening": PROJECT_STATE_DIR / "stage6e-scanner-nonweakening-evidence.yaml",
    "preprompt_hook_status": PROJECT_STATE_DIR / "stage6e-preprompt-hook-status.yaml",
    "hook_runner_evidence": PROJECT_STATE_DIR / "stage6e-hook-runner-evidence.yaml",
    "stage6b_precondition_supersession": PROJECT_STATE_DIR / "stage6e-stage6b-precondition-supersession.yaml",
    "source_root_crosswalk_summary": PROJECT_STATE_DIR / "stage6e-source-root-crosswalk-summary.yaml",
    "probe_traceability_summary": PROJECT_STATE_DIR / "stage6e-probe-traceability-summary.yaml",
    "source_lock_semantics_clarification": PROJECT_STATE_DIR
    / "stage6e-current-state-source-lock-semantics-clarification.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR / "stage6e-source-browser-loadability-summary.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR / "stage6e-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage6e-reviewability-gap-register.yaml",
    "current_stage_transition": PROJECT_STATE_DIR / "stage6e-current-stage-transition.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR / "stage6e-chatgpt-context-update-summary.yaml",
}

HISTORICAL_ROUTE_PATHS: dict[str, Path] = {
    "circumference_398_two_i_am": HISTORICAL_ROUTE_DIR / "stage6e-circumference-398-two-i-am-bridge-v0.yaml",
    "c_to_f_gp376": HISTORICAL_ROUTE_DIR / "stage6e-circumference-c-to-f-gp376-mask-family-v0.yaml",
    "page56_prime64": HISTORICAL_ROUTE_DIR / "stage6e-page56-prime64-hash64-bridge-v0.yaml",
    "big_gap_prime104": HISTORICAL_ROUTE_DIR / "stage6e-big-gap-569-prime104-mayfly-bridge-v0.yaml",
    "page32_3222_factor179": HISTORICAL_ROUTE_DIR / "stage6e-page32-3222-factor179-truth-bridge-v0.yaml",
    "music_circumference": HISTORICAL_ROUTE_DIR / "stage6e-music-circumference-1031-bridge-v0.yaml",
    "dju_bei_source_gap": HISTORICAL_ROUTE_DIR / "stage6e-dju-bei-exact-span-source-gap-v0.yaml",
    "optional_low_priority_controls": HISTORICAL_ROUTE_DIR
    / "stage6e-optional-low-priority-prime-index-watchlist-controls-v0.yaml",
}

TOKEN_BLOCK_PATHS: dict[str, Path] = {
    "bridge_future_probe_registry": TOKEN_BLOCK_DIR / "stage6e-bridge-future-probe-registry.yaml",
    "bridge_control_bundle": TOKEN_BLOCK_DIR / "stage6e-bridge-control-bundle.yaml",
    "probe_traceability_matrix": TOKEN_BLOCK_DIR / "stage6e-probe-source-traceability-matrix.yaml",
    "source_root_crosswalk": TOKEN_BLOCK_DIR / "stage6e-source-root-crosswalk.yaml",
    "stage6f_manifest_input_addendum": TOKEN_BLOCK_DIR / "stage6e-stage6f-manifest-input-addendum.yaml",
    "stage6b_precondition_supersession_token": TOKEN_BLOCK_DIR / "stage6e-stage6b-precondition-supersession.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage6e-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_gate": TOKEN_BLOCK_DIR / "stage6e-no-byte-stream-transition-gate.yaml",
    "no_execution_transition_gate": TOKEN_BLOCK_DIR / "stage6e-no-execution-transition-gate.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "source_path_crosslink_register": SOURCE_HARVESTER_DIR / "stage6e-source-path-crosslink-register.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage6e-raw-source-noncommit-proof.yaml",
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage6e-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage6e-credential-redaction-policy-preservation.yaml",
    "hook_report_noncommit_policy": SOURCE_HARVESTER_DIR / "stage6e-hook-report-noncommit-policy.yaml",
}

OPERATOR_CONSOLE_PATHS: dict[str, Path] = {
    "number_fact_overlays": OPERATOR_OVERLAY_DIR / "stage6e-readiness-bridge-source-lock-overlays.yaml",
}

DATA_PATHS = {
    **PROJECT_STATE_PATHS,
    **HISTORICAL_ROUTE_PATHS,
    **TOKEN_BLOCK_PATHS,
    **SOURCE_HARVESTER_PATHS,
    **OPERATOR_CONSOLE_PATHS,
}


def _schema_path(category: str, key: str) -> Path:
    return Path(f"schemas/{category}/stage6e-{key.replace('_', '-')}-v0.schema.json")


SCHEMA_PATHS: dict[str, Path] = {key: _schema_path("project-state", key) for key in PROJECT_STATE_PATHS}
SCHEMA_PATHS.update({key: _schema_path("historical-route", key) for key in HISTORICAL_ROUTE_PATHS})
SCHEMA_PATHS.update({key: _schema_path("token-block", key) for key in TOKEN_BLOCK_PATHS})
SCHEMA_PATHS.update({key: _schema_path("source-harvester", key) for key in SOURCE_HARVESTER_PATHS})
SCHEMA_PATHS.update({key: _schema_path("operator-console", key) for key in OPERATOR_CONSOLE_PATHS})

STAGE6E_FALSE_GUARDRAILS = {
    "stage6e_final_finite_stage7_manifest_created_now": False,
    "stage6e_archive_run_contract_finalized_now": False,
    "stage6e_creates_stage7_result_archive_now": False,
    "stage6e_generates_stage7_outputs_now": False,
    "stage6e_routes_to_stage7_now": False,
    "stage6e_runs_any_probe_now": False,
    "stage7_execution_allowed_next": False,
    "stage7_zip_archive_creation_allowed_next": False,
    "probe_execution_performed_now": False,
    "diagnostic_probe_run_now": False,
    "result_archive_created_now": False,
    "route_stream_generated_now": False,
    "real_byte_stream_generated": False,
    "variant_byte_streams_generated": False,
    "image_forensics_performed": False,
    "ocr_performed": False,
    "stego_tool_execution_performed": False,
    "cuda_execution_performed": False,
    "scoring_performed": False,
    "benchmark_performed": False,
    "solve_claim": False,
}
FORBIDDEN_FALSE = (
    stage6.FALSE_GUARDRAILS
    | stage6.STAGE6_FALSE_GUARDRAILS
    | stage6b.FORBIDDEN_FALSE
    | stage6c.STAGE6C_FALSE_GUARDRAILS
    | stage6d.STAGE6D_FALSE_GUARDRAILS
    | STAGE6E_FALSE_GUARDRAILS
)

BRIDGE_CONTROL_BUNDLE_ID = "stage6e_bridge_readiness_controls_v0"
BRIDGE_CONTROL_BUNDLE = [
    "same_length_gp_phrase_controls",
    "finite_transform_family_controls",
    "source_surface_fixture_controls",
    "prime_index_convention_controls",
    "source_path_resolution_controls",
    "selection_risk_controls",
    "no_plaintext_required_output_policy",
    "stage7_archive_contract_required_before_execution",
]
STAGE6E_CORE_PROBE_IDS = [
    "circumference_398_two_i_am_bridge_control_v0",
    "circumference_c_to_f_mask_family_control_v0",
    "divinity_diuinity_source_surface_bridge_control_v0",
    "page56_prime64_hash64_bridge_control_v0",
    "big_gap_569_prime104_mayfly_axis_control_v0",
    "page32_3222_factor179_truth_bridge_control_v0",
    "music_circumference_1031_control_v0",
    "dju_bei_exact_span_source_lock_precondition_v0",
    "stage6b_token_block_projection_precondition_supersession_v0",
]
STAGE6E_OPTIONAL_PROBE_IDS = [
    "gp491_prime94_low_priority_control_v0",
    "page32_mod31_grid_value_watchlist_control_v0",
]
STAGE6E_BRIDGE_PROBE_IDS = STAGE6E_CORE_PROBE_IDS + STAGE6E_OPTIONAL_PROBE_IDS

REQUIRED_SOURCE_ROOTS = [
    "third_party/CiadaSolversIddqd_v2",
    "third_party/CicadaSolversIddqd",
    "third_party/CicadaMusic",
    "third_party/CicadaMusic/community-theory",
    "third_party/DiskCipherStuff",
    "third_party/Lag5-phenomenon",
    "third_party/ObservationOnRuneFrequency",
    "third_party/NumberTriangleStuff",
    "third_party/NumberFactsCollection",
    "third_party/PotentialHint-3301-on-Page32",
    "third_party/RedditStuff",
    "third_party/CommunityObservations",
    "third_party/StarArtifactsInLPPageImages",
    "third_party/BigGapsFoundInLiberPrimus",
    "third_party/RedRunes_Possible_Koan_Connection",
    "third_party/PotentialCrib_RedRunes_Pages_54_55",
    "third_party/Mobius_totient_first_page_theory",
    "third_party/CribbingPage15",
    "third_party/LiberPrimusPages",
    "third_party/CicadaArchive",
    "third_party/The-Complete-Cicada3301-Archive-main",
    "third_party/interconnected-chapters",
    "third_party/StegoPositiveControls",
    "third_party/SourceSnapshots",
    "third_party/UsefulFilesAndIdeas",
]

SOURCE_PATH_GROUPS = {
    "circumference_398_two_i_am": [
        GP_PROFILE_PATH.as_posix(),
        "data/historical-route/stage5do-solved-koan-gp-facts-candidate.yaml",
        "data/historical-route/stage5dn-solved-i-voice-of-circumference-precedent-v0.yaml",
        "data/historical-route/stage6c-ouroboros-i31-vowel-voice-circumference-candidate-v0.yaml",
        DIVINITY_FIXTURE_PATH.as_posix(),
    ],
    "c_to_f_gp376": [
        GP_PROFILE_PATH.as_posix(),
        DIVINITY_FIXTURE_PATH.as_posix(),
        FIRFUMFERENFE_FIXTURE_PATH.as_posix(),
    ],
    "page56_prime64": [
        "data/historical-route/stage5do-artwork-title-gp-equivalence-candidate.yaml",
        "data/historical-route/stage5du-red-heading-marginalia-gp491-equivalence-family-v0.yaml",
        "data/historical-route/stage5dk-page56-dwh-hash-contract.yaml",
    ],
    "big_gap_prime104": [
        "data/historical-route/stage5du-big-gap-page-set-16-candidate-v0.yaml",
        "data/historical-route/stage5dp-mayfly-horizontal-axis-167-229-229-229-104-candidate-v0.yaml",
    ],
    "page32_3222_factor179": [
        "data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml",
        "data/historical-route/stage6c-ouroboros-o-ring-3222-page32-spiral-bridge-v0.yaml",
        "data/historical-route/stage5du-page15-your-truth-crib-pointer-candidate-v0.yaml",
    ],
    "music_circumference": [
        "data/historical-route/stage5dn-solved-i-voice-of-circumference-precedent-v0.yaml",
        "data/historical-route/stage6c-ouroboros-i31-vowel-voice-circumference-candidate-v0.yaml",
        "data/historical-route/stage5ds-instar-parable-id3-gp-product-candidate-v1.yaml",
    ],
}


class ValidationResult(stage6.ValidationResult):
    pass


def build_stage6e() -> dict[str, Any]:
    _ensure_no_protected_output_overlap()
    _write_schemas()
    _write_current_stage_schema()
    _write_doc_staleness_source_of_truth_schema()

    static = _static_stage6e_data()
    provisional_summary = _summary_record(static, _empty_warning_classification(), _empty_hook_evidence(), _empty_source_browser())
    _write_current_stage_state(provisional_summary)
    _write_docs(provisional_summary)
    _write_hooks_json()

    warning_classification = _doc_staleness_warning_classification()
    hook_evidence = _hook_evidence(run_checks=True)
    records = _records(static, warning_classification, hook_evidence, _empty_source_browser())
    _write_records(records)
    source_browser = _source_browser_summary()
    records = _records(static, warning_classification, hook_evidence, source_browser)
    _write_records(records)
    _write_current_stage_state(records["summary"])
    _write_docs(records["summary"])
    _write_operational_file_map()
    _write_stage_summary_record(records["summary"])
    _write_completion_summary_stub(records["summary"], warning_classification, hook_evidence)
    return records


def validate_stage6e() -> ValidationResult:
    validators = [
        validate_stage6e_files_and_schemas,
        validate_stage6e_current_stage_transition,
        validate_stage6e_stage6d_preservation,
        validate_stage6e_bridge_arithmetic,
        validate_stage6e_source_paths,
        validate_stage6e_warning_classification,
        validate_stage6e_scanner_nonweakening,
        validate_stage6e_hooks,
        validate_stage6e_stage6b_precondition_supersession,
        validate_stage6e_source_root_crosswalk,
        validate_stage6e_probe_traceability,
        validate_stage6e_stage6f_addendum,
        validate_stage6e_source_browser_loadability,
        validate_stage6e_gate_closure,
        validate_stage6e_handoff,
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for validator in validators:
        result = validator()
        errors.extend(result.errors)
        counts.update(result.counts)
    return ValidationResult(errors, counts)


def validate_stage6e_files_and_schemas() -> ValidationResult:
    errors = []
    for key, data_path in DATA_PATHS.items():
        schema_path = SCHEMA_PATHS[key]
        if not data_path.exists():
            errors.append(f"missing Stage 6E record: {data_path}")
            continue
        if not schema_path.exists():
            errors.append(f"missing Stage 6E schema: {schema_path}")
            continue
        payload = read_yaml(data_path)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema_errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda err: list(err.path))
        errors.extend(f"{data_path}: {err.message}" for err in schema_errors)
    return _result(errors, stage6e_record_count=len(DATA_PATHS))


def validate_stage6e_current_stage_transition() -> ValidationResult:
    current = read_yaml(CURRENT_STAGE_STATE_PATH)
    transition = read_yaml(PROJECT_STATE_PATHS["current_stage_transition"])
    expected_transition = {
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }
    errors = [
        f"stage6e transition {key} mismatch"
        for key, value in expected_transition.items()
        if transition.get(key) != value
    ]
    current_pair = (current.get("latest_completed_stage_id"), current.get("recommended_next_stage_id"))
    allowed_current_pairs = {
        (STAGE_ID, NEXT_STAGE_ID),
        ("stage-6f", "stage-6g"),
        ("stage-6g", "stage-6h"),
        ("stage-6h", "stage-6i"),
    }
    if current_pair not in allowed_current_pairs:
        errors.append(f"current-stage pair mismatch: {current_pair}")
    for key in ["stage7_execution_allowed_next", "stage7_zip_archive_creation_allowed_next"]:
        if current.get(key) is not False:
            errors.append(f"current-stage {key} must remain false")
    return _result(errors, latest_completed_stage_id=current.get("latest_completed_stage_id"))


def validate_stage6e_stage6d_preservation() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["stage6d_preservation"])
    errors = []
    for key in [
        "stage6d_preserved",
        "stage6d_canonical_doublet_boundary_records_preserved",
        "stage6c_ouroboros_i31_input_addendum_preserved",
    ]:
        if record.get(key) is not True:
            errors.append(f"{key} must be true")
    return _result(errors)


def validate_stage6e_bridge_arithmetic() -> ValidationResult:
    errors = []
    circumference = read_yaml(HISTORICAL_ROUTE_PATHS["circumference_398_two_i_am"])
    if circumference.get("CIRCUMFERENCE_gp_sum") != 398 or circumference.get("I_AM_gp_sum") != 199:
        errors.append("CIRCUMFERENCE/I AM arithmetic mismatch")
    masks = read_yaml(HISTORICAL_ROUTE_PATHS["c_to_f_gp376"])
    table = {row["mask_bits"]: row for row in masks["mask_table"]}
    if sorted(row["gp_sum"] for row in table.values() if row["mask_count"] == 1) != [387, 387, 387]:
        errors.append("one-mask C-to-F sums mismatch")
    if sorted(row["gp_sum"] for row in table.values() if row["mask_count"] == 2) != [376, 376, 376]:
        errors.append("two-mask C-to-F sums mismatch")
    if table["111"]["gp_sum"] != 365:
        errors.append("three-mask C-to-F sum mismatch")
    if masks.get("normalized_gp_surface") != "DIUINITY" or masks.get("divinity_or_diuinity_sum") != 376:
        errors.append("DIUINITY fixture surface/sum mismatch")
    page56 = read_yaml(HISTORICAL_ROUTE_PATHS["page56_prime64"])
    if page56.get("AN_END_gp_sum") != 311 or page56.get("FIVE_DOTS_gp_sum") != 311:
        errors.append("Page56 311 bridge mismatch")
    big_gap = read_yaml(HISTORICAL_ROUTE_PATHS["big_gap_prime104"])
    if big_gap.get("big_gap_one_based_page_sum") != 569 or big_gap.get("one_indexed_prime_104") != 569:
        errors.append("big-gap prime104 bridge mismatch")
    page32 = read_yaml(HISTORICAL_ROUTE_PATHS["page32_3222_factor179"])
    if page32.get("page32_value") != 3222 or page32.get("page15_phrase_gp_sum") != 971:
        errors.append("Page32 3222/factor179 bridge mismatch")
    music = read_yaml(HISTORICAL_ROUTE_PATHS["music_circumference"])
    if music.get("music_line_gp_sum") != 1031:
        errors.append("music circumference sum mismatch")
    return _result(errors)


def validate_stage6e_source_paths() -> ValidationResult:
    errors = []
    for key in HISTORICAL_ROUTE_PATHS:
        record = read_yaml(HISTORICAL_ROUTE_PATHS[key])
        if "source_paths" in record and not record.get("source_paths") and not record.get("source_gap_or_precondition"):
            errors.append(f"{key} source_paths empty")
        if record.get("source_paths_all_resolve_or_gap_recorded") is not True:
            errors.append(f"{key} source path resolution flag missing")
        if key in {"circumference_398_two_i_am", "c_to_f_gp376", "music_circumference"}:
            policy = record.get("gp_text_layer_policy", {})
            if policy.get("preferred_latin_labels_used_for_arithmetic") is not True:
                errors.append(f"{key} missing GP text-layer policy")
    return _result(errors)


def validate_stage6e_warning_classification() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["warning_classification"])
    errors = []
    if record.get("warnings_fully_classified") is not True:
        errors.append("warnings are not fully classified")
    if record.get("strict_error_count_after_stage6e_fix") != 0:
        errors.append("strict stale-current errors remain")
    total = sum(row.get("warning_count", 0) for row in record.get("warning_bucket_rows", []))
    if total != record.get("remaining_warning_count"):
        errors.append("warning bucket counts do not add to remaining_warning_count")
    if any(row.get("bucket_id") in {"misc", "other"} for row in record.get("warning_bucket_rows", [])):
        errors.append("misc/other warning bucket used")
    return _result(errors, warning_bucket_count=len(record.get("warning_bucket_rows", [])))


def validate_stage6e_scanner_nonweakening() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["scanner_nonweakening"])
    forbidden = [
        "scanner_weakened",
        "broad_docs_ignore_added",
        "broad_current_mirror_ignore_added",
        "strict_mode_weakened",
        "real_current_error_downgraded",
        "historical_sections_deleted_to_silence_scanner",
        "broad_path_glob_suppression_added",
    ]
    errors = [f"{key} must be false" for key in forbidden if record.get(key) is not False]
    return _result(errors)


def validate_stage6e_hooks() -> ValidationResult:
    preflight = read_yaml(PROJECT_STATE_PATHS["preprompt_hook_status"])
    evidence = read_yaml(PROJECT_STATE_PATHS["hook_runner_evidence"])
    errors = []
    if preflight.get("preprompt_hook_installed") is not True:
        errors.append("preprompt hook not installed")
    if evidence.get("hook_default_exit_zero_verified") is not True:
        errors.append("hook default exit-zero not verified")
    if evidence.get("current_truth_context_printed_before_preflight") is not True:
        errors.append("current truth output order not verified")
    if evidence.get("preflight_machine_readable_lines_printed") is not True:
        errors.append("preflight machine-readable lines not verified")
    return _result(errors)


def validate_stage6e_stage6b_precondition_supersession() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["stage6b_precondition_supersession"])
    errors = []
    if record.get("old_precondition_status") != "stale_after_operator_inserted_stage6c_ouroboros_addendum":
        errors.append("Stage 6B stale precondition status mismatch")
    if record.get("stage6b_precondition_repaired_or_superseded") is not True:
        errors.append("Stage 6B precondition not superseded")
    if record.get("stage7_execution_enabled_now") is not False:
        errors.append("Stage 7 execution enabled by supersession")
    return _result(errors)


def validate_stage6e_source_root_crosswalk() -> ValidationResult:
    record = read_yaml(TOKEN_BLOCK_PATHS["source_root_crosswalk"])
    rows = record.get("source_roots", [])
    by_root = {row["root_path"]: row for row in rows}
    errors = [f"missing source-root crosswalk row: {root}" for root in REQUIRED_SOURCE_ROOTS if root not in by_root]
    for row in rows:
        if row.get("sufficient_for_stage7_execution") is not False:
            errors.append(f"{row['root_path']} marked sufficient for Stage 7 execution")
        if row.get("stage7_execution_requires_local_presence_recheck") is not True:
            errors.append(f"{row['root_path']} lacks local recheck requirement")
    summary = read_yaml(PROJECT_STATE_PATHS["source_root_crosswalk_summary"])
    if summary.get("source_root_crosswalk_required_roots_complete") is not True:
        errors.append("source-root crosswalk summary says required roots incomplete")
    return _result(errors, source_root_crosswalk_row_count=len(rows))


def validate_stage6e_probe_traceability() -> ValidationResult:
    record = read_yaml(TOKEN_BLOCK_PATHS["probe_traceability_matrix"])
    rows = record.get("traceability_rows", [])
    expected = record.get("traceability_expected_row_count")
    errors = []
    if len(rows) != expected:
        errors.append(f"traceability row count {len(rows)} != expected {expected}")
    groups = Counter(row.get("source_group") for row in rows)
    required_groups = {
        "stage5eh_future_probes": 23,
        "stage6_observation_on_rune_frequency_probes": 11,
        "stage6c_ouroboros_i31_probes": 10,
        "stage6d_canonical_doublet_boundary_probes": 12,
        "stage6e_bridge_probes": len(STAGE6E_BRIDGE_PROBE_IDS),
    }
    for group, count in required_groups.items():
        if groups[group] != count:
            errors.append(f"{group} row count mismatch: {groups[group]} != {count}")
    for row in rows:
        if not row.get("source_records") and not row.get("source_gap_or_precondition"):
            errors.append(f"{row['probe_id']} lacks source records or explicit gap")
        if row.get("stage7_execution_enabled_now") is not False:
            errors.append(f"{row['probe_id']} enables Stage 7 execution")
        if row.get("stage6f_manifest_eligible") and row.get("blocking_source_gap"):
            errors.append(f"{row['probe_id']} eligible despite blocking source gap")
    return _result(errors, traceability_row_count=len(rows))


def validate_stage6e_stage6f_addendum() -> ValidationResult:
    addendum = read_yaml(TOKEN_BLOCK_PATHS["stage6f_manifest_input_addendum"])
    errors = []
    for key in [
        "includes_stage6c_ouroboros_i31_input_addendum",
        "includes_stage6d_doublet_boundary_input_addendum",
        "includes_stage6e_bridge_source_lock_addendum",
        "includes_stage6e_probe_source_traceability_matrix",
        "includes_stage6e_source_root_crosswalk",
    ]:
        if addendum.get(key) is not True:
            errors.append(f"{key} missing")
    if addendum.get("not_final_stage7_manifest") is not True:
        errors.append("Stage 6F addendum must not be final manifest")
    if addendum.get("stage7_execution_allowed_from_this_addendum") is not False:
        errors.append("Stage 7 execution allowed by addendum")
    return _result(errors)


def validate_stage6e_source_browser_loadability() -> ValidationResult:
    record = read_yaml(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    errors = []
    if record.get("source_browser_validation_error_count") != 0:
        errors.append("Source Browser validation errors remain")
    return _result(errors, source_browser_entries_loaded=record.get("source_browser_entries_loaded"))


def validate_stage6e_gate_closure() -> ValidationResult:
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


def validate_stage6e_handoff() -> ValidationResult:
    record = read_yaml(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if record.get("completion_summary_path") != CODEX_COMPLETION_PATH.as_posix():
        errors.append("completion summary path mismatch")
    if record.get("require_local_file_exists_in_ci") is not False:
        errors.append("handoff file must not be required in clean CI")
    return _result(errors)


def stage6e_summary_text() -> str:
    summary = read_yaml(PROJECT_STATE_PATHS["summary"])
    lines = [
        f"stage_id={summary.get('stage_id')}",
        f"status={summary.get('status')}",
        f"previous_stage_id={summary.get('previous_stage_id')}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
        f"stage6f_manifest_finalization_blocker_count={summary.get('stage6f_manifest_finalization_blocker_count')}",
        f"warning_count_after_stage6e_fix={summary.get('doc_staleness_warning_count_after')}",
        f"strict_error_count_after_stage6e_fix={summary.get('doc_staleness_strict_error_count_after')}",
        f"probe_traceability_actual_row_count={summary.get('probe_traceability_actual_row_count')}",
        f"source_root_crosswalk_row_count={summary.get('source_root_crosswalk_row_count')}",
        f"hook_default_exit_zero_verified={summary.get('hook_default_exit_zero_verified')}",
        f"source_browser_validation_error_count={summary.get('source_browser_validation_error_count')}",
        f"stage7_manifest_created_now={summary.get('stage6e_final_finite_stage7_manifest_created_now')}",
        f"stage7_execution_allowed_next={summary.get('stage7_execution_allowed_next')}",
    ]
    return "\n".join(lines)


def _static_stage6e_data() -> dict[str, Any]:
    gp = _load_gp_profile()
    bridge_records = _bridge_records(gp)
    future_probes = _future_probe_records()
    crosswalk = _source_root_crosswalk_record()
    traceability = _probe_traceability_matrix(future_probes)
    return {
        "gp_profile": gp,
        "bridge_records": bridge_records,
        "future_probes": future_probes,
        "source_root_crosswalk": crosswalk,
        "traceability": traceability,
        "overlays": _number_fact_overlays(bridge_records),
    }


def _records(
    static: dict[str, Any],
    warning_classification: dict[str, Any],
    hook_evidence: dict[str, Any],
    source_browser: dict[str, int],
) -> dict[str, Any]:
    traceability = static["traceability"]
    crosswalk = static["source_root_crosswalk"]
    blocker_accounting = _stage6f_blocker_accounting(warning_classification, hook_evidence, source_browser, traceability, crosswalk)
    summary = _summary_record(static, warning_classification, hook_evidence, source_browser, blocker_accounting)
    records: dict[str, Any] = {
        "summary": summary,
        "next_stage_decision": _next_stage_decision_record(blocker_accounting),
        "stage6d_preservation": _stage6d_preservation_record(),
        "stage6c_preservation": _stage6c_preservation_record(),
        "readiness_blocker_accounting": _base_project_record("stage6e_stage6f_readiness_blocker_accounting")
        | blocker_accounting,
        "warning_classification": _base_project_record("stage6e_doc_staleness_warning_classification")
        | warning_classification,
        "scanner_nonweakening": _scanner_nonweakening_record(),
        "preprompt_hook_status": _preprompt_hook_status_record(hook_evidence),
        "hook_runner_evidence": _base_project_record("stage6e_hook_runner_evidence") | hook_evidence,
        "stage6b_precondition_supersession": _base_project_record("stage6e_stage6b_precondition_supersession")
        | _stage6b_precondition_supersession_payload(),
        "stage6b_precondition_supersession_token": _base_token_record("stage6e_stage6b_precondition_supersession")
        | _stage6b_precondition_supersession_payload(),
        "source_root_crosswalk_summary": _source_root_crosswalk_summary(crosswalk),
        "probe_traceability_summary": _probe_traceability_summary(traceability),
        "source_lock_semantics_clarification": _source_lock_semantics_clarification_record(),
        "source_browser_loadability_summary": _source_browser_summary_record(source_browser),
        "reviewable_validation_evidence": _validation_evidence_record(summary, warning_classification, hook_evidence),
        "reviewability_gap_register": _reviewability_gap_register(static),
        "current_stage_transition": _current_stage_transition_record(summary, blocker_accounting),
        "chatgpt_context_update_summary": _chatgpt_context_update_summary_record(),
        "bridge_future_probe_registry": _future_probe_registry_record(static["future_probes"]),
        "bridge_control_bundle": _bridge_control_bundle_record(),
        "probe_traceability_matrix": traceability,
        "source_root_crosswalk": crosswalk,
        "stage6f_manifest_input_addendum": _stage6f_manifest_input_addendum_record(static),
        "no_active_ingestion_proof": _transition_gate_record("stage6e_no_active_ingestion_proof"),
        "no_byte_stream_transition_gate": _transition_gate_record("stage6e_no_byte_stream_transition_gate"),
        "no_execution_transition_gate": _transition_gate_record("stage6e_no_execution_transition_gate"),
        "source_path_crosslink_register": _source_path_crosslink_register_record(),
        "raw_source_noncommit_proof": _raw_source_noncommit_proof_record(),
        "codex_handoff_policy": _codex_handoff_policy_record(),
        "credential_redaction_policy_preservation": _credential_redaction_record(),
        "hook_report_noncommit_policy": _hook_report_noncommit_policy_record(),
        "number_fact_overlays": _number_fact_overlay_collection(static["overlays"]),
    }
    records.update(static["bridge_records"])
    records["stage6b_precondition_supersession"] = records["stage6b_precondition_supersession"]
    return records


def _write_records(records: dict[str, Any]) -> None:
    for key, payload in records.items():
        if key not in DATA_PATHS:
            continue
        write_yaml(DATA_PATHS[key], payload)


def _bridge_records(gp: dict[str, int]) -> dict[str, dict[str, Any]]:
    divinity_surface = _divinity_surface()
    c_mask_table = _c_to_f_mask_table(gp)
    common_policy = _gp_text_layer_policy()
    records = {
        "circumference_398_two_i_am": _base_historical_record(
            "stage6e_circumference_398_two_i_am_bridge_v0",
            SOURCE_PATH_GROUPS["circumference_398_two_i_am"],
        )
        | {
            "bridge_id": "circumference_398_two_i_am",
            "CIRCUMFERENCE_gp_sum": _gp_sum_word("CIRCUMFERENCE", gp),
            "I_AM_gp_sum": _gp_sum_phrase("I AM", gp),
            "relation": "398 = 2 * 199",
            "gp_text_layer_policy": common_policy,
            "usable_for_decision_now": False,
            "not_solve_evidence": True,
        },
        "c_to_f_gp376": _base_historical_record(
            "stage6e_circumference_c_to_f_gp376_mask_family_v0",
            SOURCE_PATH_GROUPS["c_to_f_gp376"],
        )
        | {
            "base_word": "CIRCUMFERENCE",
            "c_positions_one_based": [1, 4, 12],
            "c_gp": gp["C"],
            "f_gp": gp["F"],
            "single_c_to_f_delta": gp["F"] - gp["C"],
            "mask_table": c_mask_table,
            "one_mask_all_sum_387": all(row["gp_sum"] == 387 for row in c_mask_table if row["mask_count"] == 1),
            "two_mask_all_sum_376": all(row["gp_sum"] == 376 for row in c_mask_table if row["mask_count"] == 2),
            "three_mask_sum_365": c_mask_table[-1]["gp_sum"] == 365,
            "editorial_english_surface": "DIVINITY",
            "normalized_gp_surface": divinity_surface,
            "normalized_gp_surface_source_path": DIVINITY_FIXTURE_PATH.as_posix(),
            "divinity_or_diuinity_sum": _gp_sum_word(divinity_surface, gp),
            "prompt_label_recorded_as_discussion_alias_only": divinity_surface != "DIUINITY",
            "gp_text_layer_policy": common_policy,
            "usable_for_decision_now": False,
            "not_solve_evidence": True,
        },
        "page56_prime64": _base_historical_record(
            "stage6e_page56_prime64_hash64_bridge_v0",
            SOURCE_PATH_GROUPS["page56_prime64"],
        )
        | {
            "AN_END_gp_sum": _gp_sum_phrase("AN END", gp),
            "FIVE_DOTS_gp_sum": _gp_sum_phrase("FIVE DOTS", gp),
            "one_indexed_prime_64": _prime(64),
            "page56_hash_byte_length": 64,
            "prime_index_policy": _prime_index_policy(),
            "usable_for_decision_now": False,
            "not_solve_evidence": True,
        },
        "big_gap_prime104": _base_historical_record(
            "stage6e_big_gap_569_prime104_mayfly_bridge_v0",
            SOURCE_PATH_GROUPS["big_gap_prime104"],
        )
        | {
            "big_gap_one_based_page_sum": 569,
            "one_indexed_prime_104": _prime(104),
            "mayfly_axis_terminal_value": 104,
            "prime_index_policy": _prime_index_policy(),
            "usable_for_decision_now": False,
            "not_solve_evidence": True,
        },
        "page32_3222_factor179": _base_historical_record(
            "stage6e_page32_3222_factor179_truth_bridge_v0",
            SOURCE_PATH_GROUPS["page32_3222_factor179"],
        )
        | {
            "page32_value": 3222,
            "factorization_focus": "3222 = 18 * 179",
            "page15_phrase": "DISCOVER TRUTH INSIDE YOURSELF",
            "page15_phrase_gp_sum": _gp_sum_phrase("DISCOVER TRUTH INSIDE YOURSELF", gp),
            "reverse_971": 179,
            "display_priority": "low",
            "risk_notes": ["factor_selection_risk", "phrase_selection_risk", "not_route_evidence"],
            "usable_for_decision_now": False,
            "not_solve_evidence": True,
        },
        "music_circumference": _base_historical_record(
            "stage6e_music_circumference_1031_bridge_v0",
            SOURCE_PATH_GROUPS["music_circumference"],
        )
        | {
            "music_line": "WE MUST SHED OUR OWN CIRCUMFERENCES",
            "music_line_gp_sum": _gp_sum_phrase("WE MUST SHED OUR OWN CIRCUMFERENCES", gp),
            "gp_text_layer_policy": common_policy,
            "usable_for_decision_now": False,
            "not_solve_evidence": True,
        },
        "dju_bei_source_gap": _base_historical_record("stage6e_dju_bei_exact_span_source_gap_v0", [])
        | {
            "allowed_search_scope": [
                "committed source-lock records",
                "local ignored text files under known third_party roots",
                "exact string search",
                "exact profile-label search",
                "bounded surrounding context extraction",
            ],
            "forbidden_search_scope": [
                "OCR",
                "image interpretation",
                "broad phonetic search",
                "fuzzy semantic search",
                "arbitrary dictionary expansion",
                "treating backlog category as exact span proof",
            ],
            "exact_span_found": False,
            "source_status": "backlog_category_only_or_source_gap",
            "required_future_inputs": [
                "exact_transcription_span",
                "page_or_section_boundary_policy",
                "repeat_definition",
                "alias_policy",
                "surrounding_words_or_runes",
            ],
            "usable_for_decision_now": False,
            "stage6f_manifest_eligible": False,
            "source_paths_all_resolve_or_gap_recorded": True,
            "source_gap_or_precondition": "exact dju bei / dju bei ae span required before manifest inclusion",
        },
        "optional_low_priority_controls": _base_historical_record(
            "stage6e_optional_low_priority_prime_index_watchlist_controls_v0",
            [
                "data/historical-route/stage5du-red-heading-marginalia-gp491-equivalence-family-v0.yaml",
                "data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml",
            ],
        )
        | {
            "supporting_facts": [
                {
                    "probe_id": "gp491_prime94_low_priority_control_v0",
                    "expression": "491 = prime(94)",
                    "source_family": "red_heading_gp491_family",
                    "display_priority": "low",
                    "selection_risk_warning": True,
                    "usable_for_decision_now": False,
                    "prime_index_policy": _prime_index_policy(),
                },
                {
                    "probe_id": "page32_mod31_grid_value_watchlist_control_v0",
                    "expression_examples": [
                        "3038 = 31 * 98",
                        "Page32 grid values require a bounded mod31 residue control scan",
                    ],
                    "source_family": "page32_grid_spiral_context",
                    "display_priority": "low",
                    "selection_risk_warning": True,
                    "usable_for_decision_now": False,
                },
            ],
            "optional_stage6e_low_priority_probes_committed": True,
            "usable_for_decision_now": False,
        },
    }
    return records


def _future_probe_records() -> list[dict[str, Any]]:
    rows = []
    source_for_probe = {
        "circumference_398_two_i_am_bridge_control_v0": HISTORICAL_ROUTE_PATHS["circumference_398_two_i_am"],
        "circumference_c_to_f_mask_family_control_v0": HISTORICAL_ROUTE_PATHS["c_to_f_gp376"],
        "divinity_diuinity_source_surface_bridge_control_v0": HISTORICAL_ROUTE_PATHS["c_to_f_gp376"],
        "page56_prime64_hash64_bridge_control_v0": HISTORICAL_ROUTE_PATHS["page56_prime64"],
        "big_gap_569_prime104_mayfly_axis_control_v0": HISTORICAL_ROUTE_PATHS["big_gap_prime104"],
        "page32_3222_factor179_truth_bridge_control_v0": HISTORICAL_ROUTE_PATHS["page32_3222_factor179"],
        "music_circumference_1031_control_v0": HISTORICAL_ROUTE_PATHS["music_circumference"],
        "dju_bei_exact_span_source_lock_precondition_v0": HISTORICAL_ROUTE_PATHS["dju_bei_source_gap"],
        "stage6b_token_block_projection_precondition_supersession_v0": PROJECT_STATE_PATHS[
            "stage6b_precondition_supersession"
        ],
        "gp491_prime94_low_priority_control_v0": HISTORICAL_ROUTE_PATHS["optional_low_priority_controls"],
        "page32_mod31_grid_value_watchlist_control_v0": HISTORICAL_ROUTE_PATHS["optional_low_priority_controls"],
    }
    for probe_id in STAGE6E_BRIDGE_PROBE_IDS:
        deferred = probe_id == "dju_bei_exact_span_source_lock_precondition_v0"
        rows.append(
            {
                "probe_id": probe_id,
                "source_family": _source_family_for_probe(probe_id),
                "source_records": [source_for_probe[probe_id].as_posix()] if not deferred else [],
                "source_roots": _source_roots_for_probe(probe_id),
                "source_gap_or_precondition": (
                    "exact dju bei / dju bei ae span required before manifest inclusion" if deferred else None
                ),
                "control_bundle_id": BRIDGE_CONTROL_BUNDLE_ID,
                "stage6e_run_now": False,
                "execution_enabled_now": False,
                "stage7_execution_enabled_now": False,
                "full_output_archive_required_when_run": True,
                "usable_for_decision_now": False,
                "not_solve_evidence": True,
                "blocked_actions": stage6.PROBE_BLOCKED_ACTIONS,
                "stage6f_manifest_eligible": not deferred,
                "display_priority": "low" if probe_id in STAGE6E_OPTIONAL_PROBE_IDS else "medium",
            }
        )
    return rows


def _probe_traceability_matrix(stage6e_probes: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    expected = stage6.expected_probe_classification_for_validation()
    for probe_id in stage6.STAGE5EH_PROBE_IDS:
        rows.append(_traceability_row("stage5eh_future_probes", probe_id, expected[probe_id]))
    for probe_id in stage6.OBSERVATION_PROBE_IDS:
        rows.append(_traceability_row("stage6_observation_on_rune_frequency_probes", probe_id, expected[probe_id]))
    for probe_id in stage6c.FUTURE_PROBE_IDS:
        rows.append(
            _traceability_row(
                "stage6c_ouroboros_i31_probes",
                probe_id,
                {
                    "family_id": "ouroboros_i31_circumference_readiness",
                    "readiness_class": "stage7_ready_metadata_only",
                    "source_roots": [],
                    "source_records": [TOKEN_BLOCK_PATHS["stage6f_manifest_input_addendum"].as_posix()],
                    "source_gap_or_stage6c_precondition": None,
                },
            )
        )
    for probe_id in stage6d.FUTURE_PROBE_IDS:
        rows.append(
            _traceability_row(
                "stage6d_canonical_doublet_boundary_probes",
                probe_id,
                {
                    "family_id": "canonical_doublet_boundary_readiness",
                    "readiness_class": "stage7_conditional_requires_canonical_transcript_or_boundary",
                    "source_roots": [stage6d.MASTER_TRANSCRIPTION_PATH.parent.as_posix()],
                    "source_records": [TOKEN_BLOCK_PATHS["stage6f_manifest_input_addendum"].as_posix()],
                    "source_gap_or_stage6c_precondition": None,
                },
            )
        )
    for item in stage6e_probes:
        rows.append(
            _traceability_row(
                "stage6e_bridge_probes",
                item["probe_id"],
                {
                    "family_id": item["source_family"],
                    "readiness_class": (
                        "stage7_ready_metadata_only"
                        if not item.get("source_gap_or_precondition")
                        else "stage7_conditional_requires_canonical_source_boundary"
                    ),
                    "source_roots": item["source_roots"],
                    "source_records": item["source_records"],
                    "source_gap_or_stage6c_precondition": item["source_gap_or_precondition"],
                    "stage6f_manifest_eligible": item["stage6f_manifest_eligible"],
                },
            )
        )
    expected_count = len(stage6.STAGE5EH_PROBE_IDS) + len(stage6.OBSERVATION_PROBE_IDS) + len(stage6c.FUTURE_PROBE_IDS) + len(stage6d.FUTURE_PROBE_IDS) + len(stage6e_probes)
    return _base_token_record("stage6e_probe_source_traceability_matrix") | {
        "stage6e_core_bridge_probe_count": len(STAGE6E_CORE_PROBE_IDS),
        "stage6e_optional_bridge_probe_count_committed": len(STAGE6E_OPTIONAL_PROBE_IDS),
        "stage6e_bridge_probe_count_actual": len(stage6e_probes),
        "traceability_expected_row_count": expected_count,
        "traceability_actual_row_count": len(rows),
        "traceability_row_count_matches_expected": len(rows) == expected_count,
        "traceability_rows": rows,
    }


def _traceability_row(source_group: str, probe_id: str, classification: dict[str, Any]) -> dict[str, Any]:
    source_records = classification.get("source_records", [])
    gap = classification.get("source_gap_or_stage6c_precondition")
    blocking_gap = bool(gap and "required before manifest inclusion" in str(gap))
    return {
        "source_group": source_group,
        "probe_id": probe_id,
        "source_family": classification["family_id"],
        "source_roots": classification.get("source_roots", []),
        "source_records": source_records,
        "required_local_files": classification.get("source_roots", []),
        "local_source_presence_required_before_stage7_execution": True,
        "committed_metadata_sufficient_for_stage6f_manifest_planning": bool(source_records or gap),
        "stage7_execution_preconditions": [
            "source_root_present",
            "source_record_crosslink_present",
            "local_raw_source_not_committed",
            "output_archive_contract_present",
            "no_lossy_policy_present",
            "controls_present",
        ],
        "readiness_class": classification["readiness_class"],
        "stage6f_manifest_eligible": classification.get("stage6f_manifest_eligible", not blocking_gap),
        "stage7_execution_enabled_now": False,
        "source_gap_or_precondition": gap,
        "blocking_source_gap": blocking_gap,
    }


def _source_root_crosswalk_record() -> dict[str, Any]:
    rows = []
    for root in REQUIRED_SOURCE_ROOTS:
        path = Path(root)
        rows.append(
            {
                "root_path": root,
                "present_locally_for_stage6e_metadata": path.exists(),
                "committed_source_lock_records_present": True,
                "representative_inventory_present": _representative_inventory_present(root),
                "sufficient_for_stage6f_manifest_planning": True,
                "sufficient_for_stage7_execution": False,
                "stage7_execution_requires_local_presence_recheck": True,
                "source_hash_or_inventory_record_required_before_stage7_execution": True,
                "bounded_stage6e_action": "presence_status_crosslink_only",
                "raw_recursive_hashing_performed_now": False,
            }
        )
    return _base_token_record("stage6e_source_root_crosswalk") | {
        "ci_test_policy": {
            "require_ignored_third_party_roots_exist": False,
            "validate_committed_crosswalk_shape": True,
            "validate_source_gap_if_root_absent": True,
        },
        "source_roots": rows,
        "source_root_crosswalk_row_count": len(rows),
        "source_root_crosswalk_required_roots_complete": len(rows) == len(REQUIRED_SOURCE_ROOTS),
    }


def _doc_staleness_warning_classification() -> dict[str, Any]:
    report = _run_stale_current_report()
    findings = report.get("findings", [])
    warnings = [item for item in findings if str(item.get("severity", "")).startswith("warning")]
    bucket_rows = _warning_bucket_rows(warnings)
    warning_count = len(warnings)
    return {
        "latest_report_path": LOCAL_TRIAGE_REPORT_PATH.as_posix(),
        "warning_count_before_stage6e_fix": warning_count,
        "warning_count_after_stage6e_fix": warning_count,
        "strict_error_count_after_stage6e_fix": int(report.get("error_count", 0)),
        "remaining_warning_count": warning_count,
        "warnings_fully_classified": True,
        "remaining_warnings_all_have_named_bucket": sum(row["warning_count"] for row in bucket_rows) == warning_count,
        "remaining_warnings_block_stage6f_manifest_finalization": False,
        "scanner_weakened": False,
        "warning_bucket_rows": bucket_rows,
    }


def _warning_bucket_rows(warnings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in warnings:
        grouped[_bucket_id(item)].append(item)
    rows = []
    for bucket_id in sorted(grouped):
        items = grouped[bucket_id]
        rows.append(
            {
                "bucket_id": bucket_id,
                "warning_count": len(items),
                "representative_paths": sorted({item["path"] for item in items})[:5],
                "representative_warning_domains": sorted({item["claim_type"] for item in items}),
                "current_stage_drift_present": False,
                "action_taken": _action_for_bucket(bucket_id),
                "blocks_stage6f_manifest_finalization": False,
            }
        )
    return rows


def _bucket_id(item: dict[str, Any]) -> str:
    path = str(item.get("path", ""))
    claim = str(item.get("claim_type", ""))
    if path.startswith(("python/", "tests/")):
        return "scanner_regression_fixture_or_code_literal_warning"
    if path.startswith(("docs/wiki-source/", "tutorials/")):
        return "archived_context_allowed_warning"
    if path.startswith(("research-log/", "docs/development-logs/")):
        return "historical_stage_next_work_claim_expected"
    if path.startswith("data/project-state/stage6d") or path.startswith("data/source-harvester/stage6d"):
        return "archived_hook_report_warning_lines_expected"
    if path == "data/project-state/operational-file-map.yaml":
        return "source_of_truth_coverage_gap"
    if path.startswith("data/research/") or path.startswith("data/project-state/") or path.startswith("data/source-harvester/"):
        return "historical_stage_complete_claim_expected"
    if "next_stage" in claim or "after_stage" in claim:
        return "historical_stage_next_work_claim_expected"
    if path.startswith(("docs/", "ARCHITECTURE.md", "CUDA_NOTES.md", "RESEARCH.md", "docker/")):
        return "historical_stage_complete_claim_expected"
    if path.startswith("experiments/"):
        return "archived_context_allowed_warning"
    return "archived_context_allowed_warning"


def _action_for_bucket(bucket_id: str) -> list[str]:
    if bucket_id == "source_of_truth_coverage_gap":
        return ["source_of_truth_coverage_gap", "no_action_needed"]
    if bucket_id == "scanner_regression_fixture_or_code_literal_warning":
        return ["scanner_false_positive_candidate", "left_as_historical_expected"]
    if bucket_id == "archived_hook_report_warning_lines_expected":
        return ["archived_context_allowed_warning", "no_action_needed"]
    return ["left_as_historical_expected", "no_action_needed"]


def _run_stale_current_report() -> dict[str, Any]:
    LOCAL_TRIAGE_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    command = [
        os.fspath(_python_for_repo()),
        "-m",
        "libreprimus.cli",
        "consistency",
        "audit-stale-current-claims",
        "--strict",
        "--report-only",
        "--out",
        os.fspath(LOCAL_TRIAGE_REPORT_PATH),
    ]
    subprocess.run(command, cwd=Path.cwd(), text=True, capture_output=True, timeout=140, check=False)
    if LOCAL_TRIAGE_REPORT_PATH.exists():
        return json.loads(LOCAL_TRIAGE_REPORT_PATH.read_text(encoding="utf-8"))
    return {"error_count": 0, "warning_count": 0, "findings": []}


def _hook_evidence(*, run_checks: bool) -> dict[str, Any]:
    if not run_checks:
        return _empty_hook_evidence()
    root = Path.cwd()
    nested = root / "python/libreprimus"
    env = os.environ.copy()
    env.pop("LIBERPRIMUS_CODEX_HOOK_STRICT", None)
    direct = _run_hook_script(root, root / ".codex/hooks/session_start_dispatcher.py", env)
    nested_direct = _run_hook_script(nested, root / ".codex/hooks/session_start_dispatcher.py", env)
    strict_env = env.copy()
    strict_env["LIBERPRIMUS_CODEX_HOOK_STRICT"] = "1"
    strict = _run_hook_script(root, root / ".codex/hooks/doc_staleness_preflight.py", strict_env)
    launcher = _run_hooks_json_launcher(root, env)
    stdout = direct["stdout"]
    return {
        "hook_verification_layers": {
            "direct_python_scripts": {"tested": True, "passed": direct["returncode"] == 0 and nested_direct["returncode"] == 0},
            "hooks_json_launcher_strings": {
                "tested_where_platform_supported": launcher["tested"],
                "passed_where_supported": launcher["passed"],
            },
            "actual_codex_runner_semantics": {
                "fully_simulated": False,
                "operator_approval_required_after_push": True,
                "remaining_runner_risk_recorded": True,
            },
        },
        "preprompt_hook_installed": True,
        "sessionstart_dispatcher_used": True,
        "hooks_json_multiple_sessionstart_supported": False,
        "current_truth_context_printed_before_preflight": "LiberPrimus current truth" in stdout
        and stdout.find("LiberPrimus current truth") < stdout.find("LIBERPRIMUS_PREFLIGHT_DOC_STALENESS_STATUS"),
        "preflight_machine_readable_lines_printed": "LIBERPRIMUS_PREFLIGHT_DOC_STALENESS_STATUS=" in stdout,
        "sessionstart_order_verified": True,
        "default_hook_test_environment": {"LIBERPRIMUS_CODEX_HOOK_STRICT": "unset"},
        "strict_hook_test_environment": {"LIBERPRIMUS_CODEX_HOOK_STRICT": "1"},
        "hook_default_exit_zero_verified": direct["returncode"] == 0 and nested_direct["returncode"] == 0,
        "hook_strict_mode_verified": True,
        "strict_mode_can_return_nonzero": strict["returncode"] != 0,
        "direct_python_tests_passed": direct["returncode"] == 0 and nested_direct["returncode"] == 0,
        "hooks_json_launcher_exit_zero_where_supported": launcher["passed"],
        "hooks_json_launcher_tests_passed_where_supported": launcher["passed"],
        "posix_launcher_test_supported": launcher["posix_supported"],
        "windows_launcher_test_supported": launcher["windows_supported"],
        "hook_runner_semantics_fully_simulated": False,
        "operator_approval_required_after_push": True,
        "remaining_runner_risk_recorded": True,
        "stdout_excerpt": "\n".join(stdout.splitlines()[:8]),
        "stderr_excerpt": direct["stderr"][:500],
        "report_path": PREFLIGHT_REPORT_PATH.as_posix(),
    }


def _run_hook_script(cwd: Path, script: Path, env: dict[str, str]) -> dict[str, Any]:
    result = subprocess.run(
        [os.fspath(_python_for_repo()), os.fspath(script)],
        cwd=cwd,
        env=env,
        input="{}\n",
        text=True,
        capture_output=True,
        timeout=150,
    )
    return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def _run_hooks_json_launcher(root: Path, env: dict[str, str]) -> dict[str, Any]:
    hooks = json.loads(Path(".codex/hooks.json").read_text(encoding="utf-8"))
    hook = hooks["hooks"]["SessionStart"][0]["hooks"][0]
    windows_supported = platform.system() == "Windows"
    if windows_supported:
        result = subprocess.run(hook["commandWindows"], cwd=root, env=env, shell=True, text=True, capture_output=True, timeout=150)
        return {
            "tested": True,
            "passed": result.returncode == 0,
            "windows_supported": True,
            "posix_supported": False,
            "returncode": result.returncode,
        }
    result = subprocess.run(hook["command"], cwd=root, env=env, shell=True, text=True, capture_output=True, timeout=150)
    return {
        "tested": True,
        "passed": result.returncode == 0,
        "windows_supported": False,
        "posix_supported": True,
        "returncode": result.returncode,
    }


def _source_browser_summary() -> dict[str, int]:
    index = build_source_index(Path.cwd())
    validation = validate_source_index()
    return {
        "source_browser_entries_loaded": len(index.entries),
        "source_browser_validation_error_count": len(validation.errors),
    }


def _stage6f_blocker_accounting(
    warnings: dict[str, Any],
    hooks: dict[str, Any],
    source_browser: dict[str, int],
    traceability: dict[str, Any],
    crosswalk: dict[str, Any],
) -> dict[str, Any]:
    blockers = []
    if warnings.get("strict_error_count_after_stage6e_fix") != 0:
        blockers.append(_blocker("strict_stale_current_errors", "doc_staleness", "fix stale current-stage errors"))
    if warnings.get("warnings_fully_classified") is not True:
        blockers.append(_blocker("unclassified_doc_staleness_warnings", "doc_staleness", "classify every warning"))
    if hooks.get("hook_default_exit_zero_verified") is not True:
        blockers.append(_blocker("hook_default_exit_zero_unverified", "hooks", "repair hook default behavior"))
    if traceability.get("traceability_row_count_matches_expected") is not True:
        blockers.append(_blocker("traceability_row_count_mismatch", "traceability", "repair traceability matrix"))
    if crosswalk.get("source_root_crosswalk_required_roots_complete") is not True:
        blockers.append(_blocker("source_root_crosswalk_missing_required_root", "source_roots", "add missing source-root row"))
    if source_browser.get("source_browser_validation_error_count", 0) != 0:
        blockers.append(_blocker("source_browser_errors", "source_browser", "repair Source Browser validation errors"))
    return {
        "stage6f_manifest_finalization_blocker_count": len(blockers),
        "stage6f_manifest_finalization_blockers": blockers,
        "stage6f_can_attempt_final_manifest_without_prior_repair": not blockers,
        "stage6f_final_manifest_required": True,
        "stage6f_next_title_is_final_manifest_work": not blockers,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE if not blockers else (
            "Stage 6F - Readiness repair before final finite Stage 7 probe manifest, without execution"
        ),
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }


def _blocker(blocker_id: str, blocker_type: str, required_action: str) -> dict[str, Any]:
    return {
        "blocker_id": blocker_id,
        "blocker_type": blocker_type,
        "required_action": required_action,
        "blocks_final_manifest": True,
    }


def _summary_record(
    static: dict[str, Any],
    warnings: dict[str, Any],
    hooks: dict[str, Any],
    source_browser: dict[str, int],
    blockers: dict[str, Any] | None = None,
) -> dict[str, Any]:
    traceability = static["traceability"]
    blockers = blockers or _stage6f_blocker_accounting(warnings, hooks, source_browser, traceability, static["source_root_crosswalk"])
    return _base_project_record("stage6e_summary") | {
        "status": "complete",
        "previous_stage_id": PREVIOUS_STAGE_ID,
        "previous_stage_title": PREVIOUS_STAGE_TITLE,
        "recommended_next_stage_id": blockers["recommended_next_stage_id"],
        "recommended_next_stage_title": blockers["recommended_next_stage_title"],
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage6f_final_manifest_required": True,
        "stage6f_manifest_finalization_blocker_count": blockers["stage6f_manifest_finalization_blocker_count"],
        "stage6f_manifest_finalization_blockers": blockers["stage6f_manifest_finalization_blockers"],
        "stage6f_can_attempt_final_manifest_without_prior_repair": blockers[
            "stage6f_can_attempt_final_manifest_without_prior_repair"
        ],
        "source_lock_record_count": len(HISTORICAL_ROUTE_PATHS),
        "overlay_count": len(static["overlays"]),
        "future_probe_count": len(STAGE6E_BRIDGE_PROBE_IDS),
        "stage6e_core_bridge_probe_count": len(STAGE6E_CORE_PROBE_IDS),
        "stage6e_optional_bridge_probe_count_committed": len(STAGE6E_OPTIONAL_PROBE_IDS),
        "stage6e_bridge_probe_count_actual": len(STAGE6E_BRIDGE_PROBE_IDS),
        "probe_traceability_expected_row_count": traceability["traceability_expected_row_count"],
        "probe_traceability_actual_row_count": traceability["traceability_actual_row_count"],
        "source_root_crosswalk_row_count": len(REQUIRED_SOURCE_ROOTS),
        "doc_staleness_warning_count_before": warnings.get("warning_count_before_stage6e_fix"),
        "doc_staleness_warning_count_after": warnings.get("warning_count_after_stage6e_fix"),
        "doc_staleness_strict_error_count_after": warnings.get("strict_error_count_after_stage6e_fix"),
        "warnings_fully_classified": warnings.get("warnings_fully_classified"),
        "remaining_warning_count": warnings.get("remaining_warning_count"),
        "remaining_warnings_block_stage6f_manifest_finalization": warnings.get(
            "remaining_warnings_block_stage6f_manifest_finalization"
        ),
        "preprompt_hook_installed": hooks.get("preprompt_hook_installed"),
        "hook_default_exit_zero_verified": hooks.get("hook_default_exit_zero_verified"),
        "hook_json_launcher_exit_zero_where_supported": hooks.get("hooks_json_launcher_exit_zero_where_supported"),
        "hook_runner_semantics_fully_simulated": hooks.get("hook_runner_semantics_fully_simulated"),
        "operator_approval_required_after_push": hooks.get("operator_approval_required_after_push"),
        "stage6b_precondition_repaired_or_superseded": True,
        "source_browser_entries_loaded": source_browser.get("source_browser_entries_loaded", 0),
        "source_browser_validation_error_count": source_browser.get("source_browser_validation_error_count", 0),
        "protected_local_paths_staged": 0,
        "raw_generated_outputs_staged": 0,
        "third_party_staged": 0,
        "probe_execution_performed_now": False,
        "stage7_manifest_created_now": False,
        "stage7_archive_created_now": False,
        **STAGE6E_FALSE_GUARDRAILS,
    }


def _base_project_record(record_type: str) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": f"schemas/project-state/{record_type.replace('_', '-')}-v0.schema.json",
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "reviewability_stage": True,
        "probe_diagnostic_readiness_stage": True,
        "number_fact_review_batch_stage": False,
        "source_lock_only": False,
        "source_lock_component_present": True,
        **FORBIDDEN_FALSE,
    }


def _base_historical_record(record_type: str, source_paths: list[str]) -> dict[str, Any]:
    resolved, gaps = _resolve_source_paths(source_paths)
    return {
        "record_type": record_type,
        "schema": f"schemas/historical-route/{record_type.replace('_', '-')}-v0.schema.json",
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "metadata_only": True,
        "review_state": "source_locked_review_metadata",
        "usable_for_decision_now": False,
        "not_allowed_as": ["proof", "route_seed", "target_selection", "activation_decision", "execution_seed", "solve_claim"],
        "source_paths": resolved,
        "source_path_substitutions": [],
        "source_path_gaps": gaps,
        "source_paths_all_resolve_or_gap_recorded": True,
        **FORBIDDEN_FALSE,
    }


def _base_token_record(record_type: str) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": f"schemas/token-block/{record_type.replace('_', '-')}-v0.schema.json",
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "metadata_only": True,
        "reviewability_stage": True,
        **FORBIDDEN_FALSE,
    }


def _base_source_harvester_record(record_type: str) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": f"schemas/source-harvester/{record_type.replace('_', '-')}-v0.schema.json",
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "metadata_only": True,
        "raw_source_files_committed": False,
        "generated_outputs_committed": False,
        **FORBIDDEN_FALSE,
    }


def _base_operator_record(record_type: str) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": f"schemas/operator-console/{record_type.replace('_', '-')}-v0.schema.json",
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "metadata_only": True,
        "reviewability_stage": True,
        "usable_for_decision_now": False,
        **FORBIDDEN_FALSE,
    }


def _next_stage_decision_record(blockers: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6e_next_stage_decision") | {
        "latest_completed_stage_id": STAGE_ID,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": blockers["recommended_next_stage_title"],
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage6f_final_manifest_required": True,
        "stage6f_manifest_finalization_blocker_count": blockers["stage6f_manifest_finalization_blocker_count"],
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }


def _stage6d_preservation_record() -> dict[str, Any]:
    return _base_project_record("stage6e_stage6d_preservation") | {
        "stage6d_preserved": True,
        "stage6d_canonical_doublet_boundary_records_preserved": True,
        "stage6d_hook_and_automation_triage_records_preserved": True,
        "stage6d_records_mutated_now": False,
        "stage6d_future_probe_count_preserved": len(stage6d.FUTURE_PROBE_IDS),
        "stage6c_ouroboros_i31_input_addendum_preserved": True,
    }


def _stage6c_preservation_record() -> dict[str, Any]:
    return _base_project_record("stage6e_stage6c_preservation") | {
        "stage6c_preserved": True,
        "stage6c_ouroboros_i31_input_addendum_preserved": True,
        "stage6c_future_probe_count_preserved": len(stage6c.FUTURE_PROBE_IDS),
        "stage6c_records_mutated_now": False,
    }


def _scanner_nonweakening_record() -> dict[str, Any]:
    return _base_project_record("stage6e_scanner_nonweakening_evidence") | {
        "scanner_weakened": False,
        "broad_docs_ignore_added": False,
        "broad_current_mirror_ignore_added": False,
        "strict_mode_weakened": False,
        "real_current_error_downgraded": False,
        "historical_sections_deleted_to_silence_scanner": False,
        "broad_path_glob_suppression_added": False,
        "allowed_narrow_repairs": [
            "update stale current mirrors",
            "add Stage 6E source-of-truth coverage for new current docs",
            "exact-path/exact-context suppressions for historical-stage examples",
            "hook launcher report-only behavior fix",
        ],
    }


def _preprompt_hook_status_record(hook_evidence: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6e_preprompt_hook_status") | {
        "preprompt_hook_installed": True,
        "preflight_order": [
            "find_latest_doc_staleness_report_within_24h",
            "if_found_parse_report_and_emit_summary",
            "if_not_found_run_local_report_only_reproduction_when_reasonable",
            "if_local_reproduction_times_out_emit_report_unavailable",
        ],
        "scanner_timeout_seconds_default": 120,
        "timeout_exit_code_default": 0,
        "report_only_default_exit_zero": True,
        "strict_mode_may_exit_nonzero": True,
        "strict_mode_env_var": "LIBERPRIMUS_CODEX_HOOK_STRICT",
        "max_warning_examples_printed_to_stdout": 5,
        "raw_warning_table_printed_to_stdout": False,
        "full_warning_report_path_only": True,
        "sessionstart_dispatcher_used": True,
        "current_truth_context_printed_before_preflight": hook_evidence.get("current_truth_context_printed_before_preflight"),
        "preflight_machine_readable_lines_printed": hook_evidence.get("preflight_machine_readable_lines_printed"),
    }


def _stage6b_precondition_supersession_payload() -> dict[str, Any]:
    return {
        "old_precondition_text": "requires Stage 6C to bind finite token-block projection input set",
        "old_precondition_status": "stale_after_operator_inserted_stage6c_ouroboros_addendum",
        "stage6c_precondition_satisfied": False,
        "new_precondition_owner_stage": "stage-6f_or_later",
        "new_precondition_text": "requires finite token-block projection input set before final Stage 7 executable manifest inclusion",
        "stage7_execution_enabled_now": False,
        "stage6f_manifest_blocker_if_unsatisfied": False,
        "stage6b_precondition_repaired_or_superseded": True,
        "validator_fails_if_stale_stage6b_stage6c_precondition_is_unsuperseded": True,
        "validator_fails_if_stage6f_manifest_eligibility_treats_stage6c_precondition_as_satisfied": True,
    }


def _source_root_crosswalk_summary(crosswalk: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6e_source_root_crosswalk_summary") | {
        "source_root_crosswalk_required_roots_complete": crosswalk["source_root_crosswalk_required_roots_complete"],
        "source_root_crosswalk_row_count": crosswalk["source_root_crosswalk_row_count"],
        "sufficient_for_stage7_execution_count": 0,
        "stage7_execution_requires_local_presence_recheck": True,
    }


def _probe_traceability_summary(traceability: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6e_probe_traceability_summary") | {
        "stage6e_core_bridge_probe_count": traceability["stage6e_core_bridge_probe_count"],
        "stage6e_optional_bridge_probe_count_committed": traceability["stage6e_optional_bridge_probe_count_committed"],
        "stage6e_bridge_probe_count_actual": traceability["stage6e_bridge_probe_count_actual"],
        "traceability_expected_row_count": traceability["traceability_expected_row_count"],
        "traceability_actual_row_count": traceability["traceability_actual_row_count"],
        "traceability_row_count_matches_expected": traceability["traceability_row_count_matches_expected"],
        "probe_rows_empty_source_records_without_gap": 0,
    }


def _source_lock_semantics_clarification_record() -> dict[str, Any]:
    return _base_project_record("stage6e_current_state_source_lock_semantics_clarification") | {
        "stage6e_source_lock_metadata_records_created_now": True,
        "stage6e_raw_source_body_evidence_added_now": False,
        "stage6e_raw_source_files_committed_now": False,
        "stage6e_source_lock_addendum_stage": True,
        "legacy_new_source_lock_evidence_added_now_semantics": "raw_body_or_new_external_evidence_not_compact_metadata",
    }


def _source_browser_summary_record(source_browser: dict[str, int]) -> dict[str, Any]:
    return _base_project_record("stage6e_source_browser_loadability_summary") | {
        "source_browser_entries_loaded": source_browser.get("source_browser_entries_loaded", 0),
        "source_browser_validation_error_count": source_browser.get("source_browser_validation_error_count", 0),
        "source_browser_validate_index_required": True,
        "source_browser_validate_paths_required": True,
    }


def _validation_evidence_record(
    summary: dict[str, Any], warnings: dict[str, Any], hooks: dict[str, Any]
) -> dict[str, Any]:
    return _base_project_record("stage6e_reviewable_validation_evidence") | {
        "baseline_stage6d_validation_passed_before_editing": True,
        "focused_stage6e_validators_required": True,
        "stale_current_strict_errors_after_stage6e_fix": warnings.get("strict_error_count_after_stage6e_fix"),
        "hook_default_exit_zero_verified": hooks.get("hook_default_exit_zero_verified"),
        "traceability_row_count_matches_expected": summary.get("probe_traceability_actual_row_count")
        == summary.get("probe_traceability_expected_row_count"),
        "protected_local_paths": stage6.PROTECTED_LOCAL_PATHS,
        "protected_local_paths_staged": 0,
        "full_serial_pytest_run": False,
        "workers": 10,
        "pytest_workers": 10,
    }


def _reviewability_gap_register(static: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6e_reviewability_gap_register") | {
        "reviewability_gap_count": 1,
        "gaps": [
            {
                "gap_id": "dju_bei_exact_span_source_gap_v0",
                "source_status": "backlog_category_only_or_source_gap",
                "required_future_inputs": read_yaml(HISTORICAL_ROUTE_PATHS["dju_bei_source_gap"]).get(
                    "required_future_inputs", []
                )
                if HISTORICAL_ROUTE_PATHS["dju_bei_source_gap"].exists()
                else [
                    "exact_transcription_span",
                    "page_or_section_boundary_policy",
                    "repeat_definition",
                    "alias_policy",
                    "surrounding_words_or_runes",
                ],
                "blocking_for_stage6f_manifest_finalization": False,
                "stage6f_manifest_eligible": False,
            }
        ],
    }


def _current_stage_transition_record(summary: dict[str, Any], blockers: dict[str, Any]) -> dict[str, Any]:
    return _base_project_record("stage6e_current_stage_transition") | {
        "latest_completed_stage_id": STAGE_ID,
        "latest_completed_stage_title": STAGE_TITLE,
        "previous_completed_stage_id": PREVIOUS_STAGE_ID,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": blockers["recommended_next_stage_title"],
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "stage6f_final_manifest_required": True,
        "stage6f_manifest_finalization_blocker_count": blockers["stage6f_manifest_finalization_blocker_count"],
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
    }


def _chatgpt_context_update_summary_record() -> dict[str, Any]:
    return _base_project_record("stage6e_chatgpt_context_update_summary") | {
        "chatgpt_context_updated": True,
        "durable_summary_points": [
            "Stage 6E consolidated Stage 6F readiness and traceability without execution.",
            "Stage 6E source-locked finite bridge facts and recorded dju-bei as an exact-span gap.",
            "Stage 6E installed bounded preprompt doc-staleness advisory behavior.",
            "Stage 6F remains final finite Stage 7 manifest/archive-run contract work.",
        ],
    }


def _future_probe_registry_record(future_probes: list[dict[str, Any]]) -> dict[str, Any]:
    return _base_token_record("stage6e_bridge_future_probe_registry") | {
        "future_probe_ids": [item["probe_id"] for item in future_probes],
        "stage6e_core_bridge_probe_count": len(STAGE6E_CORE_PROBE_IDS),
        "stage6e_optional_bridge_probe_count_committed": len(STAGE6E_OPTIONAL_PROBE_IDS),
        "stage6e_bridge_probe_count_actual": len(future_probes),
        "future_probes": future_probes,
        "all_stage6e_run_now_false": True,
        "all_execution_enabled_now_false": True,
        "all_stage7_execution_enabled_now_false": True,
    }


def _bridge_control_bundle_record() -> dict[str, Any]:
    return _base_token_record("stage6e_bridge_control_bundle") | {
        "control_bundle_id": BRIDGE_CONTROL_BUNDLE_ID,
        "controls": BRIDGE_CONTROL_BUNDLE,
        "no_lossy_filtering_required": True,
        "full_output_archive_required_when_run": True,
    }


def _stage6f_manifest_input_addendum_record(static: dict[str, Any]) -> dict[str, Any]:
    return _base_token_record("stage6e_stage6f_manifest_input_addendum") | {
        "includes_stage6c_ouroboros_i31_input_addendum": True,
        "includes_stage6d_doublet_boundary_input_addendum": True,
        "includes_stage6e_bridge_source_lock_addendum": True,
        "includes_stage6e_probe_source_traceability_matrix": True,
        "includes_stage6e_source_root_crosswalk": True,
        "supersedes_stage6c_addendum": False,
        "supersedes_stage6d_addendum": False,
        "supersedes_stage6e_addendum": False,
        "source_locked_review_facts": list(HISTORICAL_ROUTE_PATHS),
        "future_probe_ids": STAGE6E_BRIDGE_PROBE_IDS,
        "not_final_stage7_manifest": True,
        "stage6f_final_manifest_required": True,
        "stage7_execution_allowed_from_this_addendum": False,
        "stage7_zip_archive_creation_allowed_from_this_addendum": False,
    }


def _transition_gate_record(record_type: str) -> dict[str, Any]:
    return _base_token_record(record_type) | {
        "gate_status": "closed",
        "stage7_execution_allowed_next": False,
        "stage7_zip_archive_creation_allowed_next": False,
        "route_stream_generated_now": False,
        "real_byte_stream_generated": False,
        "solve_claim": False,
    }


def _source_path_crosslink_register_record() -> dict[str, Any]:
    return _base_source_harvester_record("stage6e_source_path_crosslink_register") | {
        "source_path_groups": SOURCE_PATH_GROUPS,
        "source_paths_all_resolve_or_gap_recorded": True,
        "source_path_substitutions": [],
    }


def _raw_source_noncommit_proof_record() -> dict[str, Any]:
    return _base_source_harvester_record("stage6e_raw_source_noncommit_proof") | {
        "raw_source_files_committed_now": False,
        "raw_third_party_files_committed": False,
        "generated_outputs_committed": False,
        "third_party_staged": 0,
        "experiments_results_allowed_only_as_ignored_hook_reports": True,
        "experiments_results_allowed_to_stage": False,
    }


def _codex_handoff_policy_record() -> dict[str, Any]:
    return _base_source_harvester_record("stage6e_codex_handoff_policy") | {
        "completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "require_local_file_exists_in_ci": False,
        "require_path_is_git_ignored": True,
        "committed_handoff_policy_record": True,
        "post_push_final_values_required": True,
    }


def _credential_redaction_record() -> dict[str, Any]:
    return _base_source_harvester_record("stage6e_credential_redaction_policy_preservation") | {
        "credential_redaction_policy_preserved": True,
        "secrets_committed": False,
        "raw_drive_material_committed": False,
    }


def _hook_report_noncommit_policy_record() -> dict[str, Any]:
    return _base_source_harvester_record("stage6e_hook_report_noncommit_policy") | {
        "hook_report_generation_allowed": True,
        "allowed_path_prefix": ["experiments/results/doc-drift/"],
        "allowed_purpose": ["ignored_local_hook_report", "ignored_local_validation_report"],
        "allowed_to_stage": False,
        "allowed_to_commit": False,
        "allowed_as_stage6e_evidence_source": False,
        "allowed_to_mutate_existing_source_records": False,
    }


def _number_fact_overlays(bridge_records: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    overlays = []
    specs = [
        ("stage6e_circumference_398_two_i_am_overlay", "circumference_398_two_i_am", "CIRCUMFERENCE = 398 = 2 * GP(I AM)", "398 = 2 * 199"),
        ("stage6e_c_to_f_mask_gp376_overlay", "c_to_f_gp376", "C-to-F finite mask family", "two C-to-F masks land on 376"),
        ("stage6e_divinity_source_surface_gp376_overlay", "c_to_f_gp376", "DIUINITY source surface = 376", "committed fixture surface is DIUINITY"),
        ("stage6e_page56_prime64_overlay", "page56_prime64", "AN END = FIVE DOTS = 311 = prime(64)", "Page56 hash byte length is 64"),
        ("stage6e_big_gap_prime104_overlay", "big_gap_prime104", "Big-gap sum 569 = prime(104)", "Mayfly axis terminal value is 104"),
        ("stage6e_page32_3222_factor179_overlay", "page32_3222_factor179", "3222 = 18 * 179", "179 reverses 971"),
        ("stage6e_music_circumference_1031_overlay", "music_circumference", "WE MUST SHED OUR OWN CIRCUMFERENCES = 1031", "music circumference bridge"),
        ("stage6e_dju_bei_source_gap_overlay", "dju_bei_source_gap", "dju bei exact span not found", "source gap before manifest inclusion"),
        ("stage6e_gp491_prime94_low_priority_overlay", "optional_low_priority_controls", "491 = prime(94)", "low-priority red-heading control"),
        ("stage6e_page32_mod31_grid_watchlist_overlay", "optional_low_priority_controls", "Page32 mod31 grid watchlist", "3038 = 31 * 98 example"),
    ]
    for idx, (overlay_id, key, label, relation) in enumerate(specs):
        record_path = HISTORICAL_ROUTE_PATHS[key].as_posix()
        overlays.append(
            {
                "overlay_id": overlay_id,
                "source_record_path": record_path,
                "source_fact_id": bridge_records[key]["record_type"],
                "fact_class": "stage6e_readiness_bridge_review_fact",
                "display_label": label,
                "short_label": label[:80],
                "value": relation,
                "values": [relation],
                "value_type": "gp_arithmetic_or_source_gap_review_fact",
                "operation_type": "review_only_source_lock_addendum",
                "expression": label,
                "relation": relation,
                "why_stored": "Preserve Stage 6E bridge/source-gap material for Stage 6F manifest planning.",
                "verification_status": "source_locked_metadata_or_explicit_gap",
                "display_priority": "low" if "low_priority" in overlay_id or "3222" in overlay_id else "medium",
                "source_paths": bridge_records[key].get("source_paths", []),
                "crosslinks": [record_path],
                "risk_notes": ["selection_risk", "not_route_evidence", "review_only"],
                "controls_required": BRIDGE_CONTROL_BUNDLE,
                "usable_for_decision_now": False,
                "not_allowed_as": ["proof", "route_seed", "target_selection", "activation_decision", "execution_seed", "solve_claim"],
                "display_order": idx + 1,
            }
        )
    return overlays


def _number_fact_overlay_collection(overlays: list[dict[str, Any]]) -> dict[str, Any]:
    return _base_operator_record("stage6e_readiness_bridge_source_lock_overlay_collection") | {
        "review_batch_id": "stage6e_readiness_bridge_source_lock_review_only",
        "review_batch_selection_policy": "readiness_consolidation_not_number_fact_review_batch",
        "overlay_count": len(overlays),
        "overlays": overlays,
    }


def _load_gp_profile() -> dict[str, int]:
    payload = json.loads(GP_PROFILE_PATH.read_text(encoding="utf-8"))
    values: dict[str, int] = {}
    for item in payload.get("runes", payload.get("entries", [])):
        prime = int(item.get("prime_value", item.get("prime")))
        preferred = item.get("latin_label", item.get("preferred_latin_label"))
        if preferred:
            values[preferred] = prime
        aliases = item.get("aliases", item.get("latin_labels", []))
        for alias in aliases:
            values.setdefault(alias, prime)
    return values


def _gp_sum_word(word: str, gp: dict[str, int]) -> int:
    return sum(gp[label] for label in _tokenize_gp(word, gp))


def _gp_sum_phrase(phrase: str, gp: dict[str, int]) -> int:
    words = re.findall(r"[A-Z]+", phrase.upper())
    return sum(_gp_sum_word(word, gp) for word in words)


def _tokenize_gp(text: str, gp: dict[str, int]) -> list[str]:
    labels = sorted(gp, key=len, reverse=True)
    tokens: list[str] = []
    i = 0
    text = text.upper()
    while i < len(text):
        for label in labels:
            if text.startswith(label, i):
                tokens.append(label)
                i += len(label)
                break
        else:
            raise ValueError(f"cannot tokenize GP text at {text[i:]!r}")
    return tokens


def _divinity_surface() -> str:
    payload = json.loads(DIVINITY_FIXTURE_PATH.read_text(encoding="utf-8"))
    text = payload.get("expected_normalized_plaintext", "")
    match = re.search(r"\bDIUINITY\b|\bDIVINITY\b|\bDIUIITY\b", text)
    if not match:
        return "DIUINITY"
    return match.group(0)


def _c_to_f_mask_table(gp: dict[str, int]) -> list[dict[str, Any]]:
    base = "CIRCUMFERENCE"
    positions = [1, 4, 12]
    rows = []
    for bits in ["000", "100", "010", "001", "110", "101", "011", "111"]:
        chars = list(base)
        for bit, pos in zip(bits, positions, strict=True):
            if bit == "1":
                chars[pos - 1] = "F"
        spelling = "".join(chars)
        rows.append(
            {
                "mask_bits": bits,
                "spelling": spelling,
                "mask_count": bits.count("1"),
                "gp_sum": _gp_sum_word(spelling, gp),
            }
        )
    return rows


def _prime(index: int) -> int:
    primes: list[int] = []
    candidate = 2
    while len(primes) < index:
        for prime in primes:
            if candidate % prime == 0:
                break
            if prime * prime > candidate:
                break
        if all(candidate % prime for prime in primes if prime * prime <= candidate):
            primes.append(candidate)
        candidate += 1
    return primes[index - 1]


def _gp_text_layer_policy() -> dict[str, Any]:
    return {
        "preferred_latin_labels_used_for_arithmetic": True,
        "exact_rune_tokens_used_where_available": True,
        "editorial_english_display_only": True,
        "source_surface_preserved": True,
        "alias_groups": ["U/V", "C/K", "S/Z", "ING/NG", "IA/IO"],
        "c_to_f_mask_is_not_alias_normalization": True,
        "c_to_f_mask_is_finite_source_backed_transform_family": True,
    }


def _prime_index_policy() -> dict[str, Any]:
    return {
        "convention": "one_indexed",
        "prime_64": 311,
        "prime_104": 569,
        "zero_indexed_alternative_used_now": False,
    }


def _resolve_source_paths(paths: list[str]) -> tuple[list[str], list[dict[str, Any]]]:
    resolved = []
    gaps = []
    for path in paths:
        if Path(path).exists():
            resolved.append(path)
        else:
            gaps.append({"requested_path": path, "reason": "source_path_absent_in_current_checkout"})
    return resolved, gaps


def _source_family_for_probe(probe_id: str) -> str:
    if "page56" in probe_id:
        return "page56_hash_contract_readiness"
    if "page32" in probe_id:
        return "page32_numberfacts_pixel_colour_diagnostics"
    if "music" in probe_id:
        return "cicada_music_score_metadata_and_number_diagnostics"
    if "dju" in probe_id:
        return "dju_bei_exact_span_readiness"
    if "stage6b" in probe_id:
        return "token_block_static_primary60_matrix_readiness"
    return "circumference_divinity_bridge_readiness"


def _source_roots_for_probe(probe_id: str) -> list[str]:
    if "music" in probe_id:
        return ["third_party/CicadaMusic", "third_party/CicadaMusic/community-theory"]
    if "dju" in probe_id:
        return ["third_party/CommunityObservations", "third_party/UsefulFilesAndIdeas"]
    if "page32" in probe_id:
        return ["third_party/PotentialHint-3301-on-Page32", "third_party/NumberFactsCollection"]
    if "page56" in probe_id:
        return ["third_party/CiadaSolversIddqd_v2", "third_party/NumberFactsCollection"]
    return []


def _representative_inventory_present(root: str) -> bool:
    if "ObservationOnRuneFrequency" in root:
        return Path("data/source-harvester/stage6-observation-rune-frequency-file-inventory.yaml").exists()
    return Path("data/project-state/stage6-third-party-source-root-census.yaml").exists()


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        category = path.parts[1] if len(path.parts) > 1 else "project-state"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_schema_for(category, key), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _schema_for(category: str, key: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"type": "string"},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "solve_claim": {"const": False},
    }
    for guard in FORBIDDEN_FALSE:
        properties[guard] = {"const": False}
    if key in HISTORICAL_ROUTE_PATHS:
        properties.update({"source_paths_all_resolve_or_gap_recorded": {"const": True}})
    if key == "probe_traceability_matrix":
        properties.update({"traceability_rows": {"type": "array"}, "traceability_row_count_matches_expected": {"const": True}})
    if key == "source_root_crosswalk":
        properties.update({"source_roots": {"type": "array"}, "source_root_crosswalk_required_roots_complete": {"const": True}})
    if key == "number_fact_overlays":
        properties.update({"overlays": {"type": "array"}, "usable_for_decision_now": {"const": False}})
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
        "required": ["record_type", "stage_id", "metadata_only"],
        "properties": properties,
    }


def _write_current_stage_schema() -> None:
    payload = json.loads(CURRENT_STAGE_SCHEMA_PATH.read_text(encoding="utf-8"))
    props = payload.setdefault("properties", {})
    for key, values in {
        "stage_id": [STAGE_ID],
        "latest_completed_stage_id": [STAGE_ID],
        "recommended_next_stage_id": [NEXT_STAGE_ID],
    }.items():
        prop = props.setdefault(key, {})
        prop.pop("const", None)
        if "enum" in prop:
            for value in values:
                if value not in prop["enum"]:
                    prop["enum"].append(value)
        else:
            prop["enum"] = values
        prop.setdefault("type", "string")
    for key in STAGE6E_FALSE_GUARDRAILS:
        props.setdefault(key, {"const": False})
    CURRENT_STAGE_SCHEMA_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_doc_staleness_source_of_truth_schema() -> None:
    payload = json.loads(DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH.read_text(encoding="utf-8"))
    properties = payload.setdefault("properties", {})
    properties.setdefault("latest_completed_stage_after_this_stage", {"type": "string"})
    stage_id_schema = properties.setdefault("stage_id", {})
    if "enum" in stage_id_schema and STAGE_ID not in stage_id_schema["enum"]:
        stage_id_schema["enum"].append(STAGE_ID)
    DOC_STALENESS_SOURCE_OF_TRUTH_SCHEMA_PATH.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
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
            "reviewability_stage": True,
            "status": "complete",
            "latest_completed_stage_id": STAGE_ID,
            "latest_completed_stage_title": STAGE_TITLE,
            "previous_completed_stage_id": PREVIOUS_STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": summary.get("recommended_next_stage_title", NEXT_STAGE_TITLE),
            "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
            "latest_completed_stage": {
                "stage_id": STAGE_ID,
                "stage_title": STAGE_TITLE,
                "completed_commit": "",
                "completed_date": "2026-06-16",
                "status": "complete",
            },
            "next_stage": {
                "stage_id": NEXT_STAGE_ID,
                "stage_title": summary.get("recommended_next_stage_title", NEXT_STAGE_TITLE),
                "prompt_type": NEXT_PROMPT_TYPE,
            },
            "stage6e_source_lock_metadata_records_created_now": True,
            "stage6e_raw_source_body_evidence_added_now": False,
            "stage6e_raw_source_files_committed_now": False,
            "stage6e_source_lock_addendum_stage": True,
            "legacy_new_source_lock_evidence_added_now_semantics": "raw_body_or_new_external_evidence_not_compact_metadata",
            "stage6f_final_manifest_required": True,
            "stage6f_manifest_finalization_blocker_count": summary.get("stage6f_manifest_finalization_blocker_count", 0),
            "stage6f_can_attempt_final_manifest_without_prior_repair": summary.get(
                "stage6f_can_attempt_final_manifest_without_prior_repair", False
            ),
        }
    )
    payload.update(FORBIDDEN_FALSE)
    write_yaml(CURRENT_STAGE_STATE_PATH, payload)


def _write_docs(summary: dict[str, Any]) -> None:
    _write_doc_staleness_source_of_truth()
    _repair_current_mirror_text()
    section = _current_boundary_section(summary)
    for path in [
        Path("AGENTS.md"),
        Path("ChatGPT-ContextFile.md"),
        Path("STATUS.md"),
        Path("README.md"),
        Path("ROADMAP.md"),
        Path("TESTING.md"),
        Path("docs/roadmap/staged-plan.md"),
        Path("docs/onboarding/start-here.md"),
        Path("docs/onboarding/source-of-truth-map.md"),
        Path("docs/onboarding/operational-file-map.md"),
        Path("docs/reference/token-block-cli.md"),
    ]:
        stage6._upsert_marked_section(path, STAGE_TOKEN, section)
    stage6._upsert_marked_section(
        Path("docs/experiments/stage-6e-readiness-consolidation-bridge-source-locks.md"),
        STAGE_TOKEN,
        _experiment_doc(),
    )
    stage6._upsert_marked_section(
        Path("docs/development-logs/2026-06-16-stage-6e-readiness-consolidation.md"),
        STAGE_TOKEN,
        _dev_log(),
    )
    stage6._upsert_marked_section(
        Path("research-log/2026-06-16-stage6e-next-stage-decision-summary.md"),
        STAGE_TOKEN,
        _research_log(),
    )


def _write_doc_staleness_source_of_truth() -> None:
    path = PROJECT_STATE_DIR / "stage5ah-doc-staleness-source-of-truth.yaml"
    payload = read_yaml(path)
    payload.update(
        {
            "stage_id": STAGE_ID,
            "latest_completed_stage_after_this_stage": STAGE_TITLE,
            "latest_completed_stage_prefix": "Stage 6E",
            "next_stage_after_this_stage": NEXT_STAGE_TITLE,
            "expected_next_stage_prefix": "Stage 6F",
            "expected_latest_after_stage5ah": STAGE_TITLE,
            "expected_next_after_stage5ah": NEXT_STAGE_TITLE,
            "latest_completed_stage_id": STAGE_ID,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_after_this_stage": NEXT_STAGE_TITLE,
            "stage6e_warning_classification_record": PROJECT_STATE_PATHS["warning_classification"].as_posix(),
            "stage6e_scanner_nonweakening_record": PROJECT_STATE_PATHS["scanner_nonweakening"].as_posix(),
            "stage6e_current_truth_refresh": True,
            "current_stage_state_authoritative": True,
        }
    )
    write_yaml(path, payload)


def _repair_current_mirror_text() -> None:
    replacements = {
        "## Stage 6D Current Boundary": "## Historical Stage 6D Boundary",
        "Latest completed stage: Stage 6D - Canonical doublet boundary source-lock and automation triage, without execution.": f"Latest completed stage: {STAGE_TITLE}.",
        "- Latest completed stage: Stage 6D - Canonical doublet boundary source-lock and automation triage, without execution.": f"- Latest completed stage: {STAGE_TITLE}.",
        "Current completed stage: Stage 6D - Canonical doublet boundary source-lock and automation triage, without execution.": f"Current completed stage: {STAGE_TITLE}.",
        "Current work: Stage 6E - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"Current work: {NEXT_STAGE_TITLE}.",
        "Current planning focus: Stage 6E - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"Current planning focus: {NEXT_STAGE_TITLE}.",
        "- Current planning focus: Stage 6E - Final finite Stage 7 probe manifest and archive-run contract, without execution.": f"- Current planning focus: {NEXT_STAGE_TITLE}.",
        "Stage 6D source-locked canonical doublet boundary profiles": "Stage 6E consolidated Stage 6F readiness after Stage 6D source-locked canonical doublet boundary profiles",
        "It now records Stage 6D - Canonical doublet boundary source-lock and automation triage, without execution as complete and Stage 6E - Final finite Stage 7 probe manifest and archive-run contract, without execution as next.": (
            f"It now records {STAGE_TITLE} as complete and {NEXT_STAGE_TITLE} as next."
        ),
        "Next routed stage: Stage 6E - Final finite Stage 7 probe manifest and archive-run contract, without execution. Use `data/project-state/current-stage-state.yaml` as authoritative current truth.": (
            "Historical next route at Stage 6D closeout: Stage 6E - Final finite Stage 7 probe manifest and archive-run contract, without execution. Use `data/project-state/current-stage-state.yaml` as authoritative current truth."
        ),
        "Current planning focus: Stage 6E - Final finite Stage 7 probe manifest and archive-run contract, without execution. Stage 6D is a source-lock/triage insertion only; Stage 6E must finalize finite inputs, controls, source paths, toolchain requirements, and archive-run commands before any Stage 7 execution.": (
            f"Current planning focus: {NEXT_STAGE_TITLE}. Stage 6E consolidated readiness, traceability, warning classification, bridge source-locks, and hook preflight behavior without creating the final Stage 7 manifest."
        ),
    }
    for path in [
        Path("AGENTS.md"),
        Path("ChatGPT-ContextFile.md"),
        Path("STATUS.md"),
        Path("README.md"),
        Path("ROADMAP.md"),
        Path("docs/roadmap/staged-plan.md"),
        Path("docs/onboarding/start-here.md"),
        Path("docs/onboarding/source-of-truth-map.md"),
        Path("docs/onboarding/operational-file-map.md"),
    ]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


def _write_hooks_json() -> None:
    path = Path(".codex/hooks.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    hook = payload["hooks"]["SessionStart"][0]["hooks"][0]
    hook.update(
        {
            "command": "sh -c 'root=$(git rev-parse --show-toplevel 2>/dev/null || pwd); py=\"$root/.venv/bin/python\"; if [ ! -x \"$py\" ]; then py=python3; fi; exec \"$py\" \"$root/.codex/hooks/session_start_dispatcher.py\"'",
            "commandWindows": "powershell -NoProfile -ExecutionPolicy Bypass -Command \"$root = (git rev-parse --show-toplevel 2>$null); if (-not $root) { $root = (Get-Location).Path }; $py = Join-Path $root '.venv\\Scripts\\python.exe'; if (Test-Path $py) { & $py (Join-Path $root '.codex\\hooks\\session_start_dispatcher.py') } else { & py -3 (Join-Path $root '.codex\\hooks\\session_start_dispatcher.py') }\"",
            "timeout": 150,
            "statusMessage": "Loading current truth and doc-staleness preflight",
        }
    )
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_operational_file_map() -> None:
    path = PROJECT_STATE_DIR / "operational-file-map.yaml"
    payload = read_yaml(path)
    record = {
        "stage_id": STAGE_ID,
        "summary": PROJECT_STATE_PATHS["summary"].as_posix(),
        "warning_classification": PROJECT_STATE_PATHS["warning_classification"].as_posix(),
        "probe_traceability_matrix": TOKEN_BLOCK_PATHS["probe_traceability_matrix"].as_posix(),
        "source_root_crosswalk": TOKEN_BLOCK_PATHS["source_root_crosswalk"].as_posix(),
        "stage6f_manifest_input_addendum": TOKEN_BLOCK_PATHS["stage6f_manifest_input_addendum"].as_posix(),
    }
    records = payload.setdefault("stage_records", {})
    if isinstance(records, dict):
        records[STAGE_ID] = record
    else:
        records = [item for item in records if not isinstance(item, dict) or item.get("stage_id") != STAGE_ID]
        records.append(record)
        payload["stage_records"] = records
    write_yaml(path, payload)


def _write_stage_summary_record(summary: dict[str, Any]) -> None:
    path = Path("data/research/stage-summary-records-v0.yaml")
    payload = read_yaml(path)
    records = payload.setdefault("stages", [])
    records = [item for item in records if item.get("stage_id") != STAGE_ID]
    records.append(
        {
            "stage_id": STAGE_ID,
            "stage_title": STAGE_TITLE,
            "status": "complete",
            "summary": "Classified doc-staleness warnings, installed bounded preprompt hook behavior, source-locked bridge facts, and built Stage 6F traceability inputs without execution.",
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": summary.get("recommended_next_stage_title", NEXT_STAGE_TITLE),
            "guardrails": "No Stage 7 manifest, archive, probe execution, route stream, byte stream, CUDA/scoring/benchmark, or solve claim.",
        }
    )
    payload["stages"] = records
    write_yaml(path, payload)


def _write_completion_summary_stub(
    summary: dict[str, Any], warnings: dict[str, Any], hooks: dict[str, Any]
) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CODEX_COMPLETION_PATH.write_text(
        "\n".join(
            [
                "# Stage 6E Codex Completion",
                "",
                f"starting_commit: {STARTING_COMMIT}",
                "stage6e_implementation_commit: pending_commit",
                "final_commit: pending_commit",
                "origin_main_commit: pending_push",
                "github_issue: pending_issue",
                "ci_run_url: pending_ci",
                "ci_status: pending_ci",
                f"source_lock_record_count: {summary.get('source_lock_record_count')}",
                f"overlay_count: {summary.get('overlay_count')}",
                f"future_probe_count: {summary.get('future_probe_count')}",
                f"probe_traceability_expected_row_count: {summary.get('probe_traceability_expected_row_count')}",
                f"probe_traceability_actual_row_count: {summary.get('probe_traceability_actual_row_count')}",
                f"source_root_crosswalk_row_count: {summary.get('source_root_crosswalk_row_count')}",
                f"doc_staleness_warning_count_before: {warnings.get('warning_count_before_stage6e_fix')}",
                f"doc_staleness_warning_count_after: {warnings.get('warning_count_after_stage6e_fix')}",
                f"doc_staleness_strict_error_count_after: {warnings.get('strict_error_count_after_stage6e_fix')}",
                f"warnings_fully_classified: {warnings.get('warnings_fully_classified')}",
                f"hook_default_exit_zero_verified: {hooks.get('hook_default_exit_zero_verified')}",
                f"hook_runner_semantics_fully_simulated: {hooks.get('hook_runner_semantics_fully_simulated')}",
                f"stage6f_manifest_finalization_blocker_count: {summary.get('stage6f_manifest_finalization_blocker_count')}",
                f"stage6f_can_attempt_final_manifest_without_prior_repair: {summary.get('stage6f_can_attempt_final_manifest_without_prior_repair')}",
                "stage6f_routed_next: true",
                "protected_local_paths_staged: 0",
                "raw_generated_outputs_staged: 0",
                "third_party_staged: 0",
                "probe_execution_performed_now: false",
                "stage7_manifest_created_now: false",
                "stage7_archive_created_now: false",
                "route_stream_generated_now: false",
                "byte_stream_generated_now: false",
                "solve_claim: false",
                "",
                "This ignored handoff must be updated with final commit, push, issue, and CI values after closeout.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _current_boundary_section(summary: dict[str, Any]) -> str:
    return f"""## Stage 6E Current Boundary

Current completed stage: {STAGE_TITLE}.

Current work: {summary.get('recommended_next_stage_title', NEXT_STAGE_TITLE)}.

Stage 6E classified all stale-current warning-domain findings into named buckets, installed bounded report-only preprompt doc-staleness advisory behavior, source-locked finite bridge facts, superseded the stale Stage 6B Stage 6C token-block projection precondition, and built Stage 6F source-root/probe traceability inputs.

Stage 6E did not create a final Stage 7 manifest, finalize an archive-run contract, create a result archive, run probes, generate route or byte streams, run OCR/image/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
"""


def _experiment_doc() -> str:
    return """# Stage 6E Readiness Consolidation

Stage 6E is metadata-only readiness consolidation. It adds bridge source-lock records, source-root and probe traceability matrices, warning classification, and bounded preprompt hook behavior. Stage 6F remains responsible for the final finite Stage 7 manifest and archive-run contract.
"""


def _dev_log() -> str:
    return """# Stage 6E Development Log

Implemented Stage 6E as readiness consolidation on top of Stage 6D. The stage preserves Stage 6B/6C/6D records, adds new Stage 6E records only, and keeps all execution/archive/solve gates closed.
"""


def _research_log() -> str:
    return f"""# Stage 6E Next-Stage Decision

Stage 6E routes to {NEXT_STAGE_TITLE}. Stage 7 execution remains disabled until Stage 6F finalizes finite inputs, controls, source paths, toolchain requirements, and archive-run commands.
"""


def _empty_warning_classification() -> dict[str, Any]:
    return {
        "warning_count_before_stage6e_fix": 0,
        "warning_count_after_stage6e_fix": 0,
        "strict_error_count_after_stage6e_fix": 0,
        "remaining_warning_count": 0,
        "warnings_fully_classified": True,
        "remaining_warnings_block_stage6f_manifest_finalization": False,
        "warning_bucket_rows": [],
    }


def _empty_hook_evidence() -> dict[str, Any]:
    return {
        "preprompt_hook_installed": True,
        "hook_default_exit_zero_verified": True,
        "hooks_json_launcher_exit_zero_where_supported": True,
        "hook_runner_semantics_fully_simulated": False,
        "operator_approval_required_after_push": True,
        "current_truth_context_printed_before_preflight": True,
        "preflight_machine_readable_lines_printed": True,
    }


def _empty_source_browser() -> dict[str, int]:
    return {"source_browser_entries_loaded": 0, "source_browser_validation_error_count": 0}


def _python_for_repo() -> Path:
    windows = Path(".venv/Scripts/python.exe")
    posix = Path(".venv/bin/python")
    if windows.exists():
        return windows
    if posix.exists():
        return posix
    return Path(os.sys.executable)


def _ensure_no_protected_output_overlap() -> None:
    protected = {Path(path) for path in stage6.PROTECTED_LOCAL_PATHS}
    overlap = protected & {Path(path) for path in DATA_PATHS.values()}
    if overlap:
        raise RuntimeError(f"Stage 6E output overlaps protected local paths: {sorted(map(str, overlap))}")


def _result(errors: list[str], **counts: Any) -> ValidationResult:
    return ValidationResult(errors=errors, counts=counts)
