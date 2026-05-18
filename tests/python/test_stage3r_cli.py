from __future__ import annotations

import json
from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")


def _write_yaml(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")


def test_discord_leads_cli_promote_and_builds_manifests(tmp_path: Path) -> None:
    review_dir = tmp_path / "review"
    _write_json(review_dir / "review_bundle_summary.json", {"review_lead_count": 1, "public_link_count": 1})
    _write_jsonl(review_dir / "source_links_index.jsonl", [{"public_links": ["https://github.com/rtkd/iddqd"]}])
    _write_jsonl(review_dir / "method_claims_index.jsonl", [])
    _write_jsonl(review_dir / "numeric_observations_index.jsonl", [])
    _write_jsonl(review_dir / "visual_observations_index.jsonl", [])
    _write_jsonl(review_dir / "debunks_and_false_positives_index.jsonl", [])
    empty_yaml = tmp_path / "empty.yaml"
    _write_yaml(empty_yaml, {"records": []})

    result = CliRunner().invoke(
        app,
        [
            "discord-leads",
            "promote",
            "--review-dir",
            str(review_dir),
            "--stage3o-links",
            str(empty_yaml),
            "--stage3o-methods",
            str(empty_yaml),
            "--stage3o-numerics",
            str(empty_yaml),
            "--source-registry",
            str(empty_yaml),
            "--visual-registry",
            str(empty_yaml),
            "--cookie-records",
            str(empty_yaml),
            "--out-dir",
            str(tmp_path / "out"),
            "--promoted-sources-out",
            str(tmp_path / "sources.yaml"),
            "--promoted-observations-out",
            str(tmp_path / "observations.yaml"),
            "--negative-controls-out",
            str(tmp_path / "negative.yaml"),
            "--audit-summary-out",
            str(tmp_path / "summary.yaml"),
            "--allow-warnings",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "source_records_promoted=13" in result.output

    result = CliRunner().invoke(
        app,
        [
            "discord-leads",
            "build-manifests",
            "--audit-summary",
            str(tmp_path / "summary.yaml"),
            "--out-dir",
            str(tmp_path / "manifests"),
            "--allow-warnings",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "manifest_count=3" in result.output

    result = CliRunner().invoke(
        app,
        [
            "discord-leads",
            "validate",
            "--promoted-sources",
            str(tmp_path / "sources.yaml"),
            "--promoted-observations",
            str(tmp_path / "observations.yaml"),
            "--negative-controls",
            str(tmp_path / "negative.yaml"),
            "--manifest-dir",
            str(tmp_path / "manifests"),
            "--allow-empty",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "validation_error_count=0" in result.output
