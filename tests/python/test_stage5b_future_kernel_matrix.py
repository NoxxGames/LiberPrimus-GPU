from __future__ import annotations

from libreprimus.cuda_parity.backend_capability import build_backend_capability
from libreprimus.cuda_parity.future_kernel_matrix import build_future_kernel_matrix
from libreprimus.cuda_parity.harness_plan import build_harness_plan
from libreprimus.cuda_parity.summary import build_summary


def test_stage5b_future_kernel_matrix_planned_and_blocked_only(tmp_path) -> None:
    harness_path = tmp_path / "harness.yaml"
    fixtures_path = tmp_path / "fixtures.yaml"
    backend_path = tmp_path / "backend.yaml"
    matrix_path = tmp_path / "matrix.yaml"
    summary_path = tmp_path / "summary.yaml"
    build_harness_plan(out_dir=tmp_path, harness_plan_out=harness_path, parity_fixtures_out=fixtures_path)
    build_backend_capability(out_dir=tmp_path, backend_capability_out=backend_path)
    matrix = build_future_kernel_matrix(
        harness_plan_path=harness_path,
        parity_fixtures_path=fixtures_path,
        out_dir=tmp_path,
        future_kernel_matrix_out=matrix_path,
    )
    summary = build_summary(
        harness_plan_path=harness_path,
        parity_fixtures_path=fixtures_path,
        backend_capability_path=backend_path,
        future_kernel_matrix_path=matrix_path,
        out_dir=tmp_path,
        summary_out=summary_path,
    )
    assert {record["future_kernel_status"] for record in matrix} == {"planned", "blocked"}
    assert all(record["cuda_kernel_added"] is False for record in matrix)
    assert summary["future_kernel_matrix_records"] == 9


def test_stage5b_future_kernel_matrix_blocks_missing_cpu_reference(tmp_path) -> None:
    harness_path = tmp_path / "harness.yaml"
    fixtures_path = tmp_path / "fixtures.yaml"
    matrix_path = tmp_path / "matrix.yaml"
    build_harness_plan(out_dir=tmp_path, harness_plan_out=harness_path, parity_fixtures_out=fixtures_path)
    matrix = build_future_kernel_matrix(
        harness_plan_path=harness_path,
        parity_fixtures_path=fixtures_path,
        out_dir=tmp_path,
        future_kernel_matrix_out=matrix_path,
    )
    blocked = [record for record in matrix if record["future_kernel_status"] == "blocked"]
    assert len(blocked) == 1
    assert blocked[0]["cpu_reference_present"] is False
