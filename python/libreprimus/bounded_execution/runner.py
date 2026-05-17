"""Run the Stage 3A bounded Caesar plus affine candidate enumeration."""

from __future__ import annotations

import hashlib
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from libreprimus.bounded_execution.caesar_affine import (
    affine_outputs,
    caesar_outputs,
    labels_by_index,
    normalize_indices,
    reverse_affine_outputs,
    reverse_caesar_outputs,
)
from libreprimus.bounded_execution.candidate_writer import write_candidate_outputs
from libreprimus.bounded_execution.input_slice_loader import load_input_slice
from libreprimus.bounded_execution.models import BoundedCandidateRecord, BoundedRunSummary
from libreprimus.bounded_experiments.policy_checker import check_item
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.paths import repo_root
from libreprimus.scoring.minimal_triage import score_text
from libreprimus.scoring.validation import validate_minimal_triage_score

CAESAR_COUNT = 29
AFFINE_COUNT = 812
TOTAL_COUNT = 841


def git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def run_caesar_affine_from_paths(
    policy_path: Path,
    queue_path: Path,
    *,
    item_id: str,
    out_dir: Path,
    top_k: int = 25,
    allow_warnings: bool = False,
    direction: str = "auto",
) -> BoundedRunSummary:
    policy = load_operator_policy(policy_path)
    queue = load_bounded_queue(queue_path)
    item = _find_item(queue.items, item_id)
    check = check_item(policy, item)
    if check.blocking_reasons:
        raise ValueError(f"Policy blocked {item_id}: {check.blocking_reasons}")
    if check.warnings and not allow_warnings:
        raise ValueError(f"Policy warnings require --allow-warnings: {check.warnings}")
    resolved_direction = _resolve_direction(item, direction)
    return run_caesar_affine_item(item, out_dir=out_dir, top_k=top_k, policy_id=policy.policy_id, direction=resolved_direction)


