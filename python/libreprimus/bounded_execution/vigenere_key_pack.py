"""Bounded Vigenere evidence-key pack execution."""

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
from libreprimus.solved_fixtures.direct_translation import normalize_plaintext
from libreprimus.solved_fixtures.models import to_jsonable
from libreprimus.solved_fixtures.vigenere import key_text_to_indices

TARGET_ITEM_ID = "stage3e_vig_lp_evidence_pack_v1"
HISTORICAL_ITEM_ID = "stage3e_vig_history_key_pack_v1"
EXPECTED_STAGE3F_KEYS = [
    "DIVINITY",
    "FIRFUMFERENFE",
    "PARABLE",
    "INSTAR",
    "EMERGE",
    "WITHIN",
    "WELCOME",
    "PILGRIM",
    "TOTIENT",
    "PRIMES",
    "SACRED",
    "ENCRYPTED",
]
EXPECTED_STAGE3I_KEYS = [
    "PATIENCEISAVIRTUE",
    "THEINSTAREMERGENCE",
    "SELFRELIANCE",
    "BOOKOFTHELAW",
    "MABINOGION",
    "AGRIPPA",
    "EMERSON",
    "CROWLEY",
    "BLAKE",
    "PATIENCE",
    "VIRTUE",
    "SELF",
    "RELIANCE",
    "LAW",
]
SUPPORTED_RESET_MODES = {"none", "line"}
SUPPORTED_ADVANCE_MODES = {"runes_only", "token_break_preserving"}
MODULUS = 29

KEY_PACK_CONFIGS = {
    TARGET_ITEM_ID: {
        "expected_keys": EXPECTED_STAGE3F_KEYS,
        "evidence_family": "lp_evidence_key_pack",
        "run_id_prefix": "stage3f",
        "description": "12 declared LP evidence keys",
    },
    HISTORICAL_ITEM_ID: {
        "expected_keys": EXPECTED_STAGE3I_KEYS,
        "evidence_family": "historical_motif_key_pack",
        "run_id_prefix": "stage3i",
        "description": "14 declared historical motif keys",
    },
}


@dataclass(frozen=True)
class VigenereKeyPack:
    item_id: str
    keys: list[str]
    reset_modes: list[str]
    advance_modes: list[str]
    expected_candidate_count: int
    evidence_family: str
    run_id_prefix: str


@dataclass(frozen=True)
class KeyPackInput:
    input_slice: InputSlice
    token_records: list[dict[str, Any]]
    has_token_break_metadata: bool
    has_line_metadata: bool
    warnings: list[str]


@dataclass(frozen=True)
class DeferredCandidate:
    candidate_index: int
    key_text: str
    reset_mode: str
    advance_mode: str
    reason: str


