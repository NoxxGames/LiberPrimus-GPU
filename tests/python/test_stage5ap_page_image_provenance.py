from __future__ import annotations

from pathlib import Path

from PIL import Image

from libreprimus.token_block.provenance import build_source_lock


def test_stage5ap_page_image_provenance_hashes_local_metadata_only(tmp_path: Path) -> None:
    image_root = tmp_path / "pages"
    image_root.mkdir()
    for page in ("49", "50", "51"):
        Image.new("RGB", (3, 2), "white").save(image_root / f"{page}.jpg")
    source, provenance = build_source_lock(
        search_roots=[image_root],
        out_source_lock=tmp_path / "source.yaml",
        out_image_provenance=tmp_path / "provenance.yaml",
    )
    assert source["source_locked_page_image_count"] == 3
    assert provenance["page_image_record_count"] == 3
    assert all(record["raw_image_committed"] is False for record in provenance["records"])
    assert all(record["ocr_performed"] is False for record in provenance["records"])
