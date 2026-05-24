from __future__ import annotations

import yaml

from libreprimus.paths import repo_root


def test_deep_research_export_is_ready_and_private() -> None:
    export = yaml.safe_load((repo_root() / "data/source-harvester/stage5al-deep-research-export.yaml").read_text(encoding="utf-8"))
    summary = yaml.safe_load((repo_root() / "data/source-harvester/stage5al-deep-research-export-summary.yaml").read_text(encoding="utf-8"))
    assert export["deep_research_export_ready"] is True
    assert export["private_deep_research_allowed"] is True
    assert export["website_publication_allowed"] is False
    assert summary["bundle_count"] == 10
    assert summary["claim_record_count"] == 12
    assert summary["private_generated_body_status"] == "ignored_not_committed"


def test_deep_research_export_keeps_execution_guardrails_false() -> None:
    export = yaml.safe_load((repo_root() / "data/source-harvester/stage5al-deep-research-export.yaml").read_text(encoding="utf-8"))
    for key in [
        "network_fetch_performed",
        "online_repo_clone_performed",
        "google_drive_storage_used",
        "deep_research_performed",
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "stego_tool_execution_performed",
        "cuda_execution_performed",
        "benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
    ]:
        assert export[key] is False
