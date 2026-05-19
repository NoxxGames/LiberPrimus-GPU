from __future__ import annotations

from pathlib import Path

from PIL import Image

from libreprimus.visual_annotation.static_site import write_static_site
from libreprimus.visual_annotation.template_writer import write_templates


def test_stage4c_static_site_and_template_generation(tmp_path: Path) -> None:
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    Image.new("RGB", (200, 120), "white").save(image_dir / "5.jpg")
    artifact = {
        "image_id": "liber-primus-page-image-5",
        "file_name": "5.jpg",
        "relative_path": "third_party/LiberPrimusPages/5.jpg",
        "width": 200,
        "height": 120,
    }
    task = {
        "task_id": "stage4c-task-stage4b-delimiter-three-dot-page5",
        "task_family": "mirrored_three_dot_delimiter",
        "source_observation_id": "stage4b-delimiter-three-dot-page5",
        "annotation_status": "needs_human_coordinates",
        "review_status": "human_review_required",
        "coordinate_system": "unknown_pending_annotation",
        "instructions": "mark region",
        "candidate_summary": "",
        "ambiguity_notes": "needs coordinates",
        "image_refs": ["liber-primus-page-image-5"],
    }
    summary = {
        "task_count": 1,
        "cuneiform_task_count": 0,
        "dot_task_count": 0,
        "delimiter_task_count": 1,
        "negative_control_task_count": 0,
        "unresolved_page_reference_count": 0,
    }

    paths = write_templates([task], tmp_path / "out" / "site" / "templates")
    write_static_site(
        out_dir=tmp_path / "out",
        image_dir=image_dir,
        image_artifacts=[artifact],
        tasks=[task],
        cuneiform=[],
        dot=[],
        delimiter=[{"task_id": task["task_id"]}],
        negative=[],
        summary=summary,
    )

    index = tmp_path / "out" / "site" / "index.html"
    page = tmp_path / "out" / "site" / "pages" / "liber-primus-page-image-5.html"
    assert index.is_file()
    assert page.is_file()
    assert "noindex,nofollow,noarchive" in index.read_text(encoding="utf-8")
    assert paths[0].is_file()
