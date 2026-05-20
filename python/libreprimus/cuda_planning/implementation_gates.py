"""Build Stage 5A CUDA implementation gate records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_json, write_yaml
from libreprimus.cuda_planning.models import (
    CUDA_PLANNING_POLICY,
    IMPLEMENTATION_GATE_DEFINITIONS,
    IMPLEMENTATION_GATES_PATH,
    IMPLEMENTATION_GATES_REPORT,
    PARITY_SCAFFOLD_PATH,
    STAGE5A_OUTPUT_DIR,
)


def build_implementation_gates(
    *,
    out_dir: Path = STAGE5A_OUTPUT_DIR,
    parity_scaffold_path: Path = PARITY_SCAFFOLD_PATH,
    implementation_gates_out: Path = IMPLEMENTATION_GATES_PATH,
) -> list[dict[str, Any]]:
    scaffold_count = len(read_yaml(parity_scaffold_path).get("records", []))
    records: list[dict[str, Any]] = []
    for gate_id, status, criteria in IMPLEMENTATION_GATE_DEFINITIONS:
        records.append(
            {
                "record_type": "cuda_implementation_gate",
                "stage_id": "stage-5a",
                "gate_id": gate_id,
                "implementation_gate_status": status,
                "acceptance_criteria": criteria,
                "parity_scaffold_records_available": scaffold_count,
                "enforced_before": "any future CUDA kernel implementation or GPU benchmark",
                **CUDA_PLANNING_POLICY,
            }
        )
    write_yaml(implementation_gates_out, {"records": records})
    write_json(out_dir / IMPLEMENTATION_GATES_REPORT, {"records": records})
    return records
