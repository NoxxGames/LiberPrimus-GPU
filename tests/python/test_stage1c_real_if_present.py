import json
import subprocess
from pathlib import Path

import pytest

from libreprimus.reference_sources.summary import build_stage1c_reference_summary
from libreprimus.solved_fixtures.reproduction import (
    reproduce_atbash_family_fixtures,
    reproduce_direct_translation_fixtures,
    reproduce_vigenere_fixtures,
)
from libreprimus.solved_fixtures.validation import validate_fixture_dir


REAL_REQUIREMENTS = [
    Path("data/raw/transcripts/rtkd/liber-primus__transcription--master.txt"),
    Path("data/raw/transcripts/scream314/liber_primus.md"),
    Path("data/raw/reference-repos/scream314-cicada3301/pages_and_ciphers.md"),
    Path("data/profiles/gematria/gematria-primus-v0.json"),
    Path("data/normalized/corpus-candidates/rtkd-master-v0-candidate/tokens.jsonl"),
    Path("data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json"),
    Path("data/fixtures/solved-pages/atbash-family-v0/a-warning.fixture.json"),
    Path("data/fixtures/solved-pages/vigenere-v0/welcome-divinity.fixture.json"),
]


pytestmark = pytest.mark.skipif(
    not all(path.exists() for path in REAL_REQUIREMENTS),
    reason="Stage 1C real-source fixtures require local raw sources, mirrored references, and generated Stage 0E outputs.",
)


def test_stage1c_real_fixture_reproduction_and_reference_summary() -> None:
    direct_records, direct_summary, _ = reproduce_direct_translation_fixtures(
        fixture_dir=Path("data/fixtures/solved-pages/direct-translation-v0"),
        candidate_dir=Path("data/normalized/corpus-candidates/rtkd-master-v0-candidate"),
    )
    atbash_records, atbash_summary, _ = reproduce_atbash_family_fixtures(
        fixture_dir=Path("data/fixtures/solved-pages/atbash-family-v0"),
        candidate_dir=Path("data/normalized/corpus-candidates/rtkd-master-v0-candidate"),
    )
    vigenere_records, vigenere_summary, _ = reproduce_vigenere_fixtures(
        fixture_dir=Path("data/fixtures/solved-pages/vigenere-v0"),
        candidate_dir=Path("data/normalized/corpus-candidates/rtkd-master-v0-candidate"),
    )
    reference_summary = build_stage1c_reference_summary()["summary"]
    status = subprocess.run(
        ["git", "status", "--short"], check=True, capture_output=True, text=True
    ).stdout

    assert validate_fixture_dir(Path("data/fixtures/solved-pages/vigenere-v0")) == []
    assert direct_summary.pass_count == 4
    assert atbash_summary.pass_count == 3
    assert vigenere_summary.pass_count >= 1
    assert {record.fixture_id for record in vigenere_records} >= {
        "welcome-divinity-vigenere",
        "a-koan-during-firfumferenfe-vigenere",
    }
    assert all(record.key_indices for record in vigenere_records if record.match_status == "pass")
    assert all(record.canonical_corpus_active is False for record in vigenere_records)
    assert all(record.trusted_as_canonical is False for record in vigenere_records)
    assert not any(
        "prime" in json.dumps(record.transform_chain).lower() for record in vigenere_records
    )
    assert not any(
        "cuda" in json.dumps(record.transform_chain).lower() for record in vigenere_records
    )
    assert all(record.match_status == "pass" for record in direct_records + atbash_records)
    assert reference_summary["divinity_found"] is True
    assert reference_summary["firfumferenfe_found"] is True
    assert "data/normalized/solved-baselines/vigenere-v0/summary.json" not in status
