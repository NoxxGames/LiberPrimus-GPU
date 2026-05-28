from test_stage5bn_common import load_yaml


def test_stage5bn_coordinate_context_uses_source_locked_metadata_without_interpretation() -> None:
    payload = load_yaml("data/token-block/stage5bn-target-position-coordinate-context.yaml")

    assert payload["target_token_index_0_based"] == 199
    assert payload["coordinate_record_found"] is True
    assert payload["logical_coordinate"] == "r25c08"
    assert payload["page_identifier"] == "page_51"
    assert payload["image_interpretation_performed"] is False
    assert payload["ocr_performed"] is False
    assert payload["llm_vision_token_reading_performed"] is False
    assert payload["raw_image_committed"] is False
    assert payload["generated_crop_committed"] is False
