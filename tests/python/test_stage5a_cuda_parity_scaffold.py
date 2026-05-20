from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_planning.parity_scaffold import build_parity_scaffold

def test_stage5a_parity_scaffold_matches_ready_targets(tmp_path: Path) -> None:
    target_path = Path("data/cuda/stage5a-cuda-target-plan.yaml")
    assert target_path.is_file()
    scaffolds = build_parity_scaffold(out_dir=tmp_path, parity_scaffold_out=tmp_path / "scaffold.yaml")

    assert len(scaffolds) == 9
    assert all(record["execution_enabled"] is False for record in scaffolds)
    assert all(record["cuda_execution_performed"] is False for record in scaffolds)
    assert all(record["output_token_hash"] for record in scaffolds)
