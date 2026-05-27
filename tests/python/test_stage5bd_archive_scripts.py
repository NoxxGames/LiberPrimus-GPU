from pathlib import Path


def test_stage5bd_archive_scripts_are_committed_text_scaffolds() -> None:
    paths = [
        Path("scripts/archive/create-deep-research-repo-zip.ps1"),
        Path("scripts/archive/create-deep-research-repo-zip.sh"),
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "ARCHIVE_COMMIT.txt" in text
        assert "ARCHIVE_MANIFEST.json" in text
