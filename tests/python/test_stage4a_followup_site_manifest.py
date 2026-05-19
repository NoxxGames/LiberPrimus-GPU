from __future__ import annotations

import json
from pathlib import Path

from PIL import Image
from typer.testing import CliRunner

from libreprimus.cli import app


def build_synthetic_site(tmp_path: Path) -> Path:
    discord_dir = tmp_path / "discord"
    pages_dir = tmp_path / "pages"
    out_dir = tmp_path / "out"
    discord_dir.mkdir()
    pages_dir.mkdir()
    (discord_dir / "CicadaSolvers - Cicada - manifest [123456789012345678].html").write_text(
        """
<div class="chatlog__message"><div class="chatlog__content">OutGuess https://example.org/source</div>
<a href="https://example.org/source">source</a></div>
""",
        encoding="utf-8",
    )
    Image.new("RGB", (32, 32), "white").save(pages_dir / "page001.jpg")
    result = CliRunner().invoke(
        app,
        [
            "discord-full-review",
            "build",
            "--discord-dir",
            str(discord_dir),
            "--lp-pages-dir",
            str(pages_dir),
            "--out-dir",
            str(out_dir),
            "--include-lp-page-gallery",
            "--allow-warnings",
        ],
    )
    assert result.exit_code == 0, result.output
    return out_dir


def test_stage4a_followup_site_manifest_contains_counts_and_paths(tmp_path: Path) -> None:
    out_dir = build_synthetic_site(tmp_path)
    manifest = json.loads((out_dir / "site" / "site_manifest.json").read_text(encoding="utf-8"))

    assert manifest["record_type"] == "discord_full_review_site_manifest"
    assert manifest["privacy_mode"] == "redacted_public"
    assert manifest["noindex_enabled"] is True
    assert manifest["robots_disallow_all"] is True
    assert manifest["channel_count"] == 1
    assert manifest["channel_part_count"] == 1
    assert manifest["topic_count"] == 12
    assert manifest["public_link_count"] == 1
    assert manifest["lp_page_image_count"] == 1
    assert manifest["important_paths"]["root_index"] == "index.html"
    assert manifest["important_paths"]["privacy_notice"] == "SITE_PRIVACY_NOTICE.md"


def test_stage4a_followup_site_manifest_markdown_generated(tmp_path: Path) -> None:
    out_dir = build_synthetic_site(tmp_path)
    manifest_md = (out_dir / "site" / "site_manifest.md").read_text(encoding="utf-8")

    assert "Noindex enabled: `true`" in manifest_md
    assert "LP page gallery images: `1`" in manifest_md
