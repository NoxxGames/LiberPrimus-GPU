from __future__ import annotations

from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
import json


def test_stage5ai_source_cards_include_matched_and_unclassified_sources() -> None:
    payload = yaml.safe_load(Path("data/source-harvester/stage5ai-curated-source-card-summary.yaml").read_text(encoding="utf-8"))
    assert payload["source_card_records"] == 26
    assert payload["matched_local_source_cards"] == 12
    assert payload["unclassified_source_cards"] == 14
    source_ids = {record["source_id"] for record in payload["records"]}
    assert "complete_cicada3301_archive" in source_ids
    assert "local_unclassified_fib421_jpg" in source_ids
    validator = Draft202012Validator(json.loads(Path("schemas/source-harvester/website-ingest-source-card-v0.schema.json").read_text(encoding="utf-8")))
    for record in payload["records"]:
        validator.validate(record)
