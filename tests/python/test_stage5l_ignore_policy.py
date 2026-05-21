from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5l_generated_outputs_and_codex_output_are_ignored() -> None:
    assert _ignored("experiments/results/gematria-solved-fixture-mapping/stage5l/token_mapping_report.json")
    assert _ignored("experiments/results/gematria-solved-fixture-mapping/stage5l/native_parity_report.json")
    assert _ignored("experiments/results/gematria-solved-fixture-mapping/stage5l/summary.json")
    assert _ignored("codex-output/stage5l-codex-completion.md")


def test_raw_data_and_sqlite_remain_ignored() -> None:
    assert _ignored("data/raw/transcripts/example.txt")
    assert _ignored("experiments/results/gematria-solved-fixture-mapping/stage5l/results.sqlite3")


def test_no_cpp_launches_python_workers() -> None:
    result = subprocess.run(
        ["rg", "-n", "Py_Initialize|python\\.exe|python3|popen\\(.*python|system\\(.*python", "src", "cuda"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode in {0, 1}
    assert "python" not in result.stdout.lower()
