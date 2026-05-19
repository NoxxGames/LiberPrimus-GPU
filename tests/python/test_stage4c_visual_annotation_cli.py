from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image
from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage4c_visual_annotation_cli_build_and_validate(tmp_path: Path) -> None:
    visual = tmp_path / "visual.yaml"
    negative = tmp_path / "negative.yaml"
    artifacts = tmp_path / "artifacts.jsonl"
    locks = tmp_path / "locks.jsonl"
    image_dir = tmp_path / "images"
    out_dir = tmp_path / "out"
    image_dir.mkdir()
    Image.new("RGB", (64, 64), "white").save(image_dir / "39.jpg")
    _write_records(
        visual,
        [
            {
                "observation_id": "stage4b-cuneiform-17-13-55-1",
                "observation_family": "cuneiform_base60",
                "source_id": "source",
                "page_refs": ["pages-33-39-cuneiform-cluster"],
                "candidate_readings": [{"reading_id": "r", "value": [17, 13, 55, 1]}],
                "derived_values": {"pair_55_1_base60": 3301},
                "ambiguity_notes": "needs coordinates",
            },
            {
                "observation_id": "stage4b-dot-binary-13-31-ambiguity",
                "observation_family": "dot_binary_ambiguity",
                "source_id": "source",
                "page_refs": ["page-39"],
                "candidate_readings": [{"reading_id": "r", "value": [13, 31]}],
                "derived_values": {},
                "ambiguity_notes": "ambiguous",
            }
        ],
    )
    _write_records(
        negative,
        [
            {
                "negative_control_id": "stage4b-negative-braille_dot_readings",
                "false_positive_class": "braille_dot_readings",
                "description": "Braille dot readings",
                "why_dangerous": "too many readings",
                "recommended_use": "null control",
            },
            {
                "negative_control_id": "stage4b-negative-constellation_dot_readings",
                "false_positive_class": "constellation_dot_readings",
                "description": "Constellation dot readings",
                "why_dangerous": "resemblance only",
                "recommended_use": "null control",
            },
            {
                "negative_control_id": "stage4b-negative-forced_13_31_dot_values",
                "false_positive_class": "forced_13_31_dot_values",
                "description": "Forced 13/31 dot readings",
                "why_dangerous": "anchor choices",
                "recommended_use": "ambiguity table",
            },
        ],
    )
    artifacts.write_text(
        '{"image_id":"liber-primus-page-image-39","file_name":"39.jpg","relative_path":"third_party/LiberPrimusPages/39.jpg","width":64,"height":64}\n',
        encoding="utf-8",
    )
    locks.write_text("", encoding="utf-8")

    task = tmp_path / "tasks.yaml"
    cuneiform = tmp_path / "cuneiform.yaml"
    dot = tmp_path / "dot.yaml"
    delimiter = tmp_path / "delimiter.yaml"
    neg = tmp_path / "neg.yaml"
    summary = tmp_path / "summary.yaml"

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "visual-annotation",
            "build",
            "--visual-observations",
            str(visual),
            "--negative-controls",
            str(negative),
            "--image-artifacts",
            str(artifacts),
            "--image-locks",
            str(locks),
            "--image-dir",
            str(image_dir),
            "--out-dir",
            str(out_dir),
            "--task-out",
            str(task),
            "--cuneiform-out",
            str(cuneiform),
            "--dot-out",
            str(dot),
            "--delimiter-out",
            str(delimiter),
            "--negative-out",
            str(neg),
            "--summary-out",
            str(summary),
        ],
    )
    assert result.exit_code == 0, result.output

    result = runner.invoke(
        app,
        [
            "visual-annotation",
            "validate",
            "--task",
            str(task),
            "--cuneiform",
            str(cuneiform),
            "--dot",
            str(dot),
            "--delimiter",
            str(delimiter),
            "--negative",
            str(neg),
            "--summary",
            str(summary),
        ],
    )
    assert result.exit_code == 0, result.output
    assert "visual_annotation_valid=true" in result.output


def _write_records(path: Path, records: list[dict]) -> None:
    path.write_text(
        yaml.safe_dump({"record_set_id": path.stem, "schema": "", "records": records}, sort_keys=False),
        encoding="utf-8",
    )
