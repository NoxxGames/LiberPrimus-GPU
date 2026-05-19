from __future__ import annotations

from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage4f_cli_build_and_validate_with_synthetic_records(tmp_path: Path) -> None:
    records = tmp_path / "records"
    manifests = tmp_path / "manifests"
    source_delta = records / "delta.yaml"
    source_health = records / "stage4e-health.yaml"
    stage4b_sources = records / "stage4b.yaml"
    _write(source_delta, {"records": [{"selected_path_candidates": [{"artifact_type": "lp_outguessed"}]}]})
    _write(source_health, {"records": [{"source_id": "stage4e-iddqd-lp_outguessed"}]})
    _write(
        stage4b_sources,
        {
            "records": [
                {"source_id": "stage4b-uncovering-outguess", "url": "https://example.invalid/outguess"},
                {"source_id": "stage4b-complete-archive-magicsquares", "url": "https://example.invalid/magicsquares.txt"},
                {"source_id": "stage4b-uncovering-instar-emergence", "url": "https://example.invalid/instar"},
                {"source_id": "stage4b-uncovering-what-happened-2014", "url": "https://example.invalid/2014"},
                {"source_id": "stage4b-charleswyt-mp3stego", "url": "https://example.invalid/mp3stego"},
            ]
        },
    )
    result = CliRunner().invoke(
        app,
        [
            "stego-fixtures",
            "build",
            "--stage4e-source-delta",
            str(source_delta),
            "--stage4e-source-health",
            str(source_health),
            "--stage4b-sources",
            str(stage4b_sources),
            "--out-dir",
            str(tmp_path / "out"),
            "--outguess-fixtures-out",
            str(records / "outguess.yaml"),
            "--audio-fixtures-out",
            str(records / "audio.yaml"),
            "--source-health-out",
            str(records / "health.yaml"),
            "--toolchain-out",
            str(records / "toolchain.yaml"),
            "--manifest-out-dir",
            str(manifests),
            "--allow-warnings",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "outguess_fixture_source_records_count=5" in result.output
    validate = CliRunner().invoke(
        app,
        [
            "stego-fixtures",
            "validate",
            "--outguess-fixtures",
            str(records / "outguess.yaml"),
            "--audio-fixtures",
            str(records / "audio.yaml"),
            "--source-health",
            str(records / "health.yaml"),
            "--toolchain",
            str(records / "toolchain.yaml"),
            "--manifest-dir",
            str(manifests),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "stego_fixtures_valid=true" in validate.output


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
