from __future__ import annotations

from test_stage5ei_common import stage5ei_data


def test_stage5ei_preserves_stage5eh_counts() -> None:
    payload = stage5ei_data("stage5eh_preservation")

    assert payload["previous_stage_id"] == "stage-5eh"
    assert payload["stage5eh_future_probe_manifest_count"] == 23
    assert payload["stage5eh_overlay_count"] == 36
    assert payload["stage5eh_source_browser_validation_error_count"] == 0
    assert payload["stage5eh_records_rewritten_now"] is False

