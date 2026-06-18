from __future__ import annotations

from pathlib import Path

from libreprimus.token_block import stage6h
from libreprimus.token_block.models import read_yaml

_BUILT = False


def ensure_stage6h_built() -> None:
    global _BUILT
    if _BUILT:
        return
    if stage6h.PROJECT_STATE_PATHS["summary"].exists() and stage6h.CURRENT_STAGE_STATE_PATH.exists():
        current = read_yaml(stage6h.CURRENT_STAGE_STATE_PATH)
        if current.get("latest_completed_stage_id") == "stage-6h":
            _BUILT = True
            return
    stage6h.build_stage6h()
    _BUILT = True


def test_stage6h_current_state_root_and_nested_identity() -> None:
    ensure_stage6h_built()
    current = read_yaml(stage6h.CURRENT_STAGE_STATE_PATH)
    assert current["stage_id"] == "stage-6h"
    assert current["stage_title"] == stage6h.STAGE_TITLE
    assert current["prompt_type"] == stage6h.PROMPT_TYPE
    assert current["latest_completed_stage_id"] == "stage-6h"
    assert current["previous_completed_stage_id"] == "stage-6g"
    assert current["recommended_next_stage_id"] == "stage-6i"
    assert current["latest_completed_stage"]["stage_id"] == current["latest_completed_stage_id"]
    assert current["next_stage"]["stage_id"] == current["recommended_next_stage_id"]
    assert current["post_push_handoff_locations"] == [
        "codex-output/stage6h-codex-completion.md",
        "GitHub issue comment",
    ]
    assert current["stage6g_final_manifest_required"] is False
    assert current["stage6g_can_attempt_final_manifest_without_prior_repair"] is False
    assert current["stage7_execution_allowed_next"] is False
    assert current["stage7_zip_archive_creation_allowed_next"] is False


def test_stage6h_negative_current_state_defects_fail() -> None:
    ensure_stage6h_built()
    valid = read_yaml(stage6h.CURRENT_STAGE_STATE_PATH)

    stale_top = dict(valid, stage_id="stage-6f")
    assert any("stage_id" in error for error in stage6h._current_state_integrity_errors(stale_top))

    stale_latest = dict(valid)
    stale_latest["latest_completed_stage"] = dict(valid["latest_completed_stage"], stage_id="stage-6f")
    assert any("nested latest_completed_stage" in error for error in stage6h._current_state_integrity_errors(stale_latest))

    stale_next = dict(valid)
    stale_next["next_stage"] = {
        "stage_id": "stage-6g",
        "stage_title": "Stage 6G - Final finite Stage 7 probe manifest and archive-run contract, without execution",
        "prompt_type": "codex_plan_mode_probe_manifest_finalization",
    }
    assert any("nested next_stage" in error for error in stage6h._current_state_integrity_errors(stale_next))

    stale_boolean = dict(valid, stage6g_final_manifest_required=True)
    assert any("stage6g_final_manifest_required" in error for error in stage6h._current_state_integrity_errors(stale_boolean))

    stale_handoff = dict(valid, post_push_handoff_locations=["codex-output/stage6g-codex-completion.md"])
    assert any("post_push_handoff_locations" in error for error in stage6h._current_state_integrity_errors(stale_handoff))


def test_stage6h_doc_staleness_and_operational_map_repairs() -> None:
    ensure_stage6h_built()
    doc_truth = read_yaml(stage6h.DOC_STALENESS_SOURCE_OF_TRUTH_PATH)
    operational = Path("docs/onboarding/operational-file-map.md").read_text(encoding="utf-8")
    assert doc_truth["latest_completed_stage_id"] == "stage-6h"
    assert doc_truth["recommended_next_stage_id"] == "stage-6i"
    assert doc_truth["historical_stage5ah_fields_superseded_by_stage6h_current_truth"] is True
    assert "Stage 6F - Final finite Stage 7" not in str(doc_truth)
    assert '--expected-latest-stage "Stage 5ED"' not in operational
    assert '--expected-next-stage "Stage 5EE"' not in operational
    assert "stage6h-stage6i-manifest-input-addendum.yaml" in operational


def test_stage6h_chatgpt_context_contains_required_substance() -> None:
    ensure_stage6h_built()
    text = Path("ChatGPT-ContextFile.md").read_text(encoding="utf-8")
    for topic in [
        "Stage 6H repaired Stage 6G current-state defects",
        "three-dot 7:8 angle41 bridge",
        "branch-dot binary 14/17/31/479 bridge",
        "PDD153 right-angle transform",
        "visual 7:8 ray to 133/d4",
        "folded 7:8/8:7 hits 50/51",
        "vertical split 72|9|72",
        "shared spine 81/81 surfaces",
        "word52 WAY and word55 READ prefix",
        "I AM/CIRCUMFERENCE mod153 edge bridge",
        "OUROBOROS variants 7/11/14 offsets",
        "future diagnostics remain disabled",
    ]:
        assert topic in text
    assert "created no Stage 7 manifest" in text


def test_stage6g_validator_allows_stage6h_current_state() -> None:
    ensure_stage6h_built()
    from libreprimus.token_block import stage6g

    result = stage6g.validate_stage6g_current_stage_transition()
    assert result.errors == []
