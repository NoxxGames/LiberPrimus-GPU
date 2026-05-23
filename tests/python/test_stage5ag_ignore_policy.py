from __future__ import annotations

import subprocess

from libreprimus.paths import repo_root


def _ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", path],
        cwd=repo_root(),
        check=False,
    )
    return result.returncode == 0


def test_stage5ag_generated_and_raw_paths_are_ignored() -> None:
    assert _ignored("experiments/results/source-harvester-local/stage5ag/full_file_inventory.jsonl")
    assert _ignored("experiments/results/source-harvester-local/stage5ag/full_hash_inventory.jsonl")
    assert _ignored("experiments/results/source-harvester-local/stage5ag/summary.json")
    assert _ignored("third_party/stage5ag-raw-test-image.png")
    assert _ignored("third_party/DiskCipherStuff/DiskCipherStuff.zip")
    assert _ignored("source-harvester-output/example.txt")
    assert _ignored("harvest-output/example.txt")
    assert _ignored("research-inputs/example.txt")
    assert _ignored("codex-output/stage5ag-codex-completion.md")
