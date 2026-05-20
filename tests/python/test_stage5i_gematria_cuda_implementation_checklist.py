from __future__ import annotations

from libreprimus.gematria_cuda_prep.implementation_checklist import build_implementation_checklist_records


def test_stage5i_implementation_checklist_blocks_real_and_page_cuda(tmp_path) -> None:
    record = build_implementation_checklist_records(checklist_out=tmp_path / "checklist.yaml", out_dir=tmp_path)[0]
    assert record["real_liber_primus_cuda_data_blocked"] is True
    assert record["solved_fixture_cuda_execution_blocked"] is True
    assert record["unsolved_page_cuda_execution_blocked"] is True
    assert record["gpu_benchmark_blocked"] is True


def test_stage5i_stage5j_readiness_requires_no_blockers(tmp_path) -> None:
    record = build_implementation_checklist_records(checklist_out=tmp_path / "checklist.yaml", out_dir=tmp_path)[0]
    assert record["implementation_blockers"] == []
    assert record["stage5j_ready_for_synthetic_implementation"] is True
