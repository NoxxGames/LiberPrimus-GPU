"""ChatGPT context-file helpers for the Operator Console."""

from __future__ import annotations

from pathlib import Path

from ..settings import CONTEXT_FILE, HUGE_TEXT_CHAR_LIMIT, HUGE_TEXT_LINE_LIMIT

CONTEXT_TEMPLATE = """# ChatGPT Context File

## Project Facts

- Liber Primus Operator Console can display this file as operator-maintained context.

## Stage Status

- Add concise current-stage facts here.
"""


def context_file_status(path: Path = CONTEXT_FILE) -> dict[str, object]:
    exists = path.exists()
    text = path.read_text(encoding="utf-8") if exists else ""
    return {
        "path": path.as_posix(),
        "exists": exists,
        "char_count": len(text),
        "line_count": len(text.splitlines()),
        "huge_raw_blob_suspected": has_huge_raw_blob(text),
    }


def create_context_file_if_missing(path: Path = CONTEXT_FILE) -> bool:
    if path.exists():
        return False
    path.write_text(CONTEXT_TEMPLATE, encoding="utf-8")
    return True


def has_huge_raw_blob(text: str) -> bool:
    return len(text) > HUGE_TEXT_CHAR_LIMIT or len(text.splitlines()) > HUGE_TEXT_LINE_LIMIT
