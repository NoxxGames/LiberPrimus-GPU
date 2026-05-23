from __future__ import annotations

from pathlib import Path

from PIL import Image

from libreprimus.source_harvester.extractors import extract_html_file, image_metadata


def test_stage5af_static_html_extraction_strips_navigation(tmp_path: Path) -> None:
    html = tmp_path / "fixture.html"
    html.write_text(
        """
        <html><body>
        <nav>skip navigation</nav>
        <main><h1>Liber Primus</h1><p>Main article text.</p>
        <a href="https://example.org/source">source</a><img src="page.png"></main>
        </body></html>
        """,
        encoding="utf-8",
    )
    record = extract_html_file(html, source_id="fixture")
    assert "Main article text." in record["main_text"]
    assert "skip navigation" not in record["main_text"]
    assert record["links"] == ["https://example.org/source"]
    assert record["image_links"] == ["page.png"]


def test_stage5af_image_metadata_records_dimensions_and_hash(tmp_path: Path) -> None:
    image = tmp_path / "fixture.png"
    Image.new("RGB", (3, 5), "white").save(image)
    record = image_metadata(image, source_id="fixture")
    assert record["width"] == 3
    assert record["height"] == 5
    assert len(record["sha256"]) == 64
    assert record["image_interpretation_performed"] is False
