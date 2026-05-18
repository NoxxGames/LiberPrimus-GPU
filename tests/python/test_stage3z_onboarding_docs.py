from __future__ import annotations

from libreprimus.paths import repo_root

ONBOARDING_DOCS = (
    "README.md",
    "start-here.md",
    "source-of-truth-map.md",
    "codex-navigation-map.md",
    "deep-research-handoff-map.md",
    "contributor-module-map.md",
    "newcomer-task-lanes.md",
    "private-generated-data-map.md",
)


def test_stage3z_all_onboarding_docs_exist() -> None:
    root = repo_root() / "docs/onboarding"

    for name in ONBOARDING_DOCS:
        assert (root / name).is_file(), name


def test_stage3z_start_here_links_source_of_truth_map() -> None:
    text = _read_onboarding("start-here.md").lower()

    assert "source-of-truth-map.md" in text


def test_stage3z_source_of_truth_map_links_staged_plan() -> None:
    text = _read_onboarding("source-of-truth-map.md").lower()

    assert "docs/roadmap/staged-plan.md" in text


def test_stage3z_codex_navigation_mentions_core_docs() -> None:
    text = _read_onboarding("codex-navigation-map.md").lower()

    for term in ("agents.md", "status.md", "roadmap.md", "docs/roadmap/staged-plan.md"):
        assert term in text


def test_stage3z_deep_research_handoff_mentions_repo_and_redacted_bundles() -> None:
    text = _read_onboarding("deep-research-handoff-map.md").lower()

    assert "https://github.com/noxxgames/liberprimus-gpu" in text
    assert "redacted" in text
    assert "stage 4a" in text


def test_stage3z_contributor_module_map_lists_key_areas() -> None:
    text = _read_onboarding("contributor-module-map.md").lower()

    for term in ("cli", "scoring", "discord", "image", "stego", "research synthesis"):
        assert term in text


def test_stage3z_private_generated_data_map_lists_core_paths() -> None:
    text = _read_onboarding("private-generated-data-map.md").lower()

    assert "discord" in text
    assert "page images" in text
    assert "experiments/results" in text


def _read_onboarding(name: str) -> str:
    return (repo_root() / "docs/onboarding" / name).read_text(encoding="utf-8")
