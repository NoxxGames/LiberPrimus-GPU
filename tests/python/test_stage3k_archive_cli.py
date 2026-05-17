from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
SOURCES = REPO / "data/observations/archive/source-archive-records-v0.yaml"


def test_archive_validate_sources_cli() -> None:
    result = CliRunner().invoke(app, ["archive", "validate-sources", "--records", str(SOURCES)])

    assert result.exit_code == 0, result.output
    assert "source_record_count=12" in result.output


def test_archive_scan_local_images_cli_with_synthetic_temp_dir(tmp_path: Path) -> None:
    source = tmp_path / "images"
    source.mkdir()
    (source / "sample.png").write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + b"\x00\x00\x00\rIHDR"
        + (31).to_bytes(4, "big")
        + (29).to_bytes(4, "big")
        + b"\x08\x02\x00\x00\x00\x00\x00\x00\x00"
    )
    result = CliRunner().invoke(
        app,
        [
            "archive",
            "scan-local-images",
            "--source-dir",
            str(source),
            "--lock-out",
            str(tmp_path / "locks.jsonl"),
            "--artifact-out",
            str(tmp_path / "artifacts.jsonl"),
            "--summary-out",
            str(tmp_path / "summary.json"),
            "--allow-missing",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "image_count=1" in result.output


def test_archive_validate_image_locks_cli() -> None:
    result = CliRunner().invoke(
        app,
        [
            "archive",
            "validate-image-locks",
            "--locks",
            "data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl",
            "--artifacts",
            "data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl",
            "--allow-empty",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "Image lock records OK" in result.output
