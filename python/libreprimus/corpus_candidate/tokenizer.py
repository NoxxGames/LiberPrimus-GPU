"""Tokenizer for Stage 0E corpus candidate generation."""

from __future__ import annotations

from collections import Counter
import hashlib

from libreprimus.corpus_candidate.models import CorpusGenerationWarning, CorpusLineRecord, CorpusTokenRecord
from libreprimus.profiles.gematria_profile import GematriaProfile
from libreprimus.profiles.glyph_variant_profile import GlyphVariantProfile
from libreprimus.profiles.separator_grammar import SeparatorGrammar

SOURCE_ID = "rtkd-master-transcription"
CORPUS_CANDIDATE_ID = "rtkd-master-v0-candidate"


def _is_rune(char: str) -> bool:
    return "\u16a0" <= char <= "\u16ff"


def _line_signature(tokens: list[CorpusTokenRecord]) -> str:
    payload = "|".join(token.raw_text for token in tokens)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _warning(code: str, line: int | None, column: int | None, message: str, context: str) -> CorpusGenerationWarning:
    return CorpusGenerationWarning(
        record_type="corpus_generation_warning",
        corpus_candidate_id=CORPUS_CANDIDATE_ID,
        warning_code=code,
        severity="warning",
        source_line=line,
        source_column=column,
        message=message,
        raw_context=context,
        trusted_as_canonical=False,
    )


