from __future__ import annotations

from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml"


def _synthetic_manifest(tmp_path: Path) -> Path:
    payload = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    payload["corpus_slice"] = {
        "slice_id": "synthetic-stage3s-cli",
        "corpus_candidate_id": "synthetic",
        "selector": {
            "index29_values": [0, 1, 2, 3],
            "token_records": [
                {"token_kind": "rune", "index29": 0, "token_index_global": 0, "line_index": 0},
                {"token_kind": "rune", "index29": 1, "token_index_global": 1, "line_index": 0},
                {"token_kind": "line_separator", "token_index_global": 2},
                {"token_kind": "rune", "index29": 2, "token_index_global": 3, "line_index": 1},
                {"token_kind": "rune", "index29": 3, "token_index_global": 4, "line_index": 1},
            ],
        },
    }
    path = tmp_path / "manifest.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def test_post_discord_cli_validate_manifest() -> None:
    result = CliRunner().invoke(app, ["post-discord", "validate-manifest", "--manifest", str(MANIFEST)])

    assert result.exit_code == 0, result.output
    assert "post_discord_manifest_valid=true" in result.output
    assert "expected_candidate_count=72" in result.output


def test_post_discord_cli_run_and_summary_on_synthetic_manifest(tmp_path: Path) -> None:
    manifest = _synthetic_manifest(tmp_path)
    out_dir = tmp_path / "stage3s"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "post-discord",
            "run-onion7-seed-pack",
            "--manifest",
            str(manifest),
            "--out-dir",
            str(out_dir),
            "--top-k",
            "5",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "executed_candidate_count=72" in result.output

    result = runner.invoke(app, ["post-discord", "summary", "--results-dir", str(out_dir)])
    assert result.exit_code == 0, result.output
    assert "queue_item_id=EXP-3R-003" in result.output
