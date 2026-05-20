from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.cuda_planning.loaders import load_stage4o_parity_expectations, load_stage4p_unified_results
from libreprimus.cuda_planning.target_plan import build_target_plan


def test_stage5a_target_plan_counts_and_aliases(tmp_path: Path) -> None:
    target_path = tmp_path / "target.yaml"
    non_target_path = tmp_path / "non-target.yaml"
    targets, non_targets = build_target_plan(
        out_dir=tmp_path,
        target_plan_out=target_path,
        non_targets_out=non_target_path,
    )

    assert len(targets) == 14
    assert sum(1 for record in targets if record["target_status"] == "ready_for_planning") == 9
    assert sum(1 for record in targets if str(record["target_status"]).startswith("blocked")) == 2
    assert len(non_targets) == 8

    vigenere = next(record for record in targets if record["transform_family"] == "vigenere")
    assert vigenere["stage4o_parity_expectation_id"] == "stage4o-vigenere-an-v0"
    assert vigenere["output_token_hash"]
    assert yaml.safe_load(target_path.read_text(encoding="utf-8"))["records"]


def test_stage5a_blocked_targets_have_blockers(tmp_path: Path) -> None:
    targets, _ = build_target_plan(out_dir=tmp_path, target_plan_out=tmp_path / "target.yaml")
    blocked = [record for record in targets if str(record["target_status"]).startswith("blocked")]
    assert blocked
    assert all(record["blockers"] for record in blocked)


def test_stage5a_generated_reference_fallbacks_are_raw_data_free(tmp_path: Path) -> None:
    parity = load_stage4o_parity_expectations(tmp_path / "missing-parity.jsonl")
    unified = load_stage4p_unified_results(tmp_path / "missing-unified.jsonl")
    assert len(parity) == 8
    assert len(unified) == 8
    assert all(record["generated_outputs_committed"] is False for record in parity)
    assert all(record["solve_claim"] is False for record in unified)
