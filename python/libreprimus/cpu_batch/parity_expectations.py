"""Parity expectation records for future CUDA checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.input_streams import stable_json_sha256
from libreprimus.history.source_records import resolve_repo_path
from libreprimus.scoring_consolidation.cpu_batch_integration import score_summary_from_cpu_batch_result

PARITY_CONTRACT_VERSION = "stage4o-cpu-cuda-parity-v0"


def build_parity_expectations(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return deterministic parity expectation records for CPU batch outputs."""

    expectations: list[dict[str, Any]] = []
    for record in sorted(records, key=lambda item: (str(item.get("input_stream_id")), str(item.get("candidate_id")))):
        status = _parity_status(record)
        score_view = score_summary_from_cpu_batch_result(record)
        expectations.append(
            {
                "record_type": "cpu_batch_parity_expectation",
                "parity_contract_version": PARITY_CONTRACT_VERSION,
                "input_stream_id": str(record["input_stream_id"]),
                "candidate_id": str(record["candidate_id"]),
                "transform_family": str(record["transform_family"]),
                "transform_id": str(record["transform_id"]),
                "canonical_transform_id": record.get("canonical_transform_id"),
                "parity_status": status,
                "output_token_hash": record.get("output_token_hash") if status == "passed" else None,
                "output_text_hash": record.get("output_text_hash") if status == "passed" else None,
                "score_summary_shape_hash": stable_json_sha256(sorted(score_view.keys())),
                "transform_parameters_hash": stable_json_sha256(record.get("transform_parameters", {})),
                "separator_behavior": "profile separators preserved as deterministic spaces or clauses in normalized output",
                "line_reset_behavior": "no implicit page-boundary or line-reset semantics in Stage 4O batch records",
                "unknown_token_handling": "unknown_symbol tokens are preserved as raw text by local adapters or handled by solved-fixture registry transforms",
                "cpu_only": True,
                "cuda_used": False,
                "cuda_required": False,
                "no_solve_claim": True,
                "canonical_corpus_active": False,
                "page_boundaries_final": False,
                "generated_outputs_committed": False,
            }
        )
    return expectations


def write_parity_expectations(*, records: list[dict[str, Any]], out_dir: Path) -> list[dict[str, Any]]:
    """Write parity expectation JSONL records."""

    expectations = build_parity_expectations(records)
    resolved_out = resolve_repo_path(out_dir)
    resolved_out.mkdir(parents=True, exist_ok=True)
    (resolved_out / "parity_expectations.jsonl").write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in expectations),
        encoding="utf-8",
    )
    return expectations


def _parity_status(record: dict[str, Any]) -> str:
    if record.get("execution_status") == "adapter_missing":
        return "skipped_adapter_missing"
    if record.get("execution_status") != "executed":
        return "failed"
    if not record.get("output_token_hash") or not record.get("output_text_hash"):
        return "failed"
    return "passed"
