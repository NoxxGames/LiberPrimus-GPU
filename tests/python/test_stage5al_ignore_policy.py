from __future__ import annotations

import subprocess

from libreprimus.paths import repo_root


def test_stage5al_generated_outputs_and_private_exports_are_ignored() -> None:
    paths = [
        "research-inputs/stage5al/deep_research_master_context.md",
        "experiments/results/website-ingest/stage5al/summary.json",
        "codex-output/stage5al-codex-completion.md",
    ]
    for path in paths:
        completed = subprocess.run(["git", "check-ignore", "-q", path], cwd=repo_root(), check=False)
        assert completed.returncode == 0, path


def test_stage5al_raw_and_private_guardrails_remain_false() -> None:
    summary = (repo_root() / "data/source-harvester/stage5al-summary.yaml").read_text(encoding="utf-8")
    for text in [
        "network_fetch_performed: false",
        "online_repo_clone_performed: false",
        "google_drive_storage_used: false",
        "generated_bundle_bodies_committed: false",
        "deep_research_performed: false",
        "cuda_execution_performed: false",
        "benchmark_performed: false",
        "solve_claim: false",
    ]:
        assert text in summary
