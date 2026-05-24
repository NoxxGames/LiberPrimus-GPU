from __future__ import annotations

import subprocess


def test_stage5an_generated_private_outputs_are_ignored() -> None:
    paths = [
        "deep-research-content-packs/stage5an/deep-research-content-pack-stage5an.zip",
        "website-export/stage5an/private-content/index.html",
        "website-export/stage5an/webserver-root/index.html",
        "website-export/stage5an/webserver-root/private-content/index.html",
        "website-export/stage5an/webserver-root.zip",
        "codex-output/stage5an-codex-completion.md",
    ]
    for path in paths:
        subprocess.run(["git", "check-ignore", "-q", path], check=True)


def test_stage5an_raw_roots_remain_ignored() -> None:
    for path in [
        "third_party/UsefulFilesAndIdeas/LP Excel.xlsx",
        "research-inputs/stage5ai/private.md",
        "source-harvester-output/stage5an/raw.txt",
        "harvest-output/stage5an/raw.txt",
    ]:
        subprocess.run(["git", "check-ignore", "-q", path], check=True)
