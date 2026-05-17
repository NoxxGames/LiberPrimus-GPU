from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.bounded_experiments.policy_checker import check_item
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage2j-bounded-cpu-queue.yaml"


def test_bounded_run_cli_works_on_synthetic_inline_input(tmp_path: Path) -> None:
    queue = load_bounded_queue(QUEUE).payload
    item = deepcopy(queue["items"][0])
    item["item_id"] = "stage3a-synthetic-cli"
    item["corpus_slice"]["slice_id"] = "stage3a-synthetic-cli-slice"
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "synthetic-cli-page",
        "index29_values": [0, 1, 2, 3, 4, 5],
        "raw_unsolved_text_included": False,
    }
    item["corpus_slice"]["metadata_paths"] = []
    queue["items"] = [item]
    queue_path = tmp_path / "queue.yaml"
    queue_path.write_text(yaml.safe_dump(queue, sort_keys=False), encoding="utf-8")

    runner = CliRunner()
    run = runner.invoke(
        app,
        [
            "bounded-run",
            "run-caesar-affine",
            "--policy",
            str(POLICY),
            "--queue",
            str(queue_path),
            "--item-id",
            "stage3a-synthetic-cli",
            "--out-dir",
            str(tmp_path / "out"),
            "--top-k",
            "3",
            "--allow-warnings",
        ],
    )
    summary = runner.invoke(app, ["bounded-run", "summary", "--results-dir", str(tmp_path / "out")])

    assert run.exit_code == 0, run.output
    assert "candidate_count=841" in run.output
    assert "solve_claim=false" in run.output
    assert summary.exit_code == 0, summary.output
    assert "top_k_count=3" in summary.output


def test_stage3a_policy_blocks_over_candidate_limit() -> None:
    policy = load_operator_policy(POLICY)
    item = deepcopy(load_bounded_queue(QUEUE).items[0])
    item["item_id"] = "stage3a-over-limit"
    item["candidate_count_upper_bound"] = policy.max_candidate_count + 1

    check = check_item(policy, item)

    assert check.status == "fail"
    assert "over_candidate_limit_requires_explicit_user_instruction" in check.blocking_reasons
