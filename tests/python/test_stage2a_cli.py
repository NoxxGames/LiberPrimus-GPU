from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app
from test_stage2a_solved_baseline_runner_synthetic import _write_synthetic_suite


def test_transform_registry_cli_validate_list_and_resolve() -> None:
    runner = CliRunner()

    validated = runner.invoke(
        app,
        [
            "transform-registry",
            "validate",
            "--registry",
            "data/transform-registry/cpu-reference-transforms-v0.json",
        ],
    )
    listed = runner.invoke(
        app,
        [
            "transform-registry",
            "list",
            "--registry",
            "data/transform-registry/cpu-reference-transforms-v0.json",
        ],
    )
    resolved = runner.invoke(
        app,
        [
            "transform-registry",
            "resolve",
            "--registry",
            "data/transform-registry/cpu-reference-transforms-v0.json",
            "--transform-id",
            "phi_prime_stream",
        ],
    )

    assert validated.exit_code == 0, validated.output
    assert listed.exit_code == 0, listed.output
    assert "prime_minus_one_stream" in resolved.output
    assert resolved.exit_code == 0, resolved.output


def test_solved_baseline_cli_run_summary_and_stage2a_smoke(tmp_path: Path) -> None:
    manifest_path, candidate_dir = _write_synthetic_suite(tmp_path)
    out_dir = tmp_path / "out"
    runner = CliRunner()

    validated = runner.invoke(
        app,
        ["solved-baseline", "validate-manifest", "--manifest", str(manifest_path)],
    )
    run = runner.invoke(
        app,
        [
            "solved-baseline",
            "run",
            "--manifest",
            str(manifest_path),
            "--candidate-dir",
            str(candidate_dir),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    summary = runner.invoke(app, ["solved-baseline", "summary", "--results-dir", str(out_dir)])
    smoke = runner.invoke(
        app,
        [
            "solved-baseline",
            "stage2a-smoke",
            "--manifest",
            str(manifest_path),
            "--candidate-dir",
            str(candidate_dir),
            "--out-dir",
            str(tmp_path / "smoke"),
            "--allow-warnings",
        ],
    )

    assert validated.exit_code == 0, validated.output
    assert run.exit_code == 0, run.output
    assert summary.exit_code == 0, summary.output
    assert "pass_count=4" in summary.output
    assert smoke.exit_code == 0, smoke.output


def test_solved_baseline_cli_missing_input_returns_nonzero(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        ["solved-baseline", "validate-manifest", "--manifest", str(tmp_path / "missing.yaml")],
    )

    assert result.exit_code != 0
    assert "not found" in result.output.lower()
