from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.source_harvester.cli import app


runner = CliRunner()


def test_stage5ai_cli_pipeline_builds_and_validates_tmp_bundle(tmp_path: Path) -> None:
    out = tmp_path / "results"
    bundle_root = tmp_path / "research-inputs" / "stage5ai"
    classification = tmp_path / "classification.yaml"
    source_cards = tmp_path / "source-cards.yaml"
    policy = tmp_path / "policy.yaml"
    bundle_summary = tmp_path / "bundle-summary.yaml"
    content = tmp_path / "content.yaml"
    website = tmp_path / "website.yaml"
    deep = tmp_path / "deep.yaml"
    missing = tmp_path / "missing.yaml"
    guardrail = tmp_path / "guardrail.yaml"
    readiness = tmp_path / "readiness.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"

    commands = [
        ["classify-local-sources", "--out", str(classification), "--results-dir", str(out)],
        ["build-source-cards", "--classification", str(classification), "--bundle-root", str(bundle_root), "--results-dir", str(out), "--out", str(source_cards)],
        ["build-curated-bundles", "--classification", str(classification), "--bundle-root", str(bundle_root), "--results-dir", str(out), "--out-policy", str(policy), "--out-summary", str(bundle_summary)],
        ["build-content-index", "--bundle-root", str(bundle_root), "--results-dir", str(out), "--out", str(content)],
        ["build-website-ingest-index", "--bundle-root", str(bundle_root), "--results-dir", str(out), "--out", str(website)],
        ["build-deep-research-pack-index", "--bundle-root", str(bundle_root), "--results-dir", str(out), "--out", str(deep)],
        ["build-missing-source-plan", "--out", str(missing), "--results-dir", str(out)],
        ["build-stage5ai-guardrail", "--bundle-root", str(bundle_root), "--results-dir", str(out), "--out", str(guardrail)],
        ["build-stage5ai-readiness", "--bundle-root", str(bundle_root), "--out", str(readiness)],
        ["build-stage5ai-next-stage-decision", "--readiness", str(readiness), "--missing-source-plan", str(missing), "--out", str(decision)],
        [
            "build-stage5ai-summary",
            "--policy",
            str(policy),
            "--source-card-summary",
            str(source_cards),
            "--content-index-summary",
            str(content),
            "--website-ingest-format",
            str(website),
            "--deep-research-pack-format",
            str(deep),
            "--bundle-generation-summary",
            str(bundle_summary),
            "--classification",
            str(classification),
            "--missing-source-plan",
            str(missing),
            "--readiness",
            str(readiness),
            "--guardrail",
            str(guardrail),
            "--next-stage-decision",
            str(decision),
            "--out",
            str(summary),
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
            "validate-stage5ai",
            "--policy",
            str(policy),
            "--source-card-summary",
            str(source_cards),
            "--content-index-summary",
            str(content),
            "--website-ingest-format",
            str(website),
            "--deep-research-pack-format",
            str(deep),
            "--bundle-generation-summary",
            str(bundle_summary),
            "--classification",
            str(classification),
            "--missing-source-plan",
            str(missing),
            "--readiness",
            str(readiness),
            "--guardrail",
            str(guardrail),
            "--next-stage-decision",
            str(decision),
            "--summary",
            str(summary),
            "--bundle-root",
            str(bundle_root),
            "--results-dir",
            str(out),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "source_harvester_stage5ai_valid=true" in validate.output
