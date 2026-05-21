"""Build Stage 5P method-status impact records."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.gematria_cuda_result_store.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_cuda_result_store.models import (
    COMMON_POLICY_FLAGS,
    METHOD_STATUS_IMPACT_PATH,
    METHOD_STATUS_IMPACT_REPORT,
    OUTPUT_DIR,
    RESULT_STORE_INTEGRATION_PATH,
)


def build_method_status_impact(
    *,
    result_store_integration: Path = RESULT_STORE_INTEGRATION_PATH,
    method_status_impact_out: Path = METHOD_STATUS_IMPACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Record that Stage 5P does not upgrade any method to solved."""

    integrations = read_record_set(result_store_integration)
    transform_counts = Counter(str(record["source_transform_family"]) for record in integrations)
    records: list[dict[str, Any]] = [
        {
            "record_type": "gematria_cuda_method_status_impact_record",
            "method_status_impact_id": "stage5p-method-impact-shift-score-kernel",
            "method_family": "gematria_mod29_shift_score_kernel",
            "related_transform_family": "caesar_mod29",
            "input_record_count": len(integrations),
            "impact_status": "parity_verified_infrastructure_only",
            "pre_stage_status": "infrastructure",
            "post_stage_status": "infrastructure",
            "impact_reason": "Repeat parity validates the Stage 5M shift-score kernel path for fixed mapped tokens only.",
            "original_transform_family_semantics_exercised": False,
            **COMMON_POLICY_FLAGS,
        }
    ]
    for transform_family in sorted(transform_counts):
        records.append(
            {
                "record_type": "gematria_cuda_method_status_impact_record",
                "method_status_impact_id": f"stage5p-method-impact-{transform_family.replace('_', '-')}",
                "method_family": transform_family,
                "related_transform_family": transform_family,
                "input_record_count": transform_counts[transform_family],
                "impact_status": "not_upgraded_original_semantics_not_exercised",
                "pre_stage_status": "unchanged",
                "post_stage_status": "unchanged",
                "impact_reason": (
                    "Stage 5P records that the source transform family supplied solved-fixture mappings; "
                    "it does not prove a CUDA implementation of the original transform semantics."
                ),
                "original_transform_family_semantics_exercised": False,
                **COMMON_POLICY_FLAGS,
            }
        )
    records.append(
        {
            "record_type": "gematria_cuda_method_status_impact_record",
            "method_status_impact_id": "stage5p-method-impact-unsolved-cuda",
            "method_family": "unsolved_page_cuda",
            "related_transform_family": "none",
            "input_record_count": 0,
            "impact_status": "blocked_not_activated",
            "pre_stage_status": "deferred",
            "post_stage_status": "deferred",
            "impact_reason": "Unsolved-page CUDA remains outside Stage 5P scope.",
            "original_transform_family_semantics_exercised": False,
            **COMMON_POLICY_FLAGS,
        }
    )
    write_record_set(method_status_impact_out, records)
    write_report(out_dir, METHOD_STATUS_IMPACT_REPORT, {"records": records})
    return records
