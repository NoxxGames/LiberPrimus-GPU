from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", *args],
        check=True,
        text=True,
        capture_output=True,
    )


def test_stage5z_cli_build_validate_and_summary_work_in_temp_dir(tmp_path: Path) -> None:
    out_dir = tmp_path / "reports"
    paths = {
        "contract": tmp_path / "contract.yaml",
        "kernel": tmp_path / "kernel.yaml",
        "host": tmp_path / "host.yaml",
        "buffer": tmp_path / "buffer.yaml",
        "vectors": tmp_path / "vectors.yaml",
        "future": tmp_path / "future.yaml",
        "result": tmp_path / "result.yaml",
        "blocker": tmp_path / "blocker.yaml",
        "scored": tmp_path / "scored.yaml",
        "gate": tmp_path / "gate.yaml",
        "decision": tmp_path / "decision.yaml",
        "summary": tmp_path / "summary.yaml",
    }
    commands = [
        ["build-contract-records", "--cuda-contract-out", paths["contract"]],
        ["build-kernel-abi", "--kernel-abi-out", paths["kernel"]],
        ["build-host-runner-contract", "--host-runner-contract-out", paths["host"]],
        ["build-buffer-contract", "--buffer-contract-out", paths["buffer"]],
        ["build-validation-vectors", "--validation-vectors-out", paths["vectors"]],
        ["build-future-parity-plan", "--future-parity-plan-out", paths["future"]],
        ["build-result-store-compatibility", "--result-store-compatibility-out", paths["result"]],
        ["build-full-p56-blocker", "--full-p56-blocker-out", paths["blocker"]],
        ["build-scored-experiment-deferral", "--scored-experiment-deferral-out", paths["scored"]],
        ["build-implementation-readiness-gate", "--implementation-readiness-out", paths["gate"]],
        ["build-next-stage-decision", "--next-stage-decision-out", paths["decision"]],
    ]
    for command in commands:
        _run(
            [
                "prime-minus-one-cuda-contract",
                command[0],
                *[str(item) for item in command[1:]],
                "--out-dir",
                str(out_dir),
                "--allow-warnings",
            ]
        )
    _run(
        [
            "prime-minus-one-cuda-contract",
            "build-summary",
            "--cuda-contract",
            str(paths["contract"]),
            "--kernel-abi",
            str(paths["kernel"]),
            "--host-runner-contract",
            str(paths["host"]),
            "--buffer-contract",
            str(paths["buffer"]),
            "--validation-vectors",
            str(paths["vectors"]),
            "--future-parity-plan",
            str(paths["future"]),
            "--result-store-compatibility",
            str(paths["result"]),
            "--full-p56-blocker",
            str(paths["blocker"]),
            "--scored-experiment-deferral",
            str(paths["scored"]),
            "--implementation-readiness-gate",
            str(paths["gate"]),
            "--next-stage-decision",
            str(paths["decision"]),
            "--summary-out",
            str(paths["summary"]),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ]
    )
    validate = _run(
        [
            "prime-minus-one-cuda-contract",
            "validate-stage5z",
            "--cuda-contract",
            str(paths["contract"]),
            "--kernel-abi",
            str(paths["kernel"]),
            "--host-runner-contract",
            str(paths["host"]),
            "--buffer-contract",
            str(paths["buffer"]),
            "--validation-vectors",
            str(paths["vectors"]),
            "--future-parity-plan",
            str(paths["future"]),
            "--result-store-compatibility",
            str(paths["result"]),
            "--full-p56-blocker",
            str(paths["blocker"]),
            "--scored-experiment-deferral",
            str(paths["scored"]),
            "--implementation-readiness-gate",
            str(paths["gate"]),
            "--next-stage-decision",
            str(paths["decision"]),
            "--summary",
            str(paths["summary"]),
            "--results-dir",
            str(out_dir),
        ]
    )
    summary = _run(["prime-minus-one-cuda-contract", "summary", "--summary", str(paths["summary"])])
    summary_text = " ".join(summary.stdout.split())
    assert "prime_minus_one_cuda_contract_stage5z_valid=true" in validate.stdout
    assert "Stage 5AA - prime-minus-one CUDA synthetic kernel implementation" in summary_text
