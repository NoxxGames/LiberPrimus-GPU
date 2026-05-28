from test_stage5bk_common import load_yaml


def test_stage5bk_positive_control_context_keeps_media_blocked() -> None:
    payload = load_yaml("data/historical-route/stage5bk-iddqd-v2-positive-control-context.yaml")
    assert payload["positive_control_context_count"] == 11
    assert payload["positive_control_only_count"] >= 8
    assert payload["outguess_execution_performed"] is False
    assert payload["openpuff_execution_performed"] is False
    assert payload["mp3stego_execution_performed"] is False
    image_4gq25 = next(record for record in payload["records"] if record["context_id"].endswith("image_4gq25"))
    assert image_4gq25["readiness_state"] == "source_locked_metadata_only"
    assert image_4gq25["execution_allowed"] is False
    font = next(record for record in payload["records"] if record["context_id"].endswith("babelstone_font"))
    assert font["font_committed"] is False
    assert font["font_shared"] is False
