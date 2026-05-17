"""Bounded explicit-key Vigenere execution for Stage 3D."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from libreprimus.bounded_execution.caesar_affine import labels_by_index, normalize_indices
from libreprimus.bounded_execution.candidate_writer import write_candidate_outputs, write_jsonl
from libreprimus.bounded_execution.input_slice_loader import load_input_slice
from libreprimus.bounded_execution.models import BoundedCandidateRecord, BoundedRunSummary
from libreprimus.bounded_experiments.policy_checker import check_item
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import load_gematria_profile
from libreprimus.scoring.calibration import classify_score
from libreprimus.scoring.crib_checks import crib_check
from libreprimus.scoring.minimal_triage import score_text
from libreprimus.scoring.validation import validate_crib_check_result, validate_minimal_triage_score
from libreprimus.solved_fixtures.models import to_jsonable
from libreprimus.solved_fixtures.vigenere import key_text_to_indices

EXPECTED_STAGE3D_KEYS = ["LIBER", "PRIMUS", "DIVINITY", "CICADA"]
DEFAULT_CALIBRATION_SUMMARY = Path("experiments/results/scoring-calibration/stage3c/calibration_summary.json")
MODULUS = 29


def git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def run_vigenere_key_list_from_paths(
    policy_path: Path,
    queue_path: Path,
    *,
    item_id: str,
    out_dir: Path,
    top_k: int = 4,
    allow_warnings: bool = False,
    calibration_summary_path: Path = DEFAULT_CALIBRATION_SUMMARY,
) -> BoundedRunSummary:
    policy = load_operator_policy(policy_path)
    queue = load_bounded_queue(queue_path)
    item = _find_item(queue.items, item_id)
    check = check_item(policy, item)
    if check.blocking_reasons:
        raise ValueError(f"Policy blocked {item_id}: {check.blocking_reasons}")
    if check.warnings and not allow_warnings:
        raise ValueError(f"Policy warnings require --allow-warnings: {check.warnings}")
    return run_vigenere_key_list_item(
        item,
        out_dir=out_dir,
        top_k=top_k,
        policy_id=policy.policy_id,
        calibration_summary_path=calibration_summary_path,
    )


def run_vigenere_key_list_item(
    item: dict[str, Any],
    *,
    out_dir: Path,
    top_k: int = 4,
    policy_id: str = "operator-policy-v0",
    calibration_summary_path: Path = DEFAULT_CALIBRATION_SUMMARY,
) -> BoundedRunSummary:
    start = perf_counter()
    keys = load_declared_key_list(item)
    input_slice = load_input_slice(item)
    profile = load_gematria_profile(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")
    labels = labels_by_index(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")
    key_indices_by_text = {key: key_text_to_indices(key, profile) for key in keys}
    calibration = load_calibration_summary(calibration_summary_path)
    thresholds = dict(calibration.get("thresholds", {}))
    warnings = list(input_slice.warnings)
    if not calibration:
        warnings.append("stage3c_calibration_summary_missing; calibrated label falls back to current thresholds.")

    run_id = f"stage3d-{item['item_id']}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    records = [
        _record(
            run_id,
            str(item["item_id"]),
            key_text,
            key_indices_by_text[key_text],
            candidate_index,
            input_slice.slice_id,
            input_slice.index29_values,
            labels,
            thresholds,
            warnings,
        )
        for candidate_index, key_text in enumerate(keys)
    ]
    if len(records) != int(item["candidate_count_upper_bound"]):
        raise ValueError(f"Expected {item['candidate_count_upper_bound']} candidates, got {len(records)}.")

    ranked = sorted(
        records,
        key=lambda record: (
            float(record.score_summary.get("length_normalized_score", record.score_summary["total_score"])),
            float(record.score_summary["total_score"]),
            int(record.crib_hit_count or 0),
            -record.candidate_index,
        ),
        reverse=True,
    )
    top_records = ranked[:top_k]
    top = top_records[0]
    elapsed_ms = round((perf_counter() - start) * 1000, 3)
    result_store_preview = {
        "record_type": "bounded_result_store_preview",
        "run_id": run_id,
        "policy_id": policy_id,
        "queue_item_id": item["item_id"],
        "candidate_count": len(records),
        "top_candidate_index": top.candidate_index,
        "top_key_text": top.key_text,
        "top_score": top.score_summary["total_score"],
        "top_length_normalized_score": top.score_summary.get("length_normalized_score"),
        "top_calibrated_confidence_label": top.calibrated_confidence_label,
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
        caesar_candidate_count=0,
        affine_candidate_count=0,
        top_k_count=len(top_records),
        top_candidate={
            "candidate_index": top.candidate_index,
            "transform_family": top.transform_family,
            "transform_parameters": top.transform_parameters,
            "key_text": top.key_text,
            "key_indices": top.key_indices,
            "total_score": top.score_summary["total_score"],
            "length_normalized_score": top.score_summary.get("length_normalized_score"),
            "confidence_label": top.score_summary.get("confidence_label"),
            "calibrated_confidence_label": top.calibrated_confidence_label,
            "crib_hits": top.crib_hits,
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
        warnings=warnings + [f"elapsed_ms={elapsed_ms}"],
        vigenere_candidate_count=len(records),
    )
    paths = write_candidate_outputs(out_dir, records, top_records, summary, warnings)
    score_details_path = write_jsonl(paths["summary"].parent / "calibrated_scores.jsonl", _score_details(records, calibration))
    paths["calibrated_scores"] = score_details_path
    summary = _with_output_paths(summary, paths)
    write_candidate_outputs(out_dir, records, top_records, summary, warnings)
    write_jsonl(score_details_path, _score_details(records, calibration))
    return summary


def load_declared_key_list(item: dict[str, Any]) -> list[str]:
    keys = _extract_keys(item)
    if not keys:
        raise ValueError("Vigenere key-list item must declare transform_plan.families[].parameters.keys.")
    normalized = [str(key).strip().upper() for key in keys]
    if normalized != EXPECTED_STAGE3D_KEYS:
        raise ValueError(f"Stage 3D key list must stay explicit and unexpanded: {EXPECTED_STAGE3D_KEYS}.")
    upper_bound = int(item.get("candidate_count_upper_bound", -1))
    if len(normalized) != upper_bound:
        raise ValueError(f"Key count {len(normalized)} must equal candidate_count_upper_bound {upper_bound}.")
    for family in dict(item.get("transform_plan", {})).get("families", []):
        if not isinstance(family, dict):
            continue
        params = dict(family.get("parameters", {}))
        if params.get("key_search_enabled") is not False:
            raise ValueError("Stage 3D Vigenere key-list items must set key_search_enabled=false.")
        family_count = family.get("candidate_count")
        if family_count is not None and int(family_count) != len(normalized):
            raise ValueError(f"Vigenere family candidate_count {family_count} does not match key count {len(normalized)}.")
    return normalized


def load_calibration_summary(path: Path = DEFAULT_CALIBRATION_SUMMARY) -> dict[str, Any]:
    resolved = path if path.is_absolute() else repo_root() / path
    if not resolved.is_file():
        return {}
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Calibration summary must be a mapping: {resolved}")
    return payload


def _extract_keys(item: dict[str, Any]) -> list[Any]:
    families = dict(item.get("transform_plan", {})).get("families", [])
    for family in families:
        if not isinstance(family, dict):
            continue
        name = str(family.get("transform_family", ""))
        if name in {"vigenere_explicit_tiny_key_list", "vigenere_key_list_preview", "vigenere_explicit_key"}:
            params = dict(family.get("parameters", {}))
            keys = params.get("keys", [])
            if isinstance(keys, list):
                return keys
    return []


def _record(
    run_id: str,
    queue_item_id: str,
    key_text: str,
    key_indices: list[int],
    candidate_index: int,
    input_slice_id: str,
    input_indices: list[int],
    labels: dict[int, str],
    thresholds: dict[str, float],
    warnings: list[str],
) -> BoundedCandidateRecord:
    output_indices = vigenere_decrypt_indices(input_indices, key_indices)
    text = normalize_indices(output_indices, labels)
    score = validate_minimal_triage_score(score_text(text))
    crib_payload = validate_crib_check_result(crib_check(text, candidate_id=f"{queue_item_id}-{candidate_index}"))
    calibrated_label = classify_score(score, crib_payload, thresholds)
    calibration_position = {
        "length_normalized_score": score.get("length_normalized_score"),
        "calibrated_confidence_label": calibrated_label,
        "thresholds": thresholds,
        "score_source": "stage3c_calibrated_minimal_triage",
    }
    score["calibrated_confidence_label"] = calibrated_label
    score["crib_hit_count"] = crib_payload["crib_hit_count"]
    score["crib_hits"] = crib_payload["crib_hits"]
    score["no_solve_claim"] = True
    return BoundedCandidateRecord(
        record_type="bounded_candidate_record",
        run_id=run_id,
        queue_item_id=queue_item_id,
        transform_family="vigenere_explicit_key",
        transform_id="vigenere_explicit_key_decrypt_subtract",
        transform_parameters={"direction": "decrypt_subtract", "key_text": key_text},
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
            "calibrated_confidence_label": calibrated_label,
            "common_word_hit_count": score["common_word_hit_count"],
            "crib_hit_count": crib_payload["crib_hit_count"],
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
        key_text=key_text,
        key_indices=key_indices,
        calibrated_confidence_label=calibrated_label,
        crib_hits=crib_payload["crib_hits"],
        crib_hit_count=crib_payload["crib_hit_count"],
        calibration_position=calibration_position,
    )


def vigenere_decrypt_indices(input_indices: list[int], key_indices: list[int]) -> list[int]:
    if not key_indices:
        raise ValueError("Vigenere key indices must not be empty.")
    return [(value - key_indices[position % len(key_indices)]) % MODULUS for position, value in enumerate(input_indices)]


def _score_details(records: list[BoundedCandidateRecord], calibration: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "record_type": "stage3d_calibrated_score_detail",
            "run_id": record.run_id,
            "queue_item_id": record.queue_item_id,
            "candidate_index": record.candidate_index,
            "key_text": record.key_text,
            "score_summary": record.score_summary,
            "calibrated_confidence_label": record.calibrated_confidence_label,
            "crib_hits": record.crib_hits,
            "calibration_position": record.calibration_position,
            "calibration_id": calibration.get("calibration_id", "missing-stage3c-calibration-summary"),
            "solve_claim": False,
            "cuda_used": False,
        }
        for record in records
    ]


def _find_item(items: list[dict[str, Any]], item_id: str) -> dict[str, Any]:
    for item in items:
        if item.get("item_id") == item_id:
            return item
    raise ValueError(f"Queue item not found: {item_id}")


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
        vigenere_candidate_count=summary.vigenere_candidate_count,
    )


def candidate_payloads(records: list[BoundedCandidateRecord]) -> list[dict[str, Any]]:
    return [to_jsonable(record) for record in records]
