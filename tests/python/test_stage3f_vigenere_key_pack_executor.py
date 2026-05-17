from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_execution.vigenere_key_pack import (
    EXPECTED_STAGE3F_KEYS,
    load_declared_key_pack,
    render_vigenere_key_pack_candidate,
    run_vigenere_key_pack_item,
)
from libreprimus.bounded_execution.caesar_affine import labels_by_index
from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import load_gematria_profile
from libreprimus.solved_fixtures.vigenere import key_text_to_indices

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"


def _target_item() -> dict:
    queue = load_bounded_queue(QUEUE)
    for item in queue.items:
        if item["item_id"] == "stage3e_vig_lp_evidence_pack_v1":
            return deepcopy(item)
    raise AssertionError("Stage 3F target item missing")


def _synthetic_item(*, with_line_metadata: bool = True) -> dict:
    item = _target_item()
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
    item["corpus_slice"]["slice_id"] = "stage3f-synthetic-slice"
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3f-synthetic",
        "index29_values": [20, 10, 17, 18],
        "token_records": token_records,
        "raw_unsolved_text_included": False,
    }
    item["corpus_slice"]["metadata_paths"] = []
    return item


def test_key_pack_loads_exact_declared_keys_and_count() -> None:
    pack = load_declared_key_pack(_target_item())

    assert pack.keys == EXPECTED_STAGE3F_KEYS
    assert len(pack.keys) == 12
    assert pack.reset_modes == ["none", "line"]
    assert pack.advance_modes == ["runes_only", "token_break_preserving"]
    assert pack.expected_candidate_count == 48


def test_key_pack_rejects_key_expansion_without_count_update() -> None:
    item = _target_item()
    item["transform_plan"]["parameters"]["keys"].append("EXTRA")

    try:
        load_declared_key_pack(item)
    except ValueError as error:
        assert "12 declared LP evidence keys" in str(error)
    else:
        raise AssertionError("expanded key list unexpectedly validated")


def test_all_stage3f_keys_map_to_gematria_indices() -> None:
    profile = load_gematria_profile(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")

    for key in EXPECTED_STAGE3F_KEYS:
        indices = key_text_to_indices(key, profile)
        assert indices
        assert all(0 <= index <= 28 for index in indices)


def test_reset_none_and_line_execute_with_line_metadata(tmp_path: Path) -> None:
    summary = run_vigenere_key_pack_item(_synthetic_item(with_line_metadata=True), out_dir=tmp_path, top_k=5)

    assert summary.expected_candidate_count == 48
    assert summary.executed_candidate_count == 48
    assert summary.deferred_candidate_count == 0
    assert summary.vigenere_candidate_count == 48
    assert summary.solve_claim is False


def test_line_reset_defers_without_line_metadata(tmp_path: Path) -> None:
    summary = run_vigenere_key_pack_item(_synthetic_item(with_line_metadata=False), out_dir=tmp_path, top_k=5)

    assert summary.expected_candidate_count == 48
    assert summary.executed_candidate_count == 24
    assert summary.deferred_candidate_count == 24
    assert any("line_reset_metadata_missing" in warning for warning in summary.warnings)


def test_token_break_preserving_warns_when_metadata_is_flat(tmp_path: Path) -> None:
    item = _target_item()
    item["corpus_slice"]["slice_id"] = "stage3f-flat-synthetic-slice"
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3f-flat-synthetic",
        "index29_values": [20, 10, 17, 18],
        "raw_unsolved_text_included": False,
    }
    item["corpus_slice"]["metadata_paths"] = []

    summary = run_vigenere_key_pack_item(item, out_dir=tmp_path, top_k=5)

    assert summary.executed_candidate_count == 24
    assert summary.deferred_candidate_count == 24
    assert any("token_break_metadata_missing_flat_mode_used" in warning for warning in summary.warnings)


def test_vigenere_decrypt_formula_uses_subtract_convention() -> None:
    labels = labels_by_index(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")
    text, output_indices = render_vigenere_key_pack_candidate(
        [{"token_kind": "rune", "index29": 5}, {"token_kind": "rune", "index29": 1}],
        key_indices=[2],
        labels=labels,
        reset_mode="none",
        advance_mode="runes_only",
    )

    assert output_indices == [3, 28]
    assert text
