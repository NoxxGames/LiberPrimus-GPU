from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


STAGE5BI_RECORDS = [
    "data/historical-route/stage5bi-fandom-page-triage.yaml",
    "data/historical-route/stage5bi-fandom-item-source-lock-candidates.yaml",
    "data/historical-route/stage5bi-original-archive-crosswalk-candidates.yaml",
    "data/historical-route/stage5bi-fandom-media-non-original-policy.yaml",
    "data/historical-route/stage5bi-2014-256-byte-surface-context.yaml",
    "data/historical-route/stage5bi-negative-control-quarantine.yaml",
    "data/historical-route/stage5bi-source-gap-register.yaml",
    "data/historical-route/stage5bi-guardrail.yaml",
    "data/token-block/stage5bi-token-block-external-context.yaml",
    "data/token-block/stage5bi-2014-surface-token-block-context.yaml",
    "data/token-block/stage5bi-spreadsheet-stage5aw-reconciliation.yaml",
    "data/source-harvester/stage5bi-local-spreadsheet-source-lock.yaml",
    "data/source-harvester/stage5bi-fandom-crosswalk-source-summary.yaml",
    "data/project-state/stage5bi-summary.yaml",
    "data/project-state/stage5bi-next-stage-decision.yaml",
]


def load_yaml(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def validate_record(path: str) -> None:
    payload = load_yaml(path)
    schema = json.loads(Path(payload["schema"]).read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)


def test_stage5bi_records_validate_against_schemas() -> None:
    for path in STAGE5BI_RECORDS:
        validate_record(path)


def test_stage5bi_fandom_page_triage_contains_required_pages() -> None:
    payload = load_yaml("data/historical-route/stage5bi-fandom-page-triage.yaml")
    urls = {record["source_url"] for record in payload["records"]}

    assert payload["page_count"] == len(payload["records"])
    assert "https://uncovering-cicada.fandom.com/wiki/What_Happened_Part_1_(2014)" in urls
    assert "https://uncovering-cicada.fandom.com/wiki/Page_49-51" in urls
    assert all(record["execution_allowed"] is False for record in payload["records"])
    assert all(record["solve_claim"] is False for record in payload["records"])
