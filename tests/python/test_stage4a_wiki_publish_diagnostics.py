from __future__ import annotations

import shutil
import subprocess

import pytest


def test_stage4a_wiki_publish_diagnostics_handle_inaccessible_remote() -> None:
    shell = shutil.which("powershell") or shutil.which("pwsh")
    if shell is None:
        pytest.skip("PowerShell is not available in this environment")

    result = subprocess.run(
        [
            shell,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            "scripts/github/sync-tutorials-to-wiki.ps1",
            "--Publish",
            "--WikiRemote",
            "https://github.com/NoxxGames/definitely-missing-lpgpu-wiki.wiki.git",
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode != 0
    assert "Wiki remote is not accessible" in result.stdout or "Repository not found" in result.stdout
