from pathlib import Path

from libreprimus.transforms.registry import compute_sha256, load_registry, resolve_transform
from libreprimus.transforms.validation import validate_registry


REGISTRY_PATH = Path("data/transform-registry/cpu-reference-transforms-v0.json")


def test_registry_json_validates_and_sha_lock_matches() -> None:
    registry = load_registry(REGISTRY_PATH)
    lock = REGISTRY_PATH.with_suffix(".sha256").read_text(encoding="utf-8").split()[0]

    assert compute_sha256(REGISTRY_PATH) == lock
    assert validate_registry(registry) == []


def test_registry_transform_metadata_safety_flags() -> None:
    registry = load_registry(REGISTRY_PATH)
    ids = [definition.transform_id for definition in registry.transforms]

    assert len(ids) == len(set(ids))
    for definition in registry.transforms:
        assert definition.supports_cpu_reference is True
        assert definition.supports_gpu is False
        assert definition.search_enabled is False
        assert definition.scoring_enabled is False


def test_known_fixture_sets_exist_and_phi_alias_resolves() -> None:
    registry = load_registry(REGISTRY_PATH)

    for definition in registry.transforms:
        for fixture_set in definition.known_fixture_sets:
            assert Path("data/fixtures/solved-pages", fixture_set).is_dir()
    assert resolve_transform(registry, "phi_prime_stream").transform_id == "prime_minus_one_stream"
