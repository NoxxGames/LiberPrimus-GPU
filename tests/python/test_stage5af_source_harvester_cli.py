from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.source_harvester.cli import app
from libreprimus.source_harvester.policy import is_allowed_output_root

runner = CliRunner()


def test_stage5af_cli_builds_and_validates(tmp_path: Path) -> None:
    out = tmp_path / "out"
    dry = tmp_path / "dry.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"
    commands = [
        ["validate-manifest", "--manifest", "data/source-harvester/stage5af-cicada-source-manifest.yaml", "--out-dir", str(out)],
        [
            "plan",
            "--manifest",
            "data/source-harvester/stage5af-cicada-source-manifest.yaml",
            "--out",
            str(out / "harvest_plan.json"),
            "--dry-run-summary-out",
            str(dry),
            "--out-dir",
            str(out),
        ],
        [
            "build-bundles",
            "--bundle-plan",
            "data/source-harvester/stage5af-research-bundle-plan.yaml",
            "--out-root",
            str(out / "research_bundles_preview"),
        ],
        [
            "summarize",
            "--manifest",
            "data/source-harvester/stage5af-cicada-source-manifest.yaml",
            "--collection-priorities",
            "data/source-harvester/stage5af-source-collection-priorities.yaml",
            "--clue-target-categories",
            "data/source-harvester/stage5af-clue-target-categories.yaml",
            "--bundle-plan",
            "data/source-harvester/stage5af-research-bundle-plan.yaml",
            "--tool-policy",
            "data/source-harvester/stage5af-harvest-tool-policy.yaml",
            "--dry-run-summary",
            str(dry),
            "--next-stage-decision-out",
            str(decision),
            "--summary-out",
            str(summary),
            "--out",
            str(out / "summary.json"),
        ],
    ]
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output

    validate = runner.invoke(
        app,
        [
            "validate-stage5af",
            "--source-manifest",
            "data/source-harvester/stage5af-cicada-source-manifest.yaml",
            "--collection-priorities",
            "data/source-harvester/stage5af-source-collection-priorities.yaml",
            "--clue-target-categories",
            "data/source-harvester/stage5af-clue-target-categories.yaml",
            "--research-bundle-plan",
            "data/source-harvester/stage5af-research-bundle-plan.yaml",
            "--tool-policy",
            "data/source-harvester/stage5af-harvest-tool-policy.yaml",
            "--dry-run-summary",
            str(dry),
            "--next-stage-decision",
            str(decision),
            "--summary",
            str(summary),
            "--results-dir",
            str(out),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert runner.invoke(app, ["summary", "--summary", str(summary)]).exit_code == 0


def test_stage5af_cli_fetch_guards() -> None:
    no_network = runner.invoke(
        app,
        [
            "fetch",
            "--manifest",
            "data/source-harvester/stage5af-cicada-source-manifest.yaml",
            "--source-id",
            "fandom_main_wiki",
            "--out-root",
            "source-harvester-output/test",
        ],
    )
    assert no_network.exit_code != 0
    assert "allow-network" in no_network.output

    no_downloads = runner.invoke(
        app,
        [
            "fetch",
            "--manifest",
            "data/source-harvester/stage5af-cicada-source-manifest.yaml",
            "--source-id",
            "cicada_solvers_iddqd",
            "--out-root",
            "source-harvester-output/test",
            "--allow-network",
        ],
    )
    assert no_downloads.exit_code != 0
    assert "allow-downloads" in no_downloads.output

    committed_path = runner.invoke(
        app,
        [
            "fetch",
            "--manifest",
            "data/source-harvester/stage5af-cicada-source-manifest.yaml",
            "--source-id",
            "fandom_main_wiki",
            "--out-root",
            "data/source-harvester/raw-output",
            "--allow-network",
        ],
    )
    assert committed_path.exit_code != 0
    assert not is_allowed_output_root(Path("data/source-harvester/raw-output"))
