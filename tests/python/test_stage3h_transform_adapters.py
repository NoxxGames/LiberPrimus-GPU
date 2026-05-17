from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_execution.prime_stream_variants import prime_gap_value, prime_minus_one_value, prime_mod29_value
from libreprimus.bounded_execution.reset_advance_ablation import (
    _base_transforms,
    load_declared_reset_advance_ablation,
    run_reset_advance_ablation_item,
)

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3h-bounded-cpu-queue.yaml"


def _target_item() -> dict:
    queue = load_bounded_queue(QUEUE)
    for item in queue.items:
        if item["item_id"] == "stage3h_reset_advance_ablation_v1":
            return deepcopy(item)
    raise AssertionError("Stage 3H target item missing")


def _synthetic_item(*, with_metadata: bool = True) -> dict:
    item = _target_item()
    token_records = [
        {"token_kind": "rune", "index29": 20, "token_index_global": 0, "logical_line_index": 1},
        {"token_kind": "word_separator", "token_index_global": 1, "logical_line_index": 1},
        {"token_kind": "rune", "index29": 10, "token_index_global": 2, "logical_line_index": 1},
        {"token_kind": "clause_separator", "token_index_global": 3, "logical_line_index": 1},
        {"token_kind": "rune", "index29": 17, "token_index_global": 4, "logical_line_index": 2},
        {"token_kind": "physical_newline", "token_index_global": 5, "logical_line_index": 2},
        {"token_kind": "rune", "index29": 18, "token_index_global": 6, "logical_line_index": 2},
    ]
    if not with_metadata:
        token_records = [
            {"token_kind": "rune", "index29": 20, "token_index_global": 0},
            {"token_kind": "rune", "index29": 10, "token_index_global": 1},
            {"token_kind": "rune", "index29": 17, "token_index_global": 2},
            {"token_kind": "rune", "index29": 18, "token_index_global": 3},
        ]
    item["corpus_slice"]["slice_id"] = "stage3h-synthetic-slice"
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3h-synthetic",
        "index29_values": [20, 10, 17, 18],
        "token_records": token_records,
        "raw_unsolved_text_included": False,
    }
    item["corpus_slice"]["metadata_paths"] = []
    return item


def test_stage3h_candidate_count_formula() -> None:
    ablation = load_declared_reset_advance_ablation(_target_item())

    assert len(ablation.base_transforms) == 8
    assert len(ablation.reset_modes) == 4
    assert len(ablation.advance_modes) == 2
    assert ablation.expected_candidate_count == 64


def test_transform_adapters_map_declared_families() -> None:
    transforms = _base_transforms(["vigenere:DIVINITY", "prime_minus_one:offset=0", "prime_mod29:offset=0", "prime_gap:offset=0"])

    assert [transform.family for transform in transforms] == ["vigenere", "prime_minus_one", "prime_mod29", "prime_gap"]
    assert transforms[0].key_indices


def test_prime_stream_variant_values() -> None:
    assert prime_minus_one_value(0, 0) == 1
    assert prime_mod29_value(0, 0) == 2
    assert prime_gap_value(0, 0) == 1


def test_stage3h_ablation_executes_with_metadata(tmp_path: Path) -> None:
    summary = run_reset_advance_ablation_item(_synthetic_item(with_metadata=True), out_dir=tmp_path, top_k=5)

    assert summary.expected_candidate_count == 64
    assert summary.executed_candidate_count == 64
    assert summary.deferred_candidate_count == 0
    assert summary.reset_advance_candidate_count == 64
    assert summary.negative_control_count == 100
    assert summary.solve_claim is False


def test_stage3h_ablation_defers_missing_metadata(tmp_path: Path) -> None:
    summary = run_reset_advance_ablation_item(_synthetic_item(with_metadata=False), out_dir=tmp_path, top_k=5)

    assert summary.expected_candidate_count == 64
    assert summary.executed_candidate_count == 16
    assert summary.deferred_candidate_count == 48
    assert any("word_reset_metadata_missing" in warning for warning in summary.warnings)
    assert any("clause_reset_metadata_missing" in warning for warning in summary.warnings)
    assert any("line_reset_metadata_missing" in warning for warning in summary.warnings)
