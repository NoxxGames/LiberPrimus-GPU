"""Stage 4A Discord full-review consistency checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.paths import repo_root

GROUP = "discord_full_review"
DISCORD_AGGREGATE = repo_root() / "data/observations/discord/stage4a-full-review-aggregate.yaml"
LP_AGGREGATE = repo_root() / "data/observations/visual/stage4a-lp-page-gallery-aggregate.yaml"


def check_discord_full_review_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []
    _check_aggregate(results, DISCORD_AGGREGATE, "discord_stage4a_full_review_aggregate")
    _check_aggregate(results, LP_AGGREGATE, "lp_page_stage4a_gallery_aggregate")
    for path in [
        "experiments/results/discord-full-review/stage4a/site/index.html",
        "experiments/results/discord-full-review/stage4a/channel_shards/example.part001.md",
        "experiments/results/discord-full-review/stage4a/topic_shards/cuneiform-base60.md",
        "experiments/results/discord-full-review/stage4a/lp_pages/lp_page_image_manifest.jsonl",
        "experiments/results/discord-full-review/stage4a/liberprimus-discord-review-site.zip",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stage4a_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stage4a_path_ignored", f"Expected ignored path is trackable: {path}", path=path))
    for path in [
        "schemas/history/discord-full-review-channel-record-v0.schema.json",
        "schemas/history/discord-full-review-message-record-v0.schema.json",
        "schemas/history/discord-full-review-shard-record-v0.schema.json",
        "schemas/history/discord-full-review-index-record-v0.schema.json",
        "schemas/history/discord-full-review-summary-v0.schema.json",
        "schemas/visual/lp-page-gallery-record-v0.schema.json",
        "schemas/visual/discord-image-reference-v0.schema.json",
        "data/observations/discord/stage4a-full-review-aggregate.yaml",
        "data/observations/visual/stage4a-lp-page-gallery-aggregate.yaml",
    ]:
        if _is_ignored(root, path):
            results.append(fail_result(GROUP, "stage4a_metadata_trackable", f"Expected committed path is ignored: {path}", path=path))
        else:
            results.append(pass_result(GROUP, "stage4a_metadata_trackable", f"Committed path is trackable: {path}", path=path))
    return results


def _check_aggregate(results: list[ConsistencyCheckResult], path: Path, record_type: str) -> None:
    if not path.is_file():
        results.append(fail_result(GROUP, "aggregate_present", f"Aggregate missing: {path}", path=path))
        return
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        results.append(fail_result(GROUP, "aggregate_parse", f"Aggregate is not a mapping: {path}", path=path))
        return
    if payload.get("record_type") != record_type:
        results.append(fail_result(GROUP, "aggregate_record_type", f"Unexpected record_type in {path}", path=path))
    else:
        results.append(pass_result(GROUP, "aggregate_record_type", f"{record_type} record present.", path=path))
    failures = []
    for key in (
        "raw_message_committed",
        "username_committed",
        "user_id_committed",
        "message_id_committed",
        "private_url_committed",
        "raw_discord_html_committed",
        "generated_site_committed",
        "solve_claim",
    ):
        if key in payload and payload.get(key) is not False:
            failures.append(key)
    if failures:
        results.append(fail_result(GROUP, "aggregate_privacy_flags", f"{path}:{failures} must be false", path=path))
    else:
        results.append(pass_result(GROUP, "aggregate_privacy_flags", f"Privacy flags hold for {path.name}.", path=path))


def _is_ignored(root: Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0
