import json

import pytest
from jsonschema import ValidationError, validate

from libreprimus.paths import repo_root


def _schema() -> dict:
    return json.loads((repo_root() / "schemas/corpus/solved-page-fixture-v0.schema.json").read_text(encoding="utf-8"))


def _fixture_payload() -> dict:
    return json.loads(
        (repo_root() / "data/fixtures/solved-pages/direct-translation-v0/p57-parable.fixture.json").read_text(
            encoding="utf-8"
        )
    )


def test_fixture_schema_validates_committed_fixture() -> None:
    validate(instance=_fixture_payload(), schema=_schema())


def test_fixture_schema_rejects_missing_provenance() -> None:
    payload = _fixture_payload()
    payload.pop("source_transcript_sha256")

    with pytest.raises(ValidationError):
        validate(instance=payload, schema=_schema())


def test_fixture_schema_requires_false_canonical_flags() -> None:
    for field in ["trusted_as_canonical", "canonical_corpus_active", "page_boundaries_final"]:
        payload = _fixture_payload()
        payload[field] = True
        with pytest.raises(ValidationError):
            validate(instance=payload, schema=_schema())


def test_fixture_schema_rejects_unknown_method_family() -> None:
    payload = _fixture_payload()
    payload["method_family"] = "made_up_method"

    with pytest.raises(ValidationError):
        validate(instance=payload, schema=_schema())
