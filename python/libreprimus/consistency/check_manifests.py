"""Manifest consistency checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.paths import repo_root
from libreprimus.result_store.validation import validate_result_store_manifest_file
from libreprimus.solved_baselines.validation import validate_manifest_file
from libreprimus.transforms.registry import DEFAULT_REGISTRY_PATH, compute_sha256

GROUP = "manifests"
SOLVED_MANIFEST_DIR = repo_root() / "experiments/manifests/solved-baselines"
RESULT_STORE_MANIFEST_DIR = repo_root() / "experiments/manifests/result-store"
REGISTRY_PATH = repo_root() / DEFAULT_REGISTRY_PATH


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Manifest payload must be a mapping: {path}")
    return payload


def _no_raw_dump(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return "data/raw" not in text and len(text) < 20000


def check_manifest_consistency(
    *,
    solved_manifest_dir: Path = SOLVED_MANIFEST_DIR,
    result_store_manifest_dir: Path = RESULT_STORE_MANIFEST_DIR,
    registry_path: Path = REGISTRY_PATH,
) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []
    registry_sha = compute_sha256(registry_path)

    for manifest in sorted(solved_manifest_dir.glob("*.yaml")):
        try:
            errors = validate_manifest_file(manifest)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            errors = [str(exc)]
        if errors:
            results.extend(fail_result(GROUP, "solved_manifest_valid", error, path=manifest) for error in errors)
        else:
            results.append(pass_result(GROUP, "solved_manifest_valid", "Solved manifest validates.", path=manifest))
        payload = _load_yaml(manifest)
        _check_manifest_flags(results, payload, manifest)
        if payload.get("registry_sha256") != registry_sha:
            results.append(fail_result(GROUP, "manifest_registry_sha", "Registry SHA mismatch.", path=manifest))
        for group in payload.get("fixture_groups", []):
            fixture_dir = repo_root() / str(group.get("fixture_dir", ""))
            if not fixture_dir.is_dir():
                results.append(
                    fail_result(GROUP, "manifest_fixture_dir_exists", "Fixture dir missing.", path=fixture_dir)
                )
        if not _no_raw_dump(manifest):
            results.append(fail_result(GROUP, "manifest_no_raw_dump", "Manifest appears to include raw data.", path=manifest))

    all_known = solved_manifest_dir / "stage2a-all-known-solved-baselines.yaml"
    if all_known.is_file():
        payload = _load_yaml(all_known)
        counts = payload.get("expected_counts", {})
        if counts.get("fixture_count") == 10 and counts.get("pass_count") == 10:
            results.append(pass_result(GROUP, "all_known_counts", "All-known manifest expects 10 passes."))
        else:
            results.append(fail_result(GROUP, "all_known_counts", "All-known manifest count drift."))

    for manifest in sorted(result_store_manifest_dir.glob("*.yaml")):
        try:
            errors = validate_result_store_manifest_file(manifest)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            errors = [str(exc)]
        if errors:
            results.extend(fail_result(GROUP, "result_store_manifest_valid", error, path=manifest) for error in errors)
        else:
            results.append(
                pass_result(GROUP, "result_store_manifest_valid", "Result-store manifest validates.", path=manifest)
            )
        payload = _load_yaml(manifest)
        _check_manifest_flags(results, payload, manifest)
        input_manifest = repo_root() / str(payload.get("input_manifest_path", ""))
        if not input_manifest.is_file():
            results.append(
                fail_result(GROUP, "result_store_input_manifest_exists", "Input manifest missing.", path=input_manifest)
            )

    if not any(result.check_name == "manifest_fixture_dir_exists" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "manifest_fixture_dir_exists", "Manifest fixture dirs exist."))
    if not any(result.check_name == "manifest_registry_sha" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "manifest_registry_sha", "Manifest registry SHA values match."))
    if not any(result.check_name == "manifest_flags_false" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "manifest_flags_false", "Manifest search/CUDA/scoring flags are false."))
    if not any(result.check_name == "manifest_no_raw_dump" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "manifest_no_raw_dump", "Manifests do not contain raw corpus dumps."))
    return results


def _check_manifest_flags(results: list[ConsistencyCheckResult], payload: dict[str, Any], path: Path) -> None:
    for field in ["search_enabled", "cuda_enabled", "scoring_enabled", "canonical_corpus_active"]:
        if payload.get(field) is not False:
            results.append(fail_result(GROUP, "manifest_flags_false", f"{field} must be false.", path=path))
