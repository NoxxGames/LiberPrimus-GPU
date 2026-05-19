"""Summary helpers for Stage 4M image preflight."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.image_preflight.loaders import load_yaml_records
from libreprimus.image_preflight.models import COMMON_FALSE_FLAGS


def summarize_image_preflight(
    *,
    metadata_records: list[dict[str, Any]],
    source_variant_records: list[dict[str, Any]],
    compression_records: list[dict[str, Any]],
    artifact_candidate_records: list[dict[str, Any]],
    bigram_readiness_record: dict[str, Any],
) -> dict[str, Any]:
    """Build the committed Stage 4M summary document."""

    jpeg_flag_count = sum(1 for record in compression_records if record.get("jpeg_like_metric_flag") is True)
    blocked_variant_count = sum(
        1
        for record in source_variant_records
        if record.get("source_variant_status") == "blocked_external_variant_not_cached"
    )
    return {
        "record_type": "image_preflight_summary",
        "stage": "stage4m",
        "image_count": len(metadata_records),
        "source_variant_record_count": len(source_variant_records),
        "compression_record_count": len(compression_records),
        "artifact_candidate_count": len(artifact_candidate_records),
        "jpeg_like_metric_flag_count": jpeg_flag_count,
        "source_variants_blocked_external_cache_count": blocked_variant_count,
        "bigram_readiness_records": 1 if bigram_readiness_record else 0,
        "bigram_image_present": bool(bigram_readiness_record.get("bigram_image_present")),
        "bigram_readiness_blocked": bigram_readiness_record.get("ready_state") == "blocked",
        "compression_metric_status_counts": _count_values(compression_records, "compression_metric_status"),
        "source_variant_status_counts": _count_values(source_variant_records, "source_variant_status"),
        "notes": (
            "Image metrics are deterministic preflight metadata only. Stage 4M does not infer hidden content, "
            "intentionality, canonical source status, or page boundaries."
        ),
        **COMMON_FALSE_FLAGS,
    }


def load_summary(path: Path) -> dict[str, Any]:
    """Load a committed Stage 4M summary document."""

    records = load_yaml_records(path)
    return records[0] if records else {}


def _count_values(records: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = str(record.get(key))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))
