"""Number-fact card normalization for the Source Browser.

This module is display/reviewability infrastructure only. It does not infer new
facts from raw sources and it does not mutate historical source-lock records.
"""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .entries import SourceBrowserEntry

OVERLAY_DIR = Path("data/operator-console/source-browser/number-fact-overlays")

REVIEW_STATES = {
    "rich_fact_card",
    "extracted_basic_fact",
    "vague_fact_enrichment_needed",
    "zero_extracted_facts_not_reviewed",
    "zero_extracted_facts_reviewed_none_found",
    "overlay_enriched_fact",
    "quarantined_fact",
    "canonical_verification_required",
}

VALUE_TYPES = {
    "gp_sum",
    "prime",
    "prime_index",
    "rune_count",
    "word_count",
    "pixel_count",
    "rgb_value",
    "coordinate",
    "page_number",
    "hash_length",
    "hash_value",
    "file_size",
    "duration_seconds",
    "sequence",
    "matrix_value",
    "modular_residue",
    "factorization",
    "product",
    "sum",
    "difference",
    "ratio",
    "unknown",
}

OPERATION_TYPES = {
    "source_observation",
    "gp_sum",
    "progressive_sum",
    "cumulative_sum",
    "prime_index_lookup",
    "factorization",
    "product",
    "sum",
    "difference",
    "modulo",
    "count_equality",
    "section_count_equality",
    "pixel_frequency",
    "hash_contract",
    "matrix_grid_match",
    "sequence_mapping",
    "reverse_digits",
    "base_conversion",
    "symbolic_gp_scan",
    "unknown",
}

VERIFICATION_STATUSES = {
    "arithmetic_verified_metadata_only",
    "source_author_claim",
    "operator_assistant_observed",
    "canonical_transcript_required",
    "canonical_image_required",
    "canonical_source_required",
    "needs_exact_token_selection",
    "quarantined_selection_bias",
    "not_verified",
    "verified_against_committed_source",
    "reviewed_none_found",
}

DISPLAY_PRIORITIES = {"high", "medium", "low", "quarantine", "unknown"}


@dataclass(frozen=True)
class NumberFactCard:
    fact_uid: str
    source_entry_id: str
    source_record_path: str
    source_fact_path: str | None
    source_fact_id: str | None
    display_label: str
    short_label: str
    value: str | int | float | None
    values: list[str | int | float] = field(default_factory=list)
    value_type: str | None = "unknown"
    operation_type: str | None = "unknown"
    expression: str | None = None
    relation: str | None = None
    components: list[dict[str, Any]] = field(default_factory=list)
    why_stored: str | None = None
    source_paths: list[str] = field(default_factory=list)
    source_anchor: dict[str, Any] | None = None
    verification_status: str = "not_verified"
    review_state: str = "vague_fact_enrichment_needed"
    risk_notes: list[str] = field(default_factory=list)
    crosslinks: list[str] = field(default_factory=list)
    display_priority: str = "unknown"
    usable_for_decision_now: bool = False
    not_allowed_as: list[str] = field(default_factory=lambda: ["proof", "route_seed", "solve_claim"])
    raw_fact: dict[str, Any] = field(default_factory=dict)
    overlay_applied: bool = False
    overlay_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def needs_enrichment(self) -> bool:
        return self.review_state in {
            "vague_fact_enrichment_needed",
            "extracted_basic_fact",
            "canonical_verification_required",
        }


def load_enrichment_overlays(root: Path = OVERLAY_DIR) -> list[dict[str, Any]]:
    """Load live overlays and intentionally ignore templates/drafts."""
    overlays: list[dict[str, Any]] = []
    if not root.exists():
        return overlays
    for path in sorted(root.rglob("*.yaml")):
        rel = path.as_posix()
        if "/templates/" in rel.replace("\\", "/") or path.name.startswith("example"):
            continue
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(payload, dict):
            continue
        if payload.get("review_state") == "overlay_draft" or payload.get("template") is True:
            continue
        if isinstance(payload.get("overlays"), list):
            for item in payload["overlays"]:
                if not isinstance(item, dict):
                    continue
                if item.get("review_state") == "overlay_draft" or item.get("template") is True:
                    continue
                item = dict(item)
                item["_overlay_path"] = rel
                overlays.append(item)
            continue
        payload["_overlay_path"] = rel
        overlays.append(payload)
    return overlays


