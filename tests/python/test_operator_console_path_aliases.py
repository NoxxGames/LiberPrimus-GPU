from __future__ import annotations

from pathlib import Path

import libreprimus.operator_console.source_browser.path_aliases as path_aliases_module
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


def test_archive_relative_image_path_resolution(monkeypatch, tmp_path) -> None:
    archive_root = tmp_path / "third_party" / "CicadaSolversIddqd"
    image_path = archive_root / "2014" / "additional images" / "example.jpg"
    image_path.parent.mkdir(parents=True)
    image_path.write_bytes(b"fixture")

    monkeypatch.setattr(path_aliases_module, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        path_aliases_module,
        "ARCHIVE_RELATIVE_ROOTS",
        (Path("third_party/CicadaSolversIddqd"),),
    )

    resolved = resolve_with_aliases("2014/additional images/example.jpg", [])

    assert resolved == image_path
