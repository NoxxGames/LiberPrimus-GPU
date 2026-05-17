"""Candidate-pack loading and deterministic expansion."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.hash_preimage.base29 import render_base29_upper
from libreprimus.hash_preimage.byte_variants import apply_byte_variant
from libreprimus.hash_preimage.models import CandidateText, ExpandedPack
from libreprimus.history.source_records import SOURCE_CLASSES, resolve_repo_path

SUPPORTED_ALGORITHMS = {"sha256"}
LITERAL_VARIANTS = {
    "raw",
    "lower",
    "upper",
    "trailing_lf",
    "trailing_crlf",
    "leading_space",
    "trailing_space",
    "wrapped_space",
}
NUMERIC_VARIANTS = {"raw", "trailing_lf", "trailing_crlf", "trailing_space"}
RENDER_FORMS = {"decimal", "hex_lower", "hex_upper", "binary", "base29_upper"}
PAIR_SEPARATORS = {
    "empty": "",
    "colon": ":",
    "comma": ",",
    "hyphen": "-",
    "underscore": "_",
    "slash": "/",
    "space": " ",
}


def load_candidate_pack(path: Path) -> dict[str, Any]:
    resolved = resolve_repo_path(path)
    payload = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Candidate pack must be a mapping: {resolved}")
    return payload


def iter_candidate_pack_paths(pack_dir: Path) -> list[Path]:
    resolved = resolve_repo_path(pack_dir)
    return sorted(resolved.glob("*.yaml"))


def load_candidate_packs(pack_dir: Path) -> list[dict[str, Any]]:
    return [load_candidate_pack(path) for path in iter_candidate_pack_paths(pack_dir)]


def validate_candidate_pack(pack: dict[str, Any]) -> list[str]:
    pack_id = str(pack.get("pack_id", "<unknown>"))
    errors: list[str] = []
    required = {
        "record_type",
        "pack_id",
        "description",
        "algorithm",
        "source_class",
        "candidate_groups",
        "byte_variants",
        "candidate_count_upper_bound",
        "generated_from_external_dictionary",
        "cuda_enabled",
        "cloud_execution",
        "no_solve_claim",
        "trusted_as_canonical",
        "notes",
    }
    missing = sorted(required - set(pack))
    if missing:
        errors.append(f"{pack_id}: missing fields {missing}")
    if pack.get("record_type") != "hash_preimage_candidate_pack":
        errors.append(f"{pack_id}: invalid record_type")
    if pack.get("algorithm") != "sha256":
        errors.append(f"{pack_id}: only sha256 is allowed")
    if pack.get("source_class") not in SOURCE_CLASSES:
        errors.append(f"{pack_id}: invalid source_class")
    if pack.get("generated_from_external_dictionary") is not False:
        errors.append(f"{pack_id}: external dictionary flag must be false")
    if pack.get("cuda_enabled") is not False:
        errors.append(f"{pack_id}: cuda_enabled must be false")
    if pack.get("cloud_execution") is not False:
        errors.append(f"{pack_id}: cloud_execution must be false")
    if pack.get("no_solve_claim") is not True:
        errors.append(f"{pack_id}: no_solve_claim must be true")
    if pack.get("trusted_as_canonical") is not False:
        errors.append(f"{pack_id}: trusted_as_canonical must be false")
    if not isinstance(pack.get("candidate_groups"), dict):
        errors.append(f"{pack_id}: candidate_groups must be a mapping")
    byte_variants = pack.get("byte_variants")
    if not isinstance(byte_variants, list) or not byte_variants:
        errors.append(f"{pack_id}: byte_variants must be a non-empty list")
    else:
        allowed = NUMERIC_VARIANTS if "numeric" in pack_id else LITERAL_VARIANTS
        for variant in byte_variants:
            if variant not in allowed:
                errors.append(f"{pack_id}: unsupported byte variant {variant}")
    upper_bound = pack.get("candidate_count_upper_bound")
    if not isinstance(upper_bound, int) or upper_bound <= 0 or upper_bound > 100000:
        errors.append(f"{pack_id}: invalid candidate_count_upper_bound")
    try:
        expanded = expand_candidate_pack(pack)
    except Exception as exc:  # noqa: BLE001 - returned as validation detail.
        errors.append(f"{pack_id}: expansion failed: {exc}")
    else:
        if expanded.total_generated_before_dedup > expanded.candidate_count_upper_bound:
            errors.append(
                f"{pack_id}: generated {expanded.total_generated_before_dedup} exceeds upper bound "
                f"{expanded.candidate_count_upper_bound}"
            )
    return errors


def validate_pack_dir(pack_dir: Path) -> tuple[int, list[str]]:
    packs = load_candidate_packs(pack_dir)
    errors: list[str] = []
    seen: set[str] = set()
    for pack in packs:
        pack_id = str(pack.get("pack_id", ""))
        if pack_id in seen:
            errors.append(f"{pack_id}: duplicate pack_id")
        seen.add(pack_id)
        errors.extend(validate_candidate_pack(pack))
    return len(packs), errors


def expand_candidate_pack(pack: dict[str, Any]) -> ExpandedPack:
    pack_id = str(pack["pack_id"])
    algorithm = str(pack["algorithm"])
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    variants = [str(variant) for variant in pack["byte_variants"]]
    base_literals = (
        _expand_numeric_literals(pack)
        if pack_id == "hist_cookie_base29_numeric_pack_v1"
        else _expand_literal_pack(pack)
    )

    generated: list[CandidateText] = []
    for group_name, source_literal in base_literals:
        for variant in variants:
            literal_text = apply_byte_variant(source_literal, variant)
            generated.append(
                CandidateText(
                    pack_id=pack_id,
                    candidate_group=group_name,
                    source_literal=source_literal,
                    literal_text=literal_text,
                    byte_variant=variant,
                )
            )

    deduped: list[CandidateText] = []
    seen_bytes: set[bytes] = set()
    for candidate in generated:
        candidate_bytes = candidate.literal_text.encode(candidate.encoding)
        if candidate_bytes in seen_bytes:
            continue
        seen_bytes.add(candidate_bytes)
        deduped.append(candidate)
    return ExpandedPack(
        pack_id=pack_id,
        algorithm=algorithm,
        candidates=deduped,
        total_generated_before_dedup=len(generated),
        duplicate_count=len(generated) - len(deduped),
        candidate_count_upper_bound=int(pack["candidate_count_upper_bound"]),
    )


def _expand_literal_pack(pack: dict[str, Any]) -> list[tuple[str, str]]:
    groups = pack["candidate_groups"]
    literals: list[tuple[str, str]] = []
    for group_name, values in groups.items():
        if not isinstance(values, list):
            raise ValueError(f"{group_name}: literal group must be a list")
        for value in values:
            literals.append((str(group_name), str(value)))
    return literals


def _expand_numeric_literals(pack: dict[str, Any]) -> list[tuple[str, str]]:
    groups = pack["candidate_groups"]
    render_forms = [str(form) for form in groups.get("render_forms", [])]
    separators = [str(separator) for separator in groups.get("pair_separators", [])]
    if any(form not in RENDER_FORMS for form in render_forms):
        raise ValueError("numeric pack has unsupported render form")
    if any(separator not in PAIR_SEPARATORS for separator in separators):
        raise ValueError("numeric pack has unsupported pair separator")

    literals: list[tuple[str, str]] = []
    for number in groups.get("historical_numbers", []):
        numeric_value = int(number)
        for form in render_forms:
            literals.append((f"historical_numbers:{form}", render_number(numeric_value, form)))
    for pair in groups.get("ordered_pairs", []):
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("ordered pair entries must have two values")
        left, right = int(pair[0]), int(pair[1])
        for form in render_forms:
            rendered_left = render_number(left, form)
            rendered_right = render_number(right, form)
            for separator_name in separators:
                separator = PAIR_SEPARATORS[separator_name]
                literals.append(
                    (
                        f"ordered_pairs:{form}:{separator_name}",
                        f"{rendered_left}{separator}{rendered_right}",
                    )
                )
    return literals


def render_number(value: int, form: str) -> str:
    if form == "decimal":
        return str(value)
    if form == "hex_lower":
        return format(value, "x")
    if form == "hex_upper":
        return format(value, "X")
    if form == "binary":
        return format(value, "b")
    if form == "base29_upper":
        return render_base29_upper(value)
    raise ValueError(f"Unsupported numeric render form: {form}")
