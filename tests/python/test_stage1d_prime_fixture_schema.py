import json
from pathlib import Path

from libreprimus.solved_fixtures.validation import validate_fixture_dir, validate_fixture_file


def test_p56_prime_stream_fixture_validates() -> None:
    assert validate_fixture_file(Path("data/fixtures/solved-pages/prime-stream-v0/p56-an-end-prime-minus-one.fixture.json")) == []


def test_prime_stream_fixture_requires_prime_start_index_unless_pending(tmp_path: Path) -> None:
    payload = json.loads(Path("data/fixtures/solved-pages/prime-stream-v0/p56-an-end-prime-minus-one.fixture.json").read_text())
    payload["transform_chain"][0]["params"].pop("prime_start_index")
    path = tmp_path / "bad.fixture.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert any("prime_start_index" in error for error in validate_fixture_file(path))


def test_payload_check_schema_and_sha_validate() -> None:
    payload = json.loads(Path("data/fixtures/solved-pages/prime-stream-v0/p56-an-end-prime-minus-one.fixture.json").read_text())
    assert payload["payload_checks"][0]["payload_id"] == "p56-hex-block"
    assert payload["trusted_as_canonical"] is False
    assert payload["canonical_corpus_active"] is False
    assert payload["page_boundaries_final"] is False


def test_phi_prime_alias_fixture_shape_validates(tmp_path: Path) -> None:
    payload = json.loads(Path("data/fixtures/solved-pages/prime-stream-v0/p56-an-end-prime-minus-one.fixture.json").read_text())
    payload["fixture_id"] = "synthetic-phi-alias"
    payload["method_family"] = "phi_prime_stream"
    payload["transform_chain"][0]["name"] = "phi_prime_stream"
    path = tmp_path / "phi.fixture.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert validate_fixture_file(path) == []


def test_prior_stage_fixture_sets_still_validate() -> None:
    assert validate_fixture_dir(Path("data/fixtures/solved-pages/direct-translation-v0")) == []
    assert validate_fixture_dir(Path("data/fixtures/solved-pages/atbash-family-v0")) == []
    assert validate_fixture_dir(Path("data/fixtures/solved-pages/vigenere-v0")) == []
