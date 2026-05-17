"""Scoring calibration against positive, null, negative, and candidate controls."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import hashlib
import json
import subprocess
from pathlib import Path
from statistics import mean
from typing import Any

from libreprimus.candidate_inspection.loader import load_jsonl, resolve_results_dir
from libreprimus.paths import repo_root
from libreprimus.scoring.crib_checks import crib_check, load_cribs
from libreprimus.scoring.minimal_triage import score_text
from libreprimus.scoring.null_controls import generate_negative_control_texts, generate_null_control_texts, load_null_control_policy
from libreprimus.scoring.positive_controls import load_positive_control_texts
from libreprimus.solved_fixtures.models import to_jsonable

DEFAULT_CALIBRATION_OUT_DIR = repo_root() / "experiments/results/scoring-calibration/stage3c"


@dataclass(frozen=True)
class CalibrationResult:
    positive_records: list[dict[str, Any]]
    null_records: list[dict[str, Any]]
    negative_records: list[dict[str, Any]]
    candidate_records: list[dict[str, Any]]
    summary: dict[str, Any]
    output_paths: dict[str, Path]


def run_scoring_calibration(
    *,
    stage3_results_dir: Path,
    stage3b_results_dir: Path,
    out_dir: Path = DEFAULT_CALIBRATION_OUT_DIR,
    allow_warnings: bool = False,
) -> CalibrationResult:
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    git_commit = _git_commit()
    output_dir = out_dir if out_dir.is_absolute() else repo_root() / out_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    cribs = load_cribs()
    warnings: list[str] = []

    stage3a_top = _load_first_jsonl(resolve_results_dir(stage3_results_dir) / "top_candidates.jsonl")
    seed_text = str(stage3a_top.get("output_normalized_text") or stage3a_top.get("output_preview") or "")
    policy = load_null_control_policy()
    positive_records = [
        build_control_record(control, "positive", generated_at=generated_at, cribs=cribs)
        for control in load_positive_control_texts()
    ]
    null_records = [
        build_control_record(control, "null", generated_at=generated_at, cribs=cribs)
        for control in generate_null_control_texts(policy=policy, seed_text=seed_text)
    ]
    negative_records = [
        build_control_record(control, "negative", generated_at=generated_at, cribs=cribs)
        for control in generate_negative_control_texts(length=int(policy.get("length", 87)))
    ]

    thresholds = derive_thresholds(positive_records, null_records, negative_records)
    _apply_calibrated_labels(positive_records, thresholds)
    _apply_calibrated_labels(null_records, thresholds)
    _apply_calibrated_labels(negative_records, thresholds)
    candidate_records = [
        build_control_record(candidate, "candidate", generated_at=generated_at, cribs=cribs, thresholds=thresholds)
        for candidate in load_stage3_candidate_controls(stage3_results_dir, stage3b_results_dir)
    ]
    if not candidate_records:
        warnings.append("No Stage 3 candidate records were available for calibration.")
    if warnings and not allow_warnings:
        raise ValueError("; ".join(warnings))

    stage3a_classification = _classification_for(candidate_records, "stage3a-original-top")
    stage3b_classification = _classification_for(candidate_records, "stage3b-reverse-top")
    recommended_next_step = recommend_next_step(stage3a_classification, stage3b_classification)
    summary = {
        "record_type": "scoring_calibration_summary",
        "calibration_id": f"stage3c-scoring-calibration-{git_commit[:12]}",
        "generated_at_utc": generated_at,
        "git_commit": git_commit,
        "positive_control_count": len(positive_records),
        "null_control_count": len(null_records),
        "negative_control_count": len(negative_records),
        "candidate_count": len(candidate_records),
        "positive_score_range": score_range(positive_records),
        "null_score_range": score_range(null_records),
        "negative_score_range": score_range(negative_records),
        "candidate_score_range": score_range(candidate_records),
        "thresholds": thresholds,
        "stage3a_top_classification": stage3a_classification,
        "stage3b_top_classification": stage3b_classification,
        "recommended_next_step": recommended_next_step,
        "solve_claim": False,
        "cuda_used": False,
        "warnings": warnings,
        "notes": [
            "Calibration labels are triage metadata only.",
            "No candidate is a solve claim.",
        ],
    }
    output_paths = write_calibration_outputs(
        output_dir,
        positive_records=positive_records,
        null_records=null_records,
        negative_records=negative_records,
        candidate_records=candidate_records,
        summary=summary,
        warnings=warnings,
    )
    summary["output_paths"] = {key: str(path) for key, path in output_paths.items()}
    _write_json(output_paths["summary"], summary)
    return CalibrationResult(
        positive_records=positive_records,
        null_records=null_records,
        negative_records=negative_records,
        candidate_records=candidate_records,
        summary=summary,
        output_paths=output_paths,
    )


def build_control_record(
    control: dict[str, Any],
    control_kind: str,
    *,
    generated_at: str,
    cribs: list[str],
    thresholds: dict[str, float] | None = None,
) -> dict[str, Any]:
    text = str(control.get("text") or control.get("output_normalized_text") or control.get("output_preview") or "")
    control_id = str(control.get("control_id") or control.get("candidate_id") or control.get("transform_id") or "control")
    source = str(control.get("source") or control.get("transform_family") or "unknown")
    score_payload = to_jsonable(score_text(text))
    crib_payload = crib_check(text, candidate_id=control_id, cribs=cribs)
    label = classify_score(score_payload, crib_payload, thresholds or {})
    return {
        "record_type": "scoring_control_record",
        "control_id": control_id,
        "control_kind": control_kind,
        "source": source,
        "text": text,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "length": len(text),
        "score_summary": score_payload,
        "crib_check": crib_payload,
        "confidence_label": label,
        "generated_at_utc": generated_at,
        "notes": _record_notes(control, label),
        "trusted_as_canonical": False,
        "solve_claim": False,
    }


def load_stage3_candidate_controls(stage3_results_dir: Path, stage3b_results_dir: Path) -> list[dict[str, Any]]:
    stage3a = resolve_results_dir(stage3_results_dir)
    stage3b = resolve_results_dir(stage3b_results_dir)
    controls: list[dict[str, Any]] = []
    controls.extend(_candidate_controls_from_jsonl(stage3a / "top_candidates.jsonl", "stage3a-original-top", limit=1))
    controls.extend(_candidate_controls_from_jsonl(stage3b / "reranked_top_candidates.jsonl", "stage3a-reranked-top", limit=1))
    controls.extend(
        _candidate_controls_from_jsonl(stage3b / "reverse_direction" / "top_candidates.jsonl", "stage3b-reverse-top", limit=1)
    )
    return controls


def derive_thresholds(
    positive_records: list[dict[str, Any]],
    null_records: list[dict[str, Any]],
    negative_records: list[dict[str, Any]],
) -> dict[str, float]:
    positive_scores = _scores(positive_records)
    null_scores = _scores(null_records)
    negative_scores = _scores(negative_records)
    positive_min = min(positive_scores) if positive_scores else 999.0
    null_p95 = percentile(null_scores, 0.95)
    null_p50 = percentile(null_scores, 0.50)
    negative_p95 = percentile(negative_scores, 0.95)
    plausible = max(null_p95 + 2.0, positive_min * 0.60)
    weak = max(null_p50, negative_p95 + 1.0)
    return {
        "positive_control_like_min": round(positive_min, 6),
        "null_p95": round(null_p95, 6),
        "negative_p95": round(negative_p95, 6),
        "plausible_lead_min": round(plausible, 6),
        "weak_lead_min": round(weak, 6),
        "garbage_max": round(min(null_p50, negative_p95), 6),
    }


def classify_score(
    score_payload: dict[str, Any],
    crib_payload: dict[str, Any],
    thresholds: dict[str, float],
) -> str:
    score = float(score_payload.get("length_normalized_score", score_payload.get("total_score", 0.0)))
    negatives = set(score_payload.get("negative_features", []))
    positive_count = len(score_payload.get("positive_features", []))
    crib_count = int(crib_payload.get("crib_hit_count", 0))
    has_no_separator = "no_separator_context" in negatives
    has_impossible = any(str(feature).startswith("impossible_bigrams") for feature in negatives)
    if score >= float(thresholds.get("positive_control_like_min", 999.0)) and positive_count >= 3 and not has_no_separator:
        return "positive_control_like"
    if has_no_separator or has_impossible:
        return "noisy" if score >= float(thresholds.get("garbage_max", 0.0)) else "garbage"
    if score >= float(thresholds.get("plausible_lead_min", 999.0)) and (positive_count >= 2 or crib_count):
        return "plausible_lead"
    if score >= float(thresholds.get("weak_lead_min", 999.0)) and positive_count:
        return "weak_lead"
    if score <= float(thresholds.get("garbage_max", -999.0)):
        return "garbage"
    return "inconclusive"


def score_range(records: list[dict[str, Any]]) -> dict[str, float | int]:
    scores = _scores(records)
    if not scores:
        return {"count": 0, "min": 0.0, "max": 0.0, "mean": 0.0}
    return {
        "count": len(scores),
        "min": round(min(scores), 6),
        "max": round(max(scores), 6),
        "mean": round(mean(scores), 6),
    }


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * fraction)))
    return ordered[index]


def recommend_next_step(stage3a_label: str, stage3b_label: str) -> str:
    if stage3a_label in {"positive_control_like", "plausible_lead"} or stage3b_label in {"positive_control_like", "plausible_lead"}:
        return "Stage 3D - inspect calibrated plausible leads with null controls before adding new transforms."
    return "Stage 3D - run the conservative small Vigenere known-motif key-list preview with calibrated scoring."


def write_calibration_outputs(
    output_dir: Path,
    *,
    positive_records: list[dict[str, Any]],
    null_records: list[dict[str, Any]],
    negative_records: list[dict[str, Any]],
    candidate_records: list[dict[str, Any]],
    summary: dict[str, Any],
    warnings: list[str],
) -> dict[str, Path]:
    paths = {
        "positive_controls": output_dir / "positive_control_scores.jsonl",
        "null_controls": output_dir / "null_control_scores.jsonl",
        "negative_controls": output_dir / "negative_control_scores.jsonl",
        "candidates": output_dir / "stage3_candidates_calibrated.jsonl",
        "summary": output_dir / "calibration_summary.json",
    }
    _write_jsonl(paths["positive_controls"], positive_records)
    _write_jsonl(paths["null_controls"], null_records)
    _write_jsonl(paths["negative_controls"], negative_records)
    _write_jsonl(paths["candidates"], candidate_records)
    _write_json(paths["summary"], summary)
    if warnings:
        paths["warnings"] = output_dir / "warnings.jsonl"
        _write_jsonl(paths["warnings"], [{"record_type": "stage3c_calibration_warning", "warning": warning} for warning in warnings])
    return paths


def _apply_calibrated_labels(records: list[dict[str, Any]], thresholds: dict[str, float]) -> None:
    for record in records:
        record["confidence_label"] = classify_score(record["score_summary"], record["crib_check"], thresholds)


def _scores(records: list[dict[str, Any]]) -> list[float]:
    return [float(record.get("score_summary", {}).get("length_normalized_score", 0.0)) for record in records]


def _classification_for(records: list[dict[str, Any]], control_id: str) -> str:
    for record in records:
        if record.get("control_id") == control_id:
            return str(record.get("confidence_label", "inconclusive"))
    return "inconclusive"


def _candidate_controls_from_jsonl(path: Path, control_id: str, *, limit: int) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    controls: list[dict[str, Any]] = []
    for index, record in enumerate(load_jsonl(path)[:limit]):
        text = str(record.get("output_normalized_text") or record.get("output_preview") or "")
        controls.append(
            {
                "control_id": control_id if index == 0 else f"{control_id}-{index}",
                "source": f"{_display_path(path)}#{index}",
                "text": text,
                "transform_family": record.get("transform_family"),
                "transform_parameters": record.get("transform_parameters"),
            }
        )
    return controls


def _load_first_jsonl(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    rows = load_jsonl(path)
    return rows[0] if rows else {}


def _record_notes(control: dict[str, Any], label: str) -> list[str]:
    notes = ["Scoring calibration control; not solve evidence.", f"calibrated_label={label}"]
    transform = control.get("transform_parameters")
    if transform:
        notes.append(f"transform_parameters={json.dumps(transform, sort_keys=True)}")
    return notes


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(repo_root()))
    except ValueError:
        return str(path)


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")
    return path


def _git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root(),
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"
