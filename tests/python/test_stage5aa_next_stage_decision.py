from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.prime_minus_one_cuda_synthetic.next_stage_decision import build_next_stage_decision


def _write_parity(path: Path, status: str) -> None:
    path.write_text(yaml.safe_dump({"records": [{"parity_status": status}]}, sort_keys=False), encoding="utf-8")


def test_stage5aa_next_stage_pass_selects_stage5ab(tmp_path: Path) -> None:
    parity = tmp_path / "parity.yaml"
    _write_parity(parity, "passed")
    records = build_next_stage_decision(parity=parity, next_stage_decision_out=tmp_path / "decision.yaml", out_dir=tmp_path)
    selected = next(record for record in records if record["selected"] is True)
    assert selected["option_id"] == "stage5ab_prime_minus_one_synthetic_reporting_bounded_p56_preflight"
    assert selected["benchmark_selected"] is False
    assert selected["unsolved_cuda_selected"] is False


def test_stage5aa_next_stage_mismatch_selects_fix(tmp_path: Path) -> None:
    parity = tmp_path / "parity.yaml"
    _write_parity(parity, "failed_hash_mismatch")
    records = build_next_stage_decision(parity=parity, next_stage_decision_out=tmp_path / "decision.yaml", out_dir=tmp_path)
    selected = next(record for record in records if record["selected"] is True)
    assert selected["option_id"] == "stage5aa_fix_hash_mismatch"
