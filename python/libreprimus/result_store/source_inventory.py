"""Source inventory for Stage 4P result-store unification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root
from libreprimus.result_store.stage4p_export import resolve_repo_path, write_json, write_jsonl
from libreprimus.result_store.unified_models import (
    SOURCE_INVENTORY_JSON,
    STAGE4P_OUTPUT_DIR,
    WARNINGS_JSONL,
    ResultSourceDefinition,
)

DEFAULT_SOURCES: tuple[ResultSourceDefinition, ...] = (
    ResultSourceDefinition(
        "stage2b-result-store-summary",
        "stage-2b",
        "solved_baseline_result_store",
        "experiments/results/result-store/stage2b/summary.json",
        required=False,
        optional_generated=True,
        method_family="result_store_score_summary_unification",
        source_record_type="experiment_run_summary",
    ),
    ResultSourceDefinition(
        "stage2b-result-store-run-records",
        "stage-2b",
        "solved_baseline_result_store",
        "experiments/results/result-store/stage2b/run_records.jsonl",
        required=False,
        optional_generated=True,
        method_family="result_store_score_summary_unification",
        source_record_type="experiment_run_record",
    ),
    ResultSourceDefinition(
        "stage3-bounded-summary-missing",
        "stage-3a-3j",
        "bounded_experiment_summary",
        "experiments/results/bounded-auto-runs/stage3a/summary.json",
        required=False,
        optional_generated=True,
        method_family="caesar_affine",
        source_record_type="bounded_experiment_summary",
    ),
    ResultSourceDefinition(
        "stage4h-cpu-batch-summary",
        "stage-4h",
        "cpu_batch_result",
        "data/research/stage4h-cpu-batch-api-summary.yaml",
        required=True,
        method_family="cpu_batch_transform_api",
        source_record_type="stage4h_cpu_batch_api_summary",
    ),
    ResultSourceDefinition(
        "stage4i-scoring-records",
        "stage-4i",
        "scoring_record",
        "data/scoring/scorer-records-v0.yaml",
        required=True,
        method_family="scoring_consolidation",
        source_record_type="scorer_records",
    ),
    ResultSourceDefinition(
        "stage4i-calibration-report",
        "stage-4i",
        "scoring_record",
        "data/scoring/stage4i-calibration-report-v0.yaml",
        required=True,
        method_family="scoring_consolidation",
        source_record_type="calibration_report",
    ),
    ResultSourceDefinition(
        "stage4j-observation-review-summary",
        "stage-4j",
        "observation_promotion_summary",
        "data/observations/review/stage4j-observation-review-summary.yaml",
        required=True,
        method_family="observation_review_workflow",
        source_record_type="observation_review_summary",
    ),
    ResultSourceDefinition(
        "stage4k-source-lock-summary",
        "stage-4k",
        "source_lock_summary",
        "data/locks/third-party/source-snapshots/stage4k-source-lock-summary.yaml",
        required=True,
        method_family="source_lock_snapshots",
        source_record_type="source_lock_summary",
    ),
    ResultSourceDefinition(
        "stage4l-promotion-summary",
        "stage-4l",
        "observation_promotion_summary",
        "data/observations/review/stage4l-reviewed-observation-promotion-summary.yaml",
        required=True,
        method_family="observation_promotion_ledger",
        source_record_type="promotion_summary",
    ),
    ResultSourceDefinition(
        "stage4m-image-preflight-summary",
        "stage-4m",
        "image_preflight_summary",
        "data/observations/visual/stage4m-image-preflight-summary.yaml",
        required=True,
        method_family="image_source_variant_compression_preflight",
        source_record_type="image_preflight_summary",
    ),
    ResultSourceDefinition(
        "stage4n-positive-control-summary",
        "stage-4n",
        "fixture_readiness_summary",
        "data/observations/stego/stage4n-positive-control-summary.yaml",
        required=True,
        method_family="stego_audio_positive_control_readiness",
        source_record_type="positive_control_summary",
    ),
    ResultSourceDefinition(
        "stage4o-cpu-batch-summary",
        "stage-4o",
        "cpu_batch_result",
        "data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml",
        required=True,
        method_family="cpu_batch_transform_api",
        source_record_type="stage4o_cpu_batch_adapter_expansion_summary",
    ),
    ResultSourceDefinition(
        "stage4o-cpu-batch-results",
        "stage-4o",
        "cpu_batch_result",
        "experiments/results/cpu-batch/stage4o/result_records.jsonl",
        required=False,
        optional_generated=True,
        method_family="cpu_batch_transform_api",
        source_record_type="cpu_batch_result_record",
    ),
    ResultSourceDefinition(
        "stage4o-cpu-batch-parity",
        "stage-4o",
        "cpu_batch_parity_expectation",
        "experiments/results/cpu-batch/stage4o/parity_expectations.jsonl",
        required=False,
        optional_generated=True,
        method_family="cpu_batch_transform_api",
        source_record_type="cpu_batch_parity_expectation",
    ),
    ResultSourceDefinition(
        "stage4o-scoring-compatibility",
        "stage-4o",
        "scoring_record",
        "experiments/results/cpu-batch/stage4o/scoring_compatibility.json",
        required=False,
        optional_generated=True,
        method_family="scoring_consolidation",
        source_record_type="cpu_batch_scoring_compatibility",
    ),
    ResultSourceDefinition(
        "method-family-status-records",
        "stage-3y",
        "method_family_status",
        "data/research/method-family-status-records-v0.yaml",
        required=True,
        method_family="result_store_score_summary_unification",
        source_record_type="method_family_status_records",
    ),
    ResultSourceDefinition(
        "method-retirement-records",
        "stage-3y",
        "method_retirement",
        "data/research/method-retirement-records-v0.yaml",
        required=True,
        method_family="result_store_score_summary_unification",
        source_record_type="method_retirement_records",
    ),
    ResultSourceDefinition(
        "raw-discord-results-skipped",
        "stage-3n",
        "bounded_experiment_summary",
        "third_party/LiberPrimusDiscordChats",
        required=False,
        raw_required=True,
        method_family="discord_ingestion_review",
        source_record_type="raw_required_source",
    ),
)


def build_source_inventory_from_manifest(
    manifest_path: Path,
    *,
    out_dir: Path = STAGE4P_OUTPUT_DIR,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Build and write Stage 4P source inventory records."""

    definitions = _source_definitions_from_manifest(manifest_path)
    records: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    for definition in sorted(definitions, key=lambda item: item.source_id):
        record = _inventory_record(definition)
        records.append(record)
        if record["source_presence_status"] in {
            "optional_generated_missing",
            "skipped_raw_required",
            "skipped_schema_unknown",
        }:
            warnings.append(
                {
                    "source_id": record["source_id"],
                    "warning": record["source_presence_status"],
                    "source_path": record["source_path"],
                }
            )
    resolved_out = resolve_repo_path(out_dir)
    write_json(resolved_out / SOURCE_INVENTORY_JSON, {"records": records})
    write_jsonl(resolved_out / WARNINGS_JSONL, warnings)
    return records, warnings


