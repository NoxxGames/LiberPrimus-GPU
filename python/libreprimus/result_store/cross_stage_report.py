"""Cross-stage result-surface report for Stage 4P."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.result_store.method_status_join import build_method_status_join
from libreprimus.result_store.score_summary_unification import build_unified_score_summaries
from libreprimus.result_store.stage4p_export import read_json, read_jsonl, resolve_repo_path, write_json, write_yaml
from libreprimus.result_store.unified_models import (
    CROSS_STAGE_REPORT_JSON,
    METHOD_STATUS_JOIN_JSON,
    SOURCE_INVENTORY_JSON,
    STAGE4P_OUTPUT_DIR,
    STAGE4P_SUMMARY_PATH,
    SUMMARY_JSON,
    UNIFIED_RESULT_JSONL,
    UNIFIED_SCORE_JSONL,
)


def build_cross_stage_report(
    manifest_path: Path,
    *,
    out_dir: Path = STAGE4P_OUTPUT_DIR,
    summary_out: Path = STAGE4P_SUMMARY_PATH,
) -> dict[str, Any]:
    """Build the Stage 4P cross-stage report and committed summary."""

    resolved_out = resolve_repo_path(out_dir)
    if not (resolved_out / UNIFIED_SCORE_JSONL).is_file():
        build_unified_score_summaries(manifest_path, out_dir=out_dir)
    if not (resolved_out / METHOD_STATUS_JOIN_JSON).is_file():
        build_method_status_join(out_dir=out_dir)
    inventory = list(read_json(resolved_out / SOURCE_INVENTORY_JSON).get("records", []))
    results = read_jsonl(resolved_out / UNIFIED_RESULT_JSONL)
    scores = read_jsonl(resolved_out / UNIFIED_SCORE_JSONL)
    joins = list(read_json(resolved_out / METHOD_STATUS_JOIN_JSON).get("records", []))
    report = _report_payload(inventory, results, scores, joins)
    summary = _summary_payload(report)
    write_json(resolved_out / CROSS_STAGE_REPORT_JSON, report)
    write_json(resolved_out / SUMMARY_JSON, summary)
    write_yaml(summary_out, summary)
    return summary


def _report_payload(
    inventory: list[dict[str, Any]],
    results: list[dict[str, Any]],
    scores: list[dict[str, Any]],
    joins: list[dict[str, Any]],
) -> dict[str, Any]:
    confidence_counts = Counter(str(record.get("confidence_label", "scoring_not_available")) for record in scores)
    method_status_counts = Counter(str(record.get("method_status", "unknown")) for record in joins)
    retirement_counts = Counter(str(record.get("retirement_status", "unknown")) for record in joins)
    return {
        "record_type": "cross_stage_comparison_report",
        "stage_id": "stage-4p",
        "total_source_inventory_records": len(inventory),
        "committed_summaries_loaded": _count_status(inventory, "committed_summary_present"),
        "optional_generated_outputs_present": _count_status(inventory, "local_generated_present"),
        "optional_generated_outputs_missing": _count_status(inventory, "optional_generated_missing"),
        "unified_result_records": len(results),
        "unified_score_summary_records": len(scores),
        "method_status_joins": len(joins),
        "stages_represented": sorted({str(record.get("source_stage_id")) for record in results}),
        "method_families_represented": sorted({str(record.get("method_family")) for record in results}),
        "confidence_label_counts": dict(sorted(confidence_counts.items())),
        "method_status_counts": dict(sorted(method_status_counts.items())),
        "retirement_status_counts": dict(sorted(retirement_counts.items())),
        "records_with_output_hashes": sum(
            1 for record in results if record.get("output_text_hash") or record.get("output_token_hash")
        ),
        "records_with_parity_expectations": sum(
            1 for record in results if record.get("result_source_kind") == "cpu_batch_parity_expectation"
        ),
        "records_without_score_summaries": sum(
            1 for record in results if record.get("score_summary_available") is not True
        ),
        "records_skipped_due_raw_required_input": _count_status(inventory, "skipped_raw_required"),
        "records_skipped_due_unknown_schema": _count_status(inventory, "skipped_schema_unknown"),
        "score_interpretation": "triage_only",
        "no_solve_claim": True,
        "solve_claim": False,
        "cuda_used": False,
        "generated_outputs_committed": False,
        "raw_data_processed": False,
        "new_experiment_executed": False,
        "new_scorer_added": False,
    }


def _summary_payload(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "stage4p_result_store_score_summary_unification_summary",
        "schema": "schemas/results/result-store-unification-summary-v0.schema.json",
        "stage_id": "stage-4p",
        "status": "complete",
        "source_inventory_records": report["total_source_inventory_records"],
        "committed_summaries_loaded": report["committed_summaries_loaded"],
        "optional_generated_outputs_present": report["optional_generated_outputs_present"],
        "optional_generated_outputs_missing": report["optional_generated_outputs_missing"],
        "unified_result_records": report["unified_result_records"],
        "unified_score_summary_records": report["unified_score_summary_records"],
        "method_status_joins": report["method_status_joins"],
        "stages_represented": report["stages_represented"],
        "method_families_represented": report["method_families_represented"],
        "confidence_label_counts": report["confidence_label_counts"],
        "method_status_counts": report["method_status_counts"],
        "retirement_status_counts": report["retirement_status_counts"],
        "records_with_output_hashes": report["records_with_output_hashes"],
        "records_with_parity_expectations": report["records_with_parity_expectations"],
        "records_skipped_due_raw_required_input": report["records_skipped_due_raw_required_input"],
        "cross_stage_report_written": True,
        "score_summary_contract": "stage4i",
        "result_store_contract": "stage4p",
        "no_solve_claim": True,
        "cuda_used": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
        "new_experiment_executed": False,
        "new_scorer_added": False,
        "notes": [
            "Stage 4P unifies result surfaces for reporting only.",
            "Generated unified records remain ignored under experiments/results/result-store-unification/stage4p/.",
        ],
    }


def _count_status(records: list[dict[str, Any]], status: str) -> int:
    return sum(1 for record in records if record.get("source_presence_status") == status)
