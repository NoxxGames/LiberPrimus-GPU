from __future__ import annotations

from libreprimus.paths import repo_root
from libreprimus.research_synthesis.loader import load_all_record_sets


def test_stage3z_staged_plan_records_stage3y_complete() -> None:
    text = _staged_plan_text()

    assert "stage 3y" in text
    assert "complete" in text


def test_stage3z_staged_plan_records_stage3z_current_or_complete() -> None:
    text = _staged_plan_text()

    assert "stage 3z" in text
    assert "current stage" in text or "complete" in text


def test_stage3z_staged_plan_records_stage4a_discord_research_bundle() -> None:
    text = _staged_plan_text()

    assert "stage 4a" in text
    assert "discord research-bundle" in text
    assert "deep research" in text


def test_stage3z_direction_change_record_exists() -> None:
    records = load_all_record_sets(repo_root() / "data/research")["direction_changes"]
    record = next(
        (
            item
            for item in records
            if item.get("change_id") == "stage3z-stage4-discord-bundle-priority"
        ),
        None,
    )

    assert record is not None
    assert "discord research-bundle" in record["new_direction"].lower()
    assert "deep research" in record["new_direction"].lower()


def _staged_plan_text() -> str:
    return (repo_root() / "docs/roadmap/staged-plan.md").read_text(encoding="utf-8").lower()
