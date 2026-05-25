from pathlib import Path

import jsonschema
import yaml


def _load(path: str):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _schema(path: str):
    return jsonschema.Draft202012Validator(_load(path))


def test_stage5at_schemas_validate_committed_records() -> None:
    pairs = [
        ("schemas/token-block/case-review-policy-v0.schema.json", "data/token-block/stage5at-case-review-policy.yaml"),
        ("schemas/token-block/case-review-challenge-record-v0.schema.json", "data/token-block/stage5at-case-review-challenge-set.yaml"),
        ("schemas/token-block/canonical-transcription-challenge-record-v0.schema.json", "data/token-block/stage5at-canonical-transcription-challenge-set.yaml"),
        ("schemas/token-block/case-review-crop-manifest-v0.schema.json", "data/token-block/stage5at-case-review-crop-manifest.yaml"),
        ("schemas/token-block/human-review-decision-template-v0.schema.json", "data/token-block/stage5at-human-review-decision-template.yaml"),
        ("schemas/token-block/case-review-pack-manifest-v0.schema.json", "data/token-block/stage5at-case-review-pack-manifest.yaml"),
        ("schemas/token-block/variant-classifier-repair-summary-v0.schema.json", "data/token-block/stage5at-variant-classifier-repair-summary.yaml"),
        ("schemas/token-block/doc-drift-repair-summary-v0.schema.json", "data/token-block/stage5at-doc-drift-repair-summary.yaml"),
        ("schemas/token-block/null-control-case-update-v0.schema.json", "data/token-block/stage5at-null-control-case-update.yaml"),
        ("schemas/token-block/dwh-case-context-v0.schema.json", "data/token-block/stage5at-dwh-case-context.yaml"),
        ("schemas/token-block/stage5at-guardrail-v0.schema.json", "data/token-block/stage5at-guardrail.yaml"),
        ("schemas/project-state/stage5at-summary-v0.schema.json", "data/project-state/stage5at-summary.yaml"),
        ("schemas/project-state/stage5at-summary-v0.schema.json", "data/project-state/stage5at-next-stage-decision.yaml"),
    ]
    for schema_path, record_path in pairs:
        _schema(schema_path).validate(_load(record_path))
