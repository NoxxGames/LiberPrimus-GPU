from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

import pytest

from libreprimus.token_block import stage6, stage6b
from test_stage6_common import load_yaml


def ensure_stage6b_built() -> None:
    if not stage6b.PROJECT_STATE_PATHS["summary"].exists():
        stage6.build_stage6()
        stage6b.build_stage6b()


def test_stage6b_summary_routes_to_stage6c_and_blocks_execution() -> None:
    ensure_stage6b_built()
    summary = load_yaml(stage6b.PROJECT_STATE_PATHS["summary"])
    assert summary["stage_id"] == "stage-6b"
    assert summary["recommended_next_stage_id"] == "stage-6c"
    assert summary["stage7_execution_allowed_next"] is False
    assert summary["stage7_zip_archive_creation_allowed_next"] is False
    assert summary["stage6b_final_finite_stage7_manifest_created_now"] is False
    assert summary["stage6b_archive_run_contract_finalized_now"] is False


def test_stage6b_repair_ledger_lists_stage6_yaml_and_code_patches() -> None:
    ensure_stage6b_built()
    ledger = load_yaml(stage6b.PROJECT_STATE_PATHS["stage6_registry_repair_ledger"])
    assert ledger["stage6_records_patched_now"] is True
    assert "python/libreprimus/token_block/stage6.py" in ledger["patched_stage6_files"]
    assert "data/token-block/stage6-discovery-probe-manifest-registry.yaml" in ledger["patched_stage6_files"]
    assert ledger["historical_source_lock_records_rewritten"] is False
    assert ledger["probe_execution_performed_now"] is False
    for entry in ledger["repair_entries"]:
        assert entry["old_problem"]
        assert entry["new_value"]
        assert entry["repair_reason"] == "stage6_probe_family_source_readiness_misclassification"


def test_stage6b_validators_accept_repaired_stage6_records() -> None:
    ensure_stage6b_built()
    assert stage6.validate_stage6().validation_error_count == 0
    assert stage6b.validate_stage6b().validation_error_count == 0


def test_stage6b_family_source_and_readiness_maps_are_complete() -> None:
    ensure_stage6b_built()
    family = load_yaml(stage6b.PROJECT_STATE_PATHS["probe_family_mapping_repair"])
    sources = load_yaml(stage6b.PROJECT_STATE_PATHS["probe_source_mapping_repair"])
    readiness = load_yaml(stage6b.PROJECT_STATE_PATHS["readiness_classification_repair"])
    expected_ids = set(stage6.expected_probe_classification_for_validation())
    assert {item["diagnostic_id"] for item in family["probe_mappings"]} == expected_ids
    assert {item["diagnostic_id"] for item in sources["probe_sources"]} == expected_ids
    assert {item["diagnostic_id"] for item in readiness["probe_readiness"]} == expected_ids
    assert readiness["toolchain_sensitive_probes_unconditionally_ready"] is False
    for item in sources["probe_sources"]:
        assert item["source_records"] or item["source_roots"] or item["source_gap_or_stage6c_precondition"]


def test_stage6b_stage7_menu_is_partial_and_not_executable() -> None:
    ensure_stage6b_built()
    menu = load_yaml(stage6b.PROJECT_STATE_PATHS["stage7_menu_status_repair"])
    assert menu["candidate_menu_status"] == "partial_foundation_only"
    assert menu["stage7_candidate_menu_complete"] is False
    assert menu["not_stage7_execution_manifest"] is True
    assert menu["stage6c_final_menu_required"] is True
    assert menu["stage7_execution_allowed_from_this_menu"] is False
    assert menu["stage7_zip_archive_creation_allowed_from_this_menu"] is False


