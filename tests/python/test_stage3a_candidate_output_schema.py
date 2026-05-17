from __future__ import annotations

import json
import subprocess
from pathlib import Path

from libreprimus.bounded_execution.runner import TOTAL_COUNT, run_caesar_affine_item
from libreprimus.bounded_execution.validation import validate_candidate_record, validate_run_summary

REPO = Path(__file__).resolve().parents[2]


def _synthetic_item() -> dict:
    return {
        "item_id": "stage3a-synthetic-caesar-affine-test",
        "candidate_count_upper_bound": TOTAL_COUNT,
        "corpus_slice": {
            "slice_id": "stage3a-synthetic-inline-slice",
            "corpus_candidate_id": "synthetic-inline",
            "selector": {
                "selector_kind": "inline_index29_values",
                "page_candidate_id": "synthetic-page",
                "index29_values": [0, 1, 2, 3, 4],
            },
        },
    }


def test_candidate_records_and_summary_validate_schema(tmp_path: Path) -> None:
    summary = run_caesar_affine_item(_synthetic_item(), out_dir=tmp_path, top_k=7)
    summary_payload = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    first_candidate = json.loads((tmp_path / "candidate_records.jsonl").read_text(encoding="utf-8").splitlines()[0])
    top_lines = (tmp_path / "top_candidates.jsonl").read_text(encoding="utf-8").splitlines()

    validate_run_summary(summary_payload)
    validate_candidate_record(first_candidate)
    assert summary.candidate_count == TOTAL_COUNT
    assert summary.top_k_count == 7
    assert len(top_lines) <= 7
    assert summary.solve_claim is False
    assert summary.cuda_used is False


def test_stage3a_generated_outputs_are_ignored() -> None:
    for path in [
        "experiments/results/bounded-auto-runs/stage3a/candidate_records.jsonl",
        "experiments/results/bounded-auto-runs/stage3a/top_candidates.jsonl",
        "experiments/results/bounded-auto-runs/stage3a/summary.json",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=REPO, check=False)
        assert result.returncode == 0, path
