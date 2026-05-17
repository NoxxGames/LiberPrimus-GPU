from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.visual_observations.validation import validate_cookie_records

REPO = Path(__file__).resolve().parents[2]
COOKIES = REPO / "data/observations/web/cookie-hash-records-v0.yaml"


def test_cookie_hash_records_validate() -> None:
    count, errors = validate_cookie_records(COOKIES)

    assert count == 2
    assert errors == []


def test_cookie_values_are_hex64_and_do_not_claim_preimage() -> None:
    payload = yaml.safe_load(COOKIES.read_text(encoding="utf-8"))

    for record in payload["records"]:
        assert record["value_format"] == "hex64"
        assert len(record["cookie_value"]) == 64
        assert record["preimage_status"] == "unknown"
        assert record["trusted_as_canonical"] is False
