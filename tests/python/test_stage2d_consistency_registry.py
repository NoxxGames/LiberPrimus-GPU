from __future__ import annotations

import hashlib
import json
from pathlib import Path

from libreprimus.consistency.check_registry import check_registry_consistency


def _write_registry(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    path.with_suffix(".sha256").write_text(f"{sha}  {path.name}\n", encoding="utf-8")


def _base_registry() -> dict:
    return {
        "registry_id": "test-registry",
        "registry_kind": "cpu_reference_transform_registry",
        "status": "active_for_solved_baselines",
        "canonical_corpus_active": False,
        "search_enabled": False,
        "cuda_enabled": False,
        "scoring_enabled": False,
        "transforms": [
            {
                "transform_id": "direct_translation",
                "transform_version": "v0",
                "method_family": "direct_translation",
                "aliases": [],
                "formula": "decoded_index = cipher_index",
                "parameter_schema": {},
                "supports_cpu_reference": True,
                "supports_gpu": False,
                "search_enabled": False,
                "scoring_enabled": False,
                "fixture_baseline_supported": True,
                "implemented_module": "module.function",
                "provenance_notes": [],
                "known_fixture_sets": ["direct-translation-v0"],
            }
        ],
    }


def _run_tmp_registry(tmp_path: Path, payload: dict) -> list[str]:
    registry = tmp_path / "registry.json"
    fixture_root = tmp_path / "fixtures"
    (fixture_root / "direct-translation-v0").mkdir(parents=True)
    catalog = tmp_path / "CIPHER_CATALOG.md"
    catalog.write_text("direct_translation\n", encoding="utf-8")
    _write_registry(registry, payload)
    return [
        result.check_name
        for result in check_registry_consistency(
            registry,
            fixture_root=fixture_root,
            catalog_path=catalog,
        )
        if result.is_failure
    ]


def test_current_registry_passes() -> None:
    assert not [result for result in check_registry_consistency() if result.is_failure]


def test_bad_alias_target_fails(tmp_path: Path) -> None:
    payload = _base_registry()
    payload["transforms"].append({**payload["transforms"][0], "transform_id": "phi", "alias_of": "missing"})

    assert "alias_targets_valid" in _run_tmp_registry(tmp_path, payload)


def test_search_enabled_true_fails(tmp_path: Path) -> None:
    payload = _base_registry()
    payload["transforms"][0]["search_enabled"] = True

    assert "search_enabled_false" in _run_tmp_registry(tmp_path, payload)


def test_supports_gpu_true_fails(tmp_path: Path) -> None:
    payload = _base_registry()
    payload["transforms"][0]["supports_gpu"] = True

    assert "supports_gpu_false" in _run_tmp_registry(tmp_path, payload)


def test_missing_fixture_set_fails(tmp_path: Path) -> None:
    payload = _base_registry()
    payload["transforms"][0]["known_fixture_sets"] = ["missing"]

    assert "known_fixture_set_exists" in _run_tmp_registry(tmp_path, payload)
