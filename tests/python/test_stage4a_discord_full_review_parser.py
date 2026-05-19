from __future__ import annotations

from pathlib import Path

from libreprimus.discord_full_review.html_parser import channel_id_for_file, parse_discord_html_file


def test_stage4a_parser_handles_synthetic_discord_html(tmp_path: Path) -> None:
    html = tmp_path / "CicadaSolvers - Cicada - test [123456789012345678].html"
    html.write_text(
        """
<div class="chatlog__message" data-message-id="123456789012345678" data-user-id="999999999999999999">
<span class="chatlog__author-name">PrivateUser</span>
<span class="chatlog__timestamp" title="2020-01-01">2020-01-01</span>
<div class="chatlog__content">Cuneiform base60 and Onion 7 https://example.org/source <@123456789012345678></div>
<img src="https://cdn.discordapp.com/attachments/123/456/page.png?secret=yes">
</div>
""",
        encoding="utf-8",
    )

    records = parse_discord_html_file(html, channel_id=channel_id_for_file(html), channel_name="test")

    assert len(records) == 1
    assert "PrivateUser" not in records[0]["redacted_text"]
    assert "[redacted-user]" in records[0]["redacted_text"]
    assert records[0]["public_links"] == ["https://example.org/source"]
    assert records[0]["image_refs"][0]["private_url_committed"] is False
