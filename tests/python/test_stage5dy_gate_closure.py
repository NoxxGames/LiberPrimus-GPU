from __future__ import annotations

from test_stage5dy_common import ensure_stage5dy_built, load_yaml


def test_stage5dy_scope_keeps_all_execution_gates_closed() -> None:
    ensure_stage5dy_built()
    summary = load_yaml("data/project-state/stage5dy-summary.yaml")
    scope = load_yaml("data/project-state/stage5dy-scope-control.yaml")

    for key in (
        "number_fact_review_batch_3_performed_now",
        "pivot_target_selected_now",
        "byte_stream_generation_authorized_now",
        "execution_performed",
        "solve_claim",
    ):
        assert summary[key] is False
        assert scope[key] is False
    assert scope["recommended_next_stage_id"] == "stage-5dz"
