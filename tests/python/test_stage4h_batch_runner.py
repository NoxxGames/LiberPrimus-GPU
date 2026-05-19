from __future__ import annotations

from pathlib import Path

from libreprimus.cpu_batch.batch_runner import run_manifest


MANIFEST = Path("experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml")


def test_stage4h_batch_runner_deterministic() -> None:
    first = run_manifest(MANIFEST)
    second = run_manifest(MANIFEST)
    assert first.records == second.records
    assert first.summary == second.summary
    assert first.summary["executed_candidate_count"] == 6
    assert first.summary["cuda_used"] is False
    assert first.summary["no_solve_claim"] is True


def test_stage4h_output_hash_stable() -> None:
    batch = run_manifest(MANIFEST)
    hashes = [record["output_token_hash"] for record in batch.records]
    assert len(set(hashes)) == len(hashes)
    assert all(len(item) == 64 for item in hashes)
