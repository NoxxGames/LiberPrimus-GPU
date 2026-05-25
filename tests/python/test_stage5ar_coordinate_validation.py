from __future__ import annotations

from pathlib import Path

import yaml


def _yaml(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_stage5ar_coordinate_validation_passes_with_review_required_status() -> None:
    validation = _yaml("data/token-block/stage5ar-token-coordinate-validation.yaml")
    assert validation["coordinate_validation_status"] == "valid_with_review_required"
    assert validation["validation_error_count"] == 0
    assert validation["token_coordinate_record_count"] == 256
    assert validation["forbidden_image_reference_count"] == 0
