from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _is_ignored(path: str) -> bool:
    return (
        subprocess.run(
            ["git", "check-ignore", "-q", "--", path],
            cwd=REPO,
            check=False,
        ).returncode
        == 0
    )


def test_third_party_liber_primus_page_images_ignored() -> None:
    assert _is_ignored("third_party/LiberPrimusPages/example.jpg")
    assert _is_ignored("third_party/LiberPrimusPages/example.jpeg")
    assert _is_ignored("third_party/LiberPrimusPages/example.png")


def test_archive_visual_generated_outputs_ignored() -> None:
    assert _is_ignored(
        "experiments/results/archive-visual-registry/stage3k/local-image-scan-summary.json"
    )


def test_stage3k_registry_records_trackable() -> None:
    assert not _is_ignored("data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl")
    assert not _is_ignored(
        "data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl"
    )
