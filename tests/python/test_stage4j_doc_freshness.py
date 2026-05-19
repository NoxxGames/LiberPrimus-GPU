from __future__ import annotations

from pathlib import Path

from libreprimus.observation_review.path_sanitisation import find_stale_operational_text


def test_stage4j_stale_readme_next_stage_fixture_fails(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("Next: Stage 4I scorer consolidation.\n", encoding="utf-8")
    findings = find_stale_operational_text(tmp_path, paths=[readme])
    assert findings


def test_stage4j_current_operational_docs_pass_path_and_freshness_checks() -> None:
    assert find_stale_operational_text() == []
