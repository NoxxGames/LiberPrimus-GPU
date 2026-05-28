from jsonschema import Draft202012Validator

from test_stage5bk_common import load_json, load_yaml


SCHEMA_TO_DATA = [
    ("schemas/historical-route/stage5bk-iddqd-v2-local-source-root-v0.schema.json", "data/historical-route/stage5bk-iddqd-v2-local-source-root.yaml"),
    ("schemas/historical-route/stage5bk-iddqd-v2-tree-summary-v0.schema.json", "data/historical-route/stage5bk-iddqd-v2-tree-summary.yaml"),
    ("schemas/historical-route/stage5bk-iddqd-v2-source-candidate-index-v0.schema.json", "data/historical-route/stage5bk-iddqd-v2-source-candidate-index.yaml"),
    ("schemas/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock-v0.schema.json", "data/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock.yaml"),
    ("schemas/historical-route/stage5bk-iddqd-v2-transcription-source-lock-v0.schema.json", "data/historical-route/stage5bk-iddqd-v2-transcription-source-lock.yaml"),
    ("schemas/historical-route/stage5bk-iddqd-v2-translation-key-lineage-v0.schema.json", "data/historical-route/stage5bk-iddqd-v2-translation-key-lineage.yaml"),
    ("schemas/historical-route/stage5bk-iddqd-v2-positive-control-context-v0.schema.json", "data/historical-route/stage5bk-iddqd-v2-positive-control-context.yaml"),
    ("schemas/historical-route/stage5bk-iddqd-v2-source-gap-register-v0.schema.json", "data/historical-route/stage5bk-iddqd-v2-source-gap-register.yaml"),
    ("schemas/historical-route/stage5bk-historical-planning-constraint-policy-v0.schema.json", "data/historical-route/stage5bk-historical-planning-constraint-policy.yaml"),
    ("schemas/historical-route/stage5bk-historical-family-planning-status-v0.schema.json", "data/historical-route/stage5bk-historical-family-planning-status.yaml"),
    ("schemas/historical-route/stage5bk-authenticity-gate-integration-v0.schema.json", "data/historical-route/stage5bk-authenticity-gate-integration.yaml"),
    ("schemas/historical-route/stage5bk-stego-positive-control-constraint-integration-v0.schema.json", "data/historical-route/stage5bk-stego-positive-control-constraint-integration.yaml"),
    ("schemas/historical-route/stage5bk-numeric-and-magic-square-constraint-integration-v0.schema.json", "data/historical-route/stage5bk-numeric-and-magic-square-constraint-integration.yaml"),
    ("schemas/historical-route/stage5bk-book-code-and-text-reference-constraint-integration-v0.schema.json", "data/historical-route/stage5bk-book-code-and-text-reference-constraint-integration.yaml"),
    ("schemas/historical-route/stage5bk-network-byte-channel-constraint-integration-v0.schema.json", "data/historical-route/stage5bk-network-byte-channel-constraint-integration.yaml"),
    ("schemas/historical-route/stage5bk-liber-primus-transcription-constraint-integration-v0.schema.json", "data/historical-route/stage5bk-liber-primus-transcription-constraint-integration.yaml"),
    ("schemas/historical-route/stage5bk-dwh-quarantine-reaffirmation-v0.schema.json", "data/historical-route/stage5bk-dwh-quarantine-reaffirmation.yaml"),
    ("schemas/historical-route/stage5bk-source-gap-severity-register-v0.schema.json", "data/historical-route/stage5bk-source-gap-severity-register.yaml"),
    ("schemas/historical-route/stage5bk-stage5bj-crosswalk-review-and-errata-v0.schema.json", "data/historical-route/stage5bk-stage5bj-crosswalk-review-and-errata.yaml"),
    ("schemas/historical-route/stage5bk-guardrail-v0.schema.json", "data/historical-route/stage5bk-guardrail.yaml"),
    ("schemas/token-block/stage5bk-token-block-historical-constraint-update-v0.schema.json", "data/token-block/stage5bk-token-block-historical-constraint-update.yaml"),
    ("schemas/token-block/stage5bk-2014-surface-and-page49-context-integration-v0.schema.json", "data/token-block/stage5bk-2014-surface-and-page49-context-integration.yaml"),
    ("schemas/token-block/stage5bk-page49-51-string4-crosswalk-v0.schema.json", "data/token-block/stage5bk-page49-51-string4-crosswalk.yaml"),
    ("schemas/token-block/stage5bk-token-block-lineage-preservation-v0.schema.json", "data/token-block/stage5bk-token-block-lineage-preservation.yaml"),
    ("schemas/token-block/stage5bk-future-dry-run-planning-impact-v0.schema.json", "data/token-block/stage5bk-future-dry-run-planning-impact.yaml"),
    ("schemas/source-harvester/stage5bk-local-source-root-integration-summary-v0.schema.json", "data/source-harvester/stage5bk-local-source-root-integration-summary.yaml"),
    ("schemas/source-harvester/stage5bk-codex-handoff-policy-correction-v0.schema.json", "data/source-harvester/stage5bk-codex-handoff-policy-correction.yaml"),
    ("schemas/project-state/stage5bk-summary-v0.schema.json", "data/project-state/stage5bk-summary.yaml"),
    ("schemas/project-state/stage5bk-next-stage-decision-v0.schema.json", "data/project-state/stage5bk-next-stage-decision.yaml"),
]


def test_stage5bk_yaml_records_validate_against_schemas() -> None:
    for schema_path, data_path in SCHEMA_TO_DATA:
        Draft202012Validator(load_json(schema_path)).validate(load_yaml(data_path))
