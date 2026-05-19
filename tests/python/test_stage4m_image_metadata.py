from __future__ import annotations

from PIL import Image

from libreprimus.image_preflight.metadata import build_metadata_records


def test_stage4m_synthetic_image_metadata_deterministic(tmp_path) -> None:
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    image_path = image_dir / "sample.png"
    Image.new("RGB", (5, 7), (10, 20, 30)).save(image_path)

    first = build_metadata_records(image_dir, repo_root=tmp_path)
    second = build_metadata_records(image_dir, repo_root=tmp_path)

    assert first == second
    assert first[0]["width"] == 5
    assert first[0]["height"] == 7
    assert first[0]["image_format"] == "PNG"
    assert first[0]["raw_image_committed"] is False
