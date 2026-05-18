from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.bounded_execution.caesar_affine import labels_by_index
from libreprimus.post_discord.onion7_seed_pack import render_onion7_candidate, run_onion7_seed_pack

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml"


def _synthetic_manifest(tmp_path: Path, *, with_line_metadata: bool = True) -> Path:
    payload = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    records = [
        {"token_kind": "rune", "index29": 0, "token_index_global": 0, "line_index": 0},
        {"token_kind": "rune", "index29": 1, "token_index_global": 1, "line_index": 0},
        {"token_kind": "line_separator", "token_index_global": 2},
        {"token_kind": "rune", "index29": 2, "token_index_global": 3, "line_index": 1},
        {"token_kind": "rune", "index29": 3, "token_index_global": 4, "line_index": 1},
    ]
    if not with_line_metadata:
        for record in records:
            record.pop("line_index", None)
    payload["corpus_slice"] = {
        "slice_id": "synthetic-stage3s",
        "corpus_candidate_id": "synthetic",
        "selector": {
            "index29_values": [0, 1, 2, 3],
            "token_records": records,
        },
    }
    path = tmp_path / "manifest.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def test_onion7_stream_repeats_and_line_reset_renders() -> None:
    labels = labels_by_index(REPO / "data/profiles/gematria/gematria-primus-v0.json")
    tokens = [
        {"token_kind": "rune", "index29": 3, "line_index": 0},
        {"token_kind": "rune", "index29": 4, "line_index": 0},
        {"token_kind": "line_separator"},
        {"token_kind": "rune", "index29": 3, "line_index": 1},
    ]

    text, indices, used = render_onion7_candidate(tokens, numeric_sequence=[1, 2], reset_mode="line", labels=labels)

    assert indices == [2, 2, 2]
    assert used == [1, 2, 1]
    assert "\n" in text


def test_onion7_executor_runs_synthetic_manifest(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    summary = run_onion7_seed_pack(manifest_path=_synthetic_manifest(tmp_path), out_dir=out_dir, top_k=5)

    assert summary.expected_candidate_count == 72
    assert summary.executed_candidate_count == 72
    assert summary.deferred_candidate_count == 0
    assert summary.top_candidate["value_space"] in {"raw_table", "prime_delta_table", "prime_order_table"}
    assert (out_dir / "candidate_records.jsonl").is_file()


def test_onion7_executor_defers_line_reset_without_line_metadata(tmp_path: Path) -> None:
    summary = run_onion7_seed_pack(
        manifest_path=_synthetic_manifest(tmp_path, with_line_metadata=False),
        out_dir=tmp_path / "out",
        top_k=5,
    )

    assert summary.expected_candidate_count == 72
    assert summary.executed_candidate_count == 36
    assert summary.deferred_candidate_count == 36
    assert any("line_reset_metadata_missing" in warning for warning in summary.warnings)
