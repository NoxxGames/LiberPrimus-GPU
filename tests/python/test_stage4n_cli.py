from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage4n_cli_build_validate_summary(tmp_path) -> None:
    outguess_sources = tmp_path / "outguess.yaml"
    audio_sources = tmp_path / "audio.yaml"
    outguess_sources.write_text(
        """
record_set_id: test-outguess
records:
- fixture_id: test-4gq25
  source_url: https://example.invalid/4gq25.jpg
  source_path: 4gq25.jpg
  artifact_type: image_fixture_candidate
  expected_role: known_positive_candidate
  local_availability: source_only
  toolchain: [outguess]
""",
        encoding="utf-8",
    )
    audio_sources.write_text(
        """
record_set_id: test-audio
records:
- fixture_id: test-761
  source_url: https://example.invalid/761.MP3
  source_path: 761.MP3
  artifact_type: audio_fixture_candidate
  expected_role: known_positive_candidate
  local_availability: source_only
  toolchain: [mp3stego]
""",
        encoding="utf-8",
    )
    out_dir = tmp_path / "out"
    cache_dir = tmp_path / "cache"
    outguess = tmp_path / "outguess-readiness.yaml"
    audio = tmp_path / "audio-readiness.yaml"
    cache = tmp_path / "cache-records.yaml"
    expected = tmp_path / "expected.yaml"
    toolchain = tmp_path / "toolchain.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    build = runner.invoke(
        app,
        [
            "stego-positive-controls",
            "build",
            "--out-dir",
            str(out_dir),
            "--cache-dir",
            str(cache_dir),
            "--outguess-sources",
            str(outguess_sources),
            "--audio-sources",
            str(audio_sources),
            "--source-health",
            str(tmp_path / "missing-health.yaml"),
            "--toolchain-requirements",
            str(tmp_path / "missing-tools.yaml"),
            "--source-locks",
            str(tmp_path / "missing-locks.yaml"),
            "--source-fetches",
            str(tmp_path / "missing-fetches.yaml"),
            "--source-lock-summary",
            str(tmp_path / "missing-lock-summary.yaml"),
            "--outguess-artifacts",
            str(tmp_path / "missing-artifacts.yaml"),
            "--manifest-readiness",
            str(tmp_path / "missing-manifest.yaml"),
            "--outguess-readiness-out",
            str(outguess),
            "--audio-readiness-out",
            str(audio),
            "--fixture-cache-out",
            str(cache),
            "--expected-output-out",
            str(expected),
            "--toolchain-out",
            str(toolchain),
            "--summary-out",
            str(summary),
            "--allow-warnings",
        ],
    )
    assert build.exit_code == 0, build.output
    assert "synthetic_controls_ready_count=2" in build.output

    validate = runner.invoke(
        app,
        [
            "stego-positive-controls",
            "validate",
            "--outguess-readiness",
            str(outguess),
            "--audio-readiness",
            str(audio),
            "--fixture-cache",
            str(cache),
            "--expected-output",
            str(expected),
            "--toolchain",
            str(toolchain),
            "--summary",
            str(summary),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "stego_positive_controls_valid=true" in validate.output

    report = runner.invoke(app, ["stego-positive-controls", "summary", "--summary", str(summary)])
    assert report.exit_code == 0, report.output
    assert "historical_fixtures_blocked_count=2" in report.output
