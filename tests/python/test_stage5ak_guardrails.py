from __future__ import annotations

from pathlib import Path

from libreprimus.source_harvester.stage5ak_records import build_stage5ak_guardrail


def test_stage5ak_guardrail_preserves_non_execution_boundary(tmp_path: Path) -> None:
    source_root = tmp_path / "community-facts"
    source_root.mkdir()
    result = build_stage5ak_guardrail(
        source_root=source_root,
        results_dir=tmp_path / "results",
        out=tmp_path / "guardrail.yaml",
    )

    forbidden_flags = [
        "network_fetch_performed",
        "live_web_scrape_performed",
        "online_repo_clone_performed",
        "google_drive_storage_used",
        "deep_research_performed",
        "website_expansion_performed",
        "hypothesis_execution_performed",
        "cuda_execution_performed",
        "cuda_source_modified",
        "benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
    ]
    assert all(result[flag] is False for flag in forbidden_flags)
    assert result["new_cuda_kernels_added"] == 0
    assert result["no_solve_claim"] is True
