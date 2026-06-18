from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

from libreprimus.token_block import stage6f
from test_stage6_common import load_yaml


def ensure_stage6f_built() -> None:
    if not stage6f.PROJECT_STATE_PATHS["summary"].exists():
        stage6f.build_stage6f()


def test_stage6f_routes_to_stage6g_with_no_execution_or_artifacts() -> None:
    ensure_stage6f_built()
    summary = load_yaml(stage6f.PROJECT_STATE_PATHS["summary"])
    current = load_yaml("data/project-state/current-stage-state.yaml")
    assert summary["stage_id"] == "stage-6f"
    assert summary["previous_stage_id"] == "stage-6e"
    assert summary["recommended_next_stage_id"] == "stage-6g"
    assert summary["stage6g_blocker_count"] == 0
    assert summary["stage6g_can_attempt_final_manifest_without_prior_repair"] is True
    allowed_current_routes = {
        "stage-6f": ("stage-6e", "stage-6g"),
        "stage-6g": ("stage-6f", "stage-6h"),
        "stage-6h": ("stage-6g", "stage-6i"),
    }
    previous, next_stage = allowed_current_routes[current["latest_completed_stage_id"]]
    assert current["previous_completed_stage_id"] == previous
    assert current["recommended_next_stage_id"] == next_stage
    for key in [
        "stage7_execution_allowed_next",
        "stage7_zip_archive_creation_allowed_next",
        "stage6f_final_finite_stage7_manifest_created_now",
        "stage6f_archive_run_contract_finalized_now",
        "stage6f_creates_stage7_result_archive_now",
        "stage6f_generates_stage7_outputs_now",
        "stage6f_runs_any_probe_now",
        "new_theory_source_locks_created_now",
        "new_future_probe_ids_created_now",
        "new_number_fact_overlays_created_now",
        "stage7_manifest_created_now",
        "stage7_archive_created_now",
        "route_stream_generated_now",
        "real_byte_stream_generated",
        "solve_claim",
    ]:
        assert summary[key] is False
        assert current[key] is False


def test_stage6f_file_content_validators_read_final_docs() -> None:
    ensure_stage6f_built()
    record = load_yaml(stage6f.PROJECT_STATE_PATHS["edited_document_integrity_review"])
    assert record["edited_document_integrity_validator_reads_final_files_directly"] is True
    assert record["record_claim_only_validation_used"] is False
    assert record["malformed_repetition_found_after_repair"] is False
    assert record["errors"] == []
    for path in [
        "README.md",
        "AGENTS.md",
        "STATUS.md",
        "ROADMAP.md",
        "TESTING.md",
        "ChatGPT-ContextFile.md",
        "data/project-state/current-stage-state.yaml",
    ]:
        text = Path(path).read_text(encoding="utf-8")
        assert "Stage 6E consolidated Stage 6F readiness after Stage 6E consolidated" not in text
        assert "codex-output/stage6d-codex-completion.md" not in text
    assert stage6f.validate_stage6f_edited_document_integrity().validation_error_count == 0
    assert stage6f.validate_stage6f_current_mirror_consistency().validation_error_count == 0


def test_stage6f_chatgpt_context_preserves_stage6e_and_stage6f_topics() -> None:
    ensure_stage6f_built()
    record = load_yaml(stage6f.PROJECT_STATE_PATHS["chatgpt_context_validation"])
    assert record["chatgpt_context_file_read_directly"] is True
    assert record["errors"] == []
    text = Path("ChatGPT-ContextFile.md").read_text(encoding="utf-8")
    for topic in [
        "Stage 6E preserved Stage 6C OUROBOROS/I31 and Stage 6D doublet/boundary addenda",
        "CIRCUMFERENCE = 398 = 2 * GP(I AM)",
        "C-to-F finite mask family",
        "AN END = FIVE DOTS = 311 = prime(64)",
        "Page32 3222 = 18 * 179",
        "WE MUST SHED OUR OWN CIRCUMFERENCES = 1031",
        "preflight self-report exclusion",
        "metadata-only probe traceability semantic cleanup",
        "Ciada/Cicada alias policy",
        "Stage 6G routing",
    ]:
        assert topic in text


