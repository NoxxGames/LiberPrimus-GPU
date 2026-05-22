from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_synthetic.models import EXPECTED_SYNTHETIC_HASH, SYNTHETIC_OUTPUT_TOKENS
from libreprimus.prime_minus_one_cuda_synthetic.run_records import build_run_records, run_synthetic_cuda_parity
from libreprimus.cpu_batch.input_streams import stable_json_sha256


def test_stage5aa_cuda_run_skip_is_no_gpu_safe(tmp_path: Path) -> None:
    record = run_synthetic_cuda_parity(cuda_run_out=tmp_path / "run.yaml", out_dir=tmp_path, skip_cuda=True)[0]
    assert record["cuda_run_status"] == "skipped_by_option"
    assert record["cuda_attempted"] is False
    assert record["cuda_skip_count"] == 1
    assert record["p56_cuda_execution_performed"] is False
    assert record["solve_claim"] is False


def test_stage5aa_pending_run_record_does_not_claim_execution(tmp_path: Path) -> None:
    record = build_run_records(cuda_run_out=tmp_path / "run.yaml", out_dir=tmp_path)[0]
    assert record["cuda_run_status"] == "pending_synthetic_cuda_run"
    assert record["cuda_pass_count"] == 0
    assert record["computed_output_token_hash"] is None


def test_stage5aa_expected_synthetic_hash_material_is_stable() -> None:
    assert stable_json_sha256(SYNTHETIC_OUTPUT_TOKENS) == EXPECTED_SYNTHETIC_HASH
