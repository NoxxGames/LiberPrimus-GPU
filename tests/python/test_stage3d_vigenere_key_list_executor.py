from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from libreprimus.bounded_execution.vigenere_key_list import (
    EXPECTED_STAGE3D_KEYS,
    load_declared_key_list,
    run_vigenere_key_list_item,
    vigenere_decrypt_indices,
)
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.profiles.gematria_profile import load_gematria_profile
from libreprimus.solved_fixtures.vigenere import key_text_to_indices

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3c-bounded-cpu-queue.yaml"
PROFILE = REPO / "data/profiles/gematria/gematria-primus-v0.json"


def _stage3d_item() -> dict:
    item = deepcopy(load_bounded_queue(QUEUE).items[0])
    item["corpus_slice"]["selector"] = {
        "selector_kind": "inline_index29_values",
        "page_candidate_id": "stage3d-synthetic-input",
        "index29_values": [20, 10, 17, 18, 4, 13],
        "raw_unsolved_text_included": False,
    }
    item["corpus_slice"]["metadata_paths"] = []
    return item


def test_key_list_loads_exactly_four_keys() -> None:
    assert load_declared_key_list(_stage3d_item()) == EXPECTED_STAGE3D_KEYS


def test_key_list_rejects_mutation_or_expansion() -> None:
    item = _stage3d_item()
    params = item["transform_plan"]["families"][0]["parameters"]
    params["keys"].append("EXTRA")
    item["candidate_count_upper_bound"] = 5
    item["transform_plan"]["families"][0]["candidate_count"] = 5

    try:
        load_declared_key_list(item)
    except ValueError as error:
        assert "unexpanded" in str(error)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("expanded Stage 3D key list was accepted")


def test_keys_map_to_gematria_indices() -> None:
    profile = load_gematria_profile(PROFILE)

    mapped = {key: key_text_to_indices(key, profile) for key in EXPECTED_STAGE3D_KEYS}

    assert mapped["LIBER"] == [20, 10, 17, 18, 4]
    assert all(mapped[key] for key in EXPECTED_STAGE3D_KEYS)


def test_vigenere_execution_produces_four_candidates(tmp_path: Path) -> None:
    summary = run_vigenere_key_list_item(_stage3d_item(), out_dir=tmp_path, top_k=4)

    assert summary.candidate_count == 4
    assert summary.vigenere_candidate_count == 4
    assert summary.cuda_used is False
    assert summary.solve_claim is False
    assert (tmp_path / "candidate_records.jsonl").is_file()
    assert (tmp_path / "top_candidates.jsonl").is_file()


def test_vigenere_decrypt_subtract_formula() -> None:
    assert vigenere_decrypt_indices([20, 10, 17], [20]) == [0, 19, 26]
