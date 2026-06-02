import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from test_stage5cw_common import STAGE5CW_RECORDS, STAGE5CW_SCHEMAS, ensure_stage5cw_built


def test_stage5cw_schemas_validate_records() -> None:
    ensure_stage5cw_built()

    for schema_path in STAGE5CW_SCHEMAS:
        assert Path(schema_path).is_file(), schema_path

    for record_path in STAGE5CW_RECORDS:
        payload = yaml.safe_load(Path(record_path).read_text(encoding="utf-8"))
        schema = json.loads(Path(payload["schema"]).read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(payload)


def test_stage5cw_schema_rejects_solve_claim_and_cuda() -> None:
    ensure_stage5cw_built()
    payload = yaml.safe_load(Path("data/project-state/stage5cw-summary.yaml").read_text())
    schema = json.loads(Path(payload["schema"]).read_text())

    bad = dict(payload)
    bad["solve_claim"] = True
    assert list(Draft202012Validator(schema).iter_errors(bad))

    bad = dict(payload)
    bad["cuda_execution_performed"] = True
    assert list(Draft202012Validator(schema).iter_errors(bad))
