from __future__ import annotations

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
    (discord_dir / "CicadaSolvers - Cicada - followup [123456789012345678].html").write_text(
        """
<div class="chatlog__message" data-message-id="123456789012345678" data-user-id="999999999999999999">
<span class="chatlog__author-name">PrivateUser</span>
<div class="chatlog__content">Cuneiform base60 and OutGuess https://example.org/source</div>
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
            "--emit-noindex",
            "--emit-robots",
            "--emit-site-manifest",
            "--allow-warnings",
        ],
    )
    assert result.exit_code == 0, result.output
    return out_dir


def test_stage4a_followup_privacy_files_generated(tmp_path: Path) -> None:
    out_dir = build_synthetic_site(tmp_path)
    site = out_dir / "site"

    assert '<meta name="robots" content="noindex,nofollow,noarchive">' in (site / "index.html").read_text(encoding="utf-8")
    assert (site / "robots.txt").read_text(encoding="utf-8") == "User-agent: *\nDisallow: /\n"
    assert "redacted research review site" in (site / "SITE_PRIVACY_NOTICE.md").read_text(encoding="utf-8").lower()
    assert "Upload only" in (site / "SFTP_UPLOAD_CHECKLIST.md").read_text(encoding="utf-8")
    assert "X-Robots-Tag" in (site / ".htaccess.example").read_text(encoding="utf-8")


def test_stage4a_followup_validate_fails_without_noindex(tmp_path: Path) -> None:
    out_dir = build_synthetic_site(tmp_path)
    index = out_dir / "site" / "index.html"
    index.write_text(
        index.read_text(encoding="utf-8").replace('<meta name="robots" content="noindex,nofollow,noarchive">', ""),
        encoding="utf-8",
    )

    result = CliRunner().invoke(app, ["discord-full-review", "validate", "--results-dir", str(out_dir)])

    assert result.exit_code == 1
    assert "noindex_meta_missing" in result.output


def test_stage4a_followup_validate_accepts_privacy_hardened_site(tmp_path: Path) -> None:
    out_dir = build_synthetic_site(tmp_path)
    result = CliRunner().invoke(app, ["discord-full-review", "validate", "--results-dir", str(out_dir)])

    assert result.exit_code == 0, result.output
    assert "discord_full_review_valid=true" in result.output
