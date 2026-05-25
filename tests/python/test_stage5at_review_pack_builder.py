from pathlib import Path

import yaml


def test_stage5at_review_pack_manifest_records_generated_pack() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5at-case-review-pack-manifest.yaml").read_text())
    assert payload["review_pack_generated"] is True
    assert payload["review_pack_zip_created"] is True
    assert payload["review_pack_root"] == "human-review-packs/stage5at/token-case-review"
    assert payload["generated_review_sheet_count"] == 9
    assert payload["generated_review_pack_committed"] is False
    assert payload["derived_review_images_not_source_truth"] is True
