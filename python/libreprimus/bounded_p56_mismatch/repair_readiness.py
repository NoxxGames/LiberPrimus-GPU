"""Repair-readiness records for Stage 5AD-fix."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json_report, write_records
from .models import OUTPUT_DIR, REPAIR_READINESS_PATH, REPORT_FILES, base_record


def build_repair_readiness(
    *, repair_readiness_out: Path = REPAIR_READINESS_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    records = [
        _record(
            "stage5ad-fix-repair-readiness-reference-contract-v0",
            "reference_contract_repair",
            "ready_for_stage5ae",
            True,
            "Clarify expected hash material and keep Stage 5AD failure preserved.",
        ),
        _record(
            "stage5ad-fix-repair-readiness-hash-material-policy-v0",
            "hash_material_policy_repair",
            "ready_for_stage5ae",
            True,
            "Require distinct formula-output and candidate-major reference hash roles.",
        ),
        _record(
            "stage5ad-fix-repair-readiness-cuda-kernel-v0",
            "cuda_kernel_repair",
            "not_required_by_current_evidence",
            False,
            "No Stage 5AD-fix evidence supports modifying CUDA device arithmetic.",
        ),
    ]
    write_records(repair_readiness_out, records)
    write_json_report(out_dir, REPORT_FILES["repair_readiness"], {"records": records})
    return records


def _record(record_id: str, repair_id: str, readiness_status: str, required: bool, rationale: str) -> dict[str, Any]:
    return base_record(
        "bounded_p56_mismatch_repair_readiness_record",
        "schemas/cuda/bounded-p56-mismatch-repair-readiness-record-v0.schema.json",
        repair_readiness_record_id=record_id,
        repair_id=repair_id,
        repair_required=required,
        readiness_status=readiness_status,
        rationale=rationale,
        execution_enabled=False,
        blockers=[] if required else ["cuda_kernel_repair_not_supported_by_current_evidence"],
    )
