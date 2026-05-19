"""Stage 4C visual annotation export orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.visual_annotation.loaders import (
    load_jsonl_records,
    load_yaml_records,
    write_yaml_payload,
    write_yaml_records,
)
from libreprimus.visual_annotation.static_site import write_static_site
from libreprimus.visual_annotation.task_builder import build_annotation_pack
from libreprimus.visual_annotation.template_writer import write_templates


def run_visual_annotation_build(
    *,
    visual_observations: Path,
    negative_controls: Path,
    image_artifacts: Path,
    image_locks: Path,
    image_dir: Path,
    out_dir: Path,
    task_out: Path,
    cuneiform_out: Path,
    dot_out: Path,
    delimiter_out: Path,
    negative_out: Path,
    summary_out: Path,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Build Stage 4C committed records and ignored local annotation workspace."""

    del image_locks, allow_warnings
    out_dir.mkdir(parents=True, exist_ok=True)
    visual_records = load_yaml_records(visual_observations)
    negative_records = load_yaml_records(negative_controls)
    artifacts = load_jsonl_records(image_artifacts)

    pack = build_annotation_pack(
        visual_observations=visual_records,
        negative_controls=negative_records,
        image_artifacts=artifacts,
    )
    tasks = pack["tasks"]
    cuneiform = pack["cuneiform"]
    dot = pack["dot"]
    delimiter = pack["delimiter"]
    negative = pack["negative"]
    summary = pack["summary"]

    write_yaml_records(
        task_out,
        record_set_id="stage4c-visual-annotation-tasks",
        schema="schemas/visual/visual-annotation-task-v0.schema.json",
        records=tasks,
    )
    write_yaml_records(
        cuneiform_out,
        record_set_id="stage4c-cuneiform-reading-candidates",
        schema="schemas/visual/cuneiform-reading-candidate-v0.schema.json",
        records=cuneiform,
    )
    write_yaml_records(
        dot_out,
        record_set_id="stage4c-dot-pattern-annotation-tasks",
        schema="schemas/visual/dot-pattern-annotation-v0.schema.json",
        records=dot,
    )
    write_yaml_records(
        delimiter_out,
        record_set_id="stage4c-delimiter-annotation-tasks",
        schema="schemas/visual/delimiter-annotation-v0.schema.json",
        records=delimiter,
    )
    write_yaml_records(
        negative_out,
        record_set_id="stage4c-visual-negative-control-annotation-tasks",
        schema="schemas/visual/visual-negative-control-annotation-v0.schema.json",
        records=negative,
    )
    write_yaml_payload(summary_out, summary)

    template_paths = write_templates(tasks, out_dir / "site" / "templates")
    site_info = write_static_site(
        out_dir=out_dir,
        image_dir=image_dir,
        image_artifacts=artifacts,
        tasks=tasks,
        cuneiform=cuneiform,
        dot=dot,
        delimiter=delimiter,
        negative=negative,
        summary=summary,
    )

    result = dict(summary)
    result.update(
        {
            "run_id": "stage4c-visual-annotation-pack",
            "visual_observation_count_loaded": len(visual_records),
            "negative_control_count_loaded": len(negative_records),
            "image_artifact_count_loaded": len(artifacts),
            "generated_site_path": _display_path(site_info["site_index"]),
            "generated_template_count": len(template_paths),
            "generated_image_page_count": site_info["image_page_count"],
            "output_paths": {
                "tasks": _display_path(task_out),
                "cuneiform": _display_path(cuneiform_out),
                "dot": _display_path(dot_out),
                "delimiter": _display_path(delimiter_out),
                "negative": _display_path(negative_out),
                "summary": _display_path(summary_out),
                "site": _display_path(site_info["site_index"]),
            },
        }
    )
    return result


def _display_path(path: Path) -> str:
    return path.as_posix()
