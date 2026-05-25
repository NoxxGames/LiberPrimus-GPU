from pathlib import Path

import jsonschema
import yaml


def _load(path: str):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_stage5au_schemas_validate_committed_records() -> None:
    pairs = [
        ("schemas/token-block/review-pack-usability-audit-v0.schema.json", "data/token-block/stage5au-review-pack-usability-audit.yaml"),
        ("schemas/token-block/crop-geometry-policy-v0.schema.json", "data/token-block/stage5au-crop-geometry-policy.yaml"),
        ("schemas/token-block/crop-quality-diagnostics-v0.schema.json", "data/token-block/stage5au-crop-quality-diagnostics.yaml"),
        ("schemas/token-block/case-review-challenge-set-v2-v0.schema.json", "data/token-block/stage5au-case-review-challenge-set-v2.yaml"),
        ("schemas/token-block/canonical-transcription-challenge-set-v2-v0.schema.json", "data/token-block/stage5au-canonical-transcription-challenge-set-v2.yaml"),
        ("schemas/token-block/review-pack-v2-manifest-v0.schema.json", "data/token-block/stage5au-review-pack-v2-manifest.yaml"),
        ("schemas/token-block/review-pack-v2-ui-coverage-v0.schema.json", "data/token-block/stage5au-review-pack-v2-ui-coverage.yaml"),
        ("schemas/token-block/human-review-decision-template-v2-v0.schema.json", "data/token-block/stage5au-human-review-decision-template-v2.yaml"),
        ("schemas/token-block/null-control-review-pack-update-v0.schema.json", "data/token-block/stage5au-null-control-review-pack-update.yaml"),
        ("schemas/token-block/dwh-review-pack-context-v0.schema.json", "data/token-block/stage5au-dwh-review-pack-context.yaml"),
        ("schemas/token-block/stage5au-guardrail-v0.schema.json", "data/token-block/stage5au-guardrail.yaml"),
        ("schemas/project-state/stage5au-summary-v0.schema.json", "data/project-state/stage5au-summary.yaml"),
        ("schemas/project-state/stage5au-summary-v0.schema.json", "data/project-state/stage5au-next-stage-decision.yaml"),
    ]
    for schema_path, record_path in pairs:
        jsonschema.Draft202012Validator(_load(schema_path)).validate(_load(record_path))