def normalize_entry_number_facts(
    entry: SourceBrowserEntry,
    overlays: list[dict[str, Any]] | None = None,
) -> list[NumberFactCard]:
    overlays = overlays if overlays is not None else load_enrichment_overlays()
    overlay_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for overlay in overlays:
        overlay_by_key[_overlay_key(overlay.get("source_record_path"), overlay.get("source_fact_id"))] = overlay
    consumed_overlay_ids: set[tuple[str, str, str]] = set()
    cards: list[NumberFactCard] = []
    for index, raw_fact in enumerate(entry.number_facts):
        source_fact_id = _source_fact_id(raw_fact)
        source_fact_path = str(raw_fact.get("source_fact_path") or f"number_facts[{index}]")
        overlay = overlay_by_key.get(_overlay_key(entry.source_record_path, source_fact_id))
        if overlay:
            consumed_overlay_ids.add(_overlay_identity(overlay))
        cards.append(_card_from_fact(entry, raw_fact, index, source_fact_id, source_fact_path, overlay))
    for index, overlay in enumerate(overlays):
        if str(overlay.get("source_record_path") or "") != entry.source_record_path:
            continue
        if _overlay_identity(overlay) in consumed_overlay_ids:
            continue
        cards.append(_card_from_overlay_only(entry, overlay, index))
    return sorted(cards, key=_card_sort_key)


def zero_fact_review_state(
    entry: SourceBrowserEntry,
    overlays: list[dict[str, Any]] | None = None,
) -> str:
    if entry.number_facts:
        return ""
    overlays = overlays if overlays is not None else load_enrichment_overlays()
    for overlay in overlays:
        if overlay.get("source_record_path") != entry.source_record_path:
            continue
        if overlay.get("review_state") == "zero_extracted_facts_reviewed_none_found":
            return "zero_extracted_facts_reviewed_none_found"
    return "zero_extracted_facts_not_reviewed"


def number_fact_table_display(
    entry: SourceBrowserEntry,
    overlays: list[dict[str, Any]] | None = None,
) -> str:
    cards = normalize_entry_number_facts(entry, overlays)
    if not cards:
        return "none found" if zero_fact_review_state(entry, overlays).endswith("reviewed_none_found") else "not reviewed"
    vague = sum(1 for card in cards if card.review_state == "vague_fact_enrichment_needed")
    if vague:
        return f"{len(cards)} facts / needs context"
    labels = [card.short_label for card in cards if card.short_label][:3]
    return "; ".join(labels) if labels else f"{len(cards)} facts"


def entry_matches_fact_filter(entry: SourceBrowserEntry, filter_id: str) -> bool:
    cards = normalize_entry_number_facts(entry)
    if filter_id == "needs_fact_enrichment":
        return any(card.needs_enrichment for card in cards)
    if filter_id == "not_reviewed_for_number_facts":
        return not cards and zero_fact_review_state(entry) == "zero_extracted_facts_not_reviewed"
    if filter_id == "has_rich_number_facts":
        return any(card.review_state in {"rich_fact_card", "overlay_enriched_fact"} for card in cards)
    if filter_id == "canonical_verification_required":
        return any(
            card.review_state == "canonical_verification_required"
            or card.verification_status
            in {"canonical_transcript_required", "canonical_image_required", "canonical_source_required"}
            for card in cards
        )
    if filter_id == "quarantined_number_facts":
        return any(card.review_state == "quarantined_fact" for card in cards)
    return True


