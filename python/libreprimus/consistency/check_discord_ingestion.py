"""Stage 3N Discord ingestion consistency checks."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.discord_ingestion.validation import validate_aggregate_records, validate_results
from libreprimus.paths import repo_root

GROUP = "discord_ingestion"
RESULTS_DIR = repo_root() / "experiments/results/discord-ingestion/stage3n"
ARCHIVE_AGGREGATE = repo_root() / "data/locks/third-party/discord-chats/discord-archive-summary-v0.yaml"
OBSERVATION_AGGREGATE = (
    repo_root() / "data/observations/discord/discord-ingestion-aggregate-summary-v0.yaml"
)
SCHEMA_PATHS = [
    repo_root() / "schemas/history/discord-archive-record-v0.schema.json",
    repo_root() / "schemas/history/discord-html-file-lock-v0.schema.json",
    repo_root() / "schemas/history/discord-extracted-link-v0.schema.json",
    repo_root() / "schemas/history/discord-attachment-candidate-v0.schema.json",
    repo_root() / "schemas/history/discord-method-claim-candidate-v0.schema.json",
    repo_root() / "schemas/history/discord-numeric-observation-candidate-v0.schema.json",
    repo_root() / "schemas/history/discord-ingestion-summary-v0.schema.json",
]


def check_discord_ingestion_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    """Run raw-log-free Stage 3N consistency checks."""
    results: list[ConsistencyCheckResult] = []
    for schema_path in SCHEMA_PATHS:
        try:
            payload = json.loads(schema_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - consistency reports collect failures.
            results.append(fail_result(GROUP, "schema_parse", str(exc), path=schema_path))
            continue
        if _privacy_flags_constrained(payload):
            results.append(
                pass_result(
                    GROUP,
                    "schema_privacy_flags",
                    "Stage 3N schema constrains privacy flags.",
                    path=schema_path,
                )
            )
        else:
            results.append(
                fail_result(
                    GROUP,
                    "schema_privacy_flags",
                    "Stage 3N schema permits privacy flag drift.",
                    path=schema_path,
                )
            )

    counts, errors = validate_results(RESULTS_DIR, allow_missing=True)
    if errors:
        for error in errors:
            results.append(fail_result(GROUP, "generated_results_valid", error, path=RESULTS_DIR))
    else:
        results.append(
            pass_result(
                GROUP,
                "generated_results_valid",
                f"Generated Discord ingestion records validate or are absent: {counts}.",
                path=RESULTS_DIR,
            )
        )

    aggregate_counts, aggregate_errors = validate_aggregate_records(
        archive_record_path=ARCHIVE_AGGREGATE,
        observation_record_path=OBSERVATION_AGGREGATE,
        allow_missing=True,
    )
    if aggregate_errors:
        for error in aggregate_errors:
            results.append(fail_result(GROUP, "aggregate_records_valid", error))
    else:
        results.append(
            pass_result(
                GROUP,
                "aggregate_records_valid",
                f"Committed Discord aggregates validate or are absent: {aggregate_counts}.",
            )
        )

    ignored_expectations = [
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusDiscordChats/example.htm",
        "experiments/results/discord-ingestion/stage3n/discord_extracted_links.jsonl",
        "experiments/results/discord-ingestion/stage3n/local_review_index.html",
        "experiments/results/discord-ingestion/stage3n/discord_ingestion_summary.json",
    ]
    for path in ignored_expectations:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stage3n_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stage3n_path_ignored", f"Expected ignored path is trackable: {path}", path=path))
    return results


def _privacy_flags_constrained(payload: dict) -> bool:
    properties = payload.get("properties", {})
    if not isinstance(properties, dict):
        return False
    constrained = False
    for field in [
        "raw_logs_committed",
        "message_bodies_committed",
        "usernames_committed",
        "ai_upload_allowed",
        "ai_upload_used",
        "live_api_used",
        "scrape_used",
        "raw_content_committed",
        "message_body_committed",
        "raw_message_committed",
    ]:
        definition = properties.get(field)
        if definition is None:
            continue
        constrained = True
        if not isinstance(definition, dict) or definition.get("const") is not False:
            return False
    return constrained


def _is_ignored(root: Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0
