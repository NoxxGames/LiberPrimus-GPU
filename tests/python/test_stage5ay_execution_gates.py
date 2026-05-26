from pathlib import Path

import yaml


def test_stage5ay_execution_gates_require_later_review() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-execution-gates.yaml").read_text(encoding="utf-8"))
    statuses = {record["gate_id"]: record["status"] for record in payload["gates"]}

    assert payload["execution_authorised_now"] is False
    assert statuses["manifest_review_gate"] == "blocked_pending_stage5az_or_later_review"
    assert statuses["dwh_gate"] == "blocked_speculative_source_lock_required"
