"""Stage 3S/3T post-Discord consistency checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.paths import repo_root
from libreprimus.post_discord.gp_rune_claim_verifier import validate_gp_rune_manifest
from libreprimus.post_discord.validation import validate_manifest

GROUP = "post_discord"
ONION7_MANIFEST = repo_root() / "experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml"
GP_RUNE_MANIFEST = repo_root() / "experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml"


def check_post_discord_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    """Run raw-data-free Stage 3S checks."""
    results: list[ConsistencyCheckResult] = []
    summary, errors = validate_manifest(ONION7_MANIFEST)
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
    gp_summary, gp_errors = validate_gp_rune_manifest(GP_RUNE_MANIFEST)
    if gp_errors:
        for error in gp_errors:
            results.append(fail_result(GROUP, "stage3t_manifest_valid", error))
    else:
        results.append(
            pass_result(
                GROUP,
                "stage3t_manifest_valid",
                f"EXP-3R-004 validates with claim cap {gp_summary.get('claim_cap')}.",
            )
        )
    for path in [
        "experiments/results/post-discord/stage3s/candidate_records.jsonl",
        "experiments/results/post-discord/stage3s/top_candidates.jsonl",
        "experiments/results/post-discord/stage3s/summary.json",
        "experiments/results/post-discord/stage3t/gp_rune_claim_verification_records.jsonl",
        "experiments/results/post-discord/stage3t/summary.json",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stage3s_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stage3s_path_ignored", f"Expected ignored path is trackable: {path}", path=path))
    for manifest_path, name in [
        ("experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml", "EXP-3R-003"),
        ("experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml", "EXP-3R-004"),
    ]:
        if _is_ignored(root, manifest_path):
            results.append(fail_result(GROUP, "post_discord_manifest_trackable", f"{name} manifest is unexpectedly ignored."))
        else:
            results.append(pass_result(GROUP, "post_discord_manifest_trackable", f"{name} manifest remains trackable."))
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
