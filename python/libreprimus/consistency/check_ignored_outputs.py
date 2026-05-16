"""Ignored-output policy consistency checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.paths import repo_root

GROUP = "ignored_outputs"


def check_ignored_output_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []
    ignored_paths = [
        "data/raw/transcripts/rtkd/liber-primus__transcription--master.txt",
        "data/normalized/corpus-candidates/rtkd-master-v0-candidate/corpus_candidate_manifest.json",
        "experiments/results/solved-baselines/stage2a/summary.json",
        "experiments/results/result-store/stage2b/results.sqlite3",
        "experiments/results/consistency/stage2d/consistency_summary.json",
        "local-test.sqlite3",
    ]
    trackable_paths = [
        "data/profiles/gematria/gematria-primus-v0.json",
        "data/fixtures/solved-pages/direct-translation-v0/an-instruction-direct.fixture.json",
        "schemas/results/experiment-run-record-v0.schema.json",
        "experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml",
    ]
    for path in ignored_paths:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "path_ignored", f"Expected ignored path is trackable: {path}", path=path))
    for path in trackable_paths:
        if _is_ignored(root, path):
            results.append(
                fail_result(GROUP, "path_trackable", f"Expected committed path is ignored: {path}", path=path)
            )
        else:
            results.append(pass_result(GROUP, "path_trackable", f"Committed path is trackable: {path}", path=path))
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
