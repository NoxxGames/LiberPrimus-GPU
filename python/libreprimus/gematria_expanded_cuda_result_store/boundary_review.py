"""Build Stage 5S boundary review records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_cuda_result_store.export import write_record_set, write_report
from libreprimus.gematria_expanded_cuda_result_store.models import (
    APPROVED_SCOPE,
    COMMON_FLAGS,
    BOUNDARY_REVIEW_PATH,
    BOUNDARY_REVIEW_REPORT_JSON,
    EXECUTED_SEMANTICS,
    OUTPUT_DIR,
)


def build_boundary_review(
    *,
    boundary_review_out: Path = BOUNDARY_REVIEW_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    record = {
        "record_type": "gematria_expanded_cuda_boundary_review_record",
        "boundary_review_id": "stage5s-boundary-review-00",
        "stage5r_exact_scope_confirmed": True,
        "exact_approved_scope": APPROVED_SCOPE,
        "executed_semantics": EXECUTED_SEMANTICS,
        "stage5r_exercised_only_gematria_shift_score": True,
        "stage5r_validated_original_direct_translation_semantics": False,
        "stage5r_authorized_additional_fixture_classes": False,
        "stage5r_authorized_unsolved_page_cuda": False,
        "stage5r_authorized_generated_body_publication": False,
        "stage5r_authorized_benchmarks": False,
        "consumed_controls_excluded": True,
        "blocked_original_family_fixtures_excluded": True,
        "original_transform_family_semantics_exercised": False,
    }
    record.update(COMMON_FLAGS)
    records = [record]
    write_record_set(boundary_review_out, records)
    write_report(out_dir, BOUNDARY_REVIEW_REPORT_JSON, {"records": records})
    return records
