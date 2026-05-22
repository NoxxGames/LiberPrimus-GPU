from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5t_batch_abi_gaps_cover_required_surfaces() -> None:
    records = yaml.safe_load(
        Path("data/cuda/stage5t-cuda-candidate-batch-abi-gaps.yaml").read_text(encoding="utf-8")
    )["records"]
    surface_ids = {record["surface_id"] for record in records}
    assert surface_ids == {
        "token_buffer_header",
        "key_schedule_buffer",
        "stream_schedule_buffer",
        "score_vector_shape",
        "top_k_output_shape",
    }
    assert all(record["blocking"] is True for record in records)
    assert all(record["score_summary_compatibility"] == "requires_stage4i_shape" for record in records)
