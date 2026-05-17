from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.cli import app

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3h-bounded-cpu-queue.yaml"


def test_stage3h_reset_advance_cli_runs_on_synthetic_input(tmp_path: Path) -> None:
    queue = load_bounded_queue(QUEUE)
    item = deepcopy(queue.items[0])
    item["corpus_slice"]["slice_id"] = "stage3h-cli-synthetic"
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3h-cli-synthetic",
        "index29_values": [20, 10, 17, 18],
        "token_records": [
            {"token_kind": "rune", "index29": 20, "token_index_global": 0, "logical_line_index": 1},
            {"token_kind": "word_separator", "token_index_global": 1, "logical_line_index": 1},
            {"token_kind": "rune", "index29": 10, "token_index_global": 2, "logical_line_index": 1},
            {"token_kind": "clause_separator", "token_index_global": 3, "logical_line_index": 1},
            {"token_kind": "rune", "index29": 17, "token_index_global": 4, "logical_line_index": 2},
            {"token_kind": "physical_newline", "token_index_global": 5, "logical_line_index": 2},
            {"token_kind": "rune", "index29": 18, "token_index_global": 6, "logical_line_index": 2},
        ],
        "raw_unsolved_text_included": False,
    }
    item["corpus_slice"]["metadata_paths"] = []
    queue_path = tmp_path / "queue.yaml"
    queue_path.write_text(
        yaml.safe_dump(
            {
                "record_type": "bounded_experiment_queue",
                "queue_id": "stage3h-cli-test",
                "queue_version": "bounded-experiment-queue-v0",
                "policy_id": "operator-policy-v0",
                "default_output_dir": str(tmp_path),
                "canonical_corpus_active": False,
                "page_boundaries_final": False,
                "trusted_as_canonical": False,
                "items": [item],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    result = CliRunner().invoke(
        app,
        [
            "bounded-run",
            "run-reset-advance-ablation",
            "--policy",
            str(POLICY),
            "--queue",
            str(queue_path),
            "--item-id",
            "stage3h_reset_advance_ablation_v1",
            "--out-dir",
            str(tmp_path / "out"),
            "--top-k",
            "5",
            "--allow-warnings",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "expected_candidate_count=64" in result.output
    assert "executed_candidate_count=64" in result.output
    assert "negative_control_count=100" in result.output
