from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_planning.implementation_gates import build_implementation_gates


def test_stage5a_implementation_gates_are_planning_only(tmp_path: Path) -> None:
    gates = build_implementation_gates(out_dir=tmp_path, implementation_gates_out=tmp_path / "gates.yaml")

    assert len(gates) == 10
    assert all(record["implementation_gate_status"] == "satisfied" for record in gates)
    assert any(record["gate_id"] == "no_speedup_claim_before_parity" for record in gates)
    assert all(record["cuda_implementation_added"] is False for record in gates)
    assert all(record["gpu_benchmark_performed"] is False for record in gates)
