from __future__ import annotations

from typer.testing import CliRunner
from PIL import Image

from libreprimus.cli import app


def test_stage4m_image_preflight_cli_build_validate_summary(tmp_path) -> None:
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    Image.new("RGB", (12, 10), (30, 40, 50)).save(image_dir / "0.jpg")
    bigram_image = tmp_path / "Fib421.jpg"
    Image.new("RGB", (4, 4), (9, 8, 7)).save(bigram_image)
    out_dir = tmp_path / "out"
    source_variant = tmp_path / "source_variant.yaml"
    compression = tmp_path / "compression.yaml"
    artifact_candidates = tmp_path / "artifact_candidates.yaml"
    summary = tmp_path / "summary.yaml"
    bigram = tmp_path / "bigram.yaml"
    runner = CliRunner()

    build = runner.invoke(
        app,
        [
            "image-preflight",
            "build",
            "--image-dir",
            str(image_dir),
            "--image-artifacts",
            str(tmp_path / "missing-artifacts.jsonl"),
            "--image-locks",
            str(tmp_path / "missing-locks.jsonl"),
            "--source-delta",
            str(tmp_path / "missing-source-delta.yaml"),
            "--compression-observations",
            str(tmp_path / "missing-compression.yaml"),
            "--promotion-readiness",
            str(tmp_path / "missing-promotion.yaml"),
            "--manifest-readiness",
            str(tmp_path / "missing-manifest.yaml"),
            "--bigram-image",
            str(bigram_image),
            "--out-dir",
            str(out_dir),
            "--source-variant-out",
            str(source_variant),
            "--compression-out",
            str(compression),
            "--artifact-candidates-out",
            str(artifact_candidates),
            "--summary-out",
            str(summary),
            "--bigram-readiness-out",
            str(bigram),
            "--allow-warnings",
        ],
    )
    assert build.exit_code == 0, build.output
    assert "image_count=1" in build.output

    validate = runner.invoke(
        app,
        [
            "image-preflight",
            "validate",
            "--source-variant",
            str(source_variant),
            "--compression",
            str(compression),
            "--artifact-candidates",
            str(artifact_candidates),
            "--summary",
            str(summary),
            "--bigram-readiness",
            str(bigram),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "image_preflight_valid=true" in validate.output

    report = runner.invoke(app, ["image-preflight", "summary", "--summary", str(summary), "--bigram-readiness", str(bigram)])
    assert report.exit_code == 0, report.output
    assert "bigram_readiness_blocked=true" in report.output
