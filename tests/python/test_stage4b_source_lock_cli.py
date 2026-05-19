from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage4b_cli_run_and_validate_on_synthetic_stage4a_indexes(tmp_path: Path) -> None:
    stage4a = tmp_path / "stage4a"
    indexes = stage4a / "indexes"
    out_dir = tmp_path / "generated"
    records = tmp_path / "records"
    manifests = tmp_path / "manifests"
    indexes.mkdir(parents=True)
    records.mkdir()
    (indexes / "public_link_index.jsonl").write_text(
        "\n".join(
            json.dumps(record)
            for record in [
                {"index_id": "one", "value": "https://github.com/rtkd/iddqd?utm_source=x"},
                {"index_id": "two", "value": "https://github.com/rtkd/iddqd/"},
                {"index_id": "bad", "value": "https://cdn.discordapp.com/attachments/1/2/file.png?token=x"},
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    run_result = CliRunner().invoke(
        app,
        [
            "source-lock-triage",
            "run",
            "--stage4a-dir",
            str(stage4a),
            "--out-dir",
            str(out_dir),
            "--promoted-sources-out",
            str(records / "promoted.yaml"),
            "--source-health-out",
            str(records / "health.yaml"),
            "--visual-observations-out",
            str(records / "visual.yaml"),
            "--negative-controls-out",
            str(records / "negative.yaml"),
            "--cookie-source-records-out",
            str(records / "cookies.yaml"),
            "--manifest-out-dir",
            str(manifests),
            "--allow-warnings",
        ],
    )
    assert run_result.exit_code == 0, run_result.output
    assert "promoted_source_count=20" in run_result.output
    assert (out_dir / "source_triage_report.json").is_file()

    validate_result = CliRunner().invoke(
        app,
        [
            "source-lock-triage",
            "validate",
            "--promoted-sources",
            str(records / "promoted.yaml"),
            "--source-health",
            str(records / "health.yaml"),
            "--visual-observations",
            str(records / "visual.yaml"),
            "--negative-controls",
            str(records / "negative.yaml"),
            "--cookie-source-records",
            str(records / "cookies.yaml"),
            "--manifest-dir",
            str(manifests),
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert "source_lock_triage_valid=true" in validate_result.output
