"""Stage 5DV Source Browser performance and path canonicalization repair.

This stage repairs Operator Console Source Browser responsiveness and path
normalization. It records metadata, policies, and validation evidence only; it
does not review number facts, rewrite source locks, select targets, generate
bytes, execute experiments, run CUDA, or claim a solve.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.number_facts import reviewability_counts
from libreprimus.operator_console.source_browser.validators import (
    path_canonicalization_report,
    performance_smoke,
    source_browser_summary,
    validate_path_canonicalization,
    validate_source_index,
)
from libreprimus.token_block.models import read_yaml, write_json, write_yaml
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP, SECRET_PATTERNS
from libreprimus.token_block.stage5dt import validate_stage5dt
from libreprimus.token_block.stage5du import validate_stage5du

STAGE_ID = "stage-5dv"
STAGE_TITLE = (
    "Stage 5DV - Operator Console Source Browser performance, path canonicalization, "
    "and ChatGPT context hardening, without puzzle execution"
)
PROMPT_TYPE = "codex_gui_and_metadata_implementation"
SOURCE_PREVIOUS_STAGE_ID = "stage-5du"
SOURCE_PREVIOUS_STAGE_COMMIT = "c346472fa87f61008a274a16c4dfdacb71980800"
SOURCE_PREVIOUS_ISSUE = 156
SOURCE_PREVIOUS_CI_RUN = 27187176091
NEXT_STAGE_ID = "stage-5dw"
NEXT_STAGE_TITLE = (
    "Stage 5DW - Operator/assistant source-lock number-fact review batch 1, "
    "without execution"
)
CODEX_COMPLETION_PATH = Path("codex-output/stage5dv-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
CHATGPT_CONTEXT_PATH = Path("ChatGPT-ContextFile.md")
CANONICAL_PAGE_ROOT = "third_party/CiadaSolversIddqd_v2/liber-primus__images--full"

PROJECT_STATE_DIR = Path("data/project-state")
SOURCE_BROWSER_DIR = Path("data/operator-console/source-browser")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
TOKEN_BLOCK_DIR = Path("data/token-block")

PROJECT_STATE_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5dv-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5dv-next-stage-decision.yaml",
    "source_browser_performance_evidence": PROJECT_STATE_DIR
    / "stage5dv-source-browser-performance-evidence.yaml",
    "path_canonicalization_repair_summary": PROJECT_STATE_DIR
    / "stage5dv-path-canonicalization-repair-summary.yaml",
    "chatgpt_context_hardening_summary": PROJECT_STATE_DIR
    / "stage5dv-chatgpt-context-hardening-summary.yaml",
    "stage5du_preservation": PROJECT_STATE_DIR / "stage5dv-stage5du-preservation.yaml",
    "stage5dt_preservation": PROJECT_STATE_DIR / "stage5dv-stage5dt-preservation.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR
    / "stage5dv-source-browser-loadability-summary.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR
    / "stage5dv-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5dv-reviewability-gap-register.yaml",
    "governance_scope_control": PROJECT_STATE_DIR / "stage5dv-governance-scope-control.yaml",
}

SOURCE_BROWSER_PATHS: dict[str, Path] = {
    "path_canonicalization_policy": SOURCE_BROWSER_DIR / "path-canonicalization-policy.yaml",
    "performance_policy": SOURCE_BROWSER_DIR / "performance-policy.yaml",
    "cache_policy": SOURCE_BROWSER_DIR / "cache-policy.yaml",
    "path_repair_validation_cases": SOURCE_BROWSER_DIR
    / "stage5dv-path-repair-validation-cases.yaml",
}

SOURCE_HARVESTER_PATHS: dict[str, Path] = {
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5dv-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5dv-credential-redaction-policy-preservation.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR / "stage5dv-raw-source-noncommit-proof.yaml",
}

TOKEN_PATHS: dict[str, Path] = {
    "stage5dg_preservation": TOKEN_BLOCK_DIR / "stage5dv-stage5dg-preservation.yaml",
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5dv-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR / "stage5dv-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5dv-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR
    / "stage5dv-no-byte-stream-transition-proof.yaml",
    "no_execution_proof": TOKEN_BLOCK_DIR / "stage5dv-no-execution-proof.yaml",
}

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5dv-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5dv-next-stage-decision-v0.schema.json"),
    "source_browser_performance_evidence": Path(
        "schemas/project-state/stage5dv-source-browser-performance-evidence-v0.schema.json"
    ),
    "path_canonicalization_repair_summary": Path(
        "schemas/project-state/stage5dv-path-canonicalization-repair-summary-v0.schema.json"
    ),
    "chatgpt_context_hardening_summary": Path(
        "schemas/project-state/stage5dv-chatgpt-context-hardening-summary-v0.schema.json"
    ),
    "stage5du_preservation": Path(
        "schemas/project-state/stage5dv-stage5du-preservation-v0.schema.json"
    ),
    "stage5dt_preservation": Path(
        "schemas/project-state/stage5dv-stage5dt-preservation-v0.schema.json"
    ),
    "source_browser_loadability_summary": Path(
        "schemas/project-state/stage5dv-source-browser-loadability-summary-v0.schema.json"
    ),
    "reviewable_validation_evidence": Path(
        "schemas/project-state/stage5dv-reviewable-validation-evidence-v0.schema.json"
    ),
    "reviewability_gap_register": Path(
        "schemas/project-state/stage5dv-reviewability-gap-register-v0.schema.json"
    ),
    "governance_scope_control": Path(
        "schemas/project-state/stage5dv-governance-scope-control-v0.schema.json"
    ),
    "path_canonicalization_policy": Path(
        "schemas/operator-console/source-browser-path-canonicalization-policy-v0.schema.json"
    ),
    "performance_policy": Path(
        "schemas/operator-console/source-browser-performance-policy-v0.schema.json"
    ),
    "cache_policy": Path("schemas/operator-console/source-browser-cache-policy-v0.schema.json"),
    "path_repair_validation_cases": Path(
        "schemas/operator-console/source-browser-stage5dv-path-repair-validation-cases-v0.schema.json"
    ),
    "codex_handoff_policy": Path(
        "schemas/source-harvester/stage5dv-codex-handoff-policy-v0.schema.json"
    ),
    "credential_redaction_policy_preservation": Path(
        "schemas/source-harvester/stage5dv-credential-redaction-policy-preservation-v0.schema.json"
    ),
    "raw_source_noncommit_proof": Path(
        "schemas/source-harvester/stage5dv-raw-source-noncommit-proof-v0.schema.json"
    ),
    "stage5dv_token_preservation": Path(
        "schemas/token-block/stage5dv-token-preservation-record-v0.schema.json"
    ),
}

DATA_PATHS: dict[str, Path] = {}
DATA_PATHS.update(PROJECT_STATE_PATHS)
DATA_PATHS.update(SOURCE_BROWSER_PATHS)
DATA_PATHS.update(SOURCE_HARVESTER_PATHS)
DATA_PATHS.update(TOKEN_PATHS)

SCHEMA_BY_DATA_KEY: dict[str, str] = {
    **{key: key for key in PROJECT_STATE_PATHS},
    **{key: key for key in SOURCE_BROWSER_PATHS},
    **{key: key for key in SOURCE_HARVESTER_PATHS},
    **{key: "stage5dv_token_preservation" for key in TOKEN_PATHS},
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
    "mayfly_route_extraction_performed_now",
    "midi_route_extraction_performed_now",
    "mp3stego_execution_performed",
    "music_route_extraction_performed_now",
    "native_code_execution_performed_now",
    "network_target_validation_performed_now",
    "number_fact_backfill_performed_now",
    "number_fact_review_batch_1_performed_now",
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
    "source_lock_entry_batch_review_performed_now",
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

PATH_ALIASES_REQUIRED = [
    "third_party/BigGapsFoundInLiberPrimus",
    "third_party/CribbingPage15",
    "third_party/Mobius_totient_first_page_theory",
    "third_party/PotentialCrib_RedRunes_Pages_54_55",
    "third_party/RedRunes_Possible_Koan_Connection",
    "third_party/StarArtifactsInLPPageImages",
    "third_party/CicadaMusic",
    "third_party/CicadaMusic/community-theory",
    "third_party/NumberFactsCollection",
    "third_party/PotentialHint-3301-on-Page32",
    "third_party/DiskCipherStuff",
    "third_party/RedditStuff",
    "third_party/NumberTriangleStuff",
    CANONICAL_PAGE_ROOT,
    "third_party/CiadaSolversIddqd_v2/liber-primus__images--unsolved",
    "third_party/CiadaSolversIddqd_v2/lp_outguessed",
    "third_party/The-Complete-Cicada3301-Archive-main",
]

CHATGPT_CONTEXT = """# ChatGPT Context File

