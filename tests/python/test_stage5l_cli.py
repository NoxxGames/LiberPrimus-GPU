from __future__ import annotations

import subprocess
import sys


def test_stage5l_cli_summary_and_validate_work() -> None:
    summary = subprocess.run(
        [
            sys.executable,
            "-m",
            "libreprimus.cli",
            "gematria-solved-fixture-mapping",
            "summary",
            "--summary",
            "data/cuda/stage5l-solved-fixture-token-mapping-summary.yaml",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "mapped_count=5" in summary.stdout
    validate = subprocess.run(
        [
            sys.executable,
            "-m",
            "libreprimus.cli",
            "gematria-solved-fixture-mapping",
            "validate-stage5l",
            "--token-mapping",
            "data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml",
            "--native-parity",
            "data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml",
            "--output-hash-contract",
            "data/cuda/stage5l-gematria-solved-fixture-output-hash-contract.yaml",
            "--score-summary-shape",
            "data/cuda/stage5l-gematria-solved-fixture-score-summary-shape.yaml",
            "--summary",
            "data/cuda/stage5l-solved-fixture-token-mapping-summary.yaml",
            "--results-dir",
            "experiments/results/gematria-solved-fixture-mapping/stage5l",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "gematria_solved_fixture_mapping_stage5l_valid=true" in validate.stdout


def test_stage5l_next_stage_decision_is_deterministic() -> None:
    output = subprocess.run(
        [
            sys.executable,
            "-m",
            "libreprimus.cli",
            "gematria-solved-fixture-mapping",
            "summary",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    normalized = " ".join(output.split())
    assert "Stage 5M - first solved-fixture-safe Gematria shift_score CUDA parity run" in normalized
