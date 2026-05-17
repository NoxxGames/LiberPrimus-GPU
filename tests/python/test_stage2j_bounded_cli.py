from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage2j-bounded-cpu-queue.yaml"


def test_bounded_cli_validate_policy_and_queue() -> None:
    runner = CliRunner()
    policy = runner.invoke(app, ["bounded-experiment", "validate-policy", "--policy", str(POLICY)])
    queue = runner.invoke(app, ["bounded-experiment", "validate-queue", "--queue", str(QUEUE)])

    assert policy.exit_code == 0, policy.output
    assert "max_candidate_count=100000" in policy.output
    assert queue.exit_code == 0, queue.output
    assert "item_count=3" in queue.output


def test_bounded_cli_check_queue() -> None:
    result = CliRunner().invoke(
        app,
        ["bounded-experiment", "check-queue", "--policy", str(POLICY), "--queue", str(QUEUE)],
    )

    assert result.exit_code == 0, result.output
    assert "policy_pass_count=2" in result.output
    assert "policy_blocked_count=1" in result.output
    assert "stage2j-blocked-overbudget-example=policy:fail" in result.output


def test_bounded_cli_run_all_and_summary(tmp_path: Path) -> None:
    runner = CliRunner()
    run = runner.invoke(
        app,
        [
            "bounded-experiment",
            "run-all",
            "--policy",
            str(POLICY),
            "--queue",
            str(QUEUE),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    )
    summary = runner.invoke(app, ["bounded-experiment", "summary", "--results-dir", str(tmp_path)])

    assert run.exit_code == 0, run.output
    assert "executed_count=1" in run.output
    assert "deferred_count=1" in run.output
    assert "blocked_count=1" in run.output
    assert summary.exit_code == 0, summary.output
    assert "policy_pass_count=2" in summary.output
    assert "stage2j-caesar-affine-first-reviewable-slice=deferred" in summary.output


def test_policy_passing_bounded_items_do_not_require_approval() -> None:
    result = CliRunner().invoke(
        app,
        ["bounded-experiment", "check-queue", "--policy", str(POLICY), "--queue", str(QUEUE)],
    )

    assert result.exit_code == 0, result.output
    assert "approval" not in result.output.lower()


def test_out_of_policy_item_is_blocked_for_explicit_instruction() -> None:
    result = CliRunner().invoke(
        app,
        ["bounded-experiment", "check-queue", "--policy", str(POLICY), "--queue", str(QUEUE)],
    )

    assert result.exit_code == 0, result.output
    assert "over_candidate_limit_requires_explicit_user_instruction" in result.output.replace("\n", "")
