from __future__ import annotations

from libreprimus.token_block.dwh_context import build_dwh_context


def test_stage5ap_dwh_context_is_review_only(tmp_path) -> None:
    record = build_dwh_context(out=tmp_path / "dwh.yaml")
    assert record["context_status"] == "review_only_external_deep_research_context"
    assert record["execution_enabled"] is False
    assert record["hash_preimage_search_performed"] is False
    assert record["decode_attempted"] is False