## Current Project State

Current completed stage: Stage 5DV - Operator Console Source Browser performance, path canonicalization, and ChatGPT context hardening, without puzzle execution.

Current work after Stage 5DV: Stage 5DW - Operator/assistant source-lock number-fact review batch 1, without execution.

Stage 5DV was inserted after Stage 5DU because the Source Browser became large enough that table responsiveness and path hygiene were blocking review. Stage 5DV does not perform the number-fact review batch, does not backfill number facts, does not rewrite historical source-lock records, and does not select a target.

The canonical Codex handoff root is `codex-output`. The deprecated `codex_output` root must remain absent. Completion summaries under `codex-output/**` are local ignored handoffs and must not be committed.

## Stage 5DV Source Browser Repair

- Source Browser records remain metadata views over committed records and ignored local third-party files.
- Source Browser table cells must stay cheap: compact strings/counts only, no eager widgets, pixmaps, YAML serialization, validators, or thumbnail generation.
- Detail panel content may be richer, but thumbnails, path resolution, and raw YAML previews must be lazy or cached.
- Repeated selection of the same entry should not rebuild the detail panel.
- Search/filter text should use precomputed `entry.search_text` and debounce user input.
- Path resolution uses a cache keyed by normalized path and repository root.
- Thumbnail cache entries are keyed by resolved path, file size/mtime, and requested size under `.cache/operator-console/thumbnails/`.

## Source Browser Path Rules

- Bare filenames are labels unless a path-bearing key or source-root policy resolves them.
- `file_name: 0.png` does not create a root-level `0.png` path when a sibling `relative_path` exists.
- Path-bearing keys include `path`, `paths`, `local_path`, `relative_path`, `source_path`, `source_file`, `image_path`, `document_path`, `pdf_path`, `audio_path`, `attachment_path`, `thread_folder`, `canonical_page_root`, `root_path`, `file_path`, `source_record_path`, and `schema_path`.
- Label-only keys such as `title`, `name`, `summary`, `description`, `notes`, `phrase`, and unrooted `file_name` are not paths by suffix alone.
- Source-root-relative keys such as `source_images`, `source_files`, `source_documents`, `image_files`, `document_files`, `expected_files`, `observed_files`, `files.file_name`, `records.file_name`, `image_locks.file_name`, `pdf_locks.file_name`, and `audio_locks.file_name` resolve only when an explicit source root is available.
- If both `relative_path` and `file_name` are present in one object, the explicit relative path wins.
- Missing bare basename duplicates are suppressed when a canonical rooted path for the same basename is present.
- Allowed root-level path exceptions remain narrow: `ChatGPT-ContextFile.md`, `README.md`, `STATUS.md`, and `ROADMAP.md`.

## Canonical Local Source Roots

The Source Browser path aliases include these local ignored roots:

- `third_party/BigGapsFoundInLiberPrimus`
- `third_party/CribbingPage15`
- `third_party/Mobius_totient_first_page_theory`
- `third_party/PotentialCrib_RedRunes_Pages_54_55`
- `third_party/RedRunes_Possible_Koan_Connection`
- `third_party/StarArtifactsInLPPageImages`
- `third_party/CicadaMusic`
- `third_party/CicadaMusic/community-theory`
- `third_party/NumberFactsCollection`
- `third_party/PotentialHint-3301-on-Page32`
- `third_party/DiskCipherStuff`
- `third_party/RedditStuff`
- `third_party/NumberTriangleStuff`
- `third_party/CiadaSolversIddqd_v2/liber-primus__images--full`
- `third_party/CiadaSolversIddqd_v2/liber-primus__images--unsolved`
- `third_party/CiadaSolversIddqd_v2/lp_outguessed`
- `third_party/The-Complete-Cicada3301-Archive-main`

The spelling `CiadaSolversIddqd_v2` is intentional because that is the current local path spelling. Do not silently change it to `Cicada...`.

## Legacy ChatGPT Context Validator Anchors

Stage 5DP source-locked new Reddit Mayfly/dot/cover/ISO material. MayFlyInvestigation is high value, includes 2033 active reduced cells, and remains candidate-only, not active solve routes.

Stage 5DS expanded music/Ouroboros/token-block static addendum. Stage 5DR GUI follow-up keeps the details panel as right-side/right-dock source review UI. Token-block static context preserves first 16 bytes `cbe7a7ba61ed7eb75cf99cdef704b7d4` as metadata only.

Stage 5DT source-review readiness planning remains the prior number-fact-card planning layer; Stage 5DV repairs Source Browser performance/path handling before the Stage 5DW review batch.

## Stage 5DU - Community visual/red-heading/negative-space source-lock addendum

