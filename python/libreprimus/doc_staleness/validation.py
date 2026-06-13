"""Validation helpers for doc-staleness records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_record(path: Path) -> dict:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return payload


def validate_stage5ab_summary(path: Path) -> list[str]:
    payload = load_record(path)
    errors: list[str] = []
    expected_false = (
        "cuda_execution_performed",
        "cuda_source_modified",
        "benchmark_performed",
        "scored_experiments_executed",
        "website_expansion_performed",
        "raw_data_processed",
        "generated_outputs_committed",
        "codex_output_committed",
        "solve_claim",
    )
    for key in expected_false:
        if payload.get(key) is not False:
            errors.append(f"{key} must be false")
    if payload.get("new_cuda_kernels_added") != 0:
        errors.append("new_cuda_kernels_added must be 0")
    if payload.get("next_selected_stage") != "Stage 5AC - selected from Stage 5AA outcome after stale-doc repair":
        errors.append("next_selected_stage must be Stage 5AC selected from Stage 5AA outcome")
    return errors


def validate_stage5ah_doc_staleness_records(
    *,
    source_of_truth_path: Path,
    findings_path: Path,
    stage_ledger_coverage_path: Path,
    operational_file_map_coverage_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    results_dir: Path,
) -> list[str]:
    """Validate Stage 5AH staleness repair records and generated reports."""

    errors: list[str] = []
    records = {
        "source_of_truth": load_record(source_of_truth_path),
        "findings": load_record(findings_path),
        "stage_ledger_coverage": load_record(stage_ledger_coverage_path),
        "operational_file_map_coverage": load_record(operational_file_map_coverage_path),
        "next_stage_decision": load_record(next_stage_decision_path),
        "summary": load_record(summary_path),
    }
    source_stage_id = records["source_of_truth"].get("stage_id")
    if source_stage_id not in {"stage-5ah", "stage-5eg", "stage-5eh", "stage-5ei"}:
        errors.append(f"stage_id_expected_'stage-5ah'_or_successor_got_{source_stage_id!r}")
    _expect(records["summary"], "stage_id", "stage-5ah", errors)
    _expect(records["summary"], "status", "complete", errors)
    _expect(
        records["next_stage_decision"],
        "selected_next_stage_title",
        "Stage 5AI - curated research bundle extraction from local source inventory",
        errors,
    )
    for name, payload in records.items():
        _validate_false_flags(name, payload, errors)
    for key in (
        "stale_findings_after_repair",
        "readme_stage_ledger_findings_after",
        "operational_file_map_coverage_findings_after",
    ):
        if int(records["summary"].get(key, -1)) != 0:
            errors.append(f"summary_{key}_must_be_0")
    if int(records["stage_ledger_coverage"].get("stage_ledger_findings_after_repair", -1)) != 0:
        errors.append("stage_ledger_findings_after_repair_must_be_0")
    if int(records["operational_file_map_coverage"].get("coverage_findings_after_repair", -1)) != 0:
        errors.append("coverage_findings_after_repair_must_be_0")
    required_reports = (
        "stale_stage_ledger_report.json",
        "operational_file_map_coverage_report.json",
        "current_next_stage_report.json",
        "readme_stage_coverage_report.json",
        "doc_staleness_summary.json",
        "warnings.jsonl",
    )
    for report in required_reports:
        if not (results_dir / report).is_file():
            errors.append(f"missing_generated_report:{report}")
    _validate_report_count(
        results_dir / "stale_stage_ledger_report.json",
        "finding_count",
        "stale_stage_ledger_report_findings_must_be_0",
        errors,
    )
    _validate_report_count(
        results_dir / "operational_file_map_coverage_report.json",
        "coverage_finding_count",
        "operational_file_map_coverage_report_findings_must_be_0",
        errors,
    )
    _validate_report_count(
        results_dir / "current_next_stage_report.json",
        "finding_count",
        "current_next_stage_report_findings_must_be_0",
        errors,
    )
    _validate_report_count(
        results_dir / "readme_stage_coverage_report.json",
        "finding_count",
        "readme_stage_coverage_report_findings_must_be_0",
        errors,
    )
    return errors


def _expect(payload: dict[str, Any], key: str, value: Any, errors: list[str]) -> None:
    if payload.get(key) != value:
        errors.append(f"{key}_expected_{value!r}_got_{payload.get(key)!r}")


def _validate_false_flags(name: str, payload: dict[str, Any], errors: list[str]) -> None:
    false_flags = (
        "network_fetch_performed",
        "live_web_scrape_performed",
        "online_repo_clone_performed",
        "google_drive_storage_used",
        "raw_data_processed",
        "generated_outputs_committed",
        "codex_output_committed",
        "cuda_execution_performed",
        "cuda_source_modified",
        "new_cuda_kernel_added",
        "benchmark_performed",
        "scored_experiments_executed",
        "website_expansion_performed",
        "solve_claim",
    )
    for flag in false_flags:
        if flag in payload and payload.get(flag) is not False:
            errors.append(f"{name}:{flag}_must_be_false")
    if payload.get("new_cuda_kernels_added", 0) != 0:
        errors.append(f"{name}:new_cuda_kernels_added_must_be_0")


def _validate_report_count(path: Path, key: str, error_id: str, errors: list[str]) -> None:
    if not path.is_file():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    if int(payload.get(key, -1)) != 0:
        errors.append(error_id)
