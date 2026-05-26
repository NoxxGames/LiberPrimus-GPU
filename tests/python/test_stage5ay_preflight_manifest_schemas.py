from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def test_stage5ay_schemas_validate_records() -> None:
    pairs = [
        ("schemas/token-block/preflight-source-inputs-v0.schema.json", "data/token-block/stage5ay-preflight-source-inputs.yaml"),
        ("schemas/token-block/preflight-design-policy-v0.schema.json", "data/token-block/stage5ay-preflight-design-policy.yaml"),
        ("schemas/token-block/branch-eligibility-policy-v0.schema.json", "data/token-block/stage5ay-branch-eligibility-policy.yaml"),
        ("schemas/token-block/bounded-variant-family-manifest-v0.schema.json", "data/token-block/stage5ay-bounded-variant-family-manifest.yaml"),
        ("schemas/token-block/null-control-family-manifest-v0.schema.json", "data/token-block/stage5ay-null-control-family-manifest.yaml"),
        ("schemas/token-block/alphabet-control-manifest-v0.schema.json", "data/token-block/stage5ay-alphabet-control-manifest.yaml"),
        ("schemas/token-block/reading-order-control-manifest-v0.schema.json", "data/token-block/stage5ay-reading-order-control-manifest.yaml"),
        ("schemas/token-block/page-split-control-manifest-v0.schema.json", "data/token-block/stage5ay-page-split-control-manifest.yaml"),
        ("schemas/token-block/source-control-manifest-v0.schema.json", "data/token-block/stage5ay-source-control-manifest.yaml"),
        ("schemas/token-block/branch-count-budget-v0.schema.json", "data/token-block/stage5ay-branch-count-budget.yaml"),
        ("schemas/token-block/future-result-schema-preview-v0.schema.json", "data/token-block/stage5ay-future-result-schema-preview.yaml"),
        ("schemas/token-block/execution-gates-v0.schema.json", "data/token-block/stage5ay-execution-gates.yaml"),
        ("schemas/token-block/dwh-preflight-context-v0.schema.json", "data/token-block/stage5ay-dwh-preflight-context.yaml"),
        ("schemas/token-block/stage5ay-guardrail-v0.schema.json", "data/token-block/stage5ay-guardrail.yaml"),
        ("schemas/project-state/stage5ay-summary-v0.schema.json", "data/project-state/stage5ay-summary.yaml"),
    ]
    for schema_path, record_path in pairs:
        schema = yaml.safe_load(Path(schema_path).read_text(encoding="utf-8"))
        payload = yaml.safe_load(Path(record_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(payload)
