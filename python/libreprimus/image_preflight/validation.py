"""Validation for committed Stage 4M image preflight records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.image_preflight.loaders import load_yaml_records
from libreprimus.image_preflight.models import BIGRAM_BLOCKERS


def validate_image_preflight_records(
    *,
    source_variant: Path,
    compression: Path,
    artifact_candidates: Path,
    summary: Path,
    bigram_readiness: Path,
) -> tuple[dict[str, int], list[str]]:
    """Validate Stage 4M committed preflight records."""

    source_variant_records = load_yaml_records(source_variant)
    compression_records = load_yaml_records(compression)
    artifact_records = load_yaml_records(artifact_candidates)
    summary_records = load_yaml_records(summary)
    bigram_records = load_yaml_records(bigram_readiness)
    errors: list[str] = []
    counts = {
        "source_variant_records": len(source_variant_records),
        "compression_records": len(compression_records),
        "artifact_candidate_records": len(artifact_records),
        "summary_records": len(summary_records),
        "bigram_readiness_records": len(bigram_records),
    }
    if not source_variant_records:
        errors.append("source_variant_records_missing")
    if not compression_records:
        errors.append("compression_records_missing")
    if len(source_variant_records) != len(compression_records):
        errors.append("source_variant_compression_count_mismatch")
    if not artifact_records:
        errors.append("artifact_candidate_records_missing")
    if len(summary_records) != 1:
        errors.append("summary_missing")
    if len(bigram_records) != 1:
        errors.append("bigram_readiness_missing")
    for record in source_variant_records:
        _validate_common_false_flags(record, errors)
        if not record.get("source_variant_status"):
            errors.append(f"source_variant_status_missing:{record.get('preflight_record_id')}")
    for record in compression_records:
        _validate_common_false_flags(record, errors)
        if record.get("metric_only") is not True:
            errors.append(f"compression_metric_only_not_true:{record.get('compression_record_id')}")
        if not record.get("compression_metric_status"):
            errors.append(f"compression_metric_status_missing:{record.get('compression_record_id')}")
    for record in artifact_records:
        _validate_common_false_flags(record, errors)
        if record.get("usable_as_experiment_seed") is not False:
            errors.append(f"artifact_seed_ready:{record.get('candidate_id')}")
        if not record.get("review_state"):
            errors.append(f"artifact_review_state_missing:{record.get('candidate_id')}")
    if summary_records:
        summary_record = summary_records[0]
        _validate_common_false_flags(summary_record, errors)
        if int(summary_record.get("source_variant_record_count") or -1) != len(source_variant_records):
            errors.append("summary_source_variant_count_mismatch")
        if int(summary_record.get("compression_record_count") or -1) != len(compression_records):
            errors.append("summary_compression_count_mismatch")
    if bigram_records:
        _validate_bigram_record(bigram_records[0], errors)
    return counts, errors


def _validate_common_false_flags(record: dict[str, Any], errors: list[str]) -> None:
    label = str(
        record.get("preflight_record_id")
        or record.get("compression_record_id")
        or record.get("candidate_id")
        or record.get("readiness_id")
        or record.get("record_type")
    )
    for key in (
        "raw_image_committed",
        "generated_image_committed",
        "solve_claim",
        "trusted_as_canonical",
        "usable_as_experiment_seed",
        "image_interpretation_claim",
    ):
        if key in record and record.get(key) is not False:
            errors.append(f"{key}_not_false:{label}")


def _validate_bigram_record(record: dict[str, Any], errors: list[str]) -> None:
    label = str(record.get("readiness_id") or "bigram")
    if record.get("ready_state") != "blocked":
        errors.append(f"bigram_not_blocked:{label}")
    blockers = set(record.get("blockers") or [])
    for blocker in BIGRAM_BLOCKERS:
        if blocker not in blockers:
            errors.append(f"bigram_blocker_missing:{blocker}")
    for key in ("matrix_regenerated", "raw_transcripts_read", "frequency_pattern_experiment_executed"):
        if record.get(key) is not False:
            errors.append(f"bigram_{key}_not_false:{label}")
    for key in ("execution_enabled", "solve_claim", "trusted_as_canonical", "usable_as_experiment_seed", "cuda_enabled"):
        if record.get(key) is not False:
            errors.append(f"bigram_{key}_not_false:{label}")
    if record.get("no_solve_claim") is not True:
        errors.append(f"bigram_no_solve_claim_not_true:{label}")
