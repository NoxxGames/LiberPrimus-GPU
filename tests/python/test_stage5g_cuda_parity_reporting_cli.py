from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


PARITY_MANIFEST = "experiments/manifests/cuda/stage5g-shift-score-parity-reporting.yaml"
AUDIT_MANIFEST = "experiments/manifests/cuda/stage5g-device-code-subset-audit.yaml"
PREFLIGHT_MANIFEST = "experiments/manifests/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml"


def test_stage5g_cuda_parity_reporting_cli_no_gpu_safe_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5g"
    parity = tmp_path / "parity.yaml"
    audit = tmp_path / "audit.yaml"
    preflight = tmp_path / "preflight.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    parity_result = runner.invoke(
        app,
        [
            "cuda-parity-reporting",
            "build-parity-report",
            "--manifest",
            PARITY_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--parity-report-out",
            str(parity),
            "--allow-warnings",
        ],
    )
    assert parity_result.exit_code == 0, parity_result.output
    assert "stage5f_cuda_native_hash_match=true" in parity_result.output

    audit_result = runner.invoke(
        app,
        [
            "cuda-parity-reporting",
            "audit-device-code-subset",
            "--manifest",
            AUDIT_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--device-code-audit-out",
            str(audit),
            "--allow-warnings",
        ],
    )
    assert audit_result.exit_code == 0, audit_result.output
    assert "device_code_subset_compliant=true" in audit_result.output

    preflight_result = runner.invoke(
        app,
        [
            "cuda-parity-reporting",
            "build-solved-fixture-preflight",
            "--manifest",
            PREFLIGHT_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--preflight-out",
            str(preflight),
            "--allow-warnings",
        ],
    )
    assert preflight_result.exit_code == 0, preflight_result.output
    assert "production_gematria_mod29_cuda_ready=false" in preflight_result.output

    summary_result = runner.invoke(
        app,
        [
            "cuda-parity-reporting",
            "build-summary",
            "--parity-report",
            str(parity),
            "--device-code-audit",
            str(audit),
            "--preflight",
            str(preflight),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert summary_result.exit_code == 0, summary_result.output

    validate = runner.invoke(
        app,
        [
            "cuda-parity-reporting",
            "validate-stage5g",
            "--parity-report",
            str(parity),
            "--device-code-audit",
            str(audit),
            "--preflight",
            str(preflight),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "cuda_parity_reporting_stage5g_valid=true" in validate.output

    printed = runner.invoke(app, ["cuda-parity-reporting", "summary", "--summary", str(summary)])
    assert printed.exit_code == 0, printed.output
    assert "Stage 5H - Gematria mod-29 shift_score contract" in printed.output
