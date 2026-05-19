"""Build and export Stage 4M image preflight records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.image_preflight.artifact_candidates import build_artifact_candidates
from libreprimus.image_preflight.bigram_readiness import build_bigram_readiness_record
from libreprimus.image_preflight.compression_metrics import build_compression_records
from libreprimus.image_preflight.loaders import (
    load_jsonl_records,
    load_yaml_records,
    write_json,
    write_jsonl,
    write_yaml_document,
    write_yaml_records,
)
from libreprimus.image_preflight.metadata import build_metadata_records
from libreprimus.image_preflight.models import (
    DEFAULT_ARTIFACT_CANDIDATES_OUT,
    DEFAULT_BIGRAM_IMAGE,
    DEFAULT_BIGRAM_READINESS_OUT,
    DEFAULT_COMPRESSION_OBSERVATIONS,
    DEFAULT_COMPRESSION_OUT,
    DEFAULT_IMAGE_ARTIFACTS,
    DEFAULT_IMAGE_DIR,
    DEFAULT_IMAGE_LOCKS,
    DEFAULT_MANIFEST_READINESS,
    DEFAULT_OUT_DIR,
    DEFAULT_PROMOTION_READINESS,
    DEFAULT_SOURCE_DELTA,
    DEFAULT_SOURCE_VARIANT_OUT,
    DEFAULT_SUMMARY_OUT,
)
from libreprimus.image_preflight.source_variant import build_source_variant_records
from libreprimus.image_preflight.summary import summarize_image_preflight
from libreprimus.paths import repo_root


def build_image_preflight(
    *,
    image_dir: Path = repo_root() / DEFAULT_IMAGE_DIR,
    image_artifacts: Path = repo_root() / DEFAULT_IMAGE_ARTIFACTS,
    image_locks: Path = repo_root() / DEFAULT_IMAGE_LOCKS,
    source_delta: Path = repo_root() / DEFAULT_SOURCE_DELTA,
    compression_observations: Path = repo_root() / DEFAULT_COMPRESSION_OBSERVATIONS,
    promotion_readiness: Path = repo_root() / DEFAULT_PROMOTION_READINESS,
    manifest_readiness: Path = repo_root() / DEFAULT_MANIFEST_READINESS,
    bigram_image: Path = repo_root() / DEFAULT_BIGRAM_IMAGE,
    out_dir: Path = repo_root() / DEFAULT_OUT_DIR,
    source_variant_out: Path = repo_root() / DEFAULT_SOURCE_VARIANT_OUT,
    compression_out: Path = repo_root() / DEFAULT_COMPRESSION_OUT,
    artifact_candidates_out: Path = repo_root() / DEFAULT_ARTIFACT_CANDIDATES_OUT,
    summary_out: Path = repo_root() / DEFAULT_SUMMARY_OUT,
    bigram_readiness_out: Path = repo_root() / DEFAULT_BIGRAM_READINESS_OUT,
    allow_missing_bigram_image: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Build committed Stage 4M records and ignored generated reports."""

    del allow_warnings
    root = repo_root()
    out_dir.mkdir(parents=True, exist_ok=True)
    metadata_records = build_metadata_records(image_dir, repo_root=root)
    image_lock_records = load_jsonl_records(image_locks)
    image_artifact_records = load_jsonl_records(image_artifacts)
    source_delta_records = load_yaml_records(source_delta)
    source_variant_records = build_source_variant_records(
        metadata_records,
        image_locks=image_lock_records,
        image_artifacts=image_artifact_records,
        source_delta_records=source_delta_records,
    )
    compression_records = build_compression_records(metadata_records, repo_root=root)
    artifact_candidate_records = build_artifact_candidates(load_yaml_records(compression_observations))
    bigram_readiness_record = build_bigram_readiness_record(
        manifest_readiness_records=load_yaml_records(manifest_readiness),
        promotion_readiness_records=load_yaml_records(promotion_readiness),
        bigram_image=bigram_image,
        repo_root=root,
        allow_missing_bigram_image=allow_missing_bigram_image,
    )
    summary = summarize_image_preflight(
        metadata_records=metadata_records,
        source_variant_records=source_variant_records,
        compression_records=compression_records,
        artifact_candidate_records=artifact_candidate_records,
        bigram_readiness_record=bigram_readiness_record,
    )

    write_yaml_records(
        source_variant_out,
        record_set_id="stage4m-image-source-variant-preflight-records",
        schema="schemas/visual/image-source-variant-preflight-record-v0.schema.json",
        records=source_variant_records,
    )
    write_yaml_records(
        compression_out,
        record_set_id="stage4m-image-compression-preflight-records",
        schema="schemas/visual/image-compression-preflight-record-v0.schema.json",
        records=compression_records,
    )
    write_yaml_records(
        artifact_candidates_out,
        record_set_id="stage4m-image-artifact-review-candidates",
        schema="schemas/visual/image-artifact-review-candidate-v0.schema.json",
        records=artifact_candidate_records,
    )
    write_yaml_document(summary_out, summary)
    write_yaml_document(bigram_readiness_out, bigram_readiness_record)

    write_jsonl(out_dir / "image_metadata.jsonl", metadata_records)
    write_jsonl(out_dir / "compression_metrics.jsonl", compression_records)
    write_jsonl(out_dir / "source_variant_preflight.jsonl", source_variant_records)
    write_jsonl(out_dir / "artifact_candidate_report.jsonl", artifact_candidate_records)
    write_json(out_dir / "summary.json", summary)
    (out_dir / "warnings.jsonl").write_text("", encoding="utf-8")
    return summary