def run_caesar_affine_item(
    item: dict[str, Any],
    *,
    out_dir: Path,
    top_k: int = 25,
    policy_id: str = "operator-policy-v0",
    direction: str = "forward",
) -> BoundedRunSummary:
    if direction not in {"forward", "reverse"}:
        raise ValueError("direction must be 'forward' or 'reverse'.")
    start = perf_counter()
    input_slice = load_input_slice(item)
    labels = labels_by_index(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")
    stage_label = "stage3b" if direction == "reverse" else "stage3a"
    run_id = f"{stage_label}-{item['item_id']}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    records = _build_records(run_id, str(item["item_id"]), input_slice, labels, direction=direction)
    if len(records) != TOTAL_COUNT:
        raise ValueError(f"Expected {TOTAL_COUNT} candidates, got {len(records)}.")
    ranked = sorted(
        records,
        key=lambda record: (
            float(record.score_summary.get("length_normalized_score", record.score_summary["total_score"])),
            float(record.score_summary["total_score"]),
            int(record.ranking_features["common_word_hit_count"]),
            -record.candidate_index,
        ),
        reverse=True,
    )
    top_records = ranked[:top_k]
    warnings = list(input_slice.warnings)
    top = top_records[0]
    result_store_preview = {
        "record_type": "bounded_result_store_preview",
        "run_id": run_id,
        "policy_id": policy_id,
        "queue_item_id": item["item_id"],
        "candidate_count": len(records),
        "top_candidate_index": top.candidate_index,
        "top_score": top.score_summary["total_score"],
        "top_length_normalized_score": top.score_summary.get("length_normalized_score"),
        "top_confidence_label": top.score_summary.get("confidence_label"),
        "direction": direction,
        "import_enabled": False,
        "generated_outputs_ignored": True,
    }
    summary = BoundedRunSummary(
        record_type="bounded_experiment_run_summary",
        run_id=run_id,
        queue_item_id=str(item["item_id"]),
        input_slice_id=input_slice.slice_id,
        input_length=input_slice.input_length,
        candidate_count=len(records),
        caesar_candidate_count=CAESAR_COUNT,
        affine_candidate_count=AFFINE_COUNT,
        top_k_count=len(top_records),
        top_candidate={
            "candidate_index": top.candidate_index,
            "transform_family": top.transform_family,
            "transform_parameters": top.transform_parameters,
            "total_score": top.score_summary["total_score"],
            "length_normalized_score": top.score_summary.get("length_normalized_score"),
            "confidence_label": top.score_summary.get("confidence_label"),
            "output_sha256": top.output_sha256,
        },
        output_paths={},
        generated_outputs_ignored=True,
        result_store_preview=result_store_preview,
        search_performed=True,
        scoring_used=True,
        cuda_used=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        solve_claim=False,
        trusted_as_canonical=False,
        warnings=warnings + [f"elapsed_ms={round((perf_counter() - start) * 1000, 3)}"],
    )
    paths = write_candidate_outputs(out_dir, records, top_records, summary, warnings)
    summary = _with_output_paths(summary, paths)
    write_candidate_outputs(out_dir, records, top_records, summary, warnings)
    return summary


def _build_records(
    run_id: str,
    queue_item_id: str,
    input_slice,
    labels: dict[int, str],
    *,
    direction: str,
) -> list[BoundedCandidateRecord]:
    records: list[BoundedCandidateRecord] = []
    candidate_index = 0
    caesar_generator = reverse_caesar_outputs if direction == "reverse" else caesar_outputs
    affine_generator = reverse_affine_outputs if direction == "reverse" else affine_outputs
    caesar_family = "caesar_shift_mod29_reverse" if direction == "reverse" else "caesar_shift_mod29"
    affine_family = "affine_mod29_reverse" if direction == "reverse" else "affine_mod29"
    for params, output_indices in caesar_generator(input_slice.index29_values):
        records.append(
            _record(
                run_id,
                queue_item_id,
                caesar_family,
                caesar_family,
                params,
                candidate_index,
                input_slice.slice_id,
                output_indices,
                labels,
                input_slice.warnings,
            )
        )
        candidate_index += 1
    for params, output_indices in affine_generator(input_slice.index29_values):
        records.append(
            _record(
                run_id,
                queue_item_id,
                affine_family,
                affine_family,
                params,
                candidate_index,
                input_slice.slice_id,
                output_indices,
                labels,
                input_slice.warnings,
            )
        )
        candidate_index += 1
    return records


def _record(
    run_id: str,
    queue_item_id: str,
    transform_family: str,
    transform_id: str,
    params: dict[str, int],
    candidate_index: int,
    input_slice_id: str,
    output_indices: list[int],
    labels: dict[int, str],
    warnings: list[str],
) -> BoundedCandidateRecord:
    text = normalize_indices(output_indices, labels)
    score = validate_minimal_triage_score(score_text(text))
    return BoundedCandidateRecord(
        record_type="bounded_candidate_record",
        run_id=run_id,
        queue_item_id=queue_item_id,
        transform_family=transform_family,
        transform_id=transform_id,
        transform_parameters=params,
        candidate_index=candidate_index,
        input_slice_id=input_slice_id,
        output_normalized_text=text,
        output_preview=text[:160],
        output_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        score_summary=score,
        ranking_features={
            "total_score": score["total_score"],
            "length_normalized_score": score.get("length_normalized_score", score["total_score"]),
            "confidence_label": score.get("confidence_label", "noisy"),
            "common_word_hit_count": score["common_word_hit_count"],
            "latin_letter_count": score["latin_letter_count"],
            "entropy": score["entropy"],
        },
        search_performed=True,
        scoring_used=True,
        cuda_used=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        solve_claim=False,
        trusted_as_canonical=False,
        warnings=warnings,
    )


def _find_item(items: list[dict[str, Any]], item_id: str) -> dict[str, Any]:
    for item in items:
        if item.get("item_id") == item_id:
            return item
    raise ValueError(f"Queue item not found: {item_id}")


def _resolve_direction(item: dict[str, Any], direction: str) -> str:
    if direction != "auto":
        return direction
    transform_plan = dict(item.get("transform_plan", {}))
    return str(transform_plan.get("direction", transform_plan.get("convention", "forward")))


def _with_output_paths(summary: BoundedRunSummary, paths: dict[str, Path]) -> BoundedRunSummary:
    return BoundedRunSummary(
        record_type=summary.record_type,
        run_id=summary.run_id,
        queue_item_id=summary.queue_item_id,
        input_slice_id=summary.input_slice_id,
        input_length=summary.input_length,
        candidate_count=summary.candidate_count,
        caesar_candidate_count=summary.caesar_candidate_count,
        affine_candidate_count=summary.affine_candidate_count,
        top_k_count=summary.top_k_count,
        top_candidate=summary.top_candidate,
        output_paths={key: str(path) for key, path in paths.items()},
        generated_outputs_ignored=summary.generated_outputs_ignored,
        result_store_preview=summary.result_store_preview,
        search_performed=summary.search_performed,
        scoring_used=summary.scoring_used,
        cuda_used=summary.cuda_used,
        canonical_corpus_active=summary.canonical_corpus_active,
        page_boundaries_final=summary.page_boundaries_final,
        solve_claim=summary.solve_claim,
        trusted_as_canonical=summary.trusted_as_canonical,
        warnings=summary.warnings,
    )
