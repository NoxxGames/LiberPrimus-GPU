from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[2]
PAIRS = [
    ("schemas/token-block/decision-file-ingest-v0.schema.json", "data/token-block/stage5av-decision-file-ingest.yaml"),
    ("schemas/token-block/decision-file-validation-v0.schema.json", "data/token-block/stage5av-decision-file-validation.yaml"),
    ("schemas/token-block/human-review-decision-record-v0.schema.json", "data/token-block/stage5av-human-review-decision-records.yaml"),
    ("schemas/token-block/confirmed-token-record-v0.schema.json", "data/token-block/stage5av-confirmed-token-records.yaml"),
    ("schemas/token-block/unresolved-token-variant-record-v0.schema.json", "data/token-block/stage5av-unresolved-token-variant-records.yaml"),
    ("schemas/token-block/reviewer-extra-possible-token-v0.schema.json", "data/token-block/stage5av-reviewer-extra-possible-tokens.yaml"),
    ("schemas/token-block/primary60-variant-impact-summary-v0.schema.json", "data/token-block/stage5av-primary60-variant-impact-summary.yaml"),
    ("schemas/token-block/token-variant-branch-manifest-v0.schema.json", "data/token-block/stage5av-token-variant-branch-manifest.yaml"),
    ("schemas/token-block/canonical-transcription-update-v0.schema.json", "data/token-block/stage5av-canonical-transcription-update.yaml"),
    ("schemas/token-block/null-control-decision-update-v0.schema.json", "data/token-block/stage5av-null-control-decision-update.yaml"),
    ("schemas/token-block/dwh-decision-context-v0.schema.json", "data/token-block/stage5av-dwh-decision-context.yaml"),
    ("schemas/token-block/stage5av-guardrail-v0.schema.json", "data/token-block/stage5av-guardrail.yaml"),
    ("schemas/project-state/stage5av-summary-v0.schema.json", "data/project-state/stage5av-summary.yaml"),
]


def test_stage5av_schemas_validate_committed_records() -> None:
    for schema_path, record_path in PAIRS:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record = yaml.safe_load((ROOT / record_path).read_text(encoding="utf-8"))
        jsonschema.validate(record, schema)
