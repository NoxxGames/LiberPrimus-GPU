from __future__ import annotations

from pathlib import Path

from PIL import Image
from typer.testing import CliRunner

from libreprimus.source_harvester.cli import app


runner = CliRunner()


def _make_source_root(tmp_path: Path) -> Path:
    source_root = tmp_path / "UsefulFilesAndIdeas" / "community-facts"
    source_root.mkdir(parents=True)
    (source_root / "community-facts-collection.txt").write_text("community number fact\ncorrection note\n", encoding="utf-8")
    for index in range(1, 11):
        Image.new("RGB", (2, 2), "white").save(source_root / f"{index}.webp", format="PNG")
    return source_root


def test_stage5ak_cli_builds_and_validates_synthetic_pipeline(tmp_path: Path) -> None:
    source_root = _make_source_root(tmp_path)
    out = tmp_path / "results"
    bundle_root = tmp_path / "research-inputs" / "stage5ak"
    paths = {
        name: tmp_path / f"{name}.yaml"
        for name in (
            "inventory",
            "attachments",
            "cards",
            "content",
            "policy",
            "claims",
            "corrections",
            "categories",
            "arithmetic",
            "website",
            "deep",
            "readiness",
            "missing",
            "guardrail",
            "decision",
            "summary",
        )
    }
    commands = [
        ["inventory-community-facts", "--source-root", str(source_root), "--results-dir", str(out), "--out", str(paths["inventory"])],
        ["build-community-attachment-index", "--source-root", str(source_root), "--results-dir", str(out), "--out", str(paths["attachments"])],
        [
            "build-community-facts-source-cards",
            "--inventory",
            str(paths["inventory"]),
            "--attachment-index",
            str(paths["attachments"]),
            "--out-source-card-summary",
            str(paths["cards"]),
            "--out-content-index-summary",
            str(paths["content"]),
            "--results-dir",
            str(out),
        ],
        [
            "build-community-claim-records",
            "--source-root",
            str(source_root),
            "--attachment-index",
            str(paths["attachments"]),
            "--claim-policy-out",
            str(paths["policy"]),
            "--claim-records-out",
            str(paths["claims"]),
            "--correction-log-out",
            str(paths["corrections"]),
            "--clue-categories-out",
            str(paths["categories"]),
            "--results-dir",
            str(out),
        ],
        [
            "build-community-arithmetic-preflight",
            "--claim-records",
            str(paths["claims"]),
            "--correction-log",
            str(paths["corrections"]),
            "--out",
            str(paths["arithmetic"]),
            "--results-dir",
            str(out),
        ],
        [
            "update-community-deep-research-packs",
            "--stage5aj-bundle-root",
            str(tmp_path / "stage5aj"),
            "--source-card-summary",
            str(paths["cards"]),
            "--content-index-summary",
            str(paths["content"]),
            "--claim-records",
            str(paths["claims"]),
            "--correction-log",
            str(paths["corrections"]),
            "--bundle-root",
            str(bundle_root),
            "--results-dir",
            str(out),
            "--out-website-update",
            str(paths["website"]),
            "--out-deep-research-update",
            str(paths["deep"]),
            "--out-readiness",
            str(paths["readiness"]),
            "--out-missing-source-plan",
            str(paths["missing"]),
        ],
        ["build-stage5ak-guardrail", "--source-root", str(source_root), "--results-dir", str(out), "--out", str(paths["guardrail"])],
        [
            "build-stage5ak-next-stage-decision",
            "--readiness",
            str(paths["readiness"]),
            "--claim-records",
            str(paths["claims"]),
            "--missing-source-plan",
            str(paths["missing"]),
            "--out",
            str(paths["decision"]),
        ],
        [
            "build-stage5ak-summary",
            "--inventory",
            str(paths["inventory"]),
            "--source-card-summary",
            str(paths["cards"]),
            "--content-index-summary",
            str(paths["content"]),
            "--attachment-index",
            str(paths["attachments"]),
            "--clue-categories",
            str(paths["categories"]),
            "--claim-policy",
            str(paths["policy"]),
            "--claim-records",
            str(paths["claims"]),
            "--correction-log",
            str(paths["corrections"]),
            "--arithmetic-preflight",
            str(paths["arithmetic"]),
            "--website-update",
            str(paths["website"]),
            "--deep-research-update",
            str(paths["deep"]),
            "--readiness",
            str(paths["readiness"]),
            "--missing-source-plan",
            str(paths["missing"]),
            "--guardrail",
            str(paths["guardrail"]),
            "--next-stage-decision",
            str(paths["decision"]),
            "--out",
            str(paths["summary"]),
            "--results-dir",
            str(out),
        ],
    ]
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output

    validate = runner.invoke(
        app,
        [
            "validate-stage5ak",
            "--inventory",
            str(paths["inventory"]),
            "--attachment-index",
            str(paths["attachments"]),
            "--source-card-summary",
            str(paths["cards"]),
            "--content-index-summary",
            str(paths["content"]),
            "--clue-categories",
            str(paths["categories"]),
            "--claim-policy",
            str(paths["policy"]),
            "--claim-records",
            str(paths["claims"]),
            "--correction-log",
            str(paths["corrections"]),
            "--arithmetic-preflight",
            str(paths["arithmetic"]),
            "--website-update",
            str(paths["website"]),
            "--deep-research-update",
            str(paths["deep"]),
            "--readiness",
            str(paths["readiness"]),
            "--missing-source-plan",
            str(paths["missing"]),
            "--guardrail",
            str(paths["guardrail"]),
            "--next-stage-decision",
            str(paths["decision"]),
            "--summary",
            str(paths["summary"]),
            "--results-dir",
            str(out),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "source_harvester_stage5ak_valid=true" in validate.output
