"""Solved-page fixture reproduction pipeline."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import subprocess
from pathlib import Path
from time import perf_counter

from libreprimus.solved_fixtures.direct_translation import decode_direct_translation
from libreprimus.solved_fixtures.fixture_loader import load_fixtures
from libreprimus.solved_fixtures.models import ReproductionRecord, ReproductionSummary
from libreprimus.solved_fixtures.span_selection import select_tokens

FIXTURE_SET_ID = "direct-translation-v0"


def _git_commit() -> str:
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return result.stdout.strip()


def reproduce_direct_translation_fixtures(
    *,
    fixture_dir: Path,
    candidate_dir: Path,
) -> tuple[list[ReproductionRecord], ReproductionSummary, list[str]]:
    start = perf_counter()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    git_commit = _git_commit()
    fixtures = load_fixtures(fixture_dir)
    records: list[ReproductionRecord] = []
    warnings: list[str] = []
    for fixture in fixtures:
        decoded_text: str | None = None
        decoded_hash: str | None = None
        mismatch_reason: str | None = None
        rune_count = 0
        numeric_literal_count = 0
        separator_count = 0
        record_warnings: list[str] = []
        if fixture.method_family != "direct_translation" or not fixture.in_scope_for_stage:
            status = "pending" if fixture.method_status.startswith("pending") else "skipped"
            mismatch_reason = fixture.method_status
        else:
            tokens, selection_error = select_tokens(candidate_dir, fixture.span_selector)
            if selection_error is not None:
                status = "skipped"
                mismatch_reason = selection_error
            else:
                result = decode_direct_translation(tokens)
                decoded_text = result["decoded_normalized_plaintext"]
                decoded_hash = result["decoded_normalized_plaintext_sha256"]
                rune_count = int(result["rune_count"])
                numeric_literal_count = int(result["numeric_literal_count"])
                separator_count = int(result["separator_count"])
                record_warnings = [str(item) for item in result["warnings"]]
                if fixture.expected_normalized_plaintext_sha256 is None:
                    status = "pending"
                    mismatch_reason = "fixture has no expected hash"
                elif decoded_hash == fixture.expected_normalized_plaintext_sha256:
                    status = "pass"
                else:
                    status = "fail"
                    mismatch_reason = "decoded plaintext SHA-256 did not match fixture expectation"
        if record_warnings:
            warnings.extend(f"{fixture.fixture_id}: {warning}" for warning in record_warnings)
        records.append(
            ReproductionRecord(
                record_type="solved_page_reproduction_record",
                fixture_id=fixture.fixture_id,
                corpus_candidate_id=fixture.corpus_candidate_id,
                generated_at_utc=now,
                git_commit=git_commit,
                method_family=fixture.method_family,
                transform_chain=fixture.transform_chain,
                span_selector=fixture.span_selector,
                decoded_normalized_plaintext=decoded_text,
                decoded_normalized_plaintext_sha256=decoded_hash,
                expected_normalized_plaintext_sha256=fixture.expected_normalized_plaintext_sha256,
                match_status=status,
                mismatch_reason=mismatch_reason,
                rune_count=rune_count,
                numeric_literal_count=numeric_literal_count,
                separator_count=separator_count,
                warnings=record_warnings,
                trusted_as_canonical=False,
                canonical_corpus_active=False,
                page_boundaries_final=False,
            )
        )
    counts = Counter(record.match_status for record in records)
    summary = ReproductionSummary(
        record_type="solved_page_reproduction_summary",
        fixture_set_id=FIXTURE_SET_ID,
        generated_at_utc=now,
        git_commit=git_commit,
        fixture_count=len(records),
        pass_count=counts["pass"],
        fail_count=counts["fail"],
        pending_count=counts["pending"],
        skipped_count=counts["skipped"],
        direct_translation_pass_count=sum(
            1 for record in records if record.method_family == "direct_translation" and record.match_status == "pass"
        ),
        direct_translation_fail_count=sum(
            1 for record in records if record.method_family == "direct_translation" and record.match_status == "fail"
        ),
        canonical_corpus_active=False,
        page_boundaries_final=False,
        warnings=warnings,
        elapsed_ms=round((perf_counter() - start) * 1000, 3),
    )
    return records, summary, warnings
