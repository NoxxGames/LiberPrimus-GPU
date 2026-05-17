from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from pathlib import Path

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_execution.vigenere_key_pack import run_vigenere_key_pack_item

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"
TARGET_ID = "stage3e_vig_history_key_pack_v1"


def _synthetic_item() -> dict:
    queue = load_bounded_queue(QUEUE)
    item = next(deepcopy(candidate) for candidate in queue.items if candidate["item_id"] == TARGET_ID)
    item["corpus_slice"]["slice_id"] = "stage3i-output-synthetic-slice"
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3i-output-synthetic",
        "index29_values": [20, 10, 17, 18],
        "token_records": [
            {"token_kind": "rune", "index29": 20, "token_index_global": 0, "logical_line_index": 1},
            {"token_kind": "word_separator", "token_index_global": 1, "logical_line_index": 1},
            {"token_kind": "rune", "index29": 10, "token_index_global": 2, "logical_line_index": 1},
            {"token_kind": "physical_newline", "token_index_global": 3, "logical_line_index": 1},
            {"token_kind": "rune", "index29": 17, "token_index_global": 4, "logical_line_index": 2},
            {"token_kind": "rune", "index29": 18, "token_index_global": 5, "logical_line_index": 2},
        ],
        "raw_unsolved_text_included": False,
    }
    item["corpus_slice"]["metadata_paths"] = []
    return item


def test_stage3i_candidate_output_records_include_historical_identity(tmp_path: Path) -> None:
    summary = run_vigenere_key_pack_item(_synthetic_item(), out_dir=tmp_path, top_k=5)
    records = [
        json.loads(line)
        for line in Path(summary.output_paths["candidate_records"]).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert len(records) == 56
    first = records[0]
    assert first["transform_family"] == "vigenere_key_pack"
    assert first["transform_id"] == "vigenere_explicit_key"
    assert first["key_text"]
    assert first["key_indices"]
    assert first["evidence_family"] == "historical_motif_key_pack"
    assert first["transform_parameters"]["evidence_family"] == "historical_motif_key_pack"
    assert first["transform_parameters"]["reset_mode"] in {"none", "line"}
    assert first["transform_parameters"]["advance_mode"] in {"runes_only", "token_break_preserving"}
    assert first["cuda_used"] is False
    assert first["solve_claim"] is False
    assert first["calibrated_confidence_label"]
    assert first["score_summary"]["no_solve_claim"] is True


def test_stage3i_run_summary_records_expected_executed_and_deferred_counts(tmp_path: Path) -> None:
    summary = run_vigenere_key_pack_item(_synthetic_item(), out_dir=tmp_path, top_k=5)
    payload = json.loads(Path(summary.output_paths["summary"]).read_text(encoding="utf-8"))

    assert payload["expected_candidate_count"] == 56
    assert payload["executed_candidate_count"] == 56
    assert payload["deferred_candidate_count"] == 0
    assert payload["key_count"] == 14
    assert payload["top_candidate"]["evidence_family"] == "historical_motif_key_pack"
    assert payload["confidence_distribution"]
    assert payload["cuda_used"] is False
    assert payload["solve_claim"] is False


def test_stage3i_generated_outputs_are_ignored() -> None:
    path = "experiments/results/bounded-auto-runs/stage3i/candidate_records.jsonl"
    result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=REPO, check=False)

    assert result.returncode == 0

