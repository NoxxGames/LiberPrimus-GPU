from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


SMOKE_MANIFEST = "experiments/manifests/native-cpu/stage5d-native-cpu-smoke.yaml"
THREADING_MANIFEST = "experiments/manifests/native-cpu/stage5d-native-cpu-threading-parity.yaml"
PARITY_MANIFEST = "experiments/manifests/native-cpu/stage5d-native-python-parity.yaml"


def test_stage5d_native_cpu_cli_round_trip(tmp_path: Path) -> None:
    native = _fake_native(tmp_path)
    out_dir = tmp_path / "stage5d"
    capabilities = tmp_path / "capabilities.yaml"
    threading = tmp_path / "threading.yaml"
    parity = tmp_path / "parity.yaml"
    diagnostics = tmp_path / "diagnostics.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    smoke = runner.invoke(
        app,
        [
            "native-cpu",
            "run-smoke",
            "--native-executable",
            str(native),
            "--manifest",
            SMOKE_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--capabilities-out",
            str(capabilities),
            "--diagnostics-out",
            str(diagnostics),
            "--allow-warnings",
        ],
    )
    assert smoke.exit_code == 0, smoke.output
    assert "native_backend_built=true" in smoke.output

    thread = runner.invoke(
        app,
        [
            "native-cpu",
            "check-threading-parity",
            "--native-executable",
            str(native),
            "--manifest",
            THREADING_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--threading-out",
            str(threading),
            "--thread-counts",
            "1,2,4",
            "--allow-warnings",
        ],
    )
    assert thread.exit_code == 0, thread.output
    assert "one_thread_equals_multi_thread=true" in thread.output

    py_parity = runner.invoke(
        app,
        [
            "native-cpu",
            "check-python-parity",
            "--native-executable",
            str(native),
            "--manifest",
            PARITY_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--parity-out",
            str(parity),
            "--allow-warnings",
        ],
    )
    assert py_parity.exit_code == 0, py_parity.output
    assert "python_native_parity=true" in py_parity.output

    build_summary = runner.invoke(
        app,
        [
            "native-cpu",
            "build-summary",
            "--capabilities",
            str(capabilities),
            "--threading",
            str(threading),
            "--parity",
            str(parity),
            "--diagnostics",
            str(diagnostics),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert build_summary.exit_code == 0, build_summary.output

    validate = runner.invoke(
        app,
        [
            "native-cpu",
            "validate-stage5d",
            "--capabilities",
            str(capabilities),
            "--threading",
            str(threading),
            "--parity",
            str(parity),
            "--diagnostics",
            str(diagnostics),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "native_cpu_stage5d_valid=true" in validate.output

    printed = runner.invoke(app, ["native-cpu", "summary", "--summary", str(summary)])
    assert printed.exit_code == 0, printed.output
    assert "threading_records=3" in printed.output


def _fake_native(tmp_path: Path) -> Path:
    script = tmp_path / "fake_native.py"
    script.write_text(
        "import json\n"
        "import sys\n"
        "from libreprimus.native_cpu.runner import python_reference_run\n"
        "threads = 1\n"
        "for index, arg in enumerate(sys.argv):\n"
        "    if arg == '--threads' and index + 1 < len(sys.argv):\n"
        "        threads = int(sys.argv[index + 1])\n"
        "print(json.dumps(python_reference_run(threads=threads)))\n",
        encoding="utf-8",
    )
    return script
