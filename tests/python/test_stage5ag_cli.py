from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.source_harvester.cli import app

runner = CliRunner()


def test_stage5ag_cli_pipeline_validates_with_missing_ignored_source_root(tmp_path: Path) -> None:
    out = tmp_path / "out"
    root_inventory = tmp_path / "root.yaml"
    file_summary = tmp_path / "files.yaml"
    archive_summary = tmp_path / "archives.yaml"
    hash_summary = tmp_path / "hashes.yaml"
    linkage = tmp_path / "linkage.yaml"
    extension = tmp_path / "extension.yaml"
    candidates = tmp_path / "candidates.yaml"
    gaps = tmp_path / "gaps.yaml"
    bundles = tmp_path / "bundles.yaml"
    guardrail = tmp_path / "guardrail.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"
    source_root = "third_party/__stage5ag_cli_missing__"

    commands = [
        [
            "inventory-local-sources",
            "--source-root",
            source_root,
            "--results-dir",
            str(out),
            "--out-root-inventory",
            str(root_inventory),
            "--out-file-summary",
            str(file_summary),
            "--out-archive-summary",
            str(archive_summary),
            "--out-hash-summary",
            str(hash_summary),
        ],
        [
            "link-local-sources",
            "--source-root",
            source_root,
            "--results-dir",
            str(out),
            "--out",
            str(linkage),
            "--out-extension",
            str(extension),
        ],
        [
            "build-source-lock-candidates",
            "--local-linkage",
            str(linkage),
            "--out",
            str(candidates),
            "--gap-report",
            str(gaps),
        ],
        [
            "build-bundle-readiness",
            "--local-linkage",
            str(linkage),
            "--out",
            str(bundles),
            "--results-dir",
            str(out),
        ],
        [
            "build-stage5ag-guardrail",
            "--source-root",
            source_root,
            "--results-dir",
            str(out),
            "--out",
            str(guardrail),
        ],
        [
            "build-stage5ag-next-stage-decision",
            "--root-inventory",
            str(root_inventory),
            "--local-linkage",
            str(linkage),
            "--bundle-readiness",
            str(bundles),
            "--out",
            str(decision),
        ],
        [
            "build-stage5ag-summary",
            "--root-inventory",
            str(root_inventory),
            "--file-summary",
            str(file_summary),
            "--archive-summary",
            str(archive_summary),
            "--hash-summary",
            str(hash_summary),
            "--local-linkage",
            str(linkage),
            "--candidate-summary",
            str(candidates),
            "--gap-report",
            str(gaps),
            "--bundle-readiness",
            str(bundles),
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
            "validate-stage5ag",
            "--root-inventory",
            str(root_inventory),
            "--file-summary",
            str(file_summary),
            "--archive-summary",
            str(archive_summary),
            "--hash-summary",
            str(hash_summary),
            "--local-linkage",
            str(linkage),
            "--candidate-summary",
            str(candidates),
            "--gap-report",
            str(gaps),
            "--bundle-readiness",
            str(bundles),
            "--guardrail",
            str(guardrail),
            "--next-stage-decision",
            str(decision),
            "--summary",
            str(summary),
            "--results-dir",
            str(out),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "source_harvester_stage5ag_valid=true" in validate.output