def _source_definitions_from_manifest(manifest_path: Path) -> tuple[ResultSourceDefinition, ...]:
    path = resolve_repo_path(manifest_path)
    if not path.is_file():
        raise FileNotFoundError(f"Stage 4P manifest missing: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Stage 4P manifest must be a mapping: {manifest_path}")
    _validate_policy_flags(payload)
    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        return DEFAULT_SOURCES
    definitions: list[ResultSourceDefinition] = []
    for item in sources:
        if not isinstance(item, dict):
            raise ValueError("Stage 4P manifest source entries must be mappings")
        definitions.append(
            ResultSourceDefinition(
                source_id=str(item["source_id"]),
                source_stage_id=str(item.get("source_stage_id", "synthetic")),
                result_source_kind=str(item["result_source_kind"]),
                source_path=str(item["source_path"]),
                required=bool(item.get("required", False)),
                optional_generated=bool(item.get("optional_generated", False)),
                raw_required=bool(item.get("raw_required", False)),
                method_family=str(item.get("method_family", "unknown")),
                source_record_type=str(item.get("source_record_type", "summary")),
            )
        )
    return tuple(definitions)


def _validate_policy_flags(payload: dict[str, Any]) -> None:
    for key, expected in (
        ("cpu_only", True),
        ("cuda_used", False),
        ("cuda_required", False),
        ("no_solve_claim", True),
        ("canonical_corpus_active", False),
        ("page_boundaries_final", False),
        ("generated_outputs_committed", False),
        ("raw_data_processed", False),
        ("new_experiment_executed", False),
        ("new_scorer_added", False),
    ):
        if payload.get(key) is not expected:
            raise ValueError(f"{key} must be {str(expected).lower()}")


def _inventory_record(definition: ResultSourceDefinition) -> dict[str, Any]:
    if definition.raw_required:
        status = "skipped_raw_required"
        record_count = 0
    else:
        path = repo_root() / definition.source_path
        exists = path.is_file()
        if exists and definition.optional_generated:
            status = "local_generated_present"
        elif exists:
            status = "committed_summary_present"
        elif definition.optional_generated:
            status = "optional_generated_missing"
        else:
            status = "skipped_schema_unknown"
        record_count = _count_records(path) if exists else 0
    warnings = []
    if status == "optional_generated_missing":
        warnings.append("Optional ignored generated output is absent; committed summaries remain source of truth.")
    if status == "skipped_raw_required":
        warnings.append("Raw-required source intentionally skipped by Stage 4P.")
    if status == "skipped_schema_unknown" and definition.required:
        warnings.append("Required committed summary is missing or not readable.")
    return {
        "record_type": "result_source_inventory_record",
        "source_id": definition.source_id,
        "source_stage_id": definition.source_stage_id,
        "result_source_kind": definition.result_source_kind,
        "source_path": definition.source_path,
        "source_presence_status": status,
        "record_count_hint": record_count,
        "required": definition.required,
        "optional_generated": definition.optional_generated,
        "method_family": definition.method_family,
        "source_record_type": definition.source_record_type,
        "raw_data_processed": False,
        "generated_outputs_committed": False,
        "no_solve_claim": True,
        "solve_claim": False,
        "cuda_used": False,
        "warnings": warnings,
    }


def _count_records(path: Path) -> int:
    if not path.is_file():
        return 0
    if path.suffix == ".jsonl":
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    if path.suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
    else:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return len(payload["records"])
    return 1
