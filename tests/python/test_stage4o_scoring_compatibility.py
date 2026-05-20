from __future__ import annotations

from pathlib import Path

from libreprimus.cpu_batch.batch_runner import run_manifest
from libreprimus.cpu_batch.parity_readiness import build_scoring_compatibility


MANIFEST = Path("experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml")


def test_stage4o_scoring_compatibility_matches_stage4i_shape(tmp_path: Path) -> None:
    batch = run_manifest(MANIFEST)
    payload = build_scoring_compatibility(batch.records, out_dir=tmp_path)
    assert payload["compatible"] is True
    assert payload["record_count"] == 8
    assert payload["scoring_compatible_count"] == 8
    assert payload["scoring_unavailable_count"] == 0
    assert payload["score_summary_shape_hashes"]
