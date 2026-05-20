from __future__ import annotations

from libreprimus.consistency.state_drift import (
    scan_duplicate_stage_list_entries,
    scan_redundant_current_status_label,
)


def test_stage4q_duplicate_stage_list_entries_detected() -> None:
    text = "- Stage 4G cookie exact-candidate refresh.\n- Stage 4H cpu\n- Stage 4G cookie exact-candidate refresh.\n"

    findings = scan_duplicate_stage_list_entries(text, "README.md")

    assert findings


def test_stage4q_redundant_current_status_label_detected() -> None:
    text = "## Current status\n\nCurrent status:\n- Stage 4Q complete\n"

    findings = scan_redundant_current_status_label(text, "README.md")

    assert findings
