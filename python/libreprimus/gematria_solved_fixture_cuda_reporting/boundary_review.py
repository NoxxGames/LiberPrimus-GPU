"""Build Stage 5N boundary review records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml
from libreprimus.gematria_solved_fixture_cuda_reporting.export import common_policy_fields, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda_reporting.models import (
    BOUNDARY_REVIEW_JSON,
    BOUNDARY_REVIEW_PATH,
    EXECUTED_SEMANTICS,
    OUTPUT_DIR,
    STAGE5M_SUMMARY,
)


def build_boundary_review(
    *,
    stage5m_summary: Path = STAGE5M_SUMMARY,
    boundary_review_out: Path = BOUNDARY_REVIEW_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    stage5m = read_yaml(stage5m_summary)
    record: dict[str, Any] = {
        "record_type": "gematria_cuda_boundary_review_record",
        "boundary_review_id": "stage5n-boundary-review-00",
        "source_stage_id": "stage-5m",
        "stage5m_scope_exact_stage5l_mapped_token_buffers_only": (
            stage5m.get("solved_fixture_cuda_execution_scope") == "exact_stage5l_mapped_token_buffers_only"
        ),
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "device_kernel_arithmetic_modified": False,
        "host_runner_only_source_modification": (
            stage5m.get("cuda_source_modification_scope") == "stage5m_host_runner_only_no_device_arithmetic_change"
        ),
        "stage5m_executed_semantics": EXECUTED_SEMANTICS,
        "non_shift_original_transform_family_semantics_validated": False,
        "additional_fixture_classes_authorized": False,
        "unsolved_page_cuda_authorized": False,
        "boundary_status": "exact_stage5m_scope_only",
        "notes": [
            "Stage 5M exercises only gematria_shift_score_only.",
            "Stage 5M does not validate reverse, rotated-reverse, Vigenere, or prime-stream CUDA semantics.",
            "Stage 5M does not authorize additional fixture classes without a later gate.",
            "Stage 5M does not authorize unsolved-page CUDA.",
        ],
        **common_policy_fields(),
    }
    records = [record]
    write_record_set(boundary_review_out, records)
    write_report(out_dir, BOUNDARY_REVIEW_JSON, {"records": records})
    return records
