import json
from pathlib import Path

from libreprimus.solved_fixtures.validation import validate_fixture_dir, validate_fixture_file


def test_real_vigenere_fixtures_validate() -> None:
    assert validate_fixture_dir(Path("data/fixtures/solved-pages/vigenere-v0")) == []


def test_vigenere_fixture_missing_key_fails_unless_pending(tmp_path: Path) -> None:
    payload = json.loads(
        Path("data/fixtures/solved-pages/vigenere-v0/welcome-divinity.fixture.json").read_text()
    )
    payload["transform_chain"][0]["params"].pop("key_text")
    path = tmp_path / "missing-key.fixture.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    errors = validate_fixture_file(path)

    assert any("key_text" in error for error in errors)


def test_vigenere_fixture_unsupported_direction_fails(tmp_path: Path) -> None:
    payload = json.loads(
        Path("data/fixtures/solved-pages/vigenere-v0/welcome-divinity.fixture.json").read_text()
    )
    payload["transform_chain"][0]["params"]["direction"] = "encrypt"
    path = tmp_path / "bad-direction.fixture.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    errors = validate_fixture_file(path)

    assert any("direction" in error for error in errors)


def test_stage1a_and_stage1b_fixtures_still_validate() -> None:
    assert validate_fixture_dir(Path("data/fixtures/solved-pages/direct-translation-v0")) == []
    assert validate_fixture_dir(Path("data/fixtures/solved-pages/atbash-family-v0")) == []
