from __future__ import annotations

import subprocess


def test_stage3v_generated_outputs_are_ignored() -> None:
    for path in [
        "experiments/results/stego/outguess/stage3v/summary.json",
        "experiments/results/stego/outguess/stage3v/extraction_records.jsonl",
        "experiments/results/stego/outguess/stage3v/outguess_tool_record.json",
        "experiments/results/stego/outguess/stage3v/extracted_payloads/example.txt",
        "experiments/results/stego/outguess/stage3v/synthetic_inputs/example.jpg",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], check=False)
        assert result.returncode == 0


def test_stage3v_raw_inputs_remain_ignored() -> None:
    for path in [
        "third_party/CicadaArchive/example.jpg",
        "third_party/CicadaOutGuess/example.jpg",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], check=False)
        assert result.returncode == 0
