from __future__ import annotations

from pathlib import Path

import yaml


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def test_stage5s_generated_body_policy_keeps_bodies_outputs_and_codex_ignored() -> None:
    records = _records("data/cuda/stage5s-gematria-expanded-cuda-generated-body-policy.yaml")
    subjects = {record["policy_subject"]: record for record in records}
    assert set(subjects) == {
        "stage5r_cuda_result_bodies",
        "stage5s_report_json",
        "compact_metadata_records",
        "future_generated_body_publication",
    }
    for record in records:
        assert record["generated_body_publication_allowed"] is False
        assert record["generated_outputs_committed"] is False
        assert record["generated_result_bodies_committed"] is False
        assert record["raw_data_committed"] is False
        assert record["sqlite_committed"] is False
        assert record["codex_output_committed"] is False
        assert record["solve_claim"] is False
    assert subjects["compact_metadata_records"]["policy_status"] == "commit_allowed"
    assert subjects["future_generated_body_publication"]["policy_status"] == "blocked_requires_new_stage_policy"
