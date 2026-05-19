"""Stage 4M readiness tracking for the bigram/Fibonacci-421 observation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.image_preflight.metadata import sha256_file
from libreprimus.image_preflight.models import (
    BIGRAM_BLOCKERS,
    BIGRAM_FUTURE_MANIFEST_ID,
    EXPECTED_BIGRAM_IMAGE_SHA256,
)


def build_bigram_readiness_record(
    *,
    manifest_readiness_records: list[dict[str, Any]],
    promotion_readiness_records: list[dict[str, Any]],
    bigram_image: Path,
    repo_root: Path,
    allow_missing_bigram_image: bool,
) -> dict[str, Any]:
    """Carry Stage 4L bigram readiness forward without running a matrix audit."""

    stage4l_manifest = next(
        (
            record
            for record in manifest_readiness_records
            if record.get("future_manifest_id") == BIGRAM_FUTURE_MANIFEST_ID
        ),
        None,
    )
    promotion_record = next(
        (
            record
            for record in promotion_readiness_records
            if record.get("observation_id") == "stage4l-bigram-diagonal-fibonacci-421-claim"
        ),
        None,
    )
    image_present = bigram_image.is_file()
    if not image_present and not allow_missing_bigram_image:
        raise FileNotFoundError(f"bigram image missing: {bigram_image}")
    image_sha256 = sha256_file(bigram_image) if image_present else None
    return {
        "record_type": "bigram_frequency_pattern_readiness",
        "readiness_id": "stage4m-bigram-diagonal-fibonacci-421-readiness",
        "future_manifest_id": BIGRAM_FUTURE_MANIFEST_ID,
        "stage4l_manifest_readiness_id": stage4l_manifest.get("manifest_readiness_id") if stage4l_manifest else None,
        "stage4l_ready_state": stage4l_manifest.get("ready_state") if stage4l_manifest else None,
        "stage4l_observation_readiness_id": promotion_record.get("readiness_record_id") if promotion_record else None,
        "observation_id": "stage4l-bigram-diagonal-fibonacci-421-claim",
        "observation_type": "numeric_frequency_pattern_claim",
        "ready_state": "blocked",
        "blockers": list(BIGRAM_BLOCKERS),
        "matrix_regenerated": False,
        "raw_transcripts_read": False,
        "frequency_pattern_experiment_executed": False,
        "synthetic_fixture_only": False,
        "bigram_image_present": image_present,
        "bigram_image_relative_path": _display_path(bigram_image, repo_root) if image_present else None,
        "bigram_image_sha256": image_sha256,
        "bigram_image_sha256_matches_stage4l": image_sha256 == EXPECTED_BIGRAM_IMAGE_SHA256 if image_sha256 else False,
        "bigram_image_byte_length": bigram_image.stat().st_size if image_present else None,
        "execution_enabled": False,
        "solve_claim": False,
        "no_solve_claim": True,
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "cuda_enabled": False,
        "cuda_used": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "notes": (
            "Stage 4M records readiness only. Matrix regeneration, transcript/profile selection, null controls, "
            "and multiple-testing controls are required before any bounded audit."
        ),
    }


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()
