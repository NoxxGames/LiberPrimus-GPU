from __future__ import annotations

import json
from pathlib import Path

import yaml

from libreprimus.bounded_execution.validation import validate_candidate_record, validate_run_summary
from libreprimus.post_discord.onion7_seed_pack import run_onion7_seed_pack

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml"


def test_stage3s_candidate_output_schema_has_required_fields(tmp_path: Path) -> None:
    payload = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    payload["corpus_slice"] = {
        "slice_id": "synthetic-stage3s-schema",
        "corpus_candidate_id": "synthetic",
        "selector": {"index29_values": [0, 1, 2, 3]},
    }
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    out_dir = tmp_path / "out"

    run_onion7_seed_pack(manifest_path=manifest, out_dir=out_dir, top_k=3)

    first = json.loads((out_dir / "candidate_records.jsonl").read_text(encoding="utf-8").splitlines()[0])
    validate_candidate_record(first)
    assert first["value_space"]
    assert first["route"]
    assert first["direction"]
    assert first["reset_mode"]
    assert first["numeric_sequence_mod29"]
    assert first["cuda_used"] is False
    assert first["solve_claim"] is False
    assert first["score_summary"]["no_solve_claim"] is True
    summary = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
    validate_run_summary(summary)
    assert summary["queue_item_id"] == "EXP-3R-003"
