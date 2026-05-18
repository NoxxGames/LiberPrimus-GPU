from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.discord_ingestion.html_scanner import scan_discord_archive
from libreprimus.discord_ingestion.validation import export_aggregate_records


def test_committed_aggregate_records_contain_no_message_bodies_or_usernames(tmp_path: Path) -> None:
    source = tmp_path / "discord"
    source.mkdir()
    (source / "chat.html").write_text(
        '<a href="https://cdn.discordapp.com/attachments/1/2/a.png?token=secret">x</a>'
        "Vigenere and prime 3301 were discussed.",
        encoding="utf-8",
    )
    out = tmp_path / "out"
    scan_discord_archive(source_dir=source, out_dir=out, allow_warnings=True)
    archive_path = tmp_path / "archive.yaml"
    observation_path = tmp_path / "observation.yaml"

    export_aggregate_records(
        results_dir=out,
        archive_out=archive_path,
        observation_out=observation_path,
    )

    archive = yaml.safe_load(archive_path.read_text(encoding="utf-8"))
    observation = yaml.safe_load(observation_path.read_text(encoding="utf-8"))
    for record in [archive, observation]:
        assert record["raw_logs_committed"] is False
        assert record["message_bodies_committed"] is False
        assert record["usernames_committed"] is False
        assert record["live_api_used"] is False
        assert record["scrape_used"] is False
    committed_text = archive_path.read_text(encoding="utf-8") + observation_path.read_text(encoding="utf-8")
    assert "cdn.discordapp.com/attachments" not in committed_text
    assert "Vigenere and prime" not in committed_text
