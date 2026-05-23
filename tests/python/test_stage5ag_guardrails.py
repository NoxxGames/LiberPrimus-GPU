from __future__ import annotations

from pathlib import Path

from libreprimus.source_harvester.stage5ag_records import build_stage5ag_guardrail


def test_stage5ag_guardrail_reports_no_network_google_drive_cuda_or_solve() -> None:
    guardrail = build_stage5ag_guardrail(
        source_root=Path("third_party/__stage5ag_missing_guardrail__"),
        results_dir=Path("experiments/results/source-harvester-local/stage5ag-test"),
        out=Path("experiments/results/source-harvester-local/stage5ag-test/guardrail.yaml"),
    )
    assert guardrail["network_fetch_performed"] is False
    assert guardrail["online_repo_clone_performed"] is False
    assert guardrail["google_drive_storage_used"] is False
    assert guardrail["raw_data_committed"] is False
    assert guardrail["cuda_execution_performed"] is False
    assert guardrail["cuda_source_modified"] is False
    assert guardrail["new_cuda_kernels_added"] == 0
    assert guardrail["gpu_benchmark_performed"] is False
    assert guardrail["scored_experiment_executed"] is False
    assert guardrail["solve_claim"] is False
