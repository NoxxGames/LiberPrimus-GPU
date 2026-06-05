from __future__ import annotations

from libreprimus.token_block import stage5dk
from test_stage5dk_common import ensure_stage5dk_built, load_yaml, write_temp_yaml


def test_stage5dk_fandom_source_lock_register_has_14_expected_urls() -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/source-harvester/stage5dk-fandom-source-lock-register.yaml")

    expected_urls = {source["url"] for source in stage5dk.FANDOM_SOURCES}
    actual_urls = {source["source_url"] for source in record["sources"]}
    assert record["fandom_source_count"] == 14
    assert record["fandom_source_count_expected"] == 14
    assert actual_urls == expected_urls
    assert record["raw_webpage_bodies_committed"] is False
    assert all(source["raw_body_committed"] is False for source in record["sources"])


def test_stage5dk_fandom_lock_validator_rejects_missing_source(
    monkeypatch: object,
    tmp_path,
) -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/source-harvester/stage5dk-fandom-source-lock-register.yaml")
    record["sources"] = record["sources"][:-1]
    path = write_temp_yaml(tmp_path / "register.yaml", record)

    monkeypatch.setitem(stage5dk.DATA_PATHS, "fandom_source_lock_register", path)

    result = stage5dk.validate_stage5dk_fandom_source_locks()
    assert result.validation_error_count > 0
    assert any("fandom_source_count_must_be_14" in error for error in result.errors)


def test_stage5dk_harmonic_key_is_quarantined() -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/source-harvester/stage5dk-fandom-source-lock-register.yaml")

    harmonic = next(
        source
        for source in record["sources"]
        if source["source_key"] == "proposal_16_digit_harmonic_key"
    )
    assert harmonic["trust_tier"] == "C_quarantine"
    assert harmonic["source_lock_confidence"] == "quarantine"
    assert harmonic["usable_as_execution_input"] is False
