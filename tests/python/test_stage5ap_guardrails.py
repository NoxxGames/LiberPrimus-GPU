from __future__ import annotations

from libreprimus.stego_controls.outguess_controls import build_guardrail


def test_stage5ap_outguess_guardrail_blocks_lp_page_execution(tmp_path) -> None:
    record = build_guardrail(out=tmp_path / "guardrail.yaml")
    assert record["guardrail_status"] == "active"
    assert record["lp_page_outguess_run_performed"] is False
    assert record["outguess_tool_executed"] is False
    assert record["solve_claim"] is False
