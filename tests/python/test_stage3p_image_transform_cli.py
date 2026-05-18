from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image
from typer.testing import CliRunner

from libreprimus.cli import app


def test_image_transform_cli_runs_on_synthetic_temp_dir(tmp_path: Path) -> None:
    source = tmp_path / "images"
    source.mkdir()
    image_path = source / "sample.png"
    Image.new("RGB", (8, 8), (255, 255, 255)).save(image_path)
    locks = tmp_path / "locks.jsonl"
    locks.write_text(
        json.dumps(
            {
                "relative_path": image_path.as_posix(),
                "source_id": "synthetic-source",
                "sha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
            }
        )
        + "\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "out"

    result = CliRunner().invoke(
        app,
        [
            "image-transform",
            "run-local-pages",
            "--source-dir",
            str(source),
            "--image-locks",
            str(locks),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "image_count=1" in result.output
    assert (out_dir / "transform_records.jsonl").is_file()
    assert (out_dir / "review_index.html").is_file()


def test_image_transform_cli_supports_allow_missing(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "image-transform",
            "validate-results",
            "--results-dir",
            str(tmp_path / "missing-results"),
            "--allow-missing",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "Image transform results OK" in result.output