def run_vigenere_key_pack_from_paths(
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
    return run_vigenere_key_pack_item(
        item,
        out_dir=out_dir,
        top_k=top_k,
        policy_id=policy.policy_id,
        calibration_summary_path=calibration_summary_path,
    )


def run_vigenere_key_pack_item(
    item: dict[str, Any],
    *,
    out_dir: Path,
    top_k: int = 25,
    policy_id: str = "operator-policy-v0",
    calibration_summary_path: Path = DEFAULT_CALIBRATION_SUMMARY,
) -> BoundedRunSummary:
    start = perf_counter()
    pack = load_declared_key_pack(item)
    input_data = load_key_pack_input(item)
    profile = load_gematria_profile(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")
    labels = labels_by_index(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")
    key_indices_by_text = {key: key_text_to_indices(key, profile) for key in pack.keys}
    calibration = load_calibration_summary(calibration_summary_path)
    thresholds = dict(calibration.get("thresholds", {}))
    warnings = list(input_data.warnings)
    if not calibration:
        warnings.append("stage3c_calibration_summary_missing; calibrated label falls back to current thresholds.")

    run_id = f"{pack.run_id_prefix}-{pack.item_id}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    records: list[BoundedCandidateRecord] = []
    deferred: list[DeferredCandidate] = []
    candidate_index = 0
    for key_text in pack.keys:
        key_indices = key_indices_by_text[key_text]
        for reset_mode in pack.reset_modes:
            for advance_mode in pack.advance_modes:
                if reset_mode == "line" and not input_data.has_line_metadata:
                    deferred.append(
                        DeferredCandidate(
                            candidate_index=candidate_index,
                            key_text=key_text,
                            reset_mode=reset_mode,
                            advance_mode=advance_mode,
                            reason="line_reset_metadata_missing",
                        )
                    )
                    candidate_index += 1
                    continue
                mode_warnings = _mode_warnings(input_data, reset_mode, advance_mode)
                records.append(
                    _record(
                        run_id=run_id,
                        queue_item_id=pack.item_id,
                        key_text=key_text,
                        key_indices=key_indices,
                        candidate_index=candidate_index,
                        input_slice_id=input_data.input_slice.slice_id,
                        token_records=input_data.token_records,
                        labels=labels,
                        reset_mode=reset_mode,
                        advance_mode=advance_mode,
                        evidence_family=pack.evidence_family,
                        thresholds=thresholds,
                        warnings=warnings + mode_warnings,
                    )
                )
                candidate_index += 1

    if candidate_index != pack.expected_candidate_count:
        raise ValueError(f"Candidate loop drifted: expected {pack.expected_candidate_count}, got {candidate_index}.")
    if len(records) + len(deferred) != pack.expected_candidate_count:
        raise ValueError("Executed plus deferred candidate count does not equal expected Stage 3F count.")

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
    confidence_distribution = _confidence_distribution(records)
    elapsed_ms = round((perf_counter() - start) * 1000, 3)
    deferred_payloads = [to_jsonable(item) for item in deferred]
    if deferred:
        warnings.extend(f"{item.reason}:{item.key_text}:{item.reset_mode}:{item.advance_mode}" for item in deferred)

    result_store_preview = {
        "record_type": "bounded_result_store_preview",
        "run_id": run_id,
        "policy_id": policy_id,
        "queue_item_id": pack.item_id,
        "expected_candidate_count": pack.expected_candidate_count,
        "executed_candidate_count": len(records),
        "deferred_candidate_count": len(deferred),
        "top_candidate_index": top.candidate_index,
        "top_key_text": top.key_text,
        "top_reset_mode": top.transform_parameters["reset_mode"],
        "top_advance_mode": top.transform_parameters["advance_mode"],
        "top_evidence_family": top.transform_parameters["evidence_family"],
        "top_score": top.score_summary["total_score"],
        "top_length_normalized_score": top.score_summary.get("length_normalized_score"),
        "top_calibrated_confidence_label": top.calibrated_confidence_label,
        "confidence_distribution": confidence_distribution,
        "deferred_candidates": deferred_payloads,
        "import_enabled": False,
        "generated_outputs_ignored": True,
    }
    summary = BoundedRunSummary(
        record_type="bounded_experiment_run_summary",
        run_id=run_id,
        queue_item_id=pack.item_id,
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
            "key_text": top.key_text,
            "key_indices": top.key_indices,
            "reset_mode": top.transform_parameters["reset_mode"],
            "advance_mode": top.transform_parameters["advance_mode"],
            "evidence_family": top.transform_parameters["evidence_family"],
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
        expected_candidate_count=pack.expected_candidate_count,
        executed_candidate_count=len(records),
        deferred_candidate_count=len(deferred),
        key_count=len(pack.keys),
        reset_modes=pack.reset_modes,
        advance_modes=pack.advance_modes,
        confidence_distribution=confidence_distribution,
    )
    paths = write_candidate_outputs(out_dir, records, top_records, summary, warnings)
    score_details_path = write_jsonl(paths["summary"].parent / "calibrated_scores.jsonl", _score_details(records, calibration))
    paths["calibrated_scores"] = score_details_path
    if deferred:
        paths["deferred_candidates"] = write_jsonl(paths["summary"].parent / "deferred_candidates.jsonl", deferred_payloads)
    summary = _with_output_paths(summary, paths)
    write_candidate_outputs(out_dir, records, top_records, summary, warnings)
    write_jsonl(score_details_path, _score_details(records, calibration))
    if deferred:
        write_jsonl(paths["summary"].parent / "deferred_candidates.jsonl", deferred_payloads)
    return summary


def load_declared_key_pack(item: dict[str, Any]) -> VigenereKeyPack:
    item_id = str(item.get("item_id", ""))
    config = KEY_PACK_CONFIGS.get(item_id)
    if config is None:
        raise ValueError(f"Unsupported bounded Vigenere key-pack item: {item_id}.")
    if item.get("experiment_kind") != "vigenere_key_pack":
        raise ValueError("Bounded Vigenere key-pack items must declare experiment_kind=vigenere_key_pack.")
    if item.get("cpu_only") is not True or item.get("cuda_enabled") is not False or item.get("no_solve_claim") is not True:
        raise ValueError("Bounded Vigenere key packs must remain CPU-only, CUDA-disabled, and no-solve-claim.")
    params = _parameters(item)
    keys = [str(key).strip().upper() for key in params.get("keys", [])]
    reset_modes = [str(mode) for mode in params.get("reset_modes", [])]
    advance_modes = [str(mode) for mode in params.get("advance_modes", [])]
    expected_keys = list(config["expected_keys"])
    if keys != expected_keys:
        raise ValueError(f"{item_id} must stay at the {config['description']}.")
    if set(reset_modes) != SUPPORTED_RESET_MODES or reset_modes != ["none", "line"]:
        raise ValueError("Bounded Vigenere key-pack reset modes must be exactly [none, line].")
    if set(advance_modes) != SUPPORTED_ADVANCE_MODES or advance_modes != ["runes_only", "token_break_preserving"]:
        raise ValueError("Bounded Vigenere key-pack advance modes must be exactly [runes_only, token_break_preserving].")
    expected = len(keys) * len(reset_modes) * len(advance_modes)
    declared = int(item.get("candidate_count_upper_bound", -1))
    calculated = validate_candidate_count(item)
    if declared != expected or calculated != expected:
        raise ValueError(f"{item_id} candidate count must be {expected}, got declared={declared} calculated={calculated}.")
    for forbidden in ("key_search_enabled", "dictionary_search_enabled", "unconstrained_skip_masks"):
        if params.get(forbidden) is not False:
            raise ValueError(f"Bounded Vigenere key packs must set {forbidden}=false.")
    return VigenereKeyPack(
        item_id=item_id,
        keys=keys,
        reset_modes=reset_modes,
        advance_modes=advance_modes,
        expected_candidate_count=expected,
        evidence_family=str(config["evidence_family"]),
        run_id_prefix=str(config["run_id_prefix"]),
    )


def load_key_pack_input(item: dict[str, Any]) -> KeyPackInput:
    input_slice = load_input_slice(item)
    token_records = _load_token_records(item, input_slice)
    has_token_break_metadata = any(str(token.get("token_kind")) != "rune" for token in token_records)
    rune_tokens = [token for token in token_records if str(token.get("token_kind")) == "rune"]
    has_line_metadata = bool(rune_tokens) and all(_line_id(token) is not None for token in rune_tokens)
    warnings = [warning for warning in input_slice.warnings if warning != "flat_rune_index_stream_no_separator_context"]
    if not has_token_break_metadata:
        warnings.append("token_break_metadata_missing_flat_mode_used")
    if not has_line_metadata:
        warnings.append("line_reset_metadata_missing")
    return KeyPackInput(
        input_slice=input_slice,
        token_records=token_records,
        has_token_break_metadata=has_token_break_metadata,
        has_line_metadata=has_line_metadata,
        warnings=warnings,
    )


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
        raise ValueError("Stage 3F token metadata path did not yield selector records.")
    return records


def _record(
    *,
    run_id: str,
    queue_item_id: str,
    key_text: str,
    key_indices: list[int],
    candidate_index: int,
    input_slice_id: str,
    token_records: list[dict[str, Any]],
    labels: dict[int, str],
    reset_mode: str,
    advance_mode: str,
    evidence_family: str,
    thresholds: dict[str, float],
    warnings: list[str],
) -> BoundedCandidateRecord:
    text, output_indices = render_vigenere_key_pack_candidate(
        token_records,
        key_indices=key_indices,
        labels=labels,
        reset_mode=reset_mode,
        advance_mode=advance_mode,
    )
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
        "direction": "decrypt_subtract",
        "key_text": key_text,
        "reset_mode": reset_mode,
        "advance_mode": advance_mode,
        "evidence_family": evidence_family,
        "key_search_enabled": False,
        "dictionary_search_enabled": False,
        "unconstrained_skip_masks": False,
    }
    return BoundedCandidateRecord(
        record_type="bounded_candidate_record",
        run_id=run_id,
        queue_item_id=queue_item_id,
        transform_family="vigenere_key_pack",
        transform_id="vigenere_explicit_key",
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
            "reset_mode": reset_mode,
            "advance_mode": advance_mode,
            "evidence_family": evidence_family,
            "output_index_count": len(output_indices),
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
        evidence_family=evidence_family,
        calibrated_confidence_label=calibrated_label,
        crib_hits=crib_payload["crib_hits"],
        crib_hit_count=crib_payload["crib_hit_count"],
        calibration_position=calibration_position,
    )


def render_vigenere_key_pack_candidate(
    token_records: list[dict[str, Any]],
    *,
    key_indices: list[int],
    labels: dict[int, str],
    reset_mode: str,
    advance_mode: str,
) -> tuple[str, list[int]]:
    if not key_indices:
        raise ValueError("Vigenere key indices must not be empty.")
    if reset_mode not in SUPPORTED_RESET_MODES:
        raise ValueError(f"Unsupported Stage 3F reset mode: {reset_mode}")
    if advance_mode not in SUPPORTED_ADVANCE_MODES:
        raise ValueError(f"Unsupported Stage 3F advance mode: {advance_mode}")
    parts: list[str] = []
    output_indices: list[int] = []
    key_position = 0
    current_line_id: Any = object()
    for token in token_records:
        kind = str(token.get("token_kind"))
        if kind == "rune":
            line_id = _line_id(token)
            if reset_mode == "line" and line_id != current_line_id:
                key_position = 0
                current_line_id = line_id
            raw_index = token.get("index29")
            if not isinstance(raw_index, int) or raw_index < 0 or raw_index > 28:
                raise ValueError(f"Rune token missing valid index29 at token {token.get('token_index_global')}.")
            key_index = key_indices[key_position % len(key_indices)]
            decoded_index = (raw_index - key_index) % MODULUS
            output_indices.append(decoded_index)
            parts.append(labels[decoded_index])
            key_position += 1
            continue
        if advance_mode == "token_break_preserving":
            separator = _separator_text(token)
            if separator:
                parts.append(separator)
    return normalize_plaintext(parts), output_indices


def _separator_text(token: dict[str, Any]) -> str:
    kind = str(token.get("token_kind"))
    if kind == "word_separator":
        return " "
    if kind == "clause_separator":
        return ". "
    if kind in {"line_separator", "physical_newline"}:
        return "\n"
    if kind in {"paragraph_separator", "segment_separator", "chapter_separator", "page_separator_or_marker", "whitespace"}:
        return " "
    if kind == "numeric_literal":
        return str(token.get("raw_text", ""))
    if kind == "unknown_symbol":
        return str(token.get("raw_text", ""))
    return ""


def _mode_warnings(input_data: KeyPackInput, reset_mode: str, advance_mode: str) -> list[str]:
    warnings: list[str] = []
    if advance_mode == "token_break_preserving" and not input_data.has_token_break_metadata:
        warnings.append("token_break_metadata_missing_flat_mode_used")
    if reset_mode == "line" and not input_data.has_line_metadata:
        warnings.append("line_reset_metadata_missing")
    return warnings


def _line_id(token: dict[str, Any]) -> Any:
    for field in ("logical_line_index", "physical_line_number", "line_index"):
        value = token.get(field)
        if value is not None:
            return value
    return None


def _parameters(item: dict[str, Any]) -> dict[str, Any]:
    plan = dict(item.get("transform_plan", {}))
    params = plan.get("parameters", {})
    return dict(params) if isinstance(params, dict) else {}


def _confidence_distribution(records: list[BoundedCandidateRecord]) -> dict[str, int]:
    distribution: dict[str, int] = {}
    for record in records:
        label = record.calibrated_confidence_label or str(record.score_summary.get("confidence_label", "unlabeled"))
        distribution[label] = distribution.get(label, 0) + 1
    return dict(sorted(distribution.items()))


def _score_details(records: list[BoundedCandidateRecord], calibration: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "record_type": "stage3f_calibrated_score_detail",
            "run_id": record.run_id,
            "queue_item_id": record.queue_item_id,
            "candidate_index": record.candidate_index,
            "key_text": record.key_text,
            "reset_mode": record.transform_parameters["reset_mode"],
            "advance_mode": record.transform_parameters["advance_mode"],
            "evidence_family": record.transform_parameters["evidence_family"],
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
        expected_candidate_count=summary.expected_candidate_count,
        executed_candidate_count=summary.executed_candidate_count,
        deferred_candidate_count=summary.deferred_candidate_count,
        key_count=summary.key_count,
        reset_modes=summary.reset_modes,
        advance_modes=summary.advance_modes,
        confidence_distribution=summary.confidence_distribution,
    )
