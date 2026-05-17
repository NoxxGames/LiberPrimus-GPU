"""Stage 3K archive, visual, and web observation consistency checks."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.history.image_locks import validate_image_locks
from libreprimus.history.source_records import validate_source_records
from libreprimus.paths import repo_root
from libreprimus.visual_observations.validation import validate_cookie_records, validate_visual_records

GROUP = "archive_visual"
SOURCE_RECORDS = repo_root() / "data/observations/archive/source-archive-records-v0.yaml"
VISUAL_RECORDS = repo_root() / "data/observations/visual/visual-numeric-observations-v0.yaml"
COOKIE_RECORDS = repo_root() / "data/observations/web/cookie-hash-records-v0.yaml"
IMAGE_LOCKS = repo_root() / "data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl"
IMAGE_ARTIFACTS = repo_root() / "data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl"
SCHEMA_PATHS = [
    repo_root() / "schemas/history/source-archive-record-v0.schema.json",
    repo_root() / "schemas/history/source-lock-record-v0.schema.json",
    repo_root() / "schemas/history/cookie-hash-record-v0.schema.json",
    repo_root() / "schemas/visual/image-artifact-record-v0.schema.json",
    repo_root() / "schemas/visual/visual-numeric-observation-v0.schema.json",
    repo_root() / "schemas/visual/visual-observation-reading-v0.schema.json",
    repo_root() / "schemas/visual/image-analysis-summary-v0.schema.json",
]


def check_archive_visual_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []

    for schema_path in SCHEMA_PATHS:
        try:
            json.loads(schema_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "schema_parse", str(exc), path=schema_path))
        else:
            results.append(pass_result(GROUP, "schema_parse", "Stage 3K schema parses.", path=schema_path))

    source_count, source_errors = validate_source_records(SOURCE_RECORDS)
    if source_errors:
        for error in source_errors:
            results.append(fail_result(GROUP, "source_records_valid", error, path=SOURCE_RECORDS))
    else:
        results.append(
            pass_result(GROUP, "source_records_valid", f"{source_count} source records validate.", path=SOURCE_RECORDS)
        )

    visual_count, visual_errors = validate_visual_records(VISUAL_RECORDS)
    if visual_errors:
        for error in visual_errors:
            results.append(fail_result(GROUP, "visual_records_valid", error, path=VISUAL_RECORDS))
    else:
        results.append(
            pass_result(GROUP, "visual_records_valid", f"{visual_count} visual records validate.", path=VISUAL_RECORDS)
        )

    cookie_count, cookie_errors = validate_cookie_records(COOKIE_RECORDS)
    if cookie_errors:
        for error in cookie_errors:
            results.append(fail_result(GROUP, "cookie_records_valid", error, path=COOKIE_RECORDS))
    else:
        results.append(
            pass_result(GROUP, "cookie_records_valid", f"{cookie_count} cookie records validate.", path=COOKIE_RECORDS)
        )

    lock_count, artifact_count, lock_errors = validate_image_locks(
        locks=IMAGE_LOCKS,
        artifacts=IMAGE_ARTIFACTS,
        allow_empty=True,
    )
    if lock_errors:
        for error in lock_errors:
            results.append(fail_result(GROUP, "image_locks_valid", error, path=IMAGE_LOCKS))
    else:
        results.append(
            pass_result(
                GROUP,
                "image_locks_valid",
                f"{lock_count} image locks and {artifact_count} artifact records validate.",
                path=IMAGE_LOCKS,
            )
        )

    ignored_expectations = [
        "third_party/LiberPrimusPages/example.jpg",
        "third_party/LiberPrimusPages/example.jpeg",
        "third_party/LiberPrimusPages/example.png",
        "experiments/results/archive-visual-registry/stage3k/local-image-scan-summary.json",
    ]
    for path in ignored_expectations:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stage3k_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stage3k_path_ignored", f"Expected ignored path is trackable: {path}", path=path))
    return results


def _is_ignored(root: Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0
