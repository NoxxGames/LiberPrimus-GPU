from __future__ import annotations

from pathlib import Path

from PIL import Image
from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage4a_cli_build_generates_site_and_manifest(tmp_path: Path) -> None:
    discord_dir = tmp_path / "discord"
    pages_dir = tmp_path / "pages"
    out_dir = tmp_path / "out"
    discord_dir.mkdir()
    pages_dir.mkdir()
    (discord_dir / "CicadaSolvers - Cicada - test [123456789012345678].html").write_text(
        """
<div class="chatlog__message"><span class="chatlog__author-name">User</span>
<div class="chatlog__content">OutGuess audio and cuneiform base60 https://example.org/source</div>
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
            "--privacy-mode",
            "redacted_public",
            "--include-lp-page-gallery",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert (out_dir / "site" / "index.html").is_file()
    assert (out_dir / "deep_research_bundle_manifest.yaml").is_file()
    assert (out_dir / "SFTP_UPLOAD_INSTRUCTIONS.md").is_file()
    assert (out_dir / "site" / "topics" / "cuneiform-base60.html").is_file()
    assert (out_dir / "site" / "indexes" / "public-links.html").is_file()


def test_stage4a_cli_validate_accepts_synthetic_build(tmp_path: Path) -> None:
    test_stage4a_cli_build_generates_site_and_manifest(tmp_path)
    result = CliRunner().invoke(app, ["discord-full-review", "validate", "--results-dir", str(tmp_path / "out")])

    assert result.exit_code == 0, result.output
    assert "discord_full_review_valid=true" in result.output
