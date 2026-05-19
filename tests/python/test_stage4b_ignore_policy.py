from __future__ import annotations

import subprocess


def test_stage4b_generated_outputs_and_raw_inputs_ignored() -> None:
    for path in [
        "experiments/results/source-lock-triage/stage4b/source_triage_report.json",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], check=False)
        assert result.returncode == 0, path
