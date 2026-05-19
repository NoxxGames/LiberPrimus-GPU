from __future__ import annotations

from libreprimus.visual_annotation.task_builder import build_annotation_pack


def test_stage4c_task_builder_does_not_invent_coordinates() -> None:
    pack = build_annotation_pack(
        visual_observations=[
            {
                "observation_id": "stage4b-cuneiform-17-13-55-1",
                "observation_family": "cuneiform_base60",
                "source_id": "source",
                "page_refs": ["pages-33-39-cuneiform-cluster"],
                "candidate_readings": [{"reading_id": "r", "value": [17, 13, 55, 1]}],
                "derived_values": {"pair_55_1_base60": 3301},
                "ambiguity_notes": "needs coordinates",
            }
        ],
        negative_controls=[],
        image_artifacts=[{"image_id": "liber-primus-page-image-33", "file_name": "33.jpg"}],
    )

    task = pack["tasks"][0]
    assert task["annotation_status"] == "needs_human_coordinates"
    assert task["coordinate_system"] == "unknown_pending_annotation"
    assert task["usable_as_experiment_seed"] is False
