from __future__ import annotations

from libreprimus.stego_controls.outguess_toolchain import detect_outguess_toolchain


def test_stage5ap_outguess_toolchain_detection_does_not_execute_tool(tmp_path) -> None:
    record = detect_outguess_toolchain(out=tmp_path / "toolchain.yaml")
    assert record["toolchain_state"] in {"outguess_missing", "outguess_available_unverified"}
    assert record["tool_executed"] is False
    assert record["extraction_executed"] is False
    assert record["lp_page_outguess_run_performed"] is False
