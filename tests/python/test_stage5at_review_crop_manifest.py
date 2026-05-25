from pathlib import Path

import yaml


def test_stage5at_crop_manifest_marks_derived_review_images() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5at-case-review-crop-manifest.yaml").read_text())
    assert payload["crop_count"] == 1015
    assert payload["context_crop_count"] == 609
    assert payload["derived_review_images_not_source_truth"] is True
    assert payload["generated_crops_committed"] is False
    assert all(record["generated_from_original_image"] is True for record in payload["records"][:20])
    assert all(record["derived_review_image_not_source"] is True for record in payload["records"][:20])
