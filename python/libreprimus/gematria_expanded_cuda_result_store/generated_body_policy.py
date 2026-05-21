"""Build Stage 5S generated-body publication policy records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_cuda_result_store.export import write_record_set, write_report
from libreprimus.gematria_expanded_cuda_result_store.models import (
    COMMON_FLAGS,
    GENERATED_BODY_POLICY_PATH,
    GENERATED_BODY_POLICY_REPORT_JSON,
    OUTPUT_DIR,
)

_POLICIES = (
    ("stage5r_cuda_result_bodies", "ignored_unpublished", "Stage 5R generated CUDA result bodies remain ignored."),
    ("stage5s_report_json", "ignored_unpublished", "Stage 5S generated JSON reports remain ignored."),
    ("compact_metadata_records", "commit_allowed", "Schema-valid identifiers and hashes may be committed."),
    ("future_generated_body_publication", "blocked_requires_new_stage_policy", "Any generated-body publication requires an explicit future policy update."),
)


def build_generated_body_policy(
    *,
    generated_body_policy_out: Path = GENERATED_BODY_POLICY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [_record(index=index, policy_id=policy_id, status=status, rationale=rationale) for index, (policy_id, status, rationale) in enumerate(_POLICIES)]
    write_record_set(generated_body_policy_out, records)
    write_report(out_dir, GENERATED_BODY_POLICY_REPORT_JSON, {"records": records})
    return records


def _record(*, index: int, policy_id: str, status: str, rationale: str) -> dict[str, Any]:
    record = {
        "record_type": "gematria_expanded_cuda_generated_body_policy_record",
        "generated_body_policy_id": f"stage5s-generated-body-policy-{index:02d}",
        "policy_subject": policy_id,
        "policy_status": status,
        "rationale": rationale,
        "generated_result_bodies_committed": False,
        "full_token_output_bodies_committed": False,
        "raw_data_committed": False,
        "sqlite_committed": False,
        "codex_output_ignored": True,
        "future_publication_requires_policy_update": True,
    }
    record.update(COMMON_FLAGS)
    return record
