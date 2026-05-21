from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_cuda_result_store.method_status_impact import build_method_status_impact
from libreprimus.gematria_cuda_result_store.result_store_integration import build_result_store_integration


def test_stage5p_method_status_impact_does_not_upgrade_to_solved(tmp_path: Path) -> None:
    result_store = tmp_path / "result-store.yaml"
    build_result_store_integration(result_store_integration_out=result_store, out_dir=tmp_path)

    records = build_method_status_impact(
        result_store_integration=result_store,
        method_status_impact_out=tmp_path / "method-impact.yaml",
        out_dir=tmp_path,
    )

    assert len(records) >= 2
    assert all(record["method_status_upgrade_allowed"] is False for record in records)
    assert all(record["method_status_upgraded"] is False for record in records)
    assert all(record["post_stage_status"] != "solved" for record in records)


def test_stage5p_method_status_marks_unsolved_cuda_blocked(tmp_path: Path) -> None:
    result_store = tmp_path / "result-store.yaml"
    build_result_store_integration(result_store_integration_out=result_store, out_dir=tmp_path)

    records = build_method_status_impact(
        result_store_integration=result_store,
        method_status_impact_out=tmp_path / "method-impact.yaml",
        out_dir=tmp_path,
    )
    unsolved = [record for record in records if record["method_family"] == "unsolved_page_cuda"]

    assert len(unsolved) == 1
    assert unsolved[0]["impact_status"] == "blocked_not_activated"
    assert unsolved[0]["unsolved_page_cuda_used"] is False
