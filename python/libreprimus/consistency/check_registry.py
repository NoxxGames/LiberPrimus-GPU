"""Registry consistency checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.paths import repo_root

GROUP = "registry"
DEFAULT_REGISTRY = repo_root() / "data/transform-registry/cpu-reference-transforms-v0.json"
DEFAULT_FIXTURE_ROOT = repo_root() / "data/fixtures/solved-pages"
DEFAULT_CATALOG = repo_root() / "CIPHER_CATALOG.md"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON payload must be an object: {path}")
    return payload


def check_registry_consistency(
    registry_path: Path = DEFAULT_REGISTRY,
    *,
    fixture_root: Path = DEFAULT_FIXTURE_ROOT,
    catalog_path: Path = DEFAULT_CATALOG,
) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []
    if not registry_path.is_file():
        return [fail_result(GROUP, "registry_exists", "Registry file is missing.", path=registry_path)]
    results.append(pass_result(GROUP, "registry_exists", "Registry file exists.", path=registry_path))

    try:
        payload = _load_json(registry_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [fail_result(GROUP, "registry_json", str(exc), path=registry_path)]

    lock_path = registry_path.with_suffix(".sha256")
    if lock_path.is_file():
        expected = lock_path.read_text(encoding="utf-8").split()[0]
        actual = _sha256(registry_path)
        if expected == actual:
            results.append(pass_result(GROUP, "registry_sha_lock", "Registry SHA lock matches."))
        else:
            results.append(
                fail_result(
                    GROUP,
                    "registry_sha_lock",
                    "Registry SHA lock mismatch.",
                    data={"expected": expected, "actual": actual},
                )
            )
    else:
        results.append(fail_result(GROUP, "registry_sha_lock", "Registry SHA lock is missing."))

    transforms = payload.get("transforms", [])
    if not isinstance(transforms, list):
        return results + [fail_result(GROUP, "transform_list", "Registry transforms must be a list.")]
    transform_ids = [str(item.get("transform_id")) for item in transforms if isinstance(item, dict)]
    if len(transform_ids) == len(set(transform_ids)):
        results.append(pass_result(GROUP, "transform_ids_unique", "Transform IDs are unique."))
    else:
        results.append(fail_result(GROUP, "transform_ids_unique", "Transform IDs are not unique."))

    id_set = set(transform_ids)
    for item in transforms:
        if not isinstance(item, dict):
            results.append(fail_result(GROUP, "transform_shape", "Transform entry must be an object."))
            continue
        transform_id = str(item.get("transform_id"))
        alias_of = item.get("alias_of")
        if alias_of and alias_of not in id_set:
            results.append(
                fail_result(
                    GROUP,
                    "alias_targets_valid",
                    f"{transform_id} alias target is missing: {alias_of}",
                )
            )
        for field, expected in [
            ("search_enabled", False),
            ("supports_gpu", False),
            ("scoring_enabled", False),
        ]:
            if item.get(field) is not expected:
                results.append(
                    fail_result(
                        GROUP,
                        f"{field}_false",
                        f"{transform_id} has {field}={item.get(field)!r}.",
                    )
                )
        for fixture_set in item.get("known_fixture_sets", []):
            fixture_dir = fixture_root / str(fixture_set)
            if not fixture_dir.is_dir():
                results.append(
                    fail_result(
                        GROUP,
                        "known_fixture_set_exists",
                        f"{transform_id} fixture set is missing: {fixture_dir}",
                        path=fixture_dir,
                    )
                )

    if not any(result.check_name == "alias_targets_valid" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "alias_targets_valid", "Alias targets are valid."))
    if not any(result.check_name == "known_fixture_set_exists" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "known_fixture_set_exists", "Known fixture sets exist."))
    for field in ["search_enabled", "supports_gpu", "scoring_enabled"]:
        if not any(result.check_name == f"{field}_false" and result.is_failure for result in results):
            results.append(pass_result(GROUP, f"{field}_false", f"All transforms keep {field}=false."))

    if payload.get("search_enabled") is not False:
        results.append(fail_result(GROUP, "registry_search_false", "Registry search_enabled must be false."))
    else:
        results.append(pass_result(GROUP, "registry_search_false", "Registry search_enabled is false."))
    if payload.get("cuda_enabled") is not False:
        results.append(fail_result(GROUP, "registry_cuda_false", "Registry cuda_enabled must be false."))
    else:
        results.append(pass_result(GROUP, "registry_cuda_false", "Registry cuda_enabled is false."))
    if payload.get("scoring_enabled") is not False:
        results.append(fail_result(GROUP, "registry_scoring_false", "Registry scoring_enabled must be false."))
    else:
        results.append(pass_result(GROUP, "registry_scoring_false", "Registry scoring_enabled is false."))

    catalog_text = catalog_path.read_text(encoding="utf-8") if catalog_path.is_file() else ""
    missing_docs = [transform_id for transform_id in transform_ids if transform_id not in catalog_text]
    if missing_docs:
        results.append(
            fail_result(
                GROUP,
                "transform_ids_documented",
                f"Transform IDs missing from CIPHER_CATALOG.md: {missing_docs}",
                path=catalog_path,
            )
        )
    else:
        results.append(
            pass_result(
                GROUP,
                "transform_ids_documented",
                "Registry transform IDs are documented in CIPHER_CATALOG.md.",
                path=catalog_path,
            )
        )
    return results