def reviewability_counts(entries: list[SourceBrowserEntry]) -> dict[str, int]:
    counts = {
        "entries_with_extracted_number_facts": 0,
        "entries_with_zero_extracted_number_facts": 0,
        "entries_with_zero_extracted_number_facts_not_reviewed": 0,
        "entries_with_vague_number_facts": 0,
        "entries_with_rich_fact_cards": 0,
        "total_number_fact_cards_extracted": 0,
        "rich_fact_card_count": 0,
        "basic_fact_card_count": 0,
        "vague_fact_card_count": 0,
        "quarantined_fact_card_count": 0,
        "canonical_verification_required_count": 0,
    }
    for entry in entries:
        cards = normalize_entry_number_facts(entry)
        if cards:
            counts["entries_with_extracted_number_facts"] += 1
        else:
            counts["entries_with_zero_extracted_number_facts"] += 1
            if zero_fact_review_state(entry) == "zero_extracted_facts_not_reviewed":
                counts["entries_with_zero_extracted_number_facts_not_reviewed"] += 1
        counts["total_number_fact_cards_extracted"] += len(cards)
        if any(card.review_state == "vague_fact_enrichment_needed" for card in cards):
            counts["entries_with_vague_number_facts"] += 1
        if any(card.review_state in {"rich_fact_card", "overlay_enriched_fact"} for card in cards):
            counts["entries_with_rich_fact_cards"] += 1
        for card in cards:
            if card.review_state in {"rich_fact_card", "overlay_enriched_fact"}:
                counts["rich_fact_card_count"] += 1
            elif card.review_state == "extracted_basic_fact":
                counts["basic_fact_card_count"] += 1
            elif card.review_state == "vague_fact_enrichment_needed":
                counts["vague_fact_card_count"] += 1
            elif card.review_state == "quarantined_fact":
                counts["quarantined_fact_card_count"] += 1
            if card.review_state == "canonical_verification_required" or card.verification_status in {
                "canonical_transcript_required",
                "canonical_image_required",
                "canonical_source_required",
            }:
                counts["canonical_verification_required_count"] += 1
    return counts


def _card_from_fact(
    entry: SourceBrowserEntry,
    raw_fact: dict[str, Any],
    index: int,
    source_fact_id: str | None,
    source_fact_path: str,
    overlay: dict[str, Any] | None,
) -> NumberFactCard:
    merged = dict(raw_fact)
    if overlay:
        merged.update({key: value for key, value in overlay.items() if not key.startswith("_")})
    value = _first_value(merged, ("value", "result", "numeric_value", "claimed_value", "gp_sum"))
    values = _values(merged, value)
    review_state = _review_state(merged, overlay is not None)
    verification_status = _enum_value(
        str(merged.get("verification_status") or "not_verified"),
        VERIFICATION_STATUSES,
        "not_verified",
    )
    value_type = _enum_value(str(merged.get("value_type") or _guess_value_type(merged)), VALUE_TYPES, "unknown")
    operation_type = _enum_value(
        str(merged.get("operation_type") or _guess_operation_type(merged)),
        OPERATION_TYPES,
        "unknown",
    )
    display_label = _display_label(merged, source_fact_id, value)
    short_label = str(merged.get("short_label") or _short_label(display_label, value))
    fact_uid = _fact_uid(entry.source_record_path, source_fact_path, source_fact_id, value, merged)
    return NumberFactCard(
        fact_uid=fact_uid,
        source_entry_id=entry.entry_id,
        source_record_path=str(merged.get("source_record_path") or entry.source_record_path),
        source_fact_path=str(merged.get("source_fact_path") or source_fact_path),
        source_fact_id=source_fact_id,
        display_label=display_label,
        short_label=short_label,
        value=value,
        values=values,
        value_type=value_type,
        operation_type=operation_type,
        expression=_string_or_none(merged.get("expression")),
        relation=_string_or_none(merged.get("relation")),
        components=_list_of_dicts(merged.get("components")),
        why_stored=_string_or_none(merged.get("why_stored")),
        source_paths=_string_list(merged.get("source_paths")) or [entry.source_record_path],
        source_anchor=merged.get("source_anchor") if isinstance(merged.get("source_anchor"), dict) else None,
        verification_status=verification_status,
        review_state=review_state,
        risk_notes=_string_list(merged.get("risk_notes")),
        crosslinks=_string_list(merged.get("crosslinks") or merged.get("links_to")),
        display_priority=_enum_value(
            str(merged.get("display_priority") or "unknown"),
            DISPLAY_PRIORITIES,
            "unknown",
        ),
        usable_for_decision_now=bool(merged.get("usable_for_decision_now") is True),
        not_allowed_as=_string_list(merged.get("not_allowed_as")) or ["proof", "route_seed", "solve_claim"],
        raw_fact=raw_fact,
        overlay_applied=overlay is not None,
        overlay_path=str(overlay.get("_overlay_path")) if overlay else None,
    )


def _card_from_overlay_only(entry: SourceBrowserEntry, overlay: dict[str, Any], index: int) -> NumberFactCard:
    source_fact_id = str(overlay.get("source_fact_id") or overlay.get("overlay_id") or f"overlay_only_{index}")
    source_fact_path = str(overlay.get("source_fact_path") or f"overlay_only[{index}]")
    return _card_from_fact(entry, {}, index, source_fact_id, source_fact_path, overlay)


