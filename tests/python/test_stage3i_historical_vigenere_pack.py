from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from libreprimus.bounded_experiments.policy_checker import check_item
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_execution.vigenere_key_pack import (
    EXPECTED_STAGE3I_KEYS,
    load_declared_key_pack,
    run_vigenere_key_pack_item,
)
from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import load_gematria_profile
from libreprimus.solved_fixtures.vigenere import key_text_to_indices

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"
TARGET_ID = "stage3e_vig_history_key_pack_v1"


def _target_item() -> dict:
    queue = load_bounded_queue(QUEUE)
    for item in queue.items:
        if item["item_id"] == TARGET_ID:
            return deepcopy(item)
    raise AssertionError("Stage 3I historical key-pack item missing")


def _synthetic_item(*, with_line_metadata: bool = True, flat: bool = False) -> dict:
    item = _target_item()
    item["corpus_slice"]["slice_id"] = "stage3i-synthetic-slice"
    selector = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3i-synthetic",
        "index29_values": [20, 10, 17, 18],
        "raw_unsolved_text_included": False,
    }
    if not flat:
        token_records = [
            {"token_kind": "rune", "index29": 20, "token_index_global": 0, "logical_line_index": 1},
            {"token_kind": "word_separator", "token_index_global": 1, "logical_line_index": 1},
            {"token_kind": "rune", "index29": 10, "token_index_global": 2, "logical_line_index": 1},
            {"token_kind": "physical_newline", "token_index_global": 3, "logical_line_index": 1},
            {"token_kind": "rune", "index29": 17, "token_index_global": 4, "logical_line_index": 2},
            {"token_kind": "rune", "index29": 18, "token_index_global": 5, "logical_line_index": 2},
        ]
        if not with_line_metadata:
            for token in token_records:
                token.pop("logical_line_index", None)
        selector["token_records"] = token_records
    item["corpus_slice"]["selector"] = selector
    item["corpus_slice"]["metadata_paths"] = []
    return item


def test_historical_key_pack_loads_exact_declared_keys_and_count() -> None:
    pack = load_declared_key_pack(_target_item())

    assert pack.keys == EXPECTED_STAGE3I_KEYS
    assert len(pack.keys) == 14
    assert pack.reset_modes == ["none", "line"]
    assert pack.advance_modes == ["runes_only", "token_break_preserving"]
    assert pack.expected_candidate_count == 56
    assert pack.evidence_family == "historical_motif_key_pack"


def test_historical_key_pack_rejects_key_expansion_without_count_update() -> None:
    item = _target_item()
    item["transform_plan"]["parameters"]["keys"].append("EXTRA")

    try:
        load_declared_key_pack(item)
    except ValueError as error:
        assert "14 declared historical motif keys" in str(error)
    else:
        raise AssertionError("expanded historical key list unexpectedly validated")

    policy_check = check_item(load_operator_policy(POLICY), item)
    assert "declared_vigenere_key_pack_count_mismatch" in policy_check.blocking_reasons


def test_all_stage3i_keys_map_to_gematria_indices() -> None:
    profile = load_gematria_profile(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")

    for key in EXPECTED_STAGE3I_KEYS:
        indices = key_text_to_indices(key, profile)
        assert indices
        assert all(0 <= index <= 28 for index in indices)


def test_historical_reset_and_advance_modes_execute_with_line_metadata(tmp_path: Path) -> None:
    summary = run_vigenere_key_pack_item(_synthetic_item(with_line_metadata=True), out_dir=tmp_path, top_k=5)

    assert summary.expected_candidate_count == 56
    assert summary.executed_candidate_count == 56
    assert summary.deferred_candidate_count == 0
    assert summary.vigenere_candidate_count == 56
    assert summary.solve_claim is False


def test_historical_line_reset_defers_without_line_metadata(tmp_path: Path) -> None:
    summary = run_vigenere_key_pack_item(_synthetic_item(with_line_metadata=False), out_dir=tmp_path, top_k=5)

    assert summary.expected_candidate_count == 56
    assert summary.executed_candidate_count == 28
    assert summary.deferred_candidate_count == 28
    assert any("line_reset_metadata_missing" in warning for warning in summary.warnings)


def test_historical_token_break_preserving_warns_for_flat_input(tmp_path: Path) -> None:
    summary = run_vigenere_key_pack_item(_synthetic_item(flat=True), out_dir=tmp_path, top_k=5)

    assert summary.executed_candidate_count == 28
    assert summary.deferred_candidate_count == 28
    assert any("token_break_metadata_missing_flat_mode_used" in warning for warning in summary.warnings)

