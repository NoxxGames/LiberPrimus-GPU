from __future__ import annotations

from pathlib import Path

from libreprimus.paths import repo_root
from libreprimus.website_render.loader import load_stage5al_inputs
from libreprimus.website_render.models import REQUIRED_DATA_FILES, REQUIRED_PAGES
from libreprimus.website_render.privacy import audit_site
from libreprimus.website_render.renderer import render_site


def test_static_renderer_consumes_stage5al_metadata(tmp_path: Path) -> None:
    inputs = load_stage5al_inputs(
        repo_root() / "data/website-ingest/stage5al",
        repo_root() / "data/source-harvester/stage5al-summary.yaml",
    )
    assert inputs["stage5al_summary"]["source_card_count"] == 61
    assert len(inputs["datasets"]["research-bundles"]["records"]) == 10

    out_root = tmp_path / "research-index"
    manifest = render_site(inputs, out_root, create_zip=False)
    assert manifest["static_pages_generated"] == len(REQUIRED_PAGES)
    assert manifest["data_json_files_generated"] == len(REQUIRED_DATA_FILES)
    for rel in [*REQUIRED_PAGES, *REQUIRED_DATA_FILES, "assets/site.css", "assets/site.js", "robots.txt"]:
        assert (out_root / rel).exists(), rel


def test_static_renderer_uses_no_external_dependencies(tmp_path: Path) -> None:
    inputs = load_stage5al_inputs(
        repo_root() / "data/website-ingest/stage5al",
        repo_root() / "data/source-harvester/stage5al-summary.yaml",
    )
    out_root = tmp_path / "research-index"
    render_site(inputs, out_root, create_zip=False)
    for html in out_root.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        assert 'src="http' not in text
        assert 'href="http' not in text
        assert '<meta name="robots" content="noindex,nofollow,noarchive">' in text
    assert "Disallow: /" in (out_root / "robots.txt").read_text(encoding="utf-8")
    assert audit_site(out_root)["privacy_audit_passed"] is True
