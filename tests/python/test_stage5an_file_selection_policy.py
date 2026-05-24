from __future__ import annotations

from pathlib import Path

from libreprimus.deep_research_export.file_selection import is_allowed_private_file, is_forbidden_raw_file, select_research_input_files


def test_research_input_fixtures_are_selected_by_policy(tmp_path: Path) -> None:
    root = tmp_path / "research"
    root.mkdir()
    (root / "context.md").write_text("ok", encoding="utf-8")
    (root / "table.csv").write_text("a,b\n", encoding="utf-8")
    (root / "image.png").write_bytes(b"png")
    selected, excluded = select_research_input_files([root])
    assert {Path(record["source_path"]).name for record in selected} == {"context.md", "table.csv"}
    assert any(record["reason"] == "forbidden_raw_or_binary_extension" for record in excluded)
    assert is_allowed_private_file(root / "context.md")
    assert is_forbidden_raw_file(root / "image.png")