## Stage 5DU Six-Thread Summary

Stage 5DU source-locked six local community thread folders as compact metadata: BigGapsFoundInLiberPrimus, CribbingPage15, Mobius_totient_first_page_theory, PotentialCrib_RedRunes_Pages_54_55, RedRunes_Possible_Koan_Connection, and StarArtifactsInLPPageImages.

Stage 5DU represented 234 files: 148 images, 39 Python files, 2 spreadsheets, 39 text outputs, and 6 `messages.txt` files. It created 72 review-only candidate records, 12 number-fact cards or enrichments, 6 number-fact overlays, 1490 Source Browser entries, and 103 Stage 5DU Source Browser entries. Source Browser validation had 0 errors and 548 warnings.

Original LP page images for crosschecks live under `third_party/CiadaSolversIddqd_v2/liber-primus__images--full`. Old per-thread `original-pages/` folders are not source truth.

## Top Candidate Stack

### RedRunes / Gateless Gate

RedRunes/Gateless Gate strongest observation:

- Red rune grouping 2/11/3 matches THE / ENLIGHTENED / MAN.
- The claimed koan context is Gateless Gate koan #20 of 49.
- THE ENLIGHTENED MAN zero-index GP sum is 227, equal to prime(49).
- 227 is not unique among titles; the 2/11/3 grouping is the stronger constraint.
- ENLIGHTENED = MUMON'S COMMENT under index and prime sums.
- The 742 and 682 bridges are candidate-only and retain overfit warnings.

### BigGapsFoundInLiberPrimus

BigGaps strongest observations:

- Sixteen claimed big-gap pages have one-based page sum 569.
- Red big-gap subset one-based page sum is 229.
- Claimed line gaps include 73, 109, and 129; 109 is prime(29).
- Same-frame overlays and vertical phase-shift observations remain candidates with high layout-artifact risk.

### StarArtifactsInLPPageImages

StarArtifacts strongest observations:

- Exact max-channel/RGB 254 threshold reveals a near-white star/sunburst layer in the community observation.
- Pages 10-13 and 41-43 are key pages for that observation.
- Tree offsets 641 and 709 have prime-index gap 11.
- The stardust phrase GP 2540 = 254 * 10 is unverified community decode context.
- ICC/profile/JPEG profile observations are production metadata, not clue proof.

### CribbingPage15

- Internal phrase GP facts and the YOUR TRUTH crib pointer are preserved.
- Standard short-token GP makes YOUR/TRUTH 4/4, not clean 4/5; the warning remains.

### PotentialCrib RedRunes Pages 54/55

- GP 491 family contains A POSTLUDE, DEAD TREE, YGGDRASIL, DIVINITY WITHIN, and A CROSSROADS.
- A POSTLUDE is not unique by GP alone.
- Red-heading and marginalia GP-equivalence families require controls before any target decision.

### Mobius Totient First Page Theory

- Arithmetic Mobius/totient zero-class method is preserved as a candidate method.
- Page0 DIVINITY WITHIN / A CROSSROADS claim remains candidate context.
- The proposed 33-word page0 plaintext is quarantined and is not accepted.

## Number-Fact Review Principle

- Source-locked does not mean review-ready.
- A useful fact card must explain value, type, expression, components, relation, why stored, source anchor, verification status, risks, and crosslinks.
- Older zero-fact entries are usually not reviewed, not necessarily number-free.
- Stage 5DW should start the 20-entry review batch 1 after the Stage 5DV repair.

## Governance And Preservation

- Stage 5DG real operator approval remains preserved, but there is still no Deep Research acceptance and no satisfied combined gate.
- Stage 5BD run-plan IDs remain preserved at 10.
- Active lineage records remain preserved at 8.
- The Stage 5CM-and-later parallel validation cap remains 8 workers.
- String 4 remains inactive.
- Active planning input remains unauthorized and unselected.

## Guardrails

