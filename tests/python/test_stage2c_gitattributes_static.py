from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
GITATTRIBUTES = REPO / ".gitattributes"


def _lines() -> list[str]:
    return GITATTRIBUTES.read_text(encoding="utf-8").splitlines()


def test_gitattributes_exists_and_is_multiline() -> None:
    assert GITATTRIBUTES.is_file()
    lines = _lines()
    assert len(lines) > 10
    assert lines[0] != "* text=auto .gitattributes text eol=lf"


def test_gitattributes_is_not_flattened() -> None:
    assert not any("* text=auto .gitattributes" in line for line in _lines())


def test_gitattributes_has_required_text_rules() -> None:
    lines = set(_lines())
    assert "*.json text eol=lf" in lines
    assert "*.sha256 text eol=lf" in lines
    assert "*.yml text eol=lf" in lines
    assert "*.sh text eol=lf" in lines


def test_gitattributes_has_required_binary_rules() -> None:
    lines = set(_lines())
    for pattern in ["*.jpg binary", "*.png binary", "*.pdf binary", "*.xlsx binary", "*.sqlite binary", "*.db binary"]:
        assert pattern in lines
