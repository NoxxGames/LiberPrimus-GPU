from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image
from typer.testing import CliRunner

from libreprimus.cli import app


def test_image_analysis_cli_runs_on_synthetic_temp_dir(tmp_path: Path) -> None:
    source = tmp_path / "images"
    source.mkdir()
    image_path = source / "sample.png"
    Image.new("RGB", (8, 8), (255, 255, 255)).save(image_path)
    image_bytes = image_path.read_bytes()
    locks = tmp_path / "locks.jsonl"
    locks.write_text(
        json.dumps(
            {
                "relative_path": image_path.as_posix(),
                "source_id": "synthetic-source",
                "sha256": hashlib.sha256(image_bytes).hexdigest(),
            }
        )
        + "\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "out"

    result = CliRunner().invoke(
        app,
        [
            "image-analysis",
            "analyze-local-pages",
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
    assert (out_dir / "image_analysis_records.jsonl").is_file()


def test_image_analysis_cli_supports_allow_missing(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "image-analysis",
            "validate-results",
            "--results-dir",
            str(tmp_path / "missing-results"),
            "--allow-missing",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "Image analysis results OK" in result.output


def test_image_analysis_summary_cli(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    (out_dir / "summary.json").write_text(
        """{
  "record_type": "image_analysis_run_summary",
  "run_id": "synthetic",
  "generated_at_utc": "2026-05-17T00:00:00Z",
  "image_count": 0,
  "threshold_values": [32, 64, 96, 128, 160, 192, 224],
  "symmetry_metrics": ["horizontal_mirror_difference", "vertical_mirror_difference", "rotational_180_difference"],
  "feature_candidate_count": 0,
  "feature_counts": {},
  "output_paths": {},
  "warnings": [],
  "trusted_as_canonical": false,
  "solve_claim": false
}
""",
        encoding="utf-8",
    )

    result = CliRunner().invoke(app, ["image-analysis", "summary", "--results-dir", str(out_dir)])

    assert result.exit_code == 0, result.output
    assert "solve_claim=false" in result.output
