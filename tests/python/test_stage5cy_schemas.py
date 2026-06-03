from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from test_stage5cy_common import STAGE5CY_RECORDS, STAGE5CY_SCHEMAS, ensure_stage5cy_built, load_yaml


def test_stage5cy_schemas_validate_all_records() -> None:
    ensure_stage5cy_built()
    for record_path, schema_path in zip(STAGE5CY_RECORDS, STAGE5CY_SCHEMAS, strict=True):
        payload = load_yaml(record_path)
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(payload)


def test_stage5cy_summary_schema_rejects_solve_cuda_and_generated_publication() -> None:
    ensure_stage5cy_built()
    payload = load_yaml("data/project-state/stage5cy-summary.yaml")
    schema = json.loads(
        Path("schemas/project-state/stage5cy-summary-v0.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)

    for field in ["solve_claim", "cuda_execution_performed", "generated_outputs_committed"]:
        bad = copy.deepcopy(payload)
        bad[field] = True
        try:
            validator.validate(bad)
        except ValidationError:
            continue
        raise AssertionError(f"{field} must be rejected when true")


def test_stage5cy_summary_schema_rejects_selected_option_id() -> None:
    ensure_stage5cy_built()
    payload = load_yaml("data/project-state/stage5cy-summary.yaml")
    schema = json.loads(
        Path("schemas/project-state/stage5cy-summary-v0.schema.json").read_text(encoding="utf-8")
    )
    payload["selected_option_id"] = "prepare_real_operator_approval_record"
    try:
        Draft202012Validator(schema).validate(payload)
    except ValidationError:
        return
    raise AssertionError("selected_option_id must remain null")
