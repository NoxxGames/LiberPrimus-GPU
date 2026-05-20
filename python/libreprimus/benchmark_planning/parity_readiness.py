"""Future CUDA parity benchmark readiness records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path, write_json, write_yaml
from libreprimus.benchmark_planning.models import CPU_ONLY_POLICY, READINESS_JSON, STAGE4Q_OUTPUT_DIR, STAGE4Q_READINESS_PATH
from libreprimus.benchmark_planning.source_loaders import (
    load_stage4o_adapter_records,
    load_stage4o_summary,
    load_stage4p_summary,
)

NON_CUDA_STATUSES = {"unsupported_by_design"}


def build_parity_readiness(
    *,
    out_dir: Path = STAGE4Q_OUTPUT_DIR,
    readiness_out: Path = STAGE4Q_READINESS_PATH,
) -> list[dict[str, Any]]:
    """Build Stage 4Q future CUDA parity benchmark gate records."""

    stage4o = load_stage4o_summary()
    stage4p = load_stage4p_summary()
    adapter_records, used_generated_coverage = load_stage4o_adapter_records()
    parity_available = int(stage4o.get("parity_expectations_written", 0)) > 0
    score_contract_available = int(stage4o.get("scoring_compatible_count", 0)) > 0
    unified_available = int(stage4p.get("records_with_parity_expectations", 0)) > 0

    records: list[dict[str, Any]] = []
    for adapter in sorted(adapter_records, key=lambda item: str(item.get("transform_family", ""))):
        status = str(adapter.get("adapter_status", "missing"))
        transform_family = str(adapter.get("transform_family") or adapter.get("transform_id") or "unknown")
        gate_status, benchmark_status, blockers = _gate_status(
            status=status,
            parity_available=parity_available,
            score_contract_available=score_contract_available,
            unified_available=unified_available,
        )
        records.append(
            {
                "record_type": "cuda_parity_benchmark_readiness",
                "readiness_id": f"stage4q-{transform_family}-cuda-parity-readiness",
                "stage_id": "stage-4q",
                "transform_id": str(adapter.get("transform_id", transform_family)),
                "canonical_transform_id": adapter.get("canonical_transform_id"),
                "transform_family": transform_family,
                "adapter_status": status,
                "benchmark_scope": "parity_readiness",
                "benchmark_status": benchmark_status,
                "parity_gate_status": gate_status,
                "blockers": blockers,
                "cpu_reference_present": status == "supported",
                "stage4o_parity_expectation_available": parity_available,
                "stage4p_unified_result_surface_available": unified_available,
                "stage4o_parity_reference_count": int(stage4o.get("parity_expectations_written", 0)),
                "stage4p_unified_result_reference_count": int(stage4p.get("records_with_parity_expectations", 0)),
                "score_contract_available": score_contract_available,
                "generated_adapter_coverage_used": used_generated_coverage,
                "future_cuda_may_begin": False,
                "required_before_cuda": [
                    "explicit Stage 5 scope",
                    "CPU benchmark plan acceptance",
                    "parity tests",
                    "non-target list",
                    "generated-output boundary check",
                ],
                **CPU_ONLY_POLICY,
            }
        )
    payload = {"records": records}
    write_json(resolve_repo_path(out_dir) / READINESS_JSON, payload)
    write_yaml(readiness_out, payload)
    return records


def _gate_status(
    *,
    status: str,
    parity_available: bool,
    score_contract_available: bool,
    unified_available: bool,
) -> tuple[str, str, list[str]]:
    if status in NON_CUDA_STATUSES:
        return "skipped_not_cuda_target", "skipped_optional", ["not_a_cuda_transform_target"]
    blockers: list[str] = []
    if status != "supported":
        blockers.append("missing_stable_cpu_batch_adapter")
        return "blocked_missing_cpu_reference", "blocked", blockers
    if not parity_available:
        blockers.append("missing_stage4o_parity_expectation")
        return "blocked_missing_parity_expectation", "blocked", blockers
    if not score_contract_available:
        blockers.append("missing_stage4i_score_contract")
        return "blocked_missing_score_contract", "blocked", blockers
    if not unified_available:
        blockers.append("missing_stage4p_unified_result_surface")
        return "blocked_missing_unified_result_surface", "blocked", blockers
    return "ready_for_future_cuda_planning", "planned", []