def test_stage6b_current_stage_transition_record() -> None:
    ensure_stage6b_built()
    current = load_yaml("data/project-state/current-stage-state.yaml")
    allowed_current_routes = {
        "stage-6b": ("stage-6", "stage-6c"),
        "stage-6c": ("stage-6b", "stage-6d"),
        "stage-6d": ("stage-6c", "stage-6e"),
    }
    previous, next_stage = allowed_current_routes[current["latest_completed_stage_id"]]
    assert current["previous_completed_stage_id"] == previous
    assert current["recommended_next_stage_id"] == next_stage
    transition = load_yaml(stage6b.PROJECT_STATE_PATHS["current_stage_transition"])
    assert transition["latest_completed_stage_id"] == "stage-6b"
    assert transition["previous_completed_stage_id"] == "stage-6"
    assert transition["recommended_next_stage_id"] == "stage-6c"
    assert current["stage7_execution_allowed_next"] is False
    assert current["stage7_zip_archive_creation_allowed_next"] is False


def test_stage6b_codex_hook_scripts_default_exit_zero_from_root_and_subdir() -> None:
    ensure_stage6b_built()
    root = Path.cwd()
    nested = root / "python/libreprimus"
    scripts = [
        root / ".codex/hooks/session_start_current_truth_context.py",
        root / ".codex/hooks/stop_doc_staleness_guard.py",
    ]
    for cwd in (root, nested):
        for script in scripts:
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=cwd,
                input="{}",
                capture_output=True,
                text=True,
                check=False,
                timeout=120,
            )
            assert result.returncode == 0


def test_stage6b_hook_reports_are_ignored() -> None:
    ensure_stage6b_built()
    result = subprocess.run(
        ["git", "check-ignore", "-q", "experiments/results/doc-drift/stage6b-stop-hook-audit.json"],
        check=False,
    )
    assert result.returncode == 0


def test_stage6b_hook_common_default_and_strict_failure_modes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from importlib import util

    module_path = Path(".codex/hooks/hook_common.py")
    spec = util.spec_from_file_location("stage6b_hook_common", module_path)
    assert spec and spec.loader
    hook_common = util.module_from_spec(spec)
    spec.loader.exec_module(hook_common)

    report = tmp_path / "report.json"
    default_exit = hook_common.run_hook_command(
        [sys.executable, "-c", "raise SystemExit(2)"],
        root=Path.cwd(),
        report_path=report,
        timeout=30,
    )
    assert default_exit == 0

    monkeypatch.setenv("LIBERPRIMUS_CODEX_HOOK_STRICT", "1")
    strict_exit = hook_common.run_hook_command(
        [sys.executable, "-c", "raise SystemExit(2)"],
        root=Path.cwd(),
        report_path=report,
        timeout=30,
    )
    assert strict_exit == 2


def test_stage6b_hooks_json_uses_command_handlers_and_no_agent_invocation() -> None:
    hooks = load_yaml(".codex/hooks.json")
    raw = Path(".codex/hooks.json").read_text(encoding="utf-8")
    assert "agent" not in raw.lower()
    for hook_group in hooks["hooks"].values():
        for item in hook_group:
            for hook in item["hooks"]:
                assert hook["type"] == "command"


def test_stage6b_protected_local_paths_are_not_outputs() -> None:
    ensure_stage6b_built()
    stage6b_outputs = {path.as_posix() for path in stage6b.DATA_PATHS.values()}
    stage6b_outputs.update(path.as_posix() for path in stage6b.SCHEMA_PATHS.values())
    assert not stage6b_outputs.intersection(stage6.PROTECTED_LOCAL_PATHS)
    noncommit = load_yaml(stage6b.SOURCE_HARVESTER_PATHS["raw_source_noncommit_proof"])
    assert noncommit["protected_local_paths_staged"] is False
    assert noncommit["hook_reports_staged"] is False
    assert noncommit["codex_output_staged"] is False


def test_stage6b_no_forbidden_guardrails_open() -> None:
    ensure_stage6b_built()
    summary = load_yaml(stage6b.PROJECT_STATE_PATHS["summary"])
    for key, expected in stage6b.FORBIDDEN_FALSE.items():
        if key in summary:
            assert summary[key] is expected


def test_stage6b_default_hook_strict_env_var_name() -> None:
    ensure_stage6b_built()
    hook_summary = load_yaml(stage6b.PROJECT_STATE_PATHS["hook_stabilization_summary"])
    assert hook_summary["hook_strict_env_var"] == "LIBERPRIMUS_CODEX_HOOK_STRICT"
    assert os.environ.get("LIBERPRIMUS_CODEX_HOOK_STRICT") is None
