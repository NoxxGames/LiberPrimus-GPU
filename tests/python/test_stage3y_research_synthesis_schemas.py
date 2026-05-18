from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from libreprimus.paths import repo_root
from libreprimus.research_synthesis.loader import load_all_record_sets
from libreprimus.research_synthesis.models import RECORD_SET_SPECS
from libreprimus.research_synthesis.validation import validate_research_synthesis


def test_stage3y_research_schemas_validate_records() -> None:
    records_by_key = load_all_record_sets(repo_root() / "data/research")

    for spec in RECORD_SET_SPECS:
        schema = json.loads((repo_root() / spec.schema_path).read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for record in records_by_key[spec.key]:
            errors = list(validator.iter_errors(record))
            assert errors == []


def test_stage3y_research_data_records_validate() -> None:
    _summary, errors = validate_research_synthesis(
        data_dir=repo_root() / "data/research",
        staged_plan=repo_root() / "docs/roadmap/staged-plan.md",
    )

    assert errors == []
