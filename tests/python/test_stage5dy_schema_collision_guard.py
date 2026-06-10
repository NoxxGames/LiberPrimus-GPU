from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from test_stage5dy_common import ensure_stage5dy_built, load_yaml


def test_stage5dy_summary_schema_rejects_solve_claim() -> None:
    ensure_stage5dy_built()
    schema = json.loads(Path("schemas/project-state/stage5dy-summary-v0.schema.json").read_text(encoding="utf-8"))
    payload = load_yaml("data/project-state/stage5dy-summary.yaml")
    payload["solve_claim"] = True

    assert list(Draft202012Validator(schema).iter_errors(payload))


def test_stage5dy_summary_schema_rejects_execution() -> None:
    ensure_stage5dy_built()
    schema = json.loads(Path("schemas/project-state/stage5dy-summary-v0.schema.json").read_text(encoding="utf-8"))
    payload = load_yaml("data/project-state/stage5dy-summary.yaml")
    payload["execution_performed"] = True

    assert list(Draft202012Validator(schema).iter_errors(payload))
