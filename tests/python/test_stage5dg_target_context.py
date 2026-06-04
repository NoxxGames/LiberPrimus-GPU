from __future__ import annotations

from libreprimus.token_block.stage5dg import validate_stage5dg_target_context

from test_stage5dg_common import ensure_stage5dg_built, load_yaml


def test_stage5dg_target_context_is_preserved_not_validated() -> None:
    ensure_stage5dg_built()
    counts, errors = validate_stage5dg_target_context()

    assert errors == []
    assert counts["target_class_count"] == 10
    assert counts["target_class_validation_implemented"] is False
    assert counts["tor_network_access_performed"] is False

    payload = load_yaml("data/token-block/stage5dg-target-class-context-preservation.yaml")
    assert payload["target_class_context_preserved_for_future_design_only"] is True
    assert payload["byte_stream_generation_authorized_now"] is False
