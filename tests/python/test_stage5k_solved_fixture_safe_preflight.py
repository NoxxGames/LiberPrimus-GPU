from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_cuda_parity_reporting.solved_fixture_preflight import build_solved_fixture_preflight


def test_stage5k_solved_fixture_preflight_keeps_execution_blocked(tmp_path: Path) -> None:
    records = build_solved_fixture_preflight(preflight_out=tmp_path / "preflight.yaml", out_dir=tmp_path)
    assert len(records) == 5
    assert {record["readiness_status"] for record in records} == {"needs_token_mapping"}
    for record in records:
        assert record["solved_fixture_cuda_execution_allowed"] is False
        assert record["real_liber_primus_data_used"] is False
        assert record["unsolved_page_cuda_used"] is False
        assert record["cuda_execution_performed"] is False
        assert record["blocker_count"] == 7


def test_stage5k_next_stage_decision_has_blockers() -> None:
    from libreprimus.gematria_cuda_parity_reporting.summary import load_summary

    summary = load_summary()
    assert summary["blocker_count"] == 7
    assert summary["readiness_status_counts"] == {"needs_token_mapping": 5}
    assert "token mapping" in summary["selected_next_stage"]
