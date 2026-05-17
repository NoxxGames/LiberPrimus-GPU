from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from pathlib import Path

from libreprimus.bounded_execution.validation import validate_candidate_record, validate_run_summary
from libreprimus.bounded_execution.vigenere_key_list import run_vigenere_key_list_item
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3c-bounded-cpu-queue.yaml"


def _stage3d_item() -> dict:
    item = deepcopy(load_bounded_queue(QUEUE).items[0])
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3d-schema-synthetic-input",
        "index29_values": [20, 10, 17, 18, 4, 13],
        "raw_unsolved_text_included": False,
    }
    item["corpus_slice"]["metadata_paths"] = []
    return item


def test_stage3d_candidate_records_validate_schema(tmp_path: Path) -> None:
    run_vigenere_key_list_item(_stage3d_item(), out_dir=tmp_path, top_k=4)
    rows = [json.loads(line) for line in (tmp_path / "candidate_records.jsonl").read_text(encoding="utf-8").splitlines()]

    assert len(rows) == 4
    for row in rows:
        payload = validate_candidate_record(row)
        assert payload["key_text"] in {"LIBER", "PRIMUS", "DIVINITY", "CICADA"}
        assert payload["key_indices"]
        assert payload["cuda_used"] is False
        assert payload["solve_claim"] is False
        assert payload["calibrated_confidence_label"]


def test_stage3d_summary_validates_schema(tmp_path: Path) -> None:
    run_vigenere_key_list_item(_stage3d_item(), out_dir=tmp_path, top_k=4)
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))

    payload = validate_run_summary(summary)

    assert payload["candidate_count"] == 4
    assert payload["top_candidate"]["key_text"] in {"LIBER", "PRIMUS", "DIVINITY", "CICADA"}
    assert payload["top_candidate"]["calibrated_confidence_label"]


def test_stage3d_generated_outputs_are_ignored() -> None:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "experiments/results/bounded-auto-runs/stage3d/candidate_records.jsonl"],
        cwd=REPO,
        check=False,
    )

    assert result.returncode == 0
