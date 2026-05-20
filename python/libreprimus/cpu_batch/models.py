"""Models and defaults for Stage 4H CPU batch transforms."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT_DIR = Path("experiments/results/cpu-batch/stage4h")
STAGE4O_OUTPUT_DIR = Path("experiments/results/cpu-batch/stage4o")
DEFAULT_SUMMARY_PATH = Path("data/research/stage4h-cpu-batch-api-summary.yaml")
STAGE4O_SUMMARY_PATH = Path("data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml")
DEFAULT_REGISTRY = Path("data/transform-registry/cpu-reference-transforms-v0.json")

CPU_BATCH_MANIFEST_SCHEMA = Path("schemas/experiments/cpu-batch-manifest-v0.schema.json")
CPU_BATCH_INPUT_SCHEMA = Path("schemas/experiments/cpu-batch-input-stream-v0.schema.json")
CPU_BATCH_CANDIDATE_SCHEMA = Path("schemas/experiments/cpu-batch-transform-candidate-v0.schema.json")
CPU_BATCH_RESULT_SCHEMA = Path("schemas/experiments/cpu-batch-result-record-v0.schema.json")
CPU_BATCH_SUMMARY_SCHEMA = Path("schemas/experiments/cpu-batch-run-summary-v0.schema.json")
CPU_CUDA_PARITY_SCHEMA = Path("schemas/experiments/cpu-cuda-parity-contract-v0.schema.json")
CPU_BATCH_ADAPTER_COVERAGE_SCHEMA = Path("schemas/experiments/cpu-batch-adapter-coverage-v0.schema.json")
CPU_BATCH_PARITY_EXPECTATION_SCHEMA = Path("schemas/experiments/cpu-batch-parity-expectation-v0.schema.json")
CPU_BATCH_ADAPTER_EXPANSION_SUMMARY_SCHEMA = Path("schemas/experiments/cpu-batch-adapter-expansion-summary-v0.schema.json")
CPU_BATCH_SCORING_COMPATIBILITY_SCHEMA = Path("schemas/experiments/cpu-batch-scoring-compatibility-v0.schema.json")
CPU_BATCH_SOLVED_FIXTURE_STREAM_SCHEMA = Path("schemas/experiments/cpu-batch-solved-fixture-stream-v0.schema.json")

SUPPORTED_REGISTRY_TRANSFORMS = {
    "direct_translation",
    "reverse_gematria",
    "rotated_reverse_gematria",
    "vigenere_explicit_key",
    "prime_minus_one_stream",
    "phi_prime_stream",
}
SUPPORTED_LOCAL_TRANSFORMS = {"caesar_shift", "affine_mod29"}
SUPPORTED_TRANSFORMS = SUPPORTED_REGISTRY_TRANSFORMS | SUPPORTED_LOCAL_TRANSFORMS


@dataclass(frozen=True)
class CpuBatchManifest:
    payload: dict[str, Any]
    path: Path
    manifest_sha256: str

    @property
    def manifest_id(self) -> str:
        return str(self.payload["manifest_id"])

    @property
    def input_streams(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self.payload.get("input_streams", [])]

    @property
    def transform_candidates(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self.payload.get("transform_candidates", [])]

    @property
    def scoring_enabled(self) -> bool:
        scoring = self.payload.get("scoring", {})
        return isinstance(scoring, dict) and scoring.get("enabled") is True


@dataclass(frozen=True)
class AdapterResult:
    status: str
    canonical_transform_id: str | None
    output_text: str | None
    output_text_hash: str | None
    output_token_hash: str
    transform_parameters: dict[str, Any]
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BatchRun:
    records: list[dict[str, Any]]
    summary: dict[str, Any]
    warnings: list[dict[str, Any]]
