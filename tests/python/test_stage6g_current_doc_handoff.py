from __future__ import annotations

from pathlib import Path

from libreprimus.token_block import stage6g
from libreprimus.token_block.models import read_yaml

_BUILT = False


def ensure_stage6g_built() -> None:
    global _BUILT
    if _BUILT:
        return
    stage6g.build_stage6g(run_hook_checks=False)
    _BUILT = True


def test_stage6g_routes_stage6h_as_source_lock_addendum_not_manifest() -> None:
    ensure_stage6g_built()
    summary = read_yaml(stage6g.PROJECT_STATE_PATHS["summary"])
    current = read_yaml(stage6g.CURRENT_STAGE_STATE_PATH)
    assert summary["recommended_next_stage_id"] == "stage-6h"
    assert summary["recommended_next_stage_title"] == stage6g.NEXT_STAGE_TITLE
    assert summary["stage6h_source_lock_addendum_required"] is True
    assert summary["stage6h_final_manifest_required"] is False
    assert summary["stage6h_final_manifest_blocker_count"] == 1
    assert summary["stage6h_final_manifest_blockers"][0]["blocker_id"] == (
        "recent_dot_angle_triangle_material_not_source_locked"
    )
    assert summary["stage6h_can_attempt_final_manifest_without_prior_repair"] is False
    assert current["post_push_handoff_locations"] == [
        "codex-output/stage6g-codex-completion.md",
        "GitHub issue comment",
    ]
    assert current["stage7_execution_allowed_next"] is False
    assert current["stage7_zip_archive_creation_allowed_next"] is False


def test_stage6h_addendum_merges_inputs_and_records_chat_only_backlog() -> None:
    ensure_stage6g_built()
    addendum = read_yaml(stage6g.TOKEN_BLOCK_PATHS["stage6h_manifest_input_addendum"])
    nested = addendum["stage6h_input_addendum"]
    assert nested["includes_stage6c_ouroboros_i31_input_addendum"] is True
    assert nested["includes_stage6d_doublet_boundary_input_addendum"] is True
    assert nested["includes_stage6e_bridge_source_lock_addendum"] is True
    assert nested["includes_stage6f_traceability_cleanup"] is True
    assert nested["includes_stage6g_current_doc_handoff_repairs"] is True
    assert nested["acknowledges_recent_dot_angle_triangle_material_not_yet_committed"] is True
    assert nested["recent_dot_angle_triangle_material_source_lock_required_next"] is True
    assert addendum["not_final_stage7_manifest"] is True
    assert addendum["stage6h_final_manifest_required"] is False
    assert addendum["stage7_execution_allowed_from_this_addendum"] is False
    assert {row["backlog_id"] for row in addendum["pre_final_manifest_source_lock_backlog"]} == {
        "dot_angle41_triangle_anchor_bridge",
        "branch_dot_binary_parameter_bridge",
        "pdd153_right_triangle_coordinate_transform",
        "ouroboros_variant_mod153_offset_bridge",
    }
    assert all(row["source_status"] == "chat_only_pending_source_lock" for row in addendum["pre_final_manifest_source_lock_backlog"])


def test_current_docs_repaired_with_direct_file_content_checks() -> None:
    ensure_stage6g_built()
    start_here = Path("docs/onboarding/start-here.md").read_text(encoding="utf-8")
    source_map = Path("docs/onboarding/source-of-truth-map.md").read_text(encoding="utf-8")
    chatgpt = Path("ChatGPT-ContextFile.md").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "latest completed stage is Stage 6G" in start_here
    assert stage6g.NEXT_STAGE_TITLE in start_here
    assert "Stage 6H is source-lock/readiness addendum work, not final Stage 7 manifest construction" in start_here
    current_truth = source_map.split("## Current Operational Truth", 1)[1].split("\n## ", 1)[0]
    assert "latest completed stage is `stage-6g`" in current_truth
    assert "next stage is `stage-6h`" in current_truth
    assert "Stage 5ED" not in current_truth
    assert "Stage 5EE" not in current_truth
    current_chatgpt = chatgpt.split("## Current Project State", 1)[1].split("\n## ", 1)[0]
    assert "Stage 6G repaired stale current docs after Stage 6F" in current_chatgpt
    assert "dot-angle/right-triangle source-lock addendum" in current_chatgpt
    assert "## Historical Stage 6C" in chatgpt
    assert "## Historical Stage 6D" in chatgpt
    assert "## Historical Stage 6E" in chatgpt
    assert "## Historical Stage 6F" in chatgpt
    assert "Stage 6D source-locks the canonical doublet boundary" not in readme


