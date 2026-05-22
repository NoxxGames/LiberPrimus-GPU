from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def test_stage5v_generated_raw_codex_and_sqlite_paths_are_ignored() -> None:
    for path in [
        "experiments/results/cuda-candidate-batch-abi-conformance/stage5v/native_adapter_report.json",
        "experiments/results/cuda-candidate-batch-abi-conformance/stage5v/conformance_fixture_report.json",
        "experiments/results/cuda-candidate-batch-abi-conformance/stage5v/token_buffer_conformance_report.json",
        "experiments/results/cuda-candidate-batch-abi-conformance/stage5v/score_vector_conformance_report.json",
        "experiments/results/cuda-candidate-batch-abi-conformance/stage5v/topk_conformance_report.json",
        "experiments/results/cuda-candidate-batch-abi-conformance/stage5v/summary.json",
        "experiments/results/cuda-candidate-batch-abi-conformance/stage5v/results.sqlite3",
        "codex-output/stage5v-codex-completion.md",
        "data/raw/stage5v-example.txt",
    ]:
        assert _ignored(path), path


def test_stage5v_raw_generated_codex_and_sqlite_not_staged() -> None:
    result = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=ROOT, check=True, capture_output=True, text=True)
    staged = set(result.stdout.splitlines())
    assert not any(path.startswith("experiments/results/") for path in staged)
    assert not any(path.startswith("data/raw/") for path in staged)
    assert not any(path.startswith("codex-output/") for path in staged)
    assert not any(path.endswith((".sqlite", ".sqlite3", ".db")) for path in staged)