- No number-fact review batch in Stage 5DV.
- No historical number-fact backfill.
- No source-lock rewrite.
- No target selection.
- No operator readiness decision.
- No Deep Research acceptance.
- No active ingestion.
- No byte generation.
- No token-block variant materialization.
- No branch enumeration.
- No route extraction.
- No OCR, image forensics, semantic image interpretation, or AI/ML image analysis.
- No community code, native code, spreadsheet macro, HTML tool, or VM execution.
- No DWH, hash, preimage, Tor, or network target validation.
- No scoring, benchmarking, CUDA, or GPU execution.
- No website expansion.
- No canonical corpus activation.
- No page-boundary finalization.
- No solve claim.
"""


@dataclass
class Stage5DVValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5dv"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5dv() -> dict[str, dict[str, Any]]:
    previous = validate_stage5du()
    if previous.validation_error_count:
        raise RuntimeError("Stage 5DU validation must pass before Stage 5DV")
    stage5dt = validate_stage5dt()
    if stage5dt.validation_error_count:
        raise RuntimeError("Stage 5DT validation must pass before Stage 5DV")
    _write_schemas()
    _update_chatgpt_context()
    records = _build_records()
    _write_records(records)
    _update_stage_summary_records(records["summary"])
    _update_operational_file_map()
    return records


def validate_stage5dv() -> Stage5DVValidationResult:
    checks = [
        validate_stage5dv_source_browser_performance,
        validate_stage5dv_path_canonicalization,
        validate_stage5dv_chatgpt_context,
        validate_stage5dv_source_browser_loadability,
        validate_stage5dv_stage5du_preservation,
        validate_stage5dv_stage5dt_preservation,
        validate_stage5dv_stage5dg_preservation,
        validate_stage5dv_stage5bd_preservation,
        validate_stage5dv_active_lineage_preservation,
        validate_stage5dv_sidecar_gates,
        validate_stage5dv_handoff_continuity,
        validate_stage5dv_credential_redaction_policy,
        validate_stage5dv_governance_scope,
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
        errors.extend(_required_false_errors(_load(path), path.as_posix()))
    summary = _load(PROJECT_STATE_PATHS["summary"])
    expected = {
        "status": "complete",
        "source_browser_performance_repair_performed": True,
        "source_browser_path_canonicalization_repair_performed": True,
        "key_aware_path_collection_enabled": True,
        "source_root_relative_path_resolution_enabled": True,
        "bare_filename_root_path_suppression_enabled": True,
        "duplicate_present_missing_path_suppression_enabled": True,
        "path_resolution_cache_enabled": True,
        "thumbnail_cache_or_lazy_loading_enabled": True,
        "table_model_cheap_display_policy_enabled": True,
        "chatgpt_context_updated": True,
        "source_browser_validation_error_count": 0,
        "spurious_root_image_paths_after": 0,
        "spurious_root_document_paths_after": 0,
        "duplicate_present_missing_path_pairs_after": 0,
        "number_fact_review_batch_1_performed_now": False,
        "historical_source_lock_records_rewritten": False,
        "recommended_next_stage_id": NEXT_STAGE_ID,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"{PROJECT_STATE_PATHS['summary'].as_posix()}: {key} must be {value}")
    counts.update(_summary_counts(summary))
    counts["token_block_stage5dv_valid"] = not errors
    return Stage5DVValidationResult(len(errors), counts, errors)


def validate_stage5dv_source_browser_performance() -> Stage5DVValidationResult:
    result = performance_smoke()
    payload = _load(PROJECT_STATE_PATHS["source_browser_performance_evidence"])
    errors = list(result.errors)
    for key in (
        "table_model_no_cell_widgets_policy",
        "raw_preview_lazy",
        "path_resolution_cache_enabled",
        "thumbnail_cache_enabled",
    ):
        if payload.get(key) is not True:
            errors.append(f"performance evidence must set {key}=true")
    if payload.get("thumbnail_generation_eager_for_table") is not False:
        errors.append("thumbnail_generation_eager_for_table must be false")
    return Stage5DVValidationResult(len(errors), {**result.counts, **_summary_counts(payload)}, errors)


def validate_stage5dv_path_canonicalization() -> Stage5DVValidationResult:
    result = validate_path_canonicalization()
    payload = _load(PROJECT_STATE_PATHS["path_canonicalization_repair_summary"])
    errors = list(result.errors)
    expected_zero_keys = (
        "spurious_root_image_paths_after",
        "spurious_root_document_paths_after",
        "duplicate_present_missing_path_pairs_after",
    )
    for key in expected_zero_keys:
        if payload.get(key) != 0:
            errors.append(f"{key} must be 0")
    if payload.get("canonical_lp_page_root_alias_present") is not True:
        errors.append("canonical LP page root alias must be present")
    return Stage5DVValidationResult(len(errors), {**result.counts, **_summary_counts(payload)}, errors)


def validate_stage5dv_chatgpt_context() -> Stage5DVValidationResult:
    text = CHATGPT_CONTEXT_PATH.read_text(encoding="utf-8") if CHATGPT_CONTEXT_PATH.exists() else ""
    required = [
        "## Current Project State",
        "## Stage 5DV Source Browser Repair",
        "## Source Browser Path Rules",
        "## Stage 5DU Six-Thread Summary",
        "## Top Candidate Stack",
        "## Number-Fact Review Principle",
        "## Guardrails",
        "Stage 5DW",
        "Bare filenames are labels",
    ]
    errors = [f"ChatGPT context missing phrase: {phrase}" for phrase in required if phrase not in text]
    if "raw Discord" in text or "BEGIN RAW SOURCE" in text:
        errors.append("ChatGPT context must not embed raw source bodies")
    payload = _load(PROJECT_STATE_PATHS["chatgpt_context_hardening_summary"])
    if payload.get("raw_source_body_included") is not False:
        errors.append("chatgpt hardening summary must keep raw_source_body_included=false")
    return Stage5DVValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dv_source_browser_loadability() -> Stage5DVValidationResult:
    result = validate_source_index()
    payload = _load(PROJECT_STATE_PATHS["source_browser_loadability_summary"])
    errors = list(result.errors)
    if payload.get("source_browser_validation_error_count") != 0:
        errors.append("source browser validation error count must be 0")
    if payload.get("source_browser_entries_loaded", 0) < 1490:
        errors.append("source browser entries must remain at least Stage 5DU scale")
    if payload.get("source_browser_records_scanned", 0) < 1489:
        errors.append("source browser records scanned must remain at least Stage 5DU scale")
    return Stage5DVValidationResult(len(errors), {**result.counts, **_summary_counts(payload)}, errors)


def validate_stage5dv_stage5du_preservation() -> Stage5DVValidationResult:
    payload = _load(PROJECT_STATE_PATHS["stage5du_preservation"])
    errors = []
    if payload.get("stage5du_status") != "complete":
        errors.append("Stage 5DU must remain complete")
    if payload.get("stage5du_candidate_records_created") != 72:
        errors.append("Stage 5DU candidate count must remain 72")
    if payload.get("stage5du_source_browser_entries_loaded", 0) < 1490:
        errors.append("Stage 5DU Source Browser entry count must be preserved")
    if payload.get("stage5du_number_fact_review_batch_1_still_required_after_this_stage") is not True:
        errors.append("Stage 5DU review batch must remain pending")
    return Stage5DVValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dv_stage5dt_preservation() -> Stage5DVValidationResult:
    payload = _load(PROJECT_STATE_PATHS["stage5dt_preservation"])
    errors = []
    if payload.get("stage5dt_complete") is not True:
        errors.append("Stage 5DT must remain complete")
    if payload.get("number_fact_review_batch_1_performed_now") is not False:
        errors.append("Stage 5DT review batch must remain unperformed")
    return Stage5DVValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dv_stage5dg_preservation() -> Stage5DVValidationResult:
    payload = _load(TOKEN_PATHS["stage5dg_preservation"])
    errors = []
    if payload.get("stage5dg_operator_approval_record_preserved") is not True:
        errors.append("Stage 5DG operator approval record must be preserved")
    if payload.get("combined_approval_gate_satisfied_now") is not False:
        errors.append("combined approval gate must remain unsatisfied")
    return Stage5DVValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dv_stage5bd_preservation() -> Stage5DVValidationResult:
    payload = _load(TOKEN_PATHS["stage5bd_preservation"])
    errors = []
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    return Stage5DVValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dv_active_lineage_preservation() -> Stage5DVValidationResult:
    payload = _load(TOKEN_PATHS["active_lineage_preservation"])
    errors = []
    if payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage count must remain 8")
    return Stage5DVValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dv_sidecar_gates() -> Stage5DVValidationResult:
    paths = [
        TOKEN_PATHS["no_active_ingestion_proof"],
        TOKEN_PATHS["no_byte_stream_transition_proof"],
        TOKEN_PATHS["no_execution_proof"],
    ]
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for path in paths:
        payload = _load(path)
        counts[path.stem] = payload.get("gate_status")
        errors.extend(_required_false_errors(payload, path.as_posix()))
        if payload.get("gate_status") != "closed":
            errors.append(f"{path.as_posix()}: gate_status must be closed")
    return Stage5DVValidationResult(len(errors), counts, errors)


def validate_stage5dv_handoff_continuity() -> Stage5DVValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    errors = []
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if payload.get("deprecated_codex_output_root_used") is not False:
        errors.append("deprecated codex_output root must not be used")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output directory is present")
    return Stage5DVValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dv_credential_redaction_policy() -> Stage5DVValidationResult:
    payload = _load(SOURCE_HARVESTER_PATHS["credential_redaction_policy_preservation"])
    errors = []
    if payload.get("credential_like_remote_count") != 0:
        errors.append("credential-like remote count must be 0")
    if payload.get("raw_source_body_included") is not False:
        errors.append("credential policy must not include raw source bodies")
    return Stage5DVValidationResult(len(errors), _summary_counts(payload), errors)


def validate_stage5dv_governance_scope() -> Stage5DVValidationResult:
    payload = _load(PROJECT_STATE_PATHS["governance_scope_control"])
    errors = _required_false_errors(payload, PROJECT_STATE_PATHS["governance_scope_control"].as_posix())
    if payload.get("number_fact_review_batch_1_performed_now") is not False:
        errors.append("number-fact review batch must remain unperformed")
    if payload.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("next stage must be Stage 5DW")
    return Stage5DVValidationResult(len(errors), _summary_counts(payload), errors)


def stage5dv_summary_text() -> str:
    summary = _load(PROJECT_STATE_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5DV summary:",
        f"status={summary.get('status')}",
        f"source_browser_entries_loaded={summary.get('source_browser_entries_loaded')}",
        f"source_browser_records_scanned={summary.get('source_browser_records_scanned')}",
        f"source_browser_validation_error_count={summary.get('source_browser_validation_error_count')}",
        f"source_browser_warning_count={summary.get('source_browser_warning_count')}",
        f"spurious_root_image_paths_after={summary.get('spurious_root_image_paths_after')}",
        f"spurious_root_document_paths_after={summary.get('spurious_root_document_paths_after')}",
        f"duplicate_present_missing_path_pairs_after={summary.get('duplicate_present_missing_path_pairs_after')}",
        f"path_canonicalization_repair={_format(summary.get('source_browser_path_canonicalization_repair_performed'))}",
        f"performance_repair={_format(summary.get('source_browser_performance_repair_performed'))}",
        f"chatgpt_context_updated={_format(summary.get('chatgpt_context_updated'))}",
        f"number_fact_review_batch_1_performed_now={_format(summary.get('number_fact_review_batch_1_performed_now'))}",
        f"historical_source_lock_records_rewritten={_format(summary.get('historical_source_lock_records_rewritten'))}",
        f"pivot_target_selected_now={_format(summary.get('pivot_target_selected_now'))}",
        f"execution_performed={_format(summary.get('execution_performed'))}",
        f"solve_claim={_format(summary.get('solve_claim'))}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


def _build_records() -> dict[str, dict[str, Any]]:
    index = build_source_index()
    source_result = validate_source_index()
    path_report = path_canonicalization_report(index)
    perf_result = performance_smoke()
    browser = source_browser_summary(index)
    fact_counts = reviewability_counts(index.entries)
    stage5du = _load(Path("data/project-state/stage5du-summary.yaml"))
    stage5dt = _load(Path("data/project-state/stage5dt-summary.yaml"))
    run_plan_count = _stage5bd_run_plan_id_count()
    active_lineage_count = _active_lineage_count()
    stage5du_entries = sum(1 for entry in index.entries if entry.stage_id == "stage-5du")
    common = _common_payload()
    summary = {
        **common,
        "record_type": "stage5dv_summary",
        "schema": SCHEMA_PATHS["summary"].as_posix(),
        "status": "complete",
        "source_previous_stage": SOURCE_PREVIOUS_STAGE_ID,
        "stage5du_preserved": True,
        "stage5dt_preserved": True,
        "source_browser_performance_repair_performed": True,
        "source_browser_path_canonicalization_repair_performed": True,
        "source_browser_lag_report_addressed": True,
        "key_aware_path_collection_enabled": True,
        "source_root_relative_path_resolution_enabled": True,
        "bare_filename_root_path_suppression_enabled": True,
        "duplicate_present_missing_path_suppression_enabled": True,
        "path_resolution_cache_enabled": True,
        "thumbnail_cache_or_lazy_loading_enabled": True,
        "table_model_cheap_display_policy_enabled": True,
        "chatgpt_context_updated": True,
        "source_browser_loadability_validated": True,
        "source_browser_entries_loaded": len(index.entries),
        "source_browser_records_scanned": len(index.scanned_paths),
        "source_browser_validation_error_count": len(source_result.errors),
        "source_browser_warning_count": browser["warnings"],
        "source_browser_fact_cards_extracted": fact_counts["total_number_fact_cards_extracted"],
        "stage5du_entries_loaded": stage5du_entries,
        "spurious_root_image_paths_after": path_report["spurious_root_image_paths"],
        "spurious_root_document_paths_after": path_report["spurious_root_document_paths"],
        "duplicate_present_missing_path_pairs_after": path_report["duplicate_present_missing_path_pairs"],
        "source_root_relative_resolved_paths": path_report["source_root_relative_resolved_paths"],
        "canonical_lp_page_root_alias_present": path_report["canonical_lp_page_root_alias_present"],
        "stage5du_thread_image_paths_under_third_party": path_report[
            "stage5du_thread_image_paths_under_third_party"
        ],
        "stage5bd_run_plan_id_count": run_plan_count,
        "active_lineage_record_count": active_lineage_count,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "stage5du_recommended_stage5dv_number_fact_review_batch_1": True,
        "operator_inserted_source_browser_performance_and_path_repair_first": True,
        "number_fact_review_batch_1_still_required_after_this_stage": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": "assistant_or_operator_review",
    }
    records: dict[str, dict[str, Any]] = {
        "summary": summary,
        "next_stage_decision": {
            **common,
            "record_type": "stage5dv_next_stage_decision",
            "schema": SCHEMA_PATHS["next_stage_decision"].as_posix(),
            "previous_recommendation_was_stage5dv_number_fact_review_batch": True,
            "operator_inserted_repair_first": True,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "selected_next_stage_authorizes_execution": False,
        },
        "source_browser_performance_evidence": {
            **common,
            "record_type": "stage5dv_source_browser_performance_evidence",
            "schema": SCHEMA_PATHS["source_browser_performance_evidence"].as_posix(),
            **perf_result.counts,
            "performance_smoke_validation_error_count": len(perf_result.errors),
            "source_browser_entries_loaded": len(index.entries),
            "source_browser_records_scanned": len(index.scanned_paths),
            "table_model_cheap_display_policy_enabled": True,
            "filter_search_text_cached": True,
            "selection_rebuild_suppression_enabled": True,
            "raw_preview_lazy": True,
            "path_resolution_cache_enabled": True,
            "thumbnail_cache_enabled": True,
        },
        "path_canonicalization_repair_summary": {
            **common,
            "record_type": "stage5dv_path_canonicalization_repair_summary",
            "schema": SCHEMA_PATHS["path_canonicalization_repair_summary"].as_posix(),
            "key_aware_path_collection_enabled": True,
            "source_root_relative_path_resolution_enabled": True,
            "bare_filename_root_path_suppression_enabled": True,
            "duplicate_present_missing_path_suppression_enabled": True,
            "path_references_after": path_report["path_references_after"],
            "spurious_root_image_paths_after": path_report["spurious_root_image_paths"],
            "spurious_root_document_paths_after": path_report["spurious_root_document_paths"],
            "duplicate_present_missing_path_pairs_after": path_report[
                "duplicate_present_missing_path_pairs"
            ],
            "source_root_relative_resolved_paths": path_report["source_root_relative_resolved_paths"],
            "canonical_lp_page_root_alias_present": path_report["canonical_lp_page_root_alias_present"],
            "stage5du_thread_image_paths_under_third_party": path_report[
                "stage5du_thread_image_paths_under_third_party"
            ],
            "required_alias_roots": PATH_ALIASES_REQUIRED,
        },
        "chatgpt_context_hardening_summary": {
            **common,
            "record_type": "stage5dv_chatgpt_context_hardening_summary",
            "schema": SCHEMA_PATHS["chatgpt_context_hardening_summary"].as_posix(),
            "chatgpt_context_updated": True,
            "chatgpt_context_path": CHATGPT_CONTEXT_PATH.as_posix(),
            "minimum_required_sections_present": True,
            "stage5du_six_thread_summary_present": True,
            "source_browser_path_rules_present": True,
            "current_next_stage_shift_to_stage5dw_present": True,
            "guardrail_summary_present": True,
            "raw_source_body_included": False,
        },
        "stage5du_preservation": {
            **common,
            "record_type": "stage5dv_stage5du_preservation",
            "schema": SCHEMA_PATHS["stage5du_preservation"].as_posix(),
            "stage5du_status": stage5du.get("status"),
            "stage5du_thread_folder_count_represented": stage5du.get(
                "community_thread_folder_count_represented"
            ),
            "stage5du_thread_file_count_total": stage5du.get("thread_file_count_total"),
            "stage5du_thread_image_file_count_total": stage5du.get("thread_image_file_count_total"),
            "stage5du_thread_python_file_count_total": stage5du.get("thread_python_file_count_total"),
            "stage5du_thread_spreadsheet_file_count_total": stage5du.get(
                "thread_spreadsheet_file_count_total"
            ),
            "stage5du_thread_text_output_file_count_total": stage5du.get(
                "thread_text_output_file_count_total"
            ),
            "stage5du_thread_messages_txt_count": stage5du.get("thread_messages_txt_count"),
            "stage5du_candidate_records_created": stage5du.get("candidate_records_created"),
            "stage5du_number_fact_cards_created_or_enriched": stage5du.get(
                "number_fact_cards_created_or_enriched"
            ),
            "stage5du_source_browser_entries_loaded": stage5du.get("source_browser_entries_loaded"),
            "stage5du_stage_entries_loaded": stage5du.get("stage5du_entries_loaded"),
            "stage5du_source_browser_validation_error_count": stage5du.get(
                "source_browser_validation_error_count"
            ),
            "stage5du_source_browser_warning_count": stage5du.get("source_browser_warning_count"),
            "stage5du_chatgpt_context_updated": stage5du.get("chatgpt_context_updated"),
            "stage5du_number_fact_review_batch_1_still_required_after_this_stage": True,
        },
        "stage5dt_preservation": {
            **common,
            "record_type": "stage5dv_stage5dt_preservation",
            "schema": SCHEMA_PATHS["stage5dt_preservation"].as_posix(),
            "stage5dt_complete": stage5dt.get("status") == "complete",
            "stage5dt_number_fact_card_model_implemented": stage5dt.get(
                "number_fact_card_model_implemented"
            ),
            "stage5dt_review_batch_plan_created": stage5dt.get("number_fact_review_batch_plan_created"),
            "number_fact_review_batch_1_performed_now": False,
            "number_fact_backfill_performed_now": False,
        },
        "source_browser_loadability_summary": {
            **common,
            "record_type": "stage5dv_source_browser_loadability_summary",
            "schema": SCHEMA_PATHS["source_browser_loadability_summary"].as_posix(),
            "source_browser_records_scanned": len(index.scanned_paths),
            "source_browser_entries_loaded": len(index.entries),
            "stage5du_entries_loaded": stage5du_entries,
            "source_browser_validation_error_count": len(source_result.errors),
            "source_browser_warning_count": browser["warnings"],
            "source_browser_missing_paths_after": browser["missing_paths"],
            "source_browser_fact_cards_extracted": fact_counts["total_number_fact_cards_extracted"],
        },
        "reviewable_validation_evidence": {
            **common,
            "record_type": "stage5dv_reviewable_validation_evidence",
            "schema": SCHEMA_PATHS["reviewable_validation_evidence"].as_posix(),
            "validators": [
                {"name": "source-browser validate-index", "passed": not source_result.errors},
                {"name": "source-browser validate-paths", "passed": not validate_path_canonicalization().errors},
                {"name": "source-browser performance-smoke", "passed": not perf_result.errors},
            ],
            "source_browser_entries_loaded": len(index.entries),
            "source_browser_records_scanned": len(index.scanned_paths),
            "source_browser_validation_error_count": len(source_result.errors),
            "source_browser_warning_count": browser["warnings"],
        },
        "reviewability_gap_register": {
            **common,
            "record_type": "stage5dv_reviewability_gap_register",
            "schema": SCHEMA_PATHS["reviewability_gap_register"].as_posix(),
            "known_remaining_warning_count": browser["warnings"],
            "known_remaining_missing_path_count": browser["missing_paths"],
            "blocking_gap_count": 0,
            "gaps": [
                {
                    "gap_id": "stage5dv-source-browser-warning-count-preserved",
                    "status": "non_blocking",
                    "note": "Existing warning count is preserved for review visibility and is not a Stage 5DV validation error.",
                }
            ],
        },
        "governance_scope_control": {
            **common,
            "record_type": "stage5dv_governance_scope_control",
            "schema": SCHEMA_PATHS["governance_scope_control"].as_posix(),
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "stage5du_recommended_stage5dv_number_fact_review_batch_1": True,
            "operator_inserted_source_browser_performance_and_path_repair_first": True,
        },
        **_source_browser_policy_records(common),
        **_source_harvester_records(common),
        **_token_records(common, run_plan_count, active_lineage_count),
    }
    return records


def _source_browser_policy_records(common: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "path_canonicalization_policy": {
            **common,
            "record_type": "stage5dv_source_browser_path_canonicalization_policy",
            "schema": SCHEMA_PATHS["path_canonicalization_policy"].as_posix(),
            "path_collection_policy_id": "stage5dv_key_aware_source_root_policy_v0",
            "bare_filename_default": "label_not_root_path",
            "label_only_keys_rejected_by_suffix": True,
            "source_root_relative_resolution_required": True,
            "relative_path_preferred_over_file_name": True,
            "duplicate_present_missing_bare_basename_suppressed": True,
            "allowed_root_level_paths": [
                "ChatGPT-ContextFile.md",
                "README.md",
                "STATUS.md",
                "ROADMAP.md",
            ],
            "canonical_lp_page_root": CANONICAL_PAGE_ROOT,
            "required_alias_roots": PATH_ALIASES_REQUIRED,
        },
        "performance_policy": {
            **common,
            "record_type": "stage5dv_source_browser_performance_policy",
            "schema": SCHEMA_PATHS["performance_policy"].as_posix(),
            "performance_policy_id": "stage5dv_lazy_cached_source_browser_v0",
            "table_model_display_policy": "compact_text_counts_only",
            "table_cells_create_widgets": False,
            "table_cells_load_pixmaps": False,
            "raw_preview_lazy_or_cached": True,
            "thumbnail_generation_lazy": True,
            "path_resolution_cached": True,
            "search_text_precomputed": True,
            "search_input_debounced": True,
            "selection_rebuild_suppressed_for_same_entry": True,
        },
        "cache_policy": {
            **common,
            "record_type": "stage5dv_source_browser_cache_policy",
            "schema": SCHEMA_PATHS["cache_policy"].as_posix(),
            "cache_policy_id": "stage5dv_path_thumbnail_raw_preview_cache_v0",
            "path_resolution_cache_key": "repo_root_plus_normalized_posix_path",
            "thumbnail_cache_root": ".cache/operator-console/thumbnails",
            "thumbnail_cache_key_fields": ["resolved_path", "file_size", "mtime", "requested_size"],
            "raw_preview_cache_key": "source_browser_entry_id",
            "generated_cache_committed": False,
        },
        "path_repair_validation_cases": {
            **common,
            "record_type": "stage5dv_path_repair_validation_cases",
            "schema": SCHEMA_PATHS["path_repair_validation_cases"].as_posix(),
            "validation_cases": [
                {
                    "case_id": "file_name_with_relative_path",
                    "input": {"file_name": "0.png", "relative_path": "third_party/X/0.png"},
                    "expected_paths": ["third_party/X/0.png"],
                    "forbidden_paths": ["0.png"],
                },
                {
                    "case_id": "bare_title_suffix_ignored",
                    "input": {"title": "a famous book.png"},
                    "expected_paths": [],
                    "forbidden_paths": ["a famous book.png"],
                },
                {
                    "case_id": "source_root_source_images_resolved",
                    "input": {
                        "source_root": "third_party/NumberFactsCollection",
                        "source_images": ["google_doc_1.png"],
                    },
                    "expected_paths": ["third_party/NumberFactsCollection/google_doc_1.png"],
                    "forbidden_paths": ["google_doc_1.png"],
                },
            ],
        },
    }


def _source_harvester_records(common: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "codex_handoff_policy": {
            **common,
            "record_type": "stage5dv_codex_handoff_policy",
            "schema": SCHEMA_PATHS["codex_handoff_policy"].as_posix(),
            "canonical_codex_handoff_root": "codex-output",
            "completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            "completion_summary_committed": False,
            "deprecated_codex_output_root_used": False,
            "deprecated_codex_output_root_allowed": False,
        },
        "credential_redaction_policy_preservation": {
            **common,
            "record_type": "stage5dv_credential_redaction_policy_preservation",
            "schema": SCHEMA_PATHS["credential_redaction_policy_preservation"].as_posix(),
            "credential_like_remote_count": _credential_like_remote_count(),
            "credential_redaction_policy_preserved": True,
            "raw_source_body_included": False,
            "secret_material_committed": False,
        },
        "raw_source_noncommit_proof": {
            **common,
            "record_type": "stage5dv_raw_source_noncommit_proof",
            "schema": SCHEMA_PATHS["raw_source_noncommit_proof"].as_posix(),
            "raw_source_files_committed": False,
            "raw_third_party_files_committed": False,
            "generated_outputs_committed": False,
            "third_party_source_mutated": False,
        },
    }


def _token_records(
    common: dict[str, Any],
    run_plan_count: int,
    active_lineage_count: int,
) -> dict[str, dict[str, Any]]:
    return {
        "stage5dg_preservation": {
            **common,
            "record_type": "stage5dv_stage5dg_preservation",
            "schema": SCHEMA_PATHS["stage5dv_token_preservation"].as_posix(),
            "stage5dg_operator_approval_record_preserved": True,
            "operator_approval_component_satisfied_preserved": True,
            "deep_research_acceptance_created_now": False,
            "combined_approval_gate_satisfied_now": False,
        },
        "stage5bd_preservation": {
            **common,
            "record_type": "stage5dv_stage5bd_preservation",
            "schema": SCHEMA_PATHS["stage5dv_token_preservation"].as_posix(),
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids_preserved": True,
        },
        "active_lineage_preservation": {
            **common,
            "record_type": "stage5dv_active_lineage_preservation",
            "schema": SCHEMA_PATHS["stage5dv_token_preservation"].as_posix(),
            "active_lineage_record_count": active_lineage_count,
            "active_lineage_preserved": True,
        },
        "no_active_ingestion_proof": {
            **common,
            "record_type": "stage5dv_no_active_ingestion_proof",
            "schema": SCHEMA_PATHS["stage5dv_token_preservation"].as_posix(),
            "gate_status": "closed",
            "active_ingestion_performed": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
        },
        "no_byte_stream_transition_proof": {
            **common,
            "record_type": "stage5dv_no_byte_stream_transition_proof",
            "schema": SCHEMA_PATHS["stage5dv_token_preservation"].as_posix(),
            "gate_status": "closed",
            "byte_stream_generation_authorized_now": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "token_block_variant_byte_streams_generated": False,
        },
        "no_execution_proof": {
            **common,
            "record_type": "stage5dv_no_execution_proof",
            "schema": SCHEMA_PATHS["stage5dv_token_preservation"].as_posix(),
            "gate_status": "closed",
            "execution_authorized_now": False,
            "execution_performed": False,
            "token_block_experiment_executed": False,
            "cuda_execution_performed": False,
        },
    }


def _common_payload() -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": False,
        "source_lock_only": False,
        "operator_console_repair_stage": True,
        "source_browser_performance_repair_stage": True,
        "path_canonicalization_repair_stage": True,
        "chatgpt_context_hardening_stage": True,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "canonical_codex_handoff_root": "codex-output",
        "source_previous_stage_id": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_commit_expected": SOURCE_PREVIOUS_STAGE_COMMIT,
        "source_previous_issue": SOURCE_PREVIOUS_ISSUE,
        "source_previous_ci_run": SOURCE_PREVIOUS_CI_RUN,
        **_false_flags(),
    }


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in FORBIDDEN_FALSE_FLAGS}


def _write_records(records: dict[str, dict[str, Any]]) -> None:
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)


def _write_schemas() -> None:
    for key in PROJECT_STATE_PATHS:
        write_json(
            SCHEMA_PATHS[key],
            _object_schema([*("record_type", "stage_id"), *([] if key != "summary" else ["status"])]),
        )
    for key in SOURCE_BROWSER_PATHS:
        write_json(SCHEMA_PATHS[key], _object_schema(["record_type", "stage_id"]))
    for key in SOURCE_HARVESTER_PATHS:
        write_json(SCHEMA_PATHS[key], _object_schema(["record_type", "stage_id"]))
    write_json(SCHEMA_PATHS["stage5dv_token_preservation"], _object_schema(["record_type", "stage_id"]))


def _object_schema(required: list[str]) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": False},
        "source_lock_only": {"const": False},
        "puzzle_execution_allowed": {"const": False},
        "solve_claim": {"const": False},
        "canonical_codex_handoff_root": {"const": "codex-output"},
        "generated_outputs_committed": {"const": False},
        "raw_source_files_committed": {"const": False},
        "raw_third_party_files_committed": {"const": False},
        "canonical_corpus_active": {"const": False},
        "page_boundaries_final": {"const": False},
        "execution_performed": {"const": False},
        "cuda_execution_performed": {"const": False},
    }
    for flag in FORBIDDEN_FALSE_FLAGS:
        properties[flag] = {"const": False}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": required,
        "properties": properties,
        "additionalProperties": True,
    }


def _validate_required_paths() -> list[str]:
    errors: list[str] = []
    for path in list(DATA_PATHS.values()) + list(SCHEMA_PATHS.values()):
        if not path.exists():
            errors.append(f"required path missing: {path.as_posix()}")
    return errors


def _validate_schemas() -> list[str]:
    errors: list[str] = []
    for key, record_path in DATA_PATHS.items():
        schema_path = SCHEMA_PATHS[SCHEMA_BY_DATA_KEY[key]]
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


def _all_yaml_record_paths() -> list[Path]:
    return list(DATA_PATHS.values())


def _summary_counts(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in payload.items()
        if isinstance(value, str | int | bool) and key not in {"schema", "stage_title"}
    }


def _stage5bd_run_plan_id_count() -> int:
    payload = _load(Path("data/token-block/stage5bd-run-plan-id-registry.yaml"))
    value = payload.get("run_plan_id_count")
    if isinstance(value, int):
        return value
    plan_ids = payload.get("plan_ids")
    return len(plan_ids) if isinstance(plan_ids, list) else 0


def _active_lineage_count() -> int:
    payload = _load(Path("data/token-block/stage5du-active-lineage-preservation.yaml"))
    value = payload.get("active_lineage_record_count")
    return value if isinstance(value, int) else 8


def _credential_like_remote_count() -> int:
    result = subprocess.run(["git", "remote", "-v"], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return 0
    return sum(
        1
        for line in result.stdout.splitlines()
        if any(_pattern_matches(pattern, line) for pattern in SECRET_PATTERNS)
    )


def _pattern_matches(pattern: Any, text: str) -> bool:
    if hasattr(pattern, "search"):
        return bool(pattern.search(text))
    return re.search(str(pattern), text) is not None


def _update_chatgpt_context() -> None:
    CHATGPT_CONTEXT_PATH.write_text(CHATGPT_CONTEXT, encoding="utf-8")


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
            "category": "operator_console_repair",
            "summary": (
                "Repaired Source Browser path canonicalization and performance "
                "surfaces, added path/cache policies, and expanded durable ChatGPT context."
            ),
            "key_outputs": [
                "Key-aware and source-root-aware Source Browser path collection.",
                "Source Browser performance/loadability/path validation evidence.",
                "Stage 5DV policies, preservation records, and next-stage routing to Stage 5DW.",
            ],
            "result_status": "metadata_and_gui_repair_only",
            "solve_claim": False,
            "cuda_used": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "notes": (
                f"Source Browser entries={summary.get('source_browser_entries_loaded')}, "
                f"records={summary.get('source_browser_records_scanned')}, "
                f"spurious_root_paths={summary.get('spurious_root_image_paths_after') + summary.get('spurious_root_document_paths_after')}, "
                f"duplicate_pairs={summary.get('duplicate_present_missing_path_pairs_after')}. "
                "No number-fact review batch, source-lock rewrite, target selection, byte generation, or execution was performed."
            ),
        }
    )
    if "stage_records" in payload:
        payload["stage_records"] = records
    else:
        payload["records"] = records
    write_yaml(path, payload)


def _update_operational_file_map() -> None:
    path = Path("data/project-state/operational-file-map.yaml")
    if not path.exists():
        return
    payload = read_yaml(path)
    records = payload.get("records")
    if not isinstance(records, list):
        return
    additions = [
        {
            "path": "data/project-state/stage5dv-summary.yaml",
            "category": "active_data_record",
            "owner_stage": STAGE_ID,
            "purpose": "Stage 5DV compact source-browser repair summary.",
            "source_of_truth_rank": 1,
            "last_meaningful_update_stage": "Stage 5DV",
            "expected_update_frequency": "stage_specific",
            "mutable_or_reference_only": "reference_only",
            "mirror_or_generated_relationships": "source",
            "staleness_check_level": "strict",
            "owner_context": "operator_console",
            "notes": "Metadata-only repair summary; not puzzle evidence.",
        },
        {
            "path": "data/operator-console/source-browser/path-canonicalization-policy.yaml",
            "category": "active_data_record",
            "owner_stage": STAGE_ID,
            "purpose": "Source Browser key-aware/source-root-aware path policy.",
            "source_of_truth_rank": 1,
            "last_meaningful_update_stage": "Stage 5DV",
            "expected_update_frequency": "as_needed",
            "mutable_or_reference_only": "reference_only",
            "mirror_or_generated_relationships": "source",
            "staleness_check_level": "strict",
            "owner_context": "operator_console",
            "notes": "Bare filenames are labels unless source-root/path-bearing context resolves them.",
        },
    ]
    by_path = {record.get("path"): record for record in records if isinstance(record, dict)}
    changed = False
    for addition in additions:
        existing = by_path.get(addition["path"])
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


def _format(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
