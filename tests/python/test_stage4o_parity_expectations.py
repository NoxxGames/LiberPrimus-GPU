from __future__ import annotations

from pathlib import Path

from libreprimus.cpu_batch.batch_runner import run_manifest
from libreprimus.cpu_batch.parity_expectations import build_parity_expectations


MANIFEST = Path("experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml")


def test_stage4o_parity_expectations_include_output_hashes() -> None:
    batch = run_manifest(MANIFEST)
    parity = build_parity_expectations(batch.records)
    assert len(parity) == 8
    assert all(record["parity_status"] == "passed" for record in parity)
    assert all(len(record["output_token_hash"]) == 64 for record in parity)
    assert all(record["cuda_used"] is False for record in parity)
    assert all(record["no_solve_claim"] is True for record in parity)
