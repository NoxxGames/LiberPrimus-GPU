from pathlib import Path

import yaml


def test_stage5au_review_pack_v2_manifest_records_full_pack() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5au-review-pack-v2-manifest.yaml").read_text())
    assert payload["review_pack_v2_generated"] is True
    assert payload["review_pack_v2_root"] == "human-review-packs/stage5au/token-case-review-v2"
    assert payload["case_challenge_count"] == 203
    assert payload["canonical_challenge_count"] == 212
    assert payload["generated_crop_count"] == 2436
    assert payload["generated_review_pack_committed"] is False
    assert payload["derived_review_images_not_source_truth"] is True
