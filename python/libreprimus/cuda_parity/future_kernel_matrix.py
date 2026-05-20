"""Future CUDA kernel parity matrix for Stage 5B."""

from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_parity.export import write_record_set, write_report
from libreprimus.cuda_parity.loaders import load_records
from libreprimus.cuda_parity.models import (
    CUDA_PARITY_POLICY,
    FUTURE_KERNEL_DEFINITIONS,
    FUTURE_KERNEL_MATRIX_PATH,
    MATRIX_REPORT,
    STAGE5B_OUTPUT_DIR,
)


def build_future_kernel_matrix(
    *,
    harness_plan_path: Path,
    parity_fixtures_path: Path,
    out_dir: Path = STAGE5B_OUTPUT_DIR,
    future_kernel_matrix_out: Path = FUTURE_KERNEL_MATRIX_PATH,
) -> list[dict[str, object]]:
    harness_records = load_records(harness_plan_path)
    fixture_records = load_records(parity_fixtures_path)
    ready_families = {str(record.get("transform_family")) for record in harness_records if record.get("harness_status") == "ready_for_future_kernel"}
    ready_fixture_count = sum(1 for record in fixture_records if record.get("fixture_status") == "ready_for_future_kernel")
    records = [
        _matrix_record(kernel_id, family, status, ready_families, ready_fixture_count)
        for kernel_id, family, status in FUTURE_KERNEL_DEFINITIONS
    ]
    write_record_set(future_kernel_matrix_out, records)
    write_report(out_dir, MATRIX_REPORT, {"records": records})
    return records


def _matrix_record(
    kernel_id: str,
    family: str,
    status: str,
    ready_families: set[str],
    ready_fixture_count: int,
) -> dict[str, object]:
    family_ready = family in ready_families or family in {"scoring_crib_checks", "scoring_ngram_proxy", "topk_result_ordering", "cpu_batch_dispatch"}
    kernel_status = "planned" if status == "planned" and family_ready else "blocked"
    fixture_count = ready_fixture_count if family in {"scoring_crib_checks", "scoring_ngram_proxy", "topk_result_ordering", "cpu_batch_dispatch"} else int(family in ready_families)
    return {
        "record_type": "cuda_future_kernel_parity_matrix_record",
        "stage_id": "stage-5b",
        "kernel_id": kernel_id,
        "future_kernel_status": kernel_status,
        "cpu_reference_family": family,
        "cpu_reference_required": True,
        "cpu_reference_present": family_ready,
        "required_fixture_count": fixture_count,
        "required_positive_controls": 1 if family_ready else 0,
        "required_null_controls": 1 if family_ready else 0,
        "required_negative_controls": 1 if family_ready else 0,
        "compatibility_8gb_planning_note": "Keep memory layout valid for the compatibility 8 GB planning profile.",
        "local_16gb_profile_planning_note": "Local RTX 4060 Ti 16 GB can be used in future explicit benchmark stages, but is not required.",
        "vram_profile": "compatibility_8gb" if family_ready else "not_applicable",
        "local_16gb_profile_required": False,
        "no_fast_math_default": True,
        "no_performance_claim": True,
        "notes": ["Stage 5B records the future parity contract only; no CUDA kernel is implemented."],
        **CUDA_PARITY_POLICY,
    }
