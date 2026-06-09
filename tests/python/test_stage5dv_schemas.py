from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from libreprimus.token_block.stage5dv import DATA_PATHS, SCHEMA_BY_DATA_KEY, SCHEMA_PATHS
from test_stage5dv_common import ensure_stage5dv_built, load_yaml


def test_stage5dv_schema_files_validate_records() -> None:
    ensure_stage5dv_built()
    for key, record_path in DATA_PATHS.items():
        schema_path = SCHEMA_PATHS[SCHEMA_BY_DATA_KEY[key]]
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(load_yaml(record_path))


def test_stage5dv_summary_schema_rejects_opened_gates() -> None:
    ensure_stage5dv_built()
    schema = json.loads(SCHEMA_PATHS["summary"].read_text(encoding="utf-8"))
    record = load_yaml(DATA_PATHS["summary"])
    record["solve_claim"] = True
    record["cuda_execution_performed"] = True
    record["generated_outputs_committed"] = True
    errors = list(Draft202012Validator(schema).iter_errors(record))
    assert len(errors) >= 3
