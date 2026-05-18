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


def test_image_transform_generated_outputs_are_ignored() -> None:
    assert _is_ignored("experiments/results/image-transforms/stage3p/review_index.html")
    assert _is_ignored("experiments/results/image-transforms/stage3p/transform_records.jsonl")
    assert _is_ignored("experiments/results/image-transforms/stage3p/contact_sheets/example.jpg")


def test_raw_page_images_and_discord_logs_remain_ignored() -> None:
    assert _is_ignored("third_party/LiberPrimusPages/example.jpg")
    assert _is_ignored("third_party/LiberPrimusPages/example.jpeg")
    assert _is_ignored("third_party/LiberPrimusPages/example.png")
    assert _is_ignored("third_party/LiberPrimusDiscordChats/example.html")


def test_no_ocr_ai_or_opencv_dependency_required() -> None:
    pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8").lower()
    for forbidden in ["opencv", "cv2", "pytesseract", "tesseract", "torch", "tensorflow"]:
        assert forbidden not in pyproject
