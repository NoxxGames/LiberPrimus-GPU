from test_stage5bn_common import load_yaml


def test_stage5bn_human_review_pack_not_generated_when_spreadsheet_closes_gap() -> None:
    payload = load_yaml("data/token-block/stage5bn-human-review-pack-manifest.yaml")

    assert payload["human_review_status"] == "not_needed_gap_closed"
    assert payload["review_pack_root"] == "human-review-packs/stage5bn/string4-unsupported-position"
    assert payload["review_pack_generated"] is False
    assert payload["review_pack_files"] == []
    assert payload["candidate_options_presented"] == ["0I", "0l", "0j", "OI", "Oj"]
    assert payload["review_template_committed"] is False
    assert payload["generated_crops_committed"] is False
    assert payload["raw_images_committed"] is False
