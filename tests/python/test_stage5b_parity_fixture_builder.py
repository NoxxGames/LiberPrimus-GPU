from __future__ import annotations

from libreprimus.cuda_parity.fixture_builder import build_parity_fixtures


def test_stage5b_parity_fixtures_ready_blocked_and_skipped(tmp_path) -> None:
    fixtures = build_parity_fixtures(out_dir=tmp_path, parity_fixtures_out=tmp_path / "fixtures.yaml")
    statuses = {record["fixture_status"] for record in fixtures}
    assert "ready_for_future_kernel" in statuses
    assert "blocked_target_not_ready" in statuses
    assert "skipped_non_target" in statuses
    assert sum(1 for record in fixtures if record["fixture_status"] == "ready_for_future_kernel") == 9
    assert all(record["cuda_kernel_added"] is False for record in fixtures)


def test_stage5b_ready_fixtures_reference_stage4o_and_stage4p(tmp_path) -> None:
    fixtures = build_parity_fixtures(out_dir=tmp_path, parity_fixtures_out=tmp_path / "fixtures.yaml")
    ready = [record for record in fixtures if record["fixture_status"] == "ready_for_future_kernel"]
    assert ready
    assert all(record["parity_expectation_reference"] for record in ready)
    assert all(record["score_summary_reference"] for record in ready)
    assert all(record["expected_output_hash_source"] == "stage4o_parity_expectation" for record in ready)
