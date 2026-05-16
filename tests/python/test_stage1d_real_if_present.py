import subprocess
from pathlib import Path

import pytest

from libreprimus.solved_fixtures.reproduction import (
    reproduce_atbash_family_fixtures,
    reproduce_direct_translation_fixtures,
    reproduce_prime_stream_fixtures,
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
    Path("data/fixtures/solved-pages/prime-stream-v0/p56-an-end-prime-minus-one.fixture.json"),
]


pytestmark = pytest.mark.skipif(
    not all(path.exists() for path in REAL_REQUIREMENTS),
    reason="Stage 1D real-source fixtures require local raw sources and generated Stage 0E outputs.",
)


def test_stage1d_real_fixture_reproduction() -> None:
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
    prime_records, prime_summary, _ = reproduce_prime_stream_fixtures(
        fixture_dir=Path("data/fixtures/solved-pages/prime-stream-v0"),
        candidate_dir=Path("data/normalized/corpus-candidates/rtkd-master-v0-candidate"),
    )
    status = subprocess.run(["git", "status", "--short"], check=True, capture_output=True, text=True).stdout

    assert validate_fixture_dir(Path("data/fixtures/solved-pages/prime-stream-v0")) == []
    assert direct_summary.pass_count == 4
    assert atbash_summary.pass_count == 3
    assert vigenere_summary.pass_count == 2
    assert prime_summary.pass_count == 1
    assert prime_records[0].fixture_id == "p56-an-end-prime-minus-one"
    assert prime_records[0].prime_values_used_count == 84
    assert prime_records[0].stream_values_used_count == 84
    assert prime_records[0].payload_check_results[0]["match_status"] == "pass"
    assert all(record.canonical_corpus_active is False for record in prime_records)
    assert all(record.trusted_as_canonical is False for record in prime_records)
    assert all(record.match_status == "pass" for record in direct_records + atbash_records + vigenere_records)
    assert "data/normalized/solved-baselines/prime-stream-v0/summary.json" not in status
