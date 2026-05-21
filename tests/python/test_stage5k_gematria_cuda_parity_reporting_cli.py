from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


PARITY_MANIFEST = "experiments/manifests/cuda/stage5k-gematria-cuda-parity-reporting.yaml"
AUDIT_MANIFEST = "experiments/manifests/cuda/stage5k-gematria-device-code-audit.yaml"
PREFLIGHT_MANIFEST = "experiments/manifests/cuda/stage5k-solved-fixture-safe-preflight.yaml"


def test_stage5k_cli_no_gpu_safe_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5k"
    parity = tmp_path / "parity.yaml"
    audit = tmp_path / "audit.yaml"
    preflight = tmp_path / "preflight.yaml"
    score = tmp_path / "score.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    commands = [
        [
            "gematria-cuda-parity-reporting",
            "build-parity-report",
            "--manifest",
            PARITY_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--parity-report-out",
            str(parity),
            "--allow-warnings",
        ],
        [
            "gematria-cuda-parity-reporting",
            "audit-device-code",
            "--manifest",
            AUDIT_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--device-code-audit-out",
            str(audit),
            "--allow-warnings",
        ],
        [
            "gematria-cuda-parity-reporting",
            "build-solved-fixture-preflight",
            "--manifest",
            PREFLIGHT_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--preflight-out",
            str(preflight),
            "--allow-warnings",
        ],
        [
            "gematria-cuda-parity-reporting",
            "build-score-summary-preflight",
            "--manifest",
            PREFLIGHT_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--score-summary-preflight-out",
            str(score),
            "--allow-warnings",
        ],
        [
            "gematria-cuda-parity-reporting",
            "build-summary",
            "--parity-report",
            str(parity),
            "--device-code-audit",
            str(audit),
            "--preflight",
            str(preflight),
            "--score-summary-preflight",
            str(score),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    ]
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output

    validate = runner.invoke(
        app,
        [
            "gematria-cuda-parity-reporting",
            "validate-stage5k",
            "--parity-report",
            str(parity),
            "--device-code-audit",
            str(audit),
            "--preflight",
            str(preflight),
            "--score-summary-preflight",
            str(score),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "gematria_cuda_parity_reporting_stage5k_valid=true" in validate.output

    printed = runner.invoke(app, ["gematria-cuda-parity-reporting", "summary", "--summary", str(summary)])
    assert printed.exit_code == 0, printed.output
    assert "solved_fixture_cuda_execution_allowed=False" in printed.output
    assert "selected_next_stage=Stage 5L" in printed.output
