"""Small helpers for documenting solved-reference text blocks."""

from __future__ import annotations

from pathlib import Path


def find_reference_lines(path: Path, marker: str, *, context_lines: int = 8) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if marker.lower() in line.lower():
            return lines[index : index + context_lines]
    return []