def test_stage6f_preflight_report_selection_excludes_self_and_stop_reports() -> None:
    ensure_stage6f_built()
    hook_path = Path(".codex/hooks/doc_staleness_preflight.py")
    sys.path.insert(0, str(hook_path.parent.resolve()))
    spec = importlib.util.spec_from_file_location("stage6f_doc_staleness_preflight", hook_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert (
        module._may_use_as_latest_report(
            Path("experiments/results/doc-drift/codex-preprompt-doc-staleness-preflight.json"),
            {"report_kind": "codex_preprompt_doc_staleness_preflight"},
        )
        is False
    )
    assert (
        module._may_use_as_latest_report(
            Path("experiments/results/doc-drift/codex-stop-hook-stale-current-audit.json"),
            {"report_kind": "codex_stop_doc_staleness_guard"},
        )
        is False
    )
    assert (
        module._may_use_as_latest_report(
            Path("experiments/results/doc-drift/stage6f-local-stale-current-triage.json"),
            {"report_kind": "local_stale_current_reproduction"},
        )
        is True
    )
    assert stage6f.validate_stage6f_preflight_report_selection().validation_error_count == 0


def test_stage6f_hook_verification_is_honest_about_runner_semantics() -> None:
    ensure_stage6f_built()
    hooks = load_yaml(stage6f.PROJECT_STATE_PATHS["hook_verification_summary"])
    direct = hooks["hook_verification_layers"]["direct_python_scripts"]
    actual = hooks["hook_verification_layers"]["actual_codex_runner_semantics"]
    assert hooks["previous_operator_observed_hook_exit_code_1"] is True
    assert hooks["hook_default_exit_zero_verified"] is True
    assert direct["default_strict_env_unset"] is True
    assert direct["default_exit_zero"] is True
    assert actual["fully_simulated"] is False
    assert hooks["hook_actual_codex_runner_verified_by_operator_after_stage6f_push"] is False
    assert hooks["operator_followup_required_to_confirm_hook_runner"] is True


def test_stage6f_traceability_semantics_remove_fake_source_root_requirement() -> None:
    ensure_stage6f_built()
    repair = load_yaml(stage6f.TOKEN_BLOCK_PATHS["probe_source_traceability_semantics_repair"])
    assert repair["stage6e_traceability_records_patched_now"] is False
    assert repair["stage6e_source_lock_payloads_rewritten_now"] is False
    metadata_only_rows = [row for row in repair["traceability_rows"] if row["source_dependency_type"] == "committed_metadata_only"]
    assert metadata_only_rows
    for row in metadata_only_rows:
        assert row["source_roots"] == []
        assert row["local_source_presence_required_before_stage7_execution"] is False
        assert "source_root_present" not in row["stage7_execution_preconditions"]
        assert row["source_root_present_precondition_not_applicable"] is True
    assert stage6f.validate_stage6f_traceability_cleanup().validation_error_count == 0


def test_stage6f_alias_policy_dju_gap_and_acceptance_docs_are_integrated() -> None:
    ensure_stage6f_built()
    alias = load_yaml(stage6f.SOURCE_HARVESTER_PATHS["ciada_cicada_alias_policy"])
    dju = load_yaml(stage6f.SOURCE_HARVESTER_PATHS["dju_bei_gap_source_crosslink"])
    addendum = load_yaml(stage6f.TOKEN_BLOCK_PATHS["stage6g_manifest_input_addendum"])
    acceptance = Path("docs/onboarding/codex-acceptance-criteria.md").read_text(encoding="utf-8")
    assert alias["canonical_local_root_for_iddqd_v2"] == "third_party/CiadaSolversIddqd_v2"
    assert alias["semantic_evidence_from_spelling_difference"] is False
    assert addendum["includes_stage6f_ciada_cicada_alias_policy"] is True
    assert dju["exact_span_found"] is False
    assert dju["backlog_source_crosslink_present"] is True
    assert dju["stage6g_manifest_eligible"] is False
    assert "Bad instruction:" in acceptance
    assert "Good instruction:" in acceptance
    assert stage6f.validate_stage6f_alias_policy().validation_error_count == 0
    assert stage6f.validate_stage6f_dju_bei_crosslink().validation_error_count == 0
    assert stage6f.validate_stage6f_acceptance_policy().validation_error_count == 0


def test_stage6f_aggregate_validation_and_stage7_artifact_absence_pass() -> None:
    ensure_stage6f_built()
    assert stage6f.validate_stage6f_stage7_artifact_absence().validation_error_count == 0
    assert stage6f.validate_stage6f().validation_error_count == 0
