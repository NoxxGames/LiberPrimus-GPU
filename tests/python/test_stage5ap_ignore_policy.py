from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5ap_generated_outputs_are_ignored() -> None:
    assert _ignored("experiments/results/token-block/stage5ap/canonical_token_grid.csv")
    assert _ignored("experiments/results/token-block/stage5ap/token_byte_preflight_primary_60.json")
    assert _ignored("experiments/results/stego-controls/stage5ap/outguess_positive_control_matrix.json")
    assert _ignored("codex-output/stage5ap-codex-completion.md")


def test_stage5ap_raw_and_local_sources_remain_ignored() -> None:
    assert _ignored("third_party/LiberPrimusPages/49.jpg")
    assert _ignored("data/raw/images/Fib421.jpg")