def _review_state(payload: dict[str, Any], overlay_applied: bool) -> str:
    explicit = payload.get("review_state")
    if isinstance(explicit, str) and explicit in REVIEW_STATES:
        return explicit
    if overlay_applied:
        return "overlay_enriched_fact"
    verification = str(payload.get("verification_status") or "")
    if verification.startswith("canonical_"):
        return "canonical_verification_required"
    if payload.get("display_priority") == "quarantine" or "quarantine" in verification:
        return "quarantined_fact"
    rich_keys = {"display_label", "value_type", "operation_type", "why_stored", "relation"}
    if rich_keys <= set(payload):
        return "rich_fact_card"
    useful_keys = {"expression", "result", "gp_sum", "factorization", "components", "relation"}
    if useful_keys & set(payload):
        return "extracted_basic_fact"
    return "vague_fact_enrichment_needed"


def _source_fact_id(raw_fact: dict[str, Any]) -> str | None:
    for key in ("source_fact_id", "fact_id", "claim_id", "id"):
        value = raw_fact.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _overlay_key(source_record_path: Any, source_fact_id: Any) -> tuple[str, str]:
    return (str(source_record_path or ""), str(source_fact_id or ""))


def _overlay_identity(overlay: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(overlay.get("source_record_path") or ""),
        str(overlay.get("source_fact_id") or ""),
        str(overlay.get("overlay_id") or ""),
    )


def _first_value(payload: dict[str, Any], keys: tuple[str, ...]) -> str | int | float | None:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str | int | float):
            return value
    return None


def _values(payload: dict[str, Any], value: str | int | float | None) -> list[str | int | float]:
    raw_values = payload.get("values")
    if isinstance(raw_values, list):
        return [item for item in raw_values if isinstance(item, str | int | float)]
    return [] if value is None else [value]


def _display_label(
    payload: dict[str, Any],
    source_fact_id: str | None,
    value: str | int | float | None,
) -> str:
    for key in ("display_label", "label", "relation", "expression", "claim_id"):
        value_text = payload.get(key)
        if isinstance(value_text, str) and value_text:
            return value_text.replace("_", " ")
    if source_fact_id:
        return source_fact_id.replace("_", " ")
    return f"Number fact {value}" if value is not None else "Number fact needing context"


def _short_label(label: str, value: str | int | float | None) -> str:
    if value is not None:
        return str(value)
    return label[:32]


def _guess_value_type(payload: dict[str, Any]) -> str:
    keys = " ".join(payload.keys()).lower()
    if "gp" in keys:
        return "gp_sum"
    if "prime" in keys:
        return "prime"
    if "hash" in keys:
        return "hash_value"
    if "coordinate" in keys or "pixel" in keys:
        return "coordinate"
    if "count" in keys or "rune" in keys:
        return "rune_count"
    return "unknown"


def _guess_operation_type(payload: dict[str, Any]) -> str:
    keys = " ".join(payload.keys()).lower()
    if "gp" in keys:
        return "gp_sum"
    if "factor" in keys:
        return "factorization"
    if "prime" in keys:
        return "prime_index_lookup"
    if "hash" in keys:
        return "hash_contract"
    if "claim" in keys:
        return "source_observation"
    return "unknown"


def _fact_uid(
    source_record_path: str,
    source_fact_path: str,
    source_fact_id: str | None,
    value: str | int | float | None,
    payload: dict[str, Any],
) -> str:
    basis = "|".join(
        [
            source_record_path,
            source_fact_path,
            source_fact_id or "",
            "" if value is None else str(value),
            str(payload.get("expression") or ""),
        ]
    )
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str | int | float)]


def _list_of_dicts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _enum_value(value: str, allowed: set[str], fallback: str) -> str:
    return value if value in allowed else fallback


def _card_sort_key(card: NumberFactCard) -> tuple[int, str, str]:
    priority = {
        "overlay_enriched_fact": 0,
        "rich_fact_card": 1,
        "extracted_basic_fact": 2,
        "canonical_verification_required": 3,
        "vague_fact_enrichment_needed": 4,
        "quarantined_fact": 5,
    }.get(card.review_state, 9)
    return (priority, card.display_label, card.fact_uid)
