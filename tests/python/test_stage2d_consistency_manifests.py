from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.consistency.check_manifests import check_manifest_consistency
from libreprimus.paths import repo_root


def _copy_all_known(tmp_path: Path) -> tuple[Path, Path]:
    solved_dir = tmp_path / "solved"
    result_dir = tmp_path / "result"
    solved_dir.mkdir()
    result_dir.mkdir()
    source = repo_root() / "experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml"
    target = solved_dir / "stage2a-all-known-solved-baselines.yaml"
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return solved_dir, result_dir


def _mutate_yaml(path: Path, **updates: object) -> None:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    payload.update(updates)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def test_current_manifests_pass() -> None:
    assert not [result for result in check_manifest_consistency() if result.is_failure]


def test_current_result_store_manifest_passes() -> None:
    failures = [
        result
        for result in check_manifest_consistency()
        if result.check_name == "result_store_manifest_valid" and result.is_failure
    ]
    assert failures == []


def test_manifest_wrong_registry_hash_fails(tmp_path: Path) -> None:
    solved_dir, result_dir = _copy_all_known(tmp_path)
    _mutate_yaml(solved_dir / "stage2a-all-known-solved-baselines.yaml", registry_sha256="0" * 64)

    failures = check_manifest_consistency(solved_manifest_dir=solved_dir, result_store_manifest_dir=result_dir)

    assert any(result.check_name == "manifest_registry_sha" for result in failures if result.is_failure)


def test_manifest_search_enabled_true_fails(tmp_path: Path) -> None:
    solved_dir, result_dir = _copy_all_known(tmp_path)
    _mutate_yaml(solved_dir / "stage2a-all-known-solved-baselines.yaml", search_enabled=True)

    failures = check_manifest_consistency(solved_manifest_dir=solved_dir, result_store_manifest_dir=result_dir)

    assert any(result.check_name == "manifest_flags_false" for result in failures if result.is_failure)


def test_manifest_missing_fixture_dir_fails(tmp_path: Path) -> None:
    solved_dir, result_dir = _copy_all_known(tmp_path)
    path = solved_dir / "stage2a-all-known-solved-baselines.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    payload["fixture_groups"][0]["fixture_dir"] = "data/fixtures/solved-pages/missing"
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    failures = check_manifest_consistency(solved_manifest_dir=solved_dir, result_store_manifest_dir=result_dir)

    assert any(result.check_name == "manifest_fixture_dir_exists" for result in failures if result.is_failure)
