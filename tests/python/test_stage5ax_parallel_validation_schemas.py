from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def _load_yaml(path: str) -> object:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def _validator(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads((ROOT / path).read_text(encoding="utf-8")))


def test_stage5ax_schemas_validate_committed_records() -> None:
    pairs = [
        ("schemas/ci/parallel-validation-plan-v0.schema.json", "data/ci/stage5ax-parallel-validation-plan.yaml"),
        ("schemas/ci/parallel-command-registry-v0.schema.json", "data/ci/stage5ax-parallel-command-registry.yaml"),
        ("schemas/ci/parallel-run-policy-v0.schema.json", "data/ci/stage5ax-parallel-run-policy.yaml"),
        ("schemas/ci/parallel-validation-run-summary-v0.schema.json", "data/ci/stage5ax-parallel-validation-run-summary.yaml"),
        ("schemas/ci/parallel-validation-safety-audit-v0.schema.json", "data/ci/stage5ax-parallel-validation-safety-audit.yaml"),
        ("schemas/ci/pytest-shard-plan-v0.schema.json", "data/ci/stage5ax-pytest-shard-plan.yaml"),
        ("schemas/ci/stage5ax-guardrail-v0.schema.json", "data/ci/stage5ax-guardrail.yaml"),
        ("schemas/project-state/stage5ax-summary-v0.schema.json", "data/project-state/stage5ax-summary.yaml"),
    ]
    for schema_path, data_path in pairs:
        _validator(schema_path).validate(_load_yaml(data_path))
