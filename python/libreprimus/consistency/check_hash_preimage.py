"""Stage 3L hash-preimage consistency checks."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.hash_preimage.validation import validate_candidate_packs
from libreprimus.paths import repo_root
from libreprimus.visual_observations.validation import validate_cookie_records

GROUP = "hash_preimage"
PACK_DIR = repo_root() / "data/observations/web/hash-preimage-candidate-packs"
COOKIE_RECORDS = repo_root() / "data/observations/web/cookie-hash-records-v0.yaml"
SCHEMA_PATHS = [
    repo_root() / "schemas/web/hash-preimage-candidate-pack-v0.schema.json",
    repo_root() / "schemas/web/hash-preimage-candidate-record-v0.schema.json",
    repo_root() / "schemas/web/hash-preimage-run-summary-v0.schema.json",
    repo_root() / "schemas/web/hash-preimage-match-record-v0.schema.json",
]


def check_hash_preimage_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []
    for schema_path in SCHEMA_PATHS:
        try:
            json.loads(schema_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "schema_parse", str(exc), path=schema_path))
        else:
            results.append(pass_result(GROUP, "schema_parse", "Stage 3L schema parses.", path=schema_path))

    pack_count, pack_errors = validate_candidate_packs(PACK_DIR)
    if pack_errors:
        for error in pack_errors:
            results.append(fail_result(GROUP, "candidate_packs_valid", error, path=PACK_DIR))
    else:
        results.append(pass_result(GROUP, "candidate_packs_valid", f"{pack_count} packs validate.", path=PACK_DIR))

    cookie_count, cookie_errors = validate_cookie_records(COOKIE_RECORDS)
    if cookie_errors:
        for error in cookie_errors:
            results.append(fail_result(GROUP, "cookie_records_valid", error, path=COOKIE_RECORDS))
    else:
        results.append(
            pass_result(GROUP, "cookie_records_valid", f"{cookie_count} cookie records validate.", path=COOKIE_RECORDS)
        )

    ignored_expectations = [
        "experiments/results/hash-preimage/stage3l/hash_candidate_records.jsonl",
        "experiments/results/hash-preimage/stage3l/exact_matches.jsonl",
        "experiments/results/hash-preimage/stage3l/summary.json",
    ]
    for path in ignored_expectations:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stage3l_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stage3l_path_ignored", f"Expected ignored path is trackable: {path}", path=path))
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
