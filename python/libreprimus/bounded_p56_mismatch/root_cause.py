"""Root-cause records for Stage 5AD-fix."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json_report, write_records
from .models import OUTPUT_DIR, REPORT_FILES, ROOT_CAUSE_PATH, base_record


def build_root_cause(*, root_cause_out: Path = ROOT_CAUSE_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    records = [
        _cause(
            "stage5ad-fix-root-cause-reference-lineage-v0",
            "expected_hash_reference_lineage_mismatch",
            True,
            "high",
            "Stage 5AD compared a formula-output CUDA hash against a Stage 5L candidate-major reference hash.",
            cuda_kernel_repair_required=False,
            reference_contract_repair_required=True,
            hash_material_policy_repair_required=True,
        ),
        _cause(
            "stage5ad-fix-root-cause-cuda-kernel-v0",
            "cuda_kernel_bug_not_supported_by_current_evidence",
            False,
            "medium",
            "The CUDA/formula hash equals the Stage 5X formula hash; no device arithmetic defect is evidenced.",
            cuda_kernel_repair_required=False,
            reference_contract_repair_required=False,
            hash_material_policy_repair_required=False,
        ),
        _cause(
            "stage5ad-fix-root-cause-hash-material-policy-v0",
            "hash_material_policy_ambiguous_between_formula_and_candidate_major",
            False,
            "high",
            "Future reporting must name whether formula-output or Stage 5L candidate-major material is authoritative.",
            cuda_kernel_repair_required=False,
            reference_contract_repair_required=True,
            hash_material_policy_repair_required=True,
        ),
        _cause(
            "stage5ad-fix-root-cause-stage5ad-preservation-v0",
            "stage5ad_historical_failure_preserved",
            False,
            "high",
            "Stage 5AD remains a failed parity record and must not be overwritten as passed.",
            cuda_kernel_repair_required=False,
            reference_contract_repair_required=False,
            hash_material_policy_repair_required=False,
        ),
    ]
    write_records(root_cause_out, records)
    write_json_report(out_dir, REPORT_FILES["root_cause"], {"records": records})
    return records


def _cause(
    record_id: str,
    cause_id: str,
    primary: bool,
    confidence: str,
    rationale: str,
    *,
    cuda_kernel_repair_required: bool,
    reference_contract_repair_required: bool,
    hash_material_policy_repair_required: bool,
) -> dict[str, Any]:
    return base_record(
        "bounded_p56_mismatch_root_cause_record",
        "schemas/cuda/bounded-p56-mismatch-root-cause-record-v0.schema.json",
        root_cause_record_id=record_id,
        cause_id=cause_id,
        primary_root_cause=primary,
        confidence=confidence,
        rationale=rationale,
        cuda_kernel_repair_required=cuda_kernel_repair_required,
        reference_contract_repair_required=reference_contract_repair_required,
        hash_material_policy_repair_required=hash_material_policy_repair_required,
        root_cause_status="selected" if primary else "supporting",
    )
