from __future__ import annotations

import json
from pathlib import Path

from libreprimus.discord_ingestion.export import read_jsonl
from libreprimus.discord_ingestion.html_scanner import scan_discord_archive


def test_discord_html_scanner_records_file_lock_and_candidates(tmp_path: Path) -> None:
    source = tmp_path / "discord"
    source.mkdir()
    html = source / "chat.html"
    html.write_text(
        """
        <html><body>
        <a href="https://github.com/cicada-solvers/example?utm_source=test">link</a>
        <img src="https://cdn.discordapp.com/attachments/1/2/file.png?ex=secret&is=token">
        Prime p56 totient tried and failed near 3301 and 1033.
        Plain https://pastebin.com/abc123
        </body></html>
        """,
        encoding="utf-8",
    )

    summary = scan_discord_archive(
        source_dir=source,
        out_dir=tmp_path / "out",
        allow_missing=False,
        allow_warnings=True,
    )

    assert summary["html_file_count"] == 1
    assert summary["link_count"] >= 3
    assert summary["method_claim_candidate_count"] >= 1
    assert summary["numeric_observation_candidate_count"] >= 1
    locks = read_jsonl(tmp_path / "out/discord_html_file_locks.jsonl")
    assert locks[0]["file_size_bytes"] == html.stat().st_size
    assert len(locks[0]["sha256"]) == 64


def test_discord_html_scanner_handles_missing_with_allow_missing(tmp_path: Path) -> None:
    summary = scan_discord_archive(
        source_dir=tmp_path / "missing",
        out_dir=tmp_path / "out",
        allow_missing=True,
        allow_warnings=True,
    )

    assert summary["html_file_count"] == 0
    assert json.loads((tmp_path / "out/discord_ingestion_summary.json").read_text())["link_count"] == 0
