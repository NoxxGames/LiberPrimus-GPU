from __future__ import annotations

from pathlib import Path

from PIL import Image

from libreprimus.discord_full_review.lp_page_gallery import build_lp_page_gallery


def test_stage4a_lp_page_gallery_generates_thumbnails(tmp_path: Path) -> None:
    pages = tmp_path / "pages"
    out = tmp_path / "out"
    site = out / "site"
    pages.mkdir()
    Image.new("RGB", (80, 60), "white").save(pages / "page001.jpg")

    records = build_lp_page_gallery(lp_pages_dir=pages, out_dir=out, site_dir=site)

    assert len(records) == 1
    assert (site / "lp-pages" / "index.html").is_file()
    assert (site / "lp-pages" / "thumbnails" / "lp-page-001.jpg").is_file()
    assert records[0]["raw_source_committed"] is False
    assert records[0]["generated_copy_committed"] is False
