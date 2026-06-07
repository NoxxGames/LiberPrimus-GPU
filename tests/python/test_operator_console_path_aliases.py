from __future__ import annotations

from pathlib import Path

from libreprimus.operator_console.source_browser.path_aliases import PathAlias, load_path_aliases, resolve_with_aliases


def test_default_path_aliases_load() -> None:
    aliases = load_path_aliases()

    assert any(alias.source_prefix == "third_party" for alias in aliases)
    assert any(alias.source_prefix == "data" for alias in aliases)


def test_path_alias_resolution_returns_repo_relative_candidate(tmp_path) -> None:
    target = resolve_with_aliases(
        "alias-root/example.txt",
        [PathAlias(source_prefix="alias-root", target_prefix=tmp_path.as_posix())],
    )

    assert target == Path(tmp_path) / "example.txt"
