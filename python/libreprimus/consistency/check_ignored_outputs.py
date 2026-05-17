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
        "experiments/results/exploratory-dry-runs/stage2e/summary.json",
        "experiments/results/cpu-execution/stage2f/summary.json",
        "experiments/results/proposal-reviews/stage2g/summary.json",
        "experiments/results/approval-gated-execution/stage2h/summary.json",
        "experiments/results/approval-readiness/stage2i/summary.json",
        "experiments/results/bounded-auto-runs/stage2j/summary.json",
        "local-test.sqlite3",
    ]
    trackable_paths = [
        "data/profiles/gematria/gematria-primus-v0.json",
        "data/fixtures/solved-pages/direct-translation-v0/an-instruction-direct.fixture.json",
        "schemas/results/experiment-run-record-v0.schema.json",
        "schemas/experiments/exploratory-experiment-manifest-v0.schema.json",
        "schemas/experiments/cpu-execution-manifest-v0.schema.json",
        "schemas/experiments/experiment-proposal-v0.schema.json",
        "schemas/experiments/approval-gated-execution-request-v0.schema.json",
        "schemas/experiments/approval-readiness-packet-v0.schema.json",
        "schemas/experiments/operator-policy-v0.schema.json",
        "schemas/experiments/bounded-experiment-queue-v0.schema.json",
        "experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml",
        "experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml",
        "experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml",
        "experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml",
        "experiments/proposals/stage2h/stage2h-approved-synthetic-direct-request.yaml",
        "experiments/proposals/stage2i/stage2i-first-bounded-caesar-affine-review.yaml",
        "experiments/policies/operator-policy-v0.yaml",
        "experiments/queues/stage2j-bounded-cpu-queue.yaml",
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
