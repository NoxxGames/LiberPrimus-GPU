from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5dj_common import (
    ROOT,
    STAGE5DJ_RECORDS,
    STAGE5DJ_SCHEMAS,
    ensure_stage5dj_built,
    load_yaml,
)


def test_stage5dj_schemas_validate_records() -> None:
    ensure_stage5dj_built()

    for schema_path in STAGE5DJ_SCHEMAS:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record_path = schema_path.replace("schemas/", "data/").replace(
            "-v0.schema.json", ".yaml"
        )
        record = load_yaml(record_path)
        assert list(Draft202012Validator(schema).iter_errors(record)) == []


def test_stage5dj_schema_rejects_execution_solve_and_music_selection() -> None:
    ensure_stage5dj_built()
    schema = json.loads(
        (ROOT / "schemas/project-state/stage5dj-summary-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )

    for field in [
        "solve_claim",
        "execution_allowed",
        "audio_stego_performed_now",
        "music_pivot_selected_now",
        "target_priority_decision_created_now",
        "generated_outputs_committed",
    ]:
        record = load_yaml("data/project-state/stage5dj-summary.yaml")
        record[field] = True
        assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage5dj_record_and_schema_lists_are_populated() -> None:
    ensure_stage5dj_built()

    assert len(STAGE5DJ_RECORDS) == 29
    assert len(STAGE5DJ_SCHEMAS) == len(STAGE5DJ_RECORDS)
