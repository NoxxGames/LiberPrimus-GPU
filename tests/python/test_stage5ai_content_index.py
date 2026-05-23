from __future__ import annotations

from pathlib import Path
import json

import yaml
from jsonschema import Draft202012Validator


def test_stage5ai_content_index_uses_conservative_publication_statuses() -> None:
    payload = yaml.safe_load(Path("data/source-harvester/stage5ai-curated-content-index-summary.yaml").read_text(encoding="utf-8"))
    assert payload["content_index_records"] == 19
    assert payload["generated_extract_review_required_count"] >= 1
    assert payload["blocked_private_or_sensitive_count"] >= 1
    assert payload["website_publication_allowed_count"] == 0
    validator = Draft202012Validator(json.loads(Path("schemas/source-harvester/website-ingest-content-record-v0.schema.json").read_text(encoding="utf-8")))
    for record in payload["records"]:
        validator.validate(record)
