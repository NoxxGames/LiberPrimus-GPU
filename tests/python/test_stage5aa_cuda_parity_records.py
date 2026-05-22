from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.prime_minus_one_cuda_synthetic.models import EXPECTED_SYNTHETIC_HASH
from libreprimus.prime_minus_one_cuda_synthetic.parity_records import build_parity_records
from libreprimus.prime_minus_one_cuda_synthetic.run_records import run_synthetic_cuda_parity


def test_stage5aa_parity_skip_does_not_select_pass(tmp_path: Path) -> None:
    run_path = tmp_path / "run.yaml"
    parity_path = tmp_path / "parity.yaml"
    run_synthetic_cuda_parity(cuda_run_out=run_path, out_dir=tmp_path, skip_cuda=True)
    record = build_parity_records(cuda_run=run_path, parity_out=parity_path, out_dir=tmp_path)[0]
    assert record["parity_status"] == "skipped_cuda_unavailable"
    assert record["expected_hash_match"] is False
    assert record["p56_cuda_execution_performed"] is False


def test_stage5aa_parity_hash_mismatch_is_explicit(tmp_path: Path) -> None:
    run_path = tmp_path / "run.yaml"
    run_synthetic_cuda_parity(cuda_run_out=run_path, out_dir=tmp_path, skip_cuda=True)
    payload = yaml.safe_load(run_path.read_text(encoding="utf-8"))
    payload["records"][0]["cuda_run_status"] = "passed"
    payload["records"][0]["computed_output_token_hash"] = "0" * 64
    run_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    record = build_parity_records(cuda_run=run_path, parity_out=tmp_path / "parity.yaml", out_dir=tmp_path)[0]
    assert record["expected_output_token_hash"] == EXPECTED_SYNTHETIC_HASH
    assert record["parity_status"] == "failed_hash_mismatch"
