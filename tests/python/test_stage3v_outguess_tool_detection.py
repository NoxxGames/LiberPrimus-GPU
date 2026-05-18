from __future__ import annotations

from pathlib import Path

from libreprimus.stego.outguess_tool import detect_outguess


def test_stage3v_missing_tool_detection_returns_recordable_state(tmp_path: Path) -> None:
    tool = detect_outguess(tmp_path / "missing-outguess")

    assert tool.available is False
    assert tool.path is None
    assert tool.help_output_sha256 is None
