from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
REQUIRED_TUTORIALS = [
    "01-project-overview.md",
    "02-windows-setup.md",
    "03-linux-setup.md",
    "04-repo-tour.md",
    "05-local-data-policy.md",
    "06-running-tests-and-ci.md",
    "07-solved-baselines.md",
    "08-bounded-experiment-queues.md",
    "09-generated-output-policy.md",
    "10-image-analysis-workflow.md",
    "11-discord-archive-ingestion.md",
    "12-source-observation-registry.md",
    "13-github-wiki-mirror.md",
    "14-codex-assisted-development.md",
    "15-troubleshooting.md",
]


def test_stage3o_readme_links_tutorials_and_wiki() -> None:
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert "tutorials/README.md" in readme
    assert "tutorials/02-windows-setup.md" in readme
    assert "tutorials/03-linux-setup.md" in readme
    assert "docs/wiki-source/" in readme
    assert "Stage 3O" in readme


def test_stage3o_tutorial_index_lists_required_files() -> None:
    tutorial_index = (REPO / "tutorials/README.md").read_text(encoding="utf-8")
    for tutorial in REQUIRED_TUTORIALS:
        assert (REPO / "tutorials" / tutorial).is_file()
        assert tutorial in tutorial_index
