from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ai_guardrail_blocks_execution_and_publication_work() -> None:
    payload = yaml.safe_load(Path("data/source-harvester/stage5ai-curated-extraction-guardrail.yaml").read_text(encoding="utf-8"))
    for key in (
        "network_fetch_performed",
        "online_repo_clone_performed",
        "google_drive_storage_used",
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "stego_tool_execution_performed",
        "image_forensics_performed",
        "audio_analysis_performed",
        "hypothesis_generation_performed",
        "hypothesis_execution_performed",
        "cuda_execution_performed",
        "cuda_source_modified",
        "gpu_benchmark_performed",
        "scored_experiment_executed",
        "website_expansion_performed",
        "solve_claim",
    ):
        assert payload[key] is False
    assert payload["new_cuda_kernels_added"] == 0
