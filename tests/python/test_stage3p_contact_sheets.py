from __future__ import annotations

from pathlib import Path

from PIL import Image

from libreprimus.image_transforms.components_overlay import component_overlay_images
from libreprimus.image_transforms.contact_sheets import create_contact_sheet


def test_component_overlay_produces_review_output() -> None:
    image = Image.new("L", (8, 8), 255)
    for x in range(2):
        for y in range(2):
            image.putpixel((x, y), 0)

    overlays = component_overlay_images(image)

    assert {name for name, _, _, _ in overlays} == {
        "component_overlay_64",
        "component_overlay_128",
        "component_overlay_192",
    }
    assert overlays[0][2].mode == "RGB"
    assert overlays[0][3]["largest_component_area_ratio"] > 0


def test_contact_sheet_generated(tmp_path: Path) -> None:
    transform_path = tmp_path / "threshold_128.png"
    Image.new("L", (8, 8), 0).save(transform_path)

    record = create_contact_sheet(
        image_id="synthetic",
        transform_outputs={"threshold_128": transform_path},
        out_path=tmp_path / "contact.jpg",
        generated_at="2026-05-18T00:00:00Z",
    )

    assert (tmp_path / "contact.jpg").is_file()
    assert record["thumbnail_count"] == 1
    assert record["trusted_as_canonical"] is False
    assert record["solve_claim"] is False
