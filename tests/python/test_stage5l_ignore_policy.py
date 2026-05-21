from __future__ import annotations

import re
import subprocess
from pathlib import Path


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
    pattern = re.compile(r"Py_Initialize|python\.exe|python3|popen\(.*python|system\(.*python")
    tracked = subprocess.run(
        ["git", "ls-files", "src", "cuda"],
        check=True,
        capture_output=True,
        text=True,
    )
    findings: list[str] = []
    for path_text in tracked.stdout.splitlines():
        path = Path(path_text)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                findings.append(f"{path_text}:{line_number}:{line.strip()}")
    assert findings == []
