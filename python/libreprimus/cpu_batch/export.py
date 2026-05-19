"""Export CPU batch records and summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.cpu_batch.batch_runner import run_manifest
from libreprimus.cpu_batch.models import DEFAULT_OUTPUT_DIR, DEFAULT_SUMMARY_PATH
from libreprimus.cpu_batch.parity_contract import parity_contract_record
from libreprimus.cpu_batch.transform_adapter import adapter_status
from libreprimus.history.source_records import resolve_repo_path
from libreprimus.transforms.registry import load_registry


def run_cpu_batch(*, manifest: Path, out_dir: Path, allow_warnings: bool = False) -> dict[str, Any]:
    """Run a CPU batch manifest and write generated result files."""

    batch = run_manifest(manifest)
    resolved_out = resolve_repo_path(out_dir)
    resolved_out.mkdir(parents=True, exist_ok=True)
    _write_jsonl(resolved_out / "result_records.jsonl", batch.records)
    _write_json(resolved_out / "summary.json", batch.summary)
    _write_jsonl(resolved_out / "warnings.jsonl", batch.warnings)
    if batch.warnings and not allow_warnings:
        raise ValueError("CPU batch completed with warnings; rerun with --allow-warnings to accept them.")
    if resolved_out == resolve_repo_path(DEFAULT_OUTPUT_DIR):
        write_committed_summary(batch.summary, DEFAULT_SUMMARY_PATH)
    return batch.summary


def write_adapter_coverage(*, registry_path: Path, out_dir: Path) -> dict[str, Any]:
    """Write adapter coverage for the CPU reference transform registry."""

    registry = load_registry(registry_path)
    records = [
        {
            "transform_id": definition.transform_id,
            "canonical_transform_id": definition.alias_of or definition.transform_id,
            "method_family": definition.method_family,
            "adapter_status": adapter_status(definition.transform_id),
            "supports_cpu_reference": definition.supports_cpu_reference,
            "supports_gpu": definition.supports_gpu,
        }
        for definition in sorted(registry.transforms, key=lambda item: item.transform_id)
    ]
    supported = sum(1 for record in records if record["adapter_status"] == "supported")
    missing = len(records) - supported
    payload = {
        "record_type": "cpu_batch_adapter_coverage",
        "registry_id": registry.registry_id,
        "registry_sha256": registry.sha256,
        "transform_count": len(records),
        "supported_adapter_count": supported,
        "missing_adapter_count": missing,
        "records": records,
        "cpu_only": True,
        "cuda_used": False,
        "no_solve_claim": True,
    }
    resolved_out = resolve_repo_path(out_dir)
    resolved_out.mkdir(parents=True, exist_ok=True)
    _write_json(resolved_out / "adapter_coverage.json", payload)
    summary_path = resolved_out / "summary.json"
    if summary_path.is_file():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if isinstance(summary, dict):
            summary["adapter_coverage"] = {
                "supported_adapter_count": supported,
                "missing_adapter_count": missing,
                "transform_count": len(records),
            }
            _write_json(summary_path, summary)
            if resolved_out == resolve_repo_path(DEFAULT_OUTPUT_DIR):
                write_committed_summary(summary, DEFAULT_SUMMARY_PATH)
    return payload


def write_committed_summary(summary: dict[str, Any], path: Path = DEFAULT_SUMMARY_PATH) -> None:
    """Write the committed Stage 4H aggregate summary."""

    payload = {
        "record_type": "stage4h_cpu_batch_api_summary",
        "schema": "schemas/experiments/cpu-batch-run-summary-v0.schema.json",
        "stage_id": "stage-4h",
        "status": "complete",
        "cpu_batch_summary": summary,
        "parity_contract": parity_contract_record(),
        "solve_claim": False,
        "cuda_used": False,
        "raw_outputs_committed": False,
        "generated_outputs_committed": False,
        "notes": [
            "Stage 4H establishes CPU batch semantics as the future CUDA parity contract.",
            "Generated result records remain under ignored experiments/results/cpu-batch/stage4h/.",
        ],
    }
    resolved = resolve_repo_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")
