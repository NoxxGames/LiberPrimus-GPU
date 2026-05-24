from __future__ import annotations

import subprocess


def test_stage5aj_raw_and_generated_paths_are_ignored() -> None:
    paths = [
        "third_party/UsefulFilesAndIdeas/LP Excel.xlsx",
        "experiments/results/source-harvester-usefulfiles/stage5aj/xlsx_cell_metadata_index.jsonl",
        "experiments/results/source-harvester-usefulfiles/stage5aj/important_links_url_index.json",
        "research-inputs/stage5aj/master_manifest.yaml",
        "research-inputs/stage5aj/source_cards.jsonl",
        "codex-output/stage5aj-codex-completion.md",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
