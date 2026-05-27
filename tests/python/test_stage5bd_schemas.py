from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def test_stage5bd_schemas_validate_committed_records() -> None:
    pairs = {
        "schemas/token-block/dry-run-policy-v0.schema.json": "data/token-block/stage5bd-dry-run-policy.yaml",
        "schemas/token-block/active-manifest-lock-v0.schema.json": "data/token-block/stage5bd-active-manifest-lock.yaml",
        "schemas/token-block/run-plan-id-policy-v0.schema.json": "data/token-block/stage5bd-run-plan-id-policy.yaml",
        "schemas/token-block/dry-run-plan-manifest-v0.schema.json": "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
        "schemas/token-block/run-plan-id-registry-v0.schema.json": "data/token-block/stage5bd-run-plan-id-registry.yaml",
        "schemas/token-block/future-result-path-policy-v0.schema.json": "data/token-block/stage5bd-future-result-path-policy.yaml",
        "schemas/token-block/future-result-path-validation-v0.schema.json": "data/token-block/stage5bd-future-result-path-validation.yaml",
        "schemas/token-block/branch-family-plan-counters-v0.schema.json": "data/token-block/stage5bd-branch-family-plan-counters.yaml",
        "schemas/token-block/null-control-plan-counters-v0.schema.json": "data/token-block/stage5bd-null-control-plan-counters.yaml",
        "schemas/token-block/control-family-plan-counters-v0.schema.json": "data/token-block/stage5bd-control-family-plan-counters.yaml",
        "schemas/token-block/dry-run-report-schema-v0.schema.json": "data/token-block/stage5bd-dry-run-report-schema.yaml",
        "schemas/token-block/fixture-result-example-policy-v0.schema.json": "data/token-block/stage5bd-fixture-result-example-policy.yaml",
        "schemas/token-block/fixture-dry-run-records-v0.schema.json": "data/token-block/stage5bd-fixture-dry-run-records.yaml",
        "schemas/token-block/execution-gate-dry-run-validation-v0.schema.json": "data/token-block/stage5bd-execution-gate-dry-run-validation.yaml",
        "schemas/token-block/no-byte-stream-proof-v0.schema.json": "data/token-block/stage5bd-no-byte-stream-proof.yaml",
        "schemas/token-block/validation-evidence-consolidation-v0.schema.json": "data/token-block/stage5bd-stage5bb-validation-evidence-consolidation.yaml",
        "schemas/token-block/archive-marker-policy-v0.schema.json": "data/token-block/stage5bd-archive-marker-policy.yaml",
        "schemas/token-block/dwh-dry-run-context-v0.schema.json": "data/token-block/stage5bd-dwh-dry-run-context.yaml",
        "schemas/token-block/stage5bd-guardrail-v0.schema.json": "data/token-block/stage5bd-guardrail.yaml",
        "schemas/project-state/archive-review-marker-v0.schema.json": "data/project-state/stage5bd-archive-review-marker.yaml",
        "schemas/project-state/stage5bd-summary-v0.schema.json": "data/project-state/stage5bd-summary.yaml",
    }

    for schema_path, record_path in pairs.items():
        schema = yaml.safe_load(Path(schema_path).read_text(encoding="utf-8"))
        payload = yaml.safe_load(Path(record_path).read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(payload)