class CorpusTokenizer:
    """Preserve transcript characters as typed corpus candidate tokens."""

    def __init__(
        self,
        *,
        gematria: GematriaProfile,
        variants: GlyphVariantProfile,
        separators: SeparatorGrammar,
        source_sha256: str,
    ) -> None:
        self.gematria = gematria
        self.variants = variants
        self.separators = separators
        self.source_sha256 = source_sha256
        self._glyph_to_entry = gematria.rune_to_entry
        self._variant_by_glyph = variants.observed_to_variant
        self._separator_by_glyph = separators.by_glyph

    def tokenize(self, text: str) -> tuple[list[CorpusTokenRecord], list[CorpusLineRecord], list[CorpusGenerationWarning]]:
        tokens: list[CorpusTokenRecord] = []
        warnings: list[CorpusGenerationWarning] = []
        logical_line_index = 0
        token_index_in_line = 0
        current_line_tokens: list[CorpusTokenRecord] = []
        lines: list[CorpusLineRecord] = []

        def emit_line() -> None:
            nonlocal logical_line_index, token_index_in_line, current_line_tokens
            if not current_line_tokens:
                return
            physical_lines = [token.physical_line_number for token in current_line_tokens if token.token_kind != "physical_newline"]
            if not physical_lines:
                physical_lines = [current_line_tokens[0].physical_line_number]
            rune_tokens = [token for token in current_line_tokens if token.token_kind == "rune"]
            separator_counts = Counter(token.separator_class for token in current_line_tokens if token.separator_class)
            lines.append(
                CorpusLineRecord(
                    record_type="corpus_line",
                    corpus_candidate_id=CORPUS_CANDIDATE_ID,
                    source_id=SOURCE_ID,
                    source_sha256=self.source_sha256,
                    physical_line_number_start=min(physical_lines),
                    physical_line_number_end=max(physical_lines),
                    logical_line_index=logical_line_index,
                    raw_text="".join(token.raw_text for token in current_line_tokens if token.token_kind != "physical_newline"),
                    token_count=len(current_line_tokens),
                    rune_count=len(rune_tokens),
                    separator_counts=dict(sorted(separator_counts.items())),
                    rune_indices=[token.index29 for token in rune_tokens if token.index29 is not None],
                    prime_values=[token.prime_value for token in rune_tokens if token.prime_value is not None],
                    line_signature_sha256=_line_signature(current_line_tokens),
                    page_candidate_ids=[],
                    trusted_as_canonical=False,
                    warnings=[warning.message for warning in warnings if warning.source_line in physical_lines],
                )
            )
            logical_line_index += 1
            token_index_in_line = 0
            current_line_tokens = []

        def add_token(
            *,
            physical_line_number: int,
            raw_text: str,
            token_kind: str,
            source_column_start: int | None,
            source_column_end: int | None,
            raw_glyph: str | None = None,
            normalized_glyph: str | None = None,
            index29: int | None = None,
            prime_value: int | None = None,
            latin_label: str | None = None,
            variant_mapping_applied: bool = False,
            variant_source: str | None = None,
            separator_class: str | None = None,
            token_warnings: list[str] | None = None,
        ) -> CorpusTokenRecord:
            nonlocal token_index_in_line
            token = CorpusTokenRecord(
                record_type="corpus_token",
                corpus_candidate_id=CORPUS_CANDIDATE_ID,
                source_id=SOURCE_ID,
                source_sha256=self.source_sha256,
                physical_line_number=physical_line_number,
                logical_line_index=logical_line_index,
                token_index_global=len(tokens),
                token_index_in_line=token_index_in_line,
                raw_text=raw_text,
                token_kind=token_kind,
                raw_glyph=raw_glyph,
                normalized_glyph=normalized_glyph,
                index29=index29,
                prime_value=prime_value,
                latin_label=latin_label,
                variant_mapping_applied=variant_mapping_applied,
                variant_source=variant_source,
                separator_class=separator_class,
                source_column_start=source_column_start,
                source_column_end=source_column_end,
                page_candidate_ids=[],
                trusted_as_canonical=False,
                warnings=token_warnings or [],
            )
            tokens.append(token)
            current_line_tokens.append(token)
            token_index_in_line += 1
            return token

        physical_lines = text.splitlines()
        for physical_line_number, raw_line in enumerate(physical_lines, start=1):
            column = 1
            while column <= len(raw_line):
                char = raw_line[column - 1]
                if _is_rune(char):
                    entry = self._glyph_to_entry.get(char)
                    variant = self._variant_by_glyph.get(char)
                    token_warnings: list[str] = []
                    if entry is not None:
                        normalized = char
                        index29 = entry.index
                        prime = entry.prime
                        label = entry.preferred_latin_label
                        variant_applied = False
                        variant_source = None
                    elif variant is not None:
                        normalized = variant.normalized_rune_candidate
                        entry = self._glyph_to_entry[normalized]
                        index29 = entry.index
                        prime = entry.prime
                        label = entry.preferred_latin_label
                        variant_applied = True
                        variant_source = self.variants.profile_id
                        token_warnings.append("Documented glyph variant normalized view applied.")
                    else:
                        normalized = None
                        index29 = None
                        prime = None
                        label = None
                        variant_applied = False
                        variant_source = None
                        msg = f"Unknown rune glyph {char!r} preserved."
                        token_warnings.append(msg)
                        warnings.append(_warning("unknown_rune_glyph", physical_line_number, column, msg, char))
                    add_token(
                        physical_line_number=physical_line_number,
                        raw_text=char,
                        token_kind="rune",
                        raw_glyph=char,
                        normalized_glyph=normalized,
                        index29=index29,
                        prime_value=prime,
                        latin_label=label,
                        variant_mapping_applied=variant_applied,
                        variant_source=variant_source,
                        source_column_start=column,
                        source_column_end=column,
                        token_warnings=token_warnings,
                    )
                    column += 1
                    continue

                separator = self._separator_by_glyph.get(char)
                if separator is not None:
                    add_token(
                        physical_line_number=physical_line_number,
                        raw_text=char,
                        token_kind=separator.token_kind,
                        separator_class=separator.class_id,
                        source_column_start=column,
                        source_column_end=column,
                    )
                    column += 1
                    if separator.token_kind == "line_separator":
                        emit_line()
                    continue

                if char.isdigit():
                    start = column
                    while column <= len(raw_line) and raw_line[column - 1].isdigit():
                        column += 1
                    add_token(
                        physical_line_number=physical_line_number,
                        raw_text=raw_line[start - 1 : column - 1],
                        token_kind="numeric_literal",
                        separator_class="numeric_literal",
                        source_column_start=start,
                        source_column_end=column - 1,
                    )
                    continue

                if char.isspace():
                    add_token(
                        physical_line_number=physical_line_number,
                        raw_text=char,
                        token_kind="whitespace",
                        separator_class="whitespace",
                        source_column_start=column,
                        source_column_end=column,
                    )
                    column += 1
                    continue

                msg = f"Unknown symbol {char!r} preserved."
                warnings.append(_warning("unknown_symbol", physical_line_number, column, msg, char))
                add_token(
                    physical_line_number=physical_line_number,
                    raw_text=char,
                    token_kind="unknown_symbol",
                    separator_class="unknown_symbol",
                    source_column_start=column,
                    source_column_end=column,
                    token_warnings=[msg],
                )
                column += 1
            add_token(
                physical_line_number=physical_line_number,
                raw_text="\n",
                token_kind="physical_newline",
                separator_class="newline",
                source_column_start=None,
                source_column_end=None,
            )
            emit_line()
        return tokens, lines, warnings
