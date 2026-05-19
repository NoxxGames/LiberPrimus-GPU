"""Constants for Stage 4M image preflight records."""

from __future__ import annotations

from pathlib import Path

DEFAULT_IMAGE_DIR = Path("third_party/LiberPrimusPages")
DEFAULT_IMAGE_ARTIFACTS = Path("data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl")
DEFAULT_IMAGE_LOCKS = Path("data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl")
DEFAULT_SOURCE_DELTA = Path("data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml")
DEFAULT_COMPRESSION_OBSERVATIONS = Path(
    "data/observations/visual/stage4e-image-compression-artifact-observations.yaml"
)
DEFAULT_PROMOTION_READINESS = Path("data/observations/review/stage4l-observation-promotion-readiness-records.yaml")
DEFAULT_MANIFEST_READINESS = Path("data/observations/review/stage4l-manifest-readiness-records.yaml")
DEFAULT_BIGRAM_IMAGE = Path("data/raw/images/Fib421.jpg")
DEFAULT_OUT_DIR = Path("experiments/results/image-preflight/stage4m")

DEFAULT_SOURCE_VARIANT_OUT = Path("data/observations/visual/stage4m-image-source-variant-preflight-records.yaml")
DEFAULT_COMPRESSION_OUT = Path("data/observations/visual/stage4m-image-compression-preflight-records.yaml")
DEFAULT_ARTIFACT_CANDIDATES_OUT = Path("data/observations/visual/stage4m-image-artifact-review-candidates.yaml")
DEFAULT_SUMMARY_OUT = Path("data/observations/visual/stage4m-image-preflight-summary.yaml")
DEFAULT_BIGRAM_READINESS_OUT = Path("data/observations/review/stage4m-bigram-frequency-pattern-readiness.yaml")

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
EXPECTED_BIGRAM_IMAGE_SHA256 = "e9b5c84c1283fee3a0eeb5d0b9ed848e2049c5768ccfade48d58bd29dbefa321"
BIGRAM_FUTURE_MANIFEST_ID = "exp_stage4m_bigram_diagonal_fibonacci_421_audit"
BIGRAM_BLOCKERS = [
    "blocked_needs_reproducible_bigram_matrix",
    "blocked_needs_declared_rune_order",
    "blocked_needs_transcript_profile_source",
    "blocked_needs_null_model",
    "blocked_needs_multiple_testing_control",
]

COMMON_FALSE_FLAGS = {
    "raw_image_committed": False,
    "generated_image_committed": False,
    "solve_claim": False,
    "trusted_as_canonical": False,
    "usable_as_experiment_seed": False,
    "image_interpretation_claim": False,
}
