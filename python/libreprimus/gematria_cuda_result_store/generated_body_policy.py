"""Build Stage 5P generated-body publication policy records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_cuda_result_store.export import write_record_set, write_report
from libreprimus.gematria_cuda_result_store.models import (
    COMMON_POLICY_FLAGS,
    GENERATED_BODY_POLICY_PATH,
    GENERATED_BODY_POLICY_REPORT,
    OUTPUT_DIR,
)


POLICY_ROWS = (
    (
        "stage5p-generated-body-policy-cuda-result-bodies",
        "generated_cuda_result_bodies",
        "blocked_generated_body_publication",
        "Stage 5P may cite hashes and compact metadata but must not publish generated CUDA result bodies.",
    ),
    (
        "stage5p-generated-body-policy-integration-reports",
        "generated_integration_reports",
        "ignored_generated_reports",
        "Stage 5P generated JSON reports remain under ignored experiments/results paths.",
    ),
    (
        "stage5p-generated-body-policy-raw-sqlite",
        "raw_sqlite_and_local_reports",
        "blocked_raw_or_database_publication",
        "Raw data, SQLite databases, and local reports remain uncommitted.",
    ),
    (
        "stage5p-generated-body-policy-codex-output",
        "codex_completion_handoff",
        "ignored_codex_output",
        "The Stage 5P Codex completion handoff is written under ignored codex-output/.",
    ),
)


def build_generated_body_policy(
    *,
    generated_body_policy_out: Path = GENERATED_BODY_POLICY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for policy_id, artifact_class, policy_status, rationale in POLICY_ROWS:
        records.append(
            {
                "record_type": "gematria_cuda_generated_body_policy_record",
                "generated_body_policy_id": policy_id,
                "artifact_class": artifact_class,
                "policy_status": policy_status,
                "compact_metadata_allowed": True,
                "body_publication_allowed": False,
                "policy_rationale": rationale,
                **COMMON_POLICY_FLAGS,
            }
        )
    write_record_set(generated_body_policy_out, records)
    write_report(out_dir, GENERATED_BODY_POLICY_REPORT, {"records": records})
    return records
