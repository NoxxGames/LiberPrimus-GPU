from __future__ import annotations

from pathlib import Path

from PIL import Image

from libreprimus.source_harvester.community_attachments import build_community_attachment_index


def _image(path: Path) -> None:
    Image.new("RGB", (3, 2), "white").save(path, format="PNG")


def test_stage5ak_attachment_index_uses_numeric_filename_order(tmp_path: Path) -> None:
    source_root = tmp_path / "community-facts"
    source_root.mkdir()
    for name in ["10.webp", "2.webp", "1.webp"]:
        _image(source_root / name)

    result = build_community_attachment_index(
        source_root=source_root,
        results_dir=tmp_path / "results",
        out=tmp_path / "attachments.yaml",
    )

    assert result["attachment_order"] == ["1.webp", "2.webp", "10.webp"]
    assert [record["numeric_filename_order"] for record in result["records"]] == [1, 2, 10]
    assert all(record["raw_image_committed"] is False for record in result["records"])
    assert all(record["ocr_performed"] is False for record in result["records"])
    assert all(record["website_publication_allowed"] is False for record in result["records"])
