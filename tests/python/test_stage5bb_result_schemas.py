from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def test_stage5bb_schemas_validate_committed_records() -> None:
    pairs = {
        "schemas/token-block/manifest-precedence-policy-v0.schema.json": "data/token-block/stage5bb-manifest-precedence-policy.yaml",
        "schemas/token-block/legacy-pointer-audit-v0.schema.json": "data/token-block/stage5bb-legacy-pointer-audit.yaml",
        "schemas/token-block/manifest-reference-validation-v0.schema.json": "data/token-block/stage5bb-manifest-reference-validation.yaml",
        "schemas/token-block/branch-eligibility-reference-validation-v0.schema.json": "data/token-block/stage5bb-branch-eligibility-reference-validation.yaml",
        "schemas/token-block/loader-scaffold-policy-v0.schema.json": "data/token-block/stage5bb-loader-scaffold-policy.yaml",
        "schemas/token-block/runner-scaffold-manifest-v0.schema.json": "data/token-block/stage5bb-runner-scaffold-manifest.yaml",
        "schemas/token-block/dry-run-plan-preview-v0.schema.json": "data/token-block/stage5bb-dry-run-plan-preview.yaml",
        "schemas/token-block/branch-counter-summary-v0.schema.json": "data/token-block/stage5bb-branch-counter-summary.yaml",
        "schemas/token-block/family-enumeration-summary-v0.schema.json": "data/token-block/stage5bb-family-enumeration-summary.yaml",
        "schemas/token-block/execution-gate-enforcement-policy-v0.schema.json": "data/token-block/stage5bb-execution-gate-enforcement-policy.yaml",
        "schemas/token-block/execution-gate-validation-v0.schema.json": "data/token-block/stage5bb-execution-gate-validation.yaml",
        "schemas/token-block/result-schema-fixture-policy-v0.schema.json": "data/token-block/stage5bb-result-schema-fixture-policy.yaml",
        "schemas/token-block/fixture-result-schema-records-v0.schema.json": "data/token-block/stage5bb-fixture-result-schema-records.yaml",
        "schemas/token-block/validation-evidence-index-v0.schema.json": "data/token-block/stage5bb-validation-evidence-index.yaml",
        "schemas/token-block/no-execution-proof-v0.schema.json": "data/token-block/stage5bb-no-execution-proof.yaml",
        "schemas/token-block/dwh-runner-context-v0.schema.json": "data/token-block/stage5bb-dwh-runner-context.yaml",
        "schemas/token-block/stage5bb-guardrail-v0.schema.json": "data/token-block/stage5bb-guardrail.yaml",
        "schemas/project-state/stage5bb-summary-v0.schema.json": "data/project-state/stage5bb-summary.yaml",
    }

    for schema_path, record_path in pairs.items():
        schema = yaml.safe_load(Path(schema_path).read_text())
        payload = yaml.safe_load(Path(record_path).read_text())
        Draft202012Validator(schema).validate(payload)
