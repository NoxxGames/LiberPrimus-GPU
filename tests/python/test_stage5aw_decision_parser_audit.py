from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_schemas_validate_committed_records() -> None:
    pairs = [
        ("schemas/token-block/decision-parser-audit-v0.schema.json", "data/token-block/stage5aw-decision-parser-audit.yaml"),
        ("schemas/token-block/possible-token-parser-policy-v0.schema.json", "data/token-block/stage5aw-possible-token-parser-policy.yaml"),
        ("schemas/token-block/repaired-human-review-decision-record-v0.schema.json", "data/token-block/stage5aw-repaired-human-review-decision-records.yaml"),
        ("schemas/token-block/repaired-unresolved-token-variant-record-v0.schema.json", "data/token-block/stage5aw-repaired-unresolved-token-variant-records.yaml"),
        ("schemas/token-block/repaired-reviewer-extra-possible-token-v0.schema.json", "data/token-block/stage5aw-repaired-reviewer-extra-possible-tokens.yaml"),
        ("schemas/token-block/malformed-possible-token-fragment-v0.schema.json", "data/token-block/stage5aw-malformed-possible-token-fragments.yaml"),
        ("schemas/token-block/repaired-primary60-variant-impact-summary-v0.schema.json", "data/token-block/stage5aw-repaired-primary60-variant-impact-summary.yaml"),
        ("schemas/token-block/repaired-token-variant-branch-manifest-v0.schema.json", "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml"),
        ("schemas/token-block/stage5aw-guardrail-v0.schema.json", "data/token-block/stage5aw-guardrail.yaml"),
        ("schemas/project-state/stage5aw-summary-v0.schema.json", "data/project-state/stage5aw-summary.yaml"),
    ]
    for schema_path, record_path in pairs:
        schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
        record = yaml.safe_load((ROOT / record_path).read_text(encoding="utf-8"))
        jsonschema.validate(record, schema)


def test_stage5aw_detects_stage5av_malformed_reviewer_extras() -> None:
    audit = yaml.safe_load(
        (ROOT / "data/token-block/stage5aw-decision-parser-audit.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert audit["stage5av_malformed_reviewer_extra_count"] == 3
    observed = {
        record["challenge_id"]: record["raw_reviewer_extra_possible_token"]
        for record in audit["malformed_stage5av_reviewer_extra_records"]
    }
    assert observed["stage5at-token-case-025"].startswith("3l row overlay")