def test_negative_stale_current_doc_strings_do_not_recur() -> None:
    ensure_stage6g_built()
    files = [
        Path("docs/onboarding/start-here.md"),
        Path("docs/onboarding/source-of-truth-map.md"),
        Path("ChatGPT-ContextFile.md"),
        Path("README.md"),
        Path("AGENTS.md"),
        Path("data/project-state/current-stage-state.yaml"),
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in files)
    assert "Stage 6E was complete and Stage 6F was next" not in combined
    assert "Stage 6E as complete and Stage 6F as next" not in combined
    assert "Stage 5ED as latest complete and Stage 5EE as next" not in combined
    assert "Stage 6F is next" not in combined
    assert "codex-output/stage6d-codex-completion.md" not in combined
    assert "codex-output/stage6e-codex-completion.md" not in combined
    assert "codex-output/stage6f-codex-completion.md" not in combined
    assert "Stage 6H - Final" not in combined
    assert "Stage 6H final manifest" not in combined


def test_acceptance_policy_is_file_backed_and_integrated() -> None:
    ensure_stage6g_built()
    policy = stage6g.ACCEPTANCE_POLICY_PATH.read_text(encoding="utf-8")
    for section in stage6g.ACCEPTANCE_POLICY_SECTIONS:
        assert f"## {section}" in policy
    assert 'Bad instruction:\n"Update AGENTS.md."' in policy
    assert "Update AGENTS.md as a whole final file" in policy
    for path in [
        Path("AGENTS.md"),
        Path("docs/onboarding/start-here.md"),
        Path("docs/onboarding/source-of-truth-map.md"),
        Path("docs/onboarding/operational-file-map.md"),
        Path("docs/reference/token-block-cli.md"),
    ]:
        assert stage6g.ACCEPTANCE_POLICY_PATH.as_posix() in path.read_text(encoding="utf-8")


def test_stage6g_hook_record_is_honest_about_actual_runner_risk() -> None:
    ensure_stage6g_built()
    record = read_yaml(stage6g.PROJECT_STATE_PATHS["hook_runner_confirmation"])
    assert record["previous_operator_observed_hook_exit_code_1"] is True
    assert record["hook_default_exit_zero_verified"] is True
    assert record["hook_json_launcher_exit_zero_where_supported"] is True
    assert record["actual_codex_runner_semantics_fully_simulated"] is False
    assert record["operator_confirmation_required_after_stage6g_push"] is True
    assert record["blocks_current_doc_repair_completion"] is False
    assert record["blocks_claiming_hook_fully_fixed"] is True


def test_prior_stage_patch_is_ledgered_without_payload_rewrite() -> None:
    ensure_stage6g_built()
    ledger = read_yaml(stage6g.PROJECT_STATE_PATHS["prior_stage_repair_ledger"])
    rows = ledger["prior_stage_files_touched"]
    touched = {row["touched_file"]: row for row in rows}
    assert "python/libreprimus/token_block/stage6f.py" in touched
    assert "python/libreprimus/token_block/stage6b.py" in touched
    assert all(row["historical_payload_changed"] is False for row in rows)
    assert all(row["source_lock_payload_changed"] is False for row in rows)


def test_stage6g_aggregate_validation_and_guardrails() -> None:
    ensure_stage6g_built()
    result = stage6g.validate_stage6g()
    assert result.errors == []
    for path in stage6g.DATA_PATHS.values():
        payload = read_yaml(path)
        if isinstance(payload, dict):
            assert payload.get("stage7_execution_allowed_next") is not True
            assert payload.get("stage7_manifest_created_now") is not True
            assert payload.get("probe_execution_performed_now") is not True
            assert payload.get("route_stream_generated_now") is not True
            assert payload.get("solve_claim") is False
