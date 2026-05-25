from __future__ import annotations

from libreprimus.token_block.null_controls import build_null_control_plan


def test_stage5ap_null_control_plan_blocks_execution(tmp_path) -> None:
    record = build_null_control_plan(out=tmp_path / "nulls.yaml")
    assert record["null_control_count"] >= 5
    assert record["execution_enabled"] is False
    assert record["hash_preimage_search_enabled"] is False
    assert any(control["control_type"] == "alphabet_order_sensitivity" for control in record["records"])
