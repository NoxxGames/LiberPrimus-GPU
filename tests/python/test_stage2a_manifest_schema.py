import json
from pathlib import Path

import pytest
import yaml
from jsonschema import ValidationError, validate

from libreprimus.solved_baselines.manifest_loader import load_manifest_payload
from libreprimus.solved_baselines.validation import validate_manifest_file
from libreprimus.transforms.registry import load_registry


SCHEMA_PATH = Path("schemas/corpus/solved-baseline-run-manifest-v0.schema.json")
MANIFEST_DIR = Path("experiments/manifests/solved-baselines")


def _schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def test_committed_manifests_validate_against_schema() -> None:
    for path in [
        MANIFEST_DIR / "direct-translation-v0.yaml",
        MANIFEST_DIR / "atbash-family-v0.yaml",
        MANIFEST_DIR / "vigenere-v0.yaml",
        MANIFEST_DIR / "prime-stream-v0.yaml",
        MANIFEST_DIR / "stage2a-all-known-solved-baselines.yaml",
    ]:
        payload = load_manifest_payload(path)
        validate(instance=payload, schema=_schema())


@pytest.mark.parametrize("flag", ["search_enabled", "cuda_enabled", "scoring_enabled"])
def test_manifest_schema_rejects_enabled_execution_flags(flag: str) -> None:
    payload = load_manifest_payload(MANIFEST_DIR / "direct-translation-v0.yaml")
    payload[flag] = True

    with pytest.raises(ValidationError):
        validate(instance=payload, schema=_schema())


def test_manifest_validation_rejects_wrong_registry_hash_and_missing_fixture_dir(tmp_path: Path) -> None:
    payload = load_manifest_payload(MANIFEST_DIR / "direct-translation-v0.yaml")
    payload["registry_sha256"] = "0" * 64
    wrong_hash = tmp_path / "wrong-hash.yaml"
    wrong_hash.write_text(yaml.safe_dump(payload, sort_keys=True), encoding="utf-8")

    assert any("Registry SHA-256 mismatch" in error for error in validate_manifest_file(wrong_hash))

    payload["registry_sha256"] = load_registry().sha256
    payload["fixture_groups"][0]["fixture_dir"] = str(tmp_path / "missing")
    missing_fixture = tmp_path / "missing-fixture.yaml"
    missing_fixture.write_text(yaml.safe_dump(payload, sort_keys=True), encoding="utf-8")

    assert any("fixture directory missing" in error for error in validate_manifest_file(missing_fixture))
