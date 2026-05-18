"""Stage 3R Discord lead-promotion consistency checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.discord_lead_promotion.validation import validate_stage3r_outputs
from libreprimus.paths import repo_root

GROUP = "discord_leads"
PROMOTED_SOURCES = repo_root() / "data/observations/discord/stage3r-promoted-source-records.yaml"
PROMOTED_OBSERVATIONS = repo_root() / "data/observations/discord/stage3r-promoted-observation-records.yaml"
NEGATIVE_CONTROLS = repo_root() / "data/observations/discord/stage3r-negative-control-records.yaml"
MANIFEST_DIR = repo_root() / "experiments/manifests/post-discord"


def check_discord_leads_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    """Run raw-log-free Stage 3R consistency checks."""
    results: list[ConsistencyCheckResult] = []
    _, errors = validate_stage3r_outputs(
        promoted_sources=PROMOTED_SOURCES,
        promoted_observations=PROMOTED_OBSERVATIONS,
        negative_controls=NEGATIVE_CONTROLS,
        manifest_dir=MANIFEST_DIR,
        allow_empty=True,
    )
    if errors:
        for error in errors:
            results.append(fail_result(GROUP, "stage3r_records_valid", error))
    else:
        results.append(pass_result(GROUP, "stage3r_records_valid", "Stage 3R records and manifests are policy-safe."))

    for path in [
        "experiments/results/discord-lead-promotion/stage3r/promotion_audit_records.jsonl",
        "experiments/results/discord-lead-promotion/stage3r/rejected_or_quarantined_records.jsonl",
        "experiments/results/discord-lead-promotion/stage3r/promotion_summary.json",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stage3r_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stage3r_path_ignored", f"Expected ignored path is trackable: {path}", path=path))

    for path in [
        "schemas/history/promoted-discord-source-record-v0.schema.json",
        "schemas/history/promoted-discord-observation-record-v0.schema.json",
        "schemas/history/negative-control-record-v0.schema.json",
        "schemas/experiments/post-discord-experiment-manifest-v0.schema.json",
        "schemas/experiments/gp-rune-claim-record-v0.schema.json",
        "data/observations/discord/stage3r-promoted-source-records.yaml",
        "data/observations/discord/stage3r-promoted-observation-records.yaml",
        "data/observations/discord/stage3r-negative-control-records.yaml",
        "data/observations/discord/stage3r-promotion-audit-summary.yaml",
        "experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml",
        "experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml",
        "experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml",
    ]:
        if _is_ignored(root, path):
            results.append(fail_result(GROUP, "stage3r_path_trackable", f"Expected committed path is ignored: {path}", path=path))
        else:
            results.append(pass_result(GROUP, "stage3r_path_trackable", f"Committed path is trackable: {path}", path=path))

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
