from __future__ import annotations

import json
from pathlib import Path

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_execution.reset_advance_ablation import run_reset_advance_ablation_item

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3h-bounded-cpu-queue.yaml"


def test_stage3h_outputs_validate_and_keep_safety_flags(tmp_path: Path) -> None:
    queue = load_bounded_queue(QUEUE)
    summary = run_reset_advance_ablation_item(queue.items[0], out_dir=tmp_path, top_k=5)
    candidate = json.loads((tmp_path / "candidate_records.jsonl").read_text(encoding="utf-8").splitlines()[0])
    negative = json.loads((tmp_path / "negative_control_records.jsonl").read_text(encoding="utf-8").splitlines()[0])
    summary_payload = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))

    assert summary.executed_candidate_count == 64
    assert candidate["base_transform_id"]
    assert candidate["reset_mode"] in {"none", "word", "clause", "line"}
    assert candidate["advance_mode"] in {"runes_only", "token_break_preserving"}
    assert candidate["cuda_used"] is False
    assert candidate["solve_claim"] is False
    assert candidate["calibrated_confidence_label"]
    assert negative["solve_claim"] is False
    assert summary_payload["generated_outputs_ignored"] is True
    assert summary_payload["negative_control_count"] == 100
