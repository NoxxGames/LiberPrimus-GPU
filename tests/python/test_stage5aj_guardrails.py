from __future__ import annotations

from pathlib import Path

from libreprimus.source_harvester.stage5aj_records import build_stage5aj_guardrail


def test_stage5aj_guardrail_keeps_execution_false(tmp_path: Path) -> None:
    source_root = tmp_path / "UsefulFilesAndIdeas"
    source_root.mkdir()
    guardrail = build_stage5aj_guardrail(
        source_root=source_root,
        results_dir=tmp_path / "results",
        out=tmp_path / "guardrail.yaml",
    )

    for key in (
        "network_fetch_performed",
        "online_repo_clone_performed",
        "google_drive_storage_used",
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "image_forensics_performed",
        "hypothesis_execution_performed",
        "website_expansion_performed",
        "cuda_execution_performed",
        "cuda_source_modified",
        "benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
    ):
        assert guardrail[key] is False
    assert guardrail["new_cuda_kernels_added"] == 0
