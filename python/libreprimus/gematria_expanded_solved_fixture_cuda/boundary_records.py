"""Build Stage 5R expanded CUDA boundary records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_solved_fixture_cuda.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expanded_solved_fixture_cuda.models import APPROVED_SCOPE, BOUNDARY_RECORDS_PATH, BOUNDARY_REPORT, COMMON_POLICY_FLAGS, OUTPUT_DIR, PARITY_RECORDS_PATH, RUN_RECORDS_PATH


def build_boundary_records(
    *,
    run_records: Path = RUN_RECORDS_PATH,
    parity_records: Path = PARITY_RECORDS_PATH,
    boundaries_out: Path = BOUNDARY_RECORDS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    runs = read_record_set(run_records)
    parity = read_record_set(parity_records)
    attempted = sum(1 for record in runs if record.get("cuda_run_attempted") is True)
    passed = sum(1 for record in parity if record["parity_status"] == "passed")
    failed = sum(1 for record in parity if str(record["parity_status"]).startswith("failed"))
    record = {
        "record_type": "gematria_expanded_solved_fixture_cuda_boundary_record",
        "boundary_record_id": "stage5r-expanded-boundary-00",
        "approved_stage5r_scope": APPROVED_SCOPE,
        "input_fixture_ids": [record["fixture_id"] for record in runs],
        "run_records": len(runs),
        "parity_records": len(parity),
        "cuda_attempted_count": attempted,
        "cuda_pass_count": passed,
        "cuda_fail_count": failed,
        "cuda_skip_count": len(parity) - passed - failed,
        "consumed_controls_excluded": True,
        "blocked_original_family_fixtures_excluded": True,
        "original_transform_family_semantics_exercised": False,
        "broad_solved_fixture_cuda_allowed": False,
        "unsolved_page_cuda_allowed": False,
        "raw_page_text_cuda_allowed": False,
        "generated_body_publication_allowed": False,
        "method_status_upgrade_allowed": False,
        "cuda_execution_performed": attempted > 0,
        "solved_fixture_cuda_used": attempted > 0,
    }
    record.update(COMMON_POLICY_FLAGS)
    record["cuda_execution_performed"] = attempted > 0
    record["solved_fixture_cuda_used"] = attempted > 0
    records = [record]
    write_record_set(boundaries_out, records)
    write_report(out_dir, BOUNDARY_REPORT, {"records": records})
    return records
