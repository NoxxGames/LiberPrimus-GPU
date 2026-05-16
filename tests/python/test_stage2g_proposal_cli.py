from __future__ import annotations

from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
PROPOSAL_DIR = REPO / "experiments/proposals/stage2g"
PROPOSAL = PROPOSAL_DIR / "stage2g-caesar-page-candidate-proposal.yaml"
PENDING = PROPOSAL_DIR / "approval-records/stage2g-example-pending-approval.yaml"


def test_proposal_validate_works() -> None:
    result = CliRunner().invoke(app, ["proposal", "validate", "--proposal", str(PROPOSAL)])

    assert result.exit_code == 0, result.output
    assert "Experiment proposal validation OK" in result.output


def test_proposal_review_packet_works(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        ["proposal", "review-packet", "--proposal", str(PROPOSAL), "--out-dir", str(tmp_path), "--allow-warnings"],
    )

    assert result.exit_code == 0, result.output
    assert "execution_blocked=true" in result.output


def test_proposal_check_approval_blocks_pending_approval() -> None:
    result = CliRunner().invoke(
        app,
        ["proposal", "check-approval", "--proposal", str(PROPOSAL), "--approval", str(PENDING)],
    )

    assert result.exit_code == 0, result.output
    assert "approval_status=pending" in result.output
    assert "execution_blocked=true" in result.output


def test_stage2g_review_all_works(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "proposal",
            "stage2g-review-all",
            "--proposal-dir",
            str(PROPOSAL_DIR),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "proposal_count=5" in result.output
    assert "approved_count=0" in result.output


def test_review_summary_works(tmp_path: Path) -> None:
    CliRunner().invoke(
        app,
        [
            "proposal",
            "stage2g-review-all",
            "--proposal-dir",
            str(PROPOSAL_DIR),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )
    result = CliRunner().invoke(app, ["proposal", "review-summary", "--results-dir", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "packet_count=5" in result.output


def test_invalid_proposal_returns_nonzero(tmp_path: Path) -> None:
    payload = yaml.safe_load(PROPOSAL.read_text(encoding="utf-8"))
    payload["execution_enabled"] = True
    bad = tmp_path / "bad-proposal.yaml"
    bad.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    result = CliRunner().invoke(app, ["proposal", "validate", "--proposal", str(bad)])

    assert result.exit_code != 0

