from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/visual/visual-annotation-task-v0.schema.json",
    "schemas/visual/visual-region-annotation-v0.schema.json",
    "schemas/visual/cuneiform-reading-candidate-v0.schema.json",
    "schemas/visual/dot-pattern-annotation-v0.schema.json",
    "schemas/visual/delimiter-annotation-v0.schema.json",
    "schemas/visual/visual-negative-control-annotation-v0.schema.json",
    "schemas/visual/visual-annotation-pack-summary-v0.schema.json",
]


def test_stage4c_visual_annotation_schemas_validate() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4c_committed_records_have_no_solve_claim() -> None:
    text = Path("data/observations/visual/stage4c-visual-annotation-tasks.yaml").read_text(
        encoding="utf-8"
    )

    assert "solve_claim: true" not in text
    assert "usable_as_experiment_seed: true" not in text
