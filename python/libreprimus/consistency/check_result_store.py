"""Result-store consistency checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result, warning_result
from libreprimus.paths import repo_root
from libreprimus.result_store.validation import (
    validate_result_store,
    validate_result_store_manifest_file,
)

GROUP = "result_store"
DEFAULT_MANIFEST = repo_root() / "experiments/manifests/result-store/stage2b-solved-baseline-import.yaml"
DEFAULT_RESULTS_DIR = repo_root() / "experiments/results/result-store/stage2b"
DEFAULT_SQLITE = DEFAULT_RESULTS_DIR / "results.sqlite3"


def check_result_store_consistency(
    manifest_path: Path = DEFAULT_MANIFEST,
    *,
    results_dir: Path = DEFAULT_RESULTS_DIR,
    sqlite_path: Path = DEFAULT_SQLITE,
    allow_missing_generated: bool = True,
) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []
    manifest_errors = validate_result_store_manifest_file(manifest_path)
    if manifest_errors:
        results.extend(fail_result(GROUP, "manifest_valid", error, path=manifest_path) for error in manifest_errors)
    else:
        results.append(pass_result(GROUP, "manifest_valid", "Stage 2B result-store manifest validates.", path=manifest_path))

    for schema in [
        "schemas/results/experiment-run-record-v0.schema.json",
        "schemas/results/experiment-run-summary-v0.schema.json",
        "schemas/results/experiment-artifact-record-v0.schema.json",
        "schemas/results/sqlite-result-store-v0.schema.json",
    ]:
        path = repo_root() / schema
        if path.is_file():
            results.append(pass_result(GROUP, "result_schema_exists", f"Result-store schema exists: {schema}", path=path))
        else:
            results.append(fail_result(GROUP, "result_schema_exists", f"Missing result-store schema: {schema}", path=path))

    if not _is_ignored("experiments/results/result-store/stage2b/results.sqlite3"):
        results.append(fail_result(GROUP, "sqlite_path_ignored", "SQLite output path is not ignored."))
    else:
        results.append(pass_result(GROUP, "sqlite_path_ignored", "SQLite output path is ignored."))

    required_generated = [results_dir / "run_records.jsonl", results_dir / "summary.json", sqlite_path]
    if not all(path.is_file() for path in required_generated):
        message = "Generated Stage 2B outputs are absent; local generated-output validation skipped."
        if allow_missing_generated:
            results.append(warning_result(GROUP, "generated_outputs_optional", message, path=results_dir))
            return results
        results.append(fail_result(GROUP, "generated_outputs_optional", message, path=results_dir))
        return results

    errors = validate_result_store(results_dir, sqlite_path)
    if errors:
        results.extend(fail_result(GROUP, "generated_outputs_valid", error, path=results_dir) for error in errors)
    else:
        results.append(pass_result(GROUP, "generated_outputs_valid", "Generated result-store outputs validate."))
    return results


def _is_ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=repo_root(),
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0
