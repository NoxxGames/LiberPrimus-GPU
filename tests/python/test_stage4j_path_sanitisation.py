from __future__ import annotations

from pathlib import Path

from libreprimus.observation_review.path_sanitisation import find_absolute_local_paths


def test_stage4j_path_checker_rejects_windows_absolute_path(tmp_path: Path) -> None:
    record = tmp_path / "record.yaml"
    record.write_text("output_path: O:\\Programming\\LiberPrimusSolver\\output.json\n", encoding="utf-8")
    findings = find_absolute_local_paths(tmp_path, paths=[record])
    assert findings
    assert findings[0].kind == "absolute_local_path"


def test_stage4j_path_checker_rejects_posix_home_path(tmp_path: Path) -> None:
    record = tmp_path / "record.yaml"
    record.write_text("output_path: /home/user/liberprimus/output.json\n", encoding="utf-8")
    findings = find_absolute_local_paths(tmp_path, paths=[record])
    assert findings


def test_stage4j_path_checker_allows_marked_example_path(tmp_path: Path) -> None:
    record = tmp_path / "doc.md"
    record.write_text(
        "# example_path:\n```powershell\ncd O:\\Programming\\Example\n```\n",
        encoding="utf-8",
    )
    assert find_absolute_local_paths(tmp_path, paths=[record]) == []
