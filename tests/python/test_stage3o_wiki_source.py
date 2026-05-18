from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def _wiki_page_name(name: str) -> str:
    stem = Path(name).stem
    return " ".join(part if part.isdigit() else part.capitalize() for part in stem.split("-")) + ".md"


def test_stage3o_wiki_source_core_pages_exist() -> None:
    assert (REPO / "docs/wiki-source/Home.md").is_file()
    assert (REPO / "docs/wiki-source/_Sidebar.md").is_file()


def test_stage3o_each_tutorial_has_wiki_page() -> None:
    for tutorial in sorted((REPO / "tutorials").glob("*.md")):
        page = REPO / "docs/wiki-source" / _wiki_page_name(tutorial.name)
        assert page.is_file(), tutorial.name
        assert "repository tutorial file is the source of truth" in page.read_text(encoding="utf-8")
