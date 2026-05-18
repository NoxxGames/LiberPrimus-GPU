"""Stage 3Q Discord review-bundle consistency checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.discord_review.validation import validate_bundles
from libreprimus.paths import repo_root

GROUP = "discord_review"
AGGREGATE = repo_root() / "data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml"


def check_discord_review_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    """Run raw-log-free Stage 3Q consistency checks."""
    results: list[ConsistencyCheckResult] = []

    _, errors = validate_bundles(
        results_dir=root / "experiments/results/discord-review-bundles/stage3q",
        aggregate=AGGREGATE,
        allow_missing=True,
    )
    if errors:
        for error in errors:
            results.append(fail_result(GROUP, "discord_review_valid", error))
    else:
        results.append(pass_result(GROUP, "discord_review_valid", "Discord review aggregate is redacted."))

    for path in [
        "third_party/LiberPrimusDiscordChats/example.html",
        "experiments/results/discord-review-bundles/stage3q/redacted_message_stream.jsonl",
        "experiments/results/discord-review-bundles/stage3q/topic_shards/source-links-and-datasets.md",
        "experiments/results/discord-review-bundles/stage3q/review_index.html",
    ]:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stage3q_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stage3q_path_ignored", f"Expected ignored path is trackable: {path}", path=path))

    for path in [
        AGGREGATE,
        repo_root() / "schemas/history/discord-redacted-message-record-v0.schema.json",
        repo_root() / "schemas/history/discord-topic-shard-record-v0.schema.json",
        repo_root() / "schemas/history/discord-review-lead-record-v0.schema.json",
        repo_root() / "schemas/history/discord-review-bundle-summary-v0.schema.json",
    ]:
        rel_path = path.relative_to(root).as_posix()
        if _is_ignored(root, rel_path):
            results.append(fail_result(GROUP, "stage3q_path_trackable", f"Expected committed path is ignored: {rel_path}", path=rel_path))
        else:
            results.append(pass_result(GROUP, "stage3q_path_trackable", f"Committed path is trackable: {rel_path}", path=rel_path))

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
