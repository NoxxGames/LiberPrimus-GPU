from __future__ import annotations

from test_stage5ds_common import ensure_stage5ds_built, load_yaml


def test_stage5ds_keeps_sidecar_gates_closed() -> None:
    ensure_stage5ds_built()
    paths = [
        "data/token-block/stage5ds-no-active-ingestion-proof.yaml",
        "data/token-block/stage5ds-no-byte-stream-transition-proof.yaml",
        "data/token-block/stage5ds-no-token-block-execution-proof.yaml",
    ]
    for path in paths:
        record = load_yaml(path)
        assert record["gate_status"] == "closed"
        assert record["execution_performed"] is False
        assert record["byte_stream_generation_authorized_now"] is False


def test_stage5ds_summary_false_matrix() -> None:
    ensure_stage5ds_built()
    summary = load_yaml("data/project-state/stage5ds-summary.yaml")
    for key in (
        "pivot_target_selected_now",
        "active_planning_input_selected_now",
        "byte_stream_generation_authorized_now",
        "execution_performed",
        "solve_claim",
        "cuda_execution_performed",
    ):
        assert summary[key] is False
