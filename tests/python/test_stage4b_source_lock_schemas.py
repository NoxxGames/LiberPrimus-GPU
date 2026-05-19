from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMA_FILES = [
    "schemas/history/stage4b-source-triage-record-v0.schema.json",
    "schemas/history/source-health-record-v0.schema.json",
    "schemas/visual/stage4b-visual-observation-record-v0.schema.json",
    "schemas/research/negative-control-record-v1.schema.json",
    "schemas/experiments/stage4b-disabled-experiment-manifest-v0.schema.json",
]


def test_stage4b_schemas_parse() -> None:
    for relative in SCHEMA_FILES:
        schema = json.loads(Path(relative).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4b_disabled_manifest_schema_blocks_execution() -> None:
    schema = json.loads(
        Path("schemas/experiments/stage4b-disabled-experiment-manifest-v0.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    payload = {
        "record_type": "stage4b_disabled_experiment_manifest",
        "manifest_id": "exp_stage4b_test",
        "title": "test",
        "purpose": "synthetic disabled manifest",
        "source_basis": ["synthetic"],
        "candidate_count_upper_bound": 1,
        "execution_enabled": False,
        "cuda_enabled": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
        "status": "disabled_needs_annotation",
        "notes": "test",
    }

    assert list(validator.iter_errors(payload)) == []
    payload["execution_enabled"] = True
    assert list(validator.iter_errors(payload))
