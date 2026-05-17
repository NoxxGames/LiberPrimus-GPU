"""Stage 3H reset/advance ablation execution."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from libreprimus.bounded_execution.caesar_affine import labels_by_index
from libreprimus.bounded_execution.candidate_writer import write_candidate_outputs, write_jsonl
from libreprimus.bounded_execution.input_slice_loader import load_input_slice
from libreprimus.bounded_execution.models import BoundedCandidateRecord, BoundedRunSummary, InputSlice
from libreprimus.bounded_execution.negative_controls import generate_family_negative_controls
from libreprimus.bounded_execution.prime_stream_variants import (
    prime_gap_value,
    prime_minus_one_value,
    prime_mod29_value,
)
from libreprimus.bounded_execution.reset_advance import (
    ADVANCE_MODES,
    RESET_MODES,
    TransformToken,
    apply_stateful_transform,
    build_tokens,
    metadata_support,
    unsupported_reset_reason,
)
from libreprimus.bounded_execution.vigenere_key_list import DEFAULT_CALIBRATION_SUMMARY, load_calibration_summary
from libreprimus.bounded_experiments.policy_checker import check_item
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.method_backlog.counts import validate_candidate_count
from libreprimus.paths import repo_root
from libreprimus.profiles.gematria_profile import load_gematria_profile
from libreprimus.scoring.calibration import classify_score
from libreprimus.scoring.crib_checks import crib_check
from libreprimus.scoring.minimal_triage import score_text
from libreprimus.scoring.validation import validate_crib_check_result, validate_minimal_triage_score
from libreprimus.solved_fixtures.models import to_jsonable
from libreprimus.solved_fixtures.vigenere import key_text_to_indices

TARGET_ITEM_ID = "stage3h_reset_advance_ablation_v1"
EXPECTED_STAGE3H_BASE_TRANSFORMS = [
    "vigenere:DIVINITY",
    "vigenere:FIRFUMFERENFE",
    "vigenere:PATIENCEISAVIRTUE",
    "vigenere:THEINSTAREMERGENCE",
    "prime_minus_one:offset=0",
    "prime_minus_one:offset=1",
    "prime_mod29:offset=0",
    "prime_gap:offset=0",
]
SUPPORTED_RESET_MODES = ["none", "word", "clause", "line"]
SUPPORTED_ADVANCE_MODES = ["runes_only", "token_break_preserving"]
MODULUS = 29


@dataclass(frozen=True)
class BaseTransform:
    transform_id: str
    family: str
    key_text: str | None = None
    key_indices: list[int] | None = None
    offset: int | None = None


@dataclass(frozen=True)
class ResetAdvanceAblation:
    item_id: str
    base_transforms: list[str]
    reset_modes: list[str]
    advance_modes: list[str]
    expected_candidate_count: int


@dataclass(frozen=True)
class AblationInput:
    input_slice: InputSlice
    token_records: list[dict[str, Any]]
    tokens: list[TransformToken]
    metadata_support_status: dict[str, bool]
    warnings: list[str]


@dataclass(frozen=True)
class DeferredCandidate:
    candidate_index: int
    base_transform_id: str
    reset_mode: str
    advance_mode: str
    reason: str


def run_reset_advance_ablation_from_paths(
    policy_path: Path,
    queue_path: Path,
    *,
    item_id: str,
    out_dir: Path,
    top_k: int = 25,
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
    return run_reset_advance_ablation_item(
        item,
        out_dir=out_dir,
        top_k=top_k,
        policy_id=policy.policy_id,
        calibration_summary_path=calibration_summary_path,
    )


def run_reset_advance_ablation_item(
    item: dict[str, Any],
    *,
    out_dir: Path,
    top_k: int = 25,
    policy_id: str = "operator-policy-v0",
    calibration_summary_path: Path = DEFAULT_CALIBRATION_SUMMARY,
) -> BoundedRunSummary:
    start = perf_counter()
    ablation = load_declared_reset_advance_ablation(item)
    input_data = load_ablation_input(item)
    base_transforms = _base_transforms(ablation.base_transforms)
    labels = labels_by_index(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")
    calibration = load_calibration_summary(calibration_summary_path)
    thresholds = dict(calibration.get("thresholds", {}))
    warnings = list(input_data.warnings)
    if not calibration:
        warnings.append("stage3c_calibration_summary_missing; calibrated label falls back to current thresholds.")

    run_id = f"stage3h-{ablation.item_id}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    records: list[BoundedCandidateRecord] = []
    deferred: list[DeferredCandidate] = []
    candidate_index = 0
    for base_transform in base_transforms:
        for reset_mode in ablation.reset_modes:
            for advance_mode in ablation.advance_modes:
                reason = unsupported_reset_reason(input_data.tokens, reset_mode)
                if reason is not None:
                    deferred.append(
                        DeferredCandidate(
                            candidate_index=candidate_index,
                            base_transform_id=base_transform.transform_id,
                            reset_mode=reset_mode,
                            advance_mode=advance_mode,
                            reason=reason,
                        )
                    )
                    candidate_index += 1
                    continue
                records.append(
                    _record(
                        run_id=run_id,
                        queue_item_id=ablation.item_id,
                        base_transform=base_transform,
                        candidate_index=candidate_index,
                        input_slice_id=input_data.input_slice.slice_id,
                        tokens=input_data.tokens,
                        labels=labels,
                        reset_mode=reset_mode,
                        advance_mode=advance_mode,
                        thresholds=thresholds,
                        metadata_support_status=input_data.metadata_support_status,
                        warnings=warnings,
                    )
                )
                candidate_index += 1

    if candidate_index != ablation.expected_candidate_count:
        raise ValueError(f"Candidate loop drifted: expected {ablation.expected_candidate_count}, got {candidate_index}.")
    if len(records) + len(deferred) != ablation.expected_candidate_count:
        raise ValueError("Executed plus deferred candidate count does not equal expected Stage 3H count.")

    ranked = sorted(records, key=_ranking_key, reverse=True)
    top_records = ranked[:top_k]
    top = top_records[0]
    confidence_distribution = _confidence_distribution(records)
    deferred_payloads = [to_jsonable(item) for item in deferred]
    if deferred:
        warnings.extend(
            f"{item.reason}:base_transform={item.base_transform_id}:reset={item.reset_mode}:advance={item.advance_mode}"
            for item in deferred
        )

    negative_controls = generate_family_negative_controls(records, thresholds=thresholds)
    elapsed_ms = round((perf_counter() - start) * 1000, 3)
    result_store_preview = {
        "record_type": "bounded_result_store_preview",
        "run_id": run_id,
        "policy_id": policy_id,
        "queue_item_id": ablation.item_id,
        "expected_candidate_count": ablation.expected_candidate_count,
        "executed_candidate_count": len(records),
        "deferred_candidate_count": len(deferred),
        "negative_control_count": len(negative_controls),
        "top_candidate_index": top.candidate_index,
        "top_base_transform_id": top.base_transform_id,
        "top_reset_mode": top.reset_mode,
        "top_advance_mode": top.advance_mode,
        "top_score": top.score_summary["total_score"],
        "top_length_normalized_score": top.score_summary.get("length_normalized_score"),
        "top_calibrated_confidence_label": top.calibrated_confidence_label,
        "confidence_distribution": confidence_distribution,
        "metadata_support_status": input_data.metadata_support_status,
        "deferred_candidates": deferred_payloads,
        "import_enabled": False,
        "generated_outputs_ignored": True,
    }
    summary = BoundedRunSummary(
        record_type="bounded_experiment_run_summary",
        run_id=run_id,
        queue_item_id=ablation.item_id,
        input_slice_id=input_data.input_slice.slice_id,
        input_length=input_data.input_slice.input_length,
        candidate_count=len(records),
        caesar_candidate_count=0,
        affine_candidate_count=0,
        top_k_count=len(top_records),
        top_candidate={
            "candidate_index": top.candidate_index,
            "transform_family": top.transform_family,
            "transform_id": top.transform_id,
            "transform_parameters": top.transform_parameters,
            "base_transform_id": top.base_transform_id,
            "base_transform_family": top.base_transform_family,
            "reset_mode": top.reset_mode,
            "advance_mode": top.advance_mode,
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
        expected_candidate_count=ablation.expected_candidate_count,
        executed_candidate_count=len(records),
        deferred_candidate_count=len(deferred),
        reset_modes=ablation.reset_modes,
        advance_modes=ablation.advance_modes,
        confidence_distribution=confidence_distribution,
        reset_advance_candidate_count=len(records),
        negative_control_count=len(negative_controls),
        metadata_support_status=input_data.metadata_support_status,
    )
    paths = write_candidate_outputs(out_dir, records, top_records, summary, warnings)
    negative_path = write_jsonl(paths["summary"].parent / "negative_control_records.jsonl", negative_controls)
    paths["negative_control_records"] = negative_path
    score_details_path = write_jsonl(paths["summary"].parent / "calibrated_scores.jsonl", _score_details(records, calibration))
    paths["calibrated_scores"] = score_details_path
    if deferred:
        paths["deferred_candidates"] = write_jsonl(paths["summary"].parent / "deferred_candidates.jsonl", deferred_payloads)
    summary = _with_output_paths(summary, paths)
    write_candidate_outputs(out_dir, records, top_records, summary, warnings)
    write_jsonl(negative_path, negative_controls)
    write_jsonl(score_details_path, _score_details(records, calibration))
    if deferred:
        write_jsonl(paths["summary"].parent / "deferred_candidates.jsonl", deferred_payloads)
    return summary


def load_declared_reset_advance_ablation(item: dict[str, Any]) -> ResetAdvanceAblation:
    item_id = str(item.get("item_id", ""))
    if item_id != TARGET_ITEM_ID:
        raise ValueError(f"Stage 3H executor only runs {TARGET_ITEM_ID}; got {item_id}.")
    if item.get("experiment_kind") != "reset_advance_ablation":
        raise ValueError("Stage 3H target must declare experiment_kind=reset_advance_ablation.")
    if item.get("cpu_only") is not True or item.get("cuda_enabled") is not False or item.get("no_solve_claim") is not True:
        raise ValueError("Stage 3H ablation must remain CPU-only, CUDA-disabled, and no-solve-claim.")
    params = _parameters(item)
    base_transforms = [str(value) for value in params.get("base_transforms", [])]
    reset_modes = [str(value) for value in params.get("reset_modes", [])]
    advance_modes = [str(value) for value in params.get("advance_modes", [])]
    if base_transforms != EXPECTED_STAGE3H_BASE_TRANSFORMS:
        raise ValueError("Stage 3H base transforms must remain the declared eight-transform ablation pack.")
    if reset_modes != SUPPORTED_RESET_MODES or set(reset_modes) != RESET_MODES:
        raise ValueError("Stage 3H reset modes must be exactly [none, word, clause, line].")
    if advance_modes != SUPPORTED_ADVANCE_MODES or set(advance_modes) != ADVANCE_MODES:
        raise ValueError("Stage 3H advance modes must be exactly [runes_only, token_break_preserving].")
    expected = len(base_transforms) * len(reset_modes) * len(advance_modes)
    declared = int(item.get("candidate_count_upper_bound", -1))
    calculated = validate_candidate_count(item)
    if declared != expected or calculated != expected:
        raise ValueError(f"Stage 3H candidate count must be {expected}, got declared={declared} calculated={calculated}.")
    for forbidden in ("key_search_enabled", "dictionary_search_enabled", "broad_sequence_search_enabled", "arbitrary_oeis_search_enabled", "unconstrained_skip_masks"):
        if params.get(forbidden) is not False:
            raise ValueError(f"Stage 3H ablation must set {forbidden}=false.")
    return ResetAdvanceAblation(
        item_id=item_id,
        base_transforms=base_transforms,
        reset_modes=reset_modes,
        advance_modes=advance_modes,
        expected_candidate_count=expected,
    )


def load_ablation_input(item: dict[str, Any]) -> AblationInput:
    input_slice = load_input_slice(item)
    token_records = _load_token_records(item, input_slice)
    tokens = build_tokens(token_records)
    support = metadata_support(tokens)
    warnings = [warning for warning in input_slice.warnings if warning != "flat_rune_index_stream_no_separator_context"]
    if not support.token_breaks:
        warnings.append("token_break_metadata_missing_flat_mode_used")
    for mode, reason in {
        "word": "word_reset_metadata_missing",
        "clause": "clause_reset_metadata_missing",
        "line": "line_reset_metadata_missing",
    }.items():
        if unsupported_reset_reason(tokens, mode) == reason:
            warnings.append(reason)
    return AblationInput(
        input_slice=input_slice,
        token_records=token_records,
        tokens=tokens,
        metadata_support_status=support.as_dict(),
        warnings=warnings,
    )


def _record(
    *,
    run_id: str,
    queue_item_id: str,
    base_transform: BaseTransform,
    candidate_index: int,
    input_slice_id: str,
    tokens: list[TransformToken],
    labels: dict[int, str],
    reset_mode: str,
    advance_mode: str,
    thresholds: dict[str, float],
    metadata_support_status: dict[str, bool],
    warnings: list[str],
) -> BoundedCandidateRecord:
    rendered = apply_stateful_transform(
        tokens,
        labels,
        reset_mode=reset_mode,
        advance_mode=advance_mode,
        transform_step=_transform_step(base_transform),
    )
    text = rendered.output_text
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
    transform_parameters = {
        "base_transform_id": base_transform.transform_id,
        "base_transform_family": base_transform.family,
        "key_text": base_transform.key_text,
        "key_indices": base_transform.key_indices,
        "offset": base_transform.offset,
        "reset_mode": reset_mode,
        "advance_mode": advance_mode,
        "direction": "decrypt_subtract",
        "metadata_support_status": metadata_support_status,
        "key_search_enabled": False,
        "dictionary_search_enabled": False,
        "broad_sequence_search_enabled": False,
        "arbitrary_oeis_search_enabled": False,
        "unconstrained_skip_masks": False,
    }
    return BoundedCandidateRecord(
        record_type="bounded_candidate_record",
        run_id=run_id,
        queue_item_id=queue_item_id,
        transform_family="reset_advance_ablation",
        transform_id=base_transform.transform_id,
        transform_parameters=transform_parameters,
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
            "base_transform_id": base_transform.transform_id,
            "reset_mode": reset_mode,
            "advance_mode": advance_mode,
            "output_index_count": len(rendered.output_indices),
        },
        search_performed=True,
        scoring_used=True,
        cuda_used=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        solve_claim=False,
        trusted_as_canonical=False,
        warnings=warnings + rendered.warnings,
        key_text=base_transform.key_text,
        key_indices=base_transform.key_indices,
        calibrated_confidence_label=calibrated_label,
        crib_hits=crib_payload["crib_hits"],
        crib_hit_count=crib_payload["crib_hit_count"],
        calibration_position=calibration_position,
        base_transform_id=base_transform.transform_id,
        base_transform_family=base_transform.family,
        reset_mode=reset_mode,
        advance_mode=advance_mode,
        transformable_token_count=rendered.transformable_token_count,
        metadata_support_status=metadata_support_status,
    )


def _base_transforms(base_transform_ids: list[str]) -> list[BaseTransform]:
    profile = load_gematria_profile(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")
    transforms: list[BaseTransform] = []
    for transform_id in base_transform_ids:
        if transform_id.startswith("vigenere:"):
            key_text = transform_id.split(":", 1)[1]
            transforms.append(
                BaseTransform(
                    transform_id=transform_id,
                    family="vigenere",
                    key_text=key_text,
                    key_indices=key_text_to_indices(key_text, profile),
                )
            )
            continue
        if transform_id.startswith("prime_minus_one:offset="):
            transforms.append(
                BaseTransform(transform_id=transform_id, family="prime_minus_one", offset=int(transform_id.rsplit("=", 1)[1]))
            )
            continue
        if transform_id.startswith("prime_mod29:offset="):
            transforms.append(BaseTransform(transform_id=transform_id, family="prime_mod29", offset=int(transform_id.rsplit("=", 1)[1])))
            continue
        if transform_id.startswith("prime_gap:offset="):
            transforms.append(BaseTransform(transform_id=transform_id, family="prime_gap", offset=int(transform_id.rsplit("=", 1)[1])))
            continue
        raise ValueError(f"Unsupported Stage 3H base transform: {transform_id}")
    return transforms


def _transform_step(base_transform: BaseTransform):
    if base_transform.family == "vigenere":
        key_indices = base_transform.key_indices or []
        if not key_indices:
            raise ValueError("Vigenere base transform requires key indices.")

        def step(cipher_index: int, state_position: int) -> tuple[int, dict[str, Any]]:
            key_index = key_indices[state_position % len(key_indices)]
            return (cipher_index - key_index) % MODULUS, {"key_index": key_index}

        return step

    offset = int(base_transform.offset or 0)
    if base_transform.family == "prime_minus_one":

        def step(cipher_index: int, state_position: int) -> tuple[int, dict[str, Any]]:
            stream_value = prime_minus_one_value(offset, state_position)
            return (cipher_index - stream_value) % MODULUS, {"stream_value": stream_value}

        return step
    if base_transform.family == "prime_mod29":

        def step(cipher_index: int, state_position: int) -> tuple[int, dict[str, Any]]:
            stream_value = prime_mod29_value(offset, state_position)
            return (cipher_index - stream_value) % MODULUS, {"stream_value": stream_value}

        return step
    if base_transform.family == "prime_gap":

        def step(cipher_index: int, state_position: int) -> tuple[int, dict[str, Any]]:
            stream_value = prime_gap_value(offset, state_position)
            return (cipher_index - stream_value) % MODULUS, {"stream_value": stream_value}

        return step
    raise ValueError(f"Unsupported base transform family: {base_transform.family}")


def _load_token_records(item: dict[str, Any], input_slice: InputSlice) -> list[dict[str, Any]]:
    selector = dict(dict(item.get("corpus_slice", {})).get("selector", {}))
    inline_tokens = selector.get("token_records")
    if isinstance(inline_tokens, list):
        return [dict(token) for token in inline_tokens if isinstance(token, dict)]
    tokens_path = input_slice.source_metadata.get("tokens_path")
    start = input_slice.source_metadata.get("start_token_index")
    end = input_slice.source_metadata.get("end_token_index")
    if tokens_path and start is not None and end is not None:
        return _load_token_range(Path(str(tokens_path)), int(start), int(end))
    return [
        {
            "token_kind": "rune",
            "index29": value,
            "token_index_global": position,
            "synthetic_flat_token": True,
        }
        for position, value in enumerate(input_slice.index29_values)
    ]


def _load_token_range(path: Path, start: int, end: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        index = int(payload["token_index_global"])
        if index < start:
            continue
        if index > end:
            break
        records.append(payload)
    if not records:
        raise ValueError("Stage 3H token metadata path did not yield selector records.")
    return records


def _parameters(item: dict[str, Any]) -> dict[str, Any]:
    plan = dict(item.get("transform_plan", {}))
    params = plan.get("parameters", {})
    return dict(params) if isinstance(params, dict) else {}


def _ranking_key(record: BoundedCandidateRecord) -> tuple[float, float, int, int]:
    return (
        float(record.score_summary.get("length_normalized_score", record.score_summary["total_score"])),
        float(record.score_summary["total_score"]),
        int(record.crib_hit_count or 0),
        -record.candidate_index,
    )


def _confidence_distribution(records: list[BoundedCandidateRecord]) -> dict[str, int]:
    distribution: dict[str, int] = {}
    for record in records:
        label = record.calibrated_confidence_label or str(record.score_summary.get("confidence_label", "unlabeled"))
        distribution[label] = distribution.get(label, 0) + 1
    return dict(sorted(distribution.items()))


def _score_details(records: list[BoundedCandidateRecord], calibration: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "record_type": "stage3h_calibrated_score_detail",
            "run_id": record.run_id,
            "queue_item_id": record.queue_item_id,
            "candidate_index": record.candidate_index,
            "base_transform_id": record.base_transform_id,
            "base_transform_family": record.base_transform_family,
            "reset_mode": record.reset_mode,
            "advance_mode": record.advance_mode,
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
        expected_candidate_count=summary.expected_candidate_count,
        executed_candidate_count=summary.executed_candidate_count,
        deferred_candidate_count=summary.deferred_candidate_count,
        reset_modes=summary.reset_modes,
        advance_modes=summary.advance_modes,
        confidence_distribution=summary.confidence_distribution,
        reset_advance_candidate_count=summary.reset_advance_candidate_count,
        negative_control_count=summary.negative_control_count,
        metadata_support_status=summary.metadata_support_status,
    )
