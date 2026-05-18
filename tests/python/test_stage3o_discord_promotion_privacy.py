from __future__ import annotations

from pathlib import Path

from libreprimus.discord_promotion.validation import validate_promoted_records


REPO = Path(__file__).resolve().parents[2]
LINKS = REPO / "data/observations/discord/promoted-public-source-links-stage3o.yaml"
METHODS = REPO / "data/observations/discord/promoted-method-claim-candidates-stage3o.yaml"
NUMERICS = REPO / "data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml"


def test_stage3o_promoted_files_validate() -> None:
    counts, errors = validate_promoted_records(links=LINKS, methods=METHODS, numerics=NUMERICS)
    assert errors == []
    assert counts["links_count"] <= 500
    assert counts["methods_count"] <= 200
    assert counts["numerics_count"] <= 200


def test_stage3o_promoted_files_do_not_contain_private_context() -> None:
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in [LINKS, METHODS, NUMERICS])
    forbidden = [
        "message_body:",
        "raw_message:",
        "username:",
        "user_id:",
        "message_id:",
        "avatar:",
        "cdn.discordapp.com/attachments",
        "media.discordapp.net/attachments",
    ]
    for marker in forbidden:
        assert marker not in text
    assert "trusted_as_canonical: false" in text
    assert "raw_message_committed: false" in text
    assert "usernames_committed: false" in text
