import json
from pathlib import Path

import pytest

from libreprimus.solved_fixtures.reproduction import (
    reproduce_atbash_family_fixtures,
    reproduce_direct_translation_fixtures,
)
from libreprimus.solved_fixtures.validation import validate_fixture_dir


REAL_REQUIREMENTS = [
    Path("data/raw/transcripts/rtkd/liber-primus__transcription--master.txt"),
    Path("data/raw/transcripts/scream314/liber_primus.md"),
    Path("data/profiles/gematria/gematria-primus-v0.json"),
    Path("data/normalized/corpus-candidates/rtkd-master-v0-candidate/tokens.jsonl"),
    Path("data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json"),
    Path("data/fixtures/solved-pages/atbash-family-v0/a-warning.fixture.json"),
]


pytestmark = pytest.mark.skipif(
    not all(path.exists() for path in REAL_REQUIREMENTS),
    reason="Stage 1B real-source fixtures require local raw sources and generated Stage 0E candidate outputs.",
)


def test_stage1b_real_fixture_reproduction() -> None:
    direct_records, direct_summary, _ = reproduce_direct_translation_fixtures(
        fixture_dir=Path("data/fixtures/solved-pages/direct-translation-v0"),
        candidate_dir=Path("data/normalized/corpus-candidates/rtkd-master-v0-candidate"),
    )
    atbash_records, atbash_summary, _ = reproduce_atbash_family_fixtures(
        fixture_dir=Path("data/fixtures/solved-pages/atbash-family-v0"),
        candidate_dir=Path("data/normalized/corpus-candidates/rtkd-master-v0-candidate"),
    )

    assert validate_fixture_dir(Path("data/fixtures/solved-pages/atbash-family-v0")) == []
    assert direct_summary.pass_count == 4
    assert atbash_summary.pass_count >= 1
    assert any(record.fixture_id == "a-warning-reverse-gematria" for record in atbash_records)
    assert all(record.canonical_corpus_active is False for record in atbash_records)
    assert all(record.trusted_as_canonical is False for record in atbash_records)
    assert not any("vigenere" in json.dumps(record.transform_chain).lower() for record in atbash_records)
    assert not any("prime" in json.dumps(record.transform_chain).lower() for record in atbash_records)
    assert all(record.match_status == "pass" for record in direct_records)
