from __future__ import annotations

from test_stage6_common import stage6_data


def test_stage6_no_lossy_filtering_policy_blocks_triage_and_top_n() -> None:
    payload = stage6_data("no_lossy_filtering_policy")
    assert payload["lossy_filtering_before_archive_forbidden"] is True
    assert payload["top_n_only_output_allowed"] is False
    assert payload["score_threshold_discard_allowed"] is False
    assert payload["cuda_triage_allowed"] is False
    assert payload["scoring_triage_allowed"] is False
    assert payload["discard_by_score_allowed"] is False
    assert "split_probe_into_smaller_finite_batches" in payload["if_expected_output_too_large"]


def test_stage6_result_bundle_policy_defines_future_zip_without_creating_it() -> None:
    payload = stage6_data("result_bundle_policy")
    assert payload["stage7_zip_archive_required"] is True
    assert payload["all_bounded_outputs_preserved"] is True
    assert payload["stage6_creates_result_archive_now"] is False
    assert payload["generated_outputs_committed"] is False
    assert payload["assistant_archive_analysis_required"] is True


def test_stage6_triangle_boundaries_keep_stage8_and_stage9_deferred() -> None:
    payload = stage6_data("stage8_triangle_readiness_handoff")
    assert payload["stage6_triangle_readiness_inventory_allowed"] is True
    assert payload["stage6_triangle_readout_generation_allowed"] is False
    assert payload["stage6_pdd153_route_extraction_allowed"] is False
    assert payload["stage6_page32_route_extraction_allowed"] is False
    assert payload["stage8_triangle_readiness_deferred"] is True
    assert payload["stage9_triangle_experiment_deferred"] is True


def test_stage6_gate_closure_false_flags() -> None:
    summary = stage6_data("summary")
    for key in ("stage6_probe_execution_performed_now", "stage6_zip_result_bundle_created_now"):
        assert summary[key] is False
    for key in ("route_stream_generated_now", "real_byte_stream_generated", "cuda_execution_performed"):
        assert summary[key] is False
