from __future__ import annotations

from pathlib import Path

from test_stage5dj_common import ensure_stage5dj_built, git_check_ignore


def test_stage5dj_generated_outputs_music_cache_and_handoff_are_ignored() -> None:
    ensure_stage5dj_built()

    assert git_check_ignore("experiments/results/token-block/stage5dj/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5dj/metadata_report.json")
    assert git_check_ignore("codex-output/stage5dj-codex-completion.md")
    assert git_check_ignore("third_party/CicadaMusic/761.MP3")
    assert git_check_ignore("third_party/CicadaMusic/Interconnectedness.mp3")


def test_stage5dj_codex_output_underscore_root_absent() -> None:
    ensure_stage5dj_built()

    assert not (Path("codex_output")).exists()
