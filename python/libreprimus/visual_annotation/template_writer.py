"""Write generated blank annotation templates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def write_templates(tasks: list[dict[str, Any]], template_dir: Path) -> list[Path]:
    """Write ignored blank YAML templates for human coordinate capture."""

    template_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for task in tasks:
        task_id = str(task["task_id"])
        payload: dict[str, Any] = {
            "record_type": "visual_region_annotation",
            "annotation_id": f"{task_id}-annotation-pending",
            "task_id": task_id,
            "image_ref": next(iter(task.get("image_refs", [])), ""),
            "coordinate_system": "pixel_absolute",
            "region": {"x_min": None, "y_min": None, "x_max": None, "y_max": None},
            "annotator_notes": "",
            "accepted_reading": None,
            "rejected_readings": [],
            "confidence": "unknown",
            "review_status": "human_review_required",
            "trusted_as_canonical": False,
            "usable_as_experiment_seed": False,
            "solve_claim": False,
        }
        path = template_dir / f"{task_id}.annotation.yaml"
        path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")
        paths.append(path)
    return paths
