from pathlib import Path

import jsonschema
import yaml


def test_stage5au_crop_geometry_policy_schema_and_parameters() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5au-crop-geometry-policy.yaml").read_text())
    schema = yaml.safe_load(Path("schemas/token-block/crop-geometry-policy-v0.schema.json").read_text())
    jsonschema.Draft202012Validator(schema).validate(payload)
    assert payload["source_original_images_only"] is True
    assert payload["parameters"]["dark_pixel_threshold"] == 180
    assert payload["parameters"]["min_component_area_px"] == 8
    assert len(payload["crop_types"]) == 12
    assert payload["automatic_case_resolution_performed"] is False
