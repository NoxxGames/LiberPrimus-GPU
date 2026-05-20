"""Run deterministic CPU transform batches."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.input_streams import stream_index
from libreprimus.cpu_batch.manifest_loader import load_manifest
from libreprimus.cpu_batch.models import BatchRun, CpuBatchManifest
from libreprimus.cpu_batch.scoring_adapter import score_output
from libreprimus.cpu_batch.transform_adapter import apply_transform
from libreprimus.transforms.registry import load_registry


def run_manifest(path: Path) -> BatchRun:
    """Run one CPU batch manifest and return result records plus summary."""

    manifest = load_manifest(path)
    registry = load_registry()
    streams = stream_index(manifest.input_streams)
    records: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    for candidate in sorted(manifest.transform_candidates, key=lambda item: str(item["candidate_id"])):
        stream_id = str(candidate["input_stream_id"])
        if stream_id not in streams:
            raise ValueError(f"{candidate['candidate_id']}: missing input stream {stream_id}")
        stream = streams[stream_id]
        try:
            adapter = apply_transform(registry=registry, stream=stream, candidate=candidate)
            score_summary = score_output(adapter.output_text, enabled=manifest.scoring_enabled)
            scoring_available = score_summary.get("score_status") == "scored"
            record_warnings = list(adapter.warnings)
        except Exception as error:  # noqa: BLE001 - batch records deterministic execution errors.
            adapter = None
            score_summary = {"score_status": "scoring_not_available", "reason": "transform_error"}
            scoring_available = False
            record_warnings = [str(error)]
        record = _result_record(
            manifest=manifest,
            candidate=candidate,
            stream=stream,
            adapter=adapter,
            score_summary=score_summary,
            record_warnings=record_warnings,
        )
        record["scoring_available"] = scoring_available
        records.append(record)
        for warning in record_warnings:
            warnings.append({"candidate_id": candidate["candidate_id"], "warning": warning})
    summary = _summary(manifest, streams, records, warnings)
    return BatchRun(records=records, summary=summary, warnings=warnings)


def _result_record(
    *,
    manifest: CpuBatchManifest,
    candidate: dict[str, Any],
    stream: dict[str, Any],
    adapter: Any,
    score_summary: dict[str, Any],
    record_warnings: list[str],
) -> dict[str, Any]:
    if adapter is None:
        execution_status = "error"
        canonical_transform_id = None
        output_text = None
        output_text_hash = None
        output_token_hash = "0" * 64
        transform_parameters = dict(candidate.get("transform_parameters", {}))
        adapter_status = "error"
    else:
        execution_status = adapter.status
        canonical_transform_id = adapter.canonical_transform_id
        output_text = adapter.output_text
        output_text_hash = adapter.output_text_hash
        output_token_hash = adapter.output_token_hash
        transform_parameters = dict(adapter.transform_parameters)
        adapter_status = adapter.status
    return {
        "record_type": "cpu_batch_result_record",
        "run_id": _run_id(manifest),
        "manifest_id": manifest.manifest_id,
        "candidate_id": str(candidate["candidate_id"]),
        "input_stream_id": str(candidate["input_stream_id"]),
        "transform_family": str(candidate["transform_family"]),
        "transform_id": str(candidate["transform_id"]),
        "canonical_transform_id": canonical_transform_id,
        "transform_parameters": transform_parameters,
        "execution_status": execution_status,
        "adapter_status": adapter_status,
        "token_count": int(stream["token_count"]),
        "transformable_token_count": int(stream["transformable_token_count"]),
        "output_text": output_text,
        "output_text_hash": output_text_hash,
        "output_token_hash": output_token_hash,
        "score_summary": score_summary,
        "warnings": record_warnings,
        "cpu_only": True,
        "cuda_used": False,
        "cuda_required": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
    }


def _summary(
    manifest: CpuBatchManifest,
    streams: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
) -> dict[str, Any]:
    statuses = Counter(str(record["execution_status"]) for record in records)
    scored = sum(1 for record in records if record.get("scoring_available") is True)
    cleaned_records = [{key: value for key, value in record.items() if key != "scoring_available"} for record in records]
    records[:] = cleaned_records
    return {
        "record_type": "cpu_batch_run_summary",
        "run_id": _run_id(manifest),
        "manifest_id": manifest.manifest_id,
        "input_stream_count": len(streams),
        "candidate_count": len(manifest.transform_candidates),
        "executed_candidate_count": statuses["executed"],
        "adapter_missing_count": statuses["adapter_missing"],
        "result_record_count": len(records),
        "scoring_available_count": scored,
        "scoring_unavailable_count": len(records) - scored,
        "adapter_coverage": {},
        "warnings": [str(item["warning"]) for item in warnings],
        "cpu_only": True,
        "cuda_used": False,
        "cuda_required": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
    }


def _run_id(manifest: CpuBatchManifest) -> str:
    if manifest.manifest_id.startswith("stage4o-"):
        return f"stage4o-{manifest.manifest_id}-cpu-reference-v0"
    return f"stage4h-{manifest.manifest_id}-cpu-reference-v0"
