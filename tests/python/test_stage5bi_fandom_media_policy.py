from test_stage5bi_fandom_page_triage import load_yaml


def test_stage5bi_fandom_media_policy_blocks_original_source_truth() -> None:
    payload = load_yaml("data/historical-route/stage5bi-fandom-media-non-original-policy.yaml")

    assert payload["default_media_status"] == "fandom_copy_reference_only"
    assert payload["fandom_images_are_original_source_truth"] is False
    assert payload["screenshots_are_original_source_truth"] is False
    assert payload["raw_images_committed"] is False
    assert payload["solve_claim"] is False
    assert "third_party/CicadaSolversIddqd" in payload["original_archive_preference"]
