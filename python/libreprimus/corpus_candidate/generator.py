"""Stage 0E rtkd master corpus candidate generator."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import json
import subprocess
from pathlib import Path
from time import perf_counter
from typing import Any

from libreprimus.corpus_candidate.models import (
    CorpusCandidateManifest,
    CorpusCandidateSummary,
    CorpusGenerationWarning,
    CorpusPageCandidateRecord,
)
from libreprimus.corpus_candidate.separator_inventory import observed_separator_inventory
from libreprimus.corpus_candidate.tokenizer import CORPUS_CANDIDATE_ID, SOURCE_ID, CorpusTokenizer
from libreprimus.profiles.gematria_profile import assert_gematria_profile_valid, compute_sha256
from libreprimus.profiles.glyph_variant_profile import load_glyph_variant_profile, validate_glyph_variant_profile
from libreprimus.profiles.separator_grammar import load_separator_grammar, validate_separator_grammar

GENERATOR_VERSION = "stage0e-v0"


def _git_commit() -> str:
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return result.stdout.strip()


def _load_boundary_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.is_file():
        return records
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def _confidence_score(confidence: str) -> float:
    return {"high": 0.9, "exact": 1.0, "medium": 0.6, "low": 0.3, "none": 0.0}.get(confidence, 0.0)


def _page_candidates(
    boundary_records: list[dict[str, Any]],
    tokens_by_line: dict[int, list[int]],
) -> tuple[list[CorpusPageCandidateRecord], list[CorpusGenerationWarning]]:
    page_candidates: list[CorpusPageCandidateRecord] = []
    warnings: list[CorpusGenerationWarning] = []
    if not boundary_records:
        warnings.append(
            CorpusGenerationWarning(
                record_type="corpus_generation_warning",
                corpus_candidate_id=CORPUS_CANDIDATE_ID,
                warning_code="page_candidates_absent",
                severity="warning",
                source_line=None,
                source_column=None,
                message="Stage 0D-followup page boundary candidates were absent; generated corpus candidate without page candidates.",
                raw_context="",
                trusted_as_canonical=False,
            )
        )
        return page_candidates, warnings
    if len(boundary_records) > 58:
        warnings.append(
            CorpusGenerationWarning(
                record_type="corpus_generation_warning",
                corpus_candidate_id=CORPUS_CANDIDATE_ID,
                warning_code="page_candidate_overgeneration",
                severity="warning",
                source_line=None,
                source_column=None,
                message="Page candidate count exceeds expected LP2 page count; review required.",
                raw_context=str(len(boundary_records)),
                trusted_as_canonical=False,
            )
        )
    for index, record in enumerate(boundary_records):
        start_line = record.get("start_transcript_line")
        end_line = record.get("end_transcript_line")
        token_indices: list[int] = []
        if isinstance(start_line, int) and isinstance(end_line, int):
            for line_number in range(start_line, end_line + 1):
                token_indices.extend(tokens_by_line.get(line_number, []))
        candidate_id = f"page-candidate-{index:03d}"
        page_candidates.append(
            CorpusPageCandidateRecord(
                record_type="corpus_page_candidate",
                corpus_candidate_id=CORPUS_CANDIDATE_ID,
                candidate_page_id=candidate_id,
                candidate_page_label=record.get("candidate_page_label"),
                candidate_local_page_index=record.get("candidate_local_page_index"),
                candidate_global_page_index=None,
                source="stage0d_followup_page_boundary_candidate",
                confidence=str(record.get("confidence", "none")),
                confidence_score=_confidence_score(str(record.get("confidence", "none"))),
                evidence=[str(item) for item in record.get("evidence", [])],
                start_token_index=min(token_indices) if token_indices else None,
                end_token_index=max(token_indices) if token_indices else None,
                start_logical_line_index=None,
                end_logical_line_index=None,
                start_physical_line_number=start_line if isinstance(start_line, int) else None,
                end_physical_line_number=end_line if isinstance(end_line, int) else None,
                canonical_page_boundary=False,
                page_boundaries_final=False,
                trusted_as_canonical=False,
                warnings=[str(item) for item in record.get("warnings", [])],
            )
        )
    return page_candidates, warnings


def build_rtkd_corpus_candidate(
    *,
    transcript_path: Path,
    gematria_path: Path,
    glyph_variants_path: Path,
    separators_path: Path,
    alignment_dir: Path | None = None,
) -> dict[str, Any]:
    """Build in-memory Stage 0E corpus candidate records."""
    elapsed: dict[str, float] = {}
    start = perf_counter()
    gematria = assert_gematria_profile_valid(gematria_path)
    variants = load_glyph_variant_profile(glyph_variants_path)
    variant_validation = validate_glyph_variant_profile(variants, gematria)
    if not variant_validation.valid:
        raise ValueError("; ".join(variant_validation.errors))
    separators = load_separator_grammar(separators_path)
    separator_validation = validate_separator_grammar(separators)
    if not separator_validation.valid:
        raise ValueError("; ".join(separator_validation.errors))
    elapsed["profile_validation"] = (perf_counter() - start) * 1000

    start = perf_counter()
    source_sha256 = compute_sha256(transcript_path)
    text = transcript_path.read_text(encoding="utf-8-sig")
    tokenizer = CorpusTokenizer(gematria=gematria, variants=variants, separators=separators, source_sha256=source_sha256)
    tokens, lines, warnings = tokenizer.tokenize(text)
    elapsed["tokenization"] = (perf_counter() - start) * 1000

    start = perf_counter()
    tokens_by_line: dict[int, list[int]] = {}
    for token in tokens:
        tokens_by_line.setdefault(token.physical_line_number, []).append(token.token_index_global)
    boundary_path = (alignment_dir / "page_boundary_candidates.jsonl") if alignment_dir is not None else Path()
    boundary_records = _load_boundary_jsonl(boundary_path)
    page_candidates, page_warnings = _page_candidates(boundary_records, tokens_by_line)
    warnings.extend(page_warnings)
    elapsed["page_candidate_integration"] = (perf_counter() - start) * 1000

    start = perf_counter()
    inventory = observed_separator_inventory(transcript_path, separators)
    elapsed["separator_inventory"] = (perf_counter() - start) * 1000

    token_kind_counts = Counter(token.token_kind for token in tokens)
    separator_token_count = sum(
        count
        for kind, count in token_kind_counts.items()
        if kind.endswith("_separator") or kind in {"page_separator_or_marker", "physical_newline", "whitespace"}
    )
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = CorpusCandidateManifest(
        record_type="corpus_candidate_manifest",
        corpus_candidate_id=CORPUS_CANDIDATE_ID,
        source_transcript_id=SOURCE_ID,
        source_transcript_sha256=source_sha256,
        source_transcript_local_path=str(transcript_path.as_posix()),
        gematria_profile_id=gematria.profile_id,
        gematria_profile_sha256=gematria.sha256,
        separator_grammar_id=separators.profile_id,
        separator_grammar_sha256=separators.sha256,
        glyph_variant_profile_id=variants.profile_id,
        glyph_variant_profile_sha256=variants.sha256,
        generated_at_utc=now,
        git_commit=_git_commit(),
        generator_version=GENERATOR_VERSION,
        canonical_corpus_candidate=True,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        line_count=len(lines),
        token_count=len(tokens),
        rune_token_count=token_kind_counts["rune"],
        separator_token_count=separator_token_count,
        unknown_symbol_count=token_kind_counts["unknown_symbol"],
        warning_count=len(warnings),
        page_candidate_count=len(page_candidates),
        notes=[
            "Generated Stage 0E corpus candidate only.",
            "Canonical corpus is not active.",
            "Page boundaries remain reviewable and non-final.",
        ],
    )
    summary = CorpusCandidateSummary(
        record_type="corpus_candidate_summary",
        corpus_candidate_id=CORPUS_CANDIDATE_ID,
        physical_line_count=len(text.splitlines()),
        logical_line_count=len(lines),
        token_count=len(tokens),
        rune_token_count=token_kind_counts["rune"],
        separator_token_count=separator_token_count,
        numeric_literal_count=token_kind_counts["numeric_literal"],
        unknown_symbol_count=token_kind_counts["unknown_symbol"],
        variant_mapped_token_count=sum(1 for token in tokens if token.variant_mapping_applied),
        page_candidate_count=len(page_candidates),
        warning_count=len(warnings),
        canonical_corpus_candidate=True,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        elapsed_milliseconds={key: round(value, 3) for key, value in elapsed.items()},
    )
    return {
        "manifest": manifest,
        "tokens": tokens,
        "lines": lines,
        "page_candidates": page_candidates,
        "warnings": warnings,
        "separator_inventory": inventory,
        "summary": summary,
    }
