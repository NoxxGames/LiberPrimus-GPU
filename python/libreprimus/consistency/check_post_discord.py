"""Stage 3S post-Discord consistency checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.paths import repo_root
from libreprimus.post_discord.validation import validate_manifest

GROUP = "post_discord"
MANIFEST = repo_root() / "experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml"


def check_post_discord_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    """Run raw-data-free Stage 3S checks."""
    results: list[ConsistencyCheckResult] = []
    summary, errors = validate_manifest(MANIFEST)
    if errors:
        for error in errors:
            results.append(fail_result(GROUP, "stage3s_manifest_valid", error))
    else:
        results.append(
            pass_result(
                GROUP,
                "stage3s_manifest_valid",
                f"EXP-3R-003 validates with expected candidate count {summary.get('expected_candidate_count')}.",
            )
        )
    for path in [
        "experiments/results/post-discord/stage3s/candidate_records.jsonl",
        "experiments/results/post-discord/stage3s/top_candidates.jsonl",
        "experiments/results/post-discord/stage3s/summary.json",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stage3s_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stage3s_path_ignored", f"Expected ignored path is trackable: {path}", path=path))
    if _is_ignored(root, "experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml"):
        results.append(fail_result(GROUP, "stage3s_manifest_trackable", "EXP-3R-003 manifest is unexpectedly ignored."))
    else:
        results.append(pass_result(GROUP, "stage3s_manifest_trackable", "EXP-3R-003 manifest remains trackable."))
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
