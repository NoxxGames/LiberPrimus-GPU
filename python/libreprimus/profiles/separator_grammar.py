"""Separator grammar profile helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from libreprimus.profiles.gematria_profile import ProfileValidationResult, compute_sha256, load_json

SEPARATOR_GRAMMAR_ID = "rtkd-separator-grammar-v0"
REQUIRED_SEPARATOR_CLASSES = {
    "word_separator",
    "clause_separator",
    "paragraph_separator",
    "segment_separator",
    "chapter_separator",
    "line_separator",
    "page_separator_or_marker",
    "whitespace",
    "newline",
    "numeric_literal",
    "hex_literal_candidate",
    "unknown_symbol",
}


@dataclass(frozen=True)
class SeparatorClass:
    class_id: str
    token_kind: str
    glyphs: list[str]
    preserve: bool
    preserve_raw: bool
    canonical_page_boundary: bool | None
    requires_warning: bool


@dataclass(frozen=True)
class SeparatorGrammar:
    profile_id: str
    status: str
    canonical_profile_active: bool
    canonical_corpus_active: bool
    source_id: str
    separator_classes: list[SeparatorClass]
    sha256: str

    @property
    def by_glyph(self) -> dict[str, SeparatorClass]:
        mapping: dict[str, SeparatorClass] = {}
        for separator in self.separator_classes:
            for glyph in separator.glyphs:
                mapping[glyph] = separator
        return mapping

    @property
    def by_class_id(self) -> dict[str, SeparatorClass]:
        return {separator.class_id: separator for separator in self.separator_classes}


def load_separator_grammar(path: Path) -> SeparatorGrammar:
    payload = load_json(path)
    classes = []
    for item in payload.get("separator_classes", []):
        classes.append(
            SeparatorClass(
                class_id=str(item["class_id"]),
                token_kind=str(item["token_kind"]),
                glyphs=[str(glyph) for glyph in item.get("glyphs", [])],
                preserve=bool(item.get("preserve", False)),
                preserve_raw=bool(item.get("preserve_raw", False)),
                canonical_page_boundary=item.get("canonical_page_boundary"),
                requires_warning=bool(item.get("requires_warning", False)),
            )
        )
    return SeparatorGrammar(
        profile_id=str(payload["profile_id"]),
        status=str(payload["status"]),
        canonical_profile_active=bool(payload["canonical_profile_active"]),
        canonical_corpus_active=bool(payload["canonical_corpus_active"]),
        source_id=str(payload["source_id"]),
        separator_classes=classes,
        sha256=compute_sha256(path),
    )


def validate_separator_grammar(grammar: SeparatorGrammar) -> ProfileValidationResult:
    errors: list[str] = []
    class_ids = set(grammar.by_class_id)
    if grammar.profile_id != SEPARATOR_GRAMMAR_ID:
        errors.append("Unexpected separator grammar id.")
    if grammar.status != "frozen_profile":
        errors.append("Separator grammar status must be frozen_profile.")
    if grammar.canonical_profile_active is not True:
        errors.append("Separator grammar must have canonical_profile_active=true.")
    if grammar.canonical_corpus_active is not False:
        errors.append("Separator grammar must have canonical_corpus_active=false.")
    missing = REQUIRED_SEPARATOR_CLASSES - class_ids
    if missing:
        errors.append(f"Missing separator classes: {sorted(missing)}.")
    required_glyphs = {
        "word_separator": "-",
        "clause_separator": ".",
        "paragraph_separator": "&",
        "segment_separator": "$",
        "chapter_separator": "\u00a7",
        "line_separator": "/",
        "page_separator_or_marker": "%",
    }
    for class_id, glyph in required_glyphs.items():
        separator = grammar.by_class_id.get(class_id)
        if separator is None or glyph not in separator.glyphs:
            errors.append(f"Missing required glyph {glyph!r} for {class_id}.")
    page_separator = grammar.by_class_id.get("page_separator_or_marker")
    if page_separator is not None and page_separator.canonical_page_boundary is not False:
        errors.append("% must not imply canonical page boundary.")
    return ProfileValidationResult(valid=not errors, errors=errors, warnings=[])
