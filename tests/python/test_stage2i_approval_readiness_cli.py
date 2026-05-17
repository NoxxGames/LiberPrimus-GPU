from __future__ import annotations

from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
STAGE2I = REPO / "experiments/proposals/stage2i"
PROPOSAL = STAGE2I / "stage2i-first-bounded-caesar-affine-review.yaml"
APPROVAL = STAGE2I / "approval-records/stage2i-first-bounded-caesar-affine-pending-approval.yaml"


def test_validate_works() -> None:
    result = CliRunner().invoke(
        app,
        ["approval-readiness", "validate", "--proposal", str(PROPOSAL), "--approval", str(APPROVAL)],
    )

    assert result.exit_code == 0, result.output
    assert "candidate_count_estimate=841" in result.output


def test_packet_works_to_tmp_path(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "approval-readiness",
            "packet",
            "--proposal",
            str(PROPOSAL),
            "--approval",
            str(APPROVAL),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "approval_status=pending" in result.output
    assert (tmp_path / "stage2i-first-bounded-caesar-affine-review.review.md").is_file()


def test_human_summary_works() -> None:
    result = CliRunner().invoke(
        app,
        [
            "approval-readiness",
            "human-summary",
            "--proposal",
            str(PROPOSAL),
            "--approval",
            str(APPROVAL),
        ],
    )

    assert result.exit_code == 0, result.output
    assert "proposal_id=stage2i-first-bounded-caesar-affine-review" in result.output
    assert "decision_option_A=approve later execution" in result.output
    assert "decision_option_B=revise proposal" in result.output
    assert "decision_option_C=deny/defer" in result.output


def test_inspect_paths_works() -> None:
    result = CliRunner().invoke(
        app,
        ["approval-readiness", "inspect-paths", "--proposal", str(PROPOSAL)],
    )

    assert result.exit_code == 0, result.output
    output = result.output.replace("\n", "")
    assert f"proposal_path={PROPOSAL}" in output
    assert "proposal_exists=true" in result.output
    assert "approval_exists=true" in result.output
    assert "review_markdown=" in result.output
    assert "metadata_path=" in result.output


def test_stage2i_review_and_summary_work(tmp_path: Path) -> None:
    review = CliRunner().invoke(
        app,
        [
            "approval-readiness",
            "stage2i-review",
            "--proposal-dir",
            str(STAGE2I),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )
    summary = CliRunner().invoke(app, ["approval-readiness", "summary", "--results-dir", str(tmp_path)])

    assert review.exit_code == 0, review.output
    assert summary.exit_code == 0, summary.output
    assert "packet_count=1" in summary.output
    assert "candidate_count_estimate_total=841" in summary.output
    assert "stage2i-first-bounded-caesar-affine-review_review_markdown=" in summary.output


def test_invalid_approved_proposal_returns_nonzero(tmp_path: Path) -> None:
    payload = yaml.safe_load(PROPOSAL.read_text(encoding="utf-8"))
    payload["approved_for_execution"] = True
    bad = tmp_path / "bad.yaml"
    bad.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    result = CliRunner().invoke(app, ["approval-readiness", "validate", "--proposal", str(bad), "--approval", str(APPROVAL)])

    assert result.exit_code != 0
