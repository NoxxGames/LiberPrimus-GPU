from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml

from libreprimus.history.source_records import SOURCE_CLASSES, validate_source_record, validate_source_records

REPO = Path(__file__).resolve().parents[2]
SOURCE_RECORDS = REPO / "data/observations/archive/source-archive-records-v0.yaml"


def test_source_archive_records_validate() -> None:
    count, errors = validate_source_records(SOURCE_RECORDS)

    assert count >= 12
    assert errors == []


def test_source_class_vocabulary_enforced() -> None:
    payload = yaml.safe_load(SOURCE_RECORDS.read_text(encoding="utf-8"))
    record = deepcopy(payload["records"][0])
    record["source_class"] = "live_tor_claim"

    assert "live_tor_claim" not in SOURCE_CLASSES
    assert any("invalid source_class" in error for error in validate_source_record(record))


def test_source_records_noncanonical() -> None:
    payload = yaml.safe_load(SOURCE_RECORDS.read_text(encoding="utf-8"))

    assert all(record["trusted_as_canonical"] is False for record in payload["records"])
    assert all(record["canonical_status"] != "canonical_active" for record in payload["records"])
