from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")


def test_discord_review_cli_builds_on_synthetic_fixture(tmp_path: Path) -> None:
    ingestion = tmp_path / "ingestion"
    _write_jsonl(
        ingestion / "discord_extracted_links.jsonl",
        [
            {
                "source_file_sha256": "a" * 64,
                "normalized_url": "https://github.com/example/repo",
                "domain": "github.com",
                "url_kind": "github",
            }
        ],
    )
    _write_jsonl(
        ingestion / "discord_method_claim_candidates.jsonl",
        [
            {
                "source_file_sha256": "a" * 64,
                "extracted_keywords": ["cuneiform", "base60"],
                "redacted_summary": "method keyword cluster: cuneiform/base60",
            }
        ],
    )
    _write_jsonl(
        ingestion / "discord_numeric_observation_candidates.jsonl",
        [
            {
                "source_file_sha256": "a" * 64,
                "numbers": [3301, 1033],
                "context_keywords": ["prime"],
                "redacted_summary": "numeric keyword cluster",
            }
        ],
    )
    _write_jsonl(
        ingestion / "discord_attachment_candidates.jsonl",
        [{"source_file_sha256": "a" * 64, "file_name": "image.png", "media_kind": "image"}],
    )
    (ingestion / "discord_ingestion_summary.json").write_text(
        json.dumps({"html_file_count": 1, "total_bytes": 100}),
        encoding="utf-8",
    )
    out_dir = tmp_path / "out"
    aggregate = tmp_path / "aggregate.yaml"

    result = CliRunner().invoke(
        app,
        [
            "discord-review",
            "build-bundles",
            "--ingestion-dir",
            str(ingestion),
            "--promotion-dir",
            str(tmp_path / "promotion"),
            "--raw-dir",
            str(tmp_path / "raw"),
            "--out-dir",
            str(out_dir),
            "--aggregate-out",
            str(aggregate),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "redacted_message_count=" in result.output
    assert (out_dir / "redacted_message_stream.jsonl").is_file()
    assert (out_dir / "review_index.html").is_file()
    assert aggregate.is_file()


def test_discord_review_cli_supports_allow_missing(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "discord-review",
            "build-bundles",
            "--ingestion-dir",
            str(tmp_path / "missing-ingestion"),
            "--promotion-dir",
            str(tmp_path / "missing-promotion"),
            "--raw-dir",
            str(tmp_path / "missing-raw"),
            "--out-dir",
            str(tmp_path / "out"),
            "--aggregate-out",
            str(tmp_path / "aggregate.yaml"),
            "--allow-missing",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "redacted_message_count=0" in result.output
