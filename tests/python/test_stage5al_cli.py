from __future__ import annotations

import json
import subprocess
from pathlib import Path

from libreprimus.paths import repo_root


def _prepare_results(tmp_path: Path) -> Path:
    for name in [
        "source_inventory.json",
        "research_index.json",
        "website_package_manifest.json",
        "publication_gates.json",
        "deep_research_export.json",
        "summary.json",
    ]:
        (tmp_path / name).write_text(json.dumps({"stage_id": "stage-5al", "solve_claim": False}) + "\n", encoding="utf-8")
    (tmp_path / "warnings.jsonl").write_text("", encoding="utf-8")
    return tmp_path


def test_stage5al_cli_validate_works_with_committed_package(tmp_path: Path) -> None:
    results = _prepare_results(tmp_path)
    command = [
        str(repo_root() / ".venv/Scripts/python.exe"),
        "-m",
        "libreprimus.cli",
        "source-harvester",
        "validate-stage5al",
        "--website-ingest-summary",
        "data/source-harvester/stage5al-website-ingest-staging-summary.yaml",
        "--website-data-contract",
        "data/source-harvester/stage5al-website-data-contract.yaml",
        "--deep-research-export",
        "data/source-harvester/stage5al-deep-research-export.yaml",
        "--deep-research-export-summary",
        "data/source-harvester/stage5al-deep-research-export-summary.yaml",
        "--publication-gate-policy",
        "data/source-harvester/stage5al-publication-gate-policy.yaml",
        "--research-index-validation",
        "data/source-harvester/stage5al-research-index-validation.yaml",
        "--guardrail",
        "data/source-harvester/stage5al-guardrail.yaml",
        "--next-stage-decision",
        "data/source-harvester/stage5al-next-stage-decision.yaml",
        "--summary",
        "data/source-harvester/stage5al-summary.yaml",
        "--website-ingest-dir",
        "data/website-ingest/stage5al",
        "--results-dir",
        str(results),
    ]
    completed = subprocess.run(command, cwd=repo_root(), check=True, capture_output=True, text=True)
    assert "source_harvester_stage5al_valid=true" in completed.stdout
