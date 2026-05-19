"""Build Stage 4C visual annotation task records."""

from __future__ import annotations

from typing import Any
import re

from libreprimus.visual_annotation.models import VISUAL_NEGATIVE_CONTROL_CLASSES


def build_annotation_pack(
    *,
    visual_observations: list[dict[str, Any]],
    negative_controls: list[dict[str, Any]],
    image_artifacts: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build committed Stage 4C records without inventing coordinates."""

    image_lookup = _build_image_lookup(image_artifacts)
    tasks: list[dict[str, Any]] = []
    cuneiform: list[dict[str, Any]] = []
    dot: list[dict[str, Any]] = []
    delimiter: list[dict[str, Any]] = []
    negative: list[dict[str, Any]] = []

    for observation in visual_observations:
        family = str(observation.get("observation_family", ""))
        if family == "cuneiform_base60":
            task = _base_task(
                observation,
                task_id="stage4c-task-cuneiform-17-13-55-1",
                task_family="cuneiform_base60",
                image_lookup=image_lookup,
                instructions=(
                    "Mark the broad cuneiform candidate region, then record glyph segmentation "
                    "and any alternative sexagesimal readings separately."
                ),
            )
            tasks.append(task)
            cuneiform.append(_cuneiform_candidate(observation, task["task_id"]))
        elif family == "mirrored_three_dot_delimiter":
            suffix = _slug(str(observation.get("observation_id", "delimiter")))
            task = _base_task(
                observation,
                task_id=f"stage4c-task-{suffix}",
                task_family="mirrored_three_dot_delimiter",
                image_lookup=image_lookup,
                instructions=(
                    "Mark the delimiter region only. Do not promote handedness, polarity, or "
                    "reset-boundary meaning from the coordinate annotation."
                ),
            )
            tasks.append(task)
            delimiter.append(_delimiter_task(observation, task["task_id"]))
        elif family == "dot_binary_ambiguity":
            task = _base_task(
                observation,
                task_id="stage4c-task-dot-binary-13-31-ambiguity",
                task_family="dot_pattern_ambiguity",
                image_lookup=image_lookup,
                instructions=(
                    "Annotate dot locations, fill state, ordering assumptions, and polarity. "
                    "Record all plausible readings; do not force 13 or 31."
                ),
            )
            tasks.append(task)
            dot.append(_dot_task(observation, task["task_id"]))
        elif family == "number_square_raw":
            task = _base_task(
                observation,
                task_id="stage4c-task-number-square-raw-reference",
                task_family="number_square_reference",
                image_lookup=image_lookup,
                instructions="Record source and page reference gaps only; do not derive routes.",
            )
            tasks.append(task)

    for control in negative_controls:
        false_positive_class = str(control.get("false_positive_class", ""))
        if false_positive_class not in VISUAL_NEGATIVE_CONTROL_CLASSES:
            continue
        record = _negative_task(control)
        negative.append(record)
        tasks.append(
            {
                "record_type": "visual_annotation_task",
                "task_id": record["task_id"],
                "task_family": "visual_negative_control",
                "source_observation_id": str(control.get("negative_control_id", "")),
                "source_refs": [str(control.get("negative_control_id", ""))],
                "page_refs": [],
                "image_refs": [],
                "page_reference_status": "not_applicable",
                "annotation_status": "needs_human_coordinates",
                "review_status": "negative_control",
                "coordinate_system": "unknown_pending_annotation",
                "instructions": (
                    "Use this false-positive class as a review control. Record coordinates only "
                    "if a future reviewer supplies an exact motif instance."
                ),
                "candidate_summary": str(control.get("description", "")),
                "ambiguity_notes": str(control.get("why_dangerous", "")),
                "template_relative_path": f"site/templates/{record['task_id']}.annotation.yaml",
                "site_page_relative_path": f"site/tasks/{record['task_id']}.html",
                "trusted_as_canonical": False,
                "usable_as_experiment_seed": False,
                "solve_claim": False,
                "notes": "Negative-control annotation task; not evidence for a reading.",
            }
        )

    summary = _summary_record(tasks, cuneiform, dot, delimiter, negative)
    return {
        "tasks": tasks,
        "cuneiform": cuneiform,
        "dot": dot,
        "delimiter": delimiter,
        "negative": negative,
        "summary": summary,
    }


def _base_task(
    observation: dict[str, Any],
    *,
    task_id: str,
    task_family: str,
    image_lookup: dict[str, dict[str, Any]],
    instructions: str,
) -> dict[str, Any]:
    page_refs = [str(item) for item in observation.get("page_refs", [])]
    image_refs = _image_refs_for_page_refs(page_refs, image_lookup)
    if image_refs:
        page_reference_status = "broad_page_reference" if len(image_refs) > 1 else "resolved"
    else:
        page_reference_status = "unresolved" if page_refs else "not_applicable"
    return {
        "record_type": "visual_annotation_task",
        "task_id": task_id,
        "task_family": task_family,
        "source_observation_id": str(observation.get("observation_id", "")),
        "source_refs": [str(observation.get("source_id", ""))],
        "page_refs": page_refs,
        "image_refs": image_refs,
        "page_reference_status": page_reference_status,
        "annotation_status": "needs_human_coordinates",
        "review_status": "human_review_required",
        "coordinate_system": "unknown_pending_annotation",
        "instructions": instructions,
        "candidate_summary": _candidate_summary(observation),
        "ambiguity_notes": str(observation.get("ambiguity_notes", "")),
        "template_relative_path": f"site/templates/{task_id}.annotation.yaml",
        "site_page_relative_path": f"site/tasks/{task_id}.html",
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "solve_claim": False,
        "notes": "Stage 4C review task; coordinates are pending human annotation.",
    }


def _cuneiform_candidate(observation: dict[str, Any], task_id: str) -> dict[str, Any]:
    first = next(iter(observation.get("candidate_readings", [])), {})
    return {
        "record_type": "cuneiform_reading_candidate",
        "candidate_id": "stage4c-cuneiform-candidate-17-13-55-1",
        "task_id": task_id,
        "source_observation_id": str(observation.get("observation_id", "")),
        "page_refs": [str(item) for item in observation.get("page_refs", [])],
        "proposed_reading": list(first.get("value", [])),
        "reading_basis": (
            "Carried forward from Stage 4B as a candidate tuple only; visual segmentation "
            "and coordinates are not verified."
        ),
        "ambiguity_notes": str(observation.get("ambiguity_notes", "")),
        "alternative_readings": [],
        "derived_values": dict(observation.get("derived_values", {})),
        "annotation_status": "needs_human_coordinates",
        "review_status": "human_review_required",
        "coordinate_system": "unknown_pending_annotation",
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "solve_claim": False,
        "notes": "The arithmetic is review metadata only until the glyph reading is accepted.",
    }


def _delimiter_task(observation: dict[str, Any], task_id: str) -> dict[str, Any]:
    return {
        "record_type": "delimiter_annotation",
        "task_id": task_id,
        "source_observation_id": str(observation.get("observation_id", "")),
        "page_refs": [str(item) for item in observation.get("page_refs", [])],
        "delimiter_type": "mirrored_three_dot_variant",
        "orientation": "unknown_pending_annotation",
        "handedness": "unknown_pending_annotation",
        "location_reference": ", ".join(str(item) for item in observation.get("page_refs", [])),
        "reset_boundary_hypothesis": False,
        "ambiguity_notes": str(observation.get("ambiguity_notes", "")),
        "annotation_status": "needs_human_coordinates",
        "review_status": "human_review_required",
        "coordinate_system": "unknown_pending_annotation",
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "solve_claim": False,
        "notes": "Delimiter location task only; reset-boundary hypotheses remain disabled.",
    }


def _dot_task(observation: dict[str, Any], task_id: str) -> dict[str, Any]:
    possible = []
    for reading in observation.get("candidate_readings", []):
        value = reading.get("value")
        if isinstance(value, list):
            possible.extend(value)
    return {
        "record_type": "dot_pattern_annotation",
        "task_id": task_id,
        "source_observation_id": str(observation.get("observation_id", "")),
        "page_refs": [str(item) for item in observation.get("page_refs", [])],
        "dot_count": None,
        "filled_count": None,
        "hollow_count": None,
        "ordering_policy": "unknown_pending_annotation",
        "polarity_policy": "unknown_pending_annotation",
        "possible_readings": sorted({str(item) for item in possible}, key=str),
        "claimed_readings": ["13", "31"],
        "ambiguity_notes": str(observation.get("ambiguity_notes", "")),
        "annotation_status": "needs_human_coordinates",
        "review_status": "negative_control",
        "coordinate_system": "unknown_pending_annotation",
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "solve_claim": False,
        "notes": "13/31 remains ambiguous and unforced until coordinates and ordering are explicit.",
    }


def _negative_task(control: dict[str, Any]) -> dict[str, Any]:
    false_positive_class = str(control.get("false_positive_class", ""))
    task_id = f"stage4c-negative-{_slug(false_positive_class)}"
    return {
        "record_type": "visual_negative_control_annotation",
        "task_id": task_id,
        "source_negative_control_id": str(control.get("negative_control_id", "")),
        "false_positive_class": false_positive_class,
        "why_dangerous": str(control.get("why_dangerous", "")),
        "required_null_control": str(control.get("recommended_use", "")),
        "annotation_status": "needs_human_coordinates",
        "review_status": "negative_control",
        "coordinate_system": "unknown_pending_annotation",
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "solve_claim": False,
        "notes": "Negative-control task preserved for later visual review and null controls.",
    }


def _summary_record(
    tasks: list[dict[str, Any]],
    cuneiform: list[dict[str, Any]],
    dot: list[dict[str, Any]],
    delimiter: list[dict[str, Any]],
    negative: list[dict[str, Any]],
) -> dict[str, Any]:
    unresolved = sum(1 for task in tasks if task.get("page_reference_status") == "unresolved")
    return {
        "record_type": "visual_annotation_pack_summary",
        "summary_id": "stage4c-visual-annotation-pack-summary",
        "stage": "stage-4c",
        "task_count": len(tasks),
        "cuneiform_task_count": len(cuneiform),
        "dot_task_count": len(dot),
        "delimiter_task_count": len(delimiter),
        "negative_control_task_count": len(negative),
        "unresolved_page_reference_count": unresolved,
        "generated_site_path": "experiments/results/visual-annotation/stage4c/site/index.html",
        "generated_template_count": len(tasks),
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "solve_claim": False,
        "raw_outputs_committed": False,
        "generated_outputs_committed": False,
        "notes": "Stage 4C creates review tasks and generated local annotation workspace only.",
    }


def _candidate_summary(observation: dict[str, Any]) -> str:
    readings = observation.get("candidate_readings", [])
    if not readings:
        return ""
    return "; ".join(
        f"{reading.get('reading_id', 'reading')}: {reading.get('value')}" for reading in readings
    )


def _build_image_lookup(image_artifacts: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for artifact in image_artifacts:
        image_id = str(artifact.get("image_id", ""))
        file_name = str(artifact.get("file_name", ""))
        if image_id:
            lookup[image_id] = artifact
        page_no = _page_number_from_text(file_name)
        if page_no is not None:
            lookup[f"page-{page_no}"] = artifact
    return lookup


def _image_refs_for_page_refs(page_refs: list[str], image_lookup: dict[str, dict[str, Any]]) -> list[str]:
    refs: list[str] = []
    for page_ref in page_refs:
        for page_key in _page_keys(page_ref):
            artifact = image_lookup.get(page_key)
            if artifact:
                refs.append(str(artifact.get("image_id", page_key)))
    return sorted(set(refs), key=_natural_key)


def _page_keys(page_ref: str) -> list[str]:
    ranges = re.findall(r"pages?-(\d+)-(\d+)", page_ref)
    keys: list[str] = []
    for start, end in ranges:
        keys.extend(f"page-{number}" for number in range(int(start), int(end) + 1))
    singles = re.findall(r"page-(\d+)", page_ref)
    keys.extend(f"page-{number}" for number in singles)
    return keys


def _page_number_from_text(value: str) -> int | None:
    match = re.search(r"(\d+)", value)
    if not match:
        return None
    return int(match.group(1))


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _natural_key(value: str) -> tuple[int, str]:
    number = _page_number_from_text(value)
    return (-1 if number is None else number, value)
