"""Constants and small IO helpers for Stage 5AP token-block records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

STAGE_ID = "stage-5ap"
STAGE5AR_ID = "stage-5ar"
STAGE5AT_ID = "stage-5at"
STAGE5AU_ID = "stage-5au"
STAGE5AV_ID = "stage-5av"
TOKEN_BLOCK_ID = "stage5ap-page49-51-token-block"
PRIMARY_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx"
TOKEN_GRID_LINES = [
    "3N 3p 2l 36 1b 3v 26 33",
    "1W 49 2a 3g 47 04 33 3W",
    "21 3M 0F 0X 1g 2H 0x 1R",
    "1n 3l 2r 0P 2U 16 2L 2D",
    "1t 1s 3H 0d 0s 1K 2D 05",
    "1K 1O 0S 1D 3o 1I 3J 1G",
    "4D 0G 0I 0x 1Q 2p 2a 1K",
    "4E 1w 2Q 19 1k 3G 24 0p",
    "22 4F 0P 3C 3J 1D 2n 1m",
    "2i 1J 3P 2v 1s 2O 0k 1M",
    "2M 0w 3L 3D 2r 0S 1p 15",
    "3V 3e 3l 0n 3u 1O 0u 0Z",
    "3g 2U 1C 0Y 1N 3n 0W 3Q",
    "22 13 0V 3c 0E 34 0W 1t",
    "1D 2N 3H 47 0s 2p 0Z 34",
    "0g 3v 1Q 0s 0D 0K 2h 3D",
    "3L 2x 1Q 20 2n 2L 1C 2p",
    "0A 29 3r 0D 45 0k 2e 2W",
    "25 3U 1W 2r 46 2s 2X 39",
    "3p 0X 0E 1q 0q 4B 49 48",
    "3r 3b 3C 1M 1j 0I 4A 48",
    "40 3m 4E 0s 2S 1v 3T 0l",
    "3t 2B 2k 2t 2O 0e 2l 1L",
    "28 2a 0J 1L 0c 3C 2o 0X",
    "00 2Z 2d 1T 2u 1t 1j 0I",
    "1o 1E 3T 18 3E 1G 27 0L",
    "0v 2t 06 11 1A 2U 4B 1O",
    "2M 3d 2S 0x 0w 0q 0p 2V",
    "18 0q 1D 49 2O 00 1v 2t",
    "1k 3s 3G 21 3w 0W 29 2r",
    "2O 2L 0g 3Y 0M 0u 3l 3C",
    "1r 2c 2q 3o 30 0a 39 1K",
]

DATA_DIR = Path("data/token-block")
STEGO_DATA_DIR = Path("data/stego")
PROJECT_STATE_DIR = Path("data/project-state")
RESULTS_DIR = Path("experiments/results/token-block/stage5ap")
STAGE5AR_RESULTS_DIR = Path("experiments/results/token-block/stage5ar")

SOURCE_LOCK_PATH = DATA_DIR / "stage5ap-page49-51-source-lock.yaml"
IMAGE_PROVENANCE_PATH = DATA_DIR / "stage5ap-page49-51-image-provenance.yaml"
TRANSCRIPTION_PATH = DATA_DIR / "stage5ap-token-block-canonical-transcription.yaml"
COORDINATE_PATH = DATA_DIR / "stage5ap-token-block-coordinate-records.yaml"
ALPHABET_PATH = DATA_DIR / "stage5ap-token-block-alphabet-registry.yaml"
MAPPING_PATH = DATA_DIR / "stage5ap-token-block-mapping-preflight.yaml"
NULL_CONTROL_PATH = DATA_DIR / "stage5ap-token-block-null-control-plan.yaml"
DWH_CONTEXT_PATH = DATA_DIR / "stage5ap-token-block-dwh-context.yaml"
RESEARCH_SUMMARY_PATH = Path("data/research/stage5ap-page49-51-source-lock-research-summary.yaml")
NEXT_STAGE_DECISION_PATH = PROJECT_STATE_DIR / "stage5ap-next-stage-decision.yaml"
SUMMARY_PATH = PROJECT_STATE_DIR / "stage5ap-summary.yaml"

STAGE5AR_ORIGINAL_SOURCE_LOCK_PATH = DATA_DIR / "stage5ar-original-page-image-source-lock.yaml"
STAGE5AR_IMAGE_VARIANTS_PATH = DATA_DIR / "stage5ar-original-page-image-variants.yaml"
STAGE5AR_PAGE_SPLIT_POLICY_PATH = DATA_DIR / "stage5ar-page-split-policy.yaml"
STAGE5AR_PAGE_SPLIT_RECORDS_PATH = DATA_DIR / "stage5ar-page-split-records.yaml"
STAGE5AR_PIXEL_COORDINATE_POLICY_PATH = DATA_DIR / "stage5ar-token-pixel-coordinate-policy.yaml"
STAGE5AR_PIXEL_COORDINATE_RECORDS_PATH = DATA_DIR / "stage5ar-token-pixel-coordinate-records.yaml"
STAGE5AR_CASE_POLICY_PATH = DATA_DIR / "stage5ar-token-case-policy.yaml"
STAGE5AR_CASE_AMBIGUITIES_PATH = DATA_DIR / "stage5ar-token-case-ambiguity-records.yaml"
STAGE5AR_COORDINATE_VALIDATION_PATH = DATA_DIR / "stage5ar-token-coordinate-validation.yaml"
STAGE5AR_SOURCE_LOCK_UPDATE_PATH = DATA_DIR / "stage5ar-token-block-source-lock-update.yaml"
STAGE5AR_NULL_CONTROL_UPDATE_PATH = DATA_DIR / "stage5ar-token-block-null-control-update.yaml"
STAGE5AR_DWH_CONTEXT_PATH = DATA_DIR / "stage5ar-dwh-coordinate-context.yaml"
STAGE5AR_GUARDRAIL_PATH = DATA_DIR / "stage5ar-guardrail.yaml"
STAGE5AR_NEXT_STAGE_DECISION_PATH = PROJECT_STATE_DIR / "stage5ar-next-stage-decision.yaml"
STAGE5AR_SUMMARY_PATH = PROJECT_STATE_DIR / "stage5ar-summary.yaml"

STAGE5AT_RESULTS_DIR = Path("experiments/results/token-block/stage5at")
STAGE5AT_REVIEW_PACK_ROOT = Path("human-review-packs/stage5at/token-case-review")
STAGE5AT_CASE_REVIEW_POLICY_PATH = DATA_DIR / "stage5at-case-review-policy.yaml"
STAGE5AT_CASE_REVIEW_CHALLENGE_SET_PATH = DATA_DIR / "stage5at-case-review-challenge-set.yaml"
STAGE5AT_CANONICAL_CHALLENGE_SET_PATH = DATA_DIR / "stage5at-canonical-transcription-challenge-set.yaml"
STAGE5AT_CROP_MANIFEST_PATH = DATA_DIR / "stage5at-case-review-crop-manifest.yaml"
STAGE5AT_DECISION_TEMPLATE_PATH = DATA_DIR / "stage5at-human-review-decision-template.yaml"
STAGE5AT_PACK_MANIFEST_PATH = DATA_DIR / "stage5at-case-review-pack-manifest.yaml"
STAGE5AT_VARIANT_REPAIR_PATH = DATA_DIR / "stage5at-variant-classifier-repair-summary.yaml"
STAGE5AT_DOC_DRIFT_PATH = DATA_DIR / "stage5at-doc-drift-repair-summary.yaml"
STAGE5AT_NULL_CONTROL_UPDATE_PATH = DATA_DIR / "stage5at-null-control-case-update.yaml"
STAGE5AT_DWH_CASE_CONTEXT_PATH = DATA_DIR / "stage5at-dwh-case-context.yaml"
STAGE5AT_GUARDRAIL_PATH = DATA_DIR / "stage5at-guardrail.yaml"
STAGE5AT_NEXT_STAGE_DECISION_PATH = PROJECT_STATE_DIR / "stage5at-next-stage-decision.yaml"
STAGE5AT_SUMMARY_PATH = PROJECT_STATE_DIR / "stage5at-summary.yaml"

STAGE5AU_RESULTS_DIR = Path("experiments/results/token-block/stage5au")
STAGE5AU_REVIEW_PACK_ROOT = Path("human-review-packs/stage5au/token-case-review-v2")
STAGE5AU_USABILITY_AUDIT_PATH = DATA_DIR / "stage5au-review-pack-usability-audit.yaml"
STAGE5AU_CROP_GEOMETRY_POLICY_PATH = DATA_DIR / "stage5au-crop-geometry-policy.yaml"
STAGE5AU_CROP_QUALITY_PATH = DATA_DIR / "stage5au-crop-quality-diagnostics.yaml"
STAGE5AU_CASE_CHALLENGES_V2_PATH = DATA_DIR / "stage5au-case-review-challenge-set-v2.yaml"
STAGE5AU_CANONICAL_CHALLENGES_V2_PATH = DATA_DIR / "stage5au-canonical-transcription-challenge-set-v2.yaml"
STAGE5AU_PACK_MANIFEST_PATH = DATA_DIR / "stage5au-review-pack-v2-manifest.yaml"
STAGE5AU_UI_COVERAGE_PATH = DATA_DIR / "stage5au-review-pack-v2-ui-coverage.yaml"
STAGE5AU_DECISION_TEMPLATE_PATH = DATA_DIR / "stage5au-human-review-decision-template-v2.yaml"
STAGE5AU_NULL_CONTROL_UPDATE_PATH = DATA_DIR / "stage5au-null-control-review-pack-update.yaml"
STAGE5AU_DWH_CONTEXT_PATH = DATA_DIR / "stage5au-dwh-review-pack-context.yaml"
STAGE5AU_GUARDRAIL_PATH = DATA_DIR / "stage5au-guardrail.yaml"
STAGE5AU_NEXT_STAGE_DECISION_PATH = PROJECT_STATE_DIR / "stage5au-next-stage-decision.yaml"
STAGE5AU_SUMMARY_PATH = PROJECT_STATE_DIR / "stage5au-summary.yaml"

STAGE5AV_RESULTS_DIR = Path("experiments/results/token-block/stage5av")
STAGE5AV_LOCAL_DECISION_TEMPLATE_PATH = (
    STAGE5AU_REVIEW_PACK_ROOT / "decision-template.yaml"
)
STAGE5AV_DECISION_FILE_INGEST_PATH = DATA_DIR / "stage5av-decision-file-ingest.yaml"
STAGE5AV_DECISION_FILE_VALIDATION_PATH = (
    DATA_DIR / "stage5av-decision-file-validation.yaml"
)
STAGE5AV_HUMAN_REVIEW_DECISIONS_PATH = (
    DATA_DIR / "stage5av-human-review-decision-records.yaml"
)
STAGE5AV_CONFIRMED_TOKENS_PATH = DATA_DIR / "stage5av-confirmed-token-records.yaml"
STAGE5AV_UNRESOLVED_VARIANTS_PATH = (
    DATA_DIR / "stage5av-unresolved-token-variant-records.yaml"
)
STAGE5AV_REVIEWER_EXTRA_TOKENS_PATH = (
    DATA_DIR / "stage5av-reviewer-extra-possible-tokens.yaml"
)
STAGE5AV_PRIMARY60_IMPACT_PATH = (
    DATA_DIR / "stage5av-primary60-variant-impact-summary.yaml"
)
STAGE5AV_BRANCH_MANIFEST_PATH = (
    DATA_DIR / "stage5av-token-variant-branch-manifest.yaml"
)
STAGE5AV_CANONICAL_UPDATE_PATH = (
    DATA_DIR / "stage5av-canonical-transcription-update.yaml"
)
STAGE5AV_NULL_CONTROL_UPDATE_PATH = (
    DATA_DIR / "stage5av-null-control-decision-update.yaml"
)
STAGE5AV_DWH_CONTEXT_PATH = DATA_DIR / "stage5av-dwh-decision-context.yaml"
STAGE5AV_GUARDRAIL_PATH = DATA_DIR / "stage5av-guardrail.yaml"
STAGE5AV_NEXT_STAGE_DECISION_PATH = PROJECT_STATE_DIR / "stage5av-next-stage-decision.yaml"
STAGE5AV_SUMMARY_PATH = PROJECT_STATE_DIR / "stage5av-summary.yaml"

STAGE5AW_ID = "stage-5aw"
STAGE5AW_RESULTS_DIR = Path("experiments/results/token-block/stage5aw")
STAGE5AW_DECISION_PARSER_AUDIT_PATH = DATA_DIR / "stage5aw-decision-parser-audit.yaml"
STAGE5AW_PARSER_POLICY_PATH = DATA_DIR / "stage5aw-possible-token-parser-policy.yaml"
STAGE5AW_REPAIRED_HUMAN_REVIEW_DECISIONS_PATH = (
    DATA_DIR / "stage5aw-repaired-human-review-decision-records.yaml"
)
STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH = (
    DATA_DIR / "stage5aw-repaired-unresolved-token-variant-records.yaml"
)
STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH = (
    DATA_DIR / "stage5aw-repaired-reviewer-extra-possible-tokens.yaml"
)
STAGE5AW_MALFORMED_FRAGMENTS_PATH = (
    DATA_DIR / "stage5aw-malformed-possible-token-fragments.yaml"
)
STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH = (
    DATA_DIR / "stage5aw-repaired-primary60-variant-impact-summary.yaml"
)
STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH = (
    DATA_DIR / "stage5aw-repaired-token-variant-branch-manifest.yaml"
)
STAGE5AW_CANONICAL_UPDATE_PATH = DATA_DIR / "stage5aw-canonical-transcription-update.yaml"
STAGE5AW_NULL_CONTROL_UPDATE_PATH = DATA_DIR / "stage5aw-null-control-decision-update.yaml"
STAGE5AW_DWH_CONTEXT_PATH = DATA_DIR / "stage5aw-dwh-decision-context.yaml"
STAGE5AW_GUARDRAIL_PATH = DATA_DIR / "stage5aw-guardrail.yaml"
STAGE5AW_NEXT_STAGE_DECISION_PATH = PROJECT_STATE_DIR / "stage5aw-next-stage-decision.yaml"
STAGE5AW_SUMMARY_PATH = PROJECT_STATE_DIR / "stage5aw-summary.yaml"

STAGE5AY_ID = "stage-5ay"
STAGE5AY_RESULTS_DIR = Path("experiments/results/token-block/stage5ay")
STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH = DATA_DIR / "stage5ay-preflight-source-inputs.yaml"
STAGE5AY_PREFLIGHT_DESIGN_POLICY_PATH = DATA_DIR / "stage5ay-preflight-design-policy.yaml"
STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH = DATA_DIR / "stage5ay-branch-eligibility-policy.yaml"
STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH = DATA_DIR / "stage5ay-bounded-variant-family-manifest.yaml"
STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH = DATA_DIR / "stage5ay-null-control-family-manifest.yaml"
STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH = DATA_DIR / "stage5ay-alphabet-control-manifest.yaml"
STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH = DATA_DIR / "stage5ay-reading-order-control-manifest.yaml"
STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH = DATA_DIR / "stage5ay-page-split-control-manifest.yaml"
STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH = DATA_DIR / "stage5ay-source-control-manifest.yaml"
STAGE5AY_BRANCH_COUNT_BUDGET_PATH = DATA_DIR / "stage5ay-branch-count-budget.yaml"
STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH = DATA_DIR / "stage5ay-future-result-schema-preview.yaml"
STAGE5AY_EXECUTION_GATES_PATH = DATA_DIR / "stage5ay-execution-gates.yaml"
STAGE5AY_DWH_PREFLIGHT_CONTEXT_PATH = DATA_DIR / "stage5ay-dwh-preflight-context.yaml"
STAGE5AY_GUARDRAIL_PATH = DATA_DIR / "stage5ay-guardrail.yaml"
STAGE5AY_NEXT_STAGE_DECISION_PATH = PROJECT_STATE_DIR / "stage5ay-next-stage-decision.yaml"
STAGE5AY_SUMMARY_PATH = PROJECT_STATE_DIR / "stage5ay-summary.yaml"

STAGE5AZ_ID = "stage-5az"
STAGE5AZ_RESULTS_DIR = Path("experiments/results/token-block/stage5az")
STAGE5AZ_PREFLIGHT_MANIFEST_INTEGRITY_AUDIT_PATH = (
    DATA_DIR / "stage5az-preflight-manifest-integrity-audit.yaml"
)
STAGE5AZ_FAMILY_ID_UNIQUENESS_AUDIT_PATH = (
    DATA_DIR / "stage5az-family-id-uniqueness-audit.yaml"
)
STAGE5AZ_MANIFEST_REFERENCE_AUDIT_PATH = DATA_DIR / "stage5az-manifest-reference-audit.yaml"
STAGE5AZ_FAMILY_TAXONOMY_MEMBERSHIP_POLICY_PATH = (
    DATA_DIR / "stage5az-family-taxonomy-membership-policy.yaml"
)
STAGE5AZ_REPAIRED_PREFLIGHT_DESIGN_POLICY_PATH = (
    DATA_DIR / "stage5az-repaired-preflight-design-policy.yaml"
)
STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH = (
    DATA_DIR / "stage5az-repaired-bounded-variant-family-manifest.yaml"
)
STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH = (
    DATA_DIR / "stage5az-repaired-branch-count-budget.yaml"
)
STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH = DATA_DIR / "stage5az-repaired-execution-gates.yaml"
STAGE5AZ_DEEP_RESEARCH_READINESS_PATH = DATA_DIR / "stage5az-deep-research-readiness.yaml"
STAGE5AZ_DWH_MANIFEST_INTEGRITY_CONTEXT_PATH = (
    DATA_DIR / "stage5az-dwh-manifest-integrity-context.yaml"
)
STAGE5AZ_GUARDRAIL_PATH = DATA_DIR / "stage5az-guardrail.yaml"
STAGE5AZ_NEXT_STAGE_DECISION_PATH = PROJECT_STATE_DIR / "stage5az-next-stage-decision.yaml"
STAGE5AZ_SUMMARY_PATH = PROJECT_STATE_DIR / "stage5az-summary.yaml"

STAGE5BB_ID = "stage-5bb"
STAGE5BB_RESULTS_DIR = Path("experiments/results/token-block/stage5bb")
STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH = DATA_DIR / "stage5bb-active-manifest-registry.yaml"
STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH = DATA_DIR / "stage5bb-manifest-precedence-policy.yaml"
STAGE5BB_LEGACY_POINTER_AUDIT_PATH = DATA_DIR / "stage5bb-legacy-pointer-audit.yaml"
STAGE5BB_MANIFEST_REFERENCE_VALIDATION_PATH = DATA_DIR / "stage5bb-manifest-reference-validation.yaml"
STAGE5BB_BRANCH_ELIGIBILITY_REFERENCE_VALIDATION_PATH = (
    DATA_DIR / "stage5bb-branch-eligibility-reference-validation.yaml"
)
STAGE5BB_LOADER_SCAFFOLD_POLICY_PATH = DATA_DIR / "stage5bb-loader-scaffold-policy.yaml"
STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH = DATA_DIR / "stage5bb-runner-scaffold-manifest.yaml"
STAGE5BB_DRY_RUN_PLAN_PREVIEW_PATH = DATA_DIR / "stage5bb-dry-run-plan-preview.yaml"
STAGE5BB_BRANCH_COUNTER_SUMMARY_PATH = DATA_DIR / "stage5bb-branch-counter-summary.yaml"
STAGE5BB_FAMILY_ENUMERATION_SUMMARY_PATH = DATA_DIR / "stage5bb-family-enumeration-summary.yaml"
STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH = (
    DATA_DIR / "stage5bb-execution-gate-enforcement-policy.yaml"
)
STAGE5BB_EXECUTION_GATE_VALIDATION_PATH = DATA_DIR / "stage5bb-execution-gate-validation.yaml"
STAGE5BB_RESULT_SCHEMA_FIXTURE_POLICY_PATH = DATA_DIR / "stage5bb-result-schema-fixture-policy.yaml"
STAGE5BB_FIXTURE_RESULT_SCHEMA_RECORDS_PATH = DATA_DIR / "stage5bb-fixture-result-schema-records.yaml"
STAGE5BB_VALIDATION_EVIDENCE_INDEX_PATH = DATA_DIR / "stage5bb-validation-evidence-index.yaml"
STAGE5BB_NO_EXECUTION_PROOF_PATH = DATA_DIR / "stage5bb-no-execution-proof.yaml"
STAGE5BB_DWH_RUNNER_CONTEXT_PATH = DATA_DIR / "stage5bb-dwh-runner-context.yaml"
STAGE5BB_GUARDRAIL_PATH = DATA_DIR / "stage5bb-guardrail.yaml"
STAGE5BB_NEXT_STAGE_DECISION_PATH = PROJECT_STATE_DIR / "stage5bb-next-stage-decision.yaml"
STAGE5BB_SUMMARY_PATH = PROJECT_STATE_DIR / "stage5bb-summary.yaml"

FALSE_GUARDRAILS = {
    "network_fetch_performed": False,
    "online_repo_clone_performed": False,
    "google_drive_storage_used": False,
    "deep_research_performed": False,
    "ocr_performed": False,
    "ai_ml_interpretation_performed": False,
    "broad_image_forensics_performed": False,
    "stego_tool_execution_performed": False,
    "lp_page_outguess_run_performed": False,
    "hash_preimage_search_performed": False,
    "hypothesis_execution_performed": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "benchmark_performed": False,
    "scored_experiments_executed": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "generated_outputs_committed": False,
    "raw_data_committed": False,
    "solve_claim": False,
}


def token_rows() -> list[list[str]]:
    """Return the canonical 32x8 token grid."""

    return [line.split() for line in TOKEN_GRID_LINES]


def canonical_text() -> str:
    """Return the canonical token text with a trailing newline."""

    return "\n".join(TOKEN_GRID_LINES) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()
