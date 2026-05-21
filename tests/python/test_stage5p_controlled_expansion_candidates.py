from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_cuda_result_store.controlled_expansion_candidates import (
    build_controlled_expansion_candidates,
)


def test_stage5p_controlled_expansion_selects_stage5q_candidate_mapping(tmp_path: Path) -> None:
    records = build_controlled_expansion_candidates(
        controlled_expansion_candidates_out=tmp_path / "candidates.yaml",
        out_dir=tmp_path,
    )

    ready = [record for record in records if record["candidate_status"] == "ready_for_stage5q_candidate_mapping"]
    assert len(records) == 6
    assert len(ready) == 1
    assert ready[0]["recommended_next_stage"].startswith("Stage 5Q")


def test_stage5p_controlled_expansion_keeps_execution_disabled(tmp_path: Path) -> None:
    records = build_controlled_expansion_candidates(
        controlled_expansion_candidates_out=tmp_path / "candidates.yaml",
        out_dir=tmp_path,
    )

    assert all(record["requires_cuda_execution"] is False for record in records)
    assert all(record["requires_new_cuda_kernel"] is False for record in records)
    assert all(record["requires_benchmark"] is False for record in records)
    assert all(record["requires_unsolved_page_input"] is False for record in records)
