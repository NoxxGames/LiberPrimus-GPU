import json
import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.solved_baselines.summary import load_summary


REQUIRED_PATHS = [
    Path("data/profiles/gematria/gematria-primus-v0.json"),
    Path("data/fixtures/solved-pages/direct-translation-v0"),
    Path("data/fixtures/solved-pages/atbash-family-v0"),
    Path("data/fixtures/solved-pages/vigenere-v0"),
    Path("data/fixtures/solved-pages/prime-stream-v0"),
    Path("data/normalized/corpus-candidates/rtkd-master-v0-candidate/tokens.jsonl"),
]


def _have_real_inputs() -> bool:
    return all(path.exists() for path in REQUIRED_PATHS)


@pytest.mark.skipif(not _have_real_inputs(), reason="Stage 2A real-source inputs are not present.")
def test_stage2a_real_smoke_runs_and_outputs_expected_counts(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage2a"
    result = CliRunner().invoke(
        app,
        [
            "solved-baseline",
            "stage2a-smoke",
            "--manifest",
            "experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml",
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    summary = load_summary(out_dir)
    assert summary["fixture_count"] == 10
    assert summary["pass_count"] == 10
    assert summary["fail_count"] == 0
    assert summary["pending_count"] == 0
    assert summary["direct_translation_pass_count"] == 4
    assert summary["atbash_family_pass_count"] == 3
    assert summary["vigenere_pass_count"] == 2
    assert summary["prime_stream_pass_count"] == 1
    assert summary["search_performed_any"] is False
    assert summary["cuda_used_any"] is False
    assert summary["scoring_used_any"] is False

    records = [
        json.loads(line)
        for line in (out_dir / "manifest_run_records.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(records) == 10
    assert all(record["search_performed"] is False for record in records)
    assert all(record["cuda_used"] is False for record in records)
    assert all(record["scoring_used"] is False for record in records)


@pytest.mark.skipif(not _have_real_inputs(), reason="Stage 2A real-source inputs are not present.")
def test_stage2a_generated_outputs_are_not_staged() -> None:
    status = subprocess.run(["git", "status", "--short"], check=True, capture_output=True, text=True)

    assert "experiments/results/solved-baselines/stage2a/summary.json" not in status.stdout
