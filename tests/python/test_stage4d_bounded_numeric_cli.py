from __future__ import annotations

from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.source_lock_triage.disabled_manifests import write_disabled_manifests


def test_stage4d_cli_run_and_validate_on_synthetic_records(tmp_path: Path) -> None:
    manifest_dir = tmp_path / "manifests"
    write_disabled_manifests(manifest_dir)
    visual = tmp_path / "visual.yaml"
    tasks = tmp_path / "tasks.yaml"
    cuneiform = tmp_path / "cuneiform.yaml"
    dot = tmp_path / "dot.yaml"
    delimiter = tmp_path / "delimiter.yaml"
    negative = tmp_path / "negative.yaml"
    out_dir = tmp_path / "out"

    _write_records(
        visual,
        [
            {
                "observation_id": "stage4b-onion7-number-square-raw",
                "observation_family": "number_square_raw",
                "candidate_readings": [{"value": "pending_source_lock"}],
            }
        ],
    )
    _write_records(tasks, [])
    _write_records(
        cuneiform,
        [
            {
                "candidate_id": "c",
                "annotation_status": "needs_human_coordinates",
                "review_status": "human_review_required",
                "coordinate_system": "unknown_pending_annotation",
                "usable_as_experiment_seed": False,
            }
        ],
    )
    _write_records(
        dot,
        [
            {
                "task_id": "dot",
                "possible_readings": ["13", "31", "7"],
                "claimed_readings": ["13", "31"],
                "ordering_policy": "unknown_pending_annotation",
                "polarity_policy": "unknown_pending_annotation",
            }
        ],
    )
    _write_records(
        delimiter,
        [
            {
                "task_id": "delimiter",
                "delimiter_type": "mirrored_three_dot_variant",
                "orientation": "unknown_pending_annotation",
                "handedness": "unknown_pending_annotation",
                "coordinate_system": "unknown_pending_annotation",
                "annotation_status": "needs_human_coordinates",
            }
        ],
    )
    _write_records(
        negative,
        [
            {
                "task_id": "braille",
                "source_negative_control_id": "stage4b-negative-braille_dot_readings",
                "false_positive_class": "braille_dot_readings",
                "why_dangerous": "too many readings",
                "required_null_control": "visual nulls",
            }
        ],
    )

    runner = CliRunner()
    run_result = runner.invoke(
        app,
        [
            "bounded-numeric",
            "run",
            "--manifest-dir",
            str(manifest_dir),
            "--stage4b-visual",
            str(visual),
            "--stage4c-tasks",
            str(tasks),
            "--stage4c-cuneiform",
            str(cuneiform),
            "--stage4c-dot",
            str(dot),
            "--stage4c-delimiter",
            str(delimiter),
            "--stage4c-negative",
            str(negative),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert run_result.exit_code == 0, run_result.output
    assert "cuneiform_deferred=true" in run_result.output
    assert "cookie_pack_deferred=true" in run_result.output

    validate_result = runner.invoke(
        app,
        ["bounded-numeric", "validate", "--results-dir", str(out_dir)],
    )
    assert validate_result.exit_code == 0, validate_result.output
    assert "bounded_numeric_valid=true" in validate_result.output


def _write_records(path: Path, records: list[dict]) -> None:
    path.write_text(
        yaml.safe_dump({"record_set_id": path.stem, "schema": "", "records": records}, sort_keys=False),
        encoding="utf-8",
    )
