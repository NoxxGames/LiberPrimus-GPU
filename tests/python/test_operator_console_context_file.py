from __future__ import annotations

from libreprimus.operator_console.source_browser.context_file import (
    create_context_file_if_missing,
    context_file_status,
    has_huge_raw_blob,
)


def test_context_file_status_and_create_are_explicit(tmp_path) -> None:
    path = tmp_path / "ChatGPT-ContextFile.md"

    assert context_file_status(path)["exists"] is False
    assert create_context_file_if_missing(path) is True
    status = context_file_status(path)
    assert status["exists"] is True
    assert status["huge_raw_blob_suspected"] is False


def test_context_file_huge_blob_detection() -> None:
    assert has_huge_raw_blob("x" * 20001) is True
    assert has_huge_raw_blob("short context") is False
