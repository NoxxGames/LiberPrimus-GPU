import json
from pathlib import Path

from libreprimus.solved_fixtures.validation import validate_fixture_file


def _payload() -> dict:
    return json.loads(Path("data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json").read_text())


def test_fixture_validation_accepts_committed_fixture() -> None:
    assert validate_fixture_file(Path("data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json")) == []


def test_fixture_validation_fails_profile_sha_mismatch(tmp_path: Path) -> None:
    payload = _payload()
    payload["gematria_profile_sha256"] = "bad"
    path = tmp_path / "bad.fixture.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert validate_fixture_file(path)


def test_pending_fixture_is_valid_with_reason(tmp_path: Path) -> None:
    payload = _payload()
    payload["fixture_id"] = "pending"
    payload["method_status"] = "pending_reference_text"
    payload["in_scope_for_stage"] = False
    payload["span_selector"]["selector_kind"] = "pending"
    payload["expected_normalized_plaintext"] = None
    payload["expected_normalized_plaintext_sha256"] = None
    payload["notes"] = ["Reference text ambiguous."]
    path = tmp_path / "pending.fixture.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert validate_fixture_file(path) == []
