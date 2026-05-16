import json
from pathlib import Path

import pytest
from jsonschema import ValidationError, validate

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.validation import validate_fixture_file


def _schema() -> dict:
    return json.loads((repo_root() / "schemas/corpus/solved-page-fixture-v0.schema.json").read_text(encoding="utf-8"))


def _fixture_payload() -> dict:
    return json.loads(
        (repo_root() / "data/fixtures/solved-pages/atbash-family-v0/a-warning.fixture.json").read_text(
            encoding="utf-8"
        )
    )


def test_reverse_gematria_fixture_validates() -> None:
    validate(instance=_fixture_payload(), schema=_schema())
    assert validate_fixture_file(repo_root() / "data/fixtures/solved-pages/atbash-family-v0/a-warning.fixture.json") == []


def test_rotated_reverse_fixture_validates_with_rotation() -> None:
    path = repo_root() / "data/fixtures/solved-pages/atbash-family-v0/a-koan-a-man.fixture.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate(instance=payload, schema=_schema())
    assert payload["transform_chain"][0]["params"]["rotation"] == 3
    assert validate_fixture_file(path) == []


def test_rotated_reverse_without_rotation_fails_validation(tmp_path: Path) -> None:
    payload = json.loads(
        (repo_root() / "data/fixtures/solved-pages/atbash-family-v0/a-koan-a-man.fixture.json").read_text(
            encoding="utf-8"
        )
    )
    payload["transform_chain"] = [{"name": "rotated_reverse_gematria", "params": {}}]
    path = tmp_path / "bad.fixture.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert any("rotation" in error for error in validate_fixture_file(path))


def test_canonical_false_fields_are_required() -> None:
    for field in ["trusted_as_canonical", "canonical_corpus_active", "page_boundaries_final"]:
        payload = _fixture_payload()
        payload[field] = True
        with pytest.raises(ValidationError):
            validate(instance=payload, schema=_schema())


def test_stage1a_direct_fixtures_still_validate() -> None:
    path = repo_root() / "data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json"
    assert validate_fixture_file(path) == []
