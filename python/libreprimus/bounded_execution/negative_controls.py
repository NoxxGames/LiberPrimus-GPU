"""Family-specific negative controls for Stage 3H bounded experiments."""

from __future__ import annotations

import hashlib
import random
from typing import Any

from libreprimus.bounded_execution.models import BoundedCandidateRecord
from libreprimus.scoring.calibration import classify_score
from libreprimus.scoring.crib_checks import crib_check
from libreprimus.scoring.minimal_triage import score_text
from libreprimus.scoring.validation import validate_crib_check_result, validate_minimal_triage_score

CONTROL_KINDS = [
    "rune_shuffle_same_length",
    "rune_freq_preserving_shuffle",
    "separator_randomised_variant",
    "wrong_mapping_variant",
]


def generate_family_negative_controls(
    records: list[BoundedCandidateRecord],
    *,
    thresholds: dict[str, float],
    representative_transform_subset_size: int = 25,
    seed: int = 3301,
) -> list[dict[str, Any]]:
    representatives = records[:representative_transform_subset_size]
    controls: list[dict[str, Any]] = []
    control_index = 0
    for source_index, record in enumerate(representatives):
        for control_kind in CONTROL_KINDS:
            text = _control_text(record.output_normalized_text, control_kind, seed + control_index)
            score = validate_minimal_triage_score(score_text(text))
            crib_payload = validate_crib_check_result(
                crib_check(text, candidate_id=f"{record.queue_item_id}-negative-{control_index}")
            )
            label = classify_score(score, crib_payload, thresholds)
            score["calibrated_confidence_label"] = label
            score["crib_hit_count"] = crib_payload["crib_hit_count"]
            score["crib_hits"] = crib_payload["crib_hits"]
            score["no_solve_claim"] = True
            controls.append(
                {
                    "record_type": "family_negative_control_record",
                    "run_id": record.run_id,
                    "queue_item_id": record.queue_item_id,
                    "control_index": control_index,
                    "control_kind": control_kind,
                    "source_candidate_index": record.candidate_index,
                    "source_candidate_family": record.transform_family,
                    "source_base_transform_id": record.base_transform_id,
                    "output_preview": text[:160],
                    "output_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "score_summary": score,
                    "confidence_label": label,
                    "calibrated_confidence_label": label,
                    "crib_hits": crib_payload["crib_hits"],
                    "crib_hit_count": crib_payload["crib_hit_count"],
                    "search_performed": True,
                    "scoring_used": True,
                    "cuda_used": False,
                    "solve_claim": False,
                    "canonical_corpus_active": False,
                    "page_boundaries_final": False,
                    "trusted_as_canonical": False,
                    "warnings": [],
                }
            )
            control_index += 1
    return controls


def _control_text(text: str, control_kind: str, seed: int) -> str:
    if control_kind == "rune_shuffle_same_length":
        return _shuffle_letters(text, seed, keep_spaces=False)
    if control_kind == "rune_freq_preserving_shuffle":
        return _shuffle_letters(text, seed, keep_spaces=True)
    if control_kind == "separator_randomised_variant":
        return _randomise_separators(text, seed)
    if control_kind == "wrong_mapping_variant":
        return _shift_letters(text)
    raise ValueError(f"Unsupported negative control kind: {control_kind}")


def _shuffle_letters(text: str, seed: int, *, keep_spaces: bool) -> str:
    rng = random.Random(seed)
    letters = [char for char in text if char.isalpha()]
    rng.shuffle(letters)
    if not keep_spaces:
        return "".join(letters)
    output: list[str] = []
    iterator = iter(letters)
    for char in text:
        output.append(next(iterator) if char.isalpha() else char)
    return "".join(output)


def _randomise_separators(text: str, seed: int) -> str:
    letters = [char for char in text if char.isalpha()]
    if not letters:
        return text
    rng = random.Random(seed)
    output: list[str] = []
    for index, char in enumerate(letters):
        output.append(char)
        if index != len(letters) - 1 and rng.randrange(7) == 0:
            output.append(" ")
    return "".join(output)


def _shift_letters(text: str) -> str:
    shifted: list[str] = []
    for char in text:
        if "A" <= char <= "Z":
            shifted.append(chr(((ord(char) - ord("A") + 1) % 26) + ord("A")))
        else:
            shifted.append(char)
    return "".join(shifted)
